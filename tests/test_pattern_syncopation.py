import copy
import json
import unittest
from scripts.audit_pattern_syncopation import OUTPUT, anchor, observe, validate


class PatternSyncopationTests(unittest.TestCase):
    def test_historical_anchor_identifies_1320_at_480(self):
        a=anchor()
        self.assertEqual((a['case_id'],a['tick'],a['ppq'],a['zero_based_quarter_phase']),('REF-0030',1320,480,'11/4'))

    def test_1320_onset_is_detected(self):
        self.assertTrue(observe([0,1,2,3,4],{36:[2.75]},.04)['syncopation_subset'])

    def test_eighth_1200_does_not_match_sixteenth_1320(self):
        self.assertFalse(observe([0,1,2,3,4],{36:[2.5]},.04)['syncopation_subset'])

    def test_triplet_alias_only_with_coarse_tolerance(self):
        notes={36:[2+2/3]}
        self.assertFalse(observe([0,1,2,3,4],notes,.04)['syncopation_subset'])
        self.assertTrue(observe([0,1,2,3,4],notes,.1)['syncopation_subset'])

    def test_syncopation_alone_is_not_joint_pattern(self):
        self.assertFalse(observe([0,1,2,3,4],{36:[2.75]},.04)['joint_core_and_syncopation_subset'])

    def test_positive_complete_grid(self):
        notes={36:[0,2,2.75],38:[1,3],42:[i/2 for i in range(8)]}
        self.assertTrue(observe([0,1,2,3,4],notes,.04)['joint_core_and_syncopation_subset'])

    def test_changed_anchor_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
        d['anchor']['tick']=1200
        with self.assertRaises(ValueError):validate(d)

    def test_changed_source_hashes_rejected(self):
        original=json.loads(OUTPUT.read_text(encoding='utf8'))
        for field in ('midi_sha256','beat_sha256'):
            d=copy.deepcopy(original);d['rows'][0][field]='0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):validate(d)

    def test_nonmonotonic_subset_counts_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'))
        d['rows'][0]['tolerances_in_local_quarters']['0.04']['syncopation_subset']=1
        d['rows'][0]['tolerances_in_local_quarters']['0.1']['syncopation_subset']=0
        with self.assertRaises(ValueError):validate(d)


if __name__=='__main__':unittest.main()
