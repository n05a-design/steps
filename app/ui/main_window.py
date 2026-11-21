"""
STEPS Desktop Main Window – Ein Fenster, zwei Bereiche (ADR-001 / Prompt 01).

Implements the 2-Pane architectural contract:
- Area 1 (Top): Arbeitsbereich (Chord progression timeline, transpose, tempo, MIDI export)
- Area 2 (Bottom): Informations- und Theoriebereich (Voicings, scale recommendations, harmonic functions)
"""

from __future__ import annotations

import logging
import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Literal, Optional

from app.brand import apply_window_icon
from app.i18n import LocaleManager
from app.knowledge import get_reviewed_progression, list_reviewed_progressions
from app.ui.dialog_support import configure_readonly_preview
from app.ui.file_feedback import format_project_file_error
from app.ui.harmonic_inspector import format_beginner_voicings, format_chord_analysis
from app.ui.midi_export_dialog import (
    MidiExportOptions,
    MidiExportOptionsDialog,
    format_midi_file_error,
)
from app.ui.next_chord_panel import NextChordPanel
from app.ui.reviewed_library_dialog import ReviewedProgressionLibraryDialog
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager, create_button, default_theme
from app.ui.voice_leading_lab_dialog import (
    VOICE_LEADING_STYLE_OPTIONS,
    VoiceLeadingLabDialog,
)
from src.steps.midi.time import RationalMidiTime
from src.steps.models.timeline import TimeSignature
from src.steps.progression.reviewed import PublicationError
from src.steps.progression.session import ChordRecommendation
from src.steps.storage.exceptions import StorageError
from src.steps.theory.exceptions import MusicTheoryError


logger = logging.getLogger(__name__)

_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f\ud800-\udfff]')
_WINDOWS_RESERVED_FILENAME = re.compile(
    r"^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)",
    re.IGNORECASE,
)


def _portable_filename(title: str, extension: str) -> str:
    filename = _INVALID_FILENAME_CHARS.sub("_", title.strip())
    # Leave room for the extension and a possible Windows device-name prefix.
    max_stem_bytes = 254 - len(extension)
    filename = filename.encode("utf-8")[:max_stem_bytes].decode("utf-8", "ignore").rstrip(" .")
    if not filename:
        filename = "progression"
    if _WINDOWS_RESERVED_FILENAME.match(filename):
        filename = f"_{filename}"
    return f"{filename}{extension}"


