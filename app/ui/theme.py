"""
STEPS Desktop Application Theme & Design Tokens Manager (ADR-001 / Prompt 06).

Provides type-safe access to theme colors, typography and spacing tokens,
with runtime support for Light/Dark mode and WCAG 2.1 AA contrast compliance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Optional, TYPE_CHECKING

from glide_shell import custom_controls, system_appearance, text_fit, window_geometry

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk

TOKENS_PATH = Path(__file__).resolve().parents[2] / "design/tokens/tokens.json"


def _primary_font_family(font_stack: str, fallback: str = "Helvetica") -> str:
    for candidate in font_stack.split(","):
        cleaned = candidate.strip().strip("'\"")
        if cleaned and not cleaned.startswith("-") and cleaned.lower() not in {"sans-serif", "monospace"}:
            return cleaned
    return fallback


def apply_window_geometry(
    window: "tk.Misc",
    width: int,
    height: int,
    min_width: int,
    min_height: int,
) -> tuple[int, int]:
    """Clamp window dimensions to the screen via glide_shell.window_geometry (B15)."""
    try:
        screen_w = int(window.winfo_screenwidth())
        screen_h = int(window.winfo_screenheight())
    except Exception:
        screen_w, screen_h = 0, 0
    if screen_w > 0:
        effective_min_w = min(min_width, max(320, screen_w))
    else:
        effective_min_w = min_width
    if screen_h > 0:
        effective_min_h = min(min_height, max(240, screen_h - window_geometry.SCREEN_RESERVE))
    else:
        effective_min_h = min_height
    clamped_w, clamped_h, _, _ = window_geometry.clamp(
        width,
        height,
        None,
        None,
        screen_w,
        screen_h,
        (effective_min_w, effective_min_h),
    )
    window.geometry(window_geometry.format_geometry(clamped_w, clamped_h))
    window.minsize(effective_min_w, effective_min_h)
    return clamped_w, clamped_h


def fit_text(text: str, max_chars: int) -> str:
    """Shorten secondary text ergonomically via glide_shell.text_fit (B11)."""
    return text_fit.clip(text, max_chars)


def fit_text_px(text: str, measure: Callable[[str], int], max_width: int) -> str:
    """Shorten text to a pixel budget using glide_shell.text_fit (B11)."""
    return text_fit.fit(text, measure, max_width)


def create_button(parent: tk.Misc, **options) -> tk.Button | ttk.Button:
    """Use the native Aqua palette where Tk ignores classic button backgrounds."""
    import tkinter as tk
    from tkinter import ttk

    if parent.tk.call("tk", "windowingsystem") == "aqua":
        for option in ("bg", "fg", "relief", "padx", "pady", "anchor"):
            options.pop(option, None)
        return ttk.Button(parent, **options)
    return tk.Button(parent, **options)


@dataclass(frozen=True)
class ThemeColors:
    bg_window: str
    bg_surface: str
    bg_surface_hover: str
    bg_active: str
    border: str
    border_focus: str
    text_primary: str
    text_secondary: str
    text_muted: str
    text_inverted: str
    harmonic_tonic: str
    harmonic_subdominant: str
    harmonic_dominant: str
    harmonic_altered: str
    harmonic_minor: str


@dataclass(frozen=True)
class TypographyTokens:
    font_family_sans: str
    font_family_mono: str
    size_xs: int
    size_sm: int
    size_md: int
    size_lg: int
    size_xl: int
    size_title: int


@dataclass(frozen=True)
class SpacingTokens:
    xs: int
    sm: int
    md: int
    lg: int
    xl: int
    radius_sm: int
    radius_md: int


class ThemeManager:
    """Manages design tokens and active theme state."""

    def __init__(self, mode: Literal["dark", "light"] = "dark", tokens_path: Path = TOKENS_PATH) -> None:
        self._mode: Literal["dark", "light"] = mode
        self._tokens_path = tokens_path
        self._raw = self._load_tokens(tokens_path)
        self._typography = self._parse_typography()
        self._spacing = self._parse_spacing()

    def _load_tokens(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Tokens file not found at {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _parse_typography(self) -> TypographyTokens:
        raw_typo = self._raw["typography"]
        sizes = raw_typo["sizes"]
        return TypographyTokens(
            font_family_sans=raw_typo["font_family_sans"],
            font_family_mono=raw_typo["font_family_mono"],
            size_xs=sizes["xs"],
            size_sm=sizes["sm"],
            size_md=sizes["md"],
            size_lg=sizes["lg"],
            size_xl=sizes["xl"],
            size_title=sizes["title"],
        )

    def _parse_spacing(self) -> SpacingTokens:
        raw_sp = self._raw["spacing"]
        return SpacingTokens(
            xs=raw_sp["xs"],
            sm=raw_sp["sm"],
            md=raw_sp["md"],
            lg=raw_sp["lg"],
            xl=raw_sp["xl"],
            radius_sm=raw_sp["radius_sm"],
            radius_md=raw_sp["radius_md"],
        )

    @property
    def mode(self) -> Literal["dark", "light"]:
        return self._mode

    def set_mode(self, mode: Literal["dark", "light"]) -> None:
        if mode not in ("dark", "light"):
            raise ValueError(f"Invalid theme mode '{mode}', expected 'dark' or 'light'")
        self._mode = mode

    @property
    def colors(self) -> ThemeColors:
        raw_colors = self._raw["themes"][self._mode]
        return ThemeColors(**raw_colors)

    @property
    def typography(self) -> TypographyTokens:
        return self._typography

    @property
    def spacing(self) -> SpacingTokens:
        return self._spacing

    def font_spec(self, size: Optional[int] = None, *styles: str, mono: bool = False) -> tuple:
        """Return a Tk font tuple derived from STEPS typography tokens."""
        stack = self._typography.font_family_mono if mono else self._typography.font_family_sans
        family = _primary_font_family(stack, fallback="Courier" if mono else "Helvetica")
        resolved_size = int(size if size is not None else self._typography.size_sm)
        return (family, resolved_size, *styles)

    def configure_shell_providers(self, root: Optional["tk.Misc"] = None) -> None:
        """Bind STEPS font tokens into glide_shell.custom_controls with host/root isolation."""
        def _font_provider(size: int = 10, *styles: str) -> tuple:
            return self.font_spec(size, *styles)

        custom_controls.set_font_provider(_font_provider)
        if root is not None:
            try:
                setattr(root, "_font_provider", _font_provider)
            except Exception:
                pass

    @staticmethod
    def resolve_system_mode(
        root: Optional["tk.Misc"] = None,
        system_dark: Optional[bool] = None,
        fallback: Literal["dark", "light"] = "dark",
    ) -> Literal["dark", "light"]:
        """Resolve light/dark mode from OS/Tk state via glide_shell.system_appearance."""
        detected = system_dark
        if detected is None and root is not None:
            try:
                if root.tk.call("tk", "windowingsystem") == "aqua":
                    answer = root.tk.call("tk::unsupported::MacWindowStyle", "isdark", root)
                    detected = system_appearance.tk_is_dark(answer)
                else:
                    answer = root.tk.call("winfo", "isdark", root)
                    detected = system_appearance.tk_is_dark(answer)
            except Exception:
                detected = None
        return system_appearance.resolve({"light": "light", "dark": "dark"}, detected, fallback)


# Global default instance
default_theme = ThemeManager(mode="dark")
