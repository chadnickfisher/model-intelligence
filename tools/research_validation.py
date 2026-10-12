"""Portable validation receipts. Byte binding is not evidence or execution attestation."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

MAX_BYTES = 16 * 1024 * 1024
VERSION = 'research-validation-v1'
SEARCH_VERSION = 'research-validation-v2'
OUTPUT_VERSION = 'research-validation-v3'
SOURCE_VERSION = 'research-validation-v4'
REQUIRED = {'assignment.json', 'instructions.md', 'authoring-helper.py',
            'research_authoring.py', 'research_fields.py', 'research_validation.py', 'schemas.json'}


def pin(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def parse(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('Duplicate JSON key')
            out[key] = value
        return out
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda _: fail('Nonfinite JSON'))


def fail(message):
    raise ValueError(message)


def require(condition, message):
    if not condition:
        fail(message)


def receipt_binding(packet_raw, manifest_raw):
    packet, manifest = parse(packet_raw), parse(manifest_raw)
    search_enabled = 'search-receipts-contract.json' in manifest['files']
    records_enabled = 'output-contract.json' in manifest['files']
    source_enabled = 'source-bodies-contract.json' in manifest['files']
    return {'format': SOURCE_VERSION if source_enabled else OUTPUT_VERSION if records_enabled else SEARCH_VERSION if search_enabled else VERSION, 'assignment_id': manifest['assignment_id'],
            'baseline_commit': manifest['baseline_commit'], 'packet': pin(packet_raw),
            'kit_manifest': pin(manifest_raw),
            'kit_instructions': manifest['files']['instructions.md'],
            'helper_files': {name: value for name, value in manifest['files'].items() if name.endswith('.py')},
            'schema_bundle': manifest['files']['schemas.json'],
            'package_type': packet['package_type'],
            **({'search_contract': manifest['files']['search-receipts-contract.json']} if search_enabled else {}),
            **({'output_contract': manifest['files']['output-contract.json']} if records_enabled else {}),
            **({'source_contract': manifest['files']['source-bodies-contract.json']} if source_enabled else {})}


def verify_receipt(receipt, packet_raw, manifest_raw, expected_manifest_sha256, *, search_index_raw=None, search_audit_raw=None,
                   source_index_raw=None, source_audit_raw=None):
    """Check against an independently trusted manifest digest; never grant acceptance."""
    require(sha256(manifest_raw).hexdigest() == expected_manifest_sha256, 'Untrusted kit manifest')
    packet, manifest = parse(packet_raw), parse(manifest_raw)
    require(packet['assignment_id'] == manifest['assignment_id'] and
            packet['baseline_commit'] == manifest['baseline_commit'], 'Packet identity differs from kit')
    expected = {**receipt_binding(packet_raw, manifest_raw), 'status': 'structural_validation_passed',
                'checks': {'schema': 'passed', 'mechanical': 'passed'},
                'receiver_acceptance': 'not_evaluated', 'evidence_review': 'not_evaluated',
                'research_completeness': 'not_evaluated'}
    if 'search-receipts-contract.json' in manifest['files']:
        require(search_index_raw is not None and search_audit_raw is not None, 'Search index and audit bytes required for v2 binding')
        audit = parse(search_audit_raw)
        if __package__:
            from .research_search_receipts import CHECKS
        else:
            from research_search_receipts import CHECKS
        require(audit.get('status') == 'search_receipts_verified' and not audit.get('errors') and
                audit.get('checks') == {key: 'passed' for key in CHECKS} and
                audit.get('packet') == pin(packet_raw) and audit.get('index') == pin(search_index_raw) and
                audit.get('contract') == manifest['files']['search-receipts-contract.json'],
                'Search audit does not match verified packet/index/contract')
        expected['checks']['search_receipts'] = 'passed'
        expected['search_evidence'] = {'index': pin(search_index_raw), 'audit': pin(search_audit_raw)}
    if 'output-contract.json' in manifest['files']:
        expected['checks']['records'] = 'passed'
    if 'source-bodies-contract.json' in manifest['files']:
        require(source_index_raw is not None and source_audit_raw is not None,'Source index and audit bytes required for v4 binding')
        if __package__:
            from .research_source_bodies import CHECKS as SOURCE_CHECKS, LIMITS
        else:
            from research_source_bodies import CHECKS as SOURCE_CHECKS, LIMITS
        source_audit=parse(source_audit_raw)
        require(source_audit.get('status')=='source_bodies_verified' and not source_audit.get('errors') and
                source_audit.get('checks')=={key:'passed' for key in SOURCE_CHECKS} and
                source_audit.get('limits')==LIMITS and source_audit.get('packet')==pin(packet_raw) and
                source_audit.get('index')==pin(source_index_raw) and
                source_audit.get('baseline')==manifest['files']['baseline-records.json'] and
                source_audit.get('contract')==manifest['files']['source-bodies-contract.json'],
                'Source audit does not match exact packet/index/baseline/contract')
        expected['checks']['source_bodies']='passed'
        expected['source_evidence']={'index':pin(source_index_raw),'audit':pin(source_audit_raw)}
    require(receipt == expected, 'Receipt does not match exact packet, kit, or required checks')
    return {'status': 'receipt_binding_verified', 'packet': expected['packet'],
            'receiver_acceptance': 'not_evaluated', 'evidence_review': 'not_evaluated'}


class Session:
    def __init__(self, kit, args):
        self.kit = Path(kit).resolve()
        self.args = args
        self.checks = {'schema': 'not_run', 'mechanical': 'not_run'}
        self.manifest_raw = (self.kit / 'input-manifest.json').read_bytes()
        self.manifest = parse(self.manifest_raw)
        require(REQUIRED <= self.manifest['files'].keys(), 'Incomplete validation kit')
        self.inputs = {}
        for name, expected in self.manifest['files'].items():
            require(Path(name).name == name and name not in {'.', '..'} and '/' not in name and '\\' not in name,
                    'Invalid kit member name')
            path = self.kit / name
            require(not path.is_symlink(), 'Linked kit member')
            raw = path.read_bytes()
            require(pin(raw) == expected, 'Frozen kit input changed: ' + name)
            self.inputs[name] = raw
        self.search_enabled = 'search-receipts-contract.json' in self.inputs
        if self.search_enabled:
            require('research_search_receipts.py' in self.inputs, 'Search receipt helper missing from frozen kit')
            self.checks['search_receipts'] = 'not_run'
        self.records_enabled = 'output-contract.json' in self.inputs
        self.source_enabled = 'source-bodies-contract.json' in self.inputs
        if self.source_enabled:
            require(self.records_enabled and {'research_source_bodies.py','baseline-records.json'} <= self.inputs.keys(),
                    'Incomplete source-body contract kit')
            self.checks['source_bodies']='not_run'
        self.record_errors = []
        if self.records_enabled:
            require(self.search_enabled and {'research_output_contract.py','output-contract.md'} <= self.inputs.keys(),
                    'Incomplete output contract kit')
            self.checks['records'] = 'not_run'
        require(not args.packet.is_symlink(), 'Linked packet refused')
        self.path = args.packet.resolve()
        protected = {self.kit / name for name in self.inputs} | {self.kit / 'input-manifest.json'}
        require(self.path not in protected, 'Copy the template to a separate packet file before authoring')
        require(self.path.is_file() and not self.path.is_symlink(), 'Packet must be an existing regular file')
        require(0 < self.path.stat().st_size <= MAX_BYTES, 'Packet exceeds size bound or is empty')
        self.raw = self.path.read_bytes()
        self.packet = parse(self.raw)
        require(self.packet['assignment_id'] == self.manifest['assignment_id'] and
                self.packet['baseline_commit'] == self.manifest['baseline_commit'], 'Wrong assignment or baseline')
        if args.receipt:
            require(args.receipt.resolve() not in protected | {self.path}, 'Receipt would replace an input')

    def load(self, name):
        return parse(self.inputs[name])

    def schema(self, name):
        # Import failures are blocked validation, never successful partial validation.
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
        schemas = self.load('schemas.json')
        registry = Registry().with_resources((n, Resource.from_contents(s, default_specification=DRAFT202012))
                                            for n, s in schemas.items())
        Draft202012Validator(schemas[name], registry=registry, format_checker=FormatChecker()).validate(self.packet)
        self.checks['schema'] = 'passed'
        if self.records_enabled:
            self.records()

    def records(self):
        if __package__:
            from .research_output_contract import render_contract, validate_records
        else:
            from research_output_contract import render_contract, validate_records
        self.checks['records'] = 'failed'
        contract = self.load('output-contract.json')
        require(self.inputs['output-contract.md'] == render_contract(contract),
                'RC01: Human output guide differs from its pinned machine contract')
        self.record_errors = validate_records(self.packet,self.load('schemas.json'),contract)
        failed_ids=', '.join(sorted({e['check_id'] for e in self.record_errors}))
        require(not self.record_errors, failed_ids + ': Proposed records fail canonical schema validation')
        self.checks['records'] = 'passed'

    def unchanged(self):
        require(self.path.read_bytes() == self.raw, 'Packet changed during validation; rerun')
        require((self.kit / 'input-manifest.json').read_bytes() == self.manifest_raw, 'Kit manifest changed during validation')
        for name, raw in self.inputs.items():
            require((self.kit / name).read_bytes() == raw, 'Kit input changed during validation: ' + name)

    def finish(self):
        require(self.checks.get('schema') == self.checks.get('mechanical') == 'passed', 'Validation checks incomplete')
        if self.records_enabled:
            require(self.checks.get('records') == 'passed', 'RC03: Required record checks incomplete')
        search_evidence = None
        if self.search_enabled:
            index_path, audit_path = getattr(self.args, 'search_index', None), getattr(self.args, 'search_audit', None)
            require(index_path is not None and audit_path is not None, 'SR12: --search-index and --search-audit are required by this frozen kit')
            if __package__:
                from .research_search_receipts import audit, audit_attempt, read
            else:
                from research_search_receipts import audit, audit_attempt, read
            attempt = audit_attempt(self.path,audit_path)
            require(self.args.receipt is not None and self.args.receipt.name == attempt + '.validation.json' and
                    self.args.receipt.resolve().parent == self.path.parent,
                    'SR12: structural receipt must use the same deterministic validation attempt stem')
            contract_path = self.kit / 'search-receipts-contract.json'
            current = audit(self.path, index_path, parse(self.inputs['search-receipts-contract.json']), contract_path)
            audit_raw, index_raw = read(audit_path), read(index_path)
            require(current['status'] == 'search_receipts_verified' and parse(audit_raw) == current,
                    'SR12: Search evidence incomplete or saved audit differs; rerun search receipt validation')
            require(current['index'] == pin(index_raw) and current['packet'] == pin(self.raw),
                    'SR11: Search index/packet changed after search audit')
            self.checks['search_receipts'] = 'passed'
            search_evidence = {'index':pin(index_raw), 'audit':pin(audit_raw)}
        source_evidence=None
        if self.source_enabled:
            source_index_path=getattr(self.args,'source_index',None);source_audit_path=getattr(self.args,'source_audit',None)
            require(source_index_path is not None and source_audit_path is not None,'SB11: source index and audit required by this kit')
            if __package__:
                from .research_source_bodies import audit as source_audit, audit_attempt as source_attempt, read as source_read
            else:
                from research_source_bodies import audit as source_audit, audit_attempt as source_attempt, read as source_read
            source_stem=source_attempt(self.path,source_audit_path)
            require(self.args.receipt is not None and self.args.receipt.name==source_stem+'.validation.json' and
                    self.args.receipt.resolve().parent==self.path.parent,'SB11: source audit and receipt attempt must match')
            current_sources=source_audit(self.path,source_index_path,self.kit/'baseline-records.json',
                parse(self.inputs['source-bodies-contract.json']),self.kit/'source-bodies-contract.json')
            source_audit_raw,source_index_raw=source_read(source_audit_path),source_read(source_index_path)
            require(current_sources['status']=='source_bodies_verified' and parse(source_audit_raw)==current_sources,
                    'SB11: source capture incomplete or saved audit differs')
            require(current_sources['index']==pin(source_index_raw) and current_sources['packet']==pin(self.raw),
                    'SB11: source evidence changed after audit')
            self.checks['source_bodies']='passed'
            source_evidence={'index':pin(source_index_raw),'audit':pin(source_audit_raw)}
        self.unchanged()
        receipt = {**receipt_binding(self.raw, self.manifest_raw), 'status': 'structural_validation_passed',
                   'checks': dict(self.checks), 'receiver_acceptance': 'not_evaluated',
                   'evidence_review': 'not_evaluated', 'research_completeness': 'not_evaluated'}
        if search_evidence is not None:
            receipt['search_evidence'] = search_evidence
            require(read(index_path) == index_raw and read(audit_path) == audit_raw, 'Search index/audit changed during validation')
            require(all(pin(read(index_path.parent / name)) == value for name,value in current['responses'].items()),
                    'SR11: Search response changed before receipt creation')
        if source_evidence is not None:
            receipt['source_evidence']=source_evidence
            require(source_read(source_index_path)==source_index_raw and source_read(source_audit_path)==source_audit_raw,
                    'SB11: Source index/audit changed during validation')
            require(all(pin(source_read(source_index_path.parent/name))==value for name,value in current_sources['responses'].items()),
                    'SB06: source response changed before receipt creation')
        if self.args.receipt:
            with self.args.receipt.open('x', encoding='utf-8') as output:
                output.write(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
        return receipt

    def extend(self, packet):
        self.unchanged()
        output = self.path.with_name(self.path.stem + '-extended.json')
        require(output not in {self.kit / name for name in self.inputs}, 'Extension would replace a kit input')
        with output.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(packet, ensure_ascii=False, indent=2) + '\n')
        return {'status': 'pending_fields_extended', 'output': output.name,
                'validation': 'not_performed', 'research_completeness': 'not_evaluated'}


def run_authoring(kit, callback):
    parser = argparse.ArgumentParser(description='Validate exact packet bytes or extend pending field accounting.')
    parser.add_argument('packet', type=Path)
    parser.add_argument('--extend', action='store_true')
    parser.add_argument('--receipt', type=Path, help='Create a new private validation receipt; never overwrite.')
    parser.add_argument('--search-index', type=Path, help='Private search evidence index required by v2 kits.')
    parser.add_argument('--search-audit', type=Path, help='Exact saved successful search receipt audit required by v2 kits.')
    parser.add_argument('--source-index',type=Path,help='Opened-source capture index required by v4 kits.')
    parser.add_argument('--source-audit',type=Path,help='Exact successful source-body audit required by v4 kits.')
    args = parser.parse_args()
    if args.extend and args.receipt:
        parser.error('--extend does not validate and cannot issue a validation receipt')
    session = None
    try:
        session = Session(kit, args)
        result = callback(session)
    except Exception as exc:
        # Details stay local; no failed path can print a success receipt.
        blocked = isinstance(exc, ImportError)
        result = {'status': 'validation_blocked' if blocked else 'validation_failed',
                  'checks': dict(session.checks) if session else {'schema': 'not_run', 'mechanical': 'not_run'},
                  'error_type': type(exc).__name__,
                  'reason': 'Required schema validation dependencies unavailable' if blocked else str(exc)[:1000],
                  'receiver_acceptance': 'not_evaluated', 'evidence_review': 'not_evaluated'}
        if session and session.record_errors:
            result['record_errors'] = session.record_errors
        print(json.dumps(result, ensure_ascii=False))
        return 2 if blocked else 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


def main():
    parser = argparse.ArgumentParser(description='Verify a receipt binding; this never substitutes for local receiver/evidence review.')
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--kit-manifest', type=Path, required=True)
    parser.add_argument('--expected-manifest-sha256', required=True)
    parser.add_argument('--search-index', type=Path)
    parser.add_argument('--search-audit', type=Path)
    parser.add_argument('--source-index',type=Path)
    parser.add_argument('--source-audit',type=Path)
    args = parser.parse_args()
    try:
        result = verify_receipt(parse(args.receipt.read_bytes()), args.packet.read_bytes(),
                                args.kit_manifest.read_bytes(), args.expected_manifest_sha256,
                                search_index_raw=args.search_index.read_bytes() if args.search_index else None,
                                search_audit_raw=args.search_audit.read_bytes() if args.search_audit else None,
                                source_index_raw=args.source_index.read_bytes() if args.source_index else None,
                                source_audit_raw=args.source_audit.read_bytes() if args.source_audit else None)
    except Exception as exc:
        print(json.dumps({'status': 'receipt_binding_failed', 'reason': str(exc)}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
