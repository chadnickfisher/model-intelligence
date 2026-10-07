"""Read-only Field Guide. Every fact comes from canonical YAML; no model calls."""
from datetime import date, datetime, time, timezone
from decimal import Decimal
import streamlit as st
from explorer.data import (load, show, link, summary, filter_models, claims, sources, UNKNOWN,
    model_routes, route_kinds, route_label, route_status, billing_summary, route_prices,
    task_label, judgment_label, task_coverage, behavior_findings, current_price, comparable_api_offers,
    benchmark_findings, benchmark_compatibility, confidence_trace)
from explorer.cost import estimate_runs, routes_for_price, UNITS
from tools.knowledge import ROOT, history

st.set_page_config(page_title='Model Intelligence · Field Guide', layout='wide')
st.markdown('''<style>
.block-container {max-width:1400px;padding-top:2rem;}
[data-testid="stSidebar"] {background:#EFEADF;}
[data-testid="stMetric"] {background:#F4D5B7;border-radius:12px;padding:14px;}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:14px;}
h1,h2,h3 {color:#24533F;}
@media(max-width:800px){[data-testid="stHorizontalBlock"]{flex-wrap:wrap;}
[data-testid="stColumn"]{min-width:min(100%,300px);}}
</style>''', unsafe_allow_html=True)

CONFIDENCE = ('Confidence describes evidence for a finding, not model ability. '
    'High: multiple credible recent sources converge with little material contradiction. '
    'Medium: useful evidence, but incomplete, configuration-specific or mixed. '
    'Low: sparse, preliminary, old, vendor-heavy, benchmark-dependent or contradictory evidence.')
ASSESSMENT = {'conditional':'Conditional use', 'warning':'Warning', 'weak':'Documented weakness', 'unknown':'Unknown'}
SCOPE = {'direct':'Task-specific finding','compound':'Related bundle','unresolved':'Scope unresolved','performance':'Performance / deployment'}
ROUTES = ['API','Chat app','Subscription','Run locally','Download weights']

def fingerprint():
    patterns=['models/*/*/profile.yaml','providers/*/profile.yaml','data/pricing.yaml','data/access.yaml',
        'data/releases.yaml','data/capability-taxonomy.yaml','data/aliases.yaml','data/behavior.yaml',
        'data/access-coverage.yaml','data/benchmarks.yaml','data/research-coverage.yaml','evidence/sources.yaml','evidence/observations.yaml']
    return tuple((p.relative_to(ROOT).as_posix(),p.stat().st_mtime_ns,p.stat().st_size)
        for pattern in patterns for p in sorted(ROOT.glob(pattern)))

@st.cache_data(show_spinner=False)
def cached_data(version): return load()

@st.cache_data(show_spinner=False)
def cached_history(version): return history()

def source_panel(data, ids):
    for s in sources(data,ids):
        st.markdown(f"[{s.get('title') or 'Source'}]({s['url']})")
        st.caption(f"Checked {show(s.get('accessed_at'))} · published {show(s.get('published_at'))}")
    if not ids: st.caption('None separately recorded in this pass; this does not establish consensus.')

def short(text, limit=240):
    return text if len(text)<=limit else text[:limit].rsplit(' ',1)[0]+'…'

def finding_text(j):
    return f"{ASSESSMENT[j['assessment']]} · {j['confidence'].capitalize()} evidence confidence · {SCOPE[j['scope']]}"

def benchmark_text(b):
    test=b['benchmark']
    return f"{test['name']} {test['version'] or '(version unknown)'} — {test['metric']}: {show(b['value'])} {test['unit']}"

def benchmark_panel(data,b):
    st.write(benchmark_text(b))
    st.caption(f"{b['evidence_class'].replace('_',' ')} · direction: {b['benchmark']['direction']} · measured {show(b['measured_at'])} · observed {b['observed_at']}")
    st.write('Checkpoint: '+show(b['model_version']))
    st.write('Setup: '+show({'harness':b['harness'],'effort':b['effort'],'tools':b['tools'],'provider':b['provider_id']}))
    st.write('Conditions: '+show(b['conditions']))
    st.write('Limitations: '+show(b['limitations']))
    st.write('Evidence notes: '+show(b['evidence_notes']))
    source_panel(data,b['source_ids'])

