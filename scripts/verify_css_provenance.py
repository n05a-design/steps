"""Trace registered CSS blobs through saved Bandcamp embeds; optionally compare live CDN bytes.

Only hashes, paths and source URLs are reported. This does not grant redistribution rights.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.verify_registered_git_files import git, verify

IDS = ("F00412", "F00571", "F00704", "F00768", "F00937", "F01002")


class Stylesheets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and "stylesheet" in values.get("rel", "").split():
            self.links.append(values.get("href", ""))


def stylesheet_links(text):
    parser = Stylesheets()
    parser.feed(text)
    return parser.links


def saved_embed(text, filename):
    match = re.search(r"<!--\s*saved from url=\(\d+\)(https://bandcamp\.com/EmbeddedPlayer/[^\s]+)\s*-->", text)
    return match[1] if match and f"./{filename}" in stylesheet_links(text) else None


def live_match(embed_url, filename, expected_size, expected_hash):
    parsed = urlsplit(embed_url)
    if parsed.scheme != "https" or parsed.hostname != "bandcamp.com" or not parsed.path.startswith("/EmbeddedPlayer/"):
        raise ValueError("Expected an HTTPS Bandcamp embed URL")
    with urlopen(embed_url, timeout=20) as response:
        links = stylesheet_links(response.read().decode("utf-8"))
    matches = [url for url in links if PurePosixPath(urlsplit(url).path).name == filename
               and urlsplit(url).scheme == "https" and urlsplit(url).hostname
               and urlsplit(url).hostname.endswith(".bcbits.com")]
    if len(set(matches)) != 1:
        raise ValueError("The live embed does not identify exactly one matching Bandcamp CDN stylesheet")
    with urlopen(matches[0], timeout=20) as response:
        content = response.read()
        result = {"url": response.url, "size": len(content), "sha256": sha256(content).hexdigest(),
                  "last_modified": response.headers.get("Last-Modified")}
    result["status"] = "MATCH" if (result["size"], result["sha256"]) == (expected_size, expected_hash) else "MISMATCH"
    return result


def trace(repository, tree, records, online=False):
    report = verify(repository, tree, records)
    blobs = {}
    for entry in git(repository, "ls-tree", "-rz", report["tree"]).split(b"\0"):
        if entry:
            meta, path = entry.split(b"\t", 1)
            if meta.split()[1] == b"blob":
                blobs[path.decode("utf-8")] = meta.split()[2].decode()
    for result in report["results"]:
        path = PurePosixPath(result["path"])
        witnesses = []
        for html_path, oid in blobs.items():
            candidate = PurePosixPath(html_path)
            if candidate.parent != path.parent or candidate.suffix != ".html":
                continue
            content = git(repository, "cat-file", "blob", oid)
            embed_url = saved_embed(content.decode("utf-8"), path.name)
            if embed_url:
                witnesses.append({"path": html_path, "blob": oid, "sha256": sha256(content).hexdigest(), "embed_url": embed_url})
        result["saved_embed_witnesses"] = witnesses
        result["chain_status"] = "MATCH" if witnesses and result["status"] == "MATCH" else "MISSING"
        if online and witnesses:
            try:
                result["live_origin"] = live_match(witnesses[0]["embed_url"], path.name,
                                                   result["expected_size"], result["expected_sha256"])
            except (OSError, ValueError) as exc:
                result["live_origin"] = {"status": "UNAVAILABLE", "reason": str(exc)}
    report.update(checked_at=datetime.now(timezone.utc).isoformat(), online=online,
                  scope="byte identity and saved/live delivery chain; bundle rights and human approval unreviewed",
                  rights_status="UNREVIEWED_BUNDLE; jQuery UI header applies only to its component")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=ROOT)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()
    with (ROOT / "knowledge/sources/MUSIC_SOURCE_REVIEW_PROGRESS.csv").open(encoding="utf-8-sig", newline="") as source:
        records = [row for row in csv.DictReader(source) if row["file_id"] in IDS]
    if {row["file_id"] for row in records} != set(IDS):
        parser.error("The six CSS registry identities must be present")
    try:
        report = trace(args.repository, args.tree, records, args.online)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"BLOCKED: local source chain unavailable or invalid: {exc}\n")
    args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in report["results"]:
        print(row["file_id"], row["status"], row["chain_status"], row.get("live_origin", {}).get("status", "NOT_CHECKED"))
    return int(any(row["chain_status"] != "MATCH" or (args.online and row.get("live_origin", {}).get("status") != "MATCH")
                   for row in report["results"]))


if __name__ == "__main__":
    raise SystemExit(main())
