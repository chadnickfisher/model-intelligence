from streamlit.testing.v1 import AppTest
from tools.knowledge import ROOT


def test_cards_and_comparison_show_measurements_setups_and_missing_results():
    # Synthetic fixtures test rendering only; they are never saved as canonical research.
    fixture="""
fixture_data=load()
for model_id,effort in [('gpt-6-astra','high'),('gpt-6-1-sol','max')]:
    model=fixture_data['model'][model_id]
    fixture_data['benchmark'][model_id]={
      'id':model_id,'model_id':model_id,'judgment_ids':[model['capabilities'][0]['id']],
      'benchmark':{'name':'Synthetic quality test','version':'1','metric':'pass rate','unit':'%','direction':'higher'},
      'value':50,'model_version':model_id,'harness':'Synthetic harness','effort':effort,
      'provider_id':'openai','tools':[],'measured_at':'2026-10-06','observed_at':'2026-10-07',
      'evidence_class':'independent_quality','source_ids':model['evidence_ids'][:1],
      'conditions':['Synthetic fixture'],'limitations':['Not a real measurement'],'evidence_notes':[]}
data=fixture_data
"""
    script=(ROOT/'streamlit_app.py').read_text(encoding='utf-8').replace('data=cached_data(fingerprint())',fixture)
    at=AppTest.from_string(script,default_timeout=30).run()
    assert not at.exception
    assert any('Benchmark highlights' in m.value for m in at.markdown)
    at.sidebar.radio[0].set_value('Compare 2–5 Models').run()
    chooser=next(w for w in at.multiselect if w.label=='Models to compare')
    chooser.set_value(['gpt-6-astra','gpt-6-1-sol','ai21-jamba2-mini']).run()
    assert not at.exception
    assert any('Different configurations' in c.value for c in at.caption)
    assert any('Unknown / not established' in c.value for c in at.caption)
    assert any('Synthetic quality test' in m.value for m in at.markdown)
    assert any('Not a real measurement' in m.value for m in at.markdown)
    assert any('Recorded rationale' in m.value for m in at.markdown)
