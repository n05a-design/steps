"""Cross-check generated STEPS questions against independent, bounded musical oracles."""

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from functools import partial
from hashlib import sha256
from importlib.util import find_spec
from itertools import product
import json
from multiprocessing import get_context
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import monotonic
from typing import Callable
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import music_audit_references as references

DEFAULT_SEED = 20261121
RANDOMIZED_ORACLE = "steps-randomized-2"
LETTERS = "CDEFGAB"
MAJOR = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10)
MAJOR_DEGREES = ("I", "ii", "iii", "IV", "V", "vi", "vii°")
MINOR_DEGREES = ("i", "ii°", "III", "iv", "v", "VI", "VII")
MAJOR_QUALITIES = ("", "m", "m", "", "", "m", "dim")
MINOR_QUALITIES = ("m", "dim", "", "m", "m", "", "")
# Open Music Theory, Triad qualities and Seventh chords.
TRIADS = {"": (0, 4, 7), "m": (0, 3, 7), "dim": (0, 3, 6), "aug": (0, 4, 8)}
SEVENTHS = {"maj7": (0, 4, 7, 11), "7": (0, 4, 7, 10),
            "m7": (0, 3, 7, 10), "m7b5": (0, 3, 6, 10)}
QUALITIES = TRIADS | SEVENTHS | {"dim7": (0, 3, 6, 9)}
# (International, German, written letter, pitch class). Independent test vocabulary.
NOTES = (
    ("C", "C", "C", 0), ("C#", "Cis", "C", 1), ("Db", "Des", "D", 1),
    ("D", "D", "D", 2), ("Eb", "Es", "E", 3), ("E", "E", "E", 4),
    ("F", "F", "F", 5), ("F#", "Fis", "F", 6), ("Gb", "Ges", "G", 6),
    ("G", "G", "G", 7), ("Ab", "As", "A", 8), ("A", "A", "A", 9),
    ("Bb", "B", "B", 10), ("B", "H", "B", 11),
)


@dataclass(frozen=True)
class Trial:
    question: dict
    expected: object
    observe: Callable[[], object]


def tones(root, quality):
    return sorted((root + interval) % 12 for interval in QUALITIES[quality])


def note_context(rng):
    index = rng.randrange(2)
    return index, ("INT", "DE")[index]


def chord_trial(rng, _adapter, _directory):
    index, convention = note_context(rng)
    root, bass = rng.choice(NOTES), rng.choice(NOTES)
    quality = rng.choice(tuple(QUALITIES))
    symbol = f"{root[index]}{quality}/{bass[index]}"
    expected = [root[2], root[3], quality, bass[2], bass[3], tones(root[3], quality)]

    return random_trial("chords", {"chord": symbol, "notation": convention}, expected)


def inversion_trial(rng, _adapter, _directory):
    quality = rng.choice(tuple(SEVENTHS))
    root = rng.randrange(12)
    inversion = rng.randrange(4)
    pitches = [(root + interval) % 12 for interval in SEVENTHS[quality]]
    bass = pitches[inversion]
    notes = [36 + bass] + [rng.choice((60, 72, 84)) + pc for pc in pitches if pc != bass]
    rng.shuffle(notes)
    expected = [root, bass, ("7", "6/5", "4/3", "4/2")[inversion], True]

    return random_trial("inversions", {"notes": notes, "quality": quality}, expected)


def degree_trial(rng, _adapter, _directory):
    index, convention = note_context(rng)
    tonic = rng.choice(NOTES)
    minor = rng.choice((False, True))
    position = rng.randrange(7)
    numeral = (MINOR_DEGREES if minor else MAJOR_DEGREES)[position]
    quality = (MINOR_QUALITIES if minor else MAJOR_QUALITIES)[position]
    pc = (tonic[3] + (MINOR if minor else MAJOR)[position]) % 12
    letter = LETTERS[(LETTERS.index(tonic[2]) + position) % 7]

    return random_trial("degrees", {"tonic": tonic[index], "minor": minor, "degree": numeral, "notation": convention},
                        [letter, pc, quality, tones(pc, quality)])


