# ADR-019: Live audio preview and physical MIDI input

**Status:** proposed
**Date:** 2026-11-26
**Decision owner / evidence:** Owner decision required. ADR-007 (accepted) limits v0.1 to file export; this ADR does **not** change that.

## Context

The keyboard (ADR-018) would benefit from hearing notes and from playing a physical MIDI keyboard. ADR-007 states: no in-app audio and no bundled soundfonts in v0.1; a virtual MIDI output port is an option for v0.2 that needs its own decision.

What exists today (verified on `cd455e3`):

- `src/steps/ports/audio.py`: `AudioBackendPort`, `NullAudioBackend`, `MonotonicPlaybackScheduler` (worker thread, T14 all-notes-off guarantees).
- `src/steps/midi/`: SMF export (ADR-017) – unaffected by this ADR.

Added on the ADR-018 branch as **specification + test adapters only**: `src/steps/ports/live.py` with `LiveNoteEvent`, `normalize_midi_message` (note-on velocity 0 → note-off, CC64 sustain, CC120/123), `MidiInputPort` protocol, `ScriptedMidiInput` (test double) and `NotePreviewService` over `AudioBackendPort`. No driver, synthesizer or dependency was added.

## Options

| Option | Platform | Latency | Quality | Dependencies / licence | Packaging | Offline | Maintenance |
|---|---|---|---|---|---|---|---|
| A. Keep file export only (status quo) | all | n/a | DAW | none | none | yes | none |
| B. OS MIDI **output** to a virtual port (IAC / loopMIDI) – DAW plays | macOS, Windows; Linux via ALSA | DAW-dependent, typically low | DAW instrument | e.g. `python-rtmidi` (MIT; bundles RtMidi, MIT-style) | native wheel per platform | yes | moderate |
| C. Physical MIDI **input** via same library | as B | low (driver) | n/a | as B | as B | yes | moderate; threading into Tk via `after_idle` |
| D. Built-in synthesizer with soundfont (e.g. FluidSynth) | needs native library per OS | low–moderate | depends on soundfont | LGPL library + soundfont licence chain (30–140 MB) | heavy, signing/notarisation impact | yes | high |
| E. Simple generated tones (sine/additive) via OS audio API | needs audio library (e.g. `sounddevice`/PortAudio) | low–moderate | poor (pedagogical only) | PortAudio (MIT) | native library | yes | moderate |

## Recommendation (not a decision)

1. Keep ADR-007 for v0.1/0.8.x.
2. Decide B and C together for a later milestone (proposed 0.9.3/0.9.4), because both use the same library and the existing port contract; require a licence review and a native packaging test first.
3. Do not adopt D until a soundfont with a clear redistribution licence and a size budget are approved.
4. Any adapter must: marshal driver-thread callbacks to the GUI thread; call `release_all()` on disconnect/focus loss; send all-notes-off on stop/close (T14).

## Consequences of not deciding

The keyboard stays silent; users hear chords through MIDI export in a DAW (UX-09 remains accepted). All keyboard features except sound and hardware input work.

## Links

[ADR-007](ADR-007-audio-nur-dateiexport-v01.md) · [ADR-017](ADR-017-midi-export-v01.md) · [ADR-018](ADR-018-music-keyboard-domain.md) · [Rights and release](../docs/governance/RIGHTS_SECURITY_AND_RELEASE.md)
