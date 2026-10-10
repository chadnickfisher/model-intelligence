"""Transport/identity regressions use synthetic data, never research or inference."""
from copy import deepcopy
from hashlib import sha256
import io
import json
from urllib.error import HTTPError, URLError
import pytest
from tools import research_intake as intake
from tools.research_reconcile import reconcile_sources


def delivery(raw, revision=1, supersedes=None):
    return {'schema_version': '1.0', 'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40,
            'artifact_id': 'synthetic_file', 'bytes': len(raw), 'sha256': sha256(raw).hexdigest(),
            'revision': revision, 'supersedes': supersedes, 'status': 'completed'}


def credentials():
    return {'type': 'authorized_user', 'client_id': 'synthetic', 'client_secret': 'synthetic',
            'refresh_token': 'synthetic', 'scopes': [intake.READONLY]}


class Opener:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []

    def open(self, request, timeout):
        self.calls.append(request)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return io.BytesIO(reply)


def token():
    return json.dumps({'access_token': 'synthetic-token', 'expires_in': 3600,
                       'scope': intake.READONLY}).encode()


def metadata(size, version='1'):
    return json.dumps({'id': 'synthetic_file', 'name': 'test.json', 'mimeType': 'application/json',
                       'size': str(size), 'parents': ['synthetic_folder'], 'trashed': False,
                       'version': version, 'capabilities': {'canDownload': True}}).encode()


def test_actual_sized_transfer_uses_authenticated_api_bytes():
    raw = b' ' * 14023345
    opener = Opener([token(), metadata(len(raw)), raw, metadata(len(raw))])
    transport = intake.DriveTransport(credentials(), opener=opener)
    assert transport.read('synthetic_file', 'synthetic_folder', intake.MAX_BYTES, len(raw)) == raw
    assert 'alt=media' in opener.calls[2].full_url
    assert opener.calls[2].get_header('Authorization') == 'Bearer synthetic-token'
    assert len(opener.calls) == 4  # One refresh, before/after metadata, exact media.


@pytest.mark.parametrize('media,after,match', [
    (b'abc', None, 'Truncated'), (b'abcde', None, 'exceeds'),
    (b'abcd', metadata(4, '2'), 'changed during')])
def test_truncation_growth_and_concurrent_edit_rejected(media, after, match):
    replies = [token(), metadata(4), media] + ([after] if after else [])
    transport = intake.DriveTransport(credentials(), opener=Opener(replies))
    with pytest.raises(ValueError, match=match):
        transport.read('synthetic_file', 'synthetic_folder', 100)


@pytest.mark.parametrize('code', [401, 403])
def test_authorization_failure_never_retried_or_disclosed(code):
    opener = Opener([token(), HTTPError(intake.API, code, 'secret', {}, io.BytesIO(b'secret'))])
    waits = []
    transport = intake.DriveTransport(credentials(), opener=opener, sleep=waits.append)
    with pytest.raises(ValueError, match='authorization failed') as error:
        transport.metadata('synthetic_file')
    assert 'secret' not in str(error.value) and len(opener.calls) == 2 and waits == []


def test_transient_retry_is_bounded():
    waits = []
    opener = Opener([URLError('secret')] * 3)
    transport = intake.DriveTransport(credentials(), opener=opener, sleep=waits.append)
    with pytest.raises(ValueError, match='bounded retries'):
        transport.metadata('synthetic_file')
    assert len(opener.calls) == 3 and waits == [1, 2]


def test_token_refresh_rejection_is_terminal():
    opener = Opener([HTTPError(intake.TOKEN, 400, 'invalid_grant secret', {}, None)])
    transport = intake.DriveTransport(credentials(), opener=opener, sleep=lambda _: pytest.fail('retry'))
    with pytest.raises(ValueError, match='authorization failed'):
        transport.metadata('synthetic_file')
    assert len(opener.calls) == 1


def test_pagination_and_no_filename_certification():
    opener = Opener([token(), json.dumps({'files': [{'id': 'one', 'name': 'one.delivery.json'},
                      {'id': 'two', 'name': 'final.json'}], 'nextPageToken': 'next'}).encode(),
                      json.dumps({'files': [{'id': 'three', 'name': 'three.delivery.json'}]}).encode()])
    transport = intake.DriveTransport(credentials(), opener=opener)
    assert transport.manifests('synthetic_folder') == ['one', 'three']
    assert 'pageToken=next' in opener.calls[-1].full_url


