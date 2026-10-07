"""Current task definitions are concrete; historical payloads remain schema-valid."""
from copy import deepcopy
import json

from jsonschema import Draft202012Validator
import pytest

from tools.knowledge import ROOT, read


TASK_IDS = {
    'coding.scoped_edit', 'coding.debugging', 'coding.architecture',
    'coding.refactoring', 'coding.tests', 'coding.review',
    'coding.repository_work', 'coding.frontend',
    'agent.long_horizon', 'agent.tool_use', 'agent.computer_use',
    'reasoning.general', 'reasoning.math', 'reasoning.scientific',
    'research.fact_check', 'research.synthesis',
    'language.writing', 'language.summarization', 'language.instruction_following',
    'language.translation', 'language.multilingual_chat',
    'knowledge.extraction', 'knowledge.classification', 'knowledge.rag', 'knowledge.retrieval',
    'context.retrieval', 'context.reasoning',
    'vision.question_answering', 'vision.grounding',
    'image.generation', 'image.editing',
    'audio.understanding', 'audio.speech_generation', 'audio.conversation',
    'video.generation', 'video.editing', 'music.generation',
}
RULE_FIELDS = ('inclusion_rules', 'exclusion_rules', 'examples')


def tasks():
    return read(ROOT / 'data/capability-taxonomy.yaml')['capabilities']


def validator():
    schema = json.loads((ROOT / 'schema/task-record.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_current_task_rubrics_are_complete_and_distinctive():
    records = tasks()
    assert len(records) == len(TASK_IDS) == 37
    assert {record['id'] for record in records} == TASK_IDS
    assert len({record['scope'] for record in records}) == len(records)
    for record in records:
        assert record['rubric_version'] == '1.1'
        assert record['status'] == 'active'
        assert record['label'].strip() and record['scope'].strip()
        assert 'Task only;' not in record['scope']
        for field in RULE_FIELDS:
            values = record[field]
            assert isinstance(values, list) and values
            assert all(isinstance(value, str) and value.strip() for value in values)
            assert len(values) == len(set(values))
    for field in RULE_FIELDS:
        assert len({tuple(record[field]) for record in records}) == len(records)


def test_neighbors_resolve_to_distinct_current_task_ids():
    for record in tasks():
        neighbors = record['neighboring_task_ids']
        assert neighbors and len(neighbors) == len(set(neighbors))
        assert record['id'] not in neighbors
        assert set(neighbors) <= TASK_IDS


def test_schema_accepts_current_rubrics_and_historical_four_field_tasks():
    check = validator()
    for record in tasks():
        check.validate(record)
        historical = {key: record[key] for key in ('id', 'label', 'scope', 'status')}
        historical['scope'] = 'Task only; cost, deployment, modality, effort and harness belong in conditions.'
        check.validate(historical)


@pytest.mark.parametrize('field', [*RULE_FIELDS, 'neighboring_task_ids'])
def test_schema_rejects_empty_rubric_lists_when_present(field):
    record = deepcopy(tasks()[0])
    record[field] = []
    assert list(validator().iter_errors(record))


@pytest.mark.parametrize('field, value', [
    ('rubric_version', '2.0'),
    ('inclusion_rules', 'Use a specific task definition.'),
    ('exclusion_rules', ['']),
    ('examples', [None]),
    ('neighboring_task_ids', ['not-a-task-id']),
])
def test_schema_rejects_malformed_rubric_fields(field, value):
    record = deepcopy(tasks()[0])
    record[field] = value
    assert list(validator().iter_errors(record))
