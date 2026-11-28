"""Musical witnesses selected from the V2.1 generated mutation report."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.steps.keyboard import recognize_chord
from src.steps.keyboard.practice import pilot_exercises
from src.steps.keyboard.voice_motion import compare_voicings
from src.steps.midi.smf_parser import ParsedTrack
from src.steps.ports.live import LiveEventKind, LiveNoteEvent, MidiInputDevice, ScriptedMidiInput, normalize_midi_message
from src.steps.progression.reviewed import PublicationError, resolve_source_citation
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import InvalidAlterationError
from src.steps.theory.interval import ChromaticInterval, DiatonicInterval, interval_between_spellings
from src.steps.theory.inversion import detect_chord_inversion
from src.steps.theory.pitch import NoteSpelling, parse_spelling
from src.steps.theory.scale import get_scale_template


class MusicAuditSemanticWitnesses(unittest.TestCase):
    def test_compound_intervals_and_written_unison(self):
        self.assertEqual(int(ChromaticInterval.PERFECT_UNISON), 0)
        self.assertEqual(DiatonicInterval(15, "P").octaves, 2)
        self.assertEqual(DiatonicInterval(5, "d").semitones, 6)
        for first, second, number, quality, semitones in (
            ("C4", "C4", 1, "P", 0), ("C4", "Gb4", 5, "d", 6), ("C4", "D5", 9, "M", 14),
        ):
            with self.subTest(first=first, second=second):
                notes = [parse_spelling(note, "INT") for note in (first, second)]
                interval = interval_between_spellings(*notes)
                self.assertEqual((interval.number, interval.quality, interval.semitones), (number, quality, semitones))

    def test_export_voicing_preserves_major_third_and_perfect_fifth_where_required(self):
        for symbol, expected in (("C7", {0, 4, 7, 10}), ("Cmaj9", {0, 2, 4, 11})):
            self.assertEqual({midi % 12 for midi in parse_chord(symbol, "INT").to_voicing().notes}, expected, symbol)

    def test_mixolydian_profile_highlights_dominant_guide_tones(self):
        self.assertEqual(get_scale_template("mixolydian").characteristic_intervals, (4, 10))

    def test_note_spelling_distinguishes_double_and_triple_alteration(self):
        self.assertEqual(NoteSpelling("F", 2, 4).midi_number, 67)
        with self.assertRaises(InvalidAlterationError):
            NoteSpelling("F", 3, 4)

    def test_full_diminished_seventh_keeps_seventh_figures_without_root_hint(self):
        result = detect_chord_inversion([48, 51, 54, 57])
        # Exact root preference is a deterministic tie-break in this legacy API.
        # This sonority admits other enharmonic roots in recognition.
        self.assertEqual((result.root_pc, result.figured_bass, result.is_seventh_chord), (0, "7", True))

    def test_recognition_best_supported_keeps_exact_first_and_actual_bass(self):
        result = recognize_chord([48, 52, 54, 58])
        self.assertEqual(result.best_supported.chord.symbol, "C7b5")
        self.assertEqual([candidate.kind.value for candidate in result.candidates],
                         ["EXACT", "EXACT", "STANDARD_VOICING", "STANDARD_VOICING"])
        self.assertEqual(result.best_supported.bass_role.value, "ROOT")

    def test_practice_pilot_contract_starts_at_v1(self):
        self.assertTrue(all(exercise.version == 1 for exercise in pilot_exercises()))

    def test_two_voices_report_semitone_whole_tone_and_similar_outer_motion(self):
        result = compare_voicings([60, 67], [61, 69])
        self.assertEqual([motion.kind.value for motion in result.motions], ["SEMITONE", "WHOLE_TONE"])
        self.assertEqual(result.outer_voice_motion, "SIMILAR")

    def test_virtual_input_defaults_and_close_are_repeatable(self):
        reset = LiveNoteEvent(LiveEventKind.ALL_NOTES_OFF)
        self.assertEqual((reset.note, reset.velocity, reset.channel, reset.value), (0, 0, 0, 0))
        event = normalize_midi_message(0x92)
        self.assertEqual((event.kind, event.note, event.channel), (LiveEventKind.NOTE_OFF, 0, 2))
        adapter = ScriptedMidiInput([MidiInputDevice("test", "Test source")])
        events = []
        adapter.open("test", events.append)
        adapter.feed(0x92)
        adapter.close()
        adapter.close()
        adapter.feed(0x92, 60, 90)
        self.assertEqual([(e.kind, e.note, e.channel) for e in events],
                         [(LiveEventKind.NOTE_OFF, 0, 2), (LiveEventKind.ALL_NOTES_OFF, 0, 0)])

    def test_empty_smf_track_duration_starts_at_zero(self):
        self.assertEqual(ParsedTrack(track_index=0).total_ticks, 0)

    def test_synthetic_source_requires_rights_and_exact_identity(self):
        synthetic = {"id": "test-source", "title": "Synthetic fixture",
                     "url": "https://example.org/score", "rights_status": "approved"}
        with TemporaryDirectory() as directory:
            registry = Path(directory) / "sources.json"
            for source, valid in ((synthetic, True), ({**synthetic, "rights_status": "pending"}, False),
                                  ({**synthetic, "url": "http://example.org/score"}, False)):
                registry.write_text(json.dumps({"schema_version": 1, "sources": [source]}), encoding="utf-8")
                if valid:
                    citation = resolve_source_citation("test-source", "Bar 8", registry)
                    self.assertEqual((citation.source_id, citation.locator), ("test-source", "Bar 8"))
                    with self.assertRaises(PublicationError):
                        resolve_source_citation("other-source", "Bar 8", registry)
                else:
                    with self.assertRaises(PublicationError):
                        resolve_source_citation("test-source", "Bar 8", registry)
