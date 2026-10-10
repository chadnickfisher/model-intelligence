"""Portable field accounting shared by receivers and frozen authoring kits.

Arrays are atomic. New null placeholders assert no fact; existing values changed
to null still need investigation. Citation/derived metadata is checked separately.
"""
from hashlib import sha256
import json

META = {'id', 'schema_version', 'verified_at', 'evidence_ids', 'source_ids',
        'supporting_evidence_ids', 'contradictory_evidence_ids', 'access_ids', 'price_ids'}


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def leaves(value, path):
    if isinstance(value, dict) and value:
        for key, nested in sorted(value.items()):
            if key not in META - {'access_ids', 'price_ids'}:
                yield from leaves(nested, path + '/' + key.replace('~', '~0').replace('/', '~1'))
    else:
        yield path, value


def pointer(record, path):
    for part in path.split('/')[1:]:
        record = record.get(part.replace('~1', '/').replace('~0', '~')) if isinstance(record, dict) else None
    return record


def factual_fields(record):
    return {p: v for p, v in leaves(record, '') if p and p.split('/')[1] not in META}


def changed_fields(before, after):
    previous = factual_fields(before)
    return {p: v for p, v in factual_fields(after).items() if previous.get(p) != v}


def field_domain(kind, path, groups):
    field = path.split('/')[1].replace('~1', '/').replace('~0', '~')
    for domain, fields in groups.items():
        if field in fields:
            return domain
    return {'model': 'capabilities', 'provider': 'access_pricing', 'access': 'access_pricing',
            'price': 'access_pricing', 'benchmark': 'benchmarks', 'behavior': 'behavior',
            'release': 'behavior'}[kind]


def field_manifest(state, target_ids, contract):
    rows = []
    for model_id in sorted(target_ids):
        linked = {kind: [(i, r) for (k, i), r in sorted(state.items()) if k == kind and
                  (r.get('model_id') == model_id or model_id in r.get('model_ids', []))]
                  for kind in ['access', 'price', 'benchmark', 'behavior', 'release']}
        providers = {r.get('provider_id') for kind in ['access', 'price'] for _, r in linked[kind]} - {None}
        linked['provider'] = [(i, state['provider', i]) for i in sorted(providers)]
        linked['model'] = [(model_id, state['model', model_id])]
        for kind, groups in contract['field_groups'].items():
            for domain, fields in groups.items():
                if not linked[kind]:
                    rows.append(dict(model_id=model_id, domain=domain, entity_type='inventory',
                                     entity_id=model_id, path='/' + kind, baseline_value_hash=digest([])))
                for ident, record in linked[kind]:
                    for field in fields:
                        for path, value in leaves(record.get(field), '/' + field):
                            rows.append(dict(model_id=model_id, domain=domain, entity_type=kind,
                                             entity_id=ident, path=path, baseline_value_hash=digest(value)))
    return rows


def required_fields(state, targets, contract, candidate=None):
    rows = field_manifest(state, targets, contract)
    if candidate is None:
        return rows
    keys = ('model_id', 'domain', 'entity_type', 'entity_id', 'path')
    known = {tuple(r[k] for k in keys) for r in rows}
    extensions = field_manifest(candidate, targets, contract)
    for model_id in sorted(targets):
        providers = {r.get('provider_id') for (k, _), r in candidate.items()
                     if k in {'access', 'price'} and r.get('model_id') == model_id} - {None}
        for (kind, ident), record in sorted(candidate.items()):
            relevant = (kind == 'model' and ident == model_id or kind == 'provider' and ident in providers or
                        kind in {'access', 'price', 'benchmark', 'behavior', 'release'} and
                        (record.get('model_id') == model_id or model_id in record.get('model_ids', [])))
            if not relevant:
                continue
            for path in changed_fields(state.get((kind, ident), {}), record):
                extensions.append(dict(model_id=model_id, domain=field_domain(kind, path, contract['field_groups'][kind]),
                                       entity_type=kind, entity_id=ident, path=path))
    for row in extensions:
        key = tuple(row[k] for k in keys)
        if key not in known:
            rows.append({**row, 'baseline_value_hash': digest(pointer(state.get((row['entity_type'], row['entity_id']), {}), row['path']))})
            known.add(key)
    return rows
