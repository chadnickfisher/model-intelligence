"""Select structurally valid independent proposals without certifying public evidence.

Raw research and its accounting remain immutable. Selection rebuilds profiles
from the frozen baseline, records deferrals privately, then runs the unchanged
strict compiler on the derived packet. No catalog application or publication.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
import ipaddress
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, parse_qsl, unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import research_batch as batch
from tools.knowledge import record_hash, scope_errors
from tools.research_reconcile import reconcile_sources, remap_refs
from tools.research_runs import required_fields, pending_check, state_hash, digest, row_errors
from tools.task_assessments import task_assessment_errors

COLLECTIONS = ('capabilities', 'performance_characteristics')
REFERENCE_FIELDS = {'model_id', 'model_ids', 'provider_id', 'task_id', 'task_ids', 'related_task_ids',
                    'evidence_ids', 'source_ids', 'supporting_evidence_ids', 'contradictory_evidence_ids',
                    'judgment_ids', 'access_ids', 'price_ids'}
CHECK_KEYS = {'domain_checks': ('model_id', 'domain'),
              'field_checks': ('model_id', 'domain', 'entity_type', 'entity_id', 'path', 'baseline_value_hash'),
              'task_decisions': ('model_id', 'task_id'), 'source_checks': ('model_id', 'category')}
MISSING = object()


def identity(row, keys):
    return tuple(row[k] for k in keys)


def reject_private_urls(value):
    """Private content anywhere in the packet stops intake, even in a bad proposal."""
    if isinstance(value, dict):
        for nested in value.values(): reject_private_urls(nested)
    elif isinstance(value, list):
        for nested in value: reject_private_urls(nested)
    elif isinstance(value, str):
        batch.require(not re.search(r'\bfile:/{1,3}', value, re.I), 'Private file reference in research packet')
        for match in re.finditer(r'https?://[^\s<>"{}]+', value, re.I):
            try:
                url = urlsplit(match.group().rstrip('.,);'))
                host = unquote(url.hostname or '').lower().rstrip('.')
                batch.require(not url.username and not url.password, 'Private credential URL in research packet')
                batch.require(host not in {'localhost'} and not host.endswith(('.local', '.localhost', '.internal')),
                              'Private source URL in research packet')
                try:
                    address = ipaddress.ip_address(host)
                except ValueError:
                    address = None
                batch.require(address is None or address.is_global, 'Private source address in research packet')
                batch.require(not any(k.lower() in {'token', 'access_token', 'sig', 'signature', 'api_key', 'key', 'authorization', 'credential'}
                                      or k.lower().startswith('x-amz-') for k, _ in parse_qsl(url.query)),
                              'Private signed/token URL in research packet')
            except ValueError as exc:
                if str(exc).startswith('Private'):
                    raise
                # Invalid public URI syntax is rejected by the per-proposal schema.


def preflight(packet, assignment, baseline, private_patterns=()):
    """Packet-wide trust/accounting/privacy failures cannot be deferred away."""
    batch.validate_schema(packet, 'research-batch.schema.json')
    batch.require(packet['assignment_id'] == assignment['assignment_id'], 'Wrong assignment')
    batch.require(packet['baseline_commit'] == assignment['baseline_commit'], 'Stale baseline')
    created = datetime.fromisoformat(packet['created_at'].replace('Z', '+00:00'))
    batch.require(created.tzinfo and created <= datetime.now(timezone.utc), 'Invalid/future packet date')
    seed, run = assignment['research_run'], packet['research_run']
    batch.require(all(run[k] == seed[k] for k in batch.RUN_KEYS), 'Assignment metadata/rubric/bounds changed')
    batch.require(state_hash(baseline) == seed['baseline_hash'], 'Frozen baseline hash differs')
    tasks = sorted((r for (k, _), r in baseline.items() if k == 'task'), key=lambda r: r['id'])
    batch.require(digest(tasks) == seed['rubric_hash'], 'Frozen task rubric differs')
    text = json.dumps(packet)
    batch.require(not any(p in text for p in private_patterns), 'Private content in research packet')
    batch.require(not re.search(r'(?i)(?:drive\.google\.com|docs\.google\.com|[A-Z]:\\\\Users\\\\|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,})', text), 'Private content in research packet')
    reject_private_urls(packet)
    seen = set()
    local_definitions = set()
    for c in packet['changes']:
        ident = c['record']['id']
        batch.require(isinstance(ident, str) and ident, 'Invalid proposal identity')
        key = c['kind'], ident
        batch.require(key not in seen, 'Duplicate changed record')
        seen.add(key)
        definitions = [ident]
        if c['kind'] == 'model':
            for name in COLLECTIONS:
                rows = c['record'].get(name)
                if isinstance(rows, list): definitions += [j.get('id') for j in rows if isinstance(j, dict)]
        for definition in definitions:
            if isinstance(definition, str) and definition.startswith('new:'):
                batch.require(definition not in local_definitions, 'Ambiguous local definition')
                local_definitions.add(definition)
        old = baseline.get(key)
        batch.require(c['previous_hash'] == (record_hash(old) if old else None), 'Prior-record hash mismatch: ' + ident)
        public_text = json.dumps(c['record'])
        batch.require(not any(p in public_text for p in
                             (assignment['assignment_id'], seed['id'], '.local/', '.agents/', 'AGENTS.md', '.receipt.json')),
                      'Private operating material in public record')
    for name, keys in CHECK_KEYS.items():
        rows = [identity(r, keys) for r in run[name]]
        expected = {identity(r, keys) for r in seed[name]}
        batch.require(len(rows) == len(set(rows)) and expected <= set(rows), 'Original checklist omitted, duplicated or altered: ' + name)
        if name != 'field_checks':
            batch.require(set(rows) == expected, 'Original checklist scope changed: ' + name)
    batch.require(all(r['model_id'] in seed['target_model_ids'] for r in run['field_checks']), 'Field check outside assigned models')
    batch.require(all(r['result'] == 'not_checked' for r in run['domain_checks'] if r['model_id'] not in seed['target_model_ids']), 'Non-target domain scope changed')
    creators = [r['creator_id'] for r in packet['discovery_checks']]
    batch.require(len(creators) == len(set(creators)) and set(creators) == set(assignment['discovery_creator_ids']), 'Discovery creator accounting omitted/duplicated')
    for model_id in seed['target_model_ids']:
        searches = {(s['checked_at'], s['query']) for name in CHECK_KEYS for r in run[name]
                    if r['model_id'] == model_id for s in r['search_references']}
        batch.require(len(searches) <= run['bounds']['max_searches_per_model'], 'Declared search budget exceeded')
    discovery_searches = {(s['checked_at'], s['query']) for r in packet['discovery_checks'] for s in r['search_references']}
    batch.require(len(discovery_searches) <= assignment['max_discovery_searches'], 'Discovery search allowance exceeded')
    for rows in [*(run[name] for name in CHECK_KEYS), packet['discovery_checks']]:
        for row in rows:
            for search in row['search_references']:
                for url in search['urls']:
                    batch.public_url(url)
    return created


def changed_fields(before, after, path=''):
    """Lists stay atomic; independent judgments are handled by stable ID below."""
    if before == after:
        return
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) | set(after)):
            escaped = key.replace('~', '~0').replace('/', '~1')
            yield from changed_fields(before.get(key, MISSING), after.get(key, MISSING), path + '/' + escaped)
    else:
        yield path, after


def units_for(changes, baseline):
    result = []
    for c in changes:
        kind, record = c['kind'], c['record']
        old = baseline.get((kind, record['id']))
        parts = []
        if kind in {'model', 'provider'} and old:
            fields = sorted(set(old) | set(record))
            for field in fields:
                before, after = old.get(field, MISSING), record.get(field, MISSING)
                if before == after:
                    continue
                if kind == 'model' and field in COLLECTIONS and isinstance(before, list) and isinstance(after, list) and all(
                        isinstance(j, dict) and isinstance(j.get('id'), str) for j in before + after) and len({j['id'] for j in after}) == len(after):
                    prior, incoming = {j['id']: j for j in before}, {j['id']: j for j in after}
                    for ident in sorted(set(prior) | set(incoming)):
                        if prior.get(ident) != incoming.get(ident):
                            parts.append(('/' + field, ident, incoming.get(ident, MISSING)))
                else:
                    parts.extend((p, None, v) for p, v in changed_fields(before, after, '/' + field))
        else:
            parts = [('', None, record)]
        if not parts and record == old:
            parts = [('', None, record)]
        for path, finding_id, value in parts:
            scope = [kind, record['id'], path, finding_id]
            result.append({'id': 'unit-' + sha256(json.dumps(scope).encode()).hexdigest()[:20],
                           'kind': kind, 'record_id': record['id'], 'path': path, 'finding_id': finding_id,
                           'operation': 'remove' if value is MISSING else 'upsert',
                           'value': None if value is MISSING else deepcopy(value), 'change': c,
                           'dependencies': [], 'status': 'candidate', 'reason': None})
    return result


def put(record, unit):
    if unit['finding_id']:
        collection = unit['path'].lstrip('/')
        rows = record[collection]
        index = next((n for n, j in enumerate(rows) if j['id'] == unit['finding_id']), None)
        if unit['operation'] == 'remove':
            if index is not None: rows.pop(index)
        elif index is None:
            rows.append(deepcopy(unit['value']))
        else:
            rows[index] = deepcopy(unit['value'])
        return
    parts = [p.replace('~1', '/').replace('~0', '~') for p in unit['path'].split('/')[1:]]
    cursor = record
    for part in parts[:-1]:
        cursor = cursor[part]
    if unit['operation'] == 'remove':
        cursor.pop(parts[-1], None)
    else:
        cursor[parts[-1]] = deepcopy(unit['value'])


def refs(value, key=''):
    result = set()
    if isinstance(value, dict):
        for name, nested in value.items():
            if name != 'id': result |= refs(nested, name)
    elif isinstance(value, list):
        for nested in value: result |= refs(nested, key)
    elif isinstance(value, str) and key in REFERENCE_FIELDS:
        result.add(value)
    return result


def selected_change(unit, baseline, fields):
    change = deepcopy(unit['change'])
    if unit['path']:
        change['record'] = deepcopy(baseline[(unit['kind'], unit['record_id'])])
        put(change['record'], unit)
        row = fields.get((unit['kind'], unit['record_id'], unit['path']))
        if unit['finding_id'] and isinstance(unit['value'], dict):
            evidence = batch.evidence_ids(unit['value'])
            change['evidence_ids'] = sorted(evidence & set(change['evidence_ids']))
        elif row is not None:
            change['evidence_ids'] = sorted(set(row['evidence_ids']) & set(change['evidence_ids']))
    return change


def candidate_state(units, baseline):
    result = deepcopy(baseline)
    for unit in units:
        if unit['status'] != 'candidate': continue
        key = unit['kind'], unit['record_id']
        if unit['path']:
            put(result[key], unit)
        else:
            result[key] = deepcopy(unit['value'])
    return result


def defer(unit, reason, category='proposal_inconsistent'):
    unit.update(status='deferred', reason=reason, category=category)


def close_dependencies(units):
    lookup = {u['id']: u for u in units}
    changed = True
    while changed:
        changed = False
        for unit in units:
            bad = [ident for ident in unit['dependencies'] if lookup[ident]['status'] == 'deferred']
            if unit['status'] == 'candidate' and bad:
                defer(unit, 'Depends on deferred proposal: ' + ', '.join(bad), 'dependency_deferred')
                changed = True


def public_refs_valid(change, state):
    record = change['record']
    known = {i for _, i in state}
    judgments = {j['id'] for (k, _), r in state.items() if k == 'model' for c in COLLECTIONS for j in r[c]}
    batch.require(refs(record) <= known | judgments, 'Unresolved record dependency')
    models = {i: r for (k, i), r in state.items() if k == 'model'}
    access = {i: r for (k, i), r in state.items() if k == 'access'}
    tasks = {i for (k, i) in state if k == 'task'}
    if change['kind'] == 'model':
        finding_ids = [j['id'] for c in COLLECTIONS for j in record[c]]
        batch.require(len(finding_ids) == len(set(finding_ids)), 'Duplicate finding identity')
        batch.require(not scope_errors(record, tasks), 'Invalid task/finding scope')
        for ident in record['access_ids']:
            batch.require(access[ident]['model_id'] == record['id'], 'Access route belongs to another model')
        for ident in record['price_ids']:
            batch.require(state[('price', ident)]['model_id'] == record['id'], 'Price belongs to another model')
    if change['kind'] == 'access':
        for ident in record['price_ids']:
            price = state[('price', ident)]
            batch.require((price['model_id'], price['provider_id']) == (record['model_id'], record['provider_id']), 'Price does not match exact route')
    if change['kind'] == 'benchmark':
        exact = {j['id'] for c in COLLECTIONS for j in models[record['model_id']][c]}
        batch.require(set(record['judgment_ids']) <= exact, 'Benchmark judgment belongs to another model')
    if change['kind'] == 'task_assessment':
        batch.require(not task_assessment_errors([record], models, tasks, access), 'Invalid task-assessment references')
    if change['kind'] == 'behavior':
        batch.require(record['supporting_evidence_ids'] or record['contradictory_evidence_ids'], 'Behavior needs supporting or contradictory evidence')
        batch.require(not record['fix']['summary'] or record['fix']['evidence_ids'], 'Fix claim needs evidence')


def project_packet(packet, units, state, baseline, mapping):
    """Derived checklist selects claims; it never rewrites original research accounting."""
    result = deepcopy(packet)
    result['changes'] = []
    grouped = {}
    fields = {(r['entity_type'], r['entity_id'], r['path']): r for r in packet['research_run']['field_checks']}
    for unit in units:
        if unit['status'] != 'candidate': continue
        key = unit['kind'], unit['record_id']
        c = selected_change(unit, baseline, fields)
        if key not in grouped:
            grouped[key] = c
        else:
            grouped[key]['evidence_ids'] = sorted(set(grouped[key]['evidence_ids']) | set(c['evidence_ids']))
        grouped[key]['record'] = deepcopy(state[key])
    result['changes'] = list(grouped.values())
    sources = {i: r for (k, i), r in state.items() if k == 'source'}
    observations = {i: r for (k, i), r in state.items() if k == 'observation'}
    fresh = lambda ident, checked: all(i in sources and checked and sources[i]['accessed_at'] >= checked
                                     for i in batch.expanded_sources([ident], observations))
    run = result['research_run']
    contract = baseline[('research_contract', run['contract_id'])]
    expected_fields = required_fields(baseline, run['target_model_ids'], contract, state)
    originals = {identity(r, CHECK_KEYS['field_checks']): r for r in run['field_checks']}
    run['field_checks'] = [deepcopy(originals.get(identity(r, CHECK_KEYS['field_checks']), pending_check(r))) for r in expected_fields]
    projected = []
    expected_identities = {identity(r, CHECK_KEYS['field_checks']) for r in expected_fields}
    for key in sorted(originals.keys() - expected_identities):
        projected.append({'collection': 'field_checks', 'identity': list(key), 'action': 'deferred_record_field',
                          'validation_errors': ['Field belongs to an unselected proposal; original accounting retained.']})
    selected_findings = {j['id'] for (k, _), r in state.items() if k == 'model' for j in r['capabilities']}
    deferred_findings = {u['finding_id'] for u in units if u['status'] == 'deferred' and u['finding_id']}
    deferred_paths = {(u['kind'], u['record_id'], u['path']) for u in units if u['status'] == 'deferred'}
    surviving_paths = {(u['kind'], u['record_id'], u['path']) for u in units if u['status'] == 'candidate'}
    for name in CHECK_KEYS:
        for index, row in enumerate(run[name]):
            if row['result'] == 'not_checked':
                errors = row_errors(name, row, run, state, sources=sources, observations=observations)
                if errors:
                    base = {k: row[k] for k in CHECK_KEYS[name]}
                    if name == 'task_decisions':
                        base.update(applicability='not_checked', judgment_ids=[], confidence_rationale='')
                    clean = pending_check(base)
                    clean['remaining_gaps'] = list(dict.fromkeys(row['remaining_gaps'] + ['Original pending row has inconsistent metadata; retained separately.']))
                    run[name][index] = clean
                    projected.append({'collection': name, 'identity': list(identity(row, CHECK_KEYS[name])),
                                      'action': 'pending_metadata_deferred', 'validation_errors': errors})
                continue
            evidence = [i for i in row['evidence_ids'] if fresh(i, row['checked_at'])]
            reset = not evidence and (bool(row['evidence_ids']) or not row['search_references'])
            if name == 'field_checks':
                pathkey = row['entity_type'], row['entity_id'], row['path']
                reset |= pathkey in deferred_paths and pathkey not in surviving_paths
                if row['result'] == 'value' and row['entity_type'] != 'inventory':
                    actual = state.get((row['entity_type'], row['entity_id']))
                    for part in row['path'].split('/')[1:]:
                        actual = actual.get(part.replace('~1', '/').replace('~0', '~')) if isinstance(actual, dict) else None
                    reset |= actual is None
            elif name == 'task_decisions':
                reset |= bool(set(row['judgment_ids']) & deferred_findings) or not set(row['judgment_ids']) <= selected_findings
            elif name == 'domain_checks':
                reset |= any(u['status'] == 'deferred' and [row['model_id'], row['domain']] in u.get('scopes', []) for u in units)
            elif name == 'source_checks' and row['result'] == 'checked':
                source_ids = batch.expanded_sources(evidence, observations)
                reset |= not any(sources[i]['source_type'] == row['category'].replace('_', '-') for i in source_ids)
            trial = deepcopy(row)
            trial['evidence_ids'] = evidence
            errors = row_errors(name, trial, run, state, sources=sources, observations=observations)
            reset |= bool(errors)
            if reset:
                keys = CHECK_KEYS[name]
                base = {k: row[k] for k in keys}
                if name == 'task_decisions':
                    base.update(applicability='not_checked', judgment_ids=[], confidence_rationale='')
                run[name][index] = pending_check(base)
                run[name][index]['remaining_gaps'] = ['Candidate selection deferred this check; original research accounting retained separately.']
                projected.append({'collection': name, 'identity': list(identity(row, keys)), 'action': 'pending_in_candidate',
                                  'validation_errors': errors})
            elif evidence != row['evidence_ids']:
                row['evidence_ids'] = evidence
                row['remaining_gaps'] = list(dict.fromkeys(row['remaining_gaps'] + ['Some proposed evidence is deferred in this candidate.']))
                projected.append({'collection': name, 'identity': list(identity(row, CHECK_KEYS[name])), 'action': 'evidence_subset'})
    discoveries = []
    for d in result['discoveries']:
        if set(d['evidence_ids']) <= set(sources) | set(observations):
            discoveries.append(d)
        else:
            projected.append({'collection': 'discoveries', 'identity': [d['kind'], d['name'], d['url']],
                              'action': 'discovery_deferred', 'validation_errors': ['Discovery depends on deferred evidence.']})
    result['discoveries'] = discoveries
    created = datetime.fromisoformat(packet['created_at'].replace('Z', '+00:00'))
    for index, row in enumerate(result['discovery_checks']):
        try:
            batch.validate_discovery_check(row, run, created, sources, observations)
        except (ValueError, KeyError, TypeError) as exc:
            result['discovery_checks'][index] = {'creator_id': row['creator_id'], 'result': 'not_checked',
                                               'checked_at': None, 'rationale': '', 'evidence_ids': [],
                                               'search_references': [], 'remaining_gaps': ['Discovery accounting deferred; original retained separately.'],
                                               'blocked_reason': None}
            projected.append({'collection': 'discovery_checks', 'identity': [row['creator_id']],
                              'action': 'discovery_check_deferred', 'validation_errors': [str(exc)]})
    result['source_groups'] = {k: v for k, v in result['source_groups'].items() if k in sources}
    inverse = {v: k for k, v in mapping.items()}
    result = remap_refs(result, inverse)
    result['source_groups'] = {inverse.get(k, k): v for k, v in result['source_groups'].items()}
    return result, projected


def compile_partial(packet, assignment, baseline, private_patterns=(), *, review_decisions=None):
    created = preflight(packet, assignment, baseline, private_patterns)
    normalized, reconciliation = reconcile_sources(packet, baseline, defer_conflicts=True)
    raw_units = units_for(normalized['changes'], baseline)
    mapping = {}
    allocation_errors = {('source', c['canonical_id']): c['reason'] for c in reconciliation['source_conflicts']}
    # Allocate source/record definitions separately; one broken new definition
    # cannot prevent unrelated definitions from receiving deterministic IDs.
    valid_sources = []
    for c in normalized['changes']:
        if c['kind'] in {'model', 'provider'}: continue
        try:
            if c['kind'] == 'source':
                batch.require(isinstance(c['record'].get('url'), str), 'Invalid source identity URL')
            allocated = batch.allocate([c], baseline)
            batch.require(not set(allocated) & set(mapping) and not set(allocated.values()) & set(mapping.values()), 'Duplicate allocation')
            mapping.update(allocated)
            if c['kind'] == 'source': valid_sources.append(c)
        except (ValueError, KeyError, TypeError) as exc:
            allocation_errors[(c['kind'], c['record']['id'])] = str(exc)
    for unit in raw_units:
        if not unit['finding_id'] or not unit['finding_id'].startswith('new:') or unit['operation'] == 'remove': continue
        shell = {'kind': 'model', 'record': {'id': unit['record_id'], 'capabilities': [], 'performance_characteristics': []}}
        shell['record'][unit['path'].lstrip('/')] = [unit['value']]
        try:
            allocated = batch.allocate(valid_sources + [shell], baseline)
            allocated = {k: v for k, v in allocated.items() if k not in mapping}
            batch.require(not set(allocated.values()) & set(mapping.values()), 'Duplicate finding allocation')
            mapping.update(allocated)
        except (ValueError, KeyError, TypeError) as exc:
            allocation_errors[('finding', unit['finding_id'])] = str(exc)
    normalized = remap_refs(normalized, mapping)
    normalized['source_groups'] = {mapping.get(k, k): v for k, v in normalized['source_groups'].items()}
    units = units_for(normalized['changes'], baseline)
    allocation_errors = {(k, mapping.get(i, i)): v for (k, i), v in allocation_errors.items()}
    run, seed = normalized['research_run'], assignment['research_run']
    fields = {(r['entity_type'], r['entity_id'], r['path']): r for r in run['field_checks']}
    decisions = {(r['model_id'], r['task_id']): r for r in run['task_decisions']}
    targets = set(seed['target_model_ids'])
    providers = {r['provider_id'] for (k, _), r in baseline.items() if k in {'access', 'price'} and r.get('model_id') in targets}
    definitions = {u['finding_id'] or u['record_id']: u['id'] for u in units if u['finding_id'] or not u['path']}
    for unit in units:
        scopes = {(r['model_id'], r['domain']) for r in run['field_checks']
                  if r['entity_type'] == unit['kind'] and r['entity_id'] == unit['record_id'] and
                  (not unit['path'] or r['path'] == unit['path'])}
        if not scopes and unit['kind'] == 'model':
            scopes = {(unit['record_id'], d) for d in baseline[('research_contract', seed['contract_id'])]['domains']}
        unit['scopes'] = [list(s) for s in sorted(scopes)]
    for unit in units:
        try:
            failure = allocation_errors.get((unit['kind'], unit['record_id'])) or allocation_errors.get(('finding', unit['finding_id']))
            batch.require(not failure, failure or '')
            c = selected_change(unit, baseline, fields)
            dependencies = refs(unit['value'], unit['path'].lstrip('/')) | set(c['evidence_ids'])
            unit['dependencies'] = sorted({definitions[i] for i in dependencies if i in definitions and definitions[i] != unit['id']})
            batch.validate_change(c, baseline, mapping, assignment, seed, targets, providers, created)
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            defer(unit, str(exc))
    for unit in units:
        if unit['kind'] == 'research_coverage' and isinstance(unit['value'], dict):
            scope = [unit['value'].get('model_id'), unit['value'].get('domain')]
            unit['dependencies'] = sorted(set(unit['dependencies']) | {u['id'] for u in units if u['id'] != unit['id'] and scope in u['scopes']})
    close_dependencies(units)
    state = candidate_state(units, baseline)
    sources = {i: r for (k, i), r in state.items() if k == 'source'}
    observations = {i: r for (k, i), r in state.items() if k == 'observation'}
    for unit in units:
        if unit['status'] == 'deferred': continue
        try:
            c = selected_change(unit, baseline, fields)
            batch.validate_support(c, baseline, sources, observations, seed, created)
            batch.validate_accounting(c, baseline, fields, decisions, run, sources, observations)
            batch.validate_confidence(c, sources, observations, normalized['source_groups'])
            public_refs_valid(c, state)
        except (ValueError, KeyError, TypeError, IndexError, StopIteration) as exc:
            defer(unit, str(exc))
    close_dependencies(units)
    # Projection can reveal malformed accounting, independently of record shape.
    if review_decisions is not None:
        candidates = {u['id'] for u in units if u['status'] == 'candidate'}
        batch.require(set(review_decisions) <= candidates, 'Review refers to a non-candidate unit')
        for unit in units:
            if unit['status'] != 'candidate': continue
            decision = review_decisions.get(unit['id'])
            batch.require(decision is None or decision['decision'] in {'accept', 'defer'}, 'Invalid review decision')
            if decision is None or decision['decision'] != 'accept':
                defer(unit, decision['rationale'] if decision else 'No validated evidence-review decision', 'evidence_review_deferred')
        close_dependencies(units)
    # Defer only units relying on such rows, then propagate their dependency edges.
    accounting_projection = []
    for _ in range(len(units) + 1):
        state = candidate_state(units, baseline)
        selected, projected = project_packet(normalized, units, state, baseline, mapping)
        accounting_projection = projected
        projected_run = remap_refs(selected['research_run'], mapping)
        projected_fields = {(r['entity_type'], r['entity_id'], r['path']): r for r in projected_run['field_checks']}
        projected_decisions = {(r['model_id'], r['task_id']): r for r in projected_run['task_decisions']}
        sources = {i: r for (k, i), r in state.items() if k == 'source'}
        changed = False
        for unit in units:
            if unit['status'] == 'deferred': continue
            try:
                c = selected_change(unit, baseline, projected_fields)
                batch.validate_accounting(c, baseline, projected_fields, projected_decisions, projected_run, sources, observations)
            except (ValueError, KeyError, TypeError, IndexError, StopIteration) as exc:
                defer(unit, str(exc), 'accounting_deferred')
                changed = True
        if not changed: break
        close_dependencies(units)
    else:
        raise ValueError('Candidate deferral did not converge')
    # No fallback to a weaker validator. Global final failures remain failures.
    compiled = batch.compile_batch(selected, assignment, baseline, private_patterns)
    report_units = [{k: deepcopy(v) for k, v in u.items() if k not in {'value', 'change'}} for u in units]
    original_rows = [r for name in CHECK_KEYS for r in packet['research_run'][name]
                     if r['model_id'] in assignment['research_run']['target_model_ids']]
    return {'status': 'structural_selection_valid_pending_evidence_review', 'compiled': compiled,
            'selected_packet': selected, 'units': report_units, 'reconciliation': reconciliation,
            'accounting_projection': accounting_projection, 'evidence_reviewed': False,
            'original_accounting_counts': {'pending': sum(r['result'] == 'not_checked' for r in original_rows),
                                           'blocked': sum(r['result'] == 'blocked' for r in original_rows)},
            'candidate_units': sum(u['status'] == 'candidate' for u in units),
            'deferred_units': sum(u['status'] == 'deferred' for u in units)}


def main():
    from tools.git_baselines import git_state
    from tools.research_intake import private_path, retain, run_lock
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--assignment', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--bytes', type=int, required=True)
    parser.add_argument('--stage', action='store_true')
    parser.add_argument('--private-patterns', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    packet_path = private_path(root, args.packet)
    raw = packet_path.read_bytes()
    batch.require(len(raw) == args.bytes and len(raw) <= batch.MAX_BYTES and sha256(raw).hexdigest() == args.sha256, 'Packet bytes/hash differ')
    packet, _ = batch.load_json(packet_path)
    assignment, _ = batch.load_json(private_path(root, args.assignment))
    patterns = batch.load_json(private_path(root, args.private_patterns))[0]['patterns'] if args.private_patterns else []
    result = compile_partial(packet, assignment, git_state(assignment['baseline_commit']), patterns)
    destination = private_path(root, args.destination)
    with run_lock(private_path(root, destination / 'selection.lock')):
        retain(destination, 'original.json', raw)
        selected_raw = (json.dumps(result.pop('selected_packet'), ensure_ascii=False, indent=2) + '\n').encode()
        retain(destination, 'selected.json', selected_raw)
        compiled = result.pop('compiled')
        result.update(original_sha256=args.sha256, selected_sha256=sha256(selected_raw).hexdigest(), completion=compiled['completion'])
        retain(destination, 'selection.json', (json.dumps(result, indent=2) + '\n').encode())
        if args.stage:
            batch.stage(root, compiled, assignment, args.sha256, destination / 'stage')
    print(json.dumps({k: result[k] for k in ('status', 'candidate_units', 'deferred_units', 'evidence_reviewed')}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.CalledProcessError):
        print('Partial selection failed; packet-wide trust and final validation remain required.', file=sys.stderr)
        sys.exit(1)
