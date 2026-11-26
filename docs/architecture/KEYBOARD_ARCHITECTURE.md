# Music keyboard – architecture, contracts and Bento handoff

**Status:** implemented on branch `feat/steps-music-keyboard-interactive-engine` (base `cd455e3`); ADR [018](../../decisions/ADR-018-music-keyboard-domain.md) and [019](../../decisions/ADR-019-live-audio-preview-and-midi-input.md) are **proposed**, not accepted. Automated tests exist; human music-theory review, native accessibility review and owner approval are outstanding.
**Language:** English (AGENTS.md rule 12).

## 1. Layers

```
app/ui/keyboard_dialog.py   Tk dialog: controls, text, event binding      (presentation)
app/ui/keyboard_view.py     Tk canvas: draws a KeyboardViewModel           (presentation)
        │  reads only KeyboardViewModel / KeyVisual / KeyState
        ▼
src/steps/keyboard/workbench.py   UI-free controller + transient state     (mediation)
        │  reads ProgressionSession via provider; never writes it
        ▼
src/steps/keyboard/{model,chord_tones,state,recognition,voice_motion,input,practice}.py   (domain)
        │  reuse
        ▼
src/steps/theory/*  src/steps/progression/*  src/steps/ports/{audio,live}.py   (core + ports)
```

Rules (tested):

- `src/steps/**` imports no `tkinter`, `glide_shell` or `app` (`tests/test_glide_shell_integration.py`).
- `app/ui/keyboard_view.py` imports only `src.steps.keyboard.model` and `.state` from the music side (`tests/test_keyboard_dialog.py`), so the view cannot compute harmony.
- The only project mutation from the keyboard is `ProgressionSessionController.add_chord` (undoable).

## 2. Reuse matrix (inventory of `cd455e3`)

| Function | Existing module | Implementation | Status / tests | Reuse | Gap closed here | Reason |
|---|---|---|---|---|---|---|
| Pitch, MIDI, octave, A4 = 440 Hz | `theory/pitch.py` | `NoteSpelling.midi_number`, `midi_to_frequency` | `test_theory_core.py`, golden T01–T16 | direct | 88-key range, key numbers, black/white, viewport (`keyboard/model.py`) | core has MIDI 0–127 only |
| Pitch class | `theory/pitch.py` | `PitchClass` | `test_theory_core.py` | direct | – | – |
| Spelling, enharmonics, DE/INT | `theory/pitch.py` | `NoteSpelling.render`, `parse_spelling`, `transpose_diatonic` | `test_notation_contract.py`, `test_transpose_diatonic_strict.py` | direct | enharmonic list per key, `spell_at` (same letter, new octave) | keys needed all spellings of one pitch |
| Interval | `theory/interval.py` | `DiatonicInterval`, `directed_semitones` | `test_theory_core.py` | direct (`voice_motion`) | – | – |
| Chord qualities | `theory/chord.py` | `CHORD_TEMPLATES` (31 qualities, unreduced intervals) | `test_voicing_contract.py`, golden | direct | **role names** for each interval (`chord_tones.py`) | core stored semitones only |
| Chord symbol parse/print | `theory/chord.py` | `parse_chord`, `ChordDefinition.symbol` (INT) | `test_theory_core.py` | direct | DE rendering of a `ChordDefinition` (`render_chord_symbol`) | `.symbol` is INT only; session renders DE inline |
| Voicing types | `theory/chord.py` | `ChordDefinition.to_voicing` CLOSE/DROP2/SHELL/ROOTLESS, `Voicing.invert` | `test_voicing_contract.py`, `test_shell_voicings.py` | direct | labelling of each MIDI note (`label_voicing`) | – |
| Inversion / figured bass | `theory/inversion.py` | `detect_chord_inversion` | `test_chord_inversion.py` | direct | – | – |
| Progression voicings | `progression/session.py` | `ProgressionSession.get_voicings` (voice-led) | `test_progression_engine.py` | direct (keyboard shows exactly these) | – | single source of truth |
| Voice leading | `theory/voice_leading.py`, `progression/voice_leading.py` | `classify_voice_motion`, `absolute_semitone_distance` | `test_voice_leading_styles.py` | direct | per-voice HELD/SEMITONE/WHOLE_TONE/LEAP, unpaired sets (`voice_motion.py`) | lab reports only signed steps |
| Scales / modes | `theory/scale.py` | 15 `SCALE_TEMPLATES`, `construct_scale` | `test_scale.py` | direct | scale overlay layer | – |
| Harmonic function | `progression/harmony_analysis.py` | `format_harmonic_degree` via `session.harmonic_degree_at` | `test_harmonic_function_accuracy.py` | direct (shown as degree) | – | – |
| Chord recognition | – (only root deduction inside `inversion._deduce_triad_or_seventh_root`, single answer) | – | – | none | `recognition.py` returns **all** readings with reasons | existing helper picks one root; ambiguity must be kept |
| Session, undo/redo, save/load | `progression/session.py`, `storage/undo.py`, `app/ui/session_controller.py` | `ProgressionSession`, `UndoStack`, controller listeners | `test_vertical_slice_progression.py`, `test_desktop_project_workflow.py` | direct (read + `add_chord`) | `remove_listener` on the controller | dialogs must not leak listeners |
| Audio | `ports/audio.py` | `AudioBackendPort`, `NullAudioBackend`, scheduler | `test_audio_transport_ports.py` | adapter | `NotePreviewService` (`ports/live.py`) | note on/off without hung notes |
| MIDI input | – | – | – | – | `LiveNoteEvent`, `normalize_midi_message`, `MidiInputPort`, `ScriptedMidiInput` | spec only (ADR-019) |
| MIDI export | `midi/export_service.py` | ADR-017 export | `test_midi_export_service.py`, golden SHA | untouched | – | must stay regression-free |
| Knowledge library | `knowledge/adapter.py`, `knowledge/` | `KnowledgeAdapter` | `test_knowledge_adapter.py` | referenced only (`Exercise.knowledge_refs` = module ids) | – | no parallel library; see §7 |
| Localization | `app/i18n.py`, `app/locales/*.json` | `LocaleManager` | `test_i18n.py` | direct | 141 keys EN/DE | – |

