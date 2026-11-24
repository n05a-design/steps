"""
Appearance & Customization Modal Dialog for STEPS (Glide parity).

Provides interactive customization of:
- Theme (System, Dark, Light, Glass-Dark, Glass-Light, Dopamine, Contrast-Dark, Contrast-Light, Minimal-Dark, Minimal-Light, Pixel)
- Accent Color (Lila, Blau, Türkis, Grün, Gelb, Rot, Braun, Kontrastgrau)
- Background Tint (Default, Surface, Accent, Clear, Due Action, Export, Flag, Delete, Import, Muted)
- Corner Radius (Large 18px, Standard 12px, Subtle 6px, Flat 0px)
- Font Scaling (Compact 90%, Standard 100%, Large 115%)
- Font Weight (Auto, Standard, Bold)
- Animations & Hints toggles
Includes a real-time live preview using RoundedSurfaceCard and RoundedButton.
"""

from __future__ import annotations

import inspect
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

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
from glide_shell.custom_controls import ThemedAutoScrollbar


class AppearanceDialog(ModalDialog):
    """Modal dialog for configuring application appearance, geometry, and styling."""

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
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.i18n = i18n
        self.on_apply = on_apply

        self.initial_theme_preference = theme_preference
        self.initial_background = theme.background_choice
        self.initial_accent = getattr(theme, "accent_choice", "accent")
        self.initial_radius = theme.radius_choice
        self.initial_scale = theme.font_scale_choice
        self.initial_weight = getattr(theme, "font_weight_choice", "standard")
        self.initial_animations = getattr(theme, "animations_enabled", True)
        self.initial_hints = getattr(theme, "hints_visible", True)

        self.theme_var = tk.StringVar(value=theme_preference)
        self.bg_var = tk.StringVar(value=self.initial_background)
        self.accent_var = tk.StringVar(value=self.initial_accent)
        self.radius_var = tk.StringVar(value=self.initial_radius)
        self.scale_var = tk.StringVar(value=self.initial_scale)
        self.weight_var = tk.StringVar(value=self.initial_weight)
        self.animations_var = tk.BooleanVar(value=self.initial_animations)
        self.hints_var = tk.BooleanVar(value=self.initial_hints)

        t = self.i18n.translate
        self.window.title(t("appearance.dialog.title"))
        apply_window_geometry(self.window, 760, 720, 640, 580)
        self.window.configure(bg=theme.colors.bg_window)

        self._build_ui()
        self._update_preview()
        self._show(self.apply_btn)

    def _build_ui(self) -> None:
        t = self.i18n.translate
        c = self.theme.colors

        # Main vertically arranged container
        self.content_frame = tk.Frame(self.window, bg=c.bg_window, padx=16, pady=16)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Header title
        self.header_lbl = tk.Label(
            self.content_frame,
            text=t("appearance.dialog.heading"),
            font=self.theme.font_spec(self.theme.typography.size_lg, "bold"),
            bg=c.bg_window,
            fg=c.text_primary,
            anchor="w",
        )
        self.header_lbl.pack(fill=tk.X, pady=(0, 10))

        # Canvas with scrollbar for options
        canvas_container = tk.Frame(self.content_frame, bg=c.bg_window)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(
            canvas_container,
            bg=c.bg_window,
            bd=0,
            highlightthickness=0,
        )
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

        def _on_canvas_configure(event: tk.Event) -> None:
            self.scroll_canvas.itemconfig(body_window, width=event.width)

        self.scroll_canvas.bind("<Configure>", _on_canvas_configure)
        body.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        # Two-column layout: Left = Themes & Backgrounds, Right = Accents, Radii, Typography & Preview
        left_pane = tk.Frame(body, bg=c.bg_window)
        left_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_pane = tk.Frame(body, bg=c.bg_window)
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Theme selection section
        self._build_radio_section(
            left_pane,
            t("theme.menu"),
            self.THEME_OPTIONS,
            self.theme_var,
        )

        # 2. Background tint section
        self._build_radio_section(
            left_pane,
            t("theme.background.label"),
            BACKGROUND_CHOICES,
            self.bg_var,
        )

        # 3. Accent color section
        self._build_radio_section(
            right_pane,
            t("theme.accent.label"),
            ACCENT_CHOICES,
            self.accent_var,
        )

        # 4. Corner radius section
        radius_opts = [(k, label) for k, label, _ in RADIUS_CHOICES]
        self._build_radio_section(
            right_pane,
            t("theme.radius.label"),
            radius_opts,
            self.radius_var,
        )

        # 5. Font scale section
        scale_opts = [(k, label) for k, label, _ in FONT_SCALE_CHOICES]
        self._build_radio_section(
            right_pane,
            t("theme.font_scale.label"),
            scale_opts,
            self.scale_var,
        )

        # 6. Font weight section
        self._build_radio_section(
            right_pane,
            t("theme.font_weight.label"),
            FONT_WEIGHT_CHOICES,
            self.weight_var,
        )

        # 7. Behavior & Animation toggles
        behavior_card = RoundedSurfaceCard(
            right_pane,
            bg_color=c.bg_window,
            fill_color=c.bg_surface,
            outline_color=c.border,
            radius=8,
            padding=8,
            auto_height=True,
        )
        behavior_card.pack(fill=tk.X, pady=(0, 8))

        b_title = tk.Label(
            behavior_card.inner,
            text=t("settings.behavior"),
            font=self.theme.font_spec(self.theme.typography.size_xs, "bold"),
            bg=c.bg_surface,
            fg=c.text_secondary,
            anchor="w",
        )
        b_title.pack(fill=tk.X, pady=(0, 4))

        anim_cb = tk.Checkbutton(
            behavior_card.inner,
            text=t("settings.animations"),
            variable=self.animations_var,
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
        anim_cb.pack(fill=tk.X, pady=2)

        hints_cb = tk.Checkbutton(
            behavior_card.inner,
            text=t("settings.hints"),
            variable=self.hints_var,
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
        hints_cb.pack(fill=tk.X, pady=2)

        # 8. Live preview area
        preview_label = tk.Label(
            right_pane,
            text=t("appearance.dialog.preview_title"),
            font=self.theme.font_spec(self.theme.typography.size_sm, "bold"),
            bg=c.bg_window,
            fg=c.text_secondary,
            anchor="w",
        )
        preview_label.pack(fill=tk.X, pady=(10, 4))

        self.preview_window_frame = tk.Frame(right_pane, bg=c.bg_window, padx=8, pady=8)
        self.preview_window_frame.pack(fill=tk.X, pady=(0, 8))

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
        self.preview_btn.pack(anchor="w", pady=(0, 4))

        # Bottom action bar
        action_bar = tk.Frame(self.window, bg=c.bg_window, padx=16, pady=12)
        action_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.cancel_btn = create_button(
            action_bar,
            text=t("appearance.dialog.cancel"),
            command=self._close,
            bg=c.bg_surface,
            fg=c.text_secondary,
            hover_bg=c.bg_surface_hover,
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=(8, 0))

        self.apply_btn = create_button(
            action_bar,
            text=t("appearance.dialog.apply"),
            command=self._on_apply_clicked,
            bg=c.harmonic_tonic,
            fg=c.text_inverted,
            hover_bg=c.border_focus,
        )
        self.apply_btn.pack(side=tk.RIGHT)

    def _build_radio_section(
        self,
        parent: tk.Misc,
        title: str,
        options: list[tuple[str, str]] | tuple[tuple[str, str], ...],
        variable: tk.StringVar,
    ) -> None:
        t = self.i18n.translate
        c = self.theme.colors

        sec_card = RoundedSurfaceCard(
            parent,
            bg_color=c.bg_window,
            fill_color=c.bg_surface,
            outline_color=c.border,
            radius=8,
            padding=8,
            auto_height=True,
        )
        sec_card.pack(fill=tk.X, pady=(0, 8))

        title_lbl = tk.Label(
            sec_card.inner,
            text=title,
            font=self.theme.font_spec(self.theme.typography.size_xs, "bold"),
            bg=c.bg_surface,
            fg=c.text_secondary,
            anchor="w",
        )
        title_lbl.pack(fill=tk.X, pady=(0, 4))

        for key, text_key in options:
            radio = tk.Radiobutton(
                sec_card.inner,
                text=t(text_key),
                value=key,
                variable=variable,
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
            radio.pack(fill=tk.X, pady=1)

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
        self._close()
