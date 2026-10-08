"""Exact-task comparison summaries and provider-qualified text costs."""
from decimal import Decimal

from .data import comparable_api_offers
from .presentation import task_assessment


def comparison_assessments(model, data, task=None):
    rows = [a for a in data.get('task_assessment', {}).values()
            if a['model_id'] == model['id'] and a.get('aggregate')]
    if len({a['task_id'] for a in rows}) != len(rows):
        raise ValueError('Duplicate canonical model/task assessment')
    rows.sort(key=lambda a: data['task'][a['task_id']]['label'].casefold())
    suitable = [a for a in rows if a['aggregate']['suitability'] in {'high', 'medium'}]
    other = [a for a in rows if a['aggregate']['suitability'] in {'low', 'disputed'}]
    assessment = task_assessment(model, data, task) if task else None
    return {
        'assessment': assessment,
        'aggregate': assessment.get('aggregate') if assessment else None,
        'suitable': suitable,
        'other': other,
        'fit_counts': {level: sum(a['aggregate']['suitability'] == level for a in suitable)
                       for level in ('high', 'medium')},
        'confidence_counts': {level: sum(a['aggregate']['evidence_confidence'] == level for a in suitable)
                              for level in ('high', 'medium', 'low')},
    }


def comparison_offers(model, data, input_tokens, output_tokens):
    """One currency and ordinary API billing; never mix subscriptions or timed tiers."""
    rows = comparable_api_offers(model, data, input_tokens=input_tokens,
                                 output_tokens=output_tokens, currency='USD')
    special_modes = ('batch', 'flex', 'priority', 'off-peak', 'off_peak', 'peak')
    rows = [row for row in rows
            if not any(mode in (data['price'][row['price_id']]['tier'] or '').lower()
                       for mode in special_modes)]
    return sorted(rows, key=lambda row: (
        data['provider'][data['price'][row['price_id']]['provider_id']]['name'].casefold(),
        (data['price'][row['price_id']]['tier'] or '').casefold(), row['price_id']))


def usd_text(value):
    text = format(Decimal(str(value)), 'f')
    whole, _, fraction = text.partition('.')
    return '$' + whole + '.' + fraction.rstrip('0').ljust(2, '0')
