"""Portable private search receipts. Saved bytes cannot attest tool execution."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys

VERSION = 'research-search-receipts-v1'
MAX_BYTES = 16 * 1024 * 1024
MAX_CALLS = 1000
SEARCH_KEYS = {'query', 'checked_at', 'outcome', 'urls', 'notes'}
CALL_KEYS = {'id', 'tool', 'started_at', 'completed_at', 'request', 'queries',
             'capture_status', 'response', 'capture_error'}
CHECKS = {
    'SR01': 'Save index.json with format, assignment_id, baseline_commit and calls; match the packet identity.',
    'SR02': 'Save calls as a JSON array with unique sequential IDs search-000001 through search-001000.',
    'SR03': 'For each call save id, tool, started_at, completed_at, request, queries, capture_status, response and capture_error.',
    'SR04': 'Save UTC call timestamps ending in Z; require started_at <= completed_at <= packet.created_at <= validation UTC time.',
    'SR05': 'Save every query in queries using exactly query, checked_at, outcome, urls and notes; use the packet search-reference vocabulary.',
    'SR06': 'For saved capture copy the complete tool-visible JSON response to responses/<call-id>.json; response metadata must name this exact file.',
    'SR07': 'Save the response file byte count and SHA-256 after readback; preserve those exact bytes.',
    'SR08': 'Save an exact matching query entry for every packet search_references entry, including discovery and resolution searches.',
    'SR09': 'For failed capture save capture_status=capture_failed, response=null and a nonempty capture_error; this fails receipt completeness.',
    'SR10': 'Use <stem>.search-evidence as the evidence directory; keep only index.json and indexed response files inside it.',
    'SR11': 'Keep the packet, index and saved responses unchanged during validation; edits require a fresh audit.',
    'SR12': 'Save <stem>.v<attempt>.search-validation.json with packet/index/response/contract hashes and every SR check result; do not author a success report.',
}


def contract():
    return {'format': VERSION, 'index_filename': 'index.json',
            'response_filename': 'responses/<call-id>.json',
            'audit_filename': '<stem>.v<attempt>.search-validation.json',
            'structural_receipt_filename': '<stem>.v<attempt>.validation.json',
            'call_fields': sorted(CALL_KEYS), 'query_fields': sorted(SEARCH_KEYS),
            'checks': CHECKS,
            'verified_status': 'search_receipts_verified',
            'limits': 'Verifies saved bytes and accounting links, not tool execution, factual correctness, source inspection, research completeness or receiver acceptance.'}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def pin(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError('Nonfinite JSON value')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=nonfinite)


def regular(path):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or (hasattr(ancestor, 'is_junction') and ancestor.is_junction()):
            raise ValueError('Linked evidence path refused')
    return path


def read(path):
    path = regular(path)
    if not path.is_file() or not 0 < path.stat().st_size <= MAX_BYTES:
        raise ValueError('Missing, empty or oversized artifact')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Oversized artifact')
    return raw


def write_new(path, raw):
    path = regular(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)


def instant(value, utc=False):
    if not isinstance(value, str) or (utc and not value.endswith('Z')):
        raise ValueError('Timestamp must include timezone; call timestamps require UTC Z')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp lacks timezone')
    return result


def query_key(row):
    if not isinstance(row, dict) or set(row) != SEARCH_KEYS:
        raise ValueError('Search entry fields differ from the contract')
    if not isinstance(row['query'], str) or not row['query'].strip():
        raise ValueError('Missing actual query')
    if not isinstance(row['checked_at'], str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['checked_at']):
        raise ValueError('Invalid search date')
    datetime.strptime(row['checked_at'], '%Y-%m-%d')
    if row['outcome'] not in {'sources_located', 'no_matched_sources', 'blocked'}:
        raise ValueError('Invalid search outcome')
    if not isinstance(row['urls'], list) or not all(isinstance(x, str) for x in row['urls']):
        raise ValueError('Invalid returned URL list')
    if not isinstance(row['notes'], str):
        raise ValueError('Invalid search notes')
    # The ledger uses a byte-stable signature. Repeated references may share a receipt.
    return sha256(encoded(row)).hexdigest()


def searches(value, path=''):
    if isinstance(value, dict):
        for key, nested in value.items():
            child = path + '/' + key.replace('~', '~0').replace('/', '~1')
            if key == 'search_references':
                if not isinstance(nested, list):
                    raise ValueError('Search references must be an array')
                for i, row in enumerate(nested):
                    yield child + '/' + str(i), row
            else:
                yield from searches(nested, child)
    elif isinstance(value, list):
        for i, nested in enumerate(value):
            yield from searches(nested, path + '/' + str(i))


def packet_searches(packet):
    """Current accounting only; carried-forward canonical records are not new searches."""
    if 'research_run' in packet and 'scope_run' in packet:
        raise ValueError('Packet contains both research run types')
    name = 'scope_run' if 'scope_run' in packet else 'research_run'
    yield from searches(packet.get(name, {}), '/' + name)
    for name in ('discovery_checks', 'resolutions'):
        yield from searches(packet.get(name, []), '/' + name)


def audit_attempt(packet_path, report_path):
    if Path(packet_path).absolute().parent != Path(report_path).absolute().parent:
        raise ValueError('SR12: audit report must be beside the packet')
    prefix = Path(packet_path).stem + '.v'
    name = Path(report_path).name
    if not name.startswith(prefix):
        raise ValueError('SR12: audit report stem differs from packet')
    suffix = name[len(prefix):]
    if not re.fullmatch(r'[0-9]{6}\.search-validation\.json', suffix) or suffix.startswith('000000'):
        raise ValueError('SR12: validation attempt must be six digits starting at 000001')
    return prefix + suffix[:6]


def audit(packet_path, index_path, expected_contract, contract_path=None):
    packet_raw, index_raw = read(packet_path), read(index_path)
    packet, index = parse(packet_raw), parse(index_raw)
    contract_raw = read(contract_path) if contract_path else encoded(expected_contract)
    root = regular(index_path).parent
    checks = {key: 'passed' for key in CHECKS}
    errors, links, response_pins, captured = [], [], {}, {}
    def reject(code, message):
        checks[code] = 'failed'
        errors.append({'check_id': code, 'message': message})
    if expected_contract != contract():
        reject('SR12', 'Pinned search receipt contract differs from this helper')
    if not isinstance(index, dict) or set(index) != {'format', 'assignment_id', 'baseline_commit', 'calls'} or \
       index.get('format') != VERSION or any(index.get(k) != packet.get(k) for k in ('assignment_id', 'baseline_commit')):
        reject('SR01', 'Index shape, version or assignment/baseline differs')
    calls = index.get('calls', []) if isinstance(index, dict) else []
    if not isinstance(calls, list) or len(calls) > MAX_CALLS:
        reject('SR02', 'Calls must be a bounded array')
        calls = []
    expected_files = {'index.json'}
    if Path(index_path).name != 'index.json':
        reject('SR01', 'Index must be named index.json')
    if root.name != Path(packet_path).stem + '.search-evidence':
        reject('SR10', 'Evidence directory stem differs from packet')
    try:
        created = instant(packet['created_at'])
    except (KeyError, ValueError, TypeError):
        reject('SR04', 'Packet serialization timestamp is invalid')
        created = datetime.min.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    for n, call in enumerate(calls, 1):
        ident = 'search-' + str(n).zfill(6)
        if not isinstance(call, dict) or set(call) != CALL_KEYS:
            reject('SR03', ident + ': call fields differ'); continue
        if call['id'] != ident:
            reject('SR02', ident + ': IDs must be unique and sequential'); continue
        if not isinstance(call['tool'], str) or not call['tool'].strip() or not isinstance(call['request'], dict) or not call['request']:
            reject('SR03', ident + ': tool and full public request object are required')
        try:
            start, end = instant(call['started_at'], True), instant(call['completed_at'], True)
            if not start <= end <= created <= now:
                raise ValueError('Call/packet timestamps out of order')
        except (TypeError, ValueError):
            reject('SR04', ident + ': timestamps invalid, future or out of order')
        query_keys = []
        if not isinstance(call['queries'], list) or not call['queries']:
            reject('SR05', ident + ': queries must be a nonempty array')
        else:
            for row in call['queries']:
                try: query_keys.append(query_key(row))
                except (TypeError, ValueError): reject('SR05', ident + ': invalid query entry')
        if call['capture_status'] == 'capture_failed':
            if call['response'] is not None or not isinstance(call['capture_error'], str) or not call['capture_error'].strip():
                reject('SR06', ident + ': failed capture needs null response and its actual error')
            reject('SR09', ident + ': capture failed; original result payload is missing')
            continue
        if call['capture_status'] != 'saved' or call['capture_error'] is not None:
            reject('SR06', ident + ': invalid capture status/error'); continue
        response = call['response']; filename = 'responses/' + ident + '.json'
        if not isinstance(response, dict) or set(response) != {'path', 'bytes', 'sha256'} or response.get('path') != filename:
            reject('SR06', ident + ': response fields/path differ'); continue
        expected_files.add(filename)
        try:
            raw = read(root / filename)
            if parse(raw) is None:
                raise ValueError('Null payload cannot represent a complete response')
        except (ValueError, OSError, TypeError):
            reject('SR06', ident + ': complete JSON response is unavailable'); continue
        actual = pin(raw); response_pins[filename] = actual
        if type(response['bytes']) is not int or {k:response[k] for k in ('bytes','sha256')} != actual:
            reject('SR07', ident + ': response readback bytes/digest differ'); continue
        for key in query_keys: captured.setdefault(key, []).append(ident)
    try:
        for pointer, row in packet_searches(packet):
            key = query_key(row)
            matches = captured.get(key, [])
            if not matches: reject('SR08', pointer + ': no exact saved query/response receipt')
            links.append({'packet_pointer':pointer, 'call_ids':matches})
    except (ValueError, TypeError): reject('SR08', 'Invalid packet search reference')
    try:
        inventory = set()
        for item in root.iterdir():
            regular(item)
            if item.name == 'responses' and item.is_dir():
                for response_file in item.iterdir():
                    regular(response_file)
                    if not response_file.is_file(): raise ValueError('Unexpected evidence subdirectory')
                    inventory.add('responses/' + response_file.name)
            elif item.is_file(): inventory.add(item.name)
            else: raise ValueError('Unexpected evidence directory')
        if inventory != expected_files: raise ValueError('Evidence inventory differs')
    except (OSError, ValueError): reject('SR10', 'Evidence directory inventory differs from the indexed files')
    try:
        if read(packet_path) != packet_raw or read(index_path) != index_raw or (contract_path and read(contract_path) != contract_raw) or \
           any(pin(read(root / filename)) != value for filename,value in response_pins.items()):
            raise ValueError('Inputs changed')
    except (OSError, ValueError): reject('SR11', 'Input changed or disappeared during audit')
    return {'format':VERSION, 'status':'search_receipts_verified' if not errors else 'search_receipts_incomplete',
            'assignment_id':packet.get('assignment_id'), 'baseline_commit':packet.get('baseline_commit'),
            'packet':pin(packet_raw), 'index':pin(index_raw), 'contract':pin(contract_raw),
            'responses':response_pins, 'checks':checks, 'errors':errors, 'links':links,
            'execution_attestation':'not_evaluated', 'receiver_acceptance':'not_evaluated',
            'evidence_review':'not_evaluated', 'research_completeness':'not_evaluated'}


def initialize(packet_path, index_path):
    packet = parse(read(packet_path))
    if Path(index_path).name != 'index.json' or Path(index_path).parent.name != Path(packet_path).stem + '.search-evidence':
        raise ValueError('SR01/SR10: index and evidence directory names differ from the contract')
    write_new(index_path, encoded({'format':VERSION,'assignment_id':packet['assignment_id'],
                                  'baseline_commit':packet['baseline_commit'],'calls':[]}))


def capture(index_path, request_path, queries_path, response_path, tool, started_at, completed_at):
    index_raw = read(index_path); index = parse(index_raw)
    if index.get('format') != VERSION or not isinstance(index.get('calls'), list) or len(index['calls']) >= MAX_CALLS:
        raise ValueError('Invalid index or call bound exceeded')
    request, queries = parse(read(request_path)), parse(read(queries_path))
    if not isinstance(request, dict) or not request or not isinstance(queries, list) or not queries:
        raise ValueError('Actual request and query entries are required')
    for row in queries: query_key(row)
    if not isinstance(tool,str) or not tool.strip(): raise ValueError('Missing actual tool name')
    if not instant(started_at,True) <= instant(completed_at,True) <= datetime.now(timezone.utc):
        raise ValueError('Invalid call timestamps')
    ident = 'search-' + str(len(index['calls']) + 1).zfill(6)
    call = {'id':ident,'tool':tool,'started_at':started_at,'completed_at':completed_at,
            'request':request,'queries':queries,'capture_status':'capture_failed','response':None,'capture_error':None}
    root = regular(index_path).parent
    response_name = 'responses/' + ident + '.json'
    try:
        raw = read(response_path)
        if parse(raw) is None: raise ValueError('Null response payload')
        write_new(root / response_name, raw)
        if read(root / response_name) != raw: raise ValueError('Response readback differs')
        call.update(capture_status='saved',response={'path':response_name,**pin(raw)},capture_error=None)
    except (ValueError, OSError) as exc:
        call['capture_error'] = type(exc).__name__ + ': ' + str(exc)
    # A crashed save can leave a response file but no index update: the audit fails SR10.
    index['calls'].append(call)
    if read(index_path) != index_raw: raise ValueError('Index changed during capture')
    temporary = regular(Path(index_path).with_name('index.json.part'))
    write_new(temporary, encoded(index))
    os.replace(temporary, regular(index_path))
    return call


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    init = sub.add_parser('init'); init.add_argument('--packet',type=Path,required=True); init.add_argument('--index',type=Path,required=True)
    cap = sub.add_parser('capture')
    for name in ('index','request','queries','response'): cap.add_argument('--'+name,type=Path,required=True)
    for name in ('tool','started-at','completed-at'): cap.add_argument('--'+name,required=True)
    check = sub.add_parser('check')
    for name in ('packet','index','contract','report'): check.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    if args.mode == 'init': initialize(args.packet,args.index); result={'status':'search_index_initialized'}
    elif args.mode == 'capture':
        result=capture(args.index,args.request,args.queries,args.response,args.tool,args.started_at,args.completed_at)
    else:
        audit_attempt(args.packet,args.report)
        if regular(args.report).is_relative_to(regular(args.index).parent):
            raise ValueError('Audit report must be outside the evidence directory')
        if regular(args.report) in {regular(args.packet),regular(args.contract)}:
            raise ValueError('Audit report cannot replace an input')
        result=audit(args.packet,args.index,parse(read(args.contract)),args.contract)
        write_new(args.report,encoded(result))
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0 if result.get('status') in {'search_index_initialized','search_receipts_verified'} or result.get('capture_status')=='saved' else 1


if __name__ == '__main__':
    try: sys.exit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'search_receipt_operation_failed','error_type':type(exc).__name__}),file=sys.stderr)
        sys.exit(1)
