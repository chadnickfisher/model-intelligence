"""Source capture completeness, tamper rejection, receipt compatibility and reader fallback."""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from hashlib import sha256
import json
from pathlib import Path
import socket

import pytest
from test_research_batch import fixture,baseline,SID,TODAY
from test_research_review import config,fake_runtime
from test_research_output_contract import schemas,record_session
from test_research_search_receipts import evidence
from tools import research_source_bodies as bodies,research_review as review
from tools import research_evidence as reader,research_validation as validation


def stamp(delay=0):return (datetime.now(timezone.utc)-timedelta(seconds=delay)).isoformat().replace('+00:00','Z')


def bundle(tmp_path,packet=None,state=None):
    if packet is None:
        packet={'assignment_id':'source-fixture','baseline_commit':'a'*40,'created_at':stamp(),
                'changes':[{'kind':'source','record':{'id':SID,'url':'https://example.com/methods'},'evidence_ids':[SID]}]}
    packet=deepcopy(packet);packet['created_at']=stamp()
    path=tmp_path/'capture.r1.json';path.write_bytes(bodies.encoded(packet))
    rows=[{'kind':kind,'id':ident,'record':row} for (kind,ident),row in (state or {}).items() if kind in {'source','observation'}]
    base=tmp_path/'baseline.json';base.write_bytes(bodies.encoded({'baseline_commit':packet['baseline_commit'],'records':rows}))
    index=tmp_path/'capture.r1.source-evidence/index.json';bodies.initialize(path,index)
    url=next(c['record']['url'] for c in packet['changes'] if c['kind']=='source')
    return path,index,base,url


def save(index,url,text,*,source_id=SID,retrieval_status='available'):
    response=index.parent.parent/('return-'+str(len(bodies.parse(index.read_bytes())['calls']))+'.json')
    response.write_bytes(bodies.encoded(text))
    return bodies.capture(index,source_id=source_id,url=url,tool='synthetic-visible-source',started_at=stamp(8),
                          completed_at=stamp(7),request={'open':[{'ref_id':url}]},response_path=response,
                          retrieval_status=retrieval_status)


def page(url,start=0,end=3,*,total=3,suffix=''):
    lines=['Published original methods','Exact model checkpoint and effort setting.','Methods complete.']
    return 'Methods ('+url+')\nTotal lines: '+str(total)+'\n'+'\n'.join('L'+str(n)+': '+lines[n] for n in range(start,end))+suffix


def result(files,**kwargs):
    packet,index,base,_=files
    return bodies.audit(packet,index,base,bodies.contract(),**kwargs)


def test_all_page_chunks_are_required_and_overlaps_must_match(tmp_path):
    files=bundle(tmp_path);url=files[3]
    save(files[1],url,page(url,0,2))
    assert result(files)['checks']['SB07']=='failed'
    save(files[1],url,page(url,1,3))
    captures={};audit=result(files,captures=captures)
    assert audit['status']=='source_bodies_verified' and all(v=='passed' for v in audit['checks'].values())
    assert 'text' not in audit['sources'][SID]
    assert captures[SID]['text']=='Published original methods\nExact model checkpoint and effort setting.\nMethods complete.\n'
    assert sha256(captures[SID]['text'].encode()).hexdigest()==audit['sources'][SID]['body_sha256']
    save(files[1],url,page(url,1,3).replace('Methods complete.','Changed source version.'))
    assert result(files)['checks']['SB07']=='failed'


def test_sparse_continuation_is_completed_by_other_captured_chunks(tmp_path):
    files=bundle(tmp_path);url=files[3]
    def sparse(numbers):
        return 'Methods ('+url+')\nTotal lines: 591\n'+'\n'.join('L'+str(n)+': Exact method line '+str(n) for n in numbers)
    # Reproduce the real pagination pattern: the continuation repeats navigation
    # and skips 129-165, which the initial actual return already supplied.
    save(files[1],url,sparse(range(524)))
    assert result(files)['checks']['SB07']=='failed'
    save(files[1],url,sparse([*range(117,129),*range(166,591)]))
    captures={};report=result(files,captures=captures)
    assert report['status']=='source_bodies_verified'
    assert report['sources'][SID]['source_capture']['visible_line_count']==591
    assert len(captures[SID]['text'].splitlines())==591
    assert captures[SID]['text'].splitlines()[140]=='Exact method line 140'
    assert report['sources'][SID]['source_capture']['call_ids']==['source-000001','source-000002']
    save(files[1],url,sparse([128,166]).replace('Exact method line 166','Changed method line 166'))
    assert result(files)['checks']['SB07']=='failed'


