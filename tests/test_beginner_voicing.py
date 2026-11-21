"""
Tests for the STEPS Beginner Voicing & Didactic Reduction Engine (OA-0024, M10/M12).

Verifies:
- Didactic reduction of complex/extended chords to primary triads.
- Authentic realization of Pop Four Chords (C - G - Am - F) adhering 100% to PIANO_LEARNING_PATH.md.
- Common-tone retention and zero-jump voice-leading (C -> G -> Am -> F, total L1 = 9).
- Automatic generation of right-hand and left-hand beginner fingerings.
- German vs. international notation conventions (DE H vs. INT B).
- Autonomous global inversion optimization for Doo-Wop, ii-V-I, and Andalusian cadences.
- Integration into ProgressionSession and ProgressionSessionController (app/ui).
"""

from __future__ import annotations

import unittest
from itertools import product

from app.ui.session_controller import ProgressionSessionController
from src.steps.progression.engine import get_progression
from src.steps.progression.session import ProgressionSession
from src.steps.theory import (
    BeginnerChordVoicing,
    BeginnerProgressionVoicings,
    BeginnerTriadInversion,
    BeginnerVoiceLeadingTransition,
    ChordConstructionError,
    PedagogicalReduction,
    ProgressionParsingError,
    determine_beginner_fingering,
    generate_beginner_inversions,
    generate_beginner_voicings,
    parse_chord,
    reduce_chord_for_beginners,
)


