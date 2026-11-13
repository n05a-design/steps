"""
STEPS Music Theory Core Verification Test Suite (Phase 5.1).

Validates:
- PitchClass arithmetic modulo 12 & domain exceptions
- NoteSpelling orthography & enharmonic separation (C# vs Db, Fx, Bbb)
- Enharmonic equality predicates
- International vs German nomenclature parsing and rendering (B/Bb vs H/B, Fis, Es, As, Heses)
- ISO 16 acoustics & frequency calculations
- Diatonic vs Chromatic intervals (A4 vs d5), compound intervals (9th, 11th, 13th)
- Interval transpositions and interval_between_spellings
- Triad & Seventh chord constructions & inversions
- Comprehensive chord parser (Triads, Sevenths, Extensions, Slash chords, German chords)
- Lydian dominant 7#11 theoretical pitch-class set vs performance voicings
- Voicing generation styles (CLOSE, DROP2, SHELL, ROOTLESS)
- Voice leading metrics (Tymoczko circular, L1 semitone metric space axioms)
- Smooth voice leading optimizer & voice overlap detection
"""

import unittest
import math

from src.steps.theory.exceptions import (
    MusicTheoryError,
    InvalidPitchClassError,
    InvalidDiatonicStepError,
    InvalidAlterationError,
    PitchRangeError,
    InvalidIntervalError,
    ChordConstructionError,
    VoiceLeadingError,
    ProgressionParsingError
)
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
    invert_semitones_modulo12,
    transpose_spelling,
    interval_between_spellings
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
from src.steps.theory.chord import (
    ChordDefinition,
    Voicing,
    parse_chord,
    CHORD_TEMPLATES
)
from src.steps.progression.voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    circular_pc_distance,
    detect_voice_crossing,
    detect_voice_overlap,
    detect_parallel_fifths_octaves,
    guide_tone_resolution,
    optimize_smooth_voice_leading
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

    def test_pitch_class_exceptions(self):
        with self.assertRaises(InvalidPitchClassError):
            PitchClass("not-an-int")  # type: ignore

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

        # Predicate test
        self.assertTrue(c_sharp.is_enharmonic_with(d_flat))
        
        # Across octaves:
        d_flat_5 = NoteSpelling(step='D', alteration=-1, octave=5)
        self.assertFalse(c_sharp.is_enharmonic_with(d_flat_5, ignore_octave=False))
        self.assertTrue(c_sharp.is_enharmonic_with(d_flat_5, ignore_octave=True))

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

        # German inflections: Es, As, Fis, Fisis, Heses
        e_flat = NoteSpelling(step='E', alteration=-1, octave=4)
        self.assertEqual(e_flat.render('DE'), 'Es4')

        a_flat = NoteSpelling(step='A', alteration=-1, octave=4)
        self.assertEqual(a_flat.render('DE'), 'As4')

        f_sharp = NoteSpelling(step='F', alteration=1, octave=4)
        self.assertEqual(f_sharp.render('DE'), 'Fis4')

        f_double_sharp = NoteSpelling(step='F', alteration=2, octave=4)
        self.assertEqual(f_double_sharp.render('DE'), 'Fisis4')

        b_double_flat = NoteSpelling(step='B', alteration=-2, octave=4)
        self.assertEqual(b_double_flat.render('DE'), 'Heses4')

    def test_german_parsing(self):
        # Parsing German strings
        h4 = parse_spelling('H4', convention='DE')
        self.assertEqual(h4.step, 'B')
        self.assertEqual(h4.alteration, 0)
        self.assertEqual(h4.pitch_class, 11)

        b4_de = parse_spelling('B4', convention='DE')
        self.assertEqual(b4_de.step, 'B')
        self.assertEqual(b4_de.alteration, -1)
        self.assertEqual(b4_de.pitch_class, 10)

        fis4 = parse_spelling('Fis4')
        self.assertEqual(fis4.step, 'F')
        self.assertEqual(fis4.alteration, 1)

        es4 = parse_spelling('Es4')
        self.assertEqual(es4.step, 'E')
        self.assertEqual(es4.alteration, -1)

        as4 = parse_spelling('As4')
        self.assertEqual(as4.step, 'A')
        self.assertEqual(as4.alteration, -1)

        fisis4 = parse_spelling('Fisis4')
        self.assertEqual(fisis4.step, 'F')
        self.assertEqual(fisis4.alteration, 2)

    def test_note_spelling_exceptions(self):
        with self.assertRaises(InvalidDiatonicStepError):
            NoteSpelling(step='X', alteration=0, octave=4)  # type: ignore
        with self.assertRaises(InvalidAlterationError):
            NoteSpelling(step='C', alteration=3, octave=4)


