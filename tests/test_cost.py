from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import math
import pytest
from explorer.cost import estimate, PEAK_CONDITION
from explorer.data import load


@pytest.fixture(scope='module')
def data():
    return load()


def offer(data, model, tier='Standard', condition=None):
    return next(p for p in data['price'].values() if p['model_id'] == model and p['tier'] == tier
                and (condition is None or condition in ' '.join(p['conditions'])))


def calc(data, price, **kwargs):
    return estimate(price, data['access'].values(), input_tokens=kwargs.pop('input_tokens', 1000),
                    output_tokens=kwargs.pop('output_tokens', 1000), as_of=kwargs.pop('as_of', '2026-10-07'), **kwargs)


def test_cached_tokens_not_double_counted(data):
    p = offer(data, 'gpt-6-astra', condition='<=272000')
    r = calc(data, p, cached_tokens=400, cache_write_tokens=100)
    assert r['supported'] and Decimal(r['total']) == Decimal('0.05665')
    assert {c['component']: c['tokens'] for c in r['components']} == {'input': 500, 'output': 1000, 'cached': 400, 'write': 100}
    assert not calc(data, p, cached_tokens=1001)['supported']
    assert not calc(data, p, cached_tokens=900, cache_write_tokens=101)['supported']


@pytest.mark.parametrize('value', [-1, 1.5, float('nan'), float('inf'), True, '100'])
def test_invalid_token_counts(data, value):
    assert not calc(data, offer(data, 'gpt-6-astra', condition='<=272000'), input_tokens=value)['supported']


def test_context_boundary_and_full_request_long_rate(data):
    short = offer(data, 'gpt-6-astra', condition='<=272000')
    long = offer(data, 'gpt-6-astra', condition='>272000')
    assert calc(data, short, input_tokens=272000)['supported']
    assert not calc(data, long, input_tokens=272000)['supported']
    assert not calc(data, short, input_tokens=272001)['supported']
    r = calc(data, long, input_tokens=272001, cached_tokens=272000)
    assert r['supported'] and Decimal(r['total']) == Decimal('0.61902')


def test_google_long_context_and_future_effective_offer(data):
    short = offer(data, 'gemini-3-1-pro-preview', 'paid_standard', '<= 200,000')
    long = offer(data, 'gemini-3-1-pro-preview', 'paid_standard', '> 200,000')
    assert calc(data, short, input_tokens=200000)['supported']
    assert not calc(data, long, input_tokens=200000)['supported']
    assert calc(data, long, input_tokens=200001)['supported']
    future = next(p for p in data['price'].values() if p['model_id'] == 'gemini-3-8-flash' and p['effective_from'] == '2027-01-01')
    assert not calc(data, future)['supported']
    assert calc(data, future, as_of='2027-01-01')['supported']
    intro = next(p for p in data['price'].values() if p['model_id'] == 'gemini-3-8-flash' and p['tier'] == 'paid_standard' and not p['effective_from'])
    assert not calc(data, intro, as_of='2027-01-01')['supported']


def test_minimax_priority_boundary(data):
    short = offer(data, 'minimax-m3', 'priority_short')
    long = offer(data, 'minimax-m3', 'priority_long')
    assert calc(data, short, input_tokens=512000)['supported']
    assert not calc(data, short, input_tokens=512001)['supported']
    assert calc(data, long, input_tokens=512001)['supported']


def test_cache_write_ttls_and_missing_cache(data):
    p = offer(data, 'claude-opus-5-5')
    r = calc(data, p, cached_tokens=400, cache_write_5m_tokens=100, cache_write_1h_tokens=100)
    assert r['supported'] and Decimal(r['total']) == Decimal('0.02298')
    assert not calc(data, p, cache_write_tokens=100)['supported']
    batch = offer(data, 'claude-sonnet-5-5', 'Batch')
    assert calc(data, batch)['supported']
    assert not calc(data, batch, cached_tokens=1)['supported']
    deepseek = offer(data, 'deepseek-v4-1-flash', 'off_peak')
    assert not calc(data, deepseek, cache_write_tokens=100, request_time=datetime(2026, 10, 7, 12, tzinfo=timezone.utc))['supported']


