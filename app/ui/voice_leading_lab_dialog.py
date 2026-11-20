"""Compare existing voice-leading styles without changing the active project."""

from __future__ import annotations

import tkinter as tk
from typing import Callable

from app.i18n import LocaleManager
from app.ui.session_controller import (
    ProgressionSessionController,
    VoiceLeadingStyleProfile,
)
from app.ui.theme import ThemeManager
from src.steps.progression.voice_leading import VoiceLeadingStyle
from src.steps.theory.exceptions import MusicTheoryError


VOICE_LEADING_STYLE_OPTIONS = (
    (VoiceLeadingStyle.CONTEMPORARY_POP, "voice.style.pop"),
    (VoiceLeadingStyle.STRICT_CLASSICAL, "voice.style.classical"),
    (VoiceLeadingStyle.POWER_CHORDS, "voice.style.power"),
    (VoiceLeadingStyle.QUARTAL_JAZZ, "voice.style.quartal"),
)


def format_voice_leading_profile(
    profile: VoiceLeadingStyleProfile,
    chords: tuple[str, ...],
    active_style: VoiceLeadingStyle,
    translate: Callable[..., str],
) -> str:
    labels = {
        style.value: translate(label_key)
        for style, label_key in VOICE_LEADING_STYLE_OPTIONS
    }
    lines = [
        translate(
            "voice.lab.style",
            style=labels.get(profile.style.value, profile.style.value),
        ),
        translate(
            "voice.lab.current",
            style=labels.get(active_style.value, active_style.value),
        ),
        translate("voice.lab.disclaimer"),
        translate("voice.lab.total", movement=profile.total_movement),
        "",
    ]
    for index, transition in enumerate(profile.transitions[:-1]):
        distance = transition.semitone_distance_to_next
        if distance is None:
            continue
        lines.append(
            translate(
                "voice.lab.transition",
                from_chord=chords[index],
                to_chord=chords[index + 1],
                distance=distance,
                warnings=len(transition.voice_leading_warnings),
            )
        )
    return "\n".join(lines)


class VoiceLeadingLabDialog:
    """Modal style comparison panel with explicit, undoable style application."""

    def __init__(
        self,
        parent: tk.Misc,
        controller: ProgressionSessionController,
        i18n: LocaleManager,
        theme: ThemeManager,
        on_apply: Callable[[str], bool],
    ) -> None:
        self._controller = controller
        self._i18n = i18n
        self._on_apply = on_apply
        self._selected_style: VoiceLeadingStyle | None = None
        colors = theme.colors
        spacing = theme.spacing
        typography = theme.typography
        translate = i18n.translate

        self.window = tk.Toplevel(parent)
        self.window.title(translate("voice.lab.title"))
        self.window.geometry("860x560")
        self.window.minsize(720, 460)
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
            text=translate("voice.lab.heading"),
            bg=colors.bg_window,
            fg=colors.text_primary,
            font=(typography.font_family_sans, typography.size_lg, "bold"),
        ).pack(anchor=tk.W, pady=(0, spacing.sm))

        body = tk.PanedWindow(
            container,
            orient=tk.HORIZONTAL,
            bg=colors.border,
            bd=1,
            sashrelief=tk.FLAT,
            sashwidth=4,
        )
        body.pack(fill=tk.BOTH, expand=True)

        style_frame = tk.Frame(body, bg=colors.bg_surface)
        self._style_list = tk.Listbox(
            style_frame,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic,
            selectforeground=colors.text_inverted,
            activestyle="dotbox",
            exportselection=False,
            font=(typography.font_family_sans, typography.size_sm),
            relief=tk.FLAT,
        )
        self._style_list.pack(fill=tk.BOTH, expand=True)
        for _style, label_key in VOICE_LEADING_STYLE_OPTIONS:
            self._style_list.insert(tk.END, translate(label_key))
        self._style_list.bind("<<ListboxSelect>>", self._select_current)
        body.add(style_frame, minsize=210)

        preview_frame = tk.Frame(body, bg=colors.bg_window)
        self._preview = tk.Text(
            preview_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=colors.bg_window,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
            font=(typography.font_family_sans, typography.size_sm),
            relief=tk.FLAT,
            padx=spacing.sm,
            pady=spacing.sm,
        )
        preview_scrollbar = tk.Scrollbar(
            preview_frame,
            orient=tk.VERTICAL,
            command=self._preview.yview,
        )
        self._preview.configure(yscrollcommand=preview_scrollbar.set)
        self._preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        body.add(preview_frame, minsize=420)

        buttons = tk.Frame(container, bg=colors.bg_window)
        buttons.pack(fill=tk.X, pady=(spacing.sm, 0))
        tk.Button(
            buttons,
            text=translate("voice.lab.close"),
            command=self._close,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=spacing.md,
        ).pack(side=tk.RIGHT)
        self._apply_button = tk.Button(
            buttons,
            text=translate("voice.lab.apply"),
            command=self._apply_selected,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=spacing.md,
            state=tk.DISABLED,
        )
        self._apply_button.pack(side=tk.RIGHT, padx=(0, spacing.sm))

        self.window.grab_set()
        self._set_preview(translate("voice.lab.select_prompt"))
        self._style_list.focus_set()

    def _select_current(self, _event: object | None = None) -> None:
        selection = self._style_list.curselection()
        if not selection or not 0 <= selection[0] < len(VOICE_LEADING_STYLE_OPTIONS):
            self._selected_style = None
            self._apply_button.configure(state=tk.DISABLED)
            self._set_preview(self._i18n.translate("voice.lab.select_prompt"))
            return

        self._selected_style = VOICE_LEADING_STYLE_OPTIONS[selection[0]][0]
        try:
            profile = self._controller.analyze_voice_leading_style(
                self._selected_style
            )
        except (MusicTheoryError, ValueError) as exc:
            self._apply_button.configure(state=tk.DISABLED)
            self._set_preview(
                self._i18n.translate("voice.lab.error", error=exc)
            )
            return

        self._apply_button.configure(state=tk.NORMAL)
        self._set_preview(
            format_voice_leading_profile(
                profile,
                tuple(self._controller.session.chords),
                self._controller.session.voice_leading_style,
                self._i18n.translate,
            )
        )

    def _set_preview(self, text: str) -> None:
        self._preview.configure(state=tk.NORMAL)
        self._preview.delete("1.0", tk.END)
        self._preview.insert("1.0", text)
        self._preview.configure(state=tk.DISABLED)

    def _apply_selected(self) -> None:
        if self._selected_style is not None and self._on_apply(
            self._selected_style.value
        ):
            self._close()

    def _close(self) -> None:
        self.window.destroy()
