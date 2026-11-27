"""Independent trace oracles for supported single-source keyboard and session behavior."""

import random
import unittest

from src.steps.keyboard import KeyboardInputState
from src.steps.ports.live import normalize_midi_message
from src.steps.progression import ProgressionSession

try:
    from hypothesis import given, settings, strategies as st
except ImportError:
    given = None

OPERATIONS = ("on", "off", "pedal", "toggle", "reset")


def check_keyboard_trace(test, trace):
    state = KeyboardInputState()
    # Independent reference representation: a note is in the physical list
    # while held, and in the voices list from onset until it stops sounding.
    physical, voices, selected = [], [], []
    pedal = False
    for step, (action, value) in enumerate(trace):
        if action == "on":
            if value not in physical:
                physical.append(value)
            if value not in voices:
                voices.append(value)
            state.apply(normalize_midi_message(0x90, value, 96))
        elif action == "off":
            if value in physical:
                physical.remove(value)
                if not pedal:
                    voices.remove(value)
            state.apply(normalize_midi_message(0x90, value, 0))
        elif action == "pedal":
            pedal = value >= 64
            if not pedal:
                voices[:] = physical
            state.apply(normalize_midi_message(0xB0, 64, value))
        elif action == "toggle":
            if value in selected:
                selected.remove(value)
            else:
                selected.append(value)
            state.toggle_selected(value)
        else:
            physical.clear()
            voices.clear()
            pedal = False
            state.release_all()
        observed = (sorted(state.pressed), sorted(state.sustained), list(state.sounding),
                    sorted(state.selected), list(state.active_notes), state.sustain_down)
        expected = (sorted(physical), sorted(set(voices) - set(physical)), sorted(voices),
                    sorted(selected), sorted(set(voices) | set(selected)), pedal)
        test.assertEqual(observed, expected, (step, trace[:step + 1]))


class KeyboardStateAudit(unittest.TestCase):
    def test_sustain_boundary_retrigger_and_panic_preserve_selection(self):
        trace = [
            ("toggle", 64), ("on", 60), ("pedal", 63), ("off", 60),
            ("on", 60), ("pedal", 64), ("off", 60), ("off", 60),
            ("on", 60), ("pedal", 0), ("reset", 0), ("off", 60), ("on", 60),
        ]
        check_keyboard_trace(self, trace)

    def test_seeded_traces_verify_each_intermediate_state(self):
        for seed in range(64):
            rng = random.Random(seed)
            trace = []
            for _ in range(96):
                action = rng.choice(OPERATIONS)
                values = (0, 63, 64, 127) if action == "pedal" else (0, 60, 64, 67, 127)
                trace.append((action, rng.choice(values)))
            check_keyboard_trace(self, trace)

    def test_normalization_across_all_channels_and_controller_boundary(self):
        for channel in range(16):
            for note in (0, 60, 127):
                for velocity in (0, 1, 127):
                    event = normalize_midi_message(0x90 + channel, note, velocity)
                    self.assertEqual((event.kind.value, event.note, event.channel, event.velocity),
                                     ("NOTE_ON" if velocity else "NOTE_OFF", note, channel, velocity))
            for value in (63, 64):
                event = normalize_midi_message(0xB0 + channel, 64, value)
                self.assertEqual((event.kind.value, event.channel, event.value), ("SUSTAIN", channel, value))


def proposed_multi_source_trace(events):
    """Pure ADR-019 candidate; outputs identity-bearing sounding snapshots."""
    pressed = set()
    latched = set()
    pedals = set()
    for action, device, channel, note in events:
        endpoint = (device, channel)
        identity = (*endpoint, note)
        if action == "on":
            pressed.add(identity)
            latched.discard(identity)
        elif action == "off":
            if identity in pressed and endpoint in pedals:
                latched.add(identity)
            pressed.discard(identity)
        elif action == "hold":
            pedals.add(endpoint)
        elif action in {"pedal-up", "reset-controllers"}:
            pedals.discard(endpoint)
            latched = {key for key in latched if key[:2] != endpoint}
        elif action == "all-notes-off":
            released = {key for key in pressed if key[:2] == endpoint}
            pressed -= released
            if endpoint in pedals:
                latched |= released
        elif action == "all-sound-off":
            pressed = {key for key in pressed if key[:2] != endpoint}
            latched = {key for key in latched if key[:2] != endpoint}
        elif action == "disconnect":
            pressed = {key for key in pressed if key[0] != device}
            latched = {key for key in latched if key[0] != device}
            pedals = {key for key in pedals if key[0] != device}
        elif action == "panic":
            pressed.clear()
            latched.clear()
            pedals.clear()
        else:
            raise ValueError(action)
        yield pressed | latched


class MidiContractProposalTest(unittest.TestCase):
    def test_candidate_endpoint_and_channel_mode_trace(self):
        a, b, c = ("A", 0, 60), ("A", 1, 60), ("B", 0, 60)
        trace = [
            ("on", *a), ("on", *b), ("on", *c), ("on", *a), ("off", *a),
            ("hold", *b), ("all-notes-off", *b), ("all-sound-off", *c), ("reset-controllers", *b),
            ("on", *a), ("on", *c), ("hold", *a), ("off", *a),
            ("disconnect", *a), ("panic", *a), ("on", *b),
        ]
        expected = [{a}, {a, b}, {a, b, c}, {a, b, c}, {b, c}, {b, c}, {b, c}, {b}, set(),
                    {a}, {a, c}, {a, c}, {a, c}, {c}, set(), {b}]
        self.assertEqual(list(proposed_multi_source_trace(trace)), expected)


class HypothesisMusicAudit(unittest.TestCase):
    if given is None:
        @unittest.skip("The isolated Hypothesis test dependency is unavailable.")
        def test_hypothesis_dependencies(self):
            pass
    else:
        @settings(max_examples=150)
        @given(st.lists(st.tuples(st.sampled_from(OPERATIONS),
                                 st.sampled_from((0, 60, 63, 64, 67, 127))), min_size=1, max_size=128))
        def test_keyboard_transitions(self, trace):
            check_keyboard_trace(self, trace)

        @settings(max_examples=150)
        @given(st.lists(st.sampled_from(("G", "Am", "F", "undo", "redo")), min_size=1, max_size=64))
        def test_session_history(self, commands):
            session = ProgressionSession(["C"], key_root="C", convention="INT")
            history = [("C",)]
            cursor = 0
            for index, command in enumerate(commands):
                if command == "undo":
                    if cursor > 0:
                        session.undo()
                        cursor -= 1
                elif command == "redo":
                    if cursor + 1 < len(history):
                        session.redo()
                        cursor += 1
                else:
                    session.add_chord(command)
                    history[cursor + 1:] = [(*history[cursor], command)]
                    cursor += 1
                self.assertEqual(tuple(session.chords), history[cursor], commands[:index + 1])
                self.assertEqual(session.can_undo, cursor > 0)
                self.assertEqual(session.can_redo, cursor + 1 < len(history))
