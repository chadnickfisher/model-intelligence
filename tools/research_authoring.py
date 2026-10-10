"""Portable mechanical preflight for frozen kits; never certifies source quality."""
if __package__:
    from .research_fields import changed_fields, factual_fields
else:
    from research_fields import changed_fields, factual_fields


def evidence_ids(value):
    ids = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {'evidence_ids', 'source_ids', 'supporting_evidence_ids', 'contradictory_evidence_ids'}:
                ids.update(nested)
            else:
                ids.update(evidence_ids(nested))
    elif isinstance(value, list):
        for nested in value:
            ids.update(evidence_ids(nested))
    return ids


def packet_errors(packet, baseline):
    """No allocation or source fetching. Report errors against supplied local IDs."""
    run = packet.get('research_run', packet.get('scope_run'))
    state = {**baseline, **{(c['kind'], c['record']['id']): c['record'] for c in packet['changes']}}
    sources = {i: r for (k, i), r in state.items() if k == 'source'}
    observations = {i: r for (k, i), r in state.items() if k == 'observation'}
    def expanded(ids):
        return {s for i in ids for s in observations.get(i, {}).get('source_ids', [i])}
    errors = []
    urls = {}
    for (kind, ident), row in baseline.items():
        if kind == 'source':
            urls.setdefault(row['url'], set()).add(ident)
    for row in run['task_decisions']:
        if row['result'] == 'excluded' and (row['judgment_ids'] or row['applicability'] != 'excluded'):
            errors.append('Excluded decision must have excluded applicability and empty judgment_ids: ' + row['task_id'])
    for change in packet['changes']:
        kind, record = change['kind'], change['record']
        ident = record['id']
        old = baseline.get((kind, ident), {})
        label = kind + ' ' + ident + ': '
        if kind == 'source':
            if ident not in change['evidence_ids']:
                errors.append(label + 'source envelope must include its own inspection ID')
            if record['url'] in urls and ident not in urls[record['url']]:
                errors.append(label + 'registered URL must reuse a frozen source ID')
            urls.setdefault(record['url'], set()).add(ident)
            inspected=any(row['result']=='checked' and ident in expanded(row['evidence_ids']) for row in run['source_checks'])
            if not inspected:
                for row in packet.get('discovery_checks',[]):
                    refs=expanded(row['evidence_ids'])
                    fresh=all(i in sources and row['checked_at'] and row['checked_at']<=sources[i]['accessed_at']<=packet['created_at'][:10] for i in refs)
                    official=any(i in sources and sources[i]['source_type']=='primary' for i in refs)
                    if row['result']=='checked' and ident in refs and row['checked_at'] and run['created_at']<=row['checked_at']<=packet['created_at'][:10] and fresh and official:
                        inspected=True
            if not inspected:errors.append(label+'source inspection needs checked category or valid dated official discovery accounting')
            if not run['created_at'] <= record['accessed_at'] <= packet['created_at'][:10]:
                errors.append(label + 'source inspection date outside this run')
            continue
        if kind == 'task_assessment':
            if record['result'] == 'excluded' and record['judgment_ids']:
                errors.append(label + 'excluded assessment must have empty judgment_ids')
            continue
        if kind == 'research_coverage':
            continue
        if old:
            if kind in {'model','provider'} and record['verified_at']!=old['verified_at']:
                errors.append(label+'whole-profile date refresh is outside field-level research')
            if kind=='model':
                if record['identity']['version']!=old['identity']['version']:
                    errors.append(label+'immutable model checkpoint reassigned')
                prior={j['id']:j for c in ('capabilities','performance_characteristics') for j in old[c]}
                current={j['id']:j for c in ('capabilities','performance_characteristics') for j in record[c]}
                if not set(prior)<=set(current):errors.append(label+'finding deletion is not an upsert')
                for finding_id,finding in prior.items():
                    if finding_id in current and any(finding[key]!=current[finding_id][key] for key in ('scope','task_ids','related_task_ids')):
                        errors.append(label+'stable finding scope reassigned: '+finding_id)
            identity = ('model_id', 'model_ids', 'provider_id', 'task_id')
            if kind in {'access', 'price'} and 'scope_run' in packet:
                identity += ('product', 'billing_method', 'region', 'service_tier')
            for key in identity:
                if old.get(key) != record.get(key):
                    errors.append(label + 'stable identity reassigned: /' + key)
            if not set(factual_fields(old)) <= set(factual_fields(record)):
                errors.append(label + 'nested deletion is not an upsert')
        if kind in {'benchmark', 'behavior', 'release'}:
            if not expanded(change['evidence_ids']) <= expanded(evidence_ids(record)):
                errors.append(label + 'claim envelope evidence missing from permanent record citations')
        for path in changed_fields(old, record):
            if kind=='provider' and not old and path=='/model_ids':continue
            if path not in change['checked_paths']:
                errors.append(label + 'changed field missing from checked_paths: ' + path)
            rows = [r for r in run['field_checks'] if (r['entity_type'], r['entity_id'], r['path']) == (kind, ident, path)]
            if not any(r['result'] not in {'blocked', 'not_checked'} and set(r['evidence_ids']) & set(change['evidence_ids']) for r in rows):
                errors.append(label + 'changed field lacks linked investigation: ' + path)
        for source in expanded(change['evidence_ids']):
            if source not in sources or not run['created_at'] <= sources[source]['accessed_at'] <= packet['created_at'][:10]:
                errors.append(label + 'uninspected claim envelope source: ' + source)
        current = evidence_ids(record) if kind in {'benchmark', 'behavior'} else set()
        if kind == 'model':
            prior = {j['id']: j for c in ('capabilities', 'performance_characteristics') for j in old.get(c, [])}
            for collection in ('capabilities', 'performance_characteristics'):
                for finding in record[collection]:
                    if prior.get(finding['id']) != finding:
                        if not run['created_at'] <= finding['observed_at'] <= packet['created_at'][:10]:
                            errors.append(label + 'changed finding needs actual current inspection date: ' + finding['id'])
                        current.update(evidence_ids(finding))
        for source in expanded(current):
            checked = max(run['created_at'], record.get('checked_at', record.get('observed_at', run['created_at'])))
            if source not in sources or not checked <= sources[source]['accessed_at'] <= packet['created_at'][:10]:
                errors.append(label + 'uninspected carry-forward conclusion source: ' + source)
    return errors
