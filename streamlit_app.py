"""Local or Community Cloud read-only explorer. No credentials or inference calls."""
from datetime import date, datetime, time, timezone
import streamlit as st
import pandas as pd
from explorer.data import load, show, link, summary, filter_models, claims, comparison, sources, UNKNOWN
from explorer.cost import estimate
from tools.knowledge import ROOT, read, history

st.set_page_config(page_title='Model Intelligence', layout='wide')


def fingerprint():
    # Cache invalidates when canonical files change; generated indexes are never read.
    patterns = ['models/*/*/profile.yaml', 'providers/*/profile.yaml', 'data/pricing.yaml',
                'data/access.yaml', 'data/releases.yaml', 'data/capability-taxonomy.yaml',
                'data/aliases.yaml', 'evidence/sources.yaml', 'evidence/observations.yaml']
    return tuple((p.relative_to(ROOT).as_posix(), p.stat().st_mtime_ns, p.stat().st_size)
                 for pattern in patterns for p in sorted(ROOT.glob(pattern)))


@st.cache_data(show_spinner=False)
def cached_data(version):
    return load()


def source_panel(data, ids):
    for source in sources(data, ids):
        st.markdown(f"- [{source.get('title') or source['id']}]({source['url']}) — {source['id']}; accessed {show(source.get('accessed_at'))}; published {show(source.get('published_at'))}")
    if not ids:
        st.caption('None separately recorded in this pass; this does not establish consensus.')


def claim_panel(data, j):
    st.write(j['judgment'])
    st.caption(f"{j['id']} · {j['scope']} · {j['assessment']} · {j['confidence']} evidence confidence")
    st.write(j['scope_note'])
    st.write('Direct tasks: ' + show(j['task_ids']))
    st.write('Related tasks (navigation only): ' + show(j['related_task_ids']))
    st.write('Conditions: ' + show(j['conditions']))
    st.write('Failure modes / limitations: ' + show(j['known_failure_modes']))
    st.write('Supporting evidence')
    source_panel(data, j['supporting_evidence_ids'])
    st.write('Contradictory / limiting evidence')
    source_panel(data, j['contradictory_evidence_ids'])
    st.write('Evidence notes: ' + show(j['evidence_notes']))
    st.json(j['provenance'], expanded=False)


def price_rows(prices):
    return [{'Price ID': p['id'], 'Model/product': p['model_id'] or p['product'] or p['model_label'] or UNKNOWN,
             'Provider': p['provider_id'], 'Billing': p['billing_method'], 'Tier': p['tier'], 'Status': p['status'],
             'Region': p['region'] or UNKNOWN,
             'Rates': '; '.join(f"{r['metric']}: {show(r['amount'])} {show(r['currency'])} / {r['unit']}" for r in p['rates']),
             'Conditions': show(p['conditions']), 'Effective from': show(p['effective_from']),
             'Effective to': show(p['effective_to']), 'Verified': p['verified_at']} for p in prices]


def model_panel(data, model):
    ident = model['id']
    st.subheader(model['identity']['name'])
    st.markdown(f"[Canonical profile]({link(data['paths'][('model', ident)])}) · [Readable profile]({link(data['paths'][('model', ident)].replace('profile.yaml', 'README.md'))})")
    st.caption(f"Facts checked {model['verified_at']} · status: {model['identity']['status']} · release: {show(model['identity']['release_date'])}")
    st.write('Evidence-backed uses and limitations')
    if not model['capabilities']:
        st.info('Task-specific ability remains unknown. Read the performance/deployment observations below.')
    for j in model['capabilities']:
        with st.expander(f"{j['provenance']['original_task']} — {j['scope']} / {j['assessment']}"):
            claim_panel(data, j)
    for j in model['performance_characteristics']:
        with st.expander('Performance / deployment: ' + j['provenance']['original_task']):
            claim_panel(data, j)
    with st.expander('Specifications, context, licensing and local hardware'):
        for name, spec in model['specifications'].items():
            st.write(f"{name}: {show(spec['value'])} ({spec['status']})")
            st.caption('Conditions: ' + show(spec['conditions']))
            source_panel(data, spec['evidence_ids'])
        st.write('License: ' + show(model['licensing']['name']))
        st.json(model['licensing'], expanded=False)
        source_panel(data, model['licensing']['evidence_ids'])
        st.write('Local availability: ' + model['local_inference']['availability'])
        st.write('Hardware: ' + show(model['local_inference']['hardware_notes']))
        st.write('Local conditions: ' + show(model['local_inference']['conditions']))
        source_panel(data, model['local_inference']['evidence_ids'])
        st.json(model['additional_specifications'], expanded=False)
    with st.expander('Access routes and pricing'):
        routes = [data['access'][i] for i in model['access_ids']]
        st.dataframe([{'ID': a['id'], 'Provider': a['provider_id'], 'Product': a['product'], 'Methods': show(a['methods']),
                       'Status': a['status'], 'Restrictions': show(a['restrictions']), 'Verified': a['verified_at']} for a in routes], hide_index=True)
        for a in routes:
            st.write(f"{a['id']}: {show(a['conditions'])}")
            provider = data['provider'].get(a['provider_id'])
            if provider:
                st.markdown(f"[Provider {provider['name']}]({link(data['paths'][('provider', provider['id'])])})")
            source_panel(data, a['evidence_ids'])
        st.dataframe(price_rows([data['price'][i] for i in model['price_ids']]), hide_index=True)
        st.markdown(f"[Canonical access]({link('data/access.yaml')}) · [Canonical prices]({link('data/pricing.yaml')})")
        for i in model['price_ids']:
            st.write(i)
            source_panel(data, data['price'][i]['evidence_ids'])
    with st.expander('Gaps, notes and original evidence'):
        st.write(show(model['limitations']))
        st.write(show(model['notes']))
        source_panel(data, model['evidence_ids'])


