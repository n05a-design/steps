# ADR-018: Central music keyboard – domain contract and integration

**Status:** proposed
**Date:** 2026-11-26
**Decision owner / evidence:** Owner decision pending. Prepared on branch `feat/steps-music-keyboard-interactive-engine` (base `cd455e31bc25b87b33634d2feea40453deaf67e7`); implementation report: [`docs/audit/2026-11-26/MUSIC_KEYBOARD_REPORT.md`](../docs/audit/2026-11-26/MUSIC_KEYBOARD_REPORT.md).

> This ADR is a proposal. The implementation exists on a branch so the owner can review it, but the decision itself is **not accepted** until the owner says so.

## Context

STEPS has a tested theory core (`src/steps/theory`), a progression session with undo/redo (`src/steps/progression/session.py`) and several analysis views (Next Chord Explorer, Voice Leading Lab). There is no common place where chords, scales, voicings, input and practice meet on an instrument. A parallel workstream develops Glide Shell and Glide Bento; STEPS must not compete with that UI framework.

Alternatives considered:

1. **Draw a piano inside the existing piano roll.** Rejected: the piano roll is a time/pitch plot; it has no key identity, spelling or input model.
2. **Put keyboard logic into the Tk widget.** Rejected: violates AGENTS.md rule 4 and could not be reused by Bento.
3. **Separate pure keyboard domain + thin Tk view (chosen proposal).**

## Proposed decision

1. A new pure package `src/steps/keyboard/` (no `tkinter`, `glide_shell` or `app` imports, enforced by `tests/test_glide_shell_integration.py`) contains:
   - `model` – 88-key piano (A0 = MIDI 21 … C8 = MIDI 108), key identity, viewport; MIDI 0–127 remains the general domain;
   - `chord_tones` – roles (root, 3rd, 7th, 9th, …) of the existing `CHORD_TEMPLATES` intervals, contextual spelling via `NoteSpelling.transpose_diatonic`, voicing labels via `detect_chord_inversion`;
   - `state` – semantic key states, a fixed fill priority and a renderer-neutral `KeyboardViewModel`;
   - `recognition` – ambiguity-aware chord recognition (all supported readings with reasons, no confidence numbers);
   - `voice_motion` – comparison of two concrete voicings (register pairing only for equal voice counts);
   - `input` – pressed vs. selected notes, one entry point for virtual and future physical input;
   - `practice` – exercise contract, per-type scoring policies and a six-exercise pilot marked `AI_DRAFT_UNREVIEWED`;
   - `workbench` – UI-free controller that reads the leading `ProgressionSession` through a provider.
2. Physical key identity, sounding pitch, written spelling, musical meaning and visual state are separate data. A key never derives its spelling from its MIDI number alone.
3. The keyboard **reads** the project. Previews (voicing type, inversion rotation, scale overlay, comparison, practice) never write session state. The only project change offered is "add recognised chord", which uses the existing undoable `ProgressionSessionController.add_chord`.
4. The desktop integration is a modal dialog (`app/ui/keyboard_dialog.py`) reachable from the Tools menu and the sidebar, consistent with ADR-001 ("separate modal/inspector only when needed") and the Voice Leading Lab precedent. No window architecture, theme system or Glide Shell file changes.
5. Glide Bento integration later replaces only `app/ui/keyboard_view.py` / `keyboard_dialog.py`; the handoff contract is [`docs/architecture/KEYBOARD_ARCHITECTURE.md`](../docs/architecture/KEYBOARD_ARCHITECTURE.md) §8.

## Consequences

- No new dependency, asset, soundfont or schema change; project files are unchanged (`schema_version` untouched).
- Recognition returns several readings for symmetric or overlapping sets (C6/Am7, dim7, aug, sus2/sus4). Users see that ambiguity; the order is deterministic, not a truth ranking.
- Practice content is an unreviewed AI draft and must not be published or labelled as approved before human music-theory review (OA-0038 style acceptance).
- Rollback: remove the menu/sidebar entries and the `src/steps/keyboard` package; no data migration is involved.

## Links

- [ADR-001](ADR-001-ein-fenster-zwei-bereiche.md), [ADR-007](ADR-007-audio-nur-dateiexport-v01.md), [ADR-014](ADR-014-theorie-perspektiven-und-kontext.md), [ADR-015](ADR-015-kernvertraege-intervalle-voicing-notation.md), [ADR-019](ADR-019-live-audio-preview-and-midi-input.md)
