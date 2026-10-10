"""Standalone final-delivery intake. No evidence certification, writes to catalog, or publication.

Transport consumes an explicitly supplied authorized-user token file. Incoming
manifests are data; neither they nor research packets choose commands or paths.
"""
from contextlib import contextmanager
from hashlib import sha256
import argparse
import http.client
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, build_opener, HTTPRedirectHandler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.research_batch import linked, pairs, require, MAX_BYTES

API = 'https://www.googleapis.com/drive/v3/files'
TOKEN = 'https://oauth2.googleapis.com/token'
READONLY = 'https://www.googleapis.com/auth/drive.readonly'
FILE_SCOPE = 'https://www.googleapis.com/auth/drive.file'
MANIFEST_BYTES = 64 * 1024
FILE_ID = re.compile(r'^[A-Za-z0-9_-]{1,200}$')
IDENT = re.compile(r'^[a-z][a-z0-9-]{0,127}$')


def parse(raw):
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda _: require(False, 'Non-finite JSON number'))


def private_path(root, path):
    """Require ignored local storage, reject Windows reparse points in ancestors."""
    root, path = Path(root).resolve(), Path(os.path.abspath(path))
    require(path.is_relative_to(root / '.local'), 'Use private .local storage')
    cursor = path
    while cursor != root:
        require(not linked(cursor), 'Private path contains a link/reparse point')
        cursor = cursor.parent
    return path


def manifest_errors(m):
    fields = {'schema_version', 'assignment_id', 'baseline_commit', 'artifact_id',
              'bytes', 'sha256', 'revision', 'supersedes', 'status'}
    require(isinstance(m, dict) and set(m) == fields, 'Invalid final-delivery manifest fields')
    require(m['schema_version'] == '1.0' and m['status'] == 'completed', 'Delivery is not final')
    require(isinstance(m['assignment_id'], str) and IDENT.fullmatch(m['assignment_id']), 'Invalid assignment identity')
    require(isinstance(m['baseline_commit'], str) and re.fullmatch('[a-f0-9]{40}', m['baseline_commit']), 'Invalid baseline')
    require(isinstance(m['artifact_id'], str) and FILE_ID.fullmatch(m['artifact_id']), 'Invalid artifact identity')
    require(type(m['bytes']) is int and 0 < m['bytes'] <= MAX_BYTES, 'Invalid artifact byte bound')
    require(isinstance(m['sha256'], str) and re.fullmatch('[a-f0-9]{64}', m['sha256']), 'Invalid artifact digest')
    require(type(m['revision']) is int and 1 <= m['revision'] <= 1000000, 'Invalid revision')
    require(m['supersedes'] is None or isinstance(m['supersedes'], str) and
            re.fullmatch('[a-f0-9]{64}', m['supersedes']), 'Invalid supersession digest')
    require((m['revision'] == 1) == (m['supersedes'] is None), 'Revision requires explicit supersession')
    require(m['supersedes'] != m['sha256'], 'Delivery cannot supersede itself')
    return m


