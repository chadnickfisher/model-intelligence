"""Apply pinned research builds and prepare/publish isolated Git releases.

Fixed local validation, transactional writes and explicit rollout pins. No model
calls or packet-supplied commands. Publication never commits the operator index.
"""
from hashlib import sha256
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import research_batch as batch, research_build as build
from tools.knowledge import canonical
from tools.research_runs import state_hash
from tools.research_intake import run_lock, retain
from tools.package_workflow import safe_name, ORIGINS
from tools.public_boundary import private_work_path


def fingerprint(raw):
    return sha256(raw).hexdigest()


def pinned_json(path, digest):
    value, actual = batch.load_json(path)
    batch.require(actual == digest, 'Private receipt pin differs')
    return value


def guarded(path):
    batch.require(not any(batch.linked(p) for p in [path, *path.parents]), 'Linked write path')


def file_hash(path):
    guarded(path)
    batch.require(not path.exists() or path.is_file(), 'Target is not a regular file')
    return fingerprint(path.read_bytes()) if path.exists() else None


def candidate_check(stage, receipt):
    candidate = stage / 'candidate'
    batch.require(receipt['status'] == 'validated_current_repository_candidate' and
                  receipt['model_calls'] == 0 and not receipt['published'], 'Unsupported build receipt')
    batch.require(build.public_snapshot_files(candidate) == receipt['candidate_files'], 'Candidate files differ')
    batch.require(state_hash({k: r for k, (_, r) in canonical(candidate).items()}) ==
                  receipt['candidate_state_hash'], 'Candidate canonical state differs')
    expected = {name: {'previous_sha256': receipt['source_files'].get(name), 'sha256': digest}
                for name, digest in receipt['candidate_files'].items()
                if receipt['source_files'].get(name) != digest}
    batch.require(set(receipt['source_files']) <= set(receipt['candidate_files']) and
                  expected == receipt['changes'], 'Build changes manifest differs')
    batch.require(all(build.public_write(name) for name in expected), 'Build includes a forbidden write')
    for script in ('tools/render.py', 'tools/validate.py'):
        batch.require(any(c['command'] == [script] and c['exit_code'] == 0 for c in receipt['checks']),
                      'Build validation receipt is absent')
    return candidate


def current_mode(root, receipt):
    batch.require(batch.git(root, 'rev-parse', 'HEAD') == receipt['source_head'], 'Checkout commit changed')
    files = build.hashes(build.public_snapshot(root))
    state = state_hash({k: r for k, (_, r) in canonical(root).items()})
    if files == receipt['candidate_files'] and state == receipt['candidate_state_hash']:
        return 'already_applied'
    batch.require(files == receipt['source_files'] and state == receipt['current_state_hash'],
                  'Checkout files or canonical state changed')
    return 'ready'


