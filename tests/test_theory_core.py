"""
STEPS Music Theory Core Verification Test Suite (Phase 4.18).

Validates:
- PitchClass arithmetic modulo 12
- NoteSpelling orthography & enharmonic separation (C# vs Db, Fx, Bbb)
- International vs German nomenclature (B/Bb vs H/B)
- ISO 16 acoustics & frequency calculations
- Diatonic vs Chromatic intervals (A4 vs d5) and inversion invariants
- Triad construction and inversions
- Seventh chord qualities, Drop-2 transformations & Shell voicings
- Voice leading metrics (Tymoczko circular, L1 semitone, parallel 5ths/8ths)
"""

import unittest
import math

from src.steps.theory.pitch import (
    PitchClass,
    NoteSpelling,
    midi_to_pitch_class,
    midi_to_frequency,
    frequency_to_midi,
    parse_spelling
)
from src.steps.theory.interval import (
    ChromaticInterval,
    DiatonicInterval,
    semitones_between,
    directed_semitones,
    invert_semitones_modulo12
)
from src.steps.theory.triad import (
    TriadQuality,
    construct_triad,
    invert_triad_voicing,
    get_triad_pitch_class_set
)
from src.steps.theory.seventh import (
    SeventhQuality,
    construct_seventh,
    invert_seventh_voicing,
    make_drop2_voicing,
    make_shell_voicing
)
from src.steps.progression.voice_leading import (
    absolute_semitone_distance,
    circular_pc_distance,
    detect_voice_crossing,
    detect_parallel_fifths_octaves,
    guide_tone_resolution
)


class TestTheoryCoreAcousticsAndPitch(unittest.TestCase):
    """Verifies M01 (Tonsystem, Akustik, Z12) and M02 (Enharmonik & Notenorthographie)."""

    def test_pitch_class_modulo12_arithmetic(self):
        pc0 = PitchClass(0)
        pc12 = PitchClass(12)
        pc14 = PitchClass(14)
        pc_neg = PitchClass(-1)

        self.assertEqual(pc0, 0)
        self.assertEqual(pc12, 0)
        self.assertEqual(pc14, 2)
        self.assertEqual(pc_neg, 11)
        self.assertEqual((pc14 + 11), 1)
        self.assertEqual((pc0 - 1), 11)

    def test_midi_to_frequency_iso16(self):
        # A4 (MIDI 69) must be 440.0 Hz
        self.assertAlmostEqual(midi_to_frequency(69), 440.0, places=4)
        # A5 (MIDI 81) must be 880.0 Hz
        self.assertAlmostEqual(midi_to_frequency(81), 880.0, places=4)
        # A3 (MIDI 57) must be 220.0 Hz
        self.assertAlmostEqual(midi_to_frequency(57), 220.0, places=4)
        # Middle C (C4, MIDI 60) ≈ 261.6256 Hz
        self.assertAlmostEqual(midi_to_frequency(60), 261.6256, places=3)

    def test_frequency_to_midi_roundtrip(self):
        for midi_val in (36, 48, 60, 69, 72, 84):
            freq = midi_to_frequency(midi_val)
            recovered = round(frequency_to_midi(freq))
            self.assertEqual(midi_val, recovered)

    def test_enharmonic_separation_cs_vs_db(self):
        c_sharp = NoteSpelling(step='C', alteration=1, octave=4)
        d_flat = NoteSpelling(step='D', alteration=-1, octave=4)

        # Both share the same chromatic pitch class 1 in Z12
        self.assertEqual(c_sharp.pitch_class, 1)
        self.assertEqual(d_flat.pitch_class, 1)
        self.assertEqual(c_sharp.midi_number, d_flat.midi_number)

        # But their diatonic steps are strictly distinct!
        self.assertNotEqual(c_sharp.step, d_flat.step)
        self.assertEqual(c_sharp.step, 'C')
        self.assertEqual(d_flat.step, 'D')

    def test_double_accidentals_and_enharmonics(self):
        # F double sharp (Fx) has pitch class 7 (G) but step 'F'
        f_x = NoteSpelling(step='F', alteration=2, octave=4)
        self.assertEqual(f_x.pitch_class, 7)
        self.assertEqual(f_x.step, 'F')
        self.assertEqual(f_x.render('INT'), 'Fx4')

        # B double flat (Bbb) has pitch class 9 (A) but step 'B'
        b_bb = NoteSpelling(step='B', alteration=-2, octave=4)
        self.assertEqual(b_bb.pitch_class, 9)
        self.assertEqual(b_bb.step, 'B')
        self.assertEqual(b_bb.render('INT'), 'Bbb4')

    def test_international_vs_german_nomenclature(self):
        # International B natural (PC 11) is German H
        b_natural = NoteSpelling(step='B', alteration=0, octave=4)
        self.assertEqual(b_natural.render('INT'), 'B4')
        self.assertEqual(b_natural.render('DE'), 'H4')

        # International B flat (PC 10) is German B
        b_flat = NoteSpelling(step='B', alteration=-1, octave=4)
        self.assertEqual(b_flat.render('INT'), 'Bb4')
        self.assertEqual(b_flat.render('DE'), 'B4')

        # German inflections: Es, As, Fis, Fisis
        e_flat = NoteSpelling(step='E', alteration=-1, octave=4)
        self.assertEqual(e_flat.render('DE'), 'Es4')

        a_flat = NoteSpelling(step='A', alteration=-1, octave=4)
        self.assertEqual(a_flat.render('DE'), 'As4')

        f_sharp = NoteSpelling(step='F', alteration=1, octave=4)
        self.assertEqual(f_sharp.render('DE'), 'Fis4')

        f_double_sharp = NoteSpelling(step='F', alteration=2, octave=4)
        self.assertEqual(f_double_sharp.render('DE'), 'Fisis4')


