"""Canonical record construction from structurally accepted saved-source judgments.

The researcher owns the reasoning. This module maps identities and provenance,
preserves stable IDs, and never calls a model or claims semantic certification.
"""
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import json
from jsonschema import Draft202012Validator,FormatChecker,ValidationError
from tools.research_two_phase import encoded

def stable(prefix,*parts):return prefix+sha256('|'.join(parts).encode()).hexdigest()[:16]

def public_wording(value):
    """Translate known handoff references without changing the research judgment.

    Original observations remain in private intake; public prose describes the
    evidence limitation rather than the delivery revision or transport field.
    """
    replacements={
        'The pinned catalog retains a vendor scope-expansion warning. Its launch source has no views in revision two; it is background context, not a freshly inspected contradictory source in this result.':
            'An earlier vendor scope-expansion warning remains background; its supporting passage was unavailable for re-inspection.',
        'Empty contrary_source_ids means no directly inspectable contrary passage in the revision-two views, not consensus.':
            'No contrary passage was available for inspection in this pass; this does not establish consensus.',
        'Not_supported is unwarranted: no positive route/task mismatch is established.':
            'No positive route/task mismatch is established.',
        "the pinned catalog's maximum-effort scope warning":"the earlier maximum-effort scope warning",
        'The pinned catalog warning remains context only.':'The earlier warning remains background context.',
    }
    if isinstance(value,str):
        for before,after in replacements.items():value=value.replace(before,after)
        return value
    if isinstance(value,list):return [public_wording(item) for item in value]
    if isinstance(value,dict):return {key:public_wording(item) for key,item in value.items()}
    return value

