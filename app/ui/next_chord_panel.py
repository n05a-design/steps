"""Tk presentation and interaction for the Next Chord Explorer."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox

from app.i18n import LocaleManager
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager, create_button
from src.steps.progression.reviewed import PublicationError, resolve_source_citation
from src.steps.progression.session import ChordRecommendation
from src.steps.theory.exceptions import MusicTheoryError


class NextChordPanel:
    """Keep recommendation selection bound to its source chord and revision."""

    def __init__(
        self,
        toolbar: tk.Misc,
        content: tk.Misc,
        *,
        controller: ProgressionSessionController,
        i18n: LocaleManager,
        theme: ThemeManager,
        selected_chord: Callable[[], int | None],
        show_detail: Callable[[str], None],
        on_applied: Callable[[int, ChordRecommendation], None],
    ) -> None:
        self._parent = content.winfo_toplevel()
        self._controller = controller
        self._i18n = i18n
        self._selected_chord = selected_chord
        self._show_detail = show_detail
        self._on_applied = on_applied
        self._recommendations: list[ChordRecommendation] = []
        self._context: tuple[int, int] | None = None
        self._comparison_index: int | None = None
        colors, spacing = theme.colors, theme.spacing

        self.explore_button = create_button(
            toolbar, text="", command=self.explore, bg=colors.bg_active,
            fg=colors.text_primary, relief=tk.FLAT, padx=spacing.sm,
        )
        self.explore_button.pack(side=tk.RIGHT, padx=spacing.xs)
        frame = tk.Frame(content, bg=colors.bg_surface, bd=0)
        frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, spacing.sm), pady=spacing.sm)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        self._heading = tk.Label(
            frame, text="", font=("Helvetica", 10, "bold"),
            fg=colors.harmonic_dominant, bg=colors.bg_surface,
        )
        self._heading.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, spacing.xs))
        self.candidates = tk.Listbox(
            frame, font=("Helvetica", 11),
            bg=colors.bg_window, fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic, selectforeground=colors.text_inverted,
            highlightthickness=2, highlightbackground=colors.border,
            highlightcolor=colors.border_focus, relief=tk.FLAT, activestyle="dotbox",
            exportselection=False, takefocus=False, height=8, width=36,
        )
        scrollbar = tk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.candidates.yview, takefocus=False,
        )
        self.candidates.configure(yscrollcommand=scrollbar.set)
        self.candidates.grid(row=1, column=0, sticky="nsew", padx=(spacing.xs, 0))
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.candidates.bind("<<ListboxSelect>>", self._selection_changed)
        self.candidates.bind("<Return>", self._apply_shortcut)
        self.apply_button = create_button(
            frame, text="", command=self.apply, bg=colors.harmonic_tonic,
            fg=colors.text_inverted, relief=tk.FLAT, padx=spacing.sm, state=tk.DISABLED,
        )
        self.apply_button.grid(row=2, column=0, columnspan=2, sticky="e", pady=(spacing.xs, 0))
        self.comparison_button = create_button(
            frame, text="", command=self._toggle_comparison, bg=colors.bg_active,
            fg=colors.text_primary, relief=tk.FLAT, padx=spacing.sm, state=tk.DISABLED,
        )
        self.comparison_button.grid(
            row=3, column=0, columnspan=2, sticky="e", pady=(spacing.xs, 0),
        )
        self.localize()

    def localize(self) -> bool:
        """Translate the controls and restore an active, current selection."""
        t = self._i18n.translate
        self.explore_button.configure(text=t("next_chord.explore"))
        self.apply_button.configure(text=t("next_chord.apply"))
        self._heading.configure(text=t("next_chord.candidates"))
        self._update_comparison_button()
        if self._context != self._current_context():
            return False
        selected = self._selected_recommendation_index()
        self._render_candidates(selected)
        return True

    def clear(self) -> None:
        if self._parent.focus_get() in (self.candidates, self.apply_button, self.comparison_button):
            self.explore_button.focus_set()
        self._context = None
        self._comparison_index = None
        self._recommendations.clear()
        self.candidates.delete(0, tk.END)
        self.candidates.configure(takefocus=False)
        self.apply_button.configure(state=tk.DISABLED)
        self._update_comparison_button()

    def explore(self) -> None:
        index = self._selected_chord()
        t = self._i18n.translate
        if index is None:
            messagebox.showerror(
                t("chord.change.error.title"), t("chord.selection.required"), parent=self._parent,
            )
            return
        try:
            recommendations = self._controller.explore_next(index)
        except (IndexError, MusicTheoryError, ValueError) as exc:
            self.clear()
            self._show_error("next_chord.error.message", error=exc)
            return

        self._comparison_index = None
        self._recommendations = list(recommendations)
        self._context = (index, self._controller.revision)
        self._render_candidates(0 if recommendations else None)
        if recommendations:
            self.candidates.focus_set()

    def apply(self) -> None:
        index = self._selected_recommendation_index()
        chord_index, revision = self._current_context()
        if chord_index is None or index is None:
            self._show_error("next_chord.selection.required")
            return
        if self._context != (chord_index, revision):
            self.clear()
            self._show_detail(self._i18n.translate("next_chord.stale"))
            return
        recommendation = self._recommendations[index]
        try:
            applied = self._controller.apply_next_recommendation(
                chord_index, recommendation.candidate_symbol,
                selected=recommendation, expected_revision=revision,
            )
        except (IndexError, MusicTheoryError, ValueError) as exc:
            self._show_error("next_chord.error.message", error=exc)
            return
        self._on_applied(chord_index + 1, applied)

    def _current_context(self) -> tuple[int | None, int]:
        return self._selected_chord(), self._controller.revision

    def _selected_recommendation_index(self) -> int | None:
        selection = self.candidates.curselection()
        if selection and 0 <= selection[0] < len(self._recommendations):
            return selection[0]
        return None

    def _apply_shortcut(self, _event: tk.Event) -> str:
        if self._selected_recommendation_index() is not None:
            self.apply()
        return "break"

    def _render_candidates(self, selected: int | None) -> None:
        t = self._i18n.translate
        self.candidates.delete(0, tk.END)
        for recommendation in self._recommendations:
            relation = t(f"next_chord.relation.{recommendation.relation_type}")
            self.candidates.insert(tk.END, f"{recommendation.candidate_symbol} — {relation}")
        self.candidates.configure(takefocus=bool(self._recommendations))
        if selected is not None:
            self.candidates.selection_set(selected)
            self.candidates.selection_anchor(selected)
            self.candidates.activate(selected)
            self.candidates.see(selected)
        self._selection_changed()

    def _selection_changed(self, _event: tk.Event | None = None) -> None:
        index = self._selected_recommendation_index()
        self.apply_button.configure(state=tk.NORMAL if index is not None else tk.DISABLED)
        self._update_comparison_button()
        if self._context is None:
            return
        t = self._i18n.translate
        heading = f"{t('next_chord.heading')}\n\n{t('next_chord.disclaimer')}\n"
        if index is None:
            hint = "next_chord.inspect" if self._recommendations else "next_chord.empty"
            self._show_detail(f"{heading}\n{t(hint)}\n")
            return
        selected = self._format_candidate(self._recommendations[index])
        reference = self._comparison_index
        if reference is None:
            self._show_detail(f"{heading}\n{selected}\n")
        elif reference == index:
            self._show_detail(f"{heading}\n{t('next_chord.compare.choose')}\n\n{selected}\n")
        else:
            pinned = self._format_candidate(self._recommendations[reference])
            self._show_detail(
                f"{heading}\n{t('next_chord.compare.reference')}\n{pinned}\n\n"
                f"{t('next_chord.compare.selected')}\n{selected}\n"
            )

    def _format_candidate(self, recommendation: ChordRecommendation) -> str:
        t = self._i18n.translate
        relation = t(f"next_chord.relation.{recommendation.relation_type}")
        reason = t(f"next_chord.reason.{recommendation.relation_type}")
        evidence = t(f"next_chord.evidence.{recommendation.evidence_kind}")
        if recommendation.evidence_kind == "LITERATURE_REFERENCE":
            try:
                citation = resolve_source_citation(recommendation.source_id or "", recommendation.source_locator or "")
            except PublicationError:
                evidence = t("next_chord.evidence.unavailable")
            else:
                evidence = f"{evidence}\n{citation.title}\n{citation.locator}\n{citation.url}"
        return (
            f"{recommendation.candidate_symbol} — {relation}\n{reason}\n"
            f"{t('next_chord.framework')}: {recommendation.framework}\n"
            f"{evidence}\n"
            f"\n{t('next_chord.original')}\n{recommendation.explanation}"
        )

    def _update_comparison_button(self) -> None:
        pinned = self._comparison_index is not None
        enabled = pinned or (
            len(self._recommendations) > 1 and self._selected_recommendation_index() is not None
        )
        key = "next_chord.compare.clear" if pinned else "next_chord.compare.pin"
        self.comparison_button.configure(
            text=self._i18n.translate(key), state=tk.NORMAL if enabled else tk.DISABLED,
        )

    def _toggle_comparison(self) -> None:
        if self._context != self._current_context():
            self.clear()
            self._show_detail(self._i18n.translate("next_chord.stale"))
            return
        if self._comparison_index is None:
            index = self._selected_recommendation_index()
            if index is None or len(self._recommendations) < 2:
                return
            self._comparison_index = index
            self.candidates.focus_set()
        else:
            self._comparison_index = None
        self._selection_changed()

    def _show_error(self, message_key: str, **params: object) -> None:
        t = self._i18n.translate
        messagebox.showerror(t("next_chord.error.title"), t(message_key, **params), parent=self._parent)
