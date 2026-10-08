"""Validate and select explicit task suitability records; no inferred model ratings."""

DEFAULT_SUITABILITY = ('high', 'medium', 'low', 'disputed')
SELECTABLE_SUITABILITY = (*DEFAULT_SUITABILITY, 'not_supported')
EVIDENCE_CONFIDENCE = ('high', 'medium', 'low')


def select_task_assessments(records, task_id, *, suitability=None, confidence=()):
    """Shared task-query semantics; selected Disputed records survive confidence filters."""
    selected = set(DEFAULT_SUITABILITY if suitability is None else suitability)
    confidence = set(confidence)
    if not selected <= set(SELECTABLE_SUITABILITY):
        raise ValueError('Task results support High, Medium, Low, Disputed and Not supported only')
    if not confidence <= set(EVIDENCE_CONFIDENCE):
        raise ValueError('Unknown evidence-confidence selection')
    result = []
    for record in records:
        if record['task_id'] != task_id:
            continue
        aggregate = record.get('aggregate')
        if not aggregate or aggregate['suitability'] not in selected:
            continue
        if (confidence and aggregate['suitability'] != 'disputed'
                and aggregate['evidence_confidence'] not in confidence):
            continue
        result.append(record)
    return result


def task_assessment_errors(records, models, tasks, access):
    """Check identity/scope consistency, not source quality or research adequacy."""
    errors = []
    seen = set()
    for record in records:
        label = record['id']
        key = (record['model_id'], record['task_id'])
        if key in seen:
            errors.append(label + ': duplicate model/task assessment')
        seen.add(key)
        model = models.get(record['model_id'])
        if model is None or record['task_id'] not in tasks:
            errors.append(label + ': unresolved model/task')
        exact = {j['id']: j for j in (model or {}).get('capabilities', [])}
        for ident in record['judgment_ids']:
            judgment = exact.get(ident)
            if (not judgment or judgment.get('scope') != 'direct'
                    or judgment.get('task_ids') != [record['task_id']]
                    or judgment.get('related_task_ids')):
                errors.append(label + ': assessment requires an exact direct task judgment: ' + ident)
        if record['result'] == 'assessed' and (
                not record['judgment_ids'] or not record['confidence_rationale'].strip()):
            errors.append(label + ': assessed task needs judgment and confidence rationale')
        if record['result'] == 'excluded' and not record['evidence_ids']:
            errors.append(label + ': excluded task needs positive mismatch evidence')
        aggregate = record.get('aggregate')
        if not isinstance(aggregate, dict):
            continue
        assessed_at = aggregate.get('assessed_at')
        if isinstance(assessed_at, str) and assessed_at < record['checked_at']:
            errors.append(label + ': aggregate assessment predates its source check')
        cited = set(aggregate.get('supporting_evidence_ids', [])) | set(
            aggregate.get('contradictory_evidence_ids', []))
        if not cited <= set(record['evidence_ids']):
            errors.append(label + ': aggregate sources must belong to the assessment evidence')
        for ident in aggregate.get('access_ids', []):
            route = access.get(ident)
            if not route or route['model_id'] != record['model_id']:
                errors.append(label + ': aggregate access route must belong to exact model: ' + ident)
    return errors