def select_deliveries(manifests, assignments):
    """Fail on forks/gaps; select only a complete, trusted revision chain."""
    groups = {}
    for m in manifests:
        manifest_errors(m)
        a = assignments.get(m['assignment_id'])
        require(a is not None and a['assignment_id'] == m['assignment_id'] and
                a['baseline_commit'] == m['baseline_commit'], 'Untrusted assignment/baseline')
        group = groups.setdefault(m['assignment_id'], {})
        prior = group.get(m['revision'])
        require(prior is None or prior == m, 'Conflicting delivery revision')
        group[m['revision']] = m
    selected = []
    for revisions in groups.values():
        ordered = [revisions[n] for n in sorted(revisions)]
        require([m['revision'] for m in ordered] == list(range(1, len(ordered) + 1)), 'Missing delivery revision')
        for older, newer in zip(ordered, ordered[1:]):
            require(newer['supersedes'] == older['sha256'], 'Broken delivery supersession chain')
        selected.append(ordered[-1])
    return sorted(selected, key=lambda m: m['assignment_id'])


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class DriveTransport:
    """Bounded official HTTPS requests; never log response bodies or credentials."""
    def __init__(self, credentials, *, opener=None, sleep=time.sleep):
        require(isinstance(credentials, dict) and credentials.get('type') == 'authorized_user',
                'Separate authorized-user credentials required')
        require(all(isinstance(credentials.get(k), str) and credentials[k] for k in
                    ('client_id', 'client_secret', 'refresh_token')), 'Incomplete authorized-user credentials')
        scopes = credentials.get('scopes', [])
        require(isinstance(scopes, list) and scopes and set(scopes) <= {READONLY, FILE_SCOPE},
                'Explicit Drive content-read scope required')
        self.credentials, self.opener, self.sleep = credentials, opener or build_opener(NoRedirect()), sleep
        self.access_token, self.expires = None, 0

    def _request(self, url, *, data=None, authenticated=True):
        if authenticated and time.monotonic() >= self.expires:
            payload = urlencode({k: self.credentials[k] for k in
                                 ('client_id', 'client_secret', 'refresh_token')} |
                                {'grant_type': 'refresh_token'}).encode()
            with self._request(TOKEN, data=payload, authenticated=False) as response:
                raw = response.read(MANIFEST_BYTES + 1)
            require(len(raw) <= MANIFEST_BYTES, 'Token response exceeds bound')
            token = parse(raw)
            require(isinstance(token.get('access_token'), str) and token['access_token'] and
                    type(token.get('expires_in')) is int and token['expires_in'] > 60,
                    'Invalid token response')
            if 'scope' in token:
                require(set(token['scope'].split()) & {READONLY, FILE_SCOPE}, 'Token lacks content-read scope')
            self.access_token, self.expires = token['access_token'], time.monotonic() + token['expires_in'] - 60
        headers = {'Accept': 'application/json', 'Accept-Encoding': 'identity'}
        if authenticated:
            headers['Authorization'] = 'Bearer ' + self.access_token
        if data is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        for attempt in range(3):
            try:
                return self.opener.open(Request(url, data=data, headers=headers), timeout=30)
            except HTTPError as exc:
                code = exc.code
                exc.close()
                if code in {401, 403} or (url == TOKEN and code == 400):
                    raise ValueError('Drive authorization failed; reauthorize separately') from None
                if code not in {429, 500, 502, 503, 504} or attempt == 2:
                    raise ValueError('Drive request failed (HTTP ' + str(code) + ')') from None
            except (URLError, TimeoutError, OSError):
                if attempt == 2:
                    raise ValueError('Drive transport unavailable after bounded retries') from None
            self.sleep(2 ** attempt)

    def json(self, url):
        with self._request(url) as response:
            raw = response.read(1024 * 1024 + 1)
        require(len(raw) <= 1024 * 1024, 'Drive metadata exceeds bound')
        return parse(raw)

    def metadata(self, ident):
        require(isinstance(ident, str) and FILE_ID.fullmatch(ident), 'Invalid Drive file identity')
        return self.json(API + '/' + quote(ident, safe='') + '?' + urlencode({
            'fields': 'id,name,mimeType,size,parents,trashed,version,capabilities(canDownload)',
            'supportsAllDrives': 'true'}))

    def manifests(self, folder):
        require(isinstance(folder, str) and FILE_ID.fullmatch(folder), 'Invalid inbox identity')
        query = {'q': "'" + folder + "' in parents and trashed = false and mimeType = 'application/json'",
                 'fields': 'nextPageToken,files(id,name)', 'pageSize': '100',
                 'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}
        result, seen = [], set()
        for _ in range(100):
            page = self.json(API + '?' + urlencode(query))
            for item in page['files']:
                if item['name'].endswith('.delivery.json'):
                    result.append(item['id'])
            token = page.get('nextPageToken')
            if not token:
                return result
            require(token not in seen, 'Drive pagination loop')
            seen.add(token)
            query['pageToken'] = token
        raise ValueError('Inbox pagination bound exceeded')

    def read(self, ident, folder, limit, expected=None):
        """Bound bytes and pin metadata before/after media retrieval."""
        before = self.metadata(ident)
        require(before.get('id') == ident and folder in before.get('parents', []) and
                before.get('trashed') is False and before.get('mimeType') == 'application/json' and
                before.get('capabilities', {}).get('canDownload') is True and before.get('version'),
                'Artifact metadata is not eligible')
        size = int(before.get('size', -1))
        require(0 < size <= limit and (expected is None or size == expected), 'Artifact metadata size differs')
        for attempt in range(3):
            try:
                chunks, count = [], 0
                with self._request(API + '/' + quote(ident, safe='') + '?alt=media&supportsAllDrives=true') as response:
                    while True:
                        chunk = response.read(min(1024 * 1024, size - count + 1))
                        if not chunk:
                            break
                        count += len(chunk)
                        require(count <= size, 'Artifact exceeds exact byte bound')
                        chunks.append(chunk)
                require(count == size, 'Truncated artifact')
                break
            except (URLError, TimeoutError, OSError, http.client.HTTPException):
                if attempt == 2:
                    raise ValueError('Interrupted media retrieval after bounded retries') from None
                self.sleep(2 ** attempt)
        after = self.metadata(ident)
        require(after == before, 'Artifact changed during retrieval')
        return b''.join(chunks)


@contextmanager
def run_lock(path):
    """OS-held lock releases on process death; persistent file supports recovery."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        if path.stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise ValueError('Another intake run holds the lock') from None
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def retain(directory, name, raw):
    path = directory / name
    require(not linked(path), 'Retained input cannot be a link')
    if path.exists():
        require(path.read_bytes() == raw, 'Retained delivery differs')
        return False
    directory.mkdir(parents=True, exist_ok=True)
    temporary = directory / (name + '.part')
    require(not linked(temporary), 'Download checkpoint cannot be a link')
    with temporary.open('wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    return True


def intake(transport, folder, assignments, destination):
    incoming = []
    for ident in transport.manifests(folder):
        raw = transport.read(ident, folder, MANIFEST_BYTES)
        incoming.append((manifest_errors(parse(raw)), raw))
    selected = select_deliveries([m for m, _ in incoming], assignments)
    deliveries = []
    for m in selected:
        directory = destination / m['assignment_id'] / m['sha256']
        require(not linked(directory) and not linked(directory.parent), 'Delivery storage contains a link')
        path = directory / 'packet.json'
        require(not linked(path), 'Retained packet cannot be a link')
        raw = path.read_bytes() if path.exists() else transport.read(m['artifact_id'], folder, MAX_BYTES, m['bytes'])
        require(len(raw) == m['bytes'] and sha256(raw).hexdigest() == m['sha256'], 'Artifact digest/bytes differ')
        packet = parse(raw)
        require(isinstance(packet, dict) and packet.get('assignment_id') == m['assignment_id'] and
                packet.get('baseline_commit') == m['baseline_commit'], 'Packet identity differs from final manifest')
        fresh = retain(directory, 'packet.json', raw)
        manifest_raw = next(raw for value, raw in incoming if value == m)
        retain(directory, 'delivery.json', manifest_raw)
        deliveries.append({'assignment_id': m['assignment_id'], 'sha256': m['sha256'],
                           'revision': m['revision'], 'new_bytes': fresh,
                           'status': 'bytes_verified_pending_structure_and_evidence_review'})
    return {'status': 'deliveries_retained' if deliveries else 'no_final_delivery', 'deliveries': deliveries}


def verify_transport(transport, folder, assignment, destination, ident, size, digest):
    """Always download an operator-pinned artifact; do not certify final delivery.

    This supports proving transport for legacy files that lack a producer manifest.
    Its receipt is deliberately separate from normal delivery selection/retention.
    """
    require(isinstance(assignment, dict), 'Trusted assignment required')
    probe = manifest_errors({'schema_version': '1.0', 'assignment_id': assignment['assignment_id'],
        'baseline_commit': assignment['baseline_commit'], 'artifact_id': ident,
        'bytes': size, 'sha256': digest, 'revision': 1, 'supersedes': None, 'status': 'completed'})
    raw = transport.read(ident, folder, MAX_BYTES, size)
    require(len(raw) == size and sha256(raw).hexdigest() == digest, 'Artifact digest/bytes differ')
    packet = parse(raw)
    require(isinstance(packet, dict) and packet.get('assignment_id') == probe['assignment_id'] and
            packet.get('baseline_commit') == probe['baseline_commit'], 'Packet identity differs from trusted assignment')
    directory = destination / 'transport-proof' / probe['assignment_id'] / digest
    require(all(not linked(p) for p in (directory, directory.parent, directory.parent.parent)),
            'Transport proof storage contains a link')
    retain(directory, 'packet.json', raw)
    receipt = {'schema_version': '1.0', 'assignment_id': probe['assignment_id'],
        'baseline_commit': probe['baseline_commit'], 'artifact_id': ident, 'bytes': size,
        'sha256': digest, 'status': 'transport_bytes_verified', 'final_delivery_verified': False,
        'research_reviewed': False, 'published': False}
    retain(directory, 'transport-proof.json', (json.dumps(receipt, indent=2) + '\n').encode())
    return receipt


def load_config(root, path):
    config = parse(private_path(root, path).read_bytes())
    require(isinstance(config, dict) and set(config) ==
            {'schema_version', 'folder_id', 'credentials_path', 'assignments', 'destination'},
            'Invalid private intake configuration')
    require(config['schema_version'] == '1.0' and isinstance(config['folder_id'], str) and
            FILE_ID.fullmatch(config['folder_id']), 'Invalid intake configuration')
    destination = private_path(root, config['destination'])
    credential_path = private_path(root, config['credentials_path'])
    assignments = {}
    require(isinstance(config['assignments'], dict) and config['assignments'], 'Trusted assignments required')
    for ident, assignment_path in config['assignments'].items():
        require(isinstance(ident, str) and IDENT.fullmatch(ident), 'Invalid configured assignment identity')
        assignment = parse(private_path(root, assignment_path).read_bytes())
        require(isinstance(assignment, dict) and assignment.get('assignment_id') == ident and
                isinstance(assignment.get('baseline_commit'), str) and
                re.fullmatch('[a-f0-9]{40}', assignment['baseline_commit']),
                'Configured assignment identity/baseline differs')
        assignments[ident] = assignment
    return config, destination, credential_path, assignments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check-config', 'pickup', 'verify-transport'])
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--assignment-id')
    parser.add_argument('--file-id')
    parser.add_argument('--bytes', type=int)
    parser.add_argument('--sha256')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    config, destination, credential_path, assignments = load_config(root, args.config)
    if args.mode == 'verify-transport':
        require(args.assignment_id in assignments and args.file_id and args.bytes and args.sha256,
                'Pinned transport check requires assignment, file identity, exact bytes and digest')
    else:
        require(all(v is None for v in (args.assignment_id, args.file_id, args.bytes, args.sha256)),
                'Pinned artifact arguments only apply to verify-transport')
    if args.mode == 'check-config':
        print(json.dumps({'status': 'configuration_valid', 'credential_file_present': credential_path.is_file(),
                          'assignments': len(assignments), 'transport_proven': False}))
        return
    require(credential_path.is_file(), 'Separate authorized-user credential file is missing')
    transport = DriveTransport(parse(credential_path.read_bytes()))
    with run_lock(private_path(root, destination / 'intake.lock')):
        if args.mode == 'verify-transport':
            result = verify_transport(transport, config['folder_id'], assignments[args.assignment_id],
                                      destination, args.file_id, args.bytes, args.sha256)
        else:
            result = intake(transport, config['folder_id'], assignments, destination)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RecursionError):
        # Exceptions may contain credentials, private paths, or incoming text.
        print('Intake failed; check private configuration, authorization, and delivery integrity.', file=sys.stderr)
        sys.exit(1)
