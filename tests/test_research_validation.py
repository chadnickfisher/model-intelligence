"""Byte binding does not grant receiver acceptance or evidence credit."""
from argparse import Namespace
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

from tools.research_validation import REQUIRED, Session, pin, verify_receipt


@pytest.fixture
def session(tmp_path):
    kit = tmp_path / 'kit'
    kit.mkdir()
    packet = {'assignment_id': 'fixture', 'baseline_commit': 'a' * 40, 'package_type': 'fixture'}
    for name in REQUIRED:
        (kit / name).write_text('{}', encoding='utf-8')
    (kit / 'schemas.json').write_text(json.dumps({'fixture': {'type': 'object', 'required': ['package_type']}}))
    manifest = {**packet, 'files': {name: pin((kit / name).read_bytes()) for name in REQUIRED}}
    (kit / 'input-manifest.json').write_text(json.dumps(manifest))
    path = tmp_path / 'packet.json'
    path.write_text(json.dumps(packet))
    return Session(kit, Namespace(packet=path, receipt=tmp_path / 'receipt.json', extend=False))


def passed(session):
    session.schema('fixture')
    session.checks['mechanical'] = 'passed'
    return session.finish()


def test_success_binds_bytes_without_granting_acceptance(session):
    receipt = passed(session)
    result = verify_receipt(receipt, session.raw, session.manifest_raw, sha256(session.manifest_raw).hexdigest())
    assert result['status'] == 'receipt_binding_verified'
    assert receipt['receiver_acceptance'] == receipt['evidence_review'] == receipt['research_completeness'] == 'not_evaluated'
    assert json.loads(session.args.receipt.read_text()) == receipt
    assert session.path.read_bytes() == session.raw


@pytest.mark.parametrize('change', ['packet', 'manifest', 'status', 'schema', 'mechanical', 'helper'])
def test_changed_bytes_or_claims_cannot_reuse_receipt(session, change):
    receipt = passed(session)
    packet, manifest = session.raw, session.manifest_raw
    if change == 'packet': packet += b'\n'
    elif change == 'manifest': manifest += b'\n'
    elif change == 'status': receipt['status'] = 'accepted'
    elif change == 'helper': receipt['helper_files']['authoring-helper.py']['sha256'] = '0' * 64
    else: receipt['checks'][change] = 'skipped'
    with pytest.raises(ValueError):
        verify_receipt(receipt, packet, manifest, sha256(session.manifest_raw).hexdigest())


@pytest.mark.parametrize('target', ['packet', 'kit', 'manifest'])
def test_changes_during_validation_prevent_receipt(session, target):
    path = session.path if target == 'packet' else session.kit / ('instructions.md' if target == 'kit' else 'input-manifest.json')
    path.write_bytes(path.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='changed during validation'):
        passed(session)
    assert not session.args.receipt.exists()


def test_unrun_checks_and_existing_receipts_are_never_accepted(session):
    with pytest.raises(ValueError, match='incomplete'):
        session.finish()
    session.args.receipt.write_bytes(b'preserve')
    with pytest.raises(FileExistsError):
        passed(session)
    assert session.args.receipt.read_bytes() == b'preserve'


def test_library_is_not_a_silent_successful_command(tmp_path):
    module = Path(__file__).resolve().parents[1] / 'tools/research_authoring.py'
    result = subprocess.run([sys.executable, '-B', str(module), str(tmp_path / 'absent.json')], capture_output=True, text=True)
    assert result.returncode == 2
    assert 'python authoring-helper.py' in result.stderr
    assert not result.stdout
