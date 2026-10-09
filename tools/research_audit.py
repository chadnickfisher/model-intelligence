"""Deterministic packet/baseline/current reconciliation; no network or model calls.

Produces private receipts for the update builder. Researcher judgments remain
researcher judgments; code does not independently certify public claim support.
No catalog writes, staging, inference adapter, publication or scheduling.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import research_batch as batch, research_partial as partial
from tools.git_baselines import git_state
from tools.knowledge import canonical, record_hash
from tools.research_intake import private_path, retain, run_lock, parse
from tools.research_runs import state_hash

MISSING = object()


def value_at(state, unit):
    value = state.get((unit['kind'], unit['record_id']), MISSING)
    for part in unit['path'].split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        if not isinstance(value, dict) or part not in value:
            return MISSING
        value = value[part]
    if unit['finding_id']:
        if not isinstance(value, list):
            return MISSING
        matches = [r for r in value if isinstance(r, dict) and r.get('id') == unit['finding_id']]
        batch.require(len(matches) <= 1, 'Ambiguous current finding identity')
        return matches[0] if matches else MISSING
    return value


def value_hash(value):
    # Missing and explicit null are different states.
    return None if value is MISSING else record_hash(value)


def reconcile_current(selection, baseline, current, protected_context=()):
    """Three-way field comparison with stable IDs and dependency propagation.

    Never rebase a packet's prior hashes/accounting onto current records. Step 3
    must merge only ready fields into the pinned current state and validate it.
    """
    units = deepcopy(selection['units'])
    proposals = {u['id']: u for u in partial.units_for(selection['compiled']['changes'], baseline)}
    changed_context = []
    for key in sorted(set(baseline) | set(current)):
        before, now = baseline.get(key, MISSING), current.get(key, MISSING)
        if before != now:
            changed_context.append({'kind': key[0], 'record_id': key[1],
                                    'baseline_hash': value_hash(before), 'current_hash': value_hash(now)})
    references = {}
    for key in set(baseline) | set(current):
        references.setdefault(key[1], []).append(key)
        if key[0] == 'model':
            for state in (baseline, current):
                for name in partial.COLLECTIONS:
                    for finding in state.get(key, {}).get(name, []):
                        references.setdefault(finding['id'], []).append((key, name, finding['id']))
    definitions = {u['finding_id'] or u['record_id'] for u in units if u['finding_id'] or not u['path']}
    changed_rules = [key for key in protected_context if baseline.get(key, MISSING) != current.get(key, MISSING)]
    current_urls = {}
    for (kind, ident), row in current.items():
        if kind == 'source': current_urls.setdefault(row['url'], []).append(ident)
    for row in units:
        if row['status'] != 'candidate':
            row['reconciliation_status'] = 'structurally_deferred'
            continue
        batch.require(row['id'] in proposals, 'Structural unit missing from selected proposals')
        unit = proposals[row['id']]
        before, now = value_at(baseline, unit), value_at(current, unit)
        after = MISSING if unit['operation'] == 'remove' else unit['value']
        row.update(baseline_value_hash=value_hash(before), current_value_hash=value_hash(now),
                   proposed_value_hash=value_hash(after))
        if now == after:
            row['reconciliation_status'] = 'already_present'
            continue
        row['reconciliation_status'] = 'ready' if now == before else 'conflict'
        if now != before:
            row['reason'] = 'Current value differs from both frozen baseline and proposal'
            continue
        if changed_rules:
            row.update(reconciliation_status='conflict', reason='Current research contract or task rubric differs from frozen baseline')
            continue
        key = unit['kind'], unit['record_id']
        old_owner, owner = baseline.get(key), current.get(key)
        if old_owner is not None and owner is None:
            row.update(reconciliation_status='conflict', reason='Current record was removed')
            continue
        if unit['kind'] in {'model', 'provider'} and old_owner and owner:
            identity_keys = ('id', 'identity') if unit['kind'] == 'model' else ('id',)
            if any(old_owner.get(k) != owner.get(k) for k in identity_keys):
                row.update(reconciliation_status='conflict', reason='Current owner identity differs from frozen baseline')
                continue
        if unit['kind'] == 'source' and isinstance(after, dict):
            collisions = [i for i in current_urls.get(after['url'], []) if i != unit['record_id']]
            if collisions:
                row.update(reconciliation_status='conflict', reason='Source URL has another current canonical identity')
                continue
        # Existing context used by a proposal may also have changed after research.
        refs = partial.refs(unit['value'], unit['path'].lstrip('/')) | set(unit['change']['evidence_ids'])
        drift = set()
        for ref in refs - definitions:
            for ref_key in references.get(ref, []):
                if isinstance(ref_key[0], tuple):
                    owner_key, name, ident = ref_key
                    probe = {'kind': owner_key[0], 'record_id': owner_key[1],
                             'path': '/' + name, 'finding_id': ident}
                    old, present = value_at(baseline, probe), value_at(current, probe)
                else:
                    old, present = baseline.get(ref_key, MISSING), current.get(ref_key, MISSING)
                if old != present: drift.add(ref)
        if drift:
            row.update(reconciliation_status='conflict', reason='Referenced current context differs from frozen baseline',
                       changed_reference_ids=sorted(drift))
    # A ready field depending on a changed proposal is not independent.
    by_id = {u['id']: u for u in units}
    for _ in range(len(units) + 1):
        changed = False
        for row in units:
            if row['reconciliation_status'] != 'ready': continue
            batch.require(all(i in by_id for i in row['dependencies']), 'Unknown proposal dependency')
            blocked = [i for i in row['dependencies'] if by_id[i]['reconciliation_status'] not in {'ready', 'already_present'}]
            if blocked:
                row.update(reconciliation_status='dependency_deferred',
                           reason='Required proposal has a structural or current-repository conflict',
                           blocked_dependency_ids=sorted(blocked))
                changed = True
        if not changed: break
    else:
        raise ValueError('Current dependency reconciliation did not converge')
    return {'units': units, 'counts': dict(sorted(Counter(u['reconciliation_status'] for u in units).items())),
            'current_differences': changed_context, 'changed_rule_ids': sorted(key[1] for key in changed_rules),
            'current_state_hash': state_hash(current)}


def audit(packet, assignment, baseline, current, private_patterns=()):
    selection = partial.compile_partial(packet, assignment, baseline, private_patterns)
    rules = {('research_contract', assignment['research_run']['contract_id'])}
    rules |= {key for key in set(baseline) | set(current) if key[0] == 'task'}
    comparison = reconcile_current(selection, baseline, current, sorted(rules))
    return {**comparison, 'schema_version': '1.0', 'status': 'deterministic_reconciliation_complete',
            'assignment_id': assignment['assignment_id'], 'baseline_commit': assignment['baseline_commit'],
            'baseline_state_hash': state_hash(baseline),
            'structural_counts': {'eligible': selection['candidate_units'], 'deferred': selection['deferred_units']},
            'original_accounting_counts': selection['original_accounting_counts'],
            'completion': selection['compiled']['completion'], 'source_reconciliation': selection['reconciliation'],
            'accounting_projection': selection['accounting_projection'],
            'ready_unit_ids': [u['id'] for u in comparison['units'] if u['reconciliation_status'] == 'ready'],
            'selected_packet': selection['selected_packet'],
            'judgment_origin': 'researcher_packet', 'independent_claim_verification_performed': False,
            'model_calls': 0, 'catalog_updated': False, 'published': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--assignment', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--bytes', type=int, required=True)
    parser.add_argument('--private-patterns', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    packet_path = private_path(root, args.packet)
    batch.require(packet_path.is_file() and packet_path.stat().st_size <= batch.MAX_BYTES,
                  'Original packet exceeds size bound')
    raw = packet_path.read_bytes()
    batch.require(0 < args.bytes <= batch.MAX_BYTES and len(raw) == args.bytes and sha256(raw).hexdigest() == args.sha256,
                  'Original packet bytes/hash differ')
    packet = parse(raw)
    assignment, assignment_hash = batch.load_json(private_path(root, args.assignment))
    patterns = batch.load_json(private_path(root, args.private_patterns))[0]['patterns'] if args.private_patterns else []
    current = {k: r for k, (_, r) in canonical(root).items()}
    result = audit(packet, assignment, git_state(assignment['baseline_commit']), current, patterns)
    selected = (json.dumps(result.pop('selected_packet'), ensure_ascii=False, indent=2) + '\n').encode()
    result.update(original_sha256=args.sha256, assignment_sha256=assignment_hash,
                  selected_sha256=sha256(selected).hexdigest())
    # Fail if the repository changed while the audit was running.
    batch.require(result['current_state_hash'] == state_hash({k: r for k, (_, r) in canonical(root).items()}),
                  'Current repository changed during reconciliation')
    destination = private_path(root, args.destination)
    with run_lock(private_path(root, destination / 'audit.lock')):
        retain(destination, 'original.json', raw)
        retain(destination, 'selected.json', selected)
        retain(destination, 'audit.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode())
    print(json.dumps({k: result[k] for k in ('status', 'counts', 'structural_counts', 'original_accounting_counts', 'model_calls')}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.CalledProcessError):
        print('Deterministic audit failed; inspect private inputs, assignment and repository state.', file=sys.stderr)
        sys.exit(1)
