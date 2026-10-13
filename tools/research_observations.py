"""Deterministic observation compiler. No inference, writes or semantic review."""
from copy import deepcopy
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json, re
from jsonschema import Draft202012Validator, FormatChecker
from tools import research_two_phase as p
from tools.research_context import recheck

FIELDS = {'pricing.input': 'input', 'pricing.output': 'output',
    'pricing.cache_read': 'cached_input', 'pricing.cache_write_5m': 'cache_write_5m',
    'pricing.cache_write_1h': 'cache_write_1h'}

def privacy(value):
    raw = json.dumps(value, ensure_ascii=False, allow_nan=False)
    # Known private path/credential forms only, not a claimed comprehensive semantic detector.
    if re.search(r'(?i)(?:[a-z]:\\\\users\\\\|\.local[/\\\\]|bearer\s+(?:(?=[^\s"\']*[0-9])[a-z0-9._-]{12,}|[a-z0-9._-]{32,})|-----BEGIN .*PRIVATE KEY|sk-[a-z0-9]{20,})', raw):
        raise ValueError('Private content or credential marker in candidate input')

def item_schema(value, name):
    schema = p.JUDGMENT if name == 'judgment' else p.FINDING
    Draft202012Validator({'$defs': p.DEFINITIONS, **schema},
        format_checker=FormatChecker()).validate(value)

