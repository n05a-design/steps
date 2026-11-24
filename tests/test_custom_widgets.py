"""Tests for Glide custom canvas widgets and AppearanceDialog."""

from __future__ import annotations

import tkinter as tk
import unittest
from unittest.mock import Mock

from app.i18n import LocaleManager
from app.ui import layout_policy
from app.ui.appearance_dialog import AppearanceDialog
from app.ui.custom_widgets import RoundedButton, RoundedSurfaceCard
from app.ui.theme import ThemeManager, default_theme


class TestCustomWidgets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
            cls.tk_available = True
        except Exception:
            cls.tk_available = False

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "tk_available", False) and getattr(cls, "root", None) is not None:
            try:
                cls.root.destroy()
            except Exception:
                pass

    def setUp(self):
        if not self.tk_available:
            self.skipTest("Tkinter display not available")

    def test_rounded_surface_card_initialization_and_theming(self):
        card = RoundedSurfaceCard(
            self.root,
            bg_color="#111113",
            fill_color="#1C1C1E",
            outline_color="#3A3A3C",
            radius=12,
            padding=8,
            auto_height=True,
        )
        self.assertEqual(card.bg_color, "#111113")
        self.assertEqual(card.fill_color, "#1C1C1E")
        self.assertEqual(card.radius, 12)
        self.assertIsInstance(card.inner, tk.Frame)

        # Update theme
        card.set_theme(
            bg_color="#F5F5F7",
            fill_color="#FFFFFF",
            outline_color="#D8D8DE",
            radius=18,
        )
        self.assertEqual(card.bg_color, "#F5F5F7")
        self.assertEqual(card.fill_color, "#FFFFFF")
        self.assertEqual(card.radius, 18)
        card.destroy()

    def test_rounded_button_features_and_accessibility(self):
        called = False

        def _on_click():
            nonlocal called
            called = True

        long_label = "This is a very long button text that exceeds twenty four characters"
        btn = RoundedButton(
            self.root,
            text=long_label,
            command=_on_click,
            bg_color="#111113",
            base_bg="#1C1C1E",
            base_fg="#F5F5F7",
            hover_bg="#243A55",
            active_bg="#C66CF3",
            radius=10,
        )
        # B11 / D63: Button text is clipped to max 24 chars
        self.assertEqual(len(btn.display_text), layout_policy.BUTTON_TEXT_MAX_CHARS)
        self.assertTrue(btn.display_text.endswith("..."))

        # Active state toggle
        btn.set_active(True)
        self.assertTrue(btn._glide_is_active)
        btn.set_active(False)
        self.assertFalse(btn._glide_is_active)

        # Keyboard activation
        event = Mock()
        btn._on_activate(event)
        self.assertTrue(called)

        # Programmatic invoke()
        called = False
        btn.invoke()
        self.assertTrue(called)

        # Dict access getitem and setitem
        btn["text"] = "Dict Access"
        self.assertEqual(btn["text"], "Dict Access")
        self.assertEqual(btn.cget("text"), "Dict Access")

        # Retheming
        btn.set_theme(
            bg_color="#F5F5F7",
            base_bg="#E5E5EA",
            base_fg="#15243C",
            hover_bg="#D8E9FE",
            radius=6,
        )
        self.assertEqual(btn.radius, 6)
        self.assertEqual(btn.base_bg, "#E5E5EA")

        # config() and fg/bg options
        btn.config(fg="#FF0000", bg="#00FF00")
        self.assertEqual(btn.cget("fg"), "#FF0000")
        self.assertEqual(btn.cget("bg"), "#00FF00")

        # Set text dynamically
        btn.set_text("Short text")
        self.assertEqual(btn.display_text, "Short text")
        btn.destroy()

    def test_appearance_dialog_builds_and_applies(self):
        theme = ThemeManager(mode="dark")
        i18n = LocaleManager(preference="en")
        applied_results = None

        def _on_apply(m, b, r, s):
            nonlocal applied_results
            applied_results = (m, b, r, s)

        dlg = AppearanceDialog(
            parent=self.root,
            theme=theme,
            i18n=i18n,
            theme_preference="contrast-dark",
            on_apply=_on_apply,
        )
        self.assertEqual(dlg.theme_var.get(), "contrast-dark")
        self.assertEqual(dlg.bg_var.get(), "default")
        self.assertEqual(dlg.radius_var.get(), "standard")
        self.assertEqual(dlg.scale_var.get(), "standard")

        # Change vars and update preview
        dlg.theme_var.set("light")
        dlg.bg_var.set("accent")
        dlg.radius_var.set("large")
        dlg.scale_var.set("compact")
        dlg._update_preview()

        # Click apply
        dlg._on_apply_clicked()
        self.assertEqual(applied_results, ("light", "accent", "large", "compact"))


if __name__ == "__main__":
    unittest.main()
