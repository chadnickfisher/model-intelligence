"""Transactional application and isolated publication preserve operator work."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import pytest
from tools import research_publish as pub, research_build as build, research_batch as batch
from tools.research_runs import state_hash


def git(root, *args):
    return batch.git(root, *args)


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    root = tmp_path / 'root'
    root.mkdir()
    git(root, 'init', '-q')
    git(root, 'config', 'user.name', 'Fixture')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'core.autocrlf', 'false')
    git(root, 'remote', 'add', 'origin', 'https://github.com/chadnickfisher/model-intelligence.git')
    files = {'.gitignore': b'.local/\n', 'README.md': b'Unrelated public fixture\n',
             'data/state.json': b'{"value": 1}\n', 'data/second.yaml': b'value: 1\n',
             'tools/validate.py': b'print("fixture validation passed")\n', 'tools/render.py': b'pass\n'}
    for name, raw in files.items():
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    git(root, 'add', '--all'); git(root, 'commit', '-qm', 'Public fixture')
    stage = root / '.local/research/build'
    candidate = stage / 'candidate'; candidate.mkdir(parents=True)
    new_files = {**files, 'data/state.json': b'{"value": 2}\n', 'data/second.yaml': b'value: 2\n'}
    for name, raw in new_files.items():
        path = candidate / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    def canonical(directory):
        return {('fixture', 'state'): ('data/state.json', json.loads((directory / 'data/state.json').read_bytes()))}
    monkeypatch.setattr(pub, 'canonical', canonical)
    receipt = {'status': 'validated_current_repository_candidate', 'model_calls': 0, 'published': False,
               'source_head': git(root, 'rev-parse', 'HEAD'), 'source_files': build.hashes(files),
               'candidate_files': build.hashes(new_files), 'current_state_hash': state_hash({('fixture','state'):{'value':1}}),
               'candidate_state_hash': state_hash({('fixture','state'):{'value':2}}),
               'changes': {name:{'previous_sha256':pub.fingerprint(files[name]),'sha256':pub.fingerprint(raw)}
                           for name,raw in new_files.items() if raw != files[name]},
               'checks':[{'command':[s],'exit_code':0} for s in ['tools/render.py','tools/validate.py']]}
    raw = build.encoded(receipt); (stage/'build-receipt.json').write_bytes(raw)
    return root, stage, receipt, pub.fingerprint(raw), root/'.local/research/transaction'


def test_success_repeat_and_unrelated_index_preserved(prepared):
    root, stage, r, pin, tx = prepared
    before = (root/'.git/index').read_bytes()
    result = pub.apply(root,stage,r,pin,tx)
    assert result['status']=='applied' and result['changed_files']==2
    assert pub.apply(root,stage,r,pin,tx)['status']=='already_applied'
    assert (root/'.git/index').read_bytes()==before
    assert (tx/'originals/data/state.json').read_bytes()==b'{"value": 1}\n'


@pytest.mark.parametrize('mutation',['candidate','source','head','manifest','path','checks'])
def test_stale_and_forged_inputs_stop_before_write(prepared,mutation):
    root,stage,r,pin,tx=prepared
    if mutation=='candidate': (stage/'candidate/README.md').write_text('Changed')
    if mutation=='source': (root/'README.md').write_text('Concurrent work')
    if mutation=='head': git(root,'commit','--allow-empty','-qm','Advanced')
    if mutation=='manifest': r['changes']['data/state.json']['sha256']='0'*64
    if mutation=='path': r['candidate_files']['../escape']='0'*64
    if mutation=='checks': r['checks']=[]
    with pytest.raises(ValueError): pub.apply(root,stage,r,pin,tx)
    assert (root/'data/state.json').read_bytes()==b'{"value": 1}\n'
    assert not tx.exists()


def test_receipt_bytes_are_operator_pinned(prepared):
    _,stage,_,pin,_=prepared
    assert pub.pinned_json(stage/'build-receipt.json',pin)
    with pytest.raises(ValueError): pub.pinned_json(stage/'build-receipt.json','0'*64)


def test_failure_rolls_back_all_owned_writes(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    original=pub.replace_file; calls=[]
    def fail_second(target,raw):
        calls.append(target)
        if len(calls)==2: raise OSError('Synthetic write failure')
        return original(target,raw)
    monkeypatch.setattr(pub,'replace_file',fail_second)
    with pytest.raises(OSError): pub.apply(root,stage,r,pin,tx)
    assert pub.current_mode(root,r)=='ready'
    assert json.loads((tx/'transaction.json').read_text())['status']=='rolled_back'


def test_validation_failure_rolls_back(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    monkeypatch.setattr(pub,'validate',lambda root: batch.require(False,'Synthetic check failure'))
    with pytest.raises(ValueError): pub.apply(root,stage,r,pin,tx)
    assert pub.current_mode(root,r)=='ready'


def test_interrupted_process_can_recover(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    original=pub.replace_file; calls=[]
    def crash(target,raw):
        calls.append(target)
        if len(calls)==2: raise KeyboardInterrupt()
        return original(target,raw)
    monkeypatch.setattr(pub,'replace_file',crash)
    with pytest.raises(KeyboardInterrupt): pub.apply(root,stage,r,pin,tx)
    monkeypatch.setattr(pub,'replace_file',original)
    assert pub.recover(root,tx,r,pin)['status']=='rolled_back'
    assert pub.current_mode(root,r)=='ready'
    with pytest.raises(ValueError,match='Existing transaction'): pub.apply(root,stage,r,pin,tx)


def test_recovery_preserves_concurrent_edits(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    original=pub.validate
    def concurrent(root):
        (root/'data/state.json').write_text('{"value": 99}\n')
        raise ValueError('Synthetic concurrent edit')
    monkeypatch.setattr(pub,'validate',concurrent)
    with pytest.raises(ValueError): pub.apply(root,stage,r,pin,tx)
    result=json.loads((tx/'transaction.json').read_text())
    assert result['status']=='rollback_conflicts' and result['conflicts']==['data/state.json']
    assert json.loads((root/'data/state.json').read_text())=={'value':99}
    assert (root/'data/second.yaml').read_bytes()==b'value: 1\n'


def test_new_generated_file_recovery(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    (stage/'candidate/data/new.md').write_bytes(b'New generated fixture\n')
    r['candidate_files']['data/new.md']=pub.fingerprint(b'New generated fixture\n')
    r['changes']['data/new.md']={'previous_sha256':None,'sha256':r['candidate_files']['data/new.md']}
    monkeypatch.setattr(pub,'validate',lambda root: batch.require(False,'Synthetic failed validation'))
    with pytest.raises(ValueError): pub.apply(root,stage,r,pin,tx)
    assert not (root/'data/new.md').exists()


def test_tampered_recovery_backup_refused(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    monkeypatch.setattr(pub,'validate',lambda root: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt): pub.apply(root,stage,r,pin,tx)
    (tx/'originals/data/state.json').write_text('Tampered backup')
    with pytest.raises(ValueError,match='backup differs'): pub.recover(root,tx,r,pin)
    assert json.loads((root/'data/state.json').read_text())=={'value':2}


def test_recovery_does_not_restore_under_a_new_git_commit(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    monkeypatch.setattr(pub,'validate',lambda root: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt): pub.apply(root,stage,r,pin,tx)
    git(root,'commit','--allow-empty','-qm','Concurrent commit')
    assert pub.recover(root,tx,r,pin)['conflicts']==['git_head']
    assert json.loads((root/'data/state.json').read_text())=={'value':2}


def test_recovery_reports_linked_path_and_recovers_other_owned_files(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    monkeypatch.setattr(pub,'validate',lambda root: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt): pub.apply(root,stage,r,pin,tx)
    real=pub.file_hash
    def linked(path):
        if path.name=='state.json': raise ValueError('Synthetic linked target')
        return real(path)
    monkeypatch.setattr(pub,'file_hash',linked)
    assert pub.recover(root,tx,r,pin)['conflicts']==['data/state.json']
    assert (root/'data/second.yaml').read_bytes()==b'value: 1\n'


def test_rollout_needs_exact_pin_and_release_keeps_checkout(prepared,monkeypatch):
    root,stage,r,pin,tx=prepared
    (root/'tools/runtime.py').write_bytes(b'# Synthetic trusted rollout\n')
    (stage/'candidate/tools/runtime.py').write_bytes(b'# Synthetic trusted rollout\n')
    r['source_files']['tools/runtime.py']=r['candidate_files']['tools/runtime.py']=pub.fingerprint(b'# Synthetic trusted rollout\n')
    rollout=pub.rollout_manifest(root,r)
    assert set(rollout['changes'])=={'tools/runtime.py'}
    with pytest.raises(ValueError,match='exact pin'):
        pub.prepare(root,stage,r,pin,root/'.local/research/rejected','main')
    real_run=subprocess.run
    def tests(command,**kwargs):
        if 'pytest' in command: return subprocess.CompletedProcess(command,0,stdout='Synthetic suite passed',stderr='')
        return real_run(command,**kwargs)
    monkeypatch.setattr(subprocess,'run',tests)
    index=(root/'.git/index').read_bytes()
    release=pub.prepare(root,stage,r,pin,root/'.local/research/release','main',rollout)
    assert release['rollout_commit']!=release['source_head'] and release['commit']!=release['rollout_commit']
    assert release['application_status']=='applied' and not release['published']
    assert release['research_paths']==['data/second.yaml','data/state.json']
    assert pub.current_mode(root,r)=='ready' and (root/'.git/index').read_bytes()==index


@pytest.mark.parametrize('branch',['--help','HEAD','bad..branch'])
def test_unsafe_publication_branch_rejected(prepared,branch):
    root,_,_,_,_=prepared
    with pytest.raises((ValueError,subprocess.CalledProcessError)): pub.branch_check(root,branch)


def release_fixture(prepared,monkeypatch):
    root,stage,r,pin,_=prepared
    real_run=subprocess.run
    monkeypatch.setattr(subprocess,'run',lambda command,**kw:
        subprocess.CompletedProcess(command,0,stdout='Synthetic tests passed',stderr='')
        if 'pytest' in command else real_run(command,**kw))
    directory=root/'.local/research/release'
    return directory,pub.prepare(root,stage,r,pin,directory,'main')


def test_remote_advancement_refuses_push(prepared,monkeypatch):
    directory,release=release_fixture(prepared,monkeypatch)
    monkeypatch.setattr(pub,'remote_head',lambda *a:'f'*40)
    with pytest.raises(ValueError,match='Remote advanced'): pub.publish(directory,release)
    assert not (directory/'publication-receipt.json').exists()


def test_already_matching_remote_is_publication_noop(prepared,monkeypatch):
    directory,release=release_fixture(prepared,monkeypatch)
    monkeypatch.setattr(pub,'remote_head',lambda *a:release['commit'])
    first=pub.publish(directory,release)
    assert first['published'] and not first['ci_verified']
    assert pub.publish(directory,release)==first


def test_push_verified_by_exact_remote_commit(prepared,monkeypatch):
    directory,release=release_fixture(prepared,monkeypatch)
    heads=iter([release['source_head'],release['commit']])
    monkeypatch.setattr(pub,'remote_head',lambda *a:next(heads))
    real_git=batch.git; pushes=[]
    def fake_git(root,*args):
        if args[0]=='push': pushes.append(args); return ''
        return real_git(root,*args)
    monkeypatch.setattr(batch,'git',fake_git)
    assert pub.publish(directory,release)['published']
    assert pushes==[('push','origin',release['commit']+':refs/heads/main')]


def test_modified_prepared_release_refuses_push(prepared,monkeypatch):
    directory,release=release_fixture(prepared,monkeypatch)
    (directory/'repository/README.md').write_text('Concurrent alteration')
    monkeypatch.setattr(pub,'remote_head',lambda *a:pytest.fail('No remote call before verification'))
    with pytest.raises(ValueError,match='release differs'): pub.publish(directory,release)


@pytest.mark.parametrize('conclusion,status',[('success','published_ci_verified'),('failure','ci_failed'),(None,'ci_pending')])
def test_ci_matches_exact_commit_branch_workflow_and_latest_attempt(prepared,monkeypatch,conclusion,status):
    directory,release=release_fixture(prepared,monkeypatch)
    monkeypatch.setattr(pub,'remote_head',lambda *a:release['commit'])
    record={'head_sha':release['commit'],'head_branch':'main','event':'push','path':'.github/workflows/ci.yml',
            'run_number':10,'run_attempt':2,'id':123,'html_url':'https://github.com/example/run',
            'status':'completed' if conclusion else 'in_progress','conclusion':conclusion}
    old={**record,'run_attempt':1,'conclusion':'success','status':'completed'}
    unrelated={**record,'head_sha':'0'*40,'run_number':99,'conclusion':'success'}
    monkeypatch.setattr(subprocess,'run',lambda *a,**k:subprocess.CompletedProcess(a,0,
        stdout=json.dumps({'workflow_runs':[old,unrelated,record]}),stderr=''))
    assert pub.verify_ci(directory,release)['status']==status
