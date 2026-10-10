"""Pure exact-URL source identity reconciliation; original research stays immutable."""
from copy import deepcopy
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.knowledge import record_hash
from tools.research_batch import require


def remap_refs(value, mapping, key=''):
    # New sources with different URLs remain local until the strict allocator.
    if isinstance(value, dict):
        return {k: remap_refs(v, mapping, k) for k, v in value.items()}
    if isinstance(value, list):
        return [remap_refs(v, mapping, key) for v in value]
    if isinstance(value, str) and (key == 'id' or key.endswith(('_id', '_ids'))):
        return mapping.get(value, value)
    return value


def reconcile_sources(packet, baseline, *, defer_conflicts=False):
    """Retain canonical IDs, historical scopes/limitations, and all actual dates.

    Only byte-identical URLs are equivalent. Conflicting identity metadata or
    duplicate proposals need an explicit review; never silently choose a winner.
    This returns a derived packet and private map, not semantic acceptance.
    Partial selection can request conflict receipts while deferring the repaired
    source proposal and its dependents; conflicting values are never invented.
    """
    result = deepcopy(packet)
    urls = {}
    for (kind, ident), record in baseline.items():
        if kind == 'source':
            require(record['url'] not in urls, 'Ambiguous canonical source URL')
            urls[record['url']] = (ident, record)
    mapping, repairs, conflicts = {}, [], []
    for change in result['changes']:
        if change['kind'] != 'source':
            continue
        record = change['record']
        if not record['id'].startswith('new:') or not isinstance(record.get('url'), str) or record['url'] not in urls:
            continue
        ident, prior = urls[record['url']]
        require(change['previous_hash'] is None, 'New source proposal has a prior hash')
        require(record['id'] not in mapping, 'Duplicate source proposal')
        for field in ('title', 'publisher', 'source_type', 'published_at'):
            if record.get(field, object()) != prior[field]:
                require(defer_conflicts, 'Exact URL has conflicting source metadata: ' + field)
                conflicts.append({'canonical_id': ident, 'reason': 'Exact URL has conflicting source metadata: ' + field})
        if not isinstance(record.get('accessed_at'), str):
            require(defer_conflicts, 'Source inspection date missing or invalid')
            conflicts.append({'canonical_id': ident, 'reason': 'Source inspection date missing or invalid'})
        elif record['accessed_at'] < prior['accessed_at']:
            require(defer_conflicts, 'Source inspection date regressed')
            conflicts.append({'canonical_id': ident, 'reason': 'Source inspection date regressed'})
        incoming_id = record['id']
        mapping[incoming_id] = ident
        for field in ('claim_scope', 'limitations'):
            if isinstance(record.get(field), list) and all(isinstance(v, str) for v in record[field]):
                record[field] = list(dict.fromkeys(prior[field] + record[field]))
            else:
                require(defer_conflicts, 'Source history bundle missing or invalid: ' + field)
                conflicts.append({'canonical_id': ident, 'reason': 'Source history bundle missing or invalid: ' + field})
        record['id'] = ident
        change['previous_hash'] = record_hash(prior)
        change['identity_key'] = None
        repairs.append({'incoming_id': incoming_id, 'canonical_id': ident,
                        'url': record['url'], 'previous_hash': change['previous_hash']})
    result = remap_refs(result, mapping)
    groups = {}
    ambiguous_groups = set()
    for ident, group in result['source_groups'].items():
        ident = mapping.get(ident, ident)
        if ident in groups and groups[ident] != group:
            require(defer_conflicts, 'Conflicting source independence groups')
            conflicts.append({'canonical_id': ident, 'reason': 'Conflicting source independence groups'})
            ambiguous_groups.add(ident)
        groups[ident] = group
    groups = {i: g for i, g in groups.items() if i not in ambiguous_groups}
    result['source_groups'] = groups
    identities = [(c['kind'], c['record']['id']) for c in result['changes']]
    require(len(identities) == len(set(identities)), 'Reconciliation produced duplicate proposals')
    # The old URL claim bundles are retained; edited fields need honest accounting.
    return result, {'reference_mapping': mapping, 'source_repairs': repairs,
                    'source_conflicts': conflicts,
                    'status': 'identity_reconciled_pending_structure_and_evidence_review'}


def main():
    from tools import research_batch as batch
    from tools.git_baselines import git_state
    from tools.research_intake import private_path, retain, run_lock
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--assignment', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--bytes', type=int, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    packet_path = private_path(root, args.packet)
    raw = packet_path.read_bytes()
    require(len(raw) == args.bytes and len(raw) <= batch.MAX_BYTES and sha256(raw).hexdigest() == args.sha256,
            'Original packet bytes/hash differ')
    packet, _ = batch.load_json(packet_path)
    assignment, _ = batch.load_json(private_path(root, args.assignment))
    # Verify whole packet and trusted identity before producing a derived copy.
    batch.validate_schema(packet, 'research-batch.schema.json')
    require(packet['assignment_id'] == assignment['assignment_id'] and
            packet['baseline_commit'] == assignment['baseline_commit'], 'Untrusted assignment/baseline')
    baseline = git_state(assignment['baseline_commit'])
    normalized, report = reconcile_sources(packet, baseline)
    derived = (json.dumps(normalized, ensure_ascii=False, indent=2) + '\n').encode()
    report.update(original_sha256=args.sha256, normalized_sha256=sha256(derived).hexdigest())
    try:
        compiled = batch.compile_batch(normalized, assignment, baseline)
        report['compilation'] = {'status': 'structure_valid_pending_evidence_review',
                                 'changes': len(compiled['changes']), 'completion': compiled['completion']}
    except (ValueError, KeyError) as exc:
        report['compilation'] = {'status': 'rejected', 'reason': str(exc)}
    destination = private_path(root, args.destination)
    with run_lock(private_path(root, destination / 'reconcile.lock')):
        retain(destination, 'original.json', raw)
        retain(destination, 'normalized.json', derived)
        retain(destination, 'reconciliation.json', (json.dumps(report, indent=2) + '\n').encode())
    # Detailed reasons stay in the ignored report, never public stdout.
    print(json.dumps({'status': report['compilation']['status'], 'identity_repairs': len(report['source_repairs']),
                      'original_sha256': args.sha256, 'normalized_sha256': report['normalized_sha256']}))
    return 2 if report['compilation']['status'] == 'rejected' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError, RecursionError, subprocess.CalledProcessError):
        print('Reconciliation failed; check private input and trusted assignment.', file=sys.stderr)
        sys.exit(1)
