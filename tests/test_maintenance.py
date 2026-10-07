"""Maintenance completion never substitutes for a full model assessment."""
from copy import deepcopy
from datetime import date
import json

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from tools.knowledge import ROOT, read
from tools.maintenance import (account_domains, completion, field_freshness, field_ref,
                               make_pass, pass_errors, validated_report)
from tools.research_runs import digest

TODAY = date.today().isoformat()


def fixture(shared=False):
    state = {
        ('maintenance_contract', 'maintenance-contract-v1'): deepcopy(read(ROOT / 'data/maintenance-contract.yaml')['records'][0]),
        ('model', 'model-a'): {'id': 'model-a', 'identity': {'name': 'Model A'}, 'verified_at': '2020-01-01'},
        ('model', 'model-b'): {'id': 'model-b', 'identity': {'name': 'Model B'}, 'verified_at': '2020-01-01'},
        ('provider', 'vendor'): {'id': 'vendor', 'privacy_data_use': ['No training']},
        ('access', 'route-a'): {'id': 'route-a', 'model_id': 'model-a', 'provider_id': 'vendor', 'product': 'Product A'},
        ('access', 'route-b'): {'id': 'route-b', 'model_id': 'model-b', 'provider_id': 'vendor', 'product': 'Product B'},
        ('source', 'src-test'): {'id': 'src-test', 'url': 'https://example.org/documentation',
                                 'accessed_at': TODAY, 'source_type': 'primary'},
    }
    revisions = [{'id': 'revision-' + f'{i:020x}', 'entity_type': key[0], 'entity_id': key[1],
                  'value': deepcopy(value)} for i, (key, value) in enumerate(sorted(state.items()), 1)]
    targets = ['model-a', 'model-b'] if shared else ['model-a']
    scope = [{'model_id': m, 'domain': 'access_pricing' if shared else 'capabilities',
              'entity_type': 'provider' if shared else 'model', 'entity_id': 'vendor' if shared else m,
              'path': '/privacy_data_use' if shared else '/identity',
              'product': 'Product A' if m == 'model-a' and shared else 'Product B' if shared else None,
              'task_ids': []} for m in targets]
    watchlist = [{'id': 'watch-documentation', 'source_id': 'src-test', 'scope': scope}]
    run = make_pass(state, revisions, 'b' * 40, 'maintenance-pass-test', targets, watchlist,
                    {'max_research_minutes': 25, 'max_searches': 5}, TODAY, 'test')
    return state, revisions, run


def inspect(run, result='no_material_change'):
    w = run['watch_checks'][0]
    text = 'Inspected the exact documented subject; no material difference located in this scope.'
    w.update(result=result, checked_at=TODAY, observation=text, observation_hash=digest(text), remaining_gaps=[])
    return w


def candidate(state, run, kind='model', ident='model-a', path='/identity/name', result='verified', disposition='no_material_change'):
    f = {**field_ref(state, kind, ident, path), 'result': result, 'checked_at': TODAY,
         'check_ids': ['watch-documentation'], 'rationale': 'Actual source inspection supports this exact field.',
         'observed_value_hash': digest(state[(kind, ident)]['identity']['name']) if kind == 'model' else digest(state[(kind, ident)]['privacy_data_use']),
         'remaining_gaps': []}
    c = {'id': 'candidate-test', 'model_ids': ['model-a'], 'source_check_ids': ['watch-documentation'],
         'search_ids': [], 'summary': 'Inspected this scoped field', 'disposition': disposition,
         'rationale': 'Compare exact product and recorded field.', 'next_action': 'Retain existing factual dates.',
         'affected_fields': [f], 'dependencies': [{'model_id': 'model-a', 'result': 'confirmed',
             'checked_at': TODAY, 'check_ids': ['watch-documentation'], 'rationale': 'Exact model scope inspected.'}]}
    run['candidates'].append(c)
    return c


def test_schema_and_scaffold_preserve_pending_work_old_dates_and_all_domains():
    state, revisions, run = fixture()
    errors, report = validated_report(run, state, state, revisions)
    assert not errors
    assert not report['watch_complete'] and not report['reconciliation_complete']
    assert len(run['domain_accounting']) == 8
    assert all(r['result'] == 'not_checked' for r in run['domain_accounting'])
    assert state[('model', 'model-a')]['verified_at'] == '2020-01-01'
    assert field_freshness(run, 'model', 'model-a', '/identity/name', state) is None


def test_unchanged_watch_does_not_refresh_any_field_but_completes_declared_monitoring():
    state, revisions, run = fixture()
    inspect(run)
    account_domains(run, state)
    assert not pass_errors(run, state, state, revisions)
    assert completion(run)['watch_complete'] and completion(run)['reconciliation_complete']
    assert field_freshness(run, 'model', 'model-a', '/identity/name', state) is None
    assert sum(r['result'] == 'not_checked' for r in run['domain_accounting']) == 7


