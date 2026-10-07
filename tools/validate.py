#!/usr/bin/env python3
"""Validate public knowledge records locally. No network or model calls."""
from pathlib import Path
import json, re, sys
from hashlib import sha256
import yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.knowledge import canonical, judgment_index, scope_errors, research_coverage_errors, integrity_errors
from tools.research_runs import task_rubric_errors
from tools.public_boundary import private_work_path, public_files, tracked_work_paths
def read(p):return yaml.load(p.read_text(encoding='utf-8'),Loader=getattr(yaml,'CSafeLoader',yaml.SafeLoader))
def records(p):return read(ROOT/p)['records']
def run():
 errors=['Private working file is tracked: '+path for path in tracked_work_paths(ROOT)];collections={}
 files={'model-profile':sorted(ROOT.glob('models/*/*/profile.yaml')),'provider-profile':sorted(ROOT.glob('providers/*/profile.yaml'))}
 for typ,paths in files.items():collections[typ]=[(p.relative_to(ROOT).as_posix(),read(p)) for p in paths]
 for typ,path in [('price-record','data/pricing.yaml'),('access-record','data/access.yaml'),('release-record','data/releases.yaml'),('source-record','evidence/sources.yaml'),('behavior-record','data/behavior.yaml'),('access-coverage-record','data/access-coverage.yaml'),('benchmark-record','data/benchmarks.yaml'),('research-coverage-record','data/research-coverage.yaml'),('research-contract-record','data/research-contract.yaml'),('task-assessment-record','data/task-assessments.yaml')]:collections[typ]=[(path,x) for x in records(path)]
 for typ,path in [('maintenance-contract-record','data/maintenance-contract.yaml')]:collections[typ]=[(path,x) for x in records(path)]
 for typ,path,key in [('task-record','data/capability-taxonomy.yaml','capabilities'),('alias-record','data/aliases.yaml','records')]:collections[typ]=[(path,x) for x in read(ROOT/path)[key]]
 allids=set()
 for typ,items in collections.items():
  schema=json.loads((ROOT/'schema'/f'{typ}.schema.json').read_text());v=Draft202012Validator(schema,format_checker=FormatChecker())
  for path,row in items:
   rid=row.get('id','missing')
   if rid in allids:errors.append(f'Duplicate ID: {rid}')
   allids.add(rid)
   for e in v.iter_errors(row):errors.append(f'{path} {rid} {list(e.path)}: {e.message}')
 observations=records('evidence/observations.yaml')
 for row in observations:
  if row['id'] in allids:errors.append('Duplicate observation '+row['id'])
  allids.add(row['id'])
 modelids={x['id'] for _,x in collections['model-profile']};providerids={x['id'] for _,x in collections['provider-profile']}
 priceids={x['id'] for _,x in collections['price-record']};accessids={x['id'] for _,x in collections['access-record']}
 errors.extend(research_coverage_errors([r for _,r in collections['research-coverage-record']],modelids,{r['id']:r for _,r in collections['source-record']}))
 evid={x['id'] for _,x in collections['source-record']}|{x['id'] for x in observations}|{'capabilities-2026-10-07'}
 def walk(x,where,historical=False):
  if isinstance(x,dict):
   for k,v in x.items():
    target=(evid) if k in ['evidence_ids','source_ids','supporting_evidence_ids','contradictory_evidence_ids'] else (priceids) if k=='price_ids' else (accessids) if k=='access_ids' else (modelids) if k=='model_ids' else None
    if target is not None:
     for ident in v:
      if ident not in target:errors.append(f'{where}: unresolved {k} {ident}')
    if k=='model_id' and v is not None and v not in (modelids):errors.append(f'{where}: model_id {v} missing')
    if k=='provider_id' and v is not None and v not in (providerids):errors.append(f'{where}: provider_id {v} missing')
    walk(v,where,historical)
  elif isinstance(x,list):
   for v in x:walk(v,where,historical)
 for typ,rows in collections.items():
  if typ not in {'research-run-record','maintenance-pass-record'}:
   for path,row in rows:walk(row,path+' '+row['id'])
 for row in observations:walk(row,'observation '+row['id'])
 prices_by_id={x['id']:x for _,x in collections['price-record']}
 access_by_id={x['id']:x for _,x in collections['access-record']}
 for _,a in collections['access-record']:
  for ident in a['price_ids']:
   p=prices_by_id.get(ident)
   if p and (p['model_id']!=a['model_id'] or p['provider_id']!=a['provider_id']):errors.append(f"{a['id']}: price {ident} does not match exact model/provider route")
 for _,m in collections['model-profile']:
  for ident in m['access_ids']:
   a=access_by_id.get(ident)
   if a and a['model_id']!=m['id']:errors.append(f"{m['id']}: access {ident} belongs to another model")
  for ident in m['price_ids']:
   p=prices_by_id.get(ident)
   if p and p['model_id']!=m['id']:errors.append(f"{m['id']}: price {ident} is not model-specific")
 seen_coverage=set()
 for _,c in collections['access-coverage-record']:
  if c['model_id'] in seen_coverage:errors.append('Duplicate access coverage model '+c['model_id'])
  seen_coverage.add(c['model_id'])
  if c['audit_status']=='reviewed' and (not c['checked_at'] or not c['evidence_ids']):errors.append(c['id']+': reviewed coverage needs dated evidence')
  for kind,category in c['categories'].items():
   if category['state']!='unknown' and not category['evidence_ids']:errors.append(c['id']+': '+kind+' needs evidence')
 for _,b in collections['behavior-record']:
  if not b['supporting_evidence_ids'] and not b['contradictory_evidence_ids']:errors.append(b['id']+': behavior adjudication needs supporting or contradictory evidence')
  if b['fix']['summary'] and not b['fix']['evidence_ids']:errors.append(b['id']+': published fix needs evidence')
 tasks={x['id'] for _,x in collections['task-record']}
 errors.extend(task_rubric_errors([x for _,x in collections['task-record']]))
 judgments_by_model={m['id']:{j['id'] for j in m['capabilities']+m['performance_characteristics']} for _,m in collections['model-profile']}
 for _,b in collections['benchmark-record']:
  for ident in b['judgment_ids']:
   if ident not in judgments_by_model.get(b['model_id'],set()):errors.append(b['id']+': benchmark judgment does not belong to exact model '+ident)
 expected=[]
 for path,m in collections['model-profile']:
  errors.extend(scope_errors(m,tasks))
  expected.extend(judgment_index(m,path))
  for j in m['capabilities']+m['performance_characteristics']:
   if j['id'] in allids:errors.append('Duplicate judgment '+j['id'])
   allids.add(j['id'])
 for _,a in collections['task-assessment-record']:
  if a['model_id'] not in modelids or a['task_id'] not in tasks:errors.append(a['id']+': unresolved model/task')
  exact={j['id']:j for _,m in collections['model-profile'] if m['id']==a['model_id'] for j in m['capabilities']}
  for ident in a['judgment_ids']:
   if ident not in exact or a['task_id'] not in exact[ident]['task_ids']:errors.append(a['id']+': assessment requires an exact direct task judgment')
  if a['result']=='assessed' and (not a['judgment_ids'] or not a['confidence_rationale']):errors.append(a['id']+': assessed task needs judgment and confidence rationale')
 if records('data/capabilities.yaml')!=expected:errors.append('Capability index differs from canonical claims; run render.py')
 current={key:value for key,(_,value) in canonical(ROOT).items()}
 errors.extend(integrity_errors(ROOT))
 for _,m in collections['model-profile']:
  if not m['evidence_ids']:errors.append(f"{m['id']}: no profile provenance")
  for j in m['capabilities']+m['performance_characteristics']:
   if not j['supporting_evidence_ids']:errors.append(f"{m['id']}: judgment has no support")
 for _,p in collections['price-record']:
  if not p['evidence_ids']:errors.append(f"{p['id']}: price has no source")
  if p['status']=='current' and not any(r['amount'] is not None for r in p['rates']):errors.append(f"{p['id']}: current price has no numeric rate; mark unknown")
 # Public-only safety check. Heuristics supplement, not replace, human review.
 patterns=[r'sk-[A-Za-z0-9]{20,}',r'ghp_[A-Za-z0-9]{20,}',r'-----BEGIN .*PRIVATE KEY-----',r'/workspace/(scratch|shared)/']
 for p in public_files(ROOT):
  if not p.is_file() or p==Path(__file__):continue
  if p.suffix in ['.md','.yaml','.json','.py']:
   text=p.read_text(encoding='utf-8')
   for pat in patterns:
    if re.search(pat,text):errors.append(f'Public-only check flagged {p.relative_to(ROOT)}')
 # Relative links in generated Markdown must resolve; URLs checked during research.
 for p in public_files(ROOT):
  if p.suffix!='.md':continue
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
   if '://' in link or link.startswith('#'):continue
   target=p.parent/link.split('#')[0]
   if target.resolve().is_relative_to(ROOT.resolve()) and private_work_path(target.resolve().relative_to(ROOT.resolve()).as_posix()):
    errors.append(f'Public link points to private working material: {p.relative_to(ROOT)}')
   elif not target.exists():errors.append(f'Broken local link {p.relative_to(ROOT)} -> {link}')
 if errors:
  print('\n'.join(errors));return 1
 counts={k:len(v) for k,v in collections.items()};counts['observations']=len(observations)
 print('PASS: schemas, unique IDs, cross-references, evidence, local links, and public-only scan.');print(json.dumps(counts,indent=2));return 0
if __name__=='__main__':sys.exit(run())