def degree_roundtrip_trial(rng, _adapter, _directory):
    index, notation = note_context(rng)
    tonic = rng.choice(NOTES)
    minor = rng.choice((False, True))
    position = rng.choice((2, 5) if minor else (0, 3))
    scale = MINOR if minor else MAJOR
    root_pc = (tonic[3] + scale[position]) % 12
    letter = LETTERS[(LETTERS.index(tonic[2]) + position) % 7]
    # Restrict to independently spelled roots in the input vocabulary.
    match = next((note for note in NOTES if note[2:] == (letter, root_pc)), None)
    if match is None:
        tonic = NOTES[0]
        root_pc = scale[position]
        letter = LETTERS[position]
        match = next(note for note in NOTES if note[2:] == (letter, root_pc))
    quality = rng.choice(("7", "9"))
    symbol = match[index] + quality
    expected_pcs = sorted((root_pc + offset) % 12 for offset in ((0, 4, 7, 10) if quality == "7" else
                                                                  (0, 4, 7, 10, 14)))

    numeral = ("I", "II", "III", "IV", "V", "VI", "VII")[position]
    return random_trial("degree-roundtrip",
                        {"chord": symbol, "tonic": tonic[index], "minor": minor, "notation": notation},
                        [f"{numeral}dom{quality}", letter, expected_pcs])


def transposition_trial(rng, _adapter, _directory):
    index, convention = note_context(rng)
    # Natural roots and slash basses admit a common spelling in the sampled range.
    natural = [note for note in NOTES if note[0] == note[2]]
    root, bass, second = rng.sample(natural, 3)
    distance = rng.randint(-11, 11)
    chords = [f"{root[index]}maj7/{bass[index]}", f"{second[index]}m"]
    relative = [(LETTERS.index(note[2]) - LETTERS.index(root[2])) % 7 for note in (root, bass, second)]
    timing = (rng.randint(0, 70), rng.randint(100, 380))
    expected = [(root[3] + distance) % 12, (root[3] + distance) % 12,
                (bass[3] + distance) % 12, (second[3] + distance) % 12, relative, ["maj7", "m"], list(timing)]

    return random_trial("transposition", {"chords": chords, "key": root[index], "distance": distance,
                                          "notation": convention, "event": timing}, expected)


def voice_leading_trial(rng, _adapter, _directory):
    source = sorted(rng.sample(range(48, 73), 3))
    root = rng.randrange(12)
    target = {(root + offset) % 12 for offset in rng.choice(tuple(TRIADS.values()))}
    bass = rng.choice(sorted(target))
    windows = [[note for note in range(center - 12, center + 13) if note % 12 in target] for center in source]

    expected = min(movement_cost(source, notes) for notes in product(*windows)
                   if notes[0] < notes[1] < notes[2] and notes[0] % 12 == bass
                   and {note % 12 for note in notes} == target)

    return random_trial("voice-leading", {"from": source, "pitch_classes": sorted(target), "bass": bass},
                        [True, expected])


def midi_trial(rng, _adapter, directory):
    index, convention = note_context(rng)
    root, bass = rng.sample(NOTES, 2)
    quality = rng.choice(("", "m"))
    start, duration = rng.randrange(180), 20 * rng.randint(1, 20)
    mode = rng.choice(("FIXED_GAP", "PERCENT_95"))
    fmt = rng.randrange(2)
    length = duration - 10 if mode == "FIXED_GAP" else round(Fraction(19 * duration, 20))
    symbol = f"{root[index]}{quality}/{bass[index]}"
    expected_chord_pcs = sorted([*tones(root[3], quality), root[3]])
    expected = [fmt, 1 if fmt == 0 else 3, [[start, length]] * 5, expected_chord_pcs, [36 + bass[3]]]
    return random_trial("midi", {"chord": symbol, "event": [start, duration], "duration_mode": mode,
                                 "smf": fmt, "notation": convention}, expected, directory=directory)


