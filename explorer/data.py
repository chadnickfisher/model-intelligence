from datetime import date
from tools.knowledge import ROOT, canonical, read

REPO_URL = 'https://github.com/chadnickfisher/model-intelligence'
UNKNOWN = 'Unknown / not established'


def load(root=ROOT):
    records = canonical(root)
    result = {kind: {} for kind in ['model', 'provider', 'price', 'access', 'release', 'source', 'observation', 'task', 'alias', 'behavior', 'access_coverage', 'benchmark', 'research_coverage']}
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
    return route_status(model, data, kind) == 'Documented'


def route_kinds(route):
    ms = {m.lower().replace('-', '_') for m in route['methods']}
    out = set()
    if any('api' in m for m in ms): out.add('API')
    if any('subscription' in m for m in ms): out.add('Subscription')
    if any('chat' in m for m in ms): out.add('Chat app')
    if ms & {'weight_distribution', 'local_weights', 'download_self_host'}: out.add('Download weights')
    if ms & {'local_weights', 'download_self_host'}: out.add('Run locally')
    if 'dedicated_host' in ms: out.add('Dedicated hosting')
    if not out: out.add('Client / product')
    return out


def active_route(route):
    if route.get('availability') in {'unknown', 'unavailable', 'deprecated'}: return False
    # Legacy negative statements must never become positive route flags.
    status = route['status'].lower()
    return not any(s in status for s in ['not yet available', 'no first-party hosted entitlement', 'deprecated', 'unavailable'])


def model_routes(model, data, active_only=False):
    rows = [data['access'][i] for i in model['access_ids']]
    return [r for r in rows if active_route(r)] if active_only else rows


def route_status(model, data, kind):
    if kind in {'Local', 'Run locally'}:
        if model['local_inference']['availability'] == 'available': return 'Documented'
    if any(kind in route_kinds(r) for r in model_routes(model, data, True)): return 'Documented'
    coverage = next((c for c in data.get('access_coverage', {}).values() if c['model_id'] == model['id']), None)
    category = {'API':'api','Subscription':'subscription','Chat app':'chat','Download weights':'download','Local':'self_hosted','Run locally':'self_hosted'}.get(kind)
    if coverage and category:
        finding = coverage['categories'][category]
        if finding['state'] == 'unavailable' and finding['evidence_ids']: return 'Unavailable (documented)'
    return 'Not yet documented'


def route_prices(route, data):
    return [data['price'][i] for i in route['price_ids'] if i in data['price']
            and data['price'][i]['provider_id'] == route['provider_id']
            and data['price'][i]['model_id'] == route['model_id']]


def current_price(price, as_of=None):
    as_of = as_of or date.today().isoformat()
    return (price['status'] == 'current' and (not price['effective_from'] or price['effective_from'] <= as_of)
            and (not price['effective_to'] or as_of <= price['effective_to']))


def comparable_api_offers(model, data, *, input_tokens=1000, output_tokens=1000,
                          currency='USD', as_of=None):
    """Concrete supported routes for one request; never convert currencies or credits."""
    from explorer.cost import estimate
    rows = []
    for ident in model['price_ids']:
        price = data['price'][ident]
        if not current_price(price, as_of):
            continue
        result = estimate(price, data['access'].values(), input_tokens=input_tokens,
                          output_tokens=output_tokens, as_of=as_of)
        if result['supported'] and result['currency'] == currency:
            rows.append({'price_id': ident, 'total': result['total'], 'currency': currency})
    return rows


def route_label(route, data):
    provider = data['provider'].get(route['provider_id'], {}).get('name', 'Self hosted')
    return provider + ' · ' + (route['product'] or ', '.join(sorted(route_kinds(route))))


