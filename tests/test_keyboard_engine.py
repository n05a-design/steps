"""Interactive music engine: recognition, voice motion, practice, input, live ports, session sync."""

import tempfile
import unittest
from pathlib import Path

from app.ui.session_controller import ProgressionSessionController
from src.steps.keyboard import (
    CandidateKind,
    Direction,
    EvaluationPolicy,
    Exercise,
    InputSource,
    KeyboardInputState,
    KeyboardMode,
    KeyboardWorkbench,
    KeyState,
    MotionKind,
    Reason,
    RecognitionStatus,
    Verdict,
    compare_voicings,
    evaluate,
    pilot_exercises,
    recognize_chord,
)
from src.steps.ports.audio import NullAudioBackend
from src.steps.midi import SMFParser
from src.steps.ports.live import (
    LiveEventKind,
    LiveNoteEvent,
    MidiInputDevice,
    NotePreviewService,
    ScriptedMidiInput,
    normalize_midi_message,
)
from src.steps.progression.session import ProgressionSession
from src.steps.theory import construct_scale, parse_spelling
from src.steps.theory.chord import CHORD_TEMPLATES


def complete(result):
    return [c for c in result.candidates if c.kind is not CandidateKind.INCOMPLETE]


def symbols(result, convention="INT"):
    return [c.symbol(convention) for c in complete(result)]


