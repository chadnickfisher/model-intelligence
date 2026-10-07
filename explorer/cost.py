"""Conservative text-token estimator. Reads exact canonical rates, never invents discounts."""
from datetime import date, datetime, timezone
from decimal import Decimal
import math
import re

UNITS = {'per 1 million tokens', 'per 1 million text tokens', 'per_1M_tokens', 'per_1000000_tokens', 'per 1M tokens'}
METRICS = {'input': 'input', 'input_all_supported_modalities': 'input', 'output': 'output',
           'output_including_thinking': 'output', 'cached_input': 'cached', 'cache_read': 'cached',
           'cache_write': 'write', 'cache_write_5m': 'write_5m', 'cache_write_1h': 'write_1h'}
ALLOWED_CONDITIONS = {
    'Tool fees and regional/FedRAMP uplift',
    'Tool charges; enterprise provisioned capacity',
    'Cached-input storage currently labeled limited-time free; promotional expired rates are excluded.',
    'Default standard tier; regional inference, batch and priority may have different rates.',
    'Gemma 4 pricing section; paid tier unavailable. Quota limited, data-use terms differ from paid Gemini API.',
    '50% input/output discount; cache/tool charges should be checked separately',
}
PEAK_CONDITION = 'Peak weekdays 01:00–04:00 and 06:00–10:00 UTC, excluding Chinese public holidays. Off-peak all other times. Reasoning and final tokens contribute to output billing.'


def routes_for_price(price, access):
    return [a for a in access if price['id'] in a['price_ids']
            and a['provider_id'] == price['provider_id'] and a['model_id'] == price['model_id']
            and any('api' in method.lower() for method in a['methods']) and a['evidence_ids']]


def threshold(text):
    # Supports only explicit documented input/prompt comparisons, including tier text.
    match = re.match(r'^(?:input(?: length)?|prompt)\s*(<=|>=|<|>)\s*([\d,]+)(k)?(?: tokens)?(?:[.;].*)?$', text, re.I)
    if not match:
        return None
    return match[1], int(match[2].replace(',', '')) * (1000 if match[3] else 1)


def applicable_threshold(text, total):
    rule = threshold(text)
    if not rule:
        return None
    op, value = rule
    return {'<': total < value, '<=': total <= value, '>': total > value, '>=': total >= value}[op]


