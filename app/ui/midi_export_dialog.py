"""Localized ADR-017 MIDI export options dialog."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from typing import Callable, Collection, Literal, Mapping

from app.i18n import LocaleManager
from app.ui.dialog_support import ModalDialog
from app.ui.file_feedback import file_error_reason
from app.ui.theme import ThemeManager, apply_window_geometry, create_button
from src.steps.midi.export_service import ADR017_VOICINGS, Adr017ExportPreview, Adr017NoteDuration, Adr017Voicing
from src.steps.theory.exceptions import MusicTheoryError


@dataclass(frozen=True)
class MidiExportOptions:
    voicing_type: Adr017Voicing = "CLOSE"
    note_duration_mode: Adr017NoteDuration = "FIXED_GAP"
    smf_format: Literal[0, 1] = 1

    def __post_init__(self) -> None:
        if self.voicing_type not in ADR017_VOICINGS:
            raise ValueError(f"Unsupported ADR-017 voicing type: {self.voicing_type!r}.")
        if self.note_duration_mode not in {"FIXED_GAP", "PERCENT_95"}:
            raise ValueError(
                f"Unsupported ADR-017 note duration mode: {self.note_duration_mode!r}."
            )
        if type(self.smf_format) is not int or self.smf_format not in (0, 1):
            raise ValueError(f"Unsupported SMF format: {self.smf_format!r}.")


def format_midi_file_error(error: OSError, path: str, i18n: LocaleManager) -> str:
    """Describe an export file error with a localized recovery action."""
    return i18n.translate(f"midi.export.error.{file_error_reason(error)}", path=path)


class MidiExportOptionsDialog(ModalDialog):
    """Collect supported per-export options and close only after successful export."""

    def __init__(
        self,
        parent: tk.Misc,
        i18n: LocaleManager,
        theme: ThemeManager,
        on_export: Callable[[MidiExportOptions], bool],
        voicing_failures: Mapping[Adr017Voicing, str],
        preview: Callable[[Adr017Voicing, Adr017NoteDuration], Adr017ExportPreview],
    ) -> None:
        self._i18n = i18n
        self._theme = theme
        self._on_export = on_export
        self._preview = preview
        colors = theme.colors
        spacing = theme.spacing
        typography = theme.typography
        translate = i18n.translate
        self._colors = colors
        self._spacing = spacing
        self._font = (typography.font_family_sans, typography.size_sm)

        super().__init__(parent)
        self.window.title(translate("midi.options.title"))
        apply_window_geometry(
            self.window,
            620,
            650 if voicing_failures else 600,
            540,
            605 if voicing_failures else 550,
        )
        self.window.configure(bg=colors.bg_window)

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
            wraplength=496,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, spacing.sm))

        initial_voicing = next((mode for mode in ADR017_VOICINGS if mode not in voicing_failures), "")
        self._voicing_var = tk.StringVar(self.window, value=initial_voicing)
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
            disabled_values=voicing_failures.keys(),
            command=self._update_preview,
        )
        if voicing_failures:
            tk.Label(
                container,
                text="\n".join(
                    translate("midi.options.voicing.unavailable", mode=mode, chord=voicing_failures[mode])
                    for mode in ADR017_VOICINGS if mode in voicing_failures
                ),
                bg=colors.bg_window,
                fg=colors.text_secondary,
                justify=tk.LEFT,
                wraplength=496,
                font=self._font,
            ).pack(anchor=tk.W, pady=(0, spacing.sm))
        self._add_group(
            container,
            "midi.options.duration",
            self._duration_var,
            (
                ("FIXED_GAP", "midi.options.duration.fixed_gap"),
                ("PERCENT_95", "midi.options.duration.percent_95"),
            ),
            command=self._update_preview,
        )
        self._add_group(
            container,
            "midi.options.format",
            self._format_var,
            (
                ("1", "midi.options.format.type1"),
                ("0", "midi.options.format.type0"),
            ),
            command=self._update_preview,
        )

        self._preview_label = tk.Label(
            container, bg=colors.bg_window, fg=colors.text_primary, font=self._font,
            justify=tk.LEFT, wraplength=496,
        )
        self._overlap_label = tk.Label(
            container,
            bg=colors.bg_window,
            fg=colors.text_primary,
            font=self._font,
            justify=tk.LEFT,
            wraplength=496,
        )
        if initial_voicing:
            self._preview_label.pack(anchor=tk.W, pady=(spacing.xs, 0))
            self._overlap_label.pack(anchor=tk.W, pady=(spacing.xs, 0))
            self._update_preview()

        buttons = tk.Frame(container, bg=colors.bg_window)
        buttons.pack(fill=tk.X, pady=(spacing.sm, 0))
        cancel_button = create_button(
            buttons,
            text=translate("midi.options.cancel"),
            command=self._close,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=spacing.md,
        )
        cancel_button.pack(side=tk.RIGHT)
        self._export_button = create_button(
            buttons,
            text=translate("midi.options.export"),
            command=self._export,
            state=tk.NORMAL if initial_voicing else tk.DISABLED,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=spacing.md,
        )
        self._export_button.pack(side=tk.RIGHT, padx=(0, spacing.sm))

        self._show(self._export_button if initial_voicing else cancel_button)

    def _add_group(
        self,
        parent: tk.Misc,
        title_key: str,
        variable: tk.StringVar,
        options: tuple[tuple[str, str], ...],
        *,
        disabled_values: Collection[str] = (),
        command: Callable[[], None] | None = None,
    ) -> None:
        colors = self._colors
        spacing = self._spacing
        translate = self._i18n.translate
        group = self._theme.make_surface_card(
            parent,
            radius=self._theme.corner_radius,
            padding=spacing.xs,
            auto_height=True,
        )
        group.pack(fill=tk.X, pady=(0, spacing.xs))
        tk.Label(
            group.inner,
            text=translate(title_key),
            bg=colors.bg_surface,
            fg=colors.text_secondary,
            font=self._theme.font_spec(self._theme.typography.size_xs, "bold"),
            anchor=tk.W,
        ).pack(fill=tk.X, anchor=tk.W, pady=(0, spacing.xs))
        for value, label_key in options:
            tk.Radiobutton(
                group.inner,
                text=translate(label_key),
                variable=variable,
                value=value,
                command=command,
                state=tk.DISABLED if value in disabled_values else tk.NORMAL,
                anchor=tk.W,
                bg=colors.bg_surface,
                fg=colors.text_primary,
                activebackground=colors.bg_surface,
                activeforeground=colors.text_primary,
                selectcolor=colors.bg_active,
                font=self._font,
                relief=tk.FLAT,
            ).pack(fill=tk.X, anchor=tk.W)

    def _update_preview(self) -> None:
        voicing = self._voicing_var.get()
        if not voicing:
            return

        translate = self._i18n.translate
        try:
            preview = self._preview(voicing, self._duration_var.get())
        except (MusicTheoryError, ValueError):
            overview = ""
            message = translate("midi.options.overlap.unavailable")
        else:
            tracks = 1 if self._format_var.get() == "0" else 3
            if preview.chord_range and preview.bass_range:
                overview = translate(
                    "midi.options.preview.events", tracks=tracks, first=preview.first_tick, end=preview.end_tick,
                    chords=preview.chord_notes, bass=preview.bass_notes,
                    chord_low=preview.chord_range[0], chord_high=preview.chord_range[1],
                    bass_low=preview.bass_range[0], bass_high=preview.bass_range[1],
                )
            else:
                overview = translate("midi.options.preview.empty", tracks=tracks)
            message = (
                translate("midi.options.overlap.detected", count=preview.overlaps, tick=preview.first_overlap_tick)
                if preview.overlaps
                else translate("midi.options.overlap.none")
            )
        self._preview_label.configure(text=overview)
        self._overlap_label.configure(text=message)

    def _export(self) -> None:
        options = MidiExportOptions(
            voicing_type=self._voicing_var.get(),
            note_duration_mode=self._duration_var.get(),
            smf_format=int(self._format_var.get()),
        )
        if self._on_export(options):
            self._close()