class TestChordRecognition(unittest.TestCase):
    def test_trivial_inputs(self):
        self.assertEqual(recognize_chord([]).status, RecognitionStatus.EMPTY)
        self.assertEqual(recognize_chord([60]).status, RecognitionStatus.SINGLE_NOTE)
        self.assertEqual(recognize_chord([48, 60, 72]).status, RecognitionStatus.SINGLE_NOTE)
        interval = recognize_chord([60, 64])
        self.assertEqual((interval.status, interval.interval_semitones), (RecognitionStatus.INTERVAL, 4))
        self.assertEqual(recognize_chord([64, 72]).interval_semitones, 8)  # minor sixth above the bass E

    def test_complete_triads_and_sevenths_are_exact(self):
        cases = {
            (60, 64, 67): "C", (60, 63, 67): "Cm", (62, 65, 68): "Ddim",
            (55, 59, 62, 65): "G7", (60, 64, 67, 71): "Cmaj7", (57, 60, 64): "Am",
        }
        for notes, expected in cases.items():
            with self.subTest(expected=expected):
                result = recognize_chord(notes)
                self.assertEqual(result.status, RecognitionStatus.EXACT_MATCH)
                self.assertEqual(symbols(result), [expected])
                self.assertIn(Reason.ROOT_IN_BASS, result.candidates[0].reasons)

    def test_minor_seventh_and_half_diminished_share_sets_with_sixth_chords(self):
        # Same pitch classes, different readings: no artificial uniqueness.
        cases = {(62, 65, 69, 72): ("Dm7", "F6/D"), (59, 62, 65, 69): ("Bm7b5", "Dm6/B")}
        for notes, (first, other) in cases.items():
            with self.subTest(first=first):
                result = recognize_chord(notes)
                self.assertEqual(result.status, RecognitionStatus.AMBIGUOUS)
                self.assertEqual(symbols(result)[0], first)
                self.assertIn(other, symbols(result))

    def test_inversions_order_and_doublings_do_not_change_identity(self):
        for notes in ((64, 67, 72), (52, 60, 67, 72, 76), (64, 72, 79), (76, 67, 72, 64, 64)):
            with self.subTest(notes=notes):
                result = recognize_chord(notes)
                self.assertEqual(result.status, RecognitionStatus.EXACT_MATCH)
                self.assertEqual(symbols(result), ["C/E"])
                self.assertEqual(result.candidates[0].figured_bass, "6")
                self.assertIn(Reason.INVERSION_BASS, result.candidates[0].reasons)
        doubled = recognize_chord([48, 60, 64, 67])
        self.assertIn(Reason.DOUBLED_TONES, doubled.candidates[0].reasons)
        self.assertEqual(recognize_chord([60, 60, 64, 67]).notes, (60, 64, 67))  # duplicate events

    def test_g7_over_d_is_second_inversion(self):
        result = recognize_chord([50, 53, 55, 59])  # D3 F3 G3 B3
        self.assertEqual(symbols(result), ["G7/D"])
        self.assertEqual(result.candidates[0].figured_bass, "4/3")

    def test_c6_and_am7_stay_ambiguous(self):
        for notes, first in (((60, 64, 67, 69), "C6"), ((57, 60, 64, 67), "Am7")):
            with self.subTest(notes=notes):
                result = recognize_chord(notes)
                self.assertEqual(result.status, RecognitionStatus.AMBIGUOUS)
                self.assertEqual(set(symbols(result)), {"C6", "Am7/C"} if first == "C6" else {"Am7", "C6/A"})
                self.assertEqual(symbols(result)[0], first)  # root-in-bass reading listed first

    def test_symmetric_chords_list_every_root(self):
        dim7 = recognize_chord([60, 63, 66, 69])
        self.assertEqual(dim7.status, RecognitionStatus.AMBIGUOUS)
        self.assertEqual(sorted(int(c.chord.root.pitch_class) for c in complete(dim7)), [0, 3, 6, 9])
        aug = recognize_chord([60, 64, 68])
        self.assertEqual(sorted(int(c.chord.root.pitch_class) for c in complete(aug)), [0, 4, 8])
        sus = recognize_chord([60, 62, 67])  # Csus2 = Gsus4/C
        self.assertEqual(set(symbols(sus)), {"Csus2", "Gsus4/C"})

    def test_incomplete_only_when_fifth_is_omitted(self):
        result = recognize_chord([60, 64, 70])
        self.assertEqual(result.status, RecognitionStatus.INCOMPLETE)
        self.assertEqual([c.symbol() for c in result.candidates], ["C7"])
        self.assertEqual([r.value for r in result.candidates[0].missing_roles], ["PERFECT_FIFTH"])
        for notes in ((60, 61, 62), (60, 61, 66), (60, 65, 66, 71)):
            with self.subTest(notes=notes):
                self.assertEqual(recognize_chord(notes).status, RecognitionStatus.UNSUPPORTED)
                self.assertEqual(recognize_chord(notes).candidates, ())

    def test_template_standard_voicing_is_named(self):
        result = recognize_chord([48, 52, 58, 62])  # C E Bb D: C9 voiced without fifth
        kinds = {c.symbol(): c.kind for c in result.candidates}
        self.assertEqual(kinds.get("C9"), CandidateKind.STANDARD_VOICING)
        self.assertIn(Reason.OMITS_FIFTH_BY_TEMPLATE, next(c for c in result.candidates if c.symbol() == "C9").reasons)

    def test_every_template_on_every_root_is_found(self):
        for quality, template in CHORD_TEMPLATES.items():
            for root_pc in range(12):
                notes = sorted({48 + root_pc + s for s in template["theoretical"]})
                with self.subTest(quality=quality, root=root_pc):
                    result = recognize_chord(notes)
                    found = {(int(c.chord.root.pitch_class), c.chord.quality) for c in complete(result)}
                    self.assertIn((root_pc, quality), found)

    def test_key_context_controls_spelling_and_reasons(self):
        f_major = construct_scale(parse_spelling("F", "INT"), "ionian")
        result = recognize_chord([58, 62, 65], key=f_major)  # Bb major
        self.assertEqual(symbols(result), ["Bb"])
        self.assertEqual(result.candidates[0].spelling_basis, "KEY_CONTEXT")
        self.assertIn(Reason.ALL_TONES_IN_KEY, result.candidates[0].reasons)
        e_major = construct_scale(parse_spelling("E", "INT"), "ionian")
        sharp = recognize_chord([63, 67, 70], key=e_major)  # pcs 3, 7, 10 → D#? only root pc 3 is in E major
        self.assertEqual(sharp.candidates[0].symbol(), "D#")
        self.assertIn(Reason.TONES_OUTSIDE_KEY, sharp.candidates[0].reasons)
        no_key = recognize_chord([63, 67, 70])
        self.assertEqual(no_key.candidates[0].symbol(), "Eb")
        self.assertEqual(no_key.candidates[0].spelling_basis, "DEFAULT_TABLE")
        self.assertEqual(no_key.candidates[0].symbol("DE"), "Es")

    def test_no_confidence_scores_are_exposed(self):
        candidate = recognize_chord([60, 64, 67]).candidates[0]
        self.assertFalse(any("confidence" in name or "score" in name for name in vars(candidate)))