def benchmark_highlights(data,model,task=None,related=False):
    records=benchmark_findings(model,data)
    if task:
        ids={j['id'] for j in claims(model,task,related)}
        records=[b for b in records if ids.intersection(b['judgment_ids'])]
    st.write('Benchmark highlights')
    for b in records[:2]:
        st.write(benchmark_text(b));st.caption(b['evidence_class'].replace('_',' ')+' · '+show(b['measured_at'])+' · setup-specific')
    if not records:st.caption('Structured benchmark measurements not yet recorded; see source-backed findings in evidence details.')

def claim_panel(data,j):
    st.write(j['judgment']); st.caption(finding_text(j))
    st.write(j['scope_note'])
    st.write('Conditions: '+show(j['conditions']))
    st.write('Limitations: '+show(j['known_failure_modes']))
    st.write('Supporting evidence'); source_panel(data,j['supporting_evidence_ids'])
    st.write('Contradictory / limiting evidence'); source_panel(data,j['contradictory_evidence_ids'])
    if j['evidence_notes']: st.write('Evidence notes: '+show(j['evidence_notes']))
    st.caption(f"Observed {j['observed_at']} · effective {show(j['effective_from'])}")
    with st.expander('Why this evidence confidence?'):
        st.caption(CONFIDENCE)
        trace=confidence_trace(data,j)
        st.write('Recorded rationale: '+show(trace['rationale_notes']))
        st.write('Operating conditions: '+show(trace['conditions']))
        st.write('Supporting sources and freshness');st.dataframe(trace['supporting_sources'],hide_index=True)
        if trace['contradictory_sources']:st.write('Contradictory sources and freshness');st.dataframe(trace['contradictory_sources'],hide_index=True)
        measured=[b for b in data['benchmark'].values() if j['id'] in b['judgment_ids']]
        if measured:
            st.write('Measurements supporting this specific finding')
            for b in measured:benchmark_panel(data,b)
        if not trace['rationale_notes']:st.caption('A separate confidence rationale has not been recorded; inspect source limitations and conditions. Corroboration is not established by source count alone.')
        st.caption(trace['caution'])
    st.json({'judgment_id':j['id'],'direct_tasks':j['task_ids'],'related_tasks':j['related_task_ids'],
        'provenance':j['provenance']},expanded=False)

def behavior_panel(data,b):
    st.write(b['claim'])
    st.caption(f"{b['fact_status'].capitalize()} · {b['confidence']} evidence confidence · {b['status']} · reported {show(b['reported_at'])}")
    st.write('Affected setup: '+show([b['model_version'],b['provider_id'],b['product'],b['harness'],b['effort']]))
    st.write('Change type: '+b['change_type'].replace('_',' '))
    for metric in b['metrics']: st.write(metric['kind'].replace('_',' ')+': '+show(metric['measurement']))
    st.write('Conditions: '+show(b['conditions']))
    if b['official_acknowledgment']: st.write('Official statement: '+b['official_acknowledgment'])
    if b['fix']['summary']:
        st.write('Published change: '+b['fix']['summary'])
        st.caption(f"Published {show(b['fix']['published_at'])} · version {show(b['fix']['version'])} · measured improvement: {show(b['fix']['measured_improvement'])}")
        source_panel(data,b['fix']['evidence_ids'])
    st.write('Supporting evidence');source_panel(data,b['supporting_evidence_ids'])
    st.write('Contradictory / limiting evidence');source_panel(data,b['contradictory_evidence_ids'])
    if b['notes']:st.write(show(b['notes']))

def rate_text(p):
    names={'input':'Input','output':'Output','cached_input':'Cached input','cache_read':'Cache read',
        'included_compute_credit':'Included credit','output_including_thinking':'Output incl. reasoning'}
    return '; '.join(f"{names.get(r['metric'],r['metric'].replace('_',' '))}: {show(r['amount'])} {r['currency'] or ''} / {r['unit']}" for r in p['rates'])

def price_rows(data,prices):
    return [{'Model / product':data['model'].get(p['model_id'],{}).get('identity',{}).get('name') or p['product'] or p['model_label'],
        'Provider':data['provider'].get(p['provider_id'],{}).get('name',p['provider_id']),
        'Billing':p['billing_method'].replace('-',' '),'Plan / tier':p['tier'],'Status':p['status'],
        'Rates':rate_text(p),'Included usage':show(p['included_usage']),'Reset':show(p['reset_cadence']),
        'Conditions':show(p['conditions']),'Checked':p['verified_at']} for p in prices]

def access_summary(data,model):
    rows=model_routes(model,data,True)
    if not rows:return 'Access not yet documented'
    return '\n'.join(dict.fromkeys(', '.join(sorted(route_kinds(r)))+' · '+billing_summary(r,data) for r in rows))

