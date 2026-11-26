# STEPS – Music Keyboard Foundation & Interactive Music Engine – Implementation, Integration & Verification Report

**Date:** 2026-11-26 · **Branch:** `feat/steps-music-keyboard-interactive-engine` · **Base:** `cd455e31bc25b87b33634d2feea40453deaf67e7` (`main`, 0.8.0-dev) · **Language:** English (AGENTS.md rule 12)
**Status axes kept separate:** implemented ✔ · integrated ✔ · automated tests ✔ · manual native test ✘ · music-theory review ✘ · owner approval ✘ · published ✘

## 1. Executive summary

**Starting point.** STEPS had a tested theory core (pitch, spelling, 31 chord qualities, 15 scales, voicings, inversion, voice leading), a `ProgressionSession` with undo/redo, MIDI export (ADR-017), audio ports with a `NullAudioBackend`, and desktop dialogs (Next Chord Explorer, Voice Leading Lab). There was no keyboard, no chord recognition that keeps ambiguity, and no practice model.

**Delivered.**
- Pure domain package `src/steps/keyboard/` (no Tk/Glide imports): 88-key model, contextual chord-tone roles and spellings, scale overlay, semantic key-state model, ambiguity-aware recognition, voicing comparison, input state, practice pilot, and a UI-free workbench that reads the session.
- Port spec `src/steps/ports/live.py` (MIDI input normalisation, `MidiInputPort`, `NotePreviewService`), with test adapters only.
- A desktop keyboard dialog reachable from **Tools → Keyboard** and the sidebar. It has three modes: progression preview, free input, and practice pilot.
- Two proposed ADRs (018, 019), an architecture/reuse/Bento handoff document, and changelog and implementation notes.
- 82 new automated tests, including real-Tk tests through the production main window.

**Main risks.** Recognition and pilot content are AI-authored and not reviewed by a human music theorist. Native accessibility is untested. Instrument base colours are fixed hex values pending a framework token decision. The pre-existing Glide manifest mismatch on `main` is unrelated but blocks a fully green suite.

## 2. Repository status

| Item | Value |
|---|---|
| Start commit | `cd455e3` (local `main` = branch base; remote not re-fetched in this session) |
| Branch | `feat/steps-music-keyboard-interactive-engine` (local only) |
| Commits | `b27e4f1` domain · `542153d` desktop · `ef461c0` tests · `e903039` docs · plus a final report/integrity commit |
| Version | unchanged `0.8.0-dev` (version bump is an owner decision, see §12) |
| Push / PR | **not pushed, no PR**; prepared for review (requires owner go-ahead) |
| Glide Shell | `glide_shell/` untouched (no diff) |

## 3. Inventory and reuse

