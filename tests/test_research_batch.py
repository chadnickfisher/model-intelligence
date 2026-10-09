"""Synthetic proposed edits exercise research ingestion; none are catalog research."""
from copy import deepcopy
from datetime import datetime, timezone, date
from hashlib import sha256
import json
from pathlib import Path
import pytest

from tools import research_batch as batch
from tools.git_baselines import git_state
from tools.knowledge import ROOT, record_hash
from tools.research_runs import make_run

MID = 'claude-fable-5-1'
SID = 'src-c7eceee3e7d1'
TODAY = date.today().isoformat()


@pytest.fixture(scope='module')
def baseline():
    return git_state(batch.git(ROOT, 'rev-parse', 'HEAD'))


@pytest.fixture
def fixture(baseline):
    commit = batch.git(ROOT, 'rev-parse', 'HEAD')
    contract = baseline[('research_contract', 'research-contract-v1')]
    run = make_run(baseline, 'git-' + commit, commit, 'research-run-synthetic-batch', [MID],
                   {'max_minutes_per_model': 60, 'max_searches_per_model': 40,
                    'source_categories': contract['source_categories']}, TODAY)
    assignment = {'assignment_id': 'synthetic-batch', 'baseline_commit': commit, 'research_run': deepcopy(run),
                  'discovery_creator_ids':['anthropic'],'max_discovery_searches':20}
    packet = {'schema_version': '1.0', 'package_type': 'research-batch',
              'assignment_id': assignment['assignment_id'], 'baseline_commit': commit,
              'created_at': datetime.now(timezone.utc).isoformat(), 'research_run': run,
              'changes': [], 'discoveries': [], 'source_groups': {},
              'discovery_checks':[{'creator_id':'anthropic','result':'not_checked','checked_at':None,'rationale':'',
                  'evidence_ids':[],'search_references':[],'remaining_gaps':['Pending actual catalog inspection'],'blocked_reason':None}]}
    source = deepcopy(baseline[('source', SID)])
    source['accessed_at'] = TODAY
    source['claim_scope'].append('Synthetic fixture source inspection.')
    model = deepcopy(baseline[('model', MID)])
    model['notes'].append('Synthetic proposed note, not real research.')
    for kind, record, paths in [('source', source, ['/accessed_at', '/claim_scope']), ('model', model, ['/notes'])]:
        packet['changes'].append({'kind': kind, 'record': record,
            'previous_hash': record_hash(baseline[(kind, record['id'])]), 'identity_key': None,
            'evidence_ids': [SID], 'checked_paths': paths, 'rationale': 'Synthetic bounded proposed edit.'})
    check = next(r for r in run['field_checks'] if r['entity_type'] == 'model' and r['path'] == '/notes')
    inspected(check, 'value')
    category = next(r for r in run['source_checks'] if r['category'] == 'primary')
    inspected(category, 'checked')
    return packet, assignment


def inspected(row, result):
    row.update(result=result, checked_at=TODAY, rationale='Synthetic actual-source check.', evidence_ids=[SID],
               search_references=[], conditions=['Synthetic setup'], remaining_gaps=[], blocked_reason=None)


def test_partial_candidate_retains_pending_and_non_target_accounting(fixture, baseline):
    packet, assignment = fixture
    original = deepcopy(packet)
    result = batch.compile_batch(packet, assignment, baseline)
    assert len(result['changes']) == 2 and not result['completion']['complete']
    assert result['completion']['pending'] > 0
    assert result['completion']['non_target_domains_not_checked'] == (54 - 1) * 4
    assert packet == original
    assert result['candidate'][('model', MID)]['notes'][-1].startswith('Synthetic')
    assert baseline[('model', MID)]['notes'] != result['candidate'][('model', MID)]['notes']


@pytest.mark.parametrize('mutation,match', [
    ('wrong_assignment', 'assignment'), ('stale', 'baseline'), ('extra_key', 'Schema'),
    ('prior_hash', 'hash mismatch'), ('unassigned', 'Unassigned model'),
    ('unchecked', 'not investigated'), ('missing_check', 'omitted'),
    ('duplicate_change', 'Duplicate changed'), ('wrong_scope', 'scope was reassigned'),
    ('profile_date', 'Whole-profile'), ('model_version', 'Immutable'),
    ('missing_changed_path', 'checked_paths'), ('field_delete', 'deletion'),
    ('stale_source', 'not inspected'), ('private', 'Private content'),
    ('missing_category', 'category accounting'), ('future', 'future packet'),
    ('bound', 'metadata/rubric/bounds'), ('wrong_evidence', 'current inspected source')])
