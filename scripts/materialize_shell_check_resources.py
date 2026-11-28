"""Prepare exact-byte or CRLF Shell fixtures in an isolated CI checkout."""

import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SHELL = "glide_shell"


def git_blob(path: str, *, crlf: bool = False) -> bytes:
    if crlf:
        args = ("-c", "core.autocrlf=true", "-c", "core.eol=crlf", "cat-file", "--filters")
    else:
        args = ("cat-file", "blob")
    return subprocess.check_output(("git", *args, f"HEAD:{path}"), cwd=ROOT)


def materialize(mode: str) -> int:
    manifest = json.loads(git_blob(f"{SHELL}/SHELL_MANIFEST.json"))
    pending = []
    for name, expected in manifest["dateien"].items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            raise ValueError(f"Invalid manifest path: {name}")
        path = f"{SHELL}/{relative}"
        target = ROOT / path
        expected_target = ROOT / SHELL / relative
        if target.resolve() != expected_target:
            raise ValueError(f"Refusing to replace a redirected resource: {name}")
        original = git_blob(path)
        if sha256(original).hexdigest() != expected:
            raise ValueError(f"Tracked resource differs from its manifest: {name}")
        filtered = git_blob(path, crlf=True)
        if filtered != original.replace(b"\n", b"\r\n"):
            raise ValueError(f"CRLF filter did not produce the expected test bytes: {name}")
        current = target.read_bytes()
        if current not in (original, filtered):
            raise ValueError(f"Refusing to replace a modified resource: {name}")
        pending.append((target, original if mode == "exact" else filtered))
    for target, content in pending:
        target.write_bytes(content)
    return len(pending)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("exact", "crlf"))
    options = parser.parse_args()
    print(f"Prepared {materialize(options.mode)} manifest resources ({options.mode}).")


if __name__ == "__main__":
    main()