def model_explorer(data):
    st.subheader('Model Explorer')
    models = list(data['model'].values())
    with st.expander('Filters', expanded=True):
        cols = st.columns(3)
        with cols[0]:
            search = st.text_input('Model name or ID')
            vendors = st.multiselect('Vendor', sorted({m['identity']['creator'] for m in models}))
            families = st.multiselect('Family', sorted({m['identity']['family'] for m in models}))
            task = st.selectbox('Task', ['All tasks'] + list(data['task']))
            related = st.checkbox('Include related compound or unresolved evidence', value=False)
            confidence = st.multiselect('Evidence confidence', ['low', 'medium', 'high'])
        with cols[1]:
            routes = st.multiselect('Access (all selected required)', ['API', 'Subscription', 'Local'])
            weights = st.selectbox('Weights', ['Any', 'Downloadable', 'Closed', 'Unknown'])
            licenses = st.multiselect('License', sorted({m['licensing']['name'] or UNKNOWN for m in models}))
            minimum_context = st.number_input('Minimum native context tokens', min_value=0, value=0, step=1000)
            include_unknown = st.checkbox('Include unknown context when filtering', value=False)
        with cols[2]:
            input_mod = st.multiselect('Input modalities', sorted({x for m in models for x in (m['specifications']['modalities']['value'] or {}).get('input', [])}))
            output_mod = st.multiselect('Output modalities', sorted({x for m in models for x in (m['specifications']['modalities']['value'] or {}).get('output', [])}))
            max_input = st.number_input('Maximum API input rate / million text tokens (0 disables)', min_value=0.0, value=0.0)
            currency = st.selectbox('API price currency', sorted({r['currency'] for p in data['price'].values() for r in p['rates'] if r['currency']}))
            tier = st.text_input('API tier contains', help='Use Standard, Batch, Flex, peak, etc. Context bands and route conditions still apply.')
    filtered = filter_models(data, vendors=vendors, families=families, task=None if task == 'All tasks' else task,
                             include_related=related, confidence=confidence, routes=routes, licenses=licenses,
                             minimum_context=minimum_context, include_unknown_context=include_unknown,
                             input_modalities=input_mod, output_modalities=output_mod, weights=weights, search=search)
    if max_input > 0 or tier:
        from explorer.cost import UNITS, METRICS, routes_for_price
        filtered = [m for m in filtered if any(p['billing_method'] == 'metered-api' and p['status'] == 'current'
                     and routes_for_price(p, data['access'].values()) and tier.lower() in (p['tier'] or '').lower()
                     and (not p['effective_from'] or p['effective_from'] <= date.today().isoformat())
                     and (not p['effective_to'] or p['effective_to'] >= date.today().isoformat())
                     and any(METRICS.get(r['metric']) == 'input' and r['unit'] in UNITS and r['currency'] == currency
                             and r['amount'] is not None and (max_input == 0 or r['amount'] <= max_input) for r in p['rates'])
                     for p in (data['price'][i] for i in m['price_ids']))]
        st.caption('Price filter matches documented input-rate offers only; use Cost Explorer to check the full request and conditions.')
    st.caption(f'{len(filtered)} models matched. Task matching filters evidence coverage, not ability or endorsement.')
    st.dataframe([summary(m, data) for m in filtered], hide_index=True,
                 column_config={'Canonical': st.column_config.LinkColumn('Canonical')})
    if not filtered:
        st.info('No matching records. Missing evidence is unknown, not a failing score.')
        return
    selected = st.selectbox('Inspect model', [m['id'] for m in filtered], format_func=lambda i: data['model'][i]['identity']['name'])
    model_panel(data, data['model'][selected])


