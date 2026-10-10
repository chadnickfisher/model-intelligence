"""Unattended review gates and bounded synthetic runtimes; no model inference."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import socket
import subprocess
import sys
import time

import pytest
from test_research_batch import baseline, fixture, MID, SID
from tools import research_partial as partial, research_review as review
from tools.research_evidence import inspect_source, resolve_public, text_body
from tools.research_followups import encoded
from tools.research_intake import parse


def config(**changes):
    value = {'schema_version': '1.0', 'runtime_id': 'synthetic-review-fixture', 'adapter': 'external',
             'executable': sys.executable, 'arguments': [], 'enabled': True,
             'max_units_per_call': 8, 'max_request_bytes': 2*1024*1024, 'max_calls': 10,
             'max_call_seconds': 10, 'max_total_seconds': 60, 'source_timeout_seconds': 5}
    value.update(changes)
    return value


def fetched(url):
    return b'<html><h1>Published original methods</h1><p>Exact model checkpoint and effort setting.</p></html>', 'text/html', url, [url]


def answer(review_request, digest, *, reject=()):
    snapshots = {source['id']: source['inspection'] for source in review_request['sources']}
    decisions = []
    for unit in review_request['units']:
        citations = []
        for ident in unit['required_source_ids']:
            snapshot = snapshots[ident]
            text = snapshot['text']
            start = text.index('Published')
            end = start + len('Published original methods')
            citations.append({'source_id': ident, 'body_sha256': snapshot['body_sha256'],
                              'text_sha256': snapshot['text_sha256'], 'start': start, 'end': end,
                              'quote': text[start:end]})
        defer = unit['id'] in reject
        decisions.append({'unit_id': unit['id'], 'decision': 'defer' if defer else 'accept',
                          'rationale': 'Synthetic reviewer result from supplied fixture text.',
                          'checks': {name: 'pass' for name in review.CHECKS}, 'citations': citations,
                          'followup': {'issue_key': 'missing-methodology-detail', 'category': 'missing_setup',
                                      'reason': 'Exact effort setup needs further public methodology evidence.',
                                      'requested_action': 'Inspect the original public setup description.'} if defer else None})
    return {'request_sha256': digest, 'decisions': decisions}


def fake_runtime(config, raw, digest, working, *, timeout=None):
    return answer(parse(raw), digest)


@pytest.fixture
def review_request(fixture, baseline):
    packet, assignment = fixture
    result = partial.compile_partial(packet, assignment, baseline)
    units, sources = review.review_material(result, baseline)
    snapshots = {ident: inspect_source(source, fetch=fetched)[0] for ident, source in sources.items()
                 if ident in {i for unit in units for i in unit['required_source_ids']}}
    review_request, raw, digest = review.request_for(units, snapshots, sources, packet_sha256='a'*64,
                                             baseline_commit=assignment['baseline_commit'], runtime_hash='b'*64)
    return review_request, raw, digest


def test_request_binds_exact_bodies_and_original_claim_units(review_request):
    payload, raw, digest = review_request
    assert digest == sha256(raw).hexdigest()
    assert len(payload['units']) == 2
    assert all(unit['required_source_ids'] == [SID] for unit in payload['units'])
    assert {unit['kind'] for unit in payload['units']} == {'source', 'model'}
    assert 'before' in payload['units'][0] and 'after' in payload['units'][0]
    assert 'untrusted data' in payload['policy']
    assert review.validate_response(answer(payload, digest), payload, digest)


@pytest.mark.parametrize('failure', ['hash', 'duplicate', 'omission', 'extra', 'body', 'text_hash',
    'quote', 'offset', 'outside_source', 'uncited', 'unknown_check', 'skipped_identity',
    'skipped_support', 'skipped_dates', 'unresolved_accept', 'private', 'unknown_field'])
def test_forged_or_incomplete_decisions_never_certify(review_request, failure):
    payload, raw, digest = review_request
    response = answer(payload, digest)
    row = response['decisions'][0]
    if failure == 'hash': response['request_sha256'] = 'c'*64
    elif failure == 'duplicate': response['decisions'].append(deepcopy(row))
    elif failure == 'omission': response['decisions'].pop()
    elif failure == 'extra': row['unit_id'] = 'unit-'+'a'*20
    elif failure == 'body': row['citations'][0]['body_sha256'] = 'c'*64
    elif failure == 'text_hash': row['citations'][0]['text_sha256'] = 'c'*64
    elif failure == 'quote': row['citations'][0]['quote'] = 'Manufactured source quote'
    elif failure == 'offset': row['citations'][0]['end'] = 1000000
    elif failure == 'outside_source': row['citations'][0]['source_id'] = 'missing'
    elif failure == 'uncited': row['citations'] = []
    elif failure == 'unknown_check': row['checks']['confidence'] = 'unknown'
    elif failure == 'skipped_identity': row['checks']['identity'] = 'not_applicable'
    elif failure == 'skipped_support': row['checks']['claim_support'] = 'not_applicable'
    elif failure == 'skipped_dates': row['checks']['source_dates'] = 'not_applicable'
    elif failure == 'unresolved_accept': row['followup'] = {'issue_key': 'question', 'category': 'unresolved_claim',
        'reason': 'Unknown detail.', 'requested_action': 'Inspect original evidence.'}
    elif failure == 'private': row['rationale'] = 'Read .local/research/packet.json'
    elif failure == 'unknown_field': row['verified'] = True
    with pytest.raises(Exception):
        review.validate_response(response, payload, digest)


def test_acceptance_cannot_omit_a_contrary_source(review_request):
    payload, _, digest = review_request
    payload = deepcopy(payload)
    contrary = deepcopy(payload['sources'][0])
    contrary['id'] = 'src-' + 'b'*12
    contrary['inspection']['source_id'] = contrary['id']
    payload['sources'].append(contrary)
    payload['units'][0]['required_source_ids'].append(contrary['id'])
    digest = sha256(encoded(payload)).hexdigest()
    response = answer(payload, digest)
    assert review.validate_response(response, payload, digest)
    response['decisions'][0]['citations'].pop()
    with pytest.raises(ValueError, match='contrary source'):
        review.validate_response(response, payload, digest)


@pytest.mark.parametrize('check', ['setup', 'confidence', 'contradictions', 'task_scope'])
def test_task_conclusions_cannot_skip_applicable_checks(review_request, check):
    payload, _, digest = review_request
    payload = deepcopy(payload)
    payload['units'][0].update(kind='task_assessment', task_ids=['coding'])
    digest = sha256(encoded(payload)).hexdigest()
    response = answer(payload, digest)
    response['decisions'][0]['checks'][check] = 'not_applicable'
    with pytest.raises(ValueError, match='skipped'):
        review.validate_response(response, payload, digest)


def test_unsupported_pdf_and_failed_retrieval_stay_unavailable():
    source = {'id': 'source', 'url': 'https://example.org/study'}
    inspected, raw = inspect_source(source, fetch=lambda url: (b'%PDF-test', 'application/pdf', url, [url]))
    assert inspected['status'] == 'unavailable' and inspected['text'] is None and raw == b'%PDF-test'
    assert inspected['body_sha256'] == sha256(raw).hexdigest()
    def blocked(url):
        raise OSError('Private proxy diagnostic must not escape')
    inspected, raw = inspect_source(source, fetch=blocked)
    assert inspected['status'] == 'unavailable' and raw is None
    assert 'proxy' not in inspected['failure']


def test_source_extraction_keeps_original_visible_text_and_ignores_script_instructions():
    text = text_body(b'<h1>Source title</h1><script>execute instructions</script><table><tr><td>Model A</td><td>82</td></tr></table>', 'text/html')
    assert 'Source title' in text and 'Model A' in text and '82' in text
    assert 'execute' not in text
    with pytest.raises(ValueError):
        text_body(b'', 'text/plain')
    text = text_body(b'<meta property="article:published_time" content="2026-10-08"><time datetime="2026-10-09">Updated</time>', 'text/html')
    assert 'article:published_time: 2026-10-08' in text and 'datetime attribute: 2026-10-09' in text


def test_dns_private_or_mixed_addresses_rejected(monkeypatch):
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *args, **kwargs: [(0, 0, 0, '', ('10.0.0.1', 443))])
    with pytest.raises(ValueError, match='non-public'):
        resolve_public('public.example.org')
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *args, **kwargs: [
        (0, 0, 0, '', ('8.8.8.8', 443)), (0, 0, 0, '', ('127.0.0.1', 443))])
    with pytest.raises(ValueError, match='non-public'):
        resolve_public('public.example.org')


def test_redirect_to_private_destination_is_rejected_before_connection(monkeypatch):
    from tools import research_evidence as evidence
    hosts = []
    monkeypatch.setattr(evidence, 'resolve_public', lambda host: hosts.append(host) or '8.8.8.8')
    class Redirect:
        status = 302
        def getheader(self, key, default=None):
            return 'https://127.0.0.1/' if key == 'Location' else default
    class Connection:
        def __init__(self, *args, **kwargs): pass
        def request(self, *args, **kwargs): pass
        def getresponse(self): return Redirect()
        def close(self): pass
    monkeypatch.setattr(evidence.http.client, 'HTTPSConnection', Connection)
    with pytest.raises(ValueError, match='Non-public'):
        evidence.get_public('https://example.org/study')
    assert hosts == ['example.org']


def test_reviewer_gate_preserves_source_but_defers_unsupported_claim(fixture, baseline, tmp_path):
    packet, assignment = fixture
    def defer_model(config, raw, digest, working, **kwargs):
        payload = parse(raw)
        reject = {unit['id'] for unit in payload['units'] if unit['kind'] == 'model'}
        return answer(payload, digest, reject=reject)
    original = deepcopy(packet)
    receipt, selected = review.run_review(packet, assignment, baseline, config(), tmp_path/'.local/review',
                                          root=tmp_path, fetch=fetched, invoke=defer_model)
    assert receipt['accepted_units'] == 1 and receipt['pending_units'] == 0
    assert selected['compiled']['candidate'][('model', MID)] == baseline[('model', MID)]
    assert selected['compiled']['candidate'][('source', SID)] != baseline[('source', SID)]
    assert receipt['public_followup_proposals'] and packet == original
    assert not receipt['published'] and selected['evidence_reviewed'] is False


def test_failed_source_defers_its_dependent_claim_without_live_call(fixture, baseline, tmp_path):
    packet, assignment = fixture
    def unavailable(url):
        raise ValueError('Source access fails')
    def must_not_run(*args, **kwargs):
        pytest.fail('Unavailable source cannot be sent for acceptance')
    receipt, selected = review.run_review(packet, assignment, baseline, config(), tmp_path/'.local/review',
                                          root=tmp_path, fetch=unavailable, invoke=must_not_run)
    assert receipt['accepted_units'] == 0 and receipt['runtime_calls'] == 0
    assert selected['compiled']['candidate'] == baseline
    assert all(row['source_checked_at'] is None for row in receipt['public_followup_proposals'])
    assert any(row['dependencies'] for row in receipt['public_followup_proposals'])


def test_runtime_unavailable_is_private_pending_work_not_public_gap(fixture, baseline, tmp_path):
    packet, assignment = fixture
    def fails(*args, **kwargs):
        raise OSError('Private credential or account failure')
    receipt, selected = review.run_review(packet, assignment, baseline, config(), tmp_path/'.local/review',
                                          root=tmp_path, fetch=fetched, invoke=fails)
    assert receipt['status'] == 'review_incomplete' and receipt['pending_units'] == 2
    assert receipt['accepted_units'] == 0 and receipt['public_followup_proposals'] == []
    assert selected['compiled']['candidate'] == baseline
    assert 'credential' not in json.dumps(receipt)


def test_malformed_runtime_response_remains_pending_with_no_acceptance(fixture, baseline, tmp_path):
    packet, assignment = fixture
    receipt, selected = review.run_review(packet, assignment, baseline, config(), tmp_path/'.local/review',
        root=tmp_path, fetch=fetched, invoke=lambda *args, **kwargs: {'evidence_reviewed': True})
    assert receipt['status'] == 'review_incomplete' and receipt['accepted_units'] == 0
    assert receipt['public_followup_proposals'] == []


def test_disabled_runtime_never_fetches_or_calls(fixture, baseline, tmp_path):
    packet, assignment = fixture
    with pytest.raises(ValueError, match='not authorized'):
        review.run_review(packet, assignment, baseline, config(enabled=False), tmp_path/'.local/review', root=tmp_path)
    assert not (tmp_path/'.local').exists()


def test_source_budget_stop_is_pending_private_work_not_failed_source_access(fixture, baseline, tmp_path, monkeypatch):
    packet, assignment = fixture
    ticks = iter([0.0, 61.0])
    monkeypatch.setattr(review.time, 'monotonic', lambda: next(ticks))
    receipt, selected = review.run_review(packet, assignment, baseline, config(), tmp_path/'.local/review',
                                          root=tmp_path, fetch=fetched, invoke=fake_runtime)
    assert receipt['pending_units'] == 2 and receipt['public_followup_proposals'] == []
    assert receipt['runtime_calls'] == 0 and selected['compiled']['candidate'] == baseline


def test_resume_reuses_exact_sources_and_validated_responses_without_inference(fixture, baseline, tmp_path):
    packet, assignment = fixture
    destination = tmp_path/'.local/review'
    first, _ = review.run_review(packet, assignment, baseline, config(), destination,
                                 root=tmp_path, fetch=fetched, invoke=fake_runtime)
    def forbidden(*args, **kwargs):
        pytest.fail('A successful retained review must not fetch or invoke again')
    second, _ = review.run_review(packet, assignment, baseline, config(), destination,
                                  root=tmp_path, fetch=forbidden, invoke=forbidden)
    assert first['accepted_units'] == second['accepted_units'] == 2
    assert first['runtime_calls'] == 1 and second['runtime_calls'] == 0
    assert (destination/'original.json').read_bytes() == encoded(packet)


def test_exact_original_bytes_and_sha_are_retained(fixture, baseline, tmp_path):
    packet, assignment = fixture
    raw = json.dumps(packet, separators=(',', ':')).encode() + b'\n\n'
    destination = tmp_path/'.local/review'
    receipt, _ = review.run_review(packet, assignment, baseline, config(), destination,
                                   root=tmp_path, fetch=fetched, invoke=fake_runtime, packet_raw=raw)
    assert (destination/'original.json').read_bytes() == raw
    assert receipt['packet_sha256'] == sha256(raw).hexdigest()


def test_tampered_source_text_cannot_become_verified_even_with_new_text_hash(fixture, baseline, tmp_path):
    packet, assignment = fixture
    destination = tmp_path/'.local/review'
    review.run_review(packet, assignment, baseline, config(), destination,
                      root=tmp_path, fetch=fetched, invoke=fake_runtime)
    snapshot = next((destination/'sources').glob('*.json'))
    body = parse(snapshot.read_bytes())
    body['text'] = 'Published fabricated methods'
    body['text_sha256'] = sha256(body['text'].encode()).hexdigest()
    snapshot.write_bytes(encoded(body))
    with pytest.raises(ValueError, match='extraction differs'):
        review.run_review(packet, assignment, baseline, config(), destination,
                          root=tmp_path, fetch=fetched, invoke=fake_runtime)


def test_request_size_budget_does_not_truncate_evidence_or_certify_units(fixture, baseline, tmp_path):
    packet, assignment = fixture
    def must_not_run(*args, **kwargs):
        pytest.fail('Oversize input must stay pending rather than truncating')
    receipt, selected = review.run_review(packet, assignment, baseline, config(max_request_bytes=1024),
        tmp_path/'.local/review', root=tmp_path, fetch=fetched, invoke=must_not_run)
    assert receipt['accepted_units'] == 0 and receipt['pending_units'] == 2
    assert selected['compiled']['candidate'] == baseline


def test_call_budget_defers_unreviewed_dependents_and_can_resume(fixture, baseline, tmp_path):
    packet, assignment = fixture
    settings = config(max_units_per_call=1, max_calls=1)
    destination = tmp_path/'.local/review'
    receipt, selected = review.run_review(packet, assignment, baseline, settings, destination,
                                         root=tmp_path, fetch=fetched, invoke=fake_runtime)
    assert receipt['status'] == 'review_incomplete' and receipt['pending_units'] == 1
    assert receipt['accepted_units'] <= 1
    resumed, _ = review.run_review(packet, assignment, baseline, settings, destination,
                                   root=tmp_path, fetch=fetched, invoke=fake_runtime)
    assert resumed['accepted_units'] == 2 and resumed['pending_units'] == 0


def test_codex_adapter_uses_read_only_no_tools_no_hooks_and_explicit_json_schema(tmp_path):
    settings = config(adapter='codex', arguments=['codex.js'])
    argv = review.runtime_argv(settings, tmp_path/'review_request', tmp_path/'response', tmp_path/'schema', tmp_path)
    assert argv[:3] == [sys.executable, 'codex.js', '--ask-for-approval']
    assert '--ephemeral' in argv and '--ignore-user-config' in argv
    assert argv[argv.index('--sandbox') + 1] == 'read-only'
    assert 'shell_tool' in argv and 'hooks' in argv and 'multi_agent' in argv
    assert 'web_search="disabled"' in argv and 'apps' in argv and 'remote_plugin' in argv
    assert '--output-schema' in argv and '--output-last-message' in argv
    assert not any('bypass' in value for value in argv)


def test_real_external_process_interface_and_timeout(review_request, tmp_path):
    payload, raw, digest = review_request
    worker = tmp_path/'worker.py'
    expected = tmp_path/'fixture-response.json'
    expected.write_bytes(encoded(answer(payload, digest)))
    worker.write_text('import pathlib,sys\npathlib.Path(sys.argv[2]).write_bytes(pathlib.Path(sys.argv[1]).read_bytes())\n')
    settings = config(arguments=[str(worker), str(expected), '{response}'])
    working = tmp_path/'call'
    response = review.invoke_runtime(settings, raw, digest, working)
    assert review.validate_response(response, payload, digest)
    sleeper = tmp_path/'sleeper.py'
    sleeper.write_text('import time\ntime.sleep(30)\n')
    start = time.monotonic()
    with pytest.raises(ValueError, match='timed out'):
        review.invoke_runtime(config(arguments=[str(sleeper)], max_call_seconds=1), raw, digest, tmp_path/'timeout')
    assert time.monotonic() - start < 15


def test_timeout_kills_reviewer_descendants(review_request, tmp_path):
    payload, raw, digest = review_request
    sentinel = tmp_path/'orphan-sentinel'
    parent = tmp_path/'parent.py'
    child = "import pathlib,time;time.sleep(4);pathlib.Path(" + repr(str(sentinel)) + ").write_text('orphan')"
    parent.write_text("import subprocess,sys,time\ntime.sleep(.2)\nsubprocess.Popen([sys.executable,'-c'," + repr(child) + "])\ntime.sleep(30)\n")
    with pytest.raises(ValueError, match='timed out'):
        review.invoke_runtime(config(arguments=[str(parent)], max_call_seconds=1), raw, digest, tmp_path/'tree')
    time.sleep(4)
    assert not sentinel.exists(), 'A timed-out reviewer must not leave its child running'


def test_new_review_cannot_reuse_different_runtime_binding(fixture, baseline, tmp_path):
    packet, assignment = fixture
    destination = tmp_path/'.local/review'
    review.run_review(packet, assignment, baseline, config(), destination,
                      root=tmp_path, fetch=fetched, invoke=fake_runtime)
    with pytest.raises(ValueError, match='differs'):
        review.run_review(packet, assignment, baseline, config(runtime_id='different'), destination,
                          root=tmp_path, fetch=fetched, invoke=fake_runtime)


@pytest.mark.parametrize('changes', [
    {'enabled': 'yes'}, {'max_calls': 0}, {'max_request_bytes': True},
    {'max_total_seconds': 7201}, {'executable': 'relative.exe'},
    {'arguments': ['{unknown}']}, {'arguments': ['{request.__class__}']},
    {'arguments': ['{']}, {'adapter': 'codex', 'arguments': ['missing.js']},
])
def test_runtime_configuration_rejects_unsafe_or_unbounded_setup(changes):
    assert review.config_errors(config(**changes))


def test_partial_review_gate_requires_decisions_for_all_candidates(fixture, baseline):
    packet, assignment = fixture
    selected = partial.compile_partial(packet, assignment, baseline, review_decisions={})
    assert selected['candidate_units'] == 0 and selected['compiled']['candidate'] == baseline
    with pytest.raises(ValueError, match='non-candidate'):
        partial.compile_partial(packet, assignment, baseline, review_decisions={'unit-'+'a'*20: {'decision': 'accept'}})
