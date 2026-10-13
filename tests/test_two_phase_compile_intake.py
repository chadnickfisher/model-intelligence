from pathlib import Path
from copy import deepcopy
from tools import research_two_phase as p
from tools.research_context import supply
from tools.two_phase_compile import compile_run
from test_two_phase_transport import assignment,frame

ROOT=Path(__file__).resolve().parents[1]

def test_merge_guard_rejects_staged_and_untracked_canonical_inputs(tmp_path):
    import subprocess
    import pytest
    from tools.two_phase_compile import canonical_baseline
    def git(*args):return subprocess.check_output(['git','-C',str(tmp_path),*args],text=True).strip()
    git('init','--quiet');git('config','user.name','Test');git('config','user.email','test@example.com')
    (tmp_path/'data').mkdir();path=tmp_path/'data/example.yaml';path.write_text('value: original\n')
    git('add','data/example.yaml');git('commit','--quiet','-m','Fixture baseline');head=git('rev-parse','HEAD')
    baseline=canonical_baseline(tmp_path,head)
    path.write_text('value: changed\n');git('add','data/example.yaml')
    with pytest.raises(ValueError,match='staged changes'):canonical_baseline(tmp_path,head)
    git('restore','--staged','data/example.yaml');path.write_text('value: original\n')
    extra=tmp_path/'data/untracked.yaml';extra.write_text('value: extra\n')
    with pytest.raises(ValueError,match='staged changes'):canonical_baseline(tmp_path,head)
    extra.unlink();assert canonical_baseline(tmp_path,head)==baseline

def test_committed_intake_compiles_independent_observation_and_defers_bad_item(tmp_path):
    a=assignment();a['subject']={'model_id':'claude-sonnet-5-5','provider_id':'anthropic',
        'access_id':'access-proprietary-access-18','tier':'Standard','routing':'global'}
    a['questions']=[{'id':'price-question','kind':'factual','field_ids':['pricing.cache_read'],'task_ids':[],
        'text':'Controlled missing-price result'}]
    a['context_read_set'],selectors=supply(ROOT,{'price-question':[{'path':'data/models.yaml','id':'claude-sonnet-5-5'}]})
    a['rubric_sha256']=p.pin((ROOT/'data/capability-taxonomy.yaml').read_bytes())['sha256']
    a['scope_sha256']=p.pin(p.encoded(p.scope(a)))['sha256'];state=p.Run(tmp_path);state.issue(a)
    d={'protocol':p.VERSION,'kind':'discovery','status':'unknown','sources':[],'gaps':['Controlled fixture']}
    raw=p.encoded(frame(a,d,p.pin(p.encoded(a))))
    state.receive(raw,'discovery',p.pin(p.encoded(a)),'c'*32,now='2026-10-13T12:01:00+00:00')
    b={'protocol':p.VERSION,'kind':'bundle','assignment_id':a['assignment_id'],'revision':1,
        'parent_discovery':p.pin(raw),'subject':a['subject'],'questions':a['questions'],
        'sources':[],'facts':[],'failures':['No usable price source in controlled fixture'],'outside_scope':'not_checked'}
    state.evidence_ready(b)
    finding={'question_id':'price-question','conclusion':'Price remains unknown in this controlled fixture.',
        'source_ids':[],'contrary_source_ids':[],'passages':[],'conditions':[],'unknowns':['Price unknown'],
        'limitations':['No saved usable source'],'confidence':{'level':'unknown','rationale':'No source'},
        'basis':{'kind':'unknown','rationale':'No source'}}
    payload={'protocol':p.VERSION,'kind':'analysis','status':'partial','findings':[finding,{'malformed':'Fixture'}],
        'judgments':[],'inspected_source_ids':['reported-but-unknown-source'],'inspection_reported_at':None,'gaps':['Missing source'],'additional_sources':[]}
    delivered=p.encoded(frame(a,payload,p.pin(p.encoded(b))))
    state.receive(delivered,'analysis',p.pin(p.encoded(b)),'c'*32,now='2026-10-13T12:02:00+00:00')
    import subprocess
    head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
    result,canonical=compile_run(tmp_path,ROOT,selectors,merge_commit=head)
    assert result['analysis']==p.pin(delivered) and len(result['model_assertions'])==1
    assert len([r for r in result['dispositions'] if r['status']=='deferred'])==1
    assert result['question_results'][0]['remaining_field_ids']==['pricing.cache_read']
    assert result['unresolved_inspection_report_ids']==['reported-but-unknown-source']
    assert not canonical['changed_task_ids']
