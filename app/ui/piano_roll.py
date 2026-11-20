"""Tk piano roll for voicings on the project's absolute tick axis."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Sequence

from app.ui.theme import ThemeColors


class PianoRoll(tk.Canvas):
    """Draw notes using the scale shared by both comparison panes."""

    def __init__(self, parent: tk.Misc, colors: ThemeColors, label_font: tuple[str, int]) -> None:
        super().__init__(parent, width=320, height=140, bg=colors.bg_window, highlightthickness=0)
        self._colors = colors
        self._label_font = label_font

    def draw(
        self,
        timings: Sequence[tuple[int, int]],
        midi_notes: Sequence[Sequence[int]],
        pitch_range: tuple[int, int],
        end: int,
    ) -> None:
        self.delete("all")
        if not timings or end <= 0 or self.winfo_width() < 64 or self.winfo_height() <= 30:
            return
        low, high = pitch_range
        left, top = 28, 10
        right, bottom = self.winfo_width() - 10, self.winfo_height() - 20
        colors = self._colors

        def x(tick: int) -> float:
            return left + tick / end * (right - left)

        def y(note: int) -> float:
            return bottom - (note - low) / (high - low) * (bottom - top)

        for note in range(low, high + 1):
            if note in (low, high) or note % 12 == 0:
                self.create_line(left, y(note), right, y(note), fill=colors.border)
                self.create_text(left - 4, y(note), text=str(note), anchor=tk.E,
                                   fill=colors.text_secondary, font=self._label_font)
        for tick in sorted({0, end // 2, end}):
            anchor = tk.W if tick == 0 else tk.E if tick == end else tk.CENTER
            self.create_text(x(tick), bottom + 10, text=str(tick), anchor=anchor,
                               fill=colors.text_secondary, font=self._label_font)
        for start, _duration in timings:
            self.create_line(x(start), top, x(start), bottom, fill=colors.border)
        for (start, duration), notes in zip(timings, midi_notes, strict=True):
            bass = min(notes, default=None)
            for note in notes:
                self.create_line(
                    x(start), y(note), max(x(start) + 1, x(start + duration)), y(note),
                    width=3 if note == bass else 2,
                    fill=colors.harmonic_tonic if note == bass else colors.text_primary,
                    tags=("note",),
                )

