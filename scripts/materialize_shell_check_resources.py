"""Verify the tracked and checked-out byte contract of Shell resources."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SHELL = "glide_shell"


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", *args), cwd=ROOT)


def check_resources() -> int:
    manifest = json.loads((ROOT / SHELL / "SHELL_MANIFEST.json").read_bytes())
    for name, expected in manifest["dateien"].items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or chr(92) in name:
            raise ValueError(f"Invalid manifest path: {name}")
        path = f"{SHELL}/{relative}"
        original = git("cat-file", "blob", f"HEAD:{path}")
        if hashlib.sha256(original).hexdigest() != expected:
            raise ValueError(f"Tracked resource differs from its manifest: {name}")
        attributes = git("check-attr", "-z", "text", "eol", "--", path).split(b"\0")
        text, eol = attributes[2], attributes[5]
        if text != b"unset" and (text != b"set" or eol != b"lf" or b"\r" in original or b"\0" in original):
            raise ValueError(f"Manifest resource needs an explicit byte-preserving Git policy: {name}")
        if (ROOT / path).read_bytes() != original:
            raise ValueError(f"Checkout bytes differ from the tracked resource: {name}")
    return len(manifest["dateien"])


if __name__ == "__main__":
    print(f"Verified {check_resources()} shell manifest resources.")
