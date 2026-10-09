"""Compile reviewed structured research into a local candidate. No network or publication.

Incoming records are data, never executable code or filesystem paths. Research
adequacy requires evidence review; schema/completion checks cannot certify it.
"""
from copy import deepcopy
from datetime import date, datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, unquote
import argparse
import ipaddress
import json
import os
import re
import subprocess
import sys
from functools import lru_cache

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from tools.knowledge import ROOT, canonical, record_hash, scope_errors
from tools.git_baselines import git_state
from tools.research_runs import completion, digest, leaves, required_fields, run_errors
from tools.task_assessments import task_assessment_errors
from tools.package_workflow import archive_members, safe_name
from tools.migrate_v2 import write_yaml

MAX_BYTES = 16 * 1024 * 1024
SCHEMAS = {'model': 'model-profile', 'provider': 'provider-profile', 'source': 'source-record',
           'access': 'access-record', 'price': 'price-record', 'benchmark': 'benchmark-record',
           'behavior': 'behavior-record', 'release': 'release-record',
           'task_assessment': 'task-assessment-record', 'research_coverage': 'research-coverage-record'}
PATHS = {'source': 'evidence/sources.yaml', 'access': 'data/access.yaml', 'price': 'data/pricing.yaml',
         'benchmark': 'data/benchmarks.yaml', 'behavior': 'data/behavior.yaml', 'release': 'data/releases.yaml',
         'task_assessment': 'data/task-assessments.yaml', 'research_coverage': 'data/research-coverage.yaml'}
PREFIXES = {'source': ('src', 12), 'access': ('access', 16), 'price': ('price', 16),
            'benchmark': ('benchmark', 16), 'behavior': ('behavior', 16), 'release': ('release', 16),
            'task_assessment': ('task-assessment', 16), 'research_coverage': ('research-coverage', 16)}
META = {'id', 'schema_version', 'verified_at', 'evidence_ids', 'source_ids',
        'supporting_evidence_ids', 'contradictory_evidence_ids', 'access_ids', 'price_ids'}
RUN_KEYS = ('id', 'contract_id', 'base_commit', 'baseline_revision_id', 'baseline_hash', 'rubric_hash',
            'created_at', 'target_model_ids', 'bounds')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(path):
    path = Path(path)
    require(path.is_file() and not linked(path), 'Input must be a regular file')
    require(path.stat().st_size <= MAX_BYTES, 'Input exceeds size bound')
    raw = path.read_bytes()
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                       parse_constant=lambda _: require(False, 'Non-finite JSON number'))
    return value, sha256(raw).hexdigest()


def linked(path):
    return path.is_symlink() or (path.exists() and bool(getattr(path.lstat(), 'st_file_attributes', 0) & 0x400))


def public_url(value):
    url = urlsplit(value)
    host = unquote(url.hostname or '').lower().rstrip('.')
    require(url.scheme == 'https' and host and not url.username and not url.password, 'Evidence needs public HTTPS')
    require(host != 'localhost' and '.' in host and not host.endswith(('.local', '.localhost', '.internal')), 'Private source host')
    try:
        require(ipaddress.ip_address(host).is_global, 'Private source address')
    except ValueError as exc:
        if str(exc) == 'Private source address':
            raise
    require(not any(host == h or host.endswith('.' + h) for h in
                    ('drive.google.com', 'docs.google.com', 'oaiusercontent.com')), 'Private transport is not evidence')
    require(not re.search(r'(?:^|[?&])(?:token|access_token|sig|signature|api_key|key)=', url.query, re.I), 'Signed/token source URL')
    require(not any(k.lower() in {'token', 'access_token', 'sig', 'signature', 'api_key', 'key', 'authorization', 'credential'}
                    or k.lower().startswith('x-amz-') for k, _ in parse_qsl(url.query)), 'Signed/token source URL')


@lru_cache(maxsize=1)
def schema_registry():
    schemas = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in (ROOT / 'schema').glob('*.schema.json')}
    registry = Registry().with_resources((n, Resource.from_contents(s, default_specification=DRAFT202012))
                                         for n, s in schemas.items())
    return schemas, registry