def retrieval_trial(rng, adapter, _directory, *, published):
    query, claims, sources = rng.choice((
        ("axis", ["PROG-001-HARMONY", "PROG-001-TONAL-CENTER"],
         ["mto-richards-axis-progressions", "omt-four-chord-schemas", "omt-roman-numerals"]),
        ("ii–V–I", ["PROG-003-HARMONY", "PROG-003-VOICE-II-V", "PROG-003-VOICE-V-I"], ["omt-ii-v-i"]),
        ("notation", ["PILOT-NOTATION-001"], ["yale-key-names"]),
    ))
    status = "GROUNDED"
    if rng.choice((False, True)):
        query = f"Dimension und {query}"
        status, claims, sources = "NO_EVIDENCE", [], []
    query = f"  {rng.choice((query, query.upper(), query.lower()))}{rng.choice(('', '?', '.'))}  "
    notation = rng.choice(("INT", "DE"))

    return random_trial("retrieval", {"query": query, "notation": notation},
                        [status, bool(claims), claims, sources, True, True], adapter=adapter, published=published)


def movement_cost(source, notes):
    return sum(abs(before - after) for before, after in zip(source, notes, strict=True))


def random_trial(area, question, expected, **context):
    return Trial(question, expected, partial(observe_random, area, question, **context))


def observe_random(area, question, *, directory=None, adapter=None, published=None):
    notation = question.get("notation")
    if area == "chords":
        from src.steps.theory.chord import parse_chord

        chord = parse_chord(question["chord"], notation)
        return [chord.root.step, int(chord.root.pitch_class), chord.quality,
                chord.bass.step, int(chord.bass.pitch_class), sorted(chord.pitch_class_set)]
    if area == "inversions":
        from src.steps.theory.inversion import detect_chord_inversion

        result = detect_chord_inversion(question["notes"])
        return [result.root_pc, result.bass_pc, result.figured_bass, result.is_seventh_chord]
    if area in {"degrees", "degree-roundtrip"}:
        from src.steps.progression import ProgressionSession, resolve_roman_degree

        tonic, minor = question["tonic"], question["minor"]
        if area == "degrees":
            chord = resolve_roman_degree(question["degree"], tonic, minor, convention=notation,
                                         minor_accidentals="natural_minor")
            return [chord.root.step, int(chord.root.pitch_class), chord.quality, sorted(chord.pitch_class_set)]
        session = ProgressionSession([question["chord"]], key_root=tonic, convention=notation, is_minor=minor)
        label = session.harmonic_degree_at(0)
        chord = resolve_roman_degree(label, tonic, minor, convention=notation, minor_accidentals="natural_minor")
        return [label, chord.root.step, sorted(chord.pitch_class_set)]
    if area == "transposition":
        from src.steps.progression import ProgressionSession
        from src.steps.theory.chord import parse_chord

        session = ProgressionSession(question["chords"], key_root=question["key"], convention=notation)
        session.set_chord_event_timing(0, *question["event"])
        session.transpose(question["distance"])
        first, following = (parse_chord(symbol, notation) for symbol in session.chords)
        tonic = parse_chord(session.key_root, notation).root
        written = [(LETTERS.index(note.step) - LETTERS.index(tonic.step)) % 7
                   for note in (first.root, first.bass, following.root)]
        return [int(tonic.pitch_class), int(first.root.pitch_class), int(first.bass.pitch_class),
                int(following.root.pitch_class), written, [first.quality, following.quality],
                list(session.get_chord_event_timing(0))]
    if area == "voice-leading":
        from src.steps.progression.voice_leading import optimize_smooth_voice_leading

        source, target, bass = question["from"], set(question["pitch_classes"]), question["bass"]
        notes = optimize_smooth_voice_leading(source, target, bass)
        valid = (len(notes) == len(set(notes)) == 3 and notes == sorted(notes) and notes[0] % 12 == bass
                 and {note % 12 for note in notes} == target
                 and all(abs(a - b) <= 12 for a, b in zip(source, notes, strict=True)))
        return [valid, movement_cost(source, notes)]
    if area == "midi":
        from src.steps.midi import SMFParser
        from src.steps.progression import ProgressionSession

        session = ProgressionSession([question["chord"]], convention=notation)
        session.set_chord_event_timing(0, *question["event"])
        path = session.export_midi_file(directory / "probe.mid", note_duration_mode=question["duration_mode"],
                                        smf_format=question["smf"])
        decoded = SMFParser.parse(path.read_bytes())
        return [decoded.format, decoded.num_tracks, [[n.start_tick, n.duration_ticks] for n in decoded.all_notes],
                sorted(n.pitch % 12 for n in decoded.all_notes if n.channel == 0),
                [n.pitch for n in decoded.all_notes if n.channel == 1]]
    from scripts.evaluate_knowledge_adapter import citations_match_publication

    query = question["query"]
    answer = adapter.query(query, convention=notation)
    verified = all(item.verified and item.citations for item in answer.claims)
    verified &= not answer.alternatives and citations_match_publication(answer.claims, published)
    if answer.found:
        verified &= answer.explanation == " ".join(item.summary for item in answer.claims)
    else:
        verified &= answer.explanation == (
            f"Für die Anfrage {query!r} liegt kein geprüfter Primärbeleg in der STEPS-Wissensbasis vor."
        )
    located = all(source.locator and source.rights_status == "approved" for source in answer.sources)
    return [answer.status, answer.found, [item.claim_id for item in answer.claims],
            sorted({source.source_id for source in answer.sources}), verified, located]


