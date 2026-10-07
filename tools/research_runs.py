"""Bounded research accounting. Local data only; never certifies evidence quality."""
from copy import deepcopy
from datetime import date
from hashlib import sha256
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.knowledge import ROOT, canonical, history, read


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def state_hash(state):
    return digest([[kind, ident, value] for (kind, ident), value in sorted(state.items())
                   if kind != 'research_run'])


def baseline_state(revisions, revision_id):
    """Replay through an exact journal entry, including multiple edits on one day."""
    state = {}
    for revision in revisions:
        key = (revision['entity_type'], revision['entity_id'])
        if revision['value'] is None:
            state.pop(key, None)
        else:
            state[key] = deepcopy(revision['value'])
        if revision['id'] == revision_id:
            return state
    raise ValueError('Unknown baseline revision ' + revision_id)


def task_rubric_errors(tasks):
    errors = []
    ids = {task['id'] for task in tasks}
    for task in tasks:
        for field in ['scope', 'rubric_version', 'inclusion_rules', 'exclusion_rules', 'examples']:
            if not task.get(field):
                errors.append(task['id'] + ': current task needs ' + field)
        neighbors = task.get('neighboring_task_ids')
        if neighbors is None or set(neighbors) - (ids - {task['id']}):
            errors.append(task['id'] + ': invalid neighboring tasks')
    return errors


def leaves(value, path):
    """Lists remain atomic factual bundles; never split a broad claim into tags."""
    if isinstance(value, dict) and value:
        for key, nested in sorted(value.items()):
            if key not in {'id', 'schema_version', 'verified_at', 'evidence_ids', 'source_ids',
                           'supporting_evidence_ids', 'contradictory_evidence_ids'}:
                escaped = key.replace('~', '~0').replace('/', '~1')
                yield from leaves(nested, path + '/' + escaped)
    else:
        yield path, value


def field_manifest(state, target_ids, contract):
    rows = []
    for model_id in sorted(target_ids):
        model = state[('model', model_id)]
        linked = {}
        for kind in ['access', 'price', 'benchmark', 'behavior', 'release']:
            linked[kind] = [(ident, record) for (typ, ident), record in sorted(state.items())
                            if typ == kind and (record.get('model_id') == model_id
                                                or model_id in record.get('model_ids', []))]
        provider_ids = {row.get('provider_id') for kind in ['access', 'price']
                        for _, row in linked[kind]} - {None}
        linked['provider'] = [(ident, state[('provider', ident)]) for ident in sorted(provider_ids)]
        linked['model'] = [(model_id, model)]
        for kind, groups in contract['field_groups'].items():
            for domain, fields in groups.items():
                if not linked[kind]:
                    rows.append({'model_id': model_id, 'domain': domain, 'entity_type': 'inventory',
                                 'entity_id': model_id, 'path': '/' + kind,
                                 'baseline_value_hash': digest([])})
                for ident, record in linked[kind]:
                    for field in fields:
                        # Absent expected fields remain explicit pending work, including nulls.
                        for path, value in leaves(record.get(field), '/' + field):
                            rows.append({'model_id': model_id, 'domain': domain, 'entity_type': kind,
                                         'entity_id': ident, 'path': path,
                                         'baseline_value_hash': digest(value)})
    return rows


def pending_check(identity):
    return {**identity, 'result': 'not_checked', 'checked_at': None, 'rationale': '',
            'evidence_ids': [], 'search_references': [], 'conditions': [],
            'remaining_gaps': ['Pending actual source investigation'], 'blocked_reason': None}


def required_fields(state, targets, contract, candidate=None):
    rows = field_manifest(state, targets, contract)
    if candidate is not None:
        keys = ['model_id', 'domain', 'entity_type', 'entity_id', 'path']
        known = {tuple(row[k] for k in keys) for row in rows}
        for row in field_manifest(candidate, targets, contract):
            if tuple(row[k] for k in keys) not in known:
                # Newly discovered records/fields have no baseline value.
                rows.append({**row, 'baseline_value_hash': digest(None)})
    return rows


