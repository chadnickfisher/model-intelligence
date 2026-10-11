"""Portable helper regressions for receiver-rejected delivery shapes."""
from copy import deepcopy
import json
import pytest
from test_research_batch import baseline, fixture, MID, SID
from tools import research_batch as batch, research_scoped as scoped
from tools.research_authoring import contract_errors, packet_errors, SCOPED_RESULTS, MODEL_RESULTS


def test_portable_outcomes_match_authoritative_contracts():
    assert SCOPED_RESULTS == scoped.RESULTS
    schema = json.loads((batch.ROOT / 'schema/research-run-record.schema.json').read_text())
    assert MODEL_RESULTS == {name: set(schema['properties'][name]['items']['properties']['result']['enum'])
                             for name in MODEL_RESULTS}


def test_valid_partial_model_packet_is_unchanged(fixture, baseline):
    packet, assignment = fixture
    before = deepcopy(packet)
    assert packet_errors(packet, baseline) == []
    assert not batch.compile_batch(packet, assignment, baseline)['completion']['complete']
    assert packet == before


@pytest.mark.parametrize('collection,bad', [('domain_checks', 'checked'), ('domain_checks', 'value'),
    ('field_checks', 'changed'), ('field_checks', 'unchanged'), ('field_checks', 'checked'),
    ('field_checks', 'not_applicable'), ('source_checks', 'value'), ('task_decisions', 'changed')])
def test_scoped_invalid_outcomes_include_collection_and_row(fixture, baseline, collection, bad):
    packet, _ = fixture
    packet['scope_run'] = packet.pop('research_run')
    packet['scope_run'][collection][0]['result'] = bad
    before = deepcopy(packet)
    errors = contract_errors(packet, baseline)
    assert any(collection + '[0]: invalid outcome ' + bad in e for e in errors)
    assert packet == before


@pytest.mark.parametrize('token', ['assignment', 'run', '.local/work', '.agents/work', 'AGENTS.md', 'x.receipt.json'])
def test_nested_private_provenance_rejected_by_helper_and_receiver(fixture, baseline, token):
    packet, assignment = fixture
    token = packet['assignment_id'] if token == 'assignment' else packet['research_run']['id'] if token == 'run' else token
    model = packet['changes'][1]['record']
    model['capabilities'][0]['provenance']['research_batch_id'] = token
    assert any('private operating material at /capabilities/0/provenance/research_batch_id' in e
               for e in packet_errors(packet, baseline))
    with pytest.raises(ValueError, match='Private operating'):
        batch.compile_batch(packet, assignment, baseline)


def test_metadata_only_source_still_needs_checked_paths(fixture, baseline):
    packet, assignment = fixture
    change = packet['changes'][0]
    change['record'] = deepcopy(baseline['source', SID])
    change['record']['accessed_at'] = packet['created_at'][:10]
    change['checked_paths'] = []
    assert any('requires nonempty checked_paths' in e for e in packet_errors(packet, baseline))
    with pytest.raises(ValueError, match='Change lacks evidence/checked fields'):
        batch.compile_batch(packet, assignment, baseline)


def test_unchecked_work_is_not_silently_credited(fixture, baseline):
    packet, _ = fixture
    row = packet['research_run']['field_checks'][0]
    row.update(result='not_checked', rationale='Only one portion inspected', evidence_ids=[SID])
    before = deepcopy(packet)
    assert any('unchecked row claims investigation' in e for e in contract_errors(packet, baseline))
    assert packet == before


def test_null_value_cannot_be_promoted(fixture, baseline):
    packet, _ = fixture
    row = packet['research_run']['field_checks'][0]
    row.update(entity_type='model', entity_id=MID, path='/missing-value', result='value', evidence_ids=[SID])
    assert any('absent/null fact' in e for e in contract_errors(packet, baseline))


def test_scoped_searched_unknown_keeps_receiver_exception(fixture, baseline):
    packet, _ = fixture
    packet['scope_run'] = packet.pop('research_run')
    run = packet['scope_run']
    row = run['task_decisions'][0]
    row.update(result='unknown', evidence_ids=[], search_references=[{'outcome': 'no_matched_sources'}])
    change = {'kind': 'task_assessment', 'record': {'id': 'new:unknown', 'model_id': row['model_id'],
              'task_id': row['task_id'], 'result': 'unknown'}, 'evidence_ids': [], 'checked_paths': ['/result']}
    packet['changes'].append(change)
    assert not any('new:unknown: change requires evidence_ids' in e for e in contract_errors(packet, baseline))
    row['search_references'][0]['outcome'] = 'blocked'
    assert any('new:unknown: change requires evidence_ids' in e for e in contract_errors(packet, baseline))


