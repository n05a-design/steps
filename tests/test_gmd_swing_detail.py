import json
import unittest
from scripts.audit_gmd_swing_detail import OUTPUT,interval,validate,velocities


class SwingDetailTests(unittest.TestCase):
    def test_actual_interval_ratio(self):
        r=interval([(480,70),(800,50),(960,60)],0,480,1)
        self.assertEqual((r['first_interval_ticks'],r['second_interval_ticks'],r['ratio_fraction']),(320,160,'2'))

    def test_missing_endpoint_is_not_measured(self):
        self.assertEqual(interval([(480,70),(800,50)],0,480,1)['status'],'MISSING_ENDPOINT')

    def test_duplicate_endpoint_is_ambiguous(self):
        self.assertEqual(interval([(480,70),(481,60),(800,50),(960,60)],0,480,1)['status'],'AMBIGUOUS_ENDPOINT')

    def test_endpoint_does_not_count_as_interior(self):
        self.assertEqual(interval([(480,70),(960,60)],0,480,1)['status'],'NO_INTERIOR')

    def test_multiple_intermediate_hits_are_not_collapsed(self):
        self.assertEqual(interval([(480,70),(700,40),(800,50),(960,60)],0,480,1)['status'],'AMBIGUOUS_INTERIOR')

    def test_zero_velocity_is_not_a_skip_or_velocity_sample(self):
        self.assertEqual(interval([(480,70),(800,0),(960,60)],0,480,1)['status'],'NO_INTERIOR')
        self.assertEqual(velocities([(0,0),(1,70),(4,100)],0,4),{'positive_onsets':1,'min':70,'max':70,'median':70})

    def test_changed_ratio_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
        d['records'][0]['ride_bow_intervals']['2']['ratio']=2
        with self.assertRaises(ValueError):validate(d)

    def test_midi_velocity_does_not_approve_acoustic_loudness(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));d['acoustic_loudness_verified']=True
        with self.assertRaises(ValueError):validate(d)

    def test_nonfinite_ratio_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));d['records'][0]['ride_bow_intervals']['2']['ratio']=float('nan')
        with self.assertRaises(ValueError):validate(d)

    def test_boolean_candidate_bar_is_not_a_source_identity(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));d['records'][1]['bar_zero_based']=True
        with self.assertRaises(ValueError):validate(d)


if __name__=='__main__':unittest.main()
