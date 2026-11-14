"""Partial corpus observations must not become tonic, cadence or groove approvals."""
from copy import deepcopy
import json
import unittest
from scripts import audit_billboard_components as b, audit_edm_tempo as e, audit_graph_corpus as c


class CorpusComponentTests(unittest.TestCase):
    def test_transposed_exact_shape_without_tonic_claim(self):
        runs,_=b.chord_segments('0\t| D:maj | A:maj | B:min | G:maj |')
        hits,windows=b.matches(runs,[(0,'maj'),(7,'maj'),(9,'min'),(5,'maj')],'exact')
        self.assertEqual((len(hits),windows),(1,1))

    def test_minor_quality_cannot_be_lost_in_exact_matching(self):
        runs,_=b.chord_segments('0\t| C:maj | G:maj | A:maj | F:maj |')
        self.assertFalse(b.matches(runs,b.targets()['PROG-001'],'exact')[0])

    def test_extension_projection_is_separate(self):
        runs,_=b.chord_segments('0\t| C:maj7 | G:7 | A:min7 | F:maj7 |')
        self.assertFalse(b.matches(runs,b.targets()['PROG-001'],'exact')[0])
        self.assertEqual(len(b.matches(runs,b.targets()['PROG-001'],'triad_projection')[0]),1)

    def test_unsupported_bar_blocks_matches_instead_of_disappearing(self):
        for token in ['N','C:maj/3','C:maj G:maj','C:maj . . .','F:sus4','C:maj(9)']:
            runs,_=b.chord_segments('0\t| C:maj | G:maj | '+token+' | A:min | F:maj |')
            self.assertFalse(b.matches(runs,b.targets()['PROG-001'],'exact')[0],token)

    def test_metadata_boundary_blocks_implicit_functional_continuity(self):
        runs,_=b.chord_segments('0\t| C:maj | G:maj |\n# tonic: D\n1\t| A:min | F:maj |')
        self.assertFalse(b.matches(runs,b.targets()['PROG-001'],'exact')[0])

    def test_repeated_exact_chords_collapse_but_silence_does_not(self):
        runs,_=b.chord_segments('0\t| C:maj | C:maj | G:maj | A:min | F:maj |')
        self.assertEqual(len(b.matches(runs,b.targets()['PROG-001'],'exact')[0]),1)
        runs,_=b.chord_segments('0\t| C:maj | G:maj |\n1\tsilence\n2\t| A:min | F:maj |')
        self.assertFalse(b.matches(runs,b.targets()['PROG-001'],'exact')[0])

    def test_timestamps_must_be_ordered_and_finite(self):
        for text in ['1\t| C:maj |\n0\t| G:maj |','nan\t| C:maj |','-1\t| C:maj |','missing\t| C:maj |']:
            with self.assertRaises(ValueError):b.chord_segments(text)

    def test_billboard_units_are_slots_and_keys_not_verified_songs(self):
        d=json.loads(b.OUTPUT.read_text(encoding='utf8'));b.validate(d)
        self.assertEqual(d['annotation_slots'],890)
        self.assertEqual(d['artist_title_keys'],739)
        self.assertFalse(d['joint_drum_harmony_verified'])

    def test_billboard_corrupted_aggregate_is_rejected(self):
        d=json.loads(b.OUTPUT.read_text(encoding='utf8'));d['summary']['PROG-001']['exact']['matched_slots']+=1
        with self.assertRaises(ValueError):b.validate(d)

    def test_billboard_duplicate_slot_or_fake_acceptance_rejected(self):
        for mutation in [lambda d:d.update(human_approval='PASS'),lambda d:d.update(joint_drum_harmony_verified=True),
                         lambda d:d['records'][0].update(slot_id=d['records'][1]['slot_id'])]:
            d=json.loads(b.OUTPUT.read_text(encoding='utf8'));mutation(d)
            with self.assertRaises(ValueError):b.validate(d)

    def test_tempo_band_boundaries_and_missing_are_separate(self):
        self.assertEqual([e.tempo_band(x) for x in [0,119.99,120,128,128.01]],
                         ['MISSING','OUTSIDE_120_128','IN_120_128','IN_120_128','OUTSIDE_120_128'])

    def test_invalid_tempos_rejected(self):
        for value in [float('nan'),float('inf'),-1]:
            with self.assertRaises(ValueError):e.tempo_band(value)

    def test_exact_house_is_not_all_house_labels(self):
        d=json.loads(e.OUTPUT.read_text(encoding='utf8'));e.validate(d)
        self.assertEqual(sum(d['exact_house']['v2'].values()),23)
        self.assertEqual(sum(d['house_label_family']['v2'].values()),110)

    def test_versioned_tempos_and_denominators_are_not_interchangeable(self):
        d=json.loads(e.OUTPUT.read_text(encoding='utf8'))
        self.assertNotEqual(d['house_label_family']['v1'],d['house_label_family']['v2'])
        d['house_label_family']['v2']=deepcopy(d['house_label_family']['v1'])
        with self.assertRaises(ValueError):e.validate(d)

    def test_tempo_metadata_cannot_accept_historical_or_joint_claim(self):
        for change in [{'historical_assertion_closed':True},{'joint_drum_harmony_verified':True}]:
            d=json.loads(e.OUTPUT.read_text(encoding='utf8'));d.update(change)
            with self.assertRaises(ValueError):e.validate(d)

    def test_preview_catalog_and_index_are_not_original_fulltext(self):
        p=c.ROOT/'docs/audit/fable-5.2/CDR019_ORIGINALSUCHE_2026-11-14.json'
        for mutation in [lambda d:d.update(fulltext_originals_verified=1),lambda d:d.update(verified_causal_claim=True),
                         lambda d:d['records'][1].update(status='FULLTEXT_VERIFIED')]:
            d=json.loads(p.read_text(encoding='utf8'));mutation(d)
            with self.assertRaises(ValueError):c.validate_original_search(d)


if __name__=='__main__':unittest.main()
