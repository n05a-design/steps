"""
STEPS Progression Engine Verification Test Suite (Phase 5.1).

Validates:
- Loading and integrity of all 28 canonical progressions (PROG-001 through PROG-028)
- Strict preservation and correctness of PROG-021 and PROG-028
- Roman numeral scale degree harmonic resolution in Major and Minor
- Secondary dominants (V7/V, V7/vi) and borrowed modal interchange chords (bII7, iv, bVI, bVII)
- Chromatic transposition of progressions
- Progression voicing generation and voice-leading metric analysis
"""

import unittest

from src.steps.theory.pitch import NoteSpelling, PitchClass
from src.steps.theory.chord import ChordDefinition, Voicing
from src.steps.progression.voice_leading import VoiceLeadingStyle, detect_voice_crossing
from src.steps.progression.engine import (
    CanonicalProgression,
    CANONICAL_PROGRESSIONS,
    get_progression,
    list_progressions,
    resolve_roman_degree,
    generate_progression_voicings,
    analyze_progression_voice_leading
)
from src.steps.theory.exceptions import ProgressionParsingError


class TestCanonicalProgressionRegistry(unittest.TestCase):
    """Verifies that all 28 canonical progression archetypes are present and valid."""

    def test_all_28_progressions_present(self):
        all_progs = list_progressions()
        self.assertEqual(len(all_progs), 28, "Must contain exactly 28 canonical progressions.")
        
        ids = [p.prog_id for p in all_progs]
        expected_ids = [f"PROG-{i:03d}" for i in range(1, 29)]
        self.assertEqual(ids, expected_ids)

    def test_progression_attributes_and_chord_parsing(self):
        for prog in list_progressions():
            self.assertTrue(prog.prog_id.startswith('PROG-'))
            self.assertTrue(len(prog.name) > 0, f"{prog.prog_id} name is empty.")
            self.assertTrue(len(prog.roman_numerals) > 0, f"{prog.prog_id} roman is empty.")
            self.assertTrue(len(prog.default_key) > 0, f"{prog.prog_id} default_key is empty.")
            self.assertTrue(len(prog.context) > 0, f"{prog.prog_id} context is empty.")
            self.assertTrue(len(prog.sources) > 0, f"{prog.prog_id} sources is empty.")
            
            # Every chord must parse into valid ChordDefinitions
            chords = prog.chord_definitions
            self.assertGreaterEqual(len(chords), 2, f"{prog.prog_id} must have at least 2 chords.")
            for c in chords:
                self.assertIsInstance(c, ChordDefinition)
                self.assertGreater(len(c.pitch_class_set), 0)

    def test_get_progression_lookup(self):
        p1 = get_progression('PROG-001')
        self.assertEqual(p1.name, 'Pop Four Chords')
        self.assertEqual(p1.roman_numerals, 'I - V - vi - IV')

        with self.assertRaises(ProgressionParsingError):
            get_progression('PROG-999')


class TestPreservedProgressions21And28(unittest.TestCase):
    """Strict verification of PROG-021 and PROG-028 preservation."""

    def test_prog_021_preservation(self):
        p21 = get_progression('PROG-021')
        self.assertEqual(p21.name, 'Neo-Soul Rootless Minor Cycle')
        self.assertEqual(p21.roman_numerals, 'i^9 - iv^9 - bVI^maj9 - V^7(b9)')
        self.assertEqual(p21.default_key, 'Dm')
        self.assertEqual(p21.chords_str, 'Dm9 - Gm9 - Bbmaj9 - A7(b9)')

        chords = p21.chord_definitions
        self.assertEqual(len(chords), 4)
        
        # Dm9: D(2), F(5), A(9), C(0), E(4)
        self.assertEqual(chords[0].symbol, 'Dm9')
        self.assertEqual(chords[0].pitch_class_set, {2, 5, 9, 0, 4})

        # Gm9: G(7), Bb(10), D(2), F(5), A(9)
        self.assertEqual(chords[1].symbol, 'Gm9')
        self.assertEqual(chords[1].pitch_class_set, {7, 10, 2, 5, 9})

        # Bbmaj9: Bb(10), D(2), F(5), A(9), C(0)
        self.assertEqual(chords[2].symbol, 'Bbmaj9')
        self.assertEqual(chords[2].pitch_class_set, {10, 2, 5, 9, 0})

        # A7(b9): A(9), C#(1), E(4), G(7), Bb(10)
        self.assertEqual(chords[3].symbol, 'A7(b9)')
        self.assertEqual(chords[3].pitch_class_set, {9, 1, 4, 7, 10})

    def test_prog_028_preservation(self):
        p28 = get_progression('PROG-028')
        self.assertEqual(p28.name, 'Circle of Fifths Soul Cycle')
        self.assertEqual(p28.roman_numerals, 'i^9 - iv^9 - bVII^9 - III^maj9')
        self.assertEqual(p28.default_key, 'Em')
        self.assertEqual(p28.chords_str, 'Em9 - Am9 - D9 - Gmaj9')

        chords = p28.chord_definitions
        self.assertEqual(len(chords), 4)

        # Em9: E(4), G(7), B(11), D(2), F#(6)
        self.assertEqual(chords[0].symbol, 'Em9')
        self.assertEqual(chords[0].pitch_class_set, {4, 7, 11, 2, 6})

        # Am9: A(9), C(0), E(4), G(7), B(11)
        self.assertEqual(chords[1].symbol, 'Am9')
        self.assertEqual(chords[1].pitch_class_set, {9, 0, 4, 7, 11})

        # D9: D(2), F#(6), A(9), C(0), E(4)
        self.assertEqual(chords[2].symbol, 'D9')
        self.assertEqual(chords[2].pitch_class_set, {2, 6, 9, 0, 4})

        # Gmaj9: G(7), B(11), D(2), F#(6), A(9)
        self.assertEqual(chords[3].symbol, 'Gmaj9')
        self.assertEqual(chords[3].pitch_class_set, {7, 11, 2, 6, 9})


