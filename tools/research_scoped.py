"""Pinned provider/onboarding contracts and deterministic compilation. No inference.

Existing model packets keep their original contract. Scoped packets never promote
discovery, elapsed time or structural validity into verified factual evidence.
"""
from copy import deepcopy
from datetime import date,datetime,timezone
from hashlib import sha256
import json
import re
from tools import research_batch as batch
from tools.knowledge import record_hash
from tools.research_runs import digest,state_hash,leaves,pending_check,row_errors
from tools.research_fields import changed_fields, factual_fields, field_domain, pointer
from tools.research_onboarding import model_seed,provider_seed,resolve

PROVIDER_FIELDS={
 'identity':['name','roles'],
 'access_pricing':['access_methods','api_compatibility'],
 'policies_limits':['geographic_availability','rate_limits','caching_batching','privacy_data_use','limitations','notes'],
 'reliability':['reliability'],
}
KEYS={
 'domain_checks':('subject_kind','subject_id','domain'),
 'field_checks':('subject_kind','subject_id','domain','entity_type','entity_id','path','baseline_value_hash'),
 'task_decisions':('model_id','task_id'),
 'source_checks':('subject_kind','subject_id','category'),
}
META_KEYS=('id','contract_id','contract_hash','base_commit','baseline_hash','rubric_hash','created_at','subjects','bounds')
IDENTITY_FIELDS=('entity_type','name','creator','creator_id','checkpoint','identity_mode','provider_id','product','official_url','existing_id')
RESULTS={
 'domain_checks':{'not_checked','blocked','unknown','changed','unchanged'},
 'field_checks':{'not_checked','blocked','unknown','value'},
 'task_decisions':{'not_checked','blocked','unknown','excluded','assessed'},
 'source_checks':{'not_checked','blocked','unknown','checked'},
}

def rubric(state):return sorted((r for (k,_),r in state.items() if k=='task'),key=lambda r:r['id'])
def contract_hash(state):
    return digest({'version':1,'provider_fields':PROVIDER_FIELDS,'model_contract':state['research_contract','research-contract-v1'],
                   'identity_fields':IDENTITY_FIELDS,'coverage_policy':'all-model-domains; atomic-complete-onboarding',
                   'outcomes':{k:sorted(v) for k,v in RESULTS.items()},
                   'schema_hashes':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted((batch.ROOT/'schema').glob('*.schema.json'))},
                   'receiver_hashes':{name:sha256((batch.ROOT/'tools'/name).read_bytes()).hexdigest() for name in
                       ('research_scoped.py','research_onboarding.py','research_batch.py','research_runs.py','research_fields.py','research_partial.py','research_reconcile.py')}})

def drafts(subjects,day):
    return {(s['kind'],s['id']):model_seed(s,day) if s['kind']=='model' else provider_seed(s,day)
            for s in subjects if s['operation']=='onboard' and s['kind'] in {'model','provider'}}

def owned(subject,kind,record):
    sk,ident=subject['kind'],subject['id']
    if sk=='model':return kind=='model' and record.get('id')==ident or record.get('model_id')==ident or ident in record.get('model_ids',[])
    if sk=='provider':return kind=='provider' and record.get('id')==ident or record.get('provider_id')==ident
    if sk=='product':return kind in {'access','price','behavior','release'} and record.get('provider_id')==subject['identity']['provider_id'] and record.get('product')==subject['identity']['product']
    return False

def manifest(state,subjects,day,candidate=None):
    records={**state,**drafts(subjects,day)}
    if candidate:records.update(candidate)
    output=[]
    contract=state['research_contract','research-contract-v1']
    for subject in subjects:
        owner={'subject_kind':subject['kind'],'subject_id':subject['id']}
        if subject['kind']=='discovery':
            output.extend({**owner,'domain':'identity','entity_type':'discovery','entity_id':subject['id'],
                           'path':'/identity/'+field,'baseline_value_hash':digest(None)} for field in IDENTITY_FIELDS)
            continue
        grouped={}
        for (kind,ident),record in sorted(records.items()):
            if kind not in batch.SCHEMAS or not owned(subject,kind,record):continue
            if kind=='provider':groups=PROVIDER_FIELDS
            elif kind=='model':groups=contract['field_groups']['model']
            elif kind in {'source','task_assessment','research_coverage'}:continue
            else:groups=contract['field_groups'][kind]
            grouped[kind]=True
            for domain,fields in groups.items():
                if subject['kind'] in {'provider','product'}:
                    domain='reliability' if kind in {'behavior','benchmark'} else 'access_pricing' if kind in {'access','price','release'} else domain
                for field in fields:
                    for path,value in leaves(record.get(field),'/'+field):
                        before=state.get((kind,ident),{})
                        prior=before
                        for part in path.split('/')[1:]:prior=prior.get(part.replace('~1','/').replace('~0','~')) if isinstance(prior,dict) else None
                        output.append({**owner,'domain':domain,'entity_type':kind,'entity_id':ident,'path':path,'baseline_value_hash':digest(prior)})
            if candidate:
                for path in changed_fields(state.get((kind,ident),{}),record):
                    if kind=='provider' and (kind,ident) not in state and path=='/model_ids':continue
                    domain=field_domain(kind,path,groups)
                    if subject['kind'] in {'provider','product'}:
                        domain='reliability' if kind in {'behavior','benchmark'} else 'access_pricing' if kind in {'access','price','release'} else domain
                    row={**owner,'domain':domain,'entity_type':kind,'entity_id':ident,'path':path,
                         'baseline_value_hash':digest(pointer(state.get((kind,ident),{}),path))}
                    if row not in output:output.append(row)
        for kind in ('access','price','behavior','benchmark','release'):
            if kind in grouped:continue
            domain='benchmarks' if kind=='benchmark' else 'behavior' if kind in {'behavior','release'} else 'access_pricing'
            if subject['kind'] in {'provider','product'}:domain='reliability' if kind in {'behavior','benchmark'} else 'access_pricing'
            output.append({**owner,'domain':domain,'entity_type':'inventory','entity_id':subject['id'],'path':'/'+kind,'baseline_value_hash':digest(None)})
    if candidate:
        initial=manifest(state,subjects,day)
        by_key={tuple(r[k] for k in KEYS['field_checks']):r for r in initial+output}
        return list(by_key.values())
    return output

