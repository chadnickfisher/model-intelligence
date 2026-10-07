"""Scoped maintenance accounting. No network, scheduling, inference or publication."""
from copy import deepcopy
from datetime import date
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.knowledge import ROOT, canonical, read, integrity_errors
from tools.research_runs import baseline_state, digest, leaves, state_hash

KINDS = {'model', 'provider', 'access', 'price', 'benchmark', 'behavior', 'release'}
DOMAINS = {'capabilities', 'benchmarks', 'access_pricing', 'behavior'}
CLOSED = {'duplicate', 'irrelevant', 'no_material_change', 'verified_change', 'investigated_unknown'}
TERMINAL_FIELDS = {'verified', 'unknown', 'not_applicable'}


def value_at(state, ref):
    value = state.get((ref['entity_type'], ref['entity_id']))
    if value is None:
        return None
    for part in ref['path'].split('/')[1:] if ref['path'] else []:
        part = part.replace('~1', '/').replace('~0', '~')
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def model_dependencies(state, kind, ident):
    record = state.get((kind, ident), {})
    if kind == 'model':
        return {ident} if record else set()
    if kind == 'provider':
        return {r['model_id'] for (k, _), r in state.items()
                if k in {'access', 'price'} and r.get('provider_id') == ident and r.get('model_id')}
    return set(record.get('model_ids', [])) | ({record['model_id']} if record.get('model_id') else set())


def rubric_hash(state):
    return digest(sorted((v for (k, _), v in state.items() if k == 'task'), key=lambda r: r['id']))


def field_ref(state, kind, ident, path):
    ref = {'entity_type': kind, 'entity_id': ident, 'path': path}
    return {**ref, 'baseline_value_hash': digest(value_at(state, ref))}


def make_pass(state, revisions, base_commit, ident, targets, watchlist, bounds, created_at, slice_name):
    """Declare scope before investigation. No old outcome becomes fresh evidence."""
    if not targets or not set(targets) <= {i for k, i in state if k == 'model'}:
        raise ValueError('Targets must be exact catalog IDs')
    boundary = revisions[-1]['id'] if revisions is not None else 'git-'+base_commit
    if revisions is not None and baseline_state(revisions, boundary) != state:
        raise ValueError('Capture canonical changes before declaring a baseline')
    linked = {(k, i) for k, i in state if k in KINDS and
              model_dependencies(state, k, i) & set(targets)}
    latest = {(r['entity_type'], r['entity_id']): r for r in (revisions or [])}
    carry = [{'entity_type': k, 'entity_id': i, 'revision_id': latest[(k, i)]['id'] if revisions is not None else 'git-'+base_commit,
              'value_hash': digest(state[(k, i)])} for k, i in sorted(linked)]
    run = {'schema_version': '1.0', 'id': ident, 'contract_id': 'maintenance-contract-v1',
           'base_commit': base_commit, 'baseline_revision_id': boundary,
           'baseline_hash': state_hash(state), 'catalog_hash': digest(sorted(i for k, i in state if k == 'model')),
           'rubric_hash': rubric_hash(state), 'created_at': created_at, 'observation_mode': 'live',
           'slice': slice_name, 'target_model_ids': sorted(set(targets)), 'bounds': deepcopy(bounds),
           'usage': {'research_minutes': 0, 'integration_minutes': 0, 'review_minutes': 0},
           'carry_forward': carry, 'watch_manifest': deepcopy(watchlist),
           'watch_manifest_hash': digest(watchlist), 'watch_checks': [], 'searches': [], 'candidates': [],
           'domain_accounting': []}
    for item in watchlist:
        source = state[('source', item['source_id'])]
        run['watch_checks'].append({**deepcopy(item), 'url': source['url'],
            'baseline_source_hash': digest(source), 'result': 'not_checked', 'checked_at': None,
            'observation': '', 'observation_hash': None, 'upstream_revision': None,
            'content_hash': None, 'remaining_gaps': ['Pending actual source inspection'],
            'blocked_reason': None})
    account_domains(run, state)
    return run


def account_domains(run, state):
    """Derive batch scope; never mutate the latest full-domain ledger."""
    rows = []
    for model in sorted(i for k, i in state if k == 'model'):
        for domain in sorted(DOMAINS):
            checks = [w for w in run['watch_checks'] if any(
                s['model_id'] == model and s['domain'] == domain for s in w['scope'])]
            searches = [q for q in run['searches'] if model in q['model_ids'] and domain in q['domains']]
            results = [c['result'] for c in checks] + [q['outcome'] for q in searches]
            result = ('blocked' if 'blocked' in results else 'scoped' if any(
                r in {'checked', 'no_material_change', 'unknown', 'sources_found', 'no_matched_sources'}
                for r in results) else 'not_checked')
            rows.append({'model_id': model, 'domain': domain, 'result': result,
                         'check_ids': sorted(w['id'] for w in checks),
                         'search_ids': sorted(q['id'] for q in searches)})
    run['domain_accounting'] = rows