def validate_schema(value, name):
    schemas, registry = schema_registry()
    validator = Draft202012Validator(schemas[name], registry=registry, format_checker=FormatChecker())
    error = next(validator.iter_errors(value), None)
    require(error is None, 'Schema ' + name + ': ' + (error.message if error else ''))


def replace_refs(value, mapping, key=''):
    if isinstance(value, dict):
        return {k: replace_refs(v, mapping, k) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_refs(v, mapping, key) for v in value]
    if isinstance(value, str) and (key == 'id' or key.endswith(('_id', '_ids'))):
        if value.startswith('new:'):
            require(value in mapping, 'Unresolved local reference: ' + value)
        return mapping.get(value, value)
    return value


def allocate(changes, baseline):
    mapping = {}
    existing_urls = {r['url']: i for (k, i), r in baseline.items() if k == 'source'}
    all_ids = {i for _, i in baseline}
    for model in (r for (k, _), r in baseline.items() if k == 'model'):
        all_ids.update(j['id'] for j in model['capabilities'] + model['performance_characteristics'])
    new_ids = set()
    source_urls = {r['id']: r['url'] for (k, _), r in baseline.items() if k == 'source'}
    source_urls.update({c['record']['id']: c['record']['url'] for c in changes if c['kind'] == 'source'})
    for change in changes:
        kind, record = change['kind'], change['record']
        ident = record['id']
        if ident.startswith('new:'):
            require(kind not in {'model', 'provider', 'research_coverage'}, 'New model/provider onboarding needs a separately pinned scope')
            require(ident not in mapping and change['previous_hash'] is None and change['identity_key'], 'Invalid or duplicate new reference')
            if kind == 'source':
                require(record['url'] not in existing_urls, 'Existing source URL must retain its canonical ID')
                natural = record['url']
            elif kind == 'task_assessment':
                natural = record['model_id'] + '|' + record['task_id']
                require(not any(k == kind and r['model_id'] == record['model_id'] and r['task_id'] == record['task_id']
                                for (k, _), r in baseline.items()), 'Existing model/task must retain its ID')
            else:
                natural = record.get('model_id', '') + '|' + change['identity_key']
            prefix, size = PREFIXES[kind]
            allocated = prefix + '-' + sha256(natural.encode()).hexdigest()[:size]
            require(allocated not in all_ids | new_ids, 'New identity collides with an existing record')
            mapping[ident] = allocated
            new_ids.add(allocated)
        if kind == 'model':
            for collection in ('capabilities', 'performance_characteristics'):
                for judgment in record[collection]:
                    ref = judgment['id']
                    if ref.startswith('new:'):
                        require(ref not in mapping, 'Duplicate new finding reference')
                        support = judgment['supporting_evidence_ids']
                        if judgment['scope'] == 'direct' and len(judgment['task_ids']) == 1 and support:
                            require(support[0] in source_urls, 'New direct finding lacks its primary source record')
                            seed = record['id'] + '|' + judgment['task_ids'][0] + '|' + source_urls[support[0]]
                        else:
                            seed = record['id'] + '|' + ref.removeprefix('new:')
                        allocated = 'judgment-' + sha256(seed.encode()).hexdigest()[:16]
                        require(allocated not in all_ids | new_ids, 'Finding identity collision')
                        mapping[ref] = allocated
                        new_ids.add(allocated)
    return mapping


def evidence_ids(record):
    result = set()
    if isinstance(record, dict):
        for key, value in record.items():
            if key in {'evidence_ids', 'source_ids', 'supporting_evidence_ids', 'contradictory_evidence_ids'}:
                result.update(value)
            elif isinstance(value, (dict, list)):
                result.update(evidence_ids(value))
    elif isinstance(record, list):
        for value in record:
            result.update(evidence_ids(value))
    return result


