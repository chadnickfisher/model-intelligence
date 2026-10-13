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
