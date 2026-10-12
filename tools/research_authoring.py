"""Portable mechanical preflight for frozen kits; never certifies source quality."""
if __name__ == '__main__':
    import sys
    print('This is a library module. Run: python authoring-helper.py <packet.json>', file=sys.stderr)
    sys.exit(2)

if __package__:
    from .research_fields import changed_fields, factual_fields, group_field_checks, qualifying_field_checks, assessment_chronology_errors
else:
    from research_fields import changed_fields, factual_fields, group_field_checks, qualifying_field_checks, assessment_chronology_errors


# Kept portable for frozen kits. Parity tests bind these to the receiver/schema.
SCOPED_RESULTS = {
    'domain_checks': {'not_checked', 'blocked', 'unknown', 'changed', 'unchanged'},
    'field_checks': {'not_checked', 'blocked', 'unknown', 'value'},
    'task_decisions': {'not_checked', 'blocked', 'unknown', 'excluded', 'assessed'},
    'source_checks': {'not_checked', 'blocked', 'unknown', 'checked'},
}
MODEL_RESULTS = {**SCOPED_RESULTS, 'field_checks': SCOPED_RESULTS['field_checks'] | {'not_applicable'}}
ACCOUNTING_CHECKS = {
    'EA01': 'Put only source bodies inspected for the dated check in RUN.*.evidence_ids; expanded sources must exist and have check_date <= accessed_at <= packet_date. Keep historical citations in unchanged canonical records and the frozen baseline.',
    'EA02': 'For blocked rows save the actual attempt date, rationale, blocked_reason and remaining_gaps. Keep evidence_ids empty when no source was inspected; a failed attempt does not refresh source dates.',
    'EA03': 'Preserve all owner-qualified field rows. Each changed factual field needs one relevant investigated row that independently satisfies linked current evidence, date and primary-source requirements; scoped concrete values also require value status. Never pool row evidence or credit an unchecked owner.',
    'EA04': 'Save actual task checked_at and aggregate.assessed_at with checked_at <= assessed_at <= packet_date. Never refresh a carried-forward aggregate date to pass validation; defer incompatible proposals while preserving canonical history and actual research accounting.',
}


def accounting_evidence_errors(packet, baseline):
    """Current check citations are distinct from retained canonical history.

    Pure preflight, matching research_runs.row_errors and scoped.check_rows.
    A blocked attempt may cite freshly inspected partial evidence or no evidence;
    it cannot claim that retained source bodies were opened again.
    """
    run_key = 'scope_run' if 'scope_run' in packet else 'research_run'
    run = packet[run_key]
    state = {**baseline, **{(c['kind'], c['record']['id']): c['record'] for c in packet['changes']}}
    sources = {i: r for (k, i), r in state.items() if k == 'source'}
    observations = {i: r for (k, i), r in state.items() if k == 'observation'}
    errors = []
    for collection in MODEL_RESULTS:
        for index, row in enumerate(run[collection]):
            path = '/' + run_key + '/' + collection + '/' + str(index)
            checked = row['checked_at']
            if row['result'] == 'blocked' and not (
                    checked and run['created_at'] <= checked <= packet['created_at'][:10]
                    and row['rationale'].strip() and row['blocked_reason'] and row['remaining_gaps']):
                errors.append('EA02: ' + path + ': blocked attempt requires actual date, rationale, reason and gaps')
            for ident in row['evidence_ids']:
                expanded = observations.get(ident, {}).get('source_ids', [ident])
                if not expanded:
                    errors.append('EA01: ' + path + '/evidence_ids: observation has no inspected source: ' + ident)
                for source_id in expanded:
                    source = sources.get(source_id)
                    accessed = source.get('accessed_at') if source else None
                    if not (source and checked and run['created_at'] <= checked <= packet['created_at'][:10]
                            and isinstance(accessed, str) and checked <= accessed <= packet['created_at'][:10]):
                        errors.append('EA01: ' + path + '/evidence_ids: uninspected current-check source: ' + source_id)
    return errors


def private_paths(value, reserved, path=''):
    """Report locations, never echo private values into diagnostics."""
    if isinstance(value, dict):
        for key, nested in value.items():
            child = path + '/' + key.replace('~', '~0').replace('/', '~1')
            if any(token in key for token in reserved):
                yield path or '/'
            yield from private_paths(nested, reserved, child)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from private_paths(nested, reserved, path + '/' + str(index))
    elif isinstance(value, str) and any(token in value for token in reserved):
        yield path or '/'


