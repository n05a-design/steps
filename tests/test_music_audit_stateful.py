"""Independent trace oracles for supported single-source keyboard and session behavior."""

import random
import unittest

from src.steps.midi import MidiParseError, SMFParser, decode_vlq, encode_vlq
from itertools import combinations
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
                    self.assertIsNotNone(event)
                    self.assertEqual((event.kind.value, event.note, event.channel, event.velocity),
                                     ("NOTE_ON" if velocity else "NOTE_OFF", note, channel, velocity))
            for value in (63, 64):
                event = normalize_midi_message(0xB0 + channel, 64, value)
                self.assertIsNotNone(event)
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
    def test_candidate_interleavings_keep_independent_endpoints(self):
        left, right = ("midi:A", 0, 60), ("midi:B", 0, 60)
        a_trace = (("on", *left), ("hold", *left), ("off", *left), ("disconnect", *left))
        b_trace = (("on", *right), ("on", *right), ("off", *right))
        # Independently tabulated projections after each endpoint-local action.
        a_active = (False, True, True, True, False)
        b_active = (False, True, True, False)
        for indices in combinations(range(len(a_trace) + len(b_trace)), len(a_trace)):
            prefix_a = prefix_b = 0
            merged, expected = [], []
            for pos in range(len(a_trace) + len(b_trace)):
                if pos in indices:
                    merged.append(a_trace[prefix_a])
                    prefix_a += 1
                else:
                    merged.append(b_trace[prefix_b])
                    prefix_b += 1
                expected.append(({left} if a_active[prefix_a] else set())
                                | ({right} if b_active[prefix_b] else set()))
            self.assertEqual(list(proposed_multi_source_trace(merged)), expected, indices)

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


def framed_track(payload):
    return bytes.fromhex("4d546864 00000006 0000 0001 01e0 4d54726b") + len(payload).to_bytes(4, "big") + payload


class SMFTrackAudit(unittest.TestCase):
    def test_framed_invalid_events_have_the_parser_error_type(self):
        for raw in ("00", "80", "00 ff 01 80", "00 f0 80", "00 c0 80",
                    "00 90 3c 90", "00 90 3c 40 00 3c 80"):
            with self.subTest(track=raw), self.assertRaises(MidiParseError):
                SMFParser.parse(framed_track(bytes.fromhex(raw)))

    def test_eot_sysex_and_unsupported_timebase_are_distinct(self):
        good = bytes.fromhex("00 f0 03 01 02 f7 00 ff 58 04 03 03 18 08 00 ff 2f 00")
        result = SMFParser.parse(framed_track(good))
        self.assertEqual(result.time_signatures, [(0, 3, 8)])
        self.assertEqual(result.tracks[0].events[0].raw_bytes, bytes.fromhex("f0 03 01 02 f7"))
        for bad in ("00 f0 03 01", "00 ff 2f 01 00", "00 ff 2f 00 00 90 3c 40"):
            with self.subTest(payload=bad), self.assertRaises(MidiParseError):
                SMFParser.parse(framed_track(bytes.fromhex(bad)))
        full = framed_track(good)
        for variant, message in (
            (full[:8] + bytes.fromhex("0002") + full[10:], "Unsupported SMF format 2"),
            (full[:12] + bytes.fromhex("e728") + full[14:], "SMPTE division format"),
        ):
            with self.assertRaisesRegex(MidiParseError, message):
                SMFParser.parse(variant)

    def test_overlap_pairs_fifo_on_each_channel_at_scale(self):
        count = 4000
        repeated = bytes.fromhex("01 90 3c 64") * count
        released = bytes.fromhex("01 90 3c 00") * count
        result = SMFParser.parse(framed_track(repeated + released + bytes.fromhex("00 ff 2f 00")))
        self.assertEqual(len(result.all_notes), count)
        self.assertEqual([note.start_tick for note in result.all_notes], list(range(1, count + 1)))
        self.assertEqual({note.duration_ticks for note in result.all_notes}, {count})

    def test_valid_running_status_is_preserved(self):
        result = SMFParser.parse(framed_track(bytes.fromhex("00 9f 7f 7f 01 7f 00 00 ff 2f 00")))
        self.assertEqual(
            [(n.channel, n.pitch, n.velocity, n.start_tick, n.duration_ticks) for n in result.all_notes],
            [(15, 127, 127, 0, 1)],
        )


