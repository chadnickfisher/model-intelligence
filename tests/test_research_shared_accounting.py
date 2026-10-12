"""Shared factual records retain every owner and require one complete valid row."""
from copy import deepcopy
import pytest

from test_research_batch import baseline, fixture, MID, SID, TODAY, inspected
from tools import research_batch as batch, research_partial as partial
from tools.knowledge import record_hash
from tools.research_runs import make_run
from tools.research_authoring import packet_errors
from tools.research_fields import group_field_checks, qualifying_field_checks

OTHER = 'claude-opus-5-5'


@pytest.fixture
def shared_packet(fixture, baseline):
    packet, assignment = fixture
    state = deepcopy(baseline)
    behavior = deepcopy(next(r for (k, _), r in state.items() if k == 'behavior'))
    behavior.update(model_ids=[MID, OTHER], observed_at=TODAY,
                    supporting_evidence_ids=[SID], contradictory_evidence_ids=[])
    if behavior['fix']['evidence_ids']:
        behavior['fix']['evidence_ids'] = [SID]
    state['behavior', behavior['id']] = behavior
    prior_run = packet['research_run']
    run = make_run(state, prior_run['baseline_revision_id'], assignment['baseline_commit'],
                   prior_run['id'], [MID, OTHER], prior_run['bounds'], TODAY)
    packet['research_run'] = run
    assignment['research_run'] = deepcopy(run)
    inspected(next(r for r in run['field_checks'] if r['entity_type'] == 'model' and r['entity_id'] == MID and r['path'] == '/notes'), 'value')
    inspected(next(r for r in run['source_checks'] if r['model_id'] == MID and r['category'] == 'primary'), 'checked')
    notes = [r for r in run['field_checks'] if r['entity_type'] == 'behavior' and r['entity_id'] == behavior['id'] and r['path'] == '/notes']
    assert {r['model_id'] for r in notes} == {MID, OTHER}
    inspected(next(r for r in notes if r['model_id'] == MID), 'value')
    proposal = deepcopy(behavior)
    proposal['notes'].append('Synthetic shared factual note; no actual research.')
    change = {'kind': 'behavior', 'record': proposal, 'previous_hash': record_hash(behavior),
              'identity_key': None, 'evidence_ids': [SID], 'checked_paths': ['/notes'],
              'rationale': 'Synthetic shared-record accounting regression.'}
    packet['changes'].append(change)
    return packet, assignment, state, change, notes


@pytest.mark.parametrize('reverse', [False, True])
def test_shared_record_passes_both_orders_without_crediting_other_owner(shared_packet, reverse):
    packet, assignment, state, change, notes = shared_packet
    if reverse:
        packet['research_run']['field_checks'].reverse()
    before = deepcopy(packet)
    assert packet_errors(packet, state) == []
    compiled = batch.compile_batch(packet, assignment, state)
    assert compiled['candidate']['behavior', change['record']['id']] == change['record']
    unchecked = next(r for r in compiled['research_run']['field_checks'] if r['entity_type'] == 'behavior'
                     and r['entity_id'] == change['record']['id'] and r['path'] == '/notes' and r['model_id'] == OTHER)
    assert unchecked['result'] == 'not_checked' and unchecked['checked_at'] is None and unchecked['evidence_ids'] == []
    assert not compiled['completion']['complete']
    assert packet == before


@pytest.mark.parametrize('reverse', [False, True])
def test_partial_review_keeps_shared_note_independently_of_row_order(shared_packet, reverse):
    packet, assignment, state, change, _ = shared_packet
    if reverse:
        packet['research_run']['field_checks'].reverse()
    before = deepcopy(packet)
    result = partial.compile_partial(packet, assignment, state)
    assert result['compiled']['candidate']['behavior', change['record']['id']]['notes'] == change['record']['notes']
    assert result['deferred_units'] == 0
    assert packet == before


@pytest.mark.parametrize('status', ['blocked', 'not_checked'])
def test_all_eligible_rows_unfinished_cannot_support_change(shared_packet, status):
    packet, assignment, state, _, rows = shared_packet
    for row in rows:
        if status == 'blocked':
            row.update(result=status, checked_at=TODAY, rationale='Synthetic fetch failure.', evidence_ids=[],
                       blocked_reason='Synthetic tool failure.', remaining_gaps=['Source body still unavailable.'])
        else:
            row.update(result=status, checked_at=None, rationale='', evidence_ids=[], blocked_reason=None,
                       remaining_gaps=['Pending actual source inspection.'])
    assert any('EA03:' in e for e in packet_errors(packet, state))
    with pytest.raises(ValueError, match='not investigated'):
        batch.compile_batch(packet, assignment, state)