def estimate(price, access, *, input_tokens, output_tokens, cached_tokens=0, cache_write_tokens=0,
             cache_write_5m_tokens=0, cache_write_1h_tokens=0, as_of=None,
             request_time=None, chinese_public_holiday=None):
    """Input includes cached/write tokens; output includes billable reasoning. No model calls."""
    amounts = {'input': input_tokens, 'output': output_tokens, 'cached': cached_tokens,
               'write': cache_write_tokens, 'write_5m': cache_write_5m_tokens, 'write_1h': cache_write_1h_tokens}
    errors = []
    warnings = ['Text-token subtotal only. Taxes, tools, storage, regional uplifts, payment fees, retries and other modalities are excluded.',
                'Output must include all billable reasoning/thinking tokens. Unknown effective dates and account eligibility are not verified.']
    for kind, value in amounts.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or int(value) != value:
            errors.append(f'{kind} tokens must be finite, non-negative integers')
    if errors:
        return {'supported': False, 'reasons': errors}
    if cached_tokens + cache_write_tokens + cache_write_5m_tokens + cache_write_1h_tokens > input_tokens:
        errors.append('Cached reads and cache writes must be disjoint subsets of total input tokens')
    amounts['input'] -= cached_tokens + cache_write_tokens + cache_write_5m_tokens + cache_write_1h_tokens
    if price['billing_method'] != 'metered-api':
        errors.append('This is not a metered API token offer; subscriptions/credits cannot be converted to token rates')
    if price['status'] != 'current':
        errors.append('Offer is unknown or historical, not a documented current offer')
    if not price['model_id'] or not price['evidence_ids']:
        errors.append('Exact model identity and price evidence are required')
    routes = routes_for_price(price, access)
    if not routes:
        errors.append('No explicit model/provider API access route links to this price record')
    as_of = as_of or date.today().isoformat()
    date.fromisoformat(as_of)
    if as_of < price['verified_at'] and not price['effective_from']:
        errors.append('Effective start is unknown; this offer cannot establish a price before its verification date')
    if price['effective_from'] and as_of < price['effective_from']:
        errors.append(f"Offer starts on {price['effective_from']}")
    if price['effective_to'] and as_of > price['effective_to']:
        errors.append(f"Offer ended on {price['effective_to']}")
    if price['region']:
        warnings.append(f"Offer region: {price['region']}; no regional substitution is made")
    conditions = price['conditions'] + price['notes']
    # Tier itself may document a prompt boundary. Tier names alone never imply a discount.
    tier = price['tier'] or ''
    for fragment in re.findall(r'(?:prompt|input)\s*[<>]=?\s*[\d,]+k?(?: tokens)?', tier, re.I):
        conditions = conditions + [fragment]
    for condition in conditions:
        applicable = applicable_threshold(condition, input_tokens)
        if applicable is False:
            errors.append(f'Request does not satisfy documented condition: {condition}')
        elif applicable is True or condition in ALLOWED_CONDITIONS:
            continue
        elif condition == PEAK_CONDITION:
            if not isinstance(request_time, datetime) or request_time.tzinfo is None:
                errors.append('Peak/off-peak pricing requires an explicit timezone-aware request time')
                continue
            utc = request_time.astimezone(timezone.utc)
            if utc.date().isoformat() != as_of:
                errors.append('Request UTC date must match the selected price effective date')
                continue
            inside = utc.weekday() < 5 and (1 <= utc.hour < 4 or 6 <= utc.hour < 10)
            if inside and chinese_public_holiday is None:
                errors.append('Chinese public-holiday status is required to resolve this peak window')
            else:
                expected = 'peak' if inside and not chinese_public_holiday else 'off_peak'
                if tier != expected:
                    errors.append(f'Request time requires {expected}, selected offer is {tier}')
        else:
            errors.append(f'Calculation does not implement this documented condition: {condition}')
    rate_map = {}
    for rate in price['rates']:
        if rate['unit'] not in UNITS or rate['metric'] not in METRICS:
            errors.append(f"Unsupported metric/unit: {rate['metric']} / {rate['unit']}; no media or subscription conversion")
            continue
        key = METRICS[rate['metric']]
        if key in rate_map:
            errors.append(f'Duplicate or ambiguous rate for {key}')
        rate_map[key] = rate
    components, currencies = [], set()
    for kind, quantity in amounts.items():
        if not quantity:
            continue
        rate = rate_map.get(kind)
        if rate is None or rate['amount'] is None or rate['currency'] is None:
            errors.append(f'No documented numeric {kind} rate and currency for the requested tokens')
            continue
        if rate['conditions']:
            errors.append(f"Rate-specific conditions are not implemented: {rate['conditions']}")
            continue
        amount = Decimal(str(rate['amount']))
        if not amount.is_finite() or amount < 0:
            errors.append(f'Invalid {kind} rate')
            continue
        currencies.add(rate['currency'])
        cost = Decimal(int(quantity)) * amount / Decimal(1_000_000)
        components.append({'component': kind, 'tokens': int(quantity), 'rate_per_million': str(amount), 'cost': str(cost), 'currency': rate['currency']})
    if len(currencies) > 1:
        errors.append('Mixed currencies cannot be added; no exchange rate is assumed')
    if not components and not errors:
        known = {r['currency'] for r in rate_map.values() if r['amount'] is not None and r['currency'] is not None}
        if len(known) != 1:
            errors.append('A single documented currency is required, even for zero usage')
        currencies = known
    if errors:
        return {'supported': False, 'reasons': list(dict.fromkeys(errors))}
    return {'supported': True, 'total': str(sum((Decimal(c['cost']) for c in components), Decimal(0))),
            'currency': next(iter(currencies)), 'components': components, 'warnings': warnings,
            'conditions': price['conditions'], 'price_id': price['id'], 'route_ids': [r['id'] for r in routes],
            'verified_at': price['verified_at'], 'as_of': as_of, 'tier': price['tier']}
