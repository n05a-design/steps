# Manual Independent DAW MIDI Import Protocol

**Status:** Proposed manual acceptance protocol. No DAW import is currently evidenced.

## Fixture set

Use the generated fixtures described in `tests/test_midi_golden_fixtures.py`:

1. `GOLD_01` basic four-chord progression.
2. `GOLD_09` multi-tempo and meter transitions.
3. One Format 0 export and one Format 1 export.

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