def qualification(packet, state, change, rows, *, positive=False):
    candidate = {**state, **{(c['kind'], c['record']['id']): c['record'] for c in packet.get('changes', [])}}
    return qualifying_field_checks(change, '/notes', group_field_checks(rows),
                                   packet.get('research_run', packet.get('scope_run')), candidate,
                                   {i: r for (k, i), r in candidate.items() if k == 'source'},
                                   {i: r for (k, i), r in candidate.items() if k == 'observation'},
                                   packet['created_at'][:10], positive=positive)


def test_unrelated_or_unassigned_owner_cannot_supply_shared_support(shared_packet):
    packet, _, state, change, rows = shared_packet
    copied = deepcopy(next(r for r in rows if r['result'] == 'value'))
    for owner in ('unassigned-model', 'gpt-6-astra'):
        copied['model_id'] = owner
        assert qualification(packet, state, change, [copied]) == []
    packet['research_run']['target_model_ids'].append('gpt-6-astra')
    assert qualification(packet, state, change, [copied]) == []


def test_stale_or_future_or_unlinked_row_cannot_supply_support(shared_packet):
    packet, _, state, change, rows = shared_packet
    row = deepcopy(next(r for r in rows if r['result'] == 'value'))
    for source_date in ('2000-01-01', '2099-01-01'):
        failed = deepcopy(packet)
        failed['changes'][0]['record']['accessed_at'] = source_date
        assert qualification(failed, state, change, [row]) == []
    row['evidence_ids'] = [next(i for k, i in state if k == 'source' and i != SID)]
    assert qualification(packet, state, change, [row]) == []


def test_scoped_positive_and_primary_support_cannot_be_pooled_across_owners():
    primary, practitioner = 'src-primary', 'src-practitioner'
    change = {'kind': 'price', 'record': {'id': 'price-synthetic', 'provider_id': 'provider-a', 'product': 'API'},
              'evidence_ids': [primary, practitioner]}
    run = {'created_at': TODAY, 'subjects': [
        {'kind': 'provider', 'id': 'provider-a'},
        {'kind': 'product', 'id': 'product-a', 'identity': {'provider_id': 'provider-a', 'product': 'API'}}]}
    common = {'entity_type': 'price', 'entity_id': 'price-synthetic', 'path': '/notes',
              'domain': 'access_pricing', 'checked_at': TODAY}
    rows = [dict(common, subject_kind='provider', subject_id='provider-a', result='value', evidence_ids=[practitioner]),
            dict(common, subject_kind='product', subject_id='product-a', result='unknown', evidence_ids=[primary])]
    packet = {'scope_run': run, 'created_at': TODAY + 'T00:00:00Z', 'changes': []}
    state = {('source', primary): {'source_type': 'primary', 'accessed_at': TODAY},
             ('source', practitioner): {'source_type': 'practitioner', 'accessed_at': TODAY}}
    for ordered in (rows, list(reversed(rows))):
        assert qualification(packet, state, change, ordered, positive=True) == []
    rows[1]['result'] = 'value'
    assert qualification(packet, state, change, rows, positive=True) == [rows[1]]


def test_primary_evidence_without_shared_link_cannot_rescue_another_row():
    change = {'kind': 'price', 'record': {'id': 'p', 'model_id': MID}, 'evidence_ids': ['s-vendor']}
    common = {'model_id': MID, 'entity_type': 'price', 'entity_id': 'p', 'path': '/notes',
              'domain': 'access_pricing', 'checked_at': TODAY, 'result': 'value'}
    rows = [dict(common, evidence_ids=['s-vendor']), dict(common, evidence_ids=['s-primary'])]
    sources = {'s-vendor': {'source_type': 'practitioner', 'accessed_at': TODAY},
               's-primary': {'source_type': 'primary', 'accessed_at': TODAY}}
    run = {'created_at': TODAY, 'target_model_ids': [MID]}
    assert qualifying_field_checks(change, '/notes', group_field_checks(rows), run, {}, sources, {}, TODAY) == []
