"""Generate deterministic MIDI probes for the independent DAW import protocol."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from typing import Literal

from src.steps.midi import MidiExportService, MidiFile
from src.steps.progression.session import ProgressionSession
from src.steps.storage.project_io import Project


def generate_fixtures(destination: Path) -> Path:
    """Write the synthetic fixtures and their checksum manifest into a new directory."""
    destination.mkdir()
    cadence = ProgressionSession(initial_chords=["C", "F", "G", "C"])
    overlapping = ProgressionSession(initial_chords=["C", "C"])
    overlapping.set_chord_event_timing(1, 960, 1920)
    formats: tuple[Literal[0, 1], ...] = (0, 1)
    for smf_format in formats:
        cadence.export_midi_file(
            destination / f"GOLD_01_ADR017_Format{smf_format}.mid",
            smf_format=smf_format,
        )
        overlapping.export_midi_file(
            destination / f"ADR017_Overlap_Format{smf_format}.mid",
            smf_format=smf_format,
        )

    timeline = Project(
        title="Multi-Tempo and Meter Progression",
        notation_convention="INT",
        time_settings={
            "ppq": 480,
            "time_signature": {"numerator": 4, "denominator": 4},
            "tempo_bpm": 120.0,
            "tempo_points": [
                {"start_tick": tick, "bpm": bpm}
                for tick, bpm in ((0, 120.0), (1920, 90.0), (3360, 120.0))
            ],
        },
        tracks=[
            {
                "track_id": "trk_chords",
                "track_type": "CHORDS",
                "name": "Chords Track",
                "channel": 0,
                "events": [
                    {"start_tick": tick, "duration_ticks": duration, "payload": symbol}
                    for tick, duration, symbol in (
                        (0, 1920, "Cmaj7"), (1920, 1440, "Fmaj7"), (3360, 1920, "Cmaj7"),
                    )
                ],
            }
        ],
    )
    project_path = destination / "GOLD_09_Project_Format1.mid"
    MidiExportService.export_project_to_smf(timeline, project_path, smf_format=1)
    meter_probe = MidiFile.from_bytes(project_path.read_bytes())
    meter_probe.tracks[0].add_time_signature(1920, 3, 4)
    meter_probe.tracks[0].add_time_signature(3360, 4, 4)
    meter_probe.save(destination / "GOLD_09_Meter_Import_Probe.mid")

    manifest = destination / "SHA256SUMS"
    manifest.write_text(
        "".join(
            f"{sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
            for path in sorted(destination.glob("*.mid"))
        ),
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new directory for the fixtures")
    manifest = generate_fixtures(parser.parse_args().destination)
    print(manifest)


if __name__ == "__main__":
    main()
