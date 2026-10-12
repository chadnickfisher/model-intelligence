"""Portable schema-derived output requirements and proposal shape validation."""
from copy import deepcopy
from datetime import date
from hashlib import sha256
import json

if __package__:
    from .research_authoring import ACCOUNTING_CHECKS
else:
    from research_authoring import ACCOUNTING_CHECKS

FORMAT = 'research-output-contract-v1'
SCHEMAS = {'model':'model-profile','provider':'provider-profile','source':'source-record',
           'access':'access-record','price':'price-record','benchmark':'benchmark-record',
           'behavior':'behavior-record','release':'release-record',
           'task_assessment':'task-assessment-record','research_coverage':'research-coverage-record'}
PREFIXES = {'source':('src',12),'access':('access',16),'price':('price',16),
            'benchmark':('benchmark',16),'behavior':('behavior',16),'release':('release',16),
            'task_assessment':('task-assessment',16),'research_coverage':('research-coverage',16)}
CHECKS = {
    'RC01':'Use the pinned output-contract.json generated from the same schemas.json used by the validator.',
    'RC02':'Set each changes[] kind to a supported record type and place its complete proposed record under record.',
    'RC03':'Save every required record key, including nullable keys, and satisfy its exact type, branch and value constraints.',
    'RC04':'Store performance findings in performance_characteristics with scope performance and both task-ID arrays empty; keep capabilities separate.',
}
EVIDENCE_CHECKS = {
    'EV01':'Use each date only for its established event: publication, measurement, inspection, assessment or effectiveness. Save the source label and evidence ID in the change rationale; keep unsupported nullable dates null. Evidence review checks source_dates and claim_support; date shape/order checks alone do not establish meaning.',
    'EV02':'Identify each evaluator by name, type and role in benchmark conditions/evidence_notes and dependent judgment notes. Distinguish LLM judges, typed classifiers, rule-based graders and human raters. Evidence review checks setup, claim_support and confidence.',
    'EV03':'Resolve the exact result row before general methodology: save disclosed benchmark provider_id, route, region, checkpoint, effort and harness in their permitted fields and conditions. Carry the same route into dependent judgments and accounting. Evidence review checks identity, setup and claim_support.',
    'EV04':'Bind each offer condition to its exact model, provider, product, endpoint, region, tier and billing method. Save only applicable restrictions in price/access conditions; do not copy sibling endpoint rules. Evidence review checks identity, setup and claim_support.',
}
EVIDENCE_RULES = {
    'EV01':{'review_checks':['source_dates','claim_support'],
            'record_paths':{'source':['/published_at','/accessed_at'],
                'benchmark':['/measured_at','/observed_at','/evidence_notes'],
                'task_assessment':['/checked_at','/aggregate/assessed_at'],
                'price':['/effective_from','/effective_to','/verified_at'],
                'access':['/verified_at'], 'release':['/event_date','/verified_at'],
                'behavior':['/reported_at','/observed_at','/effective_from','/fix/published_at']},
            'save':['changes[].rationale: date kind, actual source label and evidence ID.',
                    'Existing record date field: only its matching event; nullable unsupported date stays null.',
                    'Receiver review citations: exact retained-source quote, offsets and body/text hashes.'],
            'unknown':'A measurement or last-updated label cannot supply publication; inspection cannot supply a run or effective date.'},
    'EV02':{'review_checks':['setup','claim_support','confidence'],
            'record_paths':{'benchmark':['/conditions','/limitations','/evidence_notes'],
                'model':['/capabilities/*/conditions','/capabilities/*/evidence_notes'],
                'source':['/claim_scope','/limitations']},
            'save':['benchmark conditions/evidence_notes: one entry per disclosed judge, with name, type and scoring role.',
                    'limitations: private rubric, same-family judge dependence and missing evaluator details.',
                    'Dependent model notes and accounting: the same verified evaluator description.'],
            'unknown':'Do not infer judge type from a product name or describe a mixed panel as all LLM or all human.'},
    'EV03':{'review_checks':['identity','setup','claim_support'],
            'record_paths':{'benchmark':['/provider_id','/model_version','/effort','/harness','/conditions','/limitations'],
                'model':['/capabilities/*/conditions','/capabilities/*/evidence_notes'],
                'source':['/claim_scope','/limitations']},
            'save':['benchmark provider_id: resolved stable provider ID when the exact row discloses it; otherwise null.',
                    'conditions: disclosed serving route, region and configuration; keep undisclosed endpoint/revision details explicit.',
                    'Dependent judgment conditions and RUN field/task rows: consistent provider-qualified scope.'],
            'unknown':'General provider alternatives do not override the exact row, and a disclosed provider does not establish an undisclosed API or checkpoint.'},
    'EV04':{'review_checks':['identity','setup','claim_support'],
            'record_paths':{'price':['/model_id','/provider_id','/model_label','/product','/region','/tier','/billing_method','/conditions','/rates'],
                'access':['/model_id','/provider_id','/model_label','/product','/conditions','/restrictions']},
            'save':['Resolve the complete offer identity before writing rates, conditions or restrictions.',
                    'conditions/rate conditions: source-supported endpoint-specific rules and thresholds only.',
                    'changes[].rationale and RUN.field_checks[]: identify the exact offer and the inspected source section.'],
            'unknown':'Keep an unresolved endpoint restriction as a gap; do not fill it from another product, subscription or service tier.'},
}
JSON_AUTHORING_FLOW = [
    {'step':1,'action':'Read the pinned assignment, baseline, worklist, schemas and output contract; preserve stable identities and hashes.','outputs':['RUN target/bounds/checklist rows','changes[].previous_hash']},
    {'step':2,'action':'Capture each actual search response and each opened-source tool return before reasoning from the original body. Save all page chunks for source-body validation; distinguish current evidence from retained history.','outputs':['Search receipt index/responses','Opened-source index/responses','RUN.*.evidence_ids','RUN.*.search_references']},
    {'step':3,'action':'Apply EV01-EV04 to date meanings, evaluator types, exact result routes and offer-specific conditions before authoring facts.','outputs':['Permitted record fields listed in evidence_review.rules','changes[].rationale']},
    {'step':4,'action':'Write complete changes[].record objects using the pinned schema; preserve nulls, conditions, limitations, contradictions and stable judgment IDs. Do not add invented date-kind, judge or route keys.','outputs':['changes[].kind','changes[].record','changes[].evidence_ids','changes[].checked_paths']},
    {'step':5,'action':'Synchronize affected field checks, task decisions, source scopes and resolutions; credit only actual inspected fields. Leave unrelated pending/blocked/unknown accounting unchanged.','outputs':['RUN.field_checks[]','RUN.task_decisions[]','RUN.source_checks[]','resolutions[] when present']},
    {'step':6,'action':'Save the actual serialization timestamp, audit searches and opened-source captures, then run the frozen authoring helper; retain its diagnostics and numbered receipt.','outputs':['created_at','Search audit','Source-body audit','Structural validation receipt']},
    {'step':7,'action':'Receiver evidence review applies EV01-EV04 through its listed checks and exact retained-source citations. Structural success does not mark these checks passed; failed or unknown checks defer the affected change.','outputs':['Private review decisions[].checks','Private review decisions[].citations','Private review decisions[].followup']},
    {'step':8,'action':'Freeze exact bytes and deliver the required artifacts with the delivery manifest last; keep evidence review, completeness, acceptance and publication statuses separate.','outputs':['Immutable delivered revision','Delivery manifest']},
]


