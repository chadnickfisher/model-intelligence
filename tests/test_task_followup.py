"""Guard the research follow-up against identity transfer and invented history."""
import json
from tools.knowledge import ROOT, canonical, history


def followup():
    receipt=json.loads((ROOT/'history/research/2026-10-07/task-followup.json').read_text(encoding='utf-8'))
    current=canonical()
    rows=[r for (kind,ident),(_,r) in current.items() if kind=='benchmark' and ident in receipt['benchmark_ids']]
    return receipt,current,rows


def test_followup_has_actual_references_for_every_previously_pending_domain():
    receipt,_,_=followup()
    assert len(set(receipt['models']))==26
    revisions=history()
    matching=[i for i,r in enumerate(revisions) if r['entity_type']=='research_coverage'
              and r['value'] and r['value'].get('research_batch_id')==receipt['research_batch_id']
              and r['value'].get('checked_at')==receipt['observed_at']]
    assert matching
    coverage={r['entity_id']:r['value'] for r in revisions[:max(matching)+1]
              if r['entity_type']=='research_coverage'}
    checks=[r for r in coverage.values() if r is not None]
    assert not any(r['result']=='not_checked' for r in checks)
    followed=[r for r in checks if r['model_id'] in receipt['models']
              and r['domain'] in {'capabilities','benchmarks'}]
    assert {(r['model_id'],r['domain']) for r in followed}=={
        (model,domain) for model in receipt['models'] for domain in {'capabilities','benchmarks'}}
    for r in checks:
        if r['model_id'] in receipt['models'] and r['domain'] in {'capabilities','benchmarks'}:
            assert r['checked_at']==receipt['observed_at']
            assert r['research_batch_id']==receipt['research_batch_id']
            assert r['evidence_ids'] and r['search_references']
            assert r['remaining_gaps']  # A check does not erase evidence uncertainty.


def test_followup_preserves_prior_claims_and_factual_dates_in_observation_history():
    receipt,_,_=followup()
    revisions=history()
    receipt_judgments=set(receipt['judgment_ids'])
    for model in receipt['models']:
        chain=[r for r in revisions if r['entity_type']=='model' and r['entity_id']==model]
        by_id={r['id']:r for r in chain}
        introductions=[]
        for revision in chain:
            if not revision['value'] or not revision['previous_revision_id']:
                continue
            before=by_id[revision['previous_revision_id']]['value']
            prior_ids={j['id'] for j in before['capabilities']} if before else set()
            added_ids={j['id'] for j in revision['value']['capabilities']}-prior_ids
            if added_ids & receipt_judgments:
                introductions.append(revision)
        assert len(introductions)==1
        event=introductions[0]
        previous=by_id[event['previous_revision_id']]
        before=previous['value'];after=event['value']
        for field in set(before)-{'capabilities','evidence_ids'}:
            assert after[field]==before[field]
        assert set(before['evidence_ids'])<=set(after['evidence_ids'])
        assert after['verified_at']==before['verified_at']
        new={j['id']:j for j in after['capabilities']}
        assert all(new[j['id']]==j for j in before['capabilities'])
        assert event['effective_from'] is None
        assert event['observed_at']==receipt['observed_at']


def test_exact_configuration_gates_and_investigated_unknowns_survive():
    receipt,current,rows=followup()
    assert len(rows)==38
    assert all(r['measured_at'] is None for r in rows)
    assert not any(r['model_id']=='qwen3-8-2-4t-a95b' for r in rows)
    live=[r for r in rows if r['model_id']=='gemini-3-8-live']
    assert {r['value'] for r in live}=={96.1,30.1}
    assert all('Extended Thinking High results are excluded' in ' '.join(r['conditions']) for r in live)
    systems=[r for r in rows if r['model_id']=='gpt-live-1']
    assert {r['effort'] for r in systems}=={'Astra medium','Sol low'}
    assert all(r['tools'] and ' + ' in r['model_version'] for r in systems)
    for model in ['qwen3-8-2-4t-a95b','bfl-flux3-video','gemini-omni-1-1-flash','veo-3-1-generate-preview']:
        j=[j for j in current[('model',model)][1]['capabilities'] if j['id'] in receipt['judgment_ids']]
        assert len(j)==1 and j[0]['assessment']=='unknown'


def test_conflicts_and_metric_direction_are_not_flattened():
    _,current,rows=followup()
    dev=[r for r in rows if r['model_id']=='devstral-small-2' and r['benchmark']['version']=='Verified']
    assert {r['value'] for r in dev}=={68.0,65.8}
    assert len({tuple(r['source_ids']) for r in dev})==2
    nem=[r for r in rows if r['model_id']=='nemotron-3-ultra' and r['benchmark']['version']=='Verified']
    assert {r['value'] for r in nem}=={70.7,71.9}
    assert all('conflicts' in ' '.join(r['conditions']) for r in nem)
    distances=[r for r in rows if r['benchmark']['metric']=='average edit distance']
    assert distances and all(r['benchmark']['direction']=='lower' for r in distances)
    images=[r for r in rows if r['model_id'] in {'gpt-image-2-5-flare','gpt-image-2-5-sunburst'}]
    assert all(r['benchmark']['direction']=='lower' and r['evidence_class']=='independent_quality' for r in images)
