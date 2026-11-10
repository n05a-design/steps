"""Entry-level repository hygiene regression test."""
from pathlib import Path
import subprocess
import sys
import unittest

class StructureTestCase(unittest.TestCase):
    def test_structure_script(self):
        root = Path(__file__).resolve().parents[1]
        cp = subprocess.run(
            [sys.executable, str(root / "tools/validation/check_structure.py")],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + "\n" + cp.stderr)

if __name__ == "__main__":
    unittest.main()

