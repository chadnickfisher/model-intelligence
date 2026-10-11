"""Scoped partial selection with inspected shared-source dependencies.

This audit-layer selector uses the frozen scoped compiler unchanged. Keeping the
projection here preserves previously issued receiver/assignment hash boundaries.
"""
from copy import deepcopy
from tools import research_batch as batch
from tools.research_scoped import preflight, compile_scope, output_template, owned, KEYS, completion


def retain_source_checks(derived,packet,baseline):
    """Keep original source inspection dependencies, not another subject's fields.

    Category rows are atomic research statements. Preserve their dates, scope and
    evidence, including proposed sources they cite. The full receiver still
    validates every retained row and record; missing inspections fail closed.
    """
    sources={c['record']['id']:c for c in packet['changes'] if c['kind']=='source'}
    original=sorted((r for r in packet['scope_run']['source_checks'] if r['result']=='checked'),
                    key=lambda r:tuple(r[k] for k in KEYS['source_checks']))
    rows=derived['scope_run']['source_checks']
    indexes={tuple(r[k] for k in KEYS['source_checks']):i for i,r in enumerate(rows)}
    changes={(c['kind'],c['record']['id']):c for c in derived['changes']}
    observations={i:r for (k,i),r in baseline.items() if k=='observation'}
    observations.update({i:c['record'] for (k,i),c in changes.items() if k=='observation'})
    while True:
        inspected={i for r in rows if r['result']=='checked' for i in r['evidence_ids']}
        missing={i for k,i in changes if k=='source'}-inspected
        donor=next((r for r in original if set(r['evidence_ids']) & missing),None)
        if donor is None:break
        rows[indexes[tuple(donor[k] for k in KEYS['source_checks'])]]=deepcopy(donor)
        for ident in sorted(batch.expanded_sources(donor['evidence_ids'],observations)):
            if ident in sources:changes.setdefault(('source',ident),deepcopy(sources[ident]))
    derived['changes']=list(changes.values())


def select_scope(packet,assignment,baseline,private_patterns=()):
    """Select valid subject groups; atomic onboarding never leaks partial profiles."""
    from tools.research_partial import units_for
    preflight(packet,assignment,baseline,private_patterns)
    try:
        compiled=compile_scope(packet,assignment,baseline,private_patterns)
        selected=deepcopy(packet);deferred=[];valid_groups=[(s['kind'],s['id']) for s in assignment['scope_run']['subjects']]
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
            retain_source_checks(derived,packet,baseline)
            evidence={i for c in derived['changes'] for i in batch.evidence_ids(c['record'])|set(c['evidence_ids'])}
            evidence|={i for name in KEYS for r in derived['scope_run'][name] for i in r['evidence_ids']}
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
            else:accepted.extend(attempt['changes']);valid_groups.extend(group)
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
    source_dependencies=[deepcopy(r) for r in selected['scope_run']['source_checks'] if r['result']=='checked' and
                         (r['subject_kind'],r['subject_id']) not in set(valid_groups)]
    return {'compiled':compiled,'selected_packet':selected,'units':report,'reconciliation':compiled['source_reconciliation'],
            'accounting_projection':deferred,'original_accounting_counts':{k:original[k] for k in ('pending','blocked')},
            'source_check_dependencies':source_dependencies,
            'candidate_units':len(units),'deferred_units':len(deferred)}
