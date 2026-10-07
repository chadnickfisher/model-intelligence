"""Readable card content from canonical findings; no new capability judgments."""
import re
from .data import claims, benchmark_findings, model_routes, route_kinds, route_label, billing_summary


def task_card_evidence(model, data, task=None, include_related=False):
    findings=claims(model,task,include_related) if task else []
    ids={j['id'] for j in findings}
    benchmarks=[b for b in benchmark_findings(model,data) if ids.intersection(b['judgment_ids'])]
    return findings,benchmarks


def concrete_limits(values):
    administrative=('no model inference or benchmark was run', 'no inference calls were made',
                    'original bundle retained', 'migration', 'research provenance:')
    return list(dict.fromkeys(v for v in values if v and not any(s in v.lower() for s in administrative)))


def readable_conditions(values):
    return [v.replace('arena_rows', "the source's model configuration table")
            for v in values if not re.fullmatch(r'[a-z0-9_]+',v)]


def card_watchouts(model, data, task=None, include_related=False):
    if task:
        findings,benchmarks=task_card_evidence(model,data,task,include_related)
        values=[v for j in findings for v in j['known_failure_modes']]
        values += [j['judgment'] for j in findings if j['assessment'] in {'warning','weak'}]
        values += [v for b in benchmarks for v in b['limitations']]
    else:
        values=[v for j in model['capabilities'] for v in j['known_failure_modes']]+model['limitations']
    return concrete_limits(values)


def access_bullets(model,data):
    return list(dict.fromkeys(
        '**'+', '.join(sorted(route_kinds(r)))+'** — '+route_label(r,data)+'; '+billing_summary(r,data)
        for r in model_routes(model,data,True)))


def complete_summary(text):
    """Keep complete sentences and limiting statements, never a character prefix."""
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])',text.strip()) if s.strip()]
    if not sentences:return ''
    limiting=re.compile(r'\b(not|no|unknown|unresolved|unverified|only|however|but|limited|'
                        r'uncertain|retract\w*|correct\w*|recipe|fix\w*|recover\w*|'
                        r'propos\w*|suggest\w*|preliminary|reported|configuration)\b',re.I)
    keep=[sentences[0]]+[s for s in sentences[1:] if limiting.search(s)]
    return ' '.join(dict.fromkeys(keep))


def observation_summary(record):
    text=complete_summary(record['claim'])
    if record['status']=='fix_published':
        outcome=('Published change; measured recovery not established.' if record['fix']['measured_improvement'] is None
                 else 'Published change; inspect the recorded recovery measurement and conditions.')
    elif record['status']=='unknown':outcome='Current outcome unresolved.'
    else:outcome='Recorded status: '+record['status'].replace('_',' ')+'.'
    return text+' '+outcome
