"""Counterchecks for additional specification calculations."""

from copy import deepcopy
import json
import unittest
from scripts import audit_golden_supplements as audit


class GoldenSupplementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads((audit.ROOT/'knowledge/research/golden_cases/golden_reference_cases.json').read_text(encoding='utf-8'))

    def test_all_supplemented_cases_compute_expected_results(self):
        rows=audit.audit(self.cases)
        self.assertEqual(sum(r['supplement_status']=='BOUNDED_CALCULATION_PASS' for r in rows),14)
        self.assertTrue(all(r['human_review']=='AUSSTEHEND' for r in rows))

    def test_changed_numeric_inputs_and_expected_values_are_detected(self):
        for original in self.cases:
            if original['case_id'] not in audit.SUPPORTED:continue
            altered=deepcopy(original);altered['expected_output']=None
            result=audit.audit([altered])[0]
            with self.subTest(case=original['case_id']):self.assertEqual(result['supplement_status'],'BOUNDED_CALCULATION_FAIL')
        case=deepcopy(next(c for c in self.cases if c['case_id']=='REF-0158'))
        case['input_params']['ab']=9
        self.assertNotEqual(audit.calculate(case),case['expected_output'])

    def test_voicing_layout_and_guide_tones_are_consumed(self):
        case=deepcopy(next(c for c in self.cases if c['case_id']=='REF-0093'))
        case['input_params']['type']='Typ B'
        self.assertNotEqual(audit.calculate(case),case['expected_output'])
        case=deepcopy(next(c for c in self.cases if c['case_id']=='REF-0193'))
        case['input_params']['g7_guide']=[6,11]
        self.assertNotEqual(audit.calculate(case),case['expected_output'])
