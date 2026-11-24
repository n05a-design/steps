"""
STEPS Desktop Application User Settings & Preferences Persistence.

Adheres to Glide Shell architectural rules:
- WA-49: Safe imports with zero side-effects (no directory creation or file I/O upon import).
- WA-50: Clean, modular, well-budgeted functions under 50 lines.
- Safe atomic persistence via temporary file and atomic replace.
- Environment override via STEPS_DATA_DIR for isolated testing without altering user data.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

from glide_shell import runtime_paths

APP_NAME = "STEPS"
SETTINGS_FILENAME = "settings.json"
ENV_DATA_DIR = "STEPS_DATA_DIR"

DEFAULT_SETTINGS: dict[str, Any] = {
    "theme_preference": "dark",
    "background_color": "default",
    "accent_color": "accent",
    "corner_radius": "standard",
    "font_scale": "standard",
    "font_weight": "standard",
    "animations_enabled": True,
    "hints_visible": True,
    "language": "system",
    "window_geometry": "",
    "saved_compact_geometry": "",
}

VALID_THEMES = frozenset({
    "system",
    "dark",
    "light",
    "glass-dark",
    "glass-light",
    "dopamine",
    "pixel",
    "contrast-dark",
    "contrast-light",
    "minimal-dark",
    "minimal-light",
})

VALID_BACKGROUNDS = frozenset({
    "default",
    "surface",
    "accent",
    "clear",
    "due_action",
    "export",
    "flag",
    "delete",
    "import",
    "muted",
})

VALID_ACCENTS = frozenset({
    "accent",
    "clear",
    "due_action",
    "export",
    "flag",
    "delete",
    "import",
    "muted",
})

VALID_RADII = frozenset({"large", "standard", "subtle", "flat"})
VALID_SCALES = frozenset({"compact", "standard", "large"})
VALID_WEIGHTS = frozenset({"auto", "standard", "bold"})
VALID_LANGUAGES = frozenset({"system", "de", "en"})


def resolve_settings_dir(base_dir: str | Path | None = None) -> Path:
    """Resolve directory for user settings without creating it."""
    if base_dir is not None:
        return Path(base_dir).resolve()
    resolved, _ = runtime_paths.resolve_base(
        None,
        os.environ,
        ENV_DATA_DIR,
        runtime_paths.platform_data_dir(APP_NAME),
    )
    return Path(resolved).resolve()


def get_settings_file(base_dir: str | Path | None = None) -> Path:
    """Return absolute path to settings.json without creating files."""
    return resolve_settings_dir(base_dir) / SETTINGS_FILENAME


def normalize_settings(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate and normalize settings dictionary against canonical defaults."""
    data = dict(raw) if isinstance(raw, Mapping) else {}
    result = dict(DEFAULT_SETTINGS)

    theme = str(data.get("theme_preference", "")).strip().lower().replace("_", "-")
    if theme in VALID_THEMES:
        result["theme_preference"] = theme

    bg = str(data.get("background_color", "")).strip().lower()
    if bg in VALID_BACKGROUNDS:
        result["background_color"] = bg

    accent = str(data.get("accent_color", "")).strip().lower()
    if accent in VALID_ACCENTS:
        result["accent_color"] = accent

    radius = str(data.get("corner_radius", "")).strip().lower()
    if radius in VALID_RADII:
        result["corner_radius"] = radius

    scale = str(data.get("font_scale", "")).strip().lower()
    if scale in VALID_SCALES:
        result["font_scale"] = scale

    weight = str(data.get("font_weight", "")).strip().lower()
    if weight in VALID_WEIGHTS:
        result["font_weight"] = weight

    if "animations_enabled" in data:
        result["animations_enabled"] = bool(data["animations_enabled"])

    if "hints_visible" in data:
        result["hints_visible"] = bool(data["hints_visible"])

    lang = str(data.get("language", "")).strip().lower()
    if lang in VALID_LANGUAGES:
        result["language"] = lang

    geom = str(data.get("window_geometry", "")).strip()
    if geom:
        result["window_geometry"] = geom

    compact_geom = str(data.get("saved_compact_geometry", "")).strip()
    if compact_geom:
        result["saved_compact_geometry"] = compact_geom

    return result


def load_settings(base_dir: str | Path | None = None) -> dict[str, Any]:
    """Load settings from JSON file; returns normalized defaults if missing or invalid."""
    filepath = get_settings_file(base_dir)
    if not filepath.is_file():
        return dict(DEFAULT_SETTINGS)
    try:
        raw_text = filepath.read_text(encoding="utf-8-sig")
        parsed = json.loads(raw_text)
        return normalize_settings(parsed)
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: Mapping[str, Any], base_dir: str | Path | None = None) -> bool:
    """Atomically write normalized settings to settings.json via temporary file."""
    normalized = normalize_settings(settings)
    target_path = get_settings_file(base_dir)
    target_dir = target_path.parent

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        content = json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
        fd, tmp_path_str = tempfile.mkstemp(
            prefix="steps_settings_",
            suffix=".tmp",
            dir=str(target_dir),
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path_str, str(target_path))
        return True
    except Exception:
        return False