def evidence_review_contract():
    return {'checks':deepcopy(EVIDENCE_CHECKS),'rules':deepcopy(EVIDENCE_RULES),
            'enforcement':'Receiver retained-source evidence review; not portable schema/mechanical attestation.',
            'response_fields':['decisions[].checks','decisions[].citations','decisions[].rationale','decisions[].followup'],
            'limits':'The structural helper checks fields, accounting and receipt bindings. Semantic acceptance requires actual source inspection and a validated review decision.'}


def authoring_directions():
    if __package__:
        from .research_source_bodies import contract as source_contract
    else:
        from research_source_bodies import contract as source_contract
    return {'json_authoring_flow':deepcopy(JSON_AUTHORING_FLOW),'evidence_review':evidence_review_contract(),
            'source_bodies':source_contract()}

METHODS = {
    'model':['Resolve the exact creator, model and checkpoint from official evidence.',
             'Inspect specifications, licensing and local-inference claims using primary sources.',
             'Apply the task rubric to attributable capability evidence; retain conditions, contradictions and confidence rationale.',
             'Retain stable judgment scope and IDs; new research provenance uses the supplied public batch identifier.',
             'Store cross-cutting performance findings in performance_characteristics with scope performance, task_ids [] and related_task_ids []; retain workload context in scope_note and conditions.'],
    'provider':['Resolve provider, access product and client boundaries.',
                'Inspect official eligibility, policies, limits, pricing and privacy rules.',
                'Keep attributable reliability observations separate from model capability claims.'],
    'source':['Open the original public source body and save the exact tool return/all page chunks under the pinned source-body contract; search snippets alone are not body inspection.',
              'Record publisher, exact URL, actual access date, explicitly established publication date, claim scope and limitations. EV01: a measurement/update label is not publication; save null when publication is unknown.',
              'Reuse a registered source ID for the same original URL; do not refresh dates without inspection.'],
    'access':['Resolve the model, provider, product and client before describing an access route.',
              'Inspect official route documentation, eligibility, restrictions and linked offers. EV04: qualify conditions by the exact endpoint/product, not a sibling route.',
              'Include model_label; save null when the provider label has not been established.'],
    'price':['Inspect the original provider tariff and resolve the exact offer.',
             'Record currency, unit, billing method, rates, actual effective dates, region, tier and conditions. EV01/EV04: bind each rule to the exact offer; inspection is not an effective date.',
             'Preserve older offers; do not compare subscriptions and token rates as a shared unit.'],
    'benchmark':['Inspect the original result and its methodology.',
                 'Record the exact checkpoint, measured configuration, metric, score, evidence class and limitations. EV01/EV03: read the exact result row and distinguish measurement from publication/inspection.',
                 'EV02: save each judge name, type and scoring role in conditions/evidence_notes; retain panel dependence and unknown evaluator details in limitations.',
                 'Keep quality measurements, preference rankings and vendor claims separate.'],
    'behavior':['Inspect attributable reports, contrary evidence and documented fixes.',
                'Record claim, applicable model/provider configuration, dates and conditions.',
                'Keep fix publication separate from measured recovery; missing reports are not proof of reliability.'],
    'release':['Inspect an official dated release or lifecycle announcement.',
               'Resolve the exact model or product and event type.',
               'Use null for a date that was not established; retain lifecycle history.'],
    'task_assessment':['Apply the pinned task rubric to the exact model.',
                       'Match the corresponding task decision and exact direct judgment IDs.',
                       'Record result and confidence reasoning; exclusions need positive mismatch evidence.'],
    'research_coverage':['Summarize the actual checked scope of the relevant research domain.',
                         'Record dated evidence and search accounting with unresolved gaps.',
                         'Keep untouched models and domains unchecked; do not refresh carry-forward dates.'],
}


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')


