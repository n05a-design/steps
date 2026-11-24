"""
Unit Tests for STEPS Design Tokens and ThemeManager (Prompt 06 / ADR-001).

Validates:
- Correct JSON schema parsing of tokens.json
- Mode toggling between dark and light
- Hex color syntax
- WCAG 2.1 AA minimum contrast (>= 4.5:1) for body text against window background
"""

import math
import unittest
from pathlib import Path

from app.ui.theme import ThemeManager


def hex_to_relative_luminance(hex_str: str) -> float:
    """Calculates relative luminance according to WCAG 2.1 specifications."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def srgb_to_lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)

    rl, gl, bl = srgb_to_lin(r), srgb_to_lin(g), srgb_to_lin(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculates contrast ratio (L1 + 0.05) / (L2 + 0.05)."""
    l1 = hex_to_relative_luminance(hex1)
    l2 = hex_to_relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class TestThemeManager(unittest.TestCase):
    def setUp(self):
        self.tm = ThemeManager(mode="dark")

    def test_default_dark_mode(self):
        self.assertEqual(self.tm.mode, "dark")
        colors = self.tm.colors
        self.assertTrue(colors.bg_window.startswith("#"))
        self.assertTrue(colors.text_primary.startswith("#"))
        self.assertIn("Tonic", colors.__dataclass_fields__["harmonic_tonic"].name.title())

    def test_switch_to_light_mode(self):
        self.tm.set_mode("light")
        self.assertEqual(self.tm.mode, "light")
        colors = self.tm.colors
        self.assertEqual(colors.bg_window, "#F5F5F7")
        self.assertEqual(colors.text_primary, "#15243C")

    def test_invalid_mode_raises(self):
        with self.assertRaises(ValueError):
            self.tm.set_mode("neon")  # type: ignore

    def test_typography_tokens(self):
        typo = self.tm.typography
        self.assertGreater(typo.size_title, typo.size_xl)
        self.assertGreater(typo.size_xl, typo.size_lg)
        self.assertGreater(typo.size_lg, typo.size_md)
        self.assertGreater(typo.size_md, typo.size_sm)
        self.assertGreater(typo.size_sm, typo.size_xs)
        self.assertIn("sans-serif", typo.font_family_sans)
        self.assertIn("monospace", typo.font_family_mono)

    def test_spacing_tokens(self):
        sp = self.tm.spacing
        self.assertEqual(sp.xs, 4)
        self.assertEqual(sp.sm, 8)
        self.assertEqual(sp.md, 16)
        self.assertEqual(sp.radius_md, 8)

    def test_wcag_contrast_dark_mode(self):
        self.tm.set_mode("dark")
        c = self.tm.colors
        for fg_name, bg_name in (
            ("text_primary", "bg_surface"),
            ("text_primary", "bg_window"),
            ("text_primary", "bg_active"),
            ("text_secondary", "bg_surface"),
            ("text_secondary", "bg_window"),
            ("text_inverted", "harmonic_tonic"),
            ("text_inverted", "harmonic_subdominant"),
        ):
            ratio = contrast_ratio(getattr(c, fg_name), getattr(c, bg_name))
            self.assertGreaterEqual(
                ratio,
                4.5,
                f"Dark mode contrast {fg_name}/{bg_name} = {ratio:.2f} is below 4.5:1",
            )

    def test_wcag_contrast_light_mode(self):
        self.tm.set_mode("light")
        c = self.tm.colors
        for fg_name, bg_name in (
            ("text_primary", "bg_surface"),
            ("text_primary", "bg_window"),
            ("text_primary", "bg_active"),
            ("text_secondary", "bg_surface"),
            ("text_secondary", "bg_window"),
            ("text_inverted", "harmonic_tonic"),
            ("text_inverted", "harmonic_subdominant"),
        ):
            ratio = contrast_ratio(getattr(c, fg_name), getattr(c, bg_name))
            self.assertGreaterEqual(
                ratio,
                4.5,
                f"Light mode contrast {fg_name}/{bg_name} = {ratio:.2f} is below 4.5:1",
            )

    def test_system_appearance_and_font_providers(self):
        self.assertEqual(ThemeManager.resolve_system_mode(system_dark=True), "dark")
        self.assertEqual(ThemeManager.resolve_system_mode(system_dark=False), "light")
        self.assertEqual(ThemeManager.resolve_system_mode(system_dark=None, fallback="light"), "light")
        self.assertEqual(
            ThemeManager.resolve_system_mode(system_dark=True, preference="contrast-dark"),
            "contrast-dark",
        )
        self.assertEqual(
            ThemeManager.resolve_system_mode(system_dark=False, preference="contrast-dark"),
            "contrast-light",
        )
        self.assertEqual(
            ThemeManager.resolve_system_mode(system_dark=True, preference="minimal-light"),
            "minimal-dark",
        )
        self.assertEqual(
            ThemeManager.resolve_system_mode(system_dark=False, preference="minimal-light"),
            "minimal-light",
        )
        spec = self.tm.font_spec(12, "bold")
        self.assertEqual(spec[1], 12)
        self.assertEqual(spec[2], "bold")
        self.tm.configure_shell_providers()

    def test_all_six_themes_and_wcag_contrast(self):
        for theme_name in ThemeManager.THEMES:
            self.tm.set_mode(theme_name)
            self.assertEqual(self.tm.mode, theme_name)
            colors = self.tm.colors
            self.assertTrue(colors.bg_window.startswith("#"))
            self.assertTrue(colors.bg_surface.startswith("#"))
            self.assertTrue(colors.text_primary.startswith("#"))

            for fg_name, bg_name in (
                ("text_primary", "bg_surface"),
                ("text_primary", "bg_window"),
                ("text_primary", "bg_active"),
                ("text_secondary", "bg_surface"),
                ("text_secondary", "bg_window"),
                ("text_inverted", "harmonic_tonic"),
                ("text_inverted", "harmonic_subdominant"),
            ):
                ratio = contrast_ratio(getattr(colors, fg_name), getattr(colors, bg_name))
                self.assertGreaterEqual(
                    ratio,
                    4.5,
                    f"Theme {theme_name} contrast {fg_name}/{bg_name} = {ratio:.2f} is below 4.5:1",
                )

    def test_theme_alias_normalization(self):
        self.assertEqual(ThemeManager.normalize_theme_name("contrast_dark"), "contrast-dark")
        self.assertEqual(ThemeManager.normalize_theme_name("minimal_light"), "minimal-light")
        self.assertEqual(ThemeManager.normalize_theme_name("cvd-dark"), "contrast-dark")
        self.assertEqual(ThemeManager.normalize_theme_name("high-contrast-light"), "contrast-light")
        self.tm.set_mode("contrast_dark")
        self.assertEqual(self.tm.mode, "contrast-dark")
        self.assertTrue(self.tm.is_dark)

    def test_background_tint_choices_and_contrast(self):
        from app.ui.theme import BACKGROUND_CHOICES, BACKGROUND_KEYS, with_background

        self.assertIn("default", BACKGROUND_KEYS)
        self.assertIn("surface", BACKGROUND_KEYS)
        self.assertIn("accent", BACKGROUND_KEYS)
        self.assertIn("clear", BACKGROUND_KEYS)

        base_colors = self.tm.colors
        # default gives identical colors
        default_colors = with_background(base_colors, "default")
        self.assertEqual(default_colors.bg_window, base_colors.bg_window)

        # surface matches bg_surface
        surface_colors = with_background(base_colors, "surface")
        self.assertEqual(surface_colors.bg_window, base_colors.bg_surface)

        # all background tints produce valid hex and maintain >= 4.5:1 text contrast
        for choice, _ in BACKGROUND_CHOICES:
            self.tm.set_background_choice(choice)
            self.assertEqual(self.tm.background_choice, choice)
            colors = self.tm.colors
            self.assertTrue(colors.bg_window.startswith("#"))
            ratio = contrast_ratio(colors.text_primary, colors.bg_window)
            self.assertGreaterEqual(
                ratio,
                4.5,
                f"Background choice '{choice}' primary text contrast = {ratio:.2f} < 4.5:1",
            )

        with self.assertRaises(ValueError):
            self.tm.set_background_choice("unknown_tint")

    def test_corner_radius_and_font_scale_choices(self):
        from app.ui.theme import FONT_SCALE_MAP, RADIUS_MAP

        self.assertEqual(self.tm.radius_choice, "standard")
        self.assertEqual(self.tm.corner_radius, 12)

        for choice, rad in RADIUS_MAP.items():
            self.tm.set_radius_choice(choice)
            self.assertEqual(self.tm.radius_choice, choice)
            self.assertEqual(self.tm.corner_radius, rad)

        with self.assertRaises(ValueError):
            self.tm.set_radius_choice("invalid_radius")

        self.assertEqual(self.tm.font_scale_choice, "standard")
        self.assertEqual(self.tm.font_scale, 1.0)

        for choice, scale in FONT_SCALE_MAP.items():
            self.tm.set_font_scale_choice(choice)
            self.assertEqual(self.tm.font_scale_choice, choice)
            self.assertEqual(self.tm.font_scale, scale)
            spec = self.tm.font_spec(10)
            self.assertEqual(spec[1], max(6, int(round(10 * scale))))

        with self.assertRaises(ValueError):
            self.tm.set_font_scale_choice("invalid_scale")


if __name__ == "__main__":
    unittest.main()
