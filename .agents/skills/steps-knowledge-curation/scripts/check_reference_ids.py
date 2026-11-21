"""Check STEPS reference identities and their reviewed graph bindings."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

from register_paths import REPOSITORY_ROOT

# Load the verifier from this checkout, even when checking a separate data directory.
sys.path.insert(0, str(REPOSITORY_ROOT))
from scripts.verify_reference_integrity import verify_csv_schema, verify_integrity


@dataclass
class ReferenceCheckReport:
    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    identities_checked: int = 0
    stats: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return vars(self).copy()


def _check_graph_bindings(repo_root: Path) -> list[str]:
    directory = repo_root / "knowledge" / "relations"
    identity_fields = ["source_id", "target_id", "relation_type"]
    review_fields = ["original_row_sha256", *identity_fields, "human_review", "production_use_allowed"]
    tables = {}
    errors = []
    for filename, fields in (
        ("MUSIC_CONCEPT_RELATIONS.csv", identity_fields),
        ("GRAPH_AUDIT_MATRIX_v3.csv", review_fields),
        ("GRAPH_HUMAN_REVIEW_v3.csv", review_fields),
    ):
        rows, issues = verify_csv_schema(
            directory / filename, ["relation_id", *fields], "relation_id", r"(?:CR|REL|CDR)-[0-9]{3}$",
        )
        errors.extend(issues)
        tables[filename] = {row["relation_id"]: row for _, row in rows if "relation_id" in row}

    if errors:
        return errors
    originals, matrix, reviews = tables.values()
    if originals.keys() != matrix.keys() or originals.keys() != reviews.keys():
        return ["Graph matrix and review IDs must match the canonical relation register."]

    for ident, original in originals.items():
        digest = sha256(json.dumps(original, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        audit, review = matrix[ident], reviews[ident]
        if audit["original_row_sha256"] != digest:
            errors.append(f"{ident}: audit matrix does not match the original relation hash.")
        if any(not audit[name].strip() or audit[name] != review[name] for name in review_fields):
            errors.append(f"{ident}: audit matrix differs from the recorded v3 review.")
        for name in ("source_id", "target_id"):
            endpoint = audit[name]
            # Named and legacy nodes retain their separately reviewed identities.
            for pattern, prefix, count in (
                (r"PROG[-_]([0-9]{3})", "PROG", 28),
                (r"PAT-([0-9]{3})", "PAT", 31),
                (r"P([0-9]{2})", "P", 19),
                (r"REF-([0-9]{4})", "REF", 198),
            ):
                match = re.fullmatch(pattern, endpoint)
                if match and not 1 <= int(match[1]) <= count:
                    errors.append(f"{ident}: dangling {prefix} reference in {name}: {endpoint}.")
    return errors


class ReferenceIdChecker:
    def __init__(self, repo_root: Path, baseline_path: Path | None = None):
        self.repo_root = repo_root.resolve()
        self.baseline_path = baseline_path

    def run_check(self) -> ReferenceCheckReport:
        try:
            result = verify_integrity(self.repo_root, baseline_path=self.baseline_path)
            errors = result["errors"] + _check_graph_bindings(self.repo_root)
        except (OSError, ValueError, csv.Error) as exc:
            return ReferenceCheckReport(False, [f"Cannot complete reference checks: {exc}"])
        stats = result["stats"]
        return ReferenceCheckReport(not errors, errors, result["warnings"], sum(stats.values()), stats)


def validate_reference_ids(repo_root: Path | None = None, baseline_path: Path | None = None) -> ReferenceCheckReport:
    return ReferenceIdChecker(repo_root or REPOSITORY_ROOT, baseline_path).run_check()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, help="Repository data directory")
    parser.add_argument("--baseline", type=Path, help="Explicit identity baseline for this check")
    parser.add_argument("--quiet", action="store_true", help="Suppress text output")
    parser.add_argument("--json", action="store_true", help="Print a JSON report")
    args = parser.parse_args()
    report = validate_reference_ids(args.repo_root, args.baseline)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    elif not args.quiet:
        status = "PASS" if report.success else "FAIL"
        print(f"{status}: reference structure, baseline and graph bindings ({report.identities_checked} entries checked).")
        for message in report.errors + report.warnings:
            print(f"  - {message}")
    return 0 if report.success else 1


if __name__ == "__main__":
    sys.exit(main())