def domain_manifest(state,subjects):
    domains=state['research_contract','research-contract-v1']['domains']
    rows={('model',i,d) for k,i in state if k=='model' for d in domains}
    for subject in subjects:
        values=domains if subject['kind']=='model' else ['identity'] if subject['kind']=='discovery' else list(PROVIDER_FIELDS)
        rows.update((subject['kind'],subject['id'],d) for d in values)
    return [{'subject_kind':k,'subject_id':i,'domain':d} for k,i,d in sorted(rows)]

def make_assignment(state,commit,ident,subjects,day,*,minutes=60,searches=40):
    batch.require(re.fullmatch('[a-f0-9]{40}',commit) and re.fullmatch('[a-z0-9][a-z0-9-]+',ident),'Pinned scope identity required')
    date.fromisoformat(day)
    batch.require(subjects and len(subjects)==len({(s['kind'],s['id']) for s in subjects}),'Unique nonempty scoped subjects required')
    batch.require(type(minutes) is int and minutes>0 and minutes*len(subjects)<=480,'Scoped research budget exceeded')
    batch.require(type(searches) is int and searches>0,'Positive query bound required')
    for subject in subjects:
        key=subject['kind'],subject['id']
        if subject['operation']=='onboard' and subject['kind'] in {'model','provider'}:
            batch.require(key not in state,'Already cataloged profile cannot be onboarded again')
            discovery={'kind':subject['kind'],'name':subject['identity']['name'],'url':subject['identity']['official_url'],'identity':subject['identity']}
            resolved=resolve(discovery,state)
            batch.require(resolved['status']=='ready_onboarding' and resolved['canonical_id']==subject['id'],'Unresolved or stale onboarding identity')
            batch.require(any(k=='source' and r['source_type']=='primary' and r['url']==subject['identity']['official_url']
                              for (k,_),r in state.items()),'Onboarding official identity source is absent from published baseline')
        elif subject['kind']=='provider':batch.require(key in state and subject['operation']=='review','Provider review target is absent')
        elif subject['kind']=='product':
            batch.require(('provider',subject['identity']['provider_id']) in state and subject['identity']['product'],'Product parent is unresolved')
            resolved=resolve({'kind':'product','name':subject['identity']['name'],'url':subject['identity']['official_url'],'identity':subject['identity']},state)
            batch.require(subject['operation']=='onboard' and resolved['status']=='ready_onboarding' and resolved['canonical_id']==subject['id'],
                          'Product has no pinned new provider-qualified identity')
            batch.require(any(k=='source' and r['source_type']=='primary' and r['url']==subject['identity']['official_url']
                              for (k,_),r in state.items()),'Product official identity source is absent from published baseline')
        else:batch.require(subject['kind']=='discovery' and subject['operation']=='resolve','Unsupported scoped operation')
    run={'schema_version':'1.0','id':'research-scope-'+ident,'contract_id':'research-scope-v1','contract_hash':contract_hash(state),
         'base_commit':commit,'baseline_hash':state_hash(state),'rubric_hash':digest(rubric(state)), 'created_at':day,
         'subjects':deepcopy(subjects),'bounds':{'max_minutes_per_subject':minutes,'max_searches_per_subject':searches,
             'source_categories':['primary','independent_evaluation','practitioner']},
         'domain_checks':[pending_check(r) for r in domain_manifest(state,subjects)],
         'field_checks':[pending_check(r) for r in manifest(state,subjects,day)],
         'task_decisions':[pending_check({'model_id':s['id'],'task_id':t['id'],'applicability':'not_checked','judgment_ids':[],
                  'confidence_rationale':''}) for s in subjects if s['kind']=='model' for t in rubric(state) if t['status']=='active'],
         'source_checks':[pending_check({'subject_kind':s['kind'],'subject_id':s['id'],'category':category}) for s in subjects
              for category in (['primary'] if s['kind']=='discovery' else ['primary','independent_evaluation','practitioner'])]}
    paths={s['id']:f"models/{s['identity']['creator_id']}/{s['id']}/profile.yaml" if s['kind']=='model' else
           f"providers/{s['id']}/profile.yaml" for s in subjects if s['operation']=='onboard' and s['kind'] in {'model','provider'}}
    return {'schema_version':'1.0','assignment_id':ident,'baseline_commit':commit,'scope_run':run,'profile_paths':paths,
            'output_filename':ident+'.r1.json','max_bytes':batch.MAX_BYTES,'day_budget_minutes':minutes*len(subjects)}

