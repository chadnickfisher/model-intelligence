"""Pinned Git baselines for research receipts; no separate full-value journal."""
from functools import lru_cache
from io import BytesIO
import re
import subprocess
import tarfile
import yaml
from tools.knowledge import ROOT

def first_file_commit(path, root=ROOT):
    """Find public provenance by path, without depending on pre-rewrite SHAs."""
    commits = subprocess.check_output(
        ['git', 'log', '--reverse', '--diff-filter=A', '--format=%H', '--', path],
        cwd=root, encoding='utf-8').splitlines()
    if not commits:
        raise ValueError('Public provenance file is absent from this history: ' + path)
    return commits[0]
def git_bytes(commit, path, root=ROOT):
    if not re.fullmatch(r'[a-f0-9]{7,40}', commit):
        raise ValueError('A pinned Git commit is required')
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=root)

@lru_cache(maxsize=32)
def legacy_revisions(root=ROOT, commit=None):
    if commit is None:
        raise ValueError('Legacy work receipts require an explicit private archive commit')
    return yaml.load(git_bytes(commit, 'history/revisions.yaml', root),
                     Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))['records']

@lru_cache(maxsize=32)
def git_state(commit, root=ROOT):
    if not re.fullmatch(r'[a-f0-9]{7,40}', commit):
        raise ValueError('A pinned Git commit is required')
    paths = subprocess.check_output(['git', 'ls-tree', '--name-only', commit,
                'models', 'providers', 'data', 'evidence'], cwd=root, encoding='utf-8').splitlines()
    if not paths:
        return {}
    raw = subprocess.check_output(['git', 'archive', commit, *paths], cwd=root)
    result = {}
    mapping = {'data/pricing.yaml':'price','data/access.yaml':'access','data/releases.yaml':'release',
       'evidence/sources.yaml':'source','evidence/observations.yaml':'observation',
       'data/behavior.yaml':'behavior','data/access-coverage.yaml':'access_coverage',
       'data/benchmarks.yaml':'benchmark','data/research-coverage.yaml':'research_coverage',
       'data/research-contract.yaml':'research_contract','data/research-runs.yaml':'research_run',
       'data/maintenance-contract.yaml':'maintenance_contract','data/maintenance-passes.yaml':'maintenance_pass',
       'data/task-assessments.yaml':'task_assessment','data/aliases.yaml':'alias','data/capability-taxonomy.yaml':'task'}
    with tarfile.open(fileobj=BytesIO(raw)) as archive:
        for item in archive:
            path = item.name
            kind = ('model' if re.fullmatch(r'models/[^/]+/[^/]+/profile.yaml', path) else
                    'provider' if re.fullmatch(r'providers/[^/]+/profile.yaml', path) else mapping.get(path))
            if not kind: continue
            doc = yaml.load(archive.extractfile(item).read(), Loader=getattr(yaml,'CSafeLoader',yaml.SafeLoader))
            rows = [doc] if kind in {'model','provider'} else doc['capabilities' if kind=='task' else 'records']
            result.update({(kind,row['id']):row for row in rows})
    return result

def baseline_for(run, root=ROOT):
    from tools.research_runs import baseline_state
    if run['baseline_revision_id'].startswith('git-'):
        if run['baseline_revision_id'] != 'git-'+run['base_commit']:
            raise ValueError('Git baseline and base commit differ')
        return git_state(run['base_commit'], root), None
    revisions = legacy_revisions(root, run['base_commit'])
    return baseline_state(revisions, run['baseline_revision_id']), revisions

def receipt_states(run, kind, current, root=ROOT):
    baseline, revisions = baseline_for(run, root)
    frozen = run.get('evidence_commit')
    if frozen:
        state = git_state(frozen, root)
        retained = state.get((kind,run['id']))
        expected = {k:v for k,v in run.items() if k!='evidence_commit'}
        if not retained or {k:v for k,v in retained.items() if k!='evidence_commit'} != expected:
            raise ValueError('Frozen Git receipt differs from current receipt')
        if not run['baseline_revision_id'].startswith('git-'):
            # Several old research passes could precede one Git commit. Their
            # exact evidence boundary lives only in that already committed blob.
            from tools.research_runs import baseline_state
            journal = legacy_revisions(root, frozen)
            captured = [r for r in journal if r['entity_type'] == kind and
                        r['entity_id'] == run['id'] and r['value'] == expected]
            if not captured:
                raise ValueError('Original receipt boundary missing from pinned Git object')
            state = baseline_state(journal, captured[-1]['id'])
        return baseline, state, revisions
    # An unchanged committed receipt validates against that commit's evidence.
    candidates = subprocess.check_output(['git','log','--format=%H','--',
                  'data/research-runs.yaml' if kind=='research_run' else 'data/maintenance-passes.yaml'],
                  cwd=root, encoding='utf-8').splitlines()
    for commit in reversed(candidates):
        state = git_state(commit,root)
        if state.get((kind,run['id'])) == run:
            return receipt_states({**run, 'evidence_commit': commit}, kind, current, root)
    return baseline,current,revisions
