from datetime import date
from tools.knowledge import ROOT, canonical, read

REPO_URL = 'https://github.com/chadnickfisher/model-intelligence'
UNKNOWN = 'Unknown / not established'


def load(root=ROOT):
    records = canonical(root)
    result = {kind: {} for kind in ['model', 'provider', 'price', 'access', 'release', 'source', 'observation', 'task', 'alias']}
    result['paths'] = {}
    for (kind, ident), (path, record) in records.items():
        result[kind][ident] = record
        result['paths'][(kind, ident)] = path
    return result


def show(value):
    if value is None:
        return UNKNOWN
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if isinstance(value, dict):
        return '; '.join(f'{k}: {show(v)}' for k, v in value.items())
    if isinstance(value, list):
        return '; '.join(show(v) for v in value) if value else 'None recorded in this pass'
    return str(value)


def link(path):
    return f'{REPO_URL}/blob/main/{path}'


def context_tokens(model, extended=False):
    spec = model['specifications']['context_window']
    if spec['status'] in ['unknown', 'conflicting']:
        return None
    value = spec['value']
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, dict):
        return value.get('extended_tokens') if extended else value.get('native_tokens')
    return None


def open_weights(model):
    value = model['additional_specifications'].get('weights', {}).get('value')
    if isinstance(value, dict):
        return value.get('downloadable')
    if value == 'open':
        return True
    if value == 'closed':
        return False
    return None


def methods(model, data):
    return {m.lower().replace('-', '_') for ident in model['access_ids'] for m in data['access'][ident]['methods']}


def has_route(model, data, kind):
    ms = methods(model, data)
    if kind == 'API':
        return any('api' in m for m in ms)
    if kind == 'Subscription':
        return any('subscription' in m for m in ms)
    return model['local_inference']['availability'] == 'available'


def claims(model, task=None, include_related=False, confidence=None):
    rows = model['capabilities']
    if task:
        rows = [j for j in rows if task in j['task_ids'] or include_related and task in j['related_task_ids']]
    if confidence:
        rows = [j for j in rows if j['confidence'] in confidence]
    return rows


def filter_models(data, *, vendors=(), families=(), task=None, include_related=False,
                  confidence=(), routes=(), licenses=(), minimum_context=0,
                  include_unknown_context=False, input_modalities=(), output_modalities=(),
                  weights='Any', search=''):
    result = []
    for model in data['model'].values():
        ident = model['identity']
        if vendors and ident['creator'] not in vendors or families and ident['family'] not in families:
            continue
        if search and search.lower() not in (model['id'] + ' ' + ident['name']).lower():
            continue
        if (task or confidence) and not claims(model, task, include_related, confidence):
            continue
        if routes and not all(has_route(model, data, r) for r in routes):
            continue
        if licenses and (model['licensing']['name'] or UNKNOWN) not in licenses:
            continue
        ctx = context_tokens(model)
        if minimum_context and (ctx is None and not include_unknown_context or ctx is not None and ctx < minimum_context):
            continue
        mod = model['specifications']['modalities']['value'] or {}
        if not set(input_modalities) <= set(mod.get('input', [])) or not set(output_modalities) <= set(mod.get('output', [])):
            continue
        weight = open_weights(model)
        if weights == 'Downloadable' and weight is not True or weights == 'Closed' and weight is not False or weights == 'Unknown' and weight is not None:
            continue
        result.append(model)
    return result


def summary(model, data):
    return {'ID': model['id'], 'Model': model['identity']['name'], 'Vendor': model['identity']['creator'],
            'Family': model['identity']['family'], 'Status': model['identity']['status'],
            'Native context tokens': context_tokens(model), 'Extended context tokens': context_tokens(model, True),
            'API': has_route(model, data, 'API'), 'Subscription': has_route(model, data, 'Subscription'),
            'Local': model['local_inference']['availability'], 'Downloadable weights': show(open_weights(model)),
            'License': model['licensing']['name'] or UNKNOWN, 'Verified': model['verified_at'],
            'Canonical': link(data['paths'][('model', model['id'])])}


def comparison(data, ids, task=None, include_related=False):
    if not 2 <= len(ids) <= 5 or len(set(ids)) != len(ids):
        raise ValueError('Choose 2–5 distinct models')
    rows = []
    for ident in ids:
        model = data['model'][ident]
        judgments = claims(model, task, include_related)
        row = summary(model, data)
        row.update({'Task evidence': '\n'.join(f"{j['scope']} / {j['assessment']} / {j['confidence']} confidence: {j['judgment']}" for j in judgments) or UNKNOWN,
                    'Input modalities': show((model['specifications']['modalities']['value'] or {}).get('input')),
                    'Output modalities': show((model['specifications']['modalities']['value'] or {}).get('output')),
                    'Local hardware': show(model['local_inference']['hardware_notes'])})
        rows.append(row)
    return rows


def sources(data, ids):
    result = {}
    for ident in ids:
        if ident in data['source']:
            result[ident] = data['source'][ident]
        elif ident in data['observation']:
            result.update({s['id']: s for s in sources(data, data['observation'][ident]['source_ids'])})
    return list(result.values())
