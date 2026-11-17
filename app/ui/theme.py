"""
STEPS Desktop Application Theme & Design Tokens Manager (ADR-001 / Prompt 06).

Provides type-safe access to theme colors, typography and spacing tokens,
with runtime support for Light/Dark mode and WCAG 2.1 AA contrast compliance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

TOKENS_PATH = Path(__file__).resolve().parents[2] / "design/tokens/tokens.json"


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


# Global default instance
default_theme = ThemeManager(mode="dark")
