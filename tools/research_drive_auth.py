"""One-time desktop Google consent for the standalone read-only research intake.

Uses the installed-app PKCE/loopback flow. No connector credential extraction,
service registration, Drive writes, inference, or catalog updates are performed.
Client configuration and resulting credentials must remain in ignored .local.
"""
import argparse
import base64
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, build_opener

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.research_intake import (DriveTransport, MANIFEST_BYTES, NoRedirect,
    READONLY, TOKEN, load_config, parse, private_path, require, run_lock)

AUTHORIZE = 'https://accounts.google.com/o/oauth2/v2/auth'
CLIENT_AUTH_URIS = {AUTHORIZE, 'https://accounts.google.com/o/oauth2/auth'}


def desktop_client(raw):
    value = parse(raw)
    require(isinstance(value, dict) and set(value) == {'installed'}, 'Google Desktop client JSON required')
    client = value['installed']
    require(isinstance(client, dict) and all(isinstance(client.get(k), str) and client[k]
            for k in ('client_id', 'client_secret')), 'Incomplete Desktop client JSON')
    require(client.get('auth_uri') in CLIENT_AUTH_URIS and client.get('token_uri') == TOKEN,
            'Only official Google authorization endpoints are supported')
    require(isinstance(client.get('redirect_uris'), list) and
            any(uri in {'http://localhost', 'http://127.0.0.1'} for uri in client['redirect_uris']),
            'Desktop loopback redirect required')
    return client


def authorization_url(client, redirect, state, verifier):
    challenge = base64.urlsafe_b64encode(sha256(verifier.encode('ascii')).digest()).rstrip(b'=').decode()
    return AUTHORIZE + '?' + urlencode({'client_id': client['client_id'],
        'redirect_uri': redirect, 'response_type': 'code', 'scope': READONLY,
        'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256',
        'access_type': 'offline', 'prompt': 'consent', 'include_granted_scopes': 'false'})


def callback_result(target, host, expected_host, state):
    require(host == expected_host and len(target) <= 8192, 'Invalid local callback')
    parsed = urlsplit(target)
    require(not parsed.scheme and not parsed.netloc and parsed.path == '/oauth2callback' and
            not parsed.fragment, 'Invalid local callback path')
    query = parse_qs(parsed.query, keep_blank_values=True, max_num_fields=20)
    require(all(len(values) == 1 for values in query.values()), 'Duplicate callback parameters')
    require(isinstance(query.get('state', [None])[0], str) and
            secrets.compare_digest(query['state'][0], state), 'Callback state differs')
    require(('code' in query) != ('error' in query), 'Callback must contain code or refusal')
    if 'error' in query:
        return {'denied': True}
    require(0 < len(query['code'][0]) <= 4096, 'Invalid authorization code')
    return {'code': query['code'][0]}


def exchange_code(client, code, redirect, verifier, *, opener=None):
    payload = urlencode({'client_id': client['client_id'], 'client_secret': client['client_secret'],
        'code': code, 'redirect_uri': redirect, 'code_verifier': verifier,
        'grant_type': 'authorization_code'}).encode()
    try:
        with (opener or build_opener(NoRedirect())).open(Request(TOKEN, data=payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded',
                         'Accept-Encoding': 'identity'}), timeout=30) as response:
            raw = response.read(MANIFEST_BYTES + 1)
    except HTTPError as error:
        error.close()
        raise ValueError('Google authorization exchange failed') from None
    except (URLError, OSError, TimeoutError):
        raise ValueError('Google authorization exchange unavailable') from None
    require(len(raw) <= MANIFEST_BYTES, 'Authorization response exceeds bound')
    token = parse(raw)
    require(isinstance(token, dict) and token.get('token_type', '').lower() == 'bearer' and
            isinstance(token.get('access_token'), str) and token['access_token'] and
            isinstance(token.get('refresh_token'), str) and token['refresh_token'],
            'Offline authorization did not return usable tokens')
    require(isinstance(token.get('scope'), str) and token['scope'].split() == [READONLY],
            'Google did not grant exactly the requested Drive read-only scope')
    result = {'type': 'authorized_user', 'client_id': client['client_id'],
        'client_secret': client['client_secret'], 'refresh_token': token['refresh_token'],
        'scopes': [READONLY]}
    DriveTransport(result)  # Validate the same credential contract used by pickup.
    return result


