"""Compare existing voice-leading styles without changing the active project."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
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
        for item in transition.voice_leading_diagnostics:
            lines.append("  • " + translate(
                f"voice.lab.warning.{item.motion}.{item.interval}",
                lower=item.lower_voice + 1,
                upper=item.upper_voice + 1,
            ))
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
        self._colors = theme.colors
        self._font = (theme.typography.font_family_sans, theme.typography.size_sm)
        self._profiles: list[VoiceLeadingStyleProfile | None] = [None, None]
        self._timings: tuple[tuple[int, int], ...] = ()
        self._revision = controller.revision
        colors = self._colors
        spacing = theme.spacing
        translate = i18n.translate

        self.window = tk.Toplevel(parent)
        self.window.title(translate("voice.lab.title"))
        self.window.geometry("940x630")
        self.window.minsize(720, 490)
        self.window.transient(parent)
        self.window.configure(bg=colors.bg_window)
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.bind("<Escape>", lambda _event: self._close())

        container = tk.Frame(
            self.window, bg=colors.bg_window, padx=spacing.md, pady=spacing.md
        )
        container.pack(fill=tk.BOTH, expand=True)
        for key in ("voice.lab.heading", "voice.lab.roll"):
            tk.Label(
                container, text=translate(key), bg=colors.bg_window,
                fg=colors.text_primary, font=self._font,
            ).pack(anchor=tk.W, pady=(0, spacing.xs))

        body = tk.Frame(container, bg=colors.bg_window)
        body.pack(fill=tk.BOTH, expand=True)
        self._selectors = []
        self._canvases = []
        self._previews = []
        self._apply_buttons = []
        labels = tuple(translate(key) for _, key in VOICE_LEADING_STYLE_OPTIONS)
        active = controller.session.voice_leading_style
        alternate = (
            VoiceLeadingStyle.STRICT_CLASSICAL
            if active == VoiceLeadingStyle.CONTEMPORARY_POP
            else VoiceLeadingStyle.CONTEMPORARY_POP
        )
        style_indices = {style: index for index, (style, _) in enumerate(VOICE_LEADING_STYLE_OPTIONS)}
        body.rowconfigure(0, weight=1)
        for side, name, initial in ((0, "a", active), (1, "b", alternate)):
            body.columnconfigure(side, weight=1, uniform="styles")
            panel = tk.Frame(body, bg=colors.bg_surface, padx=spacing.sm, pady=spacing.sm)
            panel.grid(row=0, column=side, sticky="nsew", padx=spacing.xs)

            selector = ttk.Combobox(panel, values=labels, state="readonly", font=self._font)
            tk.Label(
                panel, text=translate(f"voice.lab.{name}"), bg=colors.bg_surface,
                fg=colors.text_primary, font=self._font,
            ).pack(anchor=tk.W)
            selector.pack(fill=tk.X, pady=(0, spacing.sm))
            selector.current(style_indices[initial])
            selector.bind("<<ComboboxSelected>>", lambda _event, index=side: self._select_style(index))
            self._selectors.append(selector)

            canvas = tk.Canvas(
                panel, width=320, height=140, bg=colors.bg_window, highlightthickness=0
            )
            canvas.pack(fill=tk.X)
            canvas.bind("<Configure>", lambda _event, index=side: self._draw_roll(index))
            self._canvases.append(canvas)

            text_frame = tk.Frame(panel, bg=colors.bg_surface)
            text_frame.pack(fill=tk.BOTH, expand=True, pady=spacing.sm)
            preview = tk.Text(
                text_frame, height=5, width=24, wrap=tk.WORD, state=tk.DISABLED,
                bg=colors.bg_window, fg=colors.text_primary, font=self._font,
                padx=spacing.sm, pady=spacing.sm,
            )
            scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=preview.yview)
            preview.configure(yscrollcommand=scrollbar.set)
            preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._previews.append(preview)
            button = ttk.Button(
                panel, text=translate(f"voice.lab.apply_{name}"),
                command=lambda index=side: self._apply_profile(index), state=tk.DISABLED,
            )
            button.pack(anchor=tk.E)
            self._apply_buttons.append(button)

        ttk.Button(container, text=translate("voice.lab.close"), command=self._close).pack(
            anchor=tk.E, pady=(spacing.sm, 0)
        )
        self._render(0)
        self._render(1)
        self.window.grab_set()
        self._selectors[0].focus_set()

    def _refresh_changed_project(self) -> bool:
        if self._revision == self._controller.revision:
            return False
        self._revision = self._controller.revision
        self._profiles = [None, None]
        self._render(0)
        self._render(1)
        return True

    def _select_style(self, side: int) -> None:
        if not self._refresh_changed_project():
            self._render(side)

    def _render(self, side: int) -> None:
        session = self._controller.session
        chords = tuple(session.chords)
        self._timings = tuple(session.get_chord_event_timing(i) for i in range(len(chords)))
        style = VOICE_LEADING_STYLE_OPTIONS[self._selectors[side].current()][0]
        translate = self._i18n.translate
        try:
            profile = self._controller.analyze_voice_leading_style(style)
        except (MusicTheoryError, ValueError) as exc:
            self._profiles[side] = None
            self._apply_buttons[side].configure(state=tk.DISABLED)
            text = translate("voice.lab.error", error=exc)
        else:
            self._profiles[side] = profile
            self._apply_buttons[side].configure(state=tk.NORMAL)
            lines = [format_voice_leading_profile(profile, chords, session.voice_leading_style, translate)]
            for chord, (start, duration), notes in zip(chords, self._timings, profile.midi_notes):
                lines.append(translate(
                    "voice.lab.notes", chord=chord, start=start, duration=duration,
                    notes=", ".join(map(str, notes)),
                ))
            text = "\n".join(lines)
        preview = self._previews[side]
        preview.configure(state=tk.NORMAL)
        preview.delete("1.0", tk.END)
        preview.insert("1.0", text)
        preview.configure(state=tk.DISABLED)
        for index in range(len(self._canvases)):
            self._draw_roll(index)

    def _draw_roll(self, side: int) -> None:
        canvas = self._canvases[side]
        canvas.delete("all")
        profile = self._profiles[side]
        if profile is None or not self._timings or canvas.winfo_width() < 64:
            return
        pitches = [
            note for item in self._profiles if item
            for voicing in item.midi_notes for note in voicing
        ]
        if not pitches:
            return
        low, high = max(0, min(pitches) - 1), min(127, max(pitches) + 1)
        end = max(start + duration for start, duration in self._timings)
        left, top = 28, 10
        right, bottom = canvas.winfo_width() - 10, canvas.winfo_height() - 20
        colors = self._colors

        def x(tick: int) -> float:
            return left + tick / end * (right - left)

        def y(note: int) -> float:
            return bottom - (note - low) / (high - low) * (bottom - top)

        for note in range(low, high + 1):
            if note in (low, high) or note % 12 == 0:
                canvas.create_line(left, y(note), right, y(note), fill=colors.border)
                canvas.create_text(left - 4, y(note), text=str(note), anchor=tk.E,
                                   fill=colors.text_secondary, font=self._font)
        for tick in sorted({0, end // 2, end}):
            anchor = tk.W if tick == 0 else tk.E if tick == end else tk.CENTER
            canvas.create_text(x(tick), bottom + 10, text=str(tick), anchor=anchor,
                               fill=colors.text_secondary, font=self._font)
        for start, _duration in self._timings:
            canvas.create_line(x(start), top, x(start), bottom, fill=colors.border)
        for (start, duration), notes in zip(self._timings, profile.midi_notes, strict=True):
            bass = min(notes, default=None)
            for note in notes:
                canvas.create_line(
                    x(start), y(note), max(x(start) + 1, x(start + duration)), y(note),
                    width=3 if note == bass else 2,
                    fill=colors.harmonic_tonic if note == bass else colors.text_primary,
                    tags=("note",),
                )

    def _apply_profile(self, side: int) -> None:
        if self._refresh_changed_project():
            return
        profile = self._profiles[side]
        if profile is not None and self._on_apply(profile.style.value):
            self._close()

    def _close(self) -> None:
        self.window.destroy()
