"""Run the versioned music benchmark and report blocks for individual contents."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from hashlib import sha256
import json
from math import isclose
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.progression import analyze_progression_voice_leading, get_progression, resolve_roman_degree
from src.steps.progression import reviewed
from src.steps.theory import MusicTheoryError, Voicing, midi_to_frequency, parse_chord, parse_spelling
from src.steps.theory import make_drop2_voicing
from scripts import graph_corrections
from scripts import verify_historical_ontology

DIR = ROOT / "knowledge/benchmark"
PROGRESSIONS = ROOT / "knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md"
DRUMS = ROOT / "knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md"
LATIN = DRUMS.with_name("GENRE_RESEARCH_LATIN.md")
PIANO = ROOT / "knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md"
CLAIMS = ROOT / "knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv"
RELATIONS = ROOT / "knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv"
STATUSES = ("PASS", "FAIL", "PENDING")
SCOPES = ("pilot", "publication", "catalog", "sample", "coach", "api", "backlog")
PUBLICATION_TESTS = {
    "test_approved_fixture_publishes_same_version_and_content",
    "test_unknown_source_blocks_every_entry",
    "test_falsified_lesson_cannot_be_regenerated_with_previous_approval",
}

API_TESTS = {
    "test_sus_chords_respect_explicit_notation",
    "test_chord_tensions_require_balanced_parentheses",
    "test_voicing_invert_rotates_voices_above_original_top",
}


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
        if (not all(case[field].strip() for field in ("id", "content", "question", "basis", "method", "next_step"))
                or not re.fullmatch(r"M(?:0[1-9]|1[0-2])", case["domain"])
                or case["scope"] not in SCOPES
                or not isinstance(case["variants"], list) or type(case["mandatory"]) is not bool
                or "expected" not in case):
            raise ValueError(f"Incomplete benchmark case {case['id']}.")
    return cases


def pitch_set(chord):
    return sorted(chord.pitch_class_set)


def piano_exercise(module_id):
    document = PIANO.read_text(encoding="utf-8")
    module = document.partition(f"### Modul {module_id}:")[2].partition("\n### ")[0]
    rows = re.findall(r"^- `([^`]+)` · links `([^`]+)` · rechts `([^`]+)`$", module, re.MULTILINE)
    return [
        [label, *([parse_spelling(note, "INT").midi_number for note in hand.split()] for hand in (left, right))]
        for label, left, right in rows
    ]


def evaluate_piano_exercise(case, expected):
    module_id = case["content"]
    rows = piano_exercise(module_id)
    actual = {"voicings": rows}
    require(rows == expected["voicings"], actual)
    if module_id == "P08":
        _, left, right = rows[0]
        close = sorted(left + right)
        _, left, right = rows[1]
        drop2 = sorted(left + right)
        right_span = max(right) - min(right)
        _, left, right = rows[2]
        chord = parse_chord("Dm7", "INT")
        actual.update(
            octave_drop=close[-2] - drop2[0],
            right_span=right_span,
            distributed_hand_spans=[max(hand) - min(hand) for hand in (left, right)],
            bass=drop2[0],
        )
        require(sorted(left + right) == drop2 and close[-1] == drop2[-1]
                and sorted([close[-2] - 12, *close[:-2], close[-1]]) == drop2
                and tuple(close) == chord.to_voicing(4, "CLOSE").notes
                and tuple(drop2) == chord.to_voicing(4, "DROP2").notes, actual)
    elif module_id == "P05":
        for symbol, left, right in rows:
            chord = parse_chord(symbol, "INT")
            _, third, _, seventh = chord.theoretical_intervals
            bass = int(chord.root.pitch_class)
            require(left[0] % 12 == bass
                    and {note % 12 for note in right} == {(bass + third) % 12, (bass + seventh) % 12}, actual)
        actual["motions"] = [
            [b - a for a, b in zip(first[2], second[2], strict=True)]
            for first, second in zip(rows, rows[1:])
        ]
    elif module_id == "P06":
        for symbol, left, right in rows:
            chord = parse_chord(symbol, "INT")
            intervals = chord.theoretical_intervals[1:]
            require(left[0] % 12 == chord.root.pitch_class
                    and tuple(note - left[0] - 12 for note in right) == intervals, actual)
    else:
        raise ValueError(f"Unbekannte Klavierübung {module_id}.")
    return require(actual == expected, actual)


def case_fingerprint(case):
    value = json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(value.encode("utf-8")).hexdigest()


def evaluate_manual(case, grade):
    if grade is None:
        return "PENDING", "Hör-, Spiel- oder Fachabnahme ausstehend."
    if not isinstance(grade, dict):
        return "FAIL", "Ein Abnahme-Eintrag muss ein Objekt sein."
    if (grade.get("reviewer") == "" and grade.get("evidence") == "" and grade.get("observations") == ""
            and grade.get("criteria") == dict.fromkeys(case["expected"], None)):
        return "PENDING", "Hör-, Spiel- oder Fachabnahme ausstehend."
    if grade.get("fingerprint") != case_fingerprint(case):
        return "PENDING", "Manuelle Abnahme bezieht sich auf eine andere Fassung."
    if not all(isinstance(grade.get(key), str) and grade[key].strip()
               for key in ("reviewer", "evidence", "observations")):
        return "FAIL", "Person, konkreter Nachweis und Beobachtungen sind erforderlich."
    if not isinstance(grade.get("git_sha"), str) or not re.fullmatch(r"[a-f0-9]{40}", grade["git_sha"]):
        return "FAIL", "Der manuell geprüfte Git-SHA fehlt."
    current = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if grade["git_sha"] != current:
        return "PENDING", "Die manuelle Abnahme dokumentiert einen anderen Git-Stand."
    if grade.get("criteria") != dict.fromkeys(case["expected"], True):
        return "FAIL", "Mindestens ein manuelles Pflichtkriterium fehlt oder ist beanstandet."
    return "PASS", f"{grade['reviewer']} · {grade['evidence']} · {grade['observations']}"


def latin_timing(pattern, voice):
    header = "### Notierte Ereignisse und Zeitbasis"
    table = LATIN.read_text(encoding="utf-8").partition(header)[2].partition("\n## ")[0]
    rows = []
    for line in table.splitlines():
        if line.startswith(f"| {pattern} | {voice} |"):
            _, _, meter, tempo, ppq, bar, positions = (field.strip() for field in line.strip("|").split("|"))
            rows.append((meter, tempo, int(ppq), int(bar), [int(x) for x in positions.split(",")]))
    require(rows, f"Kein Zeitraster für {pattern} · {voice}.")
    meter, tempo, ppq, _, _ = rows[0]
    beats, denominator = map(int, meter.split("/"))
    bpm_text, beat_unit = tempo.split()
    bpm = int(bpm_text)
    catalog = DRUMS.read_text(encoding="utf-8")
    row = next(line for line in catalog.splitlines() if line.startswith(f"| `{pattern}` |"))
    _, _, catalog_tempo, catalog_meter, *_ = (field.strip() for field in row.strip("|").split("|"))
    require(catalog_tempo == f"{bpm} BPM" and re.match(re.escape(meter) + r"[, ]", catalog_meter)
            and f"({beat_unit})" in catalog_meter, "Tempo oder Metrum weicht vom Drum-Katalog ab.")
    require(beats > 0 and denominator in {2, 4} and bpm > 0
            and ppq > 0 and ppq % 4 == 0, "Ungültige Zeitbasis.")
    require(beat_unit == {2: "Halbe", 4: "Viertel"}[denominator], "Tempoeinheit passt nicht zum Metrum.")
    bar_positions = beats * (16 // denominator)
    ticks_per_bar = bar_positions * (ppq // 4)
    onsets = []
    for index, (row_meter, row_tempo, row_ppq, bar, positions) in enumerate(rows, 1):
        require((row_meter, row_tempo, row_ppq, bar) == (meter, tempo, ppq, index),
                "Uneinheitliche Zeitbasis oder unstetige Taktnummer.")
        require(positions == sorted(set(positions)) and all(0 <= x < bar_positions for x in positions),
                "Sechzehntelposition liegt außerhalb des Takts oder ist doppelt.")
        onsets.extend((bar - 1) * ticks_per_bar + x * (ppq // 4) for x in positions)
    return {"meter": [beats, denominator], "bpm": bpm, "beat_unit": beat_unit,
            "ppq": ppq, "bars": len(rows), "ticks_per_bar": ticks_per_bar,
            "onsets": onsets, "bar_seconds": round(beats * 60 / bpm, 6)}


def evaluate(case, examples, claims, coach, manual):
    method, expected, data = case["method"], case["expected"], case["input"]
    if method == "manual":
        return evaluate_manual(case, manual.get(case["id"]))
    if method == "coach":
        grade = coach.get(case["id"])
        if grade is None:
            return "PENDING", "Keine Coach-Antwort mit menschlicher Bewertung erfasst."
        if not isinstance(grade, dict):
            return "FAIL", "Ein Coach-Eintrag muss ein Objekt sein."
        if (grade.get("reviewer") == "" and grade.get("sources_verified") is None
                and grade.get("criteria") == dict.fromkeys(expected, None)):
            return "PENDING", "Keine Coach-Antwort mit menschlicher Bewertung erfasst."
        if grade.get("fingerprint") != case_fingerprint(case):
            return "PENDING", "Coach-Bewertung bezieht sich auf eine andere Fassung."
        if not all(isinstance(grade.get(key), str) and grade[key].strip()
                   for key in ("reviewer", "response", "source_evidence", "model", "skill_revision", "run_evidence")):
            return "FAIL", "Bewertung benötigt Person, Antwort, Quellenprüfung und Modell-/Skill-Version mit Laufbeleg."
        if grade.get("criteria") != {criterion: True for criterion in expected} or grade.get("sources_verified") is not True:
            return "FAIL", "Mindestens ein Pflichtbestandteil oder die Quellenprüfung fehlt."
        return "PASS", {key: grade[key] for key in ("reviewer", "model", "skill_revision", "run_evidence", "source_evidence")}

    if case["scope"] == "pilot":
        require(case["id"] in claims, "Pilot claim ID fehlt im Produktdatensatz.")
    if method in {"publication_test", "api_test"}:
        test = data["test"]
        target, allowed = (
            ("tests.test_pilot_publication.PilotPublicationTests", PUBLICATION_TESTS)
            if method == "publication_test" else
            ("tests.test_theory_core.TestTheoryCoreChordEngine", API_TESTS)
        )
        if test not in allowed:
            raise ValueError(f"Unknown benchmark regression test {test}.")
        command = (sys.executable, "-B", "-m", "unittest", f"{target}.{test}")
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
        actual = require(completed.returncode == 0, completed.stderr.strip())
    elif method == "api_contract":
        probe = data["probe"]
        if probe == "auto":
            actual = {}
            for symbol in ("Cis", "Es", "Es7"):
                for locale in ("DE", "AUTO"):
                    try:
                        actual[f"{symbol}/{locale}"] = parse_chord(symbol, locale).symbol
                    except MusicTheoryError as exc:
                        actual[f"{symbol}/{locale}"] = str(exc)
        elif probe == "analysis":
            voicing = Voicing((48, 52, 55))
            actual = {
                "empty": sorted(analyze_progression_voice_leading([])),
                "one": sorted(analyze_progression_voice_leading([voicing])),
                "two": sorted(analyze_progression_voice_leading([voicing, voicing])),
            }
        elif probe == "compound":
            actual = {symbol: list(parse_chord(symbol).theoretical_intervals) for symbol in ("Cadd9", "C7(#11)", "C9")}
        elif probe == "drop2":
            chord = parse_chord("C13")
            actual = {layout: sorted({note % 12 for note in chord.to_voicing(3, layout).notes})
                      for layout in ("CLOSE", "DROP2")}
        else:
            raise ValueError(f"Unknown API contract probe {probe}.")
        require(actual == expected, {"actual": actual, "expected": expected})
    elif method == "degree_controls":
        chords = [resolve_roman_degree(degree, data["key"], convention="INT") for degree in data["degrees"]]
        actual = [[chord.symbol, pitch_set(chord)] for chord in chords]
        require(actual == expected, actual)
    elif method == "piano_control":
        if data["type"] == "upper_structure":
            upper = pitch_set(parse_chord("Fmaj7", "INT"))
            actual = [upper, sorted({*upper, 2})]
            require(actual[1] == pitch_set(parse_chord("Dm9", "INT")), actual)
        else:
            midi = [parse_spelling(note, "INT").midi_number for note in ("C#3", "C3", "B2", "A2", "G2")]
            actual = [b - a for a, b in zip(midi, midi[1:])]
        require(actual == expected, actual)
    elif method == "notation":
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
        target = expected["pitch_classes"]
        actual = {"stage": degree, "resolved": resolved.symbol, "written": written}
        require(resolved.symbol == written == expected["symbol"]
                and pitch_set(resolved) == pitch_set(parse_chord(written, "INT")) == target, actual)
    elif method == "piano":
        document = PIANO.read_text(encoding="utf-8")
        row = next(line for line in document.splitlines() if line.startswith(f"| `{data['id']}`"))
        if data["id"] == "P12":
            upper = pitch_set(parse_chord("Fmaj7", "INT"))
            bass = parse_spelling("D3", "INT").midi_number % 12
            total = sorted({*upper, bass})
            actual = {"upper": upper, "total": total, "bass": bass, "row": row}
            require(upper == expected["upper_notes"] and bass == expected["bass"]
                    and total == expected["notes"] == pitch_set(parse_chord("Dm9", "INT"))
                    and "vierklang" in row.lower() and "grundton" in row.lower(), actual)
        else:
            midi = [parse_spelling(note, "INT").midi_number for note in ("C#3", "C3", "B2", "A2", "G2")]
            delta = [b - a for a, b in zip(midi, midi[1:])]
            progression = get_progression("PROG-026")
            stage = progression.roman_numerals.split(" - ")[4]
            symbol = progression.chords_str.split(" - ")[4]
            dominant = resolve_roman_degree(stage, progression.default_key, convention="INT")
            catalog_row = next(line for line in PROGRESSIONS.read_text(encoding="utf-8").splitlines()
                               if line.startswith("| `PROG-026`"))
            actual = {"delta": delta, "dominant": dominant.symbol, "bass": int(dominant.bass.pitch_class),
                      "dominant_tones": pitch_set(dominant), "row": row, "catalog": catalog_row}
            require({key: actual[key] for key in expected} == expected
                    and symbol == expected["dominant"]
                    and progression.roman_numerals in catalog_row and progression.chords_str in catalog_row
                    and r"V^7_{4/3}" in row and "ganzton" in row.lower()
                    and r"$D^7/A$" in document, actual)
    elif method == "piano_backdoor":
        module = PIANO.read_text(encoding="utf-8").partition("### Modul P18:")[2].partition("### Modul ")[0]
        rows = re.findall(r"^- `([^`]+)` · `([^`]+)` · links `([^`]+)` · rechts `([^`]+)`$", module, re.MULTILINE)
        stages, symbols, bass_notes, upper_notes = zip(*rows, strict=True)
        progression = get_progression(data["progression"])
        require(tuple(progression.chords_str.split(" - ")) == symbols, "Die notierten Akkorde weichen von der Progression ab.")
        resolved = [resolve_roman_degree(stage, progression.default_key, convention="INT").symbol for stage in stages]
        require(resolved == list(symbols), "Die notierten Stufen ergeben andere Akkorde.")
        bass = [parse_spelling(note, "INT").midi_number for note in bass_notes]
        right = [[parse_spelling(note, "INT").midi_number for note in notes.split()] for notes in upper_notes]
        parsed = [parse_chord(symbol, "INT") for symbol in symbols]
        require(all(note % 12 == chord.root.pitch_class for note, chord in zip(bass, parsed, strict=True)),
                "Der notierte Bass enthält einen fremden Grundton.")
        require(all(len(upper) == 3 and [note, *upper] == sorted({note, *upper}) for note, upper in zip(bass, right, strict=True)),
                "Der Bass muss unter drei aufsteigenden rechten Stimmen liegen.")
        played = [{note % 12 for note in [low, *high]} for low, high in zip(bass, right, strict=True)]
        chord_tones = [chord.pitch_class_set for chord in parsed]
        actual = {
            "symbols": list(symbols),
            "bass": bass,
            "right": right,
            "added_pitch_classes": [sorted(a - b) for a, b in zip(played, chord_tones, strict=True)],
            "omitted_pitch_classes": [sorted(b - a) for a, b in zip(played, chord_tones, strict=True)],
            "resolution": [b - a for a, b in zip(right[-2], right[-1], strict=True)],
        }
        require(actual == expected, actual)
    elif method == "piano_upper_structure":
        module = PIANO.read_text(encoding="utf-8").partition("### Modul P16:")[2].partition("### Modul ")[0]
        hands = re.search(r"^- Linke Hand: `([^`]+)`\n- Rechte Hand: `([^`]+)`$", module, re.MULTILINE)
        require(hands is not None, "Die notierte P16-Handverteilung fehlt.")
        left, right = (
            [parse_spelling(note, "INT").midi_number for note in hand.split()]
            for hand in hands.groups()
        )
        bass = min(left + right)
        actual = {
            "bass": bass % 12,
            "left": [note % 12 for note in left],
            "right": [note % 12 for note in right],
            "upper_intervals": [note - bass for note in right],
            "omitted_fifth": all((note - bass) % 12 != 7 for note in left + right),
        }
        require(actual == expected, actual)
    elif method == "piano_exercise":
        actual = evaluate_piano_exercise(case, expected)
    elif method == "compound_meter":
        catalog = DRUMS.read_text(encoding="utf-8")
        row = next(line for line in catalog.splitlines() if line.startswith(f"| `{case['content']}` |"))
        module = catalog.partition(f"\n## {case['content']} ·")[2].partition("\n## ")[0]
        pattern = re.search(r"\b([X.]{6,}) auf ", row)
        timing = re.search(
            r"`([X.]+)` umfasst (\w+) Achtel\. Bei (\d+) PPQ dauert\s+"
            r"ein Achtel (\d+) Ticks und die gesamte Folge (\d+) Ticks", module,
        )
        tempo = re.search(r"punktierte Viertel = (\d+) BPM", module)
        require(pattern is not None and timing is not None and tempo is not None, "Puls-, Tempo- oder PPQ-Angabe fehlt.")
        bell, pulse_count, ppq_text, pulse_text, total_text = timing.groups()
        ppq, pulse, bpm, total = int(ppq_text), int(pulse_text), int(tempo[1]), int(total_text)
        require(pattern[1] == bell and f"| {bpm} BPM |" in row
                and ppq == pulse * 2 and total == len(bell) * pulse,
                "Katalog, Zählvariante und Zeitbasis stimmen nicht überein.")
        require(pulse_count == "zwölf" and len(bell) == 12, "Die Glockenfolge muss zwölf Achtel umfassen.")

        def ticks(values):
            return [int(value) for value in re.findall(r"\d+", values)]

        measures = re.findall(r"^- \*\*(?:Ein|Zwei) (\d+)/8-Takt(?:e)?\*\* mit den Grenzen ([\d, und]+)\.", module, re.MULTILINE)
        written = {numerator: ticks(boundaries) for numerator, boundaries in measures}
        require(len(measures) == len(written), "Doppelte Taktvariante.")
        actual = {
            "ppq": ppq, "bpm": bpm, "pulse_ticks": pulse,
            "bell_onsets": [index * pulse for index, event in enumerate(bell) if event == "X"],
            "beat_onsets": list(range(0, total, 3 * pulse)),
            "barlines": {count: list(range(0, total + 1, int(count) * pulse)) for count in written},
            "cycle_seconds": len(bell) / 3 * (60 / bpm),
        }
        bell_ticks = re.search(r"liegen bei ([\d, und]+) Ticks", module)
        beat_ticks = re.search(r"beginnen bei ([\d, und]+) Ticks", module)
        require(bell_ticks is not None and beat_ticks is not None
                and ticks(bell_ticks[1]) == actual["bell_onsets"] and ticks(beat_ticks[1]) == actual["beat_onsets"]
                and written == actual["barlines"] and actual == expected, actual)
    elif method == "latin_timing":
        actual = latin_timing(case["content"], data["voice"])
        require(actual == expected, actual)
    elif method == "drum_ticks":
        row = next(line for line in DRUMS.read_text(encoding="utf-8").splitlines() if line.startswith("| `PAT-026`"))
        ppq = expected["ppq"]
        onset = round((ppq // 2) * data["percent"] / 100)
        actual = {"ppq": ppq, "onset": onset, "offset": onset - ppq // 4}
        require(actual == expected and all(value in row for value in (
            "64%", f"{ppq} PPQ", f"Tick {onset}", f"+{actual['offset']} Ticks",
        )), {"calculated": actual, "row": row})
    elif method == "frequency":
        actual = [midi_to_frequency(note) for note in data["midi"]]
        require(all(isclose(a, b, abs_tol=1e-5) for a, b in zip(actual, expected, strict=True)), actual)
    elif method == "enharmonic":
        notes = [parse_spelling(note, data["convention"]) for note in data["notes"]]
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
    elif method == "guide_tone_paths":
        actual = {}
        for mode, example in data.items():
            chords = [parse_chord(symbol, "INT") for symbol in example["chords"]]
            motions = []
            for first, second, (source, target) in zip(
                chords[:-1], chords[1:], example["paths"], strict=True,
            ):
                source_note = parse_spelling(source, "INT")
                target_note = parse_spelling(target, "INT")
                require(
                    source_note.pitch_class in first.pitch_class_set
                    and target_note.pitch_class in second.pitch_class_set,
                    {"mode": mode, "source": source, "target": target, "error": "note outside chord"},
                )
                motions.append(target_note.midi_number - source_note.midi_number)
            actual[mode] = motions
        require(actual == expected, actual)
    elif method == "historical_ontology":
        actual = verify_historical_ontology.verify(ROOT)
        require(actual == expected, actual)
    elif method == "night_graph_probe":
        from scripts import graph_probes
        plan = json.loads((ROOT / 'knowledge/relations/GRAPH_AUDIT_PLAN.json').read_text(encoding='utf-8'))
        spec = next(p for p in plan['probes'] if p['id'] == data['probe_id'])
        actual = graph_probes.evaluate(spec)
        require(actual == expected, actual)
    elif method == "graph_sample":
        with RELATIONS.open(encoding="utf-8-sig", newline="") as source:
            row = next(row for row in csv.DictReader(source) if row["relation_id"] == case["content"])
        require([row[key] for key in ("source_id", "target_id", "relation_type")] == data["edge"],
                "Graphkante weicht von der geprüften Zuordnung ab.")
        if data["check"] == "mode_rotation":
            steps = data["ascending_melodic_minor"]
            start = data["degree"] - 1
            actual = steps[start:] + steps[:start]
        elif data["check"] == "drop2":
            actual = make_drop2_voicing(data["close"])
        elif data["check"] == "polychord_counterexample":
            aggregate = sorted(parse_chord("C", "INT").pitch_class_set | parse_chord("D", "INT").pitch_class_set)
            slash = sorted(parse_chord("D/C", "INT").pitch_class_set | {0})
            # The parser has no maj13(#11) alias. Build the stated theoretical
            # pitch collection explicitly from maj7 and the written extensions.
            target = sorted(parse_chord("Cmaj7", "INT").pitch_class_set
                            | {int(parse_spelling(note, "INT").pitch_class) for note in ("D5", "F#5", "A5")})
            actual = {"two_triads": aggregate, "slash_bass": slash, "target": target,
                      "missing_from_two_triads": sorted(set(target) - set(aggregate))}
            require(aggregate != target and slash != target, "Das Gegenbeispiel darf keine Tonmengenidentität bestätigen.")
        elif data["check"] == "polychord_resolution":
            document = json.loads((ROOT / "knowledge/relations/GRAPH_CORRECTIONS.json").read_text(encoding="utf-8"))
            with RELATIONS.open(encoding="utf-8-sig", newline="") as source:
                relations = list(csv.DictReader(source))
            with (ROOT / "knowledge/relations/MUSIC_NODE_EVIDENCE.csv").open(encoding="utf-8-sig", newline="") as source:
                nodes = {entry["node_id"] for entry in csv.DictReader(source)}
            proposal = graph_corrections.validate(document, relations, nodes)[case["content"]]
            aggregate = sorted(parse_chord("C", "INT").pitch_class_set | parse_chord("D", "INT").pitch_class_set)
            corrected = sorted(parse_chord("C6", "INT").pitch_class_set
                               | {int(parse_spelling(note, "INT").pitch_class) for note in ("D5", "F#5")})
            require(proposal["replacement"]["pitch_classes"] == aggregate == corrected,
                    "Der Korrekturvorschlag muss exakt den beiden Dreiklängen entsprechen.")
            actual = {"target_id": proposal["replacement"]["target_id"],
                      "pitch_classes": aggregate, "major_seventh_present": 11 in aggregate,
                      "production_use_allowed": proposal["production_use_allowed"]}
        elif data["check"] == "notation_mapping":
            note = parse_spelling(data["note"], data["convention"])
            actual = [note.midi_number, int(note.pitch_class)]
        elif data["check"] == "four_families":
            rotations = {tuple(steps[start:] + steps[:start]) for steps in data["families"] for start in range(7)}
            require(all(len(steps) == 7 and sum(steps) == 12 for steps in data["families"]), "Ungültige Skalenfamilie.")
            actual = len(rotations)
        elif data["check"] == "rootless_example":
            chord = parse_chord(data["chord"], "INT")
            notes = [parse_spelling(note, "INT") for note in data["notes"]]
            pcs = {int(note.pitch_class) for note in notes}
            require(int(chord.root.pitch_class) not in pcs and pcs <= chord.pitch_class_set,
                    "Rootless-Beispiel enthält Grundton oder akkordfremde Töne.")
            actual = [note.midi_number for note in notes]
        elif data["check"] == "swing_model":
            actual = round(data["ppq"] / 2 * data["percent"] / 100)
        elif data["check"] == "clave_model":
            ppq = data["ppq"]
            actual = [bar * 4 * ppq + position * ppq // 4
                      for bar, positions in enumerate(data["sixteenth_positions"]) for position in positions]
        elif data["check"] == "applied_dominant_example":
            progression = get_progression("PROG-024")
            actual = [resolve_roman_degree("V7/V", "C", convention="INT").symbol,
                      progression.chords_str.split(" - ")[1]]
        elif data["check"] == "cyclical_example":
            actual = get_progression("PROG-025").chords_str.split(" - ")
        else:
            raise ValueError(f"Unknown graph sample: {data['check']}.")
        require(actual == expected, actual)
    elif method == "claim_sample":
        with CLAIMS.open(encoding="utf-8-sig", newline="") as source:
            row = next(r for r in csv.DictReader(source) if r["claim_id"] == data["id"])
        if data["check"] == "clave":
            written = re.search(r"\[([\d, ]+)\]", row["musical_example"])
            require(written is not None, "Die Beispielspalte enthält keine Tickfolge.")
            ticks = [int(value) for value in written[1].split(",")]
            ppq = data["ppq"]
            actual = [bar * 4 * ppq + onset * ppq // 4
                      for bar, onsets in enumerate(data["sixteenth_positions"]) for onset in onsets]
            require(actual == ticks, {"calculated": actual, "register": ticks})
        elif data["check"] == "swing_source":
            citation = row["citation_reference"]
            match = re.search(
                r", (?P<journal>[^,]+) (?P<volume_issue>\d+\(\d+\)), "
                r"(?P<pages>\d+[–-]\d+), [^,]+, https://doi\.org/(?P<doi>[^\s,]+)",
                citation,
            )
            require(match is not None, citation)
            actual = match.groupdict()
            actual["pages"] = actual["pages"].replace("-", "–")
        elif data["check"] == "alter":
            from decimal import Decimal
            from xml.etree import ElementTree

            values = re.findall(r"<alter>[^<]+</alter>", row["musical_example"])
            actual = [
                str(value) for element in values
                if (value := Decimal(ElementTree.fromstring(element).text)) % 1
            ]
        else:
            raise ValueError(f"Unknown claim sample: {data['check']}.")
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


def assessment_template(cases, method, revision):
    """Prepare empty, version-bound forms for human assessments."""
    result = {}
    for case in cases:
        if case["method"] != method:
            continue
        entry = {
            "fingerprint": case_fingerprint(case),
            "reviewer": "",
            "criteria": dict.fromkeys(case["expected"], None),
        }
        if method == "coach":
            entry.update(response="", source_evidence="", sources_verified=None,
                         model="", skill_revision="", run_evidence="")
        else:
            entry.update(git_sha=revision, evidence="", observations="")
        result[case["id"]] = entry
    return result


def run(cases, examples, claims, coach, manual=None):
    results = []
    for case in cases:
        try:
            status, observed = evaluate(case, examples, claims, coach, manual or {})
        except (AssertionError, IndexError, KeyError, TypeError, ValueError, MusicTheoryError, StopIteration, subprocess.TimeoutExpired) as exc:
            status, observed = "FAIL", exc.args[0] if exc.args else str(type(exc).__name__)
        results.append({**case, "fingerprint": case_fingerprint(case), "status": status,
                        "observed": observed, "next_step": case["next_step"] if status != "PASS" else ""})
    return results


def markdown(report):
    lines = ["# STEPS-Wissensbenchmark · Ergebnis", "",
             f"Commit `{report['git_sha']}` · Arbeitsbaum {'mit Änderungen' if report['dirty'] else 'sauber'}.", "",
             "| Bereich | Bestanden | Fehlgeschlagen | Ungeprüft |", "|---|---:|---:|---:|"]
    for scope, totals in report["areas"].items():
        lines.append(f"| {scope} | {totals['PASS']} | {totals['FAIL']} | {totals['PENDING']} |")
    lines += ["", "| Pflichtinhalt | Freigabesperre |", "|---|---|",
              *(f"| {content} | {', '.join(ids)} |" for content, ids in report["blocks"].items()), ""]
    if report["coach_domains"]:
        lines += ["## Harmony Coach · Domänenabdeckung", "",
                  "| Domäne | Aufgaben | Antworten geprüft | Ausstehend |", "|---|---:|---:|---:|"]
        for domain, totals in report["coach_domains"].items():
            lines.append(f"| {domain} | {sum(totals.values())} | {totals['PASS'] + totals['FAIL']} | {totals['PENDING']} |")
        lines.append("")
    for scope in report["areas"]:
        lines += [f"## {scope}", "", "| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |",
                  "|---|---|---|---|---|---|"]
        for r in report["results"]:
            if r["scope"] == scope:
                observed = str(r["observed"]).replace("|", r"\|").replace("\n", " ")
                lines.append(f"| {r['id']} | {r['domain']} | {r['content']} | {r['status']} | {observed} | {r['next_step']} |")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("all", *SCOPES), default="all")
    parser.add_argument("--content")
    parser.add_argument("--coach-assessment", type=Path)
    parser.add_argument("--manual-assessment", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    sheet = parser.add_mutually_exclusive_group()
    sheet.add_argument("--review-sheet", type=Path)
    sheet.add_argument("--check-review-sheet", type=Path)
    sheet.add_argument("--coach-template", type=Path)
    sheet.add_argument("--manual-template", type=Path)
    args = parser.parse_args()
    cases = load_cases()
    selected = [case for case in cases if args.scope in {"all", case["scope"]}
                and (args.content is None or args.content == case["content"])]
    if args.coach_template or args.manual_template:
        method = "coach" if args.coach_template else "manual"
        if subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT):
            parser.error("Abnahmevorlagen benötigen einen sauberen versionierten Arbeitsbaum.")
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        template = assessment_template(selected, method, revision)
        if not template:
            parser.error("Keine Abnahmefälle für diese Vorlage ausgewählt.")
        output = args.coach_template or args.manual_template
        try:
            with output.open("x", encoding="utf-8") as stream:
                json.dump(template, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        except FileExistsError:
            parser.error(f"Vorlage existiert bereits: {output}")
        return 0
    candidate_error = None
    try:
        examples, claims = reviewed._candidates()
    except reviewed.PublicationError as exc:
        if args.review_sheet or args.check_review_sheet:
            raise SystemExit(str(exc)) from None
        examples, claims = {}, {}
        candidate_error = str(exc)
    if args.review_sheet or args.check_review_sheet:
        content = review_sheet(cases, claims)
        if args.review_sheet:
            args.review_sheet.write_text(content, encoding="utf-8")
        elif not args.check_review_sheet.exists() or args.check_review_sheet.read_text(encoding="utf-8") != content:
            raise SystemExit("Pilot-Abnahmeliste ist veraltet. Mit --review-sheet aktualisieren.")
        return 0
    coach = json.loads(args.coach_assessment.read_text(encoding="utf-8")) if args.coach_assessment else {}
    manual = json.loads(args.manual_assessment.read_text(encoding="utf-8")) if args.manual_assessment else {}
    pilot_ids = {case["id"] for case in cases if case["scope"] == "pilot" and case["mandatory"]}
    if candidate_error is None and pilot_ids != claims.keys():
        parser.error("Pflichtfälle des Pilotbenchmarks müssen alle Pilot-Claims abdecken.")

    if not selected:
        parser.error("Keine Benchmarkfälle in dieser Auswahl.")
    results = run(selected, examples, claims, coach, manual)
    if candidate_error:
        for result in results:
            if result["scope"] == "pilot":
                result["observed"] = candidate_error
    blocks = {}
    for result in results:
        if result["mandatory"] and result["status"] != "PASS":
            blocks.setdefault(result["content"], []).append(result["id"])
    counts = Counter(r["status"] for r in results)
    areas = {}
    for scope in dict.fromkeys(r["scope"] for r in results):
        by_status = Counter(r["status"] for r in results if r["scope"] == scope)
        areas[scope] = {status: by_status[status] for status in STATUSES}
    coach_domains = {}
    for domain in sorted({r["domain"] for r in results if r["scope"] == "coach"}):
        by_status = Counter(r["status"] for r in results if r["scope"] == "coach" and r["domain"] == domain)
        coach_domains[domain] = {status: by_status[status] for status in STATUSES}
    report = {"schema_version": 2, "coach_domains": coach_domains, "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "dirty": bool(subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT)),
              "scope": args.scope, "areas": areas, "counts": {s: counts[s] for s in STATUSES}, "blocks": blocks, "results": results}
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
