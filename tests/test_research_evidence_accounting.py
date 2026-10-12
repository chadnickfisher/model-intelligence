"""Historical citations cannot masquerade as newly inspected check evidence."""
from copy import deepcopy
import pytest

from test_research_batch import baseline, fixture, MID, SID, TODAY
from tools import research_batch as batch, research_scoped as scoped
from tools.research_authoring import packet_errors, accounting_evidence_errors, ACCOUNTING_CHECKS
from tools.research_output_contract import build_contract, render_contract


def block(row, evidence):
    row.update(result='blocked', checked_at=TODAY, rationale='Original source body could not be loaded.',
               evidence_ids=evidence, search_references=[], remaining_gaps=['Retry the original source body.'],
               blocked_reason='Synthetic source-body fetch failure.')


@pytest.fixture(params=['model', 'scoped'])
def blocked_packet(request, fixture, baseline):
    if request.param == 'model':
        packet, assignment = fixture
        run = packet['research_run']
        row = next(r for r in run['field_checks'] if r['entity_type'] == 'model' and r['path'] == '/identity/name')
        compiler = batch.compile_batch
    else:
        provider = next(i for k, i in baseline if k == 'provider')
        subject = {'kind': 'provider', 'id': provider, 'operation': 'review', 'identity': None}
        assignment = scoped.make_assignment(baseline, 'a' * 40, 'synthetic-blocked-review', [subject], TODAY)
        packet = scoped.output_template(assignment)
        run = packet['scope_run']
        row = next(r for r in run['field_checks'] if r['entity_type'] == 'provider' and r['path'] == '/name')
        compiler = scoped.compile_scope
    historical = next(i for (k, i), source in baseline.items()
                      if k == 'source' and i != SID and source['accessed_at'] < TODAY)
    block(row, [historical])
    return packet, assignment, row, historical, compiler


def test_historical_citation_rejected_in_blocked_current_check(blocked_packet, baseline):
    packet, assignment, row, historical, compiler = blocked_packet
    before = deepcopy(packet)
    errors = packet_errors(packet, baseline)
    assert any('EA01:' in e and '/field_checks/' in e and historical in e for e in errors)
    with pytest.raises(ValueError, match='source inspection|uninspected evidence'):
        compiler(packet, assignment, baseline)
    assert packet == before


def test_empty_evidence_preserves_historical_record_and_blocked_attempt(blocked_packet, baseline):
    packet, assignment, row, historical, compiler = blocked_packet
    original = deepcopy(row)
    retained_source = deepcopy(baseline['source', historical])
    row['evidence_ids'] = []
    assert packet_errors(packet, baseline) == []
    compiled = compiler(packet, assignment, baseline)
    assert not compiled['completion']['complete'] and compiled['completion']['blocked'] > 0
    assert compiled['candidate']['source', historical] == retained_source
    assert {k: v for k, v in row.items() if k != 'evidence_ids'} == {k: v for k, v in original.items() if k != 'evidence_ids'}


def test_current_partial_inspection_does_not_remove_blocker(fixture, baseline):
    packet, assignment = fixture
    row = next(r for r in packet['research_run']['field_checks'] if r['entity_type'] == 'model' and r['path'] == '/identity/name')
    block(row, [SID])
    assert packet_errors(packet, baseline) == []
    compiled = batch.compile_batch(packet, assignment, baseline)
    assert compiled['completion']['blocked'] > 0 and not compiled['completion']['complete']


@pytest.mark.parametrize('missing', ['checked_at', 'rationale', 'blocked_reason', 'remaining_gaps'])
def test_blocked_failure_metadata_is_required(fixture, baseline, missing):
    packet, _ = fixture
    row = packet['research_run']['field_checks'][0]
    block(row, [])
    row[missing] = [] if missing == 'remaining_gaps' else '' if missing == 'rationale' else None
    assert any('EA02:' in e for e in accounting_evidence_errors(packet, baseline))


@pytest.mark.parametrize('source_date', ['2000-01-01', '2099-01-01', None])
def test_current_evidence_bounds_apply_even_to_blocked_rows(fixture, baseline, source_date):
    packet, _ = fixture
    row = packet['research_run']['field_checks'][0]
    block(row, [SID])
    source = packet['changes'][0]['record']
    source['accessed_at'] = source_date
    assert any('EA01:' in e for e in accounting_evidence_errors(packet, baseline))


def test_observation_expansion_cannot_hide_historical_source(fixture, baseline):
    packet, _ = fixture
    historical = next(i for (k, i), r in baseline.items() if k == 'source' and i != SID and r['accessed_at'] < TODAY)
    state = {**baseline, ('observation', 'synthetic-observation'): {'source_ids': [historical]}}
    row = packet['research_run']['field_checks'][0]
    block(row, ['synthetic-observation'])
    assert any('EA01:' in e and historical in e for e in accounting_evidence_errors(packet, state))


def test_blocked_current_evidence_cannot_support_changed_factual_field(fixture, baseline):
    packet, assignment = fixture
    row = next(r for r in packet['research_run']['field_checks'] if r['entity_type'] == 'model' and r['path'] == '/notes')
    block(row, [SID])
    assert any('EA03:' in e and '/notes' in e for e in packet_errors(packet, baseline))
    with pytest.raises(ValueError, match='not investigated'):
        batch.compile_batch(packet, assignment, baseline)


def test_generated_accounting_rules_are_the_portable_validator_rules():
    contract = build_contract(batch.schema_registry()[0], TODAY)
    assert contract['accounting_checks'] == ACCOUNTING_CHECKS
    guide = render_contract(contract).decode()
    for key, rule in ACCOUNTING_CHECKS.items():
        assert '| ' + key + ' | ' + rule + ' |' in guide
