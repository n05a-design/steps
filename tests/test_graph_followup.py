"""Independent oracle and source namespaces cannot silently grant acceptance."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
from scripts import audit_graph_followup as audit
from scripts import graph_followup_probes as probes


class GraphFollowupTests(unittest.TestCase):
    def test_all_original_58_open_edges_are_accounted_for(self):
        rows=audit.audit()
        self.assertEqual(len(rows),58)
        self.assertEqual(sum(r['validation_status']=='PASS' for r in rows),16)
        self.assertTrue(all(r['human_approval']=='AUSSTEHEND' and not r['production_use_allowed'] for r in rows))
        self.assertEqual(audit.render(rows),(audit.ROOT/audit.MATRIX).read_text(encoding='utf-8'))
        graph,_=audit.audit_graph.audit()
        target=next(r for r in graph if r['relation_id']=='REL-020')
        self.assertEqual(target['target_definition_status'],'AMBIGUOUS_VERSIONED_IDENTITY')
        self.assertIn('ERR-026@PHASE4_8_ARCHIVE',target['definition_evidence'])
        self.assertIn('ERR-026@REGISTER_9AFAF33',target['definition_evidence'])

    def test_unqualified_error_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Ambiguous'):audit.resolve_error('ERR-026')
        a=audit.resolve_error('ERR-026@PHASE4_8_ARCHIVE')
        b=audit.resolve_error('ERR-026@REGISTER_9AFAF33')
        self.assertNotEqual(a['meaning'],b['meaning'])

    def test_alias_and_namespace_swaps_rejected(self):
        original=json.loads((audit.ROOT/audit.IDENTITIES).read_text(encoding='utf-8'))
        for mutation in ['alias','source','approval']:
            d=deepcopy(original)
            if mutation=='alias':d['automatic_bare_id_alias_allowed']=True
            elif mutation=='source':d['records'][0]['source']=d['records'][1]['source']
            else:d['records'][0]['human_review']='APPROVED'
            with self.assertRaises(ValueError):audit.identities(d)

    def test_exhaustive_oracle_distinguishes_search_spaces(self):
        result=probes.oracle([62,65,69,72],[2,5,7,11])
        self.assertEqual((result['unconstrained_min'],result['drop2_min']),(3,7))
        self.assertTrue(result['core_matches_oracle'])

    def test_wrong_core_result_with_same_cost_cannot_fool_oracle(self):
        with patch.object(probes,'optimize_smooth_voice_leading',return_value=[59,65,69,72]):
            self.assertFalse(probes.oracle([62,65,69,72],[2,5,7,11])['core_matches_oracle'])

    def test_drop2_inverse_recognizes_exact_transformation(self):
        self.assertTrue(probes.drop2_shape([57,62,65,72]))
        self.assertFalse(probes.drop2_shape([62,65,69,72]))
        self.assertFalse(probes.drop2_shape([60,64,67,72]))

    def test_arrangements_reject_foreign_notes_and_missing_chords(self):
        plan=json.loads((audit.ROOT/audit.audit_graph.PLAN).read_text(encoding='utf-8'))
        spec=next(p for p in plan['probes'] if p['id']=='MINOR_CYCLE_HAND_LAYERS')
        for mutation in ['foreign','missing']:
            altered=deepcopy(spec)
            if mutation=='foreign':altered['input']['data']['rh'][0][0]='F#4'
            else:altered['input']['data']['rh'].pop()
            with self.assertRaises(ValueError):probes.calculate(altered)

    def test_overlay_rejects_off_cycle_and_duplicate_onsets(self):
        plan=json.loads((audit.ROOT/audit.audit_graph.PLAN).read_text(encoding='utf-8'))
        spec=next(p for p in plan['probes'] if p['id']=='CHARLESTON_UKG_OVERLAY')
        for notes in [[0,3840],[0,0]]:
            altered=deepcopy(spec);altered['input']['data']['parts']['keyboard']=notes
            with self.assertRaises(ValueError):probes.calculate(altered)
