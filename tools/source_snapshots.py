"""Check source-version links and clocks without judging claim entailment."""
from datetime import datetime

def snapshot_errors(sources,assessments):
    errors=[];snapshots={}
    for source in sources:
        for snapshot in source.get('snapshots',[]):
            ident=snapshot['id']
            if ident in snapshots: errors.append('Duplicate source snapshot '+ident)
            snapshots[ident]=(source['id'],snapshot)
            try:
                start=datetime.fromisoformat(snapshot['retrieval_started_at'])
                end=datetime.fromisoformat(snapshot['retrieval_completed_at'])
                if start.tzinfo is None or end.tzinfo is None or start>end: raise ValueError()
            except (ValueError,TypeError): errors.append(ident+': invalid retrieval clocks')
    for record in assessments:
        a=record.get('aggregate',{})
        if a.get('policy_version')!='2':continue
        ids=a['snapshot_ids'];cited=set(a['supporting_evidence_ids']+a['contradictory_evidence_ids'])
        if not set(ids)<=set(snapshots):errors.append(record['id']+': unresolved snapshot');continue
        owners={snapshots[ident][0] for ident in ids}
        if not owners<=cited:errors.append(record['id']+': snapshot belongs to uncited source')
        if ids:
            try:
                clocks=[datetime.fromisoformat(snapshots[ident][1]['retrieval_completed_at']) for ident in ids]
                days=[clock.date().isoformat() for clock in clocks]
                if record['checked_at']!=max(days):errors.append(record['id']+': source check date differs from saved captures')
                recorded=datetime.fromisoformat(a['recorded_at'])
                inspected=datetime.fromisoformat(a['inspection_reported_at']) if a['inspection_reported_at'] else None
                if any(clock>recorded or inspected and clock>inspected for clock in clocks):
                    errors.append(record['id']+': saved source postdates recording or reported inspection')
            except (ValueError,TypeError):errors.append(record['id']+': invalid cited capture clock')
        boundary=a['positive_boundary']
        if boundary and not set(boundary['source_ids'])<=cited:
            errors.append(record['id']+': positive boundary evidence is uncited')
    return errors
