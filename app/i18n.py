"""Localized interface strings and independent UI-language preferences."""

from __future__ import annotations

import json
import locale
import logging
import os
from pathlib import Path
import sys
import tempfile
from typing import Literal

from importlib.resources import files

LanguagePreference = Literal["system", "en", "de"]
SUPPORTED_LANGUAGES = ("system", "en", "de")
logger = logging.getLogger(__name__)


def preference_path(
    *,
    platform: str | None = None,
    environ: dict[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    """Return the per-user settings path without relying on third-party packages."""
    platform = platform or sys.platform
    env = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    if platform == "nt" or platform.startswith("win"):
        root = Path(env.get("APPDATA") or home / "AppData/Roaming")
        return root / "STEPS" / "preferences.json"
    if platform == "darwin":
        return home / "Library" / "Application Support" / "STEPS" / "preferences.json"
    root = Path(env.get("XDG_CONFIG_HOME") or home / ".config")
    return root / "steps" / "preferences.json"


def detect_system_locale(environ: dict[str, str] | None = None) -> str:
    """Resolve the OS locale from standard environment overrides, then Python locale."""
    env = os.environ if environ is None else environ
    for variable in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = env.get(variable, "").strip()
        if not value:
            continue
        if variable == "LANGUAGE":
            candidates = value.split(":")
            return next(
                (
                    candidate
                    for candidate in candidates
                    if candidate.split("_", 1)[0].split("-", 1)[0].lower() in {"en", "de"}
                ),
                candidates[0],
            )
        return value
    return locale.getlocale()[0] or ""


class LocaleManager:
    """Loads en/de catalogs, resolves a preference, and persists UI language only."""

    def __init__(
        self,
        preference: LanguagePreference | str | None = None,
        *,
        settings_file: Path | None = None,
        system_locale: str | None = None,
        catalog_dir: Path | None = None,
        environ: dict[str, str] | None = None,
    ) -> None:
        self.settings_file = settings_file or preference_path()
        self.catalog_dir = catalog_dir
        self.system_locale = (
            detect_system_locale(environ) if system_locale is None else system_locale
        )
        self.catalogs = {language: self._load_catalog(language) for language in ("en", "de")}
        saved = self._read_preference() if preference is None else preference
        self.preference = self._normalize_preference(saved)
        self.language = self.resolve_language(self.preference, self.system_locale)

    def _load_catalog(self, language: str) -> dict[str, str]:
        if self.catalog_dir is None:
            text = files("app.locales").joinpath(f"{language}.json").read_text(encoding="utf-8")
        else:
            text = (self.catalog_dir / f"{language}.json").read_text(encoding="utf-8")
        catalog = json.loads(text)
        if not isinstance(catalog, dict) or not catalog or not all(
            isinstance(key, str) and isinstance(value, str) and value.strip()
            for key, value in catalog.items()
        ):
            raise ValueError(f"Invalid translation catalog: {language}")
        return catalog

    def _read_preference(self) -> str:
        try:
            data = json.loads(self.settings_file.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return "system"
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Cannot read STEPS language preference at %s: %s", self.settings_file, exc)
            return "system"
        if not isinstance(data, dict):
            logger.warning("Invalid STEPS language preference format at %s", self.settings_file)
            return "system"
        return data.get("language", "system")

    @staticmethod
    def _normalize_preference(preference: str) -> LanguagePreference:
        if preference == "system":
            return "system"
        if preference == "en":
            return "en"
        if preference == "de":
            return "de"
        return "system"

    @staticmethod
    def resolve_language(preference: str, system_locale: str | None = None) -> Literal["en", "de"]:
        if preference in ("en", "de"):
            return preference
        candidate = system_locale
        if candidate is None:
            candidate = locale.getlocale()[0] or ""
        normalized = candidate.replace("-", "_").split("_", 1)[0].lower()
        return "de" if normalized == "de" else "en"

    def set_preference(self, preference: str, *, persist: bool = True) -> Literal["en", "de"]:
        normalized = self._normalize_preference(preference)
        if persist:
            self._write_preference(normalized)
        self.preference = normalized
        self.language = self.resolve_language(normalized, self.system_locale)
        return self.language

    def _write_preference(self, preference: LanguagePreference) -> None:
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.settings_file.parent,
                prefix=f".{self.settings_file.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump({"language": preference}, temporary, ensure_ascii=False)
                temporary.write("\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, self.settings_file)
        except OSError:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise

    def translate(self, message_id: str, **values: object) -> str:
        try:
            template = self.catalogs[self.language][message_id]
        except KeyError:
            raise KeyError(
                f"Missing translation key {message_id!r} for locale {self.language!r}"
            ) from None
        try:
            return template.format(**values)
        except (KeyError, ValueError, IndexError) as exc:
            raise ValueError(
                f"Invalid placeholders for translation key {message_id!r}"
            ) from exc