def escape(value):return value.replace('~','~0').replace('/','~1')


def resolve_schema(node,schemas,name,location):
    if '$ref' not in node:return node,name,location
    target,_,fragment=node['$ref'].partition('#')
    target=target or name
    resolved=schemas[target]
    if fragment:
        for part in fragment.split('/')[1:]:resolved=resolved[part.replace('~1','/').replace('~0','~')]
    return resolved,target,fragment


def types(node):
    found=set()
    value=node.get('type',[])
    found.update(value if isinstance(value,list) else [value])
    for keyword in ('oneOf','anyOf','allOf'):
        for branch in node.get(keyword,[]):found.update(types(branch))
    if 'const' in node:
        value=node['const'];found.add('null' if value is None else 'boolean' if isinstance(value,bool) else
                                    'string' if isinstance(value,str) else 'number' if isinstance(value,(int,float)) else 'object')
    if None in node.get('enum',[]):found.add('null')
    return sorted(found)


def conditional_rules(schema,schemas,name,path='',location='',seen=()):
    if '$ref' in schema:
        schema,name,location=resolve_schema(schema,schemas,name,location)
        marker=(name,location)
        if marker in seen:return
        seen=(*seen,marker)
    clauses={key:deepcopy(schema[key]) for key in ('if','then','else','dependentRequired','dependentSchemas','not') if key in schema}
    if clauses:yield {'path':path or '/','schema_location':name+'#'+location,'clauses':clauses}
    for key,child in sorted(schema.get('properties',{}).items()):
        yield from conditional_rules(child,schemas,name,path+'/'+escape(key),location+'/properties/'+escape(key),seen)
    if isinstance(schema.get('items'),dict):
        yield from conditional_rules(schema['items'],schemas,name,path+'/*',location+'/items',seen)
    for keyword in ('oneOf','anyOf','allOf'):
        for i,branch in enumerate(schema.get(keyword,[])):
            yield from conditional_rules(branch,schemas,name,path,location+'/'+keyword+'/'+str(i),seen)