def test_unfilled_gap_between_sparse_chunks_still_fails(tmp_path):
    files=bundle(tmp_path);url=files[3]
    save(files[1],url,'Methods ('+url+')\nTotal lines: 4\nL0: First\nL2: Third')
    save(files[1],url,'Methods ('+url+')\nTotal lines: 4\nL2: Third\nL3: Fourth')
    report=result(files)
    assert report['checks']['SB07']=='failed' and report['checks']['SB08']=='failed'
    assert report['status']=='source_bodies_incomplete' and report['sources']=={}


@pytest.mark.parametrize('payload',[
    {'text':'Invented plain article wrapper'},
    'Methods (https://example.com/different)\nTotal lines: 1\nL0: Original text',
    'Methods (https://example.com/methods)\nTotal lines: 1\nL0: Sign in to continue',
    'Methods (https://example.com/methods)\nTotal lines: 1\nL0: Original text\n[truncated]',
    'Methods (https://example.com/methods)\nTotal lines: 3\nL0: First\nL2: Third',
    'Methods (https://example.com/methods)\nTotal lines: 2\nL0: First\nL0: First',
])
def test_unsupported_mismatched_challenge_or_truncated_source_cannot_verify(tmp_path,payload):
    files=bundle(tmp_path);save(files[1],files[3],payload)
    report=result(files)
    assert report['status']=='source_bodies_incomplete' and report['checks']['SB07']=='failed'
    assert report['checks']['SB08']=='failed'


@pytest.mark.parametrize('mutation,check',[
    (lambda call:call.update(url='https://example.com/different'),'SB03'),
    (lambda call:call.update(source_id='src-000000000000'),'SB03'),
    (lambda call:call.update(id='source-000002'),'SB02'),
    (lambda call:call.update(completed_at='2999-01-01T00:00:00Z'),'SB04'),
    (lambda call:call.update(request={'authorization':'secret fixture'}),'SB02'),
    (lambda call:call['response'].update(path='../outside.json'),'SB05'),
    (lambda call:call['response'].update(bytes=True),'SB05'),
])
def test_index_identity_chronology_privacy_and_paths_are_guarded(tmp_path,mutation,check):
    files=bundle(tmp_path);save(files[1],files[3],page(files[3]))
    index=bodies.parse(files[1].read_bytes());mutation(index['calls'][0]);files[1].write_bytes(bodies.encoded(index))
    assert result(files)['checks'][check]=='failed'


def test_body_tampering_and_unindexed_files_fail(tmp_path):
    files=bundle(tmp_path);save(files[1],files[3],page(files[3]))
    response=files[1].parent/'responses/source-000001.json';original=response.read_bytes()
    response.write_bytes(original.replace(b'Methods complete',b'Altered content'))
    assert result(files)['checks']['SB05']=='failed'
    response.write_bytes(original);(files[1].parent/'unindexed.txt').write_text('not indexed')
    assert result(files)['checks']['SB06']=='failed'


def test_observation_references_require_the_original_body_but_history_does_not(tmp_path):
    packet={'assignment_id':'source-fixture','baseline_commit':'a'*40,'created_at':stamp(),
            'changes':[],'research_run':{'field_checks':[{'evidence_ids':['obs-012345abcdef']}]}}
    state={('source',SID):{'id':SID,'url':'https://example.com/methods'},
           ('observation','obs-012345abcdef'):{'source_ids':[SID]}}
    packet['changes']=[{'kind':'source','record':state[('source',SID)],'evidence_ids':[]}]
    files=bundle(tmp_path,packet,state)
    assert result(files)['required_source_ids']==[SID] and result(files)['checks']['SB08']=='failed'
    save(files[1],files[3],page(files[3]));assert result(files)['status']=='source_bodies_verified'
    value=bodies.parse(files[0].read_bytes());value['research_run']={};value['changes']=[]
    value['retained_record']={'evidence_ids':['src-000000000000']};files[0].write_bytes(bodies.encoded(value))
    assert result(files)['required_source_ids']==[]


def test_saved_unavailable_return_is_not_available_evidence_and_export_failure_fails(tmp_path):
    files=bundle(tmp_path)
    save(files[1],files[3],{'error':'Public source unavailable'},retrieval_status='unavailable')
    assert result(files)['checks']['SB08']=='failed'
    packet=bodies.parse(files[0].read_bytes());packet['changes'][0]['evidence_ids']=[]
    files[0].write_bytes(bodies.encoded(packet));assert result(files)['status']=='source_bodies_verified'
    bodies.capture(files[1],source_id=SID,url=files[3],tool='synthetic-visible-source',started_at=stamp(8),
                   completed_at=stamp(7),request={'open':[{'ref_id':files[3]}]},response_path=None)
    assert result(files)['checks']['SB10']=='failed'


