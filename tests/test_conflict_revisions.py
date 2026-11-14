"""Seven historical conflicts stay visible while concrete proposals execute."""
from copy import deepcopy
import json
import unittest
from scripts import audit_conflict_revisions as audit


class ConflictRevisionTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((audit.ROOT/audit.PLAN).read_text(encoding='utf-8'))

    def test_all_seven_conflicts_have_reproducible_scoped_proposals(self):
        rows=audit.audit(self.plan)
        self.assertEqual(len(rows),15)
        self.assertEqual({r['historical_case_id'] for r in rows},audit.CONFLICT_IDS)
        self.assertTrue(all(r['model_status']=='PASS' and r['historical_status']=='CONFLICT_RETAINED'
                            and not r['production_use_allowed'] for r in rows))
        self.assertEqual(audit.render(rows),(audit.ROOT/audit.MATRIX).read_text(encoding='utf-8'))

    def test_missing_duplicate_or_changed_original_rejected(self):
        for mutation in ['missing','duplicate','fingerprint']:
            p=deepcopy(self.plan)
            if mutation=='missing':p['revisions'].pop()
            elif mutation=='duplicate':p['revisions'][-1]=p['revisions'][0]
            else:p['revisions'][0]['original_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):audit.audit(p)

    def test_fabricated_acceptance_rejected(self):
        for field,value in [('human_approval','APPROVED'),('production_use_allowed',True),('historical_status','PASS')]:
            p=deepcopy(self.plan);p['revisions'][0][field]=value
            with self.assertRaises(ValueError):audit.audit(p)

    def test_wrong_expected_value_fails_every_variant(self):
        for revision in self.plan['revisions']:
            for variant in revision['variants']:
                p=deepcopy(self.plan)
                target=next(v for r in p['revisions'] for v in r['variants'] if v['id']==variant['id'])
                target['model']['expected']=None
                with self.subTest(variant=variant['id']):
                    self.assertTrue(any(r['model_status']=='FAIL' for r in audit.audit(p)))

    def test_source_version_change_and_escaping_path_rejected(self):
        for field,value in [('sha256','0'*64),('path','../outside.md')]:
            p=deepcopy(self.plan);p['revisions'][0]['sources'][0][field]=value
            with self.assertRaises(ValueError):audit.audit(p)

    def test_wrong_model_input_is_not_hidden_by_expected_output(self):
        p=deepcopy(self.plan);p['revisions'][1]['variants'][0]['model']['input']['degrees']=['V7','I']
        self.assertTrue(any(r['model_status']=='FAIL' for r in audit.audit(p)))

    def test_historical_dnb_excerpt_is_not_expanded_to_invented_second_bar(self):
        row=next(r for r in self.plan['revisions'] if r['historical_case_id']=='REF-0062')
        a,b=[audit.calculate(v['model']) for v in row['variants']]
        self.assertEqual(a['documented_bars'],1)
        self.assertEqual(a['kicks'],[0,360,1200,1800])
        self.assertNotEqual(a['kicks'],b['kicks'])
        self.assertNotEqual(a['bpm'],b['bpm'])

    def test_slash_bass_does_not_create_a_lower_triad(self):
        row=self.plan['revisions'][0]
        poly,slash=[audit.calculate(v['model']) for v in row['variants'][:2]]
        self.assertIn(4,poly)
        self.assertNotIn(4,slash['chord_pcs'])
        self.assertEqual(slash['bass_pc'],0)

    def test_hands_and_total_root_presence_are_distinct(self):
        row=next(r for r in self.plan['revisions'] if r['historical_case_id']=='REF-0073')
        rh,total=[audit.calculate(v['model']) for v in row['variants']]
        self.assertFalse(rh['contains_root']);self.assertTrue(total['contains_root'])
