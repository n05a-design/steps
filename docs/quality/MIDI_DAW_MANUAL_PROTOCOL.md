# Manual Independent DAW MIDI Import Protocol

**Status:** Ready for manual import testing. Results are recorded below.

## Fixture set

Run from the repository root. The generator accepts a new directory and
writes six synthetic files and a SHA-256 manifest.

```sh
work=$(mktemp -d)
python3 -B -m scripts.generate_midi_daw_fixtures "$work/fixtures"
(cd "$work/fixtures" && shasum -a 256 -c SHA256SUMS)
```

The automated [Golden tests](../../tests/test_midi_golden_fixtures.py)
verify that the Format 1 cadence matches the pinned Golden hash and that the
tempo fixture matches the reference project export. All fixtures use PPQ 480.

| Fixture | Expected observations |
|---|---|
| `GOLD_01_ADR017_Format0.mid` | PPQ 480, 120 BPM, 4/4, one combined track, 20 notes across channels 1 and 2. |
| `GOLD_01_ADR017_Format1.mid` | Same timing and notes, with Conductor, Chords (16 notes) and Bass (4 notes). |
| `GOLD_09_Project_Format1.mid` | PPQ 480, tempo 120 → 90 → 120 at ticks 0, 1920 and 3360, and 12 chord notes. The project exporter writes the initial 4/4 signature. |
| `GOLD_09_Meter_Import_Probe.mid` | The separate import probe explicitly adds 3/4 at tick 1920 and 4/4 at tick 3360. This checks the DAW's handling of meter changes independently of the STEPS project export contract. |
| `ADR017_Overlap_Format0.mid` and `ADR017_Overlap_Format1.mid` | Two C-major events start on beat 1 and beat 3 of bar 1. Each of the five channel/pitch pairs has note-ons at ticks 0 and 960 and note-offs at ticks 1910 and 2870. Format 0 combines the events. Format 1 separates Chords (channel 1) and Bass (channel 2). |

## Required observations

Use a fresh empty document for each fixture. Import at the project start
and capture the import settings and any tempo or meter prompt. If the DAW
offers to import the tempo map, accept it for the tempo and meter cases.
Check the arrangement timeline and note editor. Compare the musical beat
positions if the DAW uses a different internal tick resolution.

For each named DAW/application and version:

- The file opens without repair or import warnings.
- PPQ or project time is displayed consistently.
- Note count matches the exported event count.
- No hanging notes or missing note-off events remain.
- Tempo points occur at the expected beats. In the tempo-only export the
  120 BPM return is at bar 2, beat 4. With the meter probe it is at bar 3, beat 1.
- Meter changes appear at the expected positions.
- MIDI channel and track structure match the documented export settings.
- Exported enharmonic spelling is not claimed as preserved by MIDI.

For the overlap probes, record the imported note starts and ends, whether
the DAW truncates or merges any notes, and whether playback stops cleanly.
Keep any observed import conversion tied to the DAW version and SMF format.

## Result recording

Record one status per application, version and fixture:

- `PASS` with application name, application version, OS, fixture SHA-256, date,
  reviewer, and screen or log evidence.
- `FAIL` with a concrete discrepancy and fixture.
- `NOT_RUN` with a reason.

Automated fixture decoding is a separate validation step. DAW acceptance
requires an observed import.

| Date | Application | Host | Fixtures | Status | Observation |
|---|---|---|---|---|---|
| 2026-11-21 | Ableton Live 11 Standard 11.3.43 | macOS 27.2.1 | All six | `NOT_RUN` | App launch timed out through Computer Use. Finder reported an AppleEvent timeout (`-1712`). No import window was available. |
| 2026-11-21 | Ableton Live 12 Beta 12.3.5b2 | macOS 27.2.1 | All six | `NOT_RUN` | App launch timed out through Computer Use. No import window was available. |
