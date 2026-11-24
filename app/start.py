"""Standalone desktop launcher for STEPS outside DAW software.

Redirects Python bytecode into the OS user cache directory, checks the
minimum Python version before importing the application, ensures the
repository root is importable regardless of working directory, and starts
`app.main.main`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

MIN_PYTHON_VERSION: tuple[int, int] = (3, 11)


def bytecode_cache_dir() -> Path:
    """Return the per-user bytecode cache folder outside the repository."""
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches" / "STEPS"
    elif os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = (Path(local_app_data) if local_app_data else Path.home()) / "STEPS" / "Cache"
    else:
        xdg_cache = os.environ.get("XDG_CACHE_HOME")
        base = (Path(xdg_cache) if xdg_cache else Path.home() / ".cache") / "steps"
    return base / "bytecode"


def ensure_repo_on_path() -> Path:
    """Ensure the STEPS repository root is on sys.path for cwd-independent launches."""
    root = Path(__file__).resolve().parents[1]
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def check_python_version(min_version: tuple[int, int] = MIN_PYTHON_VERSION) -> None:
    """Fail fast with a readable message when launched on an unsupported interpreter."""
    if sys.version_info < min_version:
        required = ".".join(str(part) for part in min_version)
        current = ".".join(str(part) for part in sys.version_info[:3])
        raise SystemExit(f"STEPS requires Python {required} or newer (found {current}).")


def main(argv: Optional[list[str]] = None) -> int:
    """Preflight and launch the STEPS desktop application cleanly."""
    if not getattr(sys, "pycache_prefix", None):
        sys.pycache_prefix = str(bytecode_cache_dir())
    ensure_repo_on_path()
    check_python_version()
    from app.main import main as run_app

    return run_app(argv)


if __name__ == "__main__":
    raise SystemExit(main())
