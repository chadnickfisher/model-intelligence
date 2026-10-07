import json
import subprocess

import pytest

from tools.package_workflow import REPOSITORY, digest, ready_update
from tools.public_boundary import private_work_path, public_files, tracked_work_paths


@pytest.mark.parametrize('path', [
    'AGENTS.md', 'nested/AGENTS.override.md', '.agents/skills/update/SKILL.md',
    'CURRENT_STATE.md', 'ARCHITECTURE.md', 'plans/active.md',
    'decisions/0001-working-process.md', '.local/research/receipt.yaml',
    'docs/working/handoff.md', 'docs/package-workflow.md', 'MAINTENANCE.md',
    'data/.codex/session.json',
])
def test_private_working_paths_are_reserved(path):
    assert private_work_path(path)
    assert private_work_path(path.upper())


def test_public_application_and_evidence_remain_available():
    for path in ['streamlit_app.py', 'data/pricing.yaml', 'methodology.md',
                 'tools/validate.py', 'tests/test_cost.py', 'docs/change-tracking.md']:
        assert not private_work_path(path)


def test_public_export_does_not_read_local_instructions(tmp_path):
    (tmp_path / 'AGENTS.md').write_text('[Private link](absent.md)', encoding='utf-8')
    local = tmp_path / '.local'
    local.mkdir()
    (local / 'notes.md').write_text('Private work', encoding='utf-8')
    (tmp_path / 'README.md').write_text('Public product', encoding='utf-8')
    assert [path.name for path in public_files(tmp_path)] == ['README.md']
    assert tracked_work_paths(tmp_path) == []


def test_force_added_private_file_is_detected_in_git_index(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / '.gitignore').write_text('AGENTS.md\n', encoding='utf-8')
    (tmp_path / 'AGENTS.md').write_text('Local instructions', encoding='utf-8')
    subprocess.run(['git', '-C', str(tmp_path), 'add', '-f', 'AGENTS.md'], check=True)
    assert tracked_work_paths(tmp_path) == ['AGENTS.md']


@pytest.mark.parametrize('path', ['MAINTENANCE.md', 'models/example/AGENTS.md',
                                'research/decisions/private.json'])
def test_update_packages_cannot_republish_working_material(path):
    payload = b'private working material'
    manifest = {'package_type': 'ready-update', 'repository': REPOSITORY,
                'branch': 'main', 'base_commit': 'a' * 40,
                'files': [{'path': path, 'operation': 'write',
                           'previous_sha256': None, 'sha256': digest(payload)}]}
    with pytest.raises(ValueError, match='allowlist'):
        ready_update({'package.json': json.dumps(manifest).encode(),
                      'payload/' + path: payload}, [path])