class TestRomanNumeralResolver(unittest.TestCase):
    """Verifies diatonic, secondary, and modal interchange Roman numeral resolution."""

    def test_major_key_diatonic_degrees(self):
        # In C major
        c_i = resolve_roman_degree('I', key_root='C')
        self.assertEqual(c_i.symbol, 'C')

        c_ii = resolve_roman_degree('ii', key_root='C')
        self.assertEqual(c_ii.symbol, 'Dm')

        c_v7 = resolve_roman_degree('V7', key_root='C')
        self.assertEqual(c_v7.symbol, 'G7')

        c_maj7 = resolve_roman_degree('Imaj7', key_root='C')
        self.assertEqual(c_maj7.symbol, 'Cmaj7')

        c_vi = resolve_roman_degree('vi', key_root='C')
        self.assertEqual(c_vi.symbol, 'Am')

    def test_minor_key_degrees(self):
        # In D minor
        d_i = resolve_roman_degree('i', key_root='D', is_minor_key=True)
        self.assertEqual(d_i.symbol, 'Dm')

        d_iv = resolve_roman_degree('iv', key_root='D', is_minor_key=True)
        self.assertEqual(d_iv.symbol, 'Gm')

        d_v7 = resolve_roman_degree('V7', key_root='D', is_minor_key=True)
        self.assertEqual(d_v7.symbol, 'A7')

        d_bvi = resolve_roman_degree('bVI', key_root='D', is_minor_key=True)
        self.assertEqual(d_bvi.symbol, 'Bb')

    def test_secondary_dominants(self):
        # In C major:
        # V7/vi is dominant of Am -> E7
        v7_vi = resolve_roman_degree('V7/vi', key_root='C')
        self.assertEqual(v7_vi.symbol, 'E7')

        # V7/V is dominant of G -> D7
        v7_v = resolve_roman_degree('V7/V', key_root='C')
        self.assertEqual(v7_v.symbol, 'D7')

    def test_borrowed_modal_interchange_chords(self):
        # In C major:
        # bII7 (tritone sub / Neapolitan) -> Db7
        bii7 = resolve_roman_degree('bII7', key_root='C')
        self.assertEqual(bii7.symbol, 'Db7')

        # iv (minor plagal) -> Fm
        iv = resolve_roman_degree('iv', key_root='C')
        self.assertEqual(iv.symbol, 'Fm')

        # bVI (Aeolian modal interchange) -> Ab
        bvi = resolve_roman_degree('bVI', key_root='C')
        self.assertEqual(bvi.symbol, 'Ab')

        # bVII (subtonic) -> Bb
        bvii = resolve_roman_degree('bVII', key_root='C')
        self.assertEqual(bvii.symbol, 'Bb')


class TestProgressionTransposition(unittest.TestCase):
    """Verifies programmatic key transposition of canonical progressions."""

    def test_transpose_pop_four_chords(self):
        # PROG-001 in C: C - G - Am - F
        p1 = get_progression('PROG-001')
        
        # Transpose up 7 semitones (to G major): G - D - Em - C
        g_chords = p1.transpose(7)
        symbols = [c.symbol for c in g_chords]
        self.assertEqual(symbols, ['G', 'D', 'Em', 'C'])


class TestProgressionVoiceLeadingAndVoicingGeneration(unittest.TestCase):
    """Verifies progression voicing synthesis and metric analysis."""

    def test_prog_003_jazz_voice_leading(self):
        # PROG-003: Dm7 - G7 - Cmaj7
        p3 = get_progression('PROG-003')
        voicings = generate_progression_voicings(p3, style=VoiceLeadingStyle.JAZZ_POP)
        
        self.assertEqual(len(voicings), 3)
        for v in voicings:
            self.assertFalse(detect_voice_crossing(v.midi_notes))

        analysis = analyze_progression_voice_leading(voicings, style=VoiceLeadingStyle.JAZZ_POP)
        self.assertEqual(analysis['transition_count'], 2)
        self.assertEqual(analysis['voice_crossings_count'], 0)
        self.assertEqual(len(analysis['parallel_violations']), 0)
        self.assertGreater(analysis['total_l1_distance'], 0)

    def test_prog_021_voice_leading(self):
        # PROG-021: Dm9 - Gm9 - Bbmaj9 - A7(b9)
        p21 = get_progression('PROG-021')
        voicings = generate_progression_voicings(p21, style=VoiceLeadingStyle.JAZZ_POP)
        
        self.assertEqual(len(voicings), 4)
        for v in voicings:
            self.assertFalse(detect_voice_crossing(v.midi_notes))

        analysis = analyze_progression_voice_leading(voicings, style=VoiceLeadingStyle.JAZZ_POP)
        self.assertEqual(analysis['transition_count'], 3)
        self.assertEqual(analysis['voice_crossings_count'], 0)


if __name__ == '__main__':
    unittest.main()
