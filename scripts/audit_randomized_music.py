"""Cross-check generated STEPS questions against independent, bounded musical oracles."""

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import partial
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_knowledge_adapter import citations_match_publication, published_citations
from src.steps.knowledge import KnowledgeAdapter
from src.steps.midi import SMFParser
from src.steps.progression import ProgressionSession, resolve_roman_degree
from src.steps.progression.voice_leading import optimize_smooth_voice_leading
from src.steps.theory.chord import parse_chord
from src.steps.theory.inversion import detect_chord_inversion

DEFAULT_SEED = 20261121
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

    def observe():
        chord = parse_chord(symbol, convention)
        return [chord.root.step, int(chord.root.pitch_class), chord.quality,
                chord.bass.step, int(chord.bass.pitch_class), sorted(chord.pitch_class_set)]

    return Trial({"chord": symbol, "notation": convention}, expected, observe)


def inversion_trial(rng, _adapter, _directory):
    quality = rng.choice(tuple(SEVENTHS))
    root = rng.randrange(12)
    inversion = rng.randrange(4)
    pitches = [(root + interval) % 12 for interval in SEVENTHS[quality]]
    bass = pitches[inversion]
    notes = [36 + bass] + [rng.choice((60, 72, 84)) + pc for pc in pitches if pc != bass]
    rng.shuffle(notes)
    expected = [root, bass, ("7", "6/5", "4/3", "4/2")[inversion], True]

    def observe():
        result = detect_chord_inversion(notes)
        return [result.root_pc, result.bass_pc, result.figured_bass, result.is_seventh_chord]

    return Trial({"notes": notes, "quality": quality}, expected, observe)


def degree_trial(rng, _adapter, _directory):
    index, convention = note_context(rng)
    tonic = rng.choice(NOTES)
    minor = rng.choice((False, True))
    position = rng.randrange(7)
    numeral = (MINOR_DEGREES if minor else MAJOR_DEGREES)[position]
    quality = (MINOR_QUALITIES if minor else MAJOR_QUALITIES)[position]
    pc = (tonic[3] + (MINOR if minor else MAJOR)[position]) % 12
    letter = LETTERS[(LETTERS.index(tonic[2]) + position) % 7]

    def observe():
        chord = resolve_roman_degree(numeral, tonic[index], minor, convention=convention,
                                     minor_accidentals="natural_minor")
        return [chord.root.step, int(chord.root.pitch_class), chord.quality, sorted(chord.pitch_class_set)]

    return Trial({"tonic": tonic[index], "minor": minor, "degree": numeral, "notation": convention},
                 [letter, pc, quality, tones(pc, quality)], observe)


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

    def observe():
        session = ProgressionSession([symbol], key_root=tonic[index], convention=notation, is_minor=minor)
        label = session.harmonic_degree_at(0)
        rebuilt = resolve_roman_degree(label, tonic[index], minor, convention=notation, minor_accidentals="natural_minor")
        return [label, rebuilt.root.step, sorted(rebuilt.pitch_class_set)]

    numeral = ("I", "II", "III", "IV", "V", "VI", "VII")[position]
    return Trial({"chord": symbol, "tonic": tonic[index], "minor": minor, "notation": notation},
                 [f"{numeral}dom{quality}", letter, expected_pcs], observe)


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

    def observe():
        session = ProgressionSession(chords, key_root=root[index], convention=convention)
        session.set_chord_event_timing(0, *timing)
        session.transpose(distance)
        first, following = (parse_chord(symbol, convention) for symbol in session.chords)
        tonic = parse_chord(session.key_root, convention).root
        written = [(LETTERS.index(note.step) - LETTERS.index(tonic.step)) % 7 for note in (first.root, first.bass, following.root)]
        return [int(tonic.pitch_class), int(first.root.pitch_class), int(first.bass.pitch_class),
                int(following.root.pitch_class), written, [first.quality, following.quality], list(session.get_chord_event_timing(0))]

    return Trial({"chords": chords, "key": root[index], "distance": distance, "notation": convention,
                  "event": timing}, expected, observe)


