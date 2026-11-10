"""Duplicate detection utility based on SHA-256."""
from __future__ import annotations
import sys, os, hashlib

def is_duplicate(target_path: str, reference_dir: str) -> list[str]:
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target not found: {target_path}")
    with open(target_path, "rb") as f:
        target_hash = hashlib.sha256(f.read()).hexdigest()
    duplicates = []
    
    for root, _, files in os.walk(reference_dir):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.abspath(fp) == os.path.abspath(target_path):
                continue
            try:
                with open(fp, "rb") as fl:
                    h = hashlib.sha256(fl.read()).hexdigest()
                if h == target_hash:
                    duplicates.append(os.path.normpath(fp))
            except (OSError, PermissionError):
                continue
    return duplicates

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python detect_duplicates.py <target_file> <search_dir>")
        sys.exit(1)
    dups = is_duplicate(sys.argv[1], sys.argv[2])
    print(f"Found {len(dups)} duplicate(s):")
    for d in dups:
        print(f"  - {d}")