class TestTheoryCoreIntervals(unittest.TestCase):
    """Verifies interval math, diatonic distinctions, compound intervals, and inversions."""

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

    def test_compound_intervals(self):
        # Major 9th: number 9, quality 'M' -> 14 semitones
        m9 = DiatonicInterval(number=9, quality='M')
        self.assertTrue(m9.is_compound)
        self.assertEqual(m9.octaves, 1)
        self.assertEqual(m9.semitones, 14)

        # Perfect 11th: number 11, quality 'P' -> 17 semitones
        p11 = DiatonicInterval(number=11, quality='P')
        self.assertTrue(p11.is_compound)
        self.assertEqual(p11.semitones, 17)

        # Major 13th: number 13, quality 'M' -> 21 semitones
        m13 = DiatonicInterval(number=13, quality='M')
        self.assertTrue(m13.is_compound)
        self.assertEqual(m13.semitones, 21)

    def test_interval_exceptions(self):
        with self.assertRaises(InvalidIntervalError):
            DiatonicInterval(number=0, quality='P')
        # Perfect interval cannot be Major or Minor
        with self.assertRaises(InvalidIntervalError):
            DiatonicInterval(number=5, quality='M')
        # Imperfect interval cannot be Perfect
        with self.assertRaises(InvalidIntervalError):
            DiatonicInterval(number=3, quality='P')
        # Compound interval cannot be directly inverted with invert()
        with self.assertRaises(InvalidIntervalError):
            DiatonicInterval(number=9, quality='M').invert()

    def test_diatonic_transpositions_and_invariants(self):
        c4 = NoteSpelling(step='C', alteration=0, octave=4)
        
        # C4 + P5 (asc) -> G4
        g4 = transpose_spelling(c4, DiatonicInterval(5, 'P'))
        self.assertEqual(g4.step, 'G')
        self.assertEqual(g4.alteration, 0)
        self.assertEqual(g4.octave, 4)

        # C4 + A4 (asc) -> F#4
        fs4 = transpose_spelling(c4, DiatonicInterval(4, 'A'))
        self.assertEqual(fs4.step, 'F')
        self.assertEqual(fs4.alteration, 1)

        # C4 + d5 (asc) -> Gb4
        gb4 = transpose_spelling(c4, DiatonicInterval(5, 'd'))
        self.assertEqual(gb4.step, 'G')
        self.assertEqual(gb4.alteration, -1)

        # C4 + P5 (desc) -> F3
        f3 = transpose_spelling(c4, DiatonicInterval(5, 'P'), direction=-1)
        self.assertEqual(f3.step, 'F')
        self.assertEqual(f3.alteration, 0)
        self.assertEqual(f3.octave, 3)

        # Metamorphic Round-Trip: (C4 + P5) - P5 == C4
        c4_recovered = transpose_spelling(g4, DiatonicInterval(5, 'P'), direction=-1)
        self.assertEqual(c4_recovered, c4)

    def test_interval_between_spellings(self):
        c4 = NoteSpelling(step='C', alteration=0, octave=4)
        g4 = NoteSpelling(step='G', alteration=0, octave=4)
        fs4 = NoteSpelling(step='F', alteration=1, octave=4)
        gb4 = NoteSpelling(step='G', alteration=-1, octave=4)

        int_cg = interval_between_spellings(c4, g4)
        self.assertEqual(int_cg.number, 5)
        self.assertEqual(int_cg.quality, 'P')

        int_cfs = interval_between_spellings(c4, fs4)
        self.assertEqual(int_cfs.number, 4)
        self.assertEqual(int_cfs.quality, 'A')

        int_cgb = interval_between_spellings(c4, gb4)
        self.assertEqual(int_cgb.number, 5)
        self.assertEqual(int_cgb.quality, 'd')


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


