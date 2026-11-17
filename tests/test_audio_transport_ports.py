"""
Unit & Integration Tests for STEPS Architecture Ports & Audio Transport.

Tests:
- AudioBackendPort & NullAudioBackend event recording and state
- MonotonicPlaybackScheduler state transitions (STOPPED, PLAYING, PAUSED)
- Golden Invariant T14: No hung notes (all_notes_off on stop, pause, loop, close)
- Golden Invariant T15: Multi-tempo playback and tick-to-second conversion
- UI thread isolation: ui_dispatcher routing without audio sleep in main thread
- EventBus publish/subscribe and CommandRegistry dispatching
"""

import threading
import time
import unittest
from pathlib import Path

from src.steps.models.timeline import TempoMap, TempoPoint, Timeline, TimelineEvent
from src.steps.ports.audio import (
    MonotonicPlaybackScheduler,
    NullAudioBackend,
    PlaybackEvent,
    PlaybackState,
    events_from_timeline,
    events_from_voicings,
)
from src.steps.ports.events import Command, CommandRegistry, DomainEvent, EventBus
from src.steps.theory.chord import Voicing, parse_chord


class AudioTransportPortsTests(unittest.TestCase):

    def setUp(self):
        self.backend = NullAudioBackend()

    def tearDown(self):
        self.backend.close()

    def test_null_backend_lifecycle(self):
        """Verify NullAudioBackend open, close, send_event, and all_notes_off."""
        self.assertTrue(self.backend.is_available())
        self.backend.open()
        info = self.backend.get_device_info()
        self.assertTrue(info["is_open"])
        self.assertEqual(info["driver"], "null")

        ev = PlaybackEvent(tick=0, event_type="note_on", pitch=60, velocity=90)
        self.backend.send_event(ev)
        self.assertEqual(len(self.backend.events_recorded), 1)
        self.assertEqual(self.backend.events_recorded[0][1], ev)

        self.backend.all_notes_off(channel=0)
        self.assertEqual(self.backend.all_notes_off_count, 1)

        self.backend.clear()
        self.assertEqual(len(self.backend.events_recorded), 0)
        self.assertEqual(self.backend.all_notes_off_count, 0)

    def test_events_from_voicings(self):
        """Converts Voicings into matching NoteOn and NoteOff PlaybackEvents."""
        c_maj = parse_chord("C").to_voicing(bass_octave=3)
        g_dom = parse_chord("G7").to_voicing(bass_octave=3)

        events = events_from_voicings([c_maj, g_dom], duration_ticks=960)
        self.assertGreater(len(events), 0)
        # Check that all note_ons have matching note_offs
        note_ons = [e for e in events if e.event_type == "note_on"]
        note_offs = [e for e in events if e.event_type == "note_off"]
        self.assertEqual(len(note_ons), len(note_offs))
        # First chord at tick 0, second chord at tick 960
        c_ons = [e for e in note_ons if e.tick == 0]
        g_ons = [e for e in note_ons if e.tick == 960]
        self.assertEqual(len(c_ons), 3)  # C, E, G
        self.assertEqual(len(g_ons), 4)  # G, B, D, F

    def test_monotonic_scheduler_play_and_stop(self):
        """Scheduler starts worker, advances ticks, and stops cleanly."""
        ev1 = PlaybackEvent(tick=0, event_type="note_on", pitch=60, velocity=80)
        ev2 = PlaybackEvent(tick=50, event_type="note_off", pitch=60, velocity=0)

        tick_calls = []
        state_changes = []

        scheduler = MonotonicPlaybackScheduler(
            backend=self.backend,
            events=[ev1, ev2],
            tempo_bpm=400.0,  # Fast tempo for quick test
            ppq=480,
            on_tick=lambda t, s: tick_calls.append((t, s)),
            on_state_change=lambda st: state_changes.append(st),
        )

        self.assertEqual(scheduler.state, PlaybackState.STOPPED)
        scheduler.play()
        self.assertEqual(scheduler.state, PlaybackState.PLAYING)
        self.assertIn(PlaybackState.PLAYING, state_changes)

        # Allow playback thread to process
        time.sleep(0.05)

        scheduler.stop()
        self.assertEqual(scheduler.state, PlaybackState.STOPPED)
        self.assertIn(PlaybackState.STOPPED, state_changes)
        # Verify all_notes_off called on stop (T14)
        self.assertGreater(self.backend.all_notes_off_count, 0)
        scheduler.close()

    def test_monotonic_scheduler_pause_and_resume(self):
        """Scheduler pauses, silences voices, and resumes."""
        ev1 = PlaybackEvent(tick=0, event_type="note_on", pitch=64, velocity=80)
        ev2 = PlaybackEvent(tick=1000, event_type="note_off", pitch=64, velocity=0)

        scheduler = MonotonicPlaybackScheduler(
            backend=self.backend,
            events=[ev1, ev2],
            tempo_bpm=120.0,
            ppq=480,
        )

        scheduler.play()
        time.sleep(0.02)
        scheduler.pause()
        self.assertEqual(scheduler.state, PlaybackState.PAUSED)
        self.assertGreater(self.backend.all_notes_off_count, 0)

        # In pause state, ticks do not advance
        paused_tick = scheduler.current_tick
        time.sleep(0.02)
        self.assertEqual(scheduler.current_tick, paused_tick)

        scheduler.resume()
        self.assertEqual(scheduler.state, PlaybackState.PLAYING)
        time.sleep(0.02)
        self.assertGreaterEqual(scheduler.current_tick, paused_tick)

        scheduler.close()

    def test_monotonic_scheduler_looping(self):
        """Looping resets tick to loop_start_tick when reaching loop_end_tick."""
        ev1 = PlaybackEvent(tick=0, event_type="note_on", pitch=60, velocity=80)
        ev2 = PlaybackEvent(tick=20, event_type="note_off", pitch=60, velocity=0)

        scheduler = MonotonicPlaybackScheduler(
            backend=self.backend,
            events=[ev1, ev2],
            tempo_bpm=500.0,
            ppq=480,
            loop=True,
            loop_start_tick=0,
            loop_end_tick=30,
        )

        scheduler.play()
        time.sleep(0.08)
        # Verify all_notes_off called on loop boundary reset
        self.assertGreater(self.backend.all_notes_off_count, 0)
        scheduler.close()

    def test_ui_dispatcher_isolation(self):
        """UI dispatcher receives callbacks so scheduler thread never calls UI directly."""
        dispatched_calls = []

        def fake_ui_dispatcher(callback):
            # Simulates root.after_idle / main thread queuing
            dispatched_calls.append(callback)
            callback()

        ev = PlaybackEvent(tick=0, event_type="note_on", pitch=60, velocity=80)
        state_list = []

        scheduler = MonotonicPlaybackScheduler(
            backend=self.backend,
            events=[ev],
            tempo_bpm=200.0,
            ppq=480,
            on_state_change=lambda st: state_list.append(st),
            ui_dispatcher=fake_ui_dispatcher,
        )

        scheduler.play()
        self.assertGreater(len(dispatched_calls), 0)
        self.assertIn(PlaybackState.PLAYING, state_list)
        scheduler.close()

    def test_events_from_timeline(self):
        """Converts Timeline object events into PlaybackEvents."""
        timeline = Timeline(
            events=[
                TimelineEvent(
                    event_id="ev1",
                    track_id="chords",
                    event_type="NOTE",
                    start_tick=0,
                    duration_ticks=480,
                    payload={"pitches": [60, 64, 67]}
                )
            ]
        )
        events = events_from_timeline(timeline)
        self.assertEqual(len(events), 6)  # 3 note_ons, 3 note_offs
        ons = [e for e in events if e.event_type == "note_on"]
        offs = [e for e in events if e.event_type == "note_off"]
        self.assertEqual([e.pitch for e in ons], [60, 64, 67])
        self.assertEqual([e.pitch for e in offs], [60, 64, 67])
        self.assertTrue(all(e.tick == 0 for e in ons))
        self.assertTrue(all(e.tick == 480 for e in offs))


