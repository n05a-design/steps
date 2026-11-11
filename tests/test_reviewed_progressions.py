"""Production regressions from the STEPS knowledge and music-theory audit."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.knowledge import get_reviewed_progression, list_reviewed_progressions
from scripts.render_reviewed_progressions import OUTPUT, REGISTRY, render
from src.steps.progression import (
    VoiceLeadingStyle,
    generate_progression_voicings,
    get_progression,
    list_progressions,
    optimize_smooth_voice_leading,
    resolve_roman_degree,
)
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import MusicTheoryError, ProgressionParsingError, VoiceLeadingError
from src.steps.theory.pitch import frequency_to_midi, midi_to_frequency


class RomanNumeralRegressionTests(unittest.TestCase):
    def test_quality_leading_tone_and_inversions(self):
        cases = [
            ("V", "C", False, "G", {7, 11, 2}),
            ("ii^7", "C", False, "Dm7", {2, 5, 9, 0}),
            ("iii7", "C", False, "Em7", {4, 7, 11, 2}),
            ("V", "A", True, "E", {4, 8, 11}),
            ("v", "A", True, "Em", {4, 7, 11}),
            ("VII", "A", True, "G", {7, 11, 2}),
            ("vii°7", "A", True, "G#dim7", {8, 11, 2, 5}),
            ("viio7/V", "C", False, "F#dim7", {6, 9, 0, 3}),
            ("ii6", "C", False, "Dm/F", {2, 5, 9}),
            ("V7(4/3)", "G", False, "D7/A", {2, 6, 9, 0}),
            ("V7/V(6/5)", "G", False, "A7/C#", {9, 1, 4, 7}),
            ("V6/5/V", "G", False, "A7/C#", {9, 1, 4, 7}),
            ("i^(maj7)", "A", True, "Am(maj7)", {9, 0, 4, 8}),
            ("im6", "A", True, "Am6", {9, 0, 4, 6}),
            ("V7b5", "C", False, "G7b5", {7, 11, 1, 5}),
        ]
        for degree, key, minor, symbol, pitch_classes in cases:
            with self.subTest(degree=degree, key=key):
                chord = resolve_roman_degree(degree, key, minor)
                self.assertEqual(chord.symbol, symbol)
                self.assertEqual(chord.pitch_class_set, pitch_classes)

    def test_notation_and_unsupported_syntax(self):
        self.assertEqual(resolve_roman_degree("I", "B", convention="DE").symbol, "Bb")
        self.assertEqual(resolve_roman_degree("I", "B", convention="INT").symbol, "B")
        for value in ("I/V", "vii/V", "IIV", "V7(alt)", "ii nonsense"):
            with self.subTest(value=value), self.assertRaises(ProgressionParsingError):
                resolve_roman_degree(value)


class VoicingRegressionTests(unittest.TestCase):
    def test_inverted_and_non_chord_basses_keep_the_chords_identity(self):
        for symbol, bass, pitch_classes in [
            ("C/E", 4, {0, 4, 7}),
            ("C/D", 2, {0, 2, 4, 7}),
            ("D7/A", 9, {2, 6, 9, 0}),
        ]:
            with self.subTest(symbol=symbol):
                voicing = parse_chord(symbol).to_voicing()
                self.assertEqual(voicing.bass_note % 12, bass)
                self.assertEqual({note % 12 for note in voicing.midi_notes}, pitch_classes)
        self.assertEqual(parse_chord("D7/A").to_voicing(voicing_type="DROP2").bass_note % 12, 9)

    def test_all_catalog_progressions_preserve_pitch_classes_and_basses(self):
        for progression in list_progressions():
            with self.subTest(progression=progression.prog_id):
                definitions = progression.chord_definitions
                voiced = generate_progression_voicings(progression)
                self.assertEqual(len(voiced), len(definitions))
                self.assertEqual(len({len(v.notes) for v in voiced}), 1)
                for chord, voicing in zip(definitions, voiced):
                    bass = (chord.bass or chord.root).pitch_class
                    self.assertEqual(voicing.bass_note % 12, bass)
                    self.assertEqual({note % 12 for note in voicing.notes},
                                     set(chord.voiced_pitch_classes) | {bass})
                    self.assertTrue(all(0 <= note <= 127 for note in voicing.notes))

    def test_no_invalid_fallback_and_midi_boundaries(self):
        with self.assertRaises(VoiceLeadingError):
            optimize_smooth_voice_leading([48, 55, 60, 64], {0, 4, 7}, bass_pc=1)
        # Moving these boundary voices while keeping both pitch classes
        # necessarily produces parallel octaves within the one-octave window.
        with self.assertRaises(VoiceLeadingError):
            optimize_smooth_voice_leading([0, 12], {1}, style=VoiceLeadingStyle.STRICT_COUNTERPOINT)
        self.assertEqual(optimize_smooth_voice_leading([0], {11}), [11])
        self.assertEqual(optimize_smooth_voice_leading([127], {8}), [116])
        for tuning in (0, -440, float("nan"), float("inf")):
            with self.subTest(tuning=tuning), self.assertRaises(MusicTheoryError):
                midi_to_frequency(69, tuning)
            with self.subTest(tuning=tuning), self.assertRaises(MusicTheoryError):
                frequency_to_midi(440, tuning)


class ReviewedCatalogTests(unittest.TestCase):
    def test_app_catalog_and_generated_material_share_the_reviewed_data(self):
        examples = list_reviewed_progressions()
        self.assertEqual([e.progression.prog_id for e in examples], ["PROG-001", "PROG-003", "PROG-009"])
        with self.assertRaises(ProgressionParsingError):
            get_reviewed_progression("PROG-027")
        for example in examples:
            p = example.progression
            with self.subTest(progression=p.prog_id):
                self.assertIs(p, get_progression(p.prog_id))
                resolved = [resolve_roman_degree(d, p.default_key) for d in p.roman_numerals.split(" - ")]
                self.assertEqual(resolved, p.chord_definitions)
                self.assertTrue(generate_progression_voicings(p))
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), render())

    def test_unapproved_source_blocks_generated_learning_material(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        registry["sources"][0]["rights_status"] = "review_required"
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.yaml"
            path.write_text(json.dumps(registry), encoding="utf-8")
            with patch("scripts.render_reviewed_progressions.REGISTRY", path):
                with self.assertRaisesRegex(ValueError, "Unapproved reference"):
                    render()
