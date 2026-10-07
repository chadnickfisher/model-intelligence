"""The published product works without local development/research archives."""
from pathlib import Path
import shutil
import subprocess
import sys
from tools.knowledge import ROOT


def test_product_validation_needs_no_work_receipts_or_git_checkout(tmp_path):
    root = tmp_path / 'product'
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
        '.git', '.local', '.venv', '__pycache__', '.pytest_cache'))
    assert not (root / 'data/research-runs.yaml').exists()
    assert not (root / 'data/maintenance-passes.yaml').exists()
    local = root / '.local/research'
    local.mkdir(parents=True)
    (local / 'report.md').write_text('[Local work](missing-local-file.md)', encoding='utf-8')
    result = subprocess.run([sys.executable, str(root / 'tools/validate.py')],
        capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