class HypothesisMusicAudit(unittest.TestCase):
    if given is None:
        @unittest.skip("The isolated Hypothesis test dependency is unavailable.")
        def test_hypothesis_dependencies(self):
            pass
    else:
        @settings(max_examples=200, derandomize=True)
        @given(st.binary(min_size=0, max_size=12), st.integers(min_value=-1, max_value=12))
        def test_smf_vlq_decoder_against_independent_byte_model(self, payload, offset):
            candidate = payload[offset:offset + 4] if offset >= 0 else b""
            ending = next((index for index, value in enumerate(candidate) if value < 128), None)
            if ending is None:
                with self.assertRaises(ValueError):
                    decode_vlq(payload, offset)
                return
            digits = [byte % 128 for byte in candidate[:ending + 1]]
            expected = sum(digit * 128 ** exponent for exponent, digit in enumerate(reversed(digits)))
            self.assertEqual(decode_vlq(payload, offset), (expected, ending + 1))

        @settings(max_examples=200, derandomize=True)
        @given(st.integers(min_value=0, max_value=268435455))
        def test_smf_vlq_canonical_writer(self, value):
            encoded = encode_vlq(value)
            self.assertEqual(len(encoded), max(1, (value.bit_length() + 6) // 7))
            self.assertTrue(all(byte >= 128 for byte in encoded[:-1]))
            self.assertLess(encoded[-1], 128)
            self.assertEqual(sum(byte % 128 * 128 ** power for power, byte in enumerate(reversed(encoded))), value)

        @settings(max_examples=100, derandomize=True)
        @given(st.integers(0, 15), st.integers(0, 127), st.integers(1, 127),
               st.sampled_from((1, 127, 128, 16383, 16384, 2097151, 2097152, 268435455)))
        def test_structured_smf_and_truncated_track(self, channel, pitch, velocity, ticks):
            groups = (ticks.bit_length() + 6) // 7
            delta = bytes(((ticks >> shift) & 127) | (128 if shift else 0)
                          for shift in range((groups - 1) * 7, -1, -7))
            body = (bytes((0, 0x90 + channel, pitch, velocity)) + delta + bytes((pitch, 0))
                    + bytes.fromhex("00 ff 2f 00"))
            complete = framed_track(body)
            result = SMFParser.parse(complete)
            self.assertEqual([(n.channel, n.pitch, n.velocity, n.start_tick, n.duration_ticks)
                              for n in result.all_notes], [(channel, pitch, velocity, 0, ticks)])
            for damaged in (complete[:-1], framed_track(body[:4] + bytes.fromhex("81 80 80 80 00"))):
                with self.assertRaises(MidiParseError):
                    SMFParser.parse(damaged)

        @settings(max_examples=200, derandomize=True)
        @given(st.binary(max_size=48))
        def test_framed_smf_track_fuzz(self, payload):
            try:
                result = SMFParser.parse(framed_track(payload))
            except MidiParseError:
                return
            self.assertEqual(result.num_tracks, 1)
            previous = 0
            for event in result.tracks[0].events:
                self.assertEqual(event.abs_tick, previous + event.delta_ticks)
                previous = event.abs_tick
                if event.channel is not None:
                    self.assertIn(event.channel, range(16))
                    self.assertIn(event.data1, range(128))
                    if event.data2 is not None:
                        self.assertIn(event.data2, range(128))
            for note in result.all_notes:
                self.assertIn(note.pitch, range(128))
                self.assertIn(note.velocity, range(1, 128))
                self.assertGreaterEqual(note.duration_ticks, 1)

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