class TestTheoryCoreChordEngine(unittest.TestCase):
    """Verifies ChordDefinition, comprehensive chord parsing, and voicing synthesis."""

    def test_sus_chords_respect_explicit_notation(self):
        for suffix, intervals in (("sus", (0, 5, 7)), ("sus2", (0, 2, 7)), ("sus4", (0, 5, 7))):
            for note, convention, root in (("B", "DE", 10), ("H", "DE", 11), ("Bb", "INT", 10), ("B", "INT", 11)):
                with self.subTest(note=note, convention=convention, suffix=suffix):
                    chord = parse_chord(note + suffix, convention)
                    self.assertEqual(chord.root.pitch_class, root)
                    self.assertEqual(chord.pitch_class_set, {(root + i) % 12 for i in intervals})
            for note in ("Asus4", "Esus4"):
                self.assertEqual(parse_chord(note, "DE"), parse_chord(note, "INT"))
            with self.assertRaises(ChordConstructionError):
                parse_chord("H" + suffix, "INT")

    def test_chord_tensions_require_balanced_parentheses(self):
        for symbol in ("C7((b9)", "C7((b9))", "C7(b9", "C7b9)", "C7()"):
            with self.subTest(symbol=symbol), self.assertRaises(ChordConstructionError):
                parse_chord(symbol, "INT")
        self.assertEqual(parse_chord("C7(b9)", "INT").theoretical_intervals, (0, 4, 7, 10, 13))
        self.assertEqual(parse_chord("C7b9", "INT"), parse_chord("C7(b9)", "INT"))

    def test_voicing_invert_rotates_voices_above_original_top(self):
        initial = Voicing((48, 67, 76), "OPEN")
        rotated = initial.invert(1)
        self.assertEqual(rotated.notes, (67, 76, 84))
        self.assertEqual(rotated.bass_note, 67)
        self.assertEqual({n % 12 for n in rotated.notes}, {0, 4, 7})
        self.assertEqual(initial.invert(2).notes, (76, 84, 91))
        self.assertIs(initial.invert(3), initial)
        self.assertEqual(Voicing((48, 52, 55)).invert(1).notes, (52, 55, 60))
        with self.assertRaises(VoiceLeadingError):
            Voicing((120, 124, 127), "OPEN").invert(1)

    def test_parse_standard_chords(self):
        c_maj = parse_chord('C')
        self.assertEqual(c_maj.root.step, 'C')
        self.assertEqual(c_maj.quality, '')
        self.assertEqual(c_maj.pitch_class_set, {0, 4, 7})

        dm = parse_chord('Dm')
        self.assertEqual(dm.root.step, 'D')
        self.assertEqual(dm.pitch_class_set, {2, 5, 9})

        g7 = parse_chord('G7')
        self.assertEqual(g7.root.step, 'G')
        self.assertEqual(g7.pitch_class_set, {7, 11, 2, 5})

        cmaj7 = parse_chord('Cmaj7')
        self.assertEqual(cmaj7.pitch_class_set, {0, 4, 7, 11})

        bm7b5 = parse_chord('Bm7b5', 'INT')
        self.assertEqual(bm7b5.pitch_class_set, {11, 2, 5, 9})

        bdim7 = parse_chord('Bdim7', 'INT')
        self.assertEqual(bdim7.pitch_class_set, {11, 2, 5, 8})

    def test_parse_extended_and_altered_chords(self):
        dm9 = parse_chord('Dm9')
        self.assertEqual(dm9.pitch_class_set, {2, 5, 9, 0, 4})

        g7b9 = parse_chord('G7(b9)')
        self.assertEqual(g7b9.pitch_class_set, {7, 11, 2, 5, 8})

        cadd9 = parse_chord('Cadd9')
        self.assertEqual(cadd9.pitch_class_set, {0, 2, 4, 7})

        csus4 = parse_chord('Csus4')
        self.assertEqual(csus4.pitch_class_set, {0, 5, 7})

    def test_lydian_dominant_7sharp11_theoretical_vs_voiced(self):
        # Golden cases REF-0035, REF-0043, REF-0050:
        # Full theoretical pitch class set: {1, 3, 5, b7, #11} -> {0, 4, 6, 7, 10}
        # Performance voiced intervals (omitting 5th to avoid tritone clutter): {0, 4, 6, 10}
        c7_11 = parse_chord('C7#11')
        self.assertEqual(c7_11.theoretical_intervals, (0, 4, 6, 7, 10))
        self.assertEqual(c7_11.default_voiced_intervals, (0, 4, 6, 10))
        self.assertEqual(c7_11.pitch_class_set, {0, 4, 6, 7, 10})
        self.assertEqual([int(pc) for pc in c7_11.voiced_pitch_classes], [0, 4, 6, 10])

    def test_slash_chords(self):
        c_e = parse_chord('C/E')
        self.assertEqual(c_e.root.step, 'C')
        self.assertIsNotNone(c_e.bass)
        self.assertEqual(c_e.bass.step, 'E')
        self.assertEqual(c_e.symbol, 'C/E')

        g_b = parse_chord('G/B', 'INT')
        self.assertEqual(g_b.root.step, 'G')
        self.assertEqual(g_b.bass.step, 'B')

    def test_german_chord_symbols(self):
        # In German: H7 is B7 international
        h7 = parse_chord('H7', convention='DE')
        self.assertEqual(h7.root.step, 'B')
        self.assertEqual(h7.root.alteration, 0)
        self.assertEqual(h7.quality, '7')

        # In German: Bmaj7 is Bbmaj7 international
        b_maj7 = parse_chord('Bmaj7', convention='DE')
        self.assertEqual(b_maj7.root.step, 'B')
        self.assertEqual(b_maj7.root.alteration, -1)
        self.assertEqual(b_maj7.quality, 'maj7')

    def test_voicing_generation_styles(self):
        cmaj7 = parse_chord('Cmaj7')
        
        # Close voicing
        v_close = cmaj7.to_voicing(bass_octave=3, voicing_type='CLOSE')
        self.assertEqual(v_close.bass_note, 48)  # C3
        self.assertEqual(len(v_close.midi_notes), 4)

        # Shell voicing
        v_shell = cmaj7.to_voicing(bass_octave=3, voicing_type='SHELL')
        self.assertEqual(v_shell.bass_note, 48)
        self.assertEqual(len(v_shell.midi_notes), 3)

        # Drop-2 voicing
        v_drop2 = cmaj7.to_voicing(bass_octave=4, voicing_type='DROP2')
        self.assertEqual(len(v_drop2.midi_notes), 4)

        # Rootless voicing
        v_rootless = cmaj7.to_voicing(voicing_type='ROOTLESS')
        # Does not contain root C
        self.assertNotIn(0, [n % 12 for n in v_rootless.midi_notes])


