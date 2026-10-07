"""One-time, guarded migration of the 2026-10-06 public baseline. No network."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'b209600f8ae44d41b70d5ed4423e239dbb9d3b6d'
TASKS = {
    'coding': ['scoped_edit', 'debugging', 'architecture', 'refactoring', 'tests', 'review', 'repository_work', 'frontend'],
    'agent': ['long_horizon', 'tool_use', 'computer_use'],
    'reasoning': ['general', 'math', 'scientific'],
    'research': ['fact_check', 'synthesis'],
    'language': ['writing', 'summarization', 'instruction_following', 'translation', 'multilingual_chat'],
    'knowledge': ['extraction', 'classification', 'rag'],
    'context': ['retrieval', 'reasoning'],
    'vision': ['question_answering', 'grounding'],
    'image': ['generation', 'editing'],
    'audio': ['understanding', 'speech_generation', 'conversation'],
    'video': ['generation', 'editing'],
    'music': ['generation'],
}
# Each row is a human-reviewed scope decision, not a split of the conclusion.
# Compound and unresolved task references are navigation only, never endorsements.
MAPPINGS = {
    'ai21-jamba2-mini': [('compound', ['knowledge.extraction', 'knowledge.rag'])],
    'qwen3-5-9b': [('compound', ['vision.question_answering', 'knowledge.extraction'])],
    'qwen3-8-2-4t-a95b': [('compound', ['coding.repository_work', 'agent.tool_use'])],
    'qwen3-8-27b': [('compound', ['coding.scoped_edit', 'vision.question_answering']), ('unresolved', ['context.reasoning'])],
    'qwen3-8-flash-next': [('compound', ['agent.tool_use', 'coding.repository_work']), ('performance', [])],
    'qwen3-coder-next': [('direct', ['coding.repository_work'])],
    'claude-fable-5-1': [('compound', ['agent.long_horizon', 'reasoning.general', 'coding.repository_work']), ('performance', [])],
    'claude-haiku-4-5': [('compound', ['coding.scoped_edit', 'language.instruction_following'])],
    'claude-opus-5-5': [('compound', ['coding.repository_work', 'research.synthesis'])],
    'claude-sonnet-5-5': [('direct', ['coding.repository_work']), ('performance', [])],
    'bfl-flux3-video': [('compound', ['video.generation', 'audio.speech_generation'])],
    'cohere-command-a-plus': [('compound', ['knowledge.rag', 'agent.tool_use']), ('compound', ['reasoning.scientific', 'coding.repository_work'])],
    'cohere-embed-5-fast': [('direct', ['context.retrieval'])],
    'cohere-embed-5-pro': [('direct', ['context.retrieval'])],
    'cohere-north-small-translate': [('direct', ['language.translation'])],
    'deepseek-v4-1-flash': [('compound', ['coding.repository_work', 'coding.review', 'agent.tool_use']), ('performance', [])],
    'deepseek-v4-pro-0813': [('compound', ['coding.repository_work', 'reasoning.general'])],
    'elevenlabs-eleven-v4': [('direct', ['audio.speech_generation'])],
    'gemini-3-1-pro-preview': [('compound', ['reasoning.scientific', 'vision.question_answering', 'context.reasoning'])],
    'gemini-3-5-flash-lite': [('compound', ['knowledge.extraction', 'knowledge.classification', 'agent.tool_use'])],
    'gemini-3-8-flash': [('compound', ['vision.question_answering', 'coding.scoped_edit']), ('direct', ['agent.long_horizon'])],
    'gemini-3-8-live': [('direct', ['audio.conversation'])],
    'gemini-3-pro-image': [('direct', ['image.generation'])],
    'gemini-omni-1-1-flash': [('direct', ['video.editing'])],
    'gemini4argon': [('compound', ['agent.long_horizon', 'coding.repository_work', 'agent.tool_use'])],
    'gemma-4-31b-it': [('compound', ['coding.repository_work', 'vision.question_answering'])],
    'lyria-3-5': [('direct', ['music.generation'])],
    'veo-3-1-generate-preview': [('direct', ['video.generation'])],
    'llama-4-maverick': [('compound', ['language.multilingual_chat', 'vision.question_answering'])],
    'llama-4-scout': [('compound', ['language.multilingual_chat', 'vision.question_answering']), ('unresolved', ['context.reasoning'])],
    'phi-4-mini-instruct': [('compound', ['language.instruction_following', 'coding.scoped_edit'])],
    'phi-4-multimodal-instruct': [('compound', ['audio.understanding', 'vision.question_answering'])],
    'phi-4-reasoning-vision-15b': [('compound', ['reasoning.math', 'vision.question_answering', 'vision.grounding'])],
    'minimax-m3': [('compound', ['coding.repository_work', 'agent.tool_use', 'context.reasoning'])],
    'devstral-small-2': [('direct', ['coding.repository_work'])],
    'ministral-3-8b': [('compound', ['language.multilingual_chat', 'knowledge.extraction', 'vision.question_answering'])],
    'mistral-large-3': [('direct', ['knowledge.rag'])],
    'mistral-medium-3-5': [('compound', ['reasoning.general', 'coding.repository_work'])],
    'mistral-small-4': [('compound', ['knowledge.extraction', 'agent.tool_use', 'language.multilingual_chat'])],
    'kimi-k3': [('compound', ['agent.long_horizon', 'coding.repository_work', 'research.synthesis'])],
    'nemotron-3-ultra': [('performance', [])],
    'gpt-6-1-sol': [('compound', ['coding.repository_work', 'context.reasoning']), ('compound', ['research.fact_check', 'research.synthesis'])],
    'gpt-6-astra': [('compound', ['coding.repository_work', 'agent.computer_use']), ('direct', ['reasoning.scientific'])],
    'gpt-6-luna': [('unresolved', ['coding.scoped_edit', 'language.instruction_following'])],
    'gpt-image-2-5-flare': [('direct', ['image.generation'])],
    'gpt-image-2-5-sunburst': [('direct', ['image.editing'])],
    'gpt-live-1': [('direct', ['audio.conversation'])],
    'gpt-oss-120b': [('unresolved', ['reasoning.general', 'agent.long_horizon'])],
    'gpt-oss-20b': [('unresolved', ['reasoning.general', 'agent.long_horizon'])],
    'gpt-realtime-2-1': [('direct', ['audio.conversation'])],
    'xai-grok-4-7': [('compound', ['coding.repository_work', 'research.synthesis']), ('performance', [])],
    'glm-5-3': [('compound', ['agent.long_horizon', 'coding.repository_work'])],
    'glm-5-3-flash': [('compound', ['vision.question_answering', 'agent.tool_use'])],
}
WARNINGS = {('cohere-command-a-plus', 1), ('qwen3-8-27b', 1), ('llama-4-scout', 1),
            ('qwen3-8-flash-next', 1), ('deepseek-v4-1-flash', 1), ('xai-grok-4-7', 1)}

class PlainDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def write_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, Dumper=PlainDumper, sort_keys=False, allow_unicode=True, width=105), encoding='utf-8', newline='\n')

def migrate():
    archive = ROOT / 'history/migrations/2026-10-07-capabilities.yaml'
    if archive.exists():
        raise SystemExit('Already migrated; original archive will not be overwritten.')
    profiles = [(p, yaml.safe_load(p.read_text(encoding='utf-8'))) for p in sorted(ROOT.glob('models/*/*/profile.yaml'))]
    assert len(profiles) == 53 and sum(len(m['capabilities']) for _, m in profiles) == 64
    assert all(m['schema_version'] == '1.0' for _, m in profiles)
    tasks = [{'id': f'{group}.{name}', 'label': f'{group.capitalize()}: {name.replace("_", " ")}',
              'scope': 'Task only; cost, deployment, modality, effort and harness belong in conditions.',
              'status': 'active'} for group, names in TASKS.items() for name in names]
    taskids = {t['id'] for t in tasks}
    originals, counts = [], Counter()
    for path, model in profiles:
        assert len(model['capabilities']) == len(MAPPINGS[model['id']])
        capabilities, performance = [], []
        rows = [(i, 'capabilities', original, mapping) for i, (original, mapping) in enumerate(zip(model['capabilities'], MAPPINGS[model['id']]))]
        rows += [(i, 'performance_characteristics', original, ('performance', [])) for i, original in enumerate(model['performance_characteristics'])]
        for position, collection, original, (scope, refs) in rows:
            assert set(refs) <= taskids
            jid = 'judgment-' + sha256(f"{BASELINE}:{model['id']}:{collection}:{position}".encode()).hexdigest()[:16]
            originals.append({'judgment_id': jid, 'model_id': model['id'], 'profile': path.relative_to(ROOT).as_posix(),
                              'original_position': position, 'original_collection': collection, 'classification': scope, 'original': deepcopy(original)})
            j = deepcopy(original)
            del j['task']
            j = {'id': jid, 'scope': scope, 'task_ids': refs if scope == 'direct' else [],
                 'related_task_ids': refs if scope != 'direct' else [],
                 'assessment': 'warning' if collection == 'capabilities' and (model['id'], position) in WARNINGS else 'conditional',
                 'scope_note': {'direct': 'One task reference; conclusion remains conditional, not an ability score.',
                     'compound': 'Original bundle retained as one claim. Related tasks are navigation, not individual conclusions.',
                     'unresolved': 'Scope needs review; the original claim does not establish a specific task ability.',
                     'performance': 'Cost, deployment or throughput observation; not a task capability.'}[scope],
                 **j, 'observed_at': '2026-10-07', 'effective_from': None,
                 'provenance': {'migration_id': 'capabilities-2026-10-07', 'original_task': original['task'],
                                'baseline_commit': BASELINE, 'original_position': position,
                                'history_path': 'history/migrations/2026-10-07-capabilities.yaml'}}
            (performance if scope == 'performance' else capabilities).append(j)
            counts[scope if collection == 'capabilities' else 'existing_performance'] += 1
        model['schema_version'] = '2.0'
        model['capabilities'], model['performance_characteristics'] = capabilities, performance
        write_yaml(path, model)
    assert counts == {'direct': 19, 'compound': 34, 'unresolved': 5, 'performance': 6, 'existing_performance': 7}, counts
    write_yaml(archive, {'schema_version': '2.0', 'id': 'capabilities-2026-10-07', 'observed_at': '2026-10-07',
                        'baseline_commit': BASELINE, 'baseline_verified_at': '2026-10-06',
                        'reason': 'Task registry and scope migration; no new capability evidence or confidence changes.',
                        'counts': dict(counts), 'records': originals})
    write_yaml(ROOT / 'data/capability-taxonomy.yaml', {'schema_version': '2.0', 'capabilities': tasks})
    schema_path = ROOT / 'schema/model-profile.schema.json'
    schema = json.loads(schema_path.read_text())
    schema['properties']['schema_version'] = {'const': '2.0'}
    old = schema['properties']['capabilities']['items']
    old['properties'].pop('task'); old['required'].remove('task')
    old['properties'].update({
        'id': {'type': 'string', 'pattern': '^judgment-[a-f0-9]{16}$'},
        'scope': {'enum': ['direct', 'compound', 'unresolved', 'performance']},
        'task_ids': {'type': 'array', 'items': {'type': 'string', 'pattern': '^[a-z]+\\.[a-z_]+$'}, 'uniqueItems': True},
        'related_task_ids': {'type': 'array', 'items': {'type': 'string', 'pattern': '^[a-z]+\\.[a-z_]+$'}, 'uniqueItems': True},
        'assessment': {'enum': ['conditional', 'warning', 'unknown', 'weak']},
        'scope_note': {'type': 'string', 'minLength': 1},
        'observed_at': {'type': 'string', 'format': 'date'},
        'effective_from': {'type': ['string', 'null'], 'format': 'date'},
        'provenance': {'type': 'object', 'required': ['migration_id', 'original_task', 'baseline_commit', 'original_position', 'history_path'],
                       'properties': {'migration_id': {'type': 'string'}, 'original_task': {'type': 'string'},
                                      'baseline_commit': {'type': 'string'}, 'original_position': {'type': 'integer', 'minimum': 0},
                                      'history_path': {'type': 'string'}}, 'additionalProperties': False},
    })
    old['required'] += ['id', 'scope', 'task_ids', 'related_task_ids', 'assessment', 'scope_note', 'observed_at', 'effective_from', 'provenance']
    schema['properties']['capabilities']['items'] = deepcopy(old)
    schema['properties']['performance_characteristics']['items'] = deepcopy(old)
    schema_path.write_text(json.dumps(schema, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'tasks': len(tasks), 'originals': len(originals), **counts}, indent=2))

if __name__ == '__main__':
    migrate()
