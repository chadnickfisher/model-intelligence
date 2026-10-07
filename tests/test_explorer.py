import pytest
from streamlit.testing.v1 import AppTest
from explorer.data import load, filter_models, claims, comparison, context_tokens, open_weights, UNKNOWN
from tools.knowledge import ROOT


@pytest.fixture(scope='module')
def data():
    return load()


def test_filters_distinguish_direct_related_and_unknown(data):
    direct = filter_models(data, task='coding.repository_work')
    related = filter_models(data, task='coding.repository_work', include_related=True)
    assert len(related) > len(direct) > 0
    assert 'gpt-6-astra' not in {m['id'] for m in direct}
    assert 'gpt-6-astra' in {m['id'] for m in related}
    assert filter_models(data, task='coding.architecture') == []
    assert all(m['identity']['creator'] == 'Anthropic' for m in filter_models(data, vendors=['Anthropic']))
    assert all(open_weights(m) is True for m in filter_models(data, weights='Downloadable'))
    assert all(context_tokens(m) >= 1000000 for m in filter_models(data, minimum_context=1000000))
    unknown = {m['id'] for m in filter_models(data, minimum_context=1000000, include_unknown_context=True)}
    assert 'ai21-jamba2-mini' in unknown
    assert 'ai21-jamba2-mini' not in {m['id'] for m in filter_models(data, minimum_context=1000000)}
    assert len(filter_models(data, search='not a model')) == 0


def test_compare_preserves_unknown_and_actual_warning(data):
    rows = comparison(data, ['gpt-6-astra', 'claude-sonnet-5-5'], 'coding.architecture')
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


def test_app_load_and_model_filters():
    at = app()
    assert not at.exception
    widget(at.multiselect, 'Vendor').set_value(['Anthropic']).run()
    assert not at.exception and len(at.dataframe[0].value) == 4
    widget(at.text_input, 'Model name or ID').set_value('no matching model').run()
    assert not at.exception and any('No matching records' in i.value for i in at.info)


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
    assert not at.exception and all(v == UNKNOWN for v in at.dataframe[0].value['Task evidence'])
    at.sidebar.radio[0].set_value('Capability Explorer').run()
    widget(at.selectbox, 'Capability task').set_value('coding.repository_work').run()
    direct_count = len(at.dataframe[0].value)
    widget(at.checkbox, 'Show related compound/unresolved evidence').set_value(True).run()
    assert not at.exception and len(at.dataframe[0].value) > direct_count


def test_app_cost_and_recent_changes():
    at = app()
    at.sidebar.radio[0].set_value('Cost Explorer').run()
    assert not at.exception
    assert at.metric and '0.06' in at.metric[0].value
    widget(at.number_input, 'Cached read tokens').set_value(1001).run()
    assert not at.exception and any('Calculation unsupported' in w.value for w in at.warning)
    widget(at.multiselect, 'Billing method').set_value(['subscription']).run()
    assert not at.exception and at.warning
    at.sidebar.radio[0].set_value('Recent Changes').run()
    assert not at.exception
    assert len(at.dataframe[-1].value) == 730
    assert any('No earlier recorded value' in i.value for i in at.info)