def protect_file(path):
    """Restrict an empty credential file before placing secrets in it."""
    if os.name != 'nt':
        os.chmod(path, 0o600)
        return
    # The command is fixed; no account, path or credential is interpolated into it.
    identity = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
        '[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value'],
        capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    import re
    require(re.fullmatch(r'S-1-\d+(?:-\d+)+', identity), 'Could not determine local execution identity')
    subprocess.run(['icacls.exe', str(path), '/inheritance:r', '/grant:r', '*' + identity + ':(F)'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15, check=True)


def save_credentials(root, destination, credentials):
    destination = private_path(root, destination)
    require(not destination.exists(), 'Existing authorization is never overwritten')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = private_path(root, destination.with_name(destination.name + '.part'))
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        protect_file(temporary)
        with os.fdopen(descriptor, 'wb') as stream:
            descriptor = None
            stream.write((json.dumps(credentials, indent=2) + '\n').encode())
            stream.flush()
            os.fsync(stream.fileno())
        # Windows rename refuses replacement; POSIX link provides the same exclusion.
        if os.name == 'nt':
            os.rename(temporary, destination)
        else:
            os.link(temporary, destination)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def authorize(root, client, credential_path, work, *, seconds=600):
    require(30 <= seconds <= 900, 'Authorization timeout must be 30 to 900 seconds')
    require(not credential_path.exists(), 'Existing authorization is never overwritten')
    state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(64)
    result = {}

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(3)

        def log_message(self, *args):
            pass  # Callback URLs include a code; never log them.

        def do_GET(self):
            try:
                value = callback_result(self.path, self.headers.get('Host'), expected_host, state)
            except ValueError:
                self.send_error(400, 'Invalid authorization callback')
                return
            result.update(value)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.end_headers()
            self.wfile.write(b'Google response received. Close this tab and return to the local runner.')

    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        server.timeout = 1
        expected_host = '127.0.0.1:' + str(server.server_port)
        redirect = 'http://' + expected_host + '/oauth2callback'
        url_path = private_path(root, work / 'drive-authorization-url.txt')
        require(not url_path.exists(), 'Another authorization flow has a retained sign-in link')
        url_path.write_text(authorization_url(client, redirect, state, verifier), encoding='utf-8')
        print('Sign-in link prepared in the private setup directory; approve Drive read-only access in Google.', flush=True)
        try:
            deadline = time.monotonic() + seconds
            while not result and time.monotonic() < deadline:
                server.handle_request()
            require(result and not result.get('denied'), 'Google consent declined or authorization timed out')
            credentials = exchange_code(client, result['code'], redirect, verifier)
            save_credentials(root, credential_path, credentials)
        finally:
            url_path.unlink(missing_ok=True)
    return {'status': 'authorization_saved', 'scope': READONLY, 'transport_proven': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check-client', 'authorize'])
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--timeout-seconds', type=int, default=600)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    _, _, credential_path, _ = load_config(root, args.config)
    client_path = private_path(root, args.client)
    require(client_path.stat().st_size <= MANIFEST_BYTES, 'Desktop client JSON exceeds bound')
    client = desktop_client(client_path.read_bytes())
    if args.mode == 'check-client':
        print(json.dumps({'status': 'desktop_client_valid', 'scope': READONLY,
                          'credential_file_present': credential_path.is_file(), 'live_authorization_verified': False}))
        return
    with run_lock(private_path(root, credential_path.parent / 'drive-authorization.lock')):
        result = authorize(root, client, credential_path, credential_path.parent, seconds=args.timeout_seconds)
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.SubprocessError):
        print('Drive setup failed; check the private Desktop client, consent, and local callback. No tokens are printed.',
              file=sys.stderr)
        sys.exit(1)
