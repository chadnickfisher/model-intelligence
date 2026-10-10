"""Synthetic scoped/onboarding fixtures; no public-source research or inference."""
from copy import deepcopy
from datetime import date,timedelta,datetime,timezone
from pathlib import Path
import json
import tempfile
import unittest

from tools import research_scoped as scoped,research_onboarding as onboard,research_audit as audit,research_build as build
from tools import research_batch as batch
from tools.git_baselines import git_state
from tools.knowledge import ROOT,record_hash,canonical
from tools.research_runs import state_hash,pending_check

COMMIT='a'*40
DAY=date.today().isoformat()

def identity(kind='model',name='Synthetic Fixture',provider=None):
    return {'entity_type':kind,'name':name,'creator':'Fixture Lab' if kind=='model' else None,
            'creator_id':'fixture-lab' if kind=='model' else None,'checkpoint':'fixture-v1' if kind=='model' else None,
            'identity_mode':'immutable' if kind=='model' else 'service','provider_id':provider,
            'product':name if kind=='product' else None,'official_url':'https://example.org/scoped-fixture','existing_id':None}

def source():
    return {'id':'src-111111111111','url':'https://example.org/scoped-fixture','title':'Synthetic test fixture',
            'publisher':'Fixture Lab','source_type':'primary','published_at':None,
            'accessed_at':(date.today()-timedelta(days=1)).isoformat(),'limitations':['Synthetic test only'],
            'claim_scope':['Synthetic contract validation only']}

def proposal(kind,record,baseline):
    old=baseline.get((kind,record['id']))
    return {'kind':kind,'record':record,'previous_hash':record_hash(old) if old else None,'identity_key':record['id'] if not old else None,
            'evidence_ids':['src-111111111111'],'checked_paths':[p for p,_ in batch.leaves(record,'') if p],
            'rationale':'Synthetic validation fixture; no claim of real research.'}

def investigated(row,value=None):
    r=deepcopy(row)
    r.update(result='unknown',checked_at=DAY,rationale='Synthetic investigated unknown for validator testing.',
             evidence_ids=['src-111111111111'],remaining_gaps=['Synthetic unknown remains unknown'],
             search_references=[{'query':'synthetic fixture query','checked_at':DAY,'outcome':'no_matched_sources','urls':[],'notes':'Synthetic fixture only'}])
    if row.get('path') in {'/identity/name','/identity/creator','/identity/version','/name','/roles'}:
        r.update(result='value',remaining_gaps=[])
    if 'category' in row and row['category']=='primary':r.update(result='checked',remaining_gaps=[])
    if 'applicability' in row:r['applicability']='unknown'
    return r

def offers(model_id,provider_id,product='Synthetic API Product'):
    common={'schema_version':'1.0','verified_at':DAY,'model_id':model_id,'provider_id':provider_id,'product':product,
            'evidence_ids':['src-111111111111'],'notes':['Synthetic fixture only'],'model_label':None,
            'reset_cadence':None,'conditions':[]}
    access={**common,'id':'new:synthetic-access','methods':['api'],'status':'unknown','price_ids':['new:synthetic-price'],
            'restrictions':[],'client_id':None,'requires_account':None,'subscription_includes_api':None}
    price={**common,'id':'new:synthetic-price','billing_method':'metered-api','status':'unknown','region':None,'tier':None,
           'effective_from':None,'effective_to':None,'rates':[],'included_usage':[],'overage':[]}
    return access,price

def extended_packet(packet,assignment,baseline):
    candidate=deepcopy(baseline)
    for c in packet['changes']:candidate[c['kind'],c['record']['id']]=c['record']
    rows=scoped.manifest(baseline,assignment['scope_run']['subjects'],DAY,candidate)
    packet['scope_run']['field_checks']=[investigated(pending_check(r)) for r in rows]
    for row in packet['scope_run']['field_checks']:
        value=candidate.get((row['entity_type'],row['entity_id']))
        for key in row['path'].split('/')[1:]:value=value.get(key.replace('~1','/').replace('~0','~')) if isinstance(value,dict) else None
        if value is not None and value not in ('unknown','disputed','',[],{}):row.update(result='value',remaining_gaps=[])
    return packet

class ScopedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public={key:r for key,(_,r) in canonical(ROOT).items()}
    def setUp(self):
        self.baseline=deepcopy(self.public);self.baseline['source','src-111111111111']=source()
    def subject(self,kind='model',name='Synthetic Fixture',parent=None):
        i=identity(kind,name,parent)
        resolved=onboard.resolve({'kind':kind,'name':name,'url':i['official_url'],'identity':i},self.baseline)
        self.assertEqual(resolved['status'],'ready_onboarding')
        return {'kind':kind,'id':resolved['canonical_id'],'operation':'onboard','identity':i}
    def assignment(self,subjects):return scoped.make_assignment(self.baseline,COMMIT,'scoped-fixture-day-'+DAY.replace('-',''),subjects,DAY,minutes=30)
    def completed(self,subject):
        a=self.assignment([subject]);p=scoped.output_template(a)
        record=onboard.model_seed(subject,DAY) if subject['kind']=='model' else onboard.provider_seed(subject,DAY)
        if subject['kind']=='provider':record['roles']=['inference-provider']
        record['evidence_ids']=['src-111111111111']
        inspected=deepcopy(source());inspected['accessed_at']=DAY
        p['changes']=[proposal('source',inspected,self.baseline),proposal(subject['kind'],record,self.baseline)]
        for name in scoped.KEYS:
            p['scope_run'][name]=[investigated(r) if r.get('subject_id')==subject['id'] or r.get('model_id')==subject['id'] else r for r in p['scope_run'][name]]
        return a,p

    def test_provider_without_model_links_has_direct_scope(self):
        provider=next(i for k,i in self.baseline if k=='provider')
        s={'kind':'provider','id':provider,'operation':'review','identity':None}
        for k,r in list(self.baseline.items()):
            if k[0] in {'access','price','behavior','benchmark','release'} and r.get('provider_id')==provider:del self.baseline[k]
        a=self.assignment([s]);p=scoped.output_template(a);c=scoped.compile_scope(p,a,self.baseline)
        self.assertEqual({r['domain'] for r in a['scope_run']['domain_checks'] if r['subject_kind']=='provider'},set(scoped.PROVIDER_FIELDS))
        self.assertEqual(c['completion']['non_target_domains_not_checked'],4*sum(k=='model' for k,i in self.baseline))
        self.assertFalse(c['completion']['complete'])
        self.assertFalse(any(r.get('model_id') for r in a['scope_run']['field_checks']))

    def test_provider_onboarding_is_complete_atomic_candidate(self):
        s=self.subject('provider','Synthetic Hosting');a,p=self.completed(s)
        c=scoped.compile_scope(p,a,self.baseline)
        self.assertTrue(c['completion']['complete'])
        self.assertIn(('provider',s['id']),c['candidate'])
        self.assertEqual(c['new_profile_paths'][s['id']],'providers/'+s['id']+'/profile.yaml')

    def test_model_onboarding_derives_exact_task_and_domain_records(self):
        s=self.subject();a,p=self.completed(s);c=scoped.compile_scope(p,a,self.baseline)
        self.assertTrue(c['completion']['complete'])
        self.assertEqual(sum(k=='task_assessment' and r['model_id']==s['id'] for (k,_),r in c['candidate'].items()),sum(t['status']=='active' for t in scoped.rubric(self.baseline)))
        self.assertEqual(sum(k=='research_coverage' and r['model_id']==s['id'] for (k,_),r in c['candidate'].items()),4)
        self.assertTrue(all(r['result']=='unknown' for (k,_),r in c['candidate'].items() if k=='task_assessment' and r['model_id']==s['id']))
        self.assertEqual(c['candidate']['model',s['id']]['specifications']['maximum_output']['value'],None)

    def test_pending_or_blocked_new_profile_cannot_leak(self):
        for result in ('not_checked','blocked'):
            with self.subTest(result=result):
                s=self.subject('provider','Synthetic Hosting');a,p=self.completed(s)
                p['scope_run']['field_checks'][0]=deepcopy(a['scope_run']['field_checks'][0])
                if result=='blocked':p['scope_run']['field_checks'][0].update(result='blocked',checked_at=DAY,rationale='Synthetic blocked retrieval',blocked_reason='Synthetic tool failure')
                with self.assertRaisesRegex(ValueError,'incomplete'):scoped.compile_scope(p,a,self.baseline)
                selected=scoped.select_scope(p,a,self.baseline)
                self.assertNotIn(('provider',s['id']),selected['compiled']['candidate'])
                self.assertEqual(selected['deferred_units'],1)

    def test_unchanged_baseline_and_assignment(self):
        s=self.subject();a,p=self.completed(s);old=deepcopy((self.baseline,a,p))
        scoped.compile_scope(p,a,self.baseline)
        self.assertEqual(old,(self.baseline,a,p))

    def test_missing_checks_and_forged_metadata_rejected(self):
        a=self.assignment([self.subject()]);p=scoped.output_template(a)
        p['scope_run']['field_checks'].pop()
        with self.assertRaisesRegex(ValueError,'checklist'):scoped.compile_scope(p,a,self.baseline)
        p=scoped.output_template(a);p['scope_run']['bounds']['max_searches_per_subject']+=1
        with self.assertRaisesRegex(ValueError,'metadata'):scoped.compile_scope(p,a,self.baseline)

    def test_new_model_identity_cannot_change_after_pinning(self):
        s=self.subject();a,p=self.completed(s)
        p['changes'][1]['record']['identity']['version']='fixture-v2'
        with self.assertRaisesRegex(ValueError,'pinned resolved identity'):scoped.compile_scope(p,a,self.baseline)

    def test_positive_identity_not_just_unknown_is_required(self):
        s=self.subject();a,p=self.completed(s)
        for row in p['scope_run']['field_checks']:
            if row['path']=='/identity/name':row['result']='unknown';row['remaining_gaps']=['No established identity']
        with self.assertRaisesRegex(ValueError,'positive inspected'):scoped.compile_scope(p,a,self.baseline)

    def test_private_packet_rejected_globally(self):
        a=self.assignment([self.subject()]);p=scoped.output_template(a)
        p['scope_run']['field_checks'][0]['remaining_gaps']=['https://localhost/private']
        with self.assertRaisesRegex(ValueError,'Private'):scoped.select_scope(p,a,self.baseline)

    def test_exact_existing_match_and_variant_separation(self):
        mid='llama-4-maverick';m=self.baseline['model',mid]
        i=identity(name=m['identity']['name']);i['creator']=m['identity']['creator'];i['creator_id']='meta';i['checkpoint']=m['identity']['version']
        d={'kind':'model','name':i['name'],'url':i['official_url'],'identity':i}
        self.assertEqual(onboard.resolve(d,self.baseline)['canonical_id'],mid)
        i['checkpoint']='different-immutable-checkpoint'
        self.assertEqual(onboard.resolve(d,self.baseline)['status'],'ready_onboarding')

    def test_discovery_dedup_and_rediscovery_preserves_resolved_identity(self):
        i=identity();d={'kind':'model','name':i['name'],'url':i['official_url'],'identity':i,'evidence_ids':['src-111111111111']}
        q={'schema_version':'1.0','entries':{}}
        q=onboard.enqueue(q,[d,d],self.baseline,packet_sha256='a'*64,baseline_commit=COMMIT)
        again=onboard.enqueue(q,[{k:v for k,v in d.items() if k!='identity'}],self.baseline,packet_sha256='a'*64,baseline_commit=COMMIT)
        self.assertEqual(len(again['entries']),1)
        self.assertEqual(len(next(iter(again['entries'].values()))['origins']),1)
        self.assertEqual(next(iter(again['entries'].values()))['resolution']['status'],'ready_onboarding')

    def test_unresolved_discovery_becomes_resolution_assignment(self):
        d={'kind':'provider','name':'Synthetic Hosting','url':source()['url'],'evidence_ids':['src-111111111111']}
        q=onboard.enqueue({'schema_version':'1.0','entries':{}},[d],self.baseline,packet_sha256='b'*64,baseline_commit=COMMIT)
        subject=onboard.subjects(q,self.baseline)[0]
        self.assertEqual(subject['kind'],'discovery');a=self.assignment([subject])
        c=scoped.compile_scope(scoped.output_template(a),a,self.baseline)
        self.assertFalse(c['completion']['complete']);self.assertEqual(c['changes'],[])

    def test_product_does_not_create_an_invented_provider(self):
        parent=next(i for k,i in self.baseline if k=='provider')
        subject=self.subject('product','Synthetic Enterprise Product',parent)
        a=self.assignment([subject]);c=scoped.compile_scope(scoped.output_template(a),a,self.baseline)
        self.assertEqual(c['new_profile_paths'],{})
        i=identity('product','Synthetic Enterprise Product','absent-provider')
        self.assertEqual(onboard.resolve({'kind':'product','name':i['name'],'url':i['official_url'],'identity':i},self.baseline)['status'],'needs_parent_onboarding')

    def test_builder_writes_only_pinned_new_profile_path(self):
        s=self.subject('provider','Synthetic Hosting');a,p=self.completed(s)
        c=scoped.compile_scope(p,a,self.baseline);report=audit.audit(p,a,self.baseline,self.baseline)
        plan=build.merge_ready(c,report,self.baseline,self.baseline)
        base=ROOT/'.local/research';base.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as tmp:
            target=Path(tmp)
            build.write_updates(target,[x for x in plan['changes'] if x['kind']=='provider'],{},plan['new_profile_paths'])
            self.assertTrue((target/a['profile_paths'][s['id']]).is_file())
            with self.assertRaisesRegex(ValueError,'pinned onboarding'):
                build.write_updates(target,[x for x in plan['changes'] if x['kind']=='provider'],{}, {s['id']:'../../outside.yaml'})

    def test_schema_extension_preserves_legacy_discovery_shape(self):
        schema=json.loads((ROOT/'schema/research-batch.schema.json').read_text())
        self.assertNotIn('identity',schema['$defs']['discovery']['required'])
        from jsonschema import Draft202012Validator
        definition={**schema['$defs']['discovery'],'$defs':schema['$defs']}
        Draft202012Validator(definition).validate({'kind':'model','name':'Synthetic','url':source()['url'],
             'evidence_ids':['src-111111111111'],'rationale':'Fixture','remaining_gaps':['Exact identity pending']})

    def test_invalid_provider_does_not_veto_an_independent_provider(self):
        ids=sorted(i for k,i in self.baseline if k=='provider')[:2]
        a=self.assignment([{'kind':'provider','id':i,'operation':'review','identity':None} for i in ids]);p=scoped.output_template(a)
        inspected=deepcopy(source());inspected['accessed_at']=DAY
        p['changes']=[proposal('source',inspected,self.baseline)]
        for n,ident in enumerate(ids):
            record=deepcopy(self.baseline['provider',ident])
            if n==0:record['roles']=['invalid-role']
            else:record['privacy_data_use'].append('Synthetic fixture policy observation')
            p['changes'].append(proposal('provider',record,self.baseline))
        for row in p['scope_run']['field_checks']:
            if row['path'] in {'/roles','/privacy_data_use'}:
                row.update(investigated(row));row['result']='value'
        for row in p['scope_run']['source_checks']:
            if row['category']=='primary':row.update(investigated(row))
        selected=scoped.select_scope(p,a,self.baseline)
        self.assertEqual(selected['deferred_units'],1)
        self.assertEqual(selected['compiled']['candidate']['provider',ids[0]],self.baseline['provider',ids[0]])
        self.assertEqual(selected['compiled']['candidate']['provider',ids[1]]['privacy_data_use'][-1],'Synthetic fixture policy observation')

    def test_current_conflict_defers_entire_new_model_accounting(self):
        s=self.subject();a,p=self.completed(s)
        current=deepcopy(self.baseline)
        current['model',s['id']]=deepcopy(p['changes'][1]['record'])
        current['model',s['id']]['identity']['name']='Conflicting fixture name'
        report=audit.audit(p,a,self.baseline,current)
        self.assertTrue(any(u['reconciliation_status']=='conflict' for u in report['units'] if u['kind']=='model'))
        self.assertTrue(all(u['reconciliation_status']=='dependency_deferred' for u in report['units'] if u['kind'] in {'task_assessment','research_coverage'}))

    def test_unassigned_record_rejected_before_partial_selection(self):
        s=self.subject('provider','Synthetic Hosting');a,p=self.completed(s)
        other=deepcopy(next(r for (k,i),r in self.baseline.items() if k=='provider'))
        other['roles']=['invalid-role'];p['changes'].append(proposal('provider',other,self.baseline))
        with self.assertRaisesRegex(ValueError,'Unassigned'):scoped.select_scope(p,a,self.baseline)

    def test_wrong_collection_outcome_is_not_completion(self):
        s=self.subject('provider','Synthetic Hosting');a,p=self.completed(s)
        p['scope_run']['source_checks'][0]['result']='value'
        with self.assertRaisesRegex(ValueError,'Invalid outcome'):scoped.compile_scope(p,a,self.baseline)

    def test_search_only_unknowns_do_not_need_manufactured_evidence(self):
        s=self.subject();a,p=self.completed(s)
        for name in ('domain_checks','task_decisions'):
            for row in p['scope_run'][name]:
                if row.get('subject_id')==s['id'] or row.get('model_id')==s['id']:row['evidence_ids']=[]
        c=scoped.compile_scope(p,a,self.baseline)
        rows=[r for (k,i),r in c['candidate'].items() if k in {'task_assessment','research_coverage'} and r['model_id']==s['id']]
        self.assertTrue(rows);self.assertTrue(all(r['evidence_ids']==[] and r['result']=='unknown' for r in rows))

    def test_invalid_new_provider_does_not_veto_independent_onboarding(self):
        left=self.subject('provider','Synthetic Left');right=self.subject('provider','Synthetic Right')
        a=self.assignment([left,right]);p=scoped.output_template(a)
        inspected=source();inspected['accessed_at']=DAY
        p['changes']=[proposal('source',inspected,self.baseline)]
        for s in (left,right):
            record=onboard.provider_seed(s,DAY);record['roles']=['inference-provider'];record['evidence_ids']=['src-111111111111']
            p['changes'].append(proposal('provider',record,self.baseline))
        for name in scoped.KEYS:
            p['scope_run'][name]=[investigated(r) if r.get('subject_kind')=='provider' else r for r in p['scope_run'][name]]
        p['changes'][1]['record']['roles']=['invalid-role']
        selected=scoped.select_scope(p,a,self.baseline)
        self.assertNotIn(('provider',left['id']),selected['compiled']['candidate'])
        self.assertIn(('provider',right['id']),selected['compiled']['candidate'])

    def test_identity_resolution_drives_later_onboarding(self):
        d={'kind':'provider','name':'Synthetic Hosting','url':source()['url'],'evidence_ids':['src-111111111111']}
        q=onboard.enqueue({'schema_version':'1.0','entries':{}},[d],self.baseline,packet_sha256='c'*64,baseline_commit=COMMIT)
        s=onboard.subjects(q,self.baseline)[0];a=self.assignment([s]);p=scoped.output_template(a)
        inspected=source();inspected['accessed_at']=DAY;p['changes']=[proposal('source',inspected,self.baseline)]
        for name in scoped.KEYS:
            p['scope_run'][name]=[investigated(r) if r.get('subject_kind')=='discovery' else r for r in p['scope_run'][name]]
        for row in p['scope_run']['field_checks']:
            if row['result']=='value' and row['path']!='/identity/name':
                row['result']='unknown';row['remaining_gaps']=['Synthetic inapplicable identity field']
        row=p['resolutions'][0];row.update(result='resolved',identity=identity('provider','Synthetic Hosting'),checked_at=DAY,
            evidence_ids=['src-111111111111'],rationale='Synthetic exact service identity investigation',remaining_gaps=[])
        c=scoped.compile_scope(p,a,self.baseline)
        q=onboard.ingest_resolutions(q,{**p,'resolutions':c['resolutions']},c['candidate'],'d'*64)
        self.assertEqual(onboard.subjects(q,c['candidate'])[0]['kind'],'provider')
        self.assertEqual(onboard.subjects(q,c['candidate'])[0]['operation'],'onboard')
        self.assertFalse(any(k=='discovery' for k,i in c['candidate']))

    def test_conflicting_new_provider_anchors_require_resolution(self):
        discoveries=[]
        for url in ('https://example.org/scoped-fixture','https://example.org/other-fixture'):
            i=identity('provider','Synthetic Hosting');i['official_url']=url
            src=source();src['id']='src-'+('1'*12 if url.endswith('scoped-fixture') else '2'*12);src['url']=url
            self.baseline['source',src['id']]=src
            discoveries.append({'kind':'provider','name':i['name'],'url':url,'identity':i,'evidence_ids':[src['id']]})
        q=onboard.enqueue({'schema_version':'1.0','entries':{}},discoveries,self.baseline,packet_sha256='e'*64,baseline_commit=COMMIT)
        self.assertTrue(all(s['operation']=='resolve' for s in onboard.subjects(q,self.baseline)))

    def test_provider_qualified_product_onboards_offers_without_new_profile(self):
        parent=next(i for k,i in self.baseline if k=='provider')
        s=self.subject('product','Synthetic Enterprise Product',parent);a=self.assignment([s]);p=scoped.output_template(a)
        inspected=source();inspected['accessed_at']=DAY
        access,price=offers(None,parent,s['identity']['product'])
        p['changes']=[proposal('source',inspected,self.baseline),proposal('access',access,self.baseline),proposal('price',price,self.baseline)]
        p=extended_packet(p,a,self.baseline)
        for name in ('domain_checks','source_checks'):
            p['scope_run'][name]=[investigated(r) if r.get('subject_id')==s['id'] else r for r in p['scope_run'][name]]
        c=scoped.compile_scope(p,a,self.baseline)
        self.assertTrue(c['completion']['complete']);self.assertEqual(c['new_profile_paths'],{})
        created=[x for x in c['changes'] if x['kind'] in {'price','access'}]
        self.assertEqual(len(created),2);self.assertTrue(all(x['record']['provider_id']==parent and x['record']['model_id'] is None for x in created))

    def test_new_model_provider_and_offers_have_resolved_relationships(self):
        m=self.subject('model','Synthetic Linked Model');s=self.subject('provider','Synthetic Linked Provider')
        a=self.assignment([m,s]);p=scoped.output_template(a)
        inspected=source();inspected['accessed_at']=DAY
        access,price=offers(m['id'],s['id'])
        model=onboard.model_seed(m,DAY);provider=onboard.provider_seed(s,DAY)
        model['access_ids']=provider['access_ids']=[access['id']];model['price_ids']=provider['price_ids']=[price['id']]
        provider['model_ids']=[m['id']];provider['roles']=['inference-provider']
        model['evidence_ids']=provider['evidence_ids']=['src-111111111111']
        p['changes']=[proposal(k,r,self.baseline) for k,r in [('source',inspected),('model',model),('provider',provider),('access',access),('price',price)]]
        p=extended_packet(p,a,self.baseline)
        for name in ('domain_checks','task_decisions','source_checks'):
            p['scope_run'][name]=[investigated(r) if r.get('subject_id') in {m['id'],s['id']} or r.get('model_id')==m['id'] else r for r in p['scope_run'][name]]
        c=scoped.compile_scope(p,a,self.baseline)
        self.assertTrue(c['completion']['complete'])
        route=c['candidate']['access',c['mapping'][access['id']]]
        self.assertEqual(route['price_ids'],[c['mapping'][price['id']]])
        self.assertEqual(c['candidate']['provider',s['id']]['model_ids'],[m['id']])

    def test_unpublished_source_leads_cannot_resolve_an_identity(self):
        i=identity('provider','Synthetic Pending Provider')
        d={'kind':'provider','name':i['name'],'url':i['official_url'],'identity':i,'evidence_ids':['src-111111111111']}
        q=onboard.enqueue_pending({'schema_version':'1.0','entries':{}},d,[source()],packet_sha256='f'*64,
                                 baseline_commit=COMMIT,reason='Source proposal was not reconciled')
        s=onboard.subjects(q,self.baseline)[0]
        self.assertEqual(s['operation'],'resolve');self.assertIsNone(s['identity'])
        self.assertEqual(next(iter(q['entries'].values()))['discovery']['evidence_ids'],[])

    def test_unknown_check_cannot_support_a_positive_policy_update(self):
        provider=next(i for k,i in self.baseline if k=='provider')
        s={'kind':'provider','id':provider,'operation':'review','identity':None};a=self.assignment([s]);p=scoped.output_template(a)
        record=deepcopy(self.baseline['provider',provider]);record['privacy_data_use'].append('Synthetic policy value')
        inspected=source();inspected['accessed_at']=DAY
        p['changes']=[proposal('source',inspected,self.baseline),proposal('provider',record,self.baseline)]
        for row in p['scope_run']['field_checks']:
            if row['path']=='/privacy_data_use':row.update(investigated(row))
        for row in p['scope_run']['source_checks']:
            if row['category']=='primary':row.update(investigated(row))
        with self.assertRaisesRegex(ValueError,'positive field'):scoped.compile_scope(p,a,self.baseline)

    def test_resolution_receipt_pending_is_still_incomplete(self):
        s={'kind':'discovery','id':'synthetic-pending-resolution','operation':'resolve','identity':None}
        a=self.assignment([s]);p=scoped.output_template(a)
        for name in scoped.KEYS:
            p['scope_run'][name]=[investigated(r) if r.get('subject_kind')=='discovery' else r for r in p['scope_run'][name]]
        for row in p['scope_run']['field_checks']:row.update(result='unknown',remaining_gaps=['Exact identity unresolved'])
        inspected=source();inspected['accessed_at']=DAY;p['changes']=[proposal('source',inspected,self.baseline)]
        c=scoped.compile_scope(p,a,self.baseline)
        self.assertFalse(c['completion']['complete']);self.assertEqual(c['completion']['pending'],1)

if __name__=='__main__':unittest.main()
