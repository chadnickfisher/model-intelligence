"""Independent proposals survive; failed claims never gain evidence certification."""
from copy import deepcopy
from hashlib import sha256
import json
import os
import subprocess
import sys
import pytest
from test_research_batch import baseline, fixture, MID, SID, TODAY, inspected
from tools import research_partial as partial, research_batch as batch
from tools.knowledge import record_hash


def test_valid_partial_keeps_strict_compiler_and_pending_work(fixture, baseline):
    packet, assignment = fixture
    before = deepcopy(packet)
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['candidate_units'] == 2 and result['deferred_units'] == 0
    assert result['evidence_reviewed'] is False and not result['compiled']['completion']['complete']
    assert packet == before
    assert result['compiled']['candidate'][('model', MID)]['notes'][-1].startswith('Synthetic')


def test_source_metadata_conflict_defers_dependents_without_poisoning_disjoint_field(fixture, baseline):
    from tools.research_reconcile import remap_refs
    packet, assignment = fixture
    packet = remap_refs(packet, {SID: 'new:conflicting-source'})
    source = packet['changes'][0]
    source['previous_hash'], source['identity_key'] = None, source['record']['url']
    source['record']['title'] = 'Conflicting synthetic title'
    extra = deepcopy(next(r for (k, i), r in baseline.items() if k == 'source' and i != SID and r['source_type'] == 'primary'))
    extra['accessed_at'] = TODAY
    extra['claim_scope'].append('Synthetic independent source.')
    propose(packet, baseline, 'source', extra, ['/accessed_at', '/claim_scope'], extra['id'])
    next(r for r in packet['research_run']['source_checks'] if r['category'] == 'primary')['evidence_ids'].append(extra['id'])
    packet['changes'][1]['record']['limitations'].append('Synthetic independently supported limitation.')
    packet['changes'][1]['evidence_ids'].append(extra['id'])
    packet['changes'][1]['checked_paths'].append('/limitations')
    inspected_row(packet['research_run'], '/limitations', source=extra['id'])
    original = deepcopy(packet)
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['compiled']['candidate'][('source', SID)] == baseline[('source', SID)]
    model = result['compiled']['candidate'][('model', MID)]
    assert model['notes'] == baseline[('model', MID)]['notes']
    assert model['limitations'] == packet['changes'][1]['record']['limitations']
    assert result['reconciliation']['source_conflicts'] and packet == original


def test_immutable_version_deferred_but_profile_notes_survive(fixture, baseline):
    packet, assignment = fixture
    model = packet['changes'][1]['record']
    prior = baseline[('model', MID)]
    model['identity']['version'] = 'synthetic-checkpoint'
    model['verified_at'] = '2000-01-01'
    packet['changes'][1]['checked_paths'] += ['/identity/version', '/verified_at']
    result = partial.compile_partial(packet, assignment, baseline)
    candidate = result['compiled']['candidate'][('model', MID)]
    assert candidate['identity']['version'] == prior['identity']['version']
    assert candidate['verified_at'] == prior['verified_at']
    assert candidate['notes'] == model['notes']
    assert result['deferred_units'] == 2 and result['candidate_units'] == 2


@pytest.mark.parametrize('failure', ['date', 'category'])
def test_failed_source_defers_dependent_profile_preserving_dates(fixture, baseline, failure):
    packet, assignment = fixture
    if failure == 'date': packet['changes'][0]['record']['accessed_at'] = '2000-01-01'
    else: packet['changes'][0]['record']['source_type'] = 'not-a-category'
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['deferred_units'] == 2 and result['candidate_units'] == 0
    assert result['compiled']['changes'] == []
    assert result['compiled']['candidate'] == baseline
    assert any(u['category'] == 'dependency_deferred' for u in result['units'])


def inspected_row(run, path, result='value', source=SID):
    row = next(r for r in run['field_checks'] if r['entity_type'] == 'model' and r['path'] == path)
    inspected(row, result)
    row['evidence_ids'] = [source]
    return row


def add_finding(packet, baseline, *, bad=False, ident='new:synthetic-finding'):
    model = packet['changes'][1]['record']
    finding = deepcopy(baseline[('model', MID)]['capabilities'][0])
    finding.update(id=ident, observed_at=TODAY, supporting_evidence_ids=[SID], contradictory_evidence_ids=[])
    if bad: finding['scope'] = 'invalid-scope'
    model['capabilities'].append(finding)
    if '/capabilities' not in packet['changes'][1]['checked_paths']:
        packet['changes'][1]['checked_paths'].append('/capabilities')
    inspected_row(packet['research_run'], '/capabilities')
    return finding


