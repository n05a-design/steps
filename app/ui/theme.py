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


def hex_rgb(value: str) -> tuple[int, int, int]:
    """Convert hex string '#RRGGBB' to RGB 3-tuple."""
    text = str(value).lstrip("#")
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_hex(rgb: tuple[float, float, float] | tuple[int, int, int]) -> str:
    """Format RGB 3-tuple as '#RRGGBB'."""
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def _linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate WCAG 2.1 relative luminance for an RGB tuple."""
    r, g, b = (_linear(float(c)) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mix(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    share: float,
) -> tuple[float, float, float]:
    """Linear color blend between two RGB tuples."""
    return tuple(a + (b - a) * share for a, b in zip(first, second))  # type: ignore[return-value]


def contrast(first_hex: str, second_hex: str) -> float:
    """Compute WCAG contrast ratio between two hex colors."""
    l1 = luminance(hex_rgb(first_hex))
    l2 = luminance(hex_rgb(second_hex))
    high, low = max(l1, l2), min(l1, l2)
    return (high + 0.05) / (low + 0.05)


BACKGROUND_CHOICES: tuple[tuple[str, str], ...] = (
    ("default", "theme.background.default"),
    ("surface", "theme.background.surface"),
    ("accent", "theme.background.accent"),
    ("clear", "theme.background.clear"),
    ("due_action", "theme.background.due_action"),
    ("export", "theme.background.export"),
    ("flag", "theme.background.flag"),
    ("delete", "theme.background.delete"),
    ("muted", "theme.background.muted"),
)
BACKGROUND_KEYS: frozenset[str] = frozenset(key for key, _ in BACKGROUND_CHOICES)

RADIUS_CHOICES: tuple[tuple[str, str, int], ...] = (
    ("standard", "theme.radius.standard", 12),
    ("large", "theme.radius.large", 18),
    ("subtle", "theme.radius.subtle", 6),
    ("flat", "theme.radius.flat", 0),
)
RADIUS_MAP: dict[str, int] = {key: radius for key, _, radius in RADIUS_CHOICES}

FONT_SCALE_CHOICES: tuple[tuple[str, str, float], ...] = (
    ("compact", "theme.font_scale.compact", 0.90),
    ("standard", "theme.font_scale.standard", 1.00),
    ("large", "theme.font_scale.large", 1.15),
)
FONT_SCALE_MAP: dict[str, float] = {key: scale for key, _, scale in FONT_SCALE_CHOICES}


def with_background(colors: "ThemeColors", choice: str) -> "ThemeColors":
    """Tint the background color while preserving surfaces and role colors (Glide appearance contract)."""
    if choice not in BACKGROUND_KEYS or choice == "default":
        return colors
    if choice == "surface":
        return ThemeColors(
            bg_window=colors.bg_surface,
            bg_surface=colors.bg_surface,
            bg_surface_hover=colors.bg_surface_hover,
            bg_active=colors.bg_active,
            border=colors.border,
            border_focus=colors.border_focus,
            text_primary=colors.text_primary,
            text_secondary=colors.text_secondary,
            text_muted=colors.text_muted,
            text_inverted=colors.text_inverted,
            harmonic_tonic=colors.harmonic_tonic,
            harmonic_subdominant=colors.harmonic_subdominant,
            harmonic_dominant=colors.harmonic_dominant,
            harmonic_altered=colors.harmonic_altered,
            harmonic_minor=colors.harmonic_minor,
            selection=colors.selection,
            selection_text=colors.selection_text,
            delete=colors.delete,
            export=colors.export,
            clear=colors.clear,
            flag=colors.flag,
        )

    tint_map = {
        "accent": colors.harmonic_altered,
        "clear": colors.clear or colors.harmonic_tonic,
        "due_action": colors.harmonic_minor,
        "export": colors.export or colors.harmonic_subdominant,
        "flag": colors.flag,
        "delete": colors.delete or colors.harmonic_dominant,
        "muted": colors.text_muted,
    }
    tint_hex = tint_map.get(choice)
    if not tint_hex:
        return colors

    base = hex_rgb(colors.bg_window)
    tint = hex_rgb(tint_hex)
    share = 0.16 if luminance(base) < 0.2 else 0.08
    tinted_bg = rgb_hex(mix(base, tint, share))

    return ThemeColors(
        bg_window=tinted_bg,
        bg_surface=colors.bg_surface,
        bg_surface_hover=colors.bg_surface_hover,
        bg_active=colors.bg_active,
        border=colors.border,
        border_focus=colors.border_focus,
        text_primary=colors.text_primary,
        text_secondary=colors.text_secondary,
        text_muted=colors.text_muted,
        text_inverted=colors.text_inverted,
        harmonic_tonic=colors.harmonic_tonic,
        harmonic_subdominant=colors.harmonic_subdominant,
        harmonic_dominant=colors.harmonic_dominant,
        harmonic_altered=colors.harmonic_altered,
        harmonic_minor=colors.harmonic_minor,
        selection=colors.selection,
        selection_text=colors.selection_text,
        delete=colors.delete,
        export=colors.export,
        clear=colors.clear,
        flag=colors.flag,
    )


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


def create_button(parent: tk.Misc, **options) -> tk.Button | ttk.Button | "object":
    """Create a Glide-styled button with hover/active tracking on classic Tk, native Aqua, or rounded canvas."""
    import tkinter as tk
    from tkinter import ttk

    hover_bg = options.pop("hover_bg", None)
    active_bg = options.pop("active_bg", None)
    active_fg = options.pop("active_fg", None)
    rounded = options.pop("rounded", False)

    if rounded:
        from app.ui.custom_widgets import RoundedButton

        text = options.pop("text", "")
        cmd = options.pop("command", None)
        bg = options.pop("bg", options.pop("bg_color", "#121319"))
        fg = options.pop("fg", options.pop("base_fg", "#F3F1ED"))
        base_bg = options.pop("base_bg", bg)
        radius = options.pop("radius", 10)
        return RoundedButton(
            parent,
            text=text,
            command=cmd,
            bg_color=bg,
            base_bg=base_bg,
            base_fg=fg,
            hover_bg=hover_bg,
            active_bg=active_bg,
            active_fg=active_fg,
            radius=radius,
            **options,
        )

    if parent.tk.call("tk", "windowingsystem") == "aqua":
        for option in ("bg", "fg", "relief", "padx", "pady", "anchor", "highlightthickness", "bd"):
            options.pop(option, None)
        btn = ttk.Button(parent, **options)
        setattr(btn, "_glide_is_active", False)
        return btn

    base_bg = options.get("bg")
    base_fg = options.get("fg")
    if hover_bg and "activebackground" not in options:
        options["activebackground"] = hover_bg
    if base_fg and "activeforeground" not in options:
        options["activeforeground"] = base_fg
    options.setdefault("bd", 0)
    options.setdefault("highlightthickness", 1)

    btn = tk.Button(parent, **options)
    setattr(btn, "_glide_base_bg", base_bg)
    setattr(btn, "_glide_base_fg", base_fg)
    setattr(btn, "_glide_hover_bg", hover_bg)
    setattr(btn, "_glide_active_bg", active_bg)
    setattr(btn, "_glide_active_fg", active_fg)
    setattr(btn, "_glide_is_active", False)

    def _on_enter(_event: tk.Event) -> None:
        if getattr(btn, "_glide_is_active", False):
            return
        try:
            if str(btn.cget("state")) == tk.DISABLED:
                return
            hover = getattr(btn, "_glide_hover_bg", None)
            if hover:
                btn.configure(bg=hover)
        except Exception:
            pass

    def _on_leave(_event: tk.Event) -> None:
        if getattr(btn, "_glide_is_active", False):
            return
        try:
            base = getattr(btn, "_glide_base_bg", None)
            if base:
                btn.configure(bg=base)
        except Exception:
            pass

    btn.bind("<Enter>", _on_enter, add="+")
    btn.bind("<Leave>", _on_leave, add="+")
    return btn


def set_button_active(button: object, active: bool, colors: "ThemeColors") -> None:
    """Apply or clear Glide active-button highlighting safely across Tk and mock widgets."""
    is_active = bool(active)
    if hasattr(button, "set_active") and callable(getattr(button, "set_active")):
        button.set_active(is_active)
        return
    try:
        setattr(button, "_glide_is_active", is_active)
    except Exception:
        pass
    try:
        windowing = button.tk.call("tk", "windowingsystem")  # type: ignore[attr-defined]
    except Exception:
        windowing = ""
    if windowing == "aqua":
        # Native ttk.Button does not accept classic bg/fg; expose state cleanly for accessibility.
        return
    base_bg = getattr(button, "_glide_base_bg", colors.bg_active) or colors.bg_active
    base_fg = getattr(button, "_glide_base_fg", colors.text_primary) or colors.text_primary
    active_bg = getattr(button, "_glide_active_bg", None) or colors.harmonic_tonic
    active_fg = getattr(button, "_glide_active_fg", None) or colors.text_inverted
    target_bg = active_bg if is_active else base_bg
    target_fg = active_fg if is_active else base_fg
    try:
        button.configure(bg=target_bg, fg=target_fg)  # type: ignore[attr-defined]
    except Exception:
        pass


def retheme_button(
    button: object,
    colors: "ThemeColors",
    *,
    base_bg: str,
    base_fg: str,
    hover_bg: Optional[str] = None,
    active_bg: Optional[str] = None,
    active_fg: Optional[str] = None,
) -> None:
    """Update a Glide-styled button's palette tokens when switching Dark/Light themes."""
    if hasattr(button, "set_theme") and callable(getattr(button, "set_theme")):
        button.set_theme(
            bg_color=colors.bg_window,
            base_bg=base_bg,
            base_fg=base_fg,
            hover_bg=hover_bg or colors.bg_surface_hover,
            active_bg=active_bg or colors.harmonic_tonic,
            active_fg=active_fg or colors.text_inverted,
            border_color=colors.border,
        )
        return
    for attr, value in (
        ("_glide_base_bg", base_bg),
        ("_glide_base_fg", base_fg),
        ("_glide_hover_bg", hover_bg or colors.bg_surface_hover),
        ("_glide_active_bg", active_bg),
        ("_glide_active_fg", active_fg),
    ):
        try:
            setattr(button, attr, value)
        except Exception:
            pass
    try:
        windowing = button.tk.call("tk", "windowingsystem")  # type: ignore[attr-defined]
    except Exception:
        windowing = ""
    if windowing == "aqua":
        return
    try:
        button.configure(  # type: ignore[attr-defined]
            activebackground=hover_bg or colors.bg_surface_hover,
            activeforeground=base_fg,
            highlightbackground=colors.bg_surface,
            highlightcolor=colors.border_focus,
        )
    except Exception:
        pass
    set_button_active(button, bool(getattr(button, "_glide_is_active", False)), colors)


