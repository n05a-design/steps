"""Test the publication paths in an isolated checkout with synthetic reviews."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from src.steps.progression import resolve_roman_degree
from src.steps.progression import reviewed
from src.steps.theory import parse_chord, parse_spelling

ROOT = Path(__file__).resolve().parents[1]
RENDER = ("scripts/render_reviewed_progressions.py",)
CI = (*RENDER, "--check")
APP = (
    "-c",
    "from app.knowledge import get_reviewed_progression, list_reviewed_progressions; "
    "import json; "
    "examples = list_reviewed_progressions(); "
    "assert examples == tuple(get_reviewed_progression(ex.progression.prog_id) for ex in examples); "
    "print(json.dumps([(ex.progression.prog_id, ex.catalog_version, ex.lesson) for ex in examples]))",
)
APP_GET = (
    "-c",
    "from app.knowledge import get_reviewed_progression; get_reviewed_progression('PROG-001')",
)
CANDIDATES = reviewed.CATALOG.relative_to(ROOT)
REGISTRY = reviewed.REGISTRY.relative_to(ROOT)
APPROVALS = reviewed.APPROVALS.relative_to(ROOT)
OUTPUT = Path("knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md")


class PilotMusicTests(unittest.TestCase):
    def test_chords_and_degrees_match_independent_pitch_class_expectations(self):
        examples, _ = reviewed._candidates()
        # C=0. These literals are derived from the C-major scale and chord spellings.
        expected = {
            "PROG-001": (
                ("I", "C", 0, {0, 4, 7}), ("V", "G", 7, {7, 11, 2}),
                ("vi", "Am", 9, {9, 0, 4}), ("IV", "F", 5, {5, 9, 0}),
            ),
            "PROG-003": (
                ("ii^7", "Dm7", 2, {2, 5, 9, 0}), ("V^7", "G7", 7, {7, 11, 2, 5}),
                ("I^maj7", "Cmaj7", 0, {0, 4, 7, 11}),
            ),
            "PROG-009": (
                ("I", "C", 0, {0, 4, 7}), ("IV", "F", 5, {5, 9, 0}),
                ("iv", "Fm", 5, {5, 8, 0}), ("I", "C", 0, {0, 4, 7}),
            ),
        }
        self.assertEqual(examples.keys(), expected.keys())
        for ident, positions in expected.items():
            with self.subTest(ident=ident):
                example = examples[ident]
                self.assertEqual(example["default_key"], "C")
                self.assertEqual(example["roman"].split(" - "), [p[0] for p in positions])
                self.assertEqual(example["chords"].split(" - "), [p[1] for p in positions])
                for degree, symbol, root, pitch_classes in positions:
                    for chord in (parse_chord(symbol, "INT"), resolve_roman_degree(degree, "C", convention="INT")):
                        self.assertEqual(chord.symbol, symbol)
                        self.assertEqual(chord.root.pitch_class, root)
                        self.assertEqual(chord.pitch_class_set, pitch_classes)

        # The same loop permits the relative-minor reading with A as the assumed center.
        self.assertEqual(
            [resolve_roman_degree(degree, "A", is_minor_key=True, convention="INT").symbol
             for degree in ("III", "VII", "i", "VI")],
            ["C", "G", "Am", "F"],
        )

    def test_written_voice_paths_are_descending_semitones_with_chord_membership(self):
        examples, claims = reviewed._candidates()
        for ident, expected_path, midi in (
            ("PROG-003-VOICE-II-V", ((0, "C4"), (1, "H3")), (60, 59)),
            ("PROG-003-VOICE-V-I", ((1, "F4"), (2, "E4")), (65, 64)),
            ("PROG-009-VOICE-LEADING", ((1, "A4"), (2, "As4"), (3, "G4")), (69, 68, 67)),
        ):
            with self.subTest(ident=ident):
                path = claims[ident].voice_path
                self.assertEqual(path, expected_path)
                actual = [parse_spelling(note, "DE").midi_number for _, note in path]
                self.assertEqual(actual, list(midi))
                self.assertEqual([b - a for a, b in zip(actual, actual[1:])], [-1] * (len(path) - 1))
                chords = examples[ident[:8]]["chords"].split(" - ")
                for (chord_index, _), note in zip(path, actual, strict=True):
                    self.assertIn(note % 12, parse_chord(chords[chord_index], "INT").pitch_class_set)

        for german, international, midi in (("H3", "B3", 59), ("B3", "Bb3", 58), ("As4", "Ab4", 68)):
            self.assertEqual(parse_spelling(german, "DE").midi_number, midi)
            self.assertEqual(parse_spelling(international, "INT").midi_number, midi)


class PilotPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.claims = reviewed._candidates()

    def setUp(self):
        tmp = self.enterContext(TemporaryDirectory())
        self.root = Path(tmp)
        for folder in ("src/steps", "app"):
            shutil.copytree(ROOT / folder, self.root / folder, ignore=shutil.ignore_patterns("__pycache__"))
        for path in (REGISTRY, OUTPUT, Path(RENDER[0])):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        self.records = {
            ident: {
                "fingerprint": claim.fingerprint,
                "reviewer": "fixture-reviewer",
                "reviewed_on": datetime.now(timezone.utc).date().isoformat(),
                "evidence_url": "https://github.com/n05a-design/steps/pull/11#pullrequestreview-1",
            }
            for ident, claim in self.claims.items()
        }
        self.save_approvals()

    def run_entry(self, command):
        return subprocess.run(
            (sys.executable, "-B", *command), cwd=self.root, capture_output=True, text=True, timeout=10,
        )

    def load(self, path):
        return json.loads((self.root / path).read_text(encoding="utf-8"))

    def save(self, path, document):
        (self.root / path).write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")

    def save_approvals(self):
        self.save(APPROVALS, {"schema_version": 1, "approvals": self.records})

    def assert_blocked(self, reason):
        for command in (APP, APP_GET, RENDER, CI):
            with self.subTest(command=command):
                result = self.run_entry(command)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(reason, result.stderr)

    def assert_entry_succeeds(self, command):
        result = self.run_entry(command)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_approved_fixture_publishes_same_version_and_content(self):
        examples = json.loads(self.assert_entry_succeeds(APP))
        self.assertEqual([row[0] for row in examples], ["PROG-001", "PROG-003", "PROG-009"])
        self.assertEqual(len({row[1] for row in examples}), 1)
        self.assert_entry_succeeds(RENDER)
        self.assert_entry_succeeds(CI)
        document = (self.root / OUTPUT).read_text(encoding="utf-8")
        self.assertIn(examples[0][1], document)
        for claim in self.claims.values():
            self.assertIn(claim.claim_id, document)
            self.assertIn(claim.text, document)
            self.assertIn(claim.fingerprint, document)
        for ident, _, lesson in examples:
            texts = [claim.text for claim in self.claims.values() if claim.claim_id.startswith(ident)]
            self.assertTrue(texts)
            for text in texts:
                self.assertIn(text, lesson)

    def test_missing_human_approval_blocks_every_entry(self):
        del self.records["PROG-001-HARMONY"]
        self.save_approvals()
        self.assert_blocked("Missing human approval: PROG-001-HARMONY")

    def test_omitted_claim_blocks_every_entry(self):
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"].pop()
        self.save(CANDIDATES, doc)
        self.assert_blocked("PROG-001: missing, unexpected or reordered pilot claims")

    def test_unknown_source_blocks_every_entry(self):
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"][0]["references"][0]["source_id"] = "invented-source"
        self.save(CANDIDATES, doc)
        self.assert_blocked("unknown source invented-source")

    def test_missing_source_register_blocks_every_entry(self):
        (self.root / REGISTRY).unlink()
        self.assert_blocked("registry.yaml: cannot read publication data")

    def test_missing_references_block_every_entry(self):
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"][0]["references"] = []
        self.save(CANDIDATES, doc)
        self.assert_blocked("PROG-001-HARMONY.references: expected a nonempty list")

    def test_unapproved_registry_source_blocks_every_entry(self):
        registry = self.load(REGISTRY)
        registry["sources"][0]["rights_status"] = "review_required"
        self.save(REGISTRY, registry)
        self.assert_blocked("unapproved source omt-roman-numerals")

    def test_placeholder_blocks_every_entry(self):
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"][0]["references"][0]["locator"] = "PLACEHOLDER"
        self.save(CANDIDATES, doc)
        self.assert_blocked("locator: missing text or placeholder")

    def test_malformed_approval_evidence_blocks_every_entry(self):
        self.records["PROG-001-HARMONY"]["evidence_url"] = "https://example.org/review"
        self.save_approvals()
        self.assert_blocked("expected a permalink")

    def test_valid_fingerprint_cannot_publish_inconsistent_music(self):
        for field, replacement, reason in (
            ("chords", "Dm7 - G7 - Fmaj7", "Roman numerals disagree"),
            ("voice_path", "C#4", "invalid music data"),
            ("voice_path", "E4", "outside its chord"),
        ):
            with self.subTest(field=field, replacement=replacement):
                doc = json.loads((ROOT / CANDIDATES).read_text(encoding="utf-8"))
                example = doc["examples"][1]
                if field == "voice_path":
                    example["claims"][1]["voice_path"][0]["note"] = replacement
                else:
                    example[field] = replacement
                self.save(CANDIDATES, doc)
                command = ("-m", "src.steps.progression.reviewed", "--review-manifest")
                manifest = self.assert_entry_succeeds(command)
                for line in manifest.splitlines()[1:]:
                    ident, _, _, fingerprint = line.split("\t")
                    self.records[ident]["fingerprint"] = fingerprint
                self.save_approvals()
                self.assert_blocked(reason)

    def test_changed_source_locator_invalidates_the_approval(self):
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"][0]["references"][0]["locator"] += " in a different edition"
        self.save(CANDIDATES, doc)
        self.assert_blocked("PROG-001-HARMONY: approval does not match")

    def test_falsified_lesson_cannot_be_regenerated_with_previous_approval(self):
        self.assert_entry_succeeds(RENDER)
        before = (self.root / OUTPUT).read_bytes()
        doc = self.load(CANDIDATES)
        doc["examples"][0]["claims"][0]["text"] = "C-Dur enthält Fis anstelle von F."
        self.save(CANDIDATES, doc)
        self.assert_blocked("PROG-001-HARMONY: approval does not match")
        self.assertEqual((self.root / OUTPUT).read_bytes(), before)
        result = self.assert_entry_succeeds(("-m", "src.steps.progression.reviewed", "--review-manifest"))
        self.assertIn("PROG-001-HARMONY\tfact\tINVALID_APPROVAL", result)
        self.assertIn("PROG-001-TONAL-CENTER\tstyle_interpretation\tAPPROVAL_RECORDED", result)