def test_bad_nested_finding_preserves_history_and_valid_profile_field(fixture, baseline):
    packet, assignment = fixture
    add_finding(packet, baseline, bad=True)
    result = partial.compile_partial(packet, assignment, baseline)
    model = result['compiled']['candidate'][('model', MID)]
    assert model['capabilities'] == baseline[('model', MID)]['capabilities']
    assert model['notes'] == packet['changes'][1]['record']['notes']
    assert result['deferred_units'] == 1


def test_bad_one_of_two_nested_findings_does_not_poison_good_finding(fixture, baseline):
    packet, assignment = fixture
    bad = add_finding(packet, baseline, bad=True, ident='new:bad-finding')
    good = add_finding(packet, baseline, ident='new:good-finding')
    # A distinct compound finding avoids generating the same direct identity.
    good.update(scope='compound', task_ids=[], related_task_ids=['coding.scoped_edit', 'coding.tests'])
    result = partial.compile_partial(packet, assignment, baseline)
    findings = result['compiled']['candidate'][('model', MID)]['capabilities']
    assert len(findings) == len(baseline[('model', MID)]['capabilities']) + 1
    assert all(j['scope'] != 'invalid-scope' for j in findings)
    assert result['deferred_units'] == 1


@pytest.mark.parametrize('mutation,match', [('hash', 'hash mismatch'), ('baseline', 'baseline'),
                                           ('assignment', 'assignment'), ('privacy', 'Private'),
                                           ('checklist', 'checklist'), ('duplicate', 'Duplicate')])
def test_global_failures_never_become_partial_success(fixture, baseline, mutation, match):
    packet, assignment = fixture
    if mutation == 'hash': packet['changes'][1]['previous_hash'] = '0' * 64
    elif mutation == 'baseline': packet['baseline_commit'] = '0' * 40
    elif mutation == 'assignment': packet['assignment_id'] = 'wrong'
    elif mutation == 'privacy': packet['changes'][1]['record']['notes'].append('https://drive.google.com/file/d/private/view')
    elif mutation == 'checklist': packet['research_run']['field_checks'].pop()
    else: packet['changes'].append(deepcopy(packet['changes'][0]))
    with pytest.raises(ValueError, match=match): partial.compile_partial(packet, assignment, baseline)


@pytest.mark.parametrize('url', ['https://127.0.0.1/private', 'https://10.0.0.1/private',
                                'https://[::1]/private', 'https://[fd00::1]/private',
                                'https://example.internal/private', 'https://example.org/public?access_token=private',
                                'https://user:password@example.org/private', 'file:///private/report'])
def test_private_content_cannot_be_deferred_out_of_packet(fixture, baseline, url):
    packet, assignment = fixture
    packet['changes'][0]['record']['source_type'] = 'invalid-category'
    packet['changes'][0]['record']['limitations'].append(url)
    with pytest.raises(ValueError, match='Private'):
        partial.compile_partial(packet, assignment, baseline)


@pytest.mark.parametrize('field', ['title', 'limitations', 'url'])
def test_malformed_new_source_alias_is_local_deferral(fixture, baseline, field):
    from tools.research_reconcile import remap_refs
    packet, assignment = fixture
    packet = remap_refs(packet, {SID: 'new:malformed-source'})
    source = packet['changes'][0]
    source['previous_hash'], source['identity_key'] = None, source['record']['url']
    source['record'].pop(field)
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['deferred_units'] >= 2 and result['compiled']['changes'] == []
    assert result['compiled']['candidate'] == baseline


def test_historical_finding_deletion_is_deferred_not_applied(fixture, baseline):
    packet, assignment = fixture
    packet['changes'][1]['record']['capabilities'].pop()
    packet['changes'][1]['checked_paths'].append('/capabilities')
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['compiled']['candidate'][('model', MID)]['capabilities'] == baseline[('model', MID)]['capabilities']
    assert result['compiled']['candidate'][('model', MID)]['notes'] == packet['changes'][1]['record']['notes']


def propose(packet, baseline, kind, record, paths, source=SID):
    packet['changes'].append({'kind': kind, 'record': record, 'previous_hash': record_hash(baseline[(kind, record['id'])]),
                              'identity_key': None, 'evidence_ids': [source], 'checked_paths': paths,
                              'rationale': 'Synthetic dependency regression.'})
    for row in packet['research_run']['field_checks']:
        if row['entity_type'] == kind and row['entity_id'] == record['id'] and row['path'] in paths:
            inspected(row, 'value')
            row['evidence_ids'] = [source]


