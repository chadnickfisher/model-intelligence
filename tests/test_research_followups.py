"""Durable gap lifecycle, exact queries and frozen assignment consumption."""
from copy import deepcopy
from datetime import date, timedelta
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from tools.knowledge import ROOT, canonical, integrity_errors, read
from tools.research_followups import (
    assignment_inputs, followup_errors, followup_id, merge_followups,
    public_url, render_followups, select_followups, write_assignment_inputs,
)
from tools.research_runs import make_run

TODAY = date.today().isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()


@pytest.fixture
def state():
    return {('model', 'model-a'): {'id': 'model-a'}, ('model', 'model-b'): {'id': 'model-b'},
            ('provider', 'provider-a'): {'id': 'provider-a'}, ('task', 'coding'): {'id': 'coding'},
            ('source', 'source-a'): {'id': 'source-a', 'url': 'https://example.org/study', 'accessed_at': TODAY},
            ('access', 'route-a'): {'id': 'route-a', 'model_id': 'model-a', 'provider_id': 'provider-a'}}


def gap(**overrides):
    row = {'issue_key': 'missing-effort-setting', 'category': 'missing_setup',
           'model_ids': ['model-a'], 'provider_ids': [], 'task_ids': ['coding'],
           'fields': [], 'opened_at': YESTERDAY, 'updated_at': TODAY,
           'source_checked_at': None, 'evidence_ids': ['source-a'], 'urls': [],
           'reason': 'The effort setting is unresolved in the public report.',
           'requested_action': 'Inspect the original methodology and record the effort setting or unknown.',
           'dependencies': [], 'priority': 'normal', 'status': 'open', 'resolutions': []}
    row.update(overrides)
    row['id'] = followup_id(row)
    return row


def resolution():
    return {'method': 'source_inspection', 'checked_at': TODAY, 'evidence_ids': ['source-a'],
            'rationale': 'Inspected methodology provides the exact setup.'}


def test_open_unknown_retains_unknown_inspection_date(state):
    row = gap()
    assert not followup_errors([row], state)
    assert merge_followups([], [row], state)[0]['source_checked_at'] is None


def test_identity_ignores_mutable_prose_dates_evidence_priority_and_list_order(state):
    row = gap(model_ids=['model-a', 'model-b'])
    revised = deepcopy(row)
    revised.update(reason='A better explanation.', evidence_ids=[], urls=['https://example.org/study'],
                   priority='high', opened_at=TODAY, model_ids=['model-b', 'model-a'])
    assert followup_id(revised) == row['id']
    assert followup_id(gap(issue_key='different-effort-question')) != row['id']


def test_recurrence_updates_one_record_without_mutating_inputs(state):
    row = gap()
    revised = deepcopy(row)
    revised['requested_action'] = 'Inspect an additional public methodology source.'
    merged = merge_followups([row], [revised], state)
    assert len(merged) == 1 and merged[0] == revised
    assert row['requested_action'] != revised['requested_action']
    assert merge_followups(merged, [revised], state) == merged


def test_resolution_requires_dated_inspected_evidence_and_retains_history(state):
    row = gap()
    closed = deepcopy(row)
    closed.update(status='resolved', resolutions=[resolution()])
    assert merge_followups([row], [closed], state) == [closed]
    stale = deepcopy(state)
    stale[('source', 'source-a')]['accessed_at'] = YESTERDAY
    with pytest.raises(ValueError, match='predates'):
        merge_followups([row], [closed], stale)
    erased = deepcopy(closed)
    erased['resolutions'] = []
    with pytest.raises(ValueError, match='Preserve'):
        merge_followups([closed], [erased], state)


def test_repeated_open_report_does_not_reopen_resolved_issue(state):
    closed = gap(status='resolved', resolutions=[resolution()])
    recurrence = deepcopy(closed)
    recurrence.update(status='open', resolutions=[])
    assert merge_followups([closed], [recurrence], state) == [closed]
    recurrence['resolutions'] = closed['resolutions']
    with pytest.raises(ValueError, match='later inspected'):
        merge_followups([closed], [recurrence], state, reopen_ids=[closed['id']])


