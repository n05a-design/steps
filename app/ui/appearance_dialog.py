"""
Appearance & Customization Modal Dialog for STEPS (Glide parity).

Provides Glide's compact two-column Settings layout with rounded dropdown
selectors (`GlideOptionSelector`), a live accent monogram tile (`AccentMonogramTile`),
theme/background/accent/corner-radius/font/language/behavior controls, and a
live preview card using `RoundedSurfaceCard` and `RoundedButton`.
"""

from __future__ import annotations

import inspect
import tkinter as tk
from collections.abc import Sequence
from typing import Callable, Optional

from glide_shell import custom_controls, text_fit, window_lifetime
from glide_shell.custom_controls import ThemedAutoScrollbar

from app.i18n import LocaleManager
from app.ui import layout_policy
from app.ui.custom_widgets import RoundedButton, RoundedSurfaceCard
from app.ui.dialog_support import ModalDialog
from app.ui.theme import (
    ACCENT_CHOICES,
    BACKGROUND_CHOICES,
    FONT_SCALE_CHOICES,
    FONT_SCALE_MAP,
    FONT_WEIGHT_CHOICES,
    RADIUS_CHOICES,
    RADIUS_MAP,
    ThemeColors,
    ThemeManager,
    apply_window_geometry,
    create_button,
    with_accent,
    with_background,
)


def _measure_px(font: tuple, text: str, widget: tk.Misc) -> int:
    try:
        return int(widget.tk.call("font", "measure", font, text))
    except Exception:
        return len(text) * 8


