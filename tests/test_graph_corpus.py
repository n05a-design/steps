"""Meaningful selection, timing and acceptance boundaries for corpus evidence."""
from copy import deepcopy
import json
import unittest
from scripts import audit_graph_corpus as c
from scripts.graph_semantic_probes import calculate


class GraphCorpusTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads(c.PLAN.read_text(encoding='utf8'))
        self.obs=json.loads(c.OBS.read_text(encoding='utf8'))

    def test_all_fourteen_cases_remain_open_despite_valid_contracts(self):
        rows=c.audit(self.plan)
        self.assertEqual({r['relation_id'] for r in rows},c.SCOPE)
        self.assertTrue(all(r['relation_status']=='OPEN' and r['human_approval']=='AUSSTEHEND' for r in rows))

    def test_chord_and_drum_datasets_do_not_imply_joint_recordings(self):
        missing=c.capability_gaps(['chords','drum_events','aligned_recording_identity'],['chords','drum_events'])
        self.assertEqual(missing,['aligned_recording_identity'])

    def test_duplicate_missing_originals_and_faked_acceptance_rejected(self):
        for mutate in [lambda d:d['cases'].pop(),lambda d:d['cases'].__setitem__(0,deepcopy(d['cases'][1])),
                       lambda d:d['cases'][0].update(original_row_sha256='0'*64),
                       lambda d:d['cases'][0].update(human_approval='PASS'),
                       lambda d:d['cases'][0].update(historical_assertion_closed=True)]:
            with self.subTest(mutation=mutate):
                d=deepcopy(self.plan);mutate(d)
                with self.assertRaises(ValueError):c.audit(d)

    def test_weakening_required_evidence_rejected(self):
        d=deepcopy(self.plan);d['cases'][0]['required_annotations']=['genre']
        with self.assertRaises(ValueError):c.audit(d)

    def test_project_anchor_change_rejected(self):
        d=deepcopy(self.plan);next(x for x in d['cases'] if x['project_anchors'])['project_anchors'][0]['lf_sha256']='0'*64
        with self.assertRaises(ValueError):c.audit(d)

    def test_opportunities_are_not_counts_of_note_messages(self):
        events=[(0,36,80),(0,36,70),(480,38,90),(960,36,0),(1440,40,70)]
        result=c.beat_coverage(events,480,1)
        self.assertEqual(result,{'kick_1_3':{'matched':1,'opportunities':2},'snare_2_4':{'matched':2,'opportunities':2}})

    def test_tolerance_and_role_counterexample(self):
        result=c.beat_coverage([(49,36,80),(480,36,80),(960,38,80)],480,1)
        self.assertEqual(result['kick_1_3']['matched'],0)
        self.assertEqual(result['snare_2_4']['matched'],0)
        self.assertEqual(c.beat_coverage([(48,36,80)],480,1)['kick_1_3']['matched'],1)

    def test_invalid_timing_denominator_rejected(self):
        for ppq,bars,tol in [(True,1,.1),(480,0,.1),(480,1,.5),(0,1,.1)]:
            with self.assertRaises(ValueError):c.beat_coverage([],ppq,bars,tol)

    def test_observation_cannot_be_generalized_or_signed(self):
        for change in [{'population_generalization':True},{'human_approval':'PASS'},{'relation_status':'SAMPLE_SUPPORTED'}]:
            d=deepcopy(self.obs);d.update(change)
            with self.assertRaises(ValueError):c.validate_observation(d)

    def test_wrong_denominator_and_duplicate_take_rejected(self):
        d=deepcopy(self.obs);d['recordings'][0]['coverage']['kick_1_3']['opportunities']+=1
        with self.assertRaises(ValueError):c.validate_observation(d)
        d=deepcopy(self.obs);d['recordings'][0]['recording_id']=d['recordings'][1]['recording_id']
        with self.assertRaises(ValueError):c.validate_observation(d)

    def test_surdo_role_does_not_prove_dynamic_accent(self):
        spec={'input':{'operation':'surdo_role_grid','data':{'scope':'FLORIANOPOLIS_2010_MARCELINO_FIG3_4','meter':'2/4','ppq':480,'primeira_ticks':[480,1440],'segunda_ticks':[0,960]}}}
        observed=calculate(spec)
        self.assertFalse(observed['dynamic_accent_proven']);self.assertFalse(observed['universal_norm_proven'])
        spec['input']['data']['primeira_ticks']=[0,960]
        with self.assertRaises(ValueError):calculate(spec)

    def test_surdo_scope_cannot_become_all_samba(self):
        spec={'input':{'operation':'surdo_role_grid','data':{'scope':'ALL_SAMBA','meter':'2/4'}}}
        with self.assertRaises(ValueError):calculate(spec)

    def test_exact_boundary_slot_calculation_matches_window_calculation(self):
        events=[(48,36,90),(481,38,70),(1009,36,80),(1440,40,60)]
        self.assertEqual(c.beat_coverage(events,480,1),c.slot_set_coverage(events,480,1))

    def test_source_metadata_cannot_claim_full_definition_or_fabricated_page(self):
        p=c.ROOT/'docs/audit/fable-5.2/GRAPH_CDR019_CDR021_QUELLEN_2026-11-14.json'
        d=json.loads(p.read_text(encoding='utf8'));d['historical_definitions_resolved']=True
        with self.assertRaises(ValueError):c.validate_sources(d)
        d=json.loads(p.read_text(encoding='utf8'));d['sources'][0]['visually_checked_pdf_pages']=[1,34,35]
        with self.assertRaises(ValueError):c.validate_sources(d)


if __name__=='__main__':unittest.main()
