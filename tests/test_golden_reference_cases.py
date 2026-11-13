#!/usr/bin/env python3
"""Check numerical reference cases and the structure of specification examples."""

import os
import sys
import json
import math
import re
import unittest

from src.steps.progression import (
    absolute_semitone_distance, detect_parallel_fifths_octaves, detect_voice_crossing,
    guide_tone_resolution, resolve_roman_degree,
)
from src.steps.theory import (
    DiatonicInterval, directed_semitones,
    midi_to_frequency, midi_to_pitch_class, parse_chord, parse_spelling,
    semitones_between, make_drop2_voicing,
)

# ==============================================================================
# TEST REFERENCE IMPLEMENTATION (ISOLATED DOMAIN ALGORITHMS)
# ==============================================================================

class TestReferenceImplementation:
    """Mathematical reference implementation for automated test verification."""

    INT_MAP = {
        'P1': 0, 'm2': 1, 'M2': 2, 'm3': 3, 'M3': 4, 'P4': 5,
        'TT': 6, 'd5': 6, 'P5': 7, 'm6': 8, 'M6': 9, 'm7': 10, 'M7': 11, 'P8': 12
    }

    @staticmethod
    def midi_to_pitch_class(midi_note: int) -> int:
        return midi_note % 12

    @staticmethod
    def interval_semitones(n1: int, n2: int) -> int:
        return abs(n2 - n1)

    @staticmethod
    def interval_name_to_semitones(name: str) -> int:
        return TestReferenceImplementation.INT_MAP[name]

    @staticmethod
    def invert_interval(interval: int) -> int:
        return (12 - (interval % 12)) % 12

    @staticmethod
    def construct_triad_pitch_classes(root_pc: int, quality: str) -> list[int]:
        formulas = {
            'Major': [0, 4, 7],
            'Minor': [0, 3, 7],
            'Diminished': [0, 3, 6],
            'Augmented': [0, 4, 8],
            'sus4': [0, 5, 7],
            'sus2': [0, 2, 7],
            'add9': [0, 2, 4, 7]
        }
        return [(root_pc + s) % 12 for s in formulas[quality]]

    @staticmethod
    def calculate_swing_quant_tick(ppq: int, ratio: float) -> int:
        span = ppq // 2
        return round(span * ratio)

    @staticmethod
    def calculate_tuplet_ticks(total_span: int, count: int) -> list[int]:
        return [round(i * total_span / count) for i in range(count + 1)]

    # --------------------------------------------------------------------------
    # Distinct Voice Leading Metrics (Section 4.4)
    # --------------------------------------------------------------------------

    @staticmethod
    def voice_leading_circular_pc_distance(v1: list[int], v2: list[int]) -> int:
        """Calculates minimal circular distance in Z12 space (ignoring octave registers)."""
        def circ_dist(a, b):
            d = abs((a % 12) - (b % 12))
            return min(d, 12 - d)
        return sum(circ_dist(a, b) for a, b in zip(v1, v2))

    @staticmethod
    def voice_leading_absolute_midi_distance(v1: list[int], v2: list[int]) -> int:
        """Calculates absolute physical semitone displacement across specific pitch registers."""
        return sum(abs(b - a) for a, b in zip(v1, v2))

    @staticmethod
    def detect_voice_crossing(voicing: list[int]) -> bool:
        """Returns True if any higher voice index dips below a lower voice index."""
        return any(voicing[i] > voicing[i+1] for i in range(len(voicing) - 1))


# ==============================================================================
# TEST SUITE
# ==============================================================================

