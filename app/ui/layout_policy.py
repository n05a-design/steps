"""Responsive breakpoints, sidebar modes, and compact-mode geometry for STEPS."""

from __future__ import annotations

from typing import Callable, Literal

from glide_shell import text_fit, window_geometry

NORMAL_MIN = (860, 600)
COMPACT_MIN = (480, 560)
COMPACT_DEFAULT_WIDTH = 520
COMPACT_DEFAULT_HEIGHT = 680
SIDEBAR_WIDE_WIDTH = 196
SIDEBAR_RAIL_WIDTH = 64

HEADER_DENSITY_FULL = 1120
HEADER_DENSITY_COMPACT = 900
HEIGHT_DENSITY_FULL = 850
HEIGHT_DENSITY_COMPACT = 780

# Glide design scales & limits (DESIGN_RICHTLINIEN.md B11, D63, D67, D84, D98)
FONT_SIZES: dict[str, int] = {
    "caption": 9,
    "source": 9,
    "body": 12,
    "section": 16,
    "title": 22,
}
ROW_HEIGHT = 36
RADII: dict[str, int] = {
    "card": 18,
    "field": 16,
}
TITLE_MAX_CHARS = 40
BUTTON_TEXT_MAX_CHARS = 24
SYMBOLS: dict[str, str] = {
    "play": "▸",
    "down": "▾",
    "up": "▴",
    "left": "◂",
    "menu": "☰",
    "collapse": "«",
    "expand": "»",
}

SidebarMode = Literal["wide", "rail", "hidden"]
DensityTier = Literal["full", "compact", "minimal"]


def clip_title(text: str, limit: int = TITLE_MAX_CHARS) -> str:
    """Clip a title to the Glide D67 maximum character budget via glide_shell.text_fit."""
    return text_fit.clip(text, limit)


def clip_button_text(text: str, limit: int = BUTTON_TEXT_MAX_CHARS) -> str:
    """Clip a button label to the Glide D63 maximum character budget via glide_shell.text_fit."""
    return text_fit.clip(text, limit)


def remaining_chars_text(length: int, limit: int = TITLE_MAX_CHARS) -> str:
    """Format the remaining character counter matching Glide D67."""
    return f"{max(0, limit - length)}/{limit}"


def aligned_menu_markers(measure: Callable[[str], int]) -> dict[str, str]:
    """Return hairline-padded check markers ('✓', '□') with equal pixel width (D71/B02)."""
    return text_fit.aligned_markers(("✓", "□"), measure)


def header_density(width: int) -> DensityTier:
    """Determine horizontal density tier from window or header width."""
    if width <= 1 or width >= HEADER_DENSITY_FULL:
        return "full"
    if width >= HEADER_DENSITY_COMPACT:
        return "compact"
    return "minimal"


def height_density(height: int) -> DensityTier:
    """Determine vertical density tier from window height."""
    if height <= 1 or height >= HEIGHT_DENSITY_FULL:
        return "full"
    if height >= HEIGHT_DENSITY_COMPACT:
        return "compact"
    return "minimal"


def effective_sidebar_mode(
    visible: bool,
    narrow: bool,
    compact: bool,
    window_width: int = 0,
) -> SidebarMode:
    """Compute effective sidebar mode respecting compact mode and narrow breakpoints."""
    if compact or not visible:
        return "hidden"
    if narrow or (1 < window_width < HEADER_DENSITY_COMPACT):
        return "rail"
    return "wide"


def compact_geometry(
    normal_geom: str,
    saved_compact: str,
    screen_width: int,
    screen_height: int,
    origin: tuple[int, int] = (0, 0),
) -> str:
    """Compute clamped window geometry when entering compact mode."""
    remembered = window_geometry.parse(saved_compact)
    if remembered is not None and remembered[0] >= COMPACT_MIN[0] and remembered[1] >= COMPACT_MIN[1]:
        return window_geometry.format_geometry(
            *window_geometry.clamp(
                *remembered, screen_width, screen_height, COMPACT_MIN, origin=origin
            )
        )
    current = window_geometry.parse(normal_geom)
    if current is None:
        return window_geometry.format_geometry(
            *window_geometry.clamp(
                COMPACT_DEFAULT_WIDTH,
                COMPACT_DEFAULT_HEIGHT,
                None,
                None,
                screen_width,
                screen_height,
                COMPACT_MIN,
                origin=origin,
            )
        )
    width, height, x, y = current
    new_width = COMPACT_DEFAULT_WIDTH
    new_height = max(COMPACT_MIN[1], height)
    new_x = None if x is None else x + width - new_width
    return window_geometry.format_geometry(
        *window_geometry.clamp(
            new_width, new_height, new_x, y, screen_width, screen_height, COMPACT_MIN, origin=origin
        )
    )


def normal_geometry(remembered: str, current: str) -> str:
    """Restore previous normal window geometry when leaving compact mode."""
    parsed = window_geometry.parse(remembered) or window_geometry.parse(current)
    if parsed is None:
        return window_geometry.format_geometry(1024, 720)
    width, height, x, y = parsed
    return window_geometry.format_geometry(
        max(NORMAL_MIN[0], width),
        max(NORMAL_MIN[1], height),
        x,
        y,
    )
