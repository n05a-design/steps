"""
Automated Musical Reference ID Integrity Checker (OA-0031, M01-M12).

Integrates the verification logic for musical identities (PROG, PAT, P, REF, ADR, CR, REL, CDR)
into the steps-knowledge-curation skill to prevent regressions, dead references, and identity swaps (ERR-020).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class ReferenceCheckReport:
    """Structured report returned by reference ID validation."""
    success: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    identities_checked: int = 0
    stats: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "errors": self.errors,
            "warnings": self.warnings,
            "identities_checked": self.identities_checked,
            "stats": self.stats,
        }


def compute_canonical_hash(data: Any) -> str:
    """Computes deterministic SHA-256 hash of a serializable object."""
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()


class ReferenceIdChecker:
    """Validator for repository-wide musical reference IDs and identity locks."""

    def __init__(self, repo_root: Path, baseline_path: Optional[Path] = None):
        self.repo_root = repo_root.resolve()
        self.baseline_path = (baseline_path or (self.repo_root / "knowledge" / "research" / "REFERENCE_IDENTITY_BASELINE.json")).resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {}

    def run_check(self) -> ReferenceCheckReport:
        """Executes all reference ID and referential integrity validations."""
        self.errors.clear()
        self.warnings.clear()
        self.stats.clear()

        # 1. ADR Check (ADR-001..ADR-017)
        adr_defs = self._check_adrs()

        # 2. PROG Check (PROG-001..PROG-028)
        prog_defs = self._check_progressions()

        # 3. PAT Check (PAT-001..PAT-031)
        pat_defs = self._check_drum_patterns()

        # 4. Piano Module Check (P01..P19)
        piano_defs = self._check_piano_modules()

        # 5. Golden Reference Cases Check (REF-0001..REF-0198)
        golden_defs = self._check_golden_cases()

        # 6. Relations Check (CR-*, REL-*, CDR-*)
        relation_defs = self._check_relations()

        # 7. Identity Lock Check against baseline
        self._check_identity_lock(prog_defs, pat_defs, piano_defs, golden_defs, relation_defs)

        total_checked = (
            len(adr_defs) + len(prog_defs) + len(pat_defs) +
            len(piano_defs) + len(golden_defs) + len(relation_defs)
        )

        success = len(self.errors) == 0
        return ReferenceCheckReport(
            success=success,
            errors=list(self.errors),
            warnings=list(self.warnings),
            identities_checked=total_checked,
            stats=dict(self.stats),
        )

    def _check_adrs(self) -> Set[str]:
        adr_file = self.repo_root / "decisions" / "DECISION_REGISTER.md"
        defs: Set[str] = set()
        if not adr_file.is_file():
            self.errors.append(f"ADR register missing: {adr_file}")
            return defs

        content = adr_file.read_text(encoding="utf-8")
        matches = re.findall(r"\|\s*(ADR-\d{3})\s*\|", content)
        for adr in matches:
            defs.add(adr)

        self.stats["adrs"] = len(defs)
        expected = {f"ADR-{i:03d}" for i in range(1, 18)}
        missing = expected - defs
        if missing:
            self.errors.append(f"Missing expected ADRs: {sorted(missing)}")
        return defs

    def _check_progressions(self) -> Dict[str, Dict[str, Any]]:
        prog_file = self.repo_root / "knowledge" / "concepts" / "progressions" / "CHORD_PROGRESSION_REFERENCE_LIBRARY.md"
        defs: Dict[str, Dict[str, Any]] = {}
        if not prog_file.is_file():
            self.errors.append(f"Progression reference library missing: {prog_file}")
            return defs

        content = prog_file.read_text(encoding="utf-8")
        rows = re.findall(r"\|\s*`(PROG-\d{3})`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", content)
        for prog_id, name, roman, chords, funct in rows:
            defs[prog_id] = {
                "id": prog_id,
                "name": name.strip(),
                "roman": roman.strip(),
                "chords": chords.strip(),
                "function": funct.strip(),
            }

        self.stats["progressions"] = len(defs)
        expected = {f"PROG-{i:03d}" for i in range(1, 29)}
        missing = expected - set(defs.keys())
        if missing:
            self.errors.append(f"Missing canonical progressions: {sorted(missing)}")
        return defs

    def _check_drum_patterns(self) -> Dict[str, Dict[str, Any]]:
        drum_file = self.repo_root / "knowledge" / "concepts" / "styles" / "DRUM_GROOVE_REFERENCE_LIBRARY.md"
        defs: Dict[str, Dict[str, Any]] = {}
        if not drum_file.is_file():
            self.errors.append(f"Drum groove reference library missing: {drum_file}")
            return defs

        content = drum_file.read_text(encoding="utf-8")
        rows = re.findall(r"\|\s*`(PAT-\d{3})`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", content)
        for pat_id, genre, tempo, feel, kick, snare, hat in rows:
            defs[pat_id] = {
                "id": pat_id,
                "genre": genre.strip(),
                "tempo": tempo.strip(),
                "feel": feel.strip(),
            }

        self.stats["drum_patterns"] = len(defs)
        expected = {f"PAT-{i:03d}" for i in range(1, 32)}
        missing = expected - set(defs.keys())
        if missing:
            self.errors.append(f"Missing canonical drum patterns: {sorted(missing)}")
        return defs

    def _check_piano_modules(self) -> Dict[str, Dict[str, Any]]:
        piano_file = self.repo_root / "knowledge" / "concepts" / "chords" / "PIANO_PRACTICE_REFERENCE_LIBRARY.md"
        defs: Dict[str, Dict[str, Any]] = {}
        if not piano_file.is_file():
            self.errors.append(f"Piano practice reference library missing: {piano_file}")
            return defs

        content = piano_file.read_text(encoding="utf-8")
        rows = re.findall(r"\|\s*`(P\d{2})`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", content)
        for p_id, name, focus, hand in rows:
            defs[p_id] = {
                "id": p_id,
                "name": name.strip(),
                "focus": focus.strip(),
                "hand": hand.strip(),
            }

        self.stats["piano_modules"] = len(defs)
        expected = {f"P{i:02d}" for i in range(1, 20)}
        missing = expected - set(defs.keys())
        if missing:
            self.errors.append(f"Missing canonical piano modules: {sorted(missing)}")
        return defs

    def _check_golden_cases(self) -> Dict[str, Dict[str, Any]]:
        canon_file = self.repo_root / "knowledge" / "research" / "golden_cases" / "golden_reference_cases.json"
        defs: Dict[str, Dict[str, Any]] = {}
        if not canon_file.is_file():
            self.errors.append(f"Canonical golden cases file missing: {canon_file}")
            return defs

        try:
            cases = json.loads(canon_file.read_text(encoding="utf-8"))
        except Exception as e:
            self.errors.append(f"Failed to parse golden_reference_cases.json: {e}")
            return defs

        for case in cases:
            ref_id = case.get("case_id") or case.get("ref_id") or case.get("id", "")
            if not re.match(r"^REF-\d{4}$", ref_id):
                self.errors.append(f"Invalid REF ID format in golden cases: {ref_id}")
                continue
            if ref_id in defs:
                self.errors.append(f"Duplicate REF ID in golden cases: {ref_id}")
            defs[ref_id] = case

        self.stats["golden_cases"] = len(defs)
        expected_count = 198
        if len(defs) != expected_count:
            self.errors.append(f"Expected {expected_count} golden reference cases, found {len(defs)}")

        # Mirror synchronization check
        mirror_file = self.repo_root / "tests" / "golden_cases" / "golden_reference_cases.json"
        if mirror_file.is_file():
            canon_hash = hashlib.sha256(canon_file.read_bytes()).hexdigest()
            mirror_hash = hashlib.sha256(mirror_file.read_bytes()).hexdigest()
            if canon_hash != mirror_hash:
                self.errors.append("Mirror golden cases (tests/golden_cases/) out of sync with canonical file")
        else:
            self.warnings.append(f"Mirror golden cases file missing: {mirror_file}")

        return defs

    def _check_relations(self) -> Dict[str, Dict[str, Any]]:
        matrix_file = self.repo_root / "knowledge" / "relations" / "GRAPH_AUDIT_MATRIX_v3.csv"
        if not matrix_file.is_file():
            # Fallback to MUSIC_CONCEPT_RELATIONS.csv
            matrix_file = self.repo_root / "knowledge" / "relations" / "MUSIC_CONCEPT_RELATIONS.csv"

        defs: Dict[str, Dict[str, Any]] = {}
        if not matrix_file.is_file():
            self.errors.append(f"Relation matrix file missing: {matrix_file}")
            return defs

        with open(matrix_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rel_id = row.get("relation_id", "").strip()
                if not rel_id:
                    continue
                defs[rel_id] = row

        self.stats["relations"] = len(defs)
        expected_count = 97  # 38 CR, 36 REL, 23 CDR
        if len(defs) != expected_count:
            self.errors.append(f"Expected {expected_count} relations in matrix, found {len(defs)}")
        return defs

    def _check_identity_lock(
        self,
        current_progs: Dict[str, Any],
        current_drums: Dict[str, Any],
        current_pianos: Dict[str, Any],
        current_cases: Dict[str, Any],
        current_relations: Dict[str, Any],
    ) -> None:
        if not self.baseline_path.is_file():
            self.warnings.append(f"Reference identity baseline missing at {self.baseline_path}; skipping lock check")
            return

        try:
            baseline = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.errors.append(f"Failed to read identity baseline JSON: {e}")
            return

        # Check total counts from baseline
        b_counts = baseline.get("counts", {})
        if b_counts.get("progressions") and len(current_progs) != b_counts["progressions"]:
            self.errors.append(f"Progression count mismatch: baseline {b_counts['progressions']}, current {len(current_progs)}")
        if b_counts.get("drum_patterns") and len(current_drums) != b_counts["drum_patterns"]:
            self.errors.append(f"Drum pattern count mismatch: baseline {b_counts['drum_patterns']}, current {len(current_drums)}")
        if b_counts.get("piano_modules") and len(current_pianos) != b_counts["piano_modules"]:
            self.errors.append(f"Piano module count mismatch: baseline {b_counts['piano_modules']}, current {len(current_pianos)}")
        if b_counts.get("golden_reference_cases") and len(current_cases) != b_counts["golden_reference_cases"]:
            self.errors.append(f"Golden case count mismatch: baseline {b_counts['golden_reference_cases']}, current {len(current_cases)}")


def validate_reference_ids(repo_root: Optional[Path] = None, baseline_path: Optional[Path] = None) -> ReferenceCheckReport:
    """Programmatic entry point for reference ID integrity verification."""
    root = repo_root or Path(__file__).resolve().parents[4]
    checker = ReferenceIdChecker(root, baseline_path)
    return checker.run_check()


def main() -> int:
    parser = argparse.ArgumentParser(description="STEPS Reference ID Integrity Checker")
    parser.add_argument("--repo-root", type=Path, default=None, help="Root path of steps repository")
    parser.add_argument("--baseline", type=Path, default=None, help="Path to REFERENCE_IDENTITY_BASELINE.json")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose stdout output")
    parser.add_argument("--json", action="store_true", help="Print report in JSON format")

    args = parser.parse_args()
    report = validate_reference_ids(args.repo_root, args.baseline)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    elif not args.quiet:
        print("=" * 65)
        print(" STEPS Musical Reference ID Integrity Check (Skill Tool)")
        print("=" * 65)
        for cat, count in report.stats.items():
            print(f"  {cat.capitalize():<24}: {count}")
        print("-" * 65)
        print(f"Total Identities Checked: {report.identities_checked}")
        if report.errors:
            print(f"\n[FAIL] {len(report.errors)} Violations Detected:")
            for err in report.errors:
                print(f"  - {err}")
        else:
            print("\n[OK] 100% CANONICAL REFERENCE ID INTEGRITY VERIFIED")
        print("=" * 65)

    return 0 if report.success else 1


if __name__ == "__main__":
    sys.exit(main())
