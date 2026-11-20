"""Shared keyboard and focus behavior for modal desktop dialogs."""

from __future__ import annotations

import tkinter as tk

from app.ui.theme import ThemeColors


class ModalDialog:
    """Own a Tk modal window and restore the previous focus on close."""

    def __init__(self, parent: tk.Misc) -> None:
        owner = parent.winfo_toplevel()
        self._previous_focus = owner.focus_get() or owner.focus_lastfor()
        self._previous_grab = owner.grab_current()
        self.window = tk.Toplevel(owner)
        self.window.transient(owner)
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.bind("<Escape>", self._cancel)

    def _show(self, initial_focus: tk.Misc) -> None:
        self.window.update_idletasks()
        self.window.grab_set()
        initial_focus.focus_set()

    def _cancel(self, _event: tk.Event) -> str:
        self._close()
        return "break"

    def _close(self) -> None:
        if not self.window.winfo_exists():
            return
        active_grab = self.window.grab_current()
        if active_grab == self.window:
            self.window.grab_release()
        self.window.destroy()
        if active_grab not in (None, self.window):
            return
        if self._previous_grab is not None and self._previous_grab.winfo_viewable():
            self._previous_grab.grab_set()
        if self._previous_focus is not None and self._previous_focus.winfo_viewable():
            self._previous_focus.focus_set()


def configure_readonly_preview(widget: tk.Text, colors: ThemeColors) -> None:
    """Keep disabled analysis text keyboard reachable without trapping Tab."""
    widget.configure(
        takefocus=True,
        highlightthickness=2,
        highlightbackground=colors.border,
        highlightcolor=colors.border_focus,
    )

    def focus_adjacent(_event: tk.Event, backwards: bool = False) -> str:
        next_widget = widget.tk_focusPrev() if backwards else widget.tk_focusNext()
        if next_widget is not None:
            next_widget.focus_set()
        return "break"

    def page(_event: tk.Event, direction: int) -> str:
        widget.yview_scroll(direction, "pages")
        return "break"

    widget.bind("<Tab>", focus_adjacent)
    for sequence in ("<Shift-Tab>", "<ISO_Left_Tab>"):
        widget.bind(sequence, lambda event: focus_adjacent(event, backwards=True))
    widget.bind("<Prior>", lambda event: page(event, -1))
    widget.bind("<Next>", lambda event: page(event, 1))
