"""Mechanical contract parity and safety regression tests; no real research."""
from copy import deepcopy
from datetime import datetime
import pytest
from test_research_batch import baseline, fixture, MID, SID, TODAY, inspected
from tools import research_batch as batch, research_partial as partial, research_scoped as scoped
from tools.research_fields import changed_fields, digest, leaves, pointer, required_fields
from tools.research_runs import pending_check
from tools.research_authoring import packet_errors


def behavior_packet(packet, baseline):
    record = deepcopy(next(r for (k, _), r in baseline.items() if k == 'behavior'))
    record.update(id='new:synthetic-behavior', model_ids=[MID], observed_at=TODAY,
                  supporting_evidence_ids=[SID], contradictory_evidence_ids=[])
    if record.get('fix'):
        record['fix']['evidence_ids'] = []
    change = dict(kind='behavior', record=record, previous_hash=None, identity_key='synthetic-behavior',
                  evidence_ids=[SID], checked_paths=sorted(changed_fields({}, record)), rationale='Synthetic incident.')
    packet['changes'].append(change)
    candidate = {**baseline, **{(c['kind'], c['record']['id']): c['record'] for c in packet['changes']}}
    fields = packet['research_run']['field_checks']
    keys = ('model_id', 'domain', 'entity_type', 'entity_id', 'path')
    known = {tuple(r[k] for k in keys) for r in fields}
    contract = baseline['research_contract', 'research-contract-v1']
    for row in required_fields(baseline, [MID], contract, candidate):
        if tuple(row[k] for k in keys) in known:
            continue
        row = pending_check(row)
        actual = pointer(candidate.get((row['entity_type'], row['entity_id']), {}), row['path'])
        inspected(row, 'value' if actual is not None else 'unknown')
        if actual is None:
            row['remaining_gaps'] = ['Synthetic unknown.']
        fields.append(row)
    return record


def test_full_delta_survives_partial_projection(fixture, baseline):
    packet, assignment = fixture
    original = deepcopy(packet)
    behavior_packet(packet, baseline)
    before = deepcopy(packet)
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['deferred_units'] == 0
    rows = [r for r in result['selected_packet']['research_run']['field_checks']
            if r['entity_type'] == 'behavior' and r['path'] == '/model_ids']
    assert len(rows) == 1 and rows[0]['result'] == 'value' and rows[0]['evidence_ids'] == [SID]
    assert rows[0]['baseline_value_hash'] == digest(None)
    assert packet == before and original['changes'] == packet['changes'][:2]


def test_authoring_and_receiver_both_require_supplemental_path(fixture, baseline):
    packet, assignment = fixture
    record = behavior_packet(packet, baseline)
    packet['changes'][-1]['checked_paths'].remove('/model_ids')
    assert any('/model_ids' in error for error in packet_errors(packet, baseline))
    with pytest.raises(ValueError, match='checked_paths'):
        batch.compile_batch(packet, assignment, baseline)


def test_new_nulls_are_unknown_but_cleared_existing_values_need_checks():
    assert changed_fields({}, {'id': 'x', 'harness': None}) == {}
    assert changed_fields({'harness': 'old'}, {'harness': None}) == {'/harness': None}
    assert changed_fields({}, {'model_ids': [], 'source_ids': ['src-x']}) == {'/model_ids': []}
    assert list(leaves({'a/b': {'x~y': [1, 2]}}, '')) == [('/a~1b/x~0y', [1, 2])]


def test_baseline_hash_for_supplemental_existing_field(baseline):
    state = deepcopy(baseline)
    state['behavior', 'behavior-0000000000000001'] = {'id': 'behavior-0000000000000001', 'model_ids': [MID]}
    candidate = deepcopy(state)
    candidate['behavior', 'behavior-0000000000000001']['model_ids'] = [MID, 'synthetic-other']
    rows = required_fields(state, [MID], state['research_contract', 'research-contract-v1'], candidate)
    row = next(r for r in rows if r['entity_id'] == 'behavior-0000000000000001' and r['path'] == '/model_ids')
    assert row['baseline_value_hash'] == digest([MID])


def test_discovery_only_source_inspection_does_not_credit_model_categories(fixture, baseline):
    packet, assignment = fixture
    category = next(r for r in packet['research_run']['source_checks'] if r['category'] == 'primary')
    category.update(pending_check({k: category[k] for k in ('model_id', 'category')}))
    discovery = packet['discovery_checks'][0]
    discovery.update(result='checked', checked_at=TODAY, rationale='Synthetic official catalog inspection.',
                     evidence_ids=[SID], remaining_gaps=[])
    result = batch.compile_batch(packet, assignment, baseline)
    assert all(r['result'] == 'not_checked' for r in result['research_run']['source_checks'])
    assert result['completion']['complete'] is False


def test_discovery_route_rejects_stale_check(fixture, baseline):
    packet, assignment = fixture
    source = packet['changes'][0]
    row = deepcopy(packet['discovery_checks'][0])
    row.update(result='checked', checked_at='2000-01-01', rationale='Synthetic stale inspection.', evidence_ids=[SID], remaining_gaps=[])
    run = deepcopy(packet['research_run'])
    run['source_checks'] = []
    with pytest.raises(ValueError, match='actual date'):
        batch.validate_accounting(source, baseline, {}, {}, run, {SID: source['record']}, {},
                                  discovery_checks=[row], created=datetime.fromisoformat(packet['created_at']))


