"""Tests that GitHub configuration only references versioned labels."""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def taxonomy() -> dict[str, dict]:
    data = yaml.safe_load((ROOT / ".github/labels.yml").read_text(encoding="utf-8"))
    return {label["name"]: label for group in data.values() for label in group}


class TestGithubLabels(unittest.TestCase):
    def test_labels_are_unique_and_complete(self):
        data = yaml.safe_load((ROOT / ".github/labels.yml").read_text(encoding="utf-8"))
        names = [label["name"] for group in data.values() for label in group]
        self.assertEqual(len(names), len(set(names)))
        for label in taxonomy().values():
            self.assertRegex(label["color"], r"^[0-9a-f]{6}$")
            self.assertTrue(label["description"].strip())
            self.assertLessEqual(len(label["description"]), 100)

    def test_issue_templates_use_versioned_labels(self):
        known = taxonomy()
        for template in sorted((ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml")):
            data = yaml.safe_load(template.read_text(encoding="utf-8"))
            if "body" not in data:
                continue
            labels = data.get("labels") or []
            self.assertTrue(labels, f"{template.name} has no label")
            for label in labels:
                self.assertIn(label, known, template.name)

    def test_release_note_categories_use_versioned_labels(self):
        known = taxonomy()
        config = yaml.safe_load((ROOT / ".github/release.yml").read_text(encoding="utf-8"))
        referenced = [
            label
            for category in config["changelog"]["categories"]
            for label in category["labels"]
            if label != "*"
        ]
        referenced += config["changelog"]["exclude"]["labels"]
        for label in referenced:
            self.assertIn(label, known)


if __name__ == "__main__":
    unittest.main()
