"""Opt-in comparisons with isolated external libraries and synthetic inputs."""

from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from scripts.music_audit_references import ROOTS

MIDO_VERSION = "1.3.3"
MUSIC21_VERSION = "10.5.2"
TONAL_VERSION = "6.16.0"
# Explicit support mapping for the shared basic chord vocabulary.
QUALITIES = {
    "": ("", "M"), "m": ("m", "m"), "dim": ("dim", "dim"), "aug": ("aug", "aug"),
    "maj7": ("maj7", "maj7"), "7": ("7", "7"), "m7": ("m7", "m7"),
    "m7b5": ("m7b5", "m7b5"), "dim7": ("dim7", "dim7"),
    "m(maj7)": ("mM7", "mMaj7"), "7#5": ("7#5", "7#5"),
    "7#9": ("7#9", "7#9"), "7#11": ("7#11", "7#11"),
    "7b13": ("7b13", "7b13"), "13": ("13", "13"),
}
# Measured comparator conventions. List added and omitted pitch classes relative
# to the tonic, and require the entire difference to match on every root.
PROFILE_DIFFERENCES = {
    ("music21", "13"): ({5}, set()),
    ("tonal", "7b13"): (set(), {7}),
}
MODES = {
    "ionian": ("MajorScale", "major"), "dorian": ("DorianScale", "dorian"),
    "phrygian": ("PhrygianScale", "phrygian"), "lydian": ("LydianScale", "lydian"),
    "mixolydian": ("MixolydianScale", "mixolydian"), "aeolian": ("MinorScale", "aeolian"),
    "locrian": ("LocrianScale", "locrian"),
}


def require_version(name, expected):
    if version(name) != expected:
        raise ValueError(f"Expected {name} {expected}")


def chord_cases():
    return [(root + quality, root, *aliases, quality)
            for root in ROOTS for quality, aliases in QUALITIES.items()]


def scale_cases():
    return [(root, mode, *aliases) for root in ROOTS for mode, aliases in MODES.items()]


def compare_scales(oracle_rows):
    from src.steps.theory.pitch import parse_spelling
    from src.steps.theory.scale import construct_scale

    rows = []
    for (root, mode, *_), external in zip(scale_cases(), oracle_rows, strict=True):
        scale = construct_scale(parse_spelling(root, "INT"), mode)
        observed = [[int(note.pitch_class), note.render("INT").rstrip("0123456789").replace("x", "##")]
                    for note in scale.spellings]
        rows.append({"input": {"root": root, "mode": mode}, "external": external, "steps": observed})
    return rows


def compare_chords(oracle_rows, oracle):
    from src.steps.theory.chord import parse_chord

    rows = []
    for (symbol, _, _, _, quality), external in zip(chord_cases(), oracle_rows, strict=True):
        chord = parse_chord(symbol, "INT")
        steps = set(chord.pitch_class_set)
        observed = set(external)
        row = {"input": symbol, "external": external, "steps": sorted(steps)}
        if (oracle, quality) in PROFILE_DIFFERENCES:
            extra, absent = PROFILE_DIFFERENCES[oracle, quality]
            root = int(chord.root.pitch_class)
            additions = {(root + factor) % 12 for factor in extra}
            omissions = {(root + factor) % 12 for factor in absent}
            row["expected_profile_difference"] = observed - steps == additions and steps - observed == omissions
        rows.append(row)
    return rows


def music21_rows():
    require_version("music21", MUSIC21_VERSION)
    from music21 import scale
    from music21.harmony import ChordSymbol

    chords = compare_chords([
        sorted({pitch.pitchClass for pitch in ChordSymbol(root.replace("b", "-") + suffix).pitches})
        for _, root, suffix, _, _ in chord_cases()
    ], "music21")
    scales = []
    for root, _, name, _ in scale_cases():
        pitches = getattr(scale, name)(root.replace("b", "-") + "4").pitches
        if len(pitches) != 8 or pitches[-1].midi - pitches[0].midi != 12:
            raise ValueError("Expected a seven-degree scale and its octave")
        scales.append([[pitch.pitchClass, pitch.name.replace("-", "b")] for pitch in pitches[:-1]])
    return chords + compare_scales(scales)


def tonal_rows(module: Path):
    package = json.loads((module / "package.json").read_text(encoding="utf-8"))
    if package.get("name") != "tonal" or package.get("version") != TONAL_VERSION:
        raise ValueError("Unexpected Tonal package identity or version")
    script = """
const fs = require('node:fs');
const { Chord, Scale, Note } = require(process.argv[1]);
const { chords, scales } = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify({
  chords: chords.map(([_, root, , quality]) =>
    Chord.get(root + quality).notes.map(Note.chroma).sort((a, b) => a - b)),
  scales: scales.map(([root, , , mode]) =>
    Scale.get(root + ' ' + mode).notes.map(note => [Note.chroma(note), note]))
}));
"""
    result = subprocess.run(["node", "-e", script, str(module.resolve())], check=True,
                            input=json.dumps({"chords": chord_cases(), "scales": scale_cases()}),
                            encoding="utf-8", capture_output=True, timeout=15)
    decoded = json.loads(result.stdout)
    return compare_chords(decoded["chords"], "tonal") + compare_scales(decoded["scales"])


