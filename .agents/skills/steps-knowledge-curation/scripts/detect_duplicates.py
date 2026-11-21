"""Find matching file hashes in a search directory and report read failures."""

from __future__ import annotations

import argparse
from hashlib import file_digest
import os
from pathlib import Path
import stat

from check_source import resolve_source


def _raise_walk_error(error: OSError) -> None:
    raise error


def is_duplicate(
    target_path: str | Path, reference_dir: str | Path, *, intake_dir: str | Path | None = None,
) -> list[str]:
    target = resolve_source(target_path, intake_dir)
    base = Path(reference_dir).resolve(strict=True)
    if not base.is_dir():
        raise NotADirectoryError(base)
    with target.open("rb") as stream:
        size = os.fstat(stream.fileno()).st_size
        target_hash = file_digest(stream, "sha256").digest()

    duplicates = set()
    for root, _, files in os.walk(base, followlinks=False, onerror=_raise_walk_error):
        for name in files:
            candidate = Path(root) / name
            try:
                path = candidate.resolve(strict=True)
            except (FileNotFoundError, RuntimeError):
                if candidate.is_symlink():
                    continue
                raise
            if path == target or not path.is_relative_to(base):
                continue
            info = path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_size != size:
                continue
            with path.open("rb") as stream:
                if file_digest(stream, "sha256").digest() == target_hash:
                    duplicates.add(str(path))
    return sorted(duplicates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_file")
    parser.add_argument("search_dir")
    parser.add_argument("--intake-dir", help="Restrict the target file to this intake directory")
    args = parser.parse_args()
    try:
        duplicates = is_duplicate(args.target_file, args.search_dir, intake_dir=args.intake_dir)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Duplicate scan incomplete: {exc}\n")
    print(f"Found {len(duplicates)} duplicate candidate(s):")
    for path in duplicates:
        print(f"  - {path}")
