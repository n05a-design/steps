from copy import deepcopy
import json
import unittest
from scripts import audit_gmd_coverage as c
from scripts import audit_graph_corpus as graph


class CoverageTests(unittest.TestCase):
    def test_parent_genre_cannot_substitute_exact_subgenre(self):
        rows=[{'style':s,'beat_type':'beat','time_signature':'4-4'} for s in ('soul','soul/motown','neworleans/chacha','dance/breakbeat')]
        self.assertEqual(c.select(rows,'exact','soul/neosoul'),[])
        self.assertEqual(c.select(rows,'exact','afrocuban/chacha'),[])
        self.assertEqual(c.select(rows,'primary','dnb'),[])
        self.assertEqual(len(c.select(rows,'primary','soul')),2)

    def test_fill_or_wrong_meter_cannot_enter_frame(self):
        rows=[{'style':'soul','beat_type':'fill','time_signature':'4-4'},{'style':'soul','beat_type':'beat','time_signature':'3-4'}]
        self.assertEqual(c.select(rows,'primary','soul'),[])

    def test_half_time_backbeat_is_not_standard_two_four(self):
        d=c.components([0,1,2,3,4],{36:[0,2.5],38:[1,3]},.04)
        self.assertFalse(d['kick_snare_literal_joint'])
        self.assertTrue(c.components([0,1,2,3,4],{36:[0,2.5],38:[2]},.04)['kick_snare_literal_joint'])

    def test_drag_anchor_requires_separate_onset(self):
        self.assertFalse(c.components([0,1,2,3,4],{36:[0,2.5],38:[2]},.1)['joint_with_proposed_drag_anchor'])
        self.assertTrue(c.components([0,1,2,3,4],{36:[0,2.5],38:[1.5,2]},.04)['joint_with_proposed_drag_anchor'])

    def test_hat_copresence_excludes_next_bar(self):
        self.assertFalse(c.components([0,1,2,3,4],{22:[0],44:[4]},.04)['closed_hat_and_pedal_copresent'])

    def test_source_inventory_changes_rejected(self):
        base=json.loads(c.OUTPUT.read_text(encoding='utf8'));c.validate(base)
        for field,value in [('source_ids',[]),('relation_status','PASS'),('original_row_sha256','0'*64)]:
            d=deepcopy(base);d['frames'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(d)

    def test_proxy_source_denominator_and_counts_rejected(self):
        base=json.loads(c.OUTPUT.read_text(encoding='utf8'))
        for field,value in [('midi_sha256','0'*64),('complete_bars',True),('style','soul/neosoul')]:
            d=deepcopy(base);d['records'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(d)
        d=deepcopy(base);d['records'][0]['counts']['0.04']['kick36_1_and_3plus']=True
        with self.assertRaises(ValueError):c.validate(d)

    def test_proxy_cannot_gain_harmony_or_human_acceptance(self):
        for field,value in [('human_approval','PASS'),('harmonic_pairing_verified',True),('exact_pattern_verified',True)]:
            d=json.loads(c.OUTPUT.read_text(encoding='utf8'));d[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(d)

    def test_reily_receipt_cannot_promote_unread_figures_or_cabral(self):
        base=json.loads((graph.ROOT/'docs/audit/fable-5.2/CDR019_REILY_ORIGINALTEXT_2026-11-15.json').read_text(encoding='utf8'));graph.validate_reily_followup(base)
        for field,value in [('notation_visually_verified',False),('cabral_original_verified',True),('human_approval','PASS'),('historical_causality_verified',True),('full_pdf_sha256','0'*64)]:
            d=deepcopy(base);d[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):graph.validate_reily_followup(d)

    def test_garcia2013_fulltext_cannot_close_historical_assertion(self):
        base=json.loads((graph.ROOT/'docs/audit/fable-5.2/CDR019_GARCIA2013_VOLLTEXT_2026-11-15.json').read_text(encoding='utf8'));graph.validate_garcia_2013_fulltext(base)
        for field,value in [('human_approval','PASS'),('historical_assertion_closed',True),('requested_older_original_pages_newly_verified',1),('full_pdf_sha256','0'*64)]:
            d=deepcopy(base);d[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):graph.validate_garcia_2013_fulltext(d)

    def test_jobim_pim079_cannot_gain_premature_approval(self):
        base=json.loads((graph.ROOT/'docs/audit/fable-5.2/CDR019_JOBIM_PIM079_PRIMARQUELLE_2026-11-15.json').read_text(encoding='utf8'));graph.validate_jobim_pim079_source(base)
        for field,value in [('human_approval','PASS'),('historical_assertion_closed',True),('node_definitions_closed',True),('pdf_sha256','0'*64)]:
            d=deepcopy(base);d[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):graph.validate_jobim_pim079_source(d)


if __name__=='__main__':unittest.main()
