"""Versioned two-phase transport validation. No inference or semantic research review."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
import ipaddress, json, os, re, sqlite3
from jsonschema import Draft202012Validator, FormatChecker

VERSION = 'two-phase/2'
POLICY = 'task-suitability/2-draft'
SCHEMA = json.loads((Path(__file__).resolve().parents[1]/'schema/research-two-phase.schema.json').read_bytes())
DEFINITIONS = SCHEMA['$defs']
JUDGMENT = DEFINITIONS['analysis']['properties']['judgments']['items']
FINDING = DEFINITIONS['analysis']['properties']['findings']['items']
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

def encoded(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()

def pin(raw): return {'bytes':len(raw),'sha256':sha256(raw).hexdigest()}

def parse(raw):
    def unique(pairs):
        result = {}
        for key,value in pairs:
            if key in result: raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    def finite(value): raise ValueError('Nonfinite JSON value')
    value = json.loads(raw,object_pairs_hook=unique,parse_constant=finite)
    encoded(value)  # catches overflow such as 1e999 as well
    return value

def immutable(path,raw):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=raw: raise ValueError('Immutable bytes conflict')
        return 'duplicate'
    temp = path.with_name(path.name+'.part')
    # A retained partial from an interrupted write is never automatically trusted.
    if temp.exists():
        if temp.read_bytes()!=raw: raise ValueError('Interrupted immutable write differs')
    else:
        with temp.open('xb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    temp.rename(path)
    if path.read_bytes()!=raw: raise ValueError('Immutable readback differs')
    return 'created'

def public_https(url):
    try:
        parts = urlsplit(url)
        if parts.scheme!='https' or not parts.hostname or parts.username or parts.password or parts.fragment \
                or parts.port not in (None,443): return False
        if set(k.lower() for k in parse_qs(parts.query)) & {'token','access_token','api_key','apikey','authorization','signature','x-amz-signature'}:
            return False
        host = parts.hostname.lower()
        if host=='localhost' or host.endswith(('.localhost','.local','.internal')) or '.' not in host: return False
        try: return ipaddress.ip_address(host).is_global
        except ValueError: return bool(re.fullmatch('[a-z0-9.-]+',host))
    except ValueError: return False

def scope(a):
    return {k:a[k] for k in ('subject','questions','bounds','allowed_urls','source_policy')}

def validate(value,kind=None):
    VALIDATOR.validate(value)
    if kind is not None and value['kind']!=kind: raise ValueError('Unexpected protocol kind')
    if value['kind']=='assignment':
        if value['scope_sha256']!=pin(encoded(scope(value)))['sha256'] or value['schema_sha256']!=pin(encoded(SCHEMA))['sha256']:
            raise ValueError('Assignment contract pin differs')
        for r in value['context_read_set']:
            if r['sha256']!=pin(encoded(r['value']))['sha256']: raise ValueError('Context pin differs')
        if len({q['id'] for q in value['questions']})!=len(value['questions']): raise ValueError('Duplicate question identity')
    if value['kind']=='snapshot' and value['status']=='readable' and (value['original'] is None or value['readable'] is None):
        raise ValueError('Readable source requires pins')
    if value['kind']=='fact' and value['status']=='extracted' and value['field_id'].startswith('pricing.'):
        if type(value['value']) not in (int,float) or value['unit'] is None or value['currency'] is None:
            raise ValueError('Price requires numeric amount, currency and unit')
    if value['kind']=='bundle':
        ids = [s['id'] for s in value['sources']]
        if len(set(ids))!=len(ids): raise ValueError('Duplicate source identity')
        for s in value['sources']:
            for v in s['views']:
                if v['parent_readable_sha256']!=s['readable']['sha256'] or \
                        v['content_sha256']!=pin(v['content'].encode())['sha256'] or len(v['content'])!=v['end_char']-v['start_char']:
                    raise ValueError('Saved view pin differs')
    return value

def validate_payload(payload,a,bundle=None):
    validate(payload)
    questions = {q['id']:q for q in a['questions']}
    if payload['kind']=='discovery':
        urls = [s['url'] for s in payload['sources']]
        if len(urls)>a['bounds']['max_sources'] or len(set(urls))!=len(urls): raise ValueError('Source budget or duplicate URL')
        if any(not public_https(u) or a['allowed_urls'] and u not in a['allowed_urls'] for u in urls):
            raise ValueError('URL outside issued source policy')
        if any(s['question_id'] not in questions for s in payload['sources']): raise ValueError('Unassigned question')
        return payload
    if payload['kind']!='analysis' or bundle is None: raise ValueError('Saved bundle required')
    validate(bundle,'bundle')
    known = {s['id']:s for s in bundle['sources']}; inspected = set(payload['inspected_source_ids'])
    if not inspected <= set(known): raise ValueError('Unknown inspected source')
    if len(payload['findings'])+len(payload['judgments'])>a['bounds']['max_findings']: raise ValueError('Observation budget')
    for item in payload['findings']+payload['judgments']:
        q = questions.get(item['question_id'])
        if q is None: raise ValueError('Unassigned question')
        cited = set(item['source_ids']+item['contrary_source_ids'])
        if not cited <= inspected: raise ValueError('Uninspected or unknown citation')
        if 'task_id' in item:
            if q['kind']!='task_insight' or item['task_id'] not in q['task_ids']: raise ValueError('Unassigned task')
            boundary = item['positive_boundary']
            if item['suitability']['level']=='not_supported' and boundary is None: raise ValueError('Positive boundary required')
            if boundary and not set(boundary['source_ids']) <= cited: raise ValueError('Uncited boundary')
        else:
            for passage in item['passages']:
                if passage['source_id'] not in cited or passage['view_id'] not in {v['id'] for v in known[passage['source_id']]['views']}:
                    raise ValueError('Passage outside cited saved views')
    if any(r['question_id'] not in questions or not public_https(r['url']) for r in payload['additional_sources']):
        raise ValueError('Unassigned or unsafe extra source')
    return payload

def partition_discovery(payload,a):
    """Keep a bad individual lead from preventing collection of independent good leads."""
    if not isinstance(payload.get('sources'),list):raise ValueError('Source list required')
    shell=deepcopy(payload);shell['sources']=[];validate(shell,'discovery')
    if len(payload['sources'])>a['bounds']['max_sources']:raise ValueError('Source budget exceeded')
    good=[];failures=[];seen=set()
    for ordinal,lead in enumerate(payload['sources'],1):
        try:
            validate_payload({**shell,'sources':[lead]},a)
            if lead['url'] in seen:raise ValueError('Duplicate source URL')
            seen.add(lead['url']);good.append(lead)
        except Exception as error:
            failures.append({'ordinal':ordinal,'question_id':lead.get('question_id') if isinstance(lead,dict) else None,
                'reason':'invalid_source_lead','error_class':type(error).__name__})
    return {**shell,'sources':good},failures

def envelope(frame,a,parent,challenge,*,received_at,bundle=None):
    validate(a,'assignment')
    if frame.get('phase')=='analysis':
        # Validate framing and aggregate budgets before isolating individual observations.
        shell = deepcopy(frame)
        if not isinstance(shell.get('payload'),dict): raise ValueError('Malformed analysis payload')
        for key in ('findings','judgments'):
            if not isinstance(shell['payload'].get(key),list): raise ValueError('Observation list required')
            shell['payload'][key] = []
        validate(shell,'response_frame')
        if len(frame['payload']['findings'])+len(frame['payload']['judgments'])>a['bounds']['max_findings']:
            raise ValueError('Observation budget')
        shell['payload']['inspected_source_ids']=[s for s in shell['payload']['inspected_source_ids']
            if s in {source['id'] for source in bundle['sources']}]
        validate_payload(shell['payload'],a,bundle)
    elif frame.get('phase')=='discovery':
        shell=deepcopy(frame)
        if not isinstance(shell.get('payload'),dict):raise ValueError('Malformed discovery payload')
        shell['payload']['sources']=[];validate(shell,'response_frame')
        partition_discovery(frame['payload'],a)
    else: validate(frame,'response_frame')
    if (frame['assignment_id'],frame['revision'],frame['assignment_sha256'],frame['parent_sha256'],frame['response_challenge']) != (
        a['assignment_id'],a['revision'],pin(encoded(a))['sha256'],parent['sha256'],challenge):
        raise ValueError('Response binding mismatch')
    if frame['payload']['kind']!=frame['phase']: raise ValueError('Response phase differs')
    if frame['phase']=='discovery':
        if parent!=pin(encoded(a)): raise ValueError('Discovery parent differs')
        partition_discovery(frame['payload'],a)
    return {'protocol':VERSION,'kind':'processing_receipt','assignment':pin(encoded(a)),
        'parent':parent,'original_baseline_commit':a['baseline_commit'],'received_at':received_at,
        'payload_sha256':pin(encoded(frame['payload']))['sha256'],
        'item_validation':'deferred_to_observation_compiler' if frame['phase']=='analysis' else 'discovery_checked',
        'semantic_review_performed':False,'producer_attestation_proven':False}

class Run:
    """One immutable revision, durable original delivery and recoverable committed receipts."""
    def __init__(self,directory):
        self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.directory/'state.sqlite',timeout=10)
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY,value TEXT)'); self.db.commit()
    def get(self,key):
        row=self.db.execute('SELECT value FROM state WHERE key=?',(key,)).fetchone()
        return json.loads(row[0]) if row else None
    def put(self,key,value): self.db.execute('INSERT OR REPLACE INTO state VALUES (?,?)',(key,json.dumps(value)))
    def issue(self,a):
        validate(a,'assignment'); immutable(self.directory/'assignment.json',encoded(a))
        with self.db:
            if self.get('assignment') not in (None,a): raise ValueError('Another assignment already issued')
            if self.get('assignment') is None: self.put('assignment',a);self.put('phase','assigned')
    def receive(self,raw,phase,parent,challenge,*,now=None):
        if phase not in ('discovery','analysis'): raise ValueError('Unsupported receive phase')
        raw_pin=pin(raw); immutable(self.directory/'incoming'/(raw_pin['sha256']+'.json'),raw)
        frame=parse(raw); at=now or datetime.now(timezone.utc).isoformat()
        self.db.execute('BEGIN IMMEDIATE')
        try:
            a=self.get('assignment'); previous=self.get(phase)
            if previous:
                if previous['raw']!=raw_pin or previous['receipt']['parent']!=parent or previous['challenge']!=challenge:
                    raise ValueError('Conflicting response or phase context')
                self.db.commit(); immutable(self.directory/(phase+'-receipt.json'),encoded(previous['receipt']))
                return {'status':'duplicate','receipt':previous['receipt']}
            if self.get('phase')!=('assigned' if phase=='discovery' else 'evidence_ready'): raise ValueError('Wrong receive state')
            if datetime.fromisoformat(at)>datetime.fromisoformat(a['expires_at']): raise ValueError('Assignment expired')
            if frame['phase']!=phase: raise ValueError('Wrong response slot')
            b=self.get('bundle')
            if phase=='analysis' and parent!=pin(encoded(b)): raise ValueError('Wrong saved bundle')
            receipt=envelope(frame,a,parent,challenge,received_at=at,bundle=b)
            self.put(phase,{'raw':raw_pin,'receipt':receipt,'challenge':challenge})
            self.put('phase',phase+'_received');self.db.commit()
            immutable(self.directory/(phase+'-receipt.json'),encoded(receipt))
            return {'status':'received','receipt':receipt}
        except Exception:
            self.db.rollback();raise
    def evidence_ready(self,b):
        validate(b,'bundle'); self.db.execute('BEGIN IMMEDIATE')
        try:
            a=self.get('assignment'); previous=self.get('bundle')
            if previous:
                if previous!=b: raise ValueError('Evidence correction requires new revision')
                self.db.commit();return 'duplicate'
            if self.get('phase')!='discovery_received' or any(b[k]!=a[k] for k in ('assignment_id','revision','subject','questions')):
                raise ValueError('Evidence state or scope differs')
            if b['parent_discovery']!=self.get('discovery')['raw']: raise ValueError('Discovery parent differs')
            immutable(self.directory/'evidence-bundle.json',encoded(b));self.put('bundle',b);self.put('phase','evidence_ready');self.db.commit()
            return 'created'
        except Exception:
            self.db.rollback();raise
