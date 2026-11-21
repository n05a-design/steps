"""Fingerprint curated content outside the historical reference identity baseline."""

from __future__ import annotations

import json
from pathlib import Path
import re

from scripts.verify_reference_integrity import (
    compute_canonical_hash, extract_markdown_table_definitions, verify_csv_schema,
)

MANIFEST = Path("knowledge/research/CURATION_EVIDENCE_FINGERPRINTS.json")
CATALOGS = {
    "knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md": (r"PROG-[0-9]{3}$", 6),
    "knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md": (r"PAT-[0-9]{3}$", 7),
    "knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md": (r"P[0-9]{2}$", 5),
}
EVIDENCE_TABLES = {
    "knowledge/relations/GRAPH_AUDIT_MATRIX_v3.csv": "relation_id",
    "knowledge/relations/GRAPH_HUMAN_REVIEW_v3.csv": "relation_id",
    "knowledge/research/HISTORICAL_REFERENCE_ID_MATRIX.csv": "REF_ID",
    "knowledge/research/MUSIC_DOMAIN_READINESS_MATRIX.csv": "domain_id",
}
GOLDEN = "knowledge/research/golden_cases/golden_reference_cases.json"
GOLDEN_EVIDENCE_FIELDS = ("category", "test_class", "tolerance", "theoretical_rule", "source_citation")


def _unique_members(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON object member in curation evidence.")
    return result


def evidence_snapshot(root: Path) -> dict:
    """Build a deterministic report without changing the versioned fingerprints."""
    fingerprints = {}
    errors = []
    for path, (pattern, columns) in CATALOGS.items():
        rows, issues = extract_markdown_table_definitions(root / path, pattern, expected_cols=columns)
        errors.extend(issues)
        fingerprints[path] = {ident: compute_canonical_hash(parts) for ident, _, parts in rows}

    for path, id_field in EVIDENCE_TABLES.items():
        rows, issues = verify_csv_schema(root / path, [id_field], id_col=id_field)
        errors.extend(issues)
        fingerprints[path] = {
            row[id_field]: compute_canonical_hash({
                key: value.replace("\r\n", "\n") for key, value in row.items()
            })
            for _, row in rows if id_field in row
        }

    cases = json.loads((root / GOLDEN).read_text(encoding="utf-8"), object_pairs_hook=_unique_members)
    if not isinstance(cases, list):
        errors.append("Golden evidence requires a JSON array.")
        cases = []
    golden = {}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("case_id"), str):
            errors.append("Golden evidence record has no valid case_id.")
            continue
        if case["case_id"] in golden:
            errors.append(f"Duplicate Golden evidence ID: {case['case_id']}")
            continue
        # Preserve field presence as well as the value. An omitted and a null field differ.
        golden[case["case_id"]] = compute_canonical_hash({
            name: case[name] for name in GOLDEN_EVIDENCE_FIELDS if name in case
        })
    fingerprints[GOLDEN] = golden

    if errors:
        raise ValueError("; ".join(errors))
    return {"version": 1, "records": fingerprints}


def verify_evidence(root: Path) -> list[str]:
    current = evidence_snapshot(root)["records"]
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"), object_pairs_hook=_unique_members)
    if (not isinstance(manifest, dict) or type(manifest.get("version")) is not int
            or manifest["version"] != 1 or not isinstance(manifest.get("records"), dict)
            or manifest["records"].keys() != current.keys()):
        return [f"Invalid curation evidence manifest: {MANIFEST}"]

    errors = []
    for path, actual in current.items():
        expected = manifest["records"][path]
        if not isinstance(expected, dict) or not expected or any(
            not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)
            for digest in expected.values()
        ):
            errors.append(f"Invalid curation evidence fingerprints: {path}")
            continue
        for ident in sorted(expected.keys() | actual.keys()):
            if expected.get(ident) != actual.get(ident):
                errors.append(f"Curation evidence changed: {path} [{ident}]")
    return errors
