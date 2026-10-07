"""Read current canonical YAML and compact change summaries; no network or database."""
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
                       ('research_coverage', 'data/research-coverage.yaml'),
                       ('research_contract', 'data/research-contract.yaml'),
                       ('research_run', 'data/research-runs.yaml')]:
        for record in read(root / name)['records']:
            result[(kind, record['id'])] = (name, record)
    for record in read(root / 'data/capability-taxonomy.yaml')['capabilities']:
        result[('task', record['id'])] = ('data/capability-taxonomy.yaml', record)
    for record in read(root / 'data/aliases.yaml')['records']:
        result[('alias', record['id'])] = ('data/aliases.yaml', record)
    # Optional for older retained fixtures/snapshots; present in the current repository.
    for kind, name in [('maintenance_contract', 'data/maintenance-contract.yaml'),
                       ('maintenance_pass', 'data/maintenance-passes.yaml')]:
        if (root / name).exists():
            for record in read(root / name)['records']:
                result[(kind, record['id'])] = (name, record)
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


def integrity_records(root=ROOT):
    path = root / 'data/record-integrity.yaml'
    return read(path)['records'] if path.exists() else []

def record_hash(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()

def integrity_errors(root=ROOT):
    rows = integrity_records(root)
    stored = {(r['entity_type'],r['entity_id']):(r['canonical_path'],r['value_hash']) for r in rows}
    if len(stored) != len(rows):
        return ['Duplicate current record checksum']
    actual = {key:(path,record_hash(value)) for key,(path,value) in canonical(root).items()}
    return [] if stored == actual else ['Current record checksums differ; run capture_changes.py before publishing']

def capture(root, observed_at, reason, evidence_ids, effective_from=None):
    """Update current checksums and append a compact summary; never duplicate factual values."""
    from tools.migrate_v2 import write_yaml
    date.fromisoformat(observed_at)
    if effective_from is not None: date.fromisoformat(effective_from)
    if not reason or not evidence_ids: raise ValueError('Reason and evidence are required')
    manifest = root / 'data/record-integrity.yaml'
    old = integrity_records(root)
    if manifest.exists() and observed_at < read(manifest)['observed_at']:
        raise ValueError('Observation date cannot precede current capture')
    prior = {(r['entity_type'],r['entity_id']):r for r in old}
    current = canonical(root)
    known = {i for k,i in current if k in {'source','observation'}} | {'capabilities-2026-10-07'}
    # A source removal may refer to evidence already present in the last capture.
    known |= {i for k,i in prior if k in {'source','observation'}}
    if not set(evidence_ids) <= known: raise ValueError('Capture evidence must resolve')
    rows=[];changes=[]
    for kind,ident in sorted(set(current)|set(prior)):
        key=(kind,ident);previous=prior.get(key)
        path,value=current.get(key,(previous['canonical_path'] if previous else '',None))
        digest=record_hash(value) if value is not None else None
        if digest is not None: rows.append(dict(entity_type=kind,entity_id=ident,canonical_path=path,value_hash=digest))
        if previous and previous['value_hash']==digest and previous['canonical_path']==path: continue
        if not previous and digest is None: continue
        changes.append(dict(entity_type=kind,entity_id=ident,canonical_path=path,
                            operation='remove' if value is None else 'update' if previous else 'add'))
    if not changes: return []
    write_yaml(manifest,dict(schema_version='1.0',observed_at=observed_at,records=rows))
    log=root/'changelog/changes.yaml'
    summaries=read(log)['records'] if log.exists() else []
    entry=dict(observed_at=observed_at,summary=reason,evidence_ids=sorted(set(evidence_ids)),
               changed_entities=changes)
    entry['id']='change-'+record_hash(entry)[:16]
    if entry['id'] not in {r['id'] for r in summaries}: summaries.append(entry)
    write_yaml(log,dict(schema_version='1.0',records=summaries))
    return changes
