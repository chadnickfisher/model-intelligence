"""Provider-first cards and discovery controls for the Field Guide."""
import streamlit as st

from .data import active_route, current_price, link, show
from .providers import (BILLING, SERVICES, find_providers, readable_values,
                        provider_watchouts, service_types)


def bullets(values):
    if values:
        st.markdown('\n'.join('- ' + value for value in values))


def offer_name(data, price):
    model = data['model'].get(price['model_id'], {}).get('identity', {}).get('name')
    return ' · '.join(dict.fromkeys(v for v in [model, price['product'], price['tier']] if v))


def offer_rates(price):
    def rate_text(rate):
        amount = (show(rate['amount']) + '%' if rate['metric'] == 'percentage_fee' else
                  show(rate['amount']) + ' ' + (rate['currency'] or ''))
        return rate['metric'].replace('_', ' ').capitalize() + ': ' + amount + ' / ' + rate['unit']
    return '; '.join(rate_text(r) for r in price['rates'])


def offer_details(data, price, source_panel):
    st.markdown('**' + offer_name(data, price) + '**')
    st.write(BILLING.get(price['billing_method'], price['billing_method']) + ' · ' + offer_rates(price))
    if price['model_id'] is None:
        st.write('Provider / product scope; exact model entitlement is not established by this price.')
    for label, values in [('Included usage', price['included_usage']), ('Overage', price['overage']),
                          ('Conditions', price['conditions']), ('Notes', price['notes'])]:
        if values:
            st.write('**' + label + '**'); bullets(readable_values(values))
    for label, value in [('Reset', price['reset_cadence']), ('Region', price['region'])]:
        if value:
            st.write('**' + label + ':** ' + value)
    st.caption(f"Status: {price['status']} · checked {price['verified_at']} · "
               f"effective {show(price['effective_from'])} to {show(price['effective_to'])}")
    source_panel(data, price['evidence_ids'])


def provider_card(data, record, source_panel, model_detail, behavior_panel):
    p = record['profile']
    active = [r for r in record['routes'] if active_route(r)]
    offers = [price for price in record['offers'] if current_price(price)]
    with st.container(border=True, key='provider-card-' + p['id']):
        st.subheader(p['name'])
        st.write(' · '.join(s for s in SERVICES if s in record['services']) or 'Creator / client context')
        st.markdown('**What it offers**')
        items = readable_values(p['access_methods'])
        if not items:
            items = [product + ' — ' + ', '.join(sorted(kinds)) for product, kinds in
                     product_groups(active).items()]
        if items:
            bullets(items[:3])
        else:
            st.write('No active access service documented in this catalog.')
        coverage = [f"{len(ids)} {kind.lower()} model{'s' if len(ids) != 1 else ''}"
                    for kind, ids in sorted(record['models'].items())]
        if coverage:
            st.write('**Catalog coverage:** ' + ' · '.join(coverage))
        st.markdown('**Cost**')
        if offers:
            # A small representative preview, with each product/denominator intact.
            bullets(['**' + offer_name(data, price) + '** — ' + offer_rates(price) for price in offers[:2]])
            for price in offers[:2]:
                if price['included_usage']:
                    bullets([offer_name(data, price) + ': ' + v for v in readable_values(price['included_usage'])])
            if any(price['model_id'] is None for price in offers[:2]):
                st.write('Product-scoped prices; exact model entitlement requires a documented route.')
            if len(offers) > 2:
                st.caption(f"{len(offers)} current price records; all products, rates and conditions below.")
        else:
            st.write('Price not yet documented for an active compatible offer. Dedicated hosting and local use may incur compute costs.')
        st.markdown('**Watch-outs**')
        watchouts = provider_watchouts(record)
        bullets(watchouts[:3])
        if not watchouts:
            st.write('Account eligibility, limits and policies need review for the selected route.')
        if len(watchouts) > 3:
            with st.expander('More access conditions'):
                bullets(watchouts[3:])
        if record['models']:
            with st.expander('Models available in this catalog'):
                st.write('Counts cover explicit active model routes, grouped by access method. Downloads do not establish hosted inference.')
                for kind, ids in sorted(record['models'].items()):
                    st.markdown('**' + kind + '**')
                    bullets(['[' + data['model'][ident]['identity']['name'] + '](' +
                             link(data['paths'][('model', ident)]) + ')' for ident in
                             sorted(ids, key=lambda i: data['model'][i]['identity']['name'])])
                ids = sorted(set().union(*record['models'].values()), key=lambda i: data['model'][i]['identity']['name'])
                selected = st.selectbox('Inspect available model', [None] + ids, key='provider-model-' + p['id'],
                                        format_func=lambda i: 'Choose a model' if i is None else data['model'][i]['identity']['name'])
                if selected:
                    model_detail(data, data['model'][selected])
        with st.expander('Products, policies & evidence'):
            st.caption('Provider checked ' + p['verified_at'] + '; each route and offer retains its own verification date.')
            st.markdown('[Canonical provider record](' + link(data['paths'][('provider', p['id'])]) + ')')
            for label, field in [('API compatibility', 'api_compatibility'), ('Geographic access', 'geographic_availability'),
                                 ('Rate limits', 'rate_limits'), ('Privacy / data use', 'privacy_data_use'),
                                 ('Caching / batching', 'caching_batching'), ('Reliability evidence', 'reliability'),
                                 ('Provider notes', 'notes'), ('Limitations', 'limitations')]:
                values = readable_values(p[field])
                if values:
                    st.markdown('**' + label + '**'); bullets(values)
            for route in record['routes']:
                with st.expander((route['product'] or 'Access route') + ' · ' +
                                 (data['model'].get(route['model_id'], {}).get('identity', {}).get('name') or 'Product scope')):
                    st.write(', '.join(sorted(service_types([route]))))
                    st.write('Status: ' + route['status'])
                    if not active_route(route):
                        st.warning('This record does not establish active availability.')
                    if route['model_label']:
                        st.write('Provider model ID: ' + route['model_label'])
                    if route['requires_account'] is not None:
                        st.write('Account required: ' + show(route['requires_account']))
                    if route['subscription_includes_api'] is not None:
                        st.write('Subscription includes API: ' + show(route['subscription_includes_api']))
                    bullets(readable_values(route['conditions'] + route['restrictions'] + route['notes']))
                    st.caption('Route checked ' + route['verified_at'])
                    source_panel(data, route['evidence_ids'])
            for price in record['offers']:
                with st.expander('Price: ' + offer_name(data, price)):
                    offer_details(data, price, source_panel)
            for finding in record['behavior']:
                with st.expander('Provider observation: ' + finding['claim'][:90]):
                    behavior_panel(data, finding)
            st.markdown('**Provider sources**'); source_panel(data, p['evidence_ids'])