def test_rejects_unsafe_incomplete_or_stale_changes(fixture, baseline, mutation, match):
    packet, assignment = fixture
    model = packet['changes'][1]['record']
    if mutation == 'wrong_assignment': packet['assignment_id'] = 'wrong'
    elif mutation == 'stale': packet['baseline_commit'] = '0' * 40
    elif mutation == 'extra_key': packet['run_this_command'] = 'forbidden'
    elif mutation == 'prior_hash': packet['changes'][1]['previous_hash'] = '0' * 64
    elif mutation == 'unassigned': model['id'] = 'claude-opus-5-5'; packet['changes'][1]['previous_hash'] = record_hash(baseline[('model', model['id'])])
    elif mutation == 'unchecked': next(r for r in packet['research_run']['field_checks'] if r['path'] == '/notes' and r['entity_type'] == 'model').update(result='not_checked', checked_at=None, rationale='', evidence_ids=[], conditions=[], remaining_gaps=['Pending'])
    elif mutation == 'missing_check': packet['research_run']['field_checks'].pop()
    elif mutation == 'duplicate_change': packet['changes'].append(deepcopy(packet['changes'][1]))
    elif mutation == 'wrong_scope': model['capabilities'][0]['related_task_ids'] = []
    elif mutation == 'profile_date': model['verified_at'] = TODAY
    elif mutation == 'model_version': model['identity']['version'] = 'different-checkpoint'
    elif mutation == 'missing_changed_path': packet['changes'][1]['checked_paths'] = ['/identity']
    elif mutation == 'field_delete': model.pop('additional_specifications')
    elif mutation == 'stale_source': packet['changes'][0]['record']['accessed_at'] = '2000-01-01'
    elif mutation == 'private': model['notes'].append('https://drive.google.com' + '/file/d/synthetic-fixture/view')
    elif mutation == 'missing_category': next(r for r in packet['research_run']['source_checks'] if r['category'] == 'primary').update(result='not_checked', checked_at=None, rationale='', evidence_ids=[], conditions=[], remaining_gaps=['Pending'])
    elif mutation == 'future': packet['created_at'] = '2099-01-01T00:00:00Z'
    elif mutation == 'bound': packet['research_run']['bounds']['max_searches_per_model'] += 1
    elif mutation == 'wrong_evidence': packet['changes'][1]['evidence_ids'] = ['src-000000000000']
    with pytest.raises(ValueError, match=match): batch.compile_batch(packet, assignment, baseline)


@pytest.mark.parametrize('url', ['http://example.com', 'https://127.0.0.1/test', 'https://localhost/test',
    'https://192.168.1.1/test', 'https://docs.google.com' + '/document/d/synthetic-fixture', 'https://example.com/?token=x',
    'https://user:password@example.com/test', 'https://research.internal/test'])
def test_private_or_signed_sources_are_rejected(url):
    with pytest.raises(ValueError): batch.public_url(url)