class AccentMonogramTile(tk.Canvas):
    """Glide-style 52x52 rounded accent tile previewing STEPS brand tint contrast."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        bg_color: str,
        fill_color: str,
        text_color: str,
        radius: int = 14,
        size: int = 52,
        letter: str = "S",
        font: tuple = ("Helvetica", 20, "bold"),
    ) -> None:
        super().__init__(
            master,
            width=size,
            height=size,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
        )
        self.size = size
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.text_color = text_color
        self.radius = max(0, radius)
        self.letter = letter
        self.font = font
        self._draw()

    def set_theme(
        self,
        *,
        bg_color: str,
        fill_color: str,
        text_color: str,
        radius: Optional[int] = None,
    ) -> None:
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.text_color = text_color
        if radius is not None:
            self.radius = max(0, radius)
        try:
            super().configure(bg=bg_color)
        except tk.TclError:
            pass
        self._draw()

    def _draw(self) -> None:
        try:
            self.delete("all")
            s = self.size
            pad = 2
            if self.radius > 0:
                pts = custom_controls.rounded_rect_points(pad, pad, s - pad, s - pad, min(self.radius, s // 2 - 2))
                self.create_polygon(
                    pts,
                    smooth=True,
                    splinesteps=24,
                    fill=self.fill_color,
                    outline="",
                    tags=("tile",),
                )
            else:
                self.create_rectangle(pad, pad, s - pad, s - pad, fill=self.fill_color, outline="", tags=("tile",))
            self.create_text(
                s / 2,
                s / 2,
                text=self.letter,
                fill=self.text_color,
                font=self.font,
                anchor=tk.CENTER,
                tags=("letter",),
            )
        except tk.TclError:
            pass


class GlideOptionSelector(tk.Canvas):
    """Glide-styled rounded dropdown selector bound to a canonical key StringVar."""

    def __init__(
        self,
        master: tk.Misc,
        key_variable: tk.StringVar,
        options: Sequence[tuple[str, str]],
        colors: ThemeColors,
        *,
        radius: int = 10,
        font: tuple = ("Helvetica", 11),
        swatch_resolver: Optional[Callable[[str], Optional[str]]] = None,
        on_change: Optional[Callable[[], None]] = None,
        bg_color: Optional[str] = None,
        height: int = 34,
    ) -> None:
        self._key_var = key_variable
        self._items = list(options)
        self._label_by_key = dict(self._items)
        self._colors = colors
        self._bg_color = bg_color or colors.bg_surface
        self._radius = max(0, radius)
        self._font = font
        self._swatch_resolver = swatch_resolver
        self._on_change = on_change
        self._height = height
        self._is_open = False
        self._is_hovered = False
        self._draw_pending: Optional[str] = None

        super().__init__(
            master,
            height=height,
            bg=self._bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            takefocus=1,
        )

        self.menu = tk.Menu(self, tearoff=False)
        for key, label in self._items:
            self.menu.add_command(
                label=label,
                command=lambda selected=key: self._select(selected),
            )
        self._style_menu()

        self._trace_id = self._key_var.trace_add("write", lambda *_a: self._schedule_draw())
        self.bind("<Destroy>", self._on_destroy, add="+")
        self.bind("<Configure>", lambda _e=None: self._schedule_draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._open_menu)
        self.bind("<FocusIn>", lambda _e=None: self._schedule_draw())
        self.bind("<FocusOut>", lambda _e=None: self._schedule_draw())
        for seq in ("<space>", "<Return>", "<Down>", "<Up>"):
            self.bind(seq, self._open_menu)

        self._draw()

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self and self._trace_id is not None:
            try:
                self._key_var.trace_remove("write", self._trace_id)
            except tk.TclError:
                pass
            self._trace_id = None

    def _select(self, key: str) -> None:
        self._key_var.set(key)
        self._schedule_draw()
        if callable(self._on_change):
            self._on_change()

    def _style_menu(self) -> None:
        try:
            self.menu.configure(
                bg=self._colors.bg_surface,
                fg=self._colors.text_primary,
                activebackground=self._colors.harmonic_tonic,
                activeforeground=self._colors.text_inverted,
                bd=0,
                font=self._font,
            )
        except tk.TclError:
            pass

    def _on_enter(self, _event: tk.Event) -> None:
        self._is_hovered = True
        self._schedule_draw()

    def _on_leave(self, _event: tk.Event) -> None:
        self._is_hovered = False
        self._schedule_draw()

    def _open_menu(self, _event: Optional[tk.Event] = None) -> str:
        self.focus_set()
        self._is_open = True
        self._draw()
        try:
            self.menu.tk_popup(
                self.winfo_rootx(),
                self.winfo_rooty() + max(1, self.winfo_height()),
            )
        finally:
            self._is_open = False
            self._schedule_draw()
        return "break"

    def set_theme(
        self,
        colors: ThemeColors,
        *,
        bg_color: Optional[str] = None,
        radius: Optional[int] = None,
        font: Optional[tuple] = None,
    ) -> None:
        self._colors = colors
        if bg_color is not None:
            self._bg_color = bg_color
            try:
                super().configure(bg=bg_color)
            except tk.TclError:
                pass
        if radius is not None:
            self._radius = max(0, radius)
        if font is not None:
            self._font = font
        self._style_menu()
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
            w = max(self.winfo_width(), 120)
            h = max(self.winfo_height(), self._height)
            pad = 1
            focused = self.focus_get() is self
            border_color = (
                self._colors.border_focus
                if (focused or self._is_open or self._is_hovered)
                else self._colors.border
            )
            fill = self._colors.bg_surface_hover if self._is_hovered else self._colors.bg_active

            r = min(self._radius, (h - 2) // 2)
            if r > 0 and w > r * 2:
                pts = custom_controls.rounded_rect_points(pad, pad, w - pad, h - pad, r)
                self.create_polygon(
                    pts,
                    smooth=True,
                    splinesteps=24,
                    fill=fill,
                    outline=border_color,
                    width=2 if focused else 1,
                    tags=("field_bg",),
                )
            else:
                self.create_rectangle(
                    pad,
                    pad,
                    w - pad,
                    h - pad,
                    fill=fill,
                    outline=border_color,
                    width=2 if focused else 1,
                    tags=("field_bg",),
                )

            current_key = self._key_var.get()
            swatch = self._swatch_resolver(current_key) if self._swatch_resolver else None
            text_x = 12
            if swatch:
                cy = h / 2
                self.create_oval(10, cy - 5, 20, cy + 5, fill=swatch, outline="", tags=("swatch",))
                text_x = 28

            chevron = "\u25b4" if self._is_open else "\u25be"
            self.create_text(
                w - 14,
                h / 2,
                text=chevron,
                fill=self._colors.text_secondary,
                font=self._font,
                anchor=tk.CENTER,
                tags=("chevron",),
            )

            raw_label = self._label_by_key.get(current_key, current_key)
            max_px = max(24, w - text_x - 26)
            fitted = text_fit.fit(raw_label, lambda s: _measure_px(self._font, s, self), max_px)
            self.create_text(
                text_x,
                h / 2,
                text=fitted,
                fill=self._colors.text_primary,
                font=self._font,
                anchor=tk.W,
                tags=("label",),
            )
        except tk.TclError:
            pass


class AppearanceDialog(ModalDialog):
    """Modal Glide-style Settings dialog for appearance, geometry, language, and behavior."""

    THEME_OPTIONS: tuple[tuple[str, str], ...] = (
        ("system", "theme.system"),
        ("dark", "theme.dark"),
        ("light", "theme.light"),
        ("glass-dark", "theme.glass_dark"),
        ("glass-light", "theme.glass_light"),
        ("dopamine", "theme.dopamine"),
        ("contrast-dark", "theme.contrast_dark"),
        ("contrast-light", "theme.contrast_light"),
        ("minimal-dark", "theme.minimal_dark"),
        ("minimal-light", "theme.minimal_light"),
        ("pixel", "theme.pixel"),
    )

    def __init__(
        self,
        parent: tk.Misc,
        theme: ThemeManager,
        i18n: LocaleManager,
        theme_preference: str = "dark",
        on_apply: Optional[Callable[..., None]] = None,
        on_language_change: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.i18n = i18n
        self.on_apply = on_apply
        self.on_language_change = on_language_change

        self.initial_theme_preference = theme_preference
        self.initial_background = theme.background_choice
        self.initial_accent = getattr(theme, "accent_choice", "accent")
        self.initial_radius = theme.radius_choice
        self.initial_scale = theme.font_scale_choice
        self.initial_weight = getattr(theme, "font_weight_choice", "standard")
        self.initial_language = i18n.preference
        self.initial_animations = getattr(theme, "animations_enabled", True)
        self.initial_hints = getattr(theme, "hints_visible", True)

        self.theme_var = tk.StringVar(value=theme_preference)
        self.bg_var = tk.StringVar(value=self.initial_background)
        self.accent_var = tk.StringVar(value=self.initial_accent)
        self.radius_var = tk.StringVar(value=self.initial_radius)
        self.scale_var = tk.StringVar(value=self.initial_scale)
        self.weight_var = tk.StringVar(value=self.initial_weight)
        self.language_var = tk.StringVar(value=self.initial_language)
        self.animations_var = tk.BooleanVar(value=self.initial_animations)
        self.hints_var = tk.BooleanVar(value=self.initial_hints)

        t = self.i18n.translate
        self.window.title(t("appearance.dialog.title"))
        apply_window_geometry(self.window, 780, 620, 680, 520)
        self.window.configure(bg=theme.colors.bg_window)

        self._build_ui()
        self._update_preview()
        self._show(self.apply_btn)

    def _swatch_for_theme(self, key: str) -> Optional[str]:
        if key == "system":
            return self.theme.colors.text_muted
        normalized = self.theme.normalize_theme_name(key)
        raw = self.theme._raw.get("themes", {}).get(normalized, {})
        return raw.get("harmonic_tonic")

    def _swatch_for_accent(self, key: str) -> Optional[str]:
        return with_accent(self.theme.colors, key).harmonic_tonic

    def _swatch_for_background(self, key: str) -> Optional[str]:
        return with_background(self.theme.colors, key).bg_window

    def _build_field_label(self, parent: tk.Misc, text: str) -> tk.Label:
        c = self.theme.colors
        lbl = tk.Label(
            parent,
            text=text,
            font=self.theme.font_spec(self.theme.typography.size_xs, "bold"),
            bg=c.bg_surface,
            fg=c.text_secondary,
            anchor="w",
        )
        lbl.pack(fill=tk.X, pady=(8, 4))
        return lbl

    def _add_selector(
        self,
        parent: tk.Misc,
        label_text: str,
        variable: tk.StringVar,
        options: Sequence[tuple[str, str]],
        *,
        swatch_resolver: Optional[Callable[[str], Optional[str]]] = None,
    ) -> GlideOptionSelector:
        self._build_field_label(parent, label_text)
        c = self.theme.colors
        selector = GlideOptionSelector(
            parent,
            variable,
            options,
            c,
            radius=min(self.theme.corner_radius, 10),
            font=self.theme.font_spec(self.theme.typography.size_sm),
            swatch_resolver=swatch_resolver,
            on_change=self._update_preview,
            bg_color=c.bg_surface,
        )
        selector.pack(fill=tk.X, pady=(0, 4))
        self._selectors.append(selector)
        return selector

    def _build_ui(self) -> None:
        t = self.i18n.translate
        c = self.theme.colors
        sp = self.theme.spacing
        self._section_cards: list[RoundedSurfaceCard] = []
        self._selectors: list[GlideOptionSelector] = []

        self.content_frame = tk.Frame(self.window, bg=c.bg_window, padx=sp.md, pady=sp.md)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.header_lbl = tk.Label(
            self.content_frame,
            text=t("appearance.dialog.heading"),
            font=self.theme.font_spec(self.theme.typography.size_lg, "bold"),
            bg=c.bg_window,
            fg=c.text_primary,
            anchor="w",
        )
        self.header_lbl.pack(fill=tk.X, pady=(0, sp.sm))

        # Bottom action bar packed first so scrollable body fills the rest cleanly
        action_bar = tk.Frame(self.content_frame, bg=c.bg_window)
        action_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(sp.sm, 0))

        self.cancel_btn = create_button(
            action_bar,
            text=t("appearance.dialog.cancel"),
            command=self._close,
            bg=c.bg_surface,
            fg=c.text_secondary,
            hover_bg=c.bg_surface_hover,
            carrier_bg=c.bg_window,
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=(sp.sm, 0))

        self.apply_btn = create_button(
            action_bar,
            text=t("appearance.dialog.apply"),
            command=self._on_apply_clicked,
            bg=c.harmonic_tonic,
            fg=c.text_inverted,
            hover_bg=c.border_focus,
            carrier_bg=c.bg_window,
        )
        self.apply_btn.pack(side=tk.RIGHT)

        # Scrollable two-column body
        canvas_container = tk.Frame(self.content_frame, bg=c.bg_window)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(canvas_container, bg=c.bg_window, bd=0, highlightthickness=0)
        self.scrollbar = ThemedAutoScrollbar(
            canvas_container,
            c.bg_window,
            c.bg_surface,
            c.border,
            active_thumb_color=c.harmonic_tonic,
            orient=tk.VERTICAL,
        )
        self.scrollbar.set_command(self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        body = tk.Frame(self.scroll_canvas, bg=c.bg_window)
        body_window = self.scroll_canvas.create_window((0, 0), window=body, anchor="nw")
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.itemconfig(body_window, width=e.width))
        body.bind("<Configure>", lambda _e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        def _on_wheel(event: tk.Event) -> None:
            delta = getattr(event, "delta", 0)
            if delta:
                step = -1 if delta > 0 else 1
                self.scroll_canvas.yview_scroll(step, "units")
            elif getattr(event, "num", None) == 4:
                self.scroll_canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:
                self.scroll_canvas.yview_scroll(1, "units")

        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.window.bind(seq, _on_wheel, add="+")

        columns = tk.Frame(body, bg=c.bg_window)
        columns.pack(fill=tk.BOTH, expand=True)
        columns.columnconfigure((0, 1), weight=1, uniform="settings_cols")

        left_col = tk.Frame(columns, bg=c.bg_window)
        left_col.grid(row=0, column=0, sticky="new", padx=(0, sp.sm))

        right_col = tk.Frame(columns, bg=c.bg_window)
        right_col.grid(row=0, column=1, sticky="new", padx=(sp.sm, 0))

        # --- Left Card: Appearance & Surface (Glide left/appearance parity) ---
        appearance_card = RoundedSurfaceCard(
            left_col,
            bg_color=c.bg_window,
            fill_color=c.bg_surface,
            outline_color=c.border,
            radius=self.theme.corner_radius,
            padding=sp.md,
            auto_height=True,
        )
        appearance_card.pack(fill=tk.X, pady=(0, sp.sm))
        self._section_cards.append(appearance_card)

        tk.Label(
            appearance_card.inner,
            text=t("appearance.dialog.section_appearance"),
            font=self.theme.font_spec(self.theme.typography.size_sm, "bold"),
            bg=c.bg_surface,
            fg=c.text_primary,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 4))

        # Accent color selector + monogram preview tile side-by-side (Glide style)
        self._build_field_label(appearance_card.inner, t("theme.accent.label"))
        accent_row = tk.Frame(appearance_card.inner, bg=c.bg_surface)
        accent_row.pack(fill=tk.X, pady=(0, 6))

        self.monogram_tile = AccentMonogramTile(
            accent_row,
            bg_color=c.bg_surface,
            fill_color=c.harmonic_tonic,
            text_color=c.text_inverted,
            radius=min(14, max(4, self.theme.corner_radius)),
        )
        self.monogram_tile.pack(side=tk.LEFT, padx=(0, sp.sm))

        accent_opts = [(k, t(label_key)) for k, label_key in ACCENT_CHOICES]
        accent_sel = GlideOptionSelector(
            accent_row,
            self.accent_var,
            accent_opts,
            c,
            radius=min(self.theme.corner_radius, 10),
            font=self.theme.font_spec(self.theme.typography.size_sm),
            swatch_resolver=self._swatch_for_accent,
            on_change=self._update_preview,
            bg_color=c.bg_surface,
        )
        accent_sel.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._selectors.append(accent_sel)

        theme_opts = [(k, t(label_key)) for k, label_key in self.THEME_OPTIONS]
        self._add_selector(
            appearance_card.inner,
            t("theme.menu"),
            self.theme_var,
            theme_opts,
            swatch_resolver=self._swatch_for_theme,
        )
        self.design_note_lbl = tk.Label(
            appearance_card.inner,
            text=t("appearance.dialog.design_note"),
            font=self.theme.font_spec(self.theme.typography.size_xs),
            bg=c.bg_surface,
            fg=c.text_muted,
            anchor="w",
            justify=tk.LEFT,
            wraplength=290,
        )
        self.design_note_lbl.pack(fill=tk.X, pady=(0, 4))

        bg_opts = [(k, t(label_key)) for k, label_key in BACKGROUND_CHOICES]
        self._add_selector(
            appearance_card.inner,
            t("theme.background.label"),
            self.bg_var,
            bg_opts,
            swatch_resolver=self._swatch_for_background,
        )
        self.bg_note_lbl = tk.Label(
            appearance_card.inner,
            text=t("appearance.dialog.background_note"),
            font=self.theme.font_spec(self.theme.typography.size_xs),
            bg=c.bg_surface,
            fg=c.text_muted,
            anchor="w",
            justify=tk.LEFT,
            wraplength=290,
        )
        self.bg_note_lbl.pack(fill=tk.X, pady=(0, 4))

        radius_opts = [(k, t(label_key)) for k, label_key, _ in RADIUS_CHOICES]
        self._add_selector(
            appearance_card.inner,
            t("theme.radius.label"),
            self.radius_var,
            radius_opts,
        )

        # --- Right Upper Card: Language, Typography & Behavior ---
        typo_card = RoundedSurfaceCard(
            right_col,
            bg_color=c.bg_window,
            fill_color=c.bg_surface,
            outline_color=c.border,
            radius=self.theme.corner_radius,
            padding=sp.md,
            auto_height=True,
        )
        typo_card.pack(fill=tk.X, pady=(0, sp.sm))
        self._section_cards.append(typo_card)

        tk.Label(
            typo_card.inner,
            text=t("appearance.dialog.section_typography"),
            font=self.theme.font_spec(self.theme.typography.size_sm, "bold"),
            bg=c.bg_surface,
            fg=c.text_primary,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 4))

        lang_opts = [
            ("system", t("language.system")),
            ("de", t("language.de")),
            ("en", t("language.en")),
        ]
        self._add_selector(typo_card.inner, t("language.menu"), self.language_var, lang_opts)

        scale_opts = [(k, t(label_key)) for k, label_key, _ in FONT_SCALE_CHOICES]
        self._add_selector(typo_card.inner, t("theme.font_scale.label"), self.scale_var, scale_opts)

        weight_opts = [(k, t(label_key)) for k, label_key in FONT_WEIGHT_CHOICES]
        self._add_selector(typo_card.inner, t("theme.font_weight.label"), self.weight_var, weight_opts)

        self._build_field_label(typo_card.inner, t("settings.behavior"))
        for text_key, var in (("settings.animations", self.animations_var), ("settings.hints", self.hints_var)):
            cb = tk.Checkbutton(
                typo_card.inner,
                text=t(text_key),
                variable=var,
                command=self._update_preview,
                bg=c.bg_surface,
                fg=c.text_primary,
                selectcolor=c.bg_active,
                activebackground=c.bg_surface,
                activeforeground=c.text_primary,
                highlightthickness=0,
                bd=0,
                anchor="w",
            )
            cb.pack(fill=tk.X, pady=2)

        # --- Right Lower Card: Live Preview ---
        preview_label = tk.Label(
            right_col,
            text=t("appearance.dialog.preview_title"),
            font=self.theme.font_spec(self.theme.typography.size_xs, "bold"),
            bg=c.bg_window,
            fg=c.text_secondary,
            anchor="w",
        )
        preview_label.pack(fill=tk.X, pady=(sp.xs, 4))

        self.preview_window_frame = tk.Frame(right_col, bg=c.bg_window, padx=sp.sm, pady=sp.sm)
        self.preview_window_frame.pack(fill=tk.X)

        self.preview_card = RoundedSurfaceCard(
            self.preview_window_frame,
            bg_color=c.bg_window,
            fill_color=c.bg_surface,
            outline_color=c.border,
            radius=self.theme.corner_radius,
            padding=12,
            auto_height=True,
        )
        self.preview_card.pack(fill=tk.X)

        self.preview_title = tk.Label(
            self.preview_card.inner,
            text=t("appearance.dialog.preview_progression"),
            font=self.theme.font_spec(self.theme.typography.size_md, "bold"),
            bg=c.bg_surface,
            fg=c.text_primary,
            anchor="w",
        )
        self.preview_title.pack(fill=tk.X, pady=(0, 4))

        self.preview_sub = tk.Label(
            self.preview_card.inner,
            text=t("appearance.dialog.preview_analysis"),
            font=self.theme.font_spec(self.theme.typography.size_xs),
            bg=c.bg_surface,
            fg=c.text_secondary,
            anchor="w",
        )
        self.preview_sub.pack(fill=tk.X, pady=(0, 8))

        self.preview_btn = RoundedButton(
            self.preview_card.inner,
            text=layout_policy.clip_button_text(t("appearance.dialog.preview_button")),
            bg_color=c.bg_surface,
            base_bg=c.harmonic_tonic,
            base_fg=c.text_inverted,
            hover_bg=c.border_focus,
            hover_fg=c.text_inverted,
            active_bg=c.harmonic_tonic,
            active_fg=c.text_inverted,
            border_color=c.border,
            radius=self.theme.corner_radius,
            height=30,
            width=150,
        )
        self.preview_btn.pack(anchor="w")

    def _compute_preview_colors(self) -> tuple[ThemeColors, int, float]:
        selected_theme = self.theme_var.get()
        if selected_theme == "system":
            resolved_theme = self.theme.resolve_system_mode(self.window)
        else:
            resolved_theme = self.theme.normalize_theme_name(selected_theme)

        raw_colors = self.theme._raw["themes"].get(resolved_theme, self.theme._raw["themes"]["dark"])
        base_colors = ThemeColors(**raw_colors)
        accented_colors = with_accent(base_colors, self.accent_var.get())
        tinted_colors = with_background(accented_colors, self.bg_var.get())
        radius = RADIUS_MAP.get(self.radius_var.get(), 12)
        scale = FONT_SCALE_MAP.get(self.scale_var.get(), 1.0)
        return tinted_colors, radius, scale

    def _update_preview(self) -> None:
        try:
            colors, radius, scale = self._compute_preview_colors()
            self.preview_window_frame.configure(bg=colors.bg_window)
            if hasattr(self, "monogram_tile"):
                self.monogram_tile.set_theme(
                    bg_color=self.theme.colors.bg_surface,
                    fill_color=colors.harmonic_tonic,
                    text_color=colors.text_inverted,
                    radius=min(14, max(4, radius)),
                )
            for card in getattr(self, "_section_cards", ()):
                card.set_theme(
                    bg_color=self.theme.colors.bg_window,
                    fill_color=self.theme.colors.bg_surface,
                    outline_color=self.theme.colors.border,
                    radius=radius,
                )
            for sel in getattr(self, "_selectors", ()):
                sel.set_theme(
                    self.theme.colors,
                    bg_color=self.theme.colors.bg_surface,
                    radius=min(radius, 10),
                )
            self.preview_card.set_theme(
                bg_color=colors.bg_window,
                fill_color=colors.bg_surface,
                outline_color=colors.border,
                radius=radius,
            )
            font_title = (
                self.theme.typography.font_family_sans,
                max(6, int(round(self.theme.typography.size_md * scale))),
                "bold",
            )
            font_sub = (
                self.theme.typography.font_family_sans,
                max(6, int(round(self.theme.typography.size_xs * scale))),
            )
            self.preview_title.configure(
                bg=colors.bg_surface,
                fg=colors.text_primary,
                font=font_title,
            )
            self.preview_sub.configure(
                bg=colors.bg_surface,
                fg=colors.text_secondary,
                font=font_sub,
            )
            self.preview_btn.set_theme(
                bg_color=colors.bg_surface,
                base_bg=colors.harmonic_tonic,
                base_fg=colors.text_inverted,
                hover_bg=colors.border_focus,
                hover_fg=colors.text_inverted,
                active_bg=colors.harmonic_tonic,
                active_fg=colors.text_inverted,
                border_color=colors.border,
                radius=max(0, radius - 2),
            )
        except Exception:
            pass

    def _on_apply_clicked(self) -> None:
        if callable(self.on_apply):
            sig = inspect.signature(self.on_apply)
            params = len(sig.parameters)
            if params <= 4:
                self.on_apply(
                    self.theme_var.get(),
                    self.bg_var.get(),
                    self.radius_var.get(),
                    self.scale_var.get(),
                )
            else:
                self.on_apply(
                    self.theme_var.get(),
                    self.bg_var.get(),
                    self.radius_var.get(),
                    self.scale_var.get(),
                    self.accent_var.get(),
                    self.weight_var.get(),
                    self.animations_var.get(),
                    self.hints_var.get(),
                )
        if callable(self.on_language_change) and self.language_var.get() != self.initial_language:
            self.on_language_change(self.language_var.get())
        self._close()
