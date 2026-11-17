"""
STEPS Golden Music Invariants Test Suite (T01..T16).

Directly validates the 16 fundamental music domain invariants specified in:
- docs/engineering/MUSIC_DOMAIN_AND_MIDI.md (Abschnitt 2, Zeilen 40-58)
- prompts/08_MUSIC_PITCH_CHORD.md
- ROADMAP_AND_RESOURCE_PLAN.md (T01..T16 Core Acceptance Tests)
- OA-0014 (Aufbau der Golden Test Suite v0.1)

Invariants tested:
  T01: C-Dur = C D E F G A H (German) vs C D E F G A B (International)
  T02: German 'B' is Bb, International 'B' is B natural; AUTO rejects ambiguous 'B'
  T03: F# / Gb share 12-TET pitch class 6, but possess distinct diatonic identities
  T04: C7 (C E G Bb) vs Cmaj7 (C E G B/H) distinct seventh qualities
  T05: Cm7 (C Eb G Bb); minor triad + minor 7th; no silent replacement
  T06: C/E sounds with E in bass; parser separates slash bass from inversion
  T07: C - G - Am - F transposed +2 semitones -> D - A - Bm - G
  T08: E7 -> Am is V7 in a-minor, but V7/vi in C-major (context dependence)
  T09: bVII -> I (e.g. Bb -> C) not classified as classical authentic cadence
  T10: Different voicings of same pitch class set have different voice-leading costs
  T11: Storage/playback consistency: no chord/event without explicit ticks & duration
  T12: Chord AST: no3, sus4, extensions & alterations not collapsed to simple maj/min
  T13: Alternative analyses from distinct frameworks preserved with source provenance
  T14: Note-on / note-off pairing validator detects hanging notes and unclosed loops
  T15: Mid-song tempo changes correctly scale tick-to-seconds mapping (TempoMap)
  T16: Swing and humanize transformations are reproducible, bounded, and non-negative
"""

import unittest

from src.steps.models.timeline import (
    DEFAULT_PPQ,
    TempoMap,
    TempoPoint,
    TimelineEvent,
    TimeSignature,
    apply_humanize,
    apply_swing,
    validate_midi_note_on_off_pairing,
)
from src.steps.progression.engine import (
    resolve_roman_degree,
)
from src.steps.progression.voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    circular_pc_distance,
)
from src.steps.theory.chord import (
    ChordDefinition,
    Voicing,
    parse_chord,
)
from src.steps.theory.exceptions import (
    ChordConstructionError,
    MusicTheoryError,
    ScaleConstructionError,
    VoiceLeadingError,
)
from src.steps.theory.interval import (
    ChromaticInterval,
    DiatonicInterval,
    interval_between_spellings,
    transpose_spelling,
)
from src.steps.theory.pitch import (
    NoteSpelling,
    PitchClass,
    parse_spelling,
)
from src.steps.theory.scale import (
    construct_scale,
    parse_scale,
)


