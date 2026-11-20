"""Localized ADR-017 MIDI export options dialog."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from typing import Callable, Literal

from app.i18n import LocaleManager
from app.ui.theme import ThemeManager


@dataclass(frozen=True)
class MidiExportOptions:
    voicing_type: Literal["CLOSE", "DROP2", "ROOTLESS"] = "CLOSE"
    note_duration_mode: Literal["FIXED_GAP", "PERCENT_95"] = "FIXED_GAP"
    smf_format: Literal[0, 1] = 1

    def __post_init__(self) -> None:
        if self.voicing_type not in {"CLOSE", "DROP2", "ROOTLESS"}:
            raise ValueError(f"Unsupported ADR-017 voicing type: {self.voicing_type!r}.")
        if self.note_duration_mode not in {"FIXED_GAP", "PERCENT_95"}:
            raise ValueError(
                f"Unsupported ADR-017 note duration mode: {self.note_duration_mode!r}."
            )
        if type(self.smf_format) is not int or self.smf_format not in (0, 1):
            raise ValueError(f"Unsupported SMF format: {self.smf_format!r}.")


class MidiExportOptionsDialog:
    """Collect supported per-export options and close only after successful export."""

    def __init__(
        self,
        parent: tk.Misc,
        i18n: LocaleManager,
        theme: ThemeManager,
        on_export: Callable[[MidiExportOptions], bool],
    ) -> None:
        self._i18n = i18n
        self._on_export = on_export
        colors = theme.colors
        spacing = theme.spacing
        typography = theme.typography
        translate = i18n.translate
        self._colors = colors
        self._spacing = spacing
        self._font = (typography.font_family_sans, typography.size_sm)

        self.window = tk.Toplevel(parent)
        self.window.title(translate("midi.options.title"))
        self.window.geometry("620x520")
        self.window.minsize(540, 460)
        self.window.transient(parent)
        self.window.configure(bg=colors.bg_window)
        self.window.protocol("WM_DELETE_WINDOW", self._close)

        container = tk.Frame(
            self.window,
            bg=colors.bg_window,
            padx=spacing.md,
            pady=spacing.md,
        )
        container.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            container,
            text=translate("midi.options.heading"),
            bg=colors.bg_window,
            fg=colors.text_primary,
            font=(typography.font_family_sans, typography.size_lg, "bold"),
        ).pack(anchor=tk.W, pady=(0, spacing.xs))
        tk.Label(
            container,
            text=translate("midi.options.disclaimer"),
            bg=colors.bg_window,
            fg=colors.text_secondary,
            font=(typography.font_family_sans, typography.size_sm),
            wraplength=560,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, spacing.sm))

        self._voicing_var = tk.StringVar(self.window, value="CLOSE")
        self._duration_var = tk.StringVar(self.window, value="FIXED_GAP")
        self._format_var = tk.StringVar(self.window, value="1")
        self._add_group(
            container,
            "midi.options.voicing",
            self._voicing_var,
            (
                ("CLOSE", "midi.options.voicing.close"),
                ("DROP2", "midi.options.voicing.drop2"),
                ("ROOTLESS", "midi.options.voicing.rootless"),
            ),
        )
        self._add_group(
            container,
            "midi.options.duration",
            self._duration_var,
            (
                ("FIXED_GAP", "midi.options.duration.fixed_gap"),
                ("PERCENT_95", "midi.options.duration.percent_95"),
            ),
        )
        self._add_group(
            container,
            "midi.options.format",
            self._format_var,
            (
                ("1", "midi.options.format.type1"),
                ("0", "midi.options.format.type0"),
            ),
        )

        buttons = tk.Frame(container, bg=colors.bg_window)
        buttons.pack(fill=tk.X, pady=(spacing.sm, 0))
        tk.Button(
            buttons,
            text=translate("midi.options.cancel"),
            command=self._close,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=spacing.md,
        ).pack(side=tk.RIGHT)
        tk.Button(
            buttons,
            text=translate("midi.options.export"),
            command=self._export,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=spacing.md,
        ).pack(side=tk.RIGHT, padx=(0, spacing.sm))

        self.window.grab_set()

    def _add_group(
        self,
        parent: tk.Misc,
        title_key: str,
        variable: tk.StringVar,
        options: tuple[tuple[str, str], ...],
    ) -> None:
        colors = self._colors
        spacing = self._spacing
        translate = self._i18n.translate
        group = tk.LabelFrame(
            parent,
            text=translate(title_key),
            bg=colors.bg_window,
            fg=colors.text_secondary,
            font=self._font,
            padx=spacing.sm,
            pady=spacing.xs,
        )
        group.pack(fill=tk.X, pady=(0, spacing.xs))
        for value, label_key in options:
            tk.Radiobutton(
                group,
                text=translate(label_key),
                variable=variable,
                value=value,
                anchor=tk.W,
                bg=colors.bg_window,
                fg=colors.text_primary,
                activebackground=colors.bg_window,
                activeforeground=colors.text_primary,
                selectcolor=colors.bg_active,
                font=self._font,
                relief=tk.FLAT,
            ).pack(fill=tk.X, anchor=tk.W)

    def _export(self) -> None:
        options = MidiExportOptions(
            voicing_type=self._voicing_var.get(),
            note_duration_mode=self._duration_var.get(),
            smf_format=int(self._format_var.get()),
        )
        if self._on_export(options):
            self._close()

    def _close(self) -> None:
        self.window.destroy()