class TestVoiceMotion(unittest.TestCase):
    def test_ii_v_i_reference_voice_leading(self):
        dm7 = (50, 53, 57, 60)   # D3 F3 A3 C4
        g7_d = (50, 53, 55, 59)  # D3 F3 G3 H3
        cmaj7 = (48, 52, 55, 59)  # C3 E3 G3 H3
        first = compare_voicings(dm7, g7_d)
        self.assertTrue(first.paired)
        self.assertEqual([(m.semitones, m.kind) for m in first.motions], [
            (0, MotionKind.HELD), (0, MotionKind.HELD), (-2, MotionKind.WHOLE_TONE), (-1, MotionKind.SEMITONE),
        ])
        self.assertEqual(first.held_pitches, (50, 53))
        second = compare_voicings(g7_d, cmaj7)
        self.assertEqual([(m.start, m.end, m.semitones) for m in second.motions], [
            (50, 48, -2), (53, 52, -1), (55, 55, 0), (59, 59, 0),
        ])
        self.assertEqual([m.direction for m in second.motions][:2], [Direction.DOWN, Direction.DOWN])
        self.assertEqual(second.total_movement, 3)
        self.assertEqual(recognize_chord(g7_d).candidates[0].symbol(), "G7/D")

    def test_unequal_voice_counts_are_not_force_paired(self):
        result = compare_voicings((48, 52, 55), (47, 50, 55, 65))
        self.assertFalse(result.paired)
        self.assertEqual(result.motions, ())
        self.assertIsNone(result.total_movement)
        self.assertEqual(result.held_pitches, (55,))
        self.assertEqual(result.added_pitches, (47, 50, 65))
        self.assertEqual(result.removed_pitches, (48, 52))

    def test_same_pitch_class_in_other_octave_is_not_a_held_tone(self):
        result = compare_voicings((48, 52, 55), (52, 55, 60))
        self.assertEqual(result.held_pitches, (52, 55))
        self.assertEqual(result.common_pitch_classes_moved, (0,))
        self.assertEqual([m.kind for m in result.motions], [MotionKind.LEAP, MotionKind.LEAP, MotionKind.LEAP])


class TestPracticePilot(unittest.TestCase):
    def setUp(self):
        self.exercises = {e.exercise_id: e for e in pilot_exercises()}

    def test_pilot_is_marked_unreviewed_and_unpublishable(self):
        self.assertEqual(len(self.exercises), 6)
        for exercise in self.exercises.values():
            self.assertEqual(exercise.review_status, "AI_DRAFT_UNREVIEWED")
            self.assertFalse(exercise.publishable)
        with self.assertRaises(ValueError):
            Exercise("x", "notes", "o", "p", 1, EvaluationPolicy.EXACT_PITCHES, expected_pitches=(60,),
                     publishable=True)

    def test_reference_solutions_are_correct(self):
        solutions = {
            "pilot.find_c4": (60,),
            "pilot.c_major_triad": (48, 52, 55),
            "pilot.a_minor_triad": (57, 60, 64),
            "pilot.c_major_first_inversion": (52, 55, 60),
            "pilot.g7": (43, 59, 62, 65),
            "pilot.major_third_above_c4": (60, 64),
        }
        for exercise_id, notes in solutions.items():
            with self.subTest(exercise=exercise_id):
                exercise = self.exercises[exercise_id]
                self.assertEqual(evaluate(exercise, notes).verdict, Verdict.CORRECT)
                self.assertEqual(evaluate(exercise, exercise.reference_notes).verdict, Verdict.CORRECT)

    def test_policies_distinguish_octave_bass_and_extra_tones(self):
        find_c4 = self.exercises["pilot.find_c4"]
        self.assertEqual(evaluate(find_c4, [72]).message_key, "practice.feedback.wrong_octave")
        self.assertEqual(evaluate(find_c4, [61]).verdict, Verdict.INCORRECT)
        self.assertEqual(evaluate(find_c4, [60, 64]).verdict, Verdict.PARTIAL)
        c_major = self.exercises["pilot.c_major_triad"]
        self.assertEqual(evaluate(c_major, [72, 76, 79, 84]).verdict, Verdict.CORRECT)  # any octave, doubling
        extra = evaluate(c_major, [60, 62, 64, 67])
        self.assertEqual((extra.verdict, extra.extra_pitch_classes), (Verdict.PARTIAL, (2,)))
        missing = evaluate(c_major, [60, 64])
        self.assertEqual(missing.missing_pitch_classes, (7,))
        inversion = self.exercises["pilot.c_major_first_inversion"]
        root_position = evaluate(inversion, [60, 64, 67])
        self.assertEqual((root_position.verdict, root_position.bass_correct), (Verdict.PARTIAL, False))
        self.assertEqual(root_position.message_key, "practice.feedback.wrong_bass")
        g7 = evaluate(self.exercises["pilot.g7"], [55, 59, 62])
        self.assertEqual((g7.verdict, g7.missing_pitch_classes), (Verdict.PARTIAL, (5,)))
        self.assertEqual(evaluate(c_major, []).verdict, Verdict.EMPTY)
        self.assertEqual(evaluate(c_major, [61, 63]).verdict, Verdict.INCORRECT)


