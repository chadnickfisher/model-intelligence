"""Saved search evidence cannot silently disappear behind a helper success."""
from argparse import Namespace
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

from tools import research_search_receipts as receipts
from tools.research_validation import REQUIRED, Session, pin, verify_receipt


@pytest.fixture
def evidence(tmp_path):
    query = {'query':'exact model exact task','checked_at':'2026-10-12',
             'outcome':'sources_located','urls':['https://example.org/study'],'notes':'Returned original study.'}
    packet = {'assignment_id':'fixture','baseline_commit':'a'*40,'package_type':'fixture',
              'created_at':'2026-10-12T00:03:00Z',
              'research_run':{'field_checks':[{'search_references':[query]}]},
              'discovery_checks':[{'search_references':[query]}]}
    packet_path=tmp_path/'packet.json';packet_path.write_bytes(receipts.encoded(packet))
    index=tmp_path/'packet.search-evidence/index.json'
    receipts.initialize(packet_path,index)
    request=tmp_path/'request.json';request.write_bytes(receipts.encoded({'search_query':[{'q':query['query']}]}))
    queries=tmp_path/'queries.json';queries.write_bytes(receipts.encoded([query]))
    response=tmp_path/'response.json'
    raw=b'{"results": [{"title":"Study", "url":"https://example.org/study", "snippet":"Actual exposed result"}]}\n'
    response.write_bytes(raw)
    receipts.capture(index,request,queries,response,'search_service.web_run','2026-10-12T00:01:00Z','2026-10-12T00:02:00Z')
    return packet_path,index,query,response


def check(evidence):
    return receipts.audit(evidence[0],evidence[1],receipts.contract())


def edit_index(evidence,callback):
    index=json.loads(evidence[1].read_bytes());callback(index)
    evidence[1].write_bytes(receipts.encoded(index))


def test_exact_response_readback_and_all_packet_locations(evidence):
    report=check(evidence)
    assert report['status']=='search_receipts_verified'
    assert report['checks']=={key:'passed' for key in receipts.CHECKS}
    assert len(report['links'])==2
    assert all(row['call_ids']==['search-000001'] for row in report['links'])
    captured=evidence[1].parent/'responses/search-000001.json'
    assert captured.read_bytes()==evidence[3].read_bytes()
    assert report['receiver_acceptance']==report['execution_attestation']=='not_evaluated'


def test_canonical_carry_forward_searches_do_not_gain_new_receipt_requirements(evidence):
    packet=json.loads(evidence[0].read_bytes())
    packet['changes']=[{'kind':'research_coverage','record':{'search_references':[
        {'query':'historic search','outcome':'sources_found','notes':['Old source boundary retained']} ]}}]
    evidence[0].write_bytes(receipts.encoded(packet))
    assert check(evidence)['status']=='search_receipts_verified'


def test_scoped_resolution_searches_need_their_own_actual_query_receipt(evidence):
    packet=json.loads(evidence[0].read_bytes());packet['scope_run']=packet.pop('research_run')
    extra=deepcopy(evidence[2]);extra['query']='another identity search'
    packet['resolutions']=[{'search_references':[extra]}]
    evidence[0].write_bytes(receipts.encoded(packet))
    report=check(evidence)
    assert report['checks']['SR08']=='failed'
    assert any(e['message'].startswith('/resolutions/0/search_references/0') for e in report['errors'])


@pytest.mark.parametrize('change,code',[
    ('missing','SR06'),('digest','SR07'),('path','SR06'),('query','SR08'),
    ('extra','SR10'),('identity','SR01'),('timing','SR04'),('call-id','SR02'),
    ('null','SR06'),('query-field','SR05'),('failed-capture','SR09')])
def test_incomplete_or_tampered_capture_never_passes(evidence,change,code):
    root=evidence[1].parent
    if change=='missing':(root/'responses/search-000001.json').unlink()
    elif change=='extra':(root/'extra.json').write_text('{}')
    elif change=='null':(root/'responses/search-000001.json').write_text('null')
    else:
        def mutate(index):
            call=index['calls'][0]
            if change=='digest':call['response']['sha256']='0'*64
            elif change=='path':call['response']['path']='../response.json'
            elif change=='query':call['queries'][0]['query']='similar wording is not the same query'
            elif change=='identity':index['baseline_commit']='b'*40
            elif change=='timing':call['completed_at']='2026-10-12T00:04:00Z'
            elif change=='call-id':call['id']='search-000002'
            elif change=='query-field':call['queries'][0]['receipt_id']='invented packet key'
            elif change=='failed-capture':call.update(capture_status='capture_failed',response=None,capture_error='Export failed')
        edit_index(evidence,mutate)
    report=check(evidence)
    assert report['status']=='search_receipts_incomplete'
    assert report['checks'][code]=='failed'


