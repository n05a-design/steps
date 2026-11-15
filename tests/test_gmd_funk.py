import json
import unittest
from scripts.audit_gmd_funk import OUTPUT,components,validate


class FunkTests(unittest.TestCase):
    def probe(self,events,t=.04):return components([0,1,2,3,4],events,t)

    def test_pat013_ticks_are_not_quarter_kicks(self):
        self.assertTrue(self.probe([(q,36,80) for q in (0,.75,2.5,3.25)])['pat013_kick_grid'])
        self.assertFalse(self.probe([(q,36,80) for q in (0,1,2,3)])['pat013_kick_grid'])

    def test_family_edge_is_not_literal_hat(self):
        d=self.probe([(i/4,22,80) for i in range(16)])
        self.assertTrue(d['hat42_22_sixteenths']);self.assertFalse(d['hat42_sixteenths'])

    def test_single_eighth_event_cannot_supply_sixteenths(self):
        self.assertFalse(self.probe([(i/2,42,80) for i in range(8)],.1)['hat42_22_sixteenths'])

    def test_zero_velocity_and_next_bar_are_excluded(self):
        self.assertFalse(self.probe([(0,36,0),(4,36,90)])['kick36_downbeat'])

    def test_ghost_candidate_is_velocity_bounded_and_not_backbeat(self):
        for tick,velocity,expected in [(.5,25,True),(.5,45,True),(.5,46,False),(1,30,False)]:
            self.assertEqual(self.probe([(tick,38,velocity)])['snare38_velocity25_45_off_backbeat'],expected)

    def test_off_backbeat_is_not_monotonic(self):
        e=[(1.08,38,30)]
        self.assertTrue(self.probe(e,.04)['snare38_velocity25_45_off_backbeat'])
        self.assertFalse(self.probe(e,.1)['snare38_velocity25_45_off_backbeat'])

    def test_inclusive_tolerance_boundary_is_consistent(self):
        self.assertFalse(self.probe([(1.1,38,30)],.1)['snare38_velocity25_45_off_backbeat'])
        self.assertTrue(self.probe([(.1,36,80)],.1)['downbeat_kick_at_bar_max_velocity'])

    def test_downbeat_max_compares_only_kicks(self):
        self.assertTrue(self.probe([(0,36,50),(1,36,50),(1,38,127)])['downbeat_kick_at_bar_max_velocity'])
        self.assertFalse(self.probe([(0,36,50),(1,36,51)])['downbeat_kick_at_bar_max_velocity'])

    def test_collision_uses_distinct_pitches_and_exact_tick(self):
        self.assertTrue(self.probe([(0,36,80),(0,42,80)])['exact_tick_multi_pitch_collision'])
        self.assertFalse(self.probe([(0,36,80),(.001,42,80)])['exact_tick_multi_pitch_collision'])
        self.assertFalse(self.probe([(0,36,80),(0,36,80)])['exact_tick_multi_pitch_collision'])

    def test_complete_subset_is_still_only_component(self):
        e=[(q,36,80) for q in (0,.75,2.5,3.25)]+[(q,38,80) for q in (1,3)]+[(i/4,42,60) for i in range(16)]
        self.assertTrue(self.probe(e)['pat013_component_joint'])

    def test_source_and_denominator_tampering_rejected(self):
        for key,value in [('midi_sha256','0'*64),('recording_id','invented'),('complete_bars',True)]:
            d=json.loads(OUTPUT.read_text(encoding='utf8'));d['records'][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d)

    def test_counts_and_premature_approval_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
        d['records'][0]['counts']['0.04']['kick36_downbeat']=True
        with self.assertRaises(ValueError):validate(d)
        for key,value in [('human_approval','PASS'),('harmonic_pairing_verified',True),('exact_pattern_verified',True)]:
            d=json.loads(OUTPUT.read_text(encoding='utf8'));d[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d)


if __name__=='__main__':unittest.main()
