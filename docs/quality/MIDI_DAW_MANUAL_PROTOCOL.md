# Manual Independent DAW MIDI Import Protocol

**Status:** Proposed manual acceptance protocol. No DAW import is currently evidenced.

## Fixture set

Generate the fixtures from the repository root. They use the input definitions
in [the Golden tests](../../tests/test_midi_golden_fixtures.py).

```sh
fixtures=$(mktemp -d)
python3 -B - "$fixtures" <<'PY'
from pathlib import Path
import sys

from src.steps.midi import MidiFile
from src.steps.midi.export_service import MidiExportService
from src.steps.progression.session import ProgressionSession
from tests.test_midi_golden_fixtures import GOLDEN_PROGRESSIONS, TestMidiGoldenFixtures

out = Path(sys.argv[1])
cadence, timeline = (
    next(item for item in GOLDEN_PROGRESSIONS if item["id"].startswith(prefix))
    for prefix in ("GOLD_01_", "GOLD_09_")
)
session = ProgressionSession(initial_chords=cadence["chords"])
for mode in (0, 1):
    session.export_midi_file(out / f"GOLD_01_ADR017_Format{mode}.mid", smf_format=mode)
project = TestMidiGoldenFixtures()._build_project_from_golden(timeline)
path = out / "GOLD_09_Project_Format1.mid"
MidiExportService.export_project_to_smf(project, path, smf_format=1)
probe = MidiFile.from_bytes(path.read_bytes())
probe.tracks[0].add_time_signature(1920, 3, 4)
probe.tracks[0].add_time_signature(3360, 4, 4)
probe.save(out / "GOLD_09_Meter_Import_Probe.mid")
PY
shasum -a 256 "$fixtures"/*.mid
```

| Fixture | Expected observations |
|---|---|
| `GOLD_01_ADR017_Format0.mid` | PPQ 480, 120 BPM, 4/4, one combined track, 20 notes across channels 1 and 2. |
| `GOLD_01_ADR017_Format1.mid` | Same timing and notes, with Conductor, Chords (16 notes) and Bass (4 notes). |
| `GOLD_09_Project_Format1.mid` | PPQ 480, tempo 120 → 90 → 120 at ticks 0, 1920 and 3360, and 12 chord notes. The project exporter writes the initial 4/4 signature. |
| `GOLD_09_Meter_Import_Probe.mid` | The separate import probe explicitly adds 3/4 at tick 1920 and 4/4 at tick 3360. This checks the DAW's handling of meter changes independently of the STEPS project export contract. |

## Required observations

For each named DAW/application and version:

- The file opens without repair or import warnings.
- PPQ or project time is displayed consistently.
- Note count matches the exported event count.
- No hanging notes or missing note-off events remain.
- Tempo points occur at the expected bars/ticks.
- Meter changes appear at the expected positions.
- MIDI channel and track structure match the documented export settings.
- Exported enharmonic spelling is not claimed as preserved by MIDI.

## Result recording

Record only one of:

- `PASS` with application name, application version, OS, fixture SHA-256, date,
  reviewer, and screen or log evidence.
- `FAIL` with a concrete discrepancy and fixture.
- `NOT_RUN` with a reason.

Do not infer DAW acceptance from automated SMF parsing or loss-report tests.
