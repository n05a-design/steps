"""
Glide-aligned rounded Canvas widgets for STEPS (ADR-001 / ADR-003 / Designvertrag).

Implements:
- RoundedSurfaceCard: Carrier-card container with smooth rounded corners via
  rounded_rect_points, hosting an inner Frame for arbitrary child widgets.
- RoundedButton: Interactive button with rounded contour, hover/active fill,
  focus indicators, and full keyboard/accessibility support.
"""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import font as tkfont
from typing import Callable, Optional

from glide_shell import custom_controls, text_fit, window_lifetime
from app.ui import layout_policy


def _measure_text_width(font: tuple | tkfont.Font, text: str, widget: tk.Misc) -> int:
    try:
        return int(widget.tk.call("font", "measure", font, text))
    except Exception:
        return len(text) * 8


class RoundedSurfaceCard(tk.Canvas):
    """Glide carrier-card surface with rounded corners and embedded frame."""

    def __init__(
        self,
        master: tk.Misc,
        bg_color: str,
        fill_color: str,
        outline_color: Optional[str] = None,
        radius: int = 12,
        padding: int = 6,
        inner_pad_x: Optional[int] = None,
        inner_pad_y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        auto_height: bool = False,
        **kwargs,
    ) -> None:
        opts: dict = {
            "bg": bg_color,
            "highlightthickness": 0,
            "bd": 0,
        }
        if width is not None:
            opts["width"] = width
        if height is not None:
            opts["height"] = height
        opts.update(kwargs)
        super().__init__(master, **opts)

        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color or fill_color
        self.radius = max(0, radius)
        self.inner_pad_x = padding if inner_pad_x is None else inner_pad_x
        self.inner_pad_y = padding if inner_pad_y is None else inner_pad_y
        self.auto_height = auto_height
        self._auto_height_value: Optional[int] = None
        self._draw_pending: Optional[str] = None

        self.inner = tk.Frame(self, bg=fill_color, bd=0, highlightthickness=0)
        self._window_id = self.create_window(
            self.inner_pad_x,
            self.inner_pad_y,
            anchor="nw",
            window=self.inner,
        )

        custom_controls.bind_resize(self, self._on_configure)
        if self.auto_height:
            self.inner.bind("<Configure>", self._sync_auto_height)
        self._draw()

    def set_theme(
        self,
        bg_color: str,
        fill_color: str,
        outline_color: Optional[str] = None,
        radius: Optional[int] = None,
    ) -> None:
        """Update surface colors and redraw rounded contour."""
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color or fill_color
        if radius is not None:
            self.radius = max(0, radius)
        try:
            self.configure(bg=bg_color)
            self.inner.configure(bg=fill_color)
        except tk.TclError:
            pass
        self._draw()

    def _sync_auto_height(self, _event: Optional[tk.Event] = None) -> None:
        if not self.auto_height:
            return
        try:
            needed = max(1, self.inner.winfo_reqheight() + self.inner_pad_y * 2)
        except tk.TclError:
            return
        if needed == self._auto_height_value:
            return
        self._auto_height_value = needed
        try:
            self.configure(height=needed)
        except tk.TclError:
            pass

    def _on_configure(self, _event: Optional[tk.Event] = None) -> None:
        pad_x = self.inner_pad_x
        pad_y = self.inner_pad_y
        w = max(self.winfo_width(), pad_x * 2 + 2)
        h = max(self.winfo_height(), pad_y * 2 + 2)
        try:
            self.coords(self._window_id, pad_x, pad_y)
            if self.auto_height:
                self.itemconfigure(self._window_id, width=max(1, w - pad_x * 2), height=0)
                self._sync_auto_height()
            else:
                self.itemconfigure(
                    self._window_id,
                    width=max(1, w - pad_x * 2),
                    height=max(1, h - pad_y * 2),
                )
        except tk.TclError:
            pass
        self._schedule_draw()

    def _schedule_draw(self) -> None:
        if self._draw_pending is None:
            try:
                scope = window_lifetime.scope_for(self)
                self._draw_pending = scope.after_idle(self._draw_scheduled)
            except Exception:
                self._draw()

    def _draw_scheduled(self) -> None:
        self._draw_pending = None
        self._draw()

    def _draw(self) -> None:
        try:
            self.delete("surface")
            w = max(self.winfo_width(), 4)
            h = max(self.winfo_height(), 4)
            pad = 1
            if self.radius > 0 and w > self.radius * 2 and h > self.radius * 2:
                points = custom_controls.rounded_rect_points(
                    pad, pad, w - pad, h - pad, self.radius
                )
                self.create_polygon(
                    points,
                    smooth=True,
                    splinesteps=24,
                    fill=self.fill_color,
                    outline=self.outline_color,
                    width=1,
                    tags=("surface",),
                )
            else:
                self.create_rectangle(
                    pad, pad, w - pad, h - pad,
                    fill=self.fill_color,
                    outline=self.outline_color,
                    width=1,
                    tags=("surface",),
                )
            self.tag_lower("surface")
        except tk.TclError:
            pass