def output_template(assignment):
    return {'schema_version':'1.0','package_type':'research-scoped-batch','assignment_id':assignment['assignment_id'],
            'baseline_commit':assignment['baseline_commit'],'created_at':datetime.now(timezone.utc).isoformat(),
            'scope_run':deepcopy(assignment['scope_run']),'changes':[],'discoveries':[],'source_groups':{},
            'resolutions':[{'candidate_id':s['id'],'result':'not_checked','identity':None,'checked_at':None,'evidence_ids':[],
                'search_references':[],'rationale':'','remaining_gaps':['Pending exact public identity investigation'],'blocked_reason':None}
                for s in assignment['scope_run']['subjects'] if s['kind']=='discovery']}

def preflight(packet,assignment,baseline,private_patterns=()):
    from tools.research_partial import reject_private_urls
    batch.validate_schema(packet,'research-scoped-batch.schema.json')
    batch.require(packet['assignment_id']==assignment['assignment_id'] and packet['baseline_commit']==assignment['baseline_commit'],'Untrusted scoped assignment/baseline')
    created=datetime.fromisoformat(packet['created_at'].replace('Z','+00:00'))
    batch.require(created.tzinfo and created<=datetime.now(timezone.utc),'Invalid/future scoped packet date')
    seed,run=assignment['scope_run'],packet['scope_run']
    batch.require(all(run[k]==seed[k] for k in META_KEYS),'Scoped metadata or bounds changed')
    batch.require(seed['baseline_hash']==state_hash(baseline) and seed['rubric_hash']==digest(rubric(baseline)) and
                  seed['contract_hash']==contract_hash(baseline),'Frozen scope contract/baseline/rubric differs')
    rebuilt=make_assignment(baseline,assignment['baseline_commit'],assignment['assignment_id'],seed['subjects'],seed['created_at'],
                            minutes=seed['bounds']['max_minutes_per_subject'],searches=seed['bounds']['max_searches_per_subject'])
    batch.require(rebuilt==assignment,'Trusted scope assignment does not match deterministic reconstruction')
    text=json.dumps(packet)
    batch.require(not any(p in text for p in private_patterns) and not re.search(
        r'(?i)(?:drive\.google\.com|docs\.google\.com|[A-Z]:\\\\Users\\\\|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,})',text),'Private content in scoped packet')
    reject_private_urls(packet)
    for name,keys in KEYS.items():
        rows=[tuple(r[k] for k in keys) for r in run[name]]
        expected={tuple(r[k] for k in keys) for r in seed[name]}
        batch.require(len(rows)==len(set(rows)) and expected<=set(rows),'Scoped checklist omitted, duplicated or altered')
        if name!='field_checks':batch.require(set(rows)==expected,'Scoped checklist identity extended outside assignment')
    seen=set()
    for change in packet['changes']:
        key=change['kind'],change['record']['id']
        batch.require(change['kind']=='source' or any(owned(s,change['kind'],change['record']) for s in seed['subjects']),
                      'Unassigned scoped record')
        batch.require(key not in seen,'Duplicate scoped proposal');seen.add(key)
        batch.require(change['previous_hash']==(record_hash(baseline[key]) if key in baseline else None),'Prior-record hash mismatch')
        public=json.dumps(change['record'])
        batch.require(not any(p in public for p in (assignment['assignment_id'],seed['id'],'.local/','.agents/','AGENTS.md','.receipt.json')),'Private operating material in public record')
    expected={s['id'] for s in seed['subjects'] if s['kind']=='discovery'}
    batch.require({r['candidate_id'] for r in packet['resolutions']}==expected and len(packet['resolutions'])==len(expected),'Resolution accounting omitted/duplicated')
    return created

