"""Consent/transport boundaries, using synthetic credentials without Google calls."""
from copy import deepcopy
from hashlib import sha256
import base64
import io
import json
import os
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlsplit
import pytest
from tools import research_drive_auth as auth
from tools import research_intake as intake


def client():
    return {'client_id': 'synthetic-client', 'client_secret': 'synthetic-secret',
            'auth_uri': auth.AUTHORIZE, 'token_uri': intake.TOKEN, 'redirect_uris': ['http://localhost']}


def grant():
    return {'token_type': 'Bearer', 'access_token': 'synthetic-access',
            'refresh_token': 'synthetic-refresh', 'scope': intake.READONLY}


class Opener:
    def __init__(self, response):
        self.response, self.calls = response, []

    def open(self, request, timeout):
        self.calls.append(request)
        if isinstance(self.response, Exception):
            raise self.response
        return io.BytesIO(json.dumps(self.response).encode())


def test_only_desktop_client_and_google_endpoints():
    assert auth.desktop_client(json.dumps({'installed': client()}).encode()) == client()
    downloaded = client() | {'auth_uri': 'https://accounts.google.com/o/oauth2/auth'}
    assert auth.desktop_client(json.dumps({'installed': downloaded}).encode()) == downloaded
    invalid = [{'web': client()}, {'installed': {}}, {'installed': client(), 'extra': 'bad'}]
    for key, value in [('auth_uri', 'https://example.org/auth'),
                       ('token_uri', 'https://example.org/token'), ('redirect_uris', ['urn:ietf:wg:oauth:2.0:oob'])]:
        changed = client()
        changed[key] = value
        invalid.append({'installed': changed})
    for value in invalid:
        with pytest.raises(ValueError):
            auth.desktop_client(json.dumps(value).encode())


def test_authorization_link_uses_pkce_offline_and_read_only():
    verifier = 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'
    link = auth.authorization_url(client(), 'http://127.0.0.1:1234/oauth2callback', 'state', verifier)
    query = parse_qs(urlsplit(link).query)
    assert link.startswith(auth.AUTHORIZE + '?')
    assert query['scope'] == [intake.READONLY]
    assert query['access_type'] == ['offline'] and query['prompt'] == ['consent']
    assert query['code_challenge_method'] == ['S256']
    assert query['code_challenge'] == ['E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM']
    assert query['include_granted_scopes'] == ['false']
    assert 'client_secret' not in query and 'code_verifier' not in query
    assert 'synthetic-secret' not in link


def test_callback_requires_host_state_and_unique_parameters():
    valid = '/oauth2callback?' + urlencode({'state': 'expected', 'code': 'synthetic-code'})
    assert auth.callback_result(valid, '127.0.0.1:1234', '127.0.0.1:1234', 'expected') == {'code': 'synthetic-code'}
    bad = [(valid, 'example.org'), (valid + '&code=duplicate', '127.0.0.1:1234'),
           (valid.replace('expected', 'wrong'), '127.0.0.1:1234'),
           (valid + '&error=refused', '127.0.0.1:1234'),
           (valid.replace('/oauth2callback', '/other'), '127.0.0.1:1234'),
           ('http://example.org' + valid, '127.0.0.1:1234'),
           (valid + '#fragment', '127.0.0.1:1234')]
    for target, host in bad:
        with pytest.raises(ValueError):
            auth.callback_result(target, host, '127.0.0.1:1234', 'expected')
    refusal = '/oauth2callback?state=expected&error=access_denied'
    assert auth.callback_result(refusal, '127.0.0.1:1234', '127.0.0.1:1234', 'expected') == {'denied': True}


