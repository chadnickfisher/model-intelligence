from copy import deepcopy
from decimal import Decimal

import pytest
from streamlit.testing.v1 import AppTest

from explorer.comparison import (comparison_assessments, comparison_offers,
                                comparison_cost_options, estimate_unavailable_reason, usd_text)
from explorer.data import load
from tools.knowledge import ROOT


def test_suitable_counts_and_confidence_cover_only_explicit_high_medium_tasks():
    states=[('high','high'),('medium','low'),('low','high'),('disputed',None),
            ('not_supported','high'),('unknown',None)]
    data={'task':{str(i):{'label':'Task '+str(i)} for i in range(7)},
          'task_assessment':{str(i):{'model_id':'fixture','task_id':str(i),
              'aggregate':{'suitability':fit,'evidence_confidence':confidence}}
              for i,(fit,confidence) in enumerate(states)}}
    data['task_assessment']['legacy']={'model_id':'fixture','task_id':'6','result':'assessed'}
    summary=comparison_assessments({'id':'fixture'},data)
    assert [a['task_id'] for a in summary['suitable']]==['0','1']
    assert [a['task_id'] for a in summary['other']]==['2','3']
    assert summary['fit_counts']=={'high':1,'medium':1}
    assert summary['confidence_counts']=={'high':1,'medium':0,'low':1}
    assert comparison_assessments({'id':'fixture'},data,'3')['aggregate']['suitability']=='disputed'
    assert comparison_assessments({'id':'fixture'},data,'3')['aggregate']['evidence_confidence'] is None
    assert comparison_assessments({'id':'fixture'},data,'6')['aggregate'] is None
    assert comparison_assessments({'id':'fixture'},data,'missing')['aggregate'] is None
    data['task_assessment']['duplicate']=deepcopy(data['task_assessment']['0'])
    with pytest.raises(ValueError,match='Duplicate'):
        comparison_assessments({'id':'fixture'},data)


def test_costs_keep_exact_provider_units_currency_and_missing_rates():
    data=load()
    model=data['model']['claude-fable-5-1']
    rows=comparison_offers(model,data,10000,2000)
    official=next(o for o in rows if data['price'][o['price_id']]['provider_id']=='anthropic')
    assert Decimal(official['total'])==Decimal('.20')
    price=deepcopy(data['price'][official['price_id']])
    route=deepcopy(next(r for r in data['access'].values() if price['id'] in r['price_ids']))
    for variant in ('euro','subscription','batch','missing-output'):
        clone=deepcopy(price)
        clone['id']='fixture-'+variant
        if variant=='euro':
            for rate in clone['rates']:rate['currency']='EUR'
        elif variant=='subscription':clone['billing_method']='subscription'
        elif variant=='batch':clone['tier']='batch'
        else:clone['rates']=[r for r in clone['rates'] if r['metric']!='output']
        data['price'][clone['id']]=clone
        model['price_ids'].append(clone['id'])
        access=deepcopy(route)
        access.update(id='fixture-route-'+variant,price_ids=[clone['id']])
        data['access'][access['id']]=access
    ids={o['price_id'] for o in comparison_offers(model,data,10000,2000)}
    assert official['price_id'] in ids
    assert not any(i.startswith('fixture-') for i in ids)
    empty=deepcopy(model)
    empty['price_ids']=[]
    assert comparison_offers(empty,data,10000,2000)==[]
    assert usd_text('0')=='$0.00'
    assert usd_text('0.00000001')=='$0.00000001'


def comparison_app():
    prefix=(ROOT/'streamlit_app.py').read_text(encoding='utf-8').split('data=cached_data(fingerprint())')[0]
    script=prefix+'''
data=load()
st.session_state.setdefault('comparison-models',['claude-fable-5-1','qwen3-coder-next','gpt-oss-120b'])
compare_models(data)
'''
    return AppTest.from_string(script,default_timeout=30).run()


def widget(elements,label):
    return next(e for e in elements if e.label==label)


def test_grid_counts_drill_down_and_switch_to_exact_task():
    at=comparison_app()
    assert not at.exception
    assert [b.label for b in at.button]==['3 tasks','2 tasks','1 task']
    at.button[2].click().run()
    assert not at.exception
    breakdown=next(e for e in at.expander if e.label=='Task breakdown')
    included,other=breakdown.dataframe
    assert included.value['Task'].tolist()==['Coding: tests']
    assert included.value['Evidence confidence'].tolist()==['Low']
    assert set(other.value['Fit'])=={'Low','Disputed'}
    assert other.value.loc[other.value['Fit']=='Disputed','Evidence confidence'].tolist()==['On individual findings']
    widget(at.selectbox,'Comparison task').set_value('coding.debugging').run()
    assert not at.exception and not at.button
    grid=next(b for b in at.main if getattr(b,'key',None)=='comparison-grid')
    text='\n'.join(m.value for m in grid.markdown)
    assert 'compare-fit-disputed' in text
    assert text.count('compare-fit-medium')==2
    assert 'On individual findings' in text
    assert any(e.label=='Why these ratings?' for e in at.expander)
    widget(at.selectbox,'Comparison task').set_value('All tasks').run()
    assert not at.exception
    assert [b.label for b in at.button]==['3 tasks','2 tasks','1 task']


