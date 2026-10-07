"""Read the canonical YAML and explicit observation history; no network or database."""
from copy import deepcopy
from datetime import date
from hashlib import sha256
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return yaml.load(Path(path).read_text(encoding='utf-8'), Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))

def canonical(root=ROOT):
    result = {}
    for kind, pattern in [('model', 'models/*/*/profile.yaml'), ('provider', 'providers/*/profile.yaml')]:
        for path in sorted(root.glob(pattern)):
            record = read(path)
            result[(kind, record['id'])] = (path.relative_to(root).as_posix(), record)
    for kind, name in [('price', 'data/pricing.yaml'), ('access', 'data/access.yaml'),
                       ('release', 'data/releases.yaml'), ('source', 'evidence/sources.yaml'),
                       ('observation', 'evidence/observations.yaml'), ('behavior', 'data/behavior.yaml'),
                       ('access_coverage', 'data/access-coverage.yaml'), ('benchmark', 'data/benchmarks.yaml'),
                       ('research_coverage', 'data/research-coverage.yaml')]:
        for record in read(root / name)['records']:
            result[(kind, record['id'])] = (name, record)
    for record in read(root / 'data/capability-taxonomy.yaml')['capabilities']:
        result[('task', record['id'])] = ('data/capability-taxonomy.yaml', record)
    for record in read(root / 'data/aliases.yaml')['records']:
        result[('alias', record['id'])] = ('data/aliases.yaml', record)
    return result

def judgment_index(model, profile):
    return [{'model_id': model['id'], 'profile': profile, **deepcopy(j)} for j in model['capabilities']]

def scope_errors(model, tasks):
    errors = []
    for collection in ['capabilities', 'performance_characteristics']:
        for j in model[collection]:
            label = f"{model['id']} {j['id']}"
            for task in j['task_ids'] + j['related_task_ids']:
                if task not in tasks:
                    errors.append(f'{label}: unknown task {task}')
            if set(j['task_ids']) & set(j['related_task_ids']):
                errors.append(f'{label}: direct and related tasks overlap')
            if j['scope'] == 'direct' and (len(j['task_ids']) != 1 or j['related_task_ids']):
                errors.append(f'{label}: direct scope requires exactly one task')
            if j['scope'] != 'direct' and j['task_ids']:
                errors.append(f'{label}: non-direct scope cannot assert task conclusions')
            if j['scope'] == 'compound' and len(j['related_task_ids']) < 2:
                errors.append(f'{label}: compound scope needs at least two related tasks')
            if j['scope'] == 'performance' and j['related_task_ids']:
                errors.append(f'{label}: performance has no capability mapping')
            if (collection == 'performance_characteristics') != (j['scope'] == 'performance'):
                errors.append(f'{label}: wrong judgment collection')
    return errors

def history(root=ROOT):
    return read(root / 'history/revisions.yaml')['records']


def research_coverage_errors(records, model_ids, sources):
    """Check accounting and provenance. This cannot certify the adequacy of research."""
    expected={(m,d) for m in model_ids for d in ['capabilities','benchmarks','access_pricing','behavior']}
    found=set();errors=[]
    for r in records:
        key=(r['model_id'],r['domain']);label=r['id']
        if key in found:errors.append(label+': duplicate model/domain coverage')
        found.add(key)
        if r['result']=='not_checked':
            if r['checked_at'] or r['evidence_ids'] or r['search_references']:
                errors.append(label+': unchecked coverage cannot claim a source check')
            if not r['remaining_gaps']:errors.append(label+': unchecked domain needs a remaining gap')
            continue
        if not r['checked_at']:errors.append(label+': checked result needs an actual check date')
        elif r['checked_at']>date.today().isoformat():errors.append(label+': check date is in the future')
        if r['result']=='blocked' and not r['blocked_reason']:errors.append(label+': blocked check needs a reason')
        if r['result']!='blocked' and not r['evidence_ids'] and not r['search_references']:
            errors.append(label+': actual check needs source or search references')
        for ident in r['evidence_ids']:
            source=sources.get(ident)
            if not source or not r['checked_at'] or source['accessed_at']<r['checked_at']:
                errors.append(label+': source inspection predates the claimed check '+ident)
        for search in r['search_references']:
            if search['checked_at']!=r['checked_at']:errors.append(label+': search/check dates differ')
        if r['result'] in {'unknown','blocked'} and not r['remaining_gaps']:
            errors.append(label+': unresolved result needs remaining gaps')
    if found!=expected:errors.append('Research coverage must account for every catalog model in all four domains')
    return errors

