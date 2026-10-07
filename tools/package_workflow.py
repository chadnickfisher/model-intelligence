"""Manual, dry-run-first local package import or reviewed update publication.

Incoming packages never supply commands. Raw research does not edit the repository.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.public_boundary import private_work_path

REPOSITORY = 'https://github.com/chadnickfisher/model-intelligence'
ORIGINS = {REPOSITORY, REPOSITORY + '.git', 'git@github.com:chadnickfisher/model-intelligence.git'}
BRANCH = 'main'
MAX_BYTES = 32 * 1024 * 1024
MAX_FILES = 2500
RAW_FILES = {'model_intelligence_coding_research_2026-10-07.json',
             'model_intelligence_coding_research_2026-10-07.md',
             'access_pricing_research_2026-10-07.json',
             'model_postlaunch_research_all53_2026-10-07.zip'}
BLOCKED_PREFIXES = ('.git/', '.github/', '.agents/', 'tools/', 'schema/', 'tests/', '.streamlit/')
BLOCKED_NAMES = {'requirements.txt', 'requirements-dev.txt', 'pyproject.toml', 'uv.lock',
                 'AGENTS.md', '.gitignore', '.gitmodules', 'package.json', 'package-lock.json'}
ALLOWED_PREFIXES = ('models/', 'providers/', 'data/', 'evidence/', 'history/', 'research/',
                    'changelog/')
ALLOWED_NAMES = {'README.md', 'START-HERE.md', 'CONTRIBUTING.md', 'MAINTENANCE.md',
                 'methodology.md', 'repo-map.yaml', 'LICENSE.md', 'NOTICE.md'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    """Portable path rules also reject Windows ADS, devices and case ambiguity."""
    if '\\' in name or ':' in name or '\x00' in name:
        raise ValueError('Unsafe archive path')
    p = PurePosixPath(name)
    if p.is_absolute() or not p.parts or any(t in {'.', '..'} for t in name.split('/')):
        raise ValueError('Unsafe archive path')
    for part in p.parts:
        if part.endswith((' ', '.')) or re.match(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', part, re.I):
            raise ValueError('Unsafe Windows path')
    return p.as_posix()


def archive_members(data):
    if len(data) > MAX_BYTES:
        raise ValueError('Package exceeds compressed size limit')
    result = {}; seen = set(); expanded = 0
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if len(archive.infolist()) > MAX_FILES:
            raise ValueError('Too many archive entries')
        for item in archive.infolist():
            name = safe_name(item.filename.rstrip('/'))
            key = name.casefold()
            if key in seen:
                raise ValueError('Duplicate or case-colliding archive path')
            seen.add(key)
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in {0, stat.S_IFREG, stat.S_IFDIR}):
                raise ValueError('Archive links or special files are forbidden')
            if item.flag_bits & 1:
                raise ValueError('Encrypted archive is unsupported')
            expanded += item.file_size
            if expanded > MAX_BYTES:
                raise ValueError('Expanded archive exceeds size limit')
            if not item.is_dir():
                result[name] = archive.read(item)
    for name in result:
        if any('/'.join(PurePosixPath(name).parts[:i]).casefold() in {p.casefold() for p in result}
               for i in range(1, len(PurePosixPath(name).parts))):
            raise ValueError('File/directory collision')
    return result


def folder_members(path):
    result = {}; seen = set(); total = 0
    for item in sorted(path.rglob('*')):
        if item.is_symlink() or getattr(item.lstat(), 'st_file_attributes', 0) & 0x400:
            raise ValueError('Folder links/reparse points are forbidden')
        if item.is_file():
            name = safe_name(item.relative_to(path).as_posix())
            if name.casefold() in seen:
                raise ValueError('Case-colliding folder path')
            seen.add(name.casefold()); total += item.stat().st_size
            if total > MAX_BYTES or len(result) >= MAX_FILES:
                raise ValueError('Folder exceeds size/count limit')
            result[name] = item.read_bytes()
    return result


def package_files(path, expected_sha256=None, expected_bytes=None):
    path = Path(path)
    if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & 0x400:
        raise ValueError('Input cannot be a link/reparse point')
    if path.is_dir():
        if expected_sha256 or expected_bytes:
            raise ValueError('Archive hash/size cannot validate a folder; supply the retained ZIP')
        return folder_members(path), None
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('Package exceeds compressed size limit')
    data = path.read_bytes()
    if expected_bytes is not None and len(data) != expected_bytes:
        raise ValueError('Archive byte count mismatch')
    if expected_sha256 and digest(data) != expected_sha256:
        raise ValueError('Archive SHA-256 mismatch')
    return archive_members(data), digest(data)


def raw_research(files):
    if 'package.json' in files:
        raise ValueError('Ready-to-apply packages are not raw research')
    if not RAW_FILES <= set(files):
        raise ValueError('Unrecognized raw research identity; expected complete research bundle')
    extras = set(files) - RAW_FILES
    # Explorer's extracted behavior folder is accepted only when it matches nested bytes.
    nested = archive_members(files['model_postlaunch_research_all53_2026-10-07.zip'])
    expected_nested = {'README.md', 'COVERAGE.md', 'model_postlaunch_research_all53_2026-10-07.json',
                       'postlaunch_behavior_schema_2026-10-07.json', 'postlaunch_all_catalog_maintenance_contract.json'}
    if set(nested) != expected_nested:
        raise ValueError('Unexpected nested research members')
    for name in extras:
        p = PurePosixPath(name)
        if len(p.parts) != 2 or p.parts[0] != 'model_postlaunch_research_all53_2026-10-07' or p.name not in nested or files[name] != nested[p.name]:
            raise ValueError('Unexpected raw folder file or changed extracted copy')
    coding = json.loads(files['model_intelligence_coding_research_2026-10-07.json'])
    access = json.loads(files['access_pricing_research_2026-10-07.json'])
    behavior = json.loads(nested['model_postlaunch_research_all53_2026-10-07.json'])
    if access['repository'].removesuffix('.git') not in {REPOSITORY, 'chadnickfisher/model-intelligence'}:
        raise ValueError('Wrong research repository')
    counts = (len(coding['normalized_index']), len(access['full_catalog_model_audit']),
              len(access['baseline_consumer_client_join_review']), len(behavior['coverage_ledger']), len(behavior['records']))
    if counts != (87, 53, 27, 53, 86):
        raise ValueError('Incomplete research structure/counts')
    if sum(len(x['route_observations']) + len(x['consumer_client_routes']) for x in access['full_catalog_model_audit']) != 176:
        raise ValueError('Route observation count mismatch')
    prepared = {name: files[name] for name in RAW_FILES if not name.endswith('.zip')}
    prepared.update({'behavior/' + name: data for name, data in nested.items()})
    return prepared, counts


def write_prepared(destination, files, log):
    destination = Path(destination).absolute()
    if destination.exists() and (destination.is_symlink() or getattr(destination.lstat(), 'st_file_attributes', 0) & 0x400):
        raise ValueError('Destination cannot be a link/reparse point')
    # Preflight all conflicts before any writes. Same input is idempotent.
    for name, data in files.items():
        p = destination / name
        if p.exists() and (p.is_symlink() or not p.is_file() or p.read_bytes() != data):
            raise ValueError('Destination conflict: ' + name)
        for parent in p.parents:
            if parent.exists() and (parent.is_symlink() or getattr(parent.lstat(), 'st_file_attributes', 0) & 0x400):
                raise ValueError('Destination parent link/reparse point')
    receipt=destination/'import-receipt.json'
    if receipt.exists() and (receipt.is_symlink() or not receipt.is_file() or getattr(receipt.lstat(),'st_file_attributes',0)&0x400):
        raise ValueError('Invalid existing receipt target')
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        p = destination / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    (destination / 'import-receipt.json').write_text(json.dumps(log, indent=2) + '\n', encoding='utf-8')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def repo_guard(repo, base):
    repo = Path(repo).resolve()
    if any(git(repo, 'remote', 'get-url', *options, 'origin').rstrip('/') not in ORIGINS
           for options in [(), ('--push',)]):
        raise ValueError('Repository remote is outside exact allowlist')
    if git(repo, 'branch', '--show-current') != BRANCH:
        raise ValueError('Only main is allowed')
    if not isinstance(base,str) or not re.fullmatch('[a-f0-9]{40}', base) or git(repo, 'rev-parse', 'HEAD') != base:
        raise ValueError('Expected base commit mismatch')
    if git(repo, 'status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Ready-update requires a clean worktree and index')
    return repo


def ready_update(files, intended):
    if 'package.json' not in files:
        raise ValueError('Raw research cannot be applied as a ready update')
    manifest = json.loads(files['package.json'])
    if manifest.get('package_type') != 'ready-update' or manifest.get('repository') != REPOSITORY or manifest.get('branch') != BRANCH:
        raise ValueError('Wrong update package identity')
    entries = manifest['files'];paths = [safe_name(e['path']) for e in entries]
    if not entries:raise ValueError('Empty update package')
    if len({p.casefold() for p in paths}) != len(paths) or set(paths) != set(intended):
        raise ValueError('Manifest must match explicit intended paths exactly')
    expected = {'package.json'}
    for entry, path in zip(entries, paths):
        if private_work_path(path) or any(part.startswith('.') for part in PurePosixPath(path).parts) or path.startswith(BLOCKED_PREFIXES) or path in BLOCKED_NAMES or Path(path).suffix not in {'.md','.yaml','.json'} or not (path.startswith(ALLOWED_PREFIXES) or path in ALLOWED_NAMES):
            raise ValueError('Update path outside reviewed allowlist: ' + path)
        if entry['operation'] == 'write':
            payload = 'payload/' + path;expected.add(payload)
            if payload not in files or digest(files[payload]) != entry['sha256']:
                raise ValueError('Payload hash mismatch: ' + path)
        elif entry['operation'] == 'delete':
            if not entry.get('previous_sha256'):
                raise ValueError('Deletion requires exact prior-file hash')
        else: raise ValueError('Unsupported update operation')
    if set(files) != expected:
        raise ValueError('Unexpected package files')
    return manifest


def preflight_update(repo, manifest):
    for e in manifest['files']:
        p = repo / e['path']
        if p.exists() and (not p.is_file() or getattr(p.lstat(),'st_file_attributes',0)&0x400):
            raise ValueError('Target must be a regular file or a new path')
        if p.is_symlink() or any(parent.is_symlink() or (parent.exists() and getattr(parent.lstat(), 'st_file_attributes', 0) & 0x400) for parent in p.parents if parent != repo.parent):
            raise ValueError('Target links are forbidden')
        previous = digest(p.read_bytes()) if p.is_file() else None
        if previous != e.get('previous_sha256'):
            raise ValueError('Prior-file hash mismatch: ' + e['path'])
        if e['operation'] == 'delete' and (not p.is_file() or git(repo, 'ls-files', '--', e['path']) != e['path']):
            raise ValueError('Deletion must name one existing tracked file')


def apply_update(repo, files, manifest, publish, message):
    paths = [e['path'] for e in manifest['files']]
    preflight_update(repo, manifest)
    # Mutations begin only after every package/path/base guard has passed.
    for e in manifest['files']:
        p = repo / e['path']
        if e['operation'] == 'delete':p.unlink()
        else:p.parent.mkdir(parents=True, exist_ok=True);p.write_bytes(files['payload/' + e['path']])
    for command in ([sys.executable, 'tools/render.py'], [sys.executable, 'tools/validate.py'],
                    [sys.executable, '-m', 'pytest', '-q']):
        subprocess.run(command, cwd=repo, check=True)
    changed = set(git(repo, 'diff', '--name-only').splitlines()) | set(git(repo, 'ls-files', '--others', '--exclude-standard').splitlines())
    if not changed <= set(paths):
        raise ValueError('Reviewed checks produced changes outside intended paths; inspect worktree')
    for e in manifest['files']:
        p=repo/e['path']
        if e['operation']=='write' and digest(p.read_bytes())!=e['sha256']:
            raise ValueError('Rendered result differs from approved payload; inspect worktree')
    if not publish:return {'state':'applied-and-checked', 'paths':paths}
    # Existing auth only; no tokens, force, pull/rebase, or credential setup.
    remote = git(repo, 'ls-remote', 'origin', 'refs/heads/main').split()[0]
    if remote != manifest['base_commit']:
        raise ValueError('Remote advanced; review new main before publication')
    git(repo, 'add', '--', *paths)
    if set(git(repo, 'diff', '--cached', '--name-only').splitlines()) != changed:
        raise ValueError('Staged paths do not exactly match reviewed changes')
    git(repo, 'commit', '-m', message)
    commit = git(repo, 'rev-parse', 'HEAD');git(repo, 'push', 'origin', 'HEAD:refs/heads/main')
    if git(repo, 'ls-remote', 'origin', 'refs/heads/main').split()[0] != commit:
        raise ValueError('Remote commit verification failed')
    return {'state':'published-remote-verified', 'commit':commit,'paths':paths,
            'ci':'Check this exact commit through authorized GitHub tools; push success is not CI success.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['import-research','apply-update'])
    parser.add_argument('input',type=Path);parser.add_argument('--sha256');parser.add_argument('--bytes',type=int)
    parser.add_argument('--destination',type=Path);parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--base');parser.add_argument('--paths',nargs='*',default=[])
    parser.add_argument('--apply',action='store_true');parser.add_argument('--publish',action='store_true');parser.add_argument('--message',default='Apply reviewed Model Intelligence update')
    args=parser.parse_args()
    if args.publish and (not args.apply or args.mode!='apply-update'):raise ValueError('Publication requires explicit ready-update apply mode')
    files,sha=package_files(args.input,args.sha256,args.bytes)
    receipt={'mode':args.mode,'archive_sha256':sha,'files':{k:digest(v) for k,v in files.items()},'dry_run':not args.apply}
    if args.mode=='import-research':
        prepared,counts=raw_research(files);receipt['counts']=counts
        if args.apply:
            if not args.destination:raise ValueError('Explicit preparation destination is required')
            destination=args.destination.absolute();repo=args.repo.resolve()
            if destination==repo or repo in destination.parents:raise ValueError('Raw research destination must be outside the repository')
            write_prepared(destination,prepared,receipt)
    else:
        manifest=ready_update(files,args.paths)
        if args.base!=manifest['base_commit']:raise ValueError('Explicit base must match manifest')
        repo=repo_guard(args.repo,args.base)
        preflight_update(repo,manifest)
        if args.apply:receipt['result']=apply_update(repo,files,manifest,args.publish,args.message)
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,zipfile.BadZipFile,subprocess.CalledProcessError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);sys.exit(1)
