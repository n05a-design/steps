"""
STEPS Desktop Application Entrypoint (ADR-001 / ADR-002 / Prompt 01).

Launches the STEPS Desktop UI adhering to the 2-Pane architectural specification.
Supports headless execution mode for automated testing and CI verification.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from app.i18n import LocaleManager, SUPPORTED_LANGUAGES
from app.ui.session_controller import ProgressionSessionController


def build_parser(i18n: Optional[LocaleManager] = None) -> argparse.ArgumentParser:
    i18n = i18n or LocaleManager()
    parser = argparse.ArgumentParser(
        prog="steps",
        description=i18n.translate("cli.description")
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help=i18n.translate("cli.headless.help")
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help=i18n.translate("cli.theme.help")
    )
    parser.add_argument(
        "--export-midi",
        type=str,
        default=None,
        help=i18n.translate("cli.export.help")
    )
    parser.add_argument(
        "--language",
        choices=SUPPORTED_LANGUAGES,
        default=None,
        help=i18n.translate("cli.language.help"),
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    command_line = sys.argv[1:] if argv is None else argv
    i18n = LocaleManager()
    language_parser = argparse.ArgumentParser(add_help=False)
    language_parser.add_argument("--language")
    language_args, _ = language_parser.parse_known_args(command_line)
    if language_args.language is not None:
        i18n.set_preference(language_args.language, persist=False)

    parser = build_parser(i18n)
    args = parser.parse_args(command_line)

    controller = ProgressionSessionController()

    # Pre-populate with standard progression if empty
    if not controller.session.chords:
        for chord in ["Dm7", "G7", "Cmaj7"]:
            controller.add_chord(chord)

    if args.export_midi:
        out_path = controller.export_midi(args.export_midi)
        print(i18n.translate("cli.midi.success", path=out_path))
        return 0

    # Auto-detect headless environment (e.g. Linux CI without X11 or macOS server)
    is_headless = args.headless or (sys.platform.startswith("linux") and not os.environ.get("DISPLAY"))

    if is_headless:
        state = controller.get_state_summary()
        print(i18n.translate("cli.headless.active"))
        print(i18n.translate("cli.progression", chords=" -> ".join(state["chords"])))
        print(i18n.translate("cli.key", key=state["key"]))
        print(i18n.translate("cli.tempo", bpm=state["bpm"]))
        print(i18n.translate("cli.ready"))
        return 0

    import tkinter as tk
    from app.ui.main_window import StepsMainWindow
    from app.ui.theme import ThemeManager

    theme = ThemeManager(mode=args.theme)
    root = tk.Tk()
    app = StepsMainWindow(root, controller=controller, theme=theme, locale_manager=i18n)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
