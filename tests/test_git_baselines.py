"""Checksums, Git-pinned evidence and the simplified current-state workflow."""
from copy import deepcopy
from pathlib import Path
import subprocess
import yaml
import pytest
from tools.knowledge import ROOT, canonical, read, capture, integrity_errors
from tools.git_baselines import git_state, receipt_states, baseline_for
from tools.research_runs import digest
from tools.maintenance import make_pass, pass_errors
from explorer.cost import estimate

def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(value,sort_keys=False),encoding='utf-8')

def git(root,*args):
    return subprocess.check_output(['git',*args],cwd=root,encoding='utf-8').strip()

def small_repo(tmp_path):
    # Only public synthetic data. No network or model calls.
    model={'id':'example','identity':{'version':'v1'}}
    write(tmp_path/'models/test/example/profile.yaml',model)
    mapping={'data/pricing.yaml':[],'data/access.yaml':[],'data/releases.yaml':[],
       'evidence/sources.yaml':[{'id':'src-aaaaaaaaaaaa','accessed_at':'2026-10-07'}],
       'evidence/observations.yaml':[],'data/behavior.yaml':[],'data/access-coverage.yaml':[],
       'data/benchmarks.yaml':[],'data/research-coverage.yaml':[],'data/research-contract.yaml':[],
       'data/research-runs.yaml':[],'data/task-assessments.yaml':[],'data/aliases.yaml':[]}
    for path,rows in mapping.items():write(tmp_path/path,{'records':rows})
    write(tmp_path/'data/capability-taxonomy.yaml',{'capabilities':[]})
    git(tmp_path,'init')
    git(tmp_path,'config','user.name','Synthetic Test')
    git(tmp_path,'config','user.email','test@example.invalid')
    return model

def commit(root):
    git(root,'add','.')
    git(root,'commit','-m','Synthetic fixture')
    return git(root,'rev-parse','HEAD')

def test_compact_capture_detects_edits_removals_and_is_idempotent(tmp_path):
    model=small_repo(tmp_path)
    capture(tmp_path,'2026-10-07','Synthetic baseline',['src-aaaaaaaaaaaa'])
    manifest=read(tmp_path/'data/record-integrity.yaml')
    assert all('value' not in r for r in manifest['records'])
    assert not integrity_errors(tmp_path)
    write(tmp_path/'data/record-integrity.yaml', {**manifest, 'records':manifest['records']+[manifest['records'][0]]})
    assert integrity_errors(tmp_path) == ['Duplicate current record checksum']
    write(tmp_path/'data/record-integrity.yaml', manifest)
    model['identity']['version']='v2'
    write(tmp_path/'models/test/example/profile.yaml',model)
    assert integrity_errors(tmp_path)
    changes=capture(tmp_path,'2026-10-07','Synthetic correction',['src-aaaaaaaaaaaa'])
    assert len(changes)==1 and changes[0]['operation']=='update'
    assert not integrity_errors(tmp_path)
    assert capture(tmp_path,'2026-10-07','Repeated correction',['src-aaaaaaaaaaaa'])==[]
    moved=tmp_path/'models/renamed/example/profile.yaml'
    moved.parent.mkdir(parents=True)
    (tmp_path/'models/test/example/profile.yaml').rename(moved)
    assert integrity_errors(tmp_path)
    assert len(capture(tmp_path,'2026-10-07','Synthetic path correction',['src-aaaaaaaaaaaa']))==1
    assert not integrity_errors(tmp_path)
    moved.unlink()
    assert capture(tmp_path,'2026-10-08','Synthetic removal',['src-aaaaaaaaaaaa'])[0]['operation']=='remove'
    assert not (tmp_path/'history/revisions.yaml').exists()
    with pytest.raises(ValueError):capture(tmp_path,'2026-10-06','Backdate',['src-aaaaaaaaaaaa'])

def test_git_baseline_retains_exact_values_across_same_day_edits_and_removal(tmp_path):
    model=small_repo(tmp_path);first=commit(tmp_path)
    model['identity']['version']='v2';write(tmp_path/'models/test/example/profile.yaml',model);second=commit(tmp_path)
    (tmp_path/'models/test/example/profile.yaml').unlink();commit(tmp_path)
    assert git_state(first,tmp_path)[('model','example')]['identity']['version']=='v1'
    assert git_state(second,tmp_path)[('model','example')]['identity']['version']=='v2'
    with pytest.raises(ValueError):git_state('HEAD',tmp_path)
    with pytest.raises(subprocess.CalledProcessError):git_state('0'*40,tmp_path)