def compile_tasks(candidate,models,assessments,sources,snapshots,*,received_at):
    model_out=deepcopy(models);task_out=deepcopy(assessments);source_out=deepcopy(sources)
    dispositions=[];changed=[]
    snapshot_by_id={s['id']:s for s in snapshots}
    for item in candidate['task_judgments']:
        before=(deepcopy(model_out),deepcopy(task_out),deepcopy(source_out));j=public_wording(item['payload'])
        try:
            model=model_out[item['model_id']]
            old=[r for r in task_out if r['model_id']==item['model_id'] and r['task_id']==j['task_id']]
            if len(old)>1:raise ValueError('ambiguous_existing_task_record')
            direct=[r for r in model['capabilities'] if r['scope']=='direct' and r['task_ids']==[j['task_id']]]
            referenced=[r for r in direct if old and r['id'] in old[0]['judgment_ids']]
            if len(referenced)>1 or not referenced and len(direct)>1:raise ValueError('ambiguous_existing_judgment_id')
            selected=(referenced or direct or [None])[0]
            evidence_map={};snapshot_map={};dates=[]
            for ident in sorted(set(j['source_ids']+j['contrary_source_ids'])):
                snapshot=snapshot_by_id[ident]
                matching=[s for s in source_out if s['url']==snapshot['requested_url']]
                if len(matching)>1:raise ValueError('ambiguous_existing_source_url')
                if matching:source=matching[0]
                else:
                    source={'id':'src-'+sha256(snapshot['requested_url'].encode()).hexdigest()[:12],
                        'url':snapshot['requested_url'],'title':None,'publisher':None,'source_type':'unknown',
                        'published_at':None,'accessed_at':datetime.fromisoformat(snapshot['retrieval_completed_at']).date().isoformat(),
                        'limitations':['Source category has not been independently classified.'],
                        'claim_scope':[j['task_id']]}
                    if any(s['id']==source['id'] for s in source_out):raise ValueError('source_id_collision')
                    source_out.append(source)
                capture={k:snapshot[k] for k in ('id','original','readable','final_url','retrieval_started_at',
                    'retrieval_completed_at','extractor_version','publication_at','effective_at')}
                # Transport IDs can identify identical content in separate retrievals.
                # Public capture IDs also bind the original clocks and derivative version.
                capture['id']='snapshot-'+sha256(encoded({'url':snapshot['requested_url'],
                    **{k:v for k,v in capture.items() if k!='id'}})).hexdigest()[:20]
                snapshot_map[ident]=capture['id']
                existing=[s for s in source.get('snapshots',[]) if s['id']==capture['id']]
                if existing and existing!=[capture]:raise ValueError('immutable_source_snapshot_conflict')
                if not existing:source.setdefault('snapshots',[]).append(capture)
                evidence_map[ident]=source['id'];dates.append(datetime.fromisoformat(capture['retrieval_completed_at']).date().isoformat())
            level=j['suitability']['level'];checked=max(dates) if dates else None
            reported=item['inspection_reported_at'];assessed=datetime.fromisoformat(reported).date().isoformat() if reported else None
            supporting=sorted({evidence_map[s] for s in j['source_ids']});contrary=sorted({evidence_map[s] for s in j['contrary_source_ids']})
            public_snapshots=sorted({snapshot_map[s] for s in item['snapshot_ids']})
            judgment_ids=[]
            if level in ('high','medium','low','disputed'):
                judgment={'id':selected['id'] if selected else stable('judgment-',item['model_id'],j['task_id']),
                    'judgment':j['conclusion'],'confidence':j['confidence']['level'],
                    'supporting_evidence_ids':supporting,'contradictory_evidence_ids':contrary,
                    'conditions':list(dict.fromkeys(j['conditions'])),'known_failure_modes':list(dict.fromkeys(j['limitations'])),
                    'evidence_notes':[j['confidence']['rationale'],j['basis']['rationale']],
                    'scope':'direct','task_ids':[j['task_id']],'related_task_ids':[],
                    'assessment':'conditional','scope_note':j['suitability']['rationale'],'observed_at':datetime.fromisoformat(received_at).date().isoformat(),
                    'effective_from':None,'provenance':{'origin':'saved-source-analysis','method':'solo_researcher','snapshot_ids':public_snapshots},
                    'basis':j['basis'],'snapshot_ids':public_snapshots,'inspection_reported_at':reported}
                if selected:model['capabilities'][model['capabilities'].index(selected)]=judgment
                else:model['capabilities'].append(judgment)
                judgment_ids=[judgment['id']]
            boundary=j['positive_boundary']
            if boundary:boundary={'description':boundary['description'],'source_ids':sorted({evidence_map[s] for s in boundary['source_ids']})}
            record={'id':old[0]['id'] if old else stable('task-assessment-',item['model_id'],j['task_id']),
                'model_id':item['model_id'],'task_id':j['task_id'],
                'applicability':'excluded' if level=='not_supported' else 'unknown' if level=='unknown' else 'applicable',
                'result':'excluded' if level=='not_supported' else 'unknown' if level=='unknown' else 'assessed',
                'checked_at':checked,'rationale':j['suitability']['rationale'],'confidence_rationale':j['confidence']['rationale'],
                'judgment_ids':judgment_ids,'evidence_ids':sorted(set(supporting+contrary)),
                'conditions':list(dict.fromkeys(j['conditions'])),'remaining_gaps':list(dict.fromkeys(j['unknowns'])),
                'aggregate':{'policy_version':'2','suitability':level,
                    'evidence_confidence':None if level in ('disputed','unknown') else j['confidence']['level'],
                    'assessed_at':assessed,'rationale':j['suitability']['rationale'],'confidence_rationale':j['confidence']['rationale'],
                    'supporting_evidence_ids':supporting,'contradictory_evidence_ids':contrary,
                    'conflict_rationale':j['suitability']['rationale'] if level=='disputed' else None,
                    'watch_outs':list(dict.fromkeys(j['limitations']+j['unknowns'])),'access_ids':[item['access_id']],
                    'basis':j['basis'],'inspection_reported_at':reported,'recorded_at':received_at,
                    'snapshot_ids':public_snapshots,'positive_boundary':boundary}}
            root=Path(__file__).resolve().parents[1]
            schema=json.loads((root/'schema/task-assessment-record.schema.json').read_bytes())
            Draft202012Validator(schema,format_checker=FormatChecker()).validate(record)
            from tools.research_fields import assessment_chronology_errors
            from tools.source_snapshots import snapshot_errors
            problems=assessment_chronology_errors(record)+snapshot_errors(source_out,[record])
            if problems:raise ValueError('canonical_chronology_or_snapshot_link_invalid')
            if old:task_out[task_out.index(old[0])]=record
            else:task_out.append(record)
            changed.append(record['id']);dispositions.append({'id':item['id'],'status':'compiled','canonical_id':record['id']})
        except (ValueError,KeyError,ValidationError) as error:
            model_out,task_out,source_out=before
            dispositions.append({'id':item['id'],'status':'deferred','reason':str(error)})
    return {'models':model_out,'assessments':task_out,'sources':source_out,
        'changed_task_ids':changed,'dispositions':dispositions,'semantic_review_performed':False}