@pytest.mark.parametrize('scoped_packet', [False, True])
@pytest.mark.parametrize('result', ['unknown', 'blocked', 'not_checked'])
def test_unresolved_accounting_requires_explicit_gap(fixture, baseline, scoped_packet, result):
    packet, _ = fixture
    run = packet['research_run']
    if scoped_packet:
        packet['scope_run'] = packet.pop('research_run')
    row = run['field_checks'][0]
    row.update(result=result, remaining_gaps=[])
    before = deepcopy(packet)
    assert any('field_checks[0]: unresolved or pending result requires remaining_gaps' in e
               for e in contract_errors(packet, baseline))
    assert packet == before


def test_unknown_task_cannot_retain_endorsements_in_row_or_proposal(fixture, baseline):
    packet, _ = fixture
    row = packet['research_run']['task_decisions'][0]
    row.update(result='unknown', judgment_ids=['fixture-finding'], remaining_gaps=['Unknown exact task support'])
    record = {k:deepcopy(row[k]) for k in ('model_id', 'task_id', 'result', 'checked_at', 'judgment_ids', 'evidence_ids')}
    record['id'] = 'new:task-unknown'
    packet['changes'].append({'kind':'task_assessment', 'record':record,
                             'evidence_ids':[SID], 'checked_paths':['/judgment_ids']})
    before = deepcopy(packet)
    errors = contract_errors(packet, baseline)
    assert sum('non-assessed task cannot endorse judgments' in e for e in errors) == 2
    assert packet == before
    row['judgment_ids'] = []
    assert any('canonical proposal differ for /judgment_ids' in e for e in contract_errors(packet, baseline))
    record['judgment_ids'] = []
    assert not any('endorse judgments' in e or 'canonical proposal differ' in e for e in contract_errors(packet, baseline))


@pytest.fixture
def scoped_price_packet(baseline):
    from test_research_scoped import DAY, offers, source, proposal, investigated, extended_packet
    state = deepcopy(baseline)
    provider = next(ident for kind, ident in state if kind == 'provider')
    inspected_source = source()
    inspected_source['accessed_at'] = DAY
    state['source', inspected_source['id']] = inspected_source
    _, price = offers(None, provider)
    price.update(id='price-synthetic-tier', tier='standard')
    state['price', price['id']] = price
    subject = {'kind': 'provider', 'id': provider, 'operation': 'review', 'identity': None}
    assignment = scoped.make_assignment(state, 'a' * 40, 'synthetic-price-review', [subject], DAY)
    packet = scoped.output_template(assignment)
    updated = deepcopy(price)
    updated['notes'].append('Synthetic pricing note correction.')
    packet['changes'] = [proposal('price', updated, state)]
    for row in packet['scope_run']['source_checks']:
        if row['subject_id'] == provider and row['category'] == 'primary':
            row.update(investigated(row))
    return extended_packet(packet, assignment, state), assignment, state


@pytest.mark.parametrize('field,value', [('product', 'Different API product'),
    ('billing_method', 'prepaid-credits'), ('region', 'different-region'), ('tier', 'premium')])
def test_scoped_offer_identity_reassignment_rejected_by_helper_and_receiver(scoped_price_packet, field, value):
    from test_research_scoped import extended_packet
    packet, assignment, state = scoped_price_packet
    packet['changes'][0]['record'][field] = value
    extended_packet(packet, assignment, state)
    before = deepcopy((packet, assignment, state))
    # Complete field accounting must not permit reusing an offer ID for another tier/product.
    assert any('stable identity reassigned: /' + field in error for error in packet_errors(packet, state))
    with pytest.raises(ValueError, match='Stable product/offer identity reassigned'):
        scoped.compile_scope(packet, assignment, state)
    assert (packet, assignment, state) == before


def test_scoped_price_edit_with_unchanged_tier_passes_both_checks(scoped_price_packet):
    from test_research_scoped import extended_packet
    packet, assignment, state = scoped_price_packet
    packet['changes'][0]['record']['rates'] = [
        {'metric': 'input', 'amount': 1, 'currency': 'USD', 'unit': 'million_tokens', 'conditions': []}]
    extended_packet(packet, assignment, state)
    before = deepcopy((packet, assignment, state))
    assert packet_errors(packet, state) == []
    compiled = scoped.compile_scope(packet, assignment, state)
    assert compiled['candidate']['price', 'price-synthetic-tier']['tier'] == 'standard'
    assert (packet, assignment, state) == before
