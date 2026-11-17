"""
Tests for the STEPS Parametric Swing-Ratio & Micro-Timing Engine (OA-0022, M07).

Verifies:
- Golden References REF-0020 (Straight 8th, rho=1.0) and REF-0021 (Triplet, rho=2.0).
- Golden References REF-0177..REF-0186 (MPC 61%, Neo-Soul 57%, Triplet, variable PPQ).
- Invariant CR-027: Binary pair second-onset delay (index 0 unchanged, index 1 delayed).
- Canonical presets (Straight, MPC 54%, 57%, 58%, 61%, 64%, Triplet).
- Friberg & Sundström (2002) tempo-dependent swing decay model.
- Milliseconds and tick conversion accuracy.
- TimelineEvent sequence transformation without jitter.
"""

from __future__ import annotations

import unittest

from src.steps.models.swing import (
    SWING_PRESETS,
    SwingEngine,
    SwingProfile,
    SwingProfileType,
    SwingSubdivision,
    calculate_swing_offset_ticks,
    calculate_swing_quant_tick,
    friberg_swing_ratio,
    milliseconds_to_ticks,
    percentage_to_swing_ratio,
    swing_ratio_to_percentage,
    ticks_to_milliseconds,
)
from src.steps.models.timeline import TimelineEvent


