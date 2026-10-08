"""Exact-task comparison summaries and provider-qualified text costs."""
from decimal import Decimal

from .data import comparable_api_offers, current_price, model_routes, route_kinds, route_status
from .cost import estimate
from .presentation import task_assessment


def comparison_assessments(model, data, task=None):
    rows = [a for a in data.get('task_assessment', {}).values()
            if a['model_id'] == model['id'] and a.get('aggregate')]
    if len({a['task_id'] for a in rows}) != len(rows):
        raise ValueError('Duplicate canonical model/task assessment')
    rows.sort(key=lambda a: data['task'][a['task_id']]['label'].casefold())
    suitable = [a for a in rows if a['aggregate']['suitability'] in {'high', 'medium'}]
    other = [a for a in rows if a['aggregate']['suitability'] in {'low', 'disputed'}]
    assessment = task_assessment(model, data, task) if task else None
    return {
        'assessment': assessment,
        'aggregate': assessment.get('aggregate') if assessment else None,
        'suitable': suitable,
        'other': other,
        'fit_counts': {level: sum(a['aggregate']['suitability'] == level for a in suitable)
                       for level in ('high', 'medium')},
        'confidence_counts': {level: sum(a['aggregate']['evidence_confidence'] == level for a in suitable)
                              for level in ('high', 'medium', 'low')},
    }


def comparison_offers(model, data, input_tokens, output_tokens):
    """One currency and ordinary API billing; never mix subscriptions or timed tiers."""
    rows = comparable_api_offers(model, data, input_tokens=input_tokens,
                                 output_tokens=output_tokens, currency='USD')
    special_modes = ('batch', 'flex', 'priority', 'off-peak', 'off_peak', 'peak')
    rows = [row for row in rows
            if not any(mode in (data['price'][row['price_id']]['tier'] or '').lower()
                       for mode in special_modes)]
    return sorted(rows, key=lambda row: (
        data['provider'][data['price'][row['price_id']]['provider_id']]['name'].casefold(),
        (data['price'][row['price_id']]['tier'] or '').casefold(), row['price_id']))


def usd_text(value):
    text = format(Decimal(str(value)), 'f')
    whole, _, fraction = text.partition('.')
    return '$' + whole + '.' + fraction.rstrip('0').ljust(2, '0')


def comparison_cost_options(model, data, input_tokens, output_tokens):
    """Keep every fallback tied to a current, evidenced model/provider route.

    Shared plans require an explicit route price link; provider identity alone
    never establishes model entitlement. Only request estimates enter cost bars.
    """
    estimates = {o['price_id']: o for o in comparison_offers(model, data, input_tokens, output_tokens)}
    routes = model_routes(model, data, True)
    linked = {}
    for route in routes:
        if route['model_id'] != model['id'] or not route.get('evidence_ids'):
            continue
        for ident in route['price_ids']:
            price = data['price'].get(ident)
            if (not price or not current_price(price) or not price['evidence_ids']
                    or price['provider_id'] != route['provider_id']
                    or price['model_id'] not in (None, model['id'])):
                continue
            # An unspecified model is valid for an explicitly linked shared plan,
            # but cannot establish a model-specific API or compute rate.
            if price['model_id'] is None and price['billing_method'] != 'subscription':
                continue
            linked.setdefault(ident, []).append(route)
    options = []
    for ident, own_routes in linked.items():
        price = data['price'][ident]
        kind = price['billing_method']
        if kind == 'metered-api':
            if not any('API' in route_kinds(r) for r in own_routes):
                continue
            if any(mode in (price['tier'] or '').lower()
                   for mode in ('batch', 'flex', 'priority', 'off-peak', 'off_peak', 'peak')):
                continue
            result = estimates.get(ident)
            reasons = [] if result else estimate(price, own_routes, input_tokens=input_tokens,
                                                  output_tokens=output_tokens).get('reasons', [])
            options.append({'kind': 'estimate' if result else 'api_rates', 'price_id': ident,
                            'route_ids': [r['id'] for r in own_routes],
                            'total': result['total'] if result else None, 'reasons': reasons})
        elif kind in {'subscription', 'compute'}:
            required = 'Subscription' if kind == 'subscription' else 'Dedicated hosting'
            if not any(required in route_kinds(r) for r in own_routes):
                continue
            options.append({'kind': kind, 'price_id': ident,
                            'route_ids': [r['id'] for r in own_routes], 'total': None, 'reasons': []})
    rank = {'estimate': 0, 'api_rates': 1, 'subscription': 2, 'compute': 3}
    options.sort(key=lambda o: (rank[o['kind']],
        data['provider'][data['price'][o['price_id']]['provider_id']]['name'].casefold(), o['price_id']))
    if route_status(model, data, 'Run locally') == 'Documented':
        options.append({'kind': 'local', 'price_id': None, 'route_ids': [], 'total': None, 'reasons': []})
    return options


def estimate_unavailable_reason(reasons):
    """Explain blocked calculations without exposing raw metadata structures."""
    messages = []
    for reason in reasons:
        if 'Cannot interpret documented route' in reason:
            message = 'Provider limits are not precise enough to verify this workload.'
        elif 'Request exceeds documented route' in reason:
            message = 'This workload exceeds a documented provider limit.'
        elif 'condition' in reason.lower() or 'requires' in reason.lower():
            message = 'Pricing conditions need additional information for this workload.'
        elif 'rate' in reason.lower() or 'metric/unit' in reason.lower():
            message = 'Published billing units or rates do not support this text-workload estimate.'
        else:
            message = 'A compatible request estimate is not established for this offer.'
        if message not in messages:
            messages.append(message)
    return ' '.join(messages) or 'No compatible standard USD request estimate is established.'
