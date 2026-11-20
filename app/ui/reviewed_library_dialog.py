"""Browse source-reviewed progression examples without mutating the active project."""

from __future__ import annotations

import tkinter as tk
from typing import Callable, Iterable

from app.i18n import LocaleManager
from app.ui.theme import ThemeManager, create_button
from src.steps.progression.engine import ReviewedProgression


def reviewed_progression_matches(example: ReviewedProgression, query: str) -> bool:
    """Match a query against published example metadata and reviewed claim text."""
    needle = query.strip().casefold()
    if not needle:
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
    return needle in " ".join(fields).casefold()


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


class ReviewedProgressionLibraryDialog:
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
        colors = theme.colors
        spacing = theme.spacing
        typography = theme.typography
        translate = i18n.translate

        self.window = tk.Toplevel(parent)
        self.window.title(translate("library.title"))
        self.window.geometry("920x620")
        self.window.minsize(760, 500)
        self.window.transient(parent)
        self.window.configure(bg=colors.bg_window)
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.bind("<Escape>", lambda _event: self._close())

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

        body = tk.PanedWindow(
            container,
            orient=tk.HORIZONTAL,
            bg=colors.border,
            bd=1,
            sashrelief=tk.FLAT,
            sashwidth=4,
        )
        body.pack(fill=tk.BOTH, expand=True)

        list_frame = tk.Frame(body, bg=colors.bg_surface)
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
        body.add(list_frame, minsize=250)

        preview_frame = tk.Frame(body, bg=colors.bg_window)
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
        preview_scrollbar = tk.Scrollbar(
            preview_frame,
            orient=tk.VERTICAL,
            command=self._preview.yview,
        )
        self._preview.configure(yscrollcommand=preview_scrollbar.set)
        self._preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        body.add(preview_frame, minsize=380)

        buttons = tk.Frame(container, bg=colors.bg_window)
        buttons.pack(side=tk.BOTTOM, fill=tk.X, pady=(spacing.sm, 0), before=body)
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

        self.window.grab_set()
        self._refresh_list()
        self._search_entry.focus_set()

    def _refresh_list(self, *_args: object) -> None:
        query = self._search_var.get()
        self._visible_examples = tuple(
            example
            for example in self._examples
            if reviewed_progression_matches(example, query)
        )
        self._listbox.delete(0, tk.END)
        for example in self._visible_examples:
            progression = example.progression
            self._listbox.insert(tk.END, progression.name)
        if len(self._visible_examples) == 1:
            self._listbox.selection_set(0)
        self._select_current()
        if not self._visible_examples:
            self._set_preview(self._i18n.translate("library.no_results"))

    def _select_current(self, _event: object | None = None) -> None:
        selection = self._listbox.curselection()
        if not selection or selection[0] >= len(self._visible_examples):
            self._selected = None
            self._load_button.configure(state=tk.DISABLED)
            self._set_preview(self._i18n.translate("library.select_prompt"))
            return
        self._selected = self._visible_examples[selection[0]]
        self._load_button.configure(state=tk.NORMAL)
        self._set_preview(
            format_reviewed_progression(self._selected, self._i18n.translate)
        )

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

    def _load_selected(self, _event: object | None = None) -> None:
        if self._selected is not None and self._on_load(
            self._selected.progression.prog_id
        ):
            self._close()

    def _close(self) -> None:
        self.window.destroy()