class TestInputAndLivePorts(unittest.TestCase):
    def test_pressed_and_selected_are_separate(self):
        state = KeyboardInputState()
        self.assertTrue(state.press(60))
        self.assertFalse(state.press(60))  # auto-repeat
        state.toggle_selected(64)
        self.assertEqual(state.active_notes, (60, 64))
        self.assertTrue(state.release(60))
        self.assertFalse(state.release(60))
        self.assertEqual(state.active_notes, (64,))
        state.press(67)
        self.assertEqual(state.release_all(), (67,))
        self.assertEqual(state.selected, {64})
        with self.assertRaises(ValueError):
            state.press(60, velocity=0)

    def test_sustain_keeps_released_notes_until_pedal_up(self):
        state = KeyboardInputState()
        state.set_sustain(True)
        state.press(60)
        state.release(60)
        self.assertEqual(state.sounding, (60,))
        state.set_sustain(False)
        self.assertEqual(state.sounding, ())

    def test_midi_messages_normalize_note_on_velocity_zero_and_controllers(self):
        self.assertEqual(normalize_midi_message(0x90, 60, 100).kind, LiveEventKind.NOTE_ON)
        self.assertEqual(normalize_midi_message(0x90, 60, 0).kind, LiveEventKind.NOTE_OFF)
        self.assertEqual(normalize_midi_message(0x83, 60, 64).channel, 3)
        sustain = normalize_midi_message(0xB0, 64, 127)
        self.assertEqual((sustain.kind, sustain.value), (LiveEventKind.SUSTAIN, 127))
        self.assertEqual(normalize_midi_message(0xB2, 123, 0).kind, LiveEventKind.ALL_NOTES_OFF)
        self.assertIsNone(normalize_midi_message(0xE0, 0, 64))  # pitch bend ignored
        self.assertIsNone(normalize_midi_message(0xF8))  # clock ignored
        with self.assertRaises(ValueError):
            LiveNoteEvent(LiveEventKind.NOTE_ON, 60, 0)

    def test_virtual_and_physical_input_share_one_path(self):
        state = KeyboardInputState()
        device = ScriptedMidiInput([MidiInputDevice("test", "Test keyboard")])
        device.open("test", lambda event: state.apply(event, InputSource.MIDI_DEVICE))
        device.feed(0x90, 60, 90)
        device.feed(0x90, 64, 90)
        device.feed(0x90, 67, 90)
        self.assertEqual(recognize_chord(state.active_notes).candidates[0].symbol(), "C")
        device.feed(0x90, 64, 0)
        self.assertEqual(state.sounding, (60, 67))
        device.close()  # disconnect must not leave hung notes
        self.assertEqual(state.sounding, ())
        with self.assertRaises(LookupError):
            device.open("missing", lambda event: None)

    def test_preview_service_never_leaves_hung_notes(self):
        backend = NullAudioBackend()
        preview = NotePreviewService(backend)
        preview.preview_chord([60, 64, 67])
        self.assertEqual(preview.sounding, (60, 64, 67))
        preview.note_on(60)  # retrigger
        preview.all_notes_off()
        self.assertEqual(preview.sounding, ())
        ons = sum(1 for _, e in backend.events_recorded if e.event_type == "note_on")
        offs = sum(1 for _, e in backend.events_recorded if e.event_type == "note_off")
        self.assertEqual(ons, offs)
        self.assertGreaterEqual(backend.all_notes_off_count, 1)