def price_summary(data,model):
    ps=[data['price'][i] for i in model['price_ids'] if current_price(data['price'][i])]
    api=[p for p in ps if p['billing_method']=='metered-api' and routes_for_price(p,data['access'].values())]
    if api:
        # A concrete offer, never a cross-provider minimum or subscription conversion.
        p=sorted(api,key=lambda p:(cost_mode(p)!='standard',(p['tier'] or '').lower() not in {'standard','default'},p['provider_id'],p['id']))[0]
        return f"{data['provider'].get(p['provider_id'],{}).get('name',p['provider_id'])} · {p['tier'] or 'Documented tier'}: {rate_text(p)}"
    if ps:return 'Other billing units recorded; inspect the documented offers.'
    return 'Model-specific price not yet documented'

def model_detail(data,model):
    st.markdown(f"[Canonical profile]({link(data['paths'][('model',model['id'])])}) · [Readable profile]({link(data['paths'][('model',model['id'])].replace('profile.yaml','README.md'))})")
    tabs=st.tabs(['Findings','Access & prices','Specifications','Behavior & gaps','Benchmarks'])
    with tabs[0]:
        for j in model['capabilities']+model['performance_characteristics']:
            with st.expander(judgment_label(data,j)+' · '+ASSESSMENT[j['assessment']]):claim_panel(data,j)
        if not model['capabilities']:st.info('Task evidence not yet curated.')
    with tabs[1]:
        for r in model_routes(model,data):
            st.write(route_label(r,data));st.caption(', '.join(sorted(route_kinds(r)))+' · '+billing_summary(r,data))
            st.write('Availability: '+r['status']);st.write('Conditions: '+show(r['conditions']))
            st.write('Restrictions: '+show(r['restrictions']))
            st.caption('Account required: '+show(r['requires_account'])+' · subscription includes API: '+show(r['subscription_includes_api']))
            ps=route_prices(r,data)
            if ps:st.dataframe(price_rows(data,ps),hide_index=True)
            if r.get('research_details'):
                with st.expander('Documented route details, limits & unresolved pricing'):
                    st.caption('These source observations preserve aliases, eligibility, regions, limits and non-token tariffs. Unnormalized tariffs are not calculator inputs.')
                    st.json(r['research_details'],expanded=False)
            source_panel(data,r['evidence_ids'])
        ps=[data['price'][i] for i in model['price_ids']]
        if ps:st.dataframe(price_rows(data,ps),hide_index=True)
        else:st.info('Model-specific price not yet documented. Weight downloads and account credits are not hosted token prices.')
        coverage=next((c for c in data['access_coverage'].values() if c['model_id']==model['id']),None)
        if coverage:st.caption('Access research: '+coverage['audit_status']+' · '+show(coverage['notes']))
        st.markdown(f"[Canonical access]({link('data/access.yaml')}) · [Canonical prices]({link('data/pricing.yaml')})")
    with tabs[2]:
        for name,spec in model['specifications'].items():
            st.write(name.replace('_',' ').capitalize()+': '+show(spec['value']));st.caption(spec['status']+' · '+show(spec['conditions']))
            source_panel(data,spec['evidence_ids'])
        st.write('License: '+show(model['licensing']['name']));st.write('License restrictions: '+show(model['licensing']['restrictions']))
        source_panel(data,model['licensing']['evidence_ids'])
        st.write('Local hardware: '+show(model['local_inference']['hardware_notes']))
        st.write('Local conditions: '+show(model['local_inference']['conditions']));source_panel(data,model['local_inference']['evidence_ids'])
        with st.expander('Technical record'):st.json(model)
    with tabs[3]:
        bs=behavior_findings(model,data)
        for b in bs:
            with st.expander((b['reported_at'] or b['observed_at'])+' · '+short(b['claim'],100)):behavior_panel(data,b)
        if not bs:st.caption('No dated post-launch behavior finding curated. This is not proof that behavior has remained unchanged.')
        st.write(show(model['limitations']));st.write(show(model['notes']));source_panel(data,model['evidence_ids'])
        coverage=[c for c in data['research_coverage'].values() if c['model_id']==model['id']]
        if coverage:
            st.write('Research coverage')
            st.dataframe([{'Domain':c['domain'].replace('_',' / '),'Actual check':show(c['checked_at']),
                           'Result':c['result'].replace('_',' '),'Remaining gaps':show(c['remaining_gaps'])}
                          for c in coverage],hide_index=True)
            st.caption('Coverage accounting does not certify research adequacy. Carry-forward facts retain their original verification dates.')

    with tabs[4]:
        records=benchmark_findings(model,data)
        for b in records:
            with st.expander(benchmark_text(b)):benchmark_panel(data,b)
        if not records:st.info('No structured measurement recorded. Narrative findings and linked sources remain in Findings; missing measurements are unknown.')
        st.caption('Quality tests, preference rankings and vendor claims answer different questions. No universal score is computed.')