def style_surface_card(frame: "tk.Frame", colors: "ThemeColors") -> None:
    """Apply calm Glide carrier-card surface styling with subtle 1px border (B17/B19)."""
    import tkinter as tk

    frame.configure(
        bg=colors.bg_surface,
        bd=0,
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=colors.border,
        highlightcolor=colors.border,
    )


def style_entry(entry: "tk.Entry", colors: "ThemeColors") -> None:
    """Apply clean 1px-contoured Glide input-field styling against carrier cards (B17/B19)."""
    import tkinter as tk

    entry.configure(
        bg=colors.bg_window,
        fg=colors.text_primary,
        insertbackground=colors.text_primary,
        selectbackground=colors.harmonic_tonic,
        selectforeground=colors.text_inverted,
        relief=tk.FLAT,
        bd=0,
        highlightthickness=1,
        highlightbackground=colors.border,
        highlightcolor=colors.border_focus,
    )


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
    selection: str = ""
    selection_text: str = ""
    delete: str = ""
    export: str = ""
    clear: str = ""
    flag: str = ""


ThemeName = Literal[
    "dark",
    "light",
    "contrast-dark",
    "contrast-light",
    "minimal-dark",
    "minimal-light",
]


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
    """Manages design tokens and active theme state across 6 Glide themes and system mode."""

    THEMES: tuple[str, ...] = (
        "dark",
        "light",
        "contrast-dark",
        "contrast-light",
        "minimal-dark",
        "minimal-light",
    )
    THEME_PAIRS: dict[str, dict[str, str]] = {
        "dark": {"light": "light", "dark": "dark"},
        "light": {"light": "light", "dark": "dark"},
        "contrast-dark": {"light": "contrast-light", "dark": "contrast-dark"},
        "contrast-light": {"light": "contrast-light", "dark": "contrast-dark"},
        "minimal-dark": {"light": "minimal-light", "dark": "minimal-dark"},
        "minimal-light": {"light": "minimal-light", "dark": "minimal-dark"},
    }

    @staticmethod
    def normalize_theme_name(name: str) -> str:
        """Normalize theme aliases like contrast_dark or cvd-dark to canonical contrast-dark."""
        norm = str(name).strip().lower().replace("_", "-")
        if norm in ("high-contrast-dark", "cvd-dark"):
            return "contrast-dark"
        if norm in ("high-contrast-light", "cvd-light"):
            return "contrast-light"
        return norm

    def __init__(self, mode: str = "dark", tokens_path: Path = TOKENS_PATH) -> None:
        self._tokens_path = tokens_path
        self._raw = self._load_tokens(tokens_path)
        self._mode: str = self.normalize_theme_name(mode)
        if self._mode not in self.THEMES:
            raise ValueError(f"Invalid theme mode '{mode}', expected one of {self.THEMES}")
        self._background_choice: str = "default"
        self._radius_choice: str = "standard"
        self._font_scale_choice: str = "standard"
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
    def mode(self) -> str:
        return self._mode

    @property
    def is_dark(self) -> bool:
        return "dark" in self._mode

    def set_mode(self, mode: str) -> None:
        norm = self.normalize_theme_name(mode)
        if norm not in self.THEMES:
            raise ValueError(f"Invalid theme mode '{mode}', expected one of {self.THEMES}")
        self._mode = norm

    @property
    def background_choice(self) -> str:
        return self._background_choice

    def set_background_choice(self, choice: str) -> None:
        if choice not in BACKGROUND_KEYS:
            raise ValueError(f"Invalid background choice '{choice}', expected one of {tuple(BACKGROUND_KEYS)}")
        self._background_choice = choice

    @property
    def radius_choice(self) -> str:
        return self._radius_choice

    def set_radius_choice(self, choice: str) -> None:
        if choice not in RADIUS_MAP:
            raise ValueError(f"Invalid radius choice '{choice}', expected one of {tuple(RADIUS_MAP.keys())}")
        self._radius_choice = choice

    @property
    def corner_radius(self) -> int:
        return RADIUS_MAP.get(self._radius_choice, 12)

    @property
    def font_scale_choice(self) -> str:
        return self._font_scale_choice

    def set_font_scale_choice(self, choice: str) -> None:
        if choice not in FONT_SCALE_MAP:
            raise ValueError(f"Invalid font scale choice '{choice}', expected one of {tuple(FONT_SCALE_MAP.keys())}")
        self._font_scale_choice = choice

    @property
    def font_scale(self) -> float:
        return FONT_SCALE_MAP.get(self._font_scale_choice, 1.0)

    @property
    def colors(self) -> ThemeColors:
        raw_colors = self._raw["themes"][self._mode]
        base_colors = ThemeColors(**raw_colors)
        return with_background(base_colors, self._background_choice)

    @property
    def typography(self) -> TypographyTokens:
        return self._typography

    @property
    def spacing(self) -> SpacingTokens:
        return self._spacing

    @classmethod
    def pair_for(cls, theme: str) -> dict[str, str]:
        norm = cls.normalize_theme_name(theme)
        return cls.THEME_PAIRS.get(norm, {"light": "light", "dark": "dark"})

    def font_spec(self, size: Optional[int] = None, *styles: str, mono: bool = False) -> tuple:
        """Return a Tk font tuple derived from STEPS typography tokens, scaled by font_scale."""
        stack = self._typography.font_family_mono if mono else self._typography.font_family_sans
        family = _primary_font_family(stack, fallback="Courier" if mono else "Helvetica")
        raw_size = size if size is not None else self._typography.size_sm
        resolved_size = max(6, int(round(raw_size * self.font_scale)))
        return (family, resolved_size, *styles)

    def make_surface_card(
        self,
        master: "tk.Misc",
        radius: Optional[int] = None,
        padding: int = 6,
        inner_pad_x: Optional[int] = None,
        inner_pad_y: Optional[int] = None,
        auto_height: bool = False,
        **kwargs,
    ) -> "object":
        """Factory for Glide-styled rounded carrier cards."""
        from app.ui.custom_widgets import RoundedSurfaceCard

        r = self.corner_radius if radius is None else max(0, radius)
        return RoundedSurfaceCard(
            master,
            bg_color=self.colors.bg_window,
            fill_color=self.colors.bg_surface,
            outline_color=self.colors.border,
            radius=r,
            padding=padding,
            inner_pad_x=inner_pad_x,
            inner_pad_y=inner_pad_y,
            auto_height=auto_height,
            **kwargs,
        )

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

    @classmethod
    def resolve_system_mode(
        cls,
        root: Optional["tk.Misc"] = None,
        system_dark: Optional[bool] = None,
        fallback: str = "dark",
        preference: str = "dark",
    ) -> str:
        """Resolve theme variant from OS/Tk state via glide_shell.system_appearance."""
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
        target_pair = cls.pair_for(preference if preference != "system" else fallback)
        resolved_fallback = fallback if fallback in target_pair.values() else target_pair["dark"]
        return system_appearance.resolve(target_pair, detected, resolved_fallback)


# Global default instance
default_theme = ThemeManager(mode="dark")
