"""Partial identity facts stay separate from identity resolution and onboarding."""
from copy import deepcopy
from datetime import date, timedelta

import pytest

from test_research_batch import baseline
from test_research_scoped import COMMIT, DAY, identity, source, proposal, investigated
from tools import research_scoped as scoped
from tools.research_authoring import contract_errors, packet_errors


@pytest.fixture
def resolution(baseline):
    state=deepcopy(baseline)
    state['source','src-111111111111']=source()
    subject={'kind':'discovery','id':'discovery-synthetic-identity','operation':'resolve','identity':None}
    assignment=scoped.make_assignment(state,COMMIT,'synthetic-identity-lookup',[subject],DAY,minutes=30)
    packet=scoped.output_template(assignment)
    inspected=source();inspected['accessed_at']=DAY
    packet['changes']=[proposal('source',inspected,state)]
    ident=identity('provider','Synthetic Identity Lookup Hosting')
    for collection in scoped.KEYS:
        packet['scope_run'][collection]=[investigated(row) if row.get('subject_kind')=='discovery' else row
                                        for row in packet['scope_run'][collection]]
    for row in packet['scope_run']['field_checks']:
        value=ident[row['path'].split('/')[-1]]
        row.update(result='value' if value is not None else 'unknown',
                   remaining_gaps=[] if value is not None else ['Synthetic unknown identity field'])
    packet['resolutions'][0].update(result='resolved',identity=ident,checked_at=DAY,
        evidence_ids=['src-111111111111'],rationale='Synthetic identity lookup validation; no real research.',remaining_gaps=[])
    return packet,assignment,state


def set_result(packet,result):
    row=packet['resolutions'][0]
    row.update(result=result,remaining_gaps=[] if result=='resolved' else ['Synthetic unresolved boundary'],
               blocked_reason='Synthetic checkpoint lookup blocked' if result=='blocked' else None)


@pytest.mark.parametrize('result',['resolved','ambiguous','blocked'])
def test_known_resolution_fields_pass_both_validators_without_promoting_identity(resolution,result):
    packet,assignment,state=resolution;set_result(packet,result)
    before=deepcopy((packet,assignment,state))
    assert packet_errors(packet,state)==[]
    compiled=scoped.compile_scope(packet,assignment,state)
    assert compiled['resolutions'][0]['result']==result
    assert not any(kind=='discovery' for kind,ident in compiled['candidate'])
    assert not any(change['kind'] in {'model','provider','access','price'} for change in compiled['changes'])
    if result=='blocked':assert compiled['completion']['blocked']>0 and not compiled['completion']['complete']
    assert (packet,assignment,state)==before


@pytest.mark.parametrize('result',['resolved','ambiguous','blocked'])
def test_nullable_identity_field_cannot_be_promoted_to_value(resolution,result):
    packet,assignment,state=resolution;set_result(packet,result)
    row=next(r for r in packet['scope_run']['field_checks'] if r['path']=='/identity/checkpoint')
    row.update(result='value',remaining_gaps=[])
    assert any('absent/null fact' in error for error in contract_errors(packet,state))
    with pytest.raises(ValueError,match='Absent/null fact'):scoped.compile_scope(packet,assignment,state)


@pytest.mark.parametrize('result',['resolved','ambiguous','blocked'])
def test_known_identity_field_still_requires_evidence(resolution,result):
    packet,assignment,state=resolution;set_result(packet,result)
    row=next(r for r in packet['scope_run']['field_checks'] if r['path']=='/identity/name')
    row['evidence_ids']=[]
    assert any('absent/null fact' in error for error in contract_errors(packet,state))
    with pytest.raises(ValueError,match='accounting|investigated unknown|sourced value'):
        scoped.compile_scope(packet,assignment,state)


@pytest.mark.parametrize('result',['resolved','ambiguous','blocked'])
def test_partial_identity_cannot_bypass_source_inspection_dates(resolution,result):
    packet,assignment,state=resolution;set_result(packet,result)
    packet['changes'][0]['record']['accessed_at']=(date.today()-timedelta(days=1)).isoformat()
    assert any('source inspection date' in error for error in packet_errors(packet,state))
    with pytest.raises(ValueError,match='uninspected evidence'):scoped.compile_scope(packet,assignment,state)


def test_unattempted_resolution_is_not_used_as_a_value_lookup(resolution):
    packet,assignment,state=resolution
    packet['resolutions'][0]=deepcopy(scoped.output_template(assignment)['resolutions'][0])
    assert any('absent/null fact' in error for error in contract_errors(packet,state))
    with pytest.raises(ValueError,match='Absent/null fact'):scoped.compile_scope(packet,assignment,state)


def test_value_lookup_uses_matching_candidate_id(resolution):
    packet,assignment,state=resolution
    packet['resolutions'][0]['candidate_id']='discovery-different-identity'
    assert any('absent/null fact' in error for error in contract_errors(packet,state))
    with pytest.raises(ValueError,match='Resolution accounting'):scoped.compile_scope(packet,assignment,state)


def test_missing_identity_cannot_supply_a_known_value(resolution):
    packet,assignment,state=resolution;set_result(packet,'ambiguous')
    packet['resolutions'][0]['identity']=None
    assert any('absent/null fact' in error for error in contract_errors(packet,state))
    with pytest.raises(ValueError,match='Absent/null fact'):scoped.compile_scope(packet,assignment,state)


def test_resolution_dates_are_still_checked_before_scratch_facts(resolution):
    packet,assignment,state=resolution;set_result(packet,'ambiguous')
    packet['resolutions'][0]['checked_at']=(date.today()-timedelta(days=1)).isoformat()
    with pytest.raises(ValueError,match='actual date'):scoped.compile_scope(packet,assignment,state)
