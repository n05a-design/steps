"""Source check and hashing utility."""
from __future__ import annotations
import sys, os, hashlib

def check_file(path: str) -> dict[str, str | int]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    with open(path, "rb") as f:
        b = f.read()
    sha = hashlib.sha256(b).hexdigest()
    return {
        "path": os.path.normpath(path),
        "size_bytes": len(b),
        "sha256": sha,
        "extension": os.path.splitext(path)[1].lower()
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_source.py <file_path>")
        sys.exit(1)
    res = check_file(sys.argv[1])
    for k, v in res.items():
        print(f"{k}: {v}")