def check_rows(run,seed,baseline,candidate,created):
    sources={i:r for (k,i),r in candidate.items() if k=='source'}
    observations={i:r for (k,i),r in candidate.items() if k=='observation'}
    targets={(s['kind'],s['id']) for s in seed['subjects']}
    expected=manifest(baseline,seed['subjects'],seed['created_at'],candidate)
    identities=lambda rows:{tuple(r[k] for k in KEYS['field_checks']) for r in rows}
    batch.require(identities(run['field_checks'])==identities(expected),'Scoped extended field accounting differs from returned records')
    for collection in KEYS:
        for row in run[collection]:
            result=row['result']
            batch.require(result in RESULTS[collection],'Invalid outcome for scoped '+collection)
            if collection=='domain_checks' and (row['subject_kind'],row['subject_id']) not in targets:
                batch.require(result=='not_checked','Non-target model domain must stay unchecked')
            if result=='not_checked':
                batch.require(not row['checked_at'] and not row['rationale'] and not row['evidence_ids'] and
                              not row['search_references'] and not row['blocked_reason'] and row['remaining_gaps'],'Unchecked row claims investigation')
                if collection=='task_decisions':batch.require(row['applicability']=='not_checked' and not row['judgment_ids'] and not row['confidence_rationale'],'Unchecked task claims judgment')
                continue
            batch.require(row['checked_at'] and seed['created_at']<=row['checked_at']<=created.date().isoformat() and row['rationale'].strip(),'Actual scoped investigation date/reason required')
            batch.require((result=='blocked')==bool(row['blocked_reason']),'Blocked outcome differs')
            if result in {'unknown','blocked'}:batch.require(row['remaining_gaps'],'Unresolved row needs gaps')
            if result!='blocked':
                batch.require(row['evidence_ids'] or any(s['outcome']!='blocked' for s in row['search_references']),'Failed/unattempted work cannot become investigated unknown')
            for ident in batch.expanded_sources(row['evidence_ids'],observations):
                batch.require(ident in sources and row['checked_at']<=sources[ident]['accessed_at']<=created.date().isoformat(),'Scoped row cites uninspected evidence')
            for search in row['search_references']:
                batch.require(search['checked_at']==row['checked_at'],'Search/check dates differ')
                for url in search['urls']:batch.public_url(url)
            if result in {'excluded','not_applicable'}:batch.require(row['evidence_ids'],'Exclusions need positive evidence')
            if collection=='source_checks' and result=='checked':
                batch.require(any(sources[i]['source_type']==row['category'].replace('_','-') for i in batch.expanded_sources(row['evidence_ids'],observations)),'Checked source category lacks matching original source')
            if collection=='field_checks' and result=='value':
                actual=candidate.get((row['entity_type'],row['entity_id']))
                for part in row['path'].split('/')[1:]:actual=actual.get(part.replace('~1','/').replace('~0','~')) if isinstance(actual,dict) else None
                batch.require(actual is not None and row['evidence_ids'],'Absent/null fact cannot be a sourced value')
            if collection=='task_decisions':
                adapted={**seed,'target_model_ids':[s['id'] for s in seed['subjects'] if s['kind']=='model']}
                batch.require(not row_errors('task_decisions',row,adapted,candidate),'Invalid scoped task decision')
    for subject in seed['subjects']:
        queries={(s['checked_at'],s['query']) for name in KEYS for r in run[name]
                 if (r.get('subject_kind'),r.get('subject_id'))==(subject['kind'],subject['id']) or r.get('model_id')==subject['id']
                 for s in r['search_references']}
        batch.require(len(queries)<=seed['bounds']['max_searches_per_subject'],'Scoped query bound exceeded')

def completion(run,resolutions=()):
    targets={(s['kind'],s['id']) for s in run['subjects']}
    rows=[r for name in KEYS for r in run[name] if (r.get('subject_kind'),r.get('subject_id')) in targets or ('model',r.get('model_id')) in targets]+list(resolutions)
    pending=sum(r['result']=='not_checked' for r in rows);blocked=sum(r['result']=='blocked' for r in rows)
    return {'complete':pending==blocked==0,'batch_complete':pending==blocked==0,'pending':pending,'blocked':blocked,
            'investigated_unknown':sum(r['result'] in {'unknown','ambiguous'} for r in rows),
            'non_target_domains_not_checked':sum((r['subject_kind'],r['subject_id']) not in targets for r in run['domain_checks'])}

