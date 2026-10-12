"""Performance characteristics cannot assert direct or related capability mappings."""
from copy import deepcopy
import pytest

from test_research_batch import baseline, fixture, TODAY, SID, inspected
from test_research_output_contract import schemas, record_session
from test_research_search_receipts import evidence
from tools import research_batch as batch
from tools import research_output_contract as output


@pytest.fixture
def performance_packet(fixture):
    packet, assignment = fixture
    change = next(c for c in packet['changes'] if c['kind'] == 'model')
    model = change['record']
    finding = deepcopy(model['capabilities'][0])
    finding.update(id='new:synthetic-performance', scope='performance', task_ids=[], related_task_ids=[],
                   judgment='Synthetic response-latency characteristic, not a task-quality endorsement.',
                   assessment='conditional', observed_at=TODAY, supporting_evidence_ids=[SID],
                   contradictory_evidence_ids=[], scope_note='Synthetic workload context stays in prose.',
                   provenance={'origin': 'research', 'research_batch_id': 'public-source-inspection-' + TODAY,
                               'method': 'Synthetic schema fixture; no actual research or inference.'})
    model['performance_characteristics'].append(finding)
    change['checked_paths'].append('/performance_characteristics')
    row = next(r for r in packet['research_run']['field_checks'] if r['entity_type'] == 'model'
               and r['entity_id'] == model['id'] and r['path'] == '/performance_characteristics')
    inspected(row, 'value')
    return packet, assignment, finding


def test_valid_performance_finding_passes_record_gate_and_receiver(performance_packet, baseline, schemas):
    packet, assignment, _ = performance_packet
    before = deepcopy(packet)
    assert output.validate_records(packet, schemas, output.build_contract(schemas, TODAY)) == []
    compiled = batch.compile_batch(packet, assignment, baseline)
    assert not compiled['completion']['complete']
    assert packet == before


@pytest.mark.parametrize('field', ['task_ids', 'related_task_ids'])
def test_either_performance_task_array_rejected_before_delivery(performance_packet, baseline, schemas, field):
    packet, assignment, finding = performance_packet
    finding[field] = ['audio.conversation']
    before = deepcopy(packet)
    errors = output.validate_records(packet, schemas, output.build_contract(schemas, TODAY))
    assert len(errors) == 1 and errors[0]['check_id'] == 'RC04'
    assert errors[0]['path'].endswith('/' + field)
    with pytest.raises(ValueError, match='Schema'):
        batch.compile_batch(packet, assignment, baseline)
    assert packet == before


@pytest.mark.parametrize('field', ['task_ids', 'related_task_ids'])
def test_task_arrays_are_required_not_omittable(performance_packet, schemas, field):
    packet, _, finding = performance_packet
    finding.pop(field)
    errors = output.validate_records(packet, schemas, output.build_contract(schemas, TODAY))
    assert any(field in e['missing_keys'] for e in errors)


@pytest.mark.parametrize('misplacement', ['wrong_scope', 'wrong_collection'])
def test_performance_scope_and_collection_must_agree(performance_packet, baseline, schemas, misplacement):
    packet, assignment, finding = performance_packet
    if misplacement == 'wrong_scope':
        finding['scope'] = 'direct'
    else:
        model = next(c['record'] for c in packet['changes'] if c['kind'] == 'model')
        model['performance_characteristics'].remove(finding)
        model['capabilities'].append(finding)
    errors = output.validate_records(packet, schemas, output.build_contract(schemas, TODAY))
    assert any(e['check_id'] == 'RC04' and e['path'].endswith('/scope') for e in errors)
    with pytest.raises(ValueError, match='Schema'):
        batch.compile_batch(packet, assignment, baseline)


def test_correction_preserves_every_other_finding_field(performance_packet, baseline, schemas):
    packet, assignment, finding = performance_packet
    finding['related_task_ids'] = ['audio.conversation']
    before = deepcopy(finding)
    finding['related_task_ids'] = []
    assert {k: v for k, v in finding.items() if k != 'related_task_ids'} == {
        k: v for k, v in before.items() if k != 'related_task_ids'}
    assert output.validate_records(packet, schemas, output.build_contract(schemas, TODAY)) == []
    batch.compile_batch(packet, assignment, baseline)


def test_generated_requirements_show_exact_performance_rules(schemas):
    contract = output.build_contract(schemas, TODAY)
    fields = contract['records']['model']['fields']
    for name in ('task_ids', 'related_task_ids'):
        row = next(f for f in fields if f['path'] == '/performance_characteristics/*/' + name)
        assert row['required_in_parent'] and row['constraints']['maxItems'] == 0
    scope = next(f for f in fields if f['path'] == '/performance_characteristics/*/scope')
    assert scope['constraints']['const'] == 'performance'
    guide = output.render_contract(contract).decode()
    assert '| RC04 | ' + output.CHECKS['RC04'] + ' |' in guide


def test_v3_failure_reports_rc04_and_creates_no_success_receipt(performance_packet, evidence, tmp_path, schemas):
    packet, _, finding = performance_packet
    finding['related_task_ids'] = ['audio.conversation']
    session, _ = record_session(evidence, tmp_path, schemas, packet['changes'])
    with pytest.raises(ValueError, match='RC04'):
        session.schema('fixture')
    assert session.checks['schema'] == 'passed' and session.checks['records'] == 'failed'
    assert session.record_errors[0]['check_id'] == 'RC04'
    assert not session.args.receipt.exists()
