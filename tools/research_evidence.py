"""Retain bounded public source bodies. Failures are unavailable evidence, never verification."""
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import argparse
import base64
import http.client
import ipaddress
import json
from pathlib import Path
import socket
import ssl
import subprocess
import sys
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.research_followups import public_url

MAX_BODY = 2 * 1024 * 1024


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if not self.hidden and tag == 'meta':
            key = attributes.get('property') or attributes.get('name')
            if key in {'article:published_time', 'article:modified_time', 'date', 'datePublished',
                       'dateModified', 'author', 'og:title', 'og:url'} and attributes.get('content'):
                self.parts.append('\nSource metadata ' + key + ': ' + attributes['content'] + '\n')
        if not self.hidden and tag == 'time' and attributes.get('datetime'):
            self.parts.append('\nSource datetime attribute: ' + attributes['datetime'] + '\n')
        if tag in {'script', 'style', 'noscript'}:
            self.hidden += 1
        elif not self.hidden and tag in {'p', 'br', 'div', 'li', 'tr', 'td', 'th', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript'} and self.hidden:
            self.hidden -= 1
        elif not self.hidden and tag in {'p', 'div', 'li', 'tr', 'td', 'th', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def text_body(raw, content_type):
    media = content_type.split(';')[0].strip().lower()
    if media not in {'text/html', 'application/xhtml+xml', 'text/plain', 'text/markdown', 'application/json'}:
        raise ValueError('Unsupported source body; original bytes retained without reviewable text')
    # Strict UTF-8: unsupported encodings are disclosed, not silently repaired.
    decoded = raw.decode('utf-8-sig')
    if media in {'text/html', 'application/xhtml+xml'}:
        parser = Text()
        parser.feed(decoded)
        decoded = ''.join(parser.parts)
    if not decoded.strip() or '\x00' in decoded:
        raise ValueError('Empty or binary source text')
    return decoded


def resolve_public(host, port=443):
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise ValueError('Source resolved to a non-public address')
    return addresses[0]


def get_public(url, *, timeout=15, limit=MAX_BODY):
    """Pin a public DNS answer to the connection; verify TLS against the URL host."""
    current, history = url, []
    for _ in range(4):
        if not public_url(current):
            raise ValueError('Non-public source URL')
        parts = urlsplit(current)
        address = resolve_public(parts.hostname)
        connection = http.client.HTTPSConnection(parts.hostname, timeout=timeout, context=ssl.create_default_context())
        # HTTPSConnection still verifies server_hostname=self.host; no second DNS lookup.
        connection._create_connection = lambda target, delay, source=None: socket.create_connection((address, 443), delay)
        try:
            path = parts.path or '/'
            if parts.query:
                path += '?' + parts.query
            connection.request('GET', path, headers={'Accept-Encoding': 'identity', 'User-Agent': 'Model-Intelligence-Public-Evidence/1.0'})
            response = connection.getresponse()
            history.append(current)
            if response.status in {301, 302, 303, 307, 308}:
                location = response.getheader('Location')
                if not location:
                    raise ValueError('Redirect lacks destination')
                current = urljoin(current, location)
                continue
            if response.status != 200:
                raise ValueError('Source HTTP retrieval failed')
            if response.getheader('Content-Encoding', 'identity').lower() != 'identity':
                raise ValueError('Unsupported compressed source body')
            length = response.getheader('Content-Length')
            if length and (not length.isdigit() or int(length) > limit):
                raise ValueError('Source exceeds body limit')
            raw = response.read(limit + 1)
            if len(raw) > limit or length and len(raw) != int(length):
                raise ValueError('Oversize or incomplete source body')
            return raw, response.getheader('Content-Type', ''), current, history
        finally:
            connection.close()
    raise ValueError('Source redirect limit exceeded')


def inspect_source(source, *, fetch=get_public):
    captured = datetime.now(timezone.utc).isoformat()
    result = {'source_id': source['id'], 'url': source['url'], 'captured_at': captured,
              'status': 'unavailable', 'failure': None, 'body_sha256': None,
              'text_sha256': None, 'content_type': None, 'final_url': None, 'redirects': [], 'text': None}
    raw = None
    try:
        if not public_url(source['url']):
            raise ValueError('Non-public source URL')
        raw, content_type, final, redirects = fetch(source['url'])
        if len(raw) > MAX_BODY or not all(public_url(url) for url in [final, *redirects]):
            raise ValueError('Unsafe source response')
        result.update(body_sha256=sha256(raw).hexdigest(), content_type=content_type, final_url=final, redirects=redirects)
        text = text_body(raw, content_type)
        result.update(status='available', text=text, text_sha256=sha256(text.encode()).hexdigest())
    except (ValueError, OSError, http.client.HTTPException, UnicodeError):
        # No exception payload: may contain proxy settings, private addresses or headers.
        result['failure'] = 'Source retrieval or text extraction unavailable; not verified'
    return result, raw


def inspect_source_process(source, *, timeout=20):
    """Bound DNS, redirects, slow bodies and extraction by a worker wall-clock limit."""
    source = {'id': source['id'], 'url': source['url']}
    try:
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker'],
                                input=json.dumps(source).encode(), capture_output=True,
                                timeout=timeout, cwd=Path(__file__).resolve().parents[1],
                                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        if result.returncode != 0 or len(result.stdout) > 8*MAX_BODY:
            raise ValueError('Source worker unavailable')
        from tools.research_intake import parse
        retained = parse(result.stdout)
        raw = base64.b64decode(retained['body'], validate=True) if retained['body'] is not None else None
        if raw is not None and len(raw) > MAX_BODY:
            raise ValueError('Worker body exceeds bound')
        return retained['inspection'], raw
    except (ValueError, OSError, subprocess.SubprocessError):
        def unavailable(_):
            raise ValueError('Source worker timed out or failed')
        return inspect_source(source, fetch=unavailable)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', action='store_true', required=True)
    parser.parse_args()
    from tools.research_intake import parse
    source = parse(sys.stdin.buffer.read(64*1024))
    inspection, raw = inspect_source(source)
    print(json.dumps({'inspection': inspection, 'body': base64.b64encode(raw).decode() if raw is not None else None}))