def mido_rows():
    require_version("mido", MIDO_VERSION)
    from mido import Message, MetaMessage, MidiFile, MidiTrack
    from src.steps.midi import SMFParser
    from src.steps.progression import ProgressionSession

    def from_mido(file):
        tracks = []
        for track in file.tracks:
            tick = 0
            events = []
            for event in track:
                tick += event.time
                if event.type in ("note_on", "note_off"):
                    events.append([tick, event.type, event.channel, event.note, event.velocity])
                elif event.type == "set_tempo":
                    events.append([tick, "tempo", event.tempo])
                elif event.type == "time_signature":
                    events.append([tick, "meter", event.numerator, event.denominator])
            tracks.append([track.name, events])
        return [file.type, file.ticks_per_beat, tracks]

    def from_steps(data):
        file = SMFParser.parse(data)
        tracks = []
        for track in file.tracks:
            events = []
            for event in track.events:
                if event.event_type in ("note_on", "note_off"):
                    events.append([event.abs_tick, event.event_type, event.channel, event.data1, event.data2])
                elif event.meta_type == 0x51:
                    events.append([event.abs_tick, "tempo", int.from_bytes(event.meta_data, "big")])
                elif event.meta_type == 0x58:
                    events.append([event.abs_tick, "meter", event.meta_data[0], 2 ** event.meta_data[1]])
            tracks.append([track.name, events])
        return [file.format, file.division, tracks]

    rows = []
    with TemporaryDirectory(prefix="steps-mido-") as temporary:
        for fmt in (0, 1):
            for mode in ("FIXED_GAP", "PERCENT_95"):
                for symbol in ("C/E", "G7/D", "Am", "Cmaj7"):
                    session = ProgressionSession([symbol, "F"], key_root="C", convention="INT")
                    session.set_chord_event_timing(0, 120, 480)
                    session.set_chord_event_timing(1, 730, 390)
                    target = Path(temporary) / "probe.mid"
                    session.export_midi_file(target, smf_format=fmt, note_duration_mode=mode)
                    data = target.read_bytes()
                    mido_file = MidiFile(file=BytesIO(data))
                    rewritten = BytesIO()
                    mido_file.save(file=rewritten)
                    external = from_mido(mido_file)
                    actual = from_steps(data)
                    rows.append({"input": {"format": fmt, "mode": mode, "symbol": symbol},
                                 "external": external, "steps": actual,
                                 "mido_roundtrip_steps": from_steps(rewritten.getvalue())})
    # Generate independently in the other direction. The event stream spans
    # nonzero deltas, a tempo and meter change, and repeated pitches on channels.
    for ppq, channels in ((96, (0, 15)), (480, (2, 9))):
        conductor = MidiTrack([
            MetaMessage("track_name", name="Conductor"),
            MetaMessage("set_tempo", tempo=500000),
            MetaMessage("set_tempo", tempo=750000, time=ppq),
            MetaMessage("time_signature", numerator=7, denominator=8, time=ppq),
        ])
        streams = [MidiTrack([
            MetaMessage("track_name", name=f"Channel {channel + 1}"),
            Message("note_on", channel=channel, note=60, velocity=76, time=127),
            Message("note_on", channel=channel, note=60, velocity=85, time=128),
            Message("note_off", channel=channel, note=60, velocity=64, time=128),
            Message("note_off", channel=channel, note=60, velocity=0, time=16384),
        ]) for channel in channels]
        source = MidiFile(type=1, ticks_per_beat=ppq, tracks=[conductor, *streams])
        stream = BytesIO()
        source.save(file=stream)
        rows.append({"input": {"writer": "mido", "ppq": ppq, "channels": channels},
                     "external": from_mido(source), "steps": from_steps(stream.getvalue())})
    return rows


def run(tonal_module: Path | None):
    theory_cases = len(chord_cases()) + len(scale_cases())
    specs = [
        ("music21", MUSIC21_VERSION, music21_rows, theory_cases),
        ("mido", MIDO_VERSION, mido_rows, 18),
    ]
    results = {}
    if tonal_module is not None:
        specs.append(("tonal", TONAL_VERSION, lambda: tonal_rows(tonal_module), theory_cases))
    else:
        results["tonal"] = {"version": TONAL_VERSION, "status": "NOT_RUN", "planned": theory_cases,
                            "executed": 0, "reason": "No isolated Tonal module was selected."}
    for name, release, probe, planned in specs:
        try:
            rows = probe()
            if len(rows) != planned:
                raise ValueError("Unexpected oracle case count")
            declared = [row for row in rows if row.get("expected_profile_difference")]
            differences = [row for row in rows if not row.get("expected_profile_difference") and (
                row["external"] != row["steps"] or row.get("expected_profile_difference") is False
                or row.get("mido_roundtrip_steps", row["steps"]) != row["steps"]
            )]
            results[name] = {"version": release, "status": "FAIL" if differences else "PASS",
                             "planned": planned, "executed": len(rows), "differences": differences,
                             "expected_profile_differences": declared}
        except Exception as exc:
            results[name] = {"version": release, "status": "ERROR", "planned": planned, "executed": 0,
                             "error": type(exc).__name__}
    return results
