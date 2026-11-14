"""Find byte-identical files inside a resolved search directory."""

from __future__ import annotations

from hashlib import file_digest
import os
from pathlib import Path
import sys

from check_source import resolve_source


def is_duplicate(target_path: str | Path, reference_dir: str | Path) -> list[str]:
    target = resolve_source(target_path)
    base = Path(reference_dir).resolve(strict=True)
    if not base.is_dir():
        raise NotADirectoryError(base)
    size = target.stat().st_size
    with target.open("rb") as stream:
        target_hash = file_digest(stream, "sha256").digest()

    duplicates = set()
    for root, dirs, files in os.walk(base, followlinks=False):
        for name in dirs[:]:
            candidate = Path(root) / name
            try:
                if candidate.resolve() == candidate:
                    continue
            except (OSError, RuntimeError):
                pass
            dirs.remove(name)
        for name in files:
            candidate = Path(root) / name
            try:
                path = resolve_source(candidate, base)
                if path == target or path.stat().st_size != size:
                    continue
                with path.open("rb") as stream:
                    if file_digest(stream, "sha256").digest() == target_hash:
                        duplicates.add(str(path))
            except (OSError, ValueError, RuntimeError):
                continue
    return sorted(duplicates)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python detect_duplicates.py target_file search_dir")
    try:
        duplicates = is_duplicate(*sys.argv[1:])
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))
    print(f"Found {len(duplicates)} duplicate(s):")
    for path in duplicates:
        print(f"  - {path}")
