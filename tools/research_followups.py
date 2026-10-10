"""Public research gaps and immutable assignment inputs; no evidence certification."""
from copy import deepcopy
from datetime import date
from hashlib import sha256
import argparse
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
from urllib.parse import parse_qsl, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jsonschema import Draft202012Validator, FormatChecker
from tools.knowledge import ROOT


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def followup_id(record):
    """Descriptions, evidence, priority and dates can evolve without duplicating a gap."""
    key = {name: record[name] for name in ['issue_key', 'category']}
    for name in ['model_ids', 'provider_ids', 'task_ids']:
        key[name] = sorted(record[name])
    key['fields'] = sorted(record['fields'], key=lambda field: encoded(field))
    return 'research-followup-' + sha256(encoded(key)).hexdigest()[:16]


def public_url(url):
    try:
        parts = urlsplit(url)
        host = (parts.hostname or '').rstrip('.')
        if (parts.scheme != 'https' or not host or parts.username or parts.password
                or parts.port not in {None, 443} or '.' not in host
                or host.endswith(('.local', '.internal', '.localhost'))):
            return False
        try:
            if not ipaddress.ip_address(host).is_global:
                return False
        except ValueError:
            if not re.fullmatch(r'[a-zA-Z0-9.-]+', host) or re.fullmatch(r'[0-9.]+', host):
                return False
        keys = {key.lower() for key, _ in parse_qsl(parts.query)}
        if any(key in {'key', 'api_key', 'apikey', 'token', 'access_token', 'auth', 'auth_token',
                       'password', 'secret', 'signature', 'sig', 'credential'}
               or key.startswith(('x-amz-', 'x-goog-')) for key in keys):
            return False
        return True
    except ValueError:
        return False


def _private_content(value):
    if isinstance(value, dict):
        return any(_private_content(k) or _private_content(v) for k, v in value.items())
    if isinstance(value, list):
        return any(_private_content(v) for v in value)
    if not isinstance(value, str):
        return False
    if re.search(r'(?i)(?:(?<![a-z0-9])[a-z]:[\\/]|\\\\|\.local[\\/]|\.agents[\\/]|file://|'
                 r'drive\.google\.com|docs\.google\.com|/workspace/|/Users/|/home/|'
                 r'sk-[a-z0-9]{20,}|ghp_[a-z0-9]{20,}|BEGIN .*PRIVATE KEY)', value):
        return True
    return any(not public_url(url.rstrip('.,;')) for url in re.findall(r'\b[a-z]+://[^\s<>]+', value))