def save_journal(directory, value):
    path = directory / 'transaction.json'
    guarded(path)
    temporary = directory / 'transaction.json.part'
    guarded(temporary)
    with temporary.open('wb') as stream:
        stream.write(build.encoded(value)); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def replace_file(target, raw):
    guarded(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.research-update-tmp')
    guarded(temporary)
    batch.require(not temporary.exists(), 'Conflicting temporary write')
    try:
        with temporary.open('xb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        guarded(target)
        os.replace(temporary, target)
    finally:
        if temporary.exists(): temporary.unlink()


def recover(root, directory, receipt, digest):
    """Rollback only bytes we wrote; preserve and report concurrent edits."""
    journal, _ = batch.load_json(directory / 'transaction.json')
    batch.require(journal['receipt_sha256'] == digest and journal['changes'] == receipt['changes'] and
                  journal['source_head'] == receipt['source_head'], 'Recovery transaction differs')
    batch.require(journal['status'] != 'applied', 'Completed application cannot be recovered as an interrupted write')
    if batch.git(root, 'rev-parse', 'HEAD') != receipt['source_head']:
        journal.update(status='rollback_conflicts', conflicts=['git_head'])
        save_journal(directory, journal)
        return journal
    originals = {}
    for name, pins in receipt['changes'].items():
        safe_name(name)
        backup = directory / 'originals' / name
        guarded(backup)
        raw = backup.read_bytes() if pins['previous_sha256'] is not None else None
        batch.require(raw is None or fingerprint(raw) == pins['previous_sha256'], 'Recovery backup differs')
        originals[name] = raw
    conflicts = []
    for name, pins in reversed(list(receipt['changes'].items())):
        target = root / name
        try:
            present = file_hash(target)
            if present == pins['previous_sha256']: continue
            if present != pins['sha256']:
                conflicts.append(name); continue
            if originals[name] is None: target.unlink()
            else: replace_file(target, originals[name])
        except (OSError, ValueError):
            conflicts.append(name)
    journal.update(status='rollback_conflicts' if conflicts else 'rolled_back', conflicts=conflicts)
    save_journal(directory, journal)
    return journal


def validate(root):
    result = subprocess.run([sys.executable, 'tools/validate.py'], cwd=root, capture_output=True,
                            encoding='utf-8', errors='replace', timeout=180)
    batch.require(result.returncode == 0, 'Applied repository validation failed')
    return {'command': ['tools/validate.py'], 'exit_code': result.returncode, 'output': result.stdout + result.stderr}


def apply(root, stage, receipt, digest, transaction):
    candidate = candidate_check(stage, receipt)
    mode = current_mode(root, receipt)
    if mode == 'already_applied': return {'status': mode, 'changed_files': 0, 'model_calls': 0}
    batch.require(not transaction.exists(), 'Existing transaction requires explicit recovery or a fresh attempt')
    transaction.mkdir(parents=True)
    # Retain every backup before the first public write. Journal is durable before mutation.
    for name, pins in receipt['changes'].items():
        batch.require(file_hash(root / name) == pins['previous_sha256'], 'Stale target')
        if pins['previous_sha256'] is not None:
            backup = transaction / 'originals' / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            retain(backup.parent, backup.name, (root / name).read_bytes())
    journal = {'status': 'prepared', 'receipt_sha256': digest, 'source_head': receipt['source_head'],
               'changes': receipt['changes'], 'model_calls': 0, 'published': False}
    save_journal(transaction, journal)
    try:
        current_mode(root, receipt)
        for name, pins in receipt['changes'].items():
            batch.require(file_hash(root / name) == pins['previous_sha256'], 'Target advanced during application')
            raw = (candidate / name).read_bytes()
            batch.require(fingerprint(raw) == pins['sha256'], 'Candidate advanced during application')
            replace_file(root / name, raw)
        check = validate(root)
        batch.require(current_mode(root, receipt) == 'already_applied', 'Applied state differs')
        journal.update(status='applied', validation=check, changed_files=len(receipt['changes']))
        save_journal(transaction, journal)
        return journal
    except Exception:
        recover(root, transaction, receipt, digest)
        raise


def git_bytes(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def head_files(root, head):
    names = git_bytes(root, 'ls-tree', '-rz', '--name-only', head).decode().split('\0')
    result = {}
    for name in names:
        if not name: continue
        safe_name(name)
        batch.require(not private_work_path(name), 'Private paths in base history tree')
        result[name] = git_bytes(root, 'show', head + ':' + name)
    return result


def rollout_manifest(root, receipt):
    batch.require(current_mode(root, receipt) == 'ready', 'Prepare rollout before applying to checkout')
    before = build.hashes(head_files(root, receipt['source_head']))
    after = receipt['source_files']
    batch.require(set(before) <= set(after), 'Runtime rollout cannot remove files')
    return {'source_head': receipt['source_head'], 'source_files': after,
            'changes': {name: {'previous_sha256': before.get(name), 'sha256': digest}
                        for name, digest in after.items() if before.get(name) != digest}}


def branch_check(root, branch):
    batch.require(not branch.startswith('-') and branch != 'HEAD', 'Invalid publication branch')
    batch.git(root, 'check-ref-format', 'refs/heads/' + branch)


def commit(repo, message):
    # The isolated repository contains only the explicit public snapshot.
    batch.git(repo, 'add', '--all')
    if not batch.git(repo, 'diff', '--cached', '--name-only'): return batch.git(repo, 'rev-parse', 'HEAD')
    batch.git(repo, 'commit', '-m', message)
    return batch.git(repo, 'rev-parse', 'HEAD')


def prepare(root, stage, receipt, digest, destination, branch, rollout=None):
    candidate = candidate_check(stage, receipt)
    batch.require(current_mode(root, receipt) == 'ready', 'Release preparation needs pre-application checkout')
    branch_check(root, branch)
    origin = batch.git(root, 'remote', 'get-url', 'origin')
    batch.require(origin in ORIGINS and batch.git(root, 'remote', 'get-url', '--push', 'origin') == origin,
                  'Unexpected publication origin')
    expected = rollout_manifest(root, receipt)
    batch.require(not expected['changes'] or rollout == expected, 'Current runtime/data rollout needs its own exact pin')
    batch.require(not destination.exists(), 'Never overwrite a prepared release')
    destination.mkdir(parents=True)
    repo = destination / 'repository'
    batch.git(destination, 'init', '-q', str(repo))
    # A bundle contains only public HEAD ancestry, not local recovery refs. It
    # also avoids Git's shell-based local upload-pack helper on Windows.
    bundle = destination / 'baseline.bundle'
    batch.require(batch.git(root, 'rev-parse', 'HEAD') == receipt['source_head'], 'Source commit advanced')
    batch.git(root, 'bundle', 'create', str(bundle), 'HEAD')
    batch.git(repo, 'fetch', '--no-tags', str(bundle), 'HEAD')
    batch.git(repo, 'checkout', '--detach', receipt['source_head'])
    batch.git(repo, 'config', 'core.autocrlf', 'false')
    for field in ('user.name', 'user.email'):
        batch.git(repo, 'config', field, batch.git(root, 'config', field))
    batch.git(repo, 'remote', 'add', 'origin', origin)
    files = build.public_snapshot(root)
    for name, raw in files.items(): replace_file(repo / name, raw)
    batch.require(build.hashes(build.public_snapshot(repo)) == receipt['source_files'], 'Release source export differs')
    rollout_commit = commit(repo, 'Add researched catalog groundwork and deterministic update tooling')
    # A source commit is made only in this isolated release, never in the operator checkout.
    local_receipt = {**receipt, 'source_head': rollout_commit}
    application = apply(repo, stage, local_receipt, digest, destination / 'application')
    checks = [validate(repo)]
    rendered = subprocess.run([sys.executable, 'tools/render.py'], cwd=repo, capture_output=True,
                              encoding='utf-8', errors='replace', timeout=180)
    batch.require(rendered.returncode == 0 and build.hashes(build.public_snapshot(repo)) == receipt['candidate_files'],
                  'Release rendering differs from candidate')
    checks.append({'command': ['tools/render.py'], 'exit_code': rendered.returncode,
                   'output': rendered.stdout + rendered.stderr})
    tests = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                            '--basetemp', str(destination / 'test-temp')], cwd=repo, capture_output=True,
                           encoding='utf-8', errors='replace', timeout=900)
    checks.append({'command': ['pytest', '-q'], 'exit_code': tests.returncode,
                   'output': tests.stdout + tests.stderr})
    retain(destination, 'checks.json', build.encoded(checks))
    batch.require(tests.returncode == 0, 'Release test suite failed')
    batch.require(build.hashes(build.public_snapshot(repo)) == receipt['candidate_files'], 'Tests changed release files')
    final = commit(repo, 'Update researched model evidence, assessments and access records')
    batch.require(not batch.git(repo, 'status', '--porcelain'), 'Release is dirty')
    batch.require(current_mode(root, receipt) == 'ready', 'Operator checkout advanced during release preparation')
    result = {'status': 'prepared_release', 'build_receipt_sha256': digest, 'source_head': receipt['source_head'],
              'branch': branch, 'origin': origin, 'rollout_commit': rollout_commit, 'commit': final,
              'rollout_paths': sorted(expected['changes']), 'research_paths': sorted(receipt['changes']),
              'candidate_files': receipt['candidate_files'], 'checks_sha256': fingerprint(build.encoded(checks)),
              'model_calls': 0, 'published': False, 'operator_checkout_changed': False,
              'application_status': application['status']}
    retain(destination, 'release-receipt.json', build.encoded(result))
    return result


def remote_head(repo, branch):
    output = batch.git(repo, 'ls-remote', '--heads', 'origin', 'refs/heads/' + branch).split()
    batch.require(len(output) == 2 and output[1] == 'refs/heads/' + branch, 'Publication branch absent or ambiguous')
    return output[0]


def publish(directory, release):
    repo = directory / 'repository'
    branch_check(repo, release['branch'])
    batch.require(release['status'] == 'prepared_release' and release['origin'] in ORIGINS and
                  release['model_calls'] == 0, 'Unsupported release')
    batch.require(batch.git(repo, 'remote', 'get-url', 'origin') == release['origin'] and
                  batch.git(repo, 'remote', 'get-url', '--push', 'origin') == release['origin'], 'Release origin changed')
    batch.require(batch.git(repo, 'rev-parse', 'HEAD') == release['commit'] and
                  not batch.git(repo, 'status', '--porcelain') and
                  build.hashes(build.public_snapshot(repo)) == release['candidate_files'], 'Prepared release differs')
    checks, checks_hash = batch.load_json(directory / 'checks.json')
    batch.require(checks_hash == release['checks_sha256'] and all(c['exit_code'] == 0 for c in checks),
                  'Publication checks differ')
    remote = remote_head(repo, release['branch'])
    if remote != release['commit']:
        batch.require(remote == release['source_head'], 'Remote advanced; reconcile again, never force push')
        batch.git(repo, 'push', 'origin', release['commit'] + ':refs/heads/' + release['branch'])
    batch.require(remote_head(repo, release['branch']) == release['commit'], 'Exact remote commit not verified')
    result = {'status': 'remote_verified_ci_pending', 'commit': release['commit'], 'branch': release['branch'],
              'model_calls': 0, 'published': True, 'ci_verified': False}
    # Push recovery is idempotent: an already matching remote needs no second push.
    retain(directory, 'publication-receipt.json', build.encoded(result))
    return result


def verify_ci(directory, release):
    repo = directory / 'repository'
    batch.require(remote_head(repo, release['branch']) == release['commit'], 'Remote no longer matches release')
    repository = 'chadnickfisher/model-intelligence'
    batch.require(len(release['commit']) == 40 and all(c in '0123456789abcdef' for c in release['commit']),
                  'Invalid release commit')
    completed = subprocess.run(['gh', 'api', 'repos/' + repository + '/actions/runs?head_sha=' +
                                release['commit'] + '&event=push&per_page=100'], cwd=repo,
                               capture_output=True, encoding='utf-8', timeout=60)
    batch.require(completed.returncode == 0, 'CI lookup failed; remote success is not CI success')
    runs = json.loads(completed.stdout)['workflow_runs']
    runs = [r for r in runs if r['head_sha'] == release['commit'] and r['head_branch'] == release['branch']
            and r['event'] == 'push' and r['path'] == '.github/workflows/ci.yml']
    latest = max(runs, key=lambda r: (r['run_number'], r['run_attempt'])) if runs else None
    result = {'status': 'ci_pending', 'commit': release['commit'], 'ci_verified': False}
    if latest:
        result.update(run_id=latest['id'], run_url=latest['html_url'], conclusion=latest['conclusion'])
        if latest['status'] == 'completed':
            result.update(status='published_ci_verified' if latest['conclusion'] == 'success' else 'ci_failed',
                          ci_verified=latest['conclusion'] == 'success')
    if result['ci_verified']: retain(directory, 'ci-receipt.json', build.encoded(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'apply', 'recover', 'rollout', 'prepare', 'publish', 'verify-ci'])
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--receipt-sha256', required=True)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--branch')
    parser.add_argument('--rollout', type=Path)
    parser.add_argument('--rollout-sha256')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    destination = batch.private_destination(root, args.destination) if args.destination else None
    with run_lock(root / '.local/research/research-publication.lock'):
        if args.mode in {'publish', 'verify-ci'}:
            batch.require(destination is not None, 'Publication needs a prepared release')
            release = pinned_json(destination / 'release-receipt.json', args.receipt_sha256)
            result = publish(destination, release) if args.mode == 'publish' else verify_ci(destination, release)
        else:
            batch.require(args.stage is not None, 'Build stage required')
            stage = batch.private_destination(root, args.stage)
            receipt = pinned_json(stage / 'build-receipt.json', args.receipt_sha256)
            if args.mode != 'recover': candidate_check(stage, receipt)
            if args.mode == 'check': result = {'status': current_mode(root, receipt), 'model_calls': 0}
            elif args.mode == 'rollout':
                batch.require(destination is not None, 'Rollout manifest destination required')
                result = rollout_manifest(root, receipt)
                retain(destination, 'rollout.json', build.encoded(result))
            elif args.mode == 'prepare':
                batch.require(destination is not None and args.branch, 'Release destination and branch required')
                rollout = pinned_json(batch.private_destination(root, args.rollout), args.rollout_sha256) if args.rollout else None
                result = prepare(root, stage, receipt, args.receipt_sha256, destination, args.branch, rollout)
            else:
                batch.require(destination is not None, 'Transaction directory required')
                if args.mode == 'apply': result = apply(root, stage, receipt, args.receipt_sha256, destination)
                else: result = recover(root, destination, receipt, args.receipt_sha256)
        print(json.dumps({k: v for k, v in result.items() if k not in
                          {'validation', 'changes', 'source_files', 'candidate_files', 'checks'}}, ensure_ascii=False))
        if result.get('status') in {'ci_failed', 'rollback_conflicts'}: sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError):
        print('Research publication stopped; inspect retained private receipts and recovery state.', file=sys.stderr)
        sys.exit(1)