def compare_models(data):
    st.subheader('Compare 2–5 Models')
    selected = st.multiselect('Models to compare', list(data['model']), max_selections=5,
                              format_func=lambda i: data['model'][i]['identity']['name'])
    task = st.selectbox('Comparison task', ['All recorded evidence'] + list(data['task']))
    related = st.checkbox('Include related evidence in comparison', value=False)
    if len(selected) < 2:
        st.info('Select at least two models. Unrecorded task ability stays unknown.')
        return
    rows = comparison(data, selected, None if task == 'All recorded evidence' else task, related)
    st.dataframe(rows, hide_index=True, column_config={'Canonical': st.column_config.LinkColumn('Canonical')})
    st.caption('Context is a published capacity, not retrieval reliability. Different providers, conditions and prices are separate offers.')
    for ident in selected:
        with st.expander('Evidence, conditions and routes: ' + data['model'][ident]['identity']['name']):
            model_panel(data, data['model'][ident])


def capability_explorer(data):
    st.subheader('Capability Explorer')
    task = st.selectbox('Capability task', list(data['task']), format_func=lambda t: data['task'][t]['label'])
    related = st.checkbox('Show related compound/unresolved evidence', value=False)
    confidences = st.multiselect('Claim confidence', ['low', 'medium', 'high'], default=['low', 'medium', 'high'])
    rows = [(m, j) for m in data['model'].values() for j in claims(m, task, related, confidences)] if confidences else []
    st.caption(f'{len(rows)} claims. Confidence concerns evidence; this view has no score or ability ranking.')
    if not rows:
        st.info('No matching direct judgments are recorded. Related evidence can be viewed separately; ability remains unknown.')
    st.dataframe([{'Model': m['identity']['name'], 'Scope': j['scope'], 'Assessment': j['assessment'],
                   'Confidence': j['confidence'], 'Actual judgment': j['judgment'], 'Conditions': show(j['conditions'])} for m, j in rows], hide_index=True)
    for m, j in rows:
        with st.expander(f"{m['identity']['name']} — {j['scope']} / {j['assessment']} / {j['id']}"):
            st.markdown(f"[Canonical claim]({link(data['paths'][('model', m['id'])])})")
            claim_panel(data, j)


def cost_explorer(data):
    st.subheader('Cost Explorer')
    billing = st.multiselect('Billing method', sorted({p['billing_method'] for p in data['price'].values()}), default=['metered-api'])
    model_ids = st.multiselect('Price model', list(data['model']))
    providers = st.multiselect('Price provider', sorted(data['provider']))
    prices = [p for p in data['price'].values() if p['billing_method'] in billing
              and (not model_ids or p['model_id'] in model_ids) and (not providers or p['provider_id'] in providers)]
    st.dataframe(price_rows(prices), hide_index=True)
    st.caption('Different units and currencies stay separate. Subscriptions, audio, image, video, compute and credit fees are inspectable; this estimator handles compatible text tokens only.')
    if not prices:
        st.info('No offers match these filters.')
        return
    selected = st.selectbox('Estimate this offer', [p['id'] for p in prices], format_func=lambda i: f"{data['price'][i]['model_id'] or data['price'][i]['product']} / {data['price'][i]['provider_id']} / {data['price'][i]['tier']} / {i[-12:]}")
    p = data['price'][selected]
    st.write('Offer conditions: ' + show(p['conditions']))
    st.caption(f"{p['id']} · verified {p['verified_at']} · effective {show(p['effective_from'])} to {show(p['effective_to'])}")
    st.markdown(f"[Canonical prices]({link('data/pricing.yaml')}) · [Canonical access]({link('data/access.yaml')})")
    source_panel(data, p['evidence_ids'])
    cols = st.columns(3)
    with cols[0]:
        total_input = st.number_input('Total input tokens (includes cache reads/writes)', min_value=0, value=1000, step=100)
        output = st.number_input('Output tokens (includes billable thinking)', min_value=0, value=1000, step=100)
    with cols[1]:
        cached = st.number_input('Cached read tokens', min_value=0, value=0, step=100)
        writes = st.number_input('Generic cache write tokens', min_value=0, value=0, step=100)
    with cols[2]:
        writes5 = st.number_input('5-minute cache write tokens', min_value=0, value=0, step=100)
        writes1 = st.number_input('1-hour cache write tokens', min_value=0, value=0, step=100)
    as_of = st.date_input('Price effective date', value=date.today())
    time_of_day = st.time_input('Request time UTC (peak/off-peak only)', value=time(12, 0))
    holiday = st.selectbox('Chinese public holiday (peak/off-peak only)', ['Unknown', 'No', 'Yes'])
    result = estimate(p, data['access'].values(), input_tokens=total_input, output_tokens=output, cached_tokens=cached,
                      cache_write_tokens=writes, cache_write_5m_tokens=writes5, cache_write_1h_tokens=writes1,
                      as_of=as_of.isoformat(), request_time=datetime.combine(as_of, time_of_day, timezone.utc),
                      chinese_public_holiday={'Unknown': None, 'No': False, 'Yes': True}[holiday])
    if not result['supported']:
        st.warning('Calculation unsupported for this request')
        for reason in result['reasons']:
            st.write('- ' + reason)
    else:
        st.metric('Estimated text-token subtotal', f"{result['currency']} {result['total']}")
        st.dataframe(result['components'], hide_index=True)
        if result['components']:
            st.bar_chart(pd.DataFrame([{'Component': c['component'], 'Cost': float(c['cost'])} for c in result['components']]).set_index('Component'), horizontal=True)
        for warning in result['warnings']:
            st.caption(warning)
        st.write('Documented route IDs: ' + show(result['route_ids']))
        for route_id in result['route_ids']:
            route = data['access'][route_id]
            st.write('Access conditions: ' + show(route['conditions']))
            st.write('Access restrictions: ' + show(route['restrictions']))
    with st.expander('Complete selected offer'):
        st.json(p)


