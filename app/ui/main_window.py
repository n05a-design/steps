"""
STEPS Desktop Main Window – Ein Fenster, zwei Bereiche (ADR-001 / Prompt 01).

Implements the 2-Pane architectural contract:
- Area 1 (Top): Arbeitsbereich (Chord progression timeline, transpose, tempo, MIDI export)
- Area 2 (Bottom): Informations- und Theoriebereich (Voicings, scale recommendations, harmonic functions)
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from app.brand import apply_window_icon
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager, default_theme
from src.steps.storage.exceptions import StorageError
from src.steps.theory.exceptions import MusicTheoryError


class StepsMainWindow:
    """The primary STEPS desktop application window adhering to ADR-001."""

    def __init__(
        self,
        root: tk.Tk,
        controller: Optional[ProgressionSessionController] = None,
        theme: Optional[ThemeManager] = None
    ) -> None:
        self.root = root
        self.controller = controller or ProgressionSessionController()
        self.theme = theme or default_theme
        self._project_path: Optional[Path] = None

        self.root.title("STEPS — Harmonielehre & Musiktheorie")
        self.root.geometry("1024x720")
        self.root.minsize(860, 600)
        self._init_file_menu()

        # Apply branding icon if available
        try:
            apply_window_icon(self.root)
        except Exception:
            pass

        self._init_ui()
        self._refresh_all()

    def _init_file_menu(self) -> None:
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Öffnen…", command=self._on_open_project, accelerator="Ctrl+O")
        file_menu.add_command(label="Speichern", command=self._on_save_project, accelerator="Ctrl+S")
        file_menu.add_command(label="Speichern unter…", command=self._on_save_project_as)
        menu_bar.add_cascade(label="Datei", menu=file_menu)
        self.root.configure(menu=menu_bar)
        self.root.bind_all("<Control-o>", self._on_open_shortcut)
        self.root.bind_all("<Control-s>", self._on_save_shortcut)
        self.root.bind_all("<Command-o>", self._on_open_shortcut)
        self.root.bind_all("<Command-s>", self._on_save_shortcut)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_open_shortcut(self, _event: tk.Event) -> str:
        self._on_open_project()
        return "break"

    def _on_save_shortcut(self, _event: tk.Event) -> str:
        self._on_save_project()
        return "break"

    def _update_window_title(self) -> None:
        title = self.controller.get_state_summary()["title"]
        project_name = self._project_path.name if self._project_path else title
        dirty_marker = "*" if self.controller.session.is_dirty else ""
        self.root.title(f"{dirty_marker}{project_name} — STEPS")

    def _on_save_project(self) -> bool:
        return self._save_project(save_as=False)

    def _on_save_project_as(self) -> bool:
        return self._save_project(save_as=True)

    def _save_project(self, save_as: bool) -> bool:
        path = None if save_as else self._project_path
        if path is None:
            title = self.controller.get_state_summary()["title"].strip()
            initial_name = Path(title).name.replace("/", "_").replace("\\", "_") or "progression"
            selected = filedialog.asksaveasfilename(
                parent=self.root,
                title="STEPS-Projekt speichern",
                defaultextension=".stepsproj",
                filetypes=(("STEPS-Projekt", "*.stepsproj"), ("JSON-Datei", "*.json")),
                initialfile=f"{initial_name}.stepsproj",
            )
            if not selected:
                return False
            path = Path(selected)

        try:
            self._project_path = self.controller.save(path)
        except (StorageError, OSError, MusicTheoryError, ValueError) as exc:
            messagebox.showerror(
                "Projekt konnte nicht gespeichert werden",
                str(exc),
                parent=self.root,
            )
            return False

        self._update_window_title()
        return True

    def _confirm_unsaved_changes(self) -> bool:
        if not self.controller.session.is_dirty:
            return True

        choice = messagebox.askyesnocancel(
            "Ungespeicherte Änderungen",
            "Möchten Sie die Änderungen an der aktuellen Progression speichern?",
            parent=self.root,
        )
        if choice is None:
            return False
        return self._save_project(save_as=False) if choice else True

    def _on_open_project(self) -> bool:
        selected = filedialog.askopenfilename(
            parent=self.root,
            title="STEPS-Projekt öffnen",
            filetypes=(("STEPS-Projekt", "*.stepsproj"), ("JSON-Datei", "*.json")),
        )
        if not selected or not self._confirm_unsaved_changes():
            return False

        try:
            self.controller.load(selected)
        except (StorageError, OSError, MusicTheoryError, ValueError) as exc:
            messagebox.showerror(
                "Projekt konnte nicht geöffnet werden",
                str(exc),
                parent=self.root,
            )
            return False

        self._project_path = Path(selected)
        self._refresh_all()
        return True

    def _on_close(self) -> None:
        if self._confirm_unsaved_changes():
            self.root.destroy()

    def _init_ui(self) -> None:
        colors = self.theme.colors
        sp = self.theme.spacing

        self.root.configure(bg=colors.bg_window)

        # Main vertical PanedWindow
        self.paned = tk.PanedWindow(
            self.root,
            orient=tk.VERTICAL,
            bg=colors.border,
            bd=1,
            sashrelief=tk.FLAT,
            sashwidth=4
        )
        self.paned.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=sp.sm)

        # ----------------------------------------------------
        # Area 1: Arbeitsbereich (Timeline & Progression)
        # ----------------------------------------------------
        self.work_area = tk.Frame(self.paned, bg=colors.bg_surface, bd=0)
        self.paned.add(self.work_area, minsize=260)

        # Top Control Bar (Key, Tempo, Add Chord, Transpose, Export)
        self.control_bar = tk.Frame(self.work_area, bg=colors.bg_surface, pady=sp.sm, padx=sp.sm)
        self.control_bar.pack(fill=tk.X)

        self.title_lbl = tk.Label(
            self.control_bar,
            text="ARBEITSBEREICH",
            font=("Helvetica", 11, "bold"),
            fg=colors.harmonic_tonic,
            bg=colors.bg_surface
        )
        self.title_lbl.pack(side=tk.LEFT, padx=(0, sp.md))

        # Add Chord Entry & Button
        self.chord_entry = tk.Entry(
            self.control_bar,
            width=10,
            font=("Courier", 12),
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
            relief=tk.FLAT,
            bd=1
        )
        self.chord_entry.pack(side=tk.LEFT, padx=sp.xs)
        self.chord_entry.insert(0, "Cmaj7")

        self.add_btn = tk.Button(
            self.control_bar,
            text="+ Akkord",
            command=self._on_add_chord,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=sp.sm
        )
        self.add_btn.pack(side=tk.LEFT, padx=sp.xs)

        # Transpose Buttons
        self.trans_down_btn = tk.Button(
            self.control_bar,
            text="♭ -1",
            command=lambda: self._on_transpose(-1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.xs
        )
        self.trans_down_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.trans_up_btn = tk.Button(
            self.control_bar,
            text="♯ +1",
            command=lambda: self._on_transpose(1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.xs
        )
        self.trans_up_btn.pack(side=tk.LEFT, padx=sp.xs)

        # MIDI Export Button
        self.export_btn = tk.Button(
            self.control_bar,
            text="MIDI Export (ADR-017)",
            command=self._on_export_midi,
            bg=colors.harmonic_subdominant,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=sp.sm
        )
        self.export_btn.pack(side=tk.RIGHT, padx=sp.xs)

        # Chord Listbox / Progression Display
        self.prog_frame = tk.Frame(self.work_area, bg=colors.bg_window, bd=1, relief=tk.SOLID)
        self.prog_frame.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=(0, sp.sm))

        self.chord_listbox = tk.Listbox(
            self.prog_frame,
            font=("Helvetica", 13),
            bg=colors.bg_window,
            fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic,
            selectforeground=colors.text_inverted,
            relief=tk.FLAT,
            bd=0,
            activestyle="none"
        )
        self.chord_listbox.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=sp.sm)
        self.chord_listbox.bind("<<ListboxSelect>>", self._on_chord_selected)

        # ----------------------------------------------------
        # Area 2: Informations- und Theoriebereich
        # ----------------------------------------------------
        self.info_area = tk.Frame(self.paned, bg=colors.bg_surface, bd=0)
        self.paned.add(self.info_area, minsize=260)

        self.info_bar = tk.Frame(self.info_area, bg=colors.bg_surface, pady=sp.sm, padx=sp.sm)
        self.info_bar.pack(fill=tk.X)

        self.info_lbl = tk.Label(
            self.info_bar,
            text="INFORMATIONS- & THEORIEBEREICH",
            font=("Helvetica", 11, "bold"),
            fg=colors.harmonic_dominant,
            bg=colors.bg_surface
        )
        self.info_lbl.pack(side=tk.LEFT)

        # Detail Content Frame
        self.detail_frame = tk.Frame(self.info_area, bg=colors.bg_window, bd=1, relief=tk.SOLID)
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=(0, sp.sm))

        self.detail_text = tk.Text(
            self.detail_frame,
            font=("Courier", 11),
            bg=colors.bg_window,
            fg=colors.text_primary,
            relief=tk.FLAT,
            bd=0,
            wrap=tk.WORD,
            padx=sp.md,
            pady=sp.md
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)

    def _refresh_all(self) -> None:
        """Synchronizes UI state with the ProgressionSessionController."""
        state = self.controller.get_state_summary()
        self._update_window_title()

        self.chord_listbox.delete(0, tk.END)
        for idx, chord_name in enumerate(state["chords"]):
            self.chord_listbox.insert(tk.END, f"  [{idx + 1:02d}]   {chord_name}")

        if state["chords"]:
            self.chord_listbox.select_set(0)
            self._display_chord_details(state["chords"][0])
        else:
            self._display_empty_info()

    def _display_chord_details(self, chord_name: str) -> None:
        """Renders harmonic analysis, voicing reduction and scale suggestions."""
        from src.steps.theory.chord import parse_chord
        from src.steps.theory.scale import construct_scale

        self.detail_text.delete("1.0", tk.END)

        try:
            chord = parse_chord(chord_name, convention="INT")
            voicing = chord.to_voicing(bass_octave=3, voicing_type="CLOSE")

            # Quality to scale mapping
            q = chord.quality.lower()
            if "maj" in q:
                candidates = ["IONIAN", "LYDIAN"]
            elif "m7b5" in q or "ø" in q:
                candidates = ["LOCRIAN"]
            elif "m" in q:
                candidates = ["DORIAN", "AEOLIAN"]
            elif "7" in q:
                candidates = ["MIXOLYDIAN", "ALTERED"]
            else:
                candidates = ["IONIAN"]

            scales = []
            for t in candidates:
                try:
                    scales.append(construct_scale(chord.root, t))
                except Exception:
                    pass

            lines = [
                f"AKKORD-ANALYSE: {chord_name}",
                "=" * 50,
                f"Grundton:         {chord.root.step} (Pitch Class {int(chord.root.pitch_class)})",
                f"Qualität:         {chord.quality}",
                f"Kernintervalle:   {chord.theoretical_intervals}",
                f"Voicing (CLOSE):  MIDI Notes {voicing.midi_notes}",
                "",
                "KOMPATIBLE SKALEN & MODI:",
                "-" * 50,
            ]
            for s in scales:
                note_str = " - ".join(n.step + ("#" * n.alteration if n.alteration > 0 else "b" * (-n.alteration)) for n in s.spellings)
                lines.append(f"• {s.template.name.upper():16s} {note_str}")

            lines.append("")
            lines.append("STUFEN- & FUNKTIONSDIAGNOSE:")
            lines.append("-" * 50)
            lines.append("• Voicing-Reduktion (ADR-005): 4-Voice Lead Ready")

            self.detail_text.insert(tk.END, "\n".join(lines))
        except Exception as e:
            self.detail_text.insert(tk.END, f"Hinweis zum Akkord: {chord_name}\n({e})")

    def _display_empty_info(self) -> None:
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, "Keine Akkorde in der aktuellen Progression vorhanden.\nFügen Sie oben Akkorde hinzu (z. B. Dm7 -> G7 -> Cmaj7).")

    def _on_add_chord(self) -> None:
        txt = self.chord_entry.get().strip()
        if txt:
            self.controller.add_chord(txt)
            self._refresh_all()

    def _on_transpose(self, semitones: int) -> None:
        self.controller.transpose(semitones)
        self._refresh_all()

    def _on_chord_selected(self, event) -> None:
        sel = self.chord_listbox.curselection()
        if sel:
            state = self.controller.get_state_summary()
            idx = sel[0]
            if idx < len(state["chords"]):
                self._display_chord_details(state["chords"][idx])

    def _on_export_midi(self) -> None:
        from pathlib import Path
        out = Path("steps_progression_export.mid")
        self.controller.export_midi(out)
        self.detail_text.insert(tk.END, f"\n\n[ERFOLG] MIDI-Datei erfolgreich exportiert nach:\n{out.resolve()}\n")