def test_new_git_receipt_freezes_sources_and_rejects_tampering(tmp_path):
    small_repo(tmp_path);base=commit(tmp_path)
    run={'id':'research-run-synthetic','base_commit':base,'baseline_revision_id':'git-'+base}
    write(tmp_path/'data/research-runs.yaml',{'records':[run]});frozen=commit(tmp_path)
    write(tmp_path/'evidence/sources.yaml',{'records':[]});commit(tmp_path)
    current={k:r for k,(_,r) in canonical(tmp_path).items()}
    run={**run,'evidence_commit':frozen}
    baseline,evidence,_=receipt_states(run,'research_run',current,tmp_path)
    assert ('source','src-aaaaaaaaaaaa') in baseline and ('source','src-aaaaaaaaaaaa') in evidence
    assert ('source','src-aaaaaaaaaaaa') not in current
    assert receipt_states({k:v for k,v in run.items() if k!='evidence_commit'},
                          'research_run', current, tmp_path)[1] == evidence
    with pytest.raises(ValueError):receipt_states({**run,'invented_completion':True},'research_run',current,tmp_path)
    with pytest.raises(ValueError):baseline_for({**run,'baseline_revision_id':'git-'+'0'*40},tmp_path)

def test_git_maintenance_carry_forward_requires_the_declared_commit():
    from test_maintenance import fixture
    state,_,original=fixture()
    run=make_pass(state,None,'b'*40,original['id'],original['target_model_ids'],
                  original['watch_manifest'],
                  original['bounds'],original['created_at'],original['slice'])
    assert not pass_errors(run,state,state,None)
    run['carry_forward'][0]['revision_id']='git-'+'c'*40
    assert any('commit differs' in e for e in pass_errors(run,state,state,None))

def test_legacy_receipt_boundary_uses_only_a_synthetic_archive(tmp_path):
    small_repo(tmp_path)
    row = {'id': 'revision-base', 'entity_type': 'access', 'entity_id': 'route-example',
           'value': {'id': 'route-example', 'billing_class': 'unknown'}}
    write(tmp_path/'history/revisions.yaml', {'records': [row]})
    base = commit(tmp_path)
    run = {'id': 'maintenance-pass-synthetic', 'base_commit': base,
           'baseline_revision_id': 'revision-base'}
    write(tmp_path/'data/maintenance-passes.yaml', {'records': [run]})
    write(tmp_path/'history/revisions.yaml', {'records': [row,
          {'id': 'revision-receipt', 'entity_type': 'maintenance_pass',
           'entity_id': run['id'], 'value': run}]})
    frozen = commit(tmp_path)
    write(tmp_path/'data/access.yaml', {'records': [
          {'id': 'route-example', 'billing_class': 'metered_api'}]})
    current = {key: value for key, (_, value) in canonical(tmp_path).items()}
    _, evidence, _ = receipt_states({**run, 'evidence_commit': frozen},
                                   'maintenance_pass', current, tmp_path)
    assert evidence[('access', 'route-example')]['billing_class'] == 'unknown'
    assert current[('access', 'route-example')]['billing_class'] == 'metered_api'


def test_haiku_prompt_price_threshold_is_per_request_and_uses_exact_offer():
    state=canonical()
    prices=[r for (k,_),(_,r) in state.items() if k=='price' and r.get('model_id')=='claude-haiku-5-5' and r['tier'].startswith('Standard')]
    access=[r for (k,_),(_,r) in state.items() if k=='access']
    low=next(p for p in prices if '<=100k' in p['tier']);high=next(p for p in prices if '>100k' in p['tier'])
    assert estimate(low,access,input_tokens=100000,output_tokens=1000)['supported']
    assert not estimate(high,access,input_tokens=100000,output_tokens=1000)['supported']
    assert not estimate(low,access,input_tokens=100001,output_tokens=1000)['supported']
    assert estimate(high,access,input_tokens=100001,output_tokens=1000)['supported']