def make_run(state, revision_id, base_commit, run_id, targets, bounds, created_at):
    targets = sorted(set(targets))
    catalog = sorted(ident for kind, ident in state if kind == 'model')
    if not targets or not set(targets) <= set(catalog):
        raise ValueError('Targets must be exact catalog model IDs')
    contract = state[('research_contract', 'research-contract-v1')]
    tasks = sorted((row for (kind, _), row in state.items() if kind == 'task'), key=lambda r: r['id'])
    if task_rubric_errors(tasks) or any(t['rubric_version'] != contract['rubric_version'] for t in tasks):
        raise ValueError('Current task definitions must match the contract rubric')
    return {'schema_version': '1.0', 'id': run_id, 'contract_id': contract['id'],
            'base_commit': base_commit, 'baseline_revision_id': revision_id,
            'baseline_hash': state_hash(state), 'rubric_hash': digest(tasks),
            'created_at': created_at, 'target_model_ids': targets, 'bounds': bounds,
            'domain_checks': [pending_check({'model_id': ident, 'domain': domain})
                              for ident in catalog for domain in contract['domains']],
            'field_checks': [pending_check(row) for row in field_manifest(state, targets, contract)],
            'task_decisions': [pending_check({'model_id': ident, 'task_id': task['id'],
                                            'applicability': 'not_checked', 'judgment_ids': [],
                                            'confidence_rationale': ''})
                               for ident in targets for task in tasks if task['status'] == 'active'],
            'source_checks': [pending_check({'model_id': ident, 'category': category})
                              for ident in targets for category in contract['source_categories']]}


