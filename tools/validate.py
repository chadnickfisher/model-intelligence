#!/usr/bin/env python3
"""Validate public knowledge records locally. No network or model calls."""
from pathlib import Path
import json, re, sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def read(p):return yaml.safe_load(p.read_text(encoding='utf-8'))
def records(p):return read(ROOT/p)['records']
def run():
 errors=[];collections={}
 files={'model-profile':list(ROOT.glob('models/*/*/profile.yaml')),'provider-profile':list(ROOT.glob('providers/*/profile.yaml'))}
 for typ,paths in files.items():collections[typ]=[(str(p.relative_to(ROOT)),read(p)) for p in paths]
 for typ,path in [('price-record','data/pricing.yaml'),('access-record','data/access.yaml'),('release-record','data/releases.yaml'),('source-record','evidence/sources.yaml')]:collections[typ]=[(path,x) for x in records(path)]
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
 evid={x['id'] for _,x in collections['source-record']}|{x['id'] for x in observations}
 def walk(x,where):
  if isinstance(x,dict):
   for k,v in x.items():
    target=evid if k in ['evidence_ids','source_ids','supporting_evidence_ids','contradictory_evidence_ids'] else priceids if k=='price_ids' else accessids if k=='access_ids' else modelids if k=='model_ids' else None
    if target is not None:
     for ident in v:
      if ident not in target:errors.append(f'{where}: unresolved {k} {ident}')
    if k=='model_id' and v is not None and v not in modelids:errors.append(f'{where}: model_id {v} missing')
    if k=='provider_id' and v is not None and v not in providerids:errors.append(f'{where}: provider_id {v} missing')
    walk(v,where)
  elif isinstance(x,list):
   for v in x:walk(v,where)
 for rows in collections.values():
  for path,row in rows:walk(row,path+' '+row['id'])
 for row in observations:walk(row,'observation '+row['id'])
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
  if not p.is_file() or '.git' in p.parts or p==Path(__file__):continue
  if p.suffix in ['.md','.yaml','.json','.py']:
   text=p.read_text(encoding='utf-8')
   for pat in patterns:
    if re.search(pat,text):errors.append(f'Public-only check flagged {p.relative_to(ROOT)}')
 # Relative links in generated Markdown must resolve; URLs checked during research.
 for p in ROOT.rglob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if '://' in link or link.startswith('#'):continue
   if not (p.parent/link.split('#')[0]).exists():errors.append(f'Broken local link {p.relative_to(ROOT)} -> {link}')
 if errors:
  print('\n'.join(errors));return 1
 counts={k:len(v) for k,v in collections.items()};counts['observations']=len(observations)
 print('PASS: schemas, unique IDs, cross-references, evidence, local links, and public-only scan.');print(json.dumps(counts,indent=2));return 0
if __name__=='__main__':sys.exit(run())