def test_bad_finding_defers_exact_task_assessment_across_files(fixture, baseline):
    packet, assignment = fixture
    finding = add_finding(packet, baseline, bad=True)
    task = 'coding.scoped_edit'
    old = next(r for (k, _), r in baseline.items() if k == 'task_assessment' and r['model_id'] == MID and r['task_id'] == task)
    assessment = deepcopy(old)
    assessment.update(result='assessed', applicability='applicable', checked_at=TODAY,
                      judgment_ids=[finding['id']], evidence_ids=[SID], rationale='Synthetic dependent claim.',
                      confidence_rationale='Synthetic dated evidence.')
    propose(packet, baseline, 'task_assessment', assessment, ['/judgment_ids'])
    row = next(r for r in packet['research_run']['task_decisions'] if r['task_id'] == task)
    inspected(row, 'assessed')
    row.update(applicability='applicable', judgment_ids=[finding['id']], confidence_rationale=assessment['confidence_rationale'])
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['compiled']['candidate'][('task_assessment', old['id'])] == old
    unit = next(u for u in result['units'] if u['kind'] == 'task_assessment')
    assert unit['category'] == 'dependency_deferred' and unit['dependencies']
    assert result['compiled']['candidate'][('model', MID)]['notes'] == packet['changes'][1]['record']['notes']


def test_bad_accounting_defers_only_its_field_and_preserves_original(fixture, baseline):
    packet, assignment = fixture
    row = inspected_row(packet['research_run'], '/notes')
    row['search_references'] = [{'query': 'synthetic mismatched date', 'checked_at': '2000-01-01',
                                 'outcome': 'sources_located', 'urls': ['https://example.org/public'], 'notes': ''}]
    original = deepcopy(packet)
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['compiled']['candidate'][('model', MID)] == baseline[('model', MID)]
    assert len(result['compiled']['changes']) == 1 and result['compiled']['changes'][0]['kind'] == 'source'
    assert any(u.get('category') == 'accounting_deferred' for u in result['units'])
    assert packet == original
    assert any(r['validation_errors'] for r in result['accounting_projection'])


def test_coverage_does_not_refresh_when_domain_claim_is_deferred(fixture, baseline):
    packet, assignment = fixture
    packet['changes'][1]['record']['identity']['version'] = 'invalid-replacement'
    old = baseline[('research_coverage', 'research-coverage-' + MID + '-capabilities')]
    coverage = deepcopy(old)
    coverage.update(result='changed', checked_at=TODAY, evidence_ids=[SID])
    propose(packet, baseline, 'research_coverage', coverage, ['/result'])
    row = next(r for r in packet['research_run']['domain_checks'] if r['model_id'] == MID and r['domain'] == 'capabilities')
    inspected(row, 'changed')
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['compiled']['candidate'][('research_coverage', old['id'])] == old
    assert next(u for u in result['units'] if u['kind'] == 'research_coverage')['category'] == 'dependency_deferred'


def test_valid_mutually_linked_route_and_price_are_kept(fixture, baseline):
    packet, assignment = fixture
    route_old = next(r for (k, _), r in baseline.items() if k == 'access' and r['model_id'] == MID and r['price_ids'])
    price_old = baseline[('price', route_old['price_ids'][0])]
    route, price = deepcopy(route_old), deepcopy(price_old)
    route['notes'].append('Synthetic route update.')
    price['notes'].append('Synthetic price update.')
    propose(packet, baseline, 'access', route, ['/notes'])
    propose(packet, baseline, 'price', price, ['/notes'])
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['deferred_units'] == 0
    assert result['compiled']['candidate'][('access', route['id'])] == route
    assert result['compiled']['candidate'][('price', price['id'])] == price


def test_pending_accounting_cleanup_does_not_invent_inspection(fixture, baseline):
    packet, assignment = fixture
    row = next(r for r in packet['research_run']['field_checks'] if r['result'] == 'not_checked')
    row['rationale'] = 'Still pending; inconsistent metadata.'
    result = partial.compile_partial(packet, assignment, baseline)
    selected = next(r for r in result['selected_packet']['research_run']['field_checks']
                    if partial.identity(r, partial.CHECK_KEYS['field_checks']) == partial.identity(row, partial.CHECK_KEYS['field_checks']))
    assert selected['result'] == 'not_checked' and selected['checked_at'] is None and selected['evidence_ids'] == []
    assert row['rationale'] == 'Still pending; inconsistent metadata.'


def test_noop_record_is_an_explicit_deferral(fixture, baseline):
    packet, assignment = fixture
    packet['changes'][1]['record'] = deepcopy(baseline[('model', MID)])
    result = partial.compile_partial(packet, assignment, baseline)
    assert result['deferred_units'] == 1 and result['candidate_units'] == 1