class TestWorkbenchSessionIntegration(unittest.TestCase):
    def setUp(self):
        self.controller = ProgressionSessionController(
            ProgressionSession(["Dm7", "G7/D", "Cmaj7", "C/E"], key_root="C")
        )
        self.workbench = KeyboardWorkbench(lambda: self.controller.session)

    def snapshot(self):
        session = self.controller.session
        return (repr(session.state), session.is_dirty, session.can_undo, self.controller.revision)

    def test_selected_chord_shows_the_session_voicing(self):
        self.workbench.select(2)
        info = self.workbench.chord_info()
        self.assertEqual(info.symbol, "Cmaj7")
        expected = tuple(self.controller.session.get_voicings("CLOSE")[2].midi_notes)
        self.assertEqual(info.voicing.midi_notes, expected)
        self.assertEqual(info.roman, self.controller.harmonic_degree_at(2))
        slash = self.workbench.chord_info(3)
        self.assertFalse(slash.voicing.bass.is_root)
        self.assertEqual(slash.voicing.bass.midi % 12, 4)

    def test_previews_never_change_project_state(self):
        before = self.snapshot()
        wb = self.workbench
        for voicing in ("CLOSE", "DROP2", "SHELL", "ROOTLESS"):
            wb.set_voicing_type(voicing)
            for index in range(4):
                wb.select(index)
                wb.rotate(1)
                wb.chord_info()
                wb.view_model()
        wb.show_scale = True
        wb.compare_previous = True
        wb.view_model()
        wb.mode = KeyboardMode.FREE_INPUT
        wb.input.toggle_selected(60)
        wb.view_model()
        wb.mode = KeyboardMode.PRACTICE
        wb.check_practice()
        wb.show_practice_solution = True
        wb.view_model()
        self.assertEqual(self.snapshot(), before)

    def test_unavailable_voicing_is_reported_not_invented(self):
        self.controller.add_chord("C")
        self.workbench.set_voicing_type("DROP2")
        info = self.workbench.chord_info(4)
        self.assertIsNone(info.voicing)
        self.assertTrue(info.error)

    def test_rotation_preview_changes_bass_only_in_preview(self):
        wb = self.workbench
        wb.select(2)
        base = wb.chord_info().voicing.midi_notes
        wb.rotate(1)
        rotated = wb.chord_info().voicing
        self.assertNotEqual(rotated.midi_notes, base)
        self.assertEqual({n % 12 for n in rotated.midi_notes}, {n % 12 for n in base})
        wb.select(1)
        self.assertEqual(wb.rotation, 0)  # new chord resets the temporary inversion

    def test_sync_after_undo_redo_remove_and_project_switch(self):
        wb = self.workbench
        self.controller.add_chord("Am")
        wb.select(4)
        self.controller.undo()
        wb.sync()
        self.assertEqual(wb.selected_index, 3)
        self.controller.redo()
        wb.sync()
        self.assertEqual(wb.chord_info(4).symbol, "Am")
        self.controller.new_project()
        wb.sync()
        self.assertEqual(wb.chord_info().symbol, self.controller.session.chords[wb.selected_index])
        replacement = ProgressionSession(["E"], key_root="E")
        self.controller._session = replacement
        wb.sync()
        self.assertEqual((wb.selected_index, wb.chord_info().symbol), (0, "E"))

    def test_transposition_updates_keyboard_from_session(self):
        wb = self.workbench
        wb.select(0)
        before = wb.chord_info().voicing.midi_notes
        self.controller.transpose(2)
        after = wb.chord_info().voicing.midi_notes
        self.assertEqual(wb.chord_info().symbol, "Em7")
        self.assertEqual({(n + 2) % 12 for n in before}, {n % 12 for n in after})

    def test_notation_switch_keeps_midi_and_changes_names(self):
        session = ProgressionSession(["Bb", "B7", "F#m"], key_root="F#", is_minor=True)
        controller = ProgressionSessionController(session)
        wb = KeyboardWorkbench(lambda: controller.session)
        before = [wb.chord_info(i).voicing.midi_notes for i in range(3)]
        controller.set_notation_convention("DE")
        after = [wb.chord_info(i).voicing.midi_notes for i in range(3)]
        self.assertEqual(before, after)
        self.assertEqual(controller.session.chords, ["B", "H7", "Fism"])
        names = [n.name("DE") for n in wb.chord_info(1).voicing.notes]
        self.assertTrue(all(name[0] in "HDFA" for name in names), names)
        self.assertIn("Dis", "".join(names))
        self.assertEqual(wb.chord_info(0).tones[0].name("DE"), "B")

    def test_save_and_load_round_trip_keeps_keyboard_view(self):
        wb = self.workbench
        wb.select(1)
        before = wb.chord_info().voicing.midi_notes
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "keyboard.steps.json"
            self.controller.save(path)
            other = ProgressionSessionController(ProgressionSession(["C"]))
            other.load(path)
            reloaded = KeyboardWorkbench(lambda: other.session)
            reloaded.select(1)
            self.assertEqual(reloaded.chord_info().voicing.midi_notes, before)

    def test_recognised_chord_enters_project_only_through_undoable_command(self):
        wb = self.workbench
        wb.mode = KeyboardMode.FREE_INPUT
        for note in (57, 60, 64):
            wb.input.toggle_selected(note)
        candidate = wb.recognition().candidates[0]
        before = self.snapshot()
        self.assertEqual(self.snapshot(), before)
        symbol = wb.project_symbol_for(candidate)
        self.controller.add_chord(symbol)
        self.assertEqual(self.controller.session.chords[-1], "Am")
        self.assertTrue(self.controller.session.can_undo)
        self.controller.undo()
        self.assertEqual(self.controller.session.chords, ["Dm7", "G7/D", "Cmaj7", "C/E"])

    def test_keyboard_adoption_survives_history_and_project_reload_before_midi_export(self):
        controller = ProgressionSessionController(ProgressionSession(["G7"], key_root="C", convention="INT"))
        wb = KeyboardWorkbench(lambda: controller.session)
        for midi in (60, 64, 67):
            wb.input.toggle_selected(midi)
        candidate = next(c for c in wb.recognition().candidates if c.symbol() == "C")
        self.assertEqual(controller.session.chords, ["G7"])
        controller.add_chord(wb.project_symbol_for(candidate))
        self.assertEqual(controller.session.harmonic_degree_at(1), "I")
        wb.select(1)
        wb.rotate(2)
        self.assertEqual(wb.chord_info().voicing.bass.midi % 12, 4)
        controller.undo()
        self.assertEqual(controller.session.chords, ["G7"])
        controller.redo()
        self.assertEqual(controller.session.chords, ["G7", "C"])

        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / "keyboard.steps.json"
            controller.save(project)
            restored = ProgressionSessionController(ProgressionSession(["Am"]))
            restored.load(project)
            path = restored.session.export_midi_file(Path(folder) / "keyboard.mid")
            parsed = SMFParser.parse(path.read_bytes())
        bass = sorted((note.start_tick, note.pitch) for note in parsed.all_notes if note.channel == 1)
        self.assertEqual(bass, [(0, 43), (1920, 36)])
        chord = [note.pitch for note in parsed.all_notes if note.channel == 0 and note.start_tick == 1920]
        self.assertEqual(sorted(note % 12 for note in chord), [0, 0, 4, 7])

    def test_project_symbol_uses_project_convention(self):
        controller = ProgressionSessionController(ProgressionSession(["C"], convention="DE"))
        wb = KeyboardWorkbench(lambda: controller.session)
        for note in (58, 62, 65):
            wb.input.toggle_selected(note)
        symbol = wb.project_symbol_for(wb.recognition().candidates[0])
        self.assertEqual(symbol, "B")  # B-flat major in German notation
        controller.add_chord(symbol)
        self.assertEqual(controller.session.get_voicings()[-1].midi_notes[0] % 12, 10)

    def test_progression_view_marks_root_and_bass_of_selected_voicing(self):
        wb = self.workbench
        wb.select(3)  # C/E
        model = wb.view_model()
        info = wb.chord_info()
        bass = model.visual(info.voicing.bass.midi)
        self.assertIn(KeyState.CHORD_BASS, bass.states)
        self.assertNotIn(KeyState.CHORD_ROOT, bass.states)
        root_key = model.visual(info.voicing.root_midis[0])
        self.assertIn(KeyState.CHORD_ROOT, root_key.states)
        for note in info.voicing.midi_notes:
            self.assertTrue(model.viewport.contains(note))

    def test_compare_previous_marks_held_pitches(self):
        session = ProgressionSession(["Dm7", "G7/D"], key_root="C")
        wb = KeyboardWorkbench(lambda: session)
        wb.select(1)
        wb.compare_previous = True
        comparison = wb.comparison()
        model = wb.view_model()
        for note in comparison.held_pitches:
            self.assertIn(KeyState.COMPARISON_HELD, model.visual(note).states)

    def test_practice_marks_solution_and_mistakes_without_touching_project(self):
        before = self.snapshot()
        wb = self.workbench
        wb.mode = KeyboardMode.PRACTICE
        wb.select_exercise(1)  # C major triad
        for note in (60, 62, 64):
            wb.input.toggle_selected(note)
        feedback = wb.check_practice()
        self.assertEqual(feedback.verdict, Verdict.PARTIAL)
        model = wb.view_model()
        self.assertIn(KeyState.PRACTICE_WRONG, model.visual(62).states)
        self.assertIn(KeyState.PRACTICE_CORRECT, model.visual(60).states)
        wb.show_practice_solution = True
        missing = [k.midi for k in wb.view_model().keys if KeyState.PRACTICE_MISSING in k.states]
        self.assertEqual([m % 12 for m in missing], [7])
        self.assertEqual(self.snapshot(), before)