def completion(run):
    """Derived only after schema and semantic checks; no writable complete flag."""
    watches = run['watch_checks']
    pending = sum(w['result'] == 'not_checked' for w in watches)
    blocked = sum(w['result'] == 'blocked' for w in watches) + sum(
        q['outcome'] == 'blocked' for q in run['searches'])
    unresolved = sum(c['disposition'] not in CLOSED or any(
        f['result'] not in TERMINAL_FIELDS for f in c['affected_fields']) or any(
        d['result'] not in {'confirmed', 'unknown'} for d in c['dependencies']) for c in run['candidates'])
    watches_complete = bool(watches or run['searches']) and not pending and not blocked
    return {'watch_complete': watches_complete,
            'reconciliation_complete': watches_complete and not unresolved,
            'pending_watch_checks': pending, 'blocked_checks': blocked,
            'unresolved_candidates': unresolved,
            'domains_not_checked': sum(d['result'] == 'not_checked' for d in run['domain_accounting'])}


def field_freshness(run, kind, ident, path, state):
    """Exact investigated field/hash only; no source or root date implies whole-profile freshness."""
    if run['observation_mode'] != 'live':
        return None
    rows = [f for c in run['candidates'] for f in c['affected_fields']
            if f['entity_type'] == kind and f['entity_id'] == ident and f['path'] == path
            and path and f['result'] == 'verified'
            and f['observed_value_hash'] == digest(value_at(state, f))]
    return max((f['checked_at'] for f in rows), default=None)