The full matrix is in [KEYBOARD_ARCHITECTURE.md §2](../../architecture/KEYBOARD_ARCHITECTURE.md#2-reuse-matrix-inventory-of-cd455e3).
- **Reused directly:** `NoteSpelling`, `parse_spelling`, `transpose_diatonic`, `CHORD_TEMPLATES`, `parse_chord`, `to_voicing`, `Voicing.invert`, `detect_chord_inversion`, `construct_scale`, `ProgressionSession.get_voicings` and `harmonic_degree_at`, `classify_voice_motion`, `absolute_semitone_distance`, `directed_semitones`, `AudioBackendPort` and `NullAudioBackend`, `LocaleManager`.
- **Extended:** `ProgressionSessionController.remove_listener`; tools-menu and sidebar entries.
- **New, because the function did not exist:**
  - role naming of template intervals;
  - a multi-reading recogniser (the existing `_deduce_triad_or_seventh_root` returns exactly one root);
  - the 88-key model, viewport and state model;
  - input state and practice scoring;
  - the live-port spec.
- **Avoided duplicates:** no second chord, interval, voicing, notation, session, undo or knowledge implementation.

## 4. Architecture

Layering, data contracts, state model, session synchronisation and recognition rules are in [KEYBOARD_ARCHITECTURE.md](../../architecture/KEYBOARD_ARCHITECTURE.md) §1–§6.

Key points:
- Physical identity, pitch, spelling, meaning and visual state are separate types.
- The fill priority is fixed and every state stays in `KeyVisual.states`.
- The view only imports the keyboard `model`/`state` modules (tested).
- The workbench reads the session through a provider and never writes it.

## 5. Implemented functions

| Area | Behaviour |
|---|---|
| Keyboard | A0–C8, 52/36 keys; MIDI 0–127 validated separately; asc/desc order; viewport (≥1 octave, white edges, shift, resize, fit-to-voicing); off-screen and off-piano notes reported, never dropped |
| Notation | DE/INT via core; enharmonic list per key (B#3 = 60, Cb4 = 59, double accidentals); names only from context or, on request, all names `Cis/Des` |
| Chords | roles for all 31 qualities (1, b3, 3, 4, b5, 5, #5, 6, bb7, b7, 7, b9, 9, #9, 11, #11, b13, 13, slash bass); spelled tones (e.g. Cdim7 = C Es Ges Heses) |
| Voicings | shows the session's voice-led voicing for CLOSE/DROP2/SHELL/ROOTLESS; inversion rotation as preview; root ≠ bass (slash, inversions); omitted tones listed; unrealisable voicings reported with the core error |
| Scales | any of the 15 core scales, project key or chosen template, drawn as rings so chord markers stay dominant |
| Voice leading | previous vs. current voicing: per-voice signed steps, held/semitone/whole-tone/leap, held pitches vs. same pitch class elsewhere, no forced pairing for unequal counts |
| Recognition | EXACT / STANDARD_VOICING / INCOMPLETE (only the fifth missing); statuses EMPTY…UNSUPPORTED; reasons, no scores; key-context spelling |
| Input | mouse (white/black keys), computer row A W S E D F T G Y/Z H U J K, auto-repeat ignored, focus-loss release; pressed vs. latched selection; one path for future MIDI devices |
| Project change | "Add to progression" → `controller.add_chord` in project convention (undoable); everything else is preview |
| Practice | six pilot exercises, three scoring policies (exact pitches, pitch classes, pitch classes + bass), feedback and solution marks; `AI_DRAFT_UNREVIEWED`, not publishable |

## 6. Musical correctness

- **Contracts used:** ADR-015 (unreduced intervals), the core spelling rules, and `detect_chord_inversion` (Aldwell & Schachter figures).
- **Golden tests** use hand-written values that are not computed by the code under test:
  - reference voicings C, Cm, Am, G7, Cmaj7, Dm7 with German names;
  - C major inversions C4-E4-G4 / E4-G4-C5 / G4-C5-E5;
  - G7 third inversion (4/2);
  - Cmaj7 drop-2 G2-C3-E3-H3;
  - C/E and C/D;
  - the INT/DE table from the assignment, plus B#/Cb/Ebb/F##;
  - 17 spelled chord-tone sets;
  - the ii–V–I voicings Dm7 → G7/D → Cmaj7. Movements are C4→H3 −1, A3→G3 −2, F3→E3 −1, D3→C3 −2; held tones are D3/F3, then G3/H3; G7/D is recognised with figure 4/3.
- **Ambiguities preserved:**
  - C6 / Am7/C;
  - Dm7 / F6/D;
  - Bm7b5 / Dm6/B;
  - dim7 (four roots), aug (three), Csus2 / Gsus4/C;
  - C7b5 / C7#11 (no 5th) / F#7b5.

  Two of my own initial test expectations wrongly assumed uniqueness (Dm7, Bm7b5). They were corrected to AMBIGUOUS, and the engine was not changed.
- **Known limitations:**
  - The core marks a 6th in the bass (C6/A) as a non-chord bass (figure shown as "no figured-bass label").
  - Default spelling without key context uses the beginner table (E♭, A♭, B♭, F♯, C♯).
  - Recognition does not infer harmonic function.
- **Review status:** no human music-theory review has taken place. An AI review cannot replace it.

## 7. File inventory

| Path | Purpose | Change | Tests |
|---|---|---|---|
| `src/steps/keyboard/__init__.py` | public API | new | all keyboard tests |
| `src/steps/keyboard/model.py` | 88 keys, viewport | new | `TestPianoModel`, `TestViewport` |
| `src/steps/keyboard/chord_tones.py` | roles, spelling, voicing labels, DE symbols | new | `TestChordToneRoles`, `TestGoldenVoicings` |
| `src/steps/keyboard/state.py` | key states, priority, view model | new | `TestStatePriority`, `TestScaleOverlay` |
| `src/steps/keyboard/recognition.py` | recognition | new | `TestChordRecognition` |
| `src/steps/keyboard/voice_motion.py` | voicing comparison | new | `TestVoiceMotion` |
| `src/steps/keyboard/input.py` | input state | new | `TestInputAndLivePorts` |
| `src/steps/keyboard/practice.py` | exercises, scoring, pilot | new | `TestPracticePilot` |
| `src/steps/keyboard/workbench.py` | UI-free controller | new | `TestWorkbenchSessionIntegration` |
| `src/steps/ports/live.py` | MIDI-in / preview port spec | new | `TestInputAndLivePorts` |
| `app/ui/keyboard_view.py` | canvas renderer | new | `test_keyboard_dialog.py` |
| `app/ui/keyboard_dialog.py` | dialog + localized description | new | `test_keyboard_dialog.py` |
| `app/ui/main_window.py` | menu + sidebar entry | +18 lines | dialog Tk tests, existing desktop tests |
| `app/ui/session_controller.py` | `remove_listener`, notify over a copy | +7 | dialog Tk tests |
| `app/locales/{en,de}.json` | 141 keys each | additions | `test_i18n` parity, label-length test |
| `tests/test_i18n.py` | fake tools menu now 4 entries | fixture | itself |
| `tests/test_reference_integrity.py`, `scripts/verify_reference_integrity.py` | ADR count 17 → 19 (proposed 018/019); canonical identity lock unchanged | count | itself |
| `decisions/ADR-018…`, `ADR-019…`, `DECISION_REGISTER.md`, `README.md` | proposed decisions | new/rows | reference integrity |
| `docs/architecture/KEYBOARD_ARCHITECTURE.md` (+README) | architecture, reuse, handoff | new | link check |
| `CHANGELOG.md`, `docs/IMPLEMENTATION.md`, `src/steps/README.md`, `src/steps/ports/README.md` | status notes | additions | documentation/link checks |

No dependencies, assets, schemas, project formats, `glide_shell/` files or MIDI-export code were changed.

## 8. Tests and quality

Environment: Windows 11, CPython 3.14 (`py -3.14`), PyYAML 6.0.4 in an isolated target folder. Clean clones with `core.autocrlf=false` (LF, like CI).

| Run | Ran | Failures | Skipped | Notes |
|---|---|---|---|---|
| Baseline `cd455e3` (LF clone) | 914 | 4 | 1 | pre-existing (see below) |
| Branch `e903039` (LF clone) | 996 | 6 | 1 | the 4 pre-existing + 2 caused by this branch, both fixed in the final commit (missing report link; ADR count) |
| **Branch tip `44dd71a` (LF clone, after review fixes)** | **1001** | **4** | 1 | **exactly the 4 pre-existing failures; no new failure** |
| Keyboard suites (worktree) | 82 | 0 | 0 | `test_keyboard_domain` 32, `test_keyboard_engine` 36, `test_keyboard_dialog` 14 (real Tk) |

Pre-existing failures on unmodified `main`:
- `glide_shell` manifest: `AI_GUIDE_NEW_PROJECTS.md: modified`, two tests, and the wheel smoke test that calls the same check.
- `test_documentation_consistency` in the cloned checkout.

These are not caused by this branch and were not "fixed" by weakening anything.

The tip result above is the final full-suite figure (+87 tests vs. baseline). Additional scripts at the branch tip:
- `check_ui_text_inventory` and `check_cli_text_inventory`: PASS.
- `verify_reference_integrity`: PASS.
- `check_markdown_links`: PASS after the report was added.
- `check_release_consistency`: PASS.
- `check_documentation_consistency`: PASS in the worktree.

Not run: macOS/Linux, the CI matrix 3.11–3.13, native screen readers, DAW, and Xvfb.

**Architecture tests:**
- `src/steps/**` stays free of `tkinter`, `glide_shell` and `app` (existing test, now covering the new package).
- The view-import restriction (new test).
- No project mutation by previews or practice (repr, dirty flag, undo and revision compared).

**GUI lifecycle (real Tk):**
- repeated open/close removes the listener;
- the focus-out release;
- resize does not cause a re-layout loop, and repaint reuses canvas items;
- the dialog builds under 4 themes;
- controller changes refresh the open dialog.

## 9. Acceptance matrix

| AC | Status | Evidence |
|---|---|---|
| 01 repo inventory | VERIFIED | §2, §3; baseline run |
| 02 reuse matrix | VERIFIED | architecture §2 |
| 03 reuse preferred | VERIFIED | §3; no duplicate engines |
| 04 88 keys | VERIFIED | `TestPianoModel` |
| 05 MIDI/octave/pc | VERIFIED | `TestPianoModel`, invalid-input tests |
| 06 INT/DE consistent | VERIFIED | `TestNotationContract`, notation-switch test |
| 07 enharmonics kept | VERIFIED | context labels, `spell_at`, key-context recognition |
| 08 chords visualised | VERIFIED (auto) / EXTERNAL_REVIEW_REQUIRED (music) | golden roles, Tk tests |
| 09 scales | VERIFIED | `TestScaleOverlay` |
| 10 chord+scale combined | VERIFIED | overlay test (fill + ring) |
| 11 concrete voicings | VERIFIED | workbench = `get_voicings` |
| 12 root ≠ bass | VERIFIED | slash/inversion tests |
| 13 inversions visible | VERIFIED | rotation preview + figures |
| 14 voice leading from core | VERIFIED | ii–V–I test; core functions |
| 15 session bound | VERIFIED | sync tests (undo, redo, transpose, load, new, replace, notation) |
| 16 previews don't mutate | VERIFIED | snapshot tests (domain + Tk) |
| 17 undo/redo intact | VERIFIED | insert-then-undo tests |
| 18 interactive input | VERIFIED | Tk click/keyboard tests |
| 19 ambiguity handled | VERIFIED (auto) / EXTERNAL_REVIEW_REQUIRED | recognition tests |
| 20 practice pilot works | VERIFIED (function) / EXTERNAL_REVIEW_REQUIRED (content) | pilot tests |
| 21 extensible practice contract | VERIFIED | `Exercise` validation |
| 22 audio interfaces specified | VERIFIED | ADR-019, `NotePreviewService` |
| 23 MIDI-live interfaces specified | VERIFIED | `live.py`, ADR-019 |
| 24 MIDI export regression-free | VERIFIED | existing MIDI/golden SHA suites pass; no code change |
| 25 domain testable without GUI | VERIFIED | domain/engine suites headless |
| 26 reachable in app | VERIFIED | Tools menu + sidebar Tk test |
| 27 Glide Shell unchanged | VERIFIED | no diff under `glide_shell/` |
| 28 no competing Bento | VERIFIED | only STEPS components; handoff spec |
| 29 golden tests | VERIFIED | §6 |
| 30 regression run | PARTIAL | full suite 1001 tests, only pre-existing failures; Windows/3.14 only |
| 31 GUI lifecycle | PARTIAL | Tk tests on Windows; no native a11y |
| 32 gates intact | VERIFIED | no gate weakened; ADR count adjusted for new proposals only |
| 33 docs consolidated | VERIFIED | §7 |
| 34 ADRs/owner decisions | OWNER_ACTION_REQUIRED | ADR-018/019 proposed; §12 |
| 35 Bento integration specified | VERIFIED | architecture §8 |
| 36 critical review | VERIFIED (AI) / EXTERNAL_REVIEW_REQUIRED (human) | §10 |
| 37 blockers documented | VERIFIED | §12, §13 |
| 38 PR-ready | PARTIAL | committed locally; push/PR await owner go-ahead |

## 10. Independent review

Method: a separate AI review agent (no shared context, read-only) received the diff, the repo rules and the focus areas. Its findings and the fixes are listed below. This is an AI review, **not** a human music-theory review.

No critical findings. The reviewer confirmed the following:
- The domain boundary holds.
- Previews and practice cannot change the project or the undo stack.
- Listener and focus lifecycle is handled correctly.
- MIDI normalisation and hung-note protection work.
- Chord-tone roles and spelling are correct, including bb7, #5, #11 and b13, and Gbm = Gb-Bbb-Db.
- German H/B rendering is correct.
- INT/DE symbol round-trips succeed for all templates, roots and inversions.

| # | Severity | Finding | Action |
|---|---|---|---|
| 1 | major | Figured bass wrong for seventh chords without a fifth (C7 no5 → `5/3`; C7/Bb → "not a chord tone"; C9/E → `6`; shell/rootless) because the core helper needs a complete 1-3-5-7 set | **fixed:** `is_seventh_quality` passes the template's seventh to `detect_chord_inversion`; hand-written tests (`TestReviewRegressions`) |
| 2 | major | Free-input names taken from the first of several readings (dim7 A shown as Heses) | **fixed:** a key is named only if all complete readings agree; test |
| 3 | major | "Not by colour alone" not backed for pressed/selected/scale | **fixed:** badges `▾ ● (n)`; doc updated; test. Shared colour tokens remain (distinguished by badges) |
| 4 | minor | Computer key could stay held after an octave shift, or with Shift released | **fixed:** key → note map, lower-cased keysym; Tk test |
| 6 | minor | "One reading" status while incomplete readings are listed | **fixed:** wording "one complete reading" |
| 7 | minor | Inversion preview of a slash chord gives no hint | **fixed:** localized hint; bass that is a chord tone without a standard figure (e.g. the 6th of C6) is now named instead of "not a chord tone" |
| 8 | minor | Raw English core error shown for unrealisable DROP2 | **fixed:** localized message only; test |
| 9 | minor | Uncaught errors in add/compare | **fixed:** guarded |
| 10 | minor | Foreign notes labelled as slash bass | **fixed:** new role `NON_CHORD_TONE` (`x`) |
| 5 | minor | Default spelling table yields Abm/Dbm-type names without key context | **open, documented** (§6); a quality-aware table needs music review |
| 11 | minor | Two tests partly circular (session voicing, all-templates sweep) | **mitigated:** they remain integration checks; new hand-written regressions added. More golden cases for incomplete readings are recommended for the human review |

After the fixes, the keyboard, i18n and reference suites ran 145 tests with 0 failures.

## 11. Glide / Bento compatibility

- `glide_shell/` and the theme system are unchanged.
- The keyboard uses `ThemeManager`, `create_button`, `make_surface_card`, `ModalDialog` and `ThemedAutoScrollbar`.
- The architecture boundary is enforced by tests.
- The handoff specification is in [KEYBOARD_ARCHITECTURE.md §8](../../architecture/KEYBOARD_ARCHITECTURE.md#8-handoff-specification-for-glide-bento).
- **Framework questions:**
  - instrument surface tokens (currently three fixed hex values);
  - a reusable segmented-instrument canvas with roving focus.

## 12. Owner decisions

| # | Topic | Existing decision | Options | Recommendation | If undecided |
|---|---|---|---|---|---|
| 1 | Integrated audio | ADR-007: export only | ADR-019 A–E | keep A now; decide B+C later | silent keyboard, DAW playback |
| 2 | Physical MIDI keyboard | none | ADR-019 C | adopt together with B after licence and packaging test | virtual input only |
| 3 | STEPS as real-time MIDI tool | none | B (virtual port) | yes as optional output | file export only |
| 4 | Sound source | ADR-007 no soundfonts | D / E / DAW | DAW via B | – |
| 5 | Additional dependencies | none | `python-rtmidi`, PortAudio, FluidSynth | at most `python-rtmidi`, after review | none added |
| 6 | Metronome | none | with B, or own audio | defer | none |
| 7 | Persist learning progress | none | settings file / project / none | defer until reviewed content exists | nothing stored (current) |
| 8 | Approve practice content | pilot is unreviewed | human review per item | review the six pilot items first | pilot stays labelled draft |
| 9 | Scope of 1.0 | V1.0.0 contract | include keyboard preview + recognition | include; practice optional | keyboard stays branch-only |
| 10 | Deferred features | – | audio, MIDI-in, timed playback | 0.9.3+ | – |
| 11 | Form of Bento integration | – | tile set per §8 | decided by the Glide agent with the owner | Tk dialog remains |
| 12 | Native platforms | partial CI smokes | macOS/Windows/Linux | unchanged | – |
| 13 | Required acceptances | E3 in roadmap | music theory, a11y, EN/DE text | add "keyboard" to E3 | – |
| 14 | ADR-018 itself / version 0.9.0-dev | proposed | accept / amend / reject | accept, then bump to 0.9.0-dev | branch stays unmerged |

Proposed milestones (from the assignment, judged feasible on this basis):
- 0.9.0 – this branch;
- 0.9.1 – recognition refinements;
- 0.9.2 – practice/learning with reviewed content;
- 0.9.3 and 0.9.4 – only after ADR-019 is accepted;
- 1.0 – consolidation.

## 13. Next work packages

1. Owner review of ADR-018/019. Then push and open the PR.
2. Human music-theory review of the role table, recognition readings and the six pilot exercises.
3. Fix the pre-existing Glide manifest mismatch on `main` (`AI_GUIDE_NEW_PROJECTS.md`) through `shell_uebernehmen.py`, not by hand.
4. Native accessibility pass (NVDA/VoiceOver): expose `KeyVisual.description` per key.
5. Option to spell recognised chords from the currently selected reading. Separately, let the user pick the reading before marking keys.
6. If ADR-019 is accepted: a `python-rtmidi` adapter implementing `MidiInputPort` and a virtual output behind `AudioBackendPort`.

## 14. Final status

**Technical:** VERIFIED_WITH_LIMITATIONS. The functions are implemented, integrated and covered by automated tests on Windows/CPython 3.14.
**Product / release:** OWNER_REVIEW_REQUIRED and EXTERNAL_REVIEW_REQUIRED:
- ADR-018/019 are proposed;
- the music-theory and accessibility reviews are open;
- the branch is not pushed or merged.