class StepsMainWindow:
    """The primary STEPS desktop application window adhering to ADR-001."""

    def __init__(
        self,
        root: tk.Tk,
        controller: Optional[ProgressionSessionController] = None,
        theme: Optional[ThemeManager] = None,
        locale_manager: Optional[LocaleManager] = None,
    ) -> None:
        self.root = root
        self.controller = controller or ProgressionSessionController()
        self.theme = theme or default_theme
        self.i18n = locale_manager or LocaleManager()
        self._project_path: Optional[Path] = None
        self._last_midi_export_directory: Path | None = None

        self.root.title(self.i18n.translate("app.title"))
        self.root.geometry("1024x720")
        self.root.minsize(860, 600)
        self._init_file_menu()

        # A missing optional icon must not prevent startup.
        try:
            apply_window_icon(self.root)
        except Exception:
            logger.exception("Could not apply the STEPS window icon")

        self._init_ui()
        self._localize_widgets()
        self._refresh_all()

    def _init_file_menu(self) -> None:
        shortcut = "⌘" if sys.platform == "darwin" else "Ctrl+"
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(
            label="", command=self._on_new_project, accelerator=f"{shortcut}N"
        )
        self.file_menu.add_command(
            label="", command=self._on_open_project, accelerator=f"{shortcut}O"
        )
        self.file_menu.add_command(
            label="", command=self._on_save_project, accelerator=f"{shortcut}S"
        )
        self.file_menu.add_command(label="", command=self._on_save_project_as)
        self.file_menu.add_command(
            label="", command=self._on_browse_reviewed_library
        )
        self.reviewed_menu = tk.Menu(self.file_menu, tearoff=False)
        try:
            self._reviewed_examples = list_reviewed_progressions()
            self._reviewed_catalog_error = None
        except (PublicationError, OSError, ValueError) as exc:
            self._reviewed_examples = ()
            self._reviewed_catalog_error = str(exc)
        if self._reviewed_examples:
            for example in self._reviewed_examples:
                self.reviewed_menu.add_command(
                    label=example.progression.name,
                    command=lambda prog_id=example.progression.prog_id: self._on_new_from_example(prog_id),
                )
        else:
            self.reviewed_menu.add_command(
                label="",
                command=self._on_reviewed_catalog_error,
            )
        self.file_menu.add_cascade(label="", menu=self.reviewed_menu)
        self.menu_bar.add_cascade(label="", menu=self.file_menu)
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        for action in (self._on_explore_next, self._on_open_voice_leading_lab, self._on_export_midi):
            self.tools_menu.add_command(label="", command=action)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.language_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.language_var = tk.StringVar(self.root, value=self.i18n.preference)
        for preference in ("system", "en", "de"):
            self.language_menu.add_radiobutton(
                label="",
                value=preference,
                variable=self.language_var,
                command=lambda selected=preference: self._on_language_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.language_menu)
        self.menu_bar.add_cascade(label="", menu=self.settings_menu)
        self.root.configure(menu=self.menu_bar)
        self.root.bind("<Control-o>", self._on_open_shortcut)
        self.root.bind("<Control-s>", self._on_save_shortcut)
        self.root.bind("<Control-n>", self._on_new_shortcut)
        self.root.bind("<Command-o>", self._on_open_shortcut)
        self.root.bind("<Command-s>", self._on_save_shortcut)
        self.root.bind("<Command-n>", self._on_new_shortcut)
        self.root.bind("<Control-z>", self._on_undo_shortcut)
        self.root.bind("<Control-Shift-z>", self._on_redo_shortcut)
        self.root.bind("<Command-z>", self._on_undo_shortcut)
        self.root.bind("<Command-Shift-z>", self._on_redo_shortcut)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _localize_widgets(self) -> None:
        t = self.i18n.translate
        self.root.title(t("app.title"))
        self.file_menu.entryconfigure(0, label=t("file.new"))
        self.file_menu.entryconfigure(1, label=t("file.open"))
        self.file_menu.entryconfigure(2, label=t("file.save"))
        self.file_menu.entryconfigure(3, label=t("file.save_as"))
        if hasattr(self, "reviewed_menu"):
            self.file_menu.entryconfigure(4, label=t("file.browse_reviewed"))
            self.file_menu.entryconfigure(5, label=t("file.new_from_example"))
            if hasattr(self, "_reviewed_examples"):
                if self._reviewed_examples:
                    for index, example in enumerate(self._reviewed_examples):
                        self.reviewed_menu.entryconfigure(index, label=example.progression.name)
                else:
                    self.reviewed_menu.entryconfigure(0, label=t("file.example.unavailable"))
        self.menu_bar.delete(0, tk.END)
        self.menu_bar.add_cascade(label=t("file.menu"), menu=self.file_menu)
        self.menu_bar.add_cascade(label=t("tools.menu"), menu=self.tools_menu)
        for index, key in enumerate(("next_chord.explore", "voice.lab.open", "midi.export")):
            self.tools_menu.entryconfigure(index, label=t(key))
        self.menu_bar.add_cascade(label=t("settings.menu"), menu=self.settings_menu)
        self.settings_menu.entryconfigure(0, label=t("language.menu"))
        for index, key in enumerate(("language.system", "language.en", "language.de")):
            self.language_menu.entryconfigure(index, label=t(key))
        self.title_lbl.configure(text=t("workspace.heading"))
        self.project_title_lbl.configure(text=t("project.title"))
        self.key_lbl.configure(text=t("context.key"))
        self.mode_lbl.configure(text=t("context.mode"))
        self.major_btn.configure(text=t("context.major"))
        self.minor_btn.configure(text=t("context.minor"))
        self.notation_lbl.configure(text=t("notation.label"))
        self.notation_int_btn.configure(text=t("notation.int"))
        self.notation_de_btn.configure(text=t("notation.de"))
        self.tempo_lbl.configure(text=t("context.tempo"))
        self.meter_lbl.configure(text=t("context.meter"))
        self.context_btn.configure(text=t("context.apply"))
        if hasattr(self, "voice_style_lbl"):
            self.voice_style_lbl.configure(text=t("voice.style"))
            self._localize_voice_style_menu()
        self._update_event_timing_labels()
        self.event_timing_btn.configure(text=t("event.apply"))
        self.add_btn.configure(text=t("chord.add"))
        self.update_btn.configure(text=t("chord.update"))
        self.remove_btn.configure(text=t("chord.remove"))
        self.move_up_btn.configure(text=t("chord.move_up"))
        self.move_down_btn.configure(text=t("chord.move_down"))
        self.undo_btn.configure(text=t("history.undo"))
        self.redo_btn.configure(text=t("history.redo"))
        self.trans_down_btn.configure(text=t("transpose.down"))
        self.trans_up_btn.configure(text=t("transpose.up"))
        self.export_btn.configure(text=t("midi.export"))
        self.info_lbl.configure(text=t("information.heading"))
        if hasattr(self, "voice_lab_btn"):
            self.voice_lab_btn.configure(text=t("voice.lab.open"))

    def _on_language_change(self, preference: str) -> None:
        try:
            self.i18n.set_preference(preference)
        except OSError as exc:
            self.language_var.set(self.i18n.preference)
            messagebox.showerror(
                self.i18n.translate("settings.language.error.title"),
                str(exc),
                parent=self.root,
            )
            return
        self._localize_widgets()
        self._update_window_title()
        chords = self.controller.session.chords
        selected = self._selected_chord_index()
        first_visible = self.chord_listbox.yview()[0]
        self._render_chord_rows(chords)
        if selected is not None:
            self._select_chord_row(selected)
        self.chord_listbox.yview_moveto(first_visible)

        if not self.next_chord_panel.localize():
            self.next_chord_panel.clear()
            if selected is not None:
                self._display_chord_details(chords[selected])
            else:
                self._display_empty_info()

    def _on_open_shortcut(self, _event: tk.Event) -> str:
        self._on_open_project()
        return "break"

    def _on_save_shortcut(self, _event: tk.Event) -> str:
        self._on_save_project()
        return "break"

    def _on_new_shortcut(self, _event: tk.Event) -> str:
        self._on_new_project()
        return "break"

    def _on_undo_shortcut(self, _event: tk.Event) -> Optional[str]:
        if (
            _event.widget.winfo_class() in {"Entry", "Text"}
            and _event.widget is not self.detail_text
        ):
            return None
        self._on_undo()
        return "break"

    def _on_redo_shortcut(self, _event: tk.Event) -> Optional[str]:
        if (
            _event.widget.winfo_class() in {"Entry", "Text"}
            and _event.widget is not self.detail_text
        ):
            return None
        self._on_redo()
        return "break"

    def _on_context_shortcut(self, _event: tk.Event) -> str:
        self._on_apply_context()
        return "break"

    def _update_window_title(self) -> None:
        dirty_marker = "*" if self.controller.session.is_dirty else ""
        if self._project_path:
            title = f"{self._project_path.name} — STEPS"
        else:
            title = self.i18n.translate("app.title")
        self.root.title(f"{dirty_marker}{title}")

    def _on_save_project(self) -> bool:
        return self._save_project(save_as=False)

    def _on_new_project(self) -> bool:
        if not self._confirm_unsaved_changes():
            return False
        self.controller.new_project()
        self._project_path = None
        self._last_midi_export_directory = None
        self._load_context_controls()
        self._refresh_all()
        return True

    def _on_reviewed_catalog_error(self) -> bool:
        messagebox.showerror(
            self.i18n.translate("file.example.error.title"),
            self.i18n.translate(
                "file.example.error.message",
                error=self._reviewed_catalog_error or "Unknown catalog error",
            ),
            parent=self.root,
        )
        return False

    def _on_browse_reviewed_library(self) -> ReviewedProgressionLibraryDialog | bool:
        if not self._reviewed_examples:
            return self._on_reviewed_catalog_error()
        return ReviewedProgressionLibraryDialog(
            parent=self.root,
            examples=self._reviewed_examples,
            i18n=self.i18n,
            theme=self.theme,
            on_load=self._on_new_from_example,
        )

    def _on_new_from_example(self, prog_id: str) -> bool:
        try:
            reviewed = get_reviewed_progression(prog_id)
            if not self._confirm_unsaved_changes():
                return False
            self.controller.new_reviewed_project(reviewed)
        except (PublicationError, OSError, ValueError) as exc:
            messagebox.showerror(
                self.i18n.translate("file.example.error.title"),
                str(exc),
                parent=self.root,
            )
            return False
        self._project_path = None
        self._last_midi_export_directory = None
        self._load_context_controls()
        self._refresh_all()
        self._update_window_title()
        return True

    def _on_save_project_as(self) -> bool:
        return self._save_project(save_as=True)

    def _dialog_parent(self):
        if isinstance(self.root, tk.Misc):
            return self.root.grab_current() or self.root
        return self.root

    def _choose_project_path(self, operation: Literal["open", "save"]) -> str:
        translate = self.i18n.translate
        parent = self._dialog_parent()
        options = {
            "parent": parent,
            "title": translate(f"project.{operation}.title"),
            "filetypes": (
                (translate("project.filetype"), "*.stepsproj"),
                (translate("json.filetype"), "*.json"),
            ),
        }
        try:
            if operation == "open":
                return filedialog.askopenfilename(**options)
            title = self.controller.get_state_summary()["title"]
            return filedialog.asksaveasfilename(
                **options,
                defaultextension=".stepsproj",
                initialfile=_portable_filename(title, ".stepsproj"),
            )
        except tk.TclError:
            logger.exception("Could not open the project %s dialog", operation)
            messagebox.showerror(
                translate(f"project.{operation}.error.title"),
                translate("project.file.error.dialog"),
                parent=parent,
            )
            return ""

    def _save_project(self, save_as: bool) -> bool:
        path = None if save_as else self._project_path
        if path is None:
            selected = self._choose_project_path("save")
            if not selected:
                return False
            path = Path(selected)

        try:
            self._project_path = self.controller.save(path)
        except (StorageError, OSError, MusicTheoryError, ValueError) as exc:
            logger.warning("Could not save STEPS project", exc_info=True)
            messagebox.showerror(
                self.i18n.translate("project.save.error.title"),
                format_project_file_error(exc, path, "save", self.i18n),
                parent=self._dialog_parent(),
            )
            return False

        self._update_window_title()
        return True

    def _confirm_unsaved_changes(self) -> bool:
        if not self.controller.session.is_dirty:
            return True

        choice = messagebox.askyesnocancel(
            self.i18n.translate("project.unsaved.title"),
            self.i18n.translate("project.unsaved.message"),
            parent=self._dialog_parent(),
        )
        if choice is None:
            return False
        return self._save_project(save_as=False) if choice else True

    def _on_open_project(self) -> bool:
        selected = self._choose_project_path("open")
        if not selected or not self._confirm_unsaved_changes():
            return False

        try:
            self.controller.load(selected)
        except (StorageError, OSError, MusicTheoryError, ValueError) as exc:
            logger.warning("Could not open STEPS project", exc_info=True)
            messagebox.showerror(
                self.i18n.translate("project.open.error.title"),
                format_project_file_error(exc, selected, "open", self.i18n),
                parent=self._dialog_parent(),
            )
            return False

        self._project_path = Path(selected)
        self._last_midi_export_directory = None
        self._load_context_controls()
        self._refresh_all()
        if getattr(self.controller.session, "last_load_recovered_from_backup", False):
            backup = getattr(self.controller.session, "last_loaded_backup_path", None)
            recovery_text = (
                self.i18n.translate("project.recovery.named", backup=backup.name)
                if backup else self.i18n.translate("project.recovery.message")
            )
            messagebox.showinfo(
                self.i18n.translate("project.recovery.title"),
                recovery_text,
                parent=self.root,
            )
        elif getattr(self.controller.session, "last_load_migrations", ()):
            migrations = ", ".join(self.controller.session.last_load_migrations)
            messagebox.showinfo(
                self.i18n.translate("project.migration.title"),
                self.i18n.translate("project.migration.message", migrations=migrations),
                parent=self.root,
            )
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
            text=self.i18n.translate("workspace.heading"),
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

        self.add_btn = create_button(
            self.control_bar,
            text=self.i18n.translate("chord.add"),
            command=self._on_add_chord,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=sp.sm
        )
        self.add_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.edit_bar = tk.Frame(self.work_area, bg=colors.bg_surface, padx=sp.sm)
        self.edit_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.update_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("chord.update"),
            command=self._on_update_chord,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.update_btn.pack(side=tk.LEFT, padx=sp.xs)
        self.remove_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("chord.remove"),
            command=self._on_remove_chord,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.remove_btn.pack(side=tk.LEFT, padx=sp.xs)
        self.move_up_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("chord.move_up"),
            command=lambda: self._on_move_chord(-1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.move_up_btn.pack(side=tk.LEFT, padx=(sp.md, sp.xs))
        self.move_down_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("chord.move_down"),
            command=lambda: self._on_move_chord(1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.move_down_btn.pack(side=tk.LEFT, padx=sp.xs)
        self.undo_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("history.undo"),
            command=self._on_undo,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.undo_btn.pack(side=tk.LEFT, padx=(sp.md, sp.xs))
        self.redo_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("history.redo"),
            command=self._on_redo,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.redo_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.context_bar = tk.Frame(self.work_area, bg=colors.bg_surface, padx=sp.sm)
        self.context_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.project_title_lbl = tk.Label(
            self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.project_title_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.project_title_entry = tk.Entry(
            self.context_bar,
            width=16,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.project_title_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.project_title_entry.insert(0, self.controller.session.state.title)
        self.project_title_entry.bind("<Return>", self._on_context_shortcut)

        self.key_lbl = tk.Label(self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary)
        self.key_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.key_entry = tk.Entry(
            self.context_bar,
            width=5,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.key_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.key_entry.insert(0, self.controller.session.key_root)
        self.key_entry.bind("<Return>", self._on_context_shortcut)

        self.mode_lbl = tk.Label(self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary)
        self.mode_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.mode_var = tk.BooleanVar(self.root, value=self.controller.session.is_minor)
        self.major_btn = tk.Radiobutton(
            self.context_bar,
            text="",
            variable=self.mode_var,
            value=False,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectcolor=colors.bg_window,
            activebackground=colors.bg_surface,
        )
        self.major_btn.pack(side=tk.LEFT, padx=sp.xs)
        self.minor_btn = tk.Radiobutton(
            self.context_bar,
            text="",
            variable=self.mode_var,
            value=True,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectcolor=colors.bg_window,
            activebackground=colors.bg_surface,
        )
        self.minor_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.notation_lbl = tk.Label(
            self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.notation_lbl.pack(side=tk.LEFT, padx=(sp.sm, sp.xs))
        self.notation_var = tk.StringVar(
            self.root, value=self.controller.session.convention
        )
        self.notation_int_btn = tk.Radiobutton(
            self.context_bar,
            text="",
            variable=self.notation_var,
            value="INT",
            command=self._on_notation_change,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectcolor=colors.bg_window,
            activebackground=colors.bg_surface,
        )
        self.notation_int_btn.pack(side=tk.LEFT, padx=sp.xs)
        self.notation_de_btn = tk.Radiobutton(
            self.context_bar,
            text="",
            variable=self.notation_var,
            value="DE",
            command=self._on_notation_change,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectcolor=colors.bg_window,
            activebackground=colors.bg_surface,
        )
        self.notation_de_btn.pack(side=tk.LEFT, padx=(0, sp.sm))

        self.playback_bar = tk.Frame(self.work_area, bg=colors.bg_surface, padx=sp.sm)
        self.playback_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.tempo_lbl = tk.Label(
            self.playback_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.tempo_lbl.pack(side=tk.LEFT, padx=(sp.md, sp.xs))
        self.tempo_entry = tk.Entry(
            self.playback_bar,
            width=6,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.tempo_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.tempo_entry.insert(0, f"{self.controller.session.bpm:g}")
        self.tempo_entry.bind("<Return>", self._on_context_shortcut)

        self.meter_lbl = tk.Label(
            self.playback_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.meter_lbl.pack(side=tk.LEFT, padx=(sp.sm, sp.xs))
        self.meter_entry = tk.Entry(
            self.playback_bar,
            width=5,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.meter_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.meter_entry.insert(
            0, f"{self.controller.session.time_signature[0]}/{self.controller.session.time_signature[1]}"
        )
        self.meter_entry.bind("<Return>", self._on_context_shortcut)

        self.context_btn = create_button(
            self.playback_bar,
            text="",
            command=self._on_apply_context,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.context_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.voice_style_lbl = tk.Label(
            self.playback_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.voice_style_lbl.pack(side=tk.LEFT, padx=(sp.md, sp.xs))
        self.voice_style_var = tk.StringVar(
            self.root, value=self.controller.session.voice_leading_style.value
        )
        self.voice_style_menu = tk.OptionMenu(
            self.playback_bar,
            self.voice_style_var,
            *(style.value for style, _ in VOICE_LEADING_STYLE_OPTIONS),
            command=self._on_voice_style_change,
        )
        self.voice_style_menu.configure(
            bg=colors.bg_active,
            fg=colors.text_primary,
            activebackground=colors.bg_active,
            highlightthickness=0,
            textvariable="",
        )
        self.voice_style_menu.pack(side=tk.LEFT, padx=(0, sp.sm))

        self.timing_bar = tk.Frame(self.work_area, bg=colors.bg_surface, padx=sp.sm)
        self.timing_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.event_start_lbl = tk.Label(
            self.timing_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.event_start_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.event_start_entry = tk.Entry(
            self.timing_bar,
            width=9,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.event_start_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.event_start_entry.bind("<Return>", self._on_event_timing_shortcut)

        self.event_duration_lbl = tk.Label(
            self.timing_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.event_duration_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.event_duration_entry = tk.Entry(
            self.timing_bar,
            width=9,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
        )
        self.event_duration_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.event_duration_entry.bind("<Return>", self._on_event_timing_shortcut)

        self.event_timing_btn = create_button(
            self.timing_bar,
            text="",
            command=self._on_apply_event_timing,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.event_timing_btn.pack(side=tk.LEFT, padx=sp.xs)

        # Transpose Buttons
        self.trans_down_btn = create_button(
            self.control_bar,
            text=self.i18n.translate("transpose.down"),
            command=lambda: self._on_transpose(-1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.xs
        )
        self.trans_down_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.trans_up_btn = create_button(
            self.control_bar,
            text=self.i18n.translate("transpose.up"),
            command=lambda: self._on_transpose(1),
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.xs
        )
        self.trans_up_btn.pack(side=tk.LEFT, padx=sp.xs)

        # MIDI Export Button
        self.export_btn = create_button(
            self.control_bar,
            text=self.i18n.translate("midi.export"),
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
            activestyle="dotbox",
            exportselection=False,
            highlightthickness=2,
            highlightbackground=colors.border,
            highlightcolor=colors.border_focus,
        )
        progression_scrollbar = tk.Scrollbar(
            self.prog_frame, orient=tk.VERTICAL, command=self.chord_listbox.yview, takefocus=False,
        )
        self.chord_listbox.configure(yscrollcommand=progression_scrollbar.set)
        progression_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chord_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=sp.sm, pady=sp.sm)
        self.chord_listbox.bind("<<ListboxSelect>>", self._on_chord_selected)
        modifier = "Option" if sys.platform == "darwin" else "Alt"
        self.chord_listbox.bind(f"<{modifier}-Up>", lambda _event: self._move_chord_shortcut(-1))
        self.chord_listbox.bind(f"<{modifier}-Down>", lambda _event: self._move_chord_shortcut(1))

        # ----------------------------------------------------
        # Area 2: Informations- und Theoriebereich
        # ----------------------------------------------------
        self.info_area = tk.Frame(self.paned, bg=colors.bg_surface, bd=0)
        self.paned.add(self.info_area, minsize=260)

        self.info_bar = tk.Frame(self.info_area, bg=colors.bg_surface, pady=sp.sm, padx=sp.sm)
        self.info_bar.pack(fill=tk.X)

        self.info_lbl = tk.Label(
            self.info_bar,
            text=self.i18n.translate("information.heading"),
            font=("Helvetica", 11, "bold"),
            fg=colors.harmonic_dominant,
            bg=colors.bg_surface
        )
        self.info_lbl.pack(side=tk.LEFT)

        self.voice_lab_btn = create_button(
            self.info_bar,
            text="",
            command=self._on_open_voice_leading_lab,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=sp.sm,
        )

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
        self.detail_text.configure(state=tk.DISABLED)
        configure_readonly_preview(self.detail_text, colors)
        self.next_chord_panel = NextChordPanel(
            self.info_bar, self.detail_frame,
            controller=self.controller, i18n=self.i18n, theme=self.theme,
            selected_chord=self._selected_chord_index,
            show_detail=self._write_detail, on_applied=self._on_recommendation_applied,
        )
        self.voice_lab_btn.pack(side=tk.RIGHT, padx=sp.xs)
        detail_scrollbar = tk.Scrollbar(
            self.detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview, takefocus=False,
        )
        self.detail_text.configure(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _refresh_all(
        self,
        preserve_selection: bool = False,
        selected_index: Optional[int] = None,
    ) -> None:
        """Synchronizes UI state with the ProgressionSessionController."""
        self.next_chord_panel.clear()
        state = self.controller.get_state_summary()
        selected = self.chord_listbox.curselection() if preserve_selection else ()
        self._update_window_title()
        has_chords = bool(state["chords"])
        self.update_btn.configure(state=tk.NORMAL if has_chords else tk.DISABLED)
        self.remove_btn.configure(
            state=tk.NORMAL if len(state["chords"]) > 1 else tk.DISABLED
        )
        self.undo_btn.configure(state=tk.NORMAL if state["can_undo"] else tk.DISABLED)
        self.redo_btn.configure(state=tk.NORMAL if state["can_redo"] else tk.DISABLED)

        self._render_chord_rows(state["chords"])

        if state["chords"]:
            if selected_index is not None:
                index = max(0, min(selected_index, len(state["chords"]) - 1))
            else:
                index = min(selected[0], len(state["chords"]) - 1) if selected else 0
            self._select_chord_row(index)
            self._load_event_timing_controls(index)
            self._update_move_controls(index, len(state["chords"]))
            self._display_chord_details(state["chords"][index])
        else:
            self._load_event_timing_controls(None)
            self._update_move_controls(None, 0)
            self._display_empty_info()

    def _render_chord_rows(self, chords: list[str]) -> None:
        self.chord_listbox.delete(0, tk.END)
        t = self.i18n.translate
        for index, chord in enumerate(chords):
            position, duration = self._event_timing_display(index)
            timing = t("event.row.timing", position=position, duration=duration)
            self.chord_listbox.insert(tk.END, f"  [{index + 1:02d}]   {chord}   ·   {timing}")

    def _select_chord_row(self, index: int) -> None:
        self.chord_listbox.select_set(index)
        self.chord_listbox.activate(index)
        self.chord_listbox.selection_anchor(index)
        self.chord_listbox.see(index)

    def _event_timing_display(self, index: int) -> tuple[str, int]:
        session = self.controller.session
        start_tick, duration_ticks = session.get_chord_event_timing(index)
        bar, beat, tick = RationalMidiTime.ticks_to_bar_beat_tick(
            start_tick,
            ppq=session.state.ppq,
            numerator=session.time_signature[0],
            denominator=session.time_signature[1],
        )
        return f"{bar}:{beat}:{tick}", duration_ticks

    def _load_event_timing_controls(self, index: Optional[int]) -> None:
        position, duration_ticks = self._event_timing_display(index) if index is not None else ("", "")
        self.event_start_entry.delete(0, tk.END)
        self.event_start_entry.insert(0, position)
        self.event_duration_entry.delete(0, tk.END)
        self.event_duration_entry.insert(0, str(duration_ticks))
        self.event_timing_btn.configure(state=tk.NORMAL if index is not None else tk.DISABLED)

    def _on_event_timing_shortcut(self, _event: tk.Event) -> str:
        self._on_apply_event_timing()
        return "break"

    def _parse_event_start(self, text: str) -> int:
        fields = text.split(":")
        if len(fields) == 1:
            tick = int(fields[0])
            if tick < 0:
                raise ValueError("Start tick must be non-negative.")
            return tick
        if len(fields) != 3:
            raise ValueError("Expected an absolute tick or bar:beat:tick position.")

        session = self.controller.session
        bar, beat, tick = map(int, fields)
        numerator, denominator = session.time_signature
        return RationalMidiTime.bar_beat_tick_to_ticks(
            bar, beat, tick, ppq=session.state.ppq,
            numerator=numerator, denominator=denominator,
        )

    def _on_apply_event_timing(self) -> None:
        index = self._selected_chord_index()
        if index is None:
            return
        try:
            start_tick = self._parse_event_start(self.event_start_entry.get())
            duration_ticks = int(self.event_duration_entry.get().strip())
            self.controller.set_chord_event_timing(index, start_tick, duration_ticks)
        except ValueError:
            messagebox.showerror(
                self.i18n.translate("event.timing.error.title"),
                self.i18n.translate("event.timing.invalid"),
                parent=self.root,
            )
            return
        self._refresh_all(preserve_selection=True)

    def _load_context_controls(self) -> None:
        self.project_title_entry.delete(0, tk.END)
        self.project_title_entry.insert(0, self.controller.session.state.title)
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.controller.session.key_root)
        self.mode_var.set(self.controller.session.is_minor)
        if hasattr(self, "notation_var"):
            self.notation_var.set(self.controller.session.convention)
        self.tempo_entry.delete(0, tk.END)
        self.tempo_entry.insert(0, f"{self.controller.session.bpm:g}")
        if hasattr(self, "voice_style_var"):
            self.voice_style_var.set(self.controller.session.voice_leading_style.value)
            if hasattr(self, "voice_style_menu"):
                self._localize_voice_style_menu()
        numerator, denominator = self.controller.session.time_signature
        self.meter_entry.delete(0, tk.END)
        self.meter_entry.insert(0, f"{numerator}/{denominator}")
        self._update_event_timing_labels()

    def _update_event_timing_labels(self) -> None:
        ppq = self.controller.session.state.ppq
        self.event_start_lbl.configure(
            text=self.i18n.translate("event.start", ppq=ppq)
        )
        self.event_duration_lbl.configure(
            text=self.i18n.translate("event.duration", ppq=ppq)
        )

    def _on_notation_change(self) -> None:
        convention = self.notation_var.get()
        if convention == self.controller.session.convention:
            return
        confirmed = messagebox.askyesno(
            self.i18n.translate("notation.confirm.title"),
            self.i18n.translate(
                "notation.confirm.message",
                from_convention=self.controller.session.convention,
                to_convention=convention,
            ),
            parent=self.root,
        )
        if not confirmed:
            self.notation_var.set(self.controller.session.convention)
            return
        try:
            self.controller.set_notation_convention(convention)
        except (ValueError, MusicTheoryError) as exc:
            self.notation_var.set(self.controller.session.convention)
            messagebox.showerror(
                self.i18n.translate("notation.error.title"),
                self.i18n.translate("notation.error.message", error=exc),
                parent=self.root,
            )
            return
        self._load_context_controls()
        self._refresh_all(preserve_selection=True)

    def _localize_voice_style_menu(self) -> None:
        style_labels = {
            style.value: self.i18n.translate(label_key)
            for style, label_key in VOICE_LEADING_STYLE_OPTIONS
        }
        menu = self.voice_style_menu["menu"]
        menu.delete(0, tk.END)
        for style, _label_key in VOICE_LEADING_STYLE_OPTIONS:
            value = style.value
            menu.add_radiobutton(
                label=style_labels[value],
                value=value,
                variable=self.voice_style_var,
                command=lambda selected=value: self._on_voice_style_change(selected),
            )
        selected = self.voice_style_var.get()
        self.voice_style_menu.configure(text=style_labels.get(selected, selected))

    def _on_open_voice_leading_lab(self) -> VoiceLeadingLabDialog:
        return VoiceLeadingLabDialog(
            parent=self.root,
            controller=self.controller,
            i18n=self.i18n,
            theme=self.theme,
            on_apply=self._on_voice_style_change,
            selected_index=self._selected_chord_index(),
        )

    def _on_voice_style_change(self, style: str) -> bool:
        try:
            self.controller.set_voice_leading_style(style)
        except (ValueError, MusicTheoryError) as exc:
            self.voice_style_var.set(self.controller.session.voice_leading_style.value)
            messagebox.showerror(
                self.i18n.translate("voice.style.error.title"),
                self.i18n.translate("voice.style.error.message", error=exc),
                parent=self.root,
            )
            return False
        self._localize_voice_style_menu()
        self._refresh_all(preserve_selection=True)
        return True

    def _on_apply_context(self) -> None:
        title = self.project_title_entry.get().strip()
        if not title:
            messagebox.showerror(
                self.i18n.translate("context.error.title"),
                self.i18n.translate("project.title.invalid"),
                parent=self.root,
            )
            return
        try:
            bpm = float(self.tempo_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                self.i18n.translate("context.error.title"),
                self.i18n.translate("context.tempo.invalid"),
                parent=self.root,
            )
            return
        try:
            parts = self.meter_entry.get().strip().split("/")
            if len(parts) != 2:
                raise ValueError("Expected numerator/denominator.")
            meter = (int(parts[0].strip()), int(parts[1].strip()))
            if not 1 <= meter[0] <= 32:
                raise ValueError("Numerator must be between 1 and 32.")
            TimeSignature(*meter)
        except ValueError:
            messagebox.showerror(
                self.i18n.translate("context.error.title"),
                self.i18n.translate("context.meter.invalid"),
                parent=self.root,
            )
            return
        try:
            self.controller.set_context(
                self.key_entry.get().strip(),
                bool(self.mode_var.get()),
                bpm,
                meter,
                title=title,
            )
        except MusicTheoryError:
            messagebox.showerror(
                self.i18n.translate("context.error.title"),
                self.i18n.translate("context.key.invalid"),
                parent=self.root,
            )
            return
        except ValueError:
            messagebox.showerror(
                self.i18n.translate("context.error.title"),
                self.i18n.translate("context.tempo.invalid"),
                parent=self.root,
            )
            return
        self._load_context_controls()
        self._refresh_all(preserve_selection=True)

    def _update_move_controls(self, index: Optional[int], chord_count: int) -> None:
        self.move_up_btn.configure(
            state=tk.NORMAL if index is not None and index > 0 else tk.DISABLED
        )
        self.move_down_btn.configure(
            state=tk.NORMAL if index is not None and index < chord_count - 1 else tk.DISABLED
        )

    def _selected_chord_index(self) -> Optional[int]:
        selection = self.chord_listbox.curselection()
        return selection[0] if selection else None

    def _show_chord_change_error(self, error: Exception) -> None:
        messagebox.showerror(
            self.i18n.translate("chord.change.error.title"),
            self.i18n.translate("chord.invalid", error=error),
            parent=self.root,
        )

    def _write_detail(self, text: str, *, append: bool = False) -> None:
        self.detail_text.configure(state=tk.NORMAL)
        try:
            if not append:
                self.detail_text.delete("1.0", tk.END)
            self.detail_text.insert(tk.END, text)
        finally:
            self.detail_text.configure(state=tk.DISABLED)
        if not append:
            self.detail_text.yview_moveto(0)

    def _display_chord_details(self, chord_name: str) -> None:
        """Update the inspector, keeping optional keyboard details independent."""
        translate = self.i18n.translate
        try:
            details = format_chord_analysis(chord_name, self.controller.session.convention, translate)
        except Exception as exc:
            self._write_detail(translate("chord.hint", chord=chord_name, error=exc))
            return

        try:
            keyboard = format_beginner_voicings(self.controller.get_beginner_voicings(), translate)
            if keyboard:
                details += "\n\n" + keyboard
        except Exception:
            logger.exception("Could not render optional beginner voicing details")
        self._write_detail(details)

    def _display_empty_info(self) -> None:
        self._write_detail(self.i18n.translate("progression.empty"))

    def _on_add_chord(self) -> None:
        txt = self.chord_entry.get().strip()
        if txt:
            try:
                self.controller.add_chord(txt)
            except MusicTheoryError as exc:
                self._show_chord_change_error(exc)
                return
            self._refresh_all(selected_index=len(self.controller.session.chords) - 1)

    def _on_update_chord(self) -> None:
        index = self._selected_chord_index()
        if index is None:
            messagebox.showerror(
                self.i18n.translate("chord.change.error.title"),
                self.i18n.translate("chord.selection.required"),
                parent=self.root,
            )
            return
        try:
            self.controller.set_chord(index, self.chord_entry.get().strip())
        except MusicTheoryError as exc:
            self._show_chord_change_error(exc)
            return
        self._refresh_all(selected_index=index)

    def _on_remove_chord(self) -> None:
        index = self._selected_chord_index()
        if index is None:
            messagebox.showerror(
                self.i18n.translate("chord.change.error.title"),
                self.i18n.translate("chord.selection.required"),
                parent=self.root,
            )
            return
        try:
            self.controller.remove_chord(index)
        except ValueError:
            messagebox.showerror(
                self.i18n.translate("chord.change.error.title"),
                self.i18n.translate("chord.remove.minimum"),
                parent=self.root,
            )
            return
        self._refresh_all(selected_index=min(index, len(self.controller.session.chords) - 1))

    def _move_chord_shortcut(self, direction: Literal[-1, 1]) -> str:
        self._on_move_chord(direction)
        return "break"

    def _on_move_chord(self, direction: Literal[-1, 1]) -> None:
        index = self._selected_chord_index()
        if index is None or not 0 <= index + direction < len(self.controller.session.chords):
            return
        self.controller.move_chord(index, direction)
        self._refresh_all(selected_index=index + direction)

    def _on_undo(self) -> None:
        if self.controller.session.can_undo:
            self.controller.undo()
            self._load_context_controls()
            self._refresh_all(preserve_selection=True)

    def _on_redo(self) -> None:
        if self.controller.session.can_redo:
            self.controller.redo()
            self._load_context_controls()
            self._refresh_all(preserve_selection=True)

    def _on_transpose(self, semitones: int) -> None:
        self.controller.transpose(semitones)
        self._load_context_controls()
        self._refresh_all()

    def _on_chord_selected(self, event) -> None:
        sel = self.chord_listbox.curselection()
        if sel:
            state = self.controller.get_state_summary()
            idx = sel[0]
            if idx < len(state["chords"]):
                self._update_move_controls(idx, len(state["chords"]))
                self._load_event_timing_controls(idx)
                self.next_chord_panel.clear()
                self._display_chord_details(state["chords"][idx])

    def _on_explore_next(self) -> None:
        self.next_chord_panel.explore()

    def _on_recommendation_applied(self, index: int, recommendation: ChordRecommendation) -> None:
        self._refresh_all(selected_index=index)
        self._write_detail(
            f"\n\n{self.i18n.translate('next_chord.applied', chord=recommendation.candidate_symbol)}",
            append=True,
        )
        self.chord_listbox.focus_set()

    def _on_export_midi(self) -> MidiExportOptionsDialog:
        return MidiExportOptionsDialog(
            parent=self.root,
            i18n=self.i18n,
            theme=self.theme,
            on_export=self._export_midi_with_options,
            voicing_failures=self.controller.midi_voicing_failures(),
        )

    def _midi_export_initial_directory(self) -> dict[str, str]:
        project_directory = self._project_path.parent if self._project_path else None
        for directory in (self._last_midi_export_directory, project_directory):
            if directory is None:
                continue
            try:
                if directory.is_dir():
                    return {"initialdir": str(directory)}
            except OSError:
                continue
        return {}

    def _export_midi_with_options(self, options: MidiExportOptions) -> bool:
        blocked_chord = self.controller.midi_voicing_failures().get(options.voicing_type)
        if blocked_chord is not None:
            messagebox.showerror(
                self.i18n.translate("midi.export.error.title"),
                self.i18n.translate(
                    "midi.options.voicing.unavailable", mode=options.voicing_type, chord=blocked_chord,
                ),
                parent=self._dialog_parent(),
            )
            return False
        translate = self.i18n.translate
        parent = self._dialog_parent()
        try:
            selected = filedialog.asksaveasfilename(
                parent=parent,
                title=translate("midi.save.title"),
                defaultextension=".mid",
                filetypes=((translate("midi.filetype"), "*.mid *.midi"),),
                initialfile=_portable_filename(self.controller.session.state.title, ".mid"),
                **self._midi_export_initial_directory(),
            )
        except tk.TclError:
            logger.exception("Could not open the MIDI save dialog")
            messagebox.showerror(
                translate("midi.export.error.title"),
                translate("midi.export.error.dialog"),
                parent=parent,
            )
            return False
        if not selected:
            return False
        try:
            output_path = self.controller.export_midi(
                selected,
                voicing_type=options.voicing_type,
                note_duration_mode=options.note_duration_mode,
                smf_format=options.smf_format,
            )
        except OSError as exc:
            logger.warning("Could not write MIDI export", exc_info=True)
            messagebox.showerror(
                translate("midi.export.error.title"),
                format_midi_file_error(exc, selected, self.i18n),
                parent=parent,
            )
            return False
        except (ValueError, MusicTheoryError):
            logger.warning("Could not prepare MIDI export", exc_info=True)
            messagebox.showerror(
                translate("midi.export.error.title"),
                translate("midi.export.error.data"),
                parent=parent,
            )
            return False
        destination = output_path.absolute()
        self._last_midi_export_directory = destination.parent
        self._write_detail(
            "\n\n" + translate("midi.export.success", path=destination),
            append=True,
        )
        self.detail_text.see(tk.END)
        return True
