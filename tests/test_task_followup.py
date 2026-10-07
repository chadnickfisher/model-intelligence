"""Guard public task evidence without depending on private work receipts."""
import subprocess
from tools.knowledge import ROOT, canonical
from tools.git_baselines import git_state

BATCH = 'public-task-followup-2026-10-07'


def followup():
    current = canonical()
    judgments = [(ident, j) for (kind, ident), (_, model) in current.items()
                 if kind == 'model' for j in model['capabilities']
                 if j.get('provenance', {}).get('research_batch_id') == BATCH]
    scope = {'models': sorted({ident for ident, _ in judgments}),
             'judgment_ids': [j['id'] for _, j in judgments],
             'observed_at': '2026-10-07'}
    rows = [row for (kind, _), (_, row) in current.items() if kind == 'benchmark'
            and any('Added by ' + BATCH in note for note in row['evidence_notes'])]
    return scope, current, rows


def test_public_domain_checks_have_actual_references_and_unknown_gaps():
    scope, current, _ = followup()
    assert len(scope['models']) == 26
    checks = [row for (kind, _), (_, row) in current.items()
              if kind == 'research_coverage' and row['model_id'] in scope['models']
              and row['domain'] in {'capabilities', 'benchmarks'}]
    assert {(row['model_id'], row['domain']) for row in checks} == {
        (model, domain) for model in scope['models']
        for domain in {'capabilities', 'benchmarks'}}
    for row in checks:
        assert row['checked_at'] and (row['evidence_ids'] or row['search_references'])
        if row['result'] in {'unknown', 'blocked'}:
            assert row['remaining_gaps']


def test_public_git_versions_preserve_prior_claims_and_factual_dates():
    scope, _, _ = followup()
    commits = subprocess.check_output(
        ['git', 'log', '--reverse', '--format=%H', '--', 'models'],
        cwd=ROOT, encoding='utf-8').splitlines()
    for commit in commits:
        after = git_state(commit)
        if any(j.get('provenance', {}).get('research_batch_id') == BATCH
               for (kind, _), model in after.items() if kind == 'model'
               for j in model['capabilities']):
            parent = subprocess.check_output(['git', 'rev-parse', commit + '^'],
                                             cwd=ROOT, encoding='utf-8').strip()
            before = git_state(parent)
            break
    else:
        raise AssertionError('Public task evidence introduction is absent')
    for ident in scope['models']:
        previous, model = before[('model', ident)], after[('model', ident)]
        new = {j['id']: j for j in model['capabilities']}
        assert all(new[j['id']] == j for j in previous['capabilities'])
        assert model['verified_at'] == previous['verified_at']
        assert set(previous['evidence_ids']) <= set(model['evidence_ids'])


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