def test_v4_receipt_requires_source_audit_and_binds_it_without_changing_v3(evidence,tmp_path,schemas):
    session,search_audit=record_session(evidence,tmp_path,schemas,[])
    kit=session.kit
    (kit/'research_source_bodies.py').write_bytes(Path(bodies.__file__).read_bytes())
    (kit/'source-bodies-contract.json').write_bytes(bodies.encoded(bodies.contract()))
    (kit/'baseline-records.json').write_bytes(bodies.encoded({'baseline_commit':session.packet['baseline_commit'],'records':[]}))
    manifest=bodies.parse((kit/'input-manifest.json').read_bytes())
    for name in ('research_source_bodies.py','source-bodies-contract.json','baseline-records.json'):
        manifest['files'][name]=bodies.pin((kit/name).read_bytes())
    (kit/'input-manifest.json').write_bytes(bodies.encoded(manifest))
    session=validation.Session(kit,session.args);session.schema('fixture');session.checks['mechanical']='passed'
    with pytest.raises(ValueError,match='SB11'):session.finish()
    assert not session.args.receipt.exists()
    index=evidence[0].parent/(evidence[0].stem+'.source-evidence/index.json');bodies.initialize(evidence[0],index)
    audit_path=evidence[0].with_name(evidence[0].stem+'.v000001.source-validation.json')
    report=bodies.audit(evidence[0],index,kit/'baseline-records.json',bodies.contract(),kit/'source-bodies-contract.json')
    audit_path.write_bytes(bodies.encoded(report));session.args.source_index=index;session.args.source_audit=audit_path
    receipt=session.finish()
    assert receipt['format']=='research-validation-v4' and receipt['checks']['source_bodies']=='passed'
    kwargs={'search_index_raw':evidence[1].read_bytes(),'search_audit_raw':search_audit.read_bytes(),
            'source_index_raw':index.read_bytes(),'source_audit_raw':audit_path.read_bytes()}
    assert validation.verify_receipt(receipt,session.raw,session.manifest_raw,sha256(session.manifest_raw).hexdigest(),**kwargs)['status']=='receipt_binding_verified'
    corrupted=deepcopy(report);corrupted['sources']['invented']={};audit_path.write_bytes(bodies.encoded(corrupted))
    with pytest.raises(ValueError,match='SB11'):session.finish()


def test_reader_fallback_recomputes_capture_and_retains_failed_attempt(fixture,baseline,tmp_path):
    packet,assignment=fixture;work=tmp_path/'.local';work.mkdir();files=bundle(work,packet,baseline)
    save(files[1],files[3],page(files[3]))
    report=result(files);audit_path=work/'capture.r1.v000001.source-validation.json';audit_path.write_bytes(bodies.encoded(report))
    packet=bodies.parse(files[0].read_bytes())
    def failed(_):raise reader.RetrievalError('http_status',403)
    receipt,_=review.run_review(packet,assignment,baseline,config(),work/'review',root=tmp_path,fetch=failed,
        invoke=fake_runtime,packet_raw=files[0].read_bytes(),source_index=files[1],source_audit=audit_path,source_baseline=files[2])
    assert receipt['accepted_units']==2
    snapshots=[bodies.parse(p.read_bytes()) for p in (work/'review/sources').glob('*.json') if not p.name.endswith('.http-attempt.json')]
    assert snapshots[0]['capture_origin']=='producer_tool_capture'
    assert snapshots[0]['direct_http_failure']['http_status']==403
    assert list((work/'review/sources').glob('*.http-attempt.json'))
    (files[1].parent/'responses/source-000001.json').write_bytes(b'"tampered"')
    with pytest.raises(ValueError,match='Source capture audit failed'):
        review.producer_captures(tmp_path,files[0].read_bytes(),baseline,files[1],audit_path,files[2])


def test_producer_baseline_cannot_substitute_evidence_registry(fixture,baseline,tmp_path):
    work=tmp_path/'.local';work.mkdir();files=bundle(work,fixture[0],baseline);save(files[1],files[3],page(files[3]))
    value=bodies.parse(files[2].read_bytes());value['records'][0]['record']['publisher']='Substituted publisher'
    files[2].write_bytes(bodies.encoded(value));audit_path=work/'capture.r1.v000001.source-validation.json'
    audit_path.write_bytes(bodies.encoded(result(files)))
    with pytest.raises(ValueError,match='pinned Git evidence registry'):
        review.producer_captures(tmp_path,files[0].read_bytes(),baseline,files[1],audit_path,files[2])


@pytest.mark.parametrize('error,code,status',[(reader.RetrievalError('http_status',403),'http_status',403),
    (socket.gaierror('private diagnostic must not leak'),'dns_error',None),
    (TimeoutError('private diagnostic must not leak'),'network_timeout',None)])
def test_diagnostics_are_safe_and_distinguish_failures(error,code,status):
    def failed(_):raise error
    snapshot,raw=reader.inspect_source({'id':SID,'url':'https://example.com/methods'},fetch=failed)
    assert snapshot['failure_code']==code and snapshot['http_status']==status and raw is None
    assert 'private diagnostic' not in json.dumps(snapshot)