def allowed(change,baseline,seed,mapping):
    kind,record=change['kind'],change['record'];key=kind,record['id'];old=baseline.get(key)
    batch.require(old!=record,'No-op stays a check')
    scopes=[s for s in seed['subjects'] if owned(s,kind,record)]
    batch.require(kind=='source' or scopes,'Unassigned scoped record')
    onboard=next((s for s in scopes if s['kind']==kind and s['operation']=='onboard'),None)
    batch.require(old is not None or record['id'] in mapping.values() or onboard is not None or
                  kind=='research_coverage' and any(s['id']==record['model_id'] and s['kind']=='model' and s['operation']=='onboard' for s in scopes),
                  'New record has no pinned identity')
    if old:
        batch.require(set(old)<=set(record),'Record field deletion is not an upsert')
        if kind in {'model','provider'}:batch.require(record['verified_at']==old['verified_at'],'Whole-profile date refresh is outside field checks')
        for field in ('model_id','model_ids','provider_id','task_id'):
            if kind not in {'model','provider','source'}:batch.require(old.get(field)==record.get(field),'Stable route/task identity reassigned')
        if kind in {'access','price'}:
            for field in ('product','billing_method','region','tier'):
                batch.require(old.get(field)==record.get(field),'Stable product/offer identity reassigned; add a dated offer instead')
        if kind=='model':batch.require(old['identity']['version']==record['identity']['version'],'Immutable checkpoint replaced')
    if onboard:
        batch.require(record['verified_at']>=seed['created_at'] and record['verified_at']<=date.today().isoformat(),'New profile needs actual completed research date')
        if kind=='model':
            i=onboard['identity'];batch.require(record['identity']['name']==i['name'] and record['identity']['creator']==i['creator'] and
                  record['identity']['version']==i['checkpoint'],'New model differs from pinned resolved identity')
        else:
            batch.require(record['name']==onboard['identity']['name'],'New provider differs from pinned identity')
            batch.require(record['roles'] and set(record['roles'])!={'unknown'},'New provider roles remain unresolved')
    if kind in {'access','price'}:
        valid_models={i for k,i in baseline if k=='model'}|{s['id'] for s in seed['subjects'] if s['kind']=='model'}
        valid_providers={i for k,i in baseline if k=='provider'}|{s['id'] for s in seed['subjects'] if s['kind']=='provider'}
        batch.require(record['model_id'] is None or record['model_id'] in valid_models,'Unknown route model; discovery needs separate scope')
        batch.require(record['provider_id'] in valid_providers,'Unknown route provider; discovery needs separate scope')
    batch.validate_schema(record,batch.SCHEMAS[kind]+'.schema.json')
    searched_unknown=kind in {'task_assessment','research_coverage'} and record['result']=='unknown' and any(
        r['result']=='unknown' and any(s['outcome']!='blocked' for s in r['search_references'])
        for r in seed.get('task_decisions',[])+seed.get('domain_checks',[]) if
        r.get('model_id',r.get('subject_id'))==record['model_id'] and
        (r.get('task_id')==record.get('task_id') if kind=='task_assessment' else r.get('domain')==record['domain']))
    batch.require((change['evidence_ids'] or searched_unknown) and change['checked_paths'],'Scoped proposal lacks evidence/checked paths')
    if kind=='source':batch.public_url(record['url'])

def validate_change(change,baseline,seed,run,candidate,mapping,created,groups):
    allowed(change,baseline,{**seed,'task_decisions':run['task_decisions'],'domain_checks':run['domain_checks']},mapping)
    sources={i:r for (k,i),r in candidate.items() if k=='source'};observations={i:r for (k,i),r in candidate.items() if k=='observation'}
    support_baseline=baseline
    if change['kind']=='model' and ('model',change['record']['id']) not in baseline:
        support_baseline={**baseline,('model',change['record']['id']):{'capabilities':[],'performance_characteristics':[]}}
    batch.validate_support(change,support_baseline,sources,observations,seed,created)
    record=change['record'];kind=change['kind'];old=baseline.get((kind,record['id']),{})
    if kind=='source':
        batch.require(any(record['id'] in r['evidence_ids'] and r['result']=='checked' for r in run['source_checks']),'Source inspection missing from scoped categories')
        return
    if kind=='access' and not old:
        for ident in record['price_ids']:
            batch.require(candidate['price',ident]['product']==record['product'],'New access price belongs to another product')
    if kind=='task_assessment':
        row=next(r for r in run['task_decisions'] if r['model_id']==record['model_id'] and r['task_id']==record['task_id'])
        batch.require(all(record[k]==row[k] for k in ('result','checked_at','judgment_ids','evidence_ids')),'Scoped canonical task decision differs')
        batch.validate_confidence(change,sources,observations,groups);return
    if kind=='research_coverage':
        row=next(r for r in run['domain_checks'] if r['subject_kind']=='model' and r['subject_id']==record['model_id'] and r['domain']==record['domain'])
        batch.require(record['checked_at']==row['checked_at'] and record['result']==row['result'],'Model coverage differs from actual domain investigation');return
    before=factual_fields(old);actual=factual_fields(record)
    if kind=='provider' and not old:
        related={r.get('model_id') for (k,_),r in candidate.items() if k in {'access','price'} and r.get('provider_id')==record['id']} - {None}
        batch.require(set(record['model_ids'])==related,'New provider model links differ from canonical routes')
        actual.pop('/model_ids',None)
        for field,linked_kind in [('access_ids','access'),('price_ids','price')]:
            batch.require(set(record[field])=={i for (k,i),r in candidate.items() if k==linked_kind and r.get('provider_id')==record['id']},
                          'New provider offer links differ from canonical routes')
    batch.require(not old or {p for p in before if p and p.split('/')[1] not in batch.META}<=set(actual),'Nested deletion is not an upsert')
    # Required null placeholders assert no factual value. Non-null new fields
    # still need their actual contract check, just as existing model batches do.
    altered=set(changed_fields(old,record)) & set(actual)
    batch.require(altered<=set(change['checked_paths']),'Scoped changed field omitted from checked_paths')
    for path in altered:
        checks=[r for r in run['field_checks'] if (r['entity_type'],r['entity_id'],r['path'])==(kind,record['id'],path)]
        checks=[r for r in checks if r['result'] not in {'not_checked','blocked'} and set(r['evidence_ids'])&set(change['evidence_ids'])]
        batch.require(checks,'Changed scoped field lacks actual linked investigation: '+path)
        if actual[path] is not None and actual[path] not in ('unknown','disputed','',[],{}):
            batch.require(any(r['result']=='value' for r in checks),'Changed factual value must have positive field accounting: '+path)
        primary=kind in {'access','price'} or kind=='model' and path.split('/')[1] in {'identity','specifications','additional_specifications','licensing','local_inference'} or kind=='provider' and path.split('/')[1] not in {'reliability','limitations','notes'}
        if primary:batch.require(any(sources[i]['source_type']=='primary' for r in checks for i in batch.expanded_sources(r['evidence_ids'],observations)),'Scoped specifications/policies/prices need primary evidence')

