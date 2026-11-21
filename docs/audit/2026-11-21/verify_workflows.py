"""Probe canonical chords through notation, session transposition, project and MIDI output."""
from collections import Counter
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import mido
from src.steps.progression import CANONICAL_PROGRESSIONS, ProgressionSession
from src.steps.theory.chord import parse_chord
from src.steps.theory.pitch import parse_spelling
from src.steps.theory.exceptions import MusicTheoryError

LETTERS = "CDEFGAB"
POSITIONS = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10)
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")
QUALITIES = {
    "": (0,4,7), "m": (0,3,7), "7": (0,4,7,10), "maj7": (0,4,7,11),
    "m7": (0,3,7,10), "m(maj7)": (0,3,7,11), "m6": (0,3,7,9),
    "m9": (0,3,7,10,14), "9": (0,4,7,10,14), "maj9": (0,4,7,11,14),
    "7(#11)": (0,4,7,10,18), "7(b9)": (0,4,7,10,13),
}
MATRIX = Path("knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md")


def spelling(symbol):
    match = re.fullmatch(r"([A-G])([#b]*)", symbol)
    index = LETTERS.index(match[1])
    return index, (POSITIONS[index] + match[2].count("#") - match[2].count("b")) % 12


def stated_degree(key, numeral, scale=POSITIONS):
    accidental, degree = re.match(r"([b#]*)([IViv]+)", numeral).groups()
    step = ROMAN.index(degree.upper())
    letter, tonic = spelling(key)
    return ((letter + step) % 7, (tonic + scale[step] + accidental.count("#") -
                                 accidental.count("b")) % 12)


def written_shape(session):
    key = parse_spelling(session.key_root, session.convention)
    results = []
    for symbol in session.chords:
        chord = parse_chord(symbol, session.convention)
        results.append(tuple((LETTERS.index(note.step) - LETTERS.index(key.step)) % 7
                             if note is not None else None for note in (chord.root, chord.bass)))
    return results


def sounding_shape(session):
    key = int(parse_spelling(session.key_root, session.convention).pitch_class)
    definitions = [parse_chord(symbol, session.convention) for symbol in session.chords]
    return [(sorted((tone - key) % 12 for tone in chord.pitch_class_set),
             (int(chord.root.pitch_class) - key) % 12,
             (int(chord.bass.pitch_class) - key) % 12 if chord.bass else None)
            for chord in definitions]


def midi_signature(path):
    midi = mido.MidiFile(path)
    return midi.ticks_per_beat, [
        [str(message) for message in track] for track in midi.tracks
    ]


