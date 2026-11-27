"""Run curated mutations in disposable source snapshots, one change per process."""

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_randomized_music import ROOT, checkout_provenance, write_report

REGRESSIONS = "tests.test_mvve_regressions.MusicalAuditRegressions."
STATE = "tests.test_music_audit_stateful.KeyboardStateAudit."
HARNESS = "tests.test_music_audit_harness.MusicAuditHarnessTest."


@dataclass(frozen=True)
class Mutation:
    id: str
    path: str
    original: str
    replacement: str
    witness: str


MUTATIONS = (
    Mutation("INTERVAL-COMPLEMENT", "src/steps/theory/interval.py",
             "return (12 - (semitones % 12)) % 12", "return semitones % 12",
             "tests.test_theory_properties.TestMusicTheoryProperties.test_interval_apis_for_every_ordered_midi_pair"),
    Mutation("MAJOR-THIRD", "src/steps/theory/chord.py",
             "'theoretical': (0, 4, 7),", "'theoretical': (0, 3, 7),",
             HARNESS + "test_reference_profiles_exercise_the_product"),
    Mutation("MAJOR-SEVENTH", "src/steps/theory/chord.py",
             "'theoretical': (0, 4, 7, 11),", "'theoretical': (0, 4, 7, 10),",
             HARNESS + "test_reference_profiles_exercise_the_product"),
    Mutation("GERMAN-H-B", "src/steps/theory/pitch.py",
             "base_str = 'H'\n            elif self.alteration == -1:\n                base_str = 'B'",
             "base_str = 'B'\n            elif self.alteration == -1:\n                base_str = 'H'",
             "tests.test_notation_contract.TestNotationContract.test_b_requires_context"),
    Mutation("MAXIMUM-AS-BASS", "src/steps/theory/inversion.py",
             "bass_note = min(midi_list)", "bass_note = max(midi_list)",
             "tests.test_chord_inversion"),
    Mutation("SHARP-NINTH-AS-THIRD", "src/steps/keyboard/chord_tones.py",
             "15: ChordToneRole.SHARP_NINTH", "15: ChordToneRole.MINOR_THIRD",
             REGRESSIONS + "test_bass_role_and_classical_figure"),
    Mutation("DIMINISHED-SEVENTH-AS-SIXTH", "src/steps/keyboard/chord_tones.py",
             '("dim7", 9): ChordToneRole.DIMINISHED_SEVENTH', '("dim7", 9): ChordToneRole.SIXTH',
             REGRESSIONS + "test_bass_role_and_classical_figure"),
    Mutation("FIRST-CANDIDATE-ONLY", "src/steps/keyboard/recognition.py",
             "return RecognitionResult(played, pcs, status, candidates)",
             "return RecognitionResult(played, pcs, status, candidates[:1])",
             REGRESSIONS + "test_recognition_preserves_exact_candidates_under_doubling_and_translation"),
    Mutation("TRANSPOSITION-KEEPS-KEY", "src/steps/progression/session.py",
             "new_state.key_root = self._render_note_name(new_key, self.convention)",
             "new_state.key_root = self.key_root", "tests.test_notation_contract"),
    Mutation("MIDI-CHANNEL-MASK", "src/steps/ports/live.py", "status & 0x0F", "status & 0x07",
             STATE + "test_normalization_across_all_channels_and_controller_boundary"),
    Mutation("MIDI-SUSTAIN-THRESHOLD", "src/steps/keyboard/input.py", "event.value >= 64", "event.value > 64",
             STATE + "test_sustain_boundary_retrigger_and_panic_preserve_selection"),
    Mutation("MIDI-ABSOLUTE-DELTA", "src/steps/midi/smf_parser.py",
             "current_tick += delta", "current_tick = delta", "tests.test_midi_export_service"),
    Mutation("MIDI-HEADER-TRUNCATION", "src/steps/midi/smf_parser.py",
             "if header_len > len(data) - 8:", "if False:",
             REGRESSIONS + "test_smf_rejects_truncation_even_without_declared_tracks"),
    Mutation("MISSING-PRACTICE-NOTE", "src/steps/keyboard/practice.py",
             "if not missing and not extra:", "if not extra:",
             REGRESSIONS + "test_empty_exact_exercise_reports_missing_register"),
    Mutation("HIDE-GENERATOR-ERROR", "scripts/audit_randomized_music.py",
             'trial=index + 1, status="error", classification="GENERATOR_DEFECT",',
             'trial=index + 1, status="failed", classification="GENERATOR_DEFECT",',
             HARNESS + "test_generator_failure_preserves_progress_and_other_areas"),
    Mutation("OPTIMIZED-ORACLE-BYPASS", "scripts/music_audit_references.py",
             'raise ValueError(", ".join(failures))', 'assert not failures, ", ".join(failures)',
             HARNESS + "test_optimized_self_test_rejects_mutated_fixture"),
)


def test(snapshot, witness):
    return subprocess.run([sys.executable, "-B", "-m", "unittest", witness], cwd=snapshot,
                          capture_output=True, text=True, errors="replace", timeout=30)


def run_mutation(snapshot, mutation):
    result = {"id": mutation.id, "path": mutation.path, "witness": mutation.witness}
    source_path = snapshot / mutation.path
    original = source_path.read_text(encoding="utf-8")
    if mutation.original not in original:
        result["status"] = "NOT_APPLICABLE"
        return result
    phase = "baseline"
    try:
        baseline = test(snapshot, mutation.witness)
        if baseline.returncode:
            result["status"] = "BASELINE_ERROR"
            return result
        phase = "mutation"
        source_path.write_text(original.replace(mutation.original, mutation.replacement, 1), encoding="utf-8")
        mutated = test(snapshot, mutation.witness)
        if mutated.returncode == 0:
            result["status"] = "SURVIVED"
        elif "FAIL:" in mutated.stderr and "ERROR:" not in mutated.stderr:
            result["status"] = "DETECTED"
        else:
            result["status"] = "EXECUTION_ERROR"
    except subprocess.TimeoutExpired:
        result.update(status="TIMEOUT", phase=phase)
    finally:
        source_path.write_text(original, encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    with TemporaryDirectory(prefix="steps-music-mutations-") as temporary:
        snapshot = Path(temporary)
        # Copy the implementation and only the Python harness and test sources.
        shutil.copytree(ROOT / "src/steps", snapshot / "src/steps", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(ROOT / "src/__init__.py", snapshot / "src/__init__.py")
        for directory in ("scripts", "tests"):
            (snapshot / directory).mkdir()
            for file in (ROOT / directory).glob("*.py"):
                shutil.copyfile(file, snapshot / directory / file.name)
        results = [run_mutation(snapshot, mutation) for mutation in MUTATIONS]
    counts = Counter(row["status"] for row in results)
    report = {"schema_version": 1, "planned": len(MUTATIONS), "counts": counts,
              "results": results, "gate": "PASS" if counts["DETECTED"] == len(MUTATIONS) else "FAIL",
              **checkout_provenance()}
    if args.json_out:
        write_report(args.json_out, report)
    print(json.dumps(report, indent=2))
    return int(report["gate"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
