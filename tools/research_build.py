"""Build isolated updates from a verified deterministic audit and current records.

Incoming packets are data. Only fixed repository capture/render/validate commands
run locally. No model calls, source research, catalog application or publication.
"""
from collections import Counter
from copy import deepcopy
from datetime import date
from hashlib import sha256
import argparse
import json
import re
from pathlib import Path
import subprocess
import sys
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import research_audit as audit, research_batch as batch, research_partial as partial
from tools.git_baselines import git_state
from tools.knowledge import canonical, integrity_errors, record_hash
from tools.package_workflow import safe_name, ALLOWED_NAMES, ALLOWED_PREFIXES, BLOCKED_NAMES, BLOCKED_PREFIXES
from tools.public_boundary import private_work_path
from tools.research_intake import private_path, retain, run_lock
from tools.research_runs import state_hash


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def verify_audit(packet, assignment, baseline, current, report, selected_raw,
                 packet_hash, assignment_hash, private_patterns=()):
    batch.require(report.get('original_sha256') == packet_hash and
                  report.get('assignment_sha256') == assignment_hash,
                  'Audit input bindings differ')
    batch.require(report.get('current_state_hash') == state_hash(current), 'Current records changed; audit again')
    batch.require(report.get('selected_sha256') == sha256(selected_raw).hexdigest(), 'Selected packet differs')
    # A hand-edited ready list or fabricated report cannot authorize new edits.
    verified = audit.audit(packet, assignment, baseline, current, private_patterns)
    selected = verified.pop('selected_packet')
    batch.require(encoded(selected) == selected_raw, 'Selected packet is not the audited derivation')
    verified.update(original_sha256=packet_hash, assignment_sha256=assignment_hash,
                    selected_sha256=sha256(selected_raw).hexdigest())
    batch.require(verified == report, 'Audit decisions differ from deterministic recomputation')
    return selected


def merge_ready(compiled, report, baseline, current):
    batch.require(state_hash(current) == report['current_state_hash'], 'Current state differs from audit')
    proposals = {u['id']: u for u in partial.units_for(compiled['changes'], baseline)}
    receipts = {u['id']: u for u in report['units']}
    ready = report['ready_unit_ids']
    batch.require(len(ready) == len(set(ready)) and set(ready) ==
                  {i for i, r in receipts.items() if r['reconciliation_status'] == 'ready'}, 'Ready unit list differs')
    batch.require(set(ready) <= set(proposals), 'Unknown ready proposal')
    result = deepcopy(current)
    evidence = {}
    fields = {(r['entity_type'], r['entity_id'], r['path']): r for r in compiled['research_run']['field_checks']}
    for ident in ready:
        unit, receipt = proposals[ident], receipts[ident]
        batch.require(unit['operation'] == 'upsert', 'Deletion is outside update scope')
        batch.require(audit.value_hash(audit.value_at(current, unit)) == receipt['current_value_hash'] and
                      audit.value_hash(unit['value']) == receipt['proposed_value_hash'], 'Unit value pin differs')
        batch.require(all(receipts[d]['reconciliation_status'] in {'ready', 'already_present'}
                          for d in receipt['dependencies']), 'Ready proposal has a deferred dependency')
        key = unit['kind'], unit['record_id']
        if unit['path']:
            batch.require(key in result, 'Profile was removed')
            partial.put(result[key], unit)
        else:
            result[key] = deepcopy(unit['value'])
        change = partial.selected_change(unit, baseline, fields)
        evidence.setdefault(key, set()).update(change['evidence_ids'])
    changes = []
    for key in sorted(result):
        if current.get(key) == result[key]: continue
        batch.validate_schema(result[key], batch.SCHEMAS[key[0]] + '.schema.json')
        changes.append({'kind': key[0], 'record': result[key],
                        'previous_hash': record_hash(current[key]) if key in current else None,
                        'evidence_ids': sorted(evidence[key])})
    # No operation can remove an unrelated record or rewrite its carry-forward values.
    batch.require(set(current) <= set(result), 'Current record removed by builder')
    return {'candidate': result, 'changes': changes, 'ready_unit_ids': list(ready),
            'new_profile_paths': {i:p for i,p in compiled.get('new_profile_paths', {}).items()
                                  if any(c['record']['id']==i and c['kind'] in {'model','provider'} for c in changes)},
            'current_state_hash': state_hash(current), 'candidate_state_hash': state_hash(result),
            'counts_by_kind': dict(sorted(Counter(c['kind'] for c in changes).items()))}