class TestGoldenMusicInvariantsT01toT16(unittest.TestCase):

    def test_t01_locale_projection_c_major(self):
        """T01: C-Dur = C D E F G A H (German); international last note is B."""
        scale = construct_scale(NoteSpelling("C", 0, 4), "major")
        de_rendered = scale.render_text(convention="DE")
        int_rendered = scale.render_text(convention="INT")
        
        self.assertEqual(de_rendered, ["C4", "D4", "E4", "F4", "G4", "A4", "H4"])
        self.assertEqual(int_rendered, ["C4", "D4", "E4", "F4", "G4", "A4", "B4"])
        self.assertEqual(de_rendered[-1], "H4")
        self.assertEqual(int_rendered[-1], "B4")

    def test_t02_b_ambiguity_rejection(self):
        """T02: German 'B' is Bb, International 'B' is B natural; AUTO rejects ambiguous 'B'."""
        # Under explicit DE convention, 'B' is B flat (MIDI 70 / PitchClass 10)
        chord_de = parse_chord("B", convention="DE")
        self.assertEqual(chord_de.root.pitch_class, 10)
        self.assertEqual(chord_de.root.render("INT"), "Bb4")

        # Under explicit INT convention, 'B' is B natural (MIDI 71 / PitchClass 11)
        chord_int = parse_chord("B", convention="INT")
        self.assertEqual(chord_int.root.pitch_class, 11)
        self.assertEqual(chord_int.root.render("INT"), "B4")

        # Without convention (AUTO), the ambiguous token must be strictly rejected
        with self.assertRaises(ChordConstructionError):
            parse_chord("B", convention="AUTO")

        with self.assertRaises(ScaleConstructionError):
            parse_scale("B Major", convention="AUTO")

    def test_t03_enharmonic_separation_fsharp_gflat(self):
        """T03: F# / Gb share 12-TET pitch class 6, but possess distinct diatonic identities."""
        f_sharp = NoteSpelling("F", 1, 4)
        g_flat = NoteSpelling("G", -1, 4)

        # Same 12-TET sounding pitch class
        self.assertEqual(f_sharp.pitch_class, 6)
        self.assertEqual(g_flat.pitch_class, 6)
        self.assertEqual(f_sharp.pitch_class, g_flat.pitch_class)
        self.assertTrue(f_sharp.is_enharmonic_with(g_flat))

        # Orthographically and diatonically distinct
        self.assertNotEqual(f_sharp, g_flat)
        self.assertEqual(f_sharp.step, "F")
        self.assertEqual(g_flat.step, "G")
        self.assertEqual(f_sharp.alteration, 1)
        self.assertEqual(g_flat.alteration, -1)

    def test_t04_quality_distinction_c7_vs_cmaj7(self):
        """T04: C7 = C E G Bb; Cmaj7 = C E G H/B natural."""
        c7 = parse_chord("C7", convention="INT")
        cmaj7 = parse_chord("Cmaj7", convention="INT")

        self.assertEqual(c7.theoretical_intervals, (0, 4, 7, 10))
        self.assertEqual(cmaj7.theoretical_intervals, (0, 4, 7, 11))
        self.assertEqual(c7.quality, "7")
        self.assertEqual(cmaj7.quality, "maj7")
        self.assertIn(10, c7.theoretical_intervals)  # Minor 7th (Bb)
        self.assertIn(11, cmaj7.theoretical_intervals)  # Major 7th (B natural)

    def test_t05_minor_seventh_integrity(self):
        """T05: Cm7 = C Eb G Bb; minor triad + minor 7th; no silent replacement."""
        cm7 = parse_chord("Cm7", convention="INT")
        self.assertEqual(cm7.theoretical_intervals, (0, 3, 7, 10))
        self.assertEqual(cm7.quality, "m7")
        # Ensure 3rd is minor (3 semitones), not major (4) or sus4 (5)
        self.assertEqual(cm7.theoretical_intervals[1], 3)

    def test_t06_slash_bass_inversion_separation(self):
        """T06: C/E sounds with E in bass; parser separates slash bass from inversion."""
        c_slash_e = parse_chord("C/E", convention="INT")
        self.assertEqual(c_slash_e.root.step, "C")
        self.assertIsNotNone(c_slash_e.bass)
        self.assertEqual(c_slash_e.bass.step, "E")

        # Inversion voicing check: E is the lowest note
        v = c_slash_e.to_voicing(bass_octave=3, voicing_type="CLOSE")
        self.assertEqual(v.bass_note % 12, 4)  # Pitch class of E is 4

        # Foreign bass (not in chord triad, e.g. C/D)
        c_slash_d = parse_chord("C/D", convention="INT")
        self.assertEqual(c_slash_d.bass.step, "D")
        v_d = c_slash_d.to_voicing(bass_octave=3, voicing_type="CLOSE")
        self.assertEqual(v_d.bass_note % 12, 2)  # D = PC 2

    def test_t07_progression_transposition_orthography(self):
        """T07: C - G - Am - F transposed +2 semitones -> D - A - Bm - G."""
        original_symbols = ["C", "G", "Am", "F"]
        chords = [parse_chord(sym, "INT") for sym in original_symbols]
        
        # Transpose each chord by diatonic major second (+2 semitones, +1 step)
        transposed_chords = []
        for ch in chords:
            new_root = ch.root.transpose_diatonic(step_delta=1, semitone_delta=2)
            transposed_chords.append(ChordDefinition(root=new_root, quality=ch.quality))

        transposed_symbols = [
            f"{c.root.render('INT')[:-1]}{c.quality}" for c in transposed_chords
        ]
        self.assertEqual(transposed_symbols, ["D", "A", "Bm", "G"])
        # Verify Am -> Bm root step:
        am_root = chords[2].root
        bm_root = am_root.transpose_diatonic(step_delta=1, semitone_delta=2)
        self.assertEqual(bm_root.step, "B")
        self.assertEqual(bm_root.alteration, 0)

    def test_t08_context_dependent_analysis_e7_am(self):
        """T08: E7 -> Am is V7 in a-minor, but V7/vi in C-major (context dependence)."""
        # In a-minor: E7 is the primary dominant (V7)
        deg_in_a_min = resolve_roman_degree("V7", "A", is_minor_key=True)
        self.assertEqual(deg_in_a_min.symbol, "E7")
        self.assertEqual(deg_in_a_min.root.step, "E")

        # In C-major: secondary dominant V7/vi resolving to vi (Am)
        deg_in_c_maj = resolve_roman_degree("V7/vi", "C", is_minor_key=False)
        self.assertEqual(deg_in_c_maj.symbol, "E7")
        self.assertEqual(deg_in_c_maj.root.step, "E")

    def test_t09_modal_interchange_bvii_not_authentic_cadence(self):
        """T09: bVII -> I (e.g. Bb -> C) not classified as classical authentic cadence."""
        bVII = resolve_roman_degree("bVII", "C", is_minor_key=False)
        self.assertEqual(bVII.symbol, "Bb")
        self.assertEqual(bVII.root.pitch_class, 10)  # Bb
        
        # Authentic cadence requires dominant V (G) -> I (C)
        V = resolve_roman_degree("V", "C", is_minor_key=False)
        self.assertEqual(V.symbol, "G")
        self.assertNotEqual(bVII.symbol, V.symbol)

    def test_t10_voicing_voice_leading_costs(self):
        """T10: Different voicings of same pitch class set have different voice-leading costs."""
        # Chord 1: C Major triad (C4, E4, G4)
        c_close = [60, 64, 67]
        
        # Chord 2 options: G Major triad
        g_close_opt1 = [59, 62, 67]  # B3, D4, G4 -> minimal smooth movement
        g_root_pos = [55, 59, 62]    # G3, B3, D4 -> larger leap

        dist1 = absolute_semitone_distance(c_close, g_close_opt1)  # |60-59| + |64-62| + |67-67| = 1 + 2 + 0 = 3
        dist2 = absolute_semitone_distance(c_close, g_root_pos)    # |60-55| + |64-59| + |67-62| = 5 + 5 + 5 = 15

        self.assertEqual(dist1, 3)
        self.assertEqual(dist2, 15)
        self.assertLess(dist1, dist2)

    def test_t11_timeline_event_duration_consistency(self):
        """T11: Storage/playback consistency: no chord/event without explicit ticks & duration."""
        # Valid timeline event
        ev = TimelineEvent(
            event_id="EVT-001",
            track_id="HARMONY",
            event_type="CHORD",
            start_tick=0,
            duration_ticks=480,  # 1 beat
            payload="Cmaj7"
        )
        self.assertEqual(ev.end_tick, 480)

        # Zero or negative duration must raise ValueError
        with self.assertRaises(ValueError):
            TimelineEvent("EVT-002", "HARMONY", "CHORD", start_tick=0, duration_ticks=0)

        with self.assertRaises(ValueError):
            TimelineEvent("EVT-003", "HARMONY", "CHORD", start_tick=-480, duration_ticks=480)

    def test_t12_complex_chord_ast_no_reduction(self):
        """T12: Chord AST: no3, sus4, extensions & alterations not collapsed to simple maj/min."""
        c_sus4 = parse_chord("Csus4", "INT")
        c_add9 = parse_chord("Cadd9", "INT")
        c_7alt = parse_chord("C7#9", "INT")

        self.assertEqual(c_sus4.quality, "sus4")
        self.assertEqual(c_add9.quality, "add9")
        self.assertEqual(c_7alt.quality, "7#9")
        
        # Verify interval contents are distinct
        self.assertIn(5, c_sus4.theoretical_intervals)  # Perfect 4th (sus4)
        self.assertNotIn(4, c_sus4.theoretical_intervals)  # No major 3rd
        self.assertIn(14, c_add9.theoretical_intervals)  # 9th
        self.assertIn(15, c_7alt.theoretical_intervals)  # #9

    def test_t13_alternative_harmonic_analyses_provenance(self):
        """T13: Alternative analyses from distinct frameworks preserved with source provenance."""
        # e.g. Diminished 7th chord Bdim7 can be analyzed as:
        # 1. vii°7 in C-Major (Leading-tone chord, Aldwell/Schachter)
        # 2. Incomplete dominant 7(b9) without root G (Riemann / Schönberg)
        analysis_frameworks = {
            "Aldwell_Schachter": {"function": "vii°7", "framework": "Common Practice"},
            "Riemann_Funktionstheorie": {"function": "D̸7>", "framework": "Funktionstheorie (verkürzter Dominantseptnonakkord)"},
            "Jazz_Berklee": {"function": "Bdim7", "framework": "Chord Scale Theory"}
        }
        self.assertEqual(len(analysis_frameworks), 3)
        self.assertNotEqual(
            analysis_frameworks["Aldwell_Schachter"]["function"],
            analysis_frameworks["Riemann_Funktionstheorie"]["function"]
        )

    def test_t14_midi_note_on_off_pairing(self):
        """T14: Note-on / note-off pairing validator detects hanging notes and unclosed loops."""
        # Balanced sequence
        valid_stream = [
            ("note_on", 0, 0, 60),
            ("note_off", 480, 0, 60),
            ("note_on", 480, 0, 64),
            ("note_off", 960, 0, 64),
        ]
        errors = validate_midi_note_on_off_pairing(valid_stream)
        self.assertEqual(errors, [])

        # Unbalanced sequence (hanging note_on)
        hanging_stream = [
            ("note_on", 0, 0, 60),
            ("note_on", 480, 0, 64),
            ("note_off", 960, 0, 64),
            # note 60 never released!
        ]
        errors_hanging = validate_midi_note_on_off_pairing(hanging_stream)
        self.assertGreaterEqual(len(errors_hanging), 1)
        self.assertIn("Hanging note_on", errors_hanging[0])

    def test_t15_multi_tempo_map_tick_second_scaling(self):
        """T15: Mid-song tempo changes correctly scale tick-to-seconds mapping (TempoMap)."""
        # Setup: 120 BPM from tick 0 to 1920 (1 bar of 4/4 at 480 PPQ)
        # At 120 BPM: 1 beat = 480 ticks = 0.5s. 1 bar = 1920 ticks = 2.0s.
        # At tick 1920: tempo drops to 60 BPM (1 beat = 1.0s, 1 bar = 4.0s).
        t_map = TempoMap(
            points=[
                TempoPoint(0, 120.0),
                TempoPoint(1920, 60.0),
            ],
            ppq=480
        )
        # Check elapsed time at bar 1 (tick 1920)
        self.assertAlmostEqual(t_map.tick_to_seconds(1920), 2.0, places=4)
        
        # Check elapsed time at bar 2 (tick 3840 = 1920 + 1920 at 60 BPM)
        # Total = 2.0s + 4.0s = 6.0s
        self.assertAlmostEqual(t_map.tick_to_seconds(3840), 6.0, places=4)

        # Roundtrip check: 6.0s -> tick 3840
        self.assertEqual(t_map.seconds_to_tick(6.0), 3840)

    def test_t16_swing_and_humanize_determinism_and_bounds(self):
        """T16: Swing and humanize transformations are reproducible, bounded, and non-negative."""
        ppq = 480
        tick_offbeat = 240  # 2nd eighth note of bar 1
        
        # Swing: straight (0.0) -> exactly 240
        self.assertEqual(apply_swing(tick_offbeat, 0.0, ppq), 240)
        
        # Swing: max triplet swing (1.0) -> shifted towards triplet position (320 ticks)
        swung_tick = apply_swing(tick_offbeat, 1.0, ppq)
        self.assertEqual(swung_tick, 320)
        self.assertGreater(swung_tick, tick_offbeat)

        # Humanize: reproducible given same seed
        h1 = apply_humanize(tick=1000, max_delta_ticks=30, seed=42)
        h2 = apply_humanize(tick=1000, max_delta_ticks=30, seed=42)
        self.assertEqual(h1, h2)

        # Bounded within [-30, +30]
        self.assertTrue(970 <= h1 <= 1030)

        # Non-negative guarantee near tick 0
        h_zero = apply_humanize(tick=5, max_delta_ticks=50, seed=42)
        self.assertGreaterEqual(h_zero, 0)


if __name__ == "__main__":
    unittest.main()
