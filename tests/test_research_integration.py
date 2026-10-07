from tools.git_baselines import git_bytes, first_file_commit
from explorer.data import load, behavior_findings
from tools.knowledge import ROOT,read


def test_imported_identity_gates_and_original_baseline_are_preserved():
    data=load()
    new=[j for m in data['model'].values() for j in m['capabilities'] if j['provenance'].get('research_batch_id')=='public-research-2026-10-07']
    assert len(new)==84 and all(j['scope']=='direct' and len(j['task_ids'])==1 for j in new)
    # Reported non-IT variants and pre-release checkpoints are not silently enrolled.
    assert not any(j['task_ids']==['coding.frontend'] for j in data['model']['gemma-4-31b-it']['capabilities'] if j['provenance'].get('origin')=='research')
    import yaml
    path='history/migrations/2026-10-07-capabilities.yaml'
    assert len(yaml.safe_load(git_bytes(first_file_commit(path),path))['records'])==71


def test_capped_free_routes_are_not_unlimited_metered_offers():
    data=load()
    for route in data['access'].values():
        if route.get('research_details',{}).get('route_class') in {'hosted_free_tier_api','hosted_evaluation_api'}:
            assert all(data['price'][p]['billing_method']=='free' for p in route['price_ids'])


def test_behavior_fix_notes_do_not_fabricate_measured_recovery_or_quality_badges():
    data=load()
    assert all(b['fix']['measured_improvement'] is None for b in data['behavior'].values())
    model=data['model']['gpt-6-1-sol']
    highlighted=behavior_findings(model,data,highlights=True)
    assert highlighted and len(highlighted)<len(behavior_findings(model,data))
    assert all(b['research_details']['layer']!='client_harness' for b in highlighted)
    assert any(m['kind']=='throughput' for b in data['behavior'].values() for m in b['metrics'])


def test_nested_claim_evidence_resolves_in_public_source_records():
    data=load()
    model=data['model']['gpt-6-1-sol']
    ids={s for j in model['capabilities'] for s in j['supporting_evidence_ids']+j['contradictory_evidence_ids']}
    assert ids<=set(data['source'])
