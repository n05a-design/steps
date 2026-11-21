# Desktop verification

Run the two native widget workflows from the repository root with Python and Tk.
Use a fresh Python process for each workflow on Aqua:

```sh
export STEPS_REQUIRE_DESKTOP_TK=1 PYTHONFAULTHANDLER=1
python3 -B -m unittest \
  tests.test_desktop_app_entrypoint.TestDesktopAppEntrypoint.test_main_window_instantiation_and_wiring -v
python3 -B -m unittest \
  tests.test_desktop_app_entrypoint.TestDesktopAppEntrypoint.test_native_dialog_workflow -v
```

The dialogs test uses real Tk widgets, event bindings, storage, publication
data and MIDI bytes. It scrolls a long progression to a newly added chord,
checks the active row and keyboard reordering through the native list,
and verifies that locale changes keep drafts, selection and scroll position.
It then creates a new project, searches and loads an example,
checks chord cards at the minimum dialog size, preserves the reading position
when a filter keeps the example selected, resets the preview on a new selection,
clears the cards when the search has no results, checks Tab access to the
source and review menu, confirms its commands dispatch only the selected
example's links, edits a chord, applies a
recommendation, checks MIDI range and signed voice-motion details in both style previews,
selects a shared chord event from the selector, with Left/Right keys or
by clicking a note,
zooms both tick axes in sync, checks visible note bounds and returns to the
full overview, verifies that these actions leave project state unchanged,
applies a style, and exports Format 0 after
checking the disabled voicing modes. The recommendation path runs at the
main window minimum size, switches candidates with arrow keys, verifies
Tab traversal through preview and apply controls, toggles UI language
with the same candidate selected, and inserts it with Enter. An injected file replacement error
keeps the previous MIDI file and the options dialog available for retry.
The test checks the title-based MIDI filename, then confirms that a repeated
export opens in the last successful export directory. Cancelling the chooser
leaves the previous output bytes intact.
The test then saves, closes and reopens the project. It exercises invalid
chord input, missing search results, cancellation and undo/redo. It checks
keyboard scrolling, Tab/Shift-Tab traversal, Escape focus restoration,
nested modal grabs, main-window shortcut isolation and the lab's minimum size.
The project workflow also opens a real backup after corrupt UTF-8 and
verifies that rejecting a newer schema preserves the dirty session. Native
chooser and confirmation responses are injected so CI can run unattended.
The same tests run in the Ubuntu Xvfb, Windows and macOS smoke jobs.
Windows and macOS run the workflows in separate steps and processes. The
Aqua runner showed intermittent native faults during event processing when
the second workflow reused the process of a previous Tk root. Each CI step
still fails on an assertion, unavailable Tk or a process crash.

## macOS development app

Use a macOS Python installation with Aqua Tk. The tested toolchain is Python
3.14.5 with Tk 9.0.3 and PyInstaller 6.22.3 on arm64. Build from the repository
root into a fresh local directory.

```sh
stage=$(mktemp -d)
python3 -m venv "$stage/venv"
. "$stage/venv/bin/activate"
python -m pip install 'PyInstaller==6.22.3'
sh scripts/build_macos_dev_app.sh "$stage/build"
open "$stage/build/dist/STEPS-Dev.app" --args --language en
```

Pass `--language de` to start in German. To repeat a distribution smoke
without a source checkout on the import path, start the bundle executable
with `--headless --language en` and then with `--headless --language de` from
a separate working directory. The bundle includes Aqua Tk, localized
catalogs, the app icon, and the exact product registry and approval data used
by the three reviewed examples. PyInstaller applies local ad hoc signing for
Apple Silicon. Public distribution requires separate signing, notarization
and user acceptance. Windows and Linux use their existing Python workflows.

[UI architecture](../../app/ui/README.md) · [Quality gates](../../docs/quality/QUALITY_GATES.md)