class RoundedButton(tk.Canvas):
    """Accessible Glide button with rounded outline, hover feedback and keyboard navigation."""

    TEXT_INSET = 20

    def __init__(
        self,
        master: tk.Misc,
        text: str = "",
        command: Optional[Callable[[], None]] = None,
        bg_color: str = "#121319",
        base_bg: str = "#1E222C",
        base_fg: str = "#F3F1ED",
        hover_bg: Optional[str] = None,
        hover_fg: Optional[str] = None,
        active_bg: Optional[str] = None,
        active_fg: Optional[str] = None,
        border_color: Optional[str] = None,
        radius: int = 10,
        height: int = 32,
        width: int = 80,
        font: Optional[tuple] = None,
        outline: bool = True,
        cursor: str = "hand2",
        **kwargs,
    ) -> None:
        self.anchor = str(kwargs.pop("anchor", "center"))
        self.padx = int(kwargs.pop("padx", 0))
        self.pady = int(kwargs.pop("pady", 0))
        self.relief = str(kwargs.pop("relief", "flat"))
        self._state: str = str(kwargs.pop("state", tk.NORMAL))
        self.justify = str(kwargs.pop("justify", "center"))
        self.wraplength = int(kwargs.pop("wraplength", 0))

        opts: dict = {
            "height": height,
            "width": width,
            "bg": bg_color,
            "highlightthickness": 0,
            "bd": 0,
            "cursor": cursor,
            "takefocus": 1,
        }
        opts.update(kwargs)
        super().__init__(master, **opts)

        self._text = str(text)
        self.command = command
        self.bg_color = bg_color
        self.base_bg = base_bg
        self.base_fg = base_fg
        self.hover_bg = hover_bg or base_bg
        self.hover_fg = hover_fg or base_fg
        self.active_bg = active_bg or hover_bg or base_bg
        self.active_fg = active_fg or hover_fg or base_fg
        self.border_color = border_color or base_bg
        self.radius = max(0, radius)
        self.button_height = height
        self.min_width = width
        self.outline = outline
        self.font = font or ("Helvetica", 11)

        self.is_hovered: bool = False
        self.is_pressed: bool = False
        self._glide_is_active: bool = False
        self._draw_pending: Optional[str] = None

        self.display_text = layout_policy.clip_button_text(self._text)
        self._fit_width()

        custom_controls.bind_resize(self, self._on_configure)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<space>", self._on_activate)
        self.bind("<Return>", self._on_activate)
        self.bind("<FocusIn>", lambda _e=None: self._draw())
        self.bind("<FocusOut>", lambda _e=None: self._draw())

        self._draw()

    @property
    def text(self) -> str:
        return self._text

    def set_text(self, text: str) -> None:
        self._text = str(text)
        self.display_text = layout_policy.clip_button_text(self._text)
        self._fit_width()
        self._draw()

    def configure(self, **kwargs) -> None:
        if "text" in kwargs:
            self.set_text(kwargs.pop("text"))
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "state" in kwargs:
            self._state = str(kwargs.pop("state"))
        if "fg" in kwargs:
            self.base_fg = kwargs.pop("fg")
        elif "foreground" in kwargs:
            self.base_fg = kwargs.pop("foreground")
        if "bg" in kwargs:
            self.base_bg = kwargs.pop("bg")
        elif "background" in kwargs:
            self.base_bg = kwargs.pop("background")
        if "anchor" in kwargs:
            self.anchor = str(kwargs.pop("anchor"))
        if "padx" in kwargs:
            self.padx = int(kwargs.pop("padx"))
        if "pady" in kwargs:
            self.pady = int(kwargs.pop("pady"))
        if "relief" in kwargs:
            self.relief = str(kwargs.pop("relief"))
        if "justify" in kwargs:
            self.justify = str(kwargs.pop("justify"))
        if "wraplength" in kwargs:
            self.wraplength = int(kwargs.pop("wraplength"))
        super().configure(**kwargs)
        self._draw()

    config = configure

    def cget(self, key: str) -> object:
        if key == "text":
            return self._text
        if key == "state":
            return self._state
        if key in ("fg", "foreground"):
            return self.base_fg
        if key in ("bg", "background"):
            return self.base_bg
        if key == "anchor":
            return self.anchor
        if key == "padx":
            return self.padx
        if key == "pady":
            return self.pady
        if key == "relief":
            return self.relief
        return super().cget(key)

    def __getitem__(self, key: str) -> object:
        return self.cget(key)

    def __setitem__(self, key: str, value: object) -> None:
        self.configure(**{key: value})

    def invoke(self) -> None:
        """Programmatically invoke the button's command, mirroring tk.Button.invoke()."""
        if self._state == tk.DISABLED:
            return
        if callable(self.command):
            self.command()

    def set_active(self, active: bool) -> None:
        """Toggle active selection highlight."""
        self._glide_is_active = bool(active)
        self._draw()

    def set_theme(
        self,
        bg_color: str,
        base_bg: str,
        base_fg: str,
        hover_bg: Optional[str] = None,
        hover_fg: Optional[str] = None,
        active_bg: Optional[str] = None,
        active_fg: Optional[str] = None,
        border_color: Optional[str] = None,
        radius: Optional[int] = None,
        font: Optional[tuple] = None,
    ) -> None:
        """Update button palette tokens and redraw."""
        self.bg_color = bg_color
        self.base_bg = base_bg
        self.base_fg = base_fg
        self.hover_bg = hover_bg or base_bg
        self.hover_fg = hover_fg or base_fg
        self.active_bg = active_bg or hover_bg or base_bg
        self.active_fg = active_fg or hover_fg or base_fg
        self.border_color = border_color or base_bg
        if radius is not None:
            self.radius = max(0, radius)
        if font is not None:
            self.font = font
            self._fit_width()
        try:
            super().configure(bg=bg_color)
        except tk.TclError:
            pass
        self._draw()

    def _fit_width(self) -> None:
        needed = _measure_text_width(self.font, self.display_text, self) + self.TEXT_INSET
        target_w = max(self.min_width, needed)
        try:
            if int(super().cget("width")) != target_w:
                super().configure(width=target_w)
        except (tk.TclError, ValueError):
            pass

    def _on_enter(self, _event: tk.Event) -> None:
        if self._state == tk.DISABLED:
            return
        self.is_hovered = True
        self._draw()

    def _on_leave(self, _event: tk.Event) -> None:
        self.is_hovered = False
        self.is_pressed = False
        self._draw()

    def _on_press(self, _event: tk.Event) -> None:
        if self._state == tk.DISABLED:
            return
        self.focus_set()
        self.is_pressed = True
        self._draw()

    def _on_release(self, event: tk.Event) -> None:
        if self._state == tk.DISABLED or not self.is_pressed:
            return
        self.is_pressed = False
        self._draw()
        w = self.winfo_width()
        h = self.winfo_height()
        if 0 <= event.x <= w and 0 <= event.y <= h:
            if callable(self.command):
                self.command()

    def _on_activate(self, _event: tk.Event) -> str:
        if self._state == tk.DISABLED:
            return "break"
        if callable(self.command):
            self.command()
        return "break"

    def _on_configure(self, _event: Optional[tk.Event] = None) -> None:
        self._schedule_draw()

    def _schedule_draw(self) -> None:
        if self._draw_pending is None:
            try:
                scope = window_lifetime.scope_for(self)
                self._draw_pending = scope.after_idle(self._draw_scheduled)
            except Exception:
                self._draw()

    def _draw_scheduled(self) -> None:
        self._draw_pending = None
        self._draw()

    def _draw(self) -> None:
        try:
            self.delete("all")
            w = max(self.winfo_width(), 30)
            h = max(self.winfo_height(), self.button_height)
            pad = 2

            if self._state == tk.DISABLED:
                fill = self.base_bg
                fg = self.border_color
            elif self._glide_is_active:
                fill = self.active_bg
                fg = self.active_fg
            elif self.is_pressed and self.is_hovered:
                fill = self.active_bg
                fg = self.active_fg
                pad = 3
            elif self.is_hovered:
                fill = self.hover_bg
                fg = self.hover_fg
            else:
                fill = self.base_bg
                fg = self.base_fg

            focused = self.focus_get() is self
            border_w = 2 if focused else (1 if self.outline else 0)
            outline_col = (
                self.hover_fg if focused else (self.border_color if self.outline else fill)
            )

            if self.radius > 0 and w > self.radius * 2 and h > self.radius * 2:
                points = custom_controls.rounded_rect_points(
                    pad, pad, w - pad, h - pad, self.radius
                )
                self.create_polygon(
                    points,
                    smooth=True,
                    splinesteps=24,
                    fill=fill,
                    outline=outline_col,
                    width=border_w,
                    tags=("button_bg",),
                )
            else:
                self.create_rectangle(
                    pad, pad, w - pad, h - pad,
                    fill=fill,
                    outline=outline_col,
                    width=border_w,
                    tags=("button_bg",),
                )

            cy = h / 2
            # Position text according to anchor
            if self.anchor in ("w", tk.W):
                cx = pad + max(8, self.padx)
                text_anchor = tk.W
            elif self.anchor in ("e", tk.E):
                cx = w - pad - max(8, self.padx)
                text_anchor = tk.E
            else:
                cx = w / 2
                text_anchor = tk.CENTER

            self.create_text(
                cx, cy,
                text=self.display_text,
                font=self.font,
                fill=fg,
                anchor=text_anchor,
                tags=("button_text",),
            )
        except tk.TclError:
            pass
