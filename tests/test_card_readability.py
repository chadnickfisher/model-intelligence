from copy import deepcopy
import pytest
from streamlit.testing.v1 import AppTest
from explorer.data import load
from explorer.presentation import task_card_evidence, card_watchouts, observation_summary, complete_summary, readable_conditions
from tools.knowledge import ROOT


def card_app():
    code=(ROOT/'streamlit_app.py').read_text(encoding='utf-8').split('data=cached_data(fingerprint())')[0]
    code+='''
data=load()
selection=st.selectbox('Test task',['None','coding.frontend','coding.debugging'])
model_card(data,data['model']['qwen3-8-27b'],None if selection=='None' else selection,details=False)
'''
    return AppTest.from_string(code,default_timeout=30).run()


def section(at,start,end):
    values=[m.value for m in at.markdown]
    first=next(i for i,v in enumerate(values) if v.startswith(start))
    last=next(i for i,v in enumerate(values[first+1:],first+1) if v.startswith(end))
    return '\n'.join(values[first:last])


def test_selected_frontend_explains_exact_match_and_changes_contextual_limits():
    data=load();model=data['model']['qwen3-8-27b']
    findings,benchmarks=task_card_evidence(model,data,'coding.frontend')
    assert len(findings)==1 and findings[0]['task_ids']==['coding.frontend']
    assert benchmarks and all(b['benchmark']['name']=='Arena Frontend' for b in benchmarks)
    assert any(b['value']==1598 for b in benchmarks)
    frontend=card_watchouts(model,data,'coding.frontend')
    debugging=card_watchouts(model,data,'coding.debugging')
    assert any('production-correctness' in v for v in frontend)
    assert not any('Empty content from turn6' in v for v in frontend)
    assert any('Empty content from turn6' in v for v in debugging)
    at=card_app();assert not at.exception
    assert not any(m.value.startswith('**Task fit') for m in at.markdown)
    assert any(m.value=='**Watch-outs**' for m in at.markdown)
    at.selectbox[0].set_value('coding.frontend').run();assert not at.exception
    fit=section(at,'**Task fit','**Watch-outs**')
    assert '**Suitability:** Unknown' in fit
    assert 'preference' in fit and 'executable interactions' in fit
    assert '**Evidence confidence:**' not in fit
    assert 'Long local debugging chats' not in fit
    limits=section(at,'**Watch-outs**','**How to use it**')
    assert 'production-correctness' in limits and 'Empty content from turn6' not in limits
    assert any('1598 Arena rating' in m.value for m in at.markdown)
    at.selectbox[0].set_value('coding.debugging').run();assert not at.exception
    assert '**Suitability:** Unknown' in section(at,'**Task fit','**Watch-outs**')
    assert 'Empty content from turn6' in section(at,'**Watch-outs**','**How to use it**')


def test_access_and_prices_are_native_bullets_and_missing_fields_stay_unknown():
    at=card_app();assert not at.exception
    access=section(at,'**How to use it**','**Price**')
    price=section(at,'**Price**','**Context**')
    assert '- **' in access and '- **Input**:' in price and '- **Output**:' in price
    code=(ROOT/'streamlit_app.py').read_text(encoding='utf-8').split('data=cached_data(fingerprint())')[0]
    code+='''
data=load()
model=__import__('copy').deepcopy(data['model']['qwen3-8-27b'])
model['capabilities']=[];model['limitations']=[];model['access_ids']=[];model['price_ids']=[]
data['access_coverage']={};data['benchmark']={};data['behavior']={}
data['task_assessment']={}
model_card(data,model,'coding.frontend',details=False)
'''
    empty=AppTest.from_string(code,default_timeout=30).run();assert not empty.exception
    text='\n'.join(m.value for m in empty.markdown)
    assert 'No documented watch-outs for this task yet.' in text
    assert 'ability remains unknown' in text and 'Access not yet documented' in text
    assert 'Model-specific price not yet documented' in text


def test_observation_summary_keeps_later_limits_and_distinguishes_published_fix():
    first='A practitioner observed a failure under the documented runtime '+('with the same configuration ' * 20)+'.'
    text=first+' A proposed fix is not independently verified. An unrelated introductory sentence.'
    assert complete_summary(text)==text
    assert complete_summary('  '+text+'  ')==text
    assert complete_summary(' \n ')==''
    assert '…' not in complete_summary(text)
    record={'claim':text,'status':'unknown','fix':{'measured_improvement':None}}
    assert observation_summary(record).endswith('Current outcome unresolved.')
    record['status']='fix_published'
    assert observation_summary(record).endswith('Published change; measured recovery not established.')
    at=card_app()
    assert any(e.label == 'Full observation & evidence' for e in at.expander)
    assert any('Current outcome unresolved.' in m.value for m in at.markdown)
    assert not any('Published change: none' in m.value or 'Published change: proposed' in m.value for m in at.markdown)


@pytest.mark.parametrize('record_id, qualification',[
    ('behavior-48882f04dfc15338',
     'Reporter explicitly cannot determine whether issue is model-specific or a vLLM distributed-executor defect.'),
    ('behavior-43bd710be14825f8',
     'Native W4A4/NVFP4 loading remains blocked by global-scale support in MLX MoE operations'),
    ('behavior-5efb34ca46925fce',
     'Same build with MRV2 restores 91.58%.'),
    ('behavior-5a2416670e75187b',
     'Current API docs still warn about audio-processing blocks and variable latency'),
])
def test_canonical_behavior_summary_preserves_qualifications(record_id, qualification):
    record=load()['behavior'][record_id]
    assert qualification in record['claim']
    assert complete_summary(record['claim'])==record['claim']
    assert observation_summary(record)==record['claim']+' Current outcome unresolved.'


def test_readable_conditions_preserves_meaningful_values_and_only_omits_known_marker():
    values=['reasoning','high','bf16','context_32768','exact_named_release_effort_retained',
            'exact_named_release_effort_retained under this configuration',
            'Configuration retained in arena_rows']
    assert readable_conditions(values)==[
        'reasoning','high','bf16','context_32768',
        'exact_named_release_effort_retained under this configuration',
        "Configuration retained in the source's model configuration table"]
    conditions=next(b['conditions'] for b in load()['benchmark'].values()
                    if 'exact_named_release_effort_retained' in b['conditions'])
    assert readable_conditions(conditions)==[
        value.replace('arena_rows',"the source's model configuration table")
        for value in conditions if value!='exact_named_release_effort_retained']


def test_palette_has_readable_contrast_and_mobile_wrapping_rule():
    def luminance(color):
        rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in rgb]
        return sum(c*w for c,w in zip(linear,(0.2126,0.7152,0.0722)))
    for foreground in ('#24533F','#365744','#20372C'):
        for background in ('#FAF7EF','#F0F5ED','#D9E8DC'):
            assert (luminance(background)+0.05)/(luminance(foreground)+0.05)>=4.5
    code=(ROOT/'streamlit_app.py').read_text(encoding='utf-8')
    assert 'border-left:4px solid #24533F' in code
    assert '@media(max-width:800px)' in code and 'flex-wrap:wrap' in code
