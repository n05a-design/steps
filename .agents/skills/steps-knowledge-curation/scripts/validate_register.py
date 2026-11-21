"""Validate the structure and declared evidence of the canonical register."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from register_paths import REPOSITORY_ROOT, master_path
from repository_verifier import verifier


VALID_STATUSES = {
    "OPEN", "IN_PROGRESS", "BLOCKED", "OWNER_DECISION_REQUIRED",
    "DONE_UNVERIFIED", "DONE_VERIFIED", "SUPERSEDED", "NOT_APPLICABLE",
}
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$")
TASK = re.compile(r"(OA-[0-9]{4}):[ \t]*(.*)")
FIELD_PREFIX = r"^ {0,3}(?:[-*+][ \t]+)?"
COMMIT_HASH = r"(?!0{40}(?:0{24})?$)[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?"
STATUS = re.compile(FIELD_PREFIX + r"\*\*Status:\*\*[ \t]*(.*)$")
EVIDENCE_FIELDS = {
    "Commit": COMMIT_HASH,
    "Prüfung": r".+",
    "Abnahmebeleg": r".+",
    "Abnahmekriterien": r".+",
}


def _looks_like_task_heading(title: str) -> bool:
    # Recognize formatted IDs as task attempts so they receive a syntax error.
    return title.lstrip(" `*_").upper().startswith("OA-")


def _register_tasks(content: str, errors: list[str]):
    task = None
    previous = ""
    for _, line in verifier.visible_markdown_lines(content.splitlines(), errors=errors):
        if re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", line) and _looks_like_task_heading(previous):
            errors.append(f"OA tasks require a level-three heading: {previous.strip()}")
        html_heading = re.match(r"^ {0,3}<h[1-6](?:\s[^>]*)?>[ \t]*(.*?)</h[1-6]>", line, re.I)
        if html_heading and _looks_like_task_heading(html_heading[1]):
            errors.append(f"OA tasks require a Markdown level-three heading: {html_heading[1]}")
        previous = line
        heading = HEADING.fullmatch(line)
        if heading and len(heading[1]) <= 3:
            if task is not None:
                yield task
            level, title = heading.groups()
            title = re.sub(r"[ \t]+#+[ \t]*$", "", title)
            match = TASK.fullmatch(title) if level == "###" else None
            if _looks_like_task_heading(title) and not match:
                errors.append(f"Malformed OA task heading: {title}")
            task = (*match.groups(), []) if match else None
        elif heading and _looks_like_task_heading(heading[2]):
            errors.append(f"OA tasks require a level-three heading: {heading[2]}")
        elif task is not None:
            task[2].append(line)
    if task is not None:
        yield task


def _evidence_values(lines: list[str], name: str) -> list[str]:
    field = re.compile(FIELD_PREFIX + rf"\*\*{name}:\*\*[ \t]*(.*?)[ \t]*$")
    return [match[1].strip().strip("`") for line in lines if (match := field.fullmatch(line))]


def _has_evidence(values: list[str], pattern: str) -> bool:
    return (
        len(values) == 1 and bool(re.fullmatch(pattern, values[0]))
        and values[0].casefold() not in {"-", "—", "n/a", "todo", "tbd", "offen"}
        and not (values[0].startswith("[") and values[0].endswith("]"))
    )


def _git(*args: str):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return subprocess.run(["git", *args], cwd=REPOSITORY_ROOT, env=env, capture_output=True, text=True)


def _missing_commit(commit: str) -> bool:
    result = _git("cat-file", "-t", commit)
    return result.returncode != 0 or result.stdout.strip() != "commit"


def validate_content(
    content: str, *, require_evidence: bool = True, verify_commits: bool = False,
) -> dict[str, int | list[str]]:
    errors = []
    seen = set()
    count = 0
    for ident, title, lines in _register_tasks(content, errors):
        count += 1
        if ident in seen:
            errors.append(f"Duplicate OA-ID found: {ident}")
        seen.add(ident)
        if not title.strip():
            errors.append(f"Missing title for {ident}")

        fields = []
        for line in lines:
            if re.match(FIELD_PREFIX + r"\*\*(?:Kategorie|Status):\*\*", line):
                fields.extend(
                    match[1].strip()
                    for part in re.split(r"\s+·\s+", line)
                    if (match := STATUS.fullmatch(part))
                )
        if len(fields) != 1:
            errors.append(f"{ident}: expected exactly one status field.")
            continue
        value = re.fullmatch(r"`([A-Z_]+)`", fields[0])
        if not value or value[1] not in VALID_STATUSES:
            errors.append(f"Invalid status value: {fields[0].strip('`')} ({ident})")
            continue
        if value[1] == "NOT_APPLICABLE" and not _has_evidence(_evidence_values(lines, "Begründung"), r".+"):
            errors.append(f"{ident}: NOT_APPLICABLE requires one valid Begründung field.")
        if require_evidence and value[1] == "DONE_VERIFIED":
            for name, pattern in EVIDENCE_FIELDS.items():
                values = _evidence_values(lines, name)
                if not _has_evidence(values, pattern):
                    errors.append(f"{ident}: DONE_VERIFIED requires a valid {name} field.")
                elif name == "Commit" and verify_commits and _missing_commit(values[0]):
                    hint = ""
                    if _git("rev-parse", "--is-shallow-repository").stdout.strip() == "true":
                        hint = " Fetch the Git history before validating this shallow checkout."
                    errors.append(f"{ident}: evidence commit is unavailable in the repository: {values[0]}.{hint}")

    if not count:
        errors.append("No OA task blocks found.")
    return {"total_tasks_found": count, "unique_ids": len(seen), "errors_count": len(errors), "errors": errors}


def validate_master_file(path: str | Path, *, verify_commits: bool | None = None) -> dict[str, int | list[str]]:
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Expected a regular register file: {path}")
    if verify_commits is None:
        verify_commits = path.resolve() == master_path().resolve()
    return validate_content(path.read_text(encoding="utf-8-sig"), verify_commits=verify_commits)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", nargs="?")
    parser.add_argument("--verify-commits", action="store_true", default=None, help="Resolve evidence SHAs in the STEPS Git repository")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable validation report")
    args = parser.parse_args()
    try:
        path = Path(args.register) if args.register else master_path()
        result = validate_master_file(path, verify_commits=args.verify_commits)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    if args.json:
        print(json.dumps(result))
    else:
        print("Register structure and declared evidence:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    if result["errors_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
