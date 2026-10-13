"""Materialize compiled canonical data in an isolated checkout and run normal checks.

This helper does not publish, dispatch research, schedule work or invoke models.
"""
from pathlib import Path
import json, subprocess, sys
from tools.knowledge import capture, read
from tools.migrate_v2 import write_yaml
from tools.research_observations import privacy

def preserve_key_order(reference,value):
    """Keep existing YAML key order after a canonically sorted JSON handoff.

    Only mapping presentation changes; scalar values and list order stay intact.
    """
    if isinstance(value,dict):
        prior=reference if isinstance(reference,dict) else {}
        keys=[key for key in prior if key in value]+[key for key in value if key not in prior]
        return {key:preserve_key_order(prior.get(key),value[key]) for key in keys}
    if isinstance(value,list):
        prior=reference if isinstance(reference,list) else []
        by_id={item['id']:item for item in prior if isinstance(item,dict) and 'id' in item}
        return [preserve_key_order(by_id.get(item.get('id'),prior[index] if index<len(prior) else None)
            if isinstance(item,dict) else prior[index] if index<len(prior) else None,item)
            for index,item in enumerate(value)]
    return value

def stage(root,compiled,*,observed_at,summary,allow_synthetic=False):
    root=Path(root).resolve()
    here=Path(__file__).resolve().parents[1]
    if root!=here:raise ValueError('Run staging helper from its isolated implementation checkout')
    expected={p['id'] for p in compiled['assessments']}
    if len(expected)!=len(compiled['assessments']):raise ValueError('Duplicate compiled assessment ID')
    old_tasks=read(root/'data/task-assessments.yaml');old_sources=read(root/'evidence/sources.yaml')
    planned={}; evidence=set()
    if old_tasks['records']!=compiled['assessments']:planned['data/task-assessments.yaml']={**old_tasks,'records':compiled['assessments']}
    if old_sources['records']!=compiled['sources']:planned['evidence/sources.yaml']={**old_sources,'records':compiled['sources']}
    for path in sorted(root.glob('models/*/*/profile.yaml')):
        old=read(path);new=compiled['models'].get(old['id'])
        if new and old!=new:planned[path.relative_to(root).as_posix()]=new
    if not planned:return {'status':'no_change','paths':[],'history_changes':0}
    dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain','--untracked-files=all'],text=True)
    if dirty.strip():raise ValueError('Canonical staging requires a clean isolated checkout')
    if compiled.get('merge_baseline'):
        head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
        if head!=compiled['merge_baseline']:raise ValueError('Canonical staging baseline differs')
    for task in compiled['assessments']:
        if task['id'] in compiled['changed_task_ids']:evidence.update(task['evidence_ids'])
    if not evidence:raise ValueError('Changed canonical records require saved source references')
    privacy(planned)
    # Only allow the explicit compiled canonical paths; receipts and source workspace files stay external.
    for name,value in planned.items():write_yaml(root/name,preserve_key_order(read(root/name),value))
    changes=capture(root,observed_at,summary,sorted(evidence))
    logs=[]
    for script in ('tools/render.py','tools/validate.py'):
        result=subprocess.run([sys.executable,str(root/script)],cwd=root,capture_output=True,text=True,
            encoding='utf-8',errors='replace',timeout=60)
        logs.append({'script':script,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        if result.returncode:raise ValueError('Canonical candidate check failed: '+script+'\n'+result.stdout[-3000:]+result.stderr[-1000:])
    diff=subprocess.check_output(['git','-C',str(root),'diff','--stat'],text=True,encoding='utf-8')
    return {'status':'canonical_candidate_validated','paths':sorted(planned),'history_changes':len(changes),
        'checks':logs,'diff_stat':diff,'public_data_published':False}
