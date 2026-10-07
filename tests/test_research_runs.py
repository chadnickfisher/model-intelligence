"""Completion is derived from actual accounting, never from catalog inventory."""
from copy import deepcopy
from datetime import date
import json

from jsonschema import Draft202012Validator, FormatChecker
import pytest

from tools.knowledge import ROOT, read
from tools.research_runs import (baseline_state, completion, digest, make_run,
                                 required_fields, run_errors)

TODAY = date.today().isoformat()


def fixture():
    contract = deepcopy(read(ROOT / 'data/research-contract.yaml')['records'][0])
    contract['field_groups'] = {'model': {'capabilities': ['identity', 'specifications']},
                               'access': {'access_pricing': ['availability', 'billing_class']}}
    task = deepcopy(read(ROOT / 'data/capability-taxonomy.yaml')['capabilities'][0])
    task['neighboring_task_ids'] = []  # This fixture deliberately has a one-task registry.
    state = {
        ('research_contract', contract['id']): contract,
        ('model', 'text-model'): {'id': 'text-model', 'identity': {'name': 'Text Model'},
                                 'specifications': {'context': None}, 'capabilities': [
                                     {'id': 'direct', 'task_ids': [task['id']], 'related_task_ids': []},
                                     {'id': 'compound', 'task_ids': [], 'related_task_ids': [task['id']]}]},
        ('model', 'other-model'): {'id': 'other-model'},
        ('task', task['id']): task,
        ('source', 'source1'): {'id': 'source1', 'accessed_at': TODAY, 'source_type': 'primary'},
    }
    run = make_run(state, 'revision-' + 'a' * 20, 'b' * 40, 'research-run-test',
                   ['text-model'], {'max_minutes_per_model': 30, 'max_searches_per_model': 10,
                                    'source_categories': contract['source_categories']}, TODAY)
    return state, run


def investigate(row, result='unknown', source=False):
    row.update(result=result, checked_at=TODAY, rationale='Public search inspected; setup remains uncertain.',
               evidence_ids=['source1'] if source else [],
               search_references=[] if source else [
                   {'query': 'exact checkpoint task evidence', 'checked_at': TODAY,
                    'outcome': 'no_matched_sources', 'urls': [], 'notes': 'No matched public evidence'}],
               remaining_gaps=['No measured task setup established'] if result == 'unknown' else [])
    return row


def unknown_completed():
    state, run = fixture()
    for group in ['domain_checks', 'field_checks', 'task_decisions', 'source_checks']:
        for row in run[group]:
            if row['model_id'] == 'text-model':
                investigate(row)
                if group == 'task_decisions':
                    row['applicability'] = 'unknown'
    return state, run


def test_scaffold_does_not_promote_nulls_old_judgments_or_non_targets():
    state, run = fixture()
    assert not run_errors(run, state)
    assert not completion(run)['complete']
    assert completion(run)['non_target_domains_not_checked'] == 4
    assert all(row['result'] == 'not_checked' for row in run['field_checks'])
    assert next(row for row in run['field_checks'] if row['path'] == '/specifications/context')['baseline_value_hash'] == digest(None)
    assert run['task_decisions'][0]['judgment_ids'] == []


def test_investigated_unknowns_complete_but_pending_and_blocked_do_not():
    state, run = unknown_completed()
    assert not run_errors(run, state)
    assert completion(run)['complete'] and completion(run)['investigated_unknown']
    blocked = investigate(run['field_checks'][0], 'blocked')
    blocked.update(blocked_reason='Public source returned HTTP 403', remaining_gaps=['Cannot inspect'])
    assert not run_errors(run, state)
    assert not completion(run)['complete'] and completion(run)['blocked'] == 1


@pytest.mark.parametrize('group', ['field_checks', 'task_decisions', 'source_checks', 'domain_checks'])
def test_omissions_and_duplicate_checklist_entries_fail(group):
    state, run = fixture()
    run[group].pop()
    assert any('omitted' in error for error in run_errors(run, state))
    state, run = fixture()
    run[group].append(deepcopy(run[group][0]))
    assert any('duplicated' in error for error in run_errors(run, state))


def test_hashes_prevent_silent_baseline_and_rubric_change():
    state, run = fixture()
    state[('task', run['task_decisions'][0]['task_id'])]['scope'] = 'Different definition'
    errors = run_errors(run, state)
    assert any('baseline hash' in error for error in errors)
    assert any('rubric hash' in error for error in errors)