def test_source_envelope_rule_is_in_schema_and_helper(fixture, baseline):
    packet, _ = fixture
    packet['changes'][0]['evidence_ids'] = []
    with pytest.raises(ValueError, match='Schema'):
        batch.validate_schema(packet, 'research-batch.schema.json')
    assert any('own inspection ID' in error for error in packet_errors(packet, baseline))


@pytest.mark.parametrize('schema', ['research-run-record.schema.json', 'research-scope-run.schema.json', 'task-assessment-record.schema.json'])
def test_exclusion_rule_is_explicit_in_schemas(schema):
    import json
    from jsonschema import Draft202012Validator
    document = json.loads((batch.ROOT / 'schema' / schema).read_text())
    rule = (document if schema.startswith('task-') else document['properties']['task_decisions']['items'])['allOf'][-1]
    validator = Draft202012Validator(rule)
    validator.validate({'result': 'excluded', 'applicability': 'excluded', 'judgment_ids': []})
    assert list(validator.iter_errors({'result': 'excluded', 'applicability': 'excluded', 'judgment_ids': ['judgment-x']}))


def test_envelope_citation_cannot_disappear_from_permanent_record(fixture, baseline):
    packet, _ = fixture
    record = behavior_packet(packet, baseline)
    record['supporting_evidence_ids'] = []
    state = {**baseline, **{(c['kind'], c['record']['id']): c['record'] for c in packet['changes']}}
    with pytest.raises(ValueError, match='permanent record citations'):
        batch.validate_support(packet['changes'][-1], baseline, {i:r for (k,i),r in state.items() if k == 'source'},
                               {i:r for (k,i),r in state.items() if k == 'observation'}, packet['research_run'],
                               datetime.fromisoformat(packet['created_at']))


def test_registered_url_reuse_is_checked_against_full_baseline(fixture, baseline):
    packet, _ = fixture
    source = packet['changes'][0]
    source['record']['id'] = 'new:collision'
    source['evidence_ids'] = ['new:collision']
    assert any('registered URL' in error for error in packet_errors(packet, baseline))


@pytest.mark.parametrize('result', ['value', 'not_checked', 'blocked'])
def test_model_preflight_keeps_entity_identity_after_checking_findings(fixture, baseline, result):
    packet, _ = fixture
    row = next(r for r in packet['research_run']['field_checks']
               if r['entity_type'] == 'model' and r['entity_id'] == MID and r['path'] == '/notes')
    row['result'] = result
    before_packet, before_baseline = deepcopy(packet), deepcopy(baseline)
    errors = packet_errors(packet, baseline)
    missing = f'model {MID}: changed field lacks linked investigation: /notes'
    assert (missing in errors) == (result != 'value')
    if result == 'value':
        assert errors == []
    assert packet == before_packet and baseline == before_baseline


def test_model_preflight_still_rejects_stable_finding_scope_changes(fixture, baseline):
    packet, _ = fixture
    finding = packet['changes'][1]['record']['capabilities'][0]
    finding['related_task_ids'].append('synthetic-other-task')
    errors = packet_errors(packet, baseline)
    assert f'model {MID}: stable finding scope reassigned: {finding["id"]}' in errors
    assert f'model {MID}: changed field lacks linked investigation: /notes' not in errors


@pytest.mark.parametrize('checked_at', [TODAY, '2000-01-01'])
def test_partial_projection_maps_new_discovery_sources_without_model_credit(fixture, baseline, checked_at):
    packet, assignment = fixture
    source = deepcopy(packet['changes'][0])
    source['record'].update(id='new:synthetic-discovery-catalog', url='https://example.com/synthetic-catalog')
    source.update(previous_hash=None, identity_key='synthetic-discovery-catalog',
                  evidence_ids=[source['record']['id']])
    packet['changes'].append(source)
    discovery = packet['discovery_checks'][0]
    discovery.update(result='checked', checked_at=checked_at, rationale='Synthetic official catalog inspection.',
                     evidence_ids=[source['record']['id']], remaining_gaps=[])
    before_packet, before_assignment, before_baseline = deepcopy(packet), deepcopy(assignment), deepcopy(baseline)
    result = partial.compile_partial(packet, assignment, baseline)
    valid = checked_at == TODAY
    assert result['candidate_units'] == (3 if valid else 2)
    assert result['deferred_units'] == (0 if valid else 1)
    assert (result['selected_packet']['discovery_checks'][0]['result'] == 'checked') == valid
    selected_sources = [c for c in result['compiled']['changes'] if c['kind'] == 'source']
    assert any(c['record']['url'] == source['record']['url'] for c in selected_sources) == valid
    if valid:
        allocated_id = next(c['record']['id'] for c in selected_sources if c['record']['url'] == source['record']['url'])
        assert allocated_id.startswith('src-')
        assert result['selected_packet']['discovery_checks'][0]['evidence_ids'] == [source['record']['id']]
        for row in result['compiled']['research_run']['source_checks']:
            assert allocated_id not in row['evidence_ids']
        assert not any(r['collection'] == 'discovery_checks' for r in result['accounting_projection'])
    assert result['compiled']['completion']['complete'] is False
    assert packet == before_packet and assignment == before_assignment and baseline == before_baseline