def model_card(data,model,task=None,related=False,details=True):
    with st.container(border=True):
        st.subheader(model['identity']['name']);st.caption(model['identity']['creator']+' · checked '+model['verified_at'])
        js=claims(model,task,related)
        if not task:js=[j for j in js if j['scope']=='direct']
        st.write('Task fit')
        for j in js[:2]:st.write(short(j['judgment']));st.caption(finding_text(j))
        if not js:st.caption('Task-specific evidence not yet curated; ability is unknown.')
        limitations=list(dict.fromkeys([f for j in js for f in j['known_failure_modes']]+model['limitations']))
        st.write('Watch-outs');st.write(short('; '.join(limitations[:2])) if limitations else UNKNOWN)
        st.write('How to use it');st.write(access_summary(data,model))
        st.caption('API: '+route_status(model,data,'API')+' · Subscription: '+route_status(model,data,'Subscription'))
        st.write('Price');st.write(short(price_summary(data,model),320))
        st.write('Context');st.write(show(summary(model,data)['Native context tokens'])+' native tokens')
        st.caption('Published capacity; effective retrieval and provider limits may differ.')
        benchmark_highlights(data,model,task,related)
        bs=behavior_findings(model,data,highlights=True)
        st.write('Post-launch model / setup observations')
        if bs:
            for b in bs[:2]:st.write(short(b['claim']));st.caption(f"{b['reported_at'] or b['observed_at']} · {b['fact_status']} · {b['confidence']} confidence · {b['status']}")
        else:st.caption('No dated finding curated')
        if details:
            with st.expander('Evidence & details'):model_detail(data,model)

def task_options(data):return ['All tasks']+list(data['task'])
def task_format(data,t):return 'Any task' if t=='All tasks' else task_label(data,t)

