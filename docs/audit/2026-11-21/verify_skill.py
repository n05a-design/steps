"""Read-only repository audit with deliberately changed copies in isolated directories."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path.cwd()
SKILL = ROOT / ".agents/skills/steps-knowledge-curation/scripts"
REFERENCE = SKILL / "check_reference_ids.py"
PROGRESSIONS = Path("knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md")
BASELINE = Path("knowledge/research/REFERENCE_IDENTITY_BASELINE.json")
MIRROR = Path("tests/golden_cases/golden_reference_cases.json")


def run(script, *args, cwd=ROOT):
    result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                            cwd=cwd, text=True, capture_output=True)
    return {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def reference_check(repo, *args):
    result = run(REFERENCE, "--repo-root", repo, "--json", *args)
    return {"exit": result["exit"], **json.loads(result["stdout"])}


def main():
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(SKILL))
    from scripts.verify_reference_integrity import verify_integrity
    from validate_register import validate_content
    from backup_knowledge import backup_master, restore_master

    result = {}
    with TemporaryDirectory(prefix="steps-curation-audit-") as folder:
        repo = Path(folder)
        for domain in ["decisions", "knowledge", "tests"]:
            shutil.copytree(ROOT / domain, repo / domain, ignore=shutil.ignore_patterns("__pycache__"))
        result["canonical_reference_control"] = reference_check(repo)
        original = (repo / PROGRESSIONS).read_text()
        rows = original.splitlines(keepends=True)
        first = next(i for i, text in enumerate(rows) if text.startswith("| `PROG-001`"))
        cells = rows[first].split("|")
        old_harmony, old_chords = cells[3:5]
        cells[3:5] = [" I – I – I – I ", " C – C – C – C "]
        rows[first] = "|".join(cells)
        (repo / PROGRESSIONS).write_text("".join(rows))
        result["changed_progression"] = {
            "id": "PROG-001", "original": [old_harmony.strip(), old_chords.strip()],
            "mutated": ["I – I – I – I", "C – C – C – C"],
            "skill": reference_check(repo),
            "repository_gate": verify_integrity(repo),
        }
        rows = original.splitlines(keepends=True)
        (repo / PROGRESSIONS).write_text("".join(rows[:first + 1] + [rows[first]] + rows[first + 1:]))
        result["duplicate_progression_id"] = reference_check(repo)
        (repo / PROGRESSIONS).write_text(original)
        result["canonical_repository_gate"] = verify_integrity(repo)
        result["missing_baseline"] = reference_check(repo, "--baseline", repo / "nonexistent.json")
        result["missing_baseline_default_output"] = run(
            REFERENCE, "--repo-root", repo, "--baseline", repo / "nonexistent.json")
        (repo / MIRROR).unlink()
        result["missing_test_mirror"] = reference_check(repo)
        small = repo / "sample"
        small.mkdir()
        register = small / "OFFENE_ARBEITSAUFFORDERUNGEN.md"
        control = "### OA-0001: Erster Auftrag\n* **Status:** `OPEN`\n"
        invalid = control + "\n### OA-10000: Fehlerhafter Auftrag\n* **Status:** `UNKNOWN`\n"
        register.write_text(invalid)
        result["register_control"] = validate_content(control)
        result["ignored_malformed_task"] = run(SKILL / "validate_register.py", register)
        snapshot = backup_master(register)
        register.write_text(control)
        restored = restore_master(snapshot["backup"], register)
        result["restore_accepts_malformed_task"] = {"status": restored["status"],
                                                    "malformed_task_recovered": register.read_text() == invalid,
                                                    "previous_backup_exists": Path(restored["previous_backup"]).is_file()}
        document = small / "intake.txt"
        document.write_text("The documentation must be tested.\nThe documentation must first be tested.\n")
        result["extractor_word_order"] = run(SKILL / "extract_instructions.py", document, small)
        data = small / "resource.txt"
        data.write_text("Synthetic source\n")
        result["hash_source_control"] = run(SKILL / "check_source.py", data, small)
        copy = small / "copy.txt"
        copy.write_bytes(data.read_bytes())
        result["detect_duplicates_control"] = run(SKILL / "detect_duplicates.py", data, small)
    result["adapter_documented_example"] = run(
        "-c", 'from src.steps.knowledge import KnowledgeAdapter; a = KnowledgeAdapter(); '
        'r = a.query("ii-V-I", convention="INT"); print(r.found); print(r.explanation); '
        'print([(s.title, s.locator) for s in r.sources])')
    from src.steps.knowledge import KnowledgeAdapter
    adapter = KnowledgeAdapter()
    cases = [("", "INT"), ("  ", "DE"), ("dimension", "INT"),
             ("doo-wop", "INT"), ("axis", "INT"), ("ii-V-I", "INT"),
             ("ii-V-I", "DE"), ("Bdim7", "INT"), ("bVII", "DE")]
    result["adapter_retrieval"] = []
    for query, convention in cases:
        answer = adapter.query(query, convention=convention)
        result["adapter_retrieval"].append({
            "query": query, "convention": convention, "found": answer.found,
            "status": answer.status, "explanation": answer.explanation,
            "claim_ids": [claim.claim_id for claim in answer.claims],
            "source_ids": [source.source_id for source in answer.sources],
            "alternatives": answer.alternatives,
        })
    index = json.loads((ROOT / "skills/steps-knowledge/index.json").read_text())
    progression_cells = {}
    for line in (ROOT / PROGRESSIONS).read_text().splitlines():
        cells = [cell.strip().strip("`") for cell in line.split("|")]
        if len(cells) > 5 and cells[1].startswith("PROG-"):
            progression_cells[cells[1]] = dict(name=cells[2], degrees=cells[3], example=cells[4])
    result["index_alignment"] = {
        key: {"indexed": entry, "catalog": progression_cells.get(entry.get("prog_id"))}
        for key, entry in index["concepts"].items()
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