class TestTheoryCoreIntervals(unittest.TestCase):
    """Verifies interval math, diatonic distinctions, and inversions."""

    def test_interval_inversion_modulo12_invariant(self):
        for s in range(12):
            inv = invert_semitones_modulo12(s)
            self.assertEqual((s + inv) % 12, 0, f"Invariant failed for interval {s}")

    def test_diatonic_interval_semitones_and_inversion(self):
        # Perfect Fifth (P5) = 7 semitones -> invert -> Perfect Fourth (P4) = 5 semitones
        p5 = DiatonicInterval(number=5, quality='P')
        self.assertEqual(p5.semitones, 7)
        p4 = p5.invert()
        self.assertEqual(p4.number, 4)
        self.assertEqual(p4.quality, 'P')
        self.assertEqual(p4.semitones, 5)

        # Major Third (M3) = 4 semitones -> invert -> Minor Sixth (m6) = 8 semitones
        m3 = DiatonicInterval(number=3, quality='M')
        self.assertEqual(m3.semitones, 4)
        m6 = m3.invert()
        self.assertEqual(m6.number, 6)
        self.assertEqual(m6.quality, 'm')
        self.assertEqual(m6.semitones, 8)

    def test_tritone_diatonic_distinction_a4_vs_d5(self):
        # Both Augmented 4th (A4) and Diminished 5th (d5) have 6 semitones
        a4 = DiatonicInterval(number=4, quality='A')
        d5 = DiatonicInterval(number=5, quality='d')

        self.assertEqual(a4.semitones, 6)
        self.assertEqual(d5.semitones, 6)

        # But their diatonic spans and inversions are distinct:
        self.assertNotEqual(a4.number, d5.number)
        self.assertEqual(a4.invert(), d5)
        self.assertEqual(d5.invert(), a4)