def run_errors(run, state, evidence_state=None):
    """Validate completeness accounting against the frozen base, not the latest catalog."""
    errors = []
    contract = state.get(('research_contract', run['contract_id']))
    if not contract:
        return ['Run contract missing from baseline']
    if state_hash(state) != run['baseline_hash']:
        errors.append('Run baseline hash differs')
    tasks = sorted((row for (kind, _), row in state.items() if kind == 'task'), key=lambda r: r['id'])
    if digest(tasks) != run['rubric_hash']:
        errors.append('Run rubric hash differs')
    catalog = {ident for kind, ident in state if kind == 'model'}
    targets = set(run['target_model_ids'])
    if not targets or not targets <= catalog:
        return errors + ['Run targets are not exact baseline models']
    if set(run['bounds']['source_categories']) != set(contract['source_categories']):
        errors.append('Run must declare every required source category')
    evidence = evidence_state if evidence_state is not None else state
    expected_fields = required_fields(state, targets, contract, evidence)
    sources = {ident: row for (kind, ident), row in evidence.items() if kind == 'source'}
    observations = {ident: row for (kind, ident), row in evidence.items() if kind == 'observation'}
    groups = [
        ('domain_checks', ['model_id', 'domain'],
         [{'model_id': ident, 'domain': domain} for ident in sorted(catalog) for domain in contract['domains']]),
        ('field_checks', ['model_id', 'domain', 'entity_type', 'entity_id', 'path', 'baseline_value_hash'], expected_fields),
        ('task_decisions', ['model_id', 'task_id'],
         [{'model_id': ident, 'task_id': task['id']} for ident in sorted(targets)
          for task in tasks if task['status'] == 'active']),
        ('source_checks', ['model_id', 'category'],
         [{'model_id': ident, 'category': category} for ident in sorted(targets) for category in contract['source_categories']])]
    for name, keys, expected in groups:
        def identity(row):
            return tuple(row[k] for k in keys)
        found = [identity(row) for row in run[name]]
        if len(found) != len(set(found)) or set(found) != {identity(row) for row in expected}:
            errors.append(name + ': checklist omitted, duplicated or altered baseline entries')
        for row in run[name]:
            label = name + ' ' + row['model_id']
            result = row['result']
            if name == 'domain_checks' and row['model_id'] not in targets and result != 'not_checked':
                errors.append(label + ': non-target domain must stay not_checked')
            if result == 'not_checked':
                if row['checked_at'] or row['evidence_ids'] or row['search_references'] or row['rationale'] or row['blocked_reason']:
                    errors.append(label + ': unchecked cannot claim investigation')
                if not row['remaining_gaps']:
                    errors.append(label + ': unchecked needs a pending gap')
                if name == 'task_decisions' and (row['applicability'] != 'not_checked' or row['judgment_ids'] or row['confidence_rationale']):
                    errors.append(label + ': unchecked task cannot assert a decision')
                continue
            checked = row['checked_at']
            if not checked or checked < run['created_at'] or checked > date.today().isoformat():
                errors.append(label + ': actual check date must be within the run')
            if not row['rationale'].strip():
                errors.append(label + ': investigated result needs rationale')
            if result == 'blocked' and not row['blocked_reason']:
                errors.append(label + ': blocked needs a reason')
            if result != 'blocked' and row['blocked_reason']:
                errors.append(label + ': blocker must use blocked result')
            if result != 'blocked' and not row['evidence_ids'] and not row['search_references']:
                errors.append(label + ': investigated result needs source/search references')
            if result != 'blocked' and not row['evidence_ids'] and row['search_references'] and all(
                    search['outcome'] == 'blocked' for search in row['search_references']):
                errors.append(label + ': failed searches remain blocked, not investigated unknown')
            for ident in row['evidence_ids']:
                expanded = observations.get(ident, {}).get('source_ids', [ident])
                if not expanded:
                    errors.append(label + ': editorial observation cannot establish a source check ' + ident)
                for source_id in expanded:
                    source = sources.get(source_id)
                    if not source or not checked or source['accessed_at'] < checked or source['accessed_at'] > date.today().isoformat():
                        errors.append(label + ': source inspection missing, predates check, or is in the future ' + source_id)
            for search in row['search_references']:
                if search['checked_at'] != checked:
                    errors.append(label + ': search/check dates differ')
            if result in {'unknown', 'blocked'} and not row['remaining_gaps']:
                errors.append(label + ': unresolved result needs remaining gaps')
            if result in {'not_applicable', 'excluded'} and not row['evidence_ids']:
                errors.append(label + ': exclusion needs positive mismatch evidence; absence is unknown')
            if name == 'source_checks' and result == 'checked':
                source_ids = [source_id for ident in row['evidence_ids']
                              for source_id in observations.get(ident, {}).get('source_ids', [ident])]
                category = row['category'].replace('_', '-')
                if not any(sources.get(ident, {}).get('source_type') == category for ident in source_ids):
                    errors.append(label + ': checked category needs an inspected source of that category')
            if name == 'field_checks' and result == 'value' and not row['evidence_ids']:
                errors.append(label + ': factual value needs inspected evidence')
            if name == 'field_checks' and result == 'value' and row['entity_type'] != 'inventory':
                actual = evidence.get((row['entity_type'], row['entity_id']))
                for part in row['path'].split('/')[1:]:
                    key = part.replace('~1', '/').replace('~0', '~')
                    actual = actual.get(key) if isinstance(actual, dict) else None
                if actual is None:
                    errors.append(label + ': absent/null factual value must remain unknown')
            if name == 'task_decisions':
                applicability = row['applicability']
                if ((result == 'excluded') != (applicability == 'excluded') or
                        (result == 'assessed' and applicability != 'applicable') or
                        (result == 'unknown' and applicability not in {'unknown', 'applicable'})):
                    errors.append(label + ': task result/applicability differ')
                if result == 'assessed':
                    judgments = {j['id']: j for j in evidence[('model', row['model_id'])]['capabilities']}
                    if not row['judgment_ids'] or not row['confidence_rationale'].strip() or not row['evidence_ids']:
                        errors.append(label + ': assessed task needs judgments and confidence rationale')
                    for ident in row['judgment_ids']:
                        judgment = judgments.get(ident)
                        if not judgment or row['task_id'] not in judgment['task_ids']:
                            errors.append(label + ': assessment needs a direct exact-model task judgment ' + ident)
                elif row['judgment_ids']:
                    errors.append(label + ': non-assessed task cannot endorse judgments')
    for model_id in targets:
        searches = {(search['checked_at'], search['query'])
                    for name, _, _ in groups for row in run[name] if row['model_id'] == model_id
                    for search in row['search_references']}
        if len(searches) > run['bounds']['max_searches_per_model']:
            errors.append(model_id + ': declared search budget exceeded')
    return errors


