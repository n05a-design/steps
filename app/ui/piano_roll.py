"""Tk piano roll for voicings on the project's absolute tick axis."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Sequence
from dataclasses import dataclass
from tkinter.font import Font

from app.ui.theme import ThemeColors


@dataclass(frozen=True)
class TickViewport:
    """Visible interval on the absolute project tick axis."""

    start: int
    end: int

    @classmethod
    def around(cls, project_end: int, zoom: int, event: tuple[int, int]) -> TickViewport:
        duration = max(1, (project_end + zoom - 1) // zoom)
        event_start, event_duration = event
        center = event_start + event_duration // 2
        start = max(0, min(center - duration // 2, project_end - duration))
        return cls(start, start + duration)

    def clip_event(self, start: int, duration: int) -> tuple[int, int] | None:
        left = max(start, self.start)
        right = min(start + duration, self.end)
        return (left, right) if left < right else None


def pitch_axis_labels(low: int, high: int, height: int, line_height: int) -> tuple[int, ...]:
    """Keep the end labels and fit octave labels between them."""
    labels = [low]
    minimum_gap = line_height * (high - low)
    for note in range((low // 12 + 1) * 12, high, 12):
        if min(note - labels[-1], high - note) * height >= minimum_gap:
            labels.append(note)
    return (*labels, high)


class PianoRoll(tk.Canvas):
    """Draw notes using the scale shared by both comparison panes."""

    def __init__(self, parent: tk.Misc, colors: ThemeColors, label_font: tuple[str, int]) -> None:
        super().__init__(parent, width=320, height=140, bg=colors.bg_window, highlightthickness=0)
        self._colors = colors
        self._label_font = Font(root=self, font=label_font)

    def event_at(self, x: int, y: int) -> int | None:
        """Find the topmost note with a small pointer hit area."""
        for item in reversed(self.find_overlapping(x - 3, y - 3, x + 3, y + 3)):
            for tag in self.gettags(item):
                if tag.startswith("event:"):
                    return int(tag.removeprefix("event:"))
        return None

    def draw(
        self,
        timings: Sequence[tuple[int, int]],
        midi_notes: Sequence[Sequence[int]],
        pitch_range: tuple[int, int],
        viewport: TickViewport,
        selected_event: int,
    ) -> None:
        self.delete("all")
        if not timings or self.winfo_width() < 64 or self.winfo_height() <= 30:
            return
        low, high = pitch_range
        left = max(28, self._label_font.measure(str(high)) + 8)
        top = 10
        right, bottom = self.winfo_width() - 10, self.winfo_height() - 20
        colors = self._colors

        def x(tick: int) -> float:
            return left + (tick - viewport.start) / (viewport.end - viewport.start) * (right - left)

        def y(note: int) -> float:
            return bottom - (note - low) / (high - low) * (bottom - top)

        if 0 <= selected_event < len(timings):
            event = viewport.clip_event(*timings[selected_event])
            if event is not None:
                start, end = event
                self.create_rectangle(
                    x(start), top, x(end), bottom, fill=colors.bg_active,
                    outline=colors.border_focus, tags=("selected-event",),
                )

        for note in (low, *range((low // 12 + 1) * 12, high, 12), high):
            self.create_line(left, y(note), right, y(note), fill=colors.border)
        line_height = self._label_font.metrics("linespace") + 2
        for note in pitch_axis_labels(low, high, bottom - top, line_height):
            self.create_text(
                left - 4, y(note), text=str(note), anchor=tk.E,
                fill=colors.text_secondary, font=self._label_font, tags=("pitch-label",),
            )
        middle = (viewport.start + viewport.end) // 2
        for tick in sorted({viewport.start, middle, viewport.end}):
            anchor = tk.W if tick == viewport.start else tk.E if tick == viewport.end else tk.CENTER
            self.create_text(
                x(tick), bottom + 10, text=str(tick), anchor=anchor,
                fill=colors.text_secondary, font=self._label_font, tags=("tick-label",),
            )
        for start, _ in timings:
            if viewport.start <= start < viewport.end:
                self.create_line(x(start), top, x(start), bottom, fill=colors.border)
        for index, ((start, duration), notes) in enumerate(zip(timings, midi_notes, strict=True)):
            event = viewport.clip_event(start, duration)
            if event is None:
                continue
            event_left, event_right = event
            x_left = x(event_left)
            x_right = min(right, max(x_left + 1, x(event_right)))
            bass = min(notes, default=None)
            for note in notes:
                self.create_line(
                    x_left, y(note), x_right, y(note), width=3 if note == bass else 2,
                    fill=colors.harmonic_tonic if note == bass else colors.text_primary,
                    tags=("note", f"event:{index}"),
                )