PROBES = {
    "chords": chord_trial, "inversions": inversion_trial, "degrees": degree_trial,
    "degree-roundtrip": degree_roundtrip_trial, "transposition": transposition_trial, "voice-leading": voice_leading_trial,
    "midi": midi_trial, "retrieval": retrieval_trial,
}


def observe_reference(area, question):
    if area == "pitch":
        from src.steps.keyboard.model import piano_key

        key = piano_key(question["midi"])
        spellings = sorted([note.step, note.alteration, note.octave] for note in key.enharmonic_spellings())
        return [key.midi, key.pitch_class, key.octave, key.number, key.is_black, spellings]
    if area == "recognition-exact":
        from src.steps.keyboard.recognition import CandidateKind, recognize_chord

        result = recognize_chord(question["notes"], allow_incomplete=False)
        return sorted([int(c.chord.root.pitch_class), c.chord.quality]
                      for c in result.candidates if c.kind is CandidateKind.EXACT)

    from src.steps.keyboard.chord_tones import chord_tones, label_voicing
    from src.steps.theory.chord import parse_chord
    from src.steps.theory.pitch import parse_spelling
    from src.steps.theory.scale import construct_scale

    def name(spelling):
        return spelling.render("INT").rstrip("0123456789").replace("x", "##")

    def names(chord):
        return [name(tone.spelling) if tone.spelling is not None else None for tone in chord_tones(chord)]

    if area == "chord-reference":
        chord = parse_chord(question["symbol"], "INT")
        tones = chord_tones(chord)
        return [[tone.role.interval_label, tone.semitones, tone.pitch_class, spelling]
                for tone, spelling in zip(tones, names(chord), strict=True)]
    if area == "declared-bass":
        chord = parse_chord(question["symbol"], "INT")
        labelled = label_voicing(chord, question["notes"])
        return [labelled.bass.role.interval_label, labelled.inversion.figured_bass if labelled.inversion else None,
                labelled.bass.midi % 12]
    root = parse_spelling(question["root"], "INT")
    scale = construct_scale(root, question["scale"])
    if area == "scale-reference":
        return [list(scale.pitch_classes), [note - root.midi_number for note in scale.midi_notes],
                [name(note) for note in scale.spellings] if len(scale.spellings) == 7 else None]
    harmonize = scale.get_diatonic_triad if question["size"] == 3 else scale.get_diatonic_seventh
    chord = harmonize(question["degree"])
    return [list(chord.theoretical_intervals), sorted(chord.pitch_class_set), names(chord)]


def canonical_hash(data):
    canonical = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return sha256(canonical.encode("utf-8")).hexdigest()


def case_payload(area, case_id, question, expected):
    oracle = references.PROFILE if area in references.AREAS else RANDOMIZED_ORACLE
    return {"schema_version": 1, "oracle_version": oracle, "area": area,
            "case_id": case_id, "input": question, "expected": expected}