def test_conflicting_cache_tariff_blocks_only_requested_cache_reads(data):
    p = offer(data, 'claude-sonnet-5-5')
    ordinary = calc(data, p)
    assert ordinary['supported'] and Decimal(ordinary['total']) == Decimal('0.012')
    assert calc(data, p, cache_write_5m_tokens=100)['supported']
    cached = calc(data, p, cached_tokens=1)
    assert not cached['supported']
    assert any('No documented numeric cached rate' in reason for reason in cached['reasons'])


def test_batch_flex_are_exact_offers(data):
    for tier in ['Batch', 'Flex']:
        p = offer(data, 'gpt-6-astra', tier)
        assert Decimal(calc(data, p)['total']) == Decimal('0.03')
    assert not calc(data, offer(data, 'gpt-6-astra', 'Ultrafast'))['supported']  # undefined short-context boundary


def test_peak_windows_holidays_and_weekends(data):
    peak = offer(data, 'deepseek-v4-1-flash', 'peak')
    off = offer(data, 'deepseek-v4-1-flash', 'off_peak')
    inside = datetime(2026, 10, 7, 6, tzinfo=timezone.utc)
    assert not calc(data, peak)['supported']
    assert not calc(data, peak, request_time=inside)['supported']
    assert calc(data, peak, request_time=inside, chinese_public_holiday=False)['supported']
    assert not calc(data, off, request_time=inside, chinese_public_holiday=False)['supported']
    assert calc(data, off, request_time=inside, chinese_public_holiday=True)['supported']
    assert calc(data, off, as_of='2026-10-10', request_time=datetime(2026, 10, 10, 6, tzinfo=timezone.utc))['supported']
    assert calc(data, off, request_time=datetime(2026, 10, 7, 10, tzinfo=timezone.utc))['supported']


def test_unknown_media_subscriptions_and_route_missing(data):
    cases = [next(p for p in data['price'].values() if p['billing_method'] == 'subscription'),
             offer(data, 'gemini4argon', 'announced_intro'),
             offer(data, 'gpt-live-1'),
             offer(data, 'veo-3-1-generate-preview', 'paid_standard')]
    for p in cases:
        result = calc(data, p)
        assert not result['supported'] and result['reasons']
    unlinked = deepcopy(offer(data, 'gpt-6-astra', condition='<=272000'))
    unlinked['id'] = 'price-unlinked-test-fixture'
    assert not calc(data, unlinked)['supported']
    p = deepcopy(offer(data, 'gpt-6-astra', condition='<=272000'))
    p['rates'][0]['amount'] = None
    assert not calc(data, p)['supported']
    p['rates'][0]['amount'] = 0
    assert calc(data, p)['supported']  # documented zero is distinct from unknown
    p['conditions'].append('Unspecified long-context surcharge')
    assert not calc(data, p)['supported']


def test_currency_unit_rate_conditions_and_zero_usage(data):
    p = deepcopy(offer(data, 'gpt-6-astra', condition='<=272000'))
    p['rates'][0]['currency'] = 'EUR'
    assert not calc(data, p)['supported']
    for rate in p['rates']:
        rate['currency'] = 'EUR'
    assert calc(data, p)['currency'] == 'EUR'
    p['rates'][0]['unit'] = 'per 1000 requests'
    assert not calc(data, p)['supported']
    p = deepcopy(offer(data, 'gpt-6-astra', condition='<=272000'))
    p['rates'][0]['conditions'] = ['Minimum 100K input']
    assert not calc(data, p)['supported']
    p = offer(data, 'gpt-6-astra', condition='<=272000')
    assert calc(data, p, input_tokens=0, output_tokens=0)['total'] == '0'
    assert not calc(data, p, as_of='2026-10-05')['supported']
