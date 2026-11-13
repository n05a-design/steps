#!/usr/bin/env python3
"""Synchronize the test fixture from the versioned Golden Case master."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from stat import S_IMODE
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("knowledge/research")
FIXTURE = Path("golden_cases/golden_reference_cases.json")


def synchronize(root: Path, *, check: bool = False) -> int:
    master = root / RESEARCH / FIXTURE
    mirror = root / "tests" / FIXTURE
    payload = master.read_bytes()
    cases = json.loads(payload)
    if not isinstance(cases, list) or not all(isinstance(case, dict) for case in cases):
        raise ValueError("Der Golden-Master muss eine Liste von Fallobjekten sein.")

    baseline = json.loads((root / RESEARCH / "REFERENCE_IDENTITY_BASELINE.json").read_bytes())
    ids = [case.get("case_id") for case in cases]
    sequential_ids = [f"REF-{i:04d}" for i in range(1, len(ids) + 1)]
    if ids != sequential_ids or not baseline["reference_cases"].keys() <= set(ids):
        raise ValueError("Golden-Master enthält fehlende, doppelte oder falsch sortierte Fall-IDs.")

    if mirror.is_file() and mirror.read_bytes() == payload:
        return len(cases)
    if check:
        raise ValueError("Testspiegel fehlt oder weicht vom Golden-Master ab.")

    stream = NamedTemporaryFile(dir=mirror.parent, delete=False)
    pending = Path(stream.name)
    try:
        with stream:
            stream.write(payload)
        pending.chmod(S_IMODE(master.stat().st_mode))
        pending.replace(mirror)
    finally:
        pending.unlink(missing_ok=True)
    return len(cases)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Abweichungen melden, ohne zu schreiben.")
    args = parser.parse_args()
    try:
        count = synchronize(ROOT, check=args.check)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{count} Golden Cases. Master und Testspiegel sind bytegleich.")


if __name__ == "__main__":
    main()