def validate_resolutions(packet,seed,candidate,created):
    sources={i:r for (k,i),r in candidate.items() if k=='source'};observations={i:r for (k,i),r in candidate.items() if k=='observation'}
    for row in packet['resolutions']:
        if row['result']=='not_checked':
            batch.require(row['identity'] is None and row['checked_at'] is None and not row['evidence_ids'] and not row['rationale'] and
                          not row['search_references'] and not row['blocked_reason'] and row['remaining_gaps'],'Unattempted identity resolution asserts facts');continue
        batch.require(row['checked_at'] and seed['created_at']<=row['checked_at']<=created.date().isoformat() and row['rationale'],'Resolution needs actual date/rationale')
        batch.require((row['result']=='blocked')==bool(row['blocked_reason']),'Resolution blocker differs')
        for search in row['search_references']:
            batch.require(search['checked_at']==row['checked_at'],'Resolution search/check dates differ')
            for url in search['urls']:batch.public_url(url)
        support=batch.expanded_sources(row['evidence_ids'],observations)
        batch.require(all(i in sources and row['checked_at']<=sources[i]['accessed_at']<=created.date().isoformat() for i in support),
                      'Resolution cites uninspected evidence')
        if row['result']!='blocked':batch.require(support or any(s['outcome']!='blocked' for s in row['search_references']),
            'Identity resolution requires actual investigation')
        if row['result']!='resolved':batch.require(row['remaining_gaps'],'Unresolved identity needs gaps');continue
        batch.require(row['identity'] is not None,'Resolved identity missing')
        identity=row['identity']
        resolved=resolve({'kind':identity['entity_type'],'name':identity['name'],'url':identity['official_url'],'identity':identity},candidate)
        batch.require(resolved['status'] in {'existing','ready_onboarding'},'Resolved identity still has ambiguous boundaries')
        batch.require(any(i in sources and sources[i]['source_type']=='primary' and sources[i]['url']==row['identity']['official_url'] and
            row['checked_at']<=sources[i]['accessed_at']<=created.date().isoformat() for i in support),'Resolved identity needs current exact official evidence')
        candidate['discovery',row['candidate_id']]={'identity':row['identity']}
        for field in IDENTITY_FIELDS:
            checks=[r for r in packet['scope_run']['field_checks'] if r['entity_type']=='discovery' and r['entity_id']==row['candidate_id'] and r['path']=='/identity/'+field]
            batch.require(checks and checks[0]['result'] not in {'not_checked','blocked'} and set(checks[0]['evidence_ids'])&set(row['evidence_ids']),'Resolved identity field lacks inspected accounting')

def onboarding_closed(run):
    for s in run['subjects']:
        if s['operation']!='onboard':continue
        rows=[r for name in KEYS for r in run[name] if (r.get('subject_kind'),r.get('subject_id'))==(s['kind'],s['id']) or r.get('model_id')==s['id']]
        batch.require(rows and all(r['result'] not in {'not_checked','blocked'} for r in rows),'New profile/product onboarding is incomplete; retain it as follow-up work')
        identity=[r for r in run['field_checks'] if r['entity_type']==s['kind'] and r['entity_id']==s['id'] and r['path'] in
                  ({'/identity/name','/identity/creator','/identity/version'} if s['kind']=='model' else {'/name','/roles'})]
        required={'/identity/name','/identity/creator'} if s['kind']=='model' else {'/name','/roles'}
        if s['kind']=='model' and s['identity']['identity_mode']=='immutable':required.add('/identity/version')
        positive={r['path'] for r in identity if r['result']=='value' and r['evidence_ids']}
        batch.require(s['kind']=='product' or required<=positive,'Onboarding identity lacks positive inspected evidence')

