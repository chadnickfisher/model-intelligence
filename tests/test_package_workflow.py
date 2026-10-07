import io
import json
import stat
import zipfile
from pathlib import Path
import pytest
from tools.package_workflow import (archive_members, package_files, ready_update, raw_research,
                                    digest, write_prepared, REPOSITORY, repo_guard, safe_name, preflight_update)


def zipped(entries):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        for name,data in entries:z.writestr(name,data)
    return out.getvalue()


@pytest.mark.parametrize('name',['../escape.json','/root.json','C:/file.json','data/x:secret','data/CON.json','data/trailing.','data\\escape.json'])
def test_archive_rejects_unsafe_paths(name):
    # Python's ZIP writer normalizes backslashes on Windows before serialization.
    with pytest.raises(ValueError):safe_name(name)
    if '\\' in name:return
    with pytest.raises(ValueError):archive_members(zipped([(name,b'{}')]))


def test_ready_preflight_prior_hash_before_any_mutation(tmp_path):
    p=tmp_path/'research'/'old.md';p.parent.mkdir();p.write_bytes(b'old')
    manifest={'files':[{'path':'research/new.md','operation':'write','previous_sha256':None},
                       {'path':'research/old.md','operation':'write','previous_sha256':'0'*64}]}
    with pytest.raises(ValueError):preflight_update(tmp_path,manifest)
    assert p.read_bytes()==b'old' and not (p.parent/'new.md').exists()


def test_archive_case_collisions_and_symlinks_rejected():
    with pytest.raises(ValueError):archive_members(zipped([('a.json',b'1'),('A.json',b'2')]))
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        i=zipfile.ZipInfo('link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,'target')
    with pytest.raises(ValueError):archive_members(out.getvalue())


def test_archive_hash_size_and_expansion_guards(tmp_path,monkeypatch):
    p=tmp_path/'x.zip';p.write_bytes(zipped([('a.json',b'{}')]))
    with pytest.raises(ValueError):package_files(p,'0'*64)
    with pytest.raises(ValueError):package_files(p,expected_bytes=1)
    import tools.package_workflow as workflow
    monkeypatch.setattr(workflow,'MAX_BYTES',200)
    with pytest.raises(ValueError):archive_members(zipped([('x',b'x'*500)]))


def test_raw_and_ready_packages_cannot_be_confused():
    with pytest.raises(ValueError):raw_research({'package.json':b'{}'})
    with pytest.raises(ValueError):ready_update({'raw.json':b'{}'},[])


def test_ready_payload_paths_hashes_and_code_guard():
    manifest={'package_type':'ready-update','repository':REPOSITORY,'branch':'main','base_commit':'a'*40,
              'files':[{'path':'evidence/new.yaml','operation':'write','previous_sha256':None,'sha256':digest(b'ok')}]}
    files={'package.json':json.dumps(manifest).encode(),'payload/evidence/new.yaml':b'ok'}
    assert ready_update(files,['evidence/new.yaml'])==manifest
    with pytest.raises(ValueError):ready_update(files,['evidence/other.yaml'])
    files['payload/evidence/new.yaml']=b'changed'
    with pytest.raises(ValueError):ready_update(files,['evidence/new.yaml'])
    for path in ['tools/validate.py','.github/workflows/check.yml','schema/access.json','explorer/incoming.py',
                 'research/new.md','history/research/input.json','AGENTS.md']:
        manifest['files'][0]['path']=path
        with pytest.raises(ValueError,match='outside reviewed allowlist'):
            ready_update({'package.json':json.dumps(manifest).encode(),'payload/'+path:b'ok'},[path])


def test_prepare_is_idempotent_and_preflights_conflicts(tmp_path):
    out=tmp_path/'prepared';files={'a.json':b'{}','behavior/b.json':b'[]'}
    write_prepared(out,files,{'kind':'raw'});write_prepared(out,files,{'kind':'raw'})
    assert (out/'a.json').read_bytes()==b'{}'
    with pytest.raises(ValueError):write_prepared(out,{'new.json':b'ok','a.json':b'conflict'}, {})
    assert not (out/'new.json').exists()


def test_repo_guards_wrong_remote_branch_base_and_dirty(monkeypatch,tmp_path):
    import tools.package_workflow as w
    answers={'remote':REPOSITORY,'branch':'main','rev-parse':'a'*40,'status':''}
    monkeypatch.setattr(w,'git',lambda repo,*args:answers[args[0]])
    assert repo_guard(tmp_path,'a'*40)==tmp_path.resolve()
    for key,bad in [('remote','https://github.com/other/repo'),('branch','topic'),('rev-parse','b'*40),('status',' M data/access.yaml')]:
        old=answers[key];answers[key]=bad
        with pytest.raises(ValueError):repo_guard(tmp_path,'a'*40)
        answers[key]=old


def test_push_destination_guard_is_independent_of_fetch_origin(monkeypatch,tmp_path):
    import tools.package_workflow as w
    def answer(repo,*args):
        if args[0]=='remote':return 'https://github.com/other/repo' if '--push' in args else REPOSITORY
        return {'branch':'main','rev-parse':'a'*40,'status':''}[args[0]]
    monkeypatch.setattr(w,'git',answer)
    with pytest.raises(ValueError):repo_guard(tmp_path,'a'*40)


def test_ready_apply_uses_only_local_trusted_checks_and_rejects_extra_changes(tmp_path,monkeypatch):
    import tools.package_workflow as w
    entry={'path':'research/new.md','operation':'write','previous_sha256':None,'sha256':digest(b'ok')}
    manifest={'files':[entry]};files={'payload/research/new.md':b'ok'}
    commands=[]
    monkeypatch.setattr(w.subprocess,'run',lambda command,**kwargs:commands.append(command))
    monkeypatch.setattr(w,'git',lambda repo,*args:'research/new.md' if args[0]=='ls-files' else '')
    assert w.apply_update(tmp_path,files,manifest,False,'message')['state']=='applied-and-checked'
    assert (tmp_path/'research/new.md').read_bytes()==b'ok'
    assert [c[1:] for c in commands]==[['tools/render.py'],['tools/validate.py'],['-m','pytest','-q']]
    (tmp_path/'research/new.md').unlink()
    monkeypatch.setattr(w,'git',lambda repo,*args:'research/new.md\nother.md' if args[0]=='ls-files' else '')
    with pytest.raises(ValueError,match='outside intended paths'):w.apply_update(tmp_path,files,manifest,False,'message')
