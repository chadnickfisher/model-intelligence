"""Current repository drift never becomes an overwrite or evidence certificate."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import pytest
from tools import research_audit as audit, research_partial as partial
from test_research_batch import fixture, baseline, MID, SID


def selection(changes, baseline, dependencies=None):
    units = partial.units_for(changes, baseline)
    for unit in units:
        unit['dependencies'] = (dependencies or {}).get(unit['record_id'], [])
    return {'units': [{k: v for k, v in u.items() if k not in {'value', 'change'}} for u in units],
            'compiled': {'changes': changes}}


def model_change(record, evidence=()):
    return {'kind': 'model', 'record': record, 'evidence_ids': list(evidence)}


def simple():
    before = {('model', 'model-a'): {'id': 'model-a', 'identity': {'version': 'v1'},
                                   'notes': ['old'], 'limitations': ['old limitation'],
                                   'capabilities': [], 'performance_characteristics': []}}
    after = deepcopy(before[('model', 'model-a')])
    after['notes'] = ['researched note']
    return before, selection([model_change(after)], before)


def test_disjoint_current_edit_is_preserved_without_mutating_inputs():
    baseline, selected = simple()
    current = deepcopy(baseline)
    current[('model', 'model-a')]['limitations'].append('Concurrent edit')
    original = deepcopy((baseline, selected, current))
    report = audit.reconcile_current(selected, baseline, current)
    assert report['counts'] == {'ready': 1} and len(report['current_differences']) == 1
    assert (baseline, selected, current) == original


def test_same_field_current_edit_is_a_conflict():
    baseline, selected = simple()
    current = deepcopy(baseline)
    current[('model', 'model-a')]['notes'] = ['Concurrent different conclusion']
    report = audit.reconcile_current(selected, baseline, current)
    assert report['counts'] == {'conflict': 1}
    assert report['units'][0]['current_value_hash'] != report['units'][0]['proposed_value_hash']


def test_already_present_proposal_is_a_noop():
    baseline, selected = simple()
    current = deepcopy(baseline)
    current[('model', 'model-a')]['notes'] = ['researched note']
    assert audit.reconcile_current(selected, baseline, current)['counts'] == {'already_present': 1}


@pytest.mark.parametrize('change', ['identity', 'removed'])
def test_current_identity_change_or_removal_blocks_profile_update(change):
    baseline, selected = simple()
    current = deepcopy(baseline)
    if change == 'identity': current[('model', 'model-a')]['identity']['version'] = 'v2'
    else: del current[('model', 'model-a')]
    assert audit.reconcile_current(selected, baseline, current)['counts'] == {'conflict': 1}


def test_changed_existing_source_context_defers_claim():
    baseline, selected = simple()
    baseline[('source', 'source-a')] = {'id': 'source-a', 'url': 'https://example.org/research', 'title': 'Original'}
    selected['compiled']['changes'][0]['evidence_ids'] = ['source-a']
    current = deepcopy(baseline)
    current[('source', 'source-a')]['title'] = 'Changed context'
    report = audit.reconcile_current(selected, baseline, current)
    assert report['counts'] == {'conflict': 1}
    assert report['units'][0]['changed_reference_ids'] == ['source-a']


def test_new_source_url_cannot_duplicate_new_current_canonical_identity():
    row = {'id': 'source-proposed', 'url': 'https://example.org/research'}
    selected = selection([{'kind': 'source', 'record': row, 'evidence_ids': []}], {})
    current = {('source', 'source-other'): {**row, 'id': 'source-other'}}
    assert audit.reconcile_current(selected, {}, current)['counts'] == {'conflict': 1}


def test_transitive_current_conflict_defers_dependents_only():
    baseline = {('source', 'source-a'): {'id': 'source-a', 'url': 'https://example.org/a', 'title': 'old'}}
    changes = [ {'kind': 'source', 'record': {'id': 'source-a', 'url': 'https://example.org/a', 'title': 'new'}, 'evidence_ids': []},
               {'kind': 'source', 'record': {'id': 'source-b', 'url': 'https://example.org/b'}, 'evidence_ids': []},
               {'kind': 'source', 'record': {'id': 'source-c', 'url': 'https://example.org/c'}, 'evidence_ids': []},
               {'kind': 'source', 'record': {'id': 'source-d', 'url': 'https://example.org/d'}, 'evidence_ids': []}]
    selected = selection(changes, baseline)
    units = {u['record_id']: u for u in selected['units']}
    units['source-b']['dependencies'] = [units['source-a']['id']]
    units['source-c']['dependencies'] = [units['source-b']['id']]
    current = deepcopy(baseline)
    current[('source', 'source-a')]['title'] = 'Concurrent conflict'
    report = audit.reconcile_current(selected, baseline, current)
    assert report['counts'] == {'conflict': 1, 'dependency_deferred': 2, 'ready': 1}


def test_missing_null_and_json_pointer_escapes_remain_distinct():
    baseline, selected = simple()
    unit = {**selected['units'][0], 'path': '/key~1with~0escapes'}
    assert audit.value_at(baseline, unit) is audit.MISSING
    current = deepcopy(baseline)
    current[('model', 'model-a')]['key/with~escapes'] = None
    assert audit.value_at(current, unit) is None
    assert audit.value_hash(None) != audit.value_hash(audit.MISSING)


def test_stable_finding_id_comparison_preserves_unrelated_finding():
    baseline, _ = simple()
    baseline[('model', 'model-a')]['capabilities'] = [{'id': 'finding-a', 'claim': 'old'}, {'id': 'finding-b', 'claim': 'old'}]
    after = deepcopy(baseline[('model', 'model-a')])
    after['capabilities'][0]['claim'] = 'new'
    selected = selection([model_change(after)], baseline)
    current = deepcopy(baseline)
    current[('model', 'model-a')]['capabilities'][1]['claim'] = 'Concurrent separate finding'
    assert audit.reconcile_current(selected, baseline, current)['counts'] == {'ready': 1}
    current[('model', 'model-a')]['capabilities'].append(deepcopy(current[('model', 'model-a')]['capabilities'][0]))
    with pytest.raises(ValueError, match='Ambiguous'): audit.reconcile_current(selected, baseline, current)


def test_full_audit_preserves_pending_and_never_uses_model_adapter(fixture, baseline, monkeypatch):
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: pytest.fail('Unexpected process/model execution'))
    packet, assignment = fixture
    original = deepcopy(packet)
    report = audit.audit(packet, assignment, baseline, deepcopy(baseline))
    assert report['counts'] == {'ready': 2}
    assert report['original_accounting_counts']['pending'] > 0 and not report['completion']['complete']
    assert report['model_calls'] == 0 and not report['independent_claim_verification_performed']
    assert not report['catalog_updated'] and packet == original


def test_real_structural_dependency_respects_current_source_conflict(fixture, baseline):
    packet, assignment = fixture
    current = deepcopy(baseline)
    current[('source', SID)]['title'] += ' Concurrent change'
    report = audit.audit(packet, assignment, baseline, current)
    assert report['counts'] == {'conflict': 1, 'dependency_deferred': 1}


@pytest.mark.parametrize('kind', ['research_contract', 'task'])
def test_changed_current_research_rules_block_building_under_old_rules(fixture, baseline, kind):
    packet, assignment = fixture
    current = deepcopy(baseline)
    del current[next(key for key in current if key[0] == kind)]
    report = audit.audit(packet, assignment, baseline, current)
    assert report['counts'] == {'conflict': 2} and report['ready_unit_ids'] == []
    assert report['changed_rule_ids']


def test_cli_rejects_modified_packet_without_retaining_output(tmp_path):
    root = Path(__file__).resolve().parents[1]
    work = root / '.local/research/audit-cli-reject-test'
    work.mkdir(parents=True, exist_ok=True)
    packet = work / 'invalid.json'
    packet.write_text('{"tampered": true}', encoding='utf-8')
    destination = work / 'output'
    result = subprocess.run([sys.executable, str(root/'tools/research_audit.py'), '--packet', str(packet),
        '--assignment', str(work/'unused-assignment.json'), '--destination', str(destination),
        '--bytes', '10', '--sha256', '0'*64], cwd=root, capture_output=True, text=True)
    assert result.returncode == 1 and not destination.exists()
    assert 'tampered' not in result.stdout + result.stderr
