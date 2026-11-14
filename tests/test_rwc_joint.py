"""Joint time axes must not be mistaken for exact groove or genre acceptance."""
from copy import deepcopy
import json
import unittest
from scripts import audit_rwc_joint as r


class RwcJointTests(unittest.TestCase):
    def rows(self,items):
        return [{'t_start':str(a),'t_end':str(b),'chord':s} for a,b,s in items]

    def test_contiguous_chord_shapes_keep_their_time_extent(self):
        runs,_=r.segments(self.rows([(0,1,'C:maj'),(1,2,'C:maj'),(2,3,'G:maj'),(3,4,'A:min'),(4,5,'F:maj')]))
        self.assertEqual(r.windows(runs,r.targets()['PROG-001'],'exact'),[(0.,5.)])

    def test_unknown_chord_and_gap_never_bridge_a_shape(self):
        for items in [[(0,1,'C:maj'),(1,2,'N'),(2,3,'G:maj'),(3,4,'A:min'),(4,5,'F:maj')],
                      [(0,1,'C:maj'),(1.1,2,'G:maj'),(2,3,'A:min'),(3,4,'F:maj')]]:
            runs,_=r.segments(self.rows(items))
            self.assertFalse(r.windows(runs,r.targets()['PROG-001'],'exact'))

    def test_invalid_and_overlapping_intervals_are_not_repaired(self):
        for items in [[(1,0,'C:maj')],[(0,2,'C:maj'),(1,3,'G:maj')],[(float('nan'),2,'C:maj')]]:
            with self.assertRaises(ValueError):r.segments(self.rows(items))

    def test_half_open_event_bounds_count_shared_onset_once(self):
        times=[0,1,2,3]
        self.assertEqual(r.bounded_count(times,0,2),2)
        self.assertEqual(r.bounded_count(times,2,4),2)

    def test_complete_four_four_requires_next_downbeat(self):
        beats=[{'t':i*.5,'beat':b} for i,b in enumerate([1,2,3,4,1])]
        self.assertEqual(r.four_four_bars(beats),[[0.,.5,1.,1.5,2.]])
        self.assertEqual(r.four_four_bars(beats[:-1]),[])

    def test_three_four_is_not_relabelled_four_four(self):
        beats=[{'t':i,'beat':b} for i,b in enumerate([1,2,3,1,2,3,1])]
        self.assertEqual(r.four_four_bars(beats),[])

    def test_noteclass_subset_is_explicit_and_allows_extras(self):
        times={36:[0,1,1.9],38:[.5,1.5],42:[i*.25 for i in range(8)]}
        self.assertEqual(r.role_subset([0,.5,1,1.5,2],times),{'kick_snare_subset':True,'closed_hat_eighth_subset':True,'combined_subset':True})

    def test_percussion_presence_alone_is_not_backbeat_subset(self):
        result=r.role_subset([0,.5,1,1.5,2],{36:[.25],38:[.75],42:[.1]})
        self.assertFalse(any(result.values()))

    def test_unrelated_note_classes_do_not_become_hat_hits(self):
        result=r.role_subset([0,.5,1,1.5,2],{36:[0,1],38:[.5,1.5],46:[i*.25 for i in range(8)]})
        self.assertTrue(result['kick_snare_subset']);self.assertFalse(result['combined_subset'])

    def test_local_beat_durations_are_used_for_tolerance(self):
        result=r.role_subset([0,.4,.9,1.5,2.2],{36:[0,.9],38:[.4,1.5],42:[0,.2,.4,.65,.9,1.2,1.5,1.85]})
        self.assertTrue(result['combined_subset'])

    def test_invalid_bar_or_tolerance_rejected(self):
        for bar,tol in [([0,1,2,3],.1),([0,1,1,2,3],.1),([0,1,2,3,4],.5)]:
            with self.assertRaises(ValueError):r.role_subset(bar,{},tol)

    def test_full_observations_remain_unapproved(self):
        d=json.loads(r.OUTPUT.read_text(encoding='utf8'));r.validate(d)
        self.assertEqual(len(d['records']),100);self.assertFalse(d['exact_drum_pattern_verified'])

    def test_duplicate_record_and_faked_mapping_approval_rejected(self):
        for mutation in [lambda d:d['records'][0].update(recording_id=d['records'][1]['recording_id']),
                         lambda d:d['records'][0].update(recording_id='UNVERIFIED_RECORDING'),
                         lambda d:d.update(exact_drum_pattern_verified=True),
                         lambda d:d.update(noteclass_mapping_scope='GM1_VERIFIED')]:
            d=json.loads(r.OUTPUT.read_text(encoding='utf8'));mutation(d)
            with self.assertRaises(ValueError):r.validate(d)

    def test_changed_aggregate_does_not_pass_as_new_evidence(self):
        d=json.loads(r.OUTPUT.read_text(encoding='utf8'));d['summary']['PROG-001']['exact']['records_with_both']+=1
        with self.assertRaises(ValueError):r.validate(d)


if __name__=='__main__':unittest.main()