def test_missing_export_is_retained_as_failure_not_reconstructed(evidence,tmp_path):
    packet,index,query,_=evidence
    call=receipts.capture(index,tmp_path/'request.json',tmp_path/'queries.json',tmp_path/'absent.json',
                          'search_service.web_run','2026-10-12T00:01:00Z','2026-10-12T00:02:00Z')
    assert call['id']=='search-000002' and call['capture_status']=='capture_failed'
    assert call['response'] is None and 'ValueError' in call['capture_error']
    assert check(evidence)['checks']['SR09']=='failed'


def test_changed_response_during_audit_is_rejected(evidence,monkeypatch):
    original=receipts.read;counts={}
    def changing(path):
        path=Path(path);counts[path]=counts.get(path,0)+1
        raw=original(path)
        if path.name=='search-000001.json' and counts[path]>1:return raw+b' '
        return raw
    monkeypatch.setattr(receipts,'read',changing)
    assert check(evidence)['checks']['SR11']=='failed'


def test_duplicate_json_keys_and_nonfinite_data_are_rejected():
    for raw in (b'{"query":"a","query":"b"}',b'{"x":NaN}'):
        with pytest.raises(ValueError):receipts.parse(raw)


def new_session(evidence,tmp_path):
    kit=tmp_path/'kit';kit.mkdir()
    for name in REQUIRED:(kit/name).write_text('{}')
    (kit/'schemas.json').write_bytes(receipts.encoded({'fixture':{'type':'object'}}))
    (kit/'research_search_receipts.py').write_bytes(Path(receipts.__file__).read_bytes())
    (kit/'search-receipts-contract.json').write_bytes(receipts.encoded(receipts.contract()))
    names=REQUIRED|{'research_search_receipts.py','search-receipts-contract.json'}
    manifest={'assignment_id':'fixture','baseline_commit':'a'*40,
              'files':{name:pin((kit/name).read_bytes()) for name in names}}
    (kit/'input-manifest.json').write_bytes(receipts.encoded(manifest))
    report_path=tmp_path/'packet.v000001.search-validation.json'
    report=receipts.audit(evidence[0],evidence[1],receipts.contract(),kit/'search-receipts-contract.json')
    report_path.write_bytes(receipts.encoded(report))
    args=Namespace(packet=evidence[0],receipt=tmp_path/'packet.v000001.validation.json',extend=False,
                   search_index=evidence[1],search_audit=report_path)
    session=Session(kit,args);session.schema('fixture');session.checks['mechanical']='passed'
    return session,report_path


def test_v2_structural_receipt_requires_verified_search_artifacts(evidence,tmp_path):
    session,report=new_session(evidence,tmp_path)
    receipt=session.finish()
    assert receipt['format']=='research-validation-v2'
    assert receipt['checks']['search_receipts']=='passed'
    assert verify_receipt(receipt,session.raw,session.manifest_raw,sha256(session.manifest_raw).hexdigest(),
                          search_index_raw=evidence[1].read_bytes(),search_audit_raw=report.read_bytes())['status']=='receipt_binding_verified'
    with pytest.raises(ValueError,match='required for v2'):
        verify_receipt(receipt,session.raw,session.manifest_raw,sha256(session.manifest_raw).hexdigest())


@pytest.mark.parametrize('problem',['missing-arguments','changed-response','forged-audit'])
def test_v2_cannot_bypass_search_audit_with_claimed_success(evidence,tmp_path,problem):
    session,report=new_session(evidence,tmp_path)
    if problem=='missing-arguments':session.args.search_index=None
    elif problem=='changed-response':(evidence[1].parent/'responses/search-000001.json').write_text('{}')
    else:
        value=json.loads(report.read_bytes());value['links']=[];report.write_bytes(receipts.encoded(value))
    with pytest.raises(ValueError,match='SR12'):session.finish()
    assert not session.args.receipt.exists()


def test_cli_writes_failed_audit_but_exits_nonzero(evidence,tmp_path):
    (evidence[1].parent/'responses/search-000001.json').unlink()
    contract=tmp_path/'contract.json';contract.write_bytes(receipts.encoded(receipts.contract()))
    report=tmp_path/'packet.v000001.search-validation.json'
    result=subprocess.run([sys.executable,str(Path(receipts.__file__)),'check','--packet',str(evidence[0]),
                           '--index',str(evidence[1]),'--contract',str(contract),'--report',str(report)],capture_output=True,text=True)
    assert result.returncode==1 and json.loads(report.read_bytes())['status']=='search_receipts_incomplete'


@pytest.mark.parametrize('filename',['packet.search-validation.json','other.v000001.search-validation.json',
                                    'packet.v000000.search-validation.json','packet.v1.search-validation.json'])
def test_audit_attempt_filename_cannot_drift(filename):
    with pytest.raises(ValueError,match='SR12'):receipts.audit_attempt('packet.json',filename)


def test_audit_report_must_be_beside_packet():
    with pytest.raises(ValueError,match='SR12'):
        receipts.audit_attempt('work/packet.json','other/packet.v000001.search-validation.json')
