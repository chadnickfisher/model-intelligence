"""Deterministic bounded queues; selection does not claim research was completed."""
from datetime import date
from tools import research_two_phase as p

LANES = ('factual', 'task_insight', 'identity')
DOMAINS = ('task-specific capabilities', 'benchmarks/confidence rationale',
           'access/pricing/limits', 'dated post-launch behavior')
VOLATILITY = {'high': 7, 'medium': 30, 'low': 90}

def select(queue, catalog, *, today, lane_limits, carryover_cap=1):
    day = date.fromisoformat(today)
    if set(lane_limits) != set(LANES) or any(type(n) is not int or n < 0 for n in lane_limits.values()):
        raise ValueError('Explicit nonnegative lane budgets required')
    if type(carryover_cap) is not int or carryover_cap < 0:
        raise ValueError('Invalid carryover cap')
    if len({row['id'] for row in queue}) != len(queue):
        raise ValueError('Duplicate queue identity')
    ranked = []; dispositions = []
    for row in queue:
        if row['lane'] not in LANES or row['volatility'] not in VOLATILITY:
            raise ValueError('Unknown lane or volatility')
        if row['model_id'] not in catalog:
            dispositions.append({'id': row['id'], 'status': 'unresolved_identity'}); continue
        if row['status'] not in ('pending', 'unknown', 'blocked', 'unchanged', 'changed'):
            raise ValueError('Unknown queue state')
        if type(row['attempts']) is not int or row['attempts'] < 0:
            raise ValueError('Invalid attempt count')
        entered = date.fromisoformat(row['queued_at'])
        checked = date.fromisoformat(row['last_checked_at']) if row['last_checked_at'] else None
        attempted = date.fromisoformat(row['last_attempt_at']) if row.get('last_attempt_at') else None
        if entered > day or checked and checked > day or attempted and attempted > day:
            raise ValueError('Future queue date')
        overdue = checked is None or (day - checked).days >= VOLATILITY[row['volatility']]
        unresolved = row['status'] in ('pending', 'unknown', 'blocked')
        if not overdue and not unresolved:
            dispositions.append({'id': row['id'], 'status': 'not_due'}); continue
        # Age first within unresolved/due classes; stable ID breaks ties, never input order.
        key = (not unresolved, attempted or date.min, entered, checked or date.min, row['id'])
        ranked.append((row['lane'], key, row))
    chosen = []
    for lane in LANES:
        count = 0; carry = 0
        for _, _, row in sorted((r for r in ranked if r[0] == lane), key=lambda r: r[1]):
            repeated = row['attempts'] > 0
            if count >= lane_limits[lane]: status = 'lane_budget'
            elif repeated and carry >= carryover_cap: status = 'carryover_cap'
            else:
                chosen.append(row); count += 1; carry += int(repeated); status = 'selected'
            dispositions.append({'id': row['id'], 'status': status})
    selected_ids = {r['id'] for r in chosen}
    return {'version': 'question-planner/1', 'as_of': today,
        'queue_pin': p.pin(p.encoded(sorted(queue, key=lambda r: r['id']))),
        'selected': chosen, 'dispositions': sorted(dispositions, key=lambda r: r['id']),
        'queue_after_dispatch': [{**r, **({'attempts': r['attempts'] + 1, 'last_attempt_at': today}
            if r['id'] in selected_ids else {})} for r in sorted(queue, key=lambda r: r['id'])],
        'domain_accounting': [{'model_id': model, 'domain': domain, 'result': 'not_checked',
            'selected_question_ids': sorted(r['id'] for r in chosen if r['model_id'] == model)}
            for model in sorted(catalog) for domain in DOMAINS]}
