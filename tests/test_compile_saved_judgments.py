from copy import deepcopy
from tools.research_compile_records import compile_tasks

def inputs():
    source='snapshot-'+'d'*20
    payload={'task_id':'coding.scoped_edit','conclusion':'Illustrative strong fit under specified conditions',
        'suitability':{'level':'high','rationale':'Matching mechanism supports an inference'},
        'confidence':{'level':'low','rationale':'Sparse task-matching observations'},
        'basis':{'kind':'reasoned_inference','rationale':'Mechanism and adjacent evidence'},
        'source_ids':[source],'contrary_source_ids':[],'conditions':['Fixed illustrative setup'],
        'limitations':['Exact task evaluation absent'],'unknowns':['Success probability unknown'],'positive_boundary':None}
    item={'id':'private-observation','model_id':'example-model','access_id':'example-access','payload':payload,
          'snapshot_ids':[source],'inspection_reported_at':None}
    snap={'id':source,'requested_url':'https://example.com/evidence','final_url':'https://example.com/evidence',
        'original':{'bytes':100,'sha256':'a'*64},'readable':{'bytes':90,'sha256':'b'*64},
        'retrieval_started_at':'2026-10-13T12:00:00+00:00','retrieval_completed_at':'2026-10-13T12:01:00+00:00',
        'extractor_version':'fixture','publication_at':None,'effective_at':None}
    return {'task_judgments':[item]}, {'example-model':{'capabilities':[]}},[],[],[snap]

def compile(values):return compile_tasks(*values,received_at='2026-10-13T12:10:00+00:00')

def test_compile_inference_without_promoting_confidence_or_dates():
    values=inputs();before=deepcopy(values);result=compile(values)
    assert values==before and result['dispositions'][0]['status']=='compiled'
    r=result['assessments'][0];j=result['models']['example-model']['capabilities'][0]
    assert r['aggregate']['suitability']=='high' and r['aggregate']['evidence_confidence']=='low'
    assert r['aggregate']['basis']['kind']=='reasoned_inference'
    assert r['aggregate']['assessed_at'] is None and j['scope']=='direct'
    assert j['effective_from'] is None
    assert 'private-observation' not in str(result['models'])+str(result['assessments'])+str(result['sources'])

def test_stable_existing_ids_and_repeat_noop():
    result=compile(inputs());record=result['assessments'][0];model=result['models']['example-model']
    record['id']='task-assessment-'+'f'*16;model['capabilities'][0]['id']='judgment-'+'e'*16
    record['judgment_ids']=['judgment-'+'e'*16]
    values=inputs();values=(values[0],result['models'],result['assessments'],result['sources'],values[4])
    repeated=compile(values)
    assert repeated['assessments'][0]['id']==record['id']
    assert repeated['models']['example-model']['capabilities'][0]['id']=='judgment-'+'e'*16
    again=compile((values[0],repeated['models'],repeated['assessments'],repeated['sources'],values[4]))
    assert repeated==again

def test_invalid_record_isolated_and_prior_records_preserved():
    values=inputs();bad=deepcopy(values[0]['task_judgments'][0]);bad['id']='bad'
    bad['payload']['conditions']=[];values[0]['task_judgments'].append(bad)
    result=compile(values)
    assert [r['status'] for r in result['dispositions']]==['compiled','deferred']
    assert len(result['assessments'])==1

def test_snapshot_conflict_never_overwrites_older_source():
    result=compile(inputs());values=inputs()
    values=(values[0],values[1],values[2],result['sources'],values[4])
    values[4][0]['original']['sha256']='f'*64
    again=compile(values)
    assert again['dispositions'][0]['status']=='compiled'
    captures=again['sources'][0]['snapshots']
    assert len(captures)==2 and captures[0]==result['sources'][0]['snapshots'][0]
    assert captures[0]['id']!=captures[1]['id']

def test_identical_content_with_new_capture_clock_keeps_both_versions():
    result=compile(inputs());values=inputs()
    values=(values[0],result['models'],result['assessments'],result['sources'],values[4])
    values[4][0]['retrieval_completed_at']='2026-10-13T12:02:00+00:00'
    again=compile(values);captures=again['sources'][0]['snapshots']
    assert len(captures)==2 and captures[0]['original']==captures[1]['original']
    assert captures[0]['id']!=captures[1]['id']
    assert result['sources'][0]['accessed_at']==again['sources'][0]['accessed_at']

def test_investigated_unknown_does_not_manufacture_source_check_date():
    values=inputs();item=values[0]['task_judgments'][0]
    item['payload']['suitability']['level']='unknown';item['payload']['confidence']['level']='unknown'
    item['payload']['source_ids']=[];item['snapshot_ids']=[]
    result=compile(values);record=result['assessments'][0]
    assert record['result']=='unknown' and record['checked_at'] is None
    assert record['aggregate']['recorded_at']=='2026-10-13T12:10:00+00:00'
    assert not result['models']['example-model']['capabilities']
