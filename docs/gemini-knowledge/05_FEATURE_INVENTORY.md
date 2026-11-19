# Feature Inventory

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** PARTIAL — this inventory distinguishes code, tests, and acceptance rather than treating them as one completion state.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

| Feature | Status | Evidence | Important limit |
|---|---|---|---|
| Pitch, spelling, intervals, scales, chords | IMPLEMENTED / TESTED | `src/steps/theory/`; `tests/test_theory_core.py`, `test_notation_contract.py` | Human review across all cases NOT_EVIDENCED |
| Progression analysis and transposition | IMPLEMENTED / TESTED | `src/steps/progression/engine.py`; `tests/test_progression_engine.py` | Analysis is constrained by implemented rules/context |
| Voicing / voice-leading | IMPLEMENTED / TESTED | `src/steps/theory/voicings.py`; `src/steps/progression/voice_leading.py` | No universal claim of musical optimality |
| Session editing, reorder, undo/redo | IMPLEMENTED / TESTED | `src/steps/progression/session.py`; `tests/test_vertical_slice_progression.py` | Tests are not user acceptance |
| Tkinter desktop editor | IMPLEMENTED / PARTIAL | `app/ui/main_window.py`; `tests/test_desktop_app_entrypoint.py` | Prototype, platform/accessibility acceptance incomplete |
| Project save/open and recovery | IMPLEMENTED / TESTED | `src/steps/storage/`; `tests/test_storage_recovery_io.py`, `test_desktop_project_workflow.py` | Installer and broad compatibility acceptance incomplete |
| SMF 0/1 writing/export | IMPLEMENTED / TESTED | `src/steps/midi/`; `tests/test_midi_export_service.py`, `test_smf_parser.py` | Independent DAW checks NOT_EVIDENCED here |
| In-app audio playback | BLOCKED / out of v0.1 scope | Accepted `decisions/ADR-007-audio-nur-dateiexport-v01.md` | Do not advertise as available |
| UI localization `en`/`de` | IMPLEMENTED / TESTED | `app/i18n.py`, `app/locales/`; `tests/test_i18n.py` | Human translation/native acceptance PARTIAL |
| Reviewed pilot learning content | IMPLEMENTED / TESTED in publication path | `knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md`; benchmark and approval files | Applies to reviewed items only |
| Full source knowledge retrieval | PLANNED / PARTIAL | `knowledge/sources/registry.yaml`, `src/steps/knowledge/` | Registry breadth/review is incomplete |
| Drum editing UI | PLANNED | `decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md` defers to app v2 | Research/model presence is not feature delivery |
| Desktop installer/signing | NOT_EVIDENCED | `pyproject.toml` defines Python package metadata | No verified full desktop installer/release acceptance |
| User study / market fit | NOT_EVIDENCED | Product docs specify hypotheses, not study results | Requires human research |

## Interpretation

The evidence points to a meaningful codebase and prototype, not an all-complete or release-ready product. See [testing](10_TESTING_AND_QUALITY.md), [risks](12_KNOWN_ISSUES_AND_RISKS.md), and `docs/IMPLEMENTATION.md` for behavior and caveats.
