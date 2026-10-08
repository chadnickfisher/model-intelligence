from copy import deepcopy

import pytest
from streamlit.testing.v1 import AppTest

from explorer.data import load
from explorer.providers import (find_providers, get_provider, list_provider_offers,
                                readable_values)
from tools.knowledge import ROOT


@pytest.fixture(scope='module')
def data():
    return load()


def test_downloads_do_not_establish_hosted_entitlement(data):
    record = get_provider(data, 'hugging-face')
    assert len(record['models']['Download weights']) == 22
    assert not record['models'].get('API')
    assert 'Dedicated hosting' in record['services']
    assert 'Gateway' in record['services']
    assert not find_providers(data, search='client-opencode')
    assert not find_providers(data, search='google-cli')
    assert [r['profile']['id'] for r in find_providers(data, search='client-opencode', include_context=True)] == ['client-opencode']


def test_exact_offers_require_provider_model_and_price_membership(data):
    fixture = deepcopy(data)
    record = get_provider(fixture, 'novita')
    price = next(p for p in record['offers'] if p['model_id'] == 'qwen3-coder-next')
    route = next(r for r in record['routes'] if price['id'] in r['price_ids'])
    route['availability'] = 'unavailable'
    assert price['id'] not in {p['id'] for p in list_provider_offers(fixture, 'novita')}
    assert price['id'] in {p['id'] for p in list_provider_offers(fixture, 'novita', True)}
    route['availability'] = 'documented'
    price['model_id'] = 'llama-4-scout'
    assert price['id'] not in {p['id'] for p in list_provider_offers(fixture, 'novita')}
    price['provider_id'] = 'opencode-zen'
    assert price['id'] not in {p['id'] for p in list_provider_offers(fixture, 'opencode-zen')}


def test_product_scoped_plans_and_filters(data):
    record = get_provider(data, 'opencode-zen')
    plans = [p for p in record['offers'] if p['billing_method'] == 'subscription']
    assert {p['tier'] for p in plans} == {'Go', 'Go Plus'}
    assert all(p['model_id'] is None and p['reset_cadence'] and p['overage'] for p in plans)
    assert not record['models'].get('Subscription')
    assert 'opencode-zen' in {r['profile']['id'] for r in find_providers(data, search='Go Plus', billing='subscription', currency='USD')}
    assert not find_providers(data, search='Novita', billing='subscription')
    assert 'hugging-face' in {r['profile']['id'] for r in find_providers(data, service='Download weights')}
    assert all('Download weights' in r['services'] for r in find_providers(data, service='Download weights'))
    assert not find_providers(data, search='Novita', currency='EUR')
    fixture = deepcopy(data)
    for price in fixture['price'].values():
        if price['provider_id'] == 'novita':
            price['effective_to'] = '2020-01-01'
    assert not find_providers(fixture, search='Novita', billing='metered-api')
    assert find_providers(fixture, search='Novita', billing='metered-api', include_inactive=True)


def test_readable_policies_and_provider_only_behavior(data):
    assert readable_values(['not_exhaustively_verified', '{"status":"partial","summary":"Route-dependent."}']) == ['Route-dependent.']
    for ident in data['provider']:
        record = get_provider(data, ident)
        assert all(b['provider_id'] == ident for b in record['behavior'])
        for ids in record['models'].values():
            assert ids <= set(data['model'])


def widget(elements, label):
    return next(e for e in elements if e.label == label)


def test_provider_page_filters_and_model_drilldown():
    app = AppTest.from_file(str(ROOT / 'streamlit_app.py'), default_timeout=45)
    app.query_params['view'] = 'providers'
    app.query_params['provider'] = 'novita'
    app.run()
    assert not app.exception
    assert app.sidebar.radio[0].value == 'Provider Explorer'
    assert widget(app.text_input, 'Find a provider').value == 'novita'
    assert any(e.label == 'More filters' and not e.proto.expanded for e in app.expander)
    widget(app.text_input, 'Find a provider').set_value('Novita').run()
    assert not app.exception
    assert [s.value for s in app.subheader] == ['Novita']
    widget(app.selectbox, 'Inspect available model').set_value('qwen3-coder-next').run()
    assert not app.exception and any(t.label == 'Access & prices' for t in app.tabs)
    assert any('[Canonical profile]' in m.value and 'qwen3-coder-next/profile.yaml' in m.value for m in app.markdown)
    widget(app.selectbox, 'Billing method').set_value('subscription').run()
    assert not app.exception and any('No provider records match' in i.value for i in app.info)
    widget(app.text_input, 'Find a provider').set_value('Go Plus').run()
    assert not app.exception and any(s.value == 'OpenCode Zen' for s in app.subheader)
    assert any('10 USD / per month' in m.value and '40 USD / per month' in m.value for m in app.markdown)
    assert any('exact model entitlement' in m.value for m in app.markdown)
