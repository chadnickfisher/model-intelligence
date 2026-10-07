#!/usr/bin/env python3
"""Validate public knowledge records locally. No network or model calls."""
from pathlib import Path
import json, re, sys
from hashlib import sha256
import yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.knowledge import canonical, history, judgment_index, scope_errors, snapshot
def read(p):return yaml.load(p.read_text(encoding='utf-8'),Loader=getattr(yaml,'CSafeLoader',yaml.SafeLoader))
def records(p):return read(ROOT/p)['records']
def run():
 errors=[];collections={}
 files={'model-profile':sorted(ROOT.glob('models/*/*/profile.yaml')),'provider-profile':sorted(ROOT.glob('providers/*/profile.yaml'))}
 for typ,paths in files.items():collections[typ]=[(p.relative_to(ROOT).as_posix(),read(p)) for p in paths]
 for typ,path in [('price-record','data/pricing.yaml'),('access-record','data/access.yaml'),('release-record','data/releases.yaml'),('source-record','evidence/sources.yaml')]:collections[typ]=[(path,x) for x in records(path)]
 for typ,path,key in [('task-record','data/capability-taxonomy.yaml','capabilities'),('alias-record','data/aliases.yaml','records'),('history-record','history/revisions.yaml','records')]:collections[typ]=[(path,x) for x in read(ROOT/path)[key]]
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
 evid={x['id'] for _,x in collections['source-record']}|{x['id'] for x in observations}|{'capabilities-2026-10-07'}
 historic_targets={kind:{r['entity_id'] for _,r in collections['history-record'] if r['entity_type']==kind} for kind in ['model','provider','price','access','source','observation']}
 historic_evid=evid|historic_targets['source']|historic_targets['observation']
 def walk(x,where,historical=False):
  if isinstance(x,dict):
   for k,v in x.items():
    target=(historic_evid if historical else evid) if k in ['evidence_ids','source_ids','supporting_evidence_ids','contradictory_evidence_ids'] else (historic_targets['price'] if historical else priceids) if k=='price_ids' else (historic_targets['access'] if historical else accessids) if k=='access_ids' else (historic_targets['model'] if historical else modelids) if k=='model_ids' else None
    if target is not None:
     for ident in v:
      if ident not in target:errors.append(f'{where}: unresolved {k} {ident}')
    if k=='model_id' and v is not None and v not in (historic_targets['model'] if historical else modelids):errors.append(f'{where}: model_id {v} missing')
    if k=='provider_id' and v is not None and v not in (historic_targets['provider'] if historical else providerids):errors.append(f'{where}: provider_id {v} missing')
    walk(v,where,historical)
  elif isinstance(x,list):
   for v in x:walk(v,where,historical)
 for typ,rows in collections.items():
  for path,row in rows:walk(row,path+' '+row['id'],typ=='history-record')
 for row in observations:walk(row,'observation '+row['id'])
 tasks={x['id'] for _,x in collections['task-record']}
 expected=[]
 for path,m in collections['model-profile']:
  errors.extend(scope_errors(m,tasks))
  expected.extend(judgment_index(m,path))
  for j in m['capabilities']+m['performance_characteristics']:
   if j['id'] in allids:errors.append('Duplicate judgment '+j['id'])
   allids.add(j['id'])
 if records('data/capabilities.yaml')!=expected:errors.append('Capability index differs from canonical claims; run render.py')
 archive=read(ROOT/'history/migrations/2026-10-07-capabilities.yaml')
 if len(archive['records'])!=71:errors.append('Migration must preserve 64 capabilities and 7 existing performance observations')
 preserved={x['judgment_id']:x for x in archive['records']}
 if len(preserved)!=len(archive['records']):errors.append('Duplicate migration original')
 revisions=history(ROOT);latest={};last_date='0001-01-01'
 for r in revisions:
  key=(r['entity_type'],r['entity_id']);prior=latest.get(key)
  digest=sha256(json.dumps({k:v for k,v in r.items() if k!='id'},sort_keys=True).encode()).hexdigest()[:20]
  if r['id']!='revision-'+digest:errors.append('History content hash mismatch '+r['id'])
  if r['observed_at']<last_date:errors.append('History observations are not ordered')
  last_date=r['observed_at']
  if r['previous_revision_id']!=(prior['id'] if prior else None):errors.append('Broken revision chain '+r['id'])
  if (r['operation']=='baseline')!=(prior is None):errors.append('Incorrect baseline/update operation '+r['id'])
  if (r['operation']=='remove')!=(r['value'] is None):errors.append('Invalid removal value '+r['id'])
  latest[key]=r
  type_schema={'model':'model-profile','provider':'provider-profile','price':'price-record','access':'access-record','release':'release-record','source':'source-record','task':'task-record','alias':'alias-record'}.get(r['entity_type'])
  if type_schema and r['value'] is not None:
   validator=Draft202012Validator(json.loads((ROOT/'schema'/f'{type_schema}.schema.json').read_text()),format_checker=FormatChecker())
   for e in validator.iter_errors(r['value']):errors.append(f"Historical payload {r['id']}: {e.message}")
  if r['operation']=='baseline' and r['entity_type']=='model':
   for j in r['value']['capabilities']+r['value']['performance_characteristics']:
    if j['id'] in preserved:
     original=preserved.pop(j['id'])
     for field,value in original['original'].items():
      actual=j['provenance']['original_task'] if field=='task' else j[field]
      if actual!=value:errors.append('Original evidence/conclusion lost: '+j['id']+' '+field)
     if j['scope']!=original['classification']:errors.append('Original mapping scope differs '+j['id'])
 if preserved:errors.append('Migration originals missing from baseline history')
 current={key:value for key,(_,value) in canonical(ROOT).items()}
 if snapshot(last_date,revisions)!=current:errors.append('History/current mismatch; capture canonical changes before publishing')
 for _,m in collections['model-profile']:
  if not m['evidence_ids']:errors.append(f"{m['id']}: no profile provenance")
  for j in m['capabilities']+m['performance_characteristics']:
   if not j['supporting_evidence_ids']:errors.append(f"{m['id']}: judgment has no support")
 for _,p in collections['price-record']:
  if not p['evidence_ids']:errors.append(f"{p['id']}: price has no source")
  if p['status']=='current' and not any(r['amount'] is not None for r in p['rates']):errors.append(f"{p['id']}: current price has no numeric rate; mark unknown")
 # Public-only safety check. Heuristics supplement, not replace, human review.
 patterns=[r'sk-[A-Za-z0-9]{20,}',r'ghp_[A-Za-z0-9]{20,}',r'-----BEGIN .*PRIVATE KEY-----',r'/workspace/(scratch|shared)/']
 for p in ROOT.rglob('*'):
  if not p.is_file() or any(x in p.parts for x in ['.git','.venv','__pycache__','.pytest_cache']) or p==Path(__file__):continue
  if p.suffix in ['.md','.yaml','.json','.py']:
   text=p.read_text(encoding='utf-8')
   for pat in patterns:
    if re.search(pat,text):errors.append(f'Public-only check flagged {p.relative_to(ROOT)}')
 # Relative links in generated Markdown must resolve; URLs checked during research.
 for p in ROOT.rglob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
   if '://' in link or link.startswith('#'):continue
   if not (p.parent/link.split('#')[0]).exists():errors.append(f'Broken local link {p.relative_to(ROOT)} -> {link}')
 if errors:
  print('\n'.join(errors));return 1
 counts={k:len(v) for k,v in collections.items()};counts['observations']=len(observations)
 print('PASS: schemas, unique IDs, cross-references, evidence, local links, and public-only scan.');print(json.dumps(counts,indent=2));return 0
if __name__=='__main__':sys.exit(run())
