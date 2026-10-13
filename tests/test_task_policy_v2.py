from copy import deepcopy
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator,FormatChecker
from tools.research_fields import assessment_chronology_errors
from tools.source_snapshots import snapshot_errors
from tools.task_assessments import select_task_assessments
from explorer.presentation import assessment_basis

ROOT=Path(__file__).resolve().parents[1]
def record():
    return {'id':'task-assessment-'+'a'*16,'model_id':'example-model','task_id':'coding.scoped_edit',
        'applicability':'applicable','result':'assessed','checked_at':'2026-10-13','rationale':'Fixture task conclusion',
        'confidence_rationale':'Sparse matching evidence','judgment_ids':['judgment-'+'b'*16],
        'evidence_ids':['src-'+'c'*12],'conditions':['Fixed fixture setup'],'remaining_gaps':['Exact success rate unknown'],
        'aggregate':{'policy_version':'2','suitability':'high','evidence_confidence':'low','assessed_at':None,
            'rationale':'Plausible strong task fit','confidence_rationale':'Sparse matching evidence',
            'supporting_evidence_ids':['src-'+'c'*12],'contradictory_evidence_ids':[],'conflict_rationale':None,
            'watch_outs':['Exact success rate unknown'],'access_ids':['example-access'],
            'basis':{'kind':'reasoned_inference','rationale':'Task mechanism and adjacent reported results'},
            'inspection_reported_at':None,'recorded_at':'2026-10-13T12:10:00+00:00',
            'snapshot_ids':['snapshot-'+'d'*20],'positive_boundary':None}}

def validate(r):
    schema=json.loads((ROOT/'schema/task-assessment-record.schema.json').read_bytes())
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(r)

def test_high_fit_low_confidence_and_unknown_inspection_are_valid():
    r=record();validate(r)
    assert not assessment_chronology_errors(r)
    assert assessment_basis(r['aggregate'])['label']=='Reasoned inference'
    assert assessment_basis({'policy_version':'1'}) is None
    assert select_task_assessments([r],'coding.scoped_edit',suitability=['high'],confidence=['low'])==[r]

@pytest.mark.parametrize('failure',['invented_date','before_capture','after_recording','no_timezone'])
def test_v2_actual_chronology(failure):
    r=record();a=r['aggregate']
    if failure=='invented_date':a['assessed_at']='2026-10-13'
    if failure=='before_capture':a.update(inspection_reported_at='2026-10-12T12:00:00+00:00',assessed_at='2026-10-12')
    if failure=='after_recording':a.update(inspection_reported_at='2026-10-13T13:00:00+00:00',assessed_at='2026-10-13')
    if failure=='no_timezone':a['recorded_at']='2026-10-13T12:10:00'
    assert assessment_chronology_errors(r)

def test_disputed_has_no_aggregate_badge_and_retains_basis():
    r=record();r['aggregate'].update(suitability='disputed',evidence_confidence=None,
        contradictory_evidence_ids=['src-'+'e'*12],conflict_rationale='Applicable evidence differs')
    r['evidence_ids'].append('src-'+'e'*12);validate(r)
    assert select_task_assessments([r],'coding.scoped_edit',confidence=['high'])==[r]
    assert r['aggregate']['basis']['kind']=='reasoned_inference'

def test_source_snapshot_links_and_actual_capture_day():
    r=record();source={'id':'src-'+'c'*12,'snapshots':[{'id':'snapshot-'+'d'*20,
        'retrieval_started_at':'2026-10-13T12:00:00+00:00','retrieval_completed_at':'2026-10-13T12:01:00+00:00'}]}
    assert not snapshot_errors([source],[r])
    r['checked_at']='2026-10-14';assert snapshot_errors([source],[r])
    r=record();r['aggregate']['snapshot_ids']=['snapshot-'+'f'*20];assert snapshot_errors([source],[r])
    r=record();r['aggregate'].update(inspection_reported_at='2026-10-13T11:00:00+00:00',assessed_at='2026-10-13')
    assert snapshot_errors([source],[r])

def test_v1_schema_and_chronology_preserved():
    r=record();a=r['aggregate'];a['policy_version']='1';a['assessed_at']='2026-10-13'
    for k in ('basis','inspection_reported_at','recorded_at','snapshot_ids','positive_boundary'):a.pop(k)
    validate(r);assert not assessment_chronology_errors(r)