def test_explicit_evidenced_reopening_preserves_resolution_history(state):
    closed = gap(updated_at=YESTERDAY, status='resolved', resolutions=[{**resolution(), 'checked_at': YESTERDAY}])
    recurrence = deepcopy(closed)
    recurrence.update(status='open', updated_at=TODAY, source_checked_at=TODAY)
    merged = merge_followups([closed], [recurrence], state, reopen_ids=[closed['id']])
    assert merged == [recurrence] and merged[0]['resolutions'] == closed['resolutions']
    with pytest.raises(ValueError, match='Cannot reopen'):
        merge_followups([], [recurrence], state, reopen_ids=[recurrence['id']])


@pytest.mark.parametrize('changes,match', [
    ({'status': 'resolved'}, 'non-empty'),
    ({'model_ids': ['unknown']}, 'unresolved model'),
    ({'provider_ids': ['unknown']}, 'unresolved provider'),
    ({'task_ids': ['unknown']}, 'unresolved task'),
    ({'model_ids': [], 'task_ids': ['coding']}, 'scope'),
    ({'evidence_ids': [], 'urls': []}, 'public evidence'),
    ({'evidence_ids': ['missing']}, 'unresolved evidence'),
    ({'opened_at': '2099-01-01'}, 'dates'),
    ({'updated_at': '2099-01-01'}, 'dates'),
    ({'source_checked_at': '2099-01-01'}, 'inspection'),
    ({'fields': [{'entity_type': 'model', 'entity_id': 'model-b', 'path': '/specifications/context_window'}]}, 'outside'),
    ({'fields': [{'entity_type': 'model', 'entity_id': 'missing', 'path': '/missing'}]}, 'owner'),
    ({'fields': [{'entity_type': 'access', 'entity_id': 'route-a', 'path': '/methods'}]}, 'provider'),
    ({'reason': ' '}, 'does not match'),
    ({'operator_error': 'not public research'}, 'Additional properties'),
])
def test_invalid_scope_dates_state_and_unknown_fields_rejected(state, changes, match):
    row = gap(**changes)
    assert any(match in error for error in followup_errors([row], state))


def test_missing_field_is_a_gap_not_a_manufactured_value(state):
    row = gap(fields=[{'entity_type': 'model', 'entity_id': 'model-a', 'path': '/unknown_field'}])
    assert not followup_errors([row], state)


def test_dependencies_must_resolve_without_cycles(state):
    a, b = gap(), gap(issue_key='exact-checkpoint')
    a['dependencies'] = [b['id']]
    assert not followup_errors([a, b], state)
    assert any('unresolved dependency' in error for error in followup_errors([a], state))
    b['dependencies'] = [a['id']]
    assert any('cycle' in error for error in followup_errors([a, b], state))


def test_resolved_gap_cannot_depend_on_open_research(state):
    prerequisite = gap(issue_key='checkpoint-identification')
    closed = gap(status='resolved', resolutions=[resolution()], dependencies=[prerequisite['id']])
    assert any('cannot resolve before' in error for error in followup_errors([closed, prerequisite], state))


def test_inspected_observation_expands_to_actual_sources(state):
    state[('observation', 'finding-a')] = {'source_ids': ['source-a']}
    row = gap(source_checked_at=TODAY, evidence_ids=['finding-a'])
    assert not followup_errors([row], state)
    state[('source', 'source-a')]['url'] = 'https://127.0.0.1/'
    assert any('not public' in error for error in followup_errors([row], state))


def test_field_task_scope_must_match_its_canonical_owner(state):
    state[('task_assessment', 'assessment-a')] = {'model_id': 'model-a', 'task_id': 'coding'}
    row = gap(task_ids=[], fields=[{'entity_type': 'task_assessment', 'entity_id': 'assessment-a', 'path': '/rationale'}])
    assert any('field record task' in error for error in followup_errors([row], state))


def test_merge_rejects_identity_changes_duplicates_and_backdating(state):
    row = gap()
    wrong_scope = deepcopy(row)
    wrong_scope['model_ids'] = ['model-b']
    with pytest.raises(ValueError, match='scope'):
        merge_followups([row], [wrong_scope], state)
    with pytest.raises(ValueError, match='Duplicate proposals'):
        merge_followups([row], [row, row], state)
    backdated = deepcopy(row)
    backdated['updated_at'] = YESTERDAY
    with pytest.raises(ValueError, match='backwards'):
        merge_followups([row], [backdated], state)
    moved_opening = deepcopy(row)
    moved_opening['opened_at'] = TODAY
    with pytest.raises(ValueError, match='opening dates'):
        merge_followups([row], [moved_opening], state)