@st.cache_data(show_spinner=False)
def cached_history(version):
    return history()


def recent_changes(data):
    st.subheader('Recent Changes')
    since = st.date_input('Since', value=date(2026, 9, 1))
    show_future = st.checkbox('Include future announced events', value=False)
    releases = [r for r in data['release'].values() if r['event_date'] is not None and r['event_date'] >= since.isoformat()
                and (show_future or r['event_date'] <= date.today().isoformat())]
    releases.sort(key=lambda r: r['event_date'], reverse=True)
    st.write('Documented release and lifecycle events')
    st.dataframe([{'Date': r['event_date'], 'Event': r['event_type'], 'Model/label': r['model_id'] or r['model_label'],
                   'Provider': r['provider_id'], 'Summary': r['summary'], 'Verified': r['verified_at'], 'ID': r['id']} for r in releases], hide_index=True)
    unknown = [r for r in data['release'].values() if r['event_date'] is None]
    with st.expander(f'Undated events ({len(unknown)})'):
        st.json(unknown)
    for r in releases:
        with st.expander(f"{r['event_date']} / {r['event_type']} / {r['model_id'] or r['model_label'] or r['id']}"):
            st.write(r['summary'])
            st.markdown(f"[Canonical event]({link('data/releases.yaml')})")
            source_panel(data, r['evidence_ids'])
    path = ROOT / 'history/revisions.yaml'
    revisions = [r for r in cached_history((path.stat().st_mtime_ns, path.stat().st_size)) if r['observed_at'] >= since.isoformat()]
    st.write('Repository observation history')
    st.caption('Baseline entries mean first observed by this repository; they do not mean a new model or newly available offer.')
    types = st.multiselect('History entity types', sorted({r['entity_type'] for r in revisions}))
    if types:
        revisions = [r for r in revisions if r['entity_type'] in types]
    st.dataframe([{'Observed': r['observed_at'], 'Effective': r['effective_from'], 'Type': r['entity_type'], 'Entity': r['entity_id'],
                   'Operation': r['operation'], 'Reason': r['reason'], 'Revision ID': r['id']} for r in reversed(revisions)], hide_index=True)
    st.markdown(f"[Full journal]({link('history/revisions.yaml')}) · [Historical semantics]({link('history/README.md')})")
    if revisions:
        chosen = st.selectbox('Inspect history revision', [r['id'] for r in reversed(revisions)])
        revision = next(r for r in revisions if r['id'] == chosen)
        with st.expander('Prior/current values and evidence'):
            st.json(revision, expanded=False)
            prior = next((r for r in cached_history((path.stat().st_mtime_ns, path.stat().st_size)) if r['id'] == revision['previous_revision_id']), None)
            if prior:
                st.write('Prior value')
                st.json(prior['value'], expanded=False)
            else:
                st.info('No earlier recorded value; this is the first observation.')
            source_panel(data, [i for i in revision['evidence_ids'] if i != 'capabilities-2026-10-07'])


st.title('Model Intelligence')
st.caption('Public evidence baseline: October 6, 2026. Research maintenance is paused. Read-only YAML explorer; no model calls.')
st.info('Confidence is evidence support, not ability. Compound/related evidence is not a per-task endorsement. Unknown remains unknown.')
data = cached_data(fingerprint())
page = st.sidebar.radio('Explore', ['Model Explorer', 'Compare 2–5 Models', 'Capability Explorer', 'Cost Explorer', 'Recent Changes'])
{'Model Explorer': model_explorer, 'Compare 2–5 Models': compare_models, 'Capability Explorer': capability_explorer,
 'Cost Explorer': cost_explorer, 'Recent Changes': recent_changes}[page](data)