def derived_model_records(changes,run,baseline):
    """Render researcher decisions, never infer suitability or fresh check dates."""
    changes=deepcopy(changes);present={(c['kind'],c['record']['id']) for c in changes}
    for s in run['subjects']:
        if s['kind']!='model' or s['operation']!='onboard':continue
        if not any(c['kind']=='model' and c['record']['id']==s['id'] for c in changes):continue
        for row in run['task_decisions']:
            if row['model_id']!=s['id'] or row['result'] in {'not_checked','blocked'}:continue
            ident='task-assessment-'+sha256((s['id']+'|'+row['task_id']).encode()).hexdigest()[:16]
            key='task_assessment',ident
            if key in present:continue
            record={k:deepcopy(row[k]) for k in ('model_id','task_id','applicability','result','checked_at','rationale','confidence_rationale','judgment_ids','evidence_ids','conditions','remaining_gaps')}
            record['id']=ident
            changes.append({'kind':'task_assessment','record':record,'previous_hash':None,'identity_key':s['id']+'|'+row['task_id'],
                            'evidence_ids':row['evidence_ids'],'checked_paths':['/'+k for k in record if k!='id'],'rationale':row['rationale']})
        for row in run['domain_checks']:
            if row['subject_kind']!='model' or row['subject_id']!=s['id'] or row['result'] in {'not_checked','blocked'}:continue
            ident='research-coverage-'+s['id']+'-'+row['domain'].replace('_','-');key='research_coverage',ident
            if key in present:continue
            batch.require(row['result'] in {'changed','unchanged','unknown'},'New model domain needs canonical investigated outcome')
            record={'schema_version':'1.0','id':ident,'model_id':s['id'],'domain':row['domain'],'research_batch_id':'public-source-onboarding',
                    **{k:deepcopy(row[k]) for k in ('result','checked_at','evidence_ids','remaining_gaps','blocked_reason')},
                    'scope_notes':[row['rationale']], 'search_references':[{**r,'outcome':'sources_found' if r['outcome']=='sources_located' else r['outcome'],'notes':[r['notes']]} for r in row['search_references']]}
            changes.append({'kind':'research_coverage','record':record,'previous_hash':None,'identity_key':s['id']+'|'+row['domain'],
                            'evidence_ids':row['evidence_ids'],'checked_paths':['/'+k for k in record if k!='id'],'rationale':row['rationale']})
    return changes

def compile_scope(packet,assignment,baseline,private_patterns=()):
    from tools.research_reconcile import reconcile_sources,remap_refs
    from tools.research_partial import public_refs_valid
    created=preflight(packet,assignment,baseline,private_patterns)
    normalized,reconciliation=reconcile_sources(packet,baseline)
    mapping=batch.allocate(normalized['changes'],baseline)
    normalized=remap_refs(normalized,mapping)
    normalized['source_groups']={mapping.get(k,k):v for k,v in normalized['source_groups'].items()}
    run=normalized['scope_run'];seed=assignment['scope_run']
    changes=derived_model_records(normalized['changes'],run,baseline)
    candidate=deepcopy(baseline)
    for c in changes:candidate[c['kind'],c['record']['id']]=deepcopy(c['record'])
    validate_resolutions(normalized,seed,candidate,created)
    check_rows(run,seed,baseline,candidate,created)
    active=[s for s in seed['subjects'] if s['operation']=='onboard' and any(owned(s,c['kind'],c['record']) for c in changes)]
    if active:onboarding_closed({**run,'subjects':active})
    # Derived task/coverage records have fixed natural IDs under the pinned scope.
    mapping={**mapping,**{c['record']['id']:c['record']['id'] for c in changes if c not in normalized['changes']}}
    for change in changes:
        validate_change(change,baseline,seed,run,candidate,mapping,created,normalized['source_groups'])
        public_refs_valid(change,candidate)
    batch.require(set(normalized['source_groups'])<={i for k,i in candidate if k=='source'},'Unknown source independence group')
    for discovery in normalized['discoveries']:
        batch.public_url(discovery['url'])
        batch.require(discovery['evidence_ids'] and batch.evidence_ids(discovery)<={i for k,i in candidate if k in {'source','observation'}},'Discovery has unresolved evidence')
    # Resolution scratch values are private, never canonical candidate records.
    candidate={key:r for key,r in candidate.items() if key[0]!='discovery'}
    return {'changes':changes,'candidate':candidate,'mapping':mapping,'research_run':run,'completion':completion(run,normalized['resolutions']),
            'discoveries':normalized['discoveries'],'resolutions':normalized['resolutions'],'new_profile_paths':assignment['profile_paths'],
            'source_reconciliation':reconciliation}

def compile_packet(packet,assignment,baseline,private_patterns=()):
    return compile_scope(packet,assignment,baseline,private_patterns) if packet.get('package_type')=='research-scoped-batch' else batch.compile_batch(packet,assignment,baseline,private_patterns)