def public_snapshot(root):
    """Snapshot trusted local public files, excluding ignored/private operating data.

    Packet contents never select these files or executable commands. Tracked public
    files retain current bytes. New runtime/schema/test/public data files are allowed
    only in known repository directories, and publication is a later operation.
    """
    root = Path(root).resolve()
    names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached',
                                     '--others', '--exclude-standard']).decode('utf-8').split('\0')
    tracked = set(subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode('utf-8').split('\0'))
    files, seen = {}, set()
    for name in sorted(set(names) - {''}):
        name = safe_name(name)
        batch.require(not private_work_path(name), 'Private operating path is in public snapshot inventory')
        if name not in tracked:
            batch.require(name.startswith(('tools/', 'schema/', 'tests/', 'data/')) and
                          Path(name).suffix in {'.py', '.json', '.yaml', '.md'}, 'Unreviewed untracked snapshot path')
        batch.require(name.casefold() not in seen, 'Case-colliding snapshot paths')
        seen.add(name.casefold())
        path = root / name
        batch.require(path.is_file() and not any(batch.linked(p) for p in [path, *path.parents]),
                      'Missing or linked snapshot file')
        files[name] = path.read_bytes()
    batch.require(len(files) <= 2500 and sum(map(len, files.values())) <= 64 * 1024 * 1024,
                  'Public snapshot exceeds bound')
    return files


def hashes(files):
    return {name: sha256(raw).hexdigest() for name, raw in sorted(files.items())}


