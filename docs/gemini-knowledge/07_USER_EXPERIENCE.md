# User Experience and Desktop Workflow

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED / TESTED for selected desktop and controller workflows; PARTIAL for native acceptance and usability.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Current interaction surface

`app/ui/main_window.py` implements a Tkinter desktop prototype with a progression workspace. The tested path includes chord creation/edit/removal/reordering, key/mode/tempo/meter context, timeline editing, analysis display, undo/redo, project open/save dialogs and MIDI export. `app/ui/session_controller.py` coordinates session actions. Exact details and known limits are in `docs/IMPLEMENTATION.md`.

## Desired learning interaction

The product hypothesis is learning while composing: user edits a progression, sees a qualified context-dependent explanation, and can explore alternatives. The educational standard in `docs/product/LEARNING_AND_EXPERIENCE.md` calls for examples, counterexamples, clear context, sources and understandable feedback. This is PLANNED as a complete learning experience; user comprehension evidence is NOT_EVIDENCED.

## What automated tests cannot establish

Tk initialization and workflow tests do not alone establish keyboard usability, screen-reader support, contrast, high-DPI behavior, cognitive accessibility, native dialogs, user acceptance, or cross-platform release quality. macOS/Windows/Linux smoke jobs are not equivalent to an expert accessibility review.

## Risks to preserve

- Do not equate unusual musical behavior with invalid input.
- Explain errors and save/recovery states without discarding user edits.
- Keep keyboard routes and focus visible.
- Use labels and symbols in addition to color.
- Do not claim playback exists; v0.1 is file export only.

## Acceptance evidence and follow-up

Relevant tests: `tests/test_desktop_app_entrypoint.py`, `tests/test_desktop_project_workflow.py`, `tests/test_vertical_slice_progression.py`, `tests/test_i18n.py`. Manual accessibility and usability work is NOT_RUN in this documentation audit. Track it separately in `docs/product/V1.0.0_PRODUCT_CONTRACT.md` and `docs/quality/VERIFICATION_PLAN_V2.md`.
