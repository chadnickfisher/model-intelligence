"""Exact identity resolution and private discovery queue. No research or model calls."""
from copy import deepcopy
from hashlib import sha256
import argparse
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import research_batch as batch
from tools.research_runs import digest,state_hash
from tools.knowledge import record_hash

def same(a,b):
    # Case only is insignificant for names; punctuation/checkpoint IDs stay intact.
    return isinstance(a,str) and isinstance(b,str) and a.casefold()==b.casefold()

def aliases(state,mid):
    result={mid,state['model',mid]['identity']['name']}
    result.update(r['alias'] for (k,_),r in state.items() if k=='alias' and r['model_id']==mid)
    api=state['model',mid].get('additional_specifications',{}).get('api_alias',{}).get('value')
    if isinstance(api,dict):
        result.update(x for x in api.get('aliases',[]) if isinstance(x,str))
        if isinstance(api.get('current_snapshot'),str):result.add(api['current_snapshot'])
    return result

def resolve(discovery,state):
    """Only exact names/registered aliases and scoped identities; ambiguity is retained."""
    batch.public_url(discovery['url'])
    identity=discovery.get('identity')
    if not identity or identity.get('identity_mode')=='unknown':
        return {'status':'needs_identity','reason':'Exact creator/checkpoint or provider/product identity remains unresolved.'}
    batch.validate_schema(identity,'discovery-identity.schema.json')
    batch.public_url(identity['official_url'])
    batch.require(identity['entity_type']==discovery['kind'] and same(identity['name'],discovery['name']),
                  'Discovery and resolved identity differ')
    kind=discovery['kind'];matches=[]
    if kind=='model':
        batch.require(identity['creator'] and identity['creator_id'] and re.fullmatch('[a-z0-9][a-z0-9-]*',identity['creator_id']),
                      'Model creator identity required')
        batch.require(identity['identity_mode'] in {'immutable','rolling'} and
                      (identity['checkpoint'] is not None if identity['identity_mode']=='immutable' else identity['checkpoint'] is None),
                      'Immutable checkpoint or explicit rolling boundary required')
        for (k,mid),record in state.items():
            if k!='model' or not same(identity['creator'],record['identity']['creator']):continue
            if any(same(identity['name'],a) for a in aliases(state,mid)):
                if identity['checkpoint']==record['identity']['version'] or identity['identity_mode']=='rolling' and record['identity']['version'] is None:
                    matches.append(mid)
                elif identity['checkpoint'] is not None and record['identity']['version'] is None:
                    return {'status':'needs_identity','reason':'Name/alias exists but its immutable checkpoint boundary is unresolved.'}
    elif kind=='provider':
        batch.require(identity['identity_mode']=='service','Provider must be identified as a service/provider, not a model checkpoint')
        matches=[i for (k,i),r in state.items() if k=='provider' and same(identity['name'],r['name'])]
        if matches and identity['existing_id'] is None:
            observations={i:r for (k,i),r in state.items() if k=='observation'}
            anchored=[i for i in matches if any(('source',source_id) in state and
                state['source',source_id]['url']==identity['official_url'] for source_id in
                batch.expanded_sources(state['provider',i]['evidence_ids'],observations))]
            if not anchored:return {'status':'needs_identity','reason':'Provider name matches but its official identity anchor differs; resolve the exact existing ID explicitly.'}
            matches=anchored
    else:
        parent=identity['provider_id']
        if ('provider',parent) not in state:
            return {'status':'needs_parent_onboarding','reason':'Product needs an independently resolved canonical provider first.'}
        batch.require(identity['product'] and identity['identity_mode']=='service','Exact provider-qualified product required')
        matches=sorted({r['product'] for (k,_),r in state.items() if k in {'access','price'} and
                        r.get('provider_id')==parent and same(r.get('product'),identity['product'])})
    explicit=identity['existing_id']
    if explicit is not None:
        batch.require(explicit in matches,'Claimed existing identity is not an exact scoped match')
        matches=[explicit]
    if len(matches)>1:return {'status':'needs_identity','reason':'Multiple exact scoped identities match; no automatic merge.'}
    if matches:return {'status':'existing','canonical_id':matches[0],'identity':deepcopy(identity)}
    natural=([kind,identity['creator_id'],identity['name'],identity['checkpoint'],identity['identity_mode']]
             if kind=='model' else [kind,identity['provider_id'],identity['product']] if kind=='product' else
             [kind,identity['name'],identity['official_url']])
    readable=re.sub('[^a-z0-9]+','-',identity['name'].lower()).strip('-')[:70] or kind
    ident=readable+'-'+digest(natural)[:12]
    batch.require(ident not in {i for _,i in state},'New scoped identity collides with catalog ID')
    return {'status':'ready_onboarding','canonical_id':ident,'identity':deepcopy(identity)}

