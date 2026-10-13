"""Pin every supplied premise, including exact absence, and recheck at merge."""
from pathlib import Path, PurePosixPath
import yaml
import json
from tools import research_two_phase as p

TABLES = {'data/models.yaml': 'records', 'data/access.yaml': 'records',
    'data/pricing.yaml': 'records', 'data/task-assessments.yaml': 'records',
    'evidence/sources.yaml': 'records', 'data/capability-taxonomy.yaml': 'capabilities'}

def resolve(root, selector):
    path = PurePosixPath(selector['path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('Unsafe context path')
    if str(path) not in TABLES and not (path.parts[-1] == 'profile.yaml' and
            (len(path.parts) == 4 and path.parts[0] == 'models' or len(path.parts) == 3 and path.parts[0] == 'providers')):
        raise ValueError('Context path not allowlisted')
    target = (Path(root) / str(path)).resolve()
    if not target.is_relative_to(Path(root).resolve()): raise ValueError('Context escaped repository')
    value = yaml.safe_load(target.read_text('utf-8'))
    ident = selector.get('id')
    if str(path) in TABLES and (ident is not None or selector.get('match')):
        matches = [r for r in value[TABLES[str(path)]] if (r['id'] == ident if ident is not None
            else all(r.get(key) == target for key,target in selector['match'].items()))]
        if len(matches) > 1: raise ValueError('Ambiguous context identity')
        if not matches: return {'present': False, 'record': None}
        value = matches[0]
    elif ident is not None and value.get('id') != ident:
        return {'present': False, 'record': None}
    if selector.get('fields'):
        value = {key: value[key] for key in selector['fields']}
    if selector.get('legacy_plain_value'):
        return value
    return {'present': True, 'record': value}

def supply(root, per_question):
    reads = []; selectors = {}
    for question_id, items in sorted(per_question.items()):
        for selector in items:
            identity = selector.get('id') or ('where:' + json.dumps(selector['match'],sort_keys=True,separators=(',',':'))
                if selector.get('match') else '*')
            record_id = selector['path'] + '#' + identity
            if record_id in selectors and selectors[record_id] != selector:
                raise ValueError('Conflicting selector')
            selectors[record_id] = selector
            value = resolve(root, selector)
            reads.append({'question_id': question_id, 'record_id': record_id, 'value': value,
                'sha256': p.pin(p.encoded(value))['sha256'],
                'absence_predicate': None if value['present'] else 'exact_record_absent'})
    if len({(r['question_id'], r['record_id']) for r in reads}) != len(reads):
        raise ValueError('Duplicate context premise')
    return reads, selectors

def recheck(assignment, selectors, root):
    changed = {}
    for read in assignment['context_read_set']:
        if p.pin(p.encoded(read['value']))['sha256'] != read['sha256']:
            raise ValueError('Original supplied context pin mismatch')
        if read['record_id'] not in selectors: raise ValueError('Missing context selector')
        current = resolve(root, selectors[read['record_id']])
        if p.pin(p.encoded(current))['sha256'] != read['sha256']:
            changed.setdefault(read['question_id'], []).append(read['record_id'])
    for question in assignment['questions']:
        if not any(r['question_id'] == question['id'] for r in assignment['context_read_set']):
            changed.setdefault(question['id'], []).append('missing_supplied_context')
    return changed
