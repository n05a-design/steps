# Desktop verification

Run the two native widget workflows from the repository root with Python and Tk:

```sh
STEPS_REQUIRE_DESKTOP_TK=1 python3 -B -m unittest tests.test_desktop_app_entrypoint -v
```

The dialogs test uses real Tk widgets, event bindings, storage, publication
data and MIDI bytes. It creates a project, searches and loads an example,
retains the result when the search is cleared, edits a chord, applies a
recommendation, compares and applies styles, and exports Format 0 after
checking the disabled voicing modes. An injected file replacement error
keeps the previous MIDI file and the options dialog available for retry.
The test then saves, closes and reopens the project. It exercises invalid
chord input, missing search results, cancellation and undo/redo. It checks
keyboard scrolling, Tab/Shift-Tab traversal, Escape focus restoration,
nested modal grabs, main-window shortcut isolation and the lab's minimum size. Native
chooser and confirmation responses are injected so CI can run unattended.
The same tests run in the Ubuntu Xvfb, Windows and macOS smoke jobs.

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
