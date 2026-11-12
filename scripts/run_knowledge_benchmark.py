"""Run the versioned music benchmark and report blocks for individual contents."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from math import isclose
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.progression import get_progression, resolve_roman_degree
from src.steps.progression import reviewed
from src.steps.theory import MusicTheoryError, midi_to_frequency, parse_chord, parse_spelling

DIR = ROOT / "knowledge/benchmark"
PIANO = ROOT / "knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md"
CLAIMS = ROOT / "knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv"
STATUSES = ("PASS", "FAIL", "PENDING")


def require(condition, observed):
    if not condition:
        raise AssertionError(observed)
    return observed


def load_cases():
    data = json.loads((DIR / "cases.json").read_text(encoding="utf-8"))
    cases = data["cases"]
    if data["schema_version"] != 1 or not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Invalid benchmark version or duplicate case ID.")
    for case in cases:
        if (not all(case[field].strip() for field in ("id", "content", "question", "basis", "method"))
                or not re.fullmatch(r"M(?:0[1-9]|1[0-2])", case["domain"])
                or case["scope"] not in {"pilot", "catalog", "sample", "coach"}
                or not isinstance(case["variants"], list) or type(case["mandatory"]) is not bool
                or "expected" not in case):
            raise ValueError(f"Incomplete benchmark case {case['id']}.")
    return cases


def pitch_set(chord):
    return sorted(chord.pitch_class_set)


def evaluate(case, examples, claims, coach):
    method, expected, data = case["method"], case["expected"], case["input"]
    if method == "manual":
        return "PENDING", "Redaktionelle Prüfung ausstehend."
    if method == "coach":
        grade = coach.get(case["id"])
        if grade is None:
            return "PENDING", "Keine Coach-Antwort mit menschlicher Bewertung erfasst."
        if not all(isinstance(grade.get(key), str) and grade[key].strip()
                   for key in ("reviewer", "response", "source_evidence")):
            return "FAIL", "Bewertung benötigt Person, Antwort und Nachweis zur Quellenprüfung."
        if grade.get("criteria") != {criterion: True for criterion in expected} or grade.get("sources_verified") is not True:
            return "FAIL", "Mindestens ein Pflichtbestandteil oder die Quellenprüfung fehlt."
        return "PASS", f"Rubrik erfüllt laut dokumentierter Bewertung von {grade['reviewer']}."

    if case["scope"] == "pilot":
        require(case["id"] in claims, "Pilot claim ID fehlt im Produktdatensatz.")
    if method == "notation":
        actual = [[parse_spelling(note, convention).midi_number for note, convention in zip(pair, ("DE", "INT"), strict=True)]
                  for pair in data["notes"]]
        require(actual == [[midi, midi] for midi in expected], actual)
    elif method == "harmony":
        row = examples[case["content"]]
        degrees, symbols = row["roman"].split(" - "), row["chords"].split(" - ")
        actual = {"key": row["default_key"], "stages": degrees, "chords": symbols}
        require(actual == {"key": "C", "stages": expected["stages"], "chords": expected["chords"]}, actual)
        written = [pitch_set(parse_chord(s, "INT")) for s in symbols]
        resolved = [pitch_set(resolve_roman_degree(d, "C", convention="INT")) for d in degrees]
        actual.update(written=written, resolved=resolved)
        require(written == resolved == expected["pitch_classes"], actual)
    elif method == "relative_minor":
        written = examples[case["content"]]["chords"].split(" - ")
        minor = [resolve_roman_degree(degree, "A", is_minor_key=True, convention="INT").symbol
                 for degree in expected["minor_stages"]]
        actual = {"written": written, "relative_minor": minor, "note": "Rechnerische Lesart. Höreindruck bleibt kontextabhängig."}
        require(written == minor == expected["chords"], actual)
    elif method == "voice":
        path = claims[case["id"]].voice_path
        midi = [parse_spelling(note, "DE").midi_number for _, note in path]
        steps = [b - a for a, b in zip(midi, midi[1:])]
        chords = examples[case["content"]]["chords"].split(" - ")
        membership = [m % 12 in parse_chord(chords[i], "INT").pitch_class_set
                      for (i, _), m in zip(path, midi, strict=True)]
        actual = {"path": [list(point) for point in path], "midi": midi, "delta": steps}
        require(actual == expected and all(membership), {**actual, "chord_membership": membership})
    elif method == "catalog_position":
        progression = get_progression(case["content"])
        i = data["position"] - 1
        degree = progression.roman_numerals.split(" - ")[i]
        written = progression.chords_str.split(" - ")[i]
        key = progression.default_key
        try:
            resolved = resolve_roman_degree(degree, key.removesuffix("m"), key.endswith("m"), convention="INT")
        except MusicTheoryError as exc:
            raise AssertionError(f"{degree} → {exc}; Symbolspalte {written}") from None
        target = pitch_set(parse_chord(expected, "INT"))
        actual = {"stage": degree, "resolved": resolved.symbol, "written": written}
        require(pitch_set(resolved) == pitch_set(parse_chord(written, "INT")) == target, actual)
    elif method == "piano":
        row = next(line for line in PIANO.read_text(encoding="utf-8").splitlines()
                   if line.startswith(f"| `{data['id']}`"))
        if data["id"] == "P12":
            upper = pitch_set(parse_chord("Fmaj7", "INT"))
            total = pitch_set(parse_chord("Dm9", "INT"))
            actual = {"upper": upper, "total": total, "row": row}
            require(len(upper) == 4 and total == expected["notes"] and "dreiklang" not in row.lower(), actual)
        else:
            midi = [parse_spelling(note, "INT").midi_number for note in ("C#3", "C3", "B2", "A2", "G2")]
            delta = [b - a for a, b in zip(midi, midi[1:])]
            actual = {"delta": delta, "row": row}
            require(delta == expected and ("diatonisch" in row.lower() or "ganzton" in row.lower()), actual)
    elif method == "frequency":
        actual = [midi_to_frequency(note) for note in data["midi"]]
        require(all(isclose(a, b, abs_tol=1e-5) for a, b in zip(actual, expected, strict=True)), actual)
    elif method == "enharmonic":
        notes = [parse_spelling(note, "INT") for note in ("C#4", "Db4")]
        actual = [*(note.midi_number for note in notes), *(note.render("INT") for note in notes)]
        require(actual == expected, actual)
    elif method == "distance":
        a, b = [parse_spelling(note, "INT").midi_number for note in data["notes"]]
        actual = require(b - a == expected, b - a)
    elif method == "intervals":
        actual = [list(parse_chord(s, "INT").theoretical_intervals) for s in data["symbols"]]
        require(actual == expected, actual)
    elif method == "degree":
        actual = resolve_roman_degree(data["degree"], data["key"], convention="INT").symbol
        require(actual == expected, actual)
    elif method == "claim_sample":
        with CLAIMS.open(encoding="utf-8-sig", newline="") as source:
            row = next(r for r in csv.DictReader(source) if r["claim_id"] == data["id"])
        if data["check"] == "clave":
            actual = [int(value) for value in re.search(r"\[([\d, ]+)\]", row["musical_example"])[1].split(",")]
        elif data["check"] == "swing_source":
            citation = row["citation_reference"].replace(" ", "").replace("–", "-").lower()
            actual = expected if (
                expected["doi"] in citation or all(
                    part.replace(" ", "").replace("–", "-").lower() in citation
                    for part in (expected["journal"], expected["volume_issue"], expected["pages"])
                )
            ) else row["citation_reference"]
        else:
            actual = "decimal" in row["claim_text"].lower() and "(-2 to +2)" not in row["claim_text"]
        require(actual == expected, {"actual": actual, "claim": row["claim_text"]})
    else:
        raise ValueError(f"Unknown method {method}.")
    return "PASS", actual


def review_sheet(cases, claims):
    manifest = subprocess.check_output(
        (sys.executable, "-B", "-m", "src.steps.progression.reviewed", "--review-manifest"),
        cwd=ROOT, text=True,
    )
    records = reviewed._approval_records(claims)
    states = {parts[0]: parts[2] for line in manifest.splitlines()[1:] if (parts := line.split("\t"))}
    by_id = {case["id"]: case for case in cases if case["scope"] == "pilot"}
    if claims.keys() != by_id.keys() or claims.keys() != states.keys():
        raise ValueError("Die Abnahmeliste und der Pilotbenchmark müssen dieselben Claim-IDs enthalten.")
    count = sum(status == "APPROVAL_RECORDED" for status in states.values())
    lines = ["# Pilot · fachliche Abnahmeliste", "", f"**Dokumentierte Freigaben im Register: {count} von {len(claims)}.**", "",
             "Je Aussage im Draft-PR entscheiden: freigegeben, Korrektur erforderlich oder Beleg fehlt.",
             "Für jede Freigabe Claim-ID und vollständigen Fassungsfingerabdruck angeben.",
             "Bei Korrektur oder fehlendem Beleg bitte die konkrete Passage benennen.", ""]
    for ident, claim in claims.items():
        case = by_id[ident]
        state = {"PENDING": "Ausstehend", "INVALID_APPROVAL": "Erneute Prüfung erforderlich",
                 "APPROVAL_RECORDED": "Freigabe eingetragen"}[states[ident]]
        lines += [f"## {ident}", "", f"- Stand · {state}", f"- Art · `{claim.kind}`",
                  f"- Fassung · `{claim.fingerprint}`", f"- Wortlaut · {claim.text}",
                  f"- Gültigkeitsbereich · {claim.scope}", f"- Gegencheck · {claim.countercheck}",
                  *(f"- Fundstelle · [{ref.title}](<{ref.url}>) · {ref.locator}" for ref in claim.citations),
                  f"- Prüffrage · {case['question']}",
                  f"- Sollantwort · `{json.dumps(case['expected'], ensure_ascii=False)}`",
                  f"- Herleitung · {case['basis']}"]
        if states[ident] == "APPROVAL_RECORDED":
            record = records[ident]
            lines.append(f"- Entscheidung · [{record['reviewer']}]({record['evidence_url']}) · {record['reviewed_on']}")
        lines.append("")
    return "\n".join(lines)


def run(cases, examples, claims, coach):
    results = []
    for case in cases:
        try:
            status, observed = evaluate(case, examples, claims, coach)
        except (AssertionError, KeyError, TypeError, ValueError, MusicTheoryError, StopIteration) as exc:
            status, observed = "FAIL", exc.args[0] if exc.args else str(type(exc).__name__)
        results.append({**case, "status": status, "observed": observed})
    return results


def markdown(report):
    lines = ["# STEPS-Wissensbenchmark · Ergebnis", "",
             f"Commit `{report['git_sha']}` · Arbeitsbaum {'mit Änderungen' if report['dirty'] else 'sauber'}.", "",
             "| Pflichtinhalt | Freigabesperre |", "|---|---|",
             *(f"| {content} | {', '.join(ids)} |" for content, ids in report["blocks"].items()), "",
             "| Fall | Bereich | Inhalt | Ergebnis | Beobachtung |", "|---|---|---|---|---|"]
    for r in report["results"]:
        observed = str(r["observed"]).replace("|", r"\|").replace("\n", " ")
        lines.append(f"| {r['id']} | {r['domain']} | {r['content']} | {r['status']} | {observed} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("all", "pilot", "catalog", "sample", "coach"), default="all")
    parser.add_argument("--content")
    parser.add_argument("--coach-assessment", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    sheet = parser.add_mutually_exclusive_group()
    sheet.add_argument("--review-sheet", type=Path)
    sheet.add_argument("--check-review-sheet", type=Path)
    args = parser.parse_args()
    cases = load_cases()
    examples, claims = reviewed._candidates()
    if args.review_sheet or args.check_review_sheet:
        content = review_sheet(cases, claims)
        if args.review_sheet:
            args.review_sheet.write_text(content, encoding="utf-8")
        elif not args.check_review_sheet.exists() or args.check_review_sheet.read_text(encoding="utf-8") != content:
            raise SystemExit("Pilot-Abnahmeliste ist veraltet. Mit --review-sheet aktualisieren.")
        return 0
    coach = json.loads(args.coach_assessment.read_text(encoding="utf-8")) if args.coach_assessment else {}
    pilot_ids = {case["id"] for case in cases if case["scope"] == "pilot" and case["mandatory"]}
    if pilot_ids != claims.keys():
        parser.error("Pflichtfälle des Pilotbenchmarks müssen alle Pilot-Claims abdecken.")
    selected = [case for case in cases if args.scope in {"all", case["scope"]}
                and (args.content is None or args.content == case["content"])]
    if not selected:
        parser.error("Keine Benchmarkfälle in dieser Auswahl.")
    results = run(selected, examples, claims, coach)
    blocks = {}
    for result in results:
        if result["mandatory"] and result["status"] != "PASS":
            blocks.setdefault(result["content"], []).append(result["id"])
    counts = Counter(r["status"] for r in results)
    report = {"schema_version": 1, "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "dirty": bool(subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT)),
              "scope": args.scope, "counts": {s: counts[s] for s in STATUSES}, "blocks": blocks, "results": results}
    if args.json_out:
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(markdown(report), encoding="utf-8")
    print(" · ".join(f"{status} {counts[status]}" for status in STATUSES))
    for content, ids in blocks.items():
        print(f"BLOCKED {content}: {', '.join(ids)}")
    return int(bool(blocks))


if __name__ == "__main__":
    raise SystemExit(main())
