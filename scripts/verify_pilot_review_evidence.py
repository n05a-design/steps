"""Verify the pilot's GitHub approvals against the exact catalog fingerprints."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.progression import reviewed

REPOSITORY = "n05a-design/steps"
# Numeric GitHub identity survives username changes and cannot be supplied by the catalog.
REVIEWERS = frozenset({333259995, 331406730})
URL = re.compile(r"https://github\.com/n05a-design/steps/pull/([1-9]\d*)#issuecomment-([1-9]\d*)")
APPROVAL_LINE = re.compile(r"STEPS-APPROVED ([A-Z0-9-]+) ([a-f0-9]{64})")
LEGACY_TABLE = 6833747279
LEGACY_QUOTE = 6834765537
MAX_COMMENT_BYTES = 1_000_000


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_comment(comment_id: int) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    endpoint = f"https://api.github.com/repos/{REPOSITORY}/issues/comments/{comment_id}"
    try:
        with build_opener(NoRedirect).open(Request(endpoint, headers=headers), timeout=12) as response:
            raw = response.read(MAX_COMMENT_BYTES + 1)
        if len(raw) > MAX_COMMENT_BYTES:
            raise ValueError("oversized GitHub response")
        return json.loads(raw)
    except (OSError, ValueError) as exc:
        raise reviewed.PublicationError(f"Cannot verify GitHub comment {comment_id}: {exc}") from exc


def approvals_in_body(body: str, comment_id: int) -> set[tuple[str, str]]:
    approvals = set()
    for line in body.splitlines():
        match = APPROVAL_LINE.fullmatch(line)
        if not match and comment_id == LEGACY_TABLE:
            match = re.fullmatch(
                r"\| `([A-Z0-9-]+)` \| `([a-f0-9]{64})` \| \*\*Freigegeben\.\*\* [^|]+ \|",
                line,
            )
        if not match and comment_id == LEGACY_QUOTE:
            match = re.fullmatch(
                r"> Ich gebe ([A-Z0-9-]+) in der Fassung ([a-f0-9]{64}) fachlich frei\.", line,
            )
        if match:
            approvals.add(match.groups())
    return approvals


def verify_approval(approval, comment: dict, *, now: datetime) -> None:
    claim = approval.claim
    permalink = URL.fullmatch(approval.evidence_url)
    if not permalink:
        raise reviewed.PublicationError(f"{claim.claim_id}: expected a GitHub pull request comment.")
    pr, comment_id = map(int, permalink.groups())
    try:
        author = comment["user"]
        created = datetime.fromisoformat(comment["created_at"])
        updated = datetime.fromisoformat(comment["updated_at"])
        valid = (
            comment["id"] == comment_id
            and comment["html_url"] == approval.evidence_url
            and comment["issue_url"] == f"https://api.github.com/repos/{REPOSITORY}/issues/{pr}"
            and author["id"] in REVIEWERS
            and author["type"] == "User"
            and author["login"].casefold() == approval.reviewer.casefold()
            and comment["author_association"] in {"OWNER", "MEMBER", "COLLABORATOR"}
            and created.utcoffset() is not None
            and created == updated and created <= now
            and created.astimezone(timezone.utc).date().isoformat() == approval.reviewed_on
            and (claim.claim_id, claim.fingerprint) in approvals_in_body(comment["body"], comment_id)
        )
    except (AttributeError, KeyError, TypeError, ValueError):
        valid = False
    if not valid:
        raise reviewed.PublicationError(f"{claim.claim_id}: GitHub comment {comment_id} does not prove approval.")


def verify_catalog(catalog, fetch=fetch_comment, *, now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    seen = {}
    comments = {}
    for example in catalog:
        for approval in example.claims:
            ident = approval.claim.claim_id
            if ident in seen:
                if seen[ident] != approval:
                    raise reviewed.PublicationError(f"{ident}: inconsistent approval records.")
                continue
            match = URL.fullmatch(approval.evidence_url)
            if not match:
                raise reviewed.PublicationError(f"{ident}: expected a GitHub pull request comment.")
            comment_id = int(match[2])
            if comment_id not in comments:
                comments[comment_id] = fetch(comment_id)
            verify_approval(approval, comments[comment_id], now=now)
            seen[ident] = approval
    if not seen:
        raise reviewed.PublicationError("No pilot approvals to verify.")
    return len(seen)


def catalog_from_revision(revision: str):
    """Use the verifier's code and read only three data blobs from the proposed revision."""
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Expected the full SHA of a Git commit.")
    subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=ROOT, check=True,
    )
    with TemporaryDirectory() as temporary:
        files = {}
        for key in ("CATALOG", "APPROVALS", "REGISTRY"):
            relative = getattr(reviewed, key).relative_to(ROOT).as_posix()
            target = Path(temporary) / Path(relative).name
            with target.open("wb") as stream:
                subprocess.run(
                    ["git", "cat-file", "blob", f"{revision}:{relative}"],
                    cwd=ROOT, stdout=stream, check=True,
                )
            files[key] = target
        with patch.multiple(reviewed, **files):
            return reviewed.load_reviewed_catalog()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="Full Git commit SHA. Only its catalog data is read.")
    args = parser.parse_args()
    try:
        catalog = catalog_from_revision(args.revision) if args.revision else reviewed.load_reviewed_catalog()
        count = verify_catalog(catalog)
    except (reviewed.PublicationError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Pilot evidence blocked: {exc}\n")
    print(f"Verified {count} GitHub pilot approvals.")


if __name__ == "__main__":
    main()
