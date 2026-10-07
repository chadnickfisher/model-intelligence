#!/usr/bin/env python3
"""Build navigation and Markdown from canonical YAML. No network/model calls."""
from pathlib import Path
import json,os,sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.knowledge import scope_errors
import yaml
R=Path(__file__).resolve().parents[1]
def rd(p):return yaml.load(p.read_text(encoding='utf-8'),Loader=getattr(yaml,'CSafeLoader',yaml.SafeLoader))
def wr(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,d):wr(p,yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=105))
def val(x):
 if x is None:return 'Unknown / not established'
 if isinstance(x,bool):return 'Yes' if x else 'No'
 if isinstance(x,list):return '; '.join(val(y) for y in x) if x else 'Not established in this pass'
 if isinstance(x,dict):return '; '.join(k.replace('_',' ')+': '+val(v) for k,v in x.items())
 return str(x)
def esc(x):return val(x).replace('|','\\|').replace('\n',' ')
S={s['id']:s for s in rd(R/'evidence/sources.yaml')['records']}
O={s['id']:s for s in rd(R/'evidence/observations.yaml')['records']}
def source_links(ids):
 out=[]
 for i in ids:
  if i in S:out.append(f"[{S[i].get('title') or S[i]['url'].split('/')[2]}]({S[i]['url']})")
  elif i in O:out+=source_links(O[i]['source_ids']).split(' · ')
 return ' · '.join(dict.fromkeys(out)) or 'No source established'
PR={x['id']:x for x in rd(R/'data/pricing.yaml')['records']}
AC={x['id']:x for x in rd(R/'data/access.yaml')['records']}
def rates(p):return '; '.join(r['metric']+': '+('unknown' if r['amount'] is None else str(r['amount']))+' '+str(r['currency'] or '')+' / '+r['unit'] for r in p['rates'])
tasks={x['id'] for x in rd(R/'data/capability-taxonomy.yaml')['capabilities']}
for p in R.glob('models/*/*/profile.yaml'):
 errors=scope_errors(rd(p),tasks)
 if errors:raise ValueError('\n'.join(errors))
models=[];providers=[];caps=[]
for p in sorted(R.glob('models/*/*/profile.yaml')):
 m=rd(p);ii=m['identity'];models.append({'id':m['id'],'name':ii['name'],'creator':ii['creator'],'family':ii['family'],'status':ii['status'],'local':m['local_inference']['availability'],'profile':p.relative_to(R).as_posix(),'readme':p.with_name('README.md').relative_to(R).as_posix()})
 lines=[f"# {ii['name']}",'',f"**Creator:** {ii['creator']} · **Family:** {ii['family']} · **Status:** {ii['status']}",f"**Verified:** {m['verified_at']} · **Release:** {ii['release_date'] or 'Unknown'}",'', '[Canonical data](profile.yaml) · [Methodology](../../../methodology.md) · [Catalog](../../../data/models.md)','', '## Task judgments','']
 for j in m['capabilities']+m['performance_characteristics']:
  if j['scope']!='performance':caps.append({'model_id':m['id'],'profile':p.relative_to(R).as_posix(),**j})
  lines += [f"### {j['provenance']['original_task'].replace('-',' ').capitalize()} ({j['confidence']} confidence)",'',j['judgment'],'','Scope: '+j['scope']+' / '+j['assessment']+'. '+j['scope_note'],'','Direct task IDs: '+val(j['task_ids']),'','Related task IDs (navigation only): '+val(j['related_task_ids']),'','Judgment ID: '+j['id'],'','Conditions: '+val(j['conditions']),'','Failure modes / limitations: '+val(j['known_failure_modes']),'','Supporting sources: '+source_links(j['supporting_evidence_ids']),'','Contradictory or limiting sources: '+(source_links(j['contradictory_evidence_ids']) if j['contradictory_evidence_ids'] else 'None separately identified in this pass; this is not evidence of consensus.'),'']
  if j['evidence_notes']:lines+=['Evidence notes: '+val(j['evidence_notes']),'']
 lines+=['## Specifications','', '| Field | Recorded value |','|---|---|']
 for k,v in m['specifications'].items():lines.append('| '+k.replace('_',' ')+' | '+esc(v['value'])+' |')
 lines+=['','Specifications and provenance are qualified in [canonical data](profile.yaml). Published limits do not guarantee effective retrieval or local memory feasibility.','','## Access and cost','',f"{len(m['access_ids'])} recorded access route(s); {len(m['price_ids'])} model-specific price record(s).",'', '[Access records](../../../data/access.yaml) · [Price records](../../../data/pricing.yaml)','', 'Provider routes and subscriptions are separate. Read billing units, thresholds, regions, status, and verification dates.','','## Licensing and local use','',f"License: {m['licensing']['name'] or 'Not established / proprietary terms must be checked'}",'', 'Restrictions: '+val(m['licensing']['restrictions']),'','Commercial use: '+val(m['licensing']['commercial_use']),'','Redistribution: '+val(m['licensing']['redistribution']),'','Hosted service: '+val(m['licensing']['hosted_service']),'', 'Local weights/runtime availability: '+m['local_inference']['availability'],'', 'Hardware: '+val(m['local_inference']['hardware_notes']),'', 'Local conditions: '+val(m['local_inference']['conditions']),'','## Gaps and caveats','']
 lines+=['- '+s for s in m['limitations']+m['notes']]
 lines+=['','## Recorded price offers','', '| Provider | Tier / status | Rates | Conditions | Verified |','|---|---|---|---|---|']
 for ident in m['price_ids']:
  q=PR[ident];lines.append('| '+esc(q['provider_id'])+' | '+esc(str(q['tier'])+' / '+q['status'])+' | '+esc(rates(q))+' | '+esc(q['conditions'])+' | '+q['verified_at']+' |')
 lines+=['','## Recorded access routes','']
 for ident in m['access_ids']:
  a=AC[ident];lines+=['- '+esc(a['provider_id'] or 'Local / self-hosted')+' / '+esc(a['product'] or a['methods'])+': '+esc(a['status'])+'. '+esc(a['restrictions'])]
 lines+=['','## Sources','',source_links(m['evidence_ids']),'']
 wr(p.with_name('README.md'),'\n'.join(lines))