def classify_failure(failures, counts, *, area, case_id, status, classification,
                     trial=None, question=None, expected=None, actual=None, payload=None):
    counts[status] += 1
    row = {"area": area, "case_id": case_id, "trial": trial, "question": question,
           "expected": expected, "actual": actual, "status": status, "classification": classification}
    identity = {"area": area, "case_id": case_id, "classification": classification, "input": question}
    row["fingerprint"] = canonical_hash(identity)
    if payload is not None:
        row["replay"] = {"payload": payload, "sha256": canonical_hash(payload)}
    failures.append(row)


def run(seed, trials, areas=tuple(PROBES), *, profile=None, case=None, timeout=None, replay=None, workers=1):
    """Run the existing probes and optionally the independent finite reference profile."""
    failures = []
    by_area = {}
    start = monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    if workers > 1 and len(areas) > 1 and case is None and replay is None:
        reports = []
        with ProcessPoolExecutor(max_workers=min(workers, len(areas)),
                                 mp_context=get_context("spawn")) as executor:
            tasks = [executor.submit(run, seed, trials, (area,), profile=profile, timeout=timeout)
                     for area in areas]
            for area, task in zip(areas, tasks, strict=True):
                try:
                    reports.append(task.result())
                except BrokenProcessPool:
                    failures.append({"area": area, "case_id": f"{area}:worker", "classification": "SETUP_ERROR",
                                     "status": "error", "actual": {"type": "BrokenProcessPool"}})
        combined = (reports[0] if reports else {
            "schema_version": 1, "run_id": str(uuid4()), "seed": seed, "python_version": platform.python_version(),
            "platform": platform.system(), "profile": profile or "randomized", "trials_per_area": trials,
            "timeout_seconds": timeout, "oracle_version": references.PROFILE,
        }) | {"areas": {}, "failures": failures, "not_run_areas": [row["area"] for row in failures]}
        for report in reports:
            combined["areas"].update(report["areas"])
            combined["failures"].extend(report["failures"])
        gates = {report["gate"] for report in reports}
        combined.update(workers=workers, started_at=started_at, elapsed_seconds=round(monotonic() - start, 3),
                        gate="ERROR" if combined["not_run_areas"] or "ERROR" in gates
                        else "FAIL" if "FAIL" in gates else "PASS")
        return combined
    deadline = start + timeout if timeout is not None else float("inf")
    with TemporaryDirectory(prefix="steps-musical-audit-") as temp:
        for area in areas:
            counts = Counter(dict.fromkeys(("passed", "failed", "error", "timeout", "not_run",
                                           "setup_error", "generator_error", "skipped"), 0))
            by_area[area] = counts
            if area in references.AREAS:
                # Enumerate selected inputs first so the report retains the planned count on timeout.
                try:
                    if replay is not None:
                        generated = [(replay["case_id"], replay["input"], replay["expected"])]
                    else:
                        generated = [row for row in references.cases(area, profile, seed)
                                     if case is None or row[0] == case]
                except Exception as exc:
                    counts["generator_error"] += 1
                    classify_failure(failures, counts, area=area, case_id=f"{area}:generator",
                                     status="error", classification="GENERATOR_DEFECT",
                                     actual={"type": type(exc).__name__})
                    counts.update(planned=0, selected=0)
                    continue
                counts.update(planned=len(generated), selected=len(generated))
                for index, (case_id, question, expected) in enumerate(generated, 1):
                    if monotonic() >= deadline:
                        classify_failure(failures, counts, area=area, case_id=case_id,
                                         status="timeout", classification="TIMEOUT")
                        counts["not_run"] += len(generated) - index
                        break
                    payload = case_payload(area, case_id, question, expected)
                    try:
                        actual = observe_reference(area, question)
                    except Exception as exc:
                        classify_failure(failures, counts, area=area, case_id=case_id, status="error",
                                         classification="SETUP_ERROR" if isinstance(exc, ImportError) else "PRODUCT_ERROR",
                                         trial=index, question=question, expected=expected,
                                         actual={"type": type(exc).__name__}, payload=payload)
                        continue
                    if monotonic() >= deadline:
                        classify_failure(failures, counts, area=area, case_id=case_id, status="timeout",
                                         classification="TIMEOUT", trial=index, question=question,
                                         expected=expected, actual=actual, payload=payload)
                        counts["not_run"] += len(generated) - index
                        break
                    if actual == expected:
                        counts["passed"] += 1
                    else:
                        classify_failure(failures, counts, area=area, case_id=case_id, status="failed",
                                         classification="REFERENCE_MISMATCH", trial=index, question=question,
                                         expected=expected, actual=actual, payload=payload)
                continue

            adapter = None
            count = 1 if replay is not None else trials
            counts.update(planned=count, selected=count)
            rng = random.Random(f"{seed}:{area}")
            probe = PROBES[area]
            context = {"directory": Path(temp)} if area == "midi" else {}
            if area == "retrieval":
                try:
                    from scripts.evaluate_knowledge_adapter import published_citations
                    from src.steps.knowledge import KnowledgeAdapter

                    adapter = KnowledgeAdapter()
                    published = published_citations()
                    probe = partial(probe, published=published)
                    context.update(adapter=adapter, published=published)
                except Exception as exc:
                    counts["setup_error"] += 1
                    classify_failure(failures, counts, area=area, case_id=f"{area}:setup",
                                     status="error", classification="SETUP_ERROR",
                                     actual={"type": type(exc).__name__})
                    counts["not_run"] = count
                    continue
            for index in range(count):
                case_id = replay["case_id"] if replay else f"{area}:{seed}:{index + 1}"
                if monotonic() >= deadline:
                    classify_failure(failures, counts, area=area, case_id=case_id,
                                     status="timeout", classification="TIMEOUT")
                    counts["not_run"] += count - index - 1
                    break
                try:
                    trial = (random_trial(area, replay["input"], replay["expected"], **context) if replay
                             else probe(rng, adapter, Path(temp)))
                except Exception as exc:
                    counts["generator_error"] += 1
                    classify_failure(failures, counts, area=area, case_id=case_id,
                                     trial=index + 1, status="error", classification="GENERATOR_DEFECT",
                                     actual={"type": type(exc).__name__})
                    continue
                payload = case_payload(area, case_id, trial.question, trial.expected)
                try:
                    actual = trial.observe()
                except Exception as exc:
                    classify_failure(failures, counts, area=area, case_id=case_id, status="error",
                                     classification="SETUP_ERROR" if isinstance(exc, ImportError) else "PRODUCT_ERROR",
                                     trial=index + 1, question=trial.question, expected=trial.expected,
                                     actual={"type": type(exc).__name__}, payload=payload)
                    continue
                if monotonic() >= deadline:
                    classify_failure(failures, counts, area=area, case_id=case_id, status="timeout",
                                     classification="TIMEOUT", trial=index + 1, question=trial.question,
                                     expected=trial.expected, actual=actual, payload=payload)
                    counts["not_run"] += count - index - 1
                    break
                if trial.expected == actual:
                    counts["passed"] += 1
                else:
                    classify_failure(failures, counts, area=area, case_id=case_id, status="failed",
                                     classification="REFERENCE_MISMATCH", trial=index + 1,
                                     question=trial.question, expected=trial.expected, actual=actual, payload=payload)
    if case is not None and not any(counts["selected"] for counts in by_area.values()):
        area = next(iter(areas))
        classify_failure(failures, by_area[area], area=area, case_id=case,
                         status="error", classification="UNKNOWN_CASE")
    for counts in by_area.values():
        counts["executed"] = (counts["passed"] + counts["failed"] + counts["error"]
                              - counts["setup_error"] - counts["generator_error"])
    gate = "ERROR" if any(row["status"] in ("error", "timeout") for row in failures) else (
        "FAIL" if failures else "PASS"
    )
    return {"schema_version": 1, "run_id": str(uuid4()), "started_at": started_at,
            "seed": seed, "python_version": platform.python_version(),
            "platform": platform.system(), "profile": profile or "randomized",
            "oracle_version": references.PROFILE, "timeout_seconds": timeout,
            "elapsed_seconds": round(monotonic() - start, 3), "trials_per_area": trials,
            "areas": by_area, "failures": failures, "gate": gate, "workers": 1}


