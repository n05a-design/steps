"""Duplicate detection utility based on SHA-256 with symlink safety and non-destructive traversal."""
from __future__ import annotations
import sys, os, hashlib
from pathlib import Path

def is_duplicate(target_path: str, reference_dir: str) -> list[str]:
    """Find files in reference_dir with identical SHA-256 hash, ignoring the target file itself."""
    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Target not found: {target_path}")
    if not target.is_file():
        raise ValueError(f"Target is not a regular file: {target_path}")
        
    target_resolved = target.resolve()
    with open(target_resolved, "rb") as f:
        target_hash = hashlib.sha256(f.read()).hexdigest()
        
    duplicates = []
    ref_base = Path(reference_dir).resolve()
    if not ref_base.exists() or not ref_base.is_dir():
        raise NotADirectoryError(f"Reference directory not found: {reference_dir}")
        
    for root, _, files in os.walk(ref_base, followlinks=False):
        for f in files:
            fp = Path(root) / f
            try:
                # Skip target file itself
                if fp.resolve() == target_resolved:
                    continue
                with open(fp, "rb") as fl:
                    h = hashlib.sha256(fl.read()).hexdigest()
                if h == target_hash:
                    duplicates.append(str(fp.resolve()))
            except (OSError, PermissionError):
                continue
    return sorted(duplicates)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python detect_duplicates.py target_file search_dir")
        sys.exit(1)
    dups = is_duplicate(sys.argv[1], sys.argv[2])
    print(f"Found {len(dups)} duplicate(s):")
    for d in dups:
        print(f"  - {d}")
