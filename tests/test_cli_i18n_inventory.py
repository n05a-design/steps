"""Tests for the CLI localization inventory gate."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestCliI18nInventory(unittest.TestCase):
    def test_cli_user_text_routes_through_catalog(self):
        result = subprocess.run(
            [sys.executable, "-B", "scripts/check_cli_text_inventory.py", "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLI TEXT INVENTORY PASS", result.stdout)
