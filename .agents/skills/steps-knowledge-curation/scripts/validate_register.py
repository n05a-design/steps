"""Validate the structure and declared evidence of the canonical register."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from register_paths import master_path


VALID_STATUSES = {
    "OPEN", "IN_PROGRESS", "BLOCKED", "OWNER_DECISION_REQUIRED",
    "DONE_UNVERIFIED", "DONE_VERIFIED", "SUPERSEDED", "NOT_APPLICABLE",
}
TASK = re.compile(r"^### (OA-\d{4}):[ \t]*(.*)$")
STATUS = re.compile(r"^\s*(?:[-*+]\s+)?\*\*Status:\*\*[ \t]*(.*)$")
EVIDENCE_FIELDS = {
    "Commit": r"[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?",
    "Prüfung": r".+",
    "Abnahmebeleg": r".+",
    "Abnahmekriterien": r".+",
}


def _register_tasks(content: str):
    task = None
    fence = None
    for line in content.splitlines():
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if (
                opening and opening[1].startswith(fence[0])
                and len(opening[1]) >= len(fence) and not opening[2].strip()
            ):
                fence = None
            continue
        if opening:
            fence = opening[1]
            continue
        heading = re.match(r"^ {0,3}#{1,3}(?:\s|$)", line)
        if heading:
            if task is not None:
                yield task
            match = TASK.fullmatch(line)
            task = (*match.groups(), []) if match else None
        elif task is not None:
            task[2].append(line)
    if task is not None:
        yield task


def validate_content(content: str, *, require_evidence: bool = True) -> dict[str, int | list[str]]:
    errors = []
    seen = set()
    count = 0
    for ident, title, lines in _register_tasks(content):
        count += 1
        if ident in seen:
            errors.append(f"Duplicate OA-ID found: {ident}")
        seen.add(ident)
        if not title.strip():
            errors.append(f"Missing title for {ident}")

        fields = []
        for line in lines:
            if re.match(r"^\s*(?:[-*+]\s+)?\*\*(?:Kategorie|Status):\*\*", line):
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
                field = re.compile(rf"^\s*(?:[-*+]\s+)?\*\*{name}:\*\*\s*(.*?)\s*$")
                values = [match[1].strip().strip("`") for line in lines if (match := field.fullmatch(line))]
                if (
                    len(values) != 1 or not re.fullmatch(pattern, values[0])
                    or values[0].casefold() in {"-", "—", "n/a", "todo", "tbd", "offen"}
                    or (values[0].startswith("[") and values[0].endswith("]"))
                ):
                    errors.append(f"{ident}: DONE_VERIFIED requires a valid {name} field.")

    if not count:
        errors.append("No OA task blocks found.")
    return {"total_tasks_found": count, "unique_ids": len(seen), "errors_count": len(errors), "errors": errors}


def validate_master_file(path: str | Path) -> dict[str, int | list[str]]:
    return validate_content(Path(path).read_text(encoding="utf-8-sig"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", nargs="?")
    args = parser.parse_args()
    try:
        result = validate_master_file(master_path() if args.register is None else args.register)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print("Master File Validation Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    if result["errors_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