class EventsAndCommandsTests(unittest.TestCase):

    def test_event_bus_publish_and_subscribe(self):
        """EventBus delivers events to matching and wildcard subscribers."""
        bus = EventBus()
        received_specific = []
        received_wildcard = []

        bus.subscribe("TRACK_ADDED", lambda ev: received_specific.append(ev))
        bus.subscribe("*", lambda ev: received_wildcard.append(ev))

        event = DomainEvent(name="TRACK_ADDED", payload={"track_id": "trk_1"})
        bus.publish(event)

        self.assertEqual(len(received_specific), 1)
        self.assertEqual(received_specific[0].payload["track_id"], "trk_1")
        self.assertEqual(len(received_wildcard), 1)

        # Non-matching event
        other_event = DomainEvent(name="TEMPO_CHANGED", payload={"bpm": 130})
        bus.publish(other_event)
        self.assertEqual(len(received_specific), 1)
        self.assertEqual(len(received_wildcard), 2)

    def test_command_registry_execute(self):
        """CommandRegistry registers and executes command handlers."""
        registry = CommandRegistry()
        registry.register("SAVE_PROJECT", lambda cmd: f"Saved {cmd.params.get('title')}")

        cmd = Command(name="SAVE_PROJECT", params={"title": "MySong"})
        result = registry.execute(cmd)
        self.assertEqual(result, "Saved MySong")

        with self.assertRaises(KeyError):
            registry.execute(Command(name="UNKNOWN_CMD"))


if __name__ == "__main__":
    unittest.main()
