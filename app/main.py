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

from app.ui.session_controller import ProgressionSessionController


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="steps",
        description="STEPS – Reine, testbare Musik- & Harmonielehre und Desktop Applikation"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Startet ohne graphisches Fenster (für CI- und Terminal-Automatisierung)."
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help="Aktives Farb-Theme (Standard: dark)."
    )
    parser.add_argument(
        "--export-midi",
        type=str,
        default=None,
        help="Exportiert die Initial-Progression direkt in eine SMF-MIDI-Datei und beendet."
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    controller = ProgressionSessionController()

    # Pre-populate with standard progression if empty
    if not controller.session.chords:
        for chord in ["Dm7", "G7", "Cmaj7"]:
            controller.add_chord(chord)

    if args.export_midi:
        out_path = controller.export_midi(args.export_midi)
        print(f"[STEPS] MIDI-Export erfolgreich: {out_path}")
        return 0

    # Auto-detect headless environment (e.g. Linux CI without X11 or macOS server)
    is_headless = args.headless or (sys.platform.startswith("linux") and not os.environ.get("DISPLAY"))

    if is_headless:
        state = controller.get_state_summary()
        print("[STEPS] Headless-Modus aktiv.")
        print(f"  Progression: {' -> '.join(state['chords'])}")
        print(f"  Tonart:      {state['key']}")
        print(f"  Tempo:       {state['bpm']} BPM")
        print("[STEPS] Initialisierung und Controller-Check erfolgreich.")
        return 0

    import tkinter as tk
    from app.ui.main_window import StepsMainWindow
    from app.ui.theme import ThemeManager

    theme = ThemeManager(mode=args.theme)
    root = tk.Tk()
    app = StepsMainWindow(root, controller=controller, theme=theme)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
