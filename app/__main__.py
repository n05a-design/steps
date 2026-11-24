"""Module entrypoint for `python3 -m app` standalone execution."""

from __future__ import annotations

from app.start import main

if __name__ == "__main__":
    raise SystemExit(main())
