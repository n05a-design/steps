#!/usr/bin/env python3
"""
STEPS HTML In-Place Markdown Converter (Trafilatura Engine).

Crawls a target directory tree for HTML files, filters out browser companion
artefacts (_files/, iframes, git trees), and converts each document into clean,
boilerplate-free Markdown right alongside the original HTML file.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import trafilatura
except ImportError:
    print("FEHLER: 'trafilatura' ist nicht im aktuellen Python-Environment installiert.")
    print("Bitte installieren mit: pip install trafilatura")
    sys.exit(1)


IGNORE_PATTERNS = [
    "/.git/",
    "/.claude/",
    "/node_modules/",
    "/__pycache__/",
    "_files/",
    "_files\\",
]


def is_candidate_html(path: Path) -> bool:
    s = str(path.resolve())
    for pattern in IGNORE_PATTERNS:
        if pattern in s:
            return False
    return True


def extract_spa_json_dataset(html_text: str, title: str = "") -> str | None:
    """
    Extracts structured prompt/scene datasets from interactive HTML Single Page Apps
    (e.g. Gemini prompt libraries storing datasets in <script> or JSON variables).
    """
    data = None
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html_text, re.DOTALL)
    for s in scripts:
        s_clean = s.strip()
        # Direct JSON array or object
        if (s_clean.startswith("[") and s_clean.endswith("]")) or (s_clean.startswith("{") and s_clean.endswith("}")):
            try:
                parsed = json.loads(s_clean)
                if isinstance(parsed, list) and len(parsed) > 0:
                    data = parsed
                    break
                elif isinstance(parsed, dict) and "scenes" in parsed:
                    data = parsed["scenes"]
                    break
            except Exception:
                pass

        # JS assignment: const/let/var (data|DATA|scenes|payload|SCENES) = [ ... ]
        m = re.search(r'(?:const|let|var)\s+\w+\s*=\s*(\[.*?\])\s*(?:;|\n\s*(?:function|let|const|var|\"use|document))', s, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(1).strip())
                if isinstance(parsed, list) and len(parsed) > 0:
                    data = parsed
                    break
            except Exception:
                pass

        # Bracket balancing fallback
        idx = s.find("=[")
        if idx == -1:
            idx = s.find("= [")
        if idx != -1:
            start = s.find("[", idx)
            depth = 0
            end = None
            for i in range(start, len(s)):
                if s[i] == "[": depth += 1
                elif s[i] == "]":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end:
                try:
                    parsed = json.loads(s[start:end])
                    if isinstance(parsed, list) and len(parsed) > 0:
                        data = parsed
                        break
                except Exception:
                    pass

    if not data or not isinstance(data, list):
        return None

    md = [f"# {title}\n", f"**Extrahierte Datensätze / Szenen:** {len(data)}\n"]
    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            md.append(f"\n## Element {idx}\n{item}\n")
            continue
        num = item.get("num") or item.get("number") or item.get("n") or item.get("id") or idx
        item_title = item.get("title") or item.get("name") or "Szene"
        md.append(f"\n## Szene {num}: {item_title}")
        tag = item.get("tag") or item.get("category") or item.get("cat")
        if tag: md.append(f"**Kategorie:** {tag}")
        sub = item.get("subtitle") or item.get("desc") or item.get("description")
        if sub: md.append(f"**Beschreibung:** {sub}")

        for k in ["pose", "camera", "movement", "physics", "setup", "lighting", "notes", "framing", "motion"]:
            if k in item and item[k]:
                md.append(f"- **{k.capitalize()}:** {item[k]}")

        for pk, lbl in [
            ("image_prompt", "Image Prompt (Standbild)"),
            ("imagePrompt", "Image Prompt (Standbild)"),
            ("prompt_a", "Prompt A (Standbild)"),
            ("promptA", "Prompt A (Standbild)"),
            ("still_prompt", "Still Prompt"),
            ("video_prompt", "Video Prompt (Motion)"),
            ("videoPrompt", "Video Prompt (Motion)"),
            ("prompt_b", "Prompt B (Motion)"),
            ("promptB", "Prompt B (Motion)"),
            ("motion_prompt", "Motion Prompt"),
            ("prompt", "Prompt")
        ]:
            if pk in item and item[pk]:
                md.append(f"\n### {lbl}\n```\n{item[pk]}\n```\n")
        md.append("---\n")

    return "\n".join(md)


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def process_html_file(
    html_path: Path,
    overwrite: bool = False,
    dry_run: bool = False
) -> Tuple[str, str, str, str]:
    """
    Processes a single HTML file.
    Returns: (status, target_md_path, source_sha, md_sha)
    """
    md_path = html_path.with_suffix(".md")

    if md_path.exists() and not overwrite:
        return "SKIPPED_EXISTING", str(md_path), "", ""

    raw_bytes = html_path.read_bytes()
    source_sha = compute_sha256(raw_bytes)

    if dry_run:
        return "WOULD_CONVERT", str(md_path), source_sha, ""

    html_text = raw_bytes.decode("utf-8", errors="ignore")

    # Step 1: Check if this is an interactive prompt/SPA app with JSON datasets
    extracted_md = extract_spa_json_dataset(html_text, title=html_path.stem.replace("_", " "))

    # Step 2: If not an SPA dataset, extract using Trafilatura article engine
    if not extracted_md:
        extracted_md = trafilatura.extract(
            html_text,
            output_format="markdown",
            include_links=True,
            include_images=True,
            include_tables=True,
            favor_precision=True
        )

    # Step 3: Recall fallback
    if not extracted_md or not extracted_md.strip():
        extracted_md = trafilatura.extract(
            html_text,
            output_format="markdown",
            include_links=True,
            include_images=True,
            include_tables=True,
            favor_recall=True
        )

    if not extracted_md or not extracted_md.strip():
        return "EMPTY_OR_UNEXTRACTABLE", str(md_path), source_sha, ""

    md_bytes = extracted_md.encode("utf-8")
    md_path.write_bytes(md_bytes)
    md_sha = compute_sha256(md_bytes)

    return "CONVERTED", str(md_path), source_sha, md_sha

    md_bytes = extracted_md.encode("utf-8")
    md_path.write_bytes(md_bytes)
    md_sha = compute_sha256(md_bytes)

    return "CONVERTED", str(md_path), source_sha, md_sha


def main():
    parser = argparse.ArgumentParser(
        description="Crawle HTML-Dateien und wandle sie in-place in saubere Markdown-Dateien um."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Wurzelverzeichnis für die Suche (Standard: aktuelles Verzeichnis)."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Überschreibe bestehende .md Dateien, falls sie bereits existieren."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simuliere den Vorgang, ohne .md Dateien zu schreiben."
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default="manifests/html_markdown_migration.csv",
        help="Pfad für die CSV-Manifest-Ausgabe."
    )

    args = parser.parse_args()
    root_dir = Path(args.root).resolve()

    if not root_dir.exists():
        print(f"Fehler: Pfad {root_dir} existiert nicht.")
        sys.exit(1)

    print(f"Crawle Verzeichnis: {root_dir}")
    all_html = [p for p in root_dir.rglob("*.html") if is_candidate_html(p)]

    print(f"Gefundene echte HTML-Dokumente (ohne _files/ und .git/): {len(all_html)}")

    manifest_rows = ["html_source,md_target,status,source_sha256,md_sha256"]
    stats = {"CONVERTED": 0, "SKIPPED_EXISTING": 0, "WOULD_CONVERT": 0, "EMPTY_OR_UNEXTRACTABLE": 0}

    for idx, html_path in enumerate(sorted(all_html), start=1):
        status, md_target, src_sha, md_sha = process_html_file(
            html_path,
            overwrite=args.overwrite,
            dry_run=args.dry_run
        )
        stats[status] = stats.get(status, 0) + 1
        manifest_rows.append(f'"{html_path}","{md_target}","{status}","{src_sha}","{md_sha}"')

        rel_path = html_path.relative_to(root_dir) if html_path.is_relative_to(root_dir) else html_path
        print(f"[{idx:3d}/{len(all_html)}] {status:18s} -> {rel_path}")

    # Write manifest if not dry-run
    if not args.dry_run and manifest_rows:
        manifest_path = Path(args.manifest)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text("\n".join(manifest_rows) + "\n", encoding="utf-8")
        print(f"\nManifest gespeichert: {manifest_path}")

    print("\n=== Zusammenfassung ===")
    for k, v in stats.items():
        if v > 0:
            print(f"  {k:22s}: {v}")


if __name__ == "__main__":
    main()