def compile_candidate(assignment, bundle, frame, *, challenge, selectors, merge_root,
        merge_commit, rubric_sha256, prices, dependencies=None, frame_raw=None):
    if frame_raw is not None:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result: raise ValueError('Duplicate delivery JSON key')
                result[key] = value
            return result
        if json.loads(frame_raw, object_pairs_hook=unique) != frame:
            raise ValueError('Original delivery bytes differ from parsed frame')
    privacy(frame); privacy(bundle)
    p.validate(assignment, 'assignment'); p.validate(bundle, 'bundle')
    if (bundle['assignment_id'], bundle['revision'], bundle['subject'], bundle['questions']) != (
            assignment['assignment_id'], assignment['revision'], assignment['subject'], assignment['questions']):
        raise ValueError('Bundle assignment differs')
    if not re.fullmatch('[a-f0-9]{40}', merge_commit): raise ValueError('Invalid merge baseline')
    if assignment['schema_sha256'] != p.pin(p.encoded(p.SCHEMA))['sha256'] or assignment['policy_version'] != p.POLICY:
        raise ValueError('Unsupported pinned schema or policy')
    if assignment['scope_sha256'] != p.pin(p.encoded(p.scope(assignment)))['sha256']:
        raise ValueError('Scope pin mismatch')
    # Global envelope and budget validation, with per-observation structure isolated below.
    payload = frame['payload']; stripped = deepcopy(frame)
    stripped['payload']['findings'] = []; stripped['payload']['judgments'] = []
    p.validate(stripped, 'response_frame')
    if (frame['assignment_id'], frame['revision'], frame['phase'], frame['assignment_sha256'],
        frame['parent_sha256'], frame['response_challenge']) != (assignment['assignment_id'],
        assignment['revision'], 'analysis', p.pin(p.encoded(assignment))['sha256'],
        p.pin(p.encoded(bundle))['sha256'], challenge):
        raise ValueError('Untrusted analysis phase binding')
    if not isinstance(payload['findings'], list) or not isinstance(payload['judgments'], list):
        raise ValueError('Observation arrays required')
    if len(payload['findings']) + len(payload['judgments']) > assignment['bounds']['max_findings']:
        raise ValueError('Observation budget exceeded')
    known = {s['id']: s for s in bundle['sources']}
    unknown_inspected_ids=sorted(set(payload['inspected_source_ids'])-set(known))
    changed = recheck(assignment, selectors, merge_root)
    if rubric_sha256 != assignment['rubric_sha256']:
        for q in assignment['questions']:
            if q['kind'] == 'task_insight': changed.setdefault(q['id'], []).append('task_rubric')
    questions = {q['id']: q for q in assignment['questions']}
    dependencies = dependencies or {}
    if not set(dependencies) <= set(questions) or any(not set(v) <= set(questions) for v in dependencies.values()):
        raise ValueError('Unassigned dependency')
    dispositions = []; proposals = []; assertions = []; judgments = []
    invalid_questions = set(changed)
    fact_ids = Counter(f.get('id') for f in bundle['facts'])
    subject = assignment['subject']
    for fact in bundle['facts']:
        reason = None; question = questions.get(fact.get('question_id'))
        try:
            p.validate(fact, 'fact')
            if fact_ids[fact['id']] != 1: raise ValueError('duplicate_fact_identity')
            if question is None or question['kind'] != 'factual' or fact['field_id'] not in question['field_ids']:
                raise ValueError('unassigned_field')
            if fact['adapter_id'] != 'claude-api-pricing' or fact['adapter_version'] != '1' or fact['field_id'] not in FIELDS:
                raise ValueError('unsupported_adapter_or_field')
            source = known.get(fact['snapshot_id'])
            if source is None or source['original']['sha256'] != fact['snapshot_sha256']:
                raise ValueError('fact_snapshot_mismatch')
            if fact['status'] != 'extracted': raise ValueError('unresolved_fact')
            if fact['question_id'] in changed: raise ValueError('stale_supplied_context')
            if fact['currency'] != 'USD' or fact['unit'] != 'per 1 million tokens' or fact['value'] < 0:
                raise ValueError('unsupported_currency_unit_or_amount')
            expected = {'billing_method=metered-api', 'routing=global', 'tier=standard'}
            if fact['field_id'] == 'pricing.cache_read': expected.add('cache_hit_required=true')
            if fact['field_id'] == 'pricing.cache_write_5m': expected.add('cache_write_duration_seconds=300')
            if fact['field_id'] == 'pricing.cache_write_1h': expected.add('cache_write_duration_seconds=3600')
            if set(fact['conditions']) != expected or subject['model_id'] != 'claude-sonnet-5-5' or \
                    subject['provider_id'] != 'anthropic' or subject['tier'] != 'Standard' or subject['routing'] != 'global':
                raise ValueError('offer_conditions_require_adapter')
            matching = [r for r in prices if (r['model_id'], r['provider_id'], r['tier'], r['billing_method'],
                r['region'], r['product'], r['status']) == (subject['model_id'], subject['provider_id'],
                subject['tier'], 'metered-api', None, None, 'current')]
            if len(matching) != 1: raise ValueError('ambiguous_or_missing_offer')
            offer = matching[0]; metric = FIELDS[fact['field_id']]
            rates = [r for r in offer['rates'] if r['metric'] == metric]
            if len(rates) != 1: raise ValueError('ambiguous_or_missing_metric')
            if (rates[0]['amount'], rates[0]['currency'], rates[0]['unit']) == (fact['value'], fact['currency'], fact['unit']):
                status = 'unchanged'
            else:
                # New dated offers need lifecycle grouping; never retire a row on an unknown effective date.
                status = 'deferred'; reason = 'changed_rate_needs_versioned_offer_compiler'
            dispositions.append({'id': fact['id'], 'question_id': fact['question_id'], 'origin': 'machine_extraction',
                'status': status, 'reason': reason, 'original_verified_at': offer['verified_at']})
        except Exception as error:
            if question is not None and fact.get('field_id') in question['field_ids']:
                invalid_questions.add(fact['question_id'])
            dispositions.append({'id': fact.get('id', 'invalid-fact'), 'question_id': fact.get('question_id'),
                'origin': 'machine_extraction', 'status': 'deferred', 'reason': str(error)})
    task_counts = Counter((j.get('question_id'), j.get('task_id')) for j in payload['judgments'] if isinstance(j, dict))
    for kind in ('findings', 'judgments'):
        for ordinal, item in enumerate(payload[kind]):
            ident = kind + '-' + str(ordinal); qid = item.get('question_id') if isinstance(item, dict) else None
            try:
                if not isinstance(item, dict): raise ValueError('malformed_observation')
                if kind == 'judgments':
                    item_schema(item, 'judgment')
                else: item_schema(item, 'finding')
                trial = deepcopy(payload); trial['findings'] = [item] if kind == 'findings' else []
                trial['judgments'] = [item] if kind == 'judgments' else []
                trial['inspected_source_ids']=[s for s in payload['inspected_source_ids'] if s in known]
                p.validate_payload(trial, assignment, bundle)
                if any(not known[s]['views'] for s in item['source_ids'] + item['contrary_source_ids']):
                    raise ValueError('cited_source_has_no_supplied_readable_view')
                if qid in changed: raise ValueError('stale_supplied_context')
                if kind == 'findings':
                    assertions.append({'id': ident, 'origin': 'model_assertion', 'payload': deepcopy(item)})
                else:
                    if task_counts[(qid, item['task_id'])] != 1: raise ValueError('duplicate_task_conclusion')
                    level = item['suitability']['level']
                    if level not in ('unknown',) and not item['source_ids']: raise ValueError('missing_supporting_evidence')
                    if level == 'disputed' and not item['contrary_source_ids']: raise ValueError('missing_disputed_evidence')
                    stable = 'task-assessment-' + sha256((subject['model_id'] + '|' + item['task_id']).encode()).hexdigest()[:16]
                    judgments.append({'id': stable, 'question_id': qid, 'model_id': subject['model_id'],
                        'access_id': subject['access_id'], 'origin': 'model_judgment',
                        'policy_version': assignment['policy_version'], 'payload': deepcopy(item),
                        'snapshot_ids': sorted(set(item['source_ids'] + item['contrary_source_ids'])),
                        'inspection_reported_at': payload['inspection_reported_at'],
                        'canonical_apply_gate': 'requires_canonical_validation_and_published_policy_v2'})
                dispositions.append({'id': ident, 'question_id': qid, 'origin': 'model_assertion' if kind == 'findings' else 'model_judgment',
                    'status': 'compiled_private', 'reason': None})
            except Exception as error:
                invalid_questions.add(qid)
                dispositions.append({'id': ident, 'question_id': qid, 'origin': 'model_assertion' if kind == 'findings' else 'model_judgment',
                    'status': 'deferred', 'reason': str(error)})
    # Fixed point handles transitive dependencies independent of input ordering, including cycles.
    while True:
        extra = {q for q, parents in dependencies.items() if set(parents) & invalid_questions} - invalid_questions
        if not extra: break
        invalid_questions |= extra
    for row in dispositions:
        if row['question_id'] in invalid_questions and row['status'] in ('compiled_private', 'unchanged'):
            row.update(status='deferred', reason='question_dependency_or_invalid_premise')
    eligible = {r['id'] for r in dispositions if r['status'] == 'compiled_private'}
    assertions = [r for r in assertions if r['id'] in eligible]
    judgments = [r for r in judgments if r['question_id'] not in invalid_questions]
    successful_facts = {r['id'] for r in dispositions if r['origin'] == 'machine_extraction' and r['status'] == 'unchanged'}
    question_results = []
    for qid, question in sorted(questions.items()):
        remaining_fields = sorted(set(question['field_ids']) - {f['field_id'] for f in bundle['facts']
            if f['question_id'] == qid and f['id'] in successful_facts})
        remaining_tasks = sorted(set(question['task_ids']) - {j['payload']['task_id'] for j in judgments
            if j['question_id'] == qid})
        processed = any(r['question_id'] == qid and r['status'] in ('unchanged', 'compiled_private') for r in dispositions)
        # Finding prose never certifies missing machine fields; task unknowns remain investigated unknowns.
        status = 'deferred' if qid in invalid_questions else 'partial' if processed and (remaining_fields or remaining_tasks) \
            else 'processed' if processed else payload['status'] if payload['status'] in ('unknown', 'blocked') else 'missing'
        question_results.append({'id':qid, 'result':status, 'remaining_field_ids':remaining_fields,
            'remaining_task_ids':remaining_tasks, 'domain_completion':'not_certified'})
    result = {'version': 'observation-compiler-preview/1', 'assignment': p.pin(p.encoded(assignment)),
        'bundle': p.pin(p.encoded(bundle)), 'analysis': p.pin(frame_raw if frame_raw is not None else p.encoded(frame)),
        'analysis_representation': 'original_delivery_bytes' if frame_raw is not None else 'canonical_json',
        'original_research_baseline': assignment['baseline_commit'], 'merge_baseline': merge_commit,
        'changed_context': changed, 'dispositions': dispositions, 'parsed_facts': deepcopy(bundle['facts']),
        'model_assertions': assertions, 'task_judgments': judgments, 'canonical_proposals': proposals,
        'question_results': question_results,
        'unresolved_inspection_report_ids': unknown_inspected_ids,
        'public_data_applied': False, 'semantic_review_performed': False,
        'producer_attestation_proven': False, 'compiler_uses_inference': False,
        'full_process_inference_instrumentation': 'pending'}
    privacy(result)
    return result
