"""Deterministic checks for the release surfaces uncovered by the STEPS audit."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from src.steps.knowledge import KnowledgeAdapter
from src.steps.midi import MidiFile
from src.steps.progression import ProgressionSession
from src.steps.theory import MusicTheoryError


def beginner_voices():
    failures = []
    for convention, symbols in (("INT", ["C/E", "Bb/D", "C7b5", "C6"]),
                                ("DE", ["C/E", "B/D", "C7b5", "C6"])):
        voicings = ProgressionSession(symbols, convention=convention).get_beginner_voicings().voicings
        for voicing, expected_bass in zip(voicings[:2], (4, 2), strict=True):
            if min(voicing.all_midi_notes) % 12 != expected_bass:
                failures.append(f"{convention} {voicing.chord_symbol}: incorrect slash bass")
        if {n % 12 for n in voicings[2].all_midi_notes} - {0, 4, 6, 10}:
            failures.append(f"{convention} C7b5: reduction added an unwritten tone")
        if "7th" in voicings[3].reduction.omitted_factors:
            failures.append(f"{convention} C6: reduction reports an absent seventh")
    return failures


def midi_drop2():
    session = ProgressionSession(["Cmaj7"])
    with TemporaryDirectory(prefix="steps-release-midi-") as directory:
        close, drop2 = [
            _export_upper_notes(session, Path(directory) / f"{kind}.mid", kind)
            for kind in ("CLOSE", "DROP2")
        ]
    if len(close) != 4:
        return ["Cmaj7 CLOSE does not contain four voices"]
    # A uniform octave move is allowed to place the resulting shape in range.
    expected = sorted([*close[:2], close[-2] - 12, close[-1]])
    if len(drop2) != 4 or len({out - note for out, note in zip(drop2, expected)}) != 1:
        return [f"Cmaj7: CLOSE {close}, DROP2 {drop2}, expected Drop-2 shape {expected}"]
    if (drop2[0] - expected[0]) % 12:
        return [f"Cmaj7 DROP2 moved by a non-octave interval: {drop2}"]
    return []


def _export_upper_notes(session, path, kind):
    session.export_midi_file(path, voicing_type=kind)
    parsed = MidiFile.from_bytes(path.read_bytes())
    return sorted(e.msg_bytes[1] for e in parsed.tracks[1].raw_events
                  if e.msg_bytes[0] & 0xF0 == 0x90 and e.msg_bytes[2] > 0)


def recommendations():
    failures = []
    for key, minor, chord in (("C", False, "B##m"), ("C", False, "Bxdom7"), ("C", False, "Fbbm7"),
                              ("G##", False, "G##"), ("Cbb", True, "Gbb7")):
        try:
            ProgressionSession([chord], key_root=key, is_minor=minor).explore_next_chords(0)
        except MusicTheoryError as exc:
            failures.append(f"{key} / {chord}: {exc}")
    return failures


def knowledge_retrieval():
    adapter = KnowledgeAdapter()
    failures = []
    for query in ("", "dimension"):
        if adapter.query(query).found:
            failures.append(f"{query!r}: unrelated or empty query returned a musical claim")
    answer = adapter.query("ii-V-I", convention="INT")
    if not answer.found or not answer.sources or " zu H " in answer.explanation:
        failures.append("INT ii-V-I: missing evidence or German H in the explanation")
    root = Path(__file__).resolve().parents[1]
    evaluation = json.loads((root / "skills/steps-knowledge/skill_eval_cases.json").read_text(encoding="utf-8"))
    for case in evaluation["cases"]:
        actual = adapter.query(case["prompt"]).status
        if actual != case["expected_status"]:
            failures.append(f"{case['id']}: expected {case['expected_status']}, received {actual}")
    registry = json.loads((root / "knowledge/sources/registry.yaml").read_text(encoding="utf-8"))
    for source in registry["sources"]:
        if source["id"] == "omt-ii-v-i":
            source["rights_status"] = "review_required"
            break
    with TemporaryDirectory(prefix="steps-release-knowledge-") as directory:
        path = Path(directory) / "registry.yaml"
        path.write_text(json.dumps(registry), encoding="utf-8")
        answer = KnowledgeAdapter(product_registry=path).query("ii-V-I")
        if answer.status == "GROUNDED" and any(s.source_id == "omt-ii-v-i" for s in answer.sources):
            failures.append("An unapproved source was returned as grounded evidence")
    # A result about a cadence must not be returned as evidence for a swing question.
    answer = adapter.query("Wie verhält sich das Swing-Verhältnis bei 130 BPM in Jazz-Achtelnoten?")
    if any(source.source_id == "omt-ii-v-i" for source in answer.sources):
        failures.append("Swing query cited an unrelated ii–V–I cadence")
    return failures
