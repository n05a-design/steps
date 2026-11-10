"""Source check and hashing utility with security and symlink boundary verification."""
from __future__ import annotations
import sys, os, hashlib
from pathlib import Path

def check_file(path: str, base_dir: str | None = None) -> dict[str, str | int | bool]:
    """Verify file existence, compute SHA-256, resolve symlinks, and enforce boundaries."""
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not target.is_file():
        raise ValueError(f"Path is not a regular file: {path}")
        
    resolved_path = target.resolve()
    is_symlink = target.is_symlink()
    
    # Boundary check if base_dir is supplied
    is_within_bounds = True
    if base_dir:
        base = Path(base_dir).resolve()
        try:
            resolved_path.relative_to(base)
        except ValueError:
            is_within_bounds = False
            
    with open(resolved_path, "rb") as f:
        b = f.read()
    sha = hashlib.sha256(b).hexdigest()
    
    return {
        "path": str(resolved_path),
        "size_bytes": len(b),
        "sha256": sha,
        "extension": resolved_path.suffix.lower(),
        "is_symlink": is_symlink,
        "within_bounds": is_within_bounds
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_source.py filepath [base_dir]")
        sys.exit(1)
    base = sys.argv[2] if len(sys.argv) > 2 else None
    res = check_file(sys.argv[1], base)
    for k, v in res.items():
        print(f"{k}: {v}")