def test_final_revision_selection_rejects_forks_gaps_and_untrusted_baselines():
    a, b = delivery(b'one'), delivery(b'two', 2, sha256(b'one').hexdigest())
    assignments = {'synthetic': {'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}}
    assert intake.select_deliveries([b, a, a], assignments) == [b]
    for manifests, match in [([b], 'Missing'), ([a, b, delivery(b'fork', 2, a['sha256'])], 'Conflicting'),
                              ([a, delivery(b'bad', 2, 'b' * 64)], 'Broken')]:
        with pytest.raises(ValueError, match=match):
            intake.select_deliveries(manifests, assignments)
    with pytest.raises(ValueError, match='Untrusted'):
        intake.select_deliveries([a], {})


@pytest.mark.parametrize('field,value', [('status', 'pending'), ('bytes', True), ('artifact_id', '../bad'),
                                       ('revision', True), ('sha256', 'bad'), ('baseline_commit', 'bad')])
def test_manifest_guards(field, value):
    m = delivery(b'one')
    m[field] = value
    with pytest.raises(ValueError):
        intake.manifest_errors(m)


def test_intake_repeat_noop_and_interrupted_receipt_recovery(tmp_path):
    raw = json.dumps({'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}).encode()
    m = delivery(raw)
    class FakeTransport:
        calls = []
        def manifests(self, folder): return ['manifest']
        def read(self, ident, folder, limit, expected=None):
            self.calls.append(ident)
            return json.dumps(m).encode() if ident == 'manifest' else raw
    transport = FakeTransport()
    assignments = {'synthetic': {'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}}
    result = intake.intake(transport, 'synthetic_folder', assignments, tmp_path)
    assert result['deliveries'][0]['new_bytes'] is True
    receipt = tmp_path / 'synthetic' / m['sha256'] / 'delivery.json'
    receipt.unlink()  # Crash after packet retention, before manifest retention.
    result = intake.intake(transport, 'synthetic_folder', assignments, tmp_path)
    assert result['deliveries'][0]['new_bytes'] is False and receipt.is_file()
    assert transport.calls.count('synthetic_file') == 1
    (receipt.parent / 'packet.json').write_bytes(b'edited')
    with pytest.raises(ValueError, match='digest/bytes'):
        intake.intake(transport, 'synthetic_folder', assignments, tmp_path)


def test_duplicate_json_keys_and_nonfinite_numbers_rejected():
    for raw in [b'{"a":1,"a":2}', b'{"a":NaN}']:
        with pytest.raises(ValueError): intake.parse(raw)


def test_lock_overlap_and_release(tmp_path):
    path = tmp_path / 'intake.lock'
    with intake.run_lock(path):
        with pytest.raises(ValueError, match='lock'):
            with intake.run_lock(path): pytest.fail('overlap')
    with intake.run_lock(path): pass


def test_private_path_boundary(tmp_path):
    with pytest.raises(ValueError, match='private'):
        intake.private_path(tmp_path, tmp_path / 'public.json')
    assert intake.private_path(tmp_path, tmp_path / '.local' / 'test.json').name == 'test.json'
    with pytest.raises(ValueError, match='private'):
        intake.private_path(tmp_path, tmp_path / '.local' / '..' / 'public.json')


def test_empty_inbox_is_an_honest_no_delivery(tmp_path):
    class Empty:
        def manifests(self, folder): return []
    assert intake.intake(Empty(), 'folder', {}, tmp_path) == {'status': 'no_final_delivery', 'deliveries': []}


def test_wrong_digest_never_retained(tmp_path):
    raw = json.dumps({'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}).encode()
    m = delivery(raw)
    class WrongDigest:
        def manifests(self, folder): return ['manifest']
        def read(self, ident, folder, limit, expected=None):
            return json.dumps(m).encode() if ident == 'manifest' else b'x' * len(raw)
    with pytest.raises(ValueError, match='digest/bytes'):
        intake.intake(WrongDigest(), 'folder', {'synthetic': m}, tmp_path)
    assert not list(tmp_path.rglob('packet.json'))


def test_metadata_must_belong_to_trusted_inbox():
    opener = Opener([token(), metadata(4)])
    transport = intake.DriveTransport(credentials(), opener=opener)
    with pytest.raises(ValueError, match='not eligible'):
        transport.read('synthetic_file', 'other_folder', 100)
    assert len(opener.calls) == 2


@pytest.mark.parametrize('scopes', [[], ['https://www.googleapis.com/auth/drive.metadata.readonly'],
                                  ['https://www.googleapis.com/auth/drive']])
def test_metadata_only_or_write_scope_is_not_authorized(scopes):
    value = credentials()
    value['scopes'] = scopes
    with pytest.raises(ValueError, match='content-read'):
        intake.DriveTransport(value)


def test_partial_body_network_failure_restarts_bounded_download():
    class Interrupted(io.BytesIO):
        def read(self, size=-1): raise OSError('synthetic interruption')
    class Bodies(Opener):
        def open(self, request, timeout):
            if self.replies and isinstance(self.replies[0], Interrupted):
                self.calls.append(request)
                return self.replies.pop(0)
            return super().open(request, timeout)
    waits = []
    opener = Bodies([token(), metadata(4), Interrupted(), b'abcd', metadata(4)])
    transport = intake.DriveTransport(credentials(), opener=opener, sleep=waits.append)
    assert transport.read('synthetic_file', 'synthetic_folder', 100) == b'abcd'
    assert waits == [1]


def source_fixture():
    prior = {'id': 'src-aaaaaaaaaaaa', 'url': 'https://example.org/source', 'title': 'Example',
             'publisher': 'Example', 'source_type': 'primary', 'published_at': None,
             'accessed_at': '2026-10-07', 'claim_scope': ['Historical claim'], 'limitations': ['Historical limit']}
    proposed = deepcopy(prior)
    proposed.update(id='new:example', accessed_at='2026-10-09', claim_scope=['Inspected claim'], limitations=['New limit'])
    packet = {'changes': [{'kind': 'source', 'record': proposed, 'previous_hash': None,
                           'identity_key': proposed['url'], 'evidence_ids': ['new:example']}],
              'source_groups': {'new:example': 'group'},
              'research_run': {'field_checks': [{'entity_id': 'new:example', 'evidence_ids': ['new:example']}],
                               'task_decisions': [{'contradictory_evidence_ids': ['new:example']}]}}
    return packet, {('source', prior['id']): prior}


def test_exact_source_identity_reconciliation_preserves_history_and_input():
    packet, baseline = source_fixture()
    original, original_baseline = deepcopy(packet), deepcopy(baseline)
    result, report = reconcile_sources(packet, baseline)
    record = result['changes'][0]['record']
    assert report['reference_mapping'] == {'new:example': 'src-aaaaaaaaaaaa'}
    assert record['claim_scope'] == ['Historical claim', 'Inspected claim']
    assert record['limitations'] == ['Historical limit', 'New limit']
    assert record['accessed_at'] == '2026-10-09'
    assert result['changes'][0]['previous_hash']
    assert result['source_groups'] == {'src-aaaaaaaaaaaa': 'group'}
    assert result['research_run']['field_checks'][0]['entity_id'] == 'src-aaaaaaaaaaaa'
    assert result['research_run']['task_decisions'][0]['contradictory_evidence_ids'] == ['src-aaaaaaaaaaaa']
    assert packet == original and baseline == original_baseline


def test_different_url_is_not_identity_equivalence():
    packet, baseline = source_fixture()
    packet['changes'][0]['record']['url'] += '/'
    result, report = reconcile_sources(packet, baseline)
    assert result == packet and report['reference_mapping'] == {}


@pytest.mark.parametrize('mutation,match', [('metadata', 'conflicting'), ('date', 'regressed'),
                                          ('duplicate', 'Duplicate'), ('groups', 'independence')])
def test_source_reconciliation_never_guesses(mutation, match):
    packet, baseline = source_fixture()
    if mutation == 'metadata': packet['changes'][0]['record']['published_at'] = '2026-10-09'
    elif mutation == 'date': packet['changes'][0]['record']['accessed_at'] = '2000-01-01'
    elif mutation == 'duplicate': packet['changes'].append(deepcopy(packet['changes'][0]))
    else: packet['source_groups']['src-aaaaaaaaaaaa'] = 'conflicting-group'
    with pytest.raises(ValueError, match=match): reconcile_sources(packet, baseline)
