"""Inventory the formal coverage of STEPS knowledge collections."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import date
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

from scripts import render_reviewed_progressions as renderer
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


def format_node_evidence(rows):
    repeated = duplicates(rows, "node_id")
    evidence = {}
    for row in rows:
        ident = row["node_id"]
        source = urlsplit(row["source_url"])
        if (ident in repeated or not re.fullmatch(r"[A-Z][A-Z0-9_]+", ident)
                or source.scheme != "https" or not source.hostname
                or not row["definition"].strip() or not row["locator"].strip()):
            raise ValueError(f"Ungültiger Quellenbeleg für Graphknoten {ident}.")
        evidence[ident] = f"{row['source_url']} ({row['locator']})"
    return evidence


def table(path, pattern, columns):
    rows, issues = extract_markdown_table_definitions(path, pattern, columns)
    if issues:
        raise ValueError("\n".join(issues))
    return {ident: (line, fields) for ident, line, fields in rows}


def comparable(chord):
    return int(chord.root.pitch_class), chord.theoretical_intervals, int((chord.bass or chord.root).pitch_class)


NEXT = {
    "Produktquellen": "Originalseite und konkrete Passage mit der Aussage abgleichen.",
    "Historisches Quellenregister": "Edition oder Originaldatei lokalisieren und bibliografisch bestätigen.",
    "Forschungsclaims": "Originalfundstelle öffnen und Wortlaut, Modellgrenze und Gegenbeispiel prüfen.",
    "Graphrelationen": "Endpunkte und Semantik mit einer konkreten Quellen- oder Claim-ID belegen.",
    "Akkordvorlagen": "Unabhängige Intervallwerte für Qualität, Alias und Voicing festlegen.",
    "Progressionskatalog": "Markdown und Runtime vergleichen, Stilkontext und Quellenfundstelle abnehmen.",
    "Progressionspositionen": "Grundton, Akkordqualität und Bass gegen eine unabhängige Sollposition prüfen.",
    "Klaviermodule": "Noten, Handverteilung, Tempo und Fingersatz im Spielversuch bestätigen.",
    "Drum-/Groove-Katalog": "Takt, Onsets und Stilkontext notieren und im Hörversuch abnehmen.",
    "Pilot-Lernaussagen": "Die konkrete Aussage mit ihrem Fingerabdruck fachkundig im Draft abnehmen.",
    "App-Pilotbeispiele": "Alle zugehörigen Claims freigeben, danach App und Lernmaterial neu abgleichen.",
    "Generierte Lerntexte": "Menschliche Freigaben dokumentieren, Renderer ausführen und Datenversion vergleichen.",
    "Golden-Referenzfälle": "Unabhängiges Soll und erreichten Produktionspfad je Fall nachweisen.",
    "Historisches Dateiregister": "Archivpfad oder Herkunftsbeleg ermitteln, Original und Rechte prüfen.",
    "Historische strukturierte Dateien": "Bei Übernahme zuerst Zeilen oder Objekte zum Original und zur Quellenversion zuordnen.",
}


def yaml_parser():
    try:
        import yaml
    except ImportError:
        raise SystemExit("Audit-Abhängigkeit installieren: python -m pip install -r knowledge/benchmark/requirements.txt") from None

    class UniqueSafeLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node):
        loader.flatten_mapping(node)
        pairs = loader.construct_pairs(node, deep=True)
        return reviewed._unique_keys(pairs)

    UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    return lambda text: yaml.load(text, Loader=UniqueSafeLoader), yaml.YAMLError


def structured_file(path, read_yaml, yaml_error):
    try:
        content = path.read_text(encoding="utf-8-sig")
        if path.suffix.lower() == ".json":
            json.loads(content, object_pairs_hook=reviewed._unique_keys)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            read_yaml(content)
        else:
            header = next((line for line in content.splitlines() if line.strip()), "")
            dialect = csv.Sniffer().sniff(header, delimiters=",;\t")
            rows = [r for r in csv.reader(io.StringIO(content), delimiter=dialect.delimiter, strict=True) if r]
            if rows and any(len(row) != len(rows[0]) for row in rows):
                return "Abweichende Spaltenzahl in mindestens einem Datensatz."
    except (OSError, ValueError, csv.Error, TypeError, reviewed.PublicationError, yaml_error) as exc:
        return str(exc)
    return ""

def audit():
    records = []

    def add(area, ident, formal, result="OFFEN", note="", *, complete=False, next_step=None):
        depth = "VOLLSTÄNDIG" if complete else "STICHPROBE" if result in {"PASS", "FAIL"} else "NICHT_GEPRÜFT"
        if complete and formal == "OK" and result == "PASS":
            followup = ""
        else:
            followup = next_step or NEXT.get(area, "Vor Übernahme Provenienz und konkrete Aussagen einzeln prüfen.")
        records.append({"Bereich": area, "ID": ident, "Formal": formal, "Fachlich": result,
                        "Prüftiefe": depth, "Befund": note, "Nächster_Prüfschritt": followup})

    tracked = {
        normalize("NFC", path) for path in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode("utf-8").split("\0") if path
    }
    read_yaml, yaml_error = yaml_parser()
    examples, claims = reviewed._candidates()
    results = benchmark.run([case for case in benchmark.load_cases() if case["scope"] != "publication"], examples, claims, {})
    by_case = {r["id"]: r for r in results}

    product = reviewed._sources()
    used = {citation.source_id for claim in claims.values() for citation in claim.citations}
    for ident, entry in sorted(product.items()):
        url = urlsplit(entry.get("url", ""))
        retrieved = entry.get("retrieved_at", "")
        try:
            valid_date = date.fromisoformat(retrieved).isoformat() == retrieved
        except (ValueError, TypeError):
            valid_date = False
        valid = bool(entry.get("title") and url.scheme == "https" and url.hostname
                     and entry.get("rights_status") == "approved" and entry.get("kind") == "website"
                     and entry.get("usage_notes") and valid_date)
        add("Produktquellen", ident, "OK" if valid else "BEFUND", note=(
            "Konkrete Fundstelle im Pilotkandidaten. Menschliche Quellenabnahme offen."
            if ident in used else "Derzeit kein Pilotverweis."
        ))

    historical = read_yaml((SOURCES / "curated_sources_registry.yaml").read_text(encoding="utf-8"))
    if historical.get("schema_version") != 1 or not isinstance(historical.get("sources"), list):
        raise ValueError("Ungültiges historisches Quellenregister.")
    entries = historical["sources"]
    historical_duplicates = duplicates(entries, "id")
    historic_ids = {row["id"] for row in entries}
    filenames = {Path(path).name for path in tracked}
    tracked_dirs = {parent.as_posix() for path in tracked for parent in Path(path).parents}
    for row in entries:
        ident = row["id"]
        missing = []
        if ident in historical_duplicates or not re.fullmatch(r"SRC-\d{3,4}", ident):
            missing.append("ungültige oder doppelte ID")
        if row.get("provenance_status") == "SOURCE_REVIEW_REQUIRED":
            missing.append("Historische Bibliografie und Fundstelle unbestätigt")
        if not row.get("title"):
            missing.append("Titel fehlt")
        if "filename" in row:
            local = normalize("NFC", row["filename"].rstrip("/"))
            if local not in tracked and local not in tracked_dirs and local not in filenames:
                missing.append(f"Originalpfad nicht auflösbar: {local}")
            if not all(row.get(key) for key in ("format", "rights_class", "status")):
                missing.append("Metadaten zum Dateieintrag fehlen")
        elif not all(row.get(key) for key in ("authors", "evidence_class", "assigned_domains")):
            missing.append("Bibliografische Pflichtfelder fehlen")
        add("Historisches Quellenregister", ident, "BEFUND" if missing else "OK",
            note="; ".join(missing) or "Schema und vorhandene lokale Verweise geprüft. Original und Rechte offen.")

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
        if (not all(row.get(field, "").strip() for field in ("claim_text", "evidence_class"))
                or not re.fullmatch(r"M(?:0[1-9]|1[0-2])", row.get("domain_id", ""))
                or row["validation_status"] not in {"PLACEHOLDER", "REVIEW_REQUIRED", "SOURCE_REVIEW_REQUIRED"}):
            issues.append("Pflichtangaben fehlen")
        checks = [
            r for r in results
            if r["method"] in {"claim_sample", "guide_tone_paths"} and r["content"] == ident
        ]
        depth = checks[0]["status"] if checks else "OFFEN"
        add("Forschungsclaims", ident, "BEFUND" if issues else "OK", depth,
            "; ".join([*issues, f"Registerstatus {row['validation_status']}"]),
            next_step=checks[0]["next_step"] if checks and checks[0]["next_step"] else None)

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
    # These aliases are documented in knowledge/relations/FABLE_GRAPH_REVIEW.md.
    aliases = {"PROG_024": "PROG-024", "PROG_025": "PROG-025"}
    format_nodes = format_node_evidence(read_csv(KNOWLEDGE / "relations/FORMAT_NODE_EVIDENCE.csv"))
    if (endpoints | aliases.keys()) & format_nodes.keys():
        raise ValueError("Formatknoten überschneidet sich mit einer kanonischen ID oder einem Alias.")
    for row in read_csv(KNOWLEDGE / "relations/MUSIC_CONCEPT_RELATIONS.csv"):
        terms = (row["source_id"], row["target_id"])
        unresolved = [term for term in terms if aliases.get(term, term) not in endpoints and term not in format_nodes]
        notes = f"Registerstatus {row['validation_status']}. Keine direkte Quellen-/Claim-ID in der Relationszeile."
        resolved_aliases = [f"{term} → {aliases[term]}" for term in terms
                            if term in aliases and aliases[term] in endpoints]
        if resolved_aliases:
            notes += " Historische Aliasauflösung: " + ", ".join(resolved_aliases)
        node_sources = [f"{term}: {format_nodes[term]}" for term in terms if term in format_nodes]
        if node_sources:
            notes += " Quellenbelegte Endpunkte: " + " · ".join(node_sources) + "."
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

    progressions = list_progressions()
    if progs.keys() != {progression.prog_id for progression in progressions}:
        raise ValueError("Runtime- und Markdown-Katalog enthalten unterschiedliche Progressions-IDs.")
    for progression in progressions:
        ident, key = progression.prog_id, progression.default_key
        degree = progression.roman_numerals
        written = progression.chords_str
        source_line, row = progs[ident]
        primary = lambda value: value.split("`")[1] if "`" in value else value
        form = "OK" if row[5].strip() and primary(row[2]) == degree and primary(row[3]) == written else "BEFUND"
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
                case["status"] if case else "OFFEN", observation, next_step=case["next_step"] if case else None)

    for area, rows in (("Klaviermodule", pianos), ("Drum-/Groove-Katalog", drums)):
        for ident, (line, _) in rows.items():
            checks = [r for r in results if r["content"] == ident]
            add(area, ident, "OK", checks[0]["status"] if checks else "OFFEN",
                f"Markdown-Zeile {line}; redaktionelle und spielpraktische Abnahme offen.",
                next_step=next((r["next_step"] for r in checks if r["next_step"]), None))

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
            "Freigabe eingetragen." if ident in verified else "Menschliche Freigabe ausstehend.", complete=ident in verified)
    for ident, required in reviewed.REQUIRED_CLAIMS.items():
        all_ids = (reviewed.NOTATION, *required)
        status = "PASS" if all(by_case[i]["status"] == "PASS" for i in all_ids) else "FAIL"
        add("App-Pilotbeispiele", ident, "OK", status,
            f"{sum(i in verified for i in all_ids)} von {len(all_ids)} zugehörigen Fachfreigaben eingetragen.",
            complete=all(i in verified for i in all_ids))
    markdown = renderer.OUTPUT.read_text(encoding="utf-8")
    try:
        generated = renderer.render()
    except reviewed.PublicationError as exc:
        pending = len(verified) < len(claims) and "Fachfreigabe ausstehend" in markdown
        add("Generierte Lerntexte", renderer.OUTPUT.name, "OK" if pending else "BEFUND", "PENDING", str(exc))
    else:
        matches = markdown == generated
        add("Generierte Lerntexte", renderer.OUTPUT.name, "OK" if matches else "BEFUND",
            "PASS" if matches else "FAIL", "Vergleich mit dem Renderer und dem App-Katalog.",
            complete=matches)
    golden = json.loads((KNOWLEDGE / "research/golden_cases/golden_reference_cases.json").read_text(encoding="utf-8"))
    for row in golden:
        add("Golden-Referenzfälle", row["case_id"], "OK", note=(
            f"{row['test_class']}; Identitätscheck bestanden, eigenständige fachliche Einzelabnahme offen."
        ))
    for r in results:
        if r["scope"] == "sample":
            add("Lehrtext-/Themenstichproben", r["id"], "OK", r["status"], r["basis"], next_step=r["next_step"])
        if r["scope"] == "coach":
            add("Harmony-Coach-Fragen", r["id"], "OK", r["status"], "Rubrik vorhanden; keine reale Antwort bewertet.", next_step=r["next_step"])

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
    for path in sorted(tracked):
        if (path.startswith(("archive/", "source_archive/", "research/", "knowledge/legacy/", "knowledge/research/"))
                and Path(path).suffix.lower() in {".csv", ".json", ".yaml", ".yml"}):
            issue = structured_file(ROOT / path, read_yaml, yaml_error)
            add("Historische strukturierte Dateien", path, "BEFUND" if issue else "OK",
                note=issue or "Syntax bzw. Spalten geprüft. Querverweise und fachlicher Inhalt bleiben offen.")
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
        depth = Counter(r["Prüftiefe"] for r in rows)
        result.append({"Bereich": area, "Gesamt": len(rows), "Formal_geprüft": f["OK"] + f["BEFUND"],
                       "Formale_Befunde": f["BEFUND"], "Inventar_only": f["INVENTAR"],
                       "Fachlich_untersucht": k["PASS"] + k["FAIL"], "Fachlich_bestätigt": k["PASS"],
                       "Fachlich_beanstandet": k["FAIL"], "Fachlich_offen": k["OFFEN"] + k["PENDING"],
                       "Fachlich_vollständig": depth["VOLLSTÄNDIG"], "Fachlich_Stichprobe": depth["STICHPROBE"],
                       "Fachlich_nicht_geprüft": depth["NICHT_GEPRÜFT"]})
    return result


def area_report(summary):
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT))
    lines = [
        "# STEPS · Inventur und Prüftiefe je Bereich", "",
        f"Git-Stand `{sha}` · Arbeitsbaum {'mit Änderungen' if dirty else 'sauber'}.", "",
        "Die Detail-CSV enthält pro Eintrag Befund, Prüftiefe und nächsten Schritt.", "",
        "| Bereich | Anzahl | Formal bestanden | Formale Befunde | Nur inventarisiert | Fachlich vollständig | Stichprobe | Fachlich ungeprüft |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        formal_pass = row["Formal_geprüft"] - row["Formale_Befunde"]
        lines.append(
            f"| {row['Bereich']} | {row['Gesamt']} | {formal_pass} | {row['Formale_Befunde']} | {row['Inventar_only']} "
            f"| {row['Fachlich_vollständig']} | {row['Fachlich_Stichprobe']} | {row['Fachlich_nicht_geprüft']} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--details", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--gate-content")
    args = parser.parse_args()
    records = audit()
    summary = summarize(records)
    result = render_csv(summary)
    if args.report:
        args.report.write_text(area_report(summary), encoding="utf-8")
    if args.details:
        args.details.write_text(render_csv(records), encoding="utf-8")
    if args.write:
        MATRIX.write_text(result, encoding="utf-8")
    elif MATRIX.read_text(encoding="utf-8") != result:
        raise SystemExit("Coverage.csv ist veraltet. Mit --write aktualisieren.")
    print(result, end="")
    if args.gate_content:
        matches = [row for row in records
                   if row["ID"] == args.gate_content or row["ID"].startswith(args.gate_content + ":")]
        if not matches:
            parser.error("Inhalt in der Abdeckungsmatrix nicht gefunden.")
        for row in matches:
            if row["Formal"] != "OK":
                print(f"BLOCKED {row['ID']} · {row['Bereich']} · {row['Nächster_Prüfschritt']}")
                raise SystemExit(1)


if __name__ == "__main__":
    main()
