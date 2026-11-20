"""Browse source-reviewed progression examples without mutating the active project."""

from __future__ import annotations

import tkinter as tk
from typing import Callable, Iterable

from app.i18n import LocaleManager
from app.ui.dialog_support import ModalDialog, configure_readonly_preview
from app.ui.theme import ThemeManager, create_button
from src.steps.progression.engine import ReviewedProgression


def reviewed_progression_matches(example: ReviewedProgression, query: str) -> bool:
    """Match a query against published example metadata and reviewed claim text."""
    terms = query.casefold().split()
    if not terms:
        return True

    progression = example.progression
    fields = [
        progression.prog_id,
        progression.name,
        progression.roman_numerals,
        progression.default_key,
        progression.chords_str,
        progression.context,
        example.catalog_version,
        *example.source_ids,
    ]
    for approved in example.claims:
        claim = approved.claim
        fields.extend(
            (
                claim.claim_id,
                claim.kind,
                claim.text,
                claim.scope,
                claim.countercheck,
                approved.reviewer,
                approved.reviewed_on,
            )
        )
        for citation in claim.citations:
            fields.extend(
                (citation.source_id, citation.title, citation.locator, citation.url)
            )
    haystack = " ".join(fields).casefold()
    return all(term in haystack for term in terms)


def format_reviewed_progression(
    example: ReviewedProgression,
    translate: Callable[..., str],
) -> str:
    """Render catalog data and its review evidence without translating source claims."""
    progression = example.progression
    lines = [
        translate("library.detail.id", value=progression.prog_id),
        translate("library.detail.progression", value=progression.chords_str),
        translate("library.detail.roman", value=progression.roman_numerals),
        translate("library.detail.key", value=progression.default_key),
        translate("library.detail.context", value=progression.context),
        translate("library.detail.reviewed", value=example.reviewed_on),
        translate("library.detail.catalog", value=example.catalog_version),
        translate("library.detail.sources", value=", ".join(example.source_ids)),
        "",
        translate("library.claims.heading"),
    ]

    for approved in example.claims:
        claim = approved.claim
        lines.extend(
            (
                "",
                translate("library.claim.heading", value=claim.claim_id),
                translate(
                    "library.claim.kind",
                    value=translate(f"library.claim.kind.{claim.kind}"),
                ),
                claim.text,
                translate("library.claim.scope", value=claim.scope),
                translate("library.claim.countercheck", value=claim.countercheck),
            )
        )
        for citation in claim.citations:
            lines.append(
                translate(
                    "library.claim.citation",
                    source_id=citation.source_id,
                    title=citation.title,
                    locator=citation.locator,
                    url=citation.url,
                )
            )
        lines.append(
            translate(
                "library.claim.review",
                reviewer=approved.reviewer,
                date=approved.reviewed_on,
                url=approved.evidence_url,
            )
        )

    return "\n".join(lines)