def pass_errors(run, baseline, evidence_state=None, revisions=None):
    """Structure and provenance checks do not prove source adequacy or causal attribution."""
    state = evidence_state if evidence_state is not None else baseline
    errors = []
    prefix = run['id'] + ': '
    def fail(message):
        errors.append(prefix + message)
    catalog = {i for k, i in baseline if k == 'model'}
    targets = set(run['target_model_ids'])
    contract = baseline.get(('maintenance_contract', run['contract_id']))
    if not contract:
        fail('maintenance contract missing from baseline')
    if state_hash(baseline) != run['baseline_hash']:
        fail('baseline hash differs')
    if digest(sorted(catalog)) != run['catalog_hash'] or rubric_hash(baseline) != run['rubric_hash']:
        fail('catalog or rubric hash differs')
    if not targets or not targets <= catalog:
        fail('unknown target model')
    today = date.today().isoformat()
    if run['created_at'] > today:
        fail('future pass date')
    if run['usage']['research_minutes'] > run['bounds']['max_research_minutes']:
        fail('research time budget exceeded; split follow-up into a separate pass')
    unique_queries = {(q['checked_at'], q['query']) for q in run['searches']}
    if len(unique_queries) > run['bounds']['max_searches']:
        fail('search budget exceeded')
    if len(unique_queries) != len(run['searches']):
        fail('duplicate query; record one query and its shared scope')
    checks = {w['id']: w for w in run['watch_checks']}
    searches = {q['id']: q for q in run['searches']}
    candidates = {c['id']: c for c in run['candidates']}
    if len(checks) != len(run['watch_checks']) or len(searches) != len(run['searches']) or len(candidates) != len(run['candidates']):
        fail('duplicate check/search/candidate IDs')
    if set(checks) & set(searches) or set(checks) & set(candidates) or set(searches) & set(candidates):
        fail('receipt-local IDs collide')
    if digest(run['watch_manifest']) != run['watch_manifest_hash']:
        fail('declared watch manifest hash differs')
    declared = {w['id']: w for w in run['watch_manifest']}
    if len(declared) != len(run['watch_manifest']) or set(declared) != set(checks) or any(
        declared[i] != {k: checks[i][k] for k in ['id', 'source_id', 'scope']} for i in set(declared) & set(checks)):
        fail('declared watch checks omitted, duplicated or scope changed')
    def dated(checked_at, label):
        if not checked_at or not run['created_at'] <= checked_at <= today:
            fail(label + ': actual check date missing or outside pass window')
    def inspected(check_ids, checked_at, label):
        if not check_ids:
            fail(label + ': needs actual source inspections')
        for ident in check_ids:
            w = checks.get(ident)
            if not w or w['result'] not in {'checked', 'no_material_change', 'unknown'}:
                fail(label + ': source check unresolved/uninspected ' + ident)
            elif w['checked_at'] != checked_at:
                fail(label + ': source/field dates differ')
    for w in run['watch_checks']:
        source = baseline.get(('source', w['source_id'])) or state.get(('source', w['source_id']))
        if not source or w['url'] != source['url']:
            fail(w['id'] + ': missing source or URL identity differs')
        expected_source = baseline.get(('source', w['source_id']))
        if w['baseline_source_hash'] != digest(expected_source):
            fail(w['id'] + ': source baseline hash differs')
        if not w['scope']:
            fail(w['id'] + ': missing declared scope')
        if len({digest(s) for s in w['scope']}) != len(w['scope']):
            fail(w['id'] + ': duplicate scope')
        for s in w['scope']:
            ref = (s['entity_type'], s['entity_id'])
            record = baseline.get(ref) or state.get(ref)
            if s['model_id'] not in targets or s['domain'] not in DOMAINS or not record:
                fail(w['id'] + ': unresolved or out-of-target scope')
                continue
            if s['model_id'] not in model_dependencies(baseline, *ref) | model_dependencies(state, *ref):
                fail(w['id'] + ': scope does not belong to model')
            if s['entity_type'] in {'provider', 'access', 'price'}:
                if s['entity_type'] == 'provider' and not s['product']:
                    fail(w['id'] + ': provider/offer scope needs exact product')
                if s['entity_type'] in {'access', 'price'} and s['product'] != record.get('product'):
                    fail(w['id'] + ': product differs from exact offer')
                if s['entity_type'] in {'access', 'price'} and s['product'] is None and not w['remaining_gaps']:
                    fail(w['id'] + ': unknown offer product needs explicit scope gap')
                if s['entity_type'] == 'provider' and not any(
                    k == 'access' and r.get('model_id') == s['model_id'] and
                    r.get('provider_id') == s['entity_id'] and r.get('product') == s['product']
                    for (k, _), r in {**baseline, **state}.items()):
                    fail(w['id'] + ': provider/product/model join is unresolved')
            if not set(s['task_ids']) <= {i for k, i in baseline if k == 'task'}:
                fail(w['id'] + ': unknown task scope')
        if w['result'] == 'not_checked':
            if w['checked_at'] or w['observation'] or w['observation_hash']:
                fail(w['id'] + ': pending check cannot claim inspection')
        else:
            dated(w['checked_at'], w['id'])
            if w['result'] == 'blocked':
                if not w['blocked_reason'] or not w['remaining_gaps'] or w['observation_hash']:
                    fail(w['id'] + ': blocked check needs gap and blocker, no inspected observation')
            else:
                if not w['observation'] or w['observation_hash'] != digest(w['observation']):
                    fail(w['id'] + ': actual observation/hash required')
                actual_source = state.get(('source', w['source_id']))
                if not actual_source or not actual_source.get('accessed_at') or not w['checked_at'] <= actual_source['accessed_at'] <= today:
                    fail(w['id'] + ': source inspection date missing, stale or future')
                if w['blocked_reason'] or (w['result'] == 'unknown' and not w['remaining_gaps']):
                    fail(w['id'] + ': invalid gap/blocker accounting')
    for q in run['searches']:
        dated(q['checked_at'], q['id'])
        if not set(q['model_ids']) <= targets or not q['model_ids'] or not q['domains']:
            fail(q['id'] + ': query scope outside declared targets')
        if q['outcome'] == 'sources_found' and not q['urls']:
            fail(q['id'] + ': found sources need lead URLs')
        if not q['notes']:
            fail(q['id'] + ': query outcome needs limitations/reason')
    expected = deepcopy(run)
    account_domains(expected, baseline)
    if run['domain_accounting'] != expected['domain_accounting']:
        fail('all-model/four-domain accounting omitted, duplicated or inconsistent with actual scope')
    latest = {}
    if revisions is not None:
        found = False
        for r in revisions:
            latest[(r['entity_type'], r['entity_id'])] = r
            if r['id'] == run['baseline_revision_id']:
                found = True
                break
        if not found:
            fail('journal boundary missing')
    seen_carry = set()
    for carry in run['carry_forward']:
        key = (carry['entity_type'], carry['entity_id'])
        if key in seen_carry:
            fail('duplicate carry-forward reference')
        seen_carry.add(key)
        if key not in baseline or carry['value_hash'] != digest(baseline.get(key)):
            fail('carry-forward value differs from pinned baseline')
        if run['baseline_revision_id'].startswith('git-') and carry['revision_id'] != run['baseline_revision_id']:
            fail('carry-forward commit differs from baseline')
        if revisions is not None and (key not in latest or latest[key]['id'] != carry['revision_id']):
            fail('carry-forward revision is not the baseline entity revision')
    required_carry = {(k, i) for k, i in baseline if k in KINDS and model_dependencies(baseline, k, i) & targets}
    if seen_carry != required_carry:
        fail('carry-forward inventory omitted or outside linked target scope')
    declared_fields = []
    for c in run['candidates']:
        label = c['id']
        if not c['summary'] or not c['rationale'] or not c['next_action']:
            fail(label + ': candidate needs summary, decision reason and next action')
        if not c['source_check_ids'] and not c['search_ids']:
            fail(label + ': candidate needs a discovery lead')
        if set(c['source_check_ids']) - set(checks) or set(c['search_ids']) - set(searches):
            fail(label + ': unresolved candidate references')
        discovered = c.get('discovered_model')
        if (not c['model_ids'] and not discovered) or not set(c['model_ids']) <= catalog:
            fail(label + ': unresolved candidate model IDs')
        if discovered:
            if discovered['release_date'] and discovered['release_date'] > today:
                fail(label + ': future release is a notice, not a released-model intake')
            if c['disposition'] not in {'pending', 'identity_unresolved', 'duplicate', 'irrelevant'}:
                fail(label + ': new-model intake requires a separate full assessment, not maintenance verification')
        seen_fields = set()
        required_models = set()
        for f in c['affected_fields']:
            key = (f['entity_type'], f['entity_id'], f['path'])
            if key in seen_fields:
                fail(label + ': duplicate affected field')
            seen_fields.add(key)
            required_models |= model_dependencies(baseline, *key[:2]) | model_dependencies(state, *key[:2])
            declared_fields.append((c, f))
            if f['baseline_value_hash'] != digest(value_at(baseline, f)):
                fail(label + ': affected field baseline hash differs')
            if (f['entity_type'], f['entity_id']) not in baseline and (f['entity_type'], f['entity_id']) not in state:
                fail(label + ': affected entity unresolved')
            if f['result'] == 'not_checked':
                if f['checked_at'] or f['check_ids'] or f['observed_value_hash']:
                    fail(label + ': pending affected field cannot claim inspection')
            else:
                dated(f['checked_at'], label)
                if not f['rationale']:
                    fail(label + ': field needs reason')
                if f['result'] == 'blocked':
                    if not f['remaining_gaps'] or f['observed_value_hash']:
                        fail(label + ': blocked field needs gap and no verified value hash')
                else:
                    inspected(f['check_ids'], f['checked_at'], label)
                    # The source check must declare support for this entity/path.
                    for ident in f['check_ids']:
                        w = checks.get(ident)
                        if w and not any(s['entity_type'] == f['entity_type'] and s['entity_id'] == f['entity_id']
                            and (s['path'] == f['path'] or not s['path'] or f['path'].startswith(s['path'] + '/')) for s in w['scope']):
                            fail(label + ': field inspection lies outside declared source scope')
                    if f['result'] == 'verified' and f['observed_value_hash'] != digest(value_at(state, f)):
                        fail(label + ': verified field differs from recorded current value')
                    if f['result'] == 'verified' and value_at(state, f) is None:
                        fail(label + ': null is unknown, not a verified value')
                    if f['result'] in {'unknown', 'not_applicable'}:
                        if not f['remaining_gaps'] and f['result'] == 'unknown':
                            fail(label + ': unknown field needs remaining gap')
                        if f['observed_value_hash']:
                            fail(label + ': unknown/excluded field cannot claim verified value')
        dependencies = {d['model_id']: d for d in c['dependencies']}
        if len(dependencies) != len(c['dependencies']) or set(dependencies) != required_models:
            fail(label + ': affected-model dependencies omitted or unresolved')
        if not required_models <= set(c['model_ids']):
            fail(label + ': candidate omits affected models')
        for d in c['dependencies']:
            if not d['rationale']:
                fail(label + ': dependency needs impact/applicability reason')
            if d['result'] in {'confirmed', 'unknown'}:
                dated(d['checked_at'], label)
                inspected(d['check_ids'], d['checked_at'], label)
                if not any(any(s['model_id'] == d['model_id'] for s in checks[i]['scope'])
                           for i in d['check_ids'] if i in checks):
                    fail(label + ': dependency model not covered by inspection scope')
            elif d['result'] == 'not_checked' and (d['checked_at'] or d['check_ids']):
                fail(label + ': pending dependency cannot claim inspection')
        if c['disposition'] in CLOSED and (any(f['result'] not in TERMINAL_FIELDS for f in c['affected_fields'])
                                           or any(d['result'] not in {'confirmed', 'unknown'} for d in c['dependencies'])):
            fail(label + ': terminal disposition hides pending/blocked work')
        if c['disposition'] == 'verified_change' and not c['affected_fields']:
            fail(label + ': verified change needs affected fields')
        if c['disposition'] == 'verified_change' and not any(
            f['result'] == 'verified' and f['baseline_value_hash'] != f['observed_value_hash'] for f in c['affected_fields']):
            fail(label + ': verified change has no recorded changed value')
    # Every factual edit must be accounted for, even on a provider shared beyond the cohort.
    for key in set(baseline) | set(state):
        if key[0] == 'research_coverage' and baseline.get(key) != state.get(key):
            fail('scoped maintenance must preserve the full-domain last-checked ledger ' + key[1])
        if key[0] not in KINDS or baseline.get(key) == state.get(key):
            continue
        if key in baseline and key in state and baseline[key].get('verified_at') != state[key].get('verified_at'):
            fail('scoped maintenance cannot advance whole-record verification date ' + '/'.join(key))
        before = dict(leaves(baseline.get(key), ''))
        after = dict(leaves(state.get(key), ''))
        for path in set(before) | set(after):
            if before.get(path) == after.get(path):
                continue
            if not any((f['entity_type'], f['entity_id']) == key and
                (not f['path'] or path == f['path'] or path.startswith(f['path'] + '/')) and
                ((f['result'] == 'verified' and f['observed_value_hash'] == digest(value_at(state, f))
                  and c['disposition'] in {'verified_change', 'pending'}) or
                 (f['result'] == 'unknown' and value_at(state, f) is None
                  and c['disposition'] == 'investigated_unknown')) for c, f in declared_fields):
                fail('unaccounted factual edit ' + '/'.join(key) + path)
    return errors