def expanded_sources(ids, observations):
    result = set()
    for ident in ids:
        linked_ids = observations.get(ident, {}).get('source_ids', [ident])
        require(linked_ids, 'Editorial observations cannot establish factual source checks')
        result.update(linked_ids)
    return result


def validate_change(change, baseline, mapping, assignment, seed, targets, providers, created):
    kind, record = change["kind"], change["record"]
    key = (kind, record["id"])
    old = baseline.get(key)
    public_text = json.dumps(record)
    reserved = (assignment['assignment_id'], seed['id'], '.local/', '.agents/', 'AGENTS.md', '.receipt.json')
    require(not any(value in public_text for value in reserved), 'Private operating material in public record')
    require(not any(ref in public_text for ref in mapping), 'Unresolved local reference in public prose')
    require(old is not None or record['id'] in mapping.values(), 'New records must use local new: references')
    require(change['previous_hash'] == (record_hash(old) if old else None), 'Prior-record hash mismatch: ' + record['id'])
    require(old != record, 'No-op record must remain a check, not a change')
    if old:
        require(set(old) <= set(record), 'Record field deletion is not an upsert')
    if kind == 'model':
        require(record['id'] in targets and old is not None, 'Unassigned model')
        require(record['verified_at'] == old['verified_at'], 'Whole-profile date refresh is outside field-level research')
        require(record['identity']['version'] == old['identity']['version'], 'Immutable model version cannot be replaced')
        prior_findings = {j['id']: j for c in ('capabilities', 'performance_characteristics') for j in old[c]}
        findings = {j['id']: j for c in ('capabilities', 'performance_characteristics') for j in record[c]}
        require(set(prior_findings) <= set(findings), 'Finding deletion is not an upsert')
        require(all(i in prior_findings or i in mapping.values() for i in findings), 'New findings must use local new: references')
        for ident, before in prior_findings.items():
            after = findings[ident]
            require(all(before[f] == after[f] for f in ('scope', 'task_ids', 'related_task_ids')), 'Stable finding scope was reassigned')
    elif kind == 'provider':
        require(record['id'] in providers and old is not None, 'Unassigned provider')
        require(record['verified_at'] == old['verified_at'], 'Whole-provider date refresh is outside field-level research')
    elif kind != 'source':
        affected = set(record.get('model_ids', [record.get('model_id')]))
        require(affected and affected <= targets, 'Unassigned model record')
        if kind in {'access', 'price'}:
            require(record['provider_id'] in providers, 'Unassigned provider route')
        if old:
            for field in ('model_id', 'model_ids', 'provider_id', 'task_id'):
                require(old.get(field) == record.get(field), 'Stable record identity was reassigned')
    validate_schema(record, SCHEMAS[kind] + '.schema.json')
    require(change['evidence_ids'] and change['checked_paths'], 'Change lacks evidence/checked fields')
    if kind == 'source':
        public_url(record['url'])
        require(record['accessed_at'] <= created.date().isoformat(), 'Source inspected after packet date')
        require(record['accessed_at'] >= seed['created_at'], 'Changed source was not inspected during this run')


def validate_support(change, baseline, sources, observations, seed, created):
    for ident in sorted(expanded_sources(change['evidence_ids'], observations)):
        require(ident in sources and seed['created_at'] <= sources[ident]['accessed_at'] <= created.date().isoformat(),
                'Change needs a current inspected source: ' + ident)
    record = change['record']
    require(evidence_ids(record) <= set(sources) | set(observations), 'Record has an unresolved source')
    # Historical offer/event citations can retain their actual old dates;
    # their altered fields still require fresh linked checks below.
    current_support = evidence_ids(record) if change['kind'] in {
        'task_assessment', 'benchmark', 'behavior', 'research_coverage'} else set()
    if change['kind'] == 'model':
        old = baseline[('model', record['id'])]
        prior = {j['id']: j for c in ('capabilities', 'performance_characteristics') for j in old[c]}
        for collection in ('capabilities', 'performance_characteristics'):
            for finding in record[collection]:
                if finding != prior.get(finding['id']):
                    finding_sources = expanded_sources(evidence_ids(finding), observations)
                    require(all(sources[i]['accessed_at'] >= finding['observed_at'] for i in finding_sources), 'Finding sources predate its check')
                    current_support |= finding_sources
                    require(seed['created_at'] <= finding['observed_at'] <= created.date().isoformat(), 'Changed finding needs its actual run inspection date')
    checked = record.get('checked_at', record.get('observed_at', seed['created_at']))
    require(all(max(seed['created_at'], checked) <= sources[i]['accessed_at'] <= created.date().isoformat()
                for i in expanded_sources(current_support, observations)), 'Changed conclusion cites uninspected carry-forward evidence')
    if change['kind'] == 'source':
        require(record['id'] in change['evidence_ids'], 'Source change must account for its own inspection')