def test_reopen_then_close_requires_an_additional_resolution(state):
    row = gap(resolutions=[{**resolution(), 'checked_at': YESTERDAY}])
    closed = deepcopy(row)
    closed['status'] = 'resolved'
    with pytest.raises(ValueError, match='new resolution evidence'):
        merge_followups([row], [closed], state)
    closed['resolutions'].append(resolution())
    assert merge_followups([row], [closed], state) == [closed]


def test_merge_cannot_erase_inspected_date(state):
    row = gap(source_checked_at=TODAY)
    proposed = deepcopy(row)
    proposed['source_checked_at'] = None
    with pytest.raises(ValueError, match='inspected evidence dates'):
        merge_followups([row], [proposed], state)


def test_observation_without_source_cannot_certify_inspection(state):
    state[('observation', 'editorial')] = {'source_ids': []}
    assert any('editorial' in error for error in followup_errors([gap(evidence_ids=['editorial'])], state))


@pytest.mark.parametrize('url', ['http://example.org/', 'https://localhost/', 'https://127.0.0.1/',
    'https://10.2.3.4/', 'https://[::1]/', 'https://user:password@example.org/',
    'https://example.org:8080/', 'https://example.org/?token=secret',
    'https://example.org/?X-Amz-Signature=secret', 'file:///private/example',
    'https://service.internal/', 'https://example.org:invalid/', 'https://127.0.0.1./',
    'https://0177.0.0.1/', 'https://example.org/?api_key=secret'])
def test_non_public_urls_rejected(url):
    assert not public_url(url)


@pytest.mark.parametrize('text', ['See ' + str(Path('C:/Users/example/private.json')),
    'Read .local/research/packet.json', 'https://drive.google.com/file/d/example',
    'https://example.org/?token=secret', 'Contact endpoint http://127.0.0.1/',
    'Key ' + 'sk-' + 'a' * 24])
def test_private_content_rejected_even_in_prose(state, text):
    assert any('private content' in error for error in followup_errors([gap(reason=text)], state))


def test_exact_intersection_filters_and_resolved_status(state):
    fields = [{'entity_type': 'model', 'entity_id': 'model-a', 'path': '/context'}]
    a = gap(provider_ids=['provider-a'], fields=fields, priority='high')
    b = gap(issue_key='other', status='resolved', resolutions=[resolution()])
    assert select_followups([b, a], model_id='model-a', provider_id='provider-a', task_id='coding',
        entity_type='model', entity_id='model-a', path='/context', priority='high', category='missing_setup') == [a]
    assert select_followups([a], path='/context/tokens') == []
    assert select_followups([a], provider_id='other') == []
    assert select_followups([b, a]) == [a]
    assert select_followups([b, a], status=None) == [a, b]
    selected = select_followups([a])
    selected[0]['reason'] = 'modified'
    assert a['reason'] != 'modified'


def test_view_discloses_unknowns_and_resolution_evidence():
    assert 'does not establish complete research' in render_followups([])
    rendered = render_followups([gap(status='resolved', resolutions=[resolution()])])
    assert 'Unknown / not established' in rendered
    assert 'source-a' in rendered and 'Inspected methodology' in rendered


@pytest.fixture(scope='module')
def actual_state():
    return {key: row for key, (_, row) in canonical().items()}


def assignment_fixture(actual_state):
    state = deepcopy(actual_state)
    model = 'claude-fable-5-1'
    source = next(ident for kind, ident in state if kind == 'source')
    provider = next(row['provider_id'] for (kind, _), row in state.items()
                    if kind == 'access' and row.get('model_id') == model and row.get('provider_id'))
    rows = [gap(model_ids=[model], task_ids=[], evidence_ids=[source]),
            gap(issue_key='provider-setup', model_ids=[], provider_ids=[provider], task_ids=[], evidence_ids=[source]),
            gap(issue_key='other-model-setup', model_ids=['xai-grok-4-7'], task_ids=[], evidence_ids=[source]),
            gap(issue_key='closed-prerequisite', model_ids=['xai-grok-4-7'], task_ids=[], evidence_ids=[source])]
    rows[0]['dependencies'] = [rows[3]['id']]
    for row in rows:
        state[('research_followup', row['id'])] = row
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    contract = state[('research_contract', 'research-contract-v1')]
    run = make_run(state, 'git-' + commit, commit, 'research-run-followup-test', [model],
                   {'max_minutes_per_model': 10, 'max_searches_per_model': 10,
                    'source_categories': contract['source_categories']}, TODAY)
    return run, state, rows