def test_completed_watch_with_pending_candidate_cannot_claim_reconciliation():
    state, revisions, run = fixture()
    inspect(run)
    c = candidate(state, run, disposition='pending')
    c['affected_fields'][0].update(result='not_checked', checked_at=None, check_ids=[], observed_value_hash=None)
    c['dependencies'][0].update(result='not_checked', checked_at=None, check_ids=[])
    account_domains(run, state)
    assert not pass_errors(run, state, state, revisions)
    assert completion(run)['watch_complete']
    assert not completion(run)['reconciliation_complete']
    c['disposition'] = 'duplicate'
    assert any('hides pending' in e for e in pass_errors(run, state, state, revisions))


@pytest.mark.parametrize('mutation', ['omitted-watch', 'scope-change', 'omitted-domain', 'stale-carry', 'false-revision'])
def test_pinned_scope_accounting_and_carry_forward_cannot_be_silently_changed(mutation):
    state, revisions, run = fixture()
    if mutation == 'omitted-watch': run['watch_checks'].clear()
    if mutation == 'scope-change': run['watch_checks'][0]['scope'][0]['path'] = '/other'
    if mutation == 'omitted-domain': run['domain_accounting'].pop()
    if mutation == 'stale-carry': run['carry_forward'][0]['value_hash'] = '0' * 64
    if mutation == 'false-revision': run['carry_forward'][0]['revision_id'] = 'revision-' + '0' * 20
    assert pass_errors(run, state, state, revisions)


def test_failed_inspections_queries_and_old_sources_are_not_successful_monitoring():
    state, revisions, run = fixture()
    w = run['watch_checks'][0]
    w.update(result='blocked', checked_at=TODAY, blocked_reason='HTTP 403', remaining_gaps=['Source unavailable'])
    account_domains(run, state)
    assert not pass_errors(run, state, state, revisions)
    assert not completion(run)['watch_complete']
    inspect(run)
    w['blocked_reason'] = None
    state[('source', 'src-test')]['accessed_at'] = '2000-01-01'
    assert any('stale' in e for e in pass_errors(run, fixture()[0], state, revisions))


def test_shared_provider_scope_requires_exact_product_and_all_model_dependencies():
    state, revisions, run = fixture(shared=True)
    inspect(run)
    c = candidate(state, run, kind='provider', ident='vendor', path='/privacy_data_use')
    c['model_ids'] = ['model-a', 'model-b']
    account_domains(run, state)
    assert any('dependencies omitted' in e for e in pass_errors(run, state, state, revisions))
    c['dependencies'].append({'model_id': 'model-b', 'result': 'confirmed', 'checked_at': TODAY,
        'check_ids': ['watch-documentation'], 'rationale': 'Product B policy applicability independently reviewed.'})
    assert not pass_errors(run, state, state, revisions)
    run['watch_checks'][0]['scope'][1]['product'] = 'Product A'
    assert any('join is unresolved' in e for e in pass_errors(run, state, state, revisions))


def test_exact_field_freshness_is_invalidated_by_changed_value_and_does_not_transfer():
    state, revisions, run = fixture()
    inspect(run)
    candidate(state, run)
    account_domains(run, state)
    assert not pass_errors(run, state, state, revisions)
    assert field_freshness(run, 'model', 'model-a', '/identity/name', state) == TODAY
    assert field_freshness(run, 'model', 'model-a', '/identity', state) is None
    assert field_freshness(run, 'model', 'model-a', '', state) is None
    assert field_freshness(run, 'model', 'model-b', '/identity/name', state) is None
    changed = deepcopy(state)
    changed[('model', 'model-a')]['identity']['name'] = 'Different Model'
    assert field_freshness(run, 'model', 'model-a', '/identity/name', changed) is None
    assert any('unaccounted factual edit' in e for e in pass_errors(run, state, changed, revisions))


def test_new_measurement_or_price_cannot_hide_outside_declared_change_scope():
    state, revisions, run = fixture()
    inspect(run)
    changed = deepcopy(state)
    changed[('price', 'new-offer')] = {'model_id': 'model-a', 'provider_id': 'vendor', 'product': 'Product A', 'rates': [3]}
    assert any('unaccounted factual edit' in e for e in pass_errors(run, state, changed, revisions))


def test_partial_checks_cannot_refresh_record_dates_full_domain_ledger_or_replay_freshness():
    state, revisions, run = fixture()
    inspect(run)
    candidate(state, run)
    changed = deepcopy(state)
    changed[('model','model-a')]['verified_at'] = TODAY
    assert any('whole-record verification' in e for e in pass_errors(run,state,changed,revisions))
    changed = deepcopy(state)
    changed[('research_coverage','coverage-a')] = {'checked_at':TODAY}
    assert any('full-domain last-checked' in e for e in pass_errors(run,state,changed,revisions))
    run['observation_mode']='historical_replay'
    assert field_freshness(run,'model','model-a','/identity/name',state) is None


