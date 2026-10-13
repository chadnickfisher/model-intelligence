"""Compile retained v2 intake through per-item validation; receipts stay outside public records."""
from pathlib import Path
import argparse,json,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import yaml
from tools import research_two_phase as p
from tools.research_observations import compile_candidate
from tools.research_compile_records import compile_tasks

def canonical_baseline(root,merge_commit):
    root=Path(root)
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head!=merge_commit:raise ValueError('Merge baseline differs')
    paths=('data','models','providers','evidence')
    dirty=subprocess.check_output(['git','-C',str(root),'diff','HEAD','--name-only','--',*paths],text=True)
    untracked=subprocess.check_output(['git','-C',str(root),'ls-files','--others','--exclude-standard','--',*paths],text=True)
    if dirty.strip() or untracked.strip():raise ValueError('Canonical merge inputs have working or staged changes')
    tracked=subprocess.check_output(['git','-C',str(root),'ls-files','--',*paths],text=True).splitlines()
    return {name:p.pin((root/name).read_bytes()) for name in tracked}

def compile_run(directory,root,selectors,*,merge_commit):
    directory=Path(directory);root=Path(root)
    # Application code can be reviewed in a draft checkout, but canonical inputs must be clean.
    baseline=canonical_baseline(root,merge_commit)
    state=p.Run(directory);a=state.get('assignment');b=state.get('bundle');delivery=state.get('analysis')
    if not delivery:raise ValueError('No committed analysis delivery')
    raw=(directory/'incoming'/(delivery['raw']['sha256']+'.json')).read_bytes()
    if p.pin(raw)!=delivery['raw']:raise ValueError('Retained analysis pin differs')
    frame=p.parse(raw)
    prices=yaml.safe_load((root/'data/pricing.yaml').read_bytes())['records']
    result=compile_candidate(a,b,frame,challenge=delivery['challenge'],selectors=selectors,
        merge_root=root,merge_commit=merge_commit,rubric_sha256=p.pin((root/'data/capability-taxonomy.yaml').read_bytes())['sha256'],
        prices=prices,frame_raw=raw)
    if frame['payload']['additional_sources']:
        pending={r['question_id'] for r in frame['payload']['additional_sources']}
        result['task_judgments']=[j for j in result['task_judgments'] if j['question_id'] not in pending]
        result['model_assertions']=[j for j in result['model_assertions'] if j['payload']['question_id'] not in pending]
        for row in result['dispositions']:
            if row['question_id'] in pending:row.update(status='deferred',reason='additional_source_round_incomplete')
        for row in result['question_results']:
            if row['id'] in pending:row['result']='deferred'
    sources=yaml.safe_load((root/'evidence/sources.yaml').read_bytes())['records']
    tasks=yaml.safe_load((root/'data/task-assessments.yaml').read_bytes())['records']
    models={}
    for path in root.glob('models/*/*/profile.yaml'):
        value=yaml.safe_load(path.read_bytes());models[value['id']]=value
    snapshots=[]
    for path in (directory/'durable-capture/sources').glob('*/snapshot.json'):
        value=p.parse(path.read_bytes());value['protocol']=p.VERSION;p.validate(value,'snapshot');snapshots.append(value)
    canonical=compile_tasks(result,models,tasks,sources,snapshots,received_at=delivery['receipt']['received_at'])
    result['canonical_task_dispositions']=canonical['dispositions']
    if canonical_baseline(root,merge_commit)!=baseline:
        raise ValueError('Canonical merge inputs changed during compilation')
    canonical['merge_baseline']=merge_commit
    return result,canonical

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',required=True);parser.add_argument('--merge-root',required=True)
    parser.add_argument('--selectors',required=True);parser.add_argument('--merge-commit',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args();selectors=p.parse(Path(args.selectors).read_bytes())
    result,canonical=compile_run(args.run,args.merge_root,selectors,merge_commit=args.merge_commit)
    destination=Path(args.output);p.immutable(destination/'observations.json',p.encoded(result))
    p.immutable(destination/'canonical-candidate.json',p.encoded(canonical))
    print(json.dumps({'status':'compiled_without_semantic_reviewer','dispositions':result['question_results'],
        'canonical_task_dispositions':canonical['dispositions'],'public_data_applied':False}))

if __name__=='__main__':main()
