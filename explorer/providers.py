"""Provider discovery from canonical routes and prices; no inferred entitlements."""
import json

from .data import active_route, current_price, route_kinds


BILLING = {'metered-api': 'Metered API', 'subscription': 'Subscription',
           'prepaid-credits': 'Credits', 'compute': 'Compute', 'mixed': 'Mixed billing',
           'free': 'Free', 'self-hosted': 'Self-hosted'}
SERVICES = ('API', 'Gateway', 'Subscription', 'Chat app', 'Dedicated hosting',
            'Download weights', 'Client / product')


def readable_values(values):
    """Unwrap recorded summaries, omitting status-only sentinels."""
    out = []
    for value in values or []:
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    value = parsed
            except (ValueError, TypeError):
                pass
        if isinstance(value, dict):
            value = value.get('summary') or value.get('description')
        if not value or value in ('unknown', 'not_exhaustively_verified', 'not_verified'):
            continue
        if isinstance(value, str):
            out.append(value)
    return list(dict.fromkeys(out))


def provider_routes(data, provider_id, include_inactive=False):
    return [r for r in data['access'].values() if r['provider_id'] == provider_id
            and (include_inactive or active_route(r))]


def list_provider_offers(data, provider_id, include_inactive=False):
    """Provider-wide plans keep null model scope; exact offers require exact joins."""
    routes = provider_routes(data, provider_id, include_inactive)
    return sorted([p for p in data['price'].values() if p['provider_id'] == provider_id
                   and (include_inactive or current_price(p))
                   and (p['model_id'] is None or any(
                       r['model_id'] == p['model_id'] and p['id'] in r['price_ids'] for r in routes))],
                  key=lambda p: (p['model_id'] is not None, p['product'] or '', p['tier'] or '', p['id']))


def service_types(routes):
    kinds = set()
    for route in routes:
        kinds.update(route_kinds(route) - {'Run locally'})
        methods = {m.lower().replace('-', '_') for m in route['methods']}
        if 'cloud_model_host' in methods:
            kinds.add('Dedicated hosting')
            kinds.discard('Client / product')
        if 'gateway_api' in methods or route.get('research_details', {}).get('route_class') == 'gateway_metered_api':
            kinds.add('Gateway')
    return kinds


def get_provider(data, provider_id, include_inactive=False):
    profile = data['provider'][provider_id]
    routes = provider_routes(data, provider_id, include_inactive)
    active = [r for r in routes if active_route(r)]
    offers = list_provider_offers(data, provider_id, include_inactive)
    # Model membership in a provider profile is not hosted-inference evidence.
    models = {}
    for route in active:
        if route['model_id'] not in data['model']:
            continue
        for kind in service_types([route]):
            models.setdefault(kind, set()).add(route['model_id'])
    return {'profile': profile, 'routes': routes, 'offers': offers,
            'services': service_types(active), 'models': models,
            'behavior': [b for b in data['behavior'].values() if b['provider_id'] == provider_id]}


def find_providers(data, *, search='', service=None, billing=None, currency=None,
                   roles=(), include_context=False, include_inactive=False):
    rows = []
    for ident in data['provider']:
        record = get_provider(data, ident, include_inactive)
        profile = record['profile']
        if not include_context and (not record['routes'] or set(profile['roles']) == {'client'}):
            continue
        if service and service not in record['services']:
            continue
        offers = record['offers']
        if billing:
            offers = [p for p in offers if p['billing_method'] == billing]
        if currency:
            offers = [p for p in offers if any(r['currency'] == currency for r in p['rates'])]
        if (billing or currency) and not offers:
            continue
        if roles and not set(roles).intersection(profile['roles']):
            continue
        haystack = ' '.join([profile['name'], ident] + [r['product'] or '' for r in record['routes']]
                            + [(p['product'] or '') + ' ' + (p['tier'] or '') for p in record['offers']])
        if search.strip().casefold() not in haystack.casefold():
            continue
        rows.append(record)
    return sorted(rows, key=lambda r: r['profile']['name'].casefold())


def provider_watchouts(record):
    profile = record['profile']
    items = []
    for r in record['routes']:
        if active_route(r):
            items += [(r['product'] or 'Access route') + ': ' + v
                      for v in readable_values(r.get('conditions', []) + r.get('restrictions', []))]
    items += readable_values(profile['rate_limits'] + profile['limitations'])
    return list(dict.fromkeys(items))
