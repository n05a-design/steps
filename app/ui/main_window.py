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
from functools import partial
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Literal, Optional

from glide_shell import app_host, custom_controls, desktop_adapter, window_lifetime

from app.brand import apply_window_icon, load_in_app_logo
from app.i18n import LocaleManager
from app.knowledge import get_reviewed_progression, list_reviewed_progressions
from app.ui import layout_policy
from app.ui.custom_widgets import RoundedSurfaceCard
from app.ui.dialog_support import configure_readonly_preview
from app.ui.file_feedback import format_project_file_error
from app.ui.harmonic_inspector import format_beginner_voicings, format_chord_analysis
from app.ui.midi_export_dialog import (
    MidiExportOptions,
    MidiExportOptionsDialog,
    format_midi_file_error,
)
from app.settings import load_settings, save_settings
from app.ui.next_chord_panel import NextChordPanel
from app.ui.reviewed_library_dialog import ReviewedProgressionLibraryDialog
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import (
    ACCENT_CHOICES,
    BACKGROUND_CHOICES,
    FONT_SCALE_CHOICES,
    FONT_WEIGHT_CHOICES,
    RADIUS_CHOICES,
    ThemeManager,
    apply_window_geometry,
    create_button,
    default_theme,
    retheme_button,
    set_button_active,
    style_entry,
    style_surface_card,
)
from glide_shell.custom_controls import ThemedAutoScrollbar
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