def audit():
    tally = Counter()
    failures = []
    rows = {}
    for line in MATRIX.read_text().splitlines():
        if line.startswith("| `PROG-"):
            ident, name, roman, chords, *_ = [cell.strip().strip("`") for cell in line.split("|")[1:]]
            rows[ident] = (name, roman, chords)
    assert set(rows) == set(CANONICAL_PROGRESSIONS)

    with TemporaryDirectory(prefix="steps-workflow-audit-") as directory:
        temp = Path(directory)
        for ident, prog in sorted(CANONICAL_PROGRESSIONS.items()):
            name, roman, symbols = rows[ident]
            if (name, roman, symbols) != (prog.name, prog.roman_numerals, prog.chords_str):
                failures.append(dict(check="catalog_runtime_sync", id=ident))
            tally["catalog_runtime_sync_cases"] += 1
            chords = symbols.split(" - ")
            degrees = roman.split(" - ")
            assert len(chords) == len(degrees)
            key = prog.default_key.removesuffix("m")
            minor = prog.default_key.endswith("m")
            common_references = {"major", "minor"} if minor else {"major"}
            for position, (symbol, degree) in enumerate(zip(chords, degrees), 1):
                root, quality, bass = re.fullmatch(
                    r"([A-G][b#]*)([^/]*)(?:/([A-G][b#]*))?", symbol).groups()
                root_letter, root_pc = spelling(root)
                applied = re.search(r"/([b#]*[IViv]+)$", degree)
                matches = set()
                for reference, scale in (("major", POSITIONS), ("minor", MINOR)):
                    if reference == "minor" and not minor:
                        continue
                    expected_root = stated_degree(key, degree, scale)
                    if applied:
                        letter, pc = stated_degree(key, applied[1], scale)
                        expected_root = ((letter + 4) % 7, (pc + 7) % 12)
                    if (root_letter, root_pc) == expected_root:
                        matches.add(reference)
                common_references.intersection_update(matches)
                chord = parse_chord(symbol, "INT")
                expected_pc = {(root_pc + x) % 12 for x in QUALITIES[quality]}
                if not matches or expected_pc != chord.pitch_class_set:
                    failures.append(dict(check="catalog_root_or_tones", id=ident, position=position,
                                         chord=symbol, degree=degree))
                if bass:
                    bass_offset = (spelling(bass)[1] - root_pc) % 12
                    expected_bass = 4 if "(6/5)" in degree else 7 if "(4/3)" in degree else 3 if quality == "m" else 4
                    if bass_offset != expected_bass or chord.bass.pitch_class != spelling(bass)[1]:
                        failures.append(dict(check="catalog_inversion", id=ident, position=position,
                                             chord=symbol, degree=degree))
                    tally["catalog_inversions"] += 1
                tally["catalog_root_or_tones_cases"] += 1
            if minor and not common_references:
                failures.append(dict(check="catalog_mixed_minor_degree_references", id=ident,
                                     key=key, chords=chords, roman=roman))
            for distance in range(-5, 7):
                session = ProgressionSession(chords, key_root=key, is_minor=minor, bpm=108)
                session.set_chord_event_timing(0, 13, 777)
                start_sounding = sounding_shape(session)
                start_written = written_shape(session)
                session.transpose(distance)
                after_sounding = sounding_shape(session)
                after_written = written_shape(session)
                case = dict(id=ident, semitones=distance, key=session.key_root,
                            original=chords, observed=session.chords)
                if start_sounding != after_sounding:
                    failures.append(dict(check="transpose_sounding", **case))
                if start_written != after_written:
                    failures.append(dict(check="transpose_spelling", **case,
                                         before=start_written, after=after_written))
                tally["session_transpose_cases"] += 1

                int_path = temp / "int.mid"
                de_path = temp / "de.mid"
                session.export_midi_file(int_path)
                int_degree = [session.harmonic_degree_at(i) for i in range(len(chords))]
                session.set_notation_convention("DE")
                de_degree = [session.harmonic_degree_at(i) for i in range(len(chords))]
                if after_sounding != sounding_shape(session) or after_written != written_shape(session):
                    failures.append(dict(check="notation_harmonic_equivalence", **case))
                if int_degree != de_degree:
                    tally["localized_degree_text_cases"] += 1
                    failures_before = [left for left, right in zip(int_degree, de_degree) if left != right]
                    if any(not re.search(r"/[A-G][b#]*$", label) for label in failures_before):
                        failures.append(dict(check="unexpected_degree_text_change", **case,
                                             int_degree=int_degree, de_degree=de_degree))
                project = temp / "roundtrip.steps"
                session.save_to_file(project)
                reopened = ProgressionSession()
                reopened.load_from_file(project)
                if reopened.state != session.state:
                    failures.append(dict(check="project_roundtrip", **case))
                reopened.export_midi_file(de_path)
                if midi_signature(int_path) != midi_signature(de_path):
                    failures.append(dict(check="midi_equivalence", **case))
                tally["notation_storage_midi_cases"] += 1

    boundary = ProgressionSession(["C", "G/B"], key_root="C")
    boundary.transpose(-52)
    low = {"semitones": -52, "key": boundary.key_root, "chords": boundary.chords}
    try:
        low["analysis"] = boundary.harmonic_degree_at(0)
    except MusicTheoryError as error:
        low["error"] = f"{type(error).__name__}: {error}"
    desktop = ProgressionSession(["C", "G", "Am", "F"], key_root="C")
    original_degree = [desktop.harmonic_degree_at(i) for i in range(len(desktop.chords))]
    desktop.transpose(1)
    example = {"key": desktop.key_root, "chords": desktop.chords, "before": original_degree,
               "after": [desktop.harmonic_degree_at(i) for i in range(len(desktop.chords))]}
    return dict(main_window_example=example, counts=dict(tally), failures_by_check=dict(Counter(row["check"] for row in failures)),
                failures=failures, negative_octave_boundary=low)


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
