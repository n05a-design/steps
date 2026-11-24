"""Integration and design-contract tests for Glide Shell 0.6.2 in STEPS."""

from __future__ import annotations

import ast
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import glide_shell
from glide_shell import app_host, selftest, window_lifetime

from app.i18n import LocaleManager
from app.main import create_desktop_host, main
from app.ui import layout_policy
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager, apply_window_geometry, fit_text


ROOT = Path(__file__).resolve().parents[1]
GLIDE_COMMIT = "7dcd8dc04366f88943fa17827882cef4d81421b8"


class TestGlideShellIntegration(unittest.TestCase):
    def test_glide_shell_version_manifest_and_isolation(self):
        self.assertEqual(glide_shell.SHELL_VERSION, "0.6.2")
        manifest_path = ROOT / "glide_shell" / "SHELL_MANIFEST.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["paket"], "glide_shell")
        self.assertEqual(manifest["shell_version"], "0.6.2")
        self.assertEqual(manifest["glide_system_version"], "1.86")
        self.assertEqual(manifest["quell_commit"], GLIDE_COMMIT)
        self.assertTrue(manifest["quelle_unveraendert"])
        self.assertEqual(manifest["lizenz"], "MPL-2.0")
        self.assertTrue((ROOT / "glide_shell" / "LICENSE").is_file())
        self.assertTrue((ROOT / "glide_shell" / "DESIGN_RICHTLINIEN.md").is_file())

        status = selftest.check_manifest(folder=ROOT / "glide_shell")
        self.assertIn("23 files match manifest", status)
        self.assertIn(GLIDE_COMMIT[:12], status)

    def test_music_core_remains_free_of_tkinter_and_glide_shell(self):
        forbidden = {"tkinter", "glide_shell", "app"}
        for py_file in (ROOT / "src" / "steps").rglob("*.py"):
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".", 1)[0]
                        self.assertNotIn(top, forbidden, f"{py_file} imports {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top = node.module.split(".", 1)[0]
                    self.assertNotIn(top, forbidden, f"{py_file} imports {node.module}")

    def test_app_contains_no_blocking_sleep_or_glide_domain_references(self):
        forbidden_tokens = ("ListApp", "GLIDE_DATA_DIR", ".glideexchange", "Glide-Shell-Framework")
        for py_file in (ROOT / "app").rglob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            for token in forbidden_tokens:
                self.assertNotIn(token, text, f"Forbidden token {token!r} in {py_file}")
            tree = ast.parse(text, filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if (
                        isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "time"
                        and node.func.attr == "sleep"
                    ):
                        self.fail(f"Blocking time.sleep found in UI file {py_file} (violates B01/B16)")

    def test_text_fit_helper_clips_ergonomically(self):
        clipped = fit_text("A very long progression metadata line", 15)
        self.assertEqual(clipped, "A very long...")
        self.assertLessEqual(len(clipped), 15)

    def test_glide_shell_selftest_passes_all_13_checks(self):
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        output = io.StringIO()
        code = selftest.run(out=output)
        text = output.getvalue()
        if code == 2 and not require_tk:
            self.skipTest("No Tk graphics display available")
        self.assertEqual(code, 0, text)
        self.assertIn("Glide Shell 0.6.2: 13/13 checks passed", text)

    def test_app_main_uses_apphost_and_preserves_dirty_close_and_lifetime_scope(self):
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        try:
            import tkinter as tk
            from tkinter import ttk
            from app.ui.main_window import StepsMainWindow
        except ImportError as exc:
            if require_tk:
                self.fail(f"Tk required: {exc}")
            self.skipTest("tkinter not available")

        theme = ThemeManager(mode="dark")
        host = create_desktop_host(theme)
        self.assertIsInstance(host, app_host.AppHost)

        try:
            root = host.create_root()
        except tk.TclError as exc:
            if require_tk:
                self.fail(f"Tk init failed: {exc}")
            self.skipTest("No Tk graphics display")

        def cleanup():
            try:
                if root.winfo_exists():
                    root.destroy()
            except tk.TclError:
                pass

        self.addCleanup(cleanup)
        root.withdraw()
        controller = ProgressionSessionController()
        for symbol in ("Dm7", "G7", "Cmaj7"):
            controller.add_chord(symbol)
        i18n = LocaleManager(preference="en")

        window = host.build(
            lambda r: StepsMainWindow(r, controller=controller, theme=theme, locale_manager=i18n),
            root,
        )
        self.assertIsNotNone(host.controller)
        self.assertIs(host.controller, window)
        self.assertTrue(callable(getattr(root, "_font_provider", None)))
        self.assertIsNotNone(window._lifetime_scope)

        # Verify AfterScope cancels pending jobs when window closes (B03/window_lifetime)
        fired = []
        window._lifetime_scope.after(5000, lambda: fired.append("leaked"))
        self.assertTrue(window._lifetime_scope.pending())

        # Dirty-state protection on close
        controller.add_chord("Fmaj7")
        self.assertTrue(controller.session.is_dirty)
        with patch("app.ui.main_window.messagebox.askyesnocancel", return_value=None) as ask:
            window._on_close()
            ask.assert_called_once()
        self.assertTrue(bool(root.winfo_exists()))

        # Design contract B15: minimum window size keeps all primary buttons mapped & inside bounds
        apply_window_geometry(root, 860, 600, 860, 600)
        root.deiconify()
        root.update()
        buttons = [
            window.add_btn,
            window.update_btn,
            window.remove_btn,
            window.move_up_btn,
            window.move_down_btn,
            window.undo_btn,
            window.redo_btn,
            window.trans_down_btn,
            window.trans_up_btn,
            window.export_btn,
            window.context_btn,
            window.event_timing_btn,
            window.voice_lab_btn,
            window.next_chord_panel.explore_button,
        ]
        win_w = root.winfo_width()
        win_h = root.winfo_height()
        for btn in buttons:
            self.assertIsInstance(btn, (tk.Button, ttk.Button))
            self.assertTrue(btn.winfo_ismapped(), f"Button not mapped at minsize: {btn}")
            bx = btn.winfo_rootx() - root.winfo_rootx()
            by = btn.winfo_rooty() - root.winfo_rooty()
            self.assertGreaterEqual(bx, 0)
            self.assertGreaterEqual(by, 0)
            self.assertLessEqual(bx + btn.winfo_width(), win_w + 2)
            self.assertLessEqual(by + btn.winfo_height(), win_h + 2)

        # Focus indicator check on key interactive widgets
        self.assertGreaterEqual(int(float(window.chord_listbox.cget("highlightthickness"))), 2)
        self.assertGreaterEqual(int(float(window.detail_text.cget("highlightthickness"))), 2)

        # Close cleanly discarding dirty state and verify AfterScope cleanup
        with patch("app.ui.main_window.messagebox.askyesnocancel", return_value=False):
            window._on_close()
        self.assertTrue(window._lifetime_scope.closed)
        self.assertEqual(window._lifetime_scope.jobs, set())
        self.assertEqual(fired, [])

    def test_main_entry_routes_gui_startup_through_apphost(self):
        with (
            patch("app.main.sys.platform", "darwin"),
            patch("glide_shell.app_host.AppHost.run") as run_mock,
            patch("app.ui.theme.ThemeManager") as theme_cls,
        ):
            exit_code = main(["--theme", "light", "--language", "en"])
        self.assertEqual(exit_code, 0)
        theme_cls.assert_called_once_with(mode="light")
        run_mock.assert_called_once()

    def test_layout_policy_breakpoints_and_compact_geometry(self):
        self.assertEqual(layout_policy.header_density(1200), "full")
        self.assertEqual(layout_policy.header_density(1120), "full")
        self.assertEqual(layout_policy.header_density(1024), "compact")
        self.assertEqual(layout_policy.header_density(900), "compact")
        self.assertEqual(layout_policy.header_density(860), "minimal")

        self.assertEqual(layout_policy.height_density(900), "full")
        self.assertEqual(layout_policy.height_density(800), "compact")
        self.assertEqual(layout_policy.height_density(600), "minimal")

        self.assertEqual(layout_policy.effective_sidebar_mode(True, False, False, 1024), "wide")
        self.assertEqual(layout_policy.effective_sidebar_mode(True, True, False, 1024), "rail")
        self.assertEqual(layout_policy.effective_sidebar_mode(True, False, False, 860), "rail")
        self.assertEqual(layout_policy.effective_sidebar_mode(False, False, False, 1024), "hidden")
        self.assertEqual(layout_policy.effective_sidebar_mode(True, False, True, 1024), "hidden")

        compact_geom = layout_policy.compact_geometry("1024x720+100+80", "", 1710, 1112)
        self.assertEqual(compact_geom, "520x720+604+80")
        restored_geom = layout_policy.normal_geometry("1024x720+100+80", compact_geom)
        self.assertEqual(restored_geom, "1024x720+100+80")

        self.assertEqual(layout_policy.FONT_SIZES["caption"], 9)
        self.assertEqual(layout_policy.FONT_SIZES["body"], 12)
        self.assertEqual(layout_policy.FONT_SIZES["section"], 16)
        self.assertEqual(layout_policy.FONT_SIZES["title"], 22)
        self.assertEqual(layout_policy.TITLE_MAX_CHARS, 40)
        self.assertEqual(layout_policy.BUTTON_TEXT_MAX_CHARS, 24)
        self.assertEqual(layout_policy.SYMBOLS["up"], "▴")
        self.assertEqual(layout_policy.SYMBOLS["down"], "▾")
        self.assertLessEqual(len(layout_policy.clip_title("A" * 60)), 40)
        self.assertLessEqual(len(layout_policy.clip_button_text("B" * 40)), 24)
        self.assertEqual(layout_policy.remaining_chars_text(10), "30/40")
        markers = layout_policy.aligned_menu_markers(len)
        self.assertTrue(markers["✓"].startswith("✓"))
        self.assertTrue(markers["□"].startswith("□"))

        en_i18n = LocaleManager(preference="en")
        de_i18n = LocaleManager(preference="de")
        self.assertEqual(en_i18n.translate("view.sidebar.toggle"), "Sidebar")
        self.assertEqual(de_i18n.translate("view.sidebar.toggle"), "Seitenleiste")
        self.assertEqual(en_i18n.translate("view.compact.toggle"), "Compact Mode")
        self.assertEqual(de_i18n.translate("view.compact.toggle"), "Kompaktmodus")

    def test_two_area_shell_sidebar_logo_breakpoints_and_compact_mode(self):
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        try:
            import tkinter as tk
            from app.ui.main_window import StepsMainWindow
        except ImportError as exc:
            if require_tk:
                self.fail(f"Tk required: {exc}")
            self.skipTest("tkinter not available")

        host = create_desktop_host(ThemeManager(mode="dark"))
        try:
            root = host.create_root()
        except tk.TclError as exc:
            if require_tk:
                self.fail(f"Tk init failed: {exc}")
            self.skipTest("No Tk graphics display")

        def cleanup():
            try:
                if root.winfo_exists():
                    root.destroy()
            except tk.TclError:
                pass

        self.addCleanup(cleanup)
        root.withdraw()
        controller = ProgressionSessionController()
        for symbol in ("Dm7", "G7", "Cmaj7"):
            controller.add_chord(symbol)
        window = host.build(
            lambda r: StepsMainWindow(
                r, controller=controller, theme=ThemeManager(mode="dark"), locale_manager=LocaleManager(preference="en")
            ),
            root,
        )
        root.deiconify()
        root.geometry("1024x720")
        root.update()

        # 1. Default 1024x720 shows wide sidebar, in-app logo, and D66 subtitle metrics
        self.assertEqual(window.effective_sidebar_mode(), "wide")
        self.assertTrue(window.sidebar_frame.winfo_ismapped())
        self.assertFalse(window.sidebar_rail_frame.winfo_ismapped())
        self.assertIsNotNone(window._header_logo_image)
        self.assertTrue(window.header_logo_lbl.winfo_ismapped())
        self.assertTrue(window.subtitle_lbl.winfo_ismapped())
        self.assertIn("BPM", window.subtitle_lbl.cget("text"))
        self.assertFalse(getattr(window.sidebar_toggle_btn, "_glide_is_active", True))
        self.assertTrue(getattr(window._sidebar_buttons["workspace"], "_glide_is_active", False))

        # 2. Manual narrow rail + keyboard arrow traversal + hide/show
        window.toggle_sidebar_narrow()
        root.update()
        self.assertEqual(window.effective_sidebar_mode(), "rail")
        self.assertTrue(window.sidebar_rail_frame.winfo_ismapped())
        self.assertEqual(window.sidebar_rail_frame.winfo_width(), layout_policy.SIDEBAR_RAIL_WIDTH)
        window._rail_buttons[0].focus_force()
        window._rail_buttons[0].event_generate("<Down>")
        root.update()
        self.assertEqual(root.focus_lastfor(), window._rail_buttons[1])
        window._rail_buttons[1].event_generate("<Up>")
        root.update()
        self.assertEqual(root.focus_lastfor(), window._rail_buttons[0])

        window.toggle_sidebar()
        root.update()
        self.assertEqual(window.effective_sidebar_mode(), "hidden")
        self.assertFalse(window.sidebar_frame.winfo_ismapped())
        self.assertFalse(window.sidebar_rail_frame.winfo_ismapped())
        self.assertTrue(getattr(window.sidebar_toggle_btn, "_glide_is_active", False))

        window.toggle_sidebar()
        window.toggle_sidebar_narrow()
        root.update()
        self.assertEqual(window.effective_sidebar_mode(), "wide")
        self.assertFalse(getattr(window.sidebar_toggle_btn, "_glide_is_active", True))

        # 3. Responsive breakpoint < 900 px switches wide sidebar -> rail and hides in-app logo + subtitle
        root.geometry("860x600")
        root.update()
        self.assertEqual(window._header_density, "minimal")
        self.assertEqual(window._height_density, "minimal")
        self.assertEqual(window.effective_sidebar_mode(), "rail")
        self.assertTrue(window.sidebar_rail_frame.winfo_ismapped())
        self.assertFalse(window.header_logo_lbl.winfo_ismapped())
        self.assertFalse(window.subtitle_lbl.winfo_ismapped())

        # Restoring width >= 900 restores wide sidebar, in-app logo, and subtitle
        root.geometry("1024x720")
        root.update()
        self.assertEqual(window.effective_sidebar_mode(), "wide")
        self.assertTrue(window.sidebar_frame.winfo_ismapped())
        self.assertTrue(window.header_logo_lbl.winfo_ismapped())
        self.assertTrue(window.subtitle_lbl.winfo_ismapped())

        # 4. Compact mode hides sidebar/logo/subtitle, allows COMPACT_MIN, and restores normal geometry
        window.enter_compact_mode()
        root.update()
        self.assertTrue(window.compact_mode_active())
        self.assertEqual(root.minsize(), layout_policy.COMPACT_MIN)
        self.assertFalse(window.sidebar_frame.winfo_ismapped())
        self.assertFalse(window.sidebar_rail_frame.winfo_ismapped())
        self.assertFalse(window.header_logo_lbl.winfo_ismapped())
        self.assertFalse(window.subtitle_lbl.winfo_ismapped())

        window.leave_compact_mode()
        root.update()
        self.assertFalse(window.compact_mode_active())
        self.assertEqual(root.minsize(), layout_policy.NORMAL_MIN)
        self.assertEqual(window.effective_sidebar_mode(), "wide")
        self.assertTrue(window.sidebar_frame.winfo_ismapped())
        self.assertTrue(window.header_logo_lbl.winfo_ismapped())
        self.assertTrue(window.subtitle_lbl.winfo_ismapped())

        # 5. Live theme switching updates Glide surfaces and entries across all 6 themes
        for theme_name in ("light", "contrast-dark", "contrast-light", "minimal-dark", "minimal-light", "dark"):
            window.apply_theme(theme_name)
            root.update()
            self.assertEqual(window.theme.mode, theme_name)
            self.assertEqual(window.root.cget("bg"), window.theme.colors.bg_window)
            self.assertEqual(window.sidebar_frame.cget("bg"), window.theme.colors.bg_surface)
            self.assertEqual(window.chord_entry.cget("bg"), window.theme.colors.bg_window)
        window.set_theme_preference("contrast-dark")
        root.update()
        self.assertEqual(window.theme.mode, "contrast-dark")
        window.set_theme_preference("dark")
        root.update()
        self.assertEqual(window.theme.mode, "dark")
        self.assertEqual(window.root.cget("bg"), window.theme.colors.bg_window)


if __name__ == "__main__":
    unittest.main()