def enqueue(queue,discoveries,state,*,packet_sha256,baseline_commit):
    batch.require(re.fullmatch('[a-f0-9]{64}',packet_sha256) and re.fullmatch('[a-f0-9]{40}',baseline_commit),'Pinned discovery origin required')
    queue=deepcopy(queue)
    batch.require(queue.get('schema_version')=='1.0' and isinstance(queue.get('entries'),dict),'Private queue format differs')
    for discovery in discoveries:
        batch.require(discovery['evidence_ids'],'Discovery needs public source evidence')
        source_ids=batch.expanded_sources(discovery['evidence_ids'],{i:r for (k,i),r in state.items() if k=='observation'})
        batch.require(source_ids<= {i for k,i in state if k=='source'},'Discovery source is unresolved')
        if discovery.get('identity'):
            batch.require(any(state['source',i]['source_type']=='primary' and state['source',i]['url']==discovery['identity']['official_url']
                              for i in source_ids),'Resolved discovery identity needs its exact official source')
        key='discovery-'+digest([discovery['kind'],discovery['name'].casefold(),discovery['url']])[:20]
        prior=queue['entries'].get(key)
        if prior and prior['discovery'].get('identity') and not discovery.get('identity'):
            discovery={**discovery,'identity':deepcopy(prior['discovery']['identity']),
                       'evidence_ids':list(dict.fromkeys(discovery['evidence_ids']+prior['discovery']['evidence_ids']))}
        result=resolve(discovery,state)
        if prior and prior['discovery'].get('identity') and discovery.get('identity') and prior['discovery']['identity']!=discovery['identity']:
            result={'status':'needs_identity','reason':'Conflicting resolved identities for the same discovery; preserve both leads.'}
        origin={'packet_sha256':packet_sha256,'baseline_commit':baseline_commit}
        entry={'id':key,'discovery':deepcopy(discovery),'resolution':result,
               'origins':list(prior['origins']) if prior else [],'assigned':list(prior.get('assigned',[])) if prior else [],
               'identity_history':list(prior.get('identity_history',[])) if prior else []}
        if prior and prior.get('research_resolutions'):entry['research_resolutions']=deepcopy(prior['research_resolutions'])
        if prior and prior['discovery'].get('identity')!=discovery.get('identity'):
            entry['identity_history'].append(deepcopy(prior['discovery'].get('identity')))
        if origin not in entry['origins']:entry['origins'].append(origin)
        queue['entries'][key]=entry
    return queue

def ingest_resolutions(queue,packet,state,packet_sha256):
    queue=deepcopy(queue)
    for row in packet['resolutions']:
        batch.require(row['candidate_id'] in queue['entries'],'Resolution refers to unknown discovery')
        entry=queue['entries'][row['candidate_id']]
        receipt={'packet_sha256':packet_sha256,**deepcopy(row)}
        history=entry.setdefault('research_resolutions',[])
        if receipt not in history:history.append(receipt)
        if row['result']!='resolved':continue
        discovery={**entry['discovery'],'identity':row['identity'],'evidence_ids':row['evidence_ids']}
        updated=enqueue(queue,[discovery],state,packet_sha256=packet_sha256,baseline_commit=packet['baseline_commit'])
        # An explicit resolution resolves prior conflicts; origin/history remain retained.
        updated['entries'][entry['id']]['resolution']=resolve(discovery,state)
        queue=updated
    return queue

def enqueue_pending(queue,discovery,source_leads,*,packet_sha256,baseline_commit,reason):
    """Keep rejected/unpublished evidence as private leads, never resolved identity."""
    batch.public_url(discovery['url'])
    batch.require(re.fullmatch('[a-f0-9]{64}',packet_sha256) and re.fullmatch('[a-f0-9]{40}',baseline_commit),'Pinned pending discovery origin required')
    for source in source_leads:batch.public_url(source['url'])
    queue=deepcopy(queue)
    key='discovery-'+digest([discovery['kind'],discovery['name'].casefold(),discovery['url']])[:20]
    prior=queue['entries'].get(key)
    if prior and prior['resolution']['status'] in {'existing','ready_onboarding'}:return queue
    lead={k:deepcopy(v) for k,v in discovery.items() if k!='identity'}
    lead['evidence_ids']=[]
    entry=deepcopy(prior) if prior else {'id':key,'discovery':lead,'origins':[],'assigned':[],'identity_history':[]}
    entry.update(resolution={'status':'needs_identity','reason':reason},unverified_discovery=deepcopy(discovery),
                 unpublished_source_leads=deepcopy(source_leads))
    origin={'packet_sha256':packet_sha256,'baseline_commit':baseline_commit}
    if origin not in entry['origins']:entry['origins'].append(origin)
    queue['entries'][key]=entry
    return queue