def test_next_assignment_receives_applicable_gaps_and_dependency_context(actual_state):
    run, state, rows = assignment_fixture(actual_state)
    snapshot = assignment_inputs(run, state)
    assert set(snapshot['direct_followup_ids']) == {rows[0]['id'], rows[1]['id']}
    assert snapshot['dependency_context_ids'] == [rows[3]['id']]
    assert rows[2]['id'] not in {row['id'] for row in snapshot['records']}
    assert snapshot['base_commit'] == run['base_commit']
    changed = deepcopy(state)
    changed[('research_followup', rows[0]['id'])]['reason'] = 'Changed after assignment'
    with pytest.raises(ValueError, match='baseline hash'):
        assignment_inputs(run, changed)


def test_immutable_digest_inputs_repeat_noop_and_refuse_overwrite(actual_state, tmp_path):
    run, state, rows = assignment_fixture(actual_state)
    destination = tmp_path / '.local' / 'next-assignment'
    manifest = write_assignment_inputs(run, state, destination, root=tmp_path)
    for name, metadata in manifest['files'].items():
        raw = (destination / name).read_bytes()
        assert metadata == {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}
    original = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in destination.iterdir()}
    assert write_assignment_inputs(run, state, destination, root=tmp_path) == manifest
    assert original == {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in destination.iterdir()}
    snapshot = json.loads((destination / 'followups.json').read_bytes())
    assert rows[0]['id'] in snapshot['direct_followup_ids']
    (destination / 'followups.json').write_text('{}')
    with pytest.raises(ValueError, match='Existing assignment inputs differ'):
        write_assignment_inputs(run, state, destination, root=tmp_path)
    assert (destination / 'followups.json').read_text() == '{}'


def test_assignment_inputs_refuse_public_destination(actual_state, tmp_path):
    run, state, _ = assignment_fixture(actual_state)
    with pytest.raises(ValueError, match='private'):
        write_assignment_inputs(run, state, tmp_path / 'public', root=tmp_path)


def test_assignment_inputs_retry_transient_windows_rename(actual_state,tmp_path,monkeypatch):
    from tools import research_followups as followups
    run,state,_=assignment_fixture(actual_state)
    real=followups.os.rename; attempts=[]
    def locked(source,destination):
        attempts.append(source)
        if len(attempts)<3:
            error=PermissionError('Synthetic Windows file lock'); error.winerror=32; raise error
        return real(source,destination)
    monkeypatch.setattr(followups.os,'rename',locked)
    monkeypatch.setattr(followups.time,'sleep',lambda seconds:None)
    destination=tmp_path/'.local/inputs'
    manifest=write_assignment_inputs(run,state,destination,root=tmp_path)
    assert len(attempts)==3
    assert all(sha256((destination/name).read_bytes()).hexdigest()==pin['sha256']
               for name,pin in manifest['files'].items())


def test_assignment_inputs_stop_after_bounded_windows_rename_failures(actual_state,tmp_path,monkeypatch):
    from tools import research_followups as followups
    run,state,_=assignment_fixture(actual_state); attempts=[]
    def locked(source,destination):
        attempts.append(source)
        error=PermissionError('Synthetic persistent file lock'); error.winerror=5; raise error
    monkeypatch.setattr(followups.os,'rename',locked)
    monkeypatch.setattr(followups.time,'sleep',lambda seconds:None)
    destination=tmp_path/'.local/inputs'
    with pytest.raises(PermissionError): write_assignment_inputs(run,state,destination,root=tmp_path)
    assert len(attempts)==5 and not destination.exists()
    assert not list(destination.parent.glob('.followups-*'))


def test_assignment_inputs_refuse_symlink_ancestor(actual_state, tmp_path):
    run, state, _ = assignment_fixture(actual_state)
    outside = tmp_path / 'public'
    outside.mkdir()
    local = tmp_path / '.local'
    try:
        local.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip('This Windows host does not grant symlink creation')
    with pytest.raises(ValueError, match='link/reparse'):
        write_assignment_inputs(run, state, local / 'inputs', root=tmp_path)


