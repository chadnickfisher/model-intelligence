from copy import deepcopy
from decimal import Decimal
import json
from jsonschema import Draft202012Validator
from explorer.data import (load, route_status, route_prices, billing_summary, current_price,
                          comparable_api_offers, benchmark_findings, benchmark_compatibility, confidence_trace)
from explorer.cost import estimate_runs, routes_for_price
from tools.knowledge import ROOT


def test_missing_access_is_unknown_and_unavailable_requires_evidence():
    data=load();model=deepcopy(data['model']['qwen3-coder-next']);model['access_ids']=[]
    data['access_coverage']={}
    assert route_status(model,data,'API')=='Not yet documented'
    assert route_status(model,data,'Subscription')=='Not yet documented'
    coverage={'model_id':model['id'],'categories':{'api':{'state':'unavailable','evidence_ids':[]}}}
    data['access_coverage']={'test':coverage}
    assert route_status(model,data,'API')=='Not yet documented'
    coverage['categories']['api']['evidence_ids']=['src-71b3fd269cc8']
    assert route_status(model,data,'API')=='Unavailable (documented)'


def test_credits_are_not_model_prices_and_download_is_not_free_inference():
    data=load();model=data['model']['qwen3-coder-next']
    route=data['access']['access-open-qwen3-coder-next-weights']
    assert 'hardware / hosting' in billing_summary(route,data)
    copied=deepcopy(route)
    copied['price_ids']=['price-providers-inference-providers-hugging-face-335a1fcfc401']
    assert route_prices(copied,data)==[]
    p=data['price'][copied['price_ids'][0]]
    assert not estimate_runs(p,data['access'].values(),input_tokens=1000,output_tokens=1000)['supported']


def test_runs_price_each_request_before_multiplying_and_do_not_infer_cache():
    data=load()
    p=next(p for p in data['price'].values() if p['model_id']=='gpt-6-astra' and p['tier']=='Standard' and '<=272000' in ' '.join(p['conditions']))
    result=estimate_runs(p,data['access'].values(),input_tokens=200000,output_tokens=1000,runs=3)
    assert result['supported']
    assert Decimal(result['total'])==Decimal(result['per_run'])*3
    assert all(c['component']!='cached' for c in result['components'])
    assert not estimate_runs(p,data['access'].values(),input_tokens=1000,output_tokens=1000,runs=0)['supported']


def test_deprecated_route_cannot_support_cost():
    data=load();p=next(p for p in data['price'].values() if p['model_id']=='gpt-6-astra' and p['tier']=='Standard')
    routes=deepcopy(list(data['access'].values()))
    for a in routes:
        if p['id'] in a['price_ids']:a['availability']='deprecated'
    assert routes_for_price(p,routes)==[]


def test_request_respects_provider_context_and_output_limits():
    data=load();p=next(p for p in data['price'].values() if p['model_id']=='ai21-jamba2-mini' and p['verified_at']=='2026-10-07')
    routes=deepcopy(routes_for_price(p,data['access'].values()))
    for route in routes:route['research_details']={'context':'256K','max_output':1000}
    assert estimate_runs(p,routes,input_tokens=1000,output_tokens=1000)['supported']
    assert not estimate_runs(p,routes,input_tokens=256000,output_tokens=1)['supported']
    assert not estimate_runs(p,routes,input_tokens=1000,output_tokens=1001)['supported']
    for route in routes:route['research_details']['context']='Unresolved extended limit'
    assert not estimate_runs(p,routes,input_tokens=1000,output_tokens=1)['supported']


def test_new_research_provenance_does_not_claim_a_migration():
    data=load();model=deepcopy(data['model']['qwen3-coder-next']);j=model['capabilities'][0]
    j['provenance']={'origin':'research','research_batch_id':'public-research-2026-10-07','method':'Task-specific source synthesis'}
    schema=json.loads((ROOT/'schema/model-profile.schema.json').read_text())
    assert not list(Draft202012Validator(schema).iter_errors(model))
    j['provenance']['migration_id']='fabricated'
    assert list(Draft202012Validator(schema).iter_errors(model))


def test_future_and_retired_offers_do_not_appear_as_current_card_prices():
    p={'status':'current','effective_from':'2027-01-01','effective_to':None}
    assert not current_price(p,'2026-10-07')
    assert current_price(p,'2027-01-01')
    p.update(effective_from=None,effective_to='2026-10-06')
    assert not current_price(p,'2026-10-07')


def test_behavior_fix_publication_does_not_require_or_assert_measured_recovery():
    schema=json.loads((ROOT/'schema/behavior-record.schema.json').read_text())
    record={
        'schema_version':'1.0','id':'behavior-0123456789abcdef','model_ids':['gpt-6-1-sol'],
        'provider_id':'openai','product':'Codex','model_version':None,'harness':None,'effort':None,
        'claim':'Synthetic test record','change_type':'service_change','metrics':[{'kind':'throughput','measurement':None}],
        'observed_at':'2026-10-07','reported_at':None,'effective_from':None,'status':'fix_published',
        'fact_status':'acknowledged','confidence':'low','supporting_evidence_ids':['src-0123456789ab'],
        'contradictory_evidence_ids':[],'official_acknowledgment':None,
        'fix':{'published_at':None,'version':None,'summary':'Published update','evidence_ids':['src-0123456789ab'],'measured_improvement':None},
        'conditions':['Not a measured end-to-end task result'],'notes':[]}
    assert not list(Draft202012Validator(schema).iter_errors(record))
    record['metrics'][0]['kind']='universal_speed'
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_price_filter_uses_only_documented_request_compatible_routes_and_currency():
    data=load();model=data['model']['gpt-6-astra']
    offers=comparable_api_offers(model,data,input_tokens=1000,output_tokens=1000,currency='USD')
    assert offers and all(o['currency']=='USD' for o in offers)
    assert not comparable_api_offers(model,data,currency='UNRECORDED')
    model=deepcopy(model);model['price_ids']=[]
    assert not comparable_api_offers(model,data)


def test_benchmark_missing_results_and_configuration_compatibility():
    data=load();model=data['model']['gpt-6-astra'];data['benchmark']={}
    assert not benchmark_findings(model,data)
    assert benchmark_compatibility([])=='No matched measurements for comparison'
    record={'benchmark':{'name':'Example','version':'1','metric':'pass','unit':'%','direction':'higher'},
            'model_version':'exact-checkpoint','harness':'harness1','effort':'high','tools':[],
            'provider_id':'openai','conditions':['Same test'],'evidence_class':'independent_quality'}
    other=deepcopy(record)
    assert benchmark_compatibility([record,other]).startswith('Matching documented setups')
    other['effort']='max'
    assert 'Different configurations' in benchmark_compatibility([record,other])
    other['effort']=None
    assert 'incomplete' in benchmark_compatibility([record,other])
    other['benchmark']['version']='2'
    assert 'Different benchmark versions' in benchmark_compatibility([record,other])


def test_confidence_trace_preserves_relevant_evidence_and_does_not_score_ability():
    data=load();judgment=data['model']['gpt-6-astra']['capabilities'][0]
    trace=confidence_trace(data,judgment)
    assert trace['recorded_confidence']==judgment['confidence']
    assert trace['supporting_sources']
    assert trace['conditions']==judgment['conditions']
    assert trace['rationale_notes']==judgment['evidence_notes']
    assert 'benchmark score do not determine confidence' in trace['caution']