def test_shared_workload_updates_chosen_offers_and_zero_task_models_stay_unknown():
    at=comparison_app()
    widget(at.selectbox,'Cost per text request').set_value((1000,1000)).run()
    assert not at.exception
    data=load()
    price_id=widget(at.selectbox,'Cost option — Claude Fable 5.1').value
    offer=next(o for o in comparison_offers(data['model']['claude-fable-5-1'],data,1000,1000)
               if o['price_id']==price_id)
    assert any(m.value=='**'+usd_text(offer['total'])+'**' for m in at.markdown)
    widget(at.multiselect,'Models to compare').set_value(['ai21-jamba2-mini','qwen3-coder-next']).run()
    assert not at.exception
    assert at.button[0].label=='0 tasks'
    assert any('No High/Medium assessments recorded' in c.value for c in at.caption)
    widget(at.selectbox,'Comparison task').set_value('coding.refactoring').run()
    assert not at.exception
    assert any('Not assessed' in m.value for m in at.markdown)


def test_cost_fallbacks_require_exact_route_links_and_preserve_billing_basis():
    data=load()
    model=deepcopy(data['model']['qwen3-coder-next'])
    options=comparison_cost_options(model,data,10000,2000)
    published=next(o for o in options if o['kind']=='api_rates')
    assert data['price'][published['price_id']]['provider_id']=='novita'
    assert published['total'] is None
    assert 'Provider limits' in estimate_unavailable_reason(published['reasons'])
    assert not any(o['kind']=='subscription' for o in options)

    plan=deepcopy(next(p for p in data['price'].values() if p['billing_method']=='subscription'))
    plan.update(id='fixture-plan',provider_id='novita',included_usage=['100 requests per month'])
    data['price'][plan['id']]=plan
    route=deepcopy(data['access'][published['route_ids'][0]])
    route.update(id='fixture-plan-route',methods=['subscription'],price_ids=[plan['id']])
    data['access'][route['id']]=route
    model['access_ids'].append(route['id'])
    options=comparison_cost_options(model,data,10000,2000)
    assert next(o for o in options if o['kind']=='subscription')['price_id']==plan['id']
    assert options[-1]['kind']=='local'
    route['provider_id']='together'
    assert not any(o['kind']=='subscription' for o in comparison_cost_options(model,data,10000,2000))
    route['provider_id']='novita'
    route['availability']='unavailable'
    assert not any(o['kind']=='subscription' for o in comparison_cost_options(model,data,10000,2000))
    route['availability']='documented'
    route['model_id']='different-model'
    assert not any(o['kind']=='subscription' for o in comparison_cost_options(model,data,10000,2000))
    route['model_id']=model['id']
    plan['status']='historical'
    assert not any(o['kind']=='subscription' for o in comparison_cost_options(model,data,10000,2000))
    plan.update(status='current',billing_method='compute',model_id=model['id'])
    route['methods']=['dedicated_host']
    assert next(o for o in comparison_cost_options(model,data,10000,2000) if o['kind']=='compute')['total'] is None
    plan['model_id']='different-model'
    assert not any(o['kind']=='compute' for o in comparison_cost_options(model,data,10000,2000))


def test_grid_shows_rates_for_blocked_estimate_and_keeps_monthly_and_local_off_bar_scale():
    at=comparison_app()
    assert not at.exception
    grid=next(b for b in at.main if getattr(b,'key',None)=='comparison-grid')
    text='\n'.join(m.value for m in grid.markdown)
    assert 'Published API rates' in text
    assert 'Input: 0.2 USD / per 1 million tokens' in text
    assert any('Provider limits are not precise' in c.value for c in grid.caption)
    assert 'No comparable USD offer' not in text
    prefix=(ROOT/'streamlit_app.py').read_text(encoding='utf-8').split('data=cached_data(fingerprint())')[0]
    script=prefix+'''
data=load()
plan=next(p for p in data['price'].values() if p['billing_method']=='subscription')
plan['included_usage']=['100 requests per month']
comparison_cost_cell(data,{'kind':'subscription','price_id':plan['id']},Decimal('1'))
comparison_cost_cell(data,{'kind':'local'},Decimal('1'))
comparison_cost_cell(data,None,Decimal('1'))
'''
    at=AppTest.from_string(script,default_timeout=30).run()
    assert not at.exception
    text='\n'.join(m.value for m in at.markdown)
    assert 'per_month' in text and '100 requests per month' in '\n'.join(c.value for c in at.caption)
    assert 'Self-hosted' in text and 'Cost not yet documented' in text
    assert '<div class="compare-cost-track"' not in text
