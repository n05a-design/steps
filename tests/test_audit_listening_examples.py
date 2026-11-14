"""Check that the generated audition controls contain the documented contrasts."""

from pathlib import Path
import tempfile
import unittest

from scripts import analyze_audit_listening_examples as analysis
from scripts import render_audit_listening_examples as renderer


class AuditListeningExamplesTests(unittest.TestCase):
    def test_meter_audio_preserves_bells_and_changes_midpoint_accent(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, accent_positions in (("a", [0]), ("b", [0, 6])):
                with self.subTest(variant=name):
                    path = Path(directory) / f"pat-031-{name}.wav"
                    renderer.write_wave(path, renderer.meter_audio(accent_positions))
                    measurements = analysis.analyze(path, analysis.measure_meter)["measurements"]
                    self.assertEqual(len(measurements), 4)
                    for cycle in measurements:
                        self.assertEqual(cycle["bell_eighth_positions"], [0, 2, 4, 5, 7, 9, 11])
                        self.assertEqual(cycle["marked_eighth_positions"], accent_positions)
                        self.assertEqual(list(cycle["pulse_amplitudes_by_eighth"]), [0, 3, 6, 9])

    def test_progression_audio_preserves_chords_and_changes_melodic_centers(self):
        chord_notes = [[48, 55, 60, 64], [43, 55, 59, 62], [45, 52, 57, 60], [41, 53, 57, 60]]
        melodies = {
            "c": [72, 76, 79, 76, 74, 71, 74, 74, 72, 76, 72, 69, 69, 65, 67, 72],
            "a": [69, 72, 76, 72, 71, 74, 71, 74, 69, 72, 76, 69, 72, 65, 67, 69],
        }
        with tempfile.TemporaryDirectory() as directory:
            for name, melody in melodies.items():
                with self.subTest(variant=name):
                    path = Path(directory) / f"prog-001-{name}.wav"
                    renderer.write_wave(path, renderer.pop_audio(renderer.POP_MELODIES[name]))
                    measurements = analysis.analyze(path, analysis.measure_progression)["measurements"]
                    expected = {"chord_midi": chord_notes, "melody_midi": melody,
                                "accented_quarter_positions": [0, 8, 15]}
                    self.assertEqual(measurements, [expected] * 3)
