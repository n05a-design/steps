"""Tests for active UI text localization inventory."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUiTextInventory(unittest.TestCase):
    def test_active_ui_text_has_no_uncataloged_literal_widget_text(self):
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "scripts/check_ui_text_inventory.py",
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("UI TEXT INVENTORY PASS", result.stdout)
