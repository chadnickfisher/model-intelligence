from tools.git_baselines import legacy_revisions as history
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
import shutil
import subprocess
import sys
import pytest
from tools.knowledge import ROOT, canonical, read, scope_errors, capture
from tools.migrate_v2 import write_yaml


def test_all_original_conclusions_and_evidence_survive():
    originals = read(ROOT / 'history/migrations/2026-10-07-capabilities.yaml')['records']
    current = canonical()
    revisions = history()
    assert len([r for r in originals if r['original_collection'] == 'capabilities']) == 64
    assert len(originals) == 71
    for row in originals:
        # Preservation belongs to the migration event. Later inspected evidence
        # can revise confidence while the original value remains in history.
        model = next(r['value'] for r in revisions
                     if r['entity_type'] == 'model' and r['entity_id'] == row['model_id']
                     and r['value'] and any(j['id'] == row['judgment_id']
                         for j in r['value']['capabilities'] + r['value']['performance_characteristics']))
        claim = next(j for j in model['capabilities'] + model['performance_characteristics'] if j['id'] == row['judgment_id'])
        live = current[('model', row['model_id'])][1]
        assert any(j['id'] == row['judgment_id'] for j in live['capabilities'] + live['performance_characteristics'])
        for field, value in row['original'].items():
            assert (claim['provenance']['original_task'] if field == 'task' else claim[field]) == value
    scopes = [r['classification'] for r in originals if r['original_collection'] == 'capabilities']
    assert {s: scopes.count(s) for s in set(scopes)} == {'direct': 19, 'compound': 34, 'unresolved': 5, 'performance': 6}


def test_index_retains_actual_claim_and_never_splits_bundle():
    indexed = read(ROOT / 'data/capabilities.yaml')['records']
    migrated = [j for j in indexed if j['provenance'].get('origin') != 'research']
    assert len(migrated) == 58
    assert len({j['id'] for j in indexed}) == len(indexed)
    current = canonical()
    for j in indexed:
        model = current[('model', j['model_id'])][1]
        assert {k: v for k, v in j.items() if k not in ['model_id', 'profile']} == next(c for c in model['capabilities'] if c['id'] == j['id'])
        if j['scope'] in ['compound', 'unresolved']:
            assert j['task_ids'] == []
        assert 'judgment' in j and 'known_failure_modes' in j and 'contradictory_evidence_ids' in j


def copied_repo(tmp_path):
    root = tmp_path / 'repo'
    subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(root)],check=True,capture_output=True)
    shutil.copytree(ROOT, root, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
    return root


def test_unknown_task_rejected_by_validator_and_renderer(tmp_path):
    root = copied_repo(tmp_path)
    path = next(root.glob('models/*/*/profile.yaml'))
    model = read(path)
    model['capabilities'][0]['related_task_ids'].append('invented.leaderboard')
    write_yaml(path, model)
    before = (root / 'data/capability-taxonomy.yaml').read_bytes()
    for tool in ['validate.py', 'render.py']:
        r = subprocess.run([sys.executable, str(root / 'tools' / tool)], capture_output=True, text=True, encoding='utf-8')
        assert r.returncode != 0
        assert 'unknown task invented.leaderboard' in r.stdout + r.stderr
    assert (root / 'data/capability-taxonomy.yaml').read_bytes() == before


def test_no_autoregistration_and_reproducible_views():
    def digest():
        return {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*')
                if p.is_file() and (p.name == 'README.md' or p.parent.name == 'data' or p.name == 'coverage.md')}
    before = digest()
    taxonomy = (ROOT / 'data/capability-taxonomy.yaml').read_bytes()
    rendered=subprocess.run([sys.executable, str(ROOT / 'tools/render.py')], capture_output=True, text=True, encoding='utf-8')
    assert rendered.returncode==0, rendered.stdout+rendered.stderr
    assert digest() == before
    assert (ROOT / 'data/capability-taxonomy.yaml').read_bytes() == taxonomy


def test_full_validation():
    result = subprocess.run([sys.executable, str(ROOT / 'tools/validate.py')], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
