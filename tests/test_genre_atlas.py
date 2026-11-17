"""
Unit tests for the STEPS Genre Harmony & Drum Atlas (OA-0023, M09).
"""

import re
import unittest
from pathlib import Path


class TestGenreAtlas(unittest.TestCase):
    """Verifies structure, completeness, and musical invariants of GENRE_HARMONY_AND_DRUM_ATLAS.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.atlas_path = Path("knowledge/concepts/styles/GENRE_HARMONY_AND_DRUM_ATLAS.md")
        cls.assertTrue(cls.atlas_path.is_file(), f"Atlas file not found at {cls.atlas_path}")
        cls.content = cls.atlas_path.read_text(encoding="utf-8")

    def test_required_genres_present(self) -> None:
        required_genres = [
            "Pop (Contemporary & Classic Pop)",
            "House (Classic & Deep House)",
            "Berlin Peak Techno",
            "Golden Era Boom-Bap Hip-Hop",
            "UK Garage 2-Step",
            "Modern Halftime Trap",
        ]
        for genre in required_genres:
            self.assertIn(genre, self.content, f"Genre '{genre}' missing from atlas")

    def test_canonical_pat_references(self) -> None:
        # Check that required PAT IDs are referenced
        required_pats = ["PAT-001", "PAT-002", "PAT-003", "PAT-004", "PAT-005", "PAT-006", "PAT-024", "PAT-025"]
        for pat in required_pats:
            self.assertIn(pat, self.content, f"Expected {pat} reference in atlas")

    def test_event_tables_have_valid_midi_parameters(self) -> None:
        # Regex to parse rows of event tables: | Takt.Zählzeit | Tick | Instrument | MIDI Pitch | Velocity | ... |
        # Example: | **1.1.1** | 0 | Acoustic Kick | 36 | 120 | Downbeat Takt 1 |
        row_pattern = re.compile(r"\|\s*([0-9\.\+\*]+)\s*\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+)\s*\|")
        matches = row_pattern.findall(self.content)

        self.assertGreater(len(matches), 40, "Expected at least 40 parsed drum events across tables")

        for beat_str, tick_str, instrument, pitch_str, vel_str, role in matches:
            tick = int(tick_str)
            pitch = int(pitch_str)
            vel = int(vel_str)

            self.assertGreaterEqual(tick, 0, f"Tick must be >= 0: {tick_str}")
            self.assertLess(tick, 3840, f"Tick must be < 3840 for 2-bar patterns: {tick_str}")
            self.assertGreaterEqual(pitch, 0, f"MIDI pitch must be in 0..127: {pitch_str}")
            self.assertLessEqual(pitch, 127, f"MIDI pitch must be in 0..127: {pitch_str}")
            self.assertGreaterEqual(vel, 1, f"Velocity must be >= 1: {vel_str}")
            self.assertLessEqual(vel, 127, f"Velocity must be <= 127: {vel_str}")

    def test_extended_profiles_2_bar_span(self) -> None:
        # Check that Techno, Boom-Bap, UK Garage, and Trap each have events in bar 2 (>= 1920 ticks)
        genre_sections = {
            "Techno": "## 3. Genre 3: Berlin Peak Techno",
            "Boom-Bap": "## 4. Genre 4: Golden Era Boom-Bap",
            "UK Garage": "## 5. Genre 5: UK Garage",
            "Trap": "## 6. Genre 6: Modern Halftime Trap",
        }

        for name, heading in genre_sections.items():
            self.assertIn(heading, self.content)
            sec_start = self.content.find(heading)
            # Find next section starting with \n## [0-9] or end
            next_match = re.search(r"\n## \d+\.", self.content[sec_start + len(heading):])
            sec_text = self.content[sec_start:sec_start + len(heading) + next_match.start()] if next_match else self.content[sec_start:]

            # Verify tick >= 1920 exists in section text using regex
            ticks_in_sec = [int(m.group(1)) for m in re.finditer(r"\|\s*(\d{4})\s*\|", sec_text)]
            has_bar_2 = any(t >= 1920 for t in ticks_in_sec)
            self.assertTrue(has_bar_2, f"Genre {name} must contain events in bar 2 (ticks >= 1920)")


if __name__ == "__main__":
    unittest.main()
