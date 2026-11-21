"""Compare existing voice-leading styles without changing the active project."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from app.i18n import LocaleManager
from app.ui.dialog_support import ModalDialog, configure_readonly_preview
from app.ui.piano_roll import PianoRoll, TickViewport
from app.ui.session_controller import (
    ProgressionSessionController,
    VoiceLeadingStyleProfile,
)
from app.ui.theme import ThemeManager
from src.steps.progression.voice_leading import VoiceLeadingStyle
from src.steps.theory.exceptions import MusicTheoryError


_TIME_ZOOM_LEVELS = (1, 2, 4, 8)


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
    ]
    if profile.style.is_power_chord_style:
        lines.append(translate("voice.lab.profile.power"))
    elif profile.style == VoiceLeadingStyle.QUARTAL_JAZZ:
        lines.append(translate("voice.lab.profile.quartal"))
    pitches = [note for voicing in profile.midi_notes for note in voicing]
    if pitches:
        lines.append(translate("voice.lab.register", low=min(pitches), high=max(pitches)))
    lines.extend((
        translate("voice.lab.total", movement=profile.total_movement),
        translate("voice.lab.disclaimer"),
        "",
    ))
    for index, transition in enumerate(profile.transitions[:-1]):
        distance = transition.semitone_distance_to_next
        from_chord, to_chord = chords[index:index + 2]
        if distance is None:
            lines.append(translate(
                "voice.lab.transition.unmatched", from_chord=from_chord, to_chord=to_chord,
            ))
            continue
        lines.append(
            translate(
                "voice.lab.transition",
                from_chord=from_chord,
                to_chord=to_chord,
                distance=distance,
                warnings=len(transition.voice_leading_warnings),
            )
        )
        start, end = profile.midi_notes[index:index + 2]
        movement = (after - before for before, after in zip(start, end, strict=True))
        signed_steps = ", ".join(f"{steps:+d}" if steps else "0" for steps in movement)
        lines.append("  " + translate("voice.lab.transition.voices", steps=signed_steps))
        for item in transition.voice_leading_diagnostics:
            lines.append("  • " + translate(
                f"voice.lab.warning.{item.motion}.{item.interval}",
                lower=item.lower_voice + 1,
                upper=item.upper_voice + 1,
            ))
    return "\n".join(lines)


class VoiceLeadingLabDialog(ModalDialog):
    """Modal style comparison panel with explicit, undoable style application."""

    def __init__(
        self,
        parent: tk.Misc,
        controller: ProgressionSessionController,
        i18n: LocaleManager,
        theme: ThemeManager,
        on_apply: Callable[[str], bool],
        selected_index: int | None = None,
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

        super().__init__(parent)
        self.window.title(translate("voice.lab.title"))
        self.window.geometry("940x630")
        self.window.minsize(720, 490)
        self.window.configure(bg=colors.bg_window)

        container = tk.Frame(
            self.window, bg=colors.bg_window, padx=spacing.md, pady=spacing.md
        )
        container.pack(fill=tk.BOTH, expand=True)
        for key in ("voice.lab.heading", "voice.lab.roll"):
            tk.Label(
                container, text=translate(key), bg=colors.bg_window,
                fg=colors.text_primary, font=self._font,
            ).pack(anchor=tk.W, pady=(0, spacing.xs))

        navigation = tk.Frame(container, bg=colors.bg_window)
        navigation.pack(fill=tk.X, pady=(spacing.xs, spacing.sm))
        tk.Label(
            navigation, text=translate("voice.lab.event"), bg=colors.bg_window,
            fg=colors.text_primary, font=self._font,
        ).pack(side=tk.LEFT, padx=(0, spacing.sm))
        self._event_selector = ttk.Combobox(navigation, state="readonly", font=self._font)
        self._event_selector.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._event_selector.bind("<<ComboboxSelected>>", self._on_view_change)
        self._event_selector.bind("<Left>", lambda _event: self._move_event(-1))
        self._event_selector.bind("<Right>", lambda _event: self._move_event(1))
        tk.Label(
            navigation, text=translate("voice.lab.zoom"), bg=colors.bg_window,
            fg=colors.text_primary, font=self._font,
        ).pack(side=tk.LEFT, padx=spacing.sm)
        zoom_labels = (translate("voice.lab.zoom.overview"), *(f"{level}×" for level in _TIME_ZOOM_LEVELS[1:]))
        self._zoom_selector = ttk.Combobox(
            navigation, state="readonly", values=zoom_labels, width=14, font=self._font,
        )
        self._zoom_selector.pack(side=tk.LEFT)
        self._zoom_selector.current(0)
        self._zoom_selector.bind("<<ComboboxSelected>>", self._on_view_change)
        self._zoom_selector.bind("<Left>", lambda _event: self._move_zoom(-1))
        self._zoom_selector.bind("<Right>", lambda _event: self._move_zoom(1))
        self._update_events(selected_index)

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

            canvas = PianoRoll(panel, colors, self._font)
            canvas.pack(fill=tk.X)
            canvas.bind("<Configure>", lambda _event, index=side: self._draw_roll(index))
            canvas.bind("<Button-1>", lambda event, roll=canvas: self._select_note(roll, event))
            self._canvases.append(canvas)

            text_frame = tk.Frame(panel, bg=colors.bg_surface)
            text_frame.pack(fill=tk.BOTH, expand=True, pady=spacing.sm)
            preview = tk.Text(
                text_frame, height=5, width=24, wrap=tk.WORD, state=tk.DISABLED,
                bg=colors.bg_window, fg=colors.text_primary, font=self._font,
                padx=spacing.sm, pady=spacing.sm,
            )
            configure_readonly_preview(preview, colors)
            scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=preview.yview)
            preview.configure(yscrollcommand=scrollbar.set)
            preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._previews.append(preview)
            button = ttk.Button(
                panel, text=translate(f"voice.lab.apply_{name}"),
                command=lambda index=side: self._apply_profile(index), state=tk.DISABLED,
            )
            button.pack(side=tk.BOTTOM, anchor=tk.E, before=text_frame)
            self._apply_buttons.append(button)

        ttk.Button(container, text=translate("voice.lab.close"), command=self._close).pack(
            side=tk.BOTTOM, anchor=tk.E, pady=(spacing.sm, 0), before=body
        )
        self._render(0)
        self._render(1)
        self._show(self._selectors[0])

    def _refresh_changed_project(self) -> bool:
        if self._revision == self._controller.revision:
            return False
        self._revision = self._controller.revision
        self._profiles = [None, None]
        self._update_events(self._event_selector.current())
        self._render(0)
        self._render(1)
        return True

    def _update_events(self, selected: int | None) -> None:
        session = self._controller.session
        chords = session.chords
        self._timings = tuple(session.get_chord_event_timing(i) for i in range(len(chords)))
        t = self._i18n.translate
        values = tuple(
            t("voice.lab.event.label", number=index + 1, chord=chord, start=start, end=start + duration)
            for index, (chord, (start, duration)) in enumerate(zip(chords, self._timings, strict=True))
        )
        state = "readonly" if values else tk.DISABLED
        self._event_selector.configure(values=values, state=state)
        self._zoom_selector.configure(state=state)
        if values:
            self._event_selector.current(min(max(0, selected or 0), len(values) - 1))
        else:
            self._event_selector.set("")

    def _redraw_rolls(self) -> None:
        for index in range(len(self._canvases)):
            self._draw_roll(index)

    def _on_view_change(self, _event: tk.Event) -> None:
        if not self._refresh_changed_project():
            self._redraw_rolls()

    def _select_note(self, roll: PianoRoll, event: tk.Event) -> None:
        if self._refresh_changed_project():
            return
        selected = roll.event_at(event.x, event.y)
        if selected is not None:
            self._show_event(selected)

    def _move_event(self, step: int) -> str:
        self._refresh_changed_project()
        self._show_event(self._event_selector.current() + step)
        return "break"

    def _move_zoom(self, step: int) -> str:
        self._refresh_changed_project()
        selected = self._zoom_selector.current() + step
        if self._timings and 0 <= selected < len(_TIME_ZOOM_LEVELS):
            self._zoom_selector.current(selected)
            self._redraw_rolls()
        return "break"

    def _show_event(self, selected: int) -> None:
        if 0 <= selected < len(self._timings) and selected != self._event_selector.current():
            self._event_selector.current(selected)
            self._redraw_rolls()

    def _select_style(self, side: int) -> None:
        if not self._refresh_changed_project():
            self._render(side)

    def _render(self, side: int) -> None:
        session = self._controller.session
        chords = tuple(session.chords)
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
        self._redraw_rolls()

    def _draw_roll(self, side: int) -> None:
        canvas = self._canvases[side]
        profile = self._profiles[side]
        pitches = [
            note for item in self._profiles if item
            for voicing in item.midi_notes for note in voicing
        ]
        if profile is None or not pitches or not self._timings:
            canvas.delete("all")
            return
        pitch_range = max(0, min(pitches) - 1), min(127, max(pitches) + 1)
        end = max(start + duration for start, duration in self._timings)
        selected_index = self._event_selector.current()
        zoom = _TIME_ZOOM_LEVELS[self._zoom_selector.current()]
        viewport = TickViewport.around(end, zoom, self._timings[selected_index])
        canvas.draw(self._timings, profile.midi_notes, pitch_range, viewport, selected_index)

    def _apply_profile(self, side: int) -> None:
        if self._refresh_changed_project():
            return
        profile = self._profiles[side]
        if profile is not None and self._on_apply(profile.style.value):
            self._close()