def validate_accounting(change, baseline, fields, decisions, run, sources, observations):
    kind, record = change['kind'], change['record']
    old = baseline.get((kind, record['id']), {})
    if kind in {'source', 'task_assessment', 'research_coverage'}:
        if kind == 'task_assessment':
            row = decisions[(record['model_id'], record['task_id'])]
            require(row['result'] == record['result'] and row['result'] not in {'blocked', 'not_checked'}, 'Task change lacks its investigated decision')
            require(row['checked_at'] == record['checked_at'] and row['judgment_ids'] == record['judgment_ids'], 'Task decision and canonical proposal differ')
            require(set(row['evidence_ids']) == set(record['evidence_ids']), 'Task decision source accounting differs')
        elif kind == 'source':
            require(any(record['id'] in r['evidence_ids'] and r['result'] == 'checked' for r in run['source_checks']), 'Source inspection absent from category accounting')
        else:
            row = next(r for r in run['domain_checks'] if r['model_id'] == record['model_id'] and r['domain'] == record['domain'])
            require(row['result'] == record['result'] and row['checked_at'] == record['checked_at'], 'Coverage differs from actual domain accounting')
        return
    actual = {p: v for p, v in leaves(record, '') if p.split('/')[1] not in META}
    previous = dict(leaves(old, ''))
    previous = {p: v for p, v in previous.items() if p and p.split('/')[1] not in META}
    require(not old or set(previous) <= set(actual), 'Nested field deletion is not an upsert')
    altered = {p for p, v in actual.items() if previous.get(p) != v}
    require(altered <= set(change['checked_paths']), 'Changed fields missing from checked_paths')
    for path in sorted(altered):
        row = fields.get((kind, record['id'], path))
        require(row is not None and row['result'] not in {'blocked', 'not_checked'}, 'Changed factual field was not investigated: ' + path)
        require(set(change['evidence_ids']) & set(row['evidence_ids']), 'Changed field lacks linked inspected evidence')
        primary_required = (kind in {'access', 'price'} or
            kind == 'model' and path.split('/')[1] in {'identity', 'specifications', 'additional_specifications', 'licensing', 'local_inference'} or
            kind == 'provider' and path.split('/')[1] not in {'reliability', 'limitations', 'notes'})
        if primary_required:
            require(any(sources[i]['source_type'] == 'primary' for i in expanded_sources(row['evidence_ids'], observations)), 'Specifications, prices and eligibility need primary evidence')


def validate_confidence(change, sources, observations, groups):
    if change['kind'] != 'task_assessment' or 'aggregate' not in change['record']:
        return
    a = change['record']['aggregate']
    support = expanded_sources(a['supporting_evidence_ids'], observations)
    nonvendor = [i for i in support if sources[i]['source_type'] in {'independent-evaluation', 'practitioner'}]
    if a['suitability'] not in {'unknown', 'not_supported', 'disputed'}:
        if a['evidence_confidence'] in {'medium', 'high'}:
            require(nonvendor, 'Vendor-only performance cannot have Medium/High confidence')
        if a['evidence_confidence'] == 'high':
            require(all(i in groups for i in nonvendor) and len({groups[i] for i in nonvendor}) >= 2,
                    'High performance confidence needs distinct independent evidence groups')