def write_updates(candidate, changes, locations, new_profile_paths=None):
    documents = {}
    for change in changes:
        kind, record = change['kind'], change['record']
        if kind in {'model', 'provider'}:
            if (kind, record['id']) in locations:
                path=locations[(kind, record['id'])][0]
            else:
                path=(new_profile_paths or {}).get(record['id'])
                pattern=r'models/[a-z0-9][a-z0-9-]*/'+re.escape(record['id'])+r'/profile\.yaml' if kind=='model' else r'providers/'+re.escape(record['id'])+r'/profile\.yaml'
                batch.require(path and re.fullmatch(pattern,path), 'New profile lacks a pinned onboarding path')
                batch.require(not (candidate/path).exists(),'New profile path already exists')
            target=candidate/path
            batch.require(not any(batch.linked(p) for p in [target,*target.parents]),'Linked onboarding path')
            target.parent.mkdir(parents=True,exist_ok=True)
            batch.write_yaml(target, record)
        else:
            path = batch.PATHS[kind]
            if path not in documents:
                doc = yaml.load((candidate / path).read_text(encoding='utf-8'),
                                Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
                documents[path] = doc, {r['id']: n for n, r in enumerate(doc['records'])}
            doc, indices = documents[path]
            if record['id'] in indices: doc['records'][indices[record['id']]] = record
            else:
                indices[record['id']] = len(doc['records'])
                doc['records'].append(record)
    for path, (doc, _) in documents.items(): batch.write_yaml(candidate / path, doc)


def public_write(name):
    safe_name(name)
    return (not private_work_path(name) and not name.startswith(BLOCKED_PREFIXES) and name not in BLOCKED_NAMES
            and (name.startswith(ALLOWED_PREFIXES) or name in ALLOWED_NAMES))


def stage_updates(root, plan, destination, observed_at, bindings):
    root = Path(root).resolve()
    date.fromisoformat(observed_at)
    batch.require(not integrity_errors(root), 'Current checksums must be captured before building')
    batch.require(state_hash({k: r for k, (_, r) in canonical(root).items()}) == plan['current_state_hash'],
                  'Current repository advanced before staging')
    source_head = batch.git(root, 'rev-parse', 'HEAD')
    files = public_snapshot(root)
    source_hashes = hashes(files)
    destination = batch.private_destination(root, destination)
    if destination.exists():
        receipt, _ = batch.load_json(destination / 'build-receipt.json')
        batch.require(receipt['bindings'] == bindings and receipt['source_files'] == source_hashes and
                      receipt['source_head'] == source_head and
                      receipt['observed_at'] == observed_at and
                      receipt['status'] == 'validated_current_repository_candidate' and
                      receipt['current_state_hash'] == plan['current_state_hash'] and
                      receipt['candidate_state_hash'] == plan['candidate_state_hash'] and
                      receipt['ready_unit_ids'] == plan['ready_unit_ids'], 'Existing build uses different inputs')
        candidate = destination / 'candidate'
        batch.require(public_snapshot_files(candidate) == receipt['candidate_files'], 'Retained candidate was modified')
        batch.require(state_hash({k: r for k, (_, r) in canonical(candidate).items()}) == plan['candidate_state_hash'],
                      'Retained candidate records differ')
        return {**receipt, 'repeat_noop': True}
    destination.mkdir(parents=True)
    candidate = destination / 'candidate'
    candidate.mkdir()
    checks = []
    try:
        for name, raw in files.items():
            path = candidate / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        batch.require(state_hash({k: r for k, (_, r) in canonical(candidate).items()}) == plan['current_state_hash'],
                      'Snapshot records differ from current state')
        write_updates(candidate, plan['changes'], canonical(root), plan.get('new_profile_paths'))
        def check(command):
            completed = subprocess.run([sys.executable, *command], cwd=candidate, capture_output=True,
                                       encoding='utf-8', errors='replace', timeout=180)
            checks.append({'command': command, 'exit_code': completed.returncode,
                           'output': completed.stdout + completed.stderr})
            batch.require(completed.returncode == 0, 'Isolated candidate check failed')
        if plan['changes']:
            evidence = sorted({i for c in plan['changes'] for i in c['evidence_ids']})
            batch.require(evidence, 'Updates lack capture evidence')
            reason = 'Recorded researched model, task, measurement and access updates with their evidence and limitations.'
            check(['tools/capture_changes.py', '--observed-at', observed_at, '--reason', reason, '--evidence', *evidence])
            month = candidate / 'changelog' / (observed_at[:7] + '.md')
            batch.require(month.relative_to(candidate).as_posix() in files, 'Product changelog needs a reviewed template')
            text = month.read_text(encoding='utf-8')
            heading = '## ' + date.fromisoformat(observed_at).strftime('%B') + ' ' + str(date.fromisoformat(observed_at).day)
            summary = '- Recorded researched updates to ' + ', '.join(
                str(count) + ' ' + kind.replace('_', ' ') + ' records' for kind, count in plan['counts_by_kind'].items()) + '. Evidence, conditions and unresolved gaps remain attached to the records.\n'
            if heading + '\n' in text:
                text = text.replace(heading + '\n', heading + '\n\n' + summary, 1)
            else:
                first_line, rest = text.split('\n', 1)
                text = first_line + '\n\n' + heading + '\n\n' + summary + rest
            month.write_text(text, encoding='utf-8')
        check(['tools/render.py'])
        check(['tools/validate.py'])
        batch.require(state_hash({k: r for k, (_, r) in canonical(candidate).items()}) == plan['candidate_state_hash'],
                      'Final records differ from merged updates')
        final = public_snapshot_files(candidate)
        changed = {name: {'previous_sha256': source_hashes.get(name), 'sha256': digest}
                   for name, digest in final.items() if source_hashes.get(name) != digest}
        batch.require(set(source_hashes) <= set(final), 'Snapshot file was removed')
        batch.require(all(public_write(name) for name in changed), 'Builder modified an unexpected public path')
        batch.require(hashes(public_snapshot(root)) == source_hashes, 'Original public files changed during build')
        batch.require(batch.git(root, 'rev-parse', 'HEAD') == source_head, 'Original Git commit changed during build')
        receipt = {'schema_version': '1.0', 'status': 'validated_current_repository_candidate',
                   'bindings': bindings, 'source_head': source_head, 'observed_at': observed_at, 'source_files': source_hashes,
                   'candidate_files': final, 'changes': changed, 'checks': checks,
                   'current_state_hash': plan['current_state_hash'], 'candidate_state_hash': plan['candidate_state_hash'],
                   'ready_unit_ids': plan['ready_unit_ids'], 'record_counts': plan['counts_by_kind'],
                   'records_changed': len(plan['changes']), 'model_calls': 0, 'catalog_applied': False,
                   'published': False, 'repeat_noop': False}
        retain(destination, 'build-receipt.json', encoded(receipt))
        return receipt
    except Exception:
        retain(destination, 'failed-checks.json', encoded(checks))
        raise


def public_snapshot_files(candidate):
    from tools.public_boundary import public_files
    files = {}
    for path in public_files(candidate):
        name = safe_name(path.relative_to(candidate).as_posix())
        batch.require(not any(batch.linked(p) for p in [path, *path.parents]), 'Linked candidate file')
        files[name] = path.read_bytes()
    return hashes(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--assignment', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--observed-at', required=True)
    parser.add_argument('--private-patterns', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    directory = private_path(root, args.audit)
    report, audit_hash = batch.load_json(private_path(root, directory / 'audit.json'))
    packet, packet_hash = batch.load_json(private_path(root, directory / 'original.json'))
    batch.require(packet_hash == args.sha256, 'Original packet differs from operator pin')
    selected, _ = batch.load_json(private_path(root, directory / 'selected.json'))
    selected_raw = (directory / 'selected.json').read_bytes()
    assignment, assignment_hash = batch.load_json(private_path(root, args.assignment))
    current = {k: r for k, (_, r) in canonical(root).items()}
    baseline = git_state(assignment['baseline_commit'])
    patterns = batch.load_json(private_path(root, args.private_patterns))[0]['patterns'] if args.private_patterns else []
    selected = verify_audit(packet, assignment, baseline, current, report, selected_raw,
                            packet_hash, assignment_hash, patterns)
    from tools.research_scoped import compile_packet
    compiled = compile_packet(selected, assignment, baseline, patterns)
    plan = merge_ready(compiled, report, baseline, current)
    destination = batch.private_destination(root, args.destination)
    bindings = {'audit_sha256': audit_hash, 'packet_sha256': packet_hash,
                'assignment_sha256': assignment_hash, 'selected_sha256': sha256(selected_raw).hexdigest(),
                'baseline_commit': assignment['baseline_commit']}
    with run_lock(private_path(root, destination.parent / (destination.name + '.build.lock'))):
        receipt = stage_updates(root, plan, destination, args.observed_at, bindings)
    print(json.dumps({k: receipt[k] for k in ('status', 'records_changed', 'record_counts', 'model_calls', 'repeat_noop', 'catalog_applied', 'published')}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RecursionError, yaml.YAMLError, subprocess.SubprocessError):
        print('Update build failed; inspect private audit bindings, current state and candidate checks.', file=sys.stderr)
        sys.exit(1)
