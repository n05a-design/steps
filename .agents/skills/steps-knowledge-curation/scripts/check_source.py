"""Identify and hash a source within an optional resolved directory boundary."""

from __future__ import annotations

import argparse
from hashlib import file_digest
import os
from pathlib import Path


def resolve_source(path: str | Path, base_dir: str | Path | None = None) -> Path:
    try:
        target = Path(path).resolve()
    except RuntimeError as exc:
        raise ValueError(f"Cannot resolve source path: {path}") from exc
    if base_dir is not None:
        base = Path(base_dir).resolve(strict=True)
        if not base.is_dir():
            raise NotADirectoryError(base)
        if not target.is_relative_to(base):
            raise ValueError(f"Source resolves outside the allowed directory: {path}")
    if not target.exists():
        raise FileNotFoundError(target)
    if not target.is_file():
        raise ValueError(f"Path is not a regular file: {path}")
    return target


def check_file(path: str | Path, base_dir: str | Path | None = None) -> dict[str, str | int | bool]:
    target = resolve_source(path, base_dir)
    with target.open("rb") as stream:
        size = os.fstat(stream.fileno()).st_size
        digest = file_digest(stream, "sha256").hexdigest()
    return {
        "path": str(target),
        "size_bytes": size,
        "sha256": digest,
        "extension": target.suffix.lower(),
        "is_symlink": Path(path).is_symlink(),
        "within_bounds": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("base_dir", nargs="?")
    args = parser.parse_args()
    try:
        for key, value in check_file(args.file, args.base_dir).items():
            print(f"{key}: {value}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