_CHORD_EVENT_SHORTCUTS = (("duplicate", "d"), ("split", "t"))

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

    THEME_OPTIONS: tuple[tuple[str, str], ...] = (
        ("system", "theme.system"),
        ("dark", "theme.dark"),
        ("light", "theme.light"),
        ("glass-dark", "theme.glass_dark"),
        ("glass-light", "theme.glass_light"),
        ("dopamine", "theme.dopamine"),
        ("contrast-dark", "theme.contrast_dark"),
        ("contrast-light", "theme.contrast_light"),
        ("minimal-dark", "theme.minimal_dark"),
        ("minimal-light", "theme.minimal_light"),
        ("pixel", "theme.pixel"),
    )

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
        self._sidebar_visible: bool = True
        self._sidebar_narrow: bool = False
        self._compact_state: Optional[dict[str, object]] = None
        self._saved_compact_geometry: str = ""
        self._header_density: str = "full"
        self._height_density: str = "full"
        self._header_logo_image = None

        # Load persisted appearance and user preferences (Glide parity)
        self._user_settings = load_settings()
        if locale_manager is None:
            saved_lang = self._user_settings.get("language", "system")
            if saved_lang in ("de", "en", "system"):
                try:
                    self.i18n.set_preference(saved_lang, persist=False)
                except Exception:
                    pass
        self.theme.set_background_choice(self._user_settings.get("background_color", "default"))
        if hasattr(self.theme, "set_accent_choice"):
            self.theme.set_accent_choice(self._user_settings.get("accent_color", "accent"))
        self.theme.set_radius_choice(self._user_settings.get("corner_radius", "standard"))
        self.theme.set_font_scale_choice(self._user_settings.get("font_scale", "standard"))
        if hasattr(self.theme, "set_font_weight_choice"):
            self.theme.set_font_weight_choice(self._user_settings.get("font_weight", "standard"))
        if hasattr(self.theme, "set_animations_enabled"):
            self.theme.set_animations_enabled(self._user_settings.get("animations_enabled", True))
        if hasattr(self.theme, "set_hints_visible"):
            self.theme.set_hints_visible(self._user_settings.get("hints_visible", True))
        self._theme_preference: str = self._user_settings.get("theme_preference", self.theme.mode)

        saved_geom = str(self._user_settings.get("window_geometry") or "").strip()
        saved_compact = str(self._user_settings.get("saved_compact_geometry") or "").strip()
        if saved_compact:
            self._saved_compact_geometry = saved_compact

        self.root.title(self.i18n.translate("app.title"))
        self.theme.configure_shell_providers(self.root)
        if isinstance(self.root, tk.Misc):
            restored = False
            if saved_geom:
                try:
                    parsed = layout_policy.window_geometry.parse(saved_geom)
                    if parsed:
                        w, h, x, y = parsed
                        screen_w = int(self.root.winfo_screenwidth())
                        screen_h = int(self.root.winfo_screenheight())
                        cw, ch, cx, cy = layout_policy.window_geometry.clamp(
                            w, h, x, y, screen_w, screen_h, (860, 600)
                        )
                        self.root.geometry(layout_policy.window_geometry.format_geometry(cw, ch, cx, cy))
                        self.root.minsize(860, 600)
                        restored = True
                except Exception:
                    pass
            if not restored:
                apply_window_geometry(self.root, 1024, 720, 860, 600)
            self._lifetime_scope = window_lifetime.scope_for(self.root)
        else:
            self.root.geometry("1024x720")
            self.root.minsize(860, 600)
            self._lifetime_scope = None
        self._init_file_menu()

        # A missing optional icon must not prevent startup.
        try:
            apply_window_icon(self.root)
        except Exception:
            logger.exception("Could not apply the STEPS window icon")

        self._init_ui()
        self._localize_widgets()
        self._refresh_all()

    def _window_platform(self) -> str:
        try:
            windowing = self.root.tk.call("tk", "windowingsystem")
            return app_host.platform_of(windowing)
        except Exception:
            return desktop_adapter.platform_name()

    def _init_file_menu(self) -> None:
        shortcut = "⌘" if desktop_adapter.is_macos() else "Ctrl+"
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
        self.chord_menu = tk.Menu(self.menu_bar, tearoff=False)
        for action, key in _CHORD_EVENT_SHORTCUTS:
            self.chord_menu.add_command(
                label="", accelerator=f"{shortcut}{key.upper()}", state=tk.DISABLED,
                command=lambda selected=action: self._on_chord_event_edit(selected),
            )
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        for action in (self._on_explore_next, self._on_open_voice_leading_lab, self._on_export_midi):
            self.tools_menu.add_command(label="", command=action)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.settings_menu.add_command(
            label="",
            command=self._on_open_appearance_dialog,
            accelerator=f"{shortcut},",
        )
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
        self.theme_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.theme_var = tk.StringVar(self.root, value=self._theme_preference)
        for preference, _ in self.THEME_OPTIONS:
            self.theme_menu.add_radiobutton(
                label="",
                value=preference,
                variable=self.theme_var,
                command=lambda selected=preference: self.set_theme_preference(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.theme_menu)
        self.accent_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.accent_var = tk.StringVar(self.root, value=getattr(self.theme, "accent_choice", "accent"))
        for choice, _ in ACCENT_CHOICES:
            self.accent_menu.add_radiobutton(
                label="",
                value=choice,
                variable=self.accent_var,
                command=lambda selected=choice: self._on_accent_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.accent_menu)
        self.bg_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.bg_var = tk.StringVar(self.root, value=self.theme.background_choice)
        for choice, _ in BACKGROUND_CHOICES:
            self.bg_menu.add_radiobutton(
                label="",
                value=choice,
                variable=self.bg_var,
                command=lambda selected=choice: self._on_background_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.bg_menu)
        self.radius_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.radius_var = tk.StringVar(self.root, value=self.theme.radius_choice)
        for choice, _, _ in RADIUS_CHOICES:
            self.radius_menu.add_radiobutton(
                label="",
                value=choice,
                variable=self.radius_var,
                command=lambda selected=choice: self._on_radius_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.radius_menu)
        self.scale_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.scale_var = tk.StringVar(self.root, value=self.theme.font_scale_choice)
        for choice, _, _ in FONT_SCALE_CHOICES:
            self.scale_menu.add_radiobutton(
                label="",
                value=choice,
                variable=self.scale_var,
                command=lambda selected=choice: self._on_scale_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.scale_menu)
        self.weight_menu = tk.Menu(self.settings_menu, tearoff=False)
        self.weight_var = tk.StringVar(self.root, value=getattr(self.theme, "font_weight_choice", "standard"))
        for choice, _ in FONT_WEIGHT_CHOICES:
            self.weight_menu.add_radiobutton(
                label="",
                value=choice,
                variable=self.weight_var,
                command=lambda selected=choice: self._on_weight_change(selected),
            )
        self.settings_menu.add_cascade(label="", menu=self.weight_menu)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="",
            command=self.toggle_sidebar,
            accelerator=f"{shortcut}B",
        )
        self.settings_menu.add_command(
            label="",
            command=self.toggle_sidebar_narrow,
            accelerator=f"{shortcut}Shift+B",
        )
        self.settings_menu.add_command(
            label="",
            command=self.toggle_compact_mode,
            accelerator=f"{shortcut}Shift+K",
        )
        self.menu_bar.add_cascade(label="", menu=self.settings_menu)
        if not app_host.attach_menubar(self.root, self.menu_bar):
            self.root.configure(menu=self.menu_bar)
        shortcut_entries = []
        for key, handler, shift in (
            ("o", self._on_open_shortcut, False),
            ("s", self._on_save_shortcut, False),
            ("n", self._on_new_shortcut, False),
            ("z", self._on_undo_shortcut, False),
            ("z", self._on_redo_shortcut, True),
            ("b", self._on_toggle_sidebar_shortcut, False),
            ("b", self._on_toggle_sidebar_narrow_shortcut, True),
            ("k", self._on_toggle_compact_shortcut, True),
            (",", self._on_appearance_shortcut, False),
        ):
            shortcut_entries.extend(
                app_host.primary_shortcuts(key, handler, app_host.MACOS, shift=shift)
            )
        app_host.bind_shortcuts(self.root, shortcut_entries, app_host.MACOS)
        app_host.install_close(
            self.root,
            self._on_close,
            self._window_platform(),
            scope=getattr(self, "_lifetime_scope", None),
        )

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
        self.menu_bar.add_cascade(label=t("chord.menu"), menu=self.chord_menu)
        for index, (action, _) in enumerate(_CHORD_EVENT_SHORTCUTS):
            self.chord_menu.entryconfigure(index, label=t(f"chord.event.{action}"))
        self.menu_bar.add_cascade(label=t("tools.menu"), menu=self.tools_menu)
        for index, key in enumerate(("next_chord.explore", "voice.lab.open", "midi.export")):
            self.tools_menu.entryconfigure(index, label=t(key))
        self.menu_bar.add_cascade(label=t("settings.menu"), menu=self.settings_menu)
        if (
            callable(getattr(self.settings_menu, "index", None))
            and self.settings_menu.index(tk.END) is not None
            and self.settings_menu.index(tk.END) >= 8
        ):
            self.settings_menu.entryconfigure(0, label=t("settings.appearance"))
            self.settings_menu.entryconfigure(1, label=t("language.menu"))
            self.settings_menu.entryconfigure(2, label=t("theme.menu"))
            self.settings_menu.entryconfigure(3, label=t("theme.accent.menu"))
            self.settings_menu.entryconfigure(4, label=t("theme.background.menu"))
            self.settings_menu.entryconfigure(5, label=t("theme.radius.menu"))
            self.settings_menu.entryconfigure(6, label=t("theme.font_scale.menu"))
            self.settings_menu.entryconfigure(7, label=t("theme.font_weight.menu"))
            if hasattr(self, "theme_menu") and callable(getattr(self.theme_menu, "entryconfigure", None)):
                for index, (_, key) in enumerate(self.THEME_OPTIONS):
                    self.theme_menu.entryconfigure(index, label=t(key))
            if hasattr(self, "accent_menu") and callable(getattr(self.accent_menu, "entryconfigure", None)):
                for index, (_, key) in enumerate(ACCENT_CHOICES):
                    self.accent_menu.entryconfigure(index, label=t(key))
            if hasattr(self, "bg_menu") and callable(getattr(self.bg_menu, "entryconfigure", None)):
                for index, (_, key) in enumerate(BACKGROUND_CHOICES):
                    self.bg_menu.entryconfigure(index, label=t(key))
            if hasattr(self, "radius_menu") and callable(getattr(self.radius_menu, "entryconfigure", None)):
                for index, (_, key, _) in enumerate(RADIUS_CHOICES):
                    self.radius_menu.entryconfigure(index, label=t(key))
            if hasattr(self, "scale_menu") and callable(getattr(self.scale_menu, "entryconfigure", None)):
                for index, (_, key, _) in enumerate(FONT_SCALE_CHOICES):
                    self.scale_menu.entryconfigure(index, label=t(key))
            if hasattr(self, "weight_menu") and callable(getattr(self.weight_menu, "entryconfigure", None)):
                for index, (_, key) in enumerate(FONT_WEIGHT_CHOICES):
                    self.weight_menu.entryconfigure(index, label=t(key))
            self.settings_menu.entryconfigure(9, label=t("view.sidebar.toggle"))
            self.settings_menu.entryconfigure(10, label=t("view.sidebar.narrow"))
            self.settings_menu.entryconfigure(11, label=t("view.compact.toggle"))
        elif (
            callable(getattr(self.settings_menu, "index", None))
            and self.settings_menu.index(tk.END) is not None
            and self.settings_menu.index(tk.END) >= 0
        ):
            self.settings_menu.entryconfigure(0, label=t("language.menu"))
        for index, key in enumerate(("language.system", "language.en", "language.de")):
            self.language_menu.entryconfigure(index, label=t(key))
        self._localize_sidebar_widgets()
        self.title_lbl.configure(text=layout_policy.clip_title(t("workspace.heading")))
        self._update_header_subtitle()
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
        self._persist_settings()
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
                self._display_chord_details(chords[selected], index=selected)
            else:
                self._display_empty_info()

    def _persist_settings(self) -> None:
        try:
            geom = ""
            if hasattr(self, "root") and isinstance(self.root, tk.Misc):
                try:
                    geom = self.root.geometry()
                except Exception:
                    pass
            self._user_settings.update({
                "theme_preference": self._theme_preference,
                "background_color": self.theme.background_choice,
                "accent_color": getattr(self.theme, "accent_choice", "accent"),
                "corner_radius": self.theme.radius_choice,
                "font_scale": self.theme.font_scale_choice,
                "font_weight": getattr(self.theme, "font_weight_choice", "standard"),
                "animations_enabled": getattr(self.theme, "animations_enabled", True),
                "hints_visible": getattr(self.theme, "hints_visible", True),
                "language": self.i18n.preference,
                "window_geometry": geom or self._user_settings.get("window_geometry", ""),
                "saved_compact_geometry": getattr(self, "_saved_compact_geometry", ""),
            })
            save_settings(self._user_settings)
        except Exception:
            pass

    def _on_appearance_shortcut(self, _event: Optional[tk.Event] = None) -> None:
        self._on_open_appearance_dialog()

    def _on_open_appearance_dialog(self) -> None:
        from app.ui.appearance_dialog import AppearanceDialog

        def _apply(
            theme_mode: str,
            bg_choice: str,
            radius_choice: str,
            scale_choice: str,
            accent_choice: str = "accent",
            weight_choice: str = "standard",
            animations_enabled: bool = True,
            hints_visible: bool = True,
        ) -> None:
            self.set_theme_preference(theme_mode)
            self._on_background_change(bg_choice)
            self._on_radius_change(radius_choice)
            self._on_scale_change(scale_choice)
            self._on_accent_change(accent_choice)
            self._on_weight_change(weight_choice)
            if hasattr(self.theme, "set_animations_enabled"):
                self.theme.set_animations_enabled(animations_enabled)
            if hasattr(self.theme, "set_hints_visible"):
                self.theme.set_hints_visible(hints_visible)
            self._persist_settings()

        AppearanceDialog(
            parent=self.root,
            theme=self.theme,
            i18n=self.i18n,
            theme_preference=self._theme_preference,
            on_apply=_apply,
        )

    def _on_background_change(self, choice: str) -> None:
        self.theme.set_background_choice(choice)
        if hasattr(self, "bg_var"):
            self.bg_var.set(choice)
        self.apply_theme()
        self._persist_settings()

    def _on_accent_change(self, choice: str) -> None:
        if hasattr(self.theme, "set_accent_choice"):
            self.theme.set_accent_choice(choice)
        if hasattr(self, "accent_var"):
            self.accent_var.set(choice)
        self.apply_theme()
        self._persist_settings()

    def _on_radius_change(self, choice: str) -> None:
        self.theme.set_radius_choice(choice)
        if hasattr(self, "radius_var"):
            self.radius_var.set(choice)
        self.apply_theme()
        self._persist_settings()

    def _on_scale_change(self, choice: str) -> None:
        self.theme.set_font_scale_choice(choice)
        if hasattr(self, "scale_var"):
            self.scale_var.set(choice)
        self.apply_theme()
        self._persist_settings()

    def _on_weight_change(self, choice: str) -> None:
        if hasattr(self.theme, "set_font_weight_choice"):
            self.theme.set_font_weight_choice(choice)
        if hasattr(self, "weight_var"):
            self.weight_var.set(choice)
        self.apply_theme()
        self._persist_settings()

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

    def _on_new_from_example(
        self, prog_id: str, semitones: int = 0, convention: Literal["INT", "DE"] = "INT",
    ) -> bool:
        try:
            reviewed = get_reviewed_progression(prog_id)
            if not self._confirm_unsaved_changes():
                return False
            self.controller.new_reviewed_project(reviewed, semitones, convention)
        except (MusicTheoryError, OSError, ValueError) as exc:
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
            self._persist_settings()
            self.root.destroy()

    def _on_toggle_sidebar_shortcut(self, _event: tk.Event) -> str:
        self.toggle_sidebar()
        return "break"

    def _on_toggle_sidebar_narrow_shortcut(self, _event: tk.Event) -> str:
        self.toggle_sidebar_narrow()
        return "break"

    def _on_toggle_compact_shortcut(self, _event: tk.Event) -> str:
        self.toggle_compact_mode()
        return "break"

    def _focus_workspace(self) -> None:
        if hasattr(self, "chord_listbox"):
            self.chord_listbox.focus_set()

    def _sidebar_nav_items(self) -> tuple[tuple[str, str, str, object], ...]:
        return (
            ("workspace", "sidebar.nav.workspace", "sidebar.rail.workspace", self._focus_workspace),
            ("explorer", "sidebar.nav.explorer", "sidebar.rail.explorer", self._on_explore_next),
            ("voice_lab", "sidebar.nav.voice_lab", "sidebar.rail.voice_lab", self._on_open_voice_leading_lab),
            ("library", "sidebar.nav.library", "sidebar.rail.library", self._on_browse_reviewed_library),
            ("midi", "sidebar.nav.midi", "sidebar.rail.midi", self._on_export_midi),
        )

    def _build_sidebar(self) -> None:
        colors = self.theme.colors
        sp = self.theme.spacing

        self.sidebar_frame = RoundedSurfaceCard(
            self.shell_frame,
            bg_color=colors.bg_window,
            fill_color=colors.bg_surface,
            outline_color=colors.border,
            radius=self.theme.corner_radius,
            padding=sp.xs,
            width=layout_policy.SIDEBAR_WIDE_WIDTH,
        )
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_heading_lbl = tk.Label(
            self.sidebar_frame.inner,
            text="",
            font=self.theme.font_spec(layout_policy.FONT_SIZES["caption"], "bold"),
            fg=colors.text_secondary,
            bg=colors.bg_surface,
            anchor=tk.W,
            padx=sp.sm,
            pady=sp.sm,
        )
        self.sidebar_heading_lbl.pack(fill=tk.X)

        self._sidebar_buttons: dict[str, tk.Button | tk.ttk.Button] = {}
        for item_id, _nav_key, _rail_key, callback in self._sidebar_nav_items():
            btn = create_button(
                self.sidebar_frame.inner,
                text="",
                command=callback,
                bg=colors.bg_surface,
                fg=colors.text_primary,
                hover_bg=colors.bg_surface_hover,
                active_bg=colors.bg_active,
                active_fg=colors.harmonic_tonic,
                relief=tk.FLAT,
                anchor=tk.W,
                padx=sp.sm,
            )
            btn.pack(fill=tk.X, padx=sp.xs, pady=2)
            self._sidebar_buttons[item_id] = btn
        set_button_active(self._sidebar_buttons["workspace"], True, colors)

        self.sidebar_collapse_btn = create_button(
            self.sidebar_frame.inner,
            text="",
            command=self.toggle_sidebar_narrow,
            bg=colors.bg_active,
            fg=colors.text_primary,
            hover_bg=colors.bg_surface_hover,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.sidebar_collapse_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=sp.xs, pady=sp.xs)

        self.sidebar_rail_frame = RoundedSurfaceCard(
            self.shell_frame,
            bg_color=colors.bg_window,
            fill_color=colors.bg_surface,
            outline_color=colors.border,
            radius=self.theme.corner_radius,
            padding=sp.xs,
            width=layout_policy.SIDEBAR_RAIL_WIDTH,
        )
        self.sidebar_rail_frame.pack_propagate(False)
        self._rail_buttons: list[tk.Button | tk.ttk.Button] = []
        self._rail_button_map: dict[str, tk.Button | tk.ttk.Button] = {}
        for item_id, _nav_key, _rail_key, callback in self._sidebar_nav_items():
            btn = create_button(
                self.sidebar_rail_frame.inner,
                text="",
                command=callback,
                bg=colors.bg_surface,
                fg=colors.text_primary,
                hover_bg=colors.bg_surface_hover,
                active_bg=colors.bg_active,
                active_fg=colors.harmonic_tonic,
                relief=tk.FLAT,
                padx=sp.xs,
            )
            btn.pack(fill=tk.X, padx=sp.xs, pady=2)
            self._rail_buttons.append(btn)
            self._rail_button_map[item_id] = btn
        set_button_active(self._rail_button_map["workspace"], True, colors)

        self.sidebar_expand_btn = create_button(
            self.sidebar_rail_frame.inner,
            text="",
            command=self.toggle_sidebar_narrow,
            bg=colors.bg_active,
            fg=colors.text_primary,
            hover_bg=colors.bg_surface_hover,
            relief=tk.FLAT,
            padx=sp.xs,
        )
        self.sidebar_expand_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=sp.xs, pady=sp.xs)
        self._rail_buttons.append(self.sidebar_expand_btn)

        for idx, rail_btn in enumerate(self._rail_buttons):
            rail_btn.bind(
                "<Down>",
                lambda _e, i=idx: self._focus_rail_button((i + 1) % len(self._rail_buttons)),
            )
            rail_btn.bind(
                "<Up>",
                lambda _e, i=idx: self._focus_rail_button((i - 1) % len(self._rail_buttons)),
            )

    def _focus_rail_button(self, index: int) -> str:
        self._rail_buttons[index].focus_set()
        return "break"

    def _localize_sidebar_widgets(self) -> None:
        if not hasattr(self, "sidebar_heading_lbl"):
            return
        t = self.i18n.translate
        self.sidebar_heading_lbl.configure(text=t("sidebar.heading"))
        self.sidebar_toggle_btn.configure(text=t("view.sidebar.button"))
        self.sidebar_collapse_btn.configure(text=t("view.sidebar.collapse"))
        self.sidebar_expand_btn.configure(text=t("view.sidebar.expand"))
        for item_id, nav_key, rail_key, _callback in self._sidebar_nav_items():
            self._sidebar_buttons[item_id].configure(text=layout_policy.clip_button_text(t(nav_key)))
            self._rail_button_map[item_id].configure(text=t(rail_key))

    def _current_window_width(self) -> int:
        try:
            width = int(self.root.winfo_width())
            if width <= 1:
                parsed = layout_policy.window_geometry.parse(self.root.geometry())
                if parsed is not None:
                    return parsed[0]
            return width
        except Exception:
            return 1024

    def _current_window_height(self) -> int:
        try:
            height = int(self.root.winfo_height())
            if height <= 1:
                parsed = layout_policy.window_geometry.parse(self.root.geometry())
                if parsed is not None:
                    return parsed[1]
            return height
        except Exception:
            return 720

    def effective_sidebar_mode(self, width: Optional[int] = None) -> layout_policy.SidebarMode:
        w = self._current_window_width() if width is None else width
        return layout_policy.effective_sidebar_mode(
            self._sidebar_visible,
            self._sidebar_narrow,
            self.compact_mode_active(),
            w,
        )

    def _apply_sidebar_visibility(self, width: Optional[int] = None) -> None:
        if not hasattr(self, "sidebar_frame") or not hasattr(self, "paned"):
            return
        sp = self.theme.spacing
        mode = self.effective_sidebar_mode(width)
        if mode == "wide":
            self.sidebar_rail_frame.pack_forget()
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, sp.sm), before=self.paned)
        elif mode == "rail":
            self.sidebar_frame.pack_forget()
            self.sidebar_rail_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, sp.sm), before=self.paned)
        else:
            self.sidebar_frame.pack_forget()
            self.sidebar_rail_frame.pack_forget()
        if hasattr(self, "sidebar_toggle_btn"):
            set_button_active(self.sidebar_toggle_btn, mode == "hidden", self.theme.colors)

    def toggle_sidebar(self) -> str:
        self._sidebar_visible = not self._sidebar_visible
        self._apply_sidebar_visibility()
        return "break"

    def toggle_sidebar_narrow(self) -> str:
        self._sidebar_narrow = not self._sidebar_narrow
        self._sidebar_visible = True
        self._apply_sidebar_visibility()
        return "break"

    def compact_mode_active(self) -> bool:
        return self._compact_state is not None

    def toggle_compact_mode(self) -> str:
        if self.compact_mode_active():
            return self.leave_compact_mode()
        return self.enter_compact_mode()

    def enter_compact_mode(self) -> str:
        if self.compact_mode_active():
            return "break"
        try:
            normal = self.root.geometry()
            screen_w = int(self.root.winfo_screenwidth())
            screen_h = int(self.root.winfo_screenheight())
        except tk.TclError:
            return "break"
        self._compact_state = {"normal_geometry": normal}
        sp = self.theme.spacing
        self.shell_frame.pack_configure(padx=sp.xs, pady=sp.xs)
        self._apply_sidebar_visibility()
        self.sync_header_logo()
        self.root.minsize(*layout_policy.COMPACT_MIN)
        self.root.geometry(
            layout_policy.compact_geometry(
                normal, self._saved_compact_geometry, screen_w, screen_h
            )
        )
        return "break"

    def leave_compact_mode(self) -> str:
        state = self._compact_state
        if state is None:
            return "break"
        try:
            self._saved_compact_geometry = self.root.geometry()
        except tk.TclError:
            pass
        self._compact_state = None
        sp = self.theme.spacing
        self.shell_frame.pack_configure(padx=sp.sm, pady=sp.sm)
        self.root.minsize(*layout_policy.NORMAL_MIN)
        try:
            self.root.geometry(
                layout_policy.normal_geometry(
                    str(state.get("normal_geometry") or ""), self.root.geometry()
                )
            )
        except tk.TclError:
            pass
        self._apply_sidebar_visibility()
        self.sync_header_logo()
        return "break"

    def _update_header_subtitle(self) -> None:
        if not hasattr(self, "subtitle_lbl"):
            return
        session = self.controller.session
        t = self.i18n.translate
        mode_label = t("context.minor" if session.is_minor else "context.major")
        numerator, denominator = session.time_signature
        subtitle = t(
            "workspace.subtitle",
            count=len(session.chords),
            key=session.key_root,
            mode=mode_label,
            bpm=f"{session.bpm:g}",
            meter=f"{numerator}/{denominator}",
        )
        self.subtitle_lbl.configure(text=layout_policy.clip_title(subtitle))

    def sync_header_logo(self) -> None:
        logo_lbl = getattr(self, "header_logo_lbl", None)
        subtitle_lbl = getattr(self, "subtitle_lbl", None)
        if logo_lbl is None or not hasattr(self, "title_lbl"):
            return
        show_logo_and_subtitle = (
            self._header_logo_image is not None
            and self._header_density != "minimal"
            and not self.compact_mode_active()
        )
        if not show_logo_and_subtitle:
            logo_lbl.pack_forget()
            if subtitle_lbl is not None:
                subtitle_lbl.pack_forget()
            return
        sp = self.theme.spacing
        anchor_target = getattr(self, "header_title_box", self.title_lbl)
        if not logo_lbl.winfo_manager():
            logo_lbl.pack(side=tk.LEFT, padx=(0, sp.xs), before=anchor_target)
        if subtitle_lbl is not None:
            self._update_header_subtitle()
            if not subtitle_lbl.winfo_manager():
                subtitle_lbl.pack(side=tk.TOP, anchor=tk.W)

    def _sync_height_density(self) -> None:
        if not hasattr(self, "control_bar"):
            return
        sp = self.theme.spacing
        pad_y = 2 if self._height_density == "minimal" else sp.xs
        self.control_bar.configure(pady=sp.xs if self._height_density == "minimal" else sp.sm)
        for bar in (self.edit_bar, self.context_bar, self.playback_bar, self.timing_bar):
            bar.pack_configure(pady=(0, pad_y))
        if hasattr(self, "toolbar_card") and hasattr(self.toolbar_card, "_sync_auto_height"):
            self.toolbar_card._sync_auto_height()

    def _on_window_resize(self, event: tk.Event) -> None:
        width = getattr(event, "width", 0) or self._current_window_width()
        height = getattr(event, "height", 0) or self._current_window_height()
        if width <= 1 or height <= 1:
            return
        self._header_density = layout_policy.header_density(width)
        self._height_density = layout_policy.height_density(height)
        self.sync_header_logo()
        self._sync_height_density()
        self._apply_sidebar_visibility(width=width)

    def _init_ui(self) -> None:
        colors = self.theme.colors
        sp = self.theme.spacing

        self.root.configure(bg=colors.bg_window)

        self.shell_frame = tk.Frame(self.root, bg=colors.bg_window, bd=0)
        self.shell_frame.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=sp.sm)
        self._build_sidebar()

        # Main vertical PanedWindow (right workspace + theory split)
        self.paned = tk.PanedWindow(
            self.shell_frame,
            orient=tk.VERTICAL,
            bg=colors.bg_window,
            bd=0,
            sashrelief=tk.FLAT,
            sashwidth=4,
        )
        self.paned.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ----------------------------------------------------
        # Area 1: Arbeitsbereich (Timeline & Progression)
        # ----------------------------------------------------
        self.work_area = tk.Frame(self.paned, bg=colors.bg_window, bd=0)
        self.paned.add(self.work_area, minsize=260)

        self.toolbar_card = self.theme.make_surface_card(
            self.work_area,
            radius=self.theme.corner_radius,
            padding=sp.xs,
            auto_height=True,
        )
        self.toolbar_card.pack(fill=tk.X, padx=sp.sm, pady=(0, sp.xs))

        # Top Control Bar (Sidebar toggle, Logo, Title, Add Chord, Transpose, Export)
        self.control_bar = tk.Frame(self.toolbar_card.inner, bg=colors.bg_surface, pady=sp.sm, padx=sp.sm)
        self.control_bar.pack(fill=tk.X)

        self.sidebar_toggle_btn = create_button(
            self.control_bar,
            text="",
            command=self.toggle_sidebar,
            bg=colors.bg_active,
            fg=colors.text_primary,
            hover_bg=colors.bg_surface_hover,
            active_bg=colors.harmonic_tonic,
            active_fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=sp.xs,
        )
        self.sidebar_toggle_btn.pack(side=tk.LEFT, padx=(0, sp.xs))

        try:
            self._header_logo_image = load_in_app_logo(self.root, target_height=28)
        except Exception:
            self._header_logo_image = None
        self.header_logo_lbl = tk.Label(
            self.control_bar,
            image=self._header_logo_image if self._header_logo_image is not None else "",
            bg=colors.bg_surface,
            bd=0,
        )

        self.header_title_box = tk.Frame(self.control_bar, bg=colors.bg_surface, bd=0)
        self.header_title_box.pack(side=tk.LEFT, padx=(0, sp.md))

        self.title_lbl = tk.Label(
            self.header_title_box,
            text=layout_policy.clip_title(self.i18n.translate("workspace.heading")),
            font=self.theme.font_spec(self.theme.typography.size_md, "bold"),
            fg=colors.harmonic_tonic,
            bg=colors.bg_surface,
            anchor=tk.W,
        )
        self.title_lbl.pack(side=tk.TOP, anchor=tk.W)

        self.subtitle_lbl = tk.Label(
            self.header_title_box,
            text="",
            font=self.theme.font_spec(layout_policy.FONT_SIZES["caption"], "bold"),
            fg=colors.text_secondary,
            bg=colors.bg_surface,
            anchor=tk.W,
        )

        w = self._current_window_width()
        h = self._current_window_height()
        self._header_density = layout_policy.header_density(w)
        self._height_density = layout_policy.height_density(h)
        self._apply_sidebar_visibility(width=w)
        self.sync_header_logo()
        custom_controls.bind_resize(self.root, self._on_window_resize, add="+")

        # Add Chord Entry & Button
        self.chord_entry = tk.Entry(
            self.control_bar,
            width=10,
            font=self.theme.font_spec(layout_policy.FONT_SIZES["body"], mono=True),
        )
        style_entry(self.chord_entry, colors)
        self.chord_entry.pack(side=tk.LEFT, padx=sp.xs)
        self.chord_entry.insert(0, "Cmaj7")

        self.add_btn = create_button(
            self.control_bar,
            text=self.i18n.translate("chord.add"),
            command=self._on_add_chord,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            hover_bg=colors.harmonic_tonic,
            relief=tk.FLAT,
            padx=sp.sm
        )
        self.add_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.edit_bar = tk.Frame(self.toolbar_card.inner, bg=colors.bg_surface, padx=sp.sm)
        self.edit_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.update_btn = create_button(
            self.edit_bar,
            text=self.i18n.translate("chord.update"),
            command=self._on_update_chord,
            bg=colors.bg_active,
            fg=colors.text_primary,
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
            relief=tk.FLAT,
            padx=sp.sm,
        )
        self.redo_btn.pack(side=tk.LEFT, padx=sp.xs)

        self.context_bar = tk.Frame(self.toolbar_card.inner, bg=colors.bg_surface, padx=sp.sm)
        self.context_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.project_title_lbl = tk.Label(
            self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.project_title_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.project_title_entry = tk.Entry(self.context_bar, width=16)
        style_entry(self.project_title_entry, colors)
        self.project_title_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.project_title_entry.insert(0, self.controller.session.state.title)
        self.project_title_entry.bind("<Return>", self._on_context_shortcut)

        self.key_lbl = tk.Label(self.context_bar, text="", bg=colors.bg_surface, fg=colors.text_primary)
        self.key_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.key_entry = tk.Entry(self.context_bar, width=5)
        style_entry(self.key_entry, colors)
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

        self.playback_bar = tk.Frame(self.toolbar_card.inner, bg=colors.bg_surface, padx=sp.sm)
        self.playback_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.tempo_lbl = tk.Label(
            self.playback_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.tempo_lbl.pack(side=tk.LEFT, padx=(sp.md, sp.xs))
        self.tempo_entry = tk.Entry(self.playback_bar, width=6)
        style_entry(self.tempo_entry, colors)
        self.tempo_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.tempo_entry.insert(0, f"{self.controller.session.bpm:g}")
        self.tempo_entry.bind("<Return>", self._on_context_shortcut)

        self.meter_lbl = tk.Label(
            self.playback_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.meter_lbl.pack(side=tk.LEFT, padx=(sp.sm, sp.xs))
        self.meter_entry = tk.Entry(self.playback_bar, width=5)
        style_entry(self.meter_entry, colors)
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
            hover_bg=colors.bg_surface_hover,
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

        self.timing_bar = tk.Frame(self.toolbar_card.inner, bg=colors.bg_surface, padx=sp.sm)
        self.timing_bar.pack(fill=tk.X, pady=(0, sp.xs))
        self.event_start_lbl = tk.Label(
            self.timing_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.event_start_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.event_start_entry = tk.Entry(self.timing_bar, width=9)
        style_entry(self.event_start_entry, colors)
        self.event_start_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.event_start_entry.bind("<Return>", self._on_event_timing_shortcut)
        self.event_start_entry.bind("<Escape>", self._on_reset_event_timing)

        self.event_duration_lbl = tk.Label(
            self.timing_bar, text="", bg=colors.bg_surface, fg=colors.text_primary
        )
        self.event_duration_lbl.pack(side=tk.LEFT, padx=(0, sp.xs))
        self.event_duration_entry = tk.Entry(self.timing_bar, width=9)
        style_entry(self.event_duration_entry, colors)
        self.event_duration_entry.pack(side=tk.LEFT, padx=(0, sp.sm))
        self.event_duration_entry.bind("<Return>", self._on_event_timing_shortcut)
        self.event_duration_entry.bind("<Escape>", self._on_reset_event_timing)

        self.event_timing_btn = create_button(
            self.timing_bar,
            text="",
            command=self._on_apply_event_timing,
            bg=colors.bg_active,
            fg=colors.text_primary,
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.bg_surface_hover,
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
            hover_bg=colors.harmonic_subdominant,
            relief=tk.FLAT,
            padx=sp.sm
        )
        self.export_btn.pack(side=tk.RIGHT, padx=sp.xs)

        # Chord Listbox / Progression Display
        self.prog_frame = self.theme.make_surface_card(
            self.work_area,
            radius=self.theme.corner_radius,
            padding=sp.xs,
        )
        self.prog_frame.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=(0, sp.sm))

        self.chord_listbox = tk.Listbox(
            self.prog_frame.inner,
            font=("Helvetica", 13),
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic,
            selectforeground=colors.text_inverted,
            relief=tk.FLAT,
            bd=0,
            activestyle="dotbox",
            exportselection=False,
            highlightthickness=2,
            highlightbackground=colors.bg_surface,
            highlightcolor=colors.border_focus,
        )
        self.progression_scrollbar = ThemedAutoScrollbar(
            self.prog_frame.inner,
            bg_color=colors.bg_surface,
            track_color=colors.bg_surface_hover,
            thumb_color=colors.border,
            active_thumb_color=colors.harmonic_tonic,
            width=12,
            radius=6,
            orient="vertical",
        )
        self.progression_scrollbar.set_command(self.chord_listbox.yview)
        self.chord_listbox.configure(yscrollcommand=self.progression_scrollbar.set)
        self.progression_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chord_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=sp.xs, pady=sp.xs)
        self.chord_listbox.bind("<<ListboxSelect>>", self._on_chord_selected)
        modifier = "Option" if sys.platform == "darwin" else "Alt"
        self.chord_listbox.bind(f"<{modifier}-Up>", lambda _event: self._move_chord_shortcut(-1))
        self.chord_listbox.bind(f"<{modifier}-Down>", lambda _event: self._move_chord_shortcut(1))
        edit_modifier = "Command" if sys.platform == "darwin" else "Control"
        for action, key in _CHORD_EVENT_SHORTCUTS:
            self.chord_listbox.bind(
                f"<{edit_modifier}-{key}>",
                lambda _event, selected=action: self._chord_event_edit_shortcut(selected),
            )

        # ----------------------------------------------------
        # Area 2: Informations- und Theoriebereich
        # ----------------------------------------------------
        self.info_area = tk.Frame(self.paned, bg=colors.bg_window, bd=0)
        self.paned.add(self.info_area, minsize=260)

        self.info_header_card = self.theme.make_surface_card(
            self.info_area,
            radius=self.theme.corner_radius,
            padding=sp.xs,
            auto_height=True,
        )
        self.info_header_card.pack(fill=tk.X, padx=sp.sm, pady=(0, sp.xs))

        self.info_bar = tk.Frame(self.info_header_card.inner, bg=colors.bg_surface, pady=sp.xs, padx=sp.sm)
        self.info_bar.pack(fill=tk.X)

        self.info_lbl = tk.Label(
            self.info_bar,
            text=self.i18n.translate("information.heading"),
            font=self.theme.font_spec(self.theme.typography.size_md, "bold"),
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
            hover_bg=colors.bg_surface_hover,
            relief=tk.FLAT,
            padx=sp.sm,
        )

        # Detail Content Frame
        self.detail_frame = self.theme.make_surface_card(
            self.info_area,
            radius=self.theme.corner_radius,
            padding=sp.xs,
        )
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=sp.sm, pady=(0, sp.sm))

        self.detail_text = tk.Text(
            self.detail_frame.inner,
            font=("Courier", 11),
            bg=colors.bg_surface,
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
            self.info_bar, self.detail_frame.inner,
            controller=self.controller, i18n=self.i18n, theme=self.theme,
            selected_chord=self._selected_chord_index,
            show_detail=self._write_detail, on_applied=self._on_recommendation_applied,
        )
        self.voice_lab_btn.pack(side=tk.RIGHT, padx=sp.xs)
        self.detail_scrollbar = ThemedAutoScrollbar(
            self.detail_frame.inner,
            bg_color=colors.bg_surface,
            track_color=colors.bg_surface_hover,
            thumb_color=colors.border,
            active_thumb_color=colors.harmonic_tonic,
            width=12,
            radius=6,
            orient="vertical",
        )
        self.detail_scrollbar.set_command(self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=self.detail_scrollbar.set)
        self.detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def set_theme_preference(self, preference: str) -> str:
        """Switch UI appearance between themes or OS system mode via glide_shell."""
        normalized = self.theme.normalize_theme_name(preference)
        allowed = {"system", *self.theme.THEMES}
        self._theme_preference = normalized if normalized in allowed else "dark"
        if hasattr(self, "theme_var"):
            self.theme_var.set(self._theme_preference)
        resolved = (
            self.theme.resolve_system_mode(self.root, fallback=self.theme.mode, preference=self._theme_preference)
            if self._theme_preference == "system"
            else self._theme_preference
        )
        self.apply_theme(resolved)
        self._persist_settings()
        return resolved

    def apply_theme(self, mode: Optional[str] = None) -> None:
        """Apply a Glide palette live across main-window surfaces, entries and buttons."""
        if mode is not None:
            self.theme.set_mode(mode)
        colors = self.theme.colors
        self.root.configure(bg=colors.bg_window)
        self.shell_frame.configure(bg=colors.bg_window)
        self.paned.configure(bg=colors.bg_window)
        for area in (self.work_area, self.info_area):
            area.configure(bg=colors.bg_window)
        for surface_bar in (
            self.control_bar,
            self.header_title_box,
            self.edit_bar,
            self.context_bar,
            self.playback_bar,
            self.timing_bar,
            self.info_bar,
        ):
            surface_bar.configure(bg=colors.bg_surface)
        for frame in (
            self.sidebar_frame,
            self.sidebar_rail_frame,
            self.toolbar_card,
            self.prog_frame,
            self.info_header_card,
            self.detail_frame,
        ):
            if hasattr(frame, "set_theme") and callable(getattr(frame, "set_theme")):
                frame.set_theme(
                    bg_color=colors.bg_window,
                    fill_color=colors.bg_surface,
                    outline_color=colors.border,
                    radius=self.theme.corner_radius,
                )
            else:
                style_surface_card(frame, colors)
        for scrollbar in (
            getattr(self, "progression_scrollbar", None),
            getattr(self, "detail_scrollbar", None),
        ):
            if scrollbar is not None and hasattr(scrollbar, "set_theme") and callable(getattr(scrollbar, "set_theme")):
                scrollbar.set_theme(
                    bg_color=colors.bg_surface,
                    track_color=colors.bg_surface_hover,
                    thumb_color=colors.border,
                    active_thumb_color=colors.harmonic_tonic,
                )
        if hasattr(self, "header_logo_lbl"):
            self.header_logo_lbl.configure(bg=colors.bg_surface)

        # Dynamic typography derived from tokens & font scale
        title_font = self.theme.font_spec(self.theme.typography.size_md, "bold")
        subtitle_font = self.theme.font_spec(self.theme.typography.size_xs)
        heading_font = self.theme.font_spec(self.theme.typography.size_xs, "bold")
        form_label_font = self.theme.font_spec(self.theme.typography.size_xs, "bold")
        body_font = self.theme.font_spec(self.theme.typography.size_sm)
        button_font = self.theme.font_spec(self.theme.typography.size_xs)
        mono_font = self.theme.font_spec(self.theme.typography.size_sm, mono=True)

        self.title_lbl.configure(font=title_font, fg=colors.harmonic_tonic, bg=colors.bg_surface)
        self.subtitle_lbl.configure(font=subtitle_font, fg=colors.text_secondary, bg=colors.bg_surface)
        self.info_lbl.configure(font=title_font, fg=colors.harmonic_dominant, bg=colors.bg_surface)
        self.sidebar_heading_lbl.configure(font=heading_font, fg=colors.text_secondary, bg=colors.bg_surface)
        for lbl in (
            self.project_title_lbl,
            self.key_lbl,
            self.mode_lbl,
            self.notation_lbl,
            self.tempo_lbl,
            self.meter_lbl,
            self.voice_style_lbl,
            self.event_start_lbl,
            self.event_duration_lbl,
        ):
            lbl.configure(font=form_label_font, bg=colors.bg_surface, fg=colors.text_primary)
        for radio in (
            self.major_btn,
            self.minor_btn,
            self.notation_int_btn,
            self.notation_de_btn,
        ):
            radio.configure(
                font=body_font,
                bg=colors.bg_surface,
                fg=colors.text_primary,
                selectcolor=colors.bg_window,
                activebackground=colors.bg_surface,
            )
        for entry in (
            self.chord_entry,
            self.project_title_entry,
            self.key_entry,
            self.tempo_entry,
            self.meter_entry,
            self.event_start_entry,
            self.event_duration_entry,
        ):
            style_entry(entry, colors)
            try:
                entry.configure(font=body_font)
            except Exception:
                pass
        self.voice_style_menu.configure(
            font=body_font,
            bg=colors.bg_active,
            fg=colors.text_primary,
            activebackground=colors.bg_surface_hover,
        )
        self.voice_style_menu["menu"].configure(font=body_font, bg=colors.bg_surface, fg=colors.text_primary)
        self.chord_listbox.configure(
            font=mono_font,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic,
            selectforeground=colors.text_inverted,
            highlightbackground=colors.bg_surface,
            highlightcolor=colors.border_focus,
        )
        self.detail_text.configure(
            font=mono_font,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            highlightbackground=colors.bg_surface,
            highlightcolor=colors.border_focus,
        )
        self.next_chord_panel.apply_theme(self.theme)
        for item_id in self._sidebar_buttons:
            is_ws = item_id == "workspace"
            for btn in (self._sidebar_buttons[item_id], self._rail_button_map[item_id]):
                retheme_button(
                    btn,
                    colors,
                    base_bg=colors.bg_surface,
                    base_fg=colors.text_primary,
                    active_bg=colors.bg_active,
                    active_fg=colors.harmonic_tonic,
                    radius=self.theme.corner_radius,
                    font=button_font,
                )
                set_button_active(btn, is_ws, colors)
        retheme_button(
            self.sidebar_toggle_btn,
            colors,
            base_bg=colors.bg_active,
            base_fg=colors.text_primary,
            active_bg=colors.harmonic_tonic,
            active_fg=colors.text_inverted,
            radius=self.theme.corner_radius,
            font=button_font,
        )
        set_button_active(
            self.sidebar_toggle_btn,
            self.effective_sidebar_mode() == "hidden",
            colors,
        )
        for btn in (
            self.sidebar_collapse_btn,
            self.sidebar_expand_btn,
            self.update_btn,
            self.remove_btn,
            self.move_up_btn,
            self.move_down_btn,
            self.undo_btn,
            self.redo_btn,
            self.context_btn,
            self.event_timing_btn,
            self.trans_down_btn,
            self.trans_up_btn,
            self.voice_lab_btn,
        ):
            retheme_button(
                btn,
                colors,
                base_bg=colors.bg_active,
                base_fg=colors.text_primary,
                radius=self.theme.corner_radius,
                font=button_font,
            )
        retheme_button(
            self.add_btn,
            colors,
            base_bg=colors.harmonic_tonic,
            base_fg=colors.text_inverted,
            hover_bg=colors.harmonic_tonic,
            radius=self.theme.corner_radius,
            font=button_font,
        )
        retheme_button(
            self.export_btn,
            colors,
            base_bg=colors.harmonic_subdominant,
            base_fg=colors.text_inverted,
            hover_bg=colors.harmonic_subdominant,
            radius=self.theme.corner_radius,
            font=button_font,
        )

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
        self._update_header_subtitle()
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
            self._update_chord_controls(index, len(state["chords"]))
            self._display_chord_details(state["chords"][index], index=index)
        else:
            self._load_event_timing_controls(None)
            self._update_chord_controls(None, 0)
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

    def _on_reset_event_timing(self, _event: tk.Event) -> str:
        self._load_event_timing_controls(self._selected_chord_index())
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

    def _show_event_timing_error(self, entry: tk.Entry, message: str) -> None:
        messagebox.showerror(
            self.i18n.translate("event.timing.error.title"), message, parent=self.root,
        )
        entry.focus_set()
        entry.selection_range(0, tk.END)

    def _on_apply_event_timing(self) -> None:
        index = self._selected_chord_index()
        if index is None:
            return

        session = self.controller.session
        t = self.i18n.translate
        try:
            start_tick = self._parse_event_start(self.event_start_entry.get())
        except ValueError:
            beats, denominator = session.time_signature
            last_tick = RationalMidiTime.ticks_per_beat(session.state.ppq, denominator) - 1
            self._show_event_timing_error(
                self.event_start_entry, t("event.start.invalid", beats=beats, last_tick=last_tick),
            )
            return

        try:
            duration_ticks = int(self.event_duration_entry.get())
            if duration_ticks <= 0:
                raise ValueError("Duration must be positive.")
        except ValueError:
            self._show_event_timing_error(self.event_duration_entry, t("event.duration.invalid"))
            return

        if session.get_chord_event_timing(index) == (start_tick, duration_ticks):
            self._load_event_timing_controls(index)
            return
        self.controller.set_chord_event_timing(index, start_tick, duration_ticks)
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

    def _update_chord_controls(self, index: Optional[int], chord_count: int) -> None:
        self.move_up_btn.configure(
            state=tk.NORMAL if index is not None and index > 0 else tk.DISABLED
        )
        self.move_down_btn.configure(
            state=tk.NORMAL if index is not None and index < chord_count - 1 else tk.DISABLED
        )
        self.chord_menu.entryconfigure(0, state=tk.NORMAL if index is not None else tk.DISABLED)
        can_split = (
            index is not None and self.controller.session.get_chord_event_timing(index)[1] >= 2
        )
        self.chord_menu.entryconfigure(1, state=tk.NORMAL if can_split else tk.DISABLED)

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

    def _display_chord_details(self, chord_name: str, *, index: int | None = None) -> None:
        """Update the inspector, keeping optional keyboard details independent."""
        translate = self.i18n.translate
        try:
            degree = self.controller.harmonic_degree_at(index) if index is not None else None
            details = format_chord_analysis(
                chord_name, self.controller.session.convention, translate, degree=degree,
            )
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

    def _chord_event_edit_shortcut(self, action: Literal["duplicate", "split"]) -> str:
        self._on_chord_event_edit(action)
        return "break"

    def _on_chord_event_edit(self, action: Literal["duplicate", "split"]) -> None:
        index = self._selected_chord_index()
        if index is None:
            return
        if action == "split":
            if self.controller.session.get_chord_event_timing(index)[1] < 2:
                return
            new_index = self.controller.split_chord_event(index)
        else:
            new_index = self.controller.duplicate_chord_event(index)
        self._refresh_all(selected_index=new_index)
        self.chord_listbox.focus_set()

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
        try:
            self.controller.transpose(semitones)
        except MusicTheoryError:
            messagebox.showerror(
                self.i18n.translate("transpose.error.title"),
                self.i18n.translate("transpose.error.message"),
                parent=self.root,
            )
            return
        self._load_context_controls()
        self._refresh_all()

    def _on_chord_selected(self, event) -> None:
        sel = self.chord_listbox.curselection()
        if sel:
            state = self.controller.get_state_summary()
            idx = sel[0]
            if idx < len(state["chords"]):
                self._update_chord_controls(idx, len(state["chords"]))
                self._load_event_timing_controls(idx)
                self.next_chord_panel.clear()
                self._display_chord_details(state["chords"][idx], index=idx)

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
            on_export=partial(self._export_midi_with_options, expected_revision=self.controller.revision),
            voicing_failures=self.controller.midi_voicing_failures(),
            preview=self.controller.midi_export_preview,
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

    def _check_midi_export_revision(self, revision: int) -> bool:
        if revision == self.controller.revision:
            return True
        t = self.i18n.translate
        messagebox.showerror(t("midi.export.error.title"), t("midi.export.error.stale"),
                             parent=self._dialog_parent())
        return False

    def _export_midi_with_options(
        self, options: MidiExportOptions, *, expected_revision: int | None = None,
    ) -> bool:
        revision = self.controller.revision if expected_revision is None else expected_revision
        if not self._check_midi_export_revision(revision):
            return False
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
        if not selected or not self._check_midi_export_revision(revision):
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
