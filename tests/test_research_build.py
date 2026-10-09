"""Builders preserve current edits and never turn a forged audit into writes."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import pytest
from test_research_batch import baseline, fixture, MID, SID, TODAY
from tools import research_audit as audit, research_build as build, research_batch as batch
from tools.knowledge import canonical, record_hash
from tools.research_runs import state_hash


def prepare(packet, assignment, baseline, current):
    report = audit.audit(packet, assignment, baseline, current)
    selected = report.pop('selected_packet')
    compiled = batch.compile_batch(selected, assignment, baseline)
    return report, selected, compiled


def test_merge_preserves_disjoint_current_fields_and_immutable_input(fixture, baseline):
    packet, assignment = fixture
    current = deepcopy(baseline)
    current[('model', MID)]['limitations'].append('Synthetic concurrent limitation')
    before = deepcopy((packet, current))
    report, _, compiled = prepare(packet, assignment, baseline, current)
    plan = build.merge_ready(compiled, report, baseline, current)
    assert plan['candidate'][('model', MID)]['limitations'] == current[('model', MID)]['limitations']
    assert plan['candidate'][('model', MID)]['notes'] == packet['changes'][1]['record']['notes']
    assert plan['changes'][0]['previous_hash'] == record_hash(current[('model', MID)])
    assert (packet, current) == before


def test_conflicted_field_and_dependency_are_not_built(fixture, baseline):
    packet, assignment = fixture
    current = deepcopy(baseline)
    current[('source', SID)]['title'] += ' Synthetic concurrent change'
    report, _, compiled = prepare(packet, assignment, baseline, current)
    plan = build.merge_ready(compiled, report, baseline, current)
    assert plan['changes'] == [] and plan['candidate'] == current


def test_already_present_source_does_not_prevent_dependent_new_field(fixture, baseline):
    packet, assignment = fixture
    current = deepcopy(baseline)
    current[('source', SID)] = deepcopy(packet['changes'][0]['record'])
    report, _, compiled = prepare(packet, assignment, baseline, current)
    assert report['counts'] == {'already_present': 1, 'ready': 1}
    plan = build.merge_ready(compiled, report, baseline, current)
    assert len(plan['changes']) == 1 and plan['changes'][0]['kind'] == 'model'
    assert plan['candidate'][('source', SID)] == current[('source', SID)]


def test_forged_ready_list_and_modified_value_pins_are_refused(fixture, baseline):
    packet, assignment = fixture
    report, _, compiled = prepare(packet, assignment, baseline, baseline)
    modified = deepcopy(report)
    modified['ready_unit_ids'].append(modified['ready_unit_ids'][0])
    with pytest.raises(ValueError, match='Ready unit'): build.merge_ready(compiled, modified, baseline, baseline)
    modified = deepcopy(report)
    modified['units'][0]['proposed_value_hash'] = '0' * 64
    with pytest.raises(ValueError, match='pin differs'): build.merge_ready(compiled, modified, baseline, baseline)


def test_current_advancement_requires_new_audit(fixture, baseline):
    packet, assignment = fixture
    report, _, compiled = prepare(packet, assignment, baseline, baseline)
    advanced = deepcopy(baseline)
    advanced[('model', MID)]['limitations'].append('Advanced after audit')
    with pytest.raises(ValueError, match='state differs'): build.merge_ready(compiled, report, baseline, advanced)


def test_audit_recomputed_instead_of_trusting_edited_decisions(fixture, baseline):
    packet, assignment = fixture
    report, selected, _ = prepare(packet, assignment, baseline, baseline)
    selected_raw = build.encoded(selected)
    report.update(original_sha256='a'*64, assignment_sha256='b'*64, selected_sha256=sha256(selected_raw).hexdigest())
    assert build.verify_audit(packet, assignment, baseline, baseline, report, selected_raw, 'a'*64, 'b'*64) == selected
    report['ready_unit_ids'].pop()
    with pytest.raises(ValueError, match='recomputation'):
        build.verify_audit(packet, assignment, baseline, baseline, report, selected_raw, 'a'*64, 'b'*64)


@pytest.mark.parametrize('mutation', ['packet', 'assignment', 'selected'])
def test_bad_input_binding_refused_before_recomputation(fixture, baseline, monkeypatch, mutation):
    packet, assignment = fixture
    report, selected, _ = prepare(packet, assignment, baseline, baseline)
    selected_raw = build.encoded(selected)
    report.update(original_sha256='a'*64, assignment_sha256='b'*64, selected_sha256=sha256(selected_raw).hexdigest())
    if mutation == 'packet': report['original_sha256'] = '0'*64
    if mutation == 'assignment': report['assignment_sha256'] = '0'*64
    if mutation == 'selected': selected_raw += b' '
    monkeypatch.setattr(audit, 'audit', lambda *a, **k: pytest.fail('Must fail before recomputing'))
    with pytest.raises(ValueError): build.verify_audit(packet, assignment, baseline, baseline, report, selected_raw, 'a'*64, 'b'*64)


def test_collection_upserts_write_once_and_preserve_existing_rows(tmp_path, monkeypatch):
    doc = tmp_path / 'evidence/sources.yaml'
    doc.parent.mkdir()
    batch.write_yaml(doc, {'schema_version': '1.0', 'records': [{'id': 'keep', 'v': 1}, {'id': 'edit', 'v': 1}]})
    calls = []
    real = batch.write_yaml
    monkeypatch.setattr(batch, 'write_yaml', lambda path, value: (calls.append(path), real(path, value)))
    build.write_updates(tmp_path, [{'kind':'source','record':{'id':'edit','v':2}},
                                   {'kind':'source','record':{'id':'new','v':3}}], {})
    assert calls == [doc]
    import yaml
    assert yaml.safe_load(doc.read_text())['records'] == [{'id':'keep','v':1}, {'id':'edit','v':2}, {'id':'new','v':3}]


def test_snapshot_excludes_ignored_credentials_and_rejects_new_unknown_files(tmp_path):
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    (tmp_path/'.gitignore').write_text('.local/\n',encoding='utf-8')
    (tmp_path/'README.md').write_text('Public fixture',encoding='utf-8')
    (tmp_path/'.local').mkdir()
    (tmp_path/'.local/credential.json').write_text('Private fixture',encoding='utf-8')
    subprocess.run(['git','-C',str(tmp_path),'add','.gitignore','README.md'],check=True)
    assert '.local/credential.json' not in build.public_snapshot(tmp_path)
    (tmp_path/'unexpected.json').write_text('{}',encoding='utf-8')
    with pytest.raises(ValueError,match='Unreviewed'): build.public_snapshot(tmp_path)


def test_failed_staging_and_modified_candidate_cannot_be_reused(tmp_path, monkeypatch):
    root = batch.ROOT
    if not tmp_path.resolve().is_relative_to(root/'.local/research'): pytest.skip('Requires private basetemp')
    current = {k:r for k,(_,r) in canonical(root).items()}
    merged = deepcopy(current)
    merged[('model',MID)]['notes'].append('Synthetic isolated builder test; not real research.')
    change = {'kind':'model','record':merged[('model',MID)],'previous_hash':record_hash(current[('model',MID)]),'evidence_ids':[SID]}
    plan = {'candidate':merged,'changes':[change],'ready_unit_ids':['synthetic-unit'],
            'current_state_hash':state_hash(current),'candidate_state_hash':state_hash(merged),'counts_by_kind':{'model':1}}
    before = (root/'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes()
    receipt = build.stage_updates(root,plan,tmp_path/'valid',TODAY,{'packet_sha256':'a'*64})
    assert receipt['status']=='validated_current_repository_candidate'
    assert receipt['source_head'] == batch.git(root,'rev-parse','HEAD')
    assert build.stage_updates(root,plan,tmp_path/'valid',TODAY,{'packet_sha256':'a'*64})['repeat_noop']
    assert (root/'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes() == before


    assert {k:r for k,(_,r) in canonical(tmp_path/'valid/candidate').items()} == merged
    (tmp_path/'valid/candidate/README.md').write_text('Tampered candidate',encoding='utf-8')
    with pytest.raises(ValueError,match='modified'): build.stage_updates(root,plan,tmp_path/'valid',TODAY,{'packet_sha256':'a'*64})
    real_run = subprocess.run
    def fail_render(command, **kwargs):
        if 'tools/render.py' in command:
            return subprocess.CompletedProcess(command,1,stdout='Synthetic failed render',stderr='')
        return real_run(command,**kwargs)
    monkeypatch.setattr(subprocess,'run',fail_render)
    with pytest.raises(ValueError,match='check failed'): build.stage_updates(root,plan,tmp_path/'failed',TODAY,{'packet_sha256':'a'*64})
    assert (tmp_path/'failed/failed-checks.json').exists() and not (tmp_path/'failed/build-receipt.json').exists()
    with pytest.raises(ValueError): build.stage_updates(root,plan,tmp_path/'failed',TODAY,{'packet_sha256':'a'*64})
    assert (root/'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes() == before


def test_changed_git_commit_refuses_existing_build_before_reuse(tmp_path):
    root = batch.ROOT
    if not tmp_path.resolve().is_relative_to(root/'.local/research'): pytest.skip('Requires private basetemp')
    current = {k:r for k,(_,r) in canonical(root).items()}
    plan = {'candidate':current,'changes':[],'ready_unit_ids':[],
            'current_state_hash':state_hash(current),'candidate_state_hash':state_hash(current),'counts_by_kind':{}}
    files=build.public_snapshot(root)
    target=tmp_path/'stale'
    target.mkdir()
    (target/'build-receipt.json').write_bytes(build.encoded({
        'bindings':{},'source_files':build.hashes(files),'source_head':'0'*40,
        'observed_at':TODAY,'status':'validated_current_repository_candidate',
        'current_state_hash':state_hash(current),'candidate_state_hash':state_hash(current),'ready_unit_ids':[]}))
    with pytest.raises(ValueError,match='different inputs'): build.stage_updates(root,plan,target,TODAY,{})