def test_invalid_price_defers_route_and_assessment_transitively(fixture, baseline):
    packet, assignment = fixture
    route_old = next(r for (k, _), r in baseline.items() if k == 'access' and r['model_id'] == MID and r['price_ids'])
    price_old = baseline[('price', route_old['price_ids'][0])]
    price, route = deepcopy(price_old), deepcopy(route_old)
    price['billing_method'] = 'unsupported-billing-method'
    route['notes'].append('Synthetic dependent route.')
    propose(packet, baseline, 'price', price, ['/billing_method'])
    propose(packet, baseline, 'access', route, ['/notes'])
    old = next(r for (k, _), r in baseline.items() if k == 'task_assessment' and r['model_id'] == MID and 'aggregate' in r)
    assessment = deepcopy(old)
    assessment.update(checked_at=TODAY, evidence_ids=[SID], rationale='Synthetic dependent assessment.')
    assessment['aggregate'].update(assessed_at=TODAY, supporting_evidence_ids=[SID], contradictory_evidence_ids=[],
                                   access_ids=[route['id']])
    propose(packet, baseline, 'task_assessment', assessment, ['/aggregate/access_ids'])
    result = partial.compile_partial(packet, assignment, baseline)
    by_kind = {u['kind']: u for u in result['units'] if u['kind'] in {'access', 'price', 'task_assessment'}}
    assert by_kind['price']['category'] == 'proposal_inconsistent'
    assert by_kind['access']['category'] == by_kind['task_assessment']['category'] == 'dependency_deferred'
    for kind, before in [('price', price_old), ('access', route_old), ('task_assessment', old)]:
        assert result['compiled']['candidate'][(kind, before['id'])] == before
    assert result['compiled']['candidate'][('model', MID)]['notes'] == packet['changes'][1]['record']['notes']


def test_cli_repeat_is_identical_across_process_hash_seeds(fixture, baseline, tmp_path):
    if not tmp_path.resolve().is_relative_to(batch.ROOT / '.local/research'):
        pytest.skip('Requires private CLI input storage')
    packet, assignment = fixture
    old = next(r for (k, _), r in baseline.items() if k == 'access' and r['model_id'] == MID)
    route = deepcopy(old)
    route['notes'].append('Synthetic deferred note.')
    route['restrictions'].append('Synthetic deferred restriction.')
    packet['changes'].append({'kind': 'access', 'record': route, 'previous_hash': record_hash(old),
                              'identity_key': None, 'evidence_ids': [SID], 'checked_paths': ['/notes', '/restrictions'],
                              'rationale': 'Synthetic unchecked fields stay pending.'})
    raw = json.dumps(packet).encode()
    packet_path, assignment_path = tmp_path / 'packet.json', tmp_path / 'assignment.json'
    packet_path.write_bytes(raw)
    assignment_path.write_text(json.dumps(assignment), encoding='utf-8')
    destination = tmp_path / 'selection'
    command = [sys.executable, str(batch.ROOT / 'tools/research_partial.py'), '--packet', str(packet_path),
               '--assignment', str(assignment_path), '--destination', str(destination), '--bytes', str(len(raw)),
               '--sha256', sha256(raw).hexdigest()]
    reports = []
    for seed in ['1', '2']:
        env = {**os.environ, 'PYTHONHASHSEED': seed}
        result = subprocess.run(command, cwd=batch.ROOT, env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        reports.append((destination / 'selection.json').read_bytes())
    assert reports[0] == reports[1]


def test_final_repository_stage_validates_and_preserves_existing_work(fixture, baseline, tmp_path, monkeypatch):
    if not tmp_path.resolve().is_relative_to(batch.ROOT / '.local/research'):
        pytest.skip('Requires explicit ignored research basetemp')
    packet, assignment = fixture
    extra = deepcopy(next(r for (k, i), r in baseline.items() if k == 'source' and i != SID and r['source_type'] == 'primary'))
    extra['accessed_at'] = TODAY
    extra['claim_scope'].append('Synthetic second source for batched staging.')
    propose(packet, baseline, 'source', extra, ['/accessed_at', '/claim_scope'], extra['id'])
    next(r for r in packet['research_run']['source_checks'] if r['category'] == 'primary')['evidence_ids'].append(extra['id'])
    packet['changes'][1]['record']['identity']['version'] = 'rejected-version'
    before = (batch.ROOT / 'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes()
    result = partial.compile_partial(packet, assignment, baseline)
    writes = []
    real_write = batch.write_yaml
    def counted_write(path, value):
        writes.append(path)
        real_write(path, value)
    monkeypatch.setattr(batch, 'write_yaml', counted_write)
    staged = batch.stage(batch.ROOT, result['compiled'], assignment, 'a' * 64, tmp_path / 'stage')
    assert staged['status'] == 'validated_local_candidate' and all(c['exit_code'] == 0 for c in staged['checks'])
    assert (batch.ROOT / 'models/anthropic/claude-fable-5-1/profile.yaml').read_bytes() == before
    assert sum(path.name == 'sources.yaml' for path in writes) == 1
    from tools.knowledge import canonical
    final = canonical(tmp_path / 'stage/candidate')
    assert final[('source', extra['id'])][1] == extra
    assert all(final[key][1] == record for key, record in result['compiled']['candidate'].items())
