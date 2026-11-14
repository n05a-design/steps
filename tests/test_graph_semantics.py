"""Scope, representation and review boundaries for 18 semantic proposals."""
from copy import deepcopy
import json
import struct
import unittest
from scripts import audit_graph_semantics as audit
from scripts import graph_semantic_probes as probe


class GraphSemanticTests(unittest.TestCase):
    def setUp(self):
        self.document=json.loads((audit.ROOT/audit.PLAN).read_text(encoding='utf-8'))
        self.relations=audit.audit_graph.read_csv(audit.ROOT/'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv')
        plan=json.loads((audit.ROOT/audit.audit_graph.PLAN).read_text(encoding='utf-8'))
        self.probes={p['id']:p for p in plan['probes']}

    def test_all_eighteen_contracts_do_not_turn_into_eighteen_musical_passes(self):
        rows=audit.audit(self.document)
        self.assertEqual(len(rows),18)
        self.assertEqual(sum(r['model_status']=='PASS' for r in rows),17)
        self.assertEqual(sum(r['model_status']=='NOT_EXECUTED' for r in rows),1)
        self.assertTrue(all(not r['historical_assertion_closed'] and not r['production_use_allowed'] for r in rows))
        self.assertEqual(audit.render(rows),(audit.ROOT/audit.MATRIX).read_text(encoding='utf-8'))

    def test_missing_scope_or_changed_original_rejected(self):
        for mutation in ['missing','duplicate','original']:
            d=deepcopy(self.document)
            if mutation=='missing':d['proposals'].pop()
            elif mutation=='duplicate':d['proposals'][-1]=d['proposals'][0]
            else:d['proposals'][0]['original_row_sha256']='0'*64
            with self.assertRaises(ValueError):audit.validate(d,self.relations,self.probes)

    def test_human_or_historical_acceptance_cannot_be_injected(self):
        for field,value in [('human_approval','APPROVED'),('production_use_allowed',True),('historical_assertion_closed',True)]:
            d=deepcopy(self.document);d['proposals'][0][field]=value
            with self.assertRaises(ValueError):audit.validate(d,self.relations,self.probes)

    def test_wrong_gm_profile_or_namespace_is_not_eligible(self):
        for ident,key,value in [('CDR-020','midi_profile','NON_GM'),('REL-027','namespace','LATER_READINESS')]:
            p=next(p for p in self.document['proposals'] if p['historical_relation_id']==ident)
            context=dict(p['required_context']);context[key]=value
            self.assertFalse(audit.eligible_for_review(p,context))
            self.assertFalse(audit.eligible_for_review(p,{}))

    def test_proposal_cannot_relax_protected_scope(self):
        for ident,key,value in [('CDR-020','midi_profile','ANY'),('CR-027','index_base',False),
                                ('CDR-014','historical_transcription',True),('CDR-019','historical_origin_verified',True)]:
            d=deepcopy(self.document);p=next(p for p in d['proposals'] if p['historical_relation_id']==ident)
            p['required_context'][key]=value
            with self.assertRaises(ValueError):audit.validate(d,self.relations,self.probes)

    def test_musicxml_boundaries_and_offset_are_explicit(self):
        for channel,note,expected in [(1,1,(0,0)),(10,39,(9,38)),(16,128,(15,127))]:
            xml=f'<midi-instrument><midi-channel>{channel}</midi-channel><midi-unpitched>{note}</midi-unpitched></midi-instrument>'
            value=probe.xml_midi_index(xml)
            self.assertEqual((value['wire_channel'],value['note_number']),expected)
        for channel,note in [(0,39),(17,39),(10,0),(10,129)]:
            with self.assertRaises(ValueError):probe.xml_midi_index(f'<midi-instrument><midi-channel>{channel}</midi-channel><midi-unpitched>{note}</midi-unpitched></midi-instrument>')

    def test_duplicate_or_missing_xml_fields_rejected(self):
        for xml in ['<midi-instrument><midi-channel>10</midi-channel></midi-instrument>',
                    '<midi-instrument><midi-channel>10</midi-channel><midi-channel>1</midi-channel><midi-unpitched>39</midi-unpitched></midi-instrument>']:
            with self.assertRaises(ValueError):probe.xml_midi_index(xml)

    def test_ppq_control_refuses_smpte_and_invalid_indices(self):
        b=probe.control_smf(480,38,9)
        self.assertEqual(struct.unpack('>IHHH',b[4:14]),(6,0,1,480))
        self.assertEqual(b[:4],b'MThd');self.assertEqual(b[14:18],b'MTrk')
        for ppq,note,channel in [(32768,38,9),(0,38,9),(480,128,9),(480,38,16),(True,38,9)]:
            with self.assertRaises(ValueError):probe.control_smf(ppq,note,channel)

    def test_eighth_and_sixteenth_swing_do_not_share_an_onset(self):
        a=probe.calculate(self.probes['PAIR_INDEX_EIGHTH'])
        b=probe.calculate(self.probes['PAIR_INDEX_SIXTEENTH'])
        self.assertEqual((a['onsets'][1],b['onsets'][1]),(288,144))
        self.assertEqual((a['zero_based_moving_index'],b['zero_based_moving_index']),(1,1))

    def test_same_spelling_does_not_have_a_universal_scale_degree(self):
        self.assertEqual(probe.calculate(self.probes['ENHARMONIC_FUNCTION_CONTEXT']),[7,3,3])

    def test_twenty_eight_triads_are_instances_not_unique_catalog(self):
        value=probe.calculate(self.probes['SELECTED_SCALE_TRIAD_INSTANCES'])
        self.assertEqual(value['instances'],28)
        self.assertFalse(value['all_instances_unique'])

    def test_metric_overlay_is_a_timed_draft_not_style_evidence(self):
        value=probe.calculate(self.probes['BEMBE_MONTUNO_LCM_DRAFT'])
        self.assertEqual((value['joint_ticks'],value['bell_cycles'],value['harmonic_loops'],value['seconds']),(23040,8,3,16))
        self.assertFalse(value['style_pairing_proven'])

    def test_wrong_expected_value_fails_every_new_model(self):
        from scripts import graph_probes
        for original in self.probes.values():
            if original['kind']!='semantic':continue
            altered=deepcopy(original);altered['expected']=None
            with self.subTest(probe=original['id']),self.assertRaises(ValueError):graph_probes.evaluate(altered)

    def test_primary_spec_scope_does_not_approve_full_relation(self):
        rows,_=audit.audit_graph.audit();row=next(r for r in rows if r['relation_id']=='CDR-020')
        self.assertEqual(row['source_assertion_status'],'CURRENT_PRIMARY_SPEC_SCOPED_CHECK')
        self.assertEqual(row['relation_status'],'OPEN');self.assertEqual(row['human_review'],'AUSSTEHEND')