def voice_leading_trial(rng, _adapter, _directory):
    source = sorted(rng.sample(range(48, 73), 3))
    root = rng.randrange(12)
    target = {(root + offset) % 12 for offset in rng.choice(tuple(TRIADS.values()))}
    bass = rng.choice(sorted(target))
    windows = [[note for note in range(center - 12, center + 13) if note % 12 in target] for center in source]

    def cost(notes):
        return sum(abs(before - after) for before, after in zip(source, notes, strict=True))

    expected = min(cost(notes) for notes in product(*windows)
                   if notes[0] < notes[1] < notes[2] and notes[0] % 12 == bass
                   and {note % 12 for note in notes} == target)

    def observe():
        notes = optimize_smooth_voice_leading(source, target, bass)
        valid = (len(notes) == len(set(notes)) == 3 and notes == sorted(notes) and notes[0] % 12 == bass
                 and {note % 12 for note in notes} == target
                 and all(abs(a - b) <= 12 for a, b in zip(source, notes, strict=True)))
        return [valid, cost(notes)]

    return Trial({"from": source, "pitch_classes": sorted(target), "bass": bass}, [True, expected], observe)


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
    expected = [fmt, 1 if fmt == 0 else 3, [(start, length)] * 5, expected_chord_pcs, [36 + bass[3]]]

    def observe():
        session = ProgressionSession([symbol], convention=convention)
        session.set_chord_event_timing(0, start, duration)
        path = session.export_midi_file(directory / "probe.mid", note_duration_mode=mode, smf_format=fmt)
        decoded = SMFParser.parse(path.read_bytes())
        return [decoded.format, decoded.num_tracks,
                [(note.start_tick, note.duration_ticks) for note in decoded.all_notes],
                sorted(note.pitch % 12 for note in decoded.all_notes if note.channel == 0),
                [note.pitch for note in decoded.all_notes if note.channel == 1]]

    return Trial({"chord": symbol, "event": (start, duration), "duration_mode": mode, "smf": fmt,
                  "notation": convention}, expected, observe)


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

    def observe():
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

    return Trial({"query": query, "notation": notation},
                 [status, bool(claims), claims, sources, True, True], observe)


PROBES = {
    "chords": chord_trial, "inversions": inversion_trial, "degrees": degree_trial,
    "degree-roundtrip": degree_roundtrip_trial, "transposition": transposition_trial, "voice-leading": voice_leading_trial,
    "midi": midi_trial, "retrieval": retrieval_trial,
}


def run(seed, trials, areas=tuple(PROBES)):
    failures = []
    adapter = KnowledgeAdapter() if "retrieval" in areas else None
    with TemporaryDirectory(prefix="steps-musical-audit-") as temp:
        for area in areas:
            rng = random.Random(f"{seed}:{area}")
            probe = PROBES[area]
            if area == "retrieval":
                probe = partial(probe, published=published_citations())
            for index in range(trials):
                trial = probe(rng, adapter, Path(temp))
                try:
                    actual = trial.observe()
                except Exception as exc:
                    actual = {"error": type(exc).__name__, "message": str(exc)}
                if trial.expected != actual:
                    failures.append({"area": area, "trial": index + 1, "question": trial.question,
                                     "expected": trial.expected, "actual": actual})
    failed_by_area = Counter(failure["area"] for failure in failures)
    return {"seed": seed, "python_version": sys.version.split()[0], "trials_per_area": trials,
            "areas": {area: {"passed": trials - failed_by_area[area], "failed": failed_by_area[area]} for area in areas},
            "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--trials", type=int, default=128, help="Number of questions per area.")
    parser.add_argument("--area", action="append", choices=PROBES, help="Repeat to select multiple areas.")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be positive")
    report = run(args.seed, args.trials, tuple(dict.fromkeys(args.area)) if args.area else tuple(PROBES))
    report["revision"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    report["tracked_changes"] = bool(subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT,
    ))
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Seed {args.seed}, {args.trials} questions per area")
    for area, counts in report["areas"].items():
        print(f"{area}: {counts['passed']} PASS, {counts['failed']} FAIL")
    for failure in report["failures"][:10]:
        print(json.dumps(failure, ensure_ascii=False))
    return int(bool(report["failures"]))


if __name__ == "__main__":
    raise SystemExit(main())
