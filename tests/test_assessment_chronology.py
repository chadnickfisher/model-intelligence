"""Same chronology rule in portable preflight and both authoritative receivers."""
from copy import deepcopy
from datetime import date, timedelta
import pytest

from test_research_batch import baseline, fixture, MID, SID, TODAY
import test_research_scoped as scoped_fixtures
from tools import research_batch as batch, research_scoped as scoped
from tools.knowledge import record_hash
from tools.research_fields import assessment_chronology_errors
from tools.research_authoring import packet_errors


@pytest.fixture
def dated_packet(fixture, baseline):
    packet, assignment = fixture
    original = next(r for (kind, _), r in baseline.items()
                    if kind == 'task_assessment' and r['model_id'] == MID and 'aggregate' in r)
    record = deepcopy(original)
    record.update(checked_at=TODAY, evidence_ids=[SID], conditions=['Synthetic exact-model native route.'])
    record['aggregate'].update(assessed_at=TODAY, supporting_evidence_ids=[SID], contradictory_evidence_ids=[],
                               access_ids=[], rationale='Synthetic actual aggregate reconsideration.',
                               confidence_rationale='Synthetic evidence reasoning; no actual research.')
    row = next(r for r in packet['research_run']['task_decisions'] if r['task_id'] == record['task_id'])
    row.update({k: deepcopy(record[k]) for k in ('applicability', 'result', 'checked_at', 'rationale',
                'confidence_rationale', 'judgment_ids', 'evidence_ids', 'conditions', 'remaining_gaps')})
    packet['changes'].append({'kind': 'task_assessment', 'record': record, 'previous_hash': record_hash(original),
                              'identity_key': None, 'evidence_ids': [SID], 'checked_paths': ['/checked_at', '/aggregate'],
                              'rationale': 'Synthetic chronology regression.'})
    return packet, assignment, record


@pytest.mark.parametrize('offset', [-1, 1])
def test_past_or_post_packet_aggregate_rejected_by_helper_and_model_receiver(dated_packet, baseline, offset):
    packet, assignment, record = dated_packet
    record['aggregate']['assessed_at'] = (date.today() + timedelta(days=offset)).isoformat()
    before = deepcopy(packet)
    errors = packet_errors(packet, baseline)
    assert any(e.startswith('EA04: /changes/') and '/aggregate/assessed_at:' in e for e in errors)
    with pytest.raises(ValueError, match='Invalid task-assessment references'):
        batch.compile_batch(packet, assignment, baseline)
    assert packet == before


def test_actual_same_day_judgment_passes_without_modification(dated_packet, baseline):
    packet, assignment, _ = dated_packet
    before = deepcopy(packet)
    assert packet_errors(packet, baseline) == []
    compiled = batch.compile_batch(packet, assignment, baseline)
    assert not compiled['completion']['complete']
    assert packet == before


def test_aggregate_absence_does_not_infer_a_rating():
    record = {'checked_at': TODAY}
    before = deepcopy(record)
    assert assessment_chronology_errors(record, latest_date=TODAY) == []
    assert record == before and 'aggregate' not in record


def test_judgment_can_follow_earlier_source_check_without_being_same_day():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    assert assessment_chronology_errors({'checked_at': yesterday, 'aggregate': {'assessed_at': TODAY}}, latest_date=TODAY) == []


@pytest.mark.parametrize('field,value', [('checked_at', None), ('checked_at', '2026-02-30'),
                                        ('assessed_at', ''), ('assessed_at', '20261012')])
def test_malformed_dates_get_specific_paths(field, value):
    record = {'checked_at': TODAY, 'aggregate': {'assessed_at': TODAY}}
    if field == 'checked_at': record[field] = value
    else: record['aggregate'][field] = value
    errors = assessment_chronology_errors(record, latest_date=TODAY)
    assert len(errors) == 1 and errors[0]['path'] == ('/checked_at' if field == 'checked_at' else '/aggregate/assessed_at')


@pytest.mark.parametrize('offset', [-1, 0, 1])
def test_scoped_receiver_uses_identical_chronology_rule(baseline, offset):
    suite = scoped_fixtures.ScopedTests()
    suite.public = baseline
    suite.setUp()
    subject = suite.subject('model', 'Synthetic Chronology Fixture')
    assignment, packet = suite.completed(subject)
    row = next(r for r in packet['scope_run']['task_decisions'] if r['model_id'] == subject['id'])
    record = {k: deepcopy(row[k]) for k in ('model_id', 'task_id', 'applicability', 'result', 'checked_at',
              'rationale', 'confidence_rationale', 'judgment_ids', 'evidence_ids', 'conditions', 'remaining_gaps')}
    record['id'] = 'new:synthetic-chronology-task'
    record['conditions'] = ['Synthetic exact-model native route.']
    record['aggregate'] = {'policy_version': '1', 'suitability': 'unknown', 'evidence_confidence': None,
                           'assessed_at': (date.today() + timedelta(days=offset)).isoformat(),
                           'rationale': 'Synthetic investigated unknown.', 'confidence_rationale': 'Synthetic sparse evidence.',
                           'supporting_evidence_ids': row['evidence_ids'], 'contradictory_evidence_ids': [],
                           'conflict_rationale': None, 'watch_outs': [], 'access_ids': []}
    packet['changes'].append(scoped_fixtures.proposal('task_assessment', record, suite.baseline))
    before = deepcopy(packet)
    errors = packet_errors(packet, suite.baseline)
    if offset:
        assert any('EA04:' in e for e in errors)
        with pytest.raises(ValueError, match='EA04'):
            scoped.compile_scope(packet, assignment, suite.baseline)
    else:
        assert errors == []
        scoped.compile_scope(packet, assignment, suite.baseline)
    assert packet == before
