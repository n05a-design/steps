"""Compare registered file identities with raw blobs in an explicit Git tree.

This read-only check establishes byte identity, not provenance or usage rights.
It also accepts local checkpoint trees that are not commits on a public branch.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def git(repository, *arguments):
    return subprocess.check_output(["git", "-C", str(repository), *arguments], stderr=subprocess.PIPE)


def verify(repository, tree, records):
    """Resolve a tree once and hash the exact blob bytes without checkout filters."""
    revision = git(repository, "rev-parse", "--verify", "--end-of-options", f"{tree}^{{tree}}").decode().strip()
    entries = {}
    for entry in git(repository, "ls-tree", "-rz", revision).split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            _, kind, oid = metadata.split()
            if kind == b"blob":
                entries[path.decode("utf-8")] = oid.decode("ascii")
    results, cache, seen = [], {}, set()
    for row in records:
        ident, path = row["file_id"], row["path"]
        if ident in seen:
            raise ValueError(f"Duplicate registry ID: {ident}")
        seen.add(ident)
        expected_hash = row["sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", expected_hash) or int(row["size_bytes"]) <= 0:
            raise ValueError(f"No concrete size and SHA-256 for {ident}")
        result = {"file_id": ident, "path": path, "expected_size": int(row["size_bytes"]),
                  "expected_sha256": expected_hash, "status": "MISSING"}
        if path in entries:
            oid = entries[path]
            if oid not in cache:
                content = git(repository, "cat-file", "blob", oid)
                cache[oid] = (len(content), sha256(content).hexdigest())
            size, digest = cache[oid]
            result.update(blob=oid, observed_size=size, observed_sha256=digest,
                          status="MATCH" if (size, digest) == (int(row["size_bytes"]), expected_hash) else "MISMATCH")
        results.append(result)
    return {"schema_version": 1, "tree": revision, "scope": "byte identity only; provenance and rights unreviewed",
            "counts": dict(Counter(row["status"] for row in results)), "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=ROOT)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--registry", type=Path, default=ROOT / "knowledge/sources/MUSIC_SOURCE_REVIEW_PROGRESS.csv")
    parser.add_argument("--ids", nargs="+", required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    try:
        with args.registry.open(encoding="utf-8-sig", newline="") as source:
            rows = [row for row in csv.DictReader(source) if row["file_id"] in args.ids]
        missing = set(args.ids) - {row["file_id"] for row in rows}
        if missing:
            raise ValueError(f"Unknown registry IDs: {sorted(missing)}")
        report = verify(args.repository, args.tree, rows)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"BLOCKED: registry or Git tree unavailable/invalid: {exc}\n")
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        args.json_out.write_text(content, encoding="utf-8")
    print(content, end="")
    return int(any(row["status"] != "MATCH" for row in report["results"]))


if __name__ == "__main__":
    raise SystemExit(main())