def test_token_exchange_never_persists_access_token():
    opener = Opener(grant())
    credentials = auth.exchange_code(client(), 'synthetic-code', 'http://127.0.0.1:1234/oauth2callback',
                                     'verifier', opener=opener)
    assert credentials['refresh_token'] == 'synthetic-refresh'
    assert credentials['scopes'] == [intake.READONLY] and 'access_token' not in credentials
    assert len(opener.calls) == 1 and opener.calls[0].full_url == intake.TOKEN
    body = parse_qs(opener.calls[0].data.decode())
    assert body['code_verifier'] == ['verifier'] and body['grant_type'] == ['authorization_code']


@pytest.mark.parametrize('field,value', [('refresh_token', ''), ('access_token', ''),
    ('token_type', 'other'), ('scope', intake.FILE_SCOPE),
    ('scope', intake.READONLY + ' https://www.googleapis.com/auth/drive'), ('scope', None)])
def test_incomplete_or_expanded_grant_is_refused(field, value):
    response = grant()
    response[field] = value
    with pytest.raises(ValueError):
        auth.exchange_code(client(), 'code', 'redirect', 'verifier', opener=Opener(response))


def test_exchange_error_is_sanitized_and_not_retried():
    opener = Opener(HTTPError(intake.TOKEN, 400, 'secret error', {}, io.BytesIO(b'secret')))
    with pytest.raises(ValueError, match='exchange failed') as error:
        auth.exchange_code(client(), 'code', 'redirect', 'verifier', opener=opener)
    assert 'secret' not in str(error.value) and len(opener.calls) == 1


def test_secure_storage_no_overwrite_or_public_path(tmp_path, monkeypatch):
    protected = []
    monkeypatch.setattr(auth, 'protect_file', protected.append)
    destination = tmp_path / '.local' / 'authorization.json'
    credentials = {'synthetic': 'not-a-real-token'}
    auth.save_credentials(tmp_path, destination, credentials)
    assert json.loads(destination.read_text()) == credentials
    assert protected == [destination.with_name(destination.name + '.part')]
    assert not protected[0].exists()
    with pytest.raises(ValueError, match='never overwritten'):
        auth.save_credentials(tmp_path, destination, {'changed': True})
    assert json.loads(destination.read_text()) == credentials
    with pytest.raises(ValueError, match='private'):
        auth.save_credentials(tmp_path, tmp_path / 'public.json', credentials)


def test_permissions_failure_never_writes_secrets(tmp_path, monkeypatch):
    def fail(_):
        raise OSError('permission restriction unavailable')
    monkeypatch.setattr(auth, 'protect_file', fail)
    destination = tmp_path / '.local' / 'authorization.json'
    with pytest.raises(OSError):
        auth.save_credentials(tmp_path, destination, {'secret': 'synthetic'})
    assert not destination.exists() and not destination.with_name(destination.name + '.part').exists()


def test_native_protected_storage(tmp_path):
    destination = tmp_path / '.local' / 'protected.json'
    auth.save_credentials(tmp_path, destination, {'fixture': 'synthetic'})
    assert json.loads(destination.read_text()) == {'fixture': 'synthetic'}
    if os.name != 'nt':
        assert destination.stat().st_mode & 0o777 == 0o600


