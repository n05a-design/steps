"""Entry-level repository hygiene regression test."""
from pathlib import Path
import subprocess
import sys

def test_structure_script():
    root=Path(__file__).resolve().parents[1]
    cp=subprocess.run([sys.executable, str(root/'tools/validation/check_structure.py')],
                      cwd=root, capture_output=True, text=True, check=False)
    assert cp.returncode==0, cp.stdout+'\n'+cp.stderr