for p in sorted(R.glob('providers/*/profile.yaml')):
 d=rd(p);providers.append({'id':d['id'],'name':d['name'],'roles':d['roles'],'profile':p.relative_to(R).as_posix(),'readme':p.with_name('README.md').relative_to(R).as_posix()})
 lines=['# '+d['name'],'', 'Roles: '+', '.join(d['roles']),f"Verified: {d['verified_at']}",'','[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)','']
 for k in ['access_methods','api_compatibility','geographic_availability','rate_limits','caching_batching','privacy_data_use','notes','limitations']:
  lines+=['## '+k.replace('_',' ').capitalize(),'']+['- '+x for x in (d[k] or ['Not established in this baseline.'])]+['']
 lines+=['## Offers','',f"{len(d['model_ids'])} linked model(s), {len(d['access_ids'])} access route(s), {len(d['price_ids'])} price record(s).",'','[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)','','## Sources','',source_links(d['evidence_ids']),'']
 wr(p.with_name('README.md'),'\n'.join(lines))
dump(R/'data/models.yaml',{'schema_version':'1.0','generated':True,'records':models});dump(R/'data/providers.yaml',{'schema_version':'1.0','generated':True,'records':providers});dump(R/'data/capabilities.yaml',{'schema_version':'2.0','generated':True,'records':caps})
for name,rows in [('models',models),('providers',providers)]:
 title=name.capitalize();lines=['# '+title,'','Generated navigation. Read canonical profiles for evidence, conditions, and dated verification.','', '| Name | '+('Creator | Status | Local weights' if name=='models' else 'Roles')+' |','|---|'+('---|---|---|' if name=='models' else '---|')]
 for d in rows:
  path='../'+d['readme'];lines.append('| ['+esc(d['name'])+']('+path+') | '+(' | '.join(esc(d[k]) for k in ['creator','status','local']) if name=='models' else esc(d['roles']))+' |')
 wr(R/f'data/{name}.md','\n'.join(lines)+'\n')
counts={'models':len(models),'providers_and_access_products':len(providers),'capability_judgments':len(caps),'performance_judgments':sum(len(rd(p)['performance_characteristics']) for p in R.glob('models/*/*/profile.yaml')),'price_records':len(rd(R/'data/pricing.yaml')['records']),'access_routes':len(rd(R/'data/access.yaml')['records']),'public_sources':len(S),'evidence_observations':len(O)}
dump(R/'data/coverage.yaml',{'schema_version':'1.0','generated':True,'as_of':'2026-10-06','counts':counts})
coverage=R/'research/coverage.md';t=coverage.read_text();start=t.find('\n## Baseline inventory')
if start>=0:t=t[:start]
t+='\n## Baseline inventory\n\n'+ '\n'.join('- '+k.replace('_',' ')+': '+str(v) for k,v in counts.items())+'\n\nSee [coverage gaps](coverage-gaps.yaml) for source-specific limitations and [contradictions](../evidence/contradictions.yaml) for unresolved differences. Counts indicate coverage, not quality or completeness.\n'
wr(coverage,t);print(json.dumps(counts,indent=2))

for name,rows in [('pricing',list(PR.values())),('access',list(AC.values()))]:
 lines=['# '+name.capitalize(),'','Generated from canonical YAML. Units, route conditions and dates are essential.','']
 if name=='pricing':
  lines+=['| Model / product | Provider | Method / tier / status | Rates | Verified |','|---|---|---|---|---|']
  for q in rows:lines.append('| '+esc(q['model_id'] or q['model_label'] or q['product'])+' | '+esc(q['provider_id'])+' | '+esc(q['billing_method']+' / '+str(q['tier'])+' / '+q['status'])+' | '+esc(rates(q))+' | '+q['verified_at']+' |')
 else:
  lines+=['| Model / product | Provider | Methods | Availability and restrictions |','|---|---|---|---|']
  for a in rows:lines.append('| '+esc(a['model_id'] or a['product'])+' | '+esc(a['provider_id'])+' | '+esc(a['methods'])+' | '+esc(a['status'])+'; '+esc(a['restrictions'])+' |')
 lines+=['','[Canonical records with evidence and all conditions]('+name+'.yaml)']
 wr(R/('data/'+name+'.md'),'\n'.join(lines)+'\n')