def contract_errors(packet, baseline):
    """Check portable receiver invariants without repairing research outcomes."""
    scoped = 'scope_run' in packet
    run = packet['scope_run' if scoped else 'research_run']
    outcomes = SCOPED_RESULTS if scoped else MODEL_RESULTS
    state = {**baseline, **{(c['kind'], c['record']['id']): c['record'] for c in packet['changes']}}
    if scoped:
        # Resolution identities are private scratch facts, never canonical proposals.
        # Known fields may be sourced even while another identity boundary is unresolved.
        state.update({('discovery', row['candidate_id']): {'identity': row['identity']}
                      for row in packet.get('resolutions', [])
                      if row['result'] in {'resolved', 'ambiguous', 'blocked'}
                      and isinstance(row['identity'], dict)})
    errors = []
    for collection, allowed in outcomes.items():
        for index, row in enumerate(run[collection]):
            label = collection + '[' + str(index) + ']'
            if row['result'] not in allowed:
                errors.append(label + ': invalid outcome ' + str(row['result']) + '; allowed: ' + ', '.join(sorted(allowed)))
            if row['result'] in {'not_checked', 'unknown', 'blocked'} and not row['remaining_gaps']:
                errors.append(label + ': unresolved or pending result requires remaining_gaps')
            if collection == 'task_decisions' and row['result'] != 'assessed' and row['judgment_ids']:
                errors.append(label + ': non-assessed task cannot endorse judgments')
            if row['result'] == 'not_checked' and any(row.get(k) for k in
                    ('checked_at', 'rationale', 'evidence_ids', 'search_references', 'blocked_reason')):
                errors.append(label + ': unchecked row claims investigation; retain work separately or supply an evidenced outcome')
            if collection == 'field_checks' and row['result'] == 'value':
                value = state.get((row['entity_type'], row['entity_id']))
                for part in row['path'].split('/')[1:]:
                    value = value.get(part.replace('~1', '/').replace('~0', '~')) if isinstance(value, dict) else None
                if value is None or not row['evidence_ids']:
                    errors.append(label + ': absent/null fact cannot be a sourced value')
    reserved = tuple(x for x in (packet['assignment_id'], run['id'], '.local/', '.agents/', 'AGENTS.md', '.receipt.json') if x)
    for change_index, change in enumerate(packet['changes']):
        record, kind = change['record'], change['kind']
        label = kind + ' ' + record['id'] + ': '
        if kind == 'task_assessment':
            for error in assessment_chronology_errors(record, latest_date=packet['created_at'][:10]):
                errors.append('EA04: /changes/' + str(change_index) + '/record' + error['path'] + ': ' + error['message'])
            if record.get('result') != 'assessed' and record.get('judgment_ids'):
                errors.append(label + 'non-assessed task cannot endorse judgments')
            decision = next((r for r in run['task_decisions'] if
                (r['model_id'], r['task_id']) == (record.get('model_id'), record.get('task_id'))), None)
            if decision:
                for field in ('result', 'checked_at', 'judgment_ids', 'evidence_ids'):
                    if record.get(field) != decision.get(field):
                        errors.append(label + 'task decision and canonical proposal differ for /' + field)
        for path in private_paths(record, reserved):
            errors.append(label + 'private operating material at ' + path)
        if not change['checked_paths']:
            errors.append(label + 'change requires nonempty checked_paths, including metadata-only proposals')
        searched_unknown = scoped and kind in {'task_assessment', 'research_coverage'} and record.get('result') == 'unknown' and any(
            row['result'] == 'unknown' and any(s['outcome'] != 'blocked' for s in row['search_references'])
            for row in run['task_decisions'] + run['domain_checks']
            if row.get('model_id', row.get('subject_id')) == record.get('model_id') and
            (row.get('task_id') == record.get('task_id') if kind == 'task_assessment' else row.get('domain') == record.get('domain')))
        if not change['evidence_ids'] and not searched_unknown:
            errors.append(label + 'change requires evidence_ids')
    return errors


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
    errors = contract_errors(packet, baseline) + accounting_evidence_errors(packet, baseline)
    fields = group_field_checks(run['field_checks'])
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
                identity += ('product', 'billing_method', 'region', 'tier')
            for key in identity:
                if old.get(key) != record.get(key):
                    errors.append(label + 'stable identity reassigned: /' + key)
            if not set(factual_fields(old)) <= set(factual_fields(record)):
                errors.append(label + 'nested deletion is not an upsert')
        if kind in {'benchmark', 'behavior', 'release'}:
            if not expanded(change['evidence_ids']) <= expanded(evidence_ids(record)):
                errors.append(label + 'claim envelope evidence missing from permanent record citations')
        for path, value in changed_fields(old, record).items():
            if kind=='provider' and not old and path=='/model_ids':continue
            if path not in change['checked_paths']:
                errors.append(label + 'changed field missing from checked_paths: ' + path)
            positive = 'scope_run' in packet and value is not None and value not in ('unknown', 'disputed', '', [], {})
            rows = qualifying_field_checks(change, path, fields, run, state, sources, observations, packet['created_at'][:10], positive=positive)
            if not rows:
                errors.append('EA03: ' + label + 'changed field lacks linked investigation with eligible current evidence: ' + path)
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
