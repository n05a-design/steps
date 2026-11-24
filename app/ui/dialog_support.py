"""Shared keyboard and focus behavior for modal desktop dialogs via glide_shell."""

from __future__ import annotations

import tkinter as tk

from glide_shell import modal_session, window_lifetime

from app.ui.theme import ThemeColors


class ModalDialog:
    """Own a Tk modal window and restore the previous focus/grab on close."""

    def __init__(self, parent: tk.Misc) -> None:
        owner = parent.winfo_toplevel()
        self._owner = owner
        self._previous_focus = owner.focus_get() or owner.focus_lastfor()
        self._previous_grab = owner.grab_current()
        self.window = modal_session.create_dialog(owner, "")
        self._remembered_focus = modal_session.remember_focus(owner, self.window, owner)
        self._lifetime_scope = window_lifetime.scope_for(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.bind("<Escape>", self._cancel)

    def _show(self, initial_focus: tk.Misc) -> None:
        self.window.update_idletasks()
        modal_session.ensure_min_width(self.window)
        setattr(self.window, modal_session.ACTIVE_ATTRIBUTE, True)
        try:
            self.window.grab_set()
        except tk.TclError:
            pass
        initial_focus.focus_set()

    def _cancel(self, _event: tk.Event) -> str:
        self._close()
        return "break"

    def _close(self) -> None:
        if not self.window.winfo_exists():
            return
        self._lifetime_scope.close()
        setattr(self.window, modal_session.ACTIVE_ATTRIBUTE, False)
        active_grab = self.window.grab_current()
        if active_grab == self.window:
            try:
                self.window.grab_release()
            except tk.TclError:
                pass
        self.window.destroy()
        if active_grab not in (None, self.window):
            return
        if (
            self._previous_grab is not None
            and self._previous_grab.winfo_exists()
            and self._previous_grab.winfo_viewable()
        ):
            self._previous_grab.grab_set()
        if not modal_session.return_focus(self._owner, self.window, self._remembered_focus):
            if (
                self._previous_focus is not None
                and self._previous_focus.winfo_exists()
                and self._previous_focus.winfo_viewable()
            ):
                self._previous_focus.focus_set()


def configure_readonly_preview(widget: tk.Text, colors: ThemeColors) -> None:
    """Keep disabled analysis text keyboard reachable without trapping Tab."""
    widget.configure(
        takefocus=True,
        highlightthickness=2,
        highlightbackground=colors.bg_surface,
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