def validate_discovery_check(row, seed, created, sources, observations):
    searches = set()
    if row['result'] == 'not_checked':
        require(not row['checked_at'] and not row['rationale'] and not row['evidence_ids'] and not row['search_references'] and not row['blocked_reason'] and row['remaining_gaps'], 'Unchecked discovery cannot claim investigation')
        return searches
    require(row['checked_at'] and seed['created_at'] <= row['checked_at'] <= created.date().isoformat() and row['rationale'].strip(), 'Discovery check needs actual date/reason')
    require((row['result'] == 'blocked') == bool(row['blocked_reason']), 'Discovery blocker status differs')
    if row['result'] in {'blocked', 'unknown'}:
        require(row['remaining_gaps'], 'Unresolved discovery needs gaps')
    if row['result'] != 'blocked':
        require(row['evidence_ids'] or row['search_references'], 'Discovery needs actual inspection/search')
        require(row['evidence_ids'] or any(s['outcome'] != 'blocked' for s in row['search_references']), 'Failed discovery search remains blocked')
    require(expanded_sources(row['evidence_ids'], observations) <= set(sources), 'Unknown discovery source')
    if row['result'] == 'checked':
        require(any(sources[i]['source_type'] == 'primary' for i in expanded_sources(row['evidence_ids'], observations)), 'Checked discovery needs an inspected official catalog/changelog')
    for i in expanded_sources(row['evidence_ids'], observations):
        require(i in sources and row['checked_at'] <= sources[i]['accessed_at'] <= created.date().isoformat(), 'Discovery source not freshly inspected')
    for search in row['search_references']:
        require(search['checked_at'] == row['checked_at'], 'Discovery search/check dates differ')
        searches.add((search['checked_at'], search['query']))
        for url in search['urls']:
            public_url(url)
    return searches


