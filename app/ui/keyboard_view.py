"""Tk canvas that renders a ``KeyboardViewModel``; it holds no music logic.

The canvas only draws what the view model says: key geometry from the viewport,
state colours from theme tokens, and text badges/labels from the model. Canvas
items are created once per viewport/size and then re-configured, so a note
change never rebuilds widgets.
"""

from __future__ import annotations

import tkinter as tk
from tkinter.font import Font
from typing import Callable, Optional

from app.ui.theme import ThemeColors
from src.steps.keyboard.model import KeyboardViewport, iter_white_index
from src.steps.keyboard.state import KeyState, KeyVisual, KeyboardViewModel

# Instrument base tones (not semantic states): natural keys light, raised keys dark,
# identical in every theme so the piano stays recognisable.
NATURAL_KEY = "#FBFBF8"
RAISED_KEY = "#22252B"
KEY_EDGE = "#6E7178"
_RING_STATES = (KeyState.SCALE_ROOT, KeyState.SCALE_TONE)


def state_color(state: KeyState, colors: ThemeColors) -> str:
    """Theme token for one semantic state (fallbacks keep older themes valid)."""
    mapping = {
        KeyState.PRACTICE_WRONG: colors.delete or colors.harmonic_altered,
        KeyState.PRACTICE_MISSING: colors.harmonic_subdominant,
        KeyState.PRACTICE_CORRECT: colors.harmonic_tonic,
        KeyState.PRESSED: colors.border_focus,
        KeyState.SELECTED: colors.harmonic_dominant,
        KeyState.CHORD_ROOT: colors.harmonic_tonic,
        KeyState.CHORD_TONE: colors.harmonic_minor or colors.harmonic_subdominant,
        KeyState.COMPARISON_HELD: colors.harmonic_altered,
        KeyState.COMPARISON: colors.text_muted,
        KeyState.SCALE_ROOT: colors.harmonic_tonic,
        KeyState.SCALE_TONE: colors.harmonic_subdominant,
    }
    return mapping[state]


def _luminance(color: str) -> float:
    value = color.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    try:
        r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0.5

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def readable_text(background: str) -> str:
    """Black or white, whichever has the higher WCAG contrast on ``background``."""
    lum = _luminance(background)
    return "#000000" if (lum + 0.05) / 0.05 >= 1.05 / (lum + 0.05) else "#FFFFFF"


