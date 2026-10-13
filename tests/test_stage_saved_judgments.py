from copy import deepcopy
import subprocess
import pytest
from tools import research_stage_records as writer
from tools.migrate_v2 import write_yaml

def fixture(tmp_path,monkeypatch):
    def git(*args):return subprocess.check_output(['git','-C',str(tmp_path),*args],text=True).strip()
    git('init','--quiet');git('config','user.name','Test');git('config','user.email','test@example.com')
    tasks={'schema_version':'1.0','records':[]};sources={'schema_version':'1.0','records':[]}
    write_yaml(tmp_path/'data/task-assessments.yaml',tasks);write_yaml(tmp_path/'evidence/sources.yaml',sources)
    git('add','data','evidence');git('commit','--quiet','-m','Fixture baseline')
    monkeypatch.setattr(writer,'__file__',str(tmp_path/'tools/research_stage_records.py'))
    compiled={'assessments':[],'sources':[],'models':{},'changed_task_ids':[],'merge_baseline':git('rev-parse','HEAD')}
    return git,compiled

def test_noop_replay_does_not_write_or_require_a_new_clean_checkout(tmp_path,monkeypatch):
    git,compiled=fixture(tmp_path,monkeypatch)
    (tmp_path/'already-staged-note.txt').write_text('Existing local result')
    before=(tmp_path/'data/task-assessments.yaml').read_bytes()
    result=writer.stage(tmp_path,compiled,observed_at='2026-10-13',summary='Fixture')
    assert result['status']=='no_change' and (tmp_path/'data/task-assessments.yaml').read_bytes()==before

def test_dirty_candidate_rejected_before_any_canonical_write(tmp_path,monkeypatch):
    git,compiled=fixture(tmp_path,monkeypatch)
    compiled['sources']=[{'id':'fixture'}]
    (tmp_path/'unrelated.txt').write_text('Do not overwrite')
    before=(tmp_path/'evidence/sources.yaml').read_bytes()
    with pytest.raises(ValueError,match='clean isolated'):
        writer.stage(tmp_path,compiled,observed_at='2026-10-13',summary='Fixture')
    assert (tmp_path/'evidence/sources.yaml').read_bytes()==before

def test_moved_baseline_rejected_before_any_canonical_write(tmp_path,monkeypatch):
    git,compiled=fixture(tmp_path,monkeypatch);compiled['sources']=[{'id':'fixture'}]
    compiled['merge_baseline']='0'*40
    with pytest.raises(ValueError,match='baseline differs'):
        writer.stage(tmp_path,compiled,observed_at='2026-10-13',summary='Fixture')
    assert writer.read(tmp_path/'evidence/sources.yaml')['records']==[]

def test_sorted_json_handoff_preserves_yaml_order_and_values():
    import json
    original={'schema_version':'1.0','records':[{'id':'one','z':3,'a':None,'nested':{'z':False,'a':['x','y']}}]}
    transported=json.loads(json.dumps(original,sort_keys=True))
    transported['records'][0]['new_field']={'b':1,'a':2}
    result=writer.preserve_key_order(original,transported)
    assert result==transported
    assert list(result)==list(original)
    assert list(result['records'][0])==['id','z','a','nested','new_field']
    assert list(result['records'][0]['nested'])==['z','a']
    assert original['records'][0].get('new_field') is None

def test_record_array_order_is_not_changed_by_mapping_order_preservation():
    original=[{'id':'first','z':1,'a':2},{'id':'second','a':3,'z':4}]
    incoming=[{'z':4,'id':'second','a':3},{'a':2,'id':'first','z':1},{'id':'new','value':None}]
    result=writer.preserve_key_order(original,incoming)
    assert result==incoming and [row['id'] for row in result]==['second','first','new']
    assert list(result[0])==list(original[1]) and list(result[1])==list(original[0])