def compile_batch(packet, assignment, baseline, private_patterns=()):
    """Pure compilation: exact schema, baseline, scope, accounting and record guards."""
    validate_schema(packet, 'research-batch.schema.json')
    require(packet['assignment_id'] == assignment['assignment_id'], 'Wrong assignment')
    require(packet['baseline_commit'] == assignment['baseline_commit'], 'Stale baseline')
    created = datetime.fromisoformat(packet['created_at'].replace('Z', '+00:00'))
    require(created.tzinfo and created <= datetime.now(timezone.utc), 'Invalid/future packet date')
    text = json.dumps(packet)
    require(not any(p in text for p in private_patterns), 'Private content in research packet')
    require(not re.search(r'(?i)(?:drive\.google\.com|docs\.google\.com|[A-Z]:\\\\Users\\\\|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,})', text), 'Private content in research packet')
    seed = assignment['research_run']
    run = packet['research_run']
    require(all(run[k] == seed[k] for k in RUN_KEYS), 'Assignment metadata/rubric/bounds changed')
    targets = set(seed['target_model_ids'])
    providers = {r['provider_id'] for (k, _), r in baseline.items()
                 if k in {'access', 'price'} and r.get('model_id') in targets}
    mapping = allocate(packet['changes'], baseline)
    changes = replace_refs(deepcopy(packet['changes']), mapping)
    run = replace_refs(deepcopy(run), mapping)
    candidate = deepcopy(baseline)
    changed = set()
    for change in changes:
        key = (change['kind'], change['record']['id'])
        require(key not in changed, 'Duplicate changed record')
        changed.add(key)
        validate_change(change, baseline, mapping, assignment, seed, targets, providers, created)
        candidate[key] = change['record']
    sources = {i: r for (k, i), r in candidate.items() if k == 'source'}
    observations = {i: r for (k, i), r in candidate.items() if k == 'observation'}
    for change in changes:
        validate_support(change, baseline, sources, observations, seed, created)
    # Newly discovered records/fields extend the pinned checklist; omissions fail closed.
    errors = run_errors(run, baseline, candidate)
    require(not errors, 'Research accounting: ' + '; '.join(errors[:8]))
    fields = {(r['entity_type'], r['entity_id'], r['path']): r for r in run['field_checks']}
    decisions = {(r['model_id'], r['task_id']): r for r in run['task_decisions']}
    for change in changes:
        validate_accounting(change, baseline, fields, decisions, run, sources, observations)
    tasks = {i for (k, i) in candidate if k == 'task'}
    models = {i: r for (k, i), r in candidate.items() if k == 'model'}
    access = {i: r for (k, i), r in candidate.items() if k == 'access'}
    require(not any(scope_errors(models[m], tasks) for m in targets), 'Invalid task/finding scope')
    assessments = [r for (k, _), r in candidate.items() if k == 'task_assessment']
    require(not task_assessment_errors(assessments, models, tasks, access), 'Invalid task-assessment references')
    discoveries = replace_refs(packet['discoveries'], mapping)
    for discovery in discoveries:
        public_url(discovery['url'])
        require(discovery['evidence_ids'] and set(discovery['evidence_ids']) <= set(sources) | set(observations), 'Discovery lacks sources')
    discovery_checks = replace_refs(packet['discovery_checks'], mapping)
    creator_ids = [r['creator_id'] for r in discovery_checks]
    require(len(set(creator_ids)) == len(creator_ids) and set(creator_ids) == set(assignment['discovery_creator_ids']), 'Discovery creator accounting omitted/duplicated')
    discovery_searches = set()
    for row in discovery_checks:
        discovery_searches.update(validate_discovery_check(row, seed, created, sources, observations))
    require(len(discovery_searches) <= assignment['max_discovery_searches'], 'Discovery search allowance exceeded')
    for collection in ('domain_checks', 'field_checks', 'task_decisions', 'source_checks'):
        for row in run[collection]:
            for search in row['search_references']:
                for url in search['urls']:
                    public_url(url)
    groups = replace_refs(packet['source_groups'], mapping)
    # Mapping keys are source IDs too, and require explicit handling.
    groups = {mapping.get(k, k): v for k, v in groups.items()}
    require(set(groups) <= set(sources), 'Unknown independence-group source')
    for change in changes:
        validate_confidence(change, sources, observations, groups)
    report = completion(run)
    report['discovery_pending'] = sum(r['result'] == 'not_checked' for r in discovery_checks)
    report['discovery_blocked'] = sum(r['result'] == 'blocked' for r in discovery_checks)
    report['batch_complete'] = report['complete'] and not report['discovery_pending'] and not report['discovery_blocked']
    return {'changes': changes, 'research_run': run, 'mapping': mapping, 'candidate': candidate,
            'completion': report, 'discoveries': discoveries}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], encoding='utf-8').strip()


def private_destination(root, destination):
    root, destination = Path(root).resolve(), Path(destination).absolute()
    require(destination.resolve().is_relative_to(root / '.local' / 'research'), 'Candidate must stay under ignored local research storage')
    require(not any(linked(p) for p in [destination, *destination.parents]), 'Candidate parent is a link/reparse point')
    require(git(root, 'check-ignore', '--', destination.relative_to(root).as_posix()) != '', 'Candidate destination is not ignored')
    return destination