class TestSwingEngine(unittest.TestCase):
    def test_ref_0020_and_ref_0021_golden_ratios(self) -> None:
        """Verify fundamental swing ratios rho = 1.0 (Straight) and rho = 2.0 (Triplet)."""
        # REF-0020: Straight Swing Ratio rho = 1.0
        self.assertEqual(percentage_to_swing_ratio(50.0), 1.0)
        self.assertEqual(swing_ratio_to_percentage(1.0), 50.0)

        # REF-0021: Triplet Swing Ratio rho = 2.0 (2:1 duration ratio)
        self.assertEqual(percentage_to_swing_ratio(200.0 / 3.0), 2.0)
        self.assertAlmostEqual(swing_ratio_to_percentage(2.0), 66.6667, places=4)

    def test_ref_0177_through_ref_0186_golden_cases(self) -> None:
        """Verify mathematical precision across all Golden Reference cases REF-0177..REF-0186."""
        # REF-0177: Straight timing offset 50% at 480 PPQ -> 0 ticks
        self.assertEqual(calculate_swing_offset_ticks(480, 0.50), 0)
        self.assertEqual(calculate_swing_quant_tick(480, 0.50), 120)

        # REF-0178: MPC 61% swing ticks at 480 PPQ -> 146 ticks (ERR-034)
        self.assertEqual(calculate_swing_quant_tick(480, 0.61), 146)

        # REF-0179: MPC 61% swing offset at 480 PPQ -> +26 ticks (146 - 120)
        self.assertEqual(calculate_swing_offset_ticks(480, 0.61), 26)

        # REF-0180: MPC 61% swing delay in ms at 90 BPM & 480 PPQ -> 36.11 ms
        self.assertEqual(ticks_to_milliseconds(26, 90.0, 480), 36.11)

        # REF-0181: MPC 61% swing ticks at 960 PPQ -> 293 ticks
        self.assertEqual(calculate_swing_quant_tick(960, 0.61), 293)

        # REF-0182: MPC 61% swing offset at 960 PPQ -> +53 ticks
        self.assertEqual(calculate_swing_offset_ticks(960, 0.61), 53)

        # REF-0183: MPC 61% swing ticks at 240 PPQ -> 73 ticks
        self.assertEqual(calculate_swing_quant_tick(240, 0.61), 73)

        # REF-0184: MPC 61% swing offset at 240 PPQ -> +13 ticks
        self.assertEqual(calculate_swing_offset_ticks(240, 0.61), 13)

        # REF-0185: Neo-Soul 57% swing ticks at 480 PPQ -> 137 ticks (PAT-030)
        self.assertEqual(calculate_swing_quant_tick(480, 0.57), 137)
        self.assertEqual(calculate_swing_offset_ticks(480, 0.57), 17)

        # REF-0186: Triplet swing 66.67% ticks at 480 PPQ -> 160 ticks
        self.assertEqual(calculate_swing_quant_tick(480, 2.0 / 3.0), 160)
        self.assertEqual(calculate_swing_offset_ticks(480, 2.0 / 3.0), 40)

    def test_uk_garage_58_and_64_pct_swing(self) -> None:
        """Verify UK Garage profiles (PAT-020, PAT-026, CDR-016)."""
        # PAT-020: 58% MPC-Swing -> quant tick 139, offset +19 ticks
        self.assertEqual(calculate_swing_quant_tick(480, 0.58), 139)
        self.assertEqual(calculate_swing_offset_ticks(480, 0.58), 19)

        # PAT-026: 64% Heavy Swing -> quant tick 154, offset +34 ticks
        self.assertEqual(calculate_swing_quant_tick(480, 0.64), 154)
        self.assertEqual(calculate_swing_offset_ticks(480, 0.64), 34)

    def test_friberg_tempo_dependent_swing_decay(self) -> None:
        """Verify Friberg & Sundström (2002) tempo-dependent swing decay model (CDR-017)."""
        # Slow jazz ballad (80 BPM): High swing ratio (3.00)
        rho_80 = friberg_swing_ratio(80.0)
        self.assertEqual(rho_80, 3.00)

        # Medium swing (120 BPM): 2.50
        rho_120 = friberg_swing_ratio(120.0)
        self.assertEqual(rho_120, 2.50)

        # Up-tempo bebop (160 BPM): Triplet swing (2.00)
        rho_160 = friberg_swing_ratio(160.0)
        self.assertEqual(rho_160, 2.00)

        # Fast bebop (240+ BPM): Straightening towards 1.00
        rho_240 = friberg_swing_ratio(240.0)
        self.assertEqual(rho_240, 1.00)

        # Monotonically decreasing
        self.assertGreater(rho_80, rho_120)
        self.assertGreater(rho_120, rho_160)
        self.assertGreater(rho_160, rho_240)

    def test_swing_presets_catalogue(self) -> None:
        """Verify all canonical presets in SWING_PRESETS."""
        self.assertIn(SwingProfileType.STRAIGHT, SWING_PRESETS)
        self.assertIn(SwingProfileType.MPC_54, SWING_PRESETS)
        self.assertIn(SwingProfileType.MPC_57, SWING_PRESETS)
        self.assertIn(SwingProfileType.MPC_58, SWING_PRESETS)
        self.assertIn(SwingProfileType.MPC_61, SWING_PRESETS)
        self.assertIn(SwingProfileType.MPC_64, SWING_PRESETS)
        self.assertIn(SwingProfileType.TRIPLET, SWING_PRESETS)

        p_boom_bap = SWING_PRESETS[SwingProfileType.MPC_61]
        self.assertEqual(p_boom_bap.get_offset_ticks(480), 26)
        self.assertEqual(p_boom_bap.get_quant_tick(480), 146)
        self.assertAlmostEqual(p_boom_bap.get_delay_ms(90.0, 480), 36.11, places=2)

    def test_rule_cr_027_binary_pair_second_onset_delay(self) -> None:
        """
        Verify rule CR-027:
        'Im binären Paar (nullbasiert Index 0, 1) wird immer der zweite Onset (Index 1) verzögert.'
        Downbeats (index 0, 2, 4...) remain unchanged; offbeats (index 1, 3, 5...) are shifted.
        """
        engine = SwingEngine(
            ppq=480,
            subdivision=SwingSubdivision.SIXTEENTH,
            percentage=61.0,
        )

        grid = engine.get_grid_ticks(num_steps=8)
        # Expected grid: [0, 146, 240, 386, 480, 626, 720, 866]
        expected = [0, 146, 240, 386, 480, 626, 720, 866]
        self.assertEqual(grid, expected)

        # Even indices (downbeats): 0, 240, 480, 720 (unchanged)
        for i in range(0, 8, 2):
            self.assertEqual(grid[i], i * 120)

        # Odd indices (offbeats): delayed by exactly 26 ticks
        for i in range(1, 8, 2):
            self.assertEqual(grid[i], (i * 120) + 26)

    def test_swing_engine_events_transformation(self) -> None:
        """Verify non-destructive transformation of TimelineEvents."""
        engine = SwingEngine(
            ppq=480,
            subdivision=SwingSubdivision.SIXTEENTH,
            percentage=61.0,
        )

        events = [
            TimelineEvent("ev_0", "track_1", "NOTE", 0, 60),
            TimelineEvent("ev_1", "track_1", "NOTE", 120, 60),
            TimelineEvent("ev_2", "track_1", "NOTE", 240, 60),
            TimelineEvent("ev_3", "track_1", "NOTE", 360, 60),
        ]

        swung = engine.apply_to_events(events)
        self.assertEqual(len(swung), 4)

        # Onsets
        self.assertEqual(swung[0].start_tick, 0)
        self.assertEqual(swung[1].start_tick, 146)
        self.assertEqual(swung[2].start_tick, 240)
        self.assertEqual(swung[3].start_tick, 386)

        # Original events intact
        self.assertEqual(events[1].start_tick, 120)

    def test_milliseconds_to_ticks_conversion(self) -> None:
        """Verify bidirectional ms <-> tick conversions."""
        # 36.11 ms @ 90 BPM, 480 PPQ -> 26 ticks
        ticks = milliseconds_to_ticks(36.11, bpm=90.0, ppq=480)
        self.assertEqual(ticks, 26)

    def test_eighth_note_swing_subdivision(self) -> None:
        """Verify eighth-note swing configuration (pair span = 480 ticks)."""
        engine = SwingEngine(
            ppq=480,
            subdivision=SwingSubdivision.EIGHTH,
            swing_ratio=2.0,  # Triplet swing
        )
        self.assertEqual(engine.span_ticks, 480)
        self.assertEqual(engine.straight_step_ticks, 240)
        self.assertEqual(engine.offset_ticks, 80)
        self.assertEqual(engine.quant_tick, 320)

        grid = engine.get_grid_ticks(num_steps=4)
        # Expected: 0, 320, 480, 800
        self.assertEqual(grid, [0, 320, 480, 800])

    def test_input_validation(self) -> None:
        """Verify proper exceptions on invalid inputs."""
        with self.assertRaises(ValueError):
            calculate_swing_quant_tick(0, 0.61)

        with self.assertRaises(ValueError):
            percentage_to_swing_ratio(0.0)

        with self.assertRaises(ValueError):
            percentage_to_swing_ratio(100.0)

        with self.assertRaises(ValueError):
            swing_ratio_to_percentage(-0.5)

        with self.assertRaises(ValueError):
            friberg_swing_ratio(0.0)


if __name__ == "__main__":
    unittest.main()