def completion(run):
    """Call only after schema and run_errors pass; a checkbox cannot override this."""
    targets = set(run['target_model_ids'])
    rows = [row for name in ['domain_checks', 'field_checks', 'task_decisions', 'source_checks']
            for row in run[name] if row['model_id'] in targets]
    pending = sum(row['result'] == 'not_checked' for row in rows)
    blocked = sum(row['result'] == 'blocked' for row in rows)
    return {'complete': not pending and not blocked, 'pending': pending, 'blocked': blocked,
            'investigated_unknown': sum(row['result'] == 'unknown' for row in rows),
            'non_target_domains_not_checked': sum(row['model_id'] not in targets for row in run['domain_checks'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    scaffold = commands.add_parser('scaffold')
    scaffold.add_argument('--id', required=True)
    scaffold.add_argument('--models', nargs='+', required=True)
    scaffold.add_argument('--max-minutes-per-model', type=int, required=True)
    scaffold.add_argument('--max-searches-per-model', type=int, required=True)
    scaffold.add_argument('--output', type=Path, required=True)
    inspect = commands.add_parser('check')
    inspect.add_argument('path', type=Path)
    inspect.add_argument('--require-complete', action='store_true')
    extend = commands.add_parser('extend')
    extend.add_argument('path', type=Path)
    extend.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    revisions = history(ROOT)
    current = {key: record for key, (_, record) in canonical(ROOT).items()}
    from jsonschema import Draft202012Validator, FormatChecker
    schema = json.loads((ROOT / 'schema/research-run-record.schema.json').read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    if args.command == 'scaffold':
        if baseline_state(revisions, revisions[-1]['id']) != current:
            raise ValueError('Capture canonical changes before creating a run')
        if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip():
            raise ValueError('Commit the reviewed baseline before creating a run; Git worktree must be clean')
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        contract = current[('research_contract', 'research-contract-v1')]
        run = make_run(current, revisions[-1]['id'], commit, args.id, args.models,
                       {'max_minutes_per_model': args.max_minutes_per_model,
                        'max_searches_per_model': args.max_searches_per_model,
                        'source_categories': contract['source_categories']}, date.today().isoformat())
        validator.validate(run)
        # Exclusive create: never overwrite a completed or partially researched packet.
        with args.output.open('x', encoding='utf-8') as output:
            import yaml
            yaml.safe_dump(run, output, sort_keys=False, allow_unicode=True)
        print(json.dumps(completion(run)))
    else:
        run = read(args.path)
        validator.validate(run)
        baseline = baseline_state(revisions, run['baseline_revision_id'])
        if args.command == 'extend':
            contract = baseline[('research_contract', run['contract_id'])]
            keys = ['model_id', 'domain', 'entity_type', 'entity_id', 'path', 'baseline_value_hash']
            known = {tuple(row[k] for k in keys) for row in run['field_checks']}
            for row in required_fields(baseline, run['target_model_ids'], contract, current):
                if tuple(row[k] for k in keys) not in known:
                    run['field_checks'].append(pending_check(row))
            validator.validate(run)
            errors = run_errors(run, baseline, current)
            if errors:
                print('\n'.join(errors))
                return 1
            with args.output.open('x', encoding='utf-8') as output:
                import yaml
                yaml.safe_dump(run, output, sort_keys=False, allow_unicode=True)
            print(json.dumps(completion(run)))
            return 0
        errors = run_errors(run, baseline, current)
        if errors:
            print('\n'.join(errors))
            return 1
        report = completion(run)
        print(json.dumps(report))
        return int(args.require_complete and not report['complete'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