class TestBeginnerVoicing(unittest.TestCase):
    def test_didactic_chord_reduction(self) -> None:
        """Verify that basic triads remain untouched while extended chords are simplified."""
        # Pure triads: no reduction needed
        for sym in ("C", "G", "Am", "F", "Dm", "Em"):
            red = reduce_chord_for_beginners(sym)
            self.assertFalse(red.was_reduced)
            self.assertEqual(red.reduced_symbol, sym)
            self.assertEqual(red.omitted_factors, ())

        # 7th chords reduced to triads
        red_cmaj7 = reduce_chord_for_beginners("Cmaj7")
        self.assertTrue(red_cmaj7.was_reduced)
        self.assertEqual(red_cmaj7.reduced_symbol, "C")
        self.assertIn("7th", red_cmaj7.omitted_factors)

        red_g7 = reduce_chord_for_beginners("G7")
        self.assertTrue(red_g7.was_reduced)
        self.assertEqual(red_g7.reduced_symbol, "G")
        self.assertIn("7th", red_g7.omitted_factors)

        red_dm7 = reduce_chord_for_beginners("Dm7")
        self.assertTrue(red_dm7.was_reduced)
        self.assertEqual(red_dm7.reduced_symbol, "Dm")
        self.assertIn("7th", red_dm7.omitted_factors)

        # Extended and alteration chords
        red_fadd9 = reduce_chord_for_beginners("Fadd9")
        self.assertTrue(red_fadd9.was_reduced)
        self.assertEqual(red_fadd9.reduced_symbol, "F")
        self.assertIn("9th", red_fadd9.omitted_factors)

        red_csus4 = reduce_chord_for_beginners("Csus4")
        self.assertEqual(red_csus4.reduced_symbol, "Csus4")

    def test_reduction_round_trips_german_roots_without_changing_pitches(self) -> None:
        pairs = (("Bbmaj7", "Bmaj7", "B"), ("Bmaj7", "Hmaj7", "H"), ("F#7", "Fis7", "Fis"))
        for international, german, reduced in pairs:
            with self.subTest(chord=german):
                self.assertEqual(reduce_chord_for_beginners(german, "DE").reduced_symbol, reduced)
                self.assertEqual(
                    generate_beginner_inversions(international, convention="INT"),
                    generate_beginner_inversions(german, convention="DE"),
                )

    def test_candidate_inversions_generation(self) -> None:
        """Verify generation of close triad candidates in the beginner keyboard range."""
        cands = generate_beginner_inversions("C")
        self.assertTrue(len(cands) >= 3)
        inv_types = {c[0] for c in cands}
        self.assertIn(BeginnerTriadInversion.ROOT, inv_types)
        self.assertIn(BeginnerTriadInversion.FIRST, inv_types)
        self.assertIn(BeginnerTriadInversion.SECOND, inv_types)

        # Check that 2nd inversion of C contains G3, C4, E4 (55, 60, 64)
        c_second = next((c[1] for c in cands if c[0] == BeginnerTriadInversion.SECOND and c[1][0] == 55), None)
        self.assertIsNotNone(c_second)
        self.assertEqual(c_second, (55, 60, 64))

    def test_optimized_path_matches_exhaustive_search_and_tie_order(self) -> None:
        for chords in (["C"], ["C", "G", "Am", "F"], ["Dm7", "G7", "Cmaj7"], ["F", "Fm", "C"]):
            candidates = [generate_beginner_inversions(chord) for chord in chords]
            for starting in (None, *BeginnerTriadInversion):
                with self.subTest(chords=chords, starting=starting):
                    paths = (
                        path for path in product(*candidates)
                        if starting is None or path[0][0] == starting
                    )

                    def cost(path):
                        movement = sum(
                            sum(abs(pitch_out - pitch_in) for pitch_in, pitch_out in zip(before, after))
                            for (_, before), (_, after) in zip(path, path[1:])
                        )
                        return movement + 0.05 * abs(sum(path[0][1]) / 3.0 - 60.0)

                    expected = min(paths, key=cost)
                    result = generate_beginner_voicings(chords, starting_inversion=starting)
                    self.assertEqual(tuple((item.inversion, item.rh_notes) for item in result.voicings), expected)

    def test_long_progression_preserves_every_chord_and_transition(self) -> None:
        chords = ["C", "G", "Am", "F"] * 32

        result = generate_beginner_voicings(chords)

        self.assertEqual([item.chord_symbol for item in result.voicings], chords)
        self.assertEqual(len(result.transitions), len(chords) - 1)
        self.assertEqual(result.total_l1_distance, sum(item.total_l1_distance for item in result.transitions))

    def test_golden_case_pop_four_chords(self) -> None:
        """
        Verify the exact pedagogical realization of Pop Four Chords (C - G - Am - F)
        as specified in PIANO_LEARNING_PATH.md.
        """
        result = generate_beginner_voicings(
            ["C", "G", "Am", "F"],
            starting_inversion=BeginnerTriadInversion.SECOND,
            convention="INT"
        )

        self.assertEqual(len(result.voicings), 4)
        self.assertEqual(len(result.transitions), 3)

        # 1. Bar 1: C-Major in 2nd inversion
        v_c = result.voicings[0]
        self.assertEqual(v_c.chord_symbol, "C")
        self.assertEqual(v_c.inversion, BeginnerTriadInversion.SECOND)
        self.assertEqual(v_c.rh_notes, (55, 60, 64))  # G3 - C4 - E4
        self.assertEqual(v_c.rh_spellings, ("G3", "C4", "E4"))
        self.assertEqual(v_c.rh_fingering, (1, 2, 5))
        self.assertEqual(v_c.lh_spelling, "C2")
        self.assertEqual(v_c.lh_fingering, 5)

        # 2. Bar 2: G-Major in Root position
        v_g = result.voicings[1]
        self.assertEqual(v_g.chord_symbol, "G")
        self.assertEqual(v_g.inversion, BeginnerTriadInversion.ROOT)
        self.assertEqual(v_g.rh_notes, (55, 59, 62))  # G3 - B3 - D4
        self.assertEqual(v_g.rh_spellings, ("G3", "B3", "D4"))
        self.assertEqual(v_g.rh_fingering, (1, 2, 4))
        self.assertEqual(v_g.lh_spelling, "G2")
        self.assertEqual(v_g.lh_fingering, 1)

        # 3. Bar 3: A-Minor in Root position
        v_am = result.voicings[2]
        self.assertEqual(v_am.chord_symbol, "Am")
        self.assertEqual(v_am.inversion, BeginnerTriadInversion.ROOT)
        self.assertEqual(v_am.rh_notes, (57, 60, 64))  # A3 - C4 - E4
        self.assertEqual(v_am.rh_spellings, ("A3", "C4", "E4"))
        self.assertEqual(v_am.rh_fingering, (1, 2, 5))
        self.assertEqual(v_am.lh_spelling, "A2")
        self.assertEqual(v_am.lh_fingering, 2)

        # 4. Bar 4: F-Major in 1st inversion
        v_f = result.voicings[3]
        self.assertEqual(v_f.chord_symbol, "F")
        self.assertEqual(v_f.inversion, BeginnerTriadInversion.FIRST)
        self.assertEqual(v_f.rh_notes, (57, 60, 65))  # A3 - C4 - F4
        self.assertEqual(v_f.rh_spellings, ("A3", "C4", "F4"))
        self.assertEqual(v_f.rh_fingering, (1, 2, 5))
        self.assertEqual(v_f.lh_spelling, "F2")
        self.assertEqual(v_f.lh_fingering, 4)

        # Voice leading transitions
        t_cg = result.transitions[0]
        self.assertEqual(t_cg.total_l1_distance, 3)
        self.assertEqual(t_cg.max_single_leap, 2)
        self.assertEqual(t_cg.common_tones, (55,))  # G3 held!
        self.assertFalse(t_cg.has_hand_jump)

        t_gam = result.transitions[1]
        self.assertEqual(t_gam.total_l1_distance, 5)
        self.assertEqual(t_gam.max_single_leap, 2)
        self.assertFalse(t_gam.has_hand_jump)

        t_amf = result.transitions[2]
        self.assertEqual(t_amf.total_l1_distance, 1)
        self.assertEqual(t_amf.max_single_leap, 1)
        self.assertEqual(t_amf.common_tones, (57, 60))  # A3 & C4 held!
        self.assertFalse(t_amf.has_hand_jump)

        # Aggregate progression metrics
        self.assertEqual(result.total_l1_distance, 9)
        self.assertEqual(result.average_l1_distance, 3.0)
        self.assertFalse(result.has_any_hand_jumps)
        self.assertGreater(result.movement_reduction_vs_root_percent, 70.0)

    def test_pedagogical_guidance_texts(self) -> None:
        """Verify the exact canonical explanations from PIANO_LEARNING_PATH.md."""
        result = generate_beginner_voicings(
            ["C", "G", "Am", "F"],
            starting_inversion="SECOND",
            convention="INT"
        )
        self.assertTrue(all(item.is_canonical_guidance for item in result.transitions))
        # Check descriptions
        self.assertIn("Daumen liegt auf G", result.voicings[0].pedagogical_description)
        self.assertIn("kleiner Finger auf E", result.voicings[0].pedagogical_description)

        self.assertEqual(
            result.transitions[0].pedagogical_guidance,
            "Der Daumen bleibt auf G liegen! Nur die oberen Finger bewegen sich einen Schritt nach links."
        )
        self.assertEqual(
            result.transitions[1].pedagogical_guidance,
            "Sehr entspannter Schritt, Hand wandert nur eine weiße Taste weiter."
        )
        self.assertEqual(
            result.transitions[2].pedagogical_guidance,
            "A und C bleiben exakt liegen! Nur der kleine Finger wandert von E nach F."
        )

    def test_generated_guidance_follows_the_calculated_voice_assignment(self) -> None:
        result = generate_beginner_voicings(["Cdim", "F#dim"], convention="INT")
        transition = result.transitions[0]
        self.assertEqual(transition.moving_voices, ((60, 57, -3), (63, 60, -3)))
        self.assertIn("C4 → A3 (-3)", transition.pedagogical_guidance)
        self.assertIn("Eb4 → C4 (-3)", transition.pedagogical_guidance)
        self.assertFalse(transition.is_canonical_guidance)

    def test_german_notation_convention(self) -> None:
        """Verify ADR-005 notation convention (H vs B)."""
        res_de = generate_beginner_voicings(
            ["C", "G", "Am", "F"],
            starting_inversion="SECOND",
            convention="DE"
        )
        v_g = res_de.voicings[1]
        self.assertEqual(v_g.rh_spellings, ("G3", "H3", "D4"))

    def test_autonomous_global_optimization(self) -> None:
        """Verify that omitting starting_inversion selects smooth voice-leading autonomously."""
        # Pop Four Chords without starting constraint
        res_auto = generate_beginner_voicings(["C", "G", "Am", "F"])
        self.assertEqual(res_auto.total_l1_distance, 9)
        self.assertFalse(res_auto.has_any_hand_jumps)

        # Doo-Wop Cadence (C - Am - F - G)
        res_doowop = generate_beginner_voicings(["C", "Am", "F", "G"])
        self.assertLessEqual(res_doowop.average_l1_distance, 3.5)
        self.assertFalse(res_doowop.has_any_hand_jumps)

        # Jazz ii-V-I (Dm7 - G7 - Cmaj7) reduced for beginners
        res_251 = generate_beginner_voicings(["Dm7", "G7", "Cmaj7"])
        self.assertEqual(len(res_251.voicings), 3)
        self.assertFalse(res_251.has_any_hand_jumps)
        self.assertLessEqual(res_251.total_l1_distance, 8)

    def test_canonical_progression_input(self) -> None:
        """Verify that CanonicalProgression objects are supported seamlessly."""
        prog = get_progression("PROG-001")
        res = generate_beginner_voicings(prog, starting_inversion="SECOND")
        self.assertEqual(len(res.voicings), 4)
        self.assertEqual(res.total_l1_distance, 9)

    def test_serialization_to_dict(self) -> None:
        """Verify JSON-serializable dictionary representation."""
        res = generate_beginner_voicings(["C", "G", "Am", "F"], starting_inversion="SECOND")
        d = res.to_dict()
        self.assertIn("voicings", d)
        self.assertIn("transitions", d)
        self.assertEqual(d["total_l1_distance"], 9)
        self.assertEqual(d["average_l1_distance"], 3.0)
        self.assertEqual(len(d["voicings"]), 4)
        self.assertEqual(d["voicings"][0]["rh_fingering"], [1, 2, 5])
        self.assertEqual(d["voicings"][1]["rh_fingering"], [1, 2, 4])

    def test_session_and_ui_controller_integration(self) -> None:
        """Verify that ProgressionSession and ProgressionSessionController expose beginner voicings."""
        session = ProgressionSession()
        # Default session has chords ["C", "G", "Am", "F"]
        beg_voicings = session.get_beginner_voicings(starting_inversion="SECOND")
        self.assertIsInstance(beg_voicings, BeginnerProgressionVoicings)
        self.assertEqual(beg_voicings.total_l1_distance, 9)

        controller = ProgressionSessionController(session)
        vm = controller.get_view_model()
        self.assertIn("beginner_voicings", vm)
        self.assertEqual(vm["beginner_voicings"]["total_l1_distance"], 9)

        ctrl_beg = controller.get_beginner_voicings(starting_inversion="SECOND")
        self.assertEqual(ctrl_beg["total_l1_distance"], 9)

    def test_error_handling(self) -> None:
        """Verify proper error raising for invalid inputs."""
        with self.assertRaises(ProgressionParsingError):
            generate_beginner_voicings(12345)  # type: ignore

        with self.assertRaises(ChordConstructionError):
            generate_beginner_voicings(["C", "G"], starting_inversion="INVALID_INVERSION")


if __name__ == "__main__":
    unittest.main()