def requirements(schema,schemas,name,path='',location='',required=True,conditions=(),seen=()):
    marker=(name,location)
    if '$ref' in schema:
        schema,name,location=resolve_schema(schema,schemas,name,location)
        marker=(name,location)
        if marker in seen:return
        seen=(*seen,marker)
    field_types=types(schema)
    row={'path':path or '/', 'schema_location':name+'#'+location,
         'required_in_parent':required,'types':field_types,'nullable':'null' in field_types if field_types else None,
         'conditions':list(conditions)}
    row['constraints']={k:deepcopy(schema[k]) for k in ('enum','const','pattern','format','minimum','maximum',
                        'minLength','maxLength','minItems','maxItems','uniqueItems','additionalProperties') if k in schema}
    yield row
    for key,child in sorted(schema.get('properties',{}).items()):
        yield from requirements(child,schemas,name,path+'/'+escape(key),location+'/properties/'+escape(key),
                                key in schema.get('required',[]),conditions,seen)
    if isinstance(schema.get('items'),dict):
        yield from requirements(schema['items'],schemas,name,path+'/*',location+'/items',True,conditions,seen)
    for keyword in ('oneOf','anyOf','allOf'):
        for i,branch in enumerate(schema.get(keyword,[])):
            condition={'path':path or '/','keyword':keyword,'branch':i}
            yield from requirements(branch,schemas,name,path,location+'/'+keyword+'/'+str(i),required,
                                    (*conditions,condition),seen)


def build_contract(schemas,research_date):
    date.fromisoformat(research_date)
    records={}
    for kind,stem in SCHEMAS.items():
        name=stem+'.schema.json'
        records[kind]={'schema':name,'canonical_schema_sha256':sha256(encoded(schemas[name])).hexdigest(),
                       'research_steps':METHODS[kind],
                       'fields':list(requirements(schemas[name],schemas,name)),
                       'conditional_rules':list(conditional_rules(schemas[name],schemas,name))}
    return {'format':FORMAT,'research_date':research_date,
            'public_research_batch_id':'public-source-inspection-'+research_date,
            'checks':CHECKS,'accounting_checks':ACCOUNTING_CHECKS,'records':records,**authoring_directions(),
            'limits':'Schema validity does not establish factual support, receiver acceptance or research completeness.'}


