"""Portable field accounting shared by receivers and frozen authoring kits.

Arrays are atomic. New null placeholders assert no fact; existing values changed
to null still need investigation. Citation/derived metadata is checked separately.
"""
from hashlib import sha256
from datetime import date
import json

META = {'id', 'schema_version', 'verified_at', 'evidence_ids', 'source_ids',
        'supporting_evidence_ids', 'contradictory_evidence_ids', 'access_ids', 'price_ids'}


def assessment_chronology_errors(record, *, latest_date=None):
    """Portable chronology for actual aggregate judgments, never a date repair."""
    aggregate = record.get('aggregate')
    if not isinstance(aggregate, dict):
        return []
    errors = []
    dates = {}
    for path, value in (('/checked_at', record.get('checked_at')),
                        ('/aggregate/assessed_at', aggregate.get('assessed_at'))):
        try:
            parsed = date.fromisoformat(value) if isinstance(value, str) else None
            if parsed is None or parsed.isoformat() != value:
                raise ValueError('Expected an ISO date')
            dates[path] = value
        except ValueError:
            errors.append({'path': path, 'message': 'aggregate chronology requires a valid actual date'})
    if errors:
        return errors
    assessed = dates['/aggregate/assessed_at']
    if assessed < dates['/checked_at']:
        errors.append({'path': '/aggregate/assessed_at', 'message': 'aggregate assessment predates its source check'})
    if latest_date is not None and assessed > latest_date:
        errors.append({'path': '/aggregate/assessed_at', 'message': 'aggregate assessment postdates the packet'})
    return errors


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


def group_field_checks(rows):
    """Retain every owner-qualified row for a shared record/field."""
    groups = {}
    for row in rows:
        groups.setdefault((row['entity_type'], row['entity_id'], row['path']), []).append(row)
    return groups


def subject_owns(subject, kind, record):
    sk, ident = subject['kind'], subject['id']
    if sk == 'model':
        return (kind == 'model' and record.get('id') == ident or record.get('model_id') == ident
                or ident in record.get('model_ids', []))
    if sk == 'provider':
        return kind == 'provider' and record.get('id') == ident or record.get('provider_id') == ident
    if sk == 'product':
        return (kind in {'access', 'price', 'behavior', 'release'}
                and record.get('provider_id') == subject['identity']['provider_id']
                and record.get('product') == subject['identity']['product'])
    return False


def primary_field(kind, path):
    return (kind in {'access', 'price'} or
            kind == 'model' and path.split('/')[1] in {'identity', 'specifications', 'additional_specifications', 'licensing', 'local_inference'} or
            kind == 'provider' and path.split('/')[1] not in {'reliability', 'limitations', 'notes'})


def qualifying_field_checks(change, path, groups, run, state, sources, observations, packet_date, *, positive=False):
    """Each eligible row must independently satisfy all support requirements.

    No evidence or positive/primary status is pooled across rows. This function
    never edits check results. Sorting only the returned references makes later
    selection deterministic without changing the input accounting order.
    """
    kind, record = change['kind'], change['record']
    rows = groups.get((kind, record['id'], path), [])
    if 'subjects' in run:
        owners = {(s['kind'], s['id']) for s in run['subjects'] if subject_owns(s, kind, record)}
        eligible = lambda row: (row.get('subject_kind'), row.get('subject_id')) in owners
    else:
        models = ({record['id']} if kind == 'model' else
                  {r.get('model_id') for (k, _), r in state.items()
                   if k in {'access', 'price'} and r.get('provider_id') == record['id']} if kind == 'provider' else
                  set(record.get('model_ids', [])) | {record.get('model_id')})
        models &= set(run['target_model_ids'])
        eligible = lambda row: row.get('model_id') in models
    accepted = []
    for row in rows:
        checked = row.get('checked_at')
        if (not eligible(row) or row['result'] in {'blocked', 'not_checked'}
                or positive and row['result'] != 'value'
                or not set(row['evidence_ids']) & set(change['evidence_ids'])
                or not checked or not run['created_at'] <= checked <= packet_date):
            continue
        expanded = {i for ident in row['evidence_ids']
                    for i in observations.get(ident, {}).get('source_ids', [ident])}
        if not expanded or any(not observations.get(ident, {}).get('source_ids', [ident]) for ident in row['evidence_ids']):
            continue
        if not all(i in sources and isinstance(sources[i].get('accessed_at'), str)
                   and checked <= sources[i]['accessed_at'] <= packet_date for i in expanded):
            continue
        if primary_field(kind, path) and not any(sources[i]['source_type'] == 'primary' for i in expanded):
            continue
        accepted.append(row)
    return sorted(accepted, key=lambda row: (row.get('model_id', ''), row.get('subject_kind', ''),
                                            row.get('subject_id', ''), row['domain']))


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