@pytest.mark.parametrize('raw', ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'])
def test_json_rejects_ambiguous_or_non_finite_input(tmp_path, raw):
    path = tmp_path / 'packet.json'; path.write_text(raw)
    with pytest.raises(ValueError): batch.load_json(path)


def test_private_windows_paths_and_fake_keys_are_rejected(fixture, baseline):
    packet,assignment=fixture
    packet['changes'][1]['record']['notes'].append('C:' + chr(92) + 'Users' + chr(92) + 'synthetic' + chr(92) + 'private.txt')
    with pytest.raises(ValueError,match='Private content'): batch.compile_batch(packet,assignment,baseline)


def test_assignment_metadata_cannot_be_copied_into_public_records(fixture, baseline):
    packet,assignment=fixture
    packet['changes'][1]['record']['notes'].append(assignment['assignment_id'])
    with pytest.raises(ValueError,match='Private operating'): batch.compile_batch(packet,assignment,baseline)
    packet['changes'][1]['record']['notes'][-1]='sk-'+'x'*30
    with pytest.raises(ValueError,match='Private content'): batch.compile_batch(packet,assignment,baseline)


def test_new_ids_are_deterministic_and_existing_source_cannot_be_duplicated(fixture, baseline):
    packet, _ = fixture
    change = deepcopy(packet['changes'][0]); change['record']['id'] = 'new:fixture-source'
    change.update(previous_hash=None, identity_key='fixture')
    with pytest.raises(ValueError, match='Existing source URL'): batch.allocate([change], baseline)
    change['record']['url'] = 'https://example.com/public-evaluation'
    assert batch.allocate([change], baseline) == batch.allocate([change], baseline)
    with pytest.raises(ValueError, match='duplicate new reference'): batch.allocate([change, change], baseline)


def test_new_source_refs_resolve_in_changes_accounting_and_group_keys(fixture, baseline):
    packet, assignment = fixture
    source = packet['changes'][0]
    source['record'].update(id='new:fixture-source', url='https://example.com/public-evaluation')
    source.update(previous_hash=None,identity_key='fixture-source',evidence_ids=['new:fixture-source'])
    packet['changes'][1]['evidence_ids'] = ['new:fixture-source']
    for collection in ('field_checks','source_checks'):
        for row in packet['research_run'][collection]:
            if row['result'] != 'not_checked': row['evidence_ids'] = ['new:fixture-source']
    packet['source_groups'] = {'new:fixture-source':'one evaluation'}
    result = batch.compile_batch(packet,assignment,baseline)
    ident = 'src-' + sha256(b'https://example.com/public-evaluation').hexdigest()[:12]
    assert result['mapping']['new:fixture-source'] == ident
    assert result['changes'][1]['evidence_ids'] == [ident]
    assert result['mapping'] == batch.compile_batch(packet,assignment,baseline)['mapping']


@pytest.mark.parametrize('mutation,match', [('omitted','Discovery creator'),('duplicated','Discovery creator'),
    ('fake_checked','actual date'),('no_primary','official catalog'),('failed_unknown','remains blocked')])
def test_discovery_cannot_be_omitted_or_falsely_completed(fixture, baseline, mutation, match):
    packet,assignment=fixture
    row=packet['discovery_checks'][0]
    if mutation=='omitted': packet['discovery_checks']=[]
    elif mutation=='duplicated': packet['discovery_checks'].append(deepcopy(row))
    elif mutation=='fake_checked': row['result']='checked'
    elif mutation=='no_primary': row.update(result='checked',checked_at=TODAY,rationale='Synthetic search only',
        search_references=[{'query':'catalog','checked_at':TODAY,'outcome':'no_matched_sources','urls':[],'notes':''}])
    elif mutation=='failed_unknown': row.update(result='unknown',checked_at=TODAY,rationale='Synthetic failed search',
        search_references=[{'query':'catalog','checked_at':TODAY,'outcome':'blocked','urls':[],'notes':''}])
    with pytest.raises(ValueError,match=match): batch.compile_batch(packet,assignment,baseline)


def test_vendor_only_medium_aggregate_is_rejected(fixture, baseline):
    packet, assignment = fixture
    old = next(r for (k, _), r in baseline.items() if k == 'task_assessment' and r['model_id'] == MID and r['task_id'] == 'coding.debugging')
    record = deepcopy(old); record['checked_at'] = TODAY
    record['evidence_ids'] = [SID]
    record['aggregate'].update(evidence_confidence='medium', assessed_at=TODAY, supporting_evidence_ids=[SID], contradictory_evidence_ids=[])
    packet['changes'].append({'kind':'task_assessment','record':record,'previous_hash':record_hash(old),
        'identity_key':None,'evidence_ids':[SID],'checked_paths':['/aggregate'],'rationale':'Synthetic vendor-only proposal'})
    decision = next(r for r in packet['research_run']['task_decisions'] if r['task_id'] == 'coding.debugging')
    inspected(decision, 'assessed')
    decision.update(applicability='applicable',judgment_ids=record['judgment_ids'],confidence_rationale='Synthetic')
    with pytest.raises(ValueError, match='Vendor-only'): batch.compile_batch(packet, assignment, baseline)


@pytest.fixture
def applying(tmp_path, monkeypatch):
    root = tmp_path
    destination = root / '.local/research/stage'; destination.mkdir(parents=True)
    candidate = destination / 'candidate'; candidate.mkdir()
    changes = {}
    for name in ['data/first.yaml', 'data/second.yaml']:
        target = root / name; target.parent.mkdir(exist_ok=True); target.write_bytes(b'old\n')
        proposed = candidate / name; proposed.parent.mkdir(exist_ok=True); proposed.write_bytes(b'new\n')
        changes[name] = {'previous_sha256':sha256(b'old\n').hexdigest(), 'sha256':sha256(b'new\n').hexdigest()}
    receipt = {'packet_sha256':'a'*64,'baseline_commit':'b'*40,'completion':{'complete':False,'batch_complete':False},
               'changes':changes,'tests_passed':True}
    (destination/'stage-receipt.json').write_text(json.dumps(receipt))
    review = {'packet_sha256':'a'*64,'candidate_changes':changes,'evidence_reviewed':True,'accept_partial':True}
    monkeypatch.setattr(batch, 'private_destination', lambda root, path: path)
    monkeypatch.setattr(batch, 'git', lambda *args:'b'*40)
    monkeypatch.setattr(batch, 'git_state', lambda *args:{})
    monkeypatch.setattr(batch, 'canonical', lambda *args:{})
    return root, destination, review


def test_apply_is_idempotent_and_never_commits_or_pushes(applying):
    root, destination, review = applying
    assert batch.apply_candidate(root, destination, review)['changed_files'] == 2
    assert batch.apply_candidate(root, destination, review)['status'] == 'already_applied'
    assert (root/'data/first.yaml').read_bytes() == b'new\n'


@pytest.mark.parametrize('failure', ['dirty_target','changed_candidate','wrong_review','unreviewed','partial','no_tests','code_path','unrelated_data','locked'])
def test_apply_preflights_everything_before_first_write(applying, monkeypatch, failure):
    root, destination, review = applying
    receipt_path = destination/'stage-receipt.json'
    receipt = json.loads(receipt_path.read_text())
    if failure == 'dirty_target': (root/'data/second.yaml').write_bytes(b'user work')
    elif failure == 'changed_candidate': (destination/'candidate/data/second.yaml').write_bytes(b'tampered')
    elif failure == 'wrong_review': review['packet_sha256'] = '0'*64
    elif failure == 'unreviewed': review['evidence_reviewed'] = False
    elif failure == 'partial': review['accept_partial'] = False
    elif failure == 'no_tests': receipt['tests_passed'] = False; receipt_path.write_text(json.dumps(receipt))
    elif failure == 'code_path': receipt['changes']['tools/incoming.py'] = receipt['changes'].pop('data/second.yaml'); receipt_path.write_text(json.dumps(receipt))
    elif failure == 'unrelated_data': monkeypatch.setattr(batch,'canonical',lambda *args:{('model','user-model'):('model.yaml',{'id':'user-model'})})
    elif failure == 'locked': (root/'.local/research/candidate-apply.lock').write_text('another run')
    with pytest.raises((ValueError, FileExistsError)): batch.apply_candidate(root,destination,review)
    assert (root/'data/first.yaml').read_bytes() == b'old\n'


def test_failed_second_replace_rolls_back_first_and_cleans_lock(applying, monkeypatch):
    root, destination, review = applying
    replace = batch.os.replace
    def fail(source, target):
        if Path(target).name == 'second.yaml': raise OSError('Synthetic interrupted write')
        replace(source,target)
    monkeypatch.setattr(batch.os,'replace',fail)
    with pytest.raises(OSError,match='interrupted'): batch.apply_candidate(root,destination,review)
    assert (root/'data/first.yaml').read_bytes() == b'old\n'
    assert (root/'data/second.yaml').read_bytes() == b'old\n'
    assert not (root/'.local/research/candidate-apply.lock').exists()
    assert not list((root/'data').glob('*.research-batch-tmp'))


def test_isolated_real_candidate_validates_and_original_files_are_untouched(fixture, baseline, tmp_path):
    # The test runner supplies an ignored workspace basetemp for this integration case.
    if not tmp_path.resolve().is_relative_to(ROOT / '.local/research'):
        pytest.skip('Integration stage requires an explicit ignored workspace basetemp')
    packet, assignment = fixture
    before = (ROOT/'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes()
    compiled = batch.compile_batch(packet,assignment,baseline)
    result = batch.stage(ROOT,compiled,assignment,'a'*64,tmp_path/'stage')
    assert result['status'] == 'validated_local_candidate'
    assert all(c['exit_code']==0 for c in result['checks'])
    assert not result['completion']['complete'] and not result['tests_passed']
    assert (ROOT/'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes() == before
    with pytest.raises(ValueError,match='already exists'):
        batch.stage(ROOT,compiled,assignment,'a'*64,tmp_path/'stage')
