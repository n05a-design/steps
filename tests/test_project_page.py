"""Check that GitHub shows the root README and that its figure is current."""

from pathlib import Path
import re
import unittest

from scripts import render_project_page_figure as figure

ROOT = Path(__file__).resolve().parents[1]


class ProjectPageTests(unittest.TestCase):
    def test_no_readme_outranks_the_root_readme(self):
        # GitHub shows .github/README.md instead of the root README when it exists.
        names = [path.name for path in (ROOT / ".github").iterdir() if path.is_file()]
        self.assertEqual([name for name in names if name.lower().startswith("readme")], [])

    def test_root_readme_shows_the_logo_and_existing_local_targets(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn('<img src="app/assets/brand/steps-app-icon-512.png"', text.split("<h1", 1)[0])
        targets = re.findall(r'(?:src|href)="([^"#]+)', text) + re.findall(r"\]\(([^)#]+)", text)
        missing = [target for target in targets
                   if not target.startswith("http") and not (ROOT / target).exists()]
        self.assertEqual(missing, [])

    def test_figure_matches_the_pilot_voicings(self):
        stored = figure.OUTPUT.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(stored, figure.render())


if __name__ == "__main__":
    unittest.main()