def subjects(queue,state,limit=4):
    """Resolve against current baseline on every issue; assigning is never completing."""
    batch.require(type(limit) is int and limit>=0,'Nonnegative onboarding limit required')
    if limit==0:return []
    output=[];seen=set()
    provider_names={}
    for key,entry in queue['entries'].items():
        if entry['discovery']['kind']=='provider':provider_names.setdefault(entry['discovery']['name'].casefold(),set()).add(
            (entry['discovery'].get('identity') or {}).get('official_url',entry['discovery']['url']))
    for key,entry in sorted(queue['entries'].items(),key=lambda pair:(len(pair[1].get('assigned',[])),pair[0])):
        resolution=entry['resolution'] if entry['resolution']['status']=='needs_identity' and entry.get('identity_history') else resolve(entry['discovery'],state)
        if resolution['status']=='ready_onboarding' and entry['discovery']['kind']=='provider' and len(provider_names[entry['discovery']['name'].casefold()])>1:
            resolution={'status':'needs_identity','reason':'Prospective provider name has conflicting official anchors; resolve before onboarding.'}
        if resolution['status']=='existing':continue
        if resolution['status']=='ready_onboarding':
            subject={'kind':entry['discovery']['kind'],'id':resolution['canonical_id'],
                     'operation':'onboard','identity':resolution['identity']}
        else:
            subject={'kind':'discovery','id':key,'operation':'resolve','identity':None}
        if (subject['kind'],subject['id']) in seen:continue
        seen.add((subject['kind'],subject['id']));output.append(subject)
        if len(output)>=limit:break
    return output

def model_seed(subject,checked_on):
    i=subject['identity']
    fact=lambda:{'value':None,'status':'unknown','conditions':[],'evidence_ids':[]}
    return {'schema_version':'2.0','id':subject['id'],'verified_at':checked_on,
            'identity':{'name':i['name'],'creator':i['creator'],'family':'unknown','version':i['checkpoint'],
                        'release_date':None,'latest_meaningful_update':None,'status':'unknown','model_types':[]},
            'specifications':{k:fact() for k in ('architecture','parameters','context_window','maximum_output','modalities','language_support')},
            'additional_specifications':{},'licensing':{'name':None,'commercial_use':None,'redistribution':None,'fine_tuning':None,
                'hosted_service':None,'restrictions':[],'evidence_ids':[]},
            'local_inference':{'availability':'unknown','hardware_notes':[],'conditions':[],'evidence_ids':[]},
            'capabilities':[],'performance_characteristics':[],'access_ids':[],'price_ids':[],'evidence_ids':[],
            'notes':[],'limitations':[]}

def provider_seed(subject,checked_on):
    return {'schema_version':'1.0','id':subject['id'],'verified_at':checked_on,'name':subject['identity']['name'],
            'roles':['unknown'],**{k:[] for k in ('api_compatibility','access_methods','geographic_availability','rate_limits',
                 'caching_batching','privacy_data_use','reliability','model_ids','price_ids','access_ids','evidence_ids','notes','limitations')}}

if __name__=='__main__':
    from tools.git_baselines import git_state
    from tools.research_intake import private_path,retain,run_lock
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',required=True);p.add_argument('--assignment',required=True);p.add_argument('--queue',required=True)
    p.add_argument('--repo',default=str(Path(__file__).resolve().parents[1]))
    a=p.parse_args();root=Path(a.repo).resolve()
    packet,packet_hash=batch.load_json(private_path(root,a.packet))
    assignment,_=batch.load_json(private_path(root,a.assignment))
    baseline=git_state(assignment['baseline_commit'],root)
    from tools.research_scoped import compile_packet
    compiled=compile_packet(packet,assignment,baseline)
    path=private_path(root,a.queue)
    with run_lock(path.parent/'onboarding.lock'):
        queue=batch.load_json(path)[0] if path.exists() else {'schema_version':'1.0','entries':{}}
        queue=enqueue(queue,compiled['discoveries'],compiled['candidate'],packet_sha256=packet_hash,baseline_commit=assignment['baseline_commit'])
        if packet.get('resolutions'):queue=ingest_resolutions(queue,{**packet,'resolutions':compiled['resolutions']},compiled['candidate'],packet_hash)
        raw=(json.dumps(queue,indent=2,ensure_ascii=False)+'\n').encode()
        if path.exists():retain(path.parent/'queue-history',sha256(path.read_bytes()).hexdigest()+'.json',path.read_bytes())
        path.parent.mkdir(parents=True,exist_ok=True)
        temp=private_path(root,path.with_suffix('.tmp'));temp.write_bytes(raw);temp.replace(path)
    print(json.dumps({'status':'discovery_queue_updated','entries':len(queue['entries']),'model_calls':0}))