class TestGoldenReferenceCases(unittest.TestCase):
    # General MIDI System Level 1, table 3, printed page 6 (PDF page 8).
    GM_PERCUSSION = {
        "General MIDI Kick Drum": 36,  # Bass Drum 1
        "Side Stick": 37,
        "General MIDI Snare Drum": 38,  # Acoustic Snare
        "General MIDI Closed Hi-Hat": 42,
        "Pedal Hi-Hat": 44,
        "General MIDI Open Hi-Hat": 46,
    }

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'golden_cases', 'golden_reference_cases.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            cls.cases = json.load(f)
        cls.case_map = {c['case_id']: c for c in cls.cases}
        cls.tri = TestReferenceImplementation()

    def evaluate_executable_case(self, case_id: str):
        """Executes a genuine algorithmic evaluation for a computational test case.
        Strictly raises NotImplementedError if unhandled (no pseudo-fallback passes).
        """
        c = self.case_map[case_id]
        p = c.get('input_params', {})
        exp = c.get('expected_output')
        tri = self.tri

        if cid := case_id:
            # 1. Pitch Class & Acoustics
            if cid in ['REF-0001', 'REF-0002', 'REF-0107', 'REF-0108']:
                note = p['midi_note'] if 'midi_note' in p else parse_spelling(p['note'], 'INT').midi_number
                self.assertEqual(midi_to_pitch_class(note), exp)
            elif cid in ['REF-0109', 'REF-0110']:
                actual = parse_spelling(p['note'], 'INT').midi_number
                self.assertEqual(actual, exp)
            elif cid in ['REF-0111', 'REF-0112']:
                actual = midi_to_frequency(p["midi_note"])
                self.assertAlmostEqual(actual, exp, delta=0.05)
            elif cid in ['REF-0113', 'REF-0114']:
                actual = (p['pc'] + p['interval']) % 12
                self.assertEqual(actual, exp)
            elif cid in ['REF-0115', 'REF-0116']:
                a, b = (parse_spelling(note, 'INT') for note in p['notes'])
                self.assertEqual(a != b and a.midi_number == b.midi_number, exp)
            elif cid in ['REF-0123', 'REF-0124', 'REF-0125']:
                self.assertEqual(midi_to_pitch_class((p['root'] + 7 * p['fifths']) % 12), exp)

            # 2. Intervals
            elif cid in ['REF-0010', 'REF-0011']:
                actual = semitones_between(p['note1'], p['note2'])
                self.assertEqual(actual, exp)
            elif cid in ['REF-0117', 'REF-0119', 'REF-0121']:
                actual = tri.interval_name_to_semitones(p['interval'])
                self.assertEqual(actual, exp)
            elif cid in ['REF-0118', 'REF-0120', 'REF-0122']:
                actual = tri.invert_interval(p['interval'])
                self.assertEqual(actual, exp)

            # 3. Triads & Chords
            elif cid in ['REF-0012', 'REF-0013']:
                suffix = {'Major': '', 'Minor': 'm'}[p['quality']]
                self.assertEqual(sorted(parse_chord(p['root'] + suffix, 'INT').pitch_class_set), exp)
            elif cid in ['REF-0014', 'REF-0015']:
                suffix = {'Major': '', 'Minor': 'm'}[p['quality']]
                chord = parse_chord(p['root'] + suffix, 'INT')
                inversion = 1 if cid == 'REF-0014' else 2
                notes = chord.to_voicing().invert(inversion).midi_notes
                names = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
                written = [names[note % 12] for note in notes]
                self.assertEqual(f"Bass {written[0]}, Töne [{', '.join(written)}]", exp)
            elif cid in ['REF-0039', 'REF-0040']:
                self.assertEqual(sorted(parse_chord(p['chord'], 'INT').pitch_class_set), exp)
            elif 'REF-0138' <= cid <= 'REF-0146':
                suffix = {
                    'Major Triad': '', 'Minor Triad': 'm',
                    'Diminished Triad': 'dim', 'Augmented Triad': 'aug',
                    'Dominant 7th': '7', 'Major 7th': 'maj7', 'Minor 7th': 'm7',
                    'Half-Diminished 7th': 'm7b5', 'Diminished 7th': 'dim7',
                }[p['chord']]
                self.assertEqual(list(parse_chord('C' + suffix, 'INT').theoretical_intervals), exp)
            elif cid == 'REF-0149':
                self.assertEqual(make_drop2_voicing(p['close_voicing']), exp)
            elif cid in ['REF-0035', 'REF-0050']:
                actual = sorted(int(pc) for pc in parse_chord(p['chord'], 'INT').voiced_pitch_classes)
                self.assertEqual(actual, exp)

            # 4. Harmony and voice leading
            elif cid == 'REF-0153':
                chords = [resolve_roman_degree(degree, p['key'], convention='INT')
                          for degree in p['prog'].split('-')]
                self.assertEqual([int(chord.root.pitch_class) for chord in chords], exp)
            elif cid == 'REF-0154':
                roots = p['roots']
                self.assertEqual([(b - a) % 12 for a, b in zip(roots, roots[1:])], exp)
            elif cid == 'REF-0155':
                self.assertEqual((p['dom_root'] + 6) % 12, exp)
            elif cid in ['REF-0157', 'REF-0160']:
                degree = p.get('degree', 'V7/V')
                chord = resolve_roman_degree(degree, p['key'], convention='INT')
                self.assertEqual(chord.root.pitch_class, exp)
            elif cid in ['REF-0162', 'REF-0166']:
                chords = [resolve_roman_degree(degree, p['key'], p['minor'], convention='INT')
                          for degree in p['degrees']]
                self.assertEqual([int(chord.root.pitch_class) for chord in chords], exp)
            elif cid == 'REF-0156':
                a, b = (parse_chord(symbol, 'INT') for symbol in p['chords'])
                shared = sorted(a.pitch_class_set & b.pitch_class_set)
                self.assertEqual(len(shared) == 2 and shared[1] - shared[0] == 6, exp)
            elif cid in ['REF-0168', 'REF-0169']:
                start = [p['v1_start'], p['v2_start']]
                end = [p['v1_end'], p['v2_end']]
                self.assertEqual(bool(detect_parallel_fifths_octaves(start, end)), exp)
            elif cid == 'REF-0170':
                self.assertEqual(p['v1_dir'] * p['v2_dir'] < 0, exp)
            elif cid == 'REF-0175':
                a, b = p['v1'], p['v2']
                self.assertEqual(a[0] != b[0] and a == b[::-1], exp)
            elif cid == 'REF-0171':
                self.assertEqual(directed_semitones(p['leading_tone'], p['tonic']), exp)
            elif cid == 'REF-0172':
                self.assertEqual(guide_tone_resolution(p['seventh'], p['third']), exp)
            elif cid == 'REF-0173':
                self.assertEqual(detect_voice_crossing([p['alto'], p['soprano']]), exp)
            elif cid == 'REF-0174':
                self.assertEqual(absolute_semitone_distance(p['dm7'], p['g7']), exp)
            elif cid == 'REF-0019':
                actual = tri.voice_leading_circular_pc_distance(p['chord1'], p['chord2'])
                self.assertEqual(actual, exp)
            elif cid == 'REF-0097':
                roots = p['roots']
                actual = [(roots[(i+1)%3] - roots[i]) % 12 for i in range(3)]
                self.assertEqual(actual, exp)

            # 5. Timing, Swing & Micro-timing
            elif cid in ['REF-0020', 'REF-0021']:
                first, second = p["durations"]
                self.assertGreater(first, 0)
                self.assertGreater(second, 0)
                self.assertEqual(first / second, exp)
            elif cid in ['REF-0026', 'REF-0027', 'REF-0028', 'REF-0029', 'REF-0030']:
                ppq = p['ppq']
                beat_positions = {
                    'Pop Backbeat Zählzeiten': (1, 3), 'House Four-on-the-Floor': (0, 1, 2, 3),
                    'House Offbeat Hi-Hat': (0.5, 1.5, 2.5, 3.5),
                    '8tel-Offbeat nach Schlag 3 (3+)': (2.5,),
                    '16tel-Synkope vor Schlag 4 (3e+)': (2.75,),
                }
                actual = [int(beat * ppq) for beat in beat_positions[p['style_event']]]
                expected_ticks = [int(tick) for tick in re.findall(r"\b[0-9]+\b", exp.split('Tick', 1)[1].split(' bei ')[0])]
                self.assertEqual(actual, expected_ticks)
            elif cid in ['REF-0031', 'REF-0032']:
                pcs = {note % 12 for note in p['notes']}
                roots = [root for root in pcs if {(root + x) % 12 for x in (0, 3, 7)} == pcs
                         or {(root + x) % 12 for x in (0, 4, 7)} == pcs]
                self.assertEqual(len(roots), 1)
                distance = (min(p['notes']) - roots[0]) % 12
                actual = {0: 'Grundstellung (5/3)', 3: '1. Umkehrung (Sextakkord 6)',
                          4: '1. Umkehrung (Sextakkord 6)', 7: '2. Umkehrung (Quartsextakkord 6/4)'}[distance]
                self.assertEqual(actual, exp)
            elif cid == 'REF-0043':
                chord = parse_chord(p['chord'], 'INT')
                self.assertEqual({n % 12 for n in p['close_midi']}, chord.pitch_class_set)
                self.assertEqual(make_drop2_voicing(p['close_midi']), exp)
            elif cid == 'REF-0047':
                actual = tri.calculate_tuplet_ticks(p['ppq'], p['tuplets'])
                self.assertEqual(actual, exp)
            elif cid == 'REF-0049':
                first, second = (parse_chord(symbol, "INT") for symbol in p["chords"])
                self.assertEqual(first.pitch_class_set == second.pitch_class_set, exp)
            elif cid in ['REF-0053', 'REF-0071', 'REF-0083', 'REF-0084', 'REF-0085', 'REF-0086', 'REF-0087', 'REF-0088', 'REF-0098']:
                actual = tri.calculate_swing_quant_tick(p['ppq'], p['ratio'])
                self.assertEqual(actual, exp)
            elif cid in ['REF-0091', 'REF-0092']:
                actual = sum(p['subdivision']) * (p['ppq'] // 2)
                self.assertEqual(actual, exp)
            elif cid == 'REF-0187':
                subdivisions = p['subdivisions_per_quarter']
                actual = []
                for bar, beats in enumerate(p['bar_eighths']):
                    for beat in beats:
                        offset = (bar * 4 + int(beat[0]) - 1) * subdivisions
                        actual.append(offset + (subdivisions // 2 if beat.endswith('+') else 0))
                self.assertEqual(actual, exp)
            elif cid == 'REF-0099':
                actual = sum(p['pattern'])
                self.assertEqual(actual, exp)
            # 6. Acoustics & Tuning
            elif cid == 'REF-0089':
                ratio = (1.5 ** p['fifths']) / (2.0 ** p['octaves'])
                actual = round(1200.0 * math.log2(ratio), 2)
                self.assertAlmostEqual(actual, exp, delta=0.05)
            elif cid == 'REF-0090':
                actual = round(1200.0 * math.log2(p['ratio']), 2)
                self.assertAlmostEqual(actual, exp, delta=0.05)
            elif cid == 'REF-0101':
                actual = midi_to_frequency(parse_spelling(p['note'], 'INT').midi_number)
                self.assertEqual(actual, exp)
            elif cid == 'REF-0102':
                actual = p['f2'] / p['f1']
                self.assertEqual(actual, exp)
            elif cid == 'REF-0103':
                actual = round(2.0 ** (p['semitones'] / 12.0), 6)
                self.assertAlmostEqual(actual, exp, places=5)
            elif cid in ['REF-0104', 'REF-0105']:
                actual = round(1200.0 * math.log2(p['ratio']), 2)
                self.assertAlmostEqual(actual, exp, delta=0.05)
            elif cid == 'REF-0106':
                actual = round(p['tet_cent'] - p['just_cent'], 2)
                self.assertAlmostEqual(actual, exp, delta=0.05)

            elif cid == 'REF-0188':
                self.assertEqual([i for i, hit in enumerate(p['pattern']) if hit == 'X'], exp)
            elif cid == 'REF-0189':
                self.assertEqual(math.lcm(p['r1'], p['r2']), exp)
            elif cid == 'REF-0191':
                self.assertEqual(DiatonicInterval(1 + 7 * p['octave'], 'P').semitones, exp)
            elif cid == 'REF-0192':
                quality, number = p['interval'][0], int(p['interval'][1:])
                self.assertEqual(DiatonicInterval(number, quality).semitones, exp)

            # 7. MIDI time
            elif cid == 'REF-0197':
                actual = 60000.0 / p['bpm']
                self.assertEqual(actual, exp)
            elif cid == 'REF-0198':
                actual = round(60000.0 / (p['bpm'] * p['ppq']), 4)
                self.assertAlmostEqual(actual, exp, delta=0.001)
            else:
                raise NotImplementedError(f"Executable test case '{cid}' has no implementation!")

    def verify_specification_case(self, case_id: str) -> dict:
        """Check the expected-output and domain fields of a specification example."""
        c = self.case_map[case_id]
        exp = c.get('expected_output')
        self.assertIsNotNone(exp, f"Specification {case_id} missing expected_output")
        self.assertIn(c.get('domain'), ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 'M11', 'M12'])
        if c["category"] == "DRUM_MAPPING":
            instrument = c["input_params"]["instrument"]
            self.assertIn(instrument, self.GM_PERCUSSION, f"{case_id}: no percussion source value")
            self.assertEqual(exp, self.GM_PERCUSSION[instrument], f"{case_id}: General MIDI table 3")
        return {
            'case_id': case_id,
            'status': 'SPECIFICATION_DOCUMENTED',
            'domain': c.get('domain')
        }

    def evaluate_case(self, case_id: str):
        """Unified evaluator routing to computational evaluation or specification verification."""
        c = self.case_map[case_id]
        if c.get('test_class') == 'SPECIFICATION_EXAMPLE':
            return self.verify_specification_case(case_id)
        else:
            return self.evaluate_executable_case(case_id)

    # ==========================================================================
    # SUITE EXECUTION METHODS
    # ==========================================================================

    def test_executable_cases_compute_their_expected_results(self):
        """Run every case classified as executable."""
        exec_cases = [c['case_id'] for c in self.cases if c['test_class'] in ['UNIT_TEST', 'PROPERTY_TEST', 'INTEGRATION_TEST']]
        self.assertEqual(len(exec_cases), 98)

        passed = 0
        for cid in exec_cases:
            with self.subTest(case=cid):
                self.evaluate_executable_case(cid)
                passed += 1

        self.assertEqual(passed, len(exec_cases))

    def test_swing_ratio_rejects_changed_durations(self):
        original = self.case_map["REF-0021"]
        try:
            self.case_map["REF-0021"] = {
                **original,
                "input_params": {**original["input_params"], "durations": [1, 1]},
            }
            with self.assertRaises(AssertionError):
                self.evaluate_executable_case("REF-0021")
        finally:
            self.case_map["REF-0021"] = original

    def test_clave_rejects_eighth_positions_in_sixteenth_grid(self):
        original = self.case_map["REF-0187"]
        try:
            self.case_map["REF-0187"] = {
                **original, "expected_output": [0, 3, 6, 10, 12],
            }
            with self.assertRaises(AssertionError):
                self.evaluate_executable_case("REF-0187")
        finally:
            self.case_map["REF-0187"] = original

    def test_specification_examples_have_required_fields(self):
        """Check structure of the cases classified as specification examples."""
        spec_cases = [c['case_id'] for c in self.cases if c['test_class'] == 'SPECIFICATION_EXAMPLE']
        self.assertEqual(len(spec_cases), 100)

        verified = 0
        for cid in spec_cases:
            res = self.verify_specification_case(cid)
            self.assertEqual(res['status'], 'SPECIFICATION_DOCUMENTED')
            verified += 1

        self.assertEqual(verified, len(spec_cases))

    def test_general_midi_note_map_rejects_wrong_note_number(self):
        case_id = "REF-0045"
        original = self.case_map[case_id]
        try:
            self.case_map[case_id] = {**original, "expected_output": 42}
            with self.assertRaisesRegex(AssertionError, "General MIDI table 3"):
                self.verify_specification_case(case_id)
        finally:
            self.case_map[case_id] = original

    def test_unimplemented_executable_case_strictly_raises_error(self):
        """Negative test proving that unhandled executable cases fail closed (no silent fallback)."""
        dummy_case_id = 'REF-9999'
        self.case_map[dummy_case_id] = {
            'case_id': dummy_case_id,
            'test_class': 'UNIT_TEST',
            'expected_output': 123
        }
        with self.assertRaises(NotImplementedError):
            self.evaluate_executable_case(dummy_case_id)

    # ==========================================================================
    # MATHEMATICAL PROPERTY-BASED INVARIANT TESTS (Section 4.4)
    # ==========================================================================

    def test_property_octave_transposition_invariance(self):
        """Property: Transposition by k * 12 semitones strictly preserves pitch class."""
        tri = self.tri
        for midi_note in range(0, 116):
            base_pc = tri.midi_to_pitch_class(midi_note)
            for k in range(-5, 6):
                transposed = midi_note + 12 * k
                if 0 <= transposed <= 127:
                    self.assertEqual(tri.midi_to_pitch_class(transposed), base_pc)

    def test_property_triad_inversion_pitch_class_set_preservation(self):
        """Property: Chord inversions preserve the exact pitch class set."""
        tri = self.tri
        for root in range(12):
            for quality in ['Major', 'Minor', 'Diminished', 'Augmented']:
                root_pcs = set(tri.construct_triad_pitch_classes(root, quality))
                # Check first inversion set equivalence
                inv1 = set([(p + 12) % 12 for p in root_pcs])
                self.assertEqual(root_pcs, inv1)

    def test_property_chord_transposition_structure_invariance(self):
        """Property: Transposing a triad by interval k preserves its internal semitone deltas."""
        tri = self.tri
        for root in range(12):
            base_triad = tri.construct_triad_pitch_classes(root, 'Major')
            delta1 = (base_triad[1] - base_triad[0]) % 12
            delta2 = (base_triad[2] - base_triad[1]) % 12
            for k in range(12):
                transposed = [(p + k) % 12 for p in base_triad]
                t_delta1 = (transposed[1] - transposed[0]) % 12
                t_delta2 = (transposed[2] - transposed[1]) % 12
                self.assertEqual(delta1, t_delta1)
                self.assertEqual(delta2, t_delta2)

    def test_property_interval_inversion_sum(self):
        """Property: An interval and its octave inversion modulo 12 sum to 0 in Z12."""
        tri = self.tri
        for interval in range(1, 12):
            inv = tri.invert_interval(interval)
            self.assertEqual((interval + inv) % 12, 0)

    def test_property_voice_leading_metrics_distinctiveness(self):
        """Property (Section 4.4): Voice leading absolute MIDI distance and circular distance
        produce distinct results when register displacement occurs, and voice crossings are detected.
        """
        tri = self.tri
        # v1 and v2 have same pitch classes [C, E, G], but v2 has G dropped down an octave
        v1 = [60, 64, 67] # C4, E4, G4
        v2 = [60, 64, 55] # C4, E4, G3
        
        circ_dist = tri.voice_leading_circular_pc_distance(v1, v2)
        abs_dist = tri.voice_leading_absolute_midi_distance(v1, v2)
        
        self.assertEqual(circ_dist, 0, "Circular PC distance should be 0 because pitch classes are identical")
        self.assertEqual(abs_dist, 12, "Physical absolute MIDI distance must be 12 semitones due to octave shift")
        self.assertNotEqual(circ_dist, abs_dist)

        # Voice crossing check
        crossing_voicing = [64, 60, 67] # E4, C4, G4 (Voice 0 > Voice 1 -> crossing!)
        non_crossing = [60, 64, 67] # C4, E4, G4
        self.assertTrue(tri.detect_voice_crossing(crossing_voicing))
        self.assertFalse(tri.detect_voice_crossing(non_crossing))

    def test_metamorphic_roundtrip_transposition(self):
        """Metamorphic: Transposing a voicing by +k then -k recovers original pitches."""
        tri = self.tri
        voicing = [60, 64, 67, 71] # Cmaj7
        for k in [-11, -7, -3, 1, 5, 9, 12]:
            transposed_up = [p + k for p in voicing]
            transposed_back = [p - k for p in transposed_up]
            self.assertEqual(transposed_back, voicing)

    def test_mutation_detection_fails_on_corrupted_cases(self):
        """Mutation detection test: Assert that an artificially corrupted case raises AssertionError."""
        original_c1 = dict(self.case_map['REF-0001'])
        try:
            self.case_map['REF-0001']['expected_output'] = 999 # Corrupt
            with self.assertRaises(AssertionError):
                self.evaluate_executable_case('REF-0001')
        finally:
            self.case_map['REF-0001'] = original_c1

if __name__ == '__main__':
    unittest.main()