def render_contract(contract):
    lines=['# Required research output','',
           'This generated guide and the validator use the same pinned schemas. Required means the key must be present when its parent object is present. Nullable means null is permitted; it does not make the key optional.',
           '', 'Public provenance identifier for new research findings: `'+contract['public_research_batch_id']+'`.',
           'Retain provenance on unchanged baseline findings. Do not copy private assignment or run IDs into public records.', '',
           '| Check ID | Required output and validation rule |','| --- | --- |']
    lines += ['| '+key+' | '+value+' |' for key,value in contract['checks'].items()]
    lines += ['', '## Current checks and historical evidence', '',
              'RUN means research_run for model packets and scope_run for scoped packets. These checks run in the mechanical preflight, separately from record schemas. The authoritative receiver enforces the same boundaries.', '',
              '| Check ID | Required output and validation rule |', '| --- | --- |']
    lines += ['| '+key+' | '+value+' |' for key,value in contract['accounting_checks'].items()]
    if 'source_bodies' in contract:
        lines+=['','## Required opened-source captures','',contract['source_bodies']['limits'],'',
                '| Check | Required saved artifact and validation |','| --- | --- |']
        lines+=['| '+key+' | '+value+' |' for key,value in contract['source_bodies']['checks'].items()]
    if 'json_authoring_flow' in contract:
        lines += ['', '## JSON authoring flow', '']
        for step in contract['json_authoring_flow']:
            lines += [str(step['step'])+'. '+step['action']+' Save: '+', '.join('`'+p+'`' for p in step['outputs'])+'.']
        evidence=contract['evidence_review']
        lines += ['', '## Required evidence review', '', evidence['enforcement'], '',
                  '| Check ID | Required output and validation rule |','| --- | --- |']
        lines += ['| '+key+' | '+value+' |' for key,value in evidence['checks'].items()]
        for ident,rule in evidence['rules'].items():
            lines += ['', '### '+ident, '', 'Receiver checks: '+', '.join('`'+v+'`' for v in rule['review_checks'])+'.','']
            lines += ['- '+entry for entry in rule['save']]
            lines += ['',rule['unknown'],'','Allowed record locations:','', '```json',
                      json.dumps(rule['record_paths'],ensure_ascii=False,sort_keys=True,indent=2),'```']
        lines += ['', evidence['limits']]
    for kind in sorted(contract['records']):
        record=contract['records'][kind]
        lines += ['', '## '+kind,'','Schema: `'+record['schema']+'`. Follow these research steps:', '']
        lines += [str(i)+'. '+step for i,step in enumerate(record['research_steps'],1)]
        lines += ['', '| Record path | Key presence | Type | Null permitted | Condition | Value constraints | Schema location |',
                  '| --- | --- | --- | --- | --- | --- | --- |']
        for field in record['fields']:
            condition='; '.join(c['path']+' '+c['keyword']+'['+str(c['branch'])+']' for c in field['conditions']) or 'Always'
            lines.append('| `'+field['path']+'` | '+('Required' if field['required_in_parent'] else 'Optional')+
                         ' | '+(', '.join(field['types']) or 'See schema')+' | '+('See schema' if field['nullable'] is None else 'Yes' if field['nullable'] else 'No')+
                         ' | '+condition+' | `'+json.dumps(field['constraints'],sort_keys=True).replace('|','\\|')+'` | `'+field['schema_location']+'` |')
        if record['conditional_rules']:
            lines += ['', 'Apply these exact conditional constraints in addition to the field table:','']
            for rule in record['conditional_rules']:
                lines += ['At `'+rule['path']+'`, from `'+rule['schema_location']+'`:','', '```json',
                          json.dumps(rule['clauses'],ensure_ascii=False,sort_keys=True,indent=2),'```','']
    lines += ['', 'For oneOf, satisfy exactly one complete branch. For anyOf, satisfy at least one complete branch. For allOf, satisfy every branch. The exact branch constraints and enum values are retained in output-contract.json and schemas.json.', '']
    return '\n'.join(lines).encode('utf-8')