def select_scope(packet,assignment,baseline,private_patterns=()):
    """Select valid subject groups; atomic onboarding never leaks partial profiles."""
    from tools.research_partial import units_for
    preflight(packet,assignment,baseline,private_patterns)
    try:
        compiled=compile_scope(packet,assignment,baseline,private_patterns)
        selected=deepcopy(packet);deferred=[]
    except (ValueError,KeyError,TypeError,StopIteration) as failure:
        # Connected new identities are indivisible. Other providers remain independent.
        from tools.research_partial import refs
        subjects=assignment['scope_run']['subjects']
        groups=[{(s['kind'],s['id'])} for s in subjects]
        for change in packet['changes']:
            related={(s['kind'],s['id']) for s in subjects if owned(s,change['kind'],change['record']) or s['id'] in refs(change['record'])}
            touching=[g for g in groups if g&related]
            if touching:
                combined=set().union(*touching)
                groups=[g for g in groups if g not in touching]+[combined]
        accepted=[];valid_groups=[];deferred=[]
        def projection(active,changes):
            derived=output_template(assignment)
            derived['created_at']=packet['created_at'];derived['changes']=deepcopy(changes)
            for name in KEYS:
                rows=[r for r in packet['scope_run'][name] if (r.get('subject_kind'),r.get('subject_id')) in active or ('model',r.get('model_id')) in active]
                keyed={tuple(r[k] for k in KEYS[name]):r for r in rows}
                initial=derived['scope_run'][name]
                kept=[deepcopy(keyed.get(tuple(r[k] for k in KEYS[name]),r)) for r in initial]
                basekeys={tuple(r[k] for k in KEYS[name]) for r in initial}
                kept.extend(deepcopy(r) for r in rows if tuple(r[k] for k in KEYS[name]) not in basekeys)
                derived['scope_run'][name]=kept
            derived['resolutions']=[deepcopy(next(r for r in packet['resolutions'] if r['candidate_id']==row['candidate_id']))
                                    if ('discovery',row['candidate_id']) in active else row for row in derived['resolutions']]
            evidence={i for c in changes for i in batch.evidence_ids(c['record'])|set(c['evidence_ids'])}
            derived['source_groups']={i:g for i,g in packet['source_groups'].items() if i in evidence}
            return derived
        for group in sorted(groups,key=lambda g:sorted(g)):
            subjects_in=[s for s in subjects if (s['kind'],s['id']) in group]
            changes=[c for c in packet['changes'] if c['kind']!='source' and any(owned(s,c['kind'],c['record']) for s in subjects_in)]
            wanted={i for c in changes for i in batch.evidence_ids(c['record'])|set(c['evidence_ids'])}
            wanted|={i for name in KEYS for r in packet['scope_run'][name] if (r.get('subject_kind'),r.get('subject_id')) in group or ('model',r.get('model_id')) in group for i in r['evidence_ids']}
            wanted|={i for r in packet['resolutions'] if ('discovery',r['candidate_id']) in group for i in r['evidence_ids']}
            changes+=[c for c in packet['changes'] if c['kind']=='source' and c['record']['id'] in wanted]
            attempt=projection(group,changes)
            try:compile_scope(attempt,assignment,baseline,private_patterns)
            except (ValueError,KeyError,TypeError,StopIteration) as exc:
                deferred.append({'subjects':[list(s) for s in sorted(group)],'reason':str(exc)})
            else:accepted.extend(changes);valid_groups.extend(group)
        dedup={}
        for change in accepted:
            key=change['kind'],change['record']['id']
            batch.require(key not in dedup or dedup[key]==change,'Accepted groups disagree on a shared record')
            dedup[key]=change
        selected=projection(set(valid_groups),list(dedup.values()))
        # Discoveries are retained only when their evidence survives acceptance.
        evidence={i for k,i in baseline if k in {'source','observation'}}|{c['record']['id'] for c in accepted if c['kind']=='source'}
        selected['discoveries']=[deepcopy(d) for d in packet['discoveries'] if set(d['evidence_ids'])<=evidence]
        compiled=compile_scope(selected,assignment,baseline,private_patterns)
    units=units_for(compiled['changes'],baseline)
    from tools.research_partial import refs
    definitions={u['finding_id'] or u['record_id']:u['id'] for u in units if u['finding_id'] or not u['path']}
    onboard_ids={s['id'] for s in assignment['scope_run']['subjects'] if s['operation']=='onboard'}
    for unit in units:
        deps=refs(unit['value'],unit['path'].lstrip('/'))|set(unit['change']['evidence_ids'])
        unit['dependencies']=sorted({definitions[i] for i in deps if i in definitions and definitions[i]!=unit['id']})
        # A new profile and its full task/domain accounting share one dependency group.
        atomic=unit['record_id'] in onboard_ids or isinstance(unit['value'],dict) and unit['value'].get('model_id') in onboard_ids
        if atomic:
            owner=unit['record_id'] if unit['record_id'] in onboard_ids else unit['value']['model_id']
            unit['dependencies']=sorted(set(unit['dependencies'])|{u['id'] for u in units if u['id']!=unit['id'] and
                 (u['record_id']==owner or isinstance(u['value'],dict) and u['value'].get('model_id')==owner)})
        unit['scopes']=[]
    report=[{k:deepcopy(v) for k,v in u.items() if k not in {'value','change'}} for u in units]
    original=completion(packet['scope_run'],packet['resolutions'])
    return {'compiled':compiled,'selected_packet':selected,'units':report,'reconciliation':compiled['source_reconciliation'],
            'accounting_projection':deferred,'original_accounting_counts':{k:original[k] for k in ('pending','blocked')},
            'candidate_units':len(units),'deferred_units':len(deferred)}