class ReviewedProgressionLibraryDialog(ModalDialog):
    """Modal catalog browser; loading is delegated until the user confirms."""

    def __init__(
        self,
        parent: tk.Misc,
        examples: Iterable[ReviewedProgression],
        i18n: LocaleManager,
        theme: ThemeManager,
        on_load: Callable[[str], bool],
    ) -> None:
        self._examples = tuple(examples)
        self._visible_examples: tuple[ReviewedProgression, ...] = ()
        self._selected: ReviewedProgression | None = None
        self._i18n = i18n
        self._on_load = on_load
        self._theme = theme
        colors = theme.colors
        spacing = theme.spacing
        typography = theme.typography
        translate = i18n.translate

        super().__init__(parent)
        self.window.title(translate("library.title"))
        self.window.geometry("920x620")
        self.window.minsize(760, 500)
        self.window.configure(bg=colors.bg_window)

        container = tk.Frame(self.window, bg=colors.bg_window, padx=spacing.md, pady=spacing.md)
        container.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            container,
            text=translate("library.heading"),
            bg=colors.bg_window,
            fg=colors.text_primary,
            font=(typography.font_family_sans, typography.size_lg, "bold"),
        ).pack(anchor=tk.W, pady=(0, spacing.sm))

        search_row = tk.Frame(container, bg=colors.bg_window)
        search_row.pack(fill=tk.X, pady=(0, spacing.sm))
        tk.Label(
            search_row,
            text=translate("library.search"),
            bg=colors.bg_window,
            fg=colors.text_secondary,
            font=(typography.font_family_sans, typography.size_sm),
        ).pack(side=tk.LEFT, padx=(0, spacing.sm))
        self._search_var = tk.StringVar(self.window)
        self._search_entry = tk.Entry(
            search_row,
            textvariable=self._search_var,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            insertbackground=colors.text_primary,
            relief=tk.FLAT,
            font=(typography.font_family_sans, typography.size_md),
        )
        self._search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._search_entry.bind("<Down>", self._focus_results)
        self._search_var.trace_add("write", self._refresh_list)

        self._chord_preview = tk.Frame(container, bg=colors.bg_window)
        self._body = tk.PanedWindow(
            container,
            orient=tk.HORIZONTAL,
            bg=colors.border,
            bd=1,
            sashrelief=tk.FLAT,
            sashwidth=4,
        )
        self._body.pack(fill=tk.BOTH, expand=True)

        list_frame = tk.Frame(self._body, bg=colors.bg_surface)
        self._listbox = tk.Listbox(
            list_frame,
            bg=colors.bg_surface,
            fg=colors.text_primary,
            selectbackground=colors.harmonic_tonic,
            selectforeground=colors.text_inverted,
            activestyle="dotbox",
            font=(typography.font_family_sans, typography.size_sm),
            relief=tk.FLAT,
            exportselection=False,
        )
        list_scrollbar = tk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self._listbox.yview,
        )
        self._listbox.configure(yscrollcommand=list_scrollbar.set)
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._listbox.bind("<<ListboxSelect>>", self._select_current)
        self._listbox.bind("<Double-Button-1>", self._load_selected)
        self._listbox.bind("<Return>", self._load_selected)
        self._body.add(list_frame, minsize=250)

        preview_frame = tk.Frame(self._body, bg=colors.bg_window)
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
        configure_readonly_preview(self._preview, colors)
        preview_scrollbar = tk.Scrollbar(
            preview_frame,
            orient=tk.VERTICAL,
            command=self._preview.yview,
        )
        self._preview.configure(yscrollcommand=preview_scrollbar.set)
        self._preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._body.add(preview_frame, minsize=380)

        buttons = tk.Frame(container, bg=colors.bg_window)
        buttons.pack(side=tk.BOTTOM, fill=tk.X, pady=(spacing.sm, 0), before=self._body)
        create_button(
            buttons,
            text=translate("library.close"),
            command=self._close,
            bg=colors.bg_active,
            fg=colors.text_primary,
            relief=tk.FLAT,
            padx=spacing.md,
        ).pack(side=tk.RIGHT)
        self._load_button = create_button(
            buttons,
            text=translate("library.load"),
            command=self._load_selected,
            bg=colors.harmonic_tonic,
            fg=colors.text_inverted,
            relief=tk.FLAT,
            padx=spacing.md,
            state=tk.DISABLED,
        )
        self._load_button.pack(side=tk.RIGHT, padx=(0, spacing.sm))

        self._refresh_list()
        self._show(self._search_entry)

    def _refresh_list(self, *_args: object) -> None:
        query = self._search_var.get()
        selected = self._selected
        self._visible_examples = tuple(
            example
            for example in self._examples
            if reviewed_progression_matches(example, query)
        )
        self._listbox.delete(0, tk.END)
        for index, example in enumerate(self._visible_examples):
            self._listbox.insert(tk.END, example.progression.name)
            if example is selected or len(self._visible_examples) == 1:
                self._listbox.selection_set(index)
                self._listbox.activate(index)
                self._listbox.see(index)
        self._select_current()

    def _select_current(self, _event: object | None = None) -> None:
        selection = self._listbox.curselection()
        if not selection or selection[0] >= len(self._visible_examples):
            self._selected = None
            self._chord_preview.pack_forget()
            self._load_button.configure(state=tk.DISABLED)
            prompt = "library.select_prompt" if self._visible_examples else "library.no_results"
            self._set_preview(self._i18n.translate(prompt))
            return
        selected = self._visible_examples[selection[0]]
        if selected is self._selected:
            return
        self._selected = selected
        self._render_chords(selected)
        self._load_button.configure(state=tk.NORMAL)
        self._set_preview(
            format_reviewed_progression(self._selected, self._i18n.translate)
        )

    def _render_chords(self, example: ReviewedProgression) -> None:
        progression = example.progression
        chords = progression.chords_str.split(" - ")
        degrees = progression.roman_numerals.split(" - ")
        if len(degrees) != len(chords):
            degrees = [""] * len(chords)

        colors = self._theme.colors
        spacing = self._theme.spacing
        typography = self._theme.typography
        for child in self._chord_preview.winfo_children():
            child.destroy()
        tk.Label(
            self._chord_preview,
            text=self._i18n.translate("library.detail.key", value=progression.default_key),
            fg=colors.text_secondary,
            bg=colors.bg_window,
            font=(typography.font_family_sans, typography.size_sm),
        ).pack(anchor=tk.W, pady=(0, spacing.xs))
        row = tk.Frame(self._chord_preview, bg=colors.bg_window)
        row.pack(fill=tk.X)
        for column, (chord, degree) in enumerate(zip(chords, degrees)):
            row.columnconfigure(column, weight=1, uniform="chords")
            card = tk.Frame(row, bg=colors.bg_surface, pady=spacing.xs)
            card.grid(row=0, column=column, sticky="nsew", padx=spacing.xs)
            tk.Label(
                card, text=chord, bg=colors.bg_surface, fg=colors.text_primary,
                font=(typography.font_family_mono, typography.size_md, "bold"),
            ).pack()
            if degree:
                tk.Label(
                    card, text=degree, bg=colors.bg_surface, fg=colors.text_secondary,
                    font=(typography.font_family_sans, typography.size_sm),
                ).pack()
        self._chord_preview.pack(fill=tk.X, pady=(0, spacing.sm), before=self._body)

    def _focus_results(self, _event: object) -> str:
        if self._visible_examples:
            if not self._listbox.curselection():
                self._listbox.selection_set(0)
                self._listbox.activate(0)
                self._select_current()
            self._listbox.focus_set()
        return "break"

    def _set_preview(self, text: str) -> None:
        self._preview.configure(state=tk.NORMAL)
        self._preview.delete("1.0", tk.END)
        self._preview.insert("1.0", text)
        self._preview.configure(state=tk.DISABLED)
        self._preview.yview_moveto(0)

    def _load_selected(self, _event: object | None = None) -> None:
        if self._selected is not None and self._on_load(
            self._selected.progression.prog_id
        ):
            self._close()