def validated_report(run, baseline, state, revisions):
    from jsonschema import Draft202012Validator, FormatChecker
    schema = json.loads((ROOT / 'schema/maintenance-pass-record.schema.json').read_text(encoding='utf-8'))
    schema_errors = [f'{list(e.path)}: {e.message}' for e in Draft202012Validator(
        schema, format_checker=FormatChecker()).iter_errors(run)]
    errors = schema_errors or pass_errors(run, baseline, state, revisions)
    return errors, None if errors else completion(run)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    scaffold = sub.add_parser('scaffold')
    scaffold.add_argument('--assignment', type=Path, required=True)
    scaffold.add_argument('--output', type=Path, required=True)
    check = sub.add_parser('check')
    check.add_argument('path', type=Path)
    check.add_argument('--require-watch-complete', action='store_true')
    check.add_argument('--require-reconciled', action='store_true')
    args = parser.parse_args()
    from tools.git_baselines import receipt_states
    revisions = None
    state = {key: value for key, (_, value) in canonical(ROOT).items()}
    if args.command == 'scaffold':
        if integrity_errors(ROOT):
            raise ValueError('Capture current checksums before scaffolding')
        if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, encoding='utf-8').strip():
            raise ValueError('Commit reviewed baseline before scaffolding; worktree must be clean')
        assignment = read(args.assignment)
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, encoding='utf-8').strip()
        run = make_pass(state, revisions, sha, assignment['id'], assignment['target_model_ids'],
                        assignment['watchlist'], assignment['bounds'], assignment['created_at'], assignment['slice'])
        errors, report = validated_report(run, state, state, revisions)
        if errors:
            print('\n'.join(errors))
            return 1
        import yaml
        with args.output.open('x', encoding='utf-8') as output:
            yaml.safe_dump(run, output, sort_keys=False, allow_unicode=True)
    else:
        run = read(args.path)
        baseline, evidence_state, revisions = receipt_states(run, 'maintenance_pass', state)
        errors, report = validated_report(run, baseline, evidence_state, revisions)
        if errors:
            print('\n'.join(errors))
            return 1
    print(json.dumps(report))
    if args.command == 'check':
        return int((args.require_watch_complete and not report['watch_complete']) or
                   (args.require_reconciled and not report['reconciliation_complete']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
