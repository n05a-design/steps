import copy
import json
import unittest

from scripts.audit_relation_patterns import OUTPUT, aggregate, grid_match, roles, validate


class RelationPatternTests(unittest.TestCase):
    def test_exact_grid_and_extra_event_are_distinct(self):
        self.assertTrue(grid_match([0,1,2,3,4], [1,3], [1,3])['same_note_grid'])
        result = grid_match([0,1,2,3,4], [1,2,3], [1,3])
        self.assertTrue(result['subset'])
        self.assertFalse(result['same_note_grid'])

    def test_next_bar_downbeat_cannot_cover_last_skip(self):
        self.assertEqual(grid_match([0,1,2,3,4], [4], [3.95])['matched'], 0)

    def test_previous_bar_hit_is_excluded(self):
        self.assertEqual(grid_match([4,5,6,7,8], [3.99], [0])['matched'], 0)

    def test_single_hit_is_not_reused(self):
        self.assertEqual(grid_match([0,1,2,3,4], [1.05], [1,1.1])['matched'], 1)

    def test_local_quarter_tolerance(self):
        self.assertTrue(grid_match([0,1,3,4,5], [2.18], [1.5])['subset'])
        self.assertFalse(grid_match([0,1,3,4,5], [2.21], [1.5])['subset'])

    def test_invalid_or_unordered_input_rejected(self):
        for grid, times, phases in [([0,1,1,3,4], [], [0]), ([0,1,2,3,4], [2,1], [0]),
                                    ([0,1,2,3,4], [float('nan')], [0]), ([0,1,2,3,4], [], [4])]:
            with self.subTest(grid=grid, times=times, phases=phases), self.assertRaises(ValueError):
                grid_match(grid, times, phases)

    def test_overlapping_harmony_windows_do_not_duplicate_bars(self):
        bars = [[0,1,2,3,4], [4,5,6,7,8]]
        result = aggregate(bars, {}, [(0,8),(0,8),(0,4)], 'REL-001')
        self.assertEqual(result['unique_complete_bars_in_harmony_windows'], 2)

    def test_literal_snare38_does_not_accept40(self):
        self.assertFalse(roles([0,1,2,3,4], {40:[1,3]}, 'REL-001')['snare_38']['subset'])

    def test_triplet_skip_is_separate_from_quarter_ride(self):
        result = roles([0,1,2,3,4], {51:[0,1,2,3],44:[1,3]}, 'REL-005')
        self.assertTrue(result['ride_quarters_51']['subset'])
        self.assertFalse(result['ride_triplet_skip_51_proposal']['subset'])

    def test_versioned_receipt_and_premature_acceptance(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8')); validate(data)
        for key in ('historical_assertion_closed','instrument_mapping_verified','exact_pattern_verified','sampling_prevalence_verified'):
            bad = copy.deepcopy(data); bad[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError): validate(bad)

    def test_denominator_overclaim_rejected(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8'))
        data['rows'][0]['observation']['counts']['joint_core_subset'] = 999999
        with self.assertRaises(ValueError): validate(data)

    def test_unrelated_recording_with_same_selection_size_rejected(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8'))
        data['rows'][0]['record_id'] = 'UNRELATED_RECORD'
        with self.assertRaises(ValueError): validate(data)

    def test_substituted_member_hash_rejected(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8'))
        data['rows'][0]['source_sha256'] = '0'*64
        with self.assertRaises(ValueError): validate(data)

    def test_bool_is_not_a_bar_denominator(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8'))
        data['rows'][0]['observation']['unique_complete_bars_in_harmony_windows'] = True
        with self.assertRaises(ValueError): validate(data)

    def test_zero_denominator_cannot_hide_tempo(self):
        data = json.loads(OUTPUT.read_text(encoding='utf8'))
        row = next(r for r in data['rows'] if r['observation']['unique_complete_bars_in_harmony_windows']==0)
        row['observation']['bar_average_bpm_min'] = 130
        with self.assertRaises(ValueError): validate(data)


if __name__ == '__main__': unittest.main()
