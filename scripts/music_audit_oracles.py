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
}


def require_version(name, expected):
    if version(name) != expected:
        raise ValueError(f"Expected {name} {expected}")


def chord_cases():
    return [(root + quality, root, *aliases) for root in ROOTS for quality, aliases in QUALITIES.items()]


def compare_chords(oracle_rows):
    from src.steps.theory.chord import parse_chord

    return [
        {"input": symbol, "external": external, "steps": sorted(parse_chord(symbol, "INT").pitch_class_set)}
        for symbol, external in zip((row[0] for row in chord_cases()), oracle_rows, strict=True)
    ]


def music21_rows():
    require_version("music21", MUSIC21_VERSION)
    from music21.harmony import ChordSymbol

    return compare_chords([
        sorted({pitch.pitchClass for pitch in ChordSymbol(root.replace("b", "-") + suffix).pitches})
        for _, root, suffix, _ in chord_cases()
    ])


def tonal_rows(module: Path):
    package = json.loads((module / "package.json").read_text(encoding="utf-8"))
    if package.get("name") != "tonal" or package.get("version") != TONAL_VERSION:
        raise ValueError("Unexpected Tonal package identity or version")
    script = """
const fs = require('node:fs');
const { Chord, Note } = require(process.argv[1]);
const cases = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(cases.map(([_, root, , quality]) =>
  Chord.get(root + quality).notes.map(note => Note.chroma(note)).sort((a, b) => a - b))));
"""
    result = subprocess.run(["node", "-e", script, str(module.resolve())], check=True,
                            input=json.dumps(chord_cases()), encoding="utf-8", capture_output=True, timeout=15)
    return compare_chords(json.loads(result.stdout))


def mido_rows():
    require_version("mido", MIDO_VERSION)
    from mido import MidiFile
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
    return rows


def run(tonal_module: Path | None):
    specs = [
        ("music21", MUSIC21_VERSION, music21_rows, 84),
        ("mido", MIDO_VERSION, mido_rows, 16),
    ]
    results = {}
    if tonal_module is not None:
        specs.append(("tonal", TONAL_VERSION, lambda: tonal_rows(tonal_module), 84))
    else:
        results["tonal"] = {"version": TONAL_VERSION, "status": "NOT_RUN", "planned": 84,
                            "executed": 0, "reason": "No isolated Tonal module was selected."}
    for name, release, probe, planned in specs:
        try:
            rows = probe()
            if len(rows) != planned:
                raise ValueError("Unexpected oracle case count")
            differences = [row for row in rows if row["external"] != row["steps"]
                           or row.get("mido_roundtrip_steps", row["steps"]) != row["steps"]]
            results[name] = {"version": release, "status": "FAIL" if differences else "PASS",
                             "planned": planned, "executed": len(rows), "differences": differences}
        except Exception as exc:
            results[name] = {"version": release, "status": "ERROR", "planned": planned, "executed": 0,
                             "error": type(exc).__name__}
    return results
