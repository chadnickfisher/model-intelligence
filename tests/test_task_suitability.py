"""Fictional records exercise policy boundaries; they are not catalog research."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from tools.task_assessments import select_task_assessments, task_assessment_errors

ROOT = Path(__file__).resolve().parents[1]


def fixture(rating='medium', confidence='low'):
    """A fictional model/task assessment, deliberately absent from canonical data."""
    result = 'excluded' if rating == 'not_supported' else 'unknown' if rating == 'unknown' else 'assessed'
    return {
        'id': 'task-assessment-0000000000000001', 'model_id': 'fixture-model',
        'task_id': 'coding.scoped_edit', 'applicability': 'excluded' if result == 'excluded' else 'applicable',
        'result': result, 'checked_at': '2026-10-08', 'rationale': 'Fictional applicability check.',
        'confidence_rationale': 'Fictional bounded task evidence.',
        'judgment_ids': ['fixture-judgment'] if result == 'assessed' else [],
        'evidence_ids': ['fixture-source', 'fixture-contrary'],
        'conditions': ['Fictional fixed checkpoint and tool-enabled workflow.'], 'remaining_gaps': [],
        'aggregate': {
            'policy_version': '1', 'suitability': rating, 'evidence_confidence': confidence,
            'assessed_at': '2026-10-08', 'rationale': 'Fictional task conclusion.',
            'confidence_rationale': 'Fictional evidence rationale; not source-count scoring.',
            'supporting_evidence_ids': ['fixture-source'],
            'contradictory_evidence_ids': ['fixture-contrary'] if rating == 'disputed' else [],
            'conflict_rationale': 'Fictional unresolved divergence.' if rating == 'disputed' else None,
            'watch_outs': ['Fictional limitation.'], 'access_ids': []}}


class SuitabilitySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / 'schema/task-assessment-record.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def test_valid_suitability_confidence_combinations(self):
        for rating in ('high', 'medium', 'low', 'not_supported'):
            for confidence in ('high', 'medium', 'low'):
                with self.subTest(rating=rating, confidence=confidence):
                    self.validator.validate(fixture(rating, confidence))
        for rating in ('disputed', 'unknown'):
            self.validator.validate(fixture(rating, None))

    def test_legacy_record_does_not_require_or_create_an_aggregate(self):
        record = fixture()
        del record['aggregate']
        self.validator.validate(record)
        self.assertEqual(select_task_assessments([record], record['task_id']), [])

    def test_invalid_evidence_confidence_and_applicability(self):
        cases = []
        cases.append(fixture('disputed', 'high'))
        cases.append(fixture('unknown', 'low'))
        cases.append(fixture('high', None))
        record = fixture('not_supported', 'high')
        record['applicability'] = 'applicable'
        cases.append(record)
        record = fixture('unknown', None)
        record['result'] = 'assessed'
        cases.append(record)
        record = fixture()
        record['aggregate']['assessed_at'] = None
        cases.append(record)
        for record in cases:
            with self.subTest(record=record):
                self.assertTrue(list(self.validator.iter_errors(record)))

    def test_disputed_requires_explanation_and_contrary_evidence(self):
        for field, value in [('conflict_rationale', None), ('conflict_rationale', '  '),
                             ('contradictory_evidence_ids', [])]:
            record = fixture('disputed', None)
            record['aggregate'][field] = value
            self.assertTrue(list(self.validator.iter_errors(record)))

    def test_positive_conclusions_require_support_and_conditions(self):
        for rating in ('high', 'medium', 'low', 'not_supported', 'disputed'):
            record = fixture(rating, None if rating == 'disputed' else 'low')
            record['aggregate']['supporting_evidence_ids'] = []
            self.assertTrue(list(self.validator.iter_errors(record)))
        record = fixture()
        record['conditions'] = []
        self.assertTrue(list(self.validator.iter_errors(record)))
        record['conditions'] = ['  ']
        self.assertTrue(list(self.validator.iter_errors(record)))


class SuitabilityQueryTests(unittest.TestCase):
    def setUp(self):
        self.rows = [fixture(rating, None if rating in ('unknown', 'disputed') else 'low')
                     for rating in ('high', 'medium', 'low', 'disputed', 'not_supported', 'unknown')]
        for index, row in enumerate(self.rows):
            row['id'] = f'task-assessment-{index + 1:016x}'
            row['model_id'] = 'fixture-model-' + row['aggregate']['suitability']

    def test_defaults_and_explicit_not_supported(self):
        rows = select_task_assessments(self.rows, 'coding.scoped_edit')
        self.assertEqual([r['aggregate']['suitability'] for r in rows], ['high', 'medium', 'low', 'disputed'])
        rows = select_task_assessments(self.rows, 'coding.scoped_edit', suitability=['not_supported'])
        self.assertEqual([r['aggregate']['suitability'] for r in rows], ['not_supported'])

    def test_confidence_filter_keeps_disputed_and_all_its_evidence(self):
        rows = select_task_assessments(self.rows, 'coding.scoped_edit', confidence=['high'])
        self.assertEqual([r['aggregate']['suitability'] for r in rows], ['disputed'])
        self.assertEqual(rows[0]['aggregate']['contradictory_evidence_ids'], ['fixture-contrary'])
        self.assertIsNone(rows[0]['aggregate']['evidence_confidence'])
        self.assertEqual(select_task_assessments(self.rows, 'coding.scoped_edit',
                         suitability=['high', 'medium', 'low'], confidence=['high']), [])

    def test_confidence_is_independent_of_fit_and_non_support_is_opt_in(self):
        self.rows[2]['aggregate']['evidence_confidence'] = 'high'
        self.rows[4]['aggregate']['evidence_confidence'] = 'high'
        rows = select_task_assessments(self.rows, 'coding.scoped_edit', confidence=['high'])
        self.assertEqual([r['aggregate']['suitability'] for r in rows], ['low', 'disputed'])
        rows = select_task_assessments(self.rows, 'coding.scoped_edit',
                                       suitability=['not_supported'], confidence=['high'])
        self.assertEqual([r['aggregate']['suitability'] for r in rows], ['not_supported'])

    def test_task_scope_empty_selection_and_invalid_filters(self):
        self.assertEqual(select_task_assessments(self.rows, 'coding.debugging'), [])
        self.assertEqual(select_task_assessments(self.rows, 'coding.scoped_edit', suitability=[]), [])
        for kwargs in ({'suitability': ['unknown']}, {'confidence': ['unknown']}):
            with self.assertRaises(ValueError):
                select_task_assessments(self.rows, 'coding.scoped_edit', **kwargs)


class SuitabilityIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.row = fixture()
        self.models = {'fixture-model': {'capabilities': [{
            'id': 'fixture-judgment', 'scope': 'direct',
            'task_ids': ['coding.scoped_edit'], 'related_task_ids': []}]}}
        self.tasks = {'coding.scoped_edit', 'coding.debugging'}

    def errors(self, rows=None, access=None):
        return task_assessment_errors(rows if rows is not None else [self.row],
                                      self.models, self.tasks, access or {})

    def test_duplicate_model_task_and_wrong_scope_rejected(self):
        self.assertEqual(self.errors(), [])
        duplicate = deepcopy(self.row)
        duplicate['id'] = 'task-assessment-0000000000000002'
        self.assertTrue(any('duplicate model/task' in e for e in self.errors([self.row, duplicate])))
        self.row['task_id'] = 'coding.debugging'
        self.assertTrue(any('exact direct task' in e for e in self.errors()))
        self.row['task_id'] = 'coding.scoped_edit'
        judgment = self.models['fixture-model']['capabilities'][0]
        judgment.update(scope='compound', task_ids=[], related_task_ids=['coding.scoped_edit', 'coding.debugging'])
        self.assertTrue(any('exact direct task' in e for e in self.errors()))

    def test_unchecked_evidence_wrong_route_and_backdated_assessment_rejected(self):
        self.row['aggregate']['supporting_evidence_ids'] = ['unreviewed-source']
        self.assertTrue(any('assessment evidence' in e for e in self.errors()))
        self.row = fixture()
        self.row['aggregate']['access_ids'] = ['wrong-route']
        self.assertTrue(any('exact model' in e for e in self.errors(access={
            'wrong-route': {'model_id': 'different-model'}})))
        self.row = fixture()
        self.row['aggregate']['assessed_at'] = '2026-10-07'
        self.assertTrue(any('predates' in e for e in self.errors()))
        self.row['aggregate']['assessed_at'] = None
        self.errors()  # Schema reports the type error; integrity checks must not crash.

    def test_non_support_requires_positive_evidence_without_task_quality_finding(self):
        self.row = fixture('not_supported', 'high')
        self.assertEqual(self.errors(), [])
        self.row['evidence_ids'] = []
        self.assertTrue(any('positive mismatch evidence' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