def test_duplicate_shared_queries_and_recorded_time_budget_fail():
    state, revisions, run = fixture()
    q = {'id': 'query-test', 'query': 'exact model changes', 'checked_at': TODAY, 'outcome': 'no_matched_sources',
         'urls': [], 'model_ids': ['model-a'], 'domains': ['behavior'], 'notes': 'No matched public report located.'}
    run['searches'] = [q, {**q, 'id': 'query-copy'}]
    assert any('duplicate query' in e for e in pass_errors(run, state, state, revisions))
    run['searches'] = [q]
    run['bounds']['max_searches'] = 0
    assert any('search budget' in e for e in pass_errors(run, state, state, revisions))
    run['usage']['research_minutes'] = 26
    assert any('time budget' in e for e in pass_errors(run, state, state, revisions))


def test_captured_evidence_state_preserves_receipt_after_later_source_removal():
    state, revisions, run = fixture()
    inspect(run)
    account_domains(run, state)
    observed = deepcopy(state)
    later = deepcopy(state)
    del later[('source', 'src-test')]
    assert not pass_errors(run, state, observed, revisions)
    assert pass_errors(run, state, later, revisions)


def test_completion_flag_is_rejected_and_schema_is_valid():
    _, _, run = fixture()
    schema = json.loads((ROOT / 'schema/maintenance-pass-record.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(run)
    run['complete'] = True
    assert list(validator.iter_errors(run))


def test_new_model_intake_is_separate_from_existing_ids_and_does_not_complete_assessment():
    state,revisions,run=fixture()
    inspect(run)
    c=candidate(state,run,disposition='pending')
    c.update(model_ids=[],affected_fields=[],dependencies=[],discovered_model={
        'creator':'Example Creator','name':'New Model','upstream_id':'new-model',
        'release_date':TODAY,'source_urls':['https://example.org/new-model']})
    account_domains(run,state)
    errors,report=validated_report(run,state,state,revisions)
    assert not errors and report['watch_complete'] and not report['reconciliation_complete']
    assert ('model','new-model') not in state
    c['disposition']='investigated_unknown'
    assert any('separate full assessment' in e for e in pass_errors(run,state,state,revisions))


def test_real_capture_order_idempotence_and_retained_evidence(tmp_path):
    from tools.knowledge import canonical, capture, history
    from tools.migrate_v2 import write_yaml
    from tools.research_runs import baseline_state
    state, _, _ = fixture()
    for (kind, ident), row in state.items():
        if kind in {'model', 'provider'}:
            path = tmp_path / ('models/test' if kind == 'model' else 'providers') / ident / 'profile.yaml'
            path.parent.mkdir(parents=True, exist_ok=True)
            write_yaml(path, row)
    for directory in ['data', 'evidence', 'history']:
        (tmp_path / directory).mkdir(exist_ok=True)
    mapping = {'price':'data/pricing.yaml','access':'data/access.yaml','release':'data/releases.yaml',
        'source':'evidence/sources.yaml','observation':'evidence/observations.yaml','behavior':'data/behavior.yaml',
        'access_coverage':'data/access-coverage.yaml','benchmark':'data/benchmarks.yaml',
        'research_coverage':'data/research-coverage.yaml','research_contract':'data/research-contract.yaml',
        'research_run':'data/research-runs.yaml','alias':'data/aliases.yaml',
        'maintenance_contract':'data/maintenance-contract.yaml','maintenance_pass':'data/maintenance-passes.yaml'}
    for kind, path in mapping.items():
        write_yaml(tmp_path / path, {'schema_version':'1.0','records':[r for (k, _),r in state.items() if k==kind]})
    write_yaml(tmp_path / 'data/capability-taxonomy.yaml', {'capabilities':[]})
    capture(tmp_path, TODAY, 'Synthetic test baseline', ['src-test'])
    current = {key:value for key,(_,value) in canonical(tmp_path).items()}
    w = {'id':'watch-capture','source_id':'src-test','scope':[{'model_id':'model-a','domain':'capabilities',
        'entity_type':'model','entity_id':'model-a','path':'/identity','product':None,'task_ids':[]}]}
    run = make_pass(current, history(tmp_path), 'b'*40, 'maintenance-pass-capture', ['model-a'], [w],
        {'max_research_minutes':10,'max_searches':2}, TODAY, 'discovery')
    inspect(run)
    account_domains(run, current)
    write_yaml(tmp_path / 'data/maintenance-passes.yaml', {'records':[run]})
    updates = capture(tmp_path, TODAY, 'Synthetic receipt', ['src-test'])
    assert updates[-1]['entity_type']=='maintenance_pass'
    observed=baseline_state(history(tmp_path),updates[-1]['id'])
    assert not pass_errors(run,current,observed,history(tmp_path))
    assert capture(tmp_path,TODAY,'Reapply identical reviewed receipt',['src-test'])==[]
    source=read(tmp_path / 'evidence/sources.yaml')
    source['records']=[]
    write_yaml(tmp_path / 'evidence/sources.yaml',source)
    capture(tmp_path,TODAY,'Synthetic source retirement',['src-test'])
    assert not pass_errors(run,current,baseline_state(history(tmp_path),updates[-1]['id']),history(tmp_path))
