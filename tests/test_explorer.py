import pytest
from streamlit.testing.v1 import AppTest
from explorer.data import load, filter_models, claims, comparison, context_tokens, open_weights, UNKNOWN
from tools.knowledge import ROOT


@pytest.fixture(scope='module')
def data():
    return load()


def test_filters_distinguish_direct_related_and_unknown(data):
    from copy import deepcopy
    fixture = deepcopy(data)
    fixture['task_assessment'] = {str(i): {
        'model_id': model, 'task_id': task,
        'aggregate': {'suitability': rating, 'evidence_confidence': confidence}}
        for i, (model, task, rating, confidence) in enumerate([
            ('claude-sonnet-5-5', 'coding.repository_work', 'medium', 'low'),
            ('gpt-6-astra', 'coding.architecture', 'high', 'high'),
            ('gpt-oss-20b', 'coding.repository_work', 'unknown', None),
            ('qwen3-8-27b', 'coding.repository_work', 'disputed', None),
            ('claude-haiku-4-5', 'coding.repository_work', 'not_supported', 'high')])}
    def selected(**kwargs):
        return {m['id'] for m in filter_models(fixture, task='coding.repository_work', **kwargs)}
    assert selected() == {'claude-sonnet-5-5', 'qwen3-8-27b'}
    assert selected(include_related=True) == selected()
    assert selected(confidence=['high']) == {'qwen3-8-27b'}
    assert selected(suitability=['not_supported'], confidence=['high']) == {'claude-haiku-4-5'}
    assert selected(suitability=[]) == set()
    assert all(m['identity']['creator'] == 'Anthropic' for m in filter_models(data, vendors=['Anthropic']))
    assert all(open_weights(m) is True for m in filter_models(data, weights='Downloadable'))
    assert all(context_tokens(m) >= 1000000 for m in filter_models(data, minimum_context=1000000))
    unknown = {m['id'] for m in filter_models(data, minimum_context=1000000, include_unknown_context=True)}
    assert 'ai21-jamba2-mini' in unknown
    assert 'ai21-jamba2-mini' not in {m['id'] for m in filter_models(data, minimum_context=1000000)}
    assert len(filter_models(data, search='not a model')) == 0


def test_compare_preserves_unknown_and_actual_warning(data):
    ids=['gpt-6-astra','claude-sonnet-5-5']
    missing=next(t for t in data['task'] if not any(t in j['task_ids'] for i in ids for j in data['model'][i]['capabilities']))
    rows = comparison(data, ids, missing)
    assert all(row['Task evidence'] == UNKNOWN for row in rows)
    rows = comparison(data, ['gemini-3-8-flash', 'gpt-oss-20b'], 'agent.long_horizon')
    assert rows[1]['Task evidence'] == UNKNOWN
    assert 'Conditional; use tests and checkpointing' in rows[0]['Task evidence']
    with pytest.raises(ValueError):
        comparison(data, ['gpt-6-astra'])
    with pytest.raises(ValueError):
        comparison(data, ['gpt-6-astra'] * 2)


def widget(elements, label):
    return next(e for e in elements if e.label == label)


def app():
    return AppTest.from_file(str(ROOT / 'streamlit_app.py'), default_timeout=30).run()


def test_app_load_and_model_filters(data):
    at = app()
    assert not at.exception
    widget(at.multiselect, 'Vendor').set_value(['Anthropic']).run()
    expected = len(filter_models(data, vendors=['Anthropic']))
    assert not at.exception and any(f'{expected} models with matching' in c.value for c in at.caption)
    widget(at.text_input, 'Find a model').set_value('no matching model').run()
    assert not at.exception and any('No records match' in i.value for i in at.info)


def test_app_task_search_uses_canonical_ratings(data):
    at = app()
    widget(at.selectbox, 'What are you working on?').set_value('agent.tool_use').run()
    expected = filter_models(data, task='agent.tool_use')
    assert not at.exception
    assert widget(at.multiselect, 'Task suitability').value == ['high','medium','low','disputed']
    assert any(f'{len(expected)} models with matching' in c.value for c in at.caption)
    widget(at.multiselect, 'Task suitability').set_value([]).run()
    assert not at.exception and any('No assessed models match' in i.value for i in at.info)


def test_every_model_detail_renders(data):
    at = app()
    for model_id in data['model']:
        widget(at.selectbox, 'Inspect model').set_value(model_id).run()
        assert not at.exception, model_id


def test_app_compare_and_capabilities():
    at = app()
    at.sidebar.radio[0].set_value('Compare 2–5 Models').run()
    assert not at.exception
    widget(at.multiselect, 'Models to compare').set_value(['gpt-6-astra', 'claude-sonnet-5-5']).run()
    assert not at.exception
    widget(at.selectbox, 'Comparison task').set_value('coding.architecture').run()
    assert not at.exception and any('Task fit' in m.value for m in at.markdown)
    at.sidebar.radio[0].set_value('Capability Explorer').run()
    widget(at.selectbox, 'Capability task').set_value('coding.repository_work').run()
    assert any('Task-specific finding' in h.value for h in at.subheader)
    widget(at.checkbox, 'Show related compound/unresolved evidence').set_value(False).run()
    direct_count = len(at.subheader)
    widget(at.checkbox, 'Show related compound/unresolved evidence').set_value(True).run()
    assert not at.exception and len(at.subheader) > direct_count


def test_app_cost_and_recent_changes():
    at = app()
    at.sidebar.radio[0].set_value('Cost Explorer').run()
    assert not at.exception
    widget(at.selectbox, 'Model for estimate').set_value('gpt-6-astra').run()
    assert at.metric and 'USD' in at.metric[0].value
    widget(at.number_input, 'Cached read tokens').set_value(1001).run()
    assert not at.exception and any('Calculation unsupported' in w.value for w in at.warning)
    widget(at.number_input, 'Cached read tokens').set_value(0).run()
    widget(at.number_input, 'Runs').set_value(3).run()
    assert not at.exception and at.metric
    at.sidebar.radio[0].set_value('Recent Changes').run()
    assert not at.exception
    assert any('Repository changelog' in h.value for h in at.subheader)
    assert not any(s.label == 'Inspect history revision' for s in at.selectbox)
    assert any('Haiku 5.5' in m.value for m in at.markdown)