def test_git_preserves_followups_and_checksums_in_pinned_baselines(tmp_path):
    from test_git_baselines import small_repo, write, commit
    from tools.git_baselines import git_state
    from tools.knowledge import capture
    small_repo(tmp_path)
    first = commit(tmp_path)
    source_id = 'src-aaaaaaaaaaaa'
    write(tmp_path / 'evidence/sources.yaml', {'records': [
        {'id': source_id, 'accessed_at': TODAY, 'url': 'https://example.org/study'}]})
    row = gap(model_ids=['example'], task_ids=[], evidence_ids=[source_id])
    write(tmp_path / 'data/research-followups.yaml', {'schema_version': '1.0', 'records': [row]})
    current = {key: value for key, (_, value) in canonical(tmp_path).items()}
    assert not followup_errors([row], current)
    capture(tmp_path, TODAY, 'Synthetic fixture research gap', [source_id])
    assert not integrity_errors(tmp_path)
    second = commit(tmp_path)
    assert ('research_followup', row['id']) not in git_state(first, tmp_path)
    assert git_state(second, tmp_path)[('research_followup', row['id'])] == row
    row['reason'] = 'Synthetic changed gap reasoning'
    write(tmp_path / 'data/research-followups.yaml', {'records': [row]})
    assert integrity_errors(tmp_path)
    assert git_state(second, tmp_path)[('research_followup', row['id'])]['reason'] != row['reason']


def test_scaffold_cli_consumes_populated_public_registry_in_isolated_product(tmp_path):
    from tools.public_boundary import public_files
    from tools.knowledge import capture
    from test_git_baselines import write, commit, git
    product = tmp_path / 'product'
    product.mkdir()
    for source in public_files(ROOT):
        target = product / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    state = {key: value for key, (_, value) in canonical(product).items()}
    source_id = next(ident for kind, ident in state if kind == 'source')
    row = gap(model_ids=['claude-fable-5-1'], task_ids=[], evidence_ids=[source_id])
    write(product / 'data/research-followups.yaml', {'schema_version': '1.0', 'records': [row]})
    capture(product, TODAY, 'Synthetic fixture follow-up', [source_id])
    for script in ['render.py', 'validate.py']:
        result = subprocess.run([sys.executable, str(product / 'tools' / script)],
                                capture_output=True, text=True, cwd=product)
        assert result.returncode == 0, result.stdout + result.stderr
    assert row['id'] in (product / 'data/research-followups.md').read_text()
    git(product, 'init')
    git(product, 'config', 'user.name', 'Synthetic Test')
    git(product, 'config', 'user.email', 'test@example.invalid')
    frozen = commit(product)
    local = product / '.local'
    local.mkdir()
    command = [sys.executable, str(product / 'tools/research_runs.py'), 'scaffold',
               '--id', 'research-run-followup-cli', '--models', 'claude-fable-5-1',
               '--max-minutes-per-model', '10', '--max-searches-per-model', '10',
               '--output', str(local / 'run.yaml'), '--followups-output', str(local / 'inputs')]
    result = subprocess.run(command, capture_output=True, text=True, cwd=product)
    assert result.returncode == 0, result.stdout + result.stderr
    snapshot = json.loads((local / 'inputs/followups.json').read_bytes())
    assert snapshot['base_commit'] == frozen
    assert snapshot['direct_followup_ids'] == [row['id']]
    assert read(local / 'run.yaml')['base_commit'] == frozen
    retained = (local / 'run.yaml').read_bytes()
    result = subprocess.run(command, capture_output=True, text=True, cwd=product)
    assert result.returncode != 0 and (local / 'run.yaml').read_bytes() == retained
    omitted = command[:-2]
    omitted[omitted.index('--output') + 1] = str(local / 'omitted-followups-run.yaml')
    result = subprocess.run(omitted, capture_output=True, text=True, cwd=product)
    assert result.returncode != 0 and 'Open follow-ups require' in result.stderr
    assert not (local / 'omitted-followups-run.yaml').exists()


def test_canonical_and_explorer_can_load_empty_queue_without_changing_checksums():
    from explorer.data import load
    assert read(ROOT / 'data/research-followups.yaml')['records'] == []
    assert load()['research_followup'] == {}
    assert not integrity_errors()
