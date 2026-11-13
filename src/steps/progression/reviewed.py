"""Validate publication evidence for the three pilot learning examples."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from .engine import CanonicalProgression, ReviewedProgression
from ..theory.exceptions import ProgressionParsingError

DIRECTORY = Path(__file__).resolve().parent
CATALOG = DIRECTORY / "reviewed_progressions.json"
APPROVALS = DIRECTORY / "reviewed_progression_approvals.json"
REGISTRY = DIRECTORY.parents[2] / "knowledge/sources/registry.yaml"
NOTATION = "PILOT-NOTATION-001"
REQUIRED_CLAIMS = {
    "PROG-001": ("PROG-001-HARMONY", "PROG-001-TONAL-CENTER"),
    "PROG-003": ("PROG-003-HARMONY", "PROG-003-VOICE-II-V", "PROG-003-VOICE-V-I"),
    "PROG-009": ("PROG-009-HARMONY", "PROG-009-VOICE-LEADING"),
}
KINDS = {"fact", "convention", "style_interpretation"}
VOICE_CLAIMS = {"PROG-003-VOICE-II-V", "PROG-003-VOICE-V-I", "PROG-009-VOICE-LEADING"}
PLACEHOLDER = re.compile(r"\b(?:placeholder|platzhalter|todo|tbd)\b", re.IGNORECASE)
REVIEW_LINK = re.compile(
    r"https://github\.com/n05a-design/steps/pull/[1-9]\d*#(?:pullrequestreview|issuecomment)-[1-9]\d*"
)


class PublicationError(ProgressionParsingError):
    """The pilot material does not meet the publication requirements."""


@dataclass(frozen=True)
class Citation:
    source_id: str
    title: str
    url: str
    locator: str


@dataclass(frozen=True)
class Claim:
    claim_id: str
    kind: str
    text: str
    scope: str
    countercheck: str
    citations: tuple[Citation, ...]
    fingerprint: str
    voice_path: tuple[tuple[int, str], ...]


@dataclass(frozen=True)
class ApprovedClaim:
    claim: Claim
    reviewer: str
    reviewed_on: str
    evidence_url: str


def _object(value, fields: set[str], label: str) -> dict:
    if not isinstance(value, dict) or value.keys() != fields:
        raise PublicationError(f"{label}: expected fields {', '.join(sorted(fields))}.")
    return value


def _text(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or PLACEHOLDER.search(value):
        raise PublicationError(f"{label}: missing text or placeholder.")
    return value


def _list(value, label: str) -> list:
    if not isinstance(value, list) or not value:
        raise PublicationError(f"{label}: expected a nonempty list.")
    return value


def _unique_keys(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise PublicationError(f"Duplicate data key: {key}.")
        result[key] = value
    return result


def _read(path: Path, schema_version: int, *fields: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_keys)
    except (OSError, ValueError) as exc:
        raise PublicationError(f"{path.name}: cannot read publication data ({exc}).") from exc
    _object(value, {"schema_version", *fields}, path.name)
    if type(value["schema_version"]) is not int or value["schema_version"] != schema_version:
        raise PublicationError(f"{path.name}: unsupported schema version.")
    return value


def _sha256(value) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _sources() -> dict[str, dict]:
    index = {}
    for source in _list(_read(REGISTRY, 1, "sources")["sources"], "Product sources"):
        if not isinstance(source, dict):
            raise PublicationError("Invalid product source entry.")
        ident = _text(source.get("id"), "Source ID")
        if ident in index:
            raise PublicationError(f"Duplicate source ID: {ident}.")
        index[ident] = source
    return index


def _claim(raw, owner: dict, sources: dict[str, dict]) -> Claim:
    if not isinstance(raw, dict):
        raise PublicationError("Invalid claim entry.")
    ident = _text(raw.get("id"), "Claim ID")
    fields = {"id", "kind", "text", "scope", "countercheck", "references"}
    if ident in VOICE_CLAIMS:
        fields.add("voice_path")
    _object(raw, fields, ident)
    kind = _text(raw["kind"], ident)
    if kind not in KINDS:
        raise PublicationError(f"{ident}: unknown claim kind {kind}.")
    text, scope, check = (_text(raw[key], f"{ident}.{key}") for key in ("text", "scope", "countercheck"))
    citations = []
    records = {}
    for ref in _list(raw["references"], f"{ident}.references"):
        _object(ref, {"source_id", "locator"}, ident)
        source_id = _text(ref["source_id"], f"{ident}.source_id")
        locator = _text(ref["locator"], f"{ident}.locator")
        if source_id in records:
            raise PublicationError(f"{ident}: duplicate source {source_id}.")
        source = sources.get(source_id)
        if source is None:
            raise PublicationError(f"{ident}: unknown source {source_id}.")
        if source.get("rights_status") != "approved":
            raise PublicationError(f"{ident}: unapproved source {source_id}.")
        title = _text(source.get("title"), f"{source_id}.title")
        url = _text(source.get("url"), f"{source_id}.url")
        try:
            parsed = urlsplit(url)
        except ValueError as exc:
            raise PublicationError(f"{source_id}: invalid HTTPS source URL.") from exc
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or re.search(r"[\s<>]", url):
            raise PublicationError(f"{source_id}: invalid HTTPS source URL.")
        records[source_id] = source
        citations.append(Citation(source_id, title, url, locator))
    path = []
    if ident in VOICE_CLAIMS:
        for point in _list(raw["voice_path"], f"{ident}.voice_path"):
            _object(point, {"chord_index", "note"}, ident)
            index = point["chord_index"]
            if type(index) is not int or not 0 <= index < len(owner["chords"].split(" - ")):
                raise PublicationError(f"{ident}: voice path chord index is outside the example.")
            path.append((index, _text(point["note"], f"{ident}.voice_path.note")))
        if len(path) < 2 or any(right[0] != left[0] + 1 for left, right in zip(path, path[1:])):
            raise PublicationError(f"{ident}: voice path must span successive chords.")
    fingerprint = _sha256({"format": 1, "example": owner, "claim": raw, "sources": records})
    return Claim(ident, kind, text, scope, check, tuple(citations), fingerprint, tuple(path))


def _candidates() -> tuple[dict[str, dict], dict[str, Claim]]:
    sources = _sources()
    examples = {}
    document = _read(CATALOG, 2, "notation", "examples")
    notation = _claim(document["notation"], {"applies_to": list(REQUIRED_CLAIMS)}, sources)
    if notation.claim_id != NOTATION or notation.kind != "convention":
        raise PublicationError("Missing pilot notation convention.")
    claims = {NOTATION: notation}
    fields = {"id", "name", "default_key", "roman", "chords", "context"}
    for row in _list(document["examples"], "Pilot examples"):
        if not isinstance(row, dict):
            raise PublicationError("Invalid pilot example.")
        ident = _text(row.get("id"), "Example ID")
        if ident in examples:
            raise PublicationError(f"Duplicate example: {ident}.")
        _object(row, fields | {"claims"}, ident)
        example = {field: _text(row[field], f"{ident}.{field}") for field in fields}
        examples[ident] = example
        ids = []
        for raw in _list(row["claims"], f"{ident}.claims"):
            claim = _claim(raw, {**example, "notation": notation.fingerprint}, sources)
            if claim.claim_id in claims:
                raise PublicationError(f"Duplicate claim: {claim.claim_id}.")
            claims[claim.claim_id] = claim
            ids.append(claim.claim_id)
        if tuple(ids) != REQUIRED_CLAIMS.get(ident):
            raise PublicationError(f"{ident}: missing, unexpected or reordered pilot claims.")
    if examples.keys() != REQUIRED_CLAIMS.keys():
        raise PublicationError("Pilot example set differs from the publication scope.")
    return examples, claims


def _approval_records(claims: dict[str, Claim]) -> dict[str, dict]:
    approvals = _read(APPROVALS, 1, "approvals")["approvals"]
    if not isinstance(approvals, dict) or approvals.keys() - claims.keys():
        raise PublicationError("Approval register contains unknown claim IDs or invalid data.")
    return approvals


def _approve(claim: Claim, record: dict) -> ApprovedClaim:
    ident = claim.claim_id
    _object(record, {"fingerprint", "reviewer", "reviewed_on", "evidence_url"}, ident)
    if record["fingerprint"] != claim.fingerprint:
        raise PublicationError(f"{ident}: approval does not match the current claim fingerprint.")
    reviewer = _text(record["reviewer"], f"{ident}.reviewer")
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", reviewer):
        raise PublicationError(f"{ident}: reviewer must be a GitHub user name.")
    reviewed_on = _text(record["reviewed_on"], f"{ident}.reviewed_on")
    try:
        parsed = date.fromisoformat(reviewed_on)
    except ValueError:
        raise PublicationError(f"{ident}: invalid review date.") from None
    if parsed.isoformat() != reviewed_on:
        raise PublicationError(f"{ident}: expected a review date in YYYY-MM-DD format.")
    if parsed > datetime.now(timezone.utc).date():
        raise PublicationError(f"{ident}: review date cannot be in the future.")
    evidence = _text(record["evidence_url"], f"{ident}.evidence_url")
    if not REVIEW_LINK.fullmatch(evidence):
        raise PublicationError(f"{ident}: expected a permalink to the human review or comment.")
    return ApprovedClaim(claim, reviewer, reviewed_on, evidence)


def load_reviewed_catalog() -> tuple[ReviewedProgression, ...]:
    """Load the pilot after checking the stored approvals and their fingerprints offline."""
    examples, claims = _candidates()
    records = _approval_records(claims)
    missing = claims.keys() - records.keys()
    if missing:
        raise PublicationError("Missing human approval: " + ", ".join(sorted(missing)) + ".")
    approved = {ident: _approve(claim, records[ident]) for ident, claim in claims.items()}
    version = _sha256({"claims": {ident: c.fingerprint for ident, c in claims.items()}, "approvals": records})
    result = []
    for ident, ids in REQUIRED_CLAIMS.items():
        row = examples[ident]
        items = tuple(approved[claim_id] for claim_id in (NOTATION, *ids))
        sources = tuple(dict.fromkeys(ref.source_id for item in items for ref in item.claim.citations))
        progression = CanonicalProgression(
            ident, row["name"], row["roman"], row["default_key"], row["chords"],
            row["context"], ", ".join(sources),
        )
        lesson = " ".join(item.claim.text for item in items[1:])
        result.append(ReviewedProgression(
            progression, lesson, sources, max(item.reviewed_on for item in items), items, version,
        ))
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-manifest", action="store_true", required=True)
    parser.parse_args()
    _, claims = _candidates()
    records = _approval_records(claims)
    print("Review candidates (this command does not publish)")
    for ident, claim in claims.items():
        if ident not in records:
            status = "PENDING"
        else:
            try:
                _approve(claim, records[ident])
            except PublicationError:
                status = "INVALID_APPROVAL"
            else:
                status = "APPROVAL_RECORDED"
        print(f"{ident}\t{claim.kind}\t{status}\t{claim.fingerprint}")


if __name__ == "__main__":
    main()