def model_explorer(data):
    st.header('Find a model for your work')
    cols=st.columns([2,2,1])
    with cols[0]:task=st.selectbox('What are you working on?',task_options(data),format_func=lambda t:task_format(data,t))
    with cols[1]:search=st.text_input('Find a model',placeholder='Name or family')
    with cols[2]:route=st.selectbox('How will you use it?',['Any access']+ROUTES)
    with st.expander('Refine your search'):
        cols=st.columns(3)
        with cols[0]:
            vendors=st.multiselect('Vendor',sorted({m['identity']['creator'] for m in data['model'].values()}))
            families=st.multiselect('Family',sorted({m['identity']['family'] for m in data['model'].values()}))
            related=st.checkbox('Include related evidence',value=False,help='Compound bundles and unresolved findings are not specific-task endorsements.')
            confidence=st.multiselect('Evidence confidence',['low','medium','high'],help=CONFIDENCE)
        with cols[1]:
            weights=st.selectbox('Weights',['Any','Downloadable','Closed','Unknown'])
            licenses=st.multiselect('License',sorted({m['licensing']['name'] or UNKNOWN for m in data['model'].values()}))
            minimum=st.number_input('Minimum native context tokens',min_value=0,value=0,step=1000)
            unknown=st.checkbox('Include unknown context',value=False)
        with cols[2]:
            imod=st.multiselect('Input modalities',sorted({x for m in data['model'].values() for x in (m['specifications']['modalities']['value'] or {}).get('input',[])}))
            omod=st.multiselect('Output modalities',sorted({x for m in data['model'].values() for x in (m['specifications']['modalities']['value'] or {}).get('output',[])}))
        cost_filter=st.checkbox('Filter by documented API cost',value=False)
        if cost_filter:
            cols=st.columns(4)
            with cols[0]:cost_currency=st.selectbox('Filter currency',sorted({r['currency'] for p in data['price'].values() for r in p['rates'] if r['currency']}))
            with cols[1]:cost_input=st.number_input('Filter input tokens',min_value=0,value=1000,step=100)
            with cols[2]:cost_output=st.number_input('Filter output tokens',min_value=0,value=1000,step=100)
            with cols[3]:cost_limit=st.number_input('Maximum per-run subtotal',min_value=0.0,value=1.0,step=0.01,format='%.4f')
            st.caption('Matches at least one documented compatible API offer in this currency for the specified request. Unknown prices are excluded. Cache reuse, peak windows and currency conversion are not inferred; inspect exact routes in Cost Explorer.')
        st.caption(CONFIDENCE)
    models=filter_models(data,task=None if task=='All tasks' else task,include_related=related,confidence=confidence,
        vendors=vendors,families=families,routes=[] if route=='Any access' else [route],weights=weights,licenses=licenses,
        minimum_context=minimum,include_unknown_context=unknown,input_modalities=imod,output_modalities=omod,search=search)
    if cost_filter:
        models=[m for m in models if any(Decimal(p['total'])<=Decimal(str(cost_limit)) for p in comparable_api_offers(
            m,data,input_tokens=cost_input,output_tokens=cost_output,currency=cost_currency))]
    st.caption(f'{len(models)} models with matching recorded evidence / routes. Missing research does not imply inability or unavailability.')
    if not models:st.info('No records match. Try fewer filters or view task coverage.');return
    page=st.selectbox('Results page',list(range(1,(len(models)+5)//6+1)),format_func=lambda n:f'{n}')
    subset=models[(page-1)*6:page*6]
    for start in range(0,len(subset),2):
        for col,model in zip(st.columns(2),subset[start:start+2]):
            with col:model_card(data,model,None if task=='All tasks' else task,related)
    selected=st.selectbox('Inspect model',[m['id'] for m in models],format_func=lambda i:data['model'][i]['identity']['name'])
    st.session_state['workbench_model']=selected
    with st.expander('Selected model: '+data['model'][selected]['identity']['name']):model_detail(data,data['model'][selected])

def compare_models(data):
    st.header('Compare your shortlist')
    ids=st.multiselect('Models to compare',list(data['model']),max_selections=5,format_func=lambda i:data['model'][i]['identity']['name'])
    task=st.selectbox('Comparison task',task_options(data),format_func=lambda t:task_format(data,t))
    related=st.checkbox('Include related evidence in comparison',value=False)
    st.caption(CONFIDENCE)
    if len(ids)<2:st.info('Choose 2–5 models to compare the same fields side by side.');return
    st.caption('Prices are provider-qualified offers, not a universal cheapest-model ranking. Context is published capacity, not retrieval reliability.')
    selected_task=None if task=='All tasks' else task
    for start in range(0,len(ids),2):
        models=[data['model'][i] for i in ids[start:start+2]]
        with st.container(border=True):
            for col,model in zip(st.columns(len(models)),models):
                with col:
                    st.subheader(model['identity']['name'])
                    st.caption(model['identity']['creator']+' · checked '+model['verified_at'])
            # One horizontal block per field aligns rows even when finding lengths differ.
            for field in ['Task fit','Watch-outs','How to use it','Price','Context','Local hardware','Post-launch behavior']:
                for col,model in zip(st.columns(len(models)),models):
                    with col:
                        st.write(field)
                        js=claims(model,selected_task,related)
                        if selected_task is None:js=[j for j in js if j['scope']=='direct']
                        if field=='Task fit':
                            for j in js[:2]:st.write(short(j['judgment']));st.caption(finding_text(j))
                            if not js:st.caption('Task-specific evidence not yet curated; ability is unknown.')
                        elif field=='Watch-outs':
                            values=list(dict.fromkeys([v for j in js for v in j['known_failure_modes']]+model['limitations']))
                            st.write(short('; '.join(values[:2])) if values else UNKNOWN)
                        elif field=='How to use it':
                            st.write(access_summary(data,model))
                            st.caption('API: '+route_status(model,data,'API')+' · Subscription: '+route_status(model,data,'Subscription'))
                        elif field=='Price':st.write(short(price_summary(data,model),320))
                        elif field=='Context':st.write(show(summary(model,data)['Native context tokens'])+' native tokens')
                        elif field=='Local hardware':st.write(short(show(model['local_inference']['hardware_notes']),320))
                        else:
                            bs=behavior_findings(model,data,highlights=True)
                            for b in bs[:2]:st.write(short(b['claim']));st.caption(f"{b['reported_at'] or b['observed_at']} · {b['fact_status']} · {b['confidence']} confidence · {b['status']}")
                            if not bs:st.caption('No dated finding curated')
            tests=sorted({tuple(b['benchmark'][k] or '' for k in ('name','version','metric','unit'))
                          for m in models for b in benchmark_findings(m,data)})
            st.write('Benchmark comparison')
            if not tests:st.caption('No structured measurements for this shortlist. Missing results remain unknown.')
            for test in tests:
                matched=[b for m in models for b in benchmark_findings(m,data)
                         if tuple(b['benchmark'][k] or '' for k in ('name','version','metric','unit'))==test]
                st.caption(' · '.join(v for v in test if v)+' — '+benchmark_compatibility(matched))
                for col,model in zip(st.columns(len(models)),models):
                    with col:
                        own=[b for b in matched if b['model_id']==model['id']]
                        for b in own:
                            st.write(benchmark_text(b));st.caption(b['evidence_class'].replace('_',' ')+' · '+show(b['measured_at']))
                            with st.expander('Benchmark setup & evidence: '+model['identity']['name']):benchmark_panel(data,b)
                        if not own:st.caption(UNKNOWN)
            for col,model in zip(st.columns(len(models)),models):
                with col:
                    with st.expander('Evidence & details: '+model['identity']['name']):model_detail(data,model)

def capability_explorer(data):
    st.header('Explore the evidence')
    counts=task_coverage(data)
    task=st.selectbox('Capability task',['Coverage overview']+list(data['task']),format_func=lambda t:t if t=='Coverage overview' else f"{task_label(data,t)} · {counts[t]['direct']} direct / {counts[t]['compound']} related / {counts[t]['unresolved']} unresolved")
    st.caption(CONFIDENCE)
    if task=='Coverage overview':
        st.dataframe([{'Task':task_label(data,t),'Task-specific models':c['direct'],'Related bundles':c['compound'],'Unresolved':c['unresolved']} for t,c in counts.items()],hide_index=True)
        st.caption('Coverage counts are evidence navigation, not ability rankings. Select a task to read conclusions.');return
    conf=st.multiselect('Claim confidence',['low','medium','high'],default=['low','medium','high'],help=CONFIDENCE)
    related=st.checkbox('Show related compound/unresolved evidence',value=True)
    allrows=[(m,j) for m in data['model'].values() for j in claims(m,task,True)]
    if not allrows:st.info('Evidence not yet curated for this task. Ability remains unknown.');return
    rows=[(m,j) for m,j in allrows if j['confidence'] in conf]
    if not rows:st.info('Evidence exists, but none matches the confidence filter.');return
    for scope in ['direct','compound','unresolved']:
        group=[(m,j) for m,j in rows if j['scope']==scope]
        if scope!='direct' and not related:continue
        st.subheader(SCOPE[scope]+f' ({len(group)})')
        if not group:st.caption('No findings in this group.');continue
        if scope!='direct':st.caption('Navigation context only; this is not an endorsement for the selected task.')
        for m,j in group:
            with st.container(border=True):
                st.write(m['identity']['name']);st.write(j['judgment']);st.caption(finding_text(j))
                if j['known_failure_modes']:st.write('Watch-outs: '+show(j['known_failure_modes']))
                with st.expander('Evidence & conditions'):claim_panel(data,j)

def cost_mode(p):
    text=(p['tier'] or '').lower().replace('_','-')
    return next((m for m in ['batch','flex','priority','off-peak','peak'] if m in text),'standard')

def offer_label(data,p):
    provider=data['provider'].get(p['provider_id'],{}).get('name',p['provider_id'])
    return provider+' · '+(p['tier'] or 'Standard')+' · '+(p['product'] or 'API')+' · '+rate_text(p)

def cost_explorer(data):
    st.header('Estimate API cost')
    offers=[p for p in data['price'].values() if p['model_id'] and p['billing_method']=='metered-api' and p['status']=='current'
        and routes_for_price(p,data['access'].values()) and any(r['unit'] in UNITS for r in p['rates'])]
    ids=sorted({p['model_id'] for p in offers},key=lambda i:data['model'][i]['identity']['name'])
    if not ids:st.info('No documented compatible model/API offers.');return
    preferred=st.session_state.get('workbench_model','gpt-6-1-sol')
    model=st.selectbox('Model for estimate',ids,index=ids.index(preferred) if preferred in ids else 0,format_func=lambda i:data['model'][i]['identity']['name'])
    cols=st.columns(3)
    with cols[0]:inp=st.number_input('Input tokens per run',min_value=0,value=1000,step=100)
    with cols[1]:out=st.number_input('Output tokens per run',min_value=0,value=1000,step=100,help='Include billable thinking / reasoning tokens.')
    with cols[2]:runs=st.number_input('Runs',min_value=1,value=1,step=1)
    allprices=[p for p in offers if p['model_id']==model]
    currencies=sorted({r['currency'] for p in allprices for r in p['rates'] if r['currency']})
    with st.expander('Advanced billing options'):
        currency=st.selectbox('Currency',currencies,index=currencies.index('USD') if 'USD' in currencies else 0)
        mode=st.selectbox('Billing mode',sorted({cost_mode(p) for p in allprices}),index=sorted({cost_mode(p) for p in allprices}).index('standard') if 'standard' in {cost_mode(p) for p in allprices} else 0)
    prices=[p for p in allprices if cost_mode(p)==mode and all(r['currency'] in {None,currency} for r in p['rates'])]
    prices.sort(key=lambda p:((p['tier'] or '').lower() not in {'standard','default'},p['provider_id'],p['id']))
    if not prices:st.info('No documented offers for this currency and mode. No conversion is inferred.');return
    default=next((i for i,p in enumerate(prices) if estimate_runs(p,data['access'].values(),input_tokens=inp,output_tokens=out,runs=int(runs))['supported']),0)
    selected=st.selectbox('Documented API route',[p['id'] for p in prices],index=default,format_func=lambda i:offer_label(data,data['price'][i]))
    p=data['price'][selected]
    metrics={r['metric'] for r in p['rates']}
    cached=writes=writes5=writes1=0;as_of=date.today();tod=time(12,0);holiday=None
    with st.expander('Request details & evidence'):
        if metrics & {'cached_input','cache_read','cache_write','cache_write_5m','cache_write_1h'}:
            st.caption('Cache tokens are disjoint subsets of total input, per run. No automatic reuse is assumed.')
            if metrics & {'cached_input','cache_read'}:cached=st.number_input('Cached read tokens',min_value=0,value=0,step=100)
            if 'cache_write' in metrics:writes=st.number_input('Cache write tokens',min_value=0,value=0,step=100)
            if 'cache_write_5m' in metrics:writes5=st.number_input('5-minute cache write tokens',min_value=0,value=0,step=100)
            if 'cache_write_1h' in metrics:writes1=st.number_input('1-hour cache write tokens',min_value=0,value=0,step=100)
        as_of=st.date_input('Price effective date',value=date.today())
        if mode in {'peak','off-peak'}:
            tod=st.time_input('Request time UTC',value=time(12,0))
            holiday={'Unknown':None,'No':False,'Yes':True}[st.selectbox('Chinese public holiday',['Unknown','No','Yes'])]
        st.write('Offer conditions: '+show(p['conditions']));st.write('Region: '+show(p['region']))
        st.caption('Verified '+p['verified_at']+' · effective '+show(p['effective_from'])+' to '+show(p['effective_to']))
        source_panel(data,p['evidence_ids'])
        st.markdown(f"[Canonical prices]({link('data/pricing.yaml')}) · [Canonical access]({link('data/access.yaml')})")
        st.json(p,expanded=False)
    request=dict(input_tokens=inp,output_tokens=out,cached_tokens=cached,cache_write_tokens=writes,cache_write_5m_tokens=writes5,
        cache_write_1h_tokens=writes1,as_of=as_of.isoformat(),request_time=datetime.combine(as_of,tod,timezone.utc),chinese_public_holiday=holiday)
    result=estimate_runs(p,data['access'].values(),runs=int(runs),**request)
    st.caption(f'{currency} · {mode} · {inp:,} input / {out:,} output tokens per run · {int(runs):,} identical runs · cache reads {cached:,} / writes {writes+writes5+writes1:,} · region {p["region"] or "not established"}')
    if not result['supported']:
        st.warning('Calculation unsupported for this request');st.write('\n'.join('- '+r for r in result['reasons']))
    else:
        cols=st.columns(2)
        with cols[0]:st.metric('Per-run text-token subtotal',f"{result['currency']} {result['per_run']}")
        with cols[1]:st.metric('Total text-token subtotal',f"{result['currency']} {result['total']}")
        st.caption('Excludes tools, taxes, storage, retries and other modalities. Account eligibility is not verified.')
        comparable=[]
        for offer in prices:
            r=estimate_runs(offer,data['access'].values(),runs=int(runs),**request)
            if r['supported'] and r['currency']==currency:
                comparable.append({'Route':offer_label(data,offer),'Per run':float(r['per_run']),'Total':float(r['total']),'Currency':currency,'Checked':offer['verified_at']})
        if comparable:
            st.write('Compatible documented offers for this request')
            st.dataframe(comparable,hide_index=True)
        with st.expander('Calculation breakdown & limitations'):
            st.dataframe(result['components'],hide_index=True)
            for warning in result['warnings']+result['assumptions']:st.caption(warning)
            for ident in result['route_ids']:
                route=data['access'][ident];st.write(route_label(route,data));st.write(show(route['conditions']+route['restrictions']))
    with st.expander('Subscriptions, credits & other units'):
        st.caption('Account allowances and subscriptions are separate products. They are not converted into API token prices.')
        provider_ids={r['provider_id'] for r in model_routes(data['model'][model],data)}
        other=[p for p in data['price'].values() if p['billing_method']!='metered-api' and (p['model_id']==model or p['model_id'] is None and p['provider_id'] in provider_ids)]
        if other:st.dataframe(price_rows(data,other),hide_index=True)
        else:st.caption('No other billing offer recorded for these routes.')
    with st.expander('Routes with pricing that cannot be estimated'):
        unsupported=[r for r in model_routes(data['model'][model],data)
                     if not any(p['billing_method']=='metered-api' and current_price(p)
                                and routes_for_price(p,[r]) for p in route_prices(r,data))]
        for route in unsupported:
            st.write(route_label(route,data))
            st.caption('No compatible current normalized token tariff. Account allowances, media units, conditional tariffs and missing rates cannot be converted into a token estimate.')
            if route.get('research_details'):st.json(route['research_details'],expanded=False)
            source_panel(data,route['evidence_ids'])

def recent_changes(data):
    st.header('Recent changes')
    since=st.date_input('Since',value=date(2026,9,1))
    future=st.checkbox('Include future announced events',value=False)
    releases=sorted([r for r in data['release'].values() if r['event_date'] and r['event_date']>=since.isoformat() and (future or r['event_date']<=date.today().isoformat())],key=lambda r:r['event_date'],reverse=True)
    for r in releases:
        with st.expander(f"{r['event_date']} · {r['event_type'].replace('_',' ')} · {data['model'].get(r['model_id'],{}).get('identity',{}).get('name') or r['model_label'] or r['provider_id']}"):
            st.write(r['summary']);source_panel(data,r['evidence_ids'])
    st.subheader('Post-launch behavior findings')
    bs=sorted([b for b in data['behavior'].values() if (b['reported_at'] or b['observed_at'])>=since.isoformat()],key=lambda b:b['reported_at'] or b['observed_at'],reverse=True)
    for b in bs:
        with st.expander((b['reported_at'] or b['observed_at'])+' · '+short(b['claim'],100)):behavior_panel(data,b)
    if not bs:st.caption('No dated behavior findings in this period. Unverified reports are not presented as confirmed regressions.')
    with st.expander('Repository observation history'):
        path=ROOT/'history/revisions.yaml';revisions=[r for r in cached_history((path.stat().st_mtime_ns,path.stat().st_size)) if r['observed_at']>=since.isoformat()]
        st.caption('First-observed baselines do not mean newly released or newly available.')
        st.dataframe([{'Observed':r['observed_at'],'Effective':r['effective_from'],'Type':r['entity_type'],'Entity':r['entity_id'],'Change':r['reason']} for r in reversed(revisions)],hide_index=True)
        if revisions:
            chosen=st.selectbox('Inspect history revision',[r['id'] for r in reversed(revisions)])
            revision=next(r for r in revisions if r['id']==chosen);st.json(revision,expanded=False)
            prior=next((r for r in cached_history((path.stat().st_mtime_ns,path.stat().st_size)) if r['id']==revision['previous_revision_id']),None)
            if prior:st.write('Prior value');st.json(prior['value'],expanded=False)
            else:st.info('No earlier recorded value; this is the first observation.')
        st.markdown(f"[Full journal]({link('history/revisions.yaml')}) · [Historical semantics]({link('history/README.md')})")

data=cached_data(fingerprint())
st.title('Model Intelligence')
st.caption('A field guide to models, evidence and ways to use them.')
st.sidebar.caption('WORKBENCH')
page=st.sidebar.radio('Explore',['Model Explorer','Compare 2–5 Models','Capability Explorer','Cost Explorer','Recent Changes'])
st.sidebar.caption('Research maintenance is paused. This public guide makes no model calls.')
{'Model Explorer':model_explorer,'Compare 2–5 Models':compare_models,'Capability Explorer':capability_explorer,
 'Cost Explorer':cost_explorer,'Recent Changes':recent_changes}[page](data)