def snapshot(as_of, records=None):
    """Knowledge observed by this date. Effective dates never backdate observation."""
    date.fromisoformat(as_of)
    out = {}
    for r in records if records is not None else history():
        if r['observed_at'] > as_of:
            continue
        key = (r['entity_type'], r['entity_id'])
        if r['operation'] == 'remove':
            out.pop(key, None)
        else:
            out[key] = deepcopy(r['value'])
    return out

def entity_history(kind, ident, records=None):
    return [r for r in records if r['entity_type'] == kind and r['entity_id'] == ident] if records is not None else entity_history(kind, ident, history())

def capability_history(model_id, judgment_id=None, records=None):
    result = []
    for r in entity_history('model', model_id, records):
        value = r['value'] or {}
        judgments = value.get('capabilities', []) + value.get('performance_characteristics', [])
        result.append({**r, 'value': [j for j in judgments if judgment_id is None or j['id'] == judgment_id]})
    return result

def changes_between(start, end, records=None):
    date.fromisoformat(start); date.fromisoformat(end)
    if start > end:
        raise ValueError('Start must precede end')
    return [r for r in (records if records is not None else history()) if start < r['observed_at'] <= end]

def capture(root, observed_at, reason, evidence_ids, effective_from=None):
    """Append complete changed values, linking prior revisions; no invented effective dates."""
    from tools.migrate_v2 import write_yaml
    date.fromisoformat(observed_at)
    if effective_from is not None:
        date.fromisoformat(effective_from)
    if not reason or not evidence_ids:
        raise ValueError('Reason and evidence are required')
    path = root / 'history/revisions.yaml'
    old = history(root) if path.exists() else []
    if old and observed_at < max(r['observed_at'] for r in old):
        raise ValueError('Observation date cannot precede existing history')
    latest = {(r['entity_type'], r['entity_id']): r for r in old}
    current = canonical(root)
    known_evidence = {ident for (kind, ident) in set(current) | set(latest) if kind in ['source', 'observation']}
    known_evidence.add('capabilities-2026-10-07')
    if not set(evidence_ids) <= known_evidence:
        raise ValueError('Capture evidence must resolve to a source, observation or migration record')
    changes = []
    for key in sorted(set(current) | set(latest)):
        kind, ident = key
        previous = latest.get(key)
        profile, value = current.get(key, (previous['canonical_path'] if previous else '', None))
        if previous is not None and previous['value'] == value:
            continue
        def relevant_evidence(obj):
            if isinstance(obj, dict):
                for field, nested in obj.items():
                    if field in {'evidence_ids', 'source_ids', 'supporting_evidence_ids', 'contradictory_evidence_ids'} and isinstance(nested, list):
                        yield from (s for s in nested if isinstance(s, str) and s in known_evidence)
                    else:
                        yield from relevant_evidence(nested)
            elif isinstance(obj, list):
                for nested in obj:
                    yield from relevant_evidence(nested)
        ids = evidence_ids + list(relevant_evidence(value if value is not None else previous['value']))
        revision = {'entity_type': kind, 'entity_id': ident, 'canonical_path': profile,
                    'observed_at': observed_at, 'effective_from': effective_from,
                    'operation': 'remove' if value is None else 'baseline' if previous is None else 'update',
                    'previous_revision_id': previous['id'] if previous else None,
                    'reason': reason, 'evidence_ids': sorted(set(ids)), 'value': deepcopy(value)}
        revision['id'] = 'revision-' + sha256(json.dumps(revision, sort_keys=True).encode()).hexdigest()[:20]
        changes.append(revision)
    write_yaml(path, {'schema_version': '2.0', 'records': old + changes})
    return changes