def checkout_provenance():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}

    def git(*args):
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, env=env, text=True, stderr=subprocess.DEVNULL, timeout=15,
        ).strip()

    spec = find_spec("src")
    if (Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT
            or spec is None or not spec.origin or Path(spec.origin).resolve() != ROOT / "src/__init__.py"):
        raise ValueError("Unexpected checkout or STEPS import root.")
    return {
        "revision": git("rev-parse", "HEAD"),
        "tracked_changes": bool(git("status", "--porcelain", "--untracked-files=no")),
        "working_tree_changes": bool(git("status", "--porcelain")),
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "oracle_sha256": sha256(Path(references.__file__).read_bytes()).hexdigest(),
    }


def write_report(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with NamedTemporaryFile(dir=path.parent, delete=False, mode="w", encoding="utf-8", newline="\n") as stream:
            temp = Path(stream.name)
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def replay_with_deadline(payload, seed, seconds):
    """Enforce a wall-clock deadline for one saved product case."""
    command = (
        "import json, sys; "
        "from scripts.audit_randomized_music import run; "
        "seed, payload = json.load(sys.stdin); "
        "print(json.dumps(run(seed, 1, (payload['area'],), profile='replay', replay=payload)))"
    )
    try:
        child = subprocess.run(
            [sys.executable, "-B", "-c", command], cwd=ROOT, capture_output=True, check=True,
            encoding="utf-8", input=json.dumps((seed, payload)), timeout=seconds,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        report = json.loads(child.stdout)
        report["timeout_seconds"] = seconds
        report["deadline_mode"] = "subprocess"
        return report
    except subprocess.TimeoutExpired:
        status, classification = "timeout", "TIMEOUT"
    except (OSError, subprocess.CalledProcessError, ValueError):
        status, classification = "error", "REPLAY_WORKER_ERROR"
    area = payload["area"]
    counts = Counter(dict.fromkeys(("passed", "failed", "error", "timeout", "not_run", "executed"), 0))
    counts.update(planned=1, selected=1)
    failures = []
    classify_failure(failures, counts, area=area, case_id=payload["case_id"], status=status,
                     classification=classification, question=payload["input"], expected=payload["expected"],
                     payload=payload)
    return {"schema_version": 1, "run_id": str(uuid4()), "gate": "ERROR", "profile": "replay",
            "seed": seed, "timeout_seconds": seconds, "deadline_mode": "subprocess",
            "areas": {area: counts}, "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--trials", "--cases", type=int, default=128, help="Number of random questions per area.")
    parser.add_argument("--area", action="append", choices=(*PROBES, *references.AREAS),
                        help="Repeat to select multiple areas.")
    parser.add_argument("--profile", choices=("smoke", "pr", "nightly", "full", "release"))
    parser.add_argument("--case", action="append", help="Select one finite reference case by ID.")
    parser.add_argument("--replay", type=Path, help="Replay a saved failure payload.")
    parser.add_argument("--timeout", type=float, help="Time budget in seconds. A replay uses a hard subprocess deadline.")
    parser.add_argument("--workers", type=int, default=1, help="Number of independent audit areas to run concurrently.")
    parser.add_argument("--list-areas", action="store_true", help="List selectable audit areas.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--external-oracles", action="store_true", help="Require the isolated Python comparison libraries.")
    parser.add_argument("--tonal-module", type=Path, help="Require this isolated Tonal module for comparison.")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    if args.list_areas:
        print("\n".join((*PROBES, *references.AREAS)))
        return 0
    if not 1 <= args.workers <= len(PROBES) + len(references.AREAS):
        parser.error("--workers is outside the range of available audit areas")
    if args.trials < 1:
        parser.error("--trials must be positive")
    if args.timeout is not None and not 0 < args.timeout < float("inf"):
        parser.error("--timeout must be finite and positive")
    if args.case and len(args.case) != 1:
        parser.error("--case must be supplied once")
    case = args.case[0] if args.case else None
    if args.replay and (args.profile or args.area or args.case or args.self_test):
        parser.error("--replay selects its own profile, area and case")
    if args.self_test and (args.profile or args.area or args.case or args.external_oracles or args.tonal_module):
        parser.error("--self-test only checks the independent oracle")
    if args.tonal_module and not args.external_oracles:
        parser.error("--tonal-module requires --external-oracles")
    if args.self_test:
        try:
            report = {"schema_version": 1, "gate": "PASS", "checks": references.self_test()}
        except ValueError as exc:
            report = {"schema_version": 1, "gate": "ERROR", "classification": "ORACLE_DEFECT",
                      "failed_checks": str(exc)}
        if args.json_out:
            write_report(args.json_out, report)
        print(json.dumps(report))
        return 3 if report["gate"] == "ERROR" else 0

    replay = None
    if args.replay:
        try:
            document = json.loads(args.replay.read_text(encoding="utf-8"))
            replay = document["payload"]
            area = replay["area"]
            oracle = references.PROFILE if area in references.AREAS else RANDOMIZED_ORACLE
            if (canonical_hash(replay) != document["sha256"] or replay["schema_version"] != 1
                    or replay["oracle_version"] != oracle
                    or area not in (*PROBES, *references.AREAS)
                    or not isinstance(replay["case_id"], str) or not isinstance(replay["input"], dict)
                    or "expected" not in replay):
                raise ValueError
        except (KeyError, OSError, TypeError, ValueError):
            parser.error("Invalid or unsupported audit replay payload")
    areas = tuple(dict.fromkeys(args.area)) if args.area else (
        (replay["area"],) if replay else references.AREAS if args.case else
        (*PROBES, *references.AREAS) if args.profile else tuple(PROBES)
    )
    if args.case and any(area not in references.AREAS for area in areas):
        parser.error("--case requires reference areas")
    try:
        provenance = checkout_provenance()
    except (ImportError, OSError, ValueError, subprocess.SubprocessError):
        report = {"schema_version": 1, "gate": "ERROR", "classification": "SETUP_ERROR",
                  "revision": None, "not_run_areas": areas}
        if args.json_out:
            write_report(args.json_out, report)
        print(json.dumps(report))
        return 3
    if replay is not None and args.timeout is not None:
        report = replay_with_deadline(replay, args.seed, args.timeout)
    else:
        report = run(args.seed, args.trials, areas, profile="replay" if replay else "full" if case else args.profile,
                     case=case, timeout=args.timeout, replay=replay, workers=args.workers)
    report.update(provenance)
    report["external_validation"] = "NOT_RUN"
    if args.external_oracles:
        from scripts import music_audit_oracles

        statuses = report["external_oracles"] = music_audit_oracles.run(args.tonal_module)
        outcomes = {result["status"] for result in statuses.values()}
        external = next((state for state in ("ERROR", "FAIL", "NOT_RUN") if state in outcomes), "PASS")
        report["external_validation"] = external
        if external == "ERROR":
            report["gate"] = "ERROR"
        elif report["gate"] == "PASS" and external != "PASS":
            report["gate"] = "FAIL"
    if args.json_out:
        write_report(args.json_out, report)
    print(f"Seed {args.seed}, {args.trials} questions per area")
    for area, counts in report["areas"].items():
        print(f"{area}: {counts['passed']} PASS, {counts['failed']} FAIL, "
              f"{counts['error']} ERROR, {counts['timeout']} TIMEOUT, {counts['not_run']} NOT RUN")
    for failure in report["failures"][:10]:
        print(json.dumps(failure, ensure_ascii=False))
    print(f"External validation: {report['external_validation']}")
    for name, result in report.get("external_oracles", {}).items():
        print(f"{name} {result['version']}: {result['status']} ({result['executed']}/{result['planned']})")
    if any(row["classification"] == "UNKNOWN_CASE" for row in report["failures"]):
        return 2
    return {"PASS": 0, "FAIL": 1, "ERROR": 3}[report["gate"]]


if __name__ == "__main__":
    raise SystemExit(main())