def billing_summary(route, data):
    prices = route_prices(route, data)
    if 'Download weights' in route_kinds(route):
        return 'Weight download; running costs depend on hardware / hosting'
    methods = {p['billing_method'] for p in prices}
    labels = {'metered-api':'Usage billed separately', 'subscription':'Subscription; API entitlement must be checked',
              'prepaid-credits':'Included / purchased credits; not a token price', 'compute':'Compute billed by documented units'}
    if methods: return '; '.join(labels.get(m, m.replace('-', ' ')) for m in sorted(methods))
    if 'Subscription' in route_kinds(route): return 'Subscription route; price / entitlement not yet established'
    return 'Price not yet documented for this route'


def findings(model, task=None, include_related=False):
    return claims(model, task, include_related)


def task_label(data, task):
    return data['task'].get(task, {}).get('label', task.replace('.', ' / ').replace('_', ' '))


def judgment_label(data, judgment):
    tasks = judgment['task_ids'] + judgment['related_task_ids']
    return ', '.join(task_label(data, t) for t in tasks) or judgment['provenance'].get('original_task', 'Performance observation').replace('-', ' ')


def task_coverage(data):
    return {t: {scope: sum(any(t in j['task_ids'] + j['related_task_ids'] and j['scope'] == scope
                             for j in m['capabilities']) for m in data['model'].values())
                for scope in ['direct','compound','unresolved']} for t in data['task']}


def behavior_findings(model, data, highlights=False):
    rows=[b for b in data.get('behavior', {}).values() if model['id'] in b['model_ids']]
    if highlights:
        rows=[b for b in rows if b.get('research_details',{}).get('layer') not in {'client_harness','client_product','serving_infrastructure','model_release'}]
    return sorted(rows,
                  key=lambda b: b['reported_at'] or b['observed_at'], reverse=True)


def benchmark_findings(model, data, judgment_id=None):
    return [b for b in data.get('benchmark', {}).values() if b['model_id'] == model['id']
            and (judgment_id is None or judgment_id in b['judgment_ids'])]


def benchmark_compatibility(records):
    """Comparability requires documented matching setups, never just a shared test name."""
    if len(records) < 2:
        return 'No matched measurements for comparison'
    if all(r.get('model_id') for r in records) and len({r['model_id'] for r in records}) < 2:
        return 'Measurements cover one model; no cross-model comparison'
    keys = ('name', 'version', 'metric', 'unit', 'direction')
    if len({tuple(r['benchmark'][k] for k in keys) for r in records}) > 1:
        return 'Different benchmark versions or metrics; not comparable'
    fields = ('harness', 'effort', 'provider_id', 'tools')
    if any(r['benchmark']['version'] is None or not r['model_version']
           or any(r[k] is None for k in fields) for r in records):
        return 'Configuration metadata incomplete; comparability not established'
    setups = {tuple(str(r[k]) for k in fields) + (str(r['conditions']), r['evidence_class']) for r in records}
    if len(setups) > 1:
        return 'Different configurations or evidence classes; not a controlled comparison'
    return 'Matching documented setups; dated results still do not establish general ability'


def confidence_trace(data, judgment):
    """Expose the evidence behind a recorded confidence, without recalculating an ability score."""
    support = sources(data, judgment['supporting_evidence_ids'])
    contradiction = sources(data, judgment['contradictory_evidence_ids'])
    return {'recorded_confidence': judgment['confidence'],
            'supporting_sources': [{'title': s['title'], 'type': s['source_type'],
                                   'checked': s['accessed_at'], 'published': s['published_at'],
                                   'limitations': s['limitations']} for s in support],
            'contradictory_sources': [{'title': s['title'], 'type': s['source_type'],
                                      'checked': s['accessed_at'], 'published': s['published_at'],
                                      'limitations': s['limitations']} for s in contradiction],
            'conditions': judgment['conditions'], 'rationale_notes': judgment['evidence_notes'],
            'observed_at': judgment['observed_at'],
            'caution': 'Source count and benchmark score do not determine confidence. No listed contradiction means none was located in this pass.'}


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
        if search and search.lower() not in (model['id'] + ' ' + ident['name'] + ' ' + ident['family']).lower():
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
            'API': route_status(model, data, 'API'), 'Subscription': route_status(model, data, 'Subscription'),
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
