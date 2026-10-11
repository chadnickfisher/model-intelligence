"""Portable validation receipts. Byte binding is not evidence or execution attestation."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

MAX_BYTES = 16 * 1024 * 1024
VERSION = 'research-validation-v1'
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
    return {'format': VERSION, 'assignment_id': manifest['assignment_id'],
            'baseline_commit': manifest['baseline_commit'], 'packet': pin(packet_raw),
            'kit_manifest': pin(manifest_raw),
            'kit_instructions': manifest['files']['instructions.md'],
            'helper_files': {name: value for name, value in manifest['files'].items() if name.endswith('.py')},
            'schema_bundle': manifest['files']['schemas.json'],
            'package_type': packet['package_type']}


def verify_receipt(receipt, packet_raw, manifest_raw, expected_manifest_sha256):
    """Check against an independently trusted manifest digest; never grant acceptance."""
    require(sha256(manifest_raw).hexdigest() == expected_manifest_sha256, 'Untrusted kit manifest')
    packet, manifest = parse(packet_raw), parse(manifest_raw)
    require(packet['assignment_id'] == manifest['assignment_id'] and
            packet['baseline_commit'] == manifest['baseline_commit'], 'Packet identity differs from kit')
    expected = {**receipt_binding(packet_raw, manifest_raw), 'status': 'structural_validation_passed',
                'checks': {'schema': 'passed', 'mechanical': 'passed'},
                'receiver_acceptance': 'not_evaluated', 'evidence_review': 'not_evaluated',
                'research_completeness': 'not_evaluated'}
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

    def unchanged(self):
        require(self.path.read_bytes() == self.raw, 'Packet changed during validation; rerun')
        require((self.kit / 'input-manifest.json').read_bytes() == self.manifest_raw, 'Kit manifest changed during validation')
        for name, raw in self.inputs.items():
            require((self.kit / name).read_bytes() == raw, 'Kit input changed during validation: ' + name)

    def finish(self):
        require(self.checks == {'schema': 'passed', 'mechanical': 'passed'}, 'Validation checks incomplete')
        self.unchanged()
        receipt = {**receipt_binding(self.raw, self.manifest_raw), 'status': 'structural_validation_passed',
                   'checks': dict(self.checks), 'receiver_acceptance': 'not_evaluated',
                   'evidence_review': 'not_evaluated', 'research_completeness': 'not_evaluated'}
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
    args = parser.parse_args()
    try:
        result = verify_receipt(parse(args.receipt.read_bytes()), args.packet.read_bytes(),
                                args.kit_manifest.read_bytes(), args.expected_manifest_sha256)
    except Exception as exc:
        print(json.dumps({'status': 'receipt_binding_failed', 'reason': str(exc)}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