class TestReviewRegressions(unittest.TestCase):
    """Hand-written expectations for findings of the independent review (2026-11-26)."""

    def figure(self, notes, symbol):
        result = recognize_chord(notes)
        return next(c for c in result.candidates if c.symbol() == symbol)

    def test_seventh_figures_without_a_fifth(self):
        self.assertEqual(self.figure([48, 52, 58], "C7").figured_bass, "7")          # C E Bb
        bb_bass = self.figure([46, 48, 52], "C7/Bb")                                  # Bb C E
        self.assertEqual((bb_bass.figured_bass, bb_bass.bass_role.value), ("4/2", "MINOR_SEVENTH"))
        self.assertEqual(self.figure([52, 58, 60, 62], "C9/E").figured_bass, "6/5")   # E Bb C D

    def test_shell_and_rootless_voicings_get_seventh_figures(self):
        from src.steps.keyboard import label_voicing
        from src.steps.theory import parse_chord
        g7 = parse_chord("G7", "INT")
        self.assertEqual(label_voicing(g7, (55, 59, 65)).inversion.figured_bass, "7")   # G B F
        self.assertEqual(label_voicing(g7, (53, 55, 59)).inversion.figured_bass, "4/2")  # F G B
        dm7 = parse_chord("Dm7", "INT")
        self.assertEqual(label_voicing(dm7, (48, 53, 57)).inversion.figured_bass, "4/2")  # C F A, rootless

    def test_foreign_note_gets_non_chord_tone_role(self):
        from src.steps.keyboard import ChordToneRole, label_voicing
        from src.steps.theory import parse_chord
        labelled = label_voicing(parse_chord("C", "INT"), (60, 62, 64, 67))
        self.assertEqual(labelled.notes[1].role, ChordToneRole.NON_CHORD_TONE)
        self.assertEqual(labelled.foreign_notes, (62,))

    def test_ambiguous_free_input_does_not_spell_by_one_hidden_reading(self):
        wb = KeyboardWorkbench(lambda: ProgressionSession(["C"]))
        wb.mode = KeyboardMode.FREE_INPUT
        wb.input.set_selected([60, 63, 66, 69])  # dim7: A could be A or Bbb
        model = wb.view_model()
        self.assertEqual(model.visual(69).label, "")
        self.assertIn("●", model.visual(69).badges)  # still marked without colour
        wb.input.set_selected([60, 64, 67])  # unique reading: names shown
        self.assertEqual(wb.view_model().visual(64).label, "E4")

    def test_unrealisable_voicing_message_is_localized(self):
        from app.i18n import LocaleManager
        from app.ui.keyboard_dialog import describe_workbench
        wb = KeyboardWorkbench(lambda: ProgressionSession(["C"]))
        wb.set_voicing_type("DROP2")
        for language in ("en", "de"):
            t = LocaleManager(preference=language).translate
            text = describe_workbench(wb, t)
            self.assertIn(t("keyboard.info.voicing_error", symbol="C"), text)
            self.assertNotIn("Drop-2 requires", text)


if __name__ == "__main__":
    unittest.main()
