"""Inventory the formal coverage of STEPS knowledge collections."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from unicodedata import normalize
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import run_knowledge_benchmark as benchmark
from scripts.verify_reference_integrity import extract_markdown_table_definitions, verify_integrity
from src.steps.progression import list_progressions, resolve_roman_degree, reviewed
from src.steps.theory import CHORD_TEMPLATES, MusicTheoryError, parse_chord

KNOWLEDGE = ROOT / "knowledge"
SOURCES = KNOWLEDGE / "sources"
CONCEPTS = KNOWLEDGE / "concepts"
MATRIX = KNOWLEDGE / "benchmark/COVERAGE.csv"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def duplicates(rows, field):
    return {key for key, count in Counter(row[field] for row in rows).items() if count > 1}


def table(path, pattern, columns):
    rows, issues = extract_markdown_table_definitions(path, pattern, columns)
    if issues:
        raise ValueError("\n".join(issues))
    return {ident: (line, fields) for ident, line, fields in rows}


def comparable(chord):
    return int(chord.root.pitch_class), chord.theoretical_intervals, int((chord.bass or chord.root).pitch_class)


def audit():
    records = []

    def add(area, ident, formal, result="OFFEN", note=""):
        records.append({"Bereich": area, "ID": ident, "Formal": formal, "Fachlich": result, "Befund": note})

    tracked = {
        normalize("NFC", path) for path in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode("utf-8").split("\0") if path
    }
    examples, claims = reviewed._candidates()
    results = benchmark.run(benchmark.load_cases(), examples, claims, {})
    by_case = {r["id"]: r for r in results}

    product = reviewed._sources()
    used = {citation.source_id for claim in claims.values() for citation in claim.citations}
    for ident, entry in sorted(product.items()):
        url = urlsplit(entry.get("url", ""))
        valid = bool(entry.get("title") and url.scheme == "https" and url.hostname
                     and entry.get("rights_status") == "approved")
        add("Produktquellen", ident, "OK" if valid else "BEFUND", note=(
            "Konkrete Fundstelle im Pilotkandidaten. Menschliche Quellenabnahme offen."
            if ident in used else "Derzeit kein Pilotverweis."
        ))

    # The historical file combines two metadata layouts. Inspect entry boundaries
    # and top-level fields without treating this scan as general YAML validation.
    historic_text = (SOURCES / "curated_sources_registry.yaml").read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^- id:\s*", historic_text)[1:]
    historic_ids = [block.splitlines()[0].strip(' "\'') for block in blocks]
    for ident, block in zip(historic_ids, blocks, strict=True):
        valid = historic_ids.count(ident) == 1 and bool(re.fullmatch(r"SRC-\d{4}|SRC-\d{3}", ident)) and bool(
            re.search(r"(?m)^  title:\s+\S", block)
        )
        add("Historisches Quellenregister", ident, "OK" if valid else "BEFUND",
            note="ID und Titelfeld geprüft. Zugänglichkeit, genaue Fundstelle und Rechte offen.")

    claim_rows = read_csv(benchmark.CLAIMS)
    duplicate_claims = duplicates(claim_rows, "claim_id")
    for row in claim_rows:
        ident, source = row["claim_id"], row["source_id"]
        issues = []
        if ident in duplicate_claims or not re.fullmatch(r"CLAIM-\d{3}", ident):
            issues.append("ID ungültig oder doppelt")
        if source not in historic_ids:
            issues.append(f"unbekannte Quelle {source}")
        if not row["citation_reference"].strip() or row["validation_status"] == "PLACEHOLDER":
            issues.append("Fundstelle fehlt oder Platzhalter")
        if not all(row.get(field, "").strip() for field in ("claim_text", "domain_id", "evidence_class")):
            issues.append("Pflichtangaben fehlen")
        checks = [r for r in results if r["method"] == "claim_sample" and r["content"] == ident]
        depth = checks[0]["status"] if checks else "OFFEN"
        add("Forschungsclaims", ident, "BEFUND" if issues else "OK", depth,
            "; ".join([*issues, f"Registerstatus {row['validation_status']}"]))

    progression_path = CONCEPTS / "progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md"
    drum_path = CONCEPTS / "styles/DRUM_GROOVE_REFERENCE_LIBRARY.md"
    piano_path = benchmark.PIANO
    progs = table(progression_path, r"PROG-\d{3}", 6)
    drums = table(drum_path, r"PAT-\d{3}", 7)
    pianos = table(piano_path, r"P\d{2}", 5)
    integrity = verify_integrity(str(ROOT))
    if integrity["errors"]:
        raise ValueError("\n".join(integrity["errors"]))

    domains = {f"M{i:02}" for i in range(1, 13)}
    endpoints = progs.keys() | drums.keys() | pianos.keys() | domains
    for row in read_csv(KNOWLEDGE / "relations/MUSIC_CONCEPT_RELATIONS.csv"):
        unresolved = [row[field] for field in ("source_id", "target_id") if row[field] not in endpoints]
        notes = "Keine direkte Quellen-/Claim-ID in der Relationszeile."
        if unresolved:
            notes += " Endpunktdefinition im kanonischen Knotenbestand offen: " + ", ".join(unresolved)
        add("Graphrelationen", row["relation_id"], "BEFUND", note=notes)

    template_checks = {"maj7", "m7"}
    for quality, template in CHORD_TEMPLATES.items():
        root_symbol = "C"
        aliases = [quality, *template["aliases"]]
        invalid = []
        for alias in dict.fromkeys(aliases):
            try:
                chord = parse_chord(root_symbol + alias, "INT")
            except MusicTheoryError:
                invalid.append(alias)
            else:
                if chord.theoretical_intervals != tuple(template["theoretical"]):
                    invalid.append(alias)
        add("Akkordvorlagen", quality or "Dur (leer)", "BEFUND" if invalid else "OK",
            "PASS" if quality in template_checks and by_case["KB-M04-MAJOR-MINOR"]["status"] == "PASS" else "OFFEN",
            "Parser gegen eigenes Rezept; ohne externen Beleg je Alias." + (f" Abweichung: {invalid!r}." if invalid else ""))

    for progression in list_progressions():
        ident, key = progression.prog_id, progression.default_key
        degree = progression.roman_numerals
        written = progression.chords_str
        source_line, row = progs[ident]
        primary = lambda value: value.split("`")[1] if "`" in value else value
        form = "OK" if primary(row[2]) == degree and primary(row[3]) == written else "BEFUND"
        add("Progressionskatalog", ident, form, note=(
            f"Markdown-Zeile {source_line}. Quellenangaben sind Bibliografie ohne konkrete Fundstellen."
        ))
        for i, (token, symbol) in enumerate(zip(degree.split(" - "), written.split(" - "), strict=True), 1):
            try:
                parsed = resolve_roman_degree(token, key.removesuffix("m"), key.endswith("m"), convention="INT")
                consistent = comparable(parsed) == comparable(parse_chord(symbol, "INT"))
                observation = f"{token} → {parsed.symbol}; Katalog {symbol}"
            except MusicTheoryError as exc:
                consistent, observation = False, str(exc)
            case = by_case.get(f"KB-{ident}-{i:02}") or by_case.get(f"{ident}-HARMONY")
            add("Progressionspositionen", f"{ident}:{i}", "OK" if consistent else "BEFUND",
                case["status"] if case else "OFFEN", observation)

    for area, rows in (("Klaviermodule", pianos), ("Drum-/Groove-Katalog", drums)):
        for ident, (line, _) in rows.items():
            checks = [r for r in results if r["content"] == ident]
            add(area, ident, "OK", checks[0]["status"] if checks else "OFFEN",
                f"Markdown-Zeile {line}; redaktionelle und spielpraktische Abnahme offen.")

    approvals = reviewed._approval_records(claims)
    verified = set()
    for ident, claim in claims.items():
        try:
            if ident in approvals:
                reviewed._approve(claim, approvals[ident])
                verified.add(ident)
        except reviewed.PublicationError:
            pass
        status = by_case[ident]["status"]
        add("Pilot-Lernaussagen", ident, "OK", status,
            "Freigabe eingetragen." if ident in verified else "Menschliche Freigabe ausstehend.")
    for ident, required in reviewed.REQUIRED_CLAIMS.items():
        all_ids = (reviewed.NOTATION, *required)
        status = "PASS" if all(by_case[i]["status"] == "PASS" for i in all_ids) else "FAIL"
        add("App-Pilotbeispiele", ident, "OK", status,
            f"{sum(i in verified for i in all_ids)} von {len(all_ids)} zugehörigen Fachfreigaben eingetragen.")
    for r in results:
        if r["scope"] == "sample":
            add("Lehrtext-/Themenstichproben", r["id"], "OK", r["status"], r["basis"])
        if r["scope"] == "coach":
            add("Harmony-Coach-Fragen", r["id"], "OK", r["status"], "Rubrik vorhanden; keine reale Antwort bewertet.")

    manifest = read_csv(ROOT / "archive/manifests/ARCHIVE_MANIFEST.csv")
    moved = {normalize("NFC", r["source_path"]): normalize("NFC", r["target_path"]) for r in manifest}
    source_inventory = read_csv(SOURCES / "MUSIC_SOURCE_REVIEW_PROGRESS.csv")
    duplicate_file_ids = duplicates(source_inventory, "file_id")
    for row in source_inventory:
        path = normalize("NFC", row["path"])
        target = moved.get(path)
        status = "Direkter Pfad" if path in tracked else "Archivpfad" if target in tracked else "Pfad fehlt im Checkout"
        if row["file_id"] in duplicate_file_ids or not re.fullmatch(r"[a-f0-9]{64}", row["sha256"]):
            status += ", ID oder Hashfeld auffällig"
        add("Historisches Dateiregister", row["file_id"],
            "OK" if status in {"Direkter Pfad", "Archivpfad"} else "BEFUND",
            note=f"{status}: {target if status == 'Archivpfad' else path}")

    for area, prefix in (("Forschungsbestand", "research/"), ("Archivbestand", "archive/"),
                         ("Quellenarchiv", "source_archive/"), ("Legacy-Wissensbestand", "knowledge/legacy/"),
                         ("Historische Wissensaudits", "knowledge/research/")):
        for path in sorted(p for p in tracked if p.startswith(prefix)):
            add(area, path, "INVENTAR", note="Versionierter Pfad; keine fachliche Einzelabnahme.")
    return records


def render_csv(rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def summarize(records):
    result = []
    for area in dict.fromkeys(row["Bereich"] for row in records):
        rows = [row for row in records if row["Bereich"] == area]
        f = Counter(r["Formal"] for r in rows)
        k = Counter(r["Fachlich"] for r in rows)
        result.append({"Bereich": area, "Gesamt": len(rows), "Formal_geprüft": f["OK"] + f["BEFUND"],
                       "Formale_Befunde": f["BEFUND"], "Inventar_only": f["INVENTAR"],
                       "Fachlich_untersucht": k["PASS"] + k["FAIL"], "Fachlich_bestätigt": k["PASS"],
                       "Fachlich_beanstandet": k["FAIL"], "Fachlich_offen": k["OFFEN"] + k["PENDING"]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()
    records = audit()
    result = render_csv(summarize(records))
    if args.details:
        args.details.write_text(render_csv(records), encoding="utf-8")
    if args.write:
        MATRIX.write_text(result, encoding="utf-8")
    elif MATRIX.read_text(encoding="utf-8") != result:
        raise SystemExit("Coverage.csv ist veraltet. Mit --write aktualisieren.")
    print(result, end="")


if __name__ == "__main__":
    main()