def stage(root, compiled, assignment, packet_hash, destination, run_tests=False):
    """Export trusted Git code, upsert records there, capture/render/validate there."""
    root = Path(root).resolve()
    require(git(root, 'rev-parse', 'HEAD') == assignment['baseline_commit'], 'Repository HEAD advanced')
    destination = private_destination(root, destination)
    require(not destination.exists(), 'Candidate destination already exists; never overwrite a previous stage')
    raw = subprocess.check_output(['git', '-C', str(root), 'archive', '--format=zip', assignment['baseline_commit']])
    files = archive_members(raw)
    destination.mkdir(parents=True)
    candidate = destination / 'candidate'
    candidate.mkdir()
    for name, data in files.items():
        path = candidate / safe_name(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    paths = set()
    import yaml
    baseline = git_state(assignment['baseline_commit'], root)
    locations = canonical(root)
    documents = {}
    for change in compiled['changes']:
        kind, record = change['kind'], change['record']
        if kind in {'model', 'provider'}:
            require((kind, record['id']) in baseline, 'Unassigned new profile')
            path = locations[(kind, record['id'])][0]
            write_yaml(candidate / path, record)
        else:
            path = PATHS[kind]
            if path not in documents:
                doc = yaml.load((candidate / path).read_text(encoding='utf-8'),
                                Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
                documents[path] = (doc, {r['id']: n for n, r in enumerate(doc['records'])})
            doc, indices = documents[path]
            if record['id'] in indices:
                doc['records'][indices[record['id']]] = record
            else:
                indices[record['id']] = len(doc['records'])
                doc['records'].append(record)
        paths.add(path)
    # A daily batch can update hundreds of records in one collection. Read and
    # write that document once, preserving order and the exact validated records.
    for path, (doc, _) in documents.items():
        write_yaml(candidate / path, doc)
    checks = []
    def check(command):
        result = subprocess.run([sys.executable, *command], cwd=candidate, capture_output=True, encoding='utf-8', errors='replace')
        checks.append({'command': command, 'exit_code': result.returncode, 'output': result.stdout + result.stderr})
        require(result.returncode == 0, 'Candidate check failed; original checkout untouched: ' + ' '.join(command))
    try:
        if compiled['changes']:
            evidence = sorted({i for c in compiled['changes'] for i in c['evidence_ids']})
            check(['tools/capture_changes.py', '--observed-at', date.today().isoformat(), '--reason',
                   'Updated source-backed model, task, measurement and access findings under their documented conditions.', '--evidence', *evidence])
        check(['tools/render.py'])
        check(['tools/validate.py'])
        if run_tests:
            check(['-m', 'pytest', '-q', '-p', 'no:cacheprovider'])
        changed = {name: {'previous_sha256': sha256(data).hexdigest(), 'sha256': sha256((candidate / name).read_bytes()).hexdigest()}
                   for name, data in files.items() if (candidate / name).read_bytes() != data}
        extras = {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()} - set(files)
        require(not any(p.endswith(('.yaml', '.md', '.json')) for p in extras), 'Unexpected generated public files')
        receipt = {'status': 'validated_local_candidate', 'packet_sha256': packet_hash,
                   'baseline_commit': assignment['baseline_commit'], 'completion': compiled['completion'],
                   'changes': changed, 'checks': checks, 'tests_passed': run_tests, 'published': False}
        (destination / 'stage-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
        return receipt
    except Exception:
        (destination / 'failed-checks.json').write_text(json.dumps(checks, indent=2) + '\n', encoding='utf-8')
        raise


def apply_candidate(root, destination, review):
    """Local evidence review pins exact bytes. Preflight all files; rollback our writes on failure."""
    root = Path(root).resolve()
    destination = private_destination(root, destination)
    receipt, _ = load_json(destination / 'stage-receipt.json')
    require(review['packet_sha256'] == receipt['packet_sha256'], 'Review belongs to different research bytes')
    require(review['candidate_changes'] == receipt['changes'], 'Review does not pin this exact candidate')
    require(review['evidence_reviewed'] is True, 'Semantic source review is required')
    require(receipt['tests_passed'], 'Candidate tests must pass before application')
    require(receipt['completion']['batch_complete'] or review.get('accept_partial') is True, 'Incomplete research requires explicit partial acceptance')
    require(git(root, 'rev-parse', 'HEAD') == receipt['baseline_commit'], 'Stale destination baseline')
    intended = receipt['changes']
    require(intended, 'No candidate changes to apply')
    from tools.public_boundary import private_work_path
    from tools.package_workflow import ALLOWED_PREFIXES, ALLOWED_NAMES, BLOCKED_PREFIXES, BLOCKED_NAMES
    for name in intended:
        safe_name(name)
        require(not private_work_path(name) and not name.startswith(BLOCKED_PREFIXES) and name not in BLOCKED_NAMES
                and (name.startswith(ALLOWED_PREFIXES) or name in ALLOWED_NAMES), 'Candidate write path is not public data')
    # Canonical state guard also catches unrelated dirty records and prevents stale integrity capture.
    baseline = git_state(receipt['baseline_commit'], root)
    current = {k: r for k, (_, r) in canonical(root).items()}
    same = all((root / name).is_file() and sha256((root / name).read_bytes()).hexdigest() == hashes['sha256']
               for name, hashes in intended.items())
    if same:
        return {'status': 'already_applied', 'changed_files': 0}
    require(current == baseline, 'Canonical working data differs from the pinned baseline; reconcile explicitly')
    originals = {}
    for name, hashes in intended.items():
        target, proposed = root / name, destination / 'candidate' / name
        require(not any(linked(p) for p in [target, proposed, *target.parents, *proposed.parents]), 'Linked apply path')
        require(target.is_file() and sha256(target.read_bytes()).hexdigest() == hashes['previous_sha256'], 'Dirty/stale target: ' + name)
        require(proposed.is_file() and sha256(proposed.read_bytes()).hexdigest() == hashes['sha256'], 'Candidate modified since validation')
        originals[name] = target.read_bytes()
    lock = root / '.local' / 'research' / 'candidate-apply.lock'
    handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    written = []
    try:
        for name in intended:
            target = root / name
            require(target.read_bytes() == originals[name], 'Destination changed during application')
            temporary = target.with_name(target.name + '.research-batch-tmp')
            require(not temporary.exists(), 'Conflicting temporary write')
            try:
                with temporary.open('xb') as output:
                    output.write((destination / 'candidate' / name).read_bytes())
                os.replace(temporary, target)
            finally:
                if temporary.exists():
                    temporary.unlink()
            written.append(name)
    except Exception:
        conflicts = []
        for name in reversed(written):
            target = root / name
            if not any(linked(p) for p in [target, *target.parents]) and sha256(target.read_bytes()).hexdigest() == intended[name]['sha256']:
                target.write_bytes(originals[name])
            else:
                conflicts.append(name)
        if conflicts:
            (destination / 'rollback-conflicts.json').write_text(json.dumps(conflicts), encoding='utf-8')
        raise
    finally:
        os.close(handle)
        lock.unlink()
    return {'status': 'applied_locally', 'changed_files': len(written), 'published': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'stage', 'apply'])
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--assignment', type=Path)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--review', type=Path)
    parser.add_argument('--private-patterns', type=Path)
    parser.add_argument('--sha256')
    parser.add_argument('--bytes', type=int)
    parser.add_argument('--tests', action='store_true')
    args = parser.parse_args()
    if args.mode == 'apply':
        require(args.destination and args.review, 'Apply requires candidate destination and local review')
        result = apply_candidate(ROOT, args.destination, load_json(args.review)[0])
    else:
        require(args.packet and args.assignment, 'Packet and trusted assignment required')
        packet, packet_hash = load_json(args.packet)
        require(args.sha256 and packet_hash == args.sha256, 'Externally reported SHA-256 is required and must match')
        require(args.bytes is None or args.packet.stat().st_size == args.bytes, 'Externally reported byte size differs')
        assignment, _ = load_json(args.assignment)
        patterns = load_json(args.private_patterns)[0]['patterns'] if args.private_patterns else []
        compiled = compile_batch(packet, assignment, git_state(assignment['baseline_commit']), patterns)
        result = {'status': 'structure_and_accounting_valid_pending_evidence_review', 'packet_sha256': packet_hash,
                  'proposed_records': len(compiled['changes']), 'completion': compiled['completion'], 'reference_mapping': compiled['mapping']}
        if args.mode == 'stage':
            require(args.destination, 'Explicit ignored stage destination required')
            result = stage(ROOT, compiled, assignment, packet_hash, args.destination, args.tests)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, RecursionError, subprocess.CalledProcessError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
