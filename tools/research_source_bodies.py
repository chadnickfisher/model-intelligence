"""Portable opened-source captures. Complete saved text is not execution or fact attestation."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import ipaddress
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlsplit

if __package__:
    from .research_search_receipts import encoded, instant, parse, pin, read, regular, write_new
else:
    from research_search_receipts import encoded, instant, parse, pin, read, regular, write_new

VERSION = 'research-source-bodies-v1'
MAX_CALLS = 1000
MAX_TEXT = 2 * 1024 * 1024
MAX_TOTAL_RESPONSES = 128 * 1024 * 1024
CALL_KEYS = {'id', 'source_id', 'url', 'tool', 'started_at', 'completed_at', 'request',
             'retrieval_status', 'capture_status', 'response', 'capture_error', 'extractor'}
LIMITS = 'Verifies saved responses, identity, dates and complete exposed text; not tool execution, raw HTTP HTML, factual truth, evidence review, research completeness or receiver acceptance.'
CHECKS = {
    'SB01': 'Save index.json with exactly format, assignment_id, baseline_commit and calls; match the packet identity and research-source-bodies-v1 format.',
    'SB02': 'Save every opened-source call with all required fields and sequential source-000001 IDs; preserve the actual tool name and complete public request object.',
    'SB03': 'Bind source_id and url to the declared packet/baseline source; source_id may be null only for an unavailable attempt that establishes no cited evidence.',
    'SB04': 'Save actual UTC Z timestamps with started_at <= completed_at <= packet.created_at <= validation time; never substitute publication or effective dates.',
    'SB05': 'Save the complete tool-visible return as UTF-8 JSON in responses/<call-id>.json; save read-back path, byte count and SHA-256 in response.',
    'SB06': 'Keep only index.json and indexed response files in <stem>.source-evidence; reject linked paths, unexpected files and changed response bytes.',
    'SB07': 'For available text use web-run-numbered-lines-v1: retain every numbered page or PDF chunk, including empty titles and PDF page labels, and require the exact source URL. A chunk may contain gaps; require every declared line and identical overlaps within each version. A changed version may start only when the previous version and the new return are independently complete; retain prior version hashes. Unsupported formats, incomplete combined pages and challenge/login bodies cannot supply evidence.',
    'SB08': 'Save an available complete capture for every current-check source in change envelopes, run evidence, discovery and resolution evidence; expand observation source_ids. Historical record citations alone require no new capture.',
    'SB09': 'For unavailable retrieval save retrieval_status=unavailable and its actual returned response; it supplies no evidence. Required unavailable sources fail completeness and keep affected research unresolved.',
    'SB10': 'If response export fails save capture_status=capture_failed, response=null and a nonempty capture_error; never reconstruct the return or claim complete capture.',
    'SB11': 'Run the frozen helper to save <stem>.v<attempt>.source-validation.json; bind exact packet, index, baseline, contract, responses and derived source text. Never author a success audit.',
    'SB12': 'Retain the audit limits and separate structural success from semantic review; source capture never grants execution attestation, receiver acceptance or research completion.',
}


def contract():
    return {'format': VERSION, 'call_fields': sorted(CALL_KEYS), 'checks': CHECKS,
            'extractors': ['web-run-numbered-lines-v1'], 'index_filename': 'index.json',
            'max_text_bytes_per_source':MAX_TEXT,'max_total_response_bytes':MAX_TOTAL_RESPONSES,
            'response_filename': 'responses/<call-id>.json',
            'audit_filename': '<stem>.v<attempt>.source-validation.json',
            'verified_status': 'source_bodies_verified', 'limits': LIMITS,
            'producer_preflight': {'required':'Run the bounded one-source export/readback/audit probe in the actual producer environment before claiming this route works there.',
                                  'unsupported':'Save the original return and precise failure; never rewrite an unsupported payload into numbered source text.',
                                  'local_test_limit':'Synthetic tests and current-task web captures do not certify Forge-native saving.'}}


def public_url(value):
    try:
        u = urlsplit(value)
        host = (u.hostname or '').lower().rstrip('.')
        if u.scheme != 'https' or not host or u.username or u.password or u.port not in {None, 443}:
            return False
        if host == 'localhost' or host.endswith(('.localhost', '.local', '.internal')):
            return False
        try:
            if not ipaddress.ip_address(host).is_global: return False
        except ValueError: pass
        return not any(k.lower() in {'token','access_token','sig','signature','api_key','key','authorization','credential'}
                       or k.lower().startswith('x-amz-') for k, _ in parse_qsl(u.query))
    except (ValueError, TypeError): return False


def public_request(value):
    if isinstance(value, dict):
        return all(str(k).lower() not in {'authorization','cookie','cookies','password','credentials','proxy','api_key','access_token'}
                   and public_request(v) for k,v in value.items())
    if isinstance(value, list): return all(public_request(v) for v in value)
    if isinstance(value, str):
        return not re.search(r'(?i)(?:\bfile:|[A-Z]:\\Users\\|\bsk-[A-Za-z0-9]{20,}|\bgh[pousr]_[A-Za-z0-9]{20,})', value) and \
               all(public_url(u.rstrip('.,);')) for u in re.findall(r'https?://[^\s<>"{}]+', value))
    return value is None or isinstance(value, (bool, int, float))


def catalog(packet, baseline):
    rows = baseline.get('records', []) if isinstance(baseline, dict) else []
    sources = {r['id']: r['record'] for r in rows if r['kind'] == 'source'}
    observations = {r['id']: r['record'] for r in rows if r['kind'] == 'observation'}
    sources.update({c['record']['id']:c['record'] for c in packet.get('changes', []) if c['kind']=='source'})
    return sources, observations


def evidence_refs(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {'evidence_ids','supporting_evidence_ids','contradictory_evidence_ids'}:
                if not isinstance(nested, list): raise ValueError('Evidence references must be an array')
                yield from nested
            else: yield from evidence_refs(nested)
    elif isinstance(value, list):
        for nested in value: yield from evidence_refs(nested)


def required_sources(packet, observations):
    refs = {i for c in packet.get('changes', []) for i in c.get('evidence_ids', [])}
    for key in ('research_run','scope_run','discovery_checks','resolutions'):
        refs.update(evidence_refs(packet.get(key, {})))
    result = set()
    for ident in refs:
        linked = observations.get(ident, {}).get('source_ids', [ident])
        if not linked: raise ValueError('Editorial observation cannot supply source-body evidence')
        result.update(linked)
    return result


def page_lines(response_raw, expected_url):
    """Extract only the explicitly supported, observed text response format."""
    response = parse(response_raw)
    if not isinstance(response, str): raise ValueError('Unsupported tool return; save the exact return and request an adapter')
    if re.search(r'(?i)(?:Warning: truncated output|[0-9]+ tokens truncated|\[truncated\])',response):
        raise ValueError('Truncated tool return')
    header = re.match(r'[^\n]* \((https://[^\n]+)\)\r?\n', response)
    totals = re.findall(r'Total lines: ([0-9]+)', response)
    if not header or header.group(1) != expected_url or len(totals) != 1:
        raise ValueError('Page identity or declared total differs')
    total = int(totals[0])
    if not 0 < total <= 20000: raise ValueError('Invalid declared page size')
    matches = list(re.finditer(r'L([0-9]+)(?:@P[0-9]+(?:-[0-9]+)?)?: ?', response))
    if not matches: raise ValueError('No numbered source lines')
    lines = {}
    for n, match in enumerate(matches):
        number = int(match.group(1))
        value = response[match.end():matches[n+1].start() if n+1<len(matches) else len(response)].rstrip('\r\n ')
        if not 0 <= number < total or number in lines: raise ValueError('Invalid or duplicate source line')
        lines[number] = value
    # Tool pagination can repeat navigation then jump to the requested region.
    # Preserve only the actual numbered lines here. audit() checks the union
    # of all chunks for this source, including exact coverage and overlaps.
    if re.search(r'(?i)(?:verify you are human|checking your browser|just a moment\.\.\.|access denied|enable javascript and cookies|sign in to continue)', '\n'.join(lines.values())):
        raise ValueError('Challenge or login text is unavailable evidence')
    return total, lines


def audit_attempt(packet_path, report_path):
    prefix = Path(packet_path).stem + '.v'
    name = Path(report_path).name
    if Path(report_path).absolute().parent != Path(packet_path).absolute().parent or \
       not name.startswith(prefix) or not re.fullmatch(r'[0-9]{6}\.source-validation\.json', name[len(prefix):]) or \
       name[len(prefix):].startswith('000000'):
        raise ValueError('SB11: source audit needs the packet stem and six-digit attempt beside the packet')
    return prefix + name[len(prefix):][:6]


def audit(packet_path, index_path, baseline_path, expected_contract, contract_path=None, *, captures=None):
    packet_raw, index_raw, baseline_raw = read(packet_path), read(index_path), read(baseline_path)
    packet, index, baseline = parse(packet_raw), parse(index_raw), parse(baseline_raw)
    contract_raw = read(contract_path) if contract_path else encoded(expected_contract)
    sources, observations = catalog(packet, baseline)
    root = regular(index_path).parent
    checks = {key:'passed' for key in CHECKS};errors=[];responses={};groups={};snapshots={};versions={}
    def reject(code, message):
        checks[code]='failed';errors.append({'check_id':code,'message':message})
    if expected_contract != contract() or parse(contract_raw) != expected_contract:
        reject('SB11','Pinned source-body contract differs from helper')
    if baseline.get('baseline_commit') != packet.get('baseline_commit'):
        reject('SB03','Baseline identity differs from packet')
    if not isinstance(index, dict) or set(index) != {'format','assignment_id','baseline_commit','calls'} or \
       index.get('format') != VERSION or any(index.get(k)!=packet.get(k) for k in ('assignment_id','baseline_commit')):
        reject('SB01','Index identity, format or fields differ')
    if Path(index_path).name!='index.json' or root.name!=Path(packet_path).stem+'.source-evidence':
        reject('SB06','Source evidence directory or index name differs')
    calls=index.get('calls',[]) if isinstance(index,dict) else []
    if not isinstance(calls,list) or len(calls)>MAX_CALLS:
        reject('SB02','Calls must be a bounded array');calls=[]
    try: created=instant(packet['created_at'])
    except (KeyError,ValueError,TypeError):
        reject('SB04','Invalid packet serialization timestamp');created=datetime.min.replace(tzinfo=timezone.utc)
    now=datetime.now(timezone.utc);expected_files={'index.json'};total_response_bytes=0
    for n,call in enumerate(calls,1):
        ident='source-'+str(n).zfill(6)
        if not isinstance(call,dict) or set(call)!=CALL_KEYS or call.get('id')!=ident:
            reject('SB02',ident+': call fields or sequence differ');continue
        source_id,url=call['source_id'],call['url']
        if (source_id is not None and not isinstance(source_id,str)) or not public_url(url) or \
           (source_id is None and call['retrieval_status']!='unavailable') or \
           (source_id is not None and (source_id not in sources or sources[source_id]['url']!=url)):
            reject('SB03',ident+': source identity/URL differs');continue
        if not isinstance(call['tool'],str) or not call['tool'].strip() or not isinstance(call['request'],dict) or \
           not call['request'] or not public_request(call['request']):reject('SB02',ident+': actual public request/tool required')
        try:
            start,end=instant(call['started_at'],True),instant(call['completed_at'],True)
            if not start<=end<=created<=now:raise ValueError()
        except (ValueError,TypeError):reject('SB04',ident+': invalid capture chronology')
        if call['retrieval_status'] not in {'available','unavailable'}:reject('SB09',ident+': invalid retrieval status')
        if call['capture_status']=='capture_failed':
            if call['response'] is not None or not isinstance(call['capture_error'],str) or not call['capture_error'].strip():
                reject('SB10',ident+': malformed export failure')
            reject('SB10',ident+': actual response export unavailable');continue
        if call['capture_status']!='saved' or call['capture_error'] is not None:
            reject('SB05',ident+': invalid saved response state');continue
        metadata=call['response'];name='responses/'+ident+'.json'
        expected_files.add(name)
        if not isinstance(metadata,dict) or set(metadata)!={'path','bytes','sha256'} or metadata.get('path')!=name or \
           type(metadata.get('bytes')) is not int or not isinstance(metadata.get('sha256'),str) or \
           not re.fullmatch(r'[a-f0-9]{64}',metadata['sha256']):
            reject('SB05',ident+': response metadata differs');continue
        try:
            total_response_bytes+=metadata['bytes']
            if total_response_bytes>MAX_TOTAL_RESPONSES:raise ValueError('Source capture byte budget exceeded')
            raw=read(root/name)
            if metadata!={'path':name,**pin(raw)}:raise ValueError('Response bytes/hash changed')
            parse(raw);responses[name]=pin(raw)
        except (ValueError,OSError,json.JSONDecodeError,UnicodeError):
            reject('SB05',ident+': response missing, invalid or changed');continue
        if call['retrieval_status']=='unavailable':continue
        if call['extractor']!='web-run-numbered-lines-v1':
            reject('SB07',ident+': unsupported extraction route');continue
        try:
            total,lines=page_lines(raw,url)
            group=groups.setdefault(source_id,{'url':url,'total':total,'lines':{},'calls':[], 'captured_at':call['completed_at']})
            conflicts=any(number in group['lines'] and group['lines'][number]!=value for number,value in lines.items())
            if group['url']!=url:raise ValueError('Page URL differs')
            if group['total']!=total or conflicts:
                if set(group['lines'])!=set(range(group['total'])) or set(lines)!=set(range(total)):
                    raise ValueError('Changed page versions must be independently complete')
                if instant(call['completed_at'])<instant(group['captured_at']):
                    raise ValueError('Changed page version predates its preceding capture')
                prior_text='\n'.join(group['lines'][n] for n in range(group['total']))+'\n'
                if not prior_text.strip() or len(prior_text.encode('utf-8'))>MAX_TEXT:
                    raise ValueError('Previous page version is empty or oversized')
                versions.setdefault(source_id,[]).append({'call_ids':group['calls'],
                    'captured_at':group['captured_at'],'visible_line_count':group['total'],
                    'text_sha256':sha256(prior_text.encode('utf-8')).hexdigest()})
                group={'url':url,'total':total,'lines':{},'calls':[], 'captured_at':call['completed_at']}
                groups[source_id]=group
            for number,value in lines.items():
                if number in group['lines'] and group['lines'][number]!=value:raise ValueError('Source overlap differs')
                group['lines'][number]=value
            group['calls'].append(ident)
            group['captured_at']=max(group['captured_at'],call['completed_at'],key=instant)
        except (ValueError,UnicodeError,json.JSONDecodeError) as exc:reject('SB07',ident+': '+str(exc))
    for ident,group in groups.items():
        if set(group['lines'])!=set(range(group['total'])):
            reject('SB07',ident+': missing numbered source lines');continue
        text='\n'.join(group['lines'][n] for n in range(group['total']))+'\n'
        raw=text.encode('utf-8')
        if not text.strip() or len(raw)>MAX_TEXT:reject('SB07',ident+': empty or oversized source text');continue
        snapshots[ident]={'source_id':ident,'url':group['url'],'final_url':group['url'],'redirects':[],
                         'captured_at':group['captured_at'],'status':'available','failure':None,
                         'body_sha256':sha256(raw).hexdigest(),'text_sha256':sha256(raw).hexdigest(),
                         'content_type':'text/plain; charset=utf-8','text':text,'capture_origin':'producer_tool_capture',
                         'source_capture':{'call_ids':group['calls'],'visible_line_count':group['total'],
                                           'representation':'complete tool-visible numbered text; not raw HTTP HTML'}}
        if ident in versions:snapshots[ident]['source_capture']['prior_versions']=versions[ident]
    try:
        required=required_sources(packet,observations)
        if not required<=snapshots.keys():reject('SB08','Current-check sources lack complete available captures: '+', '.join(sorted(required-snapshots.keys())))
    except (ValueError,TypeError):reject('SB08','Current source references are invalid');required=set()
    try:
        actual=set()
        for n,path in enumerate(root.iterdir()):
            regular(path)
            if n>2:raise ValueError('Unexpected source evidence members')
            if path.is_file():actual.add(path.name)
            elif path.name=='responses' and path.is_dir():
                for i,response in enumerate(path.iterdir()):
                    regular(response)
                    if i>=MAX_CALLS or not response.is_file():raise ValueError('Unexpected response member')
                    actual.add(response.relative_to(root).as_posix())
            else:raise ValueError('Unexpected source evidence member')
        if actual!=expected_files:reject('SB06','Unexpected or missing source evidence files')
    except (ValueError,OSError):reject('SB06','Linked or unreadable source evidence path')
    if read(packet_path)!=packet_raw or read(index_path)!=index_raw or read(baseline_path)!=baseline_raw:
        reject('SB11','Capture inputs changed during audit')
    for name, expected in responses.items():
        try:
            if pin(read(root/name))!=expected:reject('SB06','Source response changed during audit')
        except (ValueError,OSError):reject('SB06','Source response unavailable during audit')
    if captures is not None and not errors: captures.update(snapshots)
    return {'format':VERSION,'status':'source_bodies_verified' if not errors else 'source_bodies_incomplete',
            'packet':pin(packet_raw),'index':pin(index_raw),'baseline':pin(baseline_raw),'contract':pin(contract_raw),
            'responses':responses,'checks':checks,'errors':errors,'required_source_ids':sorted(required),
            'sources':{ident:{key:value for key,value in row.items() if key!='text'} for ident,row in snapshots.items()},
            'limits':LIMITS}


def initialize(packet_path,index_path):
    packet=parse(read(packet_path));root=regular(index_path).parent
    if Path(index_path).name!='index.json' or root.name!=Path(packet_path).stem+'.source-evidence':
        raise ValueError('SB06: use <stem>.source-evidence/index.json')
    value={'format':VERSION,'assignment_id':packet['assignment_id'],'baseline_commit':packet['baseline_commit'],'calls':[]}
    write_new(index_path,encoded(value));return value


def capture(index_path,*,source_id,url,tool,started_at,completed_at,request,response_path,
            retrieval_status='available',extractor='web-run-numbered-lines-v1'):
    index_path=regular(index_path);raw=read(index_path);index=parse(raw)
    if index.get('format')!=VERSION or len(index['calls'])>=MAX_CALLS:raise ValueError('Invalid/full source index')
    ident='source-'+str(len(index['calls'])+1).zfill(6)
    row={'id':ident,'source_id':source_id,'url':url,'tool':tool,'started_at':started_at,'completed_at':completed_at,
         'request':request,'retrieval_status':retrieval_status,'extractor':extractor,
         'capture_status':'capture_failed','response':None,'capture_error':'Actual tool response export unavailable'}
    if response_path is not None and Path(response_path).exists():
        try:
            response=read(response_path);parse(response)
        except (ValueError,OSError,UnicodeError):
            row['capture_error']='Actual response export is empty, invalid or unavailable'
        else:
            name='responses/'+ident+'.json';write_new(index_path.parent/name,response)
            retained=read(index_path.parent/name)
            if retained!=response:raise ValueError('Readback differs')
            row.update(capture_status='saved',response={'path':name,**pin(retained)},capture_error=None)
    if read(index_path)!=raw:raise ValueError('Source index changed while capturing')
    index['calls'].append(row);temporary=index_path.with_name('index.json.part')
    write_new(temporary,encoded(index));os.replace(temporary,index_path)
    return row


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    init=sub.add_parser('init');init.add_argument('--packet',type=Path,required=True);init.add_argument('--index',type=Path,required=True)
    cap=sub.add_parser('capture');cap.add_argument('--index',type=Path,required=True)
    for name in ('url','tool','started-at','completed-at'):cap.add_argument('--'+name,required=True)
    cap.add_argument('--source-id');cap.add_argument('--request',type=Path,required=True);cap.add_argument('--response',type=Path)
    cap.add_argument('--retrieval-status',choices=['available','unavailable'],default='available')
    cap.add_argument('--extractor',default='web-run-numbered-lines-v1')
    check=sub.add_parser('check')
    for name in ('packet','index','baseline','contract','report'):check.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    if a.mode=='init':result=initialize(a.packet,a.index)
    elif a.mode=='capture':result=capture(a.index,source_id=a.source_id,url=a.url,tool=a.tool,started_at=a.started_at,
        completed_at=a.completed_at,request=parse(read(a.request)),response_path=a.response,retrieval_status=a.retrieval_status,extractor=a.extractor)
    else:
        audit_attempt(a.packet,a.report);result=audit(a.packet,a.index,a.baseline,parse(read(a.contract)),a.contract)
        write_new(a.report,encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in {'sources','request'}},ensure_ascii=False))
    return int(result.get('status')=='source_bodies_incomplete' or result.get('capture_status')=='capture_failed')


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'source_capture_failed','reason':str(exc)[:500]}));raise SystemExit(1)