## 3. Data contracts

**Physical key** – `PianoKey(midi, number 1..88 | None, octave, pitch_class, is_black)`. `number` is `None` for valid MIDI notes outside A0–C8.

**Sounding pitch** – the MIDI integer; frequency from the core (`A4 = 440 Hz`).

**Written spelling** – `NoteSpelling`, always from context: chord (`chord_tones`), scale (`ScaleDefinition.spellings`), recognised reading, or none. Without context a key shows no name (or, on request, *all* single-accidental names, e.g. `Cis/Des`).

**Musical meaning** – `ChordToneRole` (ROOT, MINOR_THIRD, …, THIRTEENTH, SLASH_BASS), scale degree, `is_root` and `is_bass` as separate flags (`VoicedNote`).

**Visual state** – `KeyState` flags (§4), badges and label strings in `KeyVisual`; no colours.

**Input** – `KeyboardInputState.pressed` (temporary, with source and velocity), `.selected` (latched), `.sustained`; `InputSource` = MOUSE / COMPUTER_KEYBOARD / MIDI_DEVICE / PROGRAM.

**Practice** – `Exercise(id, topic, objective_key, prompt_key, difficulty, policy, expected_*, hint_keys, knowledge_refs, review_status, publishable, version)`; `PracticeFeedback(verdict, correct/missing/extra pitch classes, correct/missing/extra pitches, bass_correct, message_key)`.

## 4. State model and display priority

All flags of a key are kept in `KeyVisual.states`. Three display channels are derived deterministically:

| Channel | Rule |
|---|---|
| `fill` | first present state of `PRACTICE_WRONG > PRACTICE_MISSING > PRACTICE_CORRECT > PRESSED > SELECTED > CHORD_ROOT > CHORD_TONE > COMPARISON_HELD > COMPARISON > SCALE_ROOT > SCALE_TONE` |
| `outline` | `SCALE_ROOT`/`SCALE_TONE` whenever fill is not already a scale state |
| `badges` | role label (`1`, `b3`, `#11` …), `B` for bass, `=` held / `·` previous-chord pitch, `✓ ✗ ?` practice |

`CHORD_BASS` is never a fill, so the bass is always visible as a badge. The Tk view draws scale states as a ring only, so context never hides events. Information is never conveyed by colour alone (badges and text description).

## 5. Session synchronisation

| Event | Path |
|---|---|
| select / add / edit / remove / reorder / transpose / undo / redo / load / new / notation switch | controller `_notify` → dialog listener → `workbench.sync()` → redraw |
| session replaced (`new_reviewed_project`) | workbench uses `lambda: controller.session`, so the new object is read |
| temporary voicing / inversion / scale / comparison / practice | workbench fields only; tested to leave `repr(session.state)`, dirty flag, undo stack and controller revision unchanged |
| real change | "Add to progression" → `controller.add_chord(symbol)` in project convention → undoable |

Automatic timed playback is **not** implemented (ADR-007/019).

## 6. Recognition principles

