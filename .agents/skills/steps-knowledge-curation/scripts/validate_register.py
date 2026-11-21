"""Validate the structure and declared evidence of the canonical register."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from register_paths import REPOSITORY_ROOT, master_path


VALID_STATUSES = {
    "OPEN", "IN_PROGRESS", "BLOCKED", "OWNER_DECISION_REQUIRED",
    "DONE_UNVERIFIED", "DONE_VERIFIED", "SUPERSEDED", "NOT_APPLICABLE",
}
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$")
TASK = re.compile(r"(OA-[0-9]{4}):[ \t]*(.*)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)
FIELD_PREFIX = r"^ {0,3}(?:[-*+][ \t]+)?"
COMMIT_HASH = r"(?!0{40}(?:0{24})?$)[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?"
STATUS = re.compile(FIELD_PREFIX + r"\*\*Status:\*\*[ \t]*(.*)$")
EVIDENCE_FIELDS = {
    "Commit": COMMIT_HASH,
    "Prüfung": r".+",
    "Abnahmebeleg": r".+",
    "Abnahmekriterien": r".+",
}


def _register_lines(content: str, errors: list[str]):
    fence = None
    in_comment = False
    for line in content.splitlines():
        opening = FENCE.match(line)
        if fence:
            if (opening and opening[1].startswith(fence[0])
                    and len(opening[1]) >= len(fence) and not opening[2].strip()):
                fence = None
            continue
        if not in_comment and opening:
            fence = opening[1]
            continue
        if in_comment:
            _, closing, line = line.partition("-->")
            if not closing:
                continue
            in_comment = False
        for comment in COMMENT.finditer(line):
            if not comment[0].endswith("-->"):
                in_comment = True
        yield COMMENT.sub("", line)
    if fence or in_comment:
        errors.append("Unclosed fenced block or HTML comment in task register.")


def _register_tasks(content: str, errors: list[str]):
    task = None
    for line in _register_lines(content, errors):
        heading = HEADING.fullmatch(line)
        if heading and len(heading[1]) <= 3:
            if task is not None:
                yield task
            level, title = heading.groups()
            title = re.sub(r"[ \t]+#+[ \t]*$", "", title)
            match = TASK.fullmatch(title) if level == "###" else None
            if title.upper().startswith("OA-") and not match:
                errors.append(f"Malformed OA task heading: {title}")
            task = (*match.groups(), []) if match else None
        elif heading and heading[2].upper().startswith("OA-"):
            errors.append(f"OA tasks require a level-three heading: {heading[2]}")
        elif task is not None:
            task[2].append(line)
    if task is not None:
        yield task


def _evidence_values(lines: list[str], name: str) -> list[str]:
    field = re.compile(FIELD_PREFIX + rf"\*\*{name}:\*\*[ \t]*(.*?)[ \t]*$")
    return [match[1].strip().strip("`") for line in lines if (match := field.fullmatch(line))]


def _missing_commit(commit: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-t", commit], cwd=REPOSITORY_ROOT, capture_output=True, text=True,
    )
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
        if require_evidence and value[1] == "DONE_VERIFIED":
            for name, pattern in EVIDENCE_FIELDS.items():
                values = _evidence_values(lines, name)
                if (
                    len(values) != 1 or not re.fullmatch(pattern, values[0])
                    or values[0].casefold() in {"-", "—", "n/a", "todo", "tbd", "offen"}
                    or (values[0].startswith("[") and values[0].endswith("]"))
                ):
                    errors.append(f"{ident}: DONE_VERIFIED requires a valid {name} field.")
                elif name == "Commit" and verify_commits and _missing_commit(values[0]):
                    errors.append(f"{ident}: evidence commit is unavailable in the repository: {values[0]}.")

    if not count:
        errors.append("No OA task blocks found.")
    return {"total_tasks_found": count, "unique_ids": len(seen), "errors_count": len(errors), "errors": errors}


def validate_master_file(path: str | Path, *, verify_commits: bool = False) -> dict[str, int | list[str]]:
    return validate_content(Path(path).read_text(encoding="utf-8-sig"), verify_commits=verify_commits)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", nargs="?")
    parser.add_argument("--verify-commits", action="store_true", help="Resolve evidence SHAs in the STEPS Git repository")
    args = parser.parse_args()
    try:
        path = Path(args.register) if args.register else master_path()
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Expected a regular register file: {path}")
        result = validate_master_file(
            path, verify_commits=args.verify_commits or path.resolve() == master_path().resolve(),
        )
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print("Register structure and declared evidence:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    if result["errors_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
