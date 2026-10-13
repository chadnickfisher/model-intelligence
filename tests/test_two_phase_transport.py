from copy import deepcopy
import json
import pytest
from tools import research_two_phase as p

def assignment():
    a={'protocol':p.VERSION,'kind':'assignment','assignment_id':'test-two-phase','revision':1,
       'baseline_commit':'a'*40,'subject':{'model_id':'example-model','provider_id':'example-provider',
          'access_id':'example-access','tier':'Standard','routing':'global'},
       'questions':[{'id':'insight','kind':'task_insight','field_ids':[],'task_ids':['coding.scoped_edit'],'text':'Fixture'}],
       'scope_sha256':'0'*64,'schema_sha256':p.pin(p.encoded(p.SCHEMA))['sha256'],'policy_version':p.POLICY,
       'rubric_sha256':'b'*64,'context_read_set':[], 'created_at':'2026-10-13T12:00:00+00:00',
       'expires_at':'2026-10-13T12:30:00+00:00','bounds':{'max_sources':5,'max_findings':10,
          'max_source_bytes':2097152,'max_wait_seconds':240},'allowed_urls':[],
       'source_policy':{'kind':'public_https','max_redirects':4},
       'producer':{'configured_name':'Example','identity_origin':'explicit_initialization',
          'platform_attested':False,'native_invocation_id':None}}
    a['scope_sha256']=p.pin(p.encoded(p.scope(a)))['sha256'];return a

def frame(a,payload,parent):
    return {'protocol':p.VERSION,'kind':'response_frame','assignment_id':a['assignment_id'],'revision':a['revision'],
        'phase':payload['kind'],'assignment_sha256':p.pin(p.encoded(a))['sha256'],'parent_sha256':parent['sha256'],
        'response_challenge':'c'*32,'payload':payload}

def prepare(tmp_path):
    a=assignment();run=p.Run(tmp_path);run.issue(a)
    discovery={'protocol':p.VERSION,'kind':'discovery','status':'complete','sources':[
        {'question_id':'insight','url':'https://example.com/source','location':'Fixture','relevance':'Fixture','role':'unknown'}],'gaps':[]}
    raw=p.encoded(frame(a,discovery,p.pin(p.encoded(a))))
    run.receive(raw,'discovery',p.pin(p.encoded(a)),'c'*32,now='2026-10-13T12:01:00+00:00')
    b={'protocol':p.VERSION,'kind':'bundle','assignment_id':a['assignment_id'],'revision':1,'parent_discovery':p.pin(raw),
        'subject':a['subject'],'questions':a['questions'],'sources':[],'facts':[],'failures':['Fixture unavailable source'],
        'outside_scope':'not_checked'}
    run.evidence_ready(b)
    payload={'protocol':p.VERSION,'kind':'analysis','status':'partial','findings':[],
        'judgments':[{'invalid':'Individual observation intentionally malformed'}],
        'inspected_source_ids':[],'inspection_reported_at':None,'gaps':['Fixture'],'additional_sources':[]}
    return a,b,run,frame(a,payload,p.pin(p.encoded(b)))

def test_receiver_preserves_bad_item_for_isolation_and_replay(tmp_path):
    a,b,run,f=prepare(tmp_path);raw=json.dumps(f).encode();parent=p.pin(p.encoded(b))
    result=run.receive(raw,'analysis',parent,'c'*32,now='2026-10-13T12:02:00+00:00')
    assert result['receipt']['item_validation']=='deferred_to_observation_compiler'
    original=(tmp_path/'analysis-receipt.json').read_bytes()
    (tmp_path/'analysis-receipt.json').unlink()
    replay=p.Run(tmp_path).receive(raw,'analysis',parent,'c'*32,now='2026-10-14T12:00:00+00:00')
    assert replay['status']=='duplicate' and (tmp_path/'analysis-receipt.json').read_bytes()==original
    assert (tmp_path/'incoming'/(p.pin(raw)['sha256']+'.json')).read_bytes()==raw

@pytest.mark.parametrize('change',['parent','challenge','budget','phase','expired'])
def test_global_errors_reject_and_preserve_original(tmp_path,change):
    a,b,run,f=prepare(tmp_path)
    if change=='parent':f['parent_sha256']='0'*64
    if change=='challenge':f['response_challenge']='0'*32
    if change=='budget':f['payload']['judgments']*=11
    if change=='phase':f['phase']='discovery'
    raw=p.encoded(f)
    with pytest.raises(Exception):run.receive(raw,'analysis',p.pin(p.encoded(b)),'c'*32,
        now='2026-10-13T13:00:00+00:00' if change=='expired' else '2026-10-13T12:02:00+00:00')
    assert run.get('phase')=='evidence_ready'
    assert (tmp_path/'incoming'/(p.pin(raw)['sha256']+'.json')).exists()

@pytest.mark.parametrize('url',['http://example.com','https://127.0.0.1','https://[::1]',
    'https://169.254.169.254','https://localhost','https://a.internal','https://user:pass@example.com','https://example.com:444'])
def test_source_policy_rejects_unsafe_urls(url):assert not p.public_https(url)

def test_source_policy_allows_discovered_public_url_but_not_unknown_protocol():
    assert p.public_https('https://example.com/new-evidence')
    a=assignment();p.validate(a,'assignment')
    with pytest.raises(Exception):p.validate({**a,'protocol':'two-phase/99'})

def test_duplicate_keys_and_nonfinite_json():
    for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1e999}'):
        with pytest.raises(ValueError):p.parse(raw)

def test_discovery_isolates_unsafe_malformed_and_duplicate_leads(tmp_path):
    a=assignment();good={'question_id':'insight','url':'https://example.com/source',
        'location':'Exact heading','relevance':'Fixture','role':'unknown'}
    d={'protocol':p.VERSION,'kind':'discovery','status':'partial','sources':[
        good,{**good,'url':'https://127.0.0.1/private'},{'malformed':'fixture'},good],'gaps':[]}
    selected,failures=p.partition_discovery(d,a)
    assert selected['sources']==[good] and len(failures)==3
    run=p.Run(tmp_path);run.issue(a)
    result=run.receive(p.encoded(frame(a,d,p.pin(p.encoded(a)))),'discovery',p.pin(p.encoded(a)),'c'*32,
        now='2026-10-13T12:01:00+00:00')
    assert result['status']=='received'
    assert not p.public_https('https://example.com/source?access_token=secret')