- All 31 qualities × 12 roots are compared against the played pitch-class set.
- Kinds: `EXACT`, `STANDARD_VOICING` (template's own voiced selection, e.g. C9 without 5th), `INCOMPLETE` (only the perfect fifth missing, root present).
- Status: `EMPTY`, `SINGLE_NOTE`, `INTERVAL`, `EXACT_MATCH`, `AMBIGUOUS`, `INCOMPLETE`, `UNSUPPORTED`.
- Reasons, not scores: `ROOT_IN_BASS`, `INVERSION_BASS`, `OMITS_FIFTH_BY_TEMPLATE`, `MISSING_TONE`, `DOUBLED_TONES`, `ROOT_IN_KEY`, `ALL_TONES_IN_KEY`, `TONES_OUTSIDE_KEY`.
- Deterministic order: complete before standard voicing before incomplete; root in bass first; then triad < sus < seventh < add < extended. This is a display order, not a harmonic verdict.
- Spelling: key scale if it contains the root pitch class, otherwise the documented default table (the same as `theory.beginner_voicing`), flagged as `DEFAULT_TABLE`.

## 7. Practice and knowledge

The pilot (six exercises) uses three policies: `EXACT_PITCHES`, `PITCH_CLASSES`, `PITCH_CLASSES_WITH_BASS`. Expected chord tones are derived from `parse_chord`, not typed by hand. All pilot items are `AI_DRAFT_UNREVIEWED` and `publishable=False`; the constructor rejects `publishable=True` for unreviewed items.

Knowledge integration (future): `knowledge_refs` holds module ids (`M01`, `M02`, `M04`). A later generator should read concepts and reviewed claims through `KnowledgeAdapter`, carry their review state into `Exercise.review_status`, and never mark generated content as verified. No second knowledge store was created.

## 8. Handoff specification for Glide Bento

Audience: the agent developing Glide Shell / Glide Bento. Nothing in this section was implemented in Glide.

**Public interfaces to consume**

| Interface | Module | Contract |
|---|---|---|
| `KeyboardWorkbench` | `src/steps/keyboard/workbench.py` | construct with `session_provider`; set `mode`, `selected_index`, `voicing_type`, `rotation`, `show_chord`, `show_scale`, `scale_name`, `compare_previous`, `show_all_names`, `viewport`, `auto_fit`; call `sync()` after every project notification; read `view_model()`, `chord_info()`, `comparison()`, `recognition()`, `exercise`, `feedback` |
| `KeyboardViewModel` | `state.py` | `viewport`, `keys: tuple[KeyVisual]`, `hidden_below`, `hidden_above`, `off_piano` |
| `KeyVisual` | `state.py` | `key: PianoKey`, `states`, `fill`, `outline`, `badges`, `label`, `description` |
| `KeyboardInputState` | `input.py` | `press/release/toggle_selected/clear_selected/release_all/apply(LiveNoteEvent)` |
| controller | `app/ui/session_controller.py` | `add_listener/remove_listener`, `add_chord`, `revision` |

**Interaction requirements** – pointer press/release per key (raised keys hit first); latched toggle in free/practice modes; computer-keyboard row `A W S E D F T G Y/Z H U J K` from the lowest visible C, auto-repeat ignored; `FocusOut` must call `release_all()`; `PageUp/PageDown` previous/next chord; `Left/Right` octave shift.

**Layout and viewport** – width scales with the number of natural keys (`len(viewport.white_keys())`); raised keys 60 % width and 60 % height; minimum one octave, default C3–C6; `fitted_to()` grows the range to show every on-piano voicing note; off-screen notes must be reported, never dropped. Re-layout only on viewport or size change; state changes only repaint (tested: `layout_count`).

**Semantic colour roles** (proposal for a Bento token set): `keyboard.natural`, `keyboard.raised`, `keyboard.edge` (instrument base, currently fixed hex in `keyboard_view.py` – **open question for the framework**), and one role per `KeyState`. Current mapping to STEPS theme tokens is in `keyboard_view.state_color`. Text on markers uses whichever of black/white has higher WCAG contrast.

**Typography** – note names and badges at `size_sm − 2` (min 7 pt), sans family from the theme; labels can be long in German (`Heses4`), so allow clipping/ellipsis.

**Accessibility** – badges duplicate every colour meaning; `KeyVisual.description` lists the state codes for tooltips or screen-reader text; canvas focus ring uses `border_focus`. No native screen-reader test has been run.

**Lifecycle** – remove controller listeners on close; release all input on close and focus loss; no timers are used.

**Possible Bento compositions** – keyboard tile + chord inspector tile; keyboard + progression strip (shared `selected_index`); practice tile (exercise list + keyboard + feedback); recognition tile for free input. Generic needs that could become framework features: a canvas-based "segmented instrument" widget with hit testing, a focusable canvas with roving key focus, and token roles for instrument surfaces. Musical components remain part of STEPS.