class TestProgressionVoiceLeading(unittest.TestCase):
    """Verifies M06 voice leading metrics, Tymoczko distances, and contrapuntal rules."""

    def test_metric_space_axioms_for_l1_distance(self):
        v1 = [60, 64, 67, 71]
        v2 = [59, 62, 67, 71]
        v3 = [57, 60, 65, 69]

        # 1. Non-negativity: d(a, b) >= 0
        self.assertGreaterEqual(absolute_semitone_distance(v1, v2), 0)

        # 2. Identity of indiscernibles: d(a, a) == 0
        self.assertEqual(absolute_semitone_distance(v1, v1), 0)

        # 3. Symmetry: d(a, b) == d(b, a)
        self.assertEqual(absolute_semitone_distance(v1, v2), absolute_semitone_distance(v2, v1))

        # 4. Triangle inequality: d(a, c) <= d(a, b) + d(b, c)
        d_ac = absolute_semitone_distance(v1, v3)
        d_ab = absolute_semitone_distance(v1, v2)
        d_bc = absolute_semitone_distance(v2, v3)
        self.assertLessEqual(d_ac, d_ab + d_bc)

    def test_voice_crossing_and_overlap_detection(self):
        un_crossed = [48, 60, 64, 67]
        crossed = [48, 65, 64, 67]  # voice 1 (65) > voice 2 (64)!

        self.assertFalse(detect_voice_crossing(un_crossed))
        self.assertTrue(detect_voice_crossing(crossed))

        # Overlap test:
        chord_a = [48, 60, 64, 67]
        # In chord_b, lowest voice (bass) jumps to 62 (higher than voice 1 was at 60)
        chord_b_overlap = [62, 64, 67, 72]
        self.assertTrue(detect_voice_overlap(chord_a, chord_b_overlap))

    def test_parallel_fifths_octaves_detection(self):
        # Parallel fifths in strict counterpoint:
        chord1 = [48, 55, 60, 64]
        chord2 = [50, 57, 62, 65]

        violations_strict = detect_parallel_fifths_octaves(chord1, chord2, style=VoiceLeadingStyle.STRICT_COUNTERPOINT)
        self.assertTrue(any("Parallel fifth" in v for v in violations_strict))

        # In jazz/pop style: parallel planing is allowed
        violations_jazz = detect_parallel_fifths_octaves(chord1, chord2, style=VoiceLeadingStyle.JAZZ_POP)
        self.assertEqual(len(violations_jazz), 0)

    def test_smooth_voice_leading_optimizer(self):
        # Start with C major close voicing: [48, 64, 67, 72] (C3, E4, G4, C5)
        # Target: G major (pitch classes 7, 11, 2)
        source = [48, 64, 67, 72]
        opt = optimize_smooth_voice_leading(
            source_voicing=source,
            target_pcs={7, 11, 2},
            bass_pc=7,  # G in bass
            style=VoiceLeadingStyle.JAZZ_POP
        )
        self.assertFalse(detect_voice_crossing(opt))
        self.assertEqual(opt[0] % 12, 7)  # G in bass
        dist = absolute_semitone_distance(source, opt)
        # Distance must be small (smooth)
        self.assertLess(dist, 12)


if __name__ == '__main__':
    unittest.main()

