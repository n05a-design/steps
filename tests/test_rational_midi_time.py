"""
Unit tests for STEPS Rational MIDI Time Engine & Variable PPQ Conversion (OA-0029, M11).
"""

import unittest
from fractions import Fraction

from src.steps.midi.time import BarBeatPosition, RationalMidiTime


class TestRationalMidiTime(unittest.TestCase):
    """Tests the mathematical exactness of RationalMidiTime."""

    def test_bar_beat_position_basics(self) -> None:
        pos = BarBeatPosition(bar=1, beat=1, sub_beat=Fraction(0, 1))
        self.assertEqual(pos.format_daw(480), "1.1.000")

        pos2 = BarBeatPosition(bar=2, beat=3, sub_beat=Fraction(1, 2))
        self.assertEqual(pos2.format_daw(480), "2.3.240")

        # Validation errors
        with self.assertRaises(ValueError):
            BarBeatPosition(bar=0, beat=1)
        with self.assertRaises(ValueError):
            BarBeatPosition(bar=1, beat=0)
        with self.assertRaises(ValueError):
            BarBeatPosition(bar=1, beat=1, sub_beat=Fraction(1, 1))
        with self.assertRaises(ValueError):
            BarBeatPosition(bar=1, beat=1, sub_beat=Fraction(-1, 2))

    def test_ticks_per_beat_and_bar(self) -> None:
        # Standard 4/4 at 480 PPQ
        self.assertEqual(RationalMidiTime.ticks_per_beat(480, 4), 480)
        self.assertEqual(RationalMidiTime.ticks_per_bar(480, 4, 4), 1920)

        # 3/4 at 480 PPQ
        self.assertEqual(RationalMidiTime.ticks_per_bar(480, 3, 4), 1440)

        # 6/8 at 480 PPQ (beat is eighth note = 240 ticks)
        self.assertEqual(RationalMidiTime.ticks_per_beat(480, 8), 240)
        self.assertEqual(RationalMidiTime.ticks_per_bar(480, 6, 8), 1440)

        # Invalid denominator
        with self.assertRaises(ValueError):
            RationalMidiTime.ticks_per_beat(480, 3)

    def test_ticks_to_position_roundtrip(self) -> None:
        ppq = 480
        test_ticks = [0, 1, 240, 480, 960, 1919, 1920, 3840, 7680 + 360]

        for tick in test_ticks:
            pos = RationalMidiTime.ticks_to_position(tick, ppq=ppq, numerator=4, denominator=4)
            recalculated = RationalMidiTime.position_to_ticks(pos, ppq=ppq, numerator=4, denominator=4)
            self.assertEqual(tick, recalculated, f"Roundtrip failed for tick {tick}")

    def test_large_absolute_ticks_roundtrip_without_losing_a_tick(self) -> None:
        for tick in (2**53 + 1, 2**56 + 3):
            with self.subTest(tick=tick):
                settings = {"ppq": 960, "numerator": 7, "denominator": 8}
                position = RationalMidiTime.ticks_to_bar_beat_tick(tick, **settings)
                self.assertEqual(RationalMidiTime.bar_beat_tick_to_ticks(*position, **settings), tick)

    def test_fractional_tick_midpoints_keep_half_even_rounding(self) -> None:
        for half_tick, expected in ((1, 0), (3, 2), (5, 2)):
            with self.subTest(half_tick=half_tick):
                position = BarBeatPosition(1, 1, Fraction(half_tick, 960))
                self.assertEqual(position.format_daw(480), f"1.1.{expected:03d}")
                self.assertEqual(RationalMidiTime.position_to_ticks(position, ppq=480), expected)

    def test_ticks_to_position_non_4_4(self) -> None:
        # 3/4 time signature: bar = 1440 ticks
        pos = RationalMidiTime.ticks_to_position(1440, ppq=480, numerator=3, denominator=4)
        self.assertEqual(pos.bar, 2)
        self.assertEqual(pos.beat, 1)
        self.assertEqual(pos.sub_beat, Fraction(0, 1))

    def test_bar_beat_tick_roundtrip_uses_denominator_beats(self) -> None:
        cases = (
            (0, (1, 1, 0), 4, 4),
            (2100, (2, 1, 180), 4, 4),
            (1440, (2, 1, 0), 6, 8),
            (1320, (1, 6, 120), 6, 8),
        )
        for absolute_tick, position, numerator, denominator in cases:
            with self.subTest(meter=(numerator, denominator), tick=absolute_tick):
                self.assertEqual(
                    RationalMidiTime.ticks_to_bar_beat_tick(
                        absolute_tick, ppq=480, numerator=numerator, denominator=denominator
                    ),
                    position,
                )
                self.assertEqual(
                    RationalMidiTime.bar_beat_tick_to_ticks(
                        *position, ppq=480, numerator=numerator, denominator=denominator
                    ),
                    absolute_tick,
                )

    def test_bar_beat_tick_rejects_out_of_meter_coordinates(self) -> None:
        for position in ((0, 1, 0), (1, 0, 0), (1, 5, 0), (1, 1, 480), (1, 1, -1)):
            with self.subTest(position=position):
                with self.assertRaises(ValueError):
                    RationalMidiTime.bar_beat_tick_to_ticks(
                        *position, ppq=480, numerator=4, denominator=4
                    )

    def test_convert_ppq_lossless_roundtrip(self) -> None:
        # 960 <-> 480
        self.assertEqual(RationalMidiTime.convert_ppq(960, 960, 480), 480)
        self.assertEqual(RationalMidiTime.convert_ppq(480, 480, 960), 960)

        # 384 <-> 480 (384 * 480 / 384 = 480)
        self.assertEqual(RationalMidiTime.convert_ppq(384, 384, 480), 480)
        self.assertEqual(RationalMidiTime.convert_ppq(480, 480, 384), 384)

        # Arbitrary tick rounding check
        self.assertEqual(RationalMidiTime.convert_ppq(120, 480, 960), 240)
        self.assertEqual(RationalMidiTime.convert_ppq(100, 480, 480), 100)

        with self.assertRaises(ValueError):
            RationalMidiTime.convert_ppq(-1, 480, 960)
        with self.assertRaises(ValueError):
            RationalMidiTime.convert_ppq(100, 0, 960)

    def test_distribute_tuplet_ticks_zero_drift(self) -> None:
        # Standard triplet in one quarter note (480 ticks) -> 3 divisions of 160
        divisions_3 = RationalMidiTime.distribute_tuplet_ticks(480, 3)
        self.assertEqual(len(divisions_3), 3)
        self.assertEqual(divisions_3, [(0, 160), (160, 160), (320, 160)])
        self.assertEqual(sum(d for _, d in divisions_3), 480)

        # Quintuplet in 480 ticks -> 5 divisions of 96
        divisions_5 = RationalMidiTime.distribute_tuplet_ticks(480, 5)
        self.assertEqual(len(divisions_5), 5)
        self.assertEqual(sum(d for _, d in divisions_5), 480)

        # Septuplet in 480 ticks -> fractional steps: 480 / 7 ≈ 68.57 ticks
        # Must sum exactly to 480 with zero drift!
        divisions_7 = RationalMidiTime.distribute_tuplet_ticks(480, 7)
        self.assertEqual(len(divisions_7), 7)
        self.assertEqual(sum(d for _, d in divisions_7), 480)
        # Check continuity of boundaries
        for i in range(len(divisions_7) - 1):
            cur_start, cur_dur = divisions_7[i]
            next_start, _ = divisions_7[i + 1]
            self.assertEqual(cur_start + cur_dur, next_start)

        # 11-tuplet in 1920 ticks (1 bar)
        divisions_11 = RationalMidiTime.distribute_tuplet_ticks(1920, 11)
        self.assertEqual(sum(d for _, d in divisions_11), 1920)

    def test_ticks_to_seconds(self) -> None:
        # At 120 BPM, 1 beat (quarter note = 480 ticks) is 0.5 seconds
        # 1 bar = 1920 ticks = 2.0 seconds
        sec = RationalMidiTime.ticks_to_seconds(1920, ppq=480, tempo_points=[(0, 120.0)])
        self.assertAlmostEqual(sec, 2.0, places=5)

        # At 60 BPM, 1 beat (480 ticks) is 1.0 second
        sec_60 = RationalMidiTime.ticks_to_seconds(480, ppq=480, tempo_points=[(0, 60.0)])
        self.assertAlmostEqual(sec_60, 1.0, places=5)

        # Variable tempo map:
        # Bar 1 (0..1920 ticks) at 120 BPM -> 2.0 s
        # Bar 2 (1920..3840 ticks) at 60 BPM -> 4.0 s
        # Total for 3840 ticks = 6.0 s
        tempo_map = [(0, 120.0), (1920, 60.0)]
        sec_var = RationalMidiTime.ticks_to_seconds(3840, ppq=480, tempo_points=tempo_map)
        self.assertAlmostEqual(sec_var, 6.0, places=5)

        # Mid-bar query (e.g. 2880 ticks = 1920 at 120 BPM (2s) + 960 at 60 BPM (2s) = 4.0s)
        sec_mid = RationalMidiTime.ticks_to_seconds(2880, ppq=480, tempo_points=tempo_map)
        self.assertAlmostEqual(sec_mid, 4.0, places=5)


if __name__ == "__main__":
    unittest.main()