def product_groups(routes):
    groups = {}
    for route in routes:
        groups.setdefault(route['product'] or 'Documented access', set()).update(service_types([route]))
    return groups


def provider_explorer(data, source_panel, model_detail, behavior_panel):
    st.header('Find a provider for your models')
    cols = st.columns([2, 1, 1])
    with cols[0]:
        search = st.text_input('Find a provider', value=st.query_params.get('provider', ''), placeholder='Provider or product name')
    with cols[1]:
        service = st.selectbox('Service type', ['Any service'] + list(SERVICES))
    with cols[2]:
        billing = st.selectbox('Billing method', ['Any billing'] + list(BILLING),
                               format_func=lambda v: BILLING.get(v, v))
    with st.expander('More filters'):
        cols = st.columns(2)
        with cols[0]:
            currency = st.selectbox('Price currency', ['Any currency'] + sorted(
                {r['currency'] for p in data['price'].values() for r in p['rates'] if r['currency']}))
            roles = st.multiselect('Provider role', sorted({role for p in data['provider'].values() for role in p['roles']}))
        with cols[1]:
            context = st.checkbox('Include creator and client records', value=False)
            inactive = st.checkbox('Include inactive access and historical prices', value=False)
        st.caption('Billing and currency filters require a recorded offer. Fees, credits, monthly plans and token rates retain their own units.')
    records = find_providers(data, search=search, service=None if service == 'Any service' else service,
                             billing=None if billing == 'Any billing' else billing,
                             currency=None if currency == 'Any currency' else currency,
                             roles=roles, include_context=context, include_inactive=inactive)
    st.caption(f"{len(records)} provider{'s' if len(records) != 1 else ''} with matching documented products / routes. Catalog coverage is not the provider’s entire model catalog.")
    if not records:
        st.info('No provider records match. Try fewer filters or include creator and client records.')
        return
    page = st.selectbox('Provider results page', list(range(1, (len(records) + 5) // 6 + 1))) if len(records) > 6 else 1
    subset = records[(page - 1) * 6:page * 6]
    for start in range(0, len(subset), 2):
        for col, record in zip(st.columns(min(2, len(subset) - start)), subset[start:start + 2]):
            with col:
                provider_card(data, record, source_panel, model_detail, behavior_panel)