def followup_errors(records, state):
    """Validate accounting/provenance. Actual source review remains a separate step."""
    schema = json.loads((ROOT / 'schema/research-followup-record.schema.json').read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors, valid = [], {}
    today = date.today().isoformat()
    for row in records:
        issues = list(validator.iter_errors(row))
        label = row.get('id', 'missing') if isinstance(row, dict) else 'missing'
        errors.extend(f'{label}: {e.message}' for e in issues)
        if issues:
            continue
        if label in valid:
            errors.append(label + ': duplicate follow-up')
        valid[label] = row
        if label != followup_id(row):
            errors.append(label + ': stable scope identity differs')
        if not (row['model_ids'] or row['provider_ids'] or row['fields']):
            errors.append(label + ': exact model, provider or field scope is required')
        if not (row['evidence_ids'] or row['urls']):
            errors.append(label + ': a public evidence reference is required')
        for name, kind in [('model_ids', 'model'), ('provider_ids', 'provider'), ('task_ids', 'task')]:
            for ident in row[name]:
                if (kind, ident) not in state:
                    errors.append(label + ': unresolved ' + name + ' ' + ident)
        for field in row['fields']:
            # Missing/null fields are valid research gaps; their owning record must exist.
            owner = state.get((field['entity_type'], field['entity_id']))
            if owner is None:
                errors.append(label + ': unresolved field owner')
            elif field['entity_type'] == 'model' and field['entity_id'] not in row['model_ids']:
                errors.append(label + ': field model is outside the declared scope')
            elif field['entity_type'] == 'provider' and field['entity_id'] not in row['provider_ids']:
                errors.append(label + ': field provider is outside the declared scope')
            elif owner.get('model_id') and owner['model_id'] not in row['model_ids']:
                errors.append(label + ': field record model is outside the declared scope')
            elif owner.get('provider_id') and owner['provider_id'] not in row['provider_ids']:
                errors.append(label + ': field record provider is outside the declared scope')
            if owner and owner.get('task_id') and owner['task_id'] not in row['task_ids']:
                errors.append(label + ': field record task is outside the declared scope')
        if row['opened_at'] > row['updated_at'] or row['updated_at'] > today:
            errors.append(label + ': invalid opening/update dates')

        def evidence_check(ids, checked):
            for ident in ids:
                observation = state.get(('observation', ident))
                expanded = observation.get('source_ids', []) if observation else [ident]
                if not expanded:
                    errors.append(label + ': editorial observation cannot establish inspection')
                for source_id in expanded:
                    source = state.get(('source', source_id))
                    if not source:
                        errors.append(label + ': unresolved evidence ' + source_id)
                    elif not public_url(source.get('url', '')) or _private_content(source.get('url', '')):
                        errors.append(label + ': evidence URL is not public')
                    elif checked and not checked <= source['accessed_at'] <= today:
                        errors.append(label + ': source inspection missing or predates check')
            if checked and (checked > row['updated_at'] or checked > today):
                errors.append(label + ': inspection date exceeds update date')

        evidence_check(row['evidence_ids'], row['source_checked_at'])
        previous_date = row['opened_at']
        for resolution in row['resolutions']:
            evidence_check(resolution['evidence_ids'], resolution['checked_at'])
            if resolution['checked_at'] < previous_date:
                errors.append(label + ': resolution history is out of order')
            previous_date = resolution['checked_at']
        if any(not public_url(url) for url in row['urls']) or _private_content(row):
            errors.append(label + ': private content or non-public URL')
    # Unknown dependencies and cycles would make next actions impossible to order.
    visiting, visited = set(), set()
    def visit(ident):
        if ident in visiting:
            errors.append(ident + ': dependency cycle')
            return
        if ident in visited:
            return
        visiting.add(ident)
        for dependency in valid[ident]['dependencies']:
            if dependency not in valid:
                errors.append(ident + ': unresolved dependency ' + dependency)
            else:
                if valid[ident]['status'] == 'resolved' and valid[dependency]['status'] != 'resolved':
                    errors.append(ident + ': cannot resolve before its dependency')
                visit(dependency)
        visiting.remove(ident)
        visited.add(ident)
    for ident in sorted(valid):
        visit(ident)
    return errors


def merge_followups(existing, proposals, state, *, reopen_ids=()):
    """Deduplicate recurrence; closures and reopenings require explicit reviewed proposals."""
    errors = followup_errors(existing, state)
    if errors:
        raise ValueError('\n'.join(errors))
    result = {row['id']: deepcopy(row) for row in existing}
    if len(result) != len(existing):
        raise ValueError('Duplicate existing follow-ups')
    seen = set()
    reopen = set(reopen_ids)
    for proposal in proposals:
        ident = proposal['id']
        if ident in seen:
            raise ValueError('Duplicate proposals')
        seen.add(ident)
        prior = result.get(ident)
        row = deepcopy(proposal)
        if prior:
            if ident != followup_id(row):
                raise ValueError('Do not change scope under a retained follow-up identity')
            if prior['status'] == 'resolved' and row['status'] == 'open' and ident not in reopen:
                # Recurring reports never erase a prior resolution or implicitly reopen it.
                continue
            if row['opened_at'] != prior['opened_at'] or row['updated_at'] < prior['updated_at']:
                raise ValueError('Do not rewrite opening dates or move updates backwards')
            history = prior['resolutions']
            if row['resolutions'][:len(history)] != history:
                raise ValueError('Preserve prior resolution evidence')
            if prior['source_checked_at'] and (not row['source_checked_at']
                    or row['source_checked_at'] < prior['source_checked_at']):
                raise ValueError('Do not erase or move inspected evidence dates backwards')
            if prior['status'] == 'open' and row['status'] == 'resolved' and len(row['resolutions']) <= len(history):
                raise ValueError('Closing a gap requires new resolution evidence')
            if ident in reopen and (prior['status'] != 'resolved' or row['status'] != 'open'
                    or not row['source_checked_at'] or not row['evidence_ids']
                    or row['updated_at'] <= prior['updated_at']
                    or row['source_checked_at'] <= history[-1]['checked_at']):
                raise ValueError('Reopening requires a later inspected public issue')
        elif ident in reopen:
            raise ValueError('Cannot reopen an absent follow-up')
        if ident in reopen and (not prior or prior['status'] != 'resolved'):
            raise ValueError('Only resolved follow-ups can be reopened')
        result[ident] = row
    if reopen - seen:
        raise ValueError('Reopening IDs require proposals')
    rows = sorted(result.values(), key=lambda row: row['id'])
    errors = followup_errors(rows, state)
    if errors:
        raise ValueError('\n'.join(errors))
    return rows


def select_followups(records, *, model_id=None, provider_id=None, task_id=None,
                     entity_type=None, entity_id=None, path=None, category=None,
                     status='open', priority=None):
    """Exact filters intersect. None for status includes retained resolutions."""
    rows = []
    for row in records:
        if any(value is not None and value not in row[key] for key, value in
               [('model_ids', model_id), ('provider_ids', provider_id), ('task_ids', task_id)]):
            continue
        if any(value is not None and row[key] != value for key, value in
               [('category', category), ('status', status), ('priority', priority)]):
            continue
        if any(value is not None for value in [entity_type, entity_id, path]) and not any(
                all(value is None or field[key] == value for key, value in
                    [('entity_type', entity_type), ('entity_id', entity_id), ('path', path)])
                for field in row['fields']):
            continue
        rows.append(deepcopy(row))
    return sorted(rows, key=lambda row: ({'high': 0, 'normal': 1, 'low': 2}[row['priority']], row['id']))


def assignment_inputs(run, state):
    """Consume only the run's frozen baseline, including related provider-only gaps."""
    from tools.research_runs import run_errors, state_hash
    schema = json.loads((ROOT / 'schema/research-run-record.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(run)
    if run['baseline_revision_id'] != 'git-' + run['base_commit']:
        raise ValueError('New assignments require a pinned public Git baseline')
    errors = run_errors(run, state)
    rows = [row for (kind, _), row in state.items() if kind == 'research_followup']
    errors += followup_errors(rows, state)
    if errors:
        raise ValueError('\n'.join(errors))
    targets = set(run['target_model_ids'])
    providers = {row['provider_id'] for (kind, _), row in state.items()
                 if kind in {'access', 'price'} and row.get('model_id') in targets
                 and row.get('provider_id')}
    all_rows = {row['id']: row for row in rows}
    selected = {row['id'] for row in rows if row['status'] == 'open' and
                (set(row['model_ids']) & targets or
                 (not row['model_ids'] and set(row['provider_ids']) & providers))}
    direct = sorted(selected)
    def dependencies(ident):
        for dep in all_rows[ident]['dependencies']:
            if dep not in selected:
                selected.add(dep)
                dependencies(dep)
    for ident in direct:
        dependencies(ident)
    supplementary = sorted(selected - set(direct))
    return {'schema_version': '1.0', 'run_id': run['id'], 'base_commit': run['base_commit'],
            'baseline_hash': state_hash(state), 'target_model_ids': sorted(targets),
            'direct_followup_ids': direct, 'dependency_context_ids': supplementary,
            'records': [deepcopy(all_rows[ident]) for ident in sorted(selected)]}


def render_followups(rows):
    def clean(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    lines = ['# Research follow-ups', '',
             'Generated from [canonical public gaps](research-followups.yaml). '
             'An empty queue does not establish complete research. '
             'Missing evidence or failed access remains unknown.', '']
    if not rows:
        lines += ['No public follow-ups have been recorded.', '']
    for row in select_followups(rows, status=None):
        lines += ['## ' + row['id'], '',
                  f"Status: {row['status']} · Priority: {row['priority']} · Category: {row['category']}", '',
                  'Models: ' + (', '.join(row['model_ids']) or 'No model restriction'), '',
                  'Providers: ' + (', '.join(row['provider_ids']) or 'No provider restriction'), '',
                  'Tasks: ' + (', '.join(row['task_ids']) or 'No task restriction'), '',
                  'Fields: ' + ('; '.join(f"{f['entity_type']}/{f['entity_id']}{f['path']}" for f in row['fields']) or 'Whole declared scope'), '',
                  clean(row['reason']), '', 'Next action: ' + clean(row['requested_action']), '',
                  'Opened: ' + row['opened_at'] + ' · Updated: ' + row['updated_at'], '',
                  'Source inspected: ' + (row['source_checked_at'] or 'Unknown / not established'), '',
                  'Evidence IDs: ' + (', '.join(row['evidence_ids']) or 'None recorded'), '',
                  'Public URLs: ' + (' · '.join(f'[{clean(url)}]({url})' for url in row['urls']) or 'See evidence IDs'), '',
                  'Dependencies: ' + (', '.join(row['dependencies']) or 'None recorded'), '']
        for resolution in row['resolutions']:
            lines += [f"Resolution inspected {resolution['checked_at']} ({resolution['method']}): "
                      + clean(resolution['rationale']), '',
                      'Resolution evidence: ' + ', '.join(resolution['evidence_ids']), '']
    return '\n'.join(lines)


def write_assignment_inputs(run, state, destination, *, root=ROOT):
    # Reuse the intake boundary: all output remains in ignored storage without links.
    from tools.research_intake import private_path
    destination = private_path(root, destination)
    snapshot = assignment_inputs(run, state)
    prompt = ('Read and verify followups.json against followup-input-manifest.json before research.\n'
              'Investigate direct_followup_ids within the declared target scope and budget.\n'
              'dependency_context_ids preserve prerequisites; report out-of-scope work as pending.\n'
              'Keep failed access and missing evidence unknown. Do not refresh carried-forward dates.\n'
              'Do not close gaps on a checkbox: return inspected sources and a reasoned resolution.\n'
              'Resolutions remain proposals for the receiver to review; this input grants no publication authorization.\n')
    contents = {'followups.json': encoded(snapshot), 'followup-instructions.txt': prompt.encode()}
    manifest = {'schema_version': '1.0', 'run_id': run['id'], 'base_commit': run['base_commit'],
                'baseline_hash': snapshot['baseline_hash'], 'files':
                {name: {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}
                 for name, raw in sorted(contents.items())}}
    contents['followup-input-manifest.json'] = encoded(manifest)
    if destination.exists():
        from tools.research_batch import linked
        if not destination.is_dir():
            raise ValueError('Existing assignment inputs differ; retain them and use a new destination')
        if any(linked(path) for path in destination.iterdir()):
            raise ValueError('Retained inputs contain a link/reparse point')
        if ({p.name for p in destination.iterdir()} != set(contents)
                or any((destination / name).read_bytes() != raw for name, raw in contents.items())):
            raise ValueError('Existing assignment inputs differ; retain them and use a new destination')
        return manifest
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.followups-', dir=destination.parent))
    try:
        for name, raw in contents.items():
            with (staging / name).open('xb') as output:
                output.write(raw)
                output.flush()
                os.fsync(output.fileno())
        for attempt in range(5):
            private_path(root, staging)
            private_path(root, destination)
            if destination.exists():
                raise ValueError('Assignment destination appeared during staging; retain existing inputs')
            try:
                os.rename(staging, destination)
                break
            except PermissionError as error:
                # Windows scanners can briefly hold a closed file/directory.
                # Persistent failures and other permission errors still stop.
                if getattr(error, 'winerror', None) not in {5, 32} or attempt == 4:
                    raise
                time.sleep(0.05 * (2 ** attempt))
    finally:
        if staging.exists():
            private_path(root, staging)
            if not staging.resolve().is_relative_to(destination.parent.resolve()):
                raise ValueError('Staging cleanup escaped the intended directory')
            shutil.rmtree(staging)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    from tools.git_baselines import git_state
    from tools.knowledge import read
    run = read(args.run)
    schema = json.loads((ROOT / 'schema/research-run-record.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(run)
    if run['baseline_revision_id'] != 'git-' + run['base_commit']:
        raise ValueError('New assignments require a pinned public Git baseline')
    manifest = write_assignment_inputs(run, git_state(run['base_commit']), args.output)
    print(json.dumps({'run_id': manifest['run_id'], 'files': len(manifest['files'])}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
