"""Packaging smoke tests for the installable STEPS Python entry point."""

import glob
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestPackageArtifacts(unittest.TestCase):
    def test_wheel_contains_locales_brand_assets_and_console_entry_point(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            wheel_dir = Path(temp_dir)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    str(ROOT),
                    "--no-deps",
                    "--no-build-isolation",
                    "--wheel-dir",
                    str(wheel_dir),
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            wheels = glob.glob(str(wheel_dir / "*.whl"))
            self.assertEqual(len(wheels), 1)

            with zipfile.ZipFile(wheels[0]) as wheel:
                names = set(wheel.namelist())
                self.assertIn("app/locales/en.json", names)
                self.assertIn("app/locales/de.json", names)
                self.assertTrue(
                    any(name.startswith("app/assets/brand/") for name in names)
                )
                entry_points = [
                    name for name in names if name.endswith(".dist-info/entry_points.txt")
                ]
                self.assertEqual(len(entry_points), 1)
                entry_point_text = wheel.read(entry_points[0]).decode("utf-8")
                self.assertIn("steps = app.main:main", entry_point_text)