def draft_mapping(packet):
    """Schema-only normalization; does not allocate or certify public identifiers."""
    mapping={}
    for change in packet['changes']:
        record=change['record'];ident=record.get('id')
        if change['kind'] in PREFIXES and isinstance(ident,str) and ident.startswith('new:'):
            prefix,width=PREFIXES[change['kind']]
            mapping[ident]=prefix+'-'+sha256(ident.encode()).hexdigest()[:width]
        if change['kind']=='model':
            for collection in ('capabilities','performance_characteristics'):
                for finding in record.get(collection,[]):
                    ident=finding.get('id')
                    if isinstance(ident,str) and ident.startswith('new:'):
                        mapping[ident]='judgment-'+sha256(ident.encode()).hexdigest()[:16]
    return mapping


def replace_refs(value,mapping):
    if isinstance(value,dict):return {k:replace_refs(v,mapping) for k,v in value.items()}
    if isinstance(value,list):return [replace_refs(v,mapping) for v in value]
    return mapping.get(value,value) if isinstance(value,str) else value


def relevant_errors(error):
    """Report the research discriminator branch, not unrelated migration errors."""
    if error.validator in {'oneOf','anyOf'} and isinstance(error.instance,dict):
        matching=[]
        for i,branch in enumerate(error.validator_value):
            discriminators={k:v['const'] for k,v in branch.get('properties',{}).items() if 'const' in v}
            if discriminators and all(error.instance.get(k)==v for k,v in discriminators.items()):matching.append(i)
        if len(matching)==1:
            selected=[child for child in error.context if child.schema_path and child.schema_path[0]==matching[0]]
            if selected:
                for child in selected:yield from relevant_errors(child)
                return
    yield error


def validate_records(packet,schemas,contract):
    from jsonschema import Draft202012Validator,FormatChecker
    from referencing import Registry,Resource
    from referencing.jsonschema import DRAFT202012
    if contract!=build_contract(schemas,contract['research_date']):
        raise ValueError('RC01: Output contract differs from its pinned schemas or helper')
    registry=Registry().with_resources((name,Resource.from_contents(schema,default_specification=DRAFT202012))
                                      for name,schema in schemas.items())
    normalized=replace_refs(packet,draft_mapping(packet))
    errors=[]
    for index,change in enumerate(normalized['changes']):
        kind=change['kind']
        if kind not in SCHEMAS:
            errors.append({'check_id':'RC02','change_index':index,'kind':kind,'path':'/changes/'+str(index)+'/kind','message':'Unsupported record kind'})
            continue
        name=SCHEMAS[kind]+'.schema.json'
        validator=Draft202012Validator(schemas[name],registry=registry,format_checker=FormatChecker())
        for parent in validator.iter_errors(change['record']):
            for error in relevant_errors(parent):
                path='/changes/'+str(index)+'/record'+''.join('/'+escape(str(part)) for part in error.absolute_path)
                parts=list(error.absolute_path)
                performance_rule=(kind=='model' and len(parts)>=3 and
                    (parts[0]=='performance_characteristics' and parts[2] in {'scope','task_ids','related_task_ids'} or
                     parts[0]=='capabilities' and parts[2]=='scope' and error.instance=='performance'))
                errors.append({'check_id':'RC04' if performance_rule else 'RC03','change_index':index,'kind':kind,
                    'record_id':packet['changes'][index]['record'].get('id'),'schema':name,'path':path,'message':error.message,
                    'missing_keys':sorted(set(error.validator_value)-set(error.instance)) if error.validator=='required' and isinstance(error.instance,dict) else []})
    return errors


if __name__=='__main__':
    import sys
    print('Library module. Run the frozen authoring-helper.py entry point.',file=sys.stderr)
    sys.exit(2)