def test_source_absence_never_becomes_exclusion_or_known_null_value():
    state, run = fixture()
    row = investigate(run['task_decisions'][0], 'excluded')
    row['applicability'] = 'excluded'
    assert any('positive mismatch evidence' in error for error in run_errors(run, state))
    row['evidence_ids'] = ['source1']
    assert not run_errors(run, state)
    field = next(row for row in run['field_checks'] if row['path'] == '/specifications/context')
    investigate(field, 'value', source=True)
    assert any('absent/null' in error for error in run_errors(run, state))


def test_failed_searches_and_stale_or_editorial_evidence_cannot_claim_investigation():
    state, run = fixture()
    row = investigate(run['field_checks'][0])
    row['search_references'][0]['outcome'] = 'blocked'
    assert any('failed searches' in error for error in run_errors(run, state))
    investigate(row, source=True)
    state[('source', 'source1')]['accessed_at'] = '2000-01-01'
    assert any('predates' in error for error in run_errors(run, state, state))
    state[('source', 'source1')]['accessed_at'] = '2099-01-01'
    assert any('source inspection' in error for error in run_errors(run, state, state))
    state[('observation', 'editorial')] = {'source_ids': []}
    row['evidence_ids'] = ['editorial']
    assert any('editorial' in error for error in run_errors(run, state, state))


def test_assessment_needs_direct_exact_model_judgment_and_confidence_reason():
    state, run = fixture()
    row = investigate(run['task_decisions'][0], 'assessed', source=True)
    row.update(applicability='applicable', judgment_ids=['compound'], confidence_rationale='Setup is sparse.')
    assert any('direct exact-model' in error for error in run_errors(run, state))
    row['judgment_ids'] = ['direct']
    assert not run_errors(run, state)
    row['confidence_rationale'] = ''
    assert any('confidence rationale' in error for error in run_errors(run, state))


def test_new_records_extend_required_work_without_changing_base_hash():
    state, run = fixture()
    candidate = deepcopy(state)
    candidate[('access', 'route1')] = {'model_id': 'text-model', 'provider_id': None,
                                     'availability': None, 'billing_class': None}
    assert any('omitted' in error for error in run_errors(run, state, candidate))
    from tools.research_runs import pending_check
    contract = state[('research_contract', run['contract_id'])]
    keys = {(row['entity_type'], row['entity_id'], row['path']) for row in run['field_checks']}
    run['field_checks'] += [pending_check(row) for row in required_fields(state, ['text-model'], contract, candidate)
                            if (row['entity_type'], row['entity_id'], row['path']) not in keys]
    assert not run_errors(run, state, candidate)
    assert all(row['baseline_value_hash'] == digest(None) for row in run['field_checks'] if row['entity_id'] == 'route1')


def test_exact_revision_boundary_handles_same_day_updates_and_deletions():
    revisions = [{'id': 'first', 'entity_type': 'model', 'entity_id': 'm', 'value': {'version': 1}},
                 {'id': 'second', 'entity_type': 'model', 'entity_id': 'm', 'value': {'version': 2}},
                 {'id': 'third', 'entity_type': 'model', 'entity_id': 'm', 'value': None}]
    assert baseline_state(revisions, 'first')[('model', 'm')]['version'] == 1
    assert baseline_state(revisions, 'second')[('model', 'm')]['version'] == 2
    assert baseline_state(revisions, 'third') == {}
    with pytest.raises(ValueError, match='Unknown baseline'):
        baseline_state(revisions, 'missing')


def test_schema_rejects_claimed_complete_flag_and_requires_explicit_bounds():
    _, run = fixture()
    schema = json.loads((ROOT / 'schema/research-run-record.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(run)
    run['complete'] = True
    assert list(validator.iter_errors(run))
    del run['complete']
    run['bounds']['max_searches_per_model'] = 0
    assert list(validator.iter_errors(run))


def test_source_category_check_cannot_substitute_vendor_claims_for_independent_evaluation():
    state, run = fixture()
    row = next(row for row in run['source_checks'] if row['category'] == 'independent_evaluation')
    investigate(row, 'checked', source=True)
    assert any('source of that category' in error for error in run_errors(run, state))


def test_search_budget_counts_distinct_searches_not_reused_references():
    state, run = unknown_completed()
    run['bounds']['max_searches_per_model'] = 1
    assert not run_errors(run, state)
    run['source_checks'][0]['search_references'][0]['query'] = 'additional distinct query'
    assert any('budget exceeded' in error for error in run_errors(run, state))
