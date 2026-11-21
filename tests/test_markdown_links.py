"""Tests for the relative Markdown link gate."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_markdown_links.py"

spec = importlib.util.spec_from_file_location("check_markdown_links", SCRIPT)
links = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(links)


class TestMarkdownLinks(unittest.TestCase):
    def test_current_checkout_has_no_broken_active_links(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("MARKDOWN LINK CHECK PASS", result.stdout)

    def test_targets_ignore_code_external_urls_and_anchors(self):
        text = (
            "[ok](a.md) ![img](img/x.svg) `[code](no.md)`\n"
            "```\n[fenced](no.md)\n```\n"
            "[web](https://example.org) [anchor](#top) [titled](b.md \"Title\")\n"
        )
        self.assertEqual(
            links.link_targets(text),
            ["a.md", "img/x.svg", "https://example.org", "#top", "b.md"],
        )

    def test_broken_link_is_reported_and_existing_one_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "present.md").write_text("x", encoding="utf-8")
            (root / "docs" / "index.md").write_text(
                "[good](present.md#part) [bad](missing.md)", encoding="utf-8"
            )
            findings = links.broken_links(root, "docs/index.md")
        self.assertEqual(findings, ["docs/index.md: missing.md"])

    def test_archives_and_raw_research_are_out_of_scope(self):
        self.assertFalse(links.is_active("archive/old/README.md"))
        self.assertFalse(links.is_active("research/STEPS_Bibliothek/x.md"))
        self.assertTrue(links.is_active("research/gaps/OPEN_GAPS.md"))
        self.assertTrue(links.is_active("docs/roadmap/README.md"))

    def test_historical_exceptions_name_their_reason(self):
        for reason in links.HISTORICAL_LINKS.values():
            self.assertRegex(reason, r"[0-9a-f]{7}")


if __name__ == "__main__":
    unittest.main()