class TestTheoryCoreTriadsAndSevenths(unittest.TestCase):
    """Verifies triad construction, inversions, seventh chords, Drop-2, and Shells."""

    def test_triad_construction_qualities(self):
        # C Major: [0, 4, 7]
        c_maj = construct_triad(0, TriadQuality.MAJOR)
        self.assertEqual([int(p) for p in c_maj], [0, 4, 7])

        # A Minor: A (9), C (0), E (4) -> [9, 0, 4]
        a_min = construct_triad(9, TriadQuality.MINOR)
        self.assertEqual([int(p) for p in a_min], [9, 0, 4])

        # C Sus4: [0, 5, 7]
        c_sus4 = construct_triad(0, TriadQuality.SUS4)
        self.assertEqual([int(p) for p in c_sus4], [0, 5, 7])

        # C Add9: [0, 2, 4, 7]
        c_add9 = construct_triad(0, TriadQuality.ADD9)
        self.assertEqual([int(p) for p in c_add9], [0, 2, 4, 7])

    def test_triad_inversion_voicing(self):
        # Root position C-Dur: [60, 64, 67] (C4, E4, G4)
        v0 = [60, 64, 67]
        # 1st inversion (6/3): [64, 67, 72] (E4, G4, C5)
        v1 = invert_triad_voicing(v0, 1)
        self.assertEqual(v1, [64, 67, 72])
        # 2nd inversion (6/4): [67, 72, 76] (G4, C5, E5)
        v2 = invert_triad_voicing(v0, 2)
        self.assertEqual(v2, [67, 72, 76])

    def test_seventh_chord_construction(self):
        # G Dominant 7: G (7), B (11), D (2), F (5) -> [7, 11, 2, 5]
        g7 = construct_seventh(7, SeventhQuality.DOMINANT_SEVENTH)
        self.assertEqual([int(p) for p in g7], [7, 11, 2, 5])

        # C Maj7: C (0), E (4), G (7), B (11) -> [0, 4, 7, 11]
        c_maj7 = construct_seventh(0, SeventhQuality.MAJOR_SEVENTH)
        self.assertEqual([int(p) for p in c_maj7], [0, 4, 7, 11])

        # Dm7: D (2), F (5), A (9), C (0) -> [2, 5, 9, 0]
        dm7 = construct_seventh(2, SeventhQuality.MINOR_SEVENTH)
        self.assertEqual([int(p) for p in dm7], [2, 5, 9, 0])

    def test_drop2_voicing_transformation(self):
        # Close position Dm7: [F4, A4, C5, D5] = [65, 69, 72, 74]
        close_dm7 = [65, 69, 72, 74]
        # Voice 2 from top is C5 (72). Drops an octave to C4 (60).
        # Expected Drop-2: [60, 65, 69, 74] (C4, F4, A4, D5)
        drop2_dm7 = make_drop2_voicing(close_dm7)
        self.assertEqual(drop2_dm7, [60, 65, 69, 74])

    def test_shell_voicing_separation(self):
        # C7 shell: LH Root C (MIDI 36), RH Guide Tones E (4) and Bb (10)
        lh, (rh_3rd, rh_7th) = make_shell_voicing(36, SeventhQuality.DOMINANT_SEVENTH)
        self.assertEqual(lh, 36)
        self.assertEqual(rh_3rd % 12, 4)   # E
        self.assertEqual(rh_7th % 12, 10)  # Bb


class TestProgressionVoiceLeading(unittest.TestCase):
    """Verifies M06 voice leading metrics, Tymoczko distances, and contrapuntal rules."""

    def test_absolute_semitone_and_tymoczko_circular_distance(self):
        # Transition C-Dur -> G/B:
        # C-Dur: [C4, E4, G4] = [60, 64, 67]
        # G/B:   [B3, D4, G4] = [59, 62, 67]
        # Distances: C4 -> B3 (1), E4 -> D4 (2), G4 -> G4 (0).
        # Sum = 1 + 2 + 0 = 3 semitones.
        c_dur = [60, 64, 67]
        g_b = [59, 62, 67]

        self.assertEqual(absolute_semitone_distance(c_dur, g_b), 3)
        self.assertEqual(circular_pc_distance(c_dur, g_b), 3)

    def test_voice_crossing_detection(self):
        un_crossed = [48, 60, 64, 67]
        crossed = [48, 65, 64, 67]  # voice 1 (65) > voice 2 (64)!

        self.assertFalse(detect_voice_crossing(un_crossed))
        self.assertTrue(detect_voice_crossing(crossed))

    def test_parallel_fifths_octaves_detection(self):
        # Parallel fifths:
        # Chord 1: Bass=C3 (48), Tenor=G3 (55) -> interval 7
        # Chord 2: Bass=D3 (50), Tenor=A3 (57) -> interval 7
        chord1 = [48, 55, 60, 64]
        chord2 = [50, 57, 62, 65]

        violations = detect_parallel_fifths_octaves(chord1, chord2)
        self.assertTrue(any("Parallel fifth" in v for v in violations))


if __name__ == '__main__':
    unittest.main()
