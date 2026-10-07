"""Keep local operating material outside the published product."""
from pathlib import Path, PurePosixPath
import os
import subprocess


PRIVATE_DIRECTORIES = {'.local', '.agents', '.codex', '.aws', 'plans', 'decisions'}
PRIVATE_DOCUMENTS = {
    'maintenance.md', 'current_state.md', 'architecture.md',
    'docs/bounded-research.md', 'docs/scoped-maintenance.md',
    'docs/package-workflow.md',
    'docs/maintenance-pilot-scope.md', 'docs/research_and_mcp_plan.md',
    'docs/research-work-unit-proposal.md', 'docs/retrieval-task-proposal.md',
    'data/research-runs.yaml', 'data/research-runs.md',
    'data/maintenance-passes.yaml', 'data/maintenance-passes.md',
    'history/revisions.yaml', 'history/readme.md',
}
IGNORED_DIRECTORIES = PRIVATE_DIRECTORIES | {
    '.git', '.venv', '__pycache__', '.pytest_cache', 'node_modules',
}


def private_work_path(name):
    path = PurePosixPath(name.replace('\\', '/').lower())
    return (any(part in PRIVATE_DIRECTORIES for part in path.parts)
            or path.name in {'agents.md', 'agents.override.md'}
            or path.as_posix() in PRIVATE_DOCUMENTS
            or path.parts[:2] == ('history', 'research')
            or (path.parts and path.parts[0] == 'research' and path.as_posix() not in
                {'research/coverage.md', 'research/coverage-gaps.yaml'})
            or path.parts[:2] == ('docs', 'working'))


def tracked_work_paths(root):
    """Inspect the Git index, including force-added ignored files."""
    if not (root / '.git').exists():
        return []
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                            capture_output=True, check=True)
    return sorted(name for name in result.stdout.decode('utf-8').split('\0')
                  if name and private_work_path(name))


def public_files(root):
    """Also work in exported checkouts, without scanning local work archives."""
    for directory, folders, names in os.walk(root):
        folders[:] = [name for name in folders if name.lower() not in IGNORED_DIRECTORIES]
        for name in sorted(names):
            path = Path(directory) / name
            if not private_work_path(path.relative_to(root).as_posix()):
                yield path
