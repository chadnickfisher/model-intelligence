"""Temporary fictional assessments test cards; no canonical model judgments change."""
from streamlit.testing.v1 import AppTest

from tools.knowledge import ROOT


def app_prefix():
    return (ROOT / 'streamlit_app.py').read_text(encoding='utf-8').split('data=cached_data(fingerprint())')[0]


def card_app(rating='medium', confidence='low'):
    setup = '''
data=load()
model=data['model']['qwen3-8-27b']
task='agent.tool_use'
assessment=next(a for a in data['task_assessment'].values()
                if a['model_id']==model['id'] and a['task_id']==task)
assessment['aggregate']={
    'policy_version':'1', 'suitability':RATING, 'evidence_confidence':CONFIDENCE,
    'assessed_at':'2026-10-08',
    'rationale':'Fictional aggregate: useful bounded workflow with material checking.',
    'confidence_rationale':'Fictional evidence rationale: one evaluator and limited setup detail.',
    'supporting_evidence_ids':assessment['evidence_ids'][:1],
    'contradictory_evidence_ids':[], 'conflict_rationale':None,
    'watch_outs':['Fictional first limitation.', 'Fictional second limitation.',
                 'Fictional third limitation must remain visible.'], 'access_ids':[]}
if RATING=='not_supported':
    assessment.update(applicability='excluded',result='excluded',judgment_ids=[])
    model['capabilities']=[]
if RATING=='disputed':
    from copy import deepcopy
    original=next(j for j in model['capabilities'] if j['id'] in assessment['judgment_ids'])
    counter=deepcopy(original)
    original['judgment']='Fictional supporting conclusion.'
    original['confidence']='medium'
    counter.update(id='fixture-counterfinding', judgment='Fictional contrary conclusion.', confidence='low')
    model['capabilities'].append(counter)
    assessment['judgment_ids'].append(counter['id'])
    assessment['aggregate']['conflict_rationale']='Fictional unresolved same-setup disagreement.'
    assessment['aggregate']['contradictory_evidence_ids']=assessment['evidence_ids'][:1]
model_card(data,model,task,details=True)
'''
    setup = 'RATING=' + repr(rating) + '\nCONFIDENCE=' + repr(confidence) + '\n' + setup
    return AppTest.from_string(app_prefix() + setup, default_timeout=30).run()


def task_section(at):
    values = [m.value for m in at.markdown]
    start = next(i for i, text in enumerate(values) if text.startswith('**Task fit'))
    end = next(i for i, text in enumerate(values[start + 1:], start + 1) if text == '**Watch-outs**')
    return '\n'.join(values[start:end])


def test_aggregate_card_preserves_visible_full_card_sections_and_prices():
    at = card_app()
    assert not at.exception
    text = '\n'.join(m.value for m in at.markdown)
    task = task_section(at)
    assert '**Suitability:** Medium' in task and '**Evidence confidence:** Low' in task
    assert '**Why this rating?**' in task
    assert '- Fictional aggregate: useful bounded workflow' in task
    assert 'Fictional evidence rationale' not in task and '**Applies to:**' not in task
    details = next(e for e in at.expander if e.label.startswith('Task assessment:'))
    detail_text = '\n'.join(m.value for m in details.markdown)
    assert 'Fictional evidence rationale' in detail_text and '**Applies to:**' in detail_text
    assert any('Sources checked' in c.value for c in details.caption)
    assert 'Fictional third limitation must remain visible.' in text
    for section in ('**Watch-outs**', '**How to use it**', '**Price**', '**Context**',
                    '**Benchmark highlights**', '**Post-launch observations**'):
        assert section in text
    assert '- **Input**:' in text and '- **Output**:' in text
    assert '**API:**' in text and '**Subscription:**' in text
    assert any(e.label == 'Evidence & details' for e in at.expander)
    assert any(t.label == 'Access & prices' for t in at.tabs)
    assert any(t.label == 'Specifications' for t in at.tabs)
    assert any(t.label == 'Behavior & gaps' for t in at.tabs)
    # Sources and research dates belong to details, outside the compact task section.
    assert '**Supporting evidence**' not in task and '](' not in task
    assert '**Supporting evidence**' in detail_text and '](' in detail_text
    assert not any('**Checked:**' in m.value or '**Reported:**' in m.value for m in at.markdown)
    # Compare the actual existing visible content, not just its section headings.
    baseline = AppTest.from_string(app_prefix() + '''
data=load()
model_card(data,data['model']['qwen3-8-27b'],'agent.tool_use',details=True)
''', default_timeout=30).run()
    assert not baseline.exception
    def section(app, start, end):
        values = [m.value for m in app.markdown]
        first = next(i for i, value in enumerate(values) if value.startswith(start))
        last = next(i for i, value in enumerate(values[first + 1:], first + 1) if value.startswith(end))
        return values[first:last]
    for start, end in [('**How to use it**', '**Price**'), ('**Price**', '**Context**'),
                       ('**Context**', '**Benchmark highlights**'),
                       ('**Benchmark highlights**', '**Post-launch observations**'),
                       ('**Post-launch observations**', '[Canonical profile]')]:
        assert section(at, start, end) == section(baseline, start, end)


def test_disputed_has_underlying_confidence_and_full_contrary_evidence():
    at = card_app('disputed', None)
    assert not at.exception
    task = task_section(at)
    assert '**Suitability:** Disputed' in task
    assert '**Evidence confidence:**' not in task
    assert 'Fictional unresolved same-setup disagreement.' in task
    details = next(e for e in at.expander if e.label.startswith('Task assessment:'))
    detail_text = '\n'.join(m.value for m in details.markdown)
    assert 'Underlying finding' not in task
    assert 'Underlying finding (Medium evidence confidence)' in detail_text
    assert 'Underlying finding (Low evidence confidence)' in detail_text
    assert 'Fictional supporting conclusion.' in detail_text and 'Fictional contrary conclusion.' in detail_text
    assert '**Contrary / limiting evidence**' in detail_text
    assert any('Confidence belongs to the underlying findings' in c.value for c in at.caption)


def test_not_supported_can_display_high_evidence_confidence():
    at = card_app('not_supported', 'high')
    assert not at.exception
    task = task_section(at)
    assert '**Suitability:** Not supported' in task
    assert '**Evidence confidence:** High' in task
    assert not any(i.value == 'Task evidence not yet curated.' for i in at.info)


def test_assessment_and_policy_edits_invalidate_cache_fingerprint(tmp_path):
    (tmp_path / 'data').mkdir()
    (tmp_path / 'schema').mkdir()
    assessment = tmp_path / 'data/task-assessments.yaml'
    policy = tmp_path / 'schema/task-assessment-record.schema.json'
    assessment.write_text('before', encoding='utf-8')
    policy.write_text('{}', encoding='utf-8')
    script = app_prefix() + '\nfrom pathlib import Path\nROOT=Path(' + repr(str(tmp_path)) + ')\n'
    script += '''
before=fingerprint()
(ROOT/'data/task-assessments.yaml').write_text('after assessment change',encoding='utf-8')
after_assessment=fingerprint()
(ROOT/'schema/task-assessment-record.schema.json').write_text('{"changed":true}',encoding='utf-8')
after_policy=fingerprint()
st.session_state['assessment_invalidates']=before!=after_assessment
st.session_state['policy_invalidates']=after_assessment!=after_policy
'''
    at = AppTest.from_string(script, default_timeout=30).run()
    assert not at.exception
    assert at.session_state['assessment_invalidates']
    assert at.session_state['policy_invalidates']