@pytest.mark.parametrize('refuse', [False, True])
def test_complete_local_callback_flow_ignores_bad_state_and_cleans_link(tmp_path, monkeypatch, refuse):
    work = tmp_path / '.local' / 'setup'
    work.mkdir(parents=True)
    destination = work / 'authorization.json'
    link = work / 'drive-authorization-url.txt'
    calls, exchanges, responses = [], [], []
    class Server:
        server_port = 1234
        def __init__(self, address, handler):
            assert address == ('127.0.0.1', 0)
            self.handler = handler
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def handle_request(self):
            query = parse_qs(urlsplit(link.read_text()).query)
            calls.append(query)
            state = 'wrong' if len(calls) == 1 else query['state'][0]
            value = {'state': state, 'error' if refuse else 'code': 'access_denied' if refuse else 'synthetic-code'}
            handler = object.__new__(self.handler)
            handler.path = '/oauth2callback?' + urlencode(value)
            handler.headers = {'Host': '127.0.0.1:1234'}
            handler.send_error = lambda *args: responses.append(args[0])
            handler.send_response = lambda code: responses.append(code)
            handler.send_header = lambda *args: None
            handler.end_headers = lambda: None
            handler.wfile = io.BytesIO()
            handler.do_GET()
    def exchange(c, code, redirect, verifier):
        exchanges.append(code)
        challenge = base64.urlsafe_b64encode(sha256(verifier.encode()).digest()).rstrip(b'=').decode()
        assert calls[-1]['code_challenge'] == [challenge]
        assert redirect == 'http://127.0.0.1:1234/oauth2callback'
        return {'fixture': 'synthetic'}
    monkeypatch.setattr(auth, 'HTTPServer', Server)
    monkeypatch.setattr(auth, 'exchange_code', exchange)
    monkeypatch.setattr(auth, 'protect_file', lambda path: None)
    if refuse:
        with pytest.raises(ValueError, match='consent declined'):
            auth.authorize(tmp_path, client(), destination, work)
        assert exchanges == [] and not destination.exists()
    else:
        result = auth.authorize(tmp_path, client(), destination, work)
        assert result == {'status': 'authorization_saved', 'scope': intake.READONLY, 'transport_proven': False}
        assert json.loads(destination.read_text()) == {'fixture': 'synthetic'}
        assert exchanges == ['synthetic-code']
    assert responses == [400, 200] and not link.exists()


def test_local_consent_timeout_cleans_link_and_never_exchanges(tmp_path, monkeypatch):
    work = tmp_path / '.local'
    work.mkdir()
    class Server:
        server_port = 1234
        def __init__(self, *args): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def handle_request(self): pass
    ticks = iter([0, 1, 31])
    monkeypatch.setattr(auth, 'HTTPServer', Server)
    monkeypatch.setattr(auth.time, 'monotonic', lambda: next(ticks))
    monkeypatch.setattr(auth, 'exchange_code', lambda *args: pytest.fail('No exchange after timeout'))
    with pytest.raises(ValueError, match='timed out'):
        auth.authorize(tmp_path, client(), work / 'authorization.json', work, seconds=30)
    assert not list(work.glob('*.txt')) and not (work / 'authorization.json').exists()


def test_proof_always_downloads_and_does_not_create_final_delivery(tmp_path):
    assignment = {'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}
    raw = json.dumps(assignment).encode()
    class Transport:
        calls = 0
        def read(self, ident, folder, limit, expected):
            self.calls += 1
            assert ident == 'file' and expected == len(raw)
            return raw
    transport = Transport()
    digest = sha256(raw).hexdigest()
    for _ in range(2):
        receipt = intake.verify_transport(transport, 'folder', assignment, tmp_path, 'file', len(raw), digest)
        assert receipt['status'] == 'transport_bytes_verified'
        assert receipt['final_delivery_verified'] is False and receipt['research_reviewed'] is False
    assert transport.calls == 2 and not list(tmp_path.rglob('delivery.json'))


@pytest.mark.parametrize('change', ['digest', 'identity', 'size'])
def test_proof_rejects_mismatch_before_retention(tmp_path, change):
    assignment = {'assignment_id': 'synthetic', 'baseline_commit': 'a' * 40}
    raw = json.dumps(assignment).encode()
    digest, size = sha256(raw).hexdigest(), len(raw)
    if change == 'digest': digest = 'b' * 64
    if change == 'size': size += 1
    if change == 'identity': assignment = deepcopy(assignment) | {'baseline_commit': 'b' * 40}
    class Transport:
        def read(self, *args): return raw
    with pytest.raises(ValueError):
        intake.verify_transport(Transport(), 'folder', assignment, tmp_path, 'file', size, digest)
    assert not list(tmp_path.rglob('packet.json'))