class PianoKeyboardCanvas(tk.Canvas):
    """Horizontal piano keyboard for one viewport."""

    def __init__(
        self,
        parent: tk.Misc,
        colors: ThemeColors,
        font: tuple[str, int],
        *,
        on_press: Optional[Callable[[int], None]] = None,
        on_release: Optional[Callable[[int], None]] = None,
        height: int = 150,
    ) -> None:
        super().__init__(
            parent, height=height, width=640, bg=colors.bg_surface, highlightthickness=2,
            highlightbackground=colors.bg_surface, highlightcolor=colors.border_focus, takefocus=True,
        )
        self._colors = colors
        self._font = Font(root=self, font=font)
        self._small = Font(root=self, family=self._font.actual("family"), size=max(7, font[1] - 2))
        self._on_press = on_press
        self._on_release = on_release
        self._model: Optional[KeyboardViewModel] = None
        self._layout_key: Optional[tuple[KeyboardViewport, int, int]] = None
        self._items: dict[int, dict[str, int]] = {}
        self._mouse_note: Optional[int] = None
        self.layout_count = 0  # observable for tests: full re-layouts performed
        self.bind("<Configure>", self._on_configure)
        self.bind("<ButtonPress-1>", self._on_button_press)
        self.bind("<ButtonRelease-1>", self._on_button_release)

    # -- public API -------------------------------------------------------------
    @property
    def model(self) -> Optional[KeyboardViewModel]:
        return self._model

    def set_model(self, model: KeyboardViewModel) -> None:
        self._model = model
        self._ensure_layout()
        self._paint()

    def key_at(self, x: int, y: int) -> Optional[int]:
        """Topmost key under the pointer (raised keys are drawn above natural keys)."""
        for item in reversed(self.find_overlapping(x, y, x, y)):
            for tag in self.gettags(item):
                if tag.startswith("key:"):
                    return int(tag.removeprefix("key:"))
        return None

    def key_center(self, midi: int) -> tuple[int, int]:
        x0, y0, x1, y1 = self.coords(self._items[midi]["rect"])
        return int((x0 + x1) / 2), int(y0 + (y1 - y0) * 0.8)

    def item_ids(self, midi: int) -> dict[str, int]:
        return dict(self._items[midi])

    # -- layout -------------------------------------------------------------------
    def _on_configure(self, _event: tk.Event) -> None:
        if self._model is not None:
            if self._ensure_layout():
                self._paint()

    def _ensure_layout(self) -> bool:
        if self._model is None:
            return False
        width, height = max(self.winfo_width(), 1), max(self.winfo_height(), 1)
        key = (self._model.viewport, width, height)
        if key == self._layout_key:
            return False
        self._layout_key = key
        self._layout(self._model.viewport, width, height)
        return True

    def _layout(self, viewport: KeyboardViewport, width: int, height: int) -> None:
        self.delete("all")
        self._items.clear()
        self.layout_count += 1
        pad = 4
        whites = len(viewport.white_keys())
        key_w = max(4.0, (width - 2 * pad) / whites)
        top, bottom = pad, max(pad + 40, height - pad)
        black_w, black_h = key_w * 0.6, (bottom - top) * 0.6
        positions: dict[int, tuple[float, float, float, float]] = {}
        for column, key in iter_white_index(viewport):
            if key.is_white:
                x0 = pad + column * key_w
                positions[key.midi] = (x0, top, x0 + key_w, bottom)
            else:
                center = pad + (column + 1) * key_w
                positions[key.midi] = (center - black_w / 2, top, center + black_w / 2, top + black_h)
        ordered = [k for k in viewport.keys() if k.is_white] + [k for k in viewport.keys() if k.is_black]
        for key in ordered:
            x0, y0, x1, y1 = positions[key.midi]
            tag = f"key:{key.midi}"
            base = RAISED_KEY if key.is_black else NATURAL_KEY
            rect = self.create_rectangle(x0, y0, x1, y1, fill=base, outline=KEY_EDGE, width=1,
                                         tags=("key", tag, "raised" if key.is_black else "natural"))
            ring = self.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2, outline="", width=3,
                                         tags=("ring", tag))
            mh = y1 - y0
            # Natural-key marks sit below the raised keys so nothing is covered.
            m0, m1, b, lab = (0.64, 0.84, 0.74, None) if key.is_white else (0.40, 0.78, 0.59, 0.20)
            marker = self.create_rectangle(x0 + 3, y0 + mh * m0, x1 - 3, y0 + mh * m1,
                                           fill="", outline="", tags=("marker", tag))
            badge = self.create_text((x0 + x1) / 2, y0 + mh * b, text="", font=self._small,
                                     tags=("badge", tag))
            label = self.create_text((x0 + x1) / 2, y1 - 3 if lab is None else y0 + mh * lab,
                                     anchor=tk.S if lab is None else tk.CENTER, text="",
                                     font=self._small, tags=("label", tag))
            self._items[key.midi] = {"rect": rect, "ring": ring, "marker": marker, "badge": badge, "label": label}

    # -- painting -----------------------------------------------------------------
    def _paint(self) -> None:
        if self._model is None:
            return
        colors = self._colors
        for visual in self._model.keys:
            items = self._items.get(visual.midi)
            if items is None:
                continue
            self._paint_key(visual, items, colors)

    def _paint_key(self, visual: KeyVisual, items: dict[str, int], colors: ThemeColors) -> None:
        base = RAISED_KEY if visual.key.is_black else NATURAL_KEY
        # Scale membership is context, not an event: it is drawn as a ring, never as
        # a filled marker, so chord/input/practice markers stay visually dominant.
        scale_state = visual.fill if visual.fill in _RING_STATES else visual.outline
        marker_state = None if visual.fill in _RING_STATES else visual.fill
        fill = state_color(marker_state, colors) if marker_state is not None else ""
        self.itemconfigure(items["marker"], fill=fill)
        ring = state_color(scale_state, colors) if scale_state is not None else ""
        self.itemconfigure(items["ring"], outline=ring, width=3 if scale_state is KeyState.SCALE_ROOT else 2)
        badge_bg = fill or base
        self.itemconfigure(items["badge"], text=" ".join(visual.badges), fill=readable_text(badge_bg))
        self.itemconfigure(items["label"], text=visual.label, fill=readable_text(base))

    def _on_button_press(self, event: tk.Event) -> None:
        self.focus_set()
        midi = self.key_at(event.x, event.y)
        self._mouse_note = midi
        if midi is not None and self._on_press is not None:
            self._on_press(midi)

    def _on_button_release(self, _event: tk.Event) -> None:
        midi, self._mouse_note = self._mouse_note, None
        if midi is not None and self._on_release is not None:
            self._on_release(midi)


__all__ = ["NATURAL_KEY", "RAISED_KEY", "PianoKeyboardCanvas", "readable_text", "state_color"]
