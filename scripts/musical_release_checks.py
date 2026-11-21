"""Deterministic checks for the release surfaces uncovered by the STEPS audit."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from src.steps.knowledge import KnowledgeAdapter
from src.steps.midi import SMFParser
from src.steps.progression import ProgressionSession, list_progressions
from src.steps.progression.reviewed import PublicationError, resolve_source_citation
from src.steps.theory import MusicTheoryError, parse_chord


def beginner_voices():
    failures = []
    for convention, symbols in (("INT", ["C/E", "Bb/D", "C7b5", "C6"]),
                                ("DE", ["C/E", "B/D", "C7b5", "C6"])):
        voicings = ProgressionSession(symbols, convention=convention).get_beginner_voicings().voicings
        for voicing, expected_bass in zip(voicings[:2], (4, 2), strict=True):
            if min(voicing.all_midi_notes) % 12 != expected_bass:
                failures.append(f"{convention} {voicing.chord_symbol}: incorrect slash bass")
        if {n % 12 for n in voicings[2].all_midi_notes} != {0, 4, 6}:
            failures.append(f"{convention} C7b5: reduction must retain C, E and Gb")
        if voicings[3].reduction.omitted_factors != ("6th",):
            failures.append(f"{convention} C6: reduction must report the omitted sixth")
    return failures


def desktop_voicing():
    failures = beginner_voices()
    session = ProgressionSession(["Dm7", "G7", "Cmaj7"])
    power = session.get_voicings(style="POWER_CHORDS")
    if [{note % 12 for note in voicing.notes} for voicing in power] != [{2, 9}, {2, 7}, {0, 7}]:
        failures.append("Power profile did not produce root and perfect fifth")
    pop = session.get_voicings(style="CONTEMPORARY_POP")
    quartal = session.get_voicings(style="QUARTAL_JAZZ")
    if quartal[0].midi_notes != [50, 57, 60, 65] or quartal == pop:
        failures.append("Quartal profile did not choose the expected fourth-based Dm7 spacing")
    if any({note % 12 for note in a.notes} != {note % 12 for note in b.notes}
           or a.notes[0] % 12 != b.notes[0] % 12 for a, b in zip(pop, quartal, strict=True)):
        failures.append("Quartal profile changed selected pitch classes or the written bass")
    return failures


def midi_drop2():
    failures = []
    roots = {
        "INT": "C Db D Eb E F F# G Ab A Bb B".split(),
        "DE": "C Des D Es E F Fis G As A B H".split(),
    }
    tones = {
        "maj7": (0, 4, 7, 11), "7": (0, 4, 7, 10), "m7": (0, 3, 7, 10),
        "dim7": (0, 3, 6, 9), "m7b5": (0, 3, 6, 10), "7b5": (0, 4, 6, 10),
        "13": (0, 4, 10, 21), "7#11": (0, 4, 10, 18),
    }
    with TemporaryDirectory(prefix="steps-release-midi-") as directory:
        target = Path(directory) / "check.mid"
        for notation, names in roots.items():
            for root, name in enumerate(names):
                bass_pc = (root + 4) % 12
                for suffix, intervals in tones.items():
                    symbol = f"{name}{suffix}/{names[bass_pc]}"
                    session = ProgressionSession([symbol], convention=notation)
                    close, bass = _export_midi_notes(session, target, "CLOSE")
                    expected_pcs = {(root + interval) % 12 for interval in intervals}
                    if (len(close) != 4 or not 48 <= close[0] <= close[-1] <= 72
                            or close[-1] - close[0] > 12 or {n % 12 for n in close} != expected_pcs
                            or bass != [36 + bass_pc]):
                        failures.append(f"{notation} {symbol}: wrong CLOSE {close} or bass {bass}")
                        continue
                    expected = sorted([*close[:2], close[-2] - 12, close[-1]])
                    fits = any(expected[0] + offset >= 48 and expected[-1] + offset <= 72
                               for offset in (0, 12))
                    offered = "DROP2" not in session.midi_voicing_failures()
                    if fits != offered:
                        failures.append(f"{notation} {symbol}: wrong DROP2 availability")
                        continue
                    if not fits:
                        continue
                    drop2, drop_bass = _export_midi_notes(session, target, "DROP2")
                    shapes = [[note + offset for note in expected] for offset in (0, 12)]
                    if (drop2 not in shapes or not 48 <= drop2[0] <= drop2[-1] <= 72
                            or drop_bass != bass):
                        failures.append(f"{notation} {symbol}: wrong DROP2 {drop2} or bass {drop_bass}")
    return failures


def _export_midi_notes(session, path, mode):
    session.export_midi_file(path, voicing_type=mode)
    parsed = SMFParser.parse(path.read_bytes())
    return tuple(sorted(note.pitch for note in parsed.tracks[index].notes) for index in (1, 2))


def recommendations():
    failures = []
    cases = (
        ("INT", "C", False, "B##m", "Ex"),
        ("INT", "C", False, "Bxdom7", "Ex"),
        ("INT", "C", False, "Fbbm7", "Gbbm"),
        ("INT", "G##", False, "G##", "Cx"),
        ("INT", "Cbb", True, "Gbb7", "Cbbm7"),
        ("DE", "C", False, "Hisism", "Eisis"),
        ("DE", "C", False, "Fesesm7", "Gesesm"),
        ("DE", "Ceses", True, "Geses7", "Cesesm7"),
    )
    for notation, key, minor, chord, witness in cases:
        try:
            session = ProgressionSession([chord], key_root=key, is_minor=minor, convention=notation)
            symbols = [item.candidate_symbol for item in session.explore_next_chords(0)]
            for symbol in symbols:
                parse_chord(symbol, notation)
            if witness not in symbols:
                failures.append(f"{notation} {key} / {chord}: missing playable option {witness}")
        except MusicTheoryError as exc:
            failures.append(f"{notation} {key} / {chord}: {exc}")
    references = set()
    for progression in list_progressions():
        session = ProgressionSession(
            progression.chords_str.split(" - "),
            key_root=progression.default_key.removesuffix("m"),
            is_minor=progression.default_key.endswith("m"), convention="INT",
        )
        for index in range(len(session.chords)):
            for item in session.explore_next_chords(index):
                if item.evidence_kind == "LITERATURE_REFERENCE":
                    references.add((item.source_id or "", item.source_locator or ""))
                elif item.source_id is not None or item.source_locator is not None:
                    failures.append(f"{progression.prog_id}: unexpected reference for {item.evidence_kind}")
    for source_id, locator in sorted(references):
        try:
            resolve_source_citation(source_id, locator)
        except PublicationError as exc:
            failures.append(f"Explorer reference {source_id}: {exc}")
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
