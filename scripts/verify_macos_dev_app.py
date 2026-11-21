"""Verify a locally built STEPS development bundle and record its identity."""

import argparse
from hashlib import file_digest
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.midi import SMFParser
from src.steps.progression.reviewed import load_reviewed_catalog


def _digest(path: Path) -> str:
    with path.open("rb") as handle:
        return file_digest(handle, "sha256").hexdigest()


def verify(bundle: Path) -> dict:
    bundle = bundle.resolve(strict=True)
    contents = bundle / "Contents"
    with (contents / "Info.plist").open("rb") as handle:
        plist = plistlib.load(handle)
    if plist.get("CFBundleIdentifier") != "de.n05a.steps.dev" or plist.get("CFBundleExecutable") != "STEPS-Dev":
        raise ValueError("Unexpected development bundle identifier or executable")

    executable = contents / "MacOS/STEPS-Dev"
    resources = contents / "Resources"
    paths = (
        Path("LICENSE"), Path("app/locales/en.json"), Path("app/locales/de.json"),
        Path("design/tokens/tokens.json"), Path("knowledge/sources/registry.yaml"),
        Path("src/steps/progression/reviewed_progressions.json"),
        Path("src/steps/progression/reviewed_progression_approvals.json"),
        *(path.relative_to(ROOT) for path in sorted((ROOT / "app/assets/brand").iterdir()) if path.is_file()),
    )
    fingerprints = {}
    for relative in paths:
        bundled_path = (resources / relative).resolve(strict=True)
        if not bundled_path.is_relative_to(bundle):
            raise ValueError(f"Resource escapes the development bundle: {relative}")
        digest = _digest(bundled_path)
        if digest != _digest(ROOT / relative):
            raise ValueError(f"Packaged resource differs from the checkout: {relative}")
        fingerprints[relative.as_posix()] = digest
    knowledge = resources / "knowledge"
    if {path.name for path in knowledge.iterdir()} != {"sources"}:
        raise ValueError("Unexpected product knowledge directories in the development bundle")
    if {path.name for path in (knowledge / "sources").iterdir()} != {"registry.yaml"}:
        raise ValueError("Unexpected files in the packaged knowledge registry")

    pilot = load_reviewed_catalog(
        catalog_path=resources / "src/steps/progression/reviewed_progressions.json",
        registry_path=knowledge / "sources/registry.yaml",
    )

    executable = executable.resolve(strict=True)
    if not executable.is_relative_to(bundle):
        raise ValueError("Executable escapes the development bundle")
    environment = os.environ.copy()
    for variable in ("PYTHONPATH", "PYTHONHOME"):
        environment.pop(variable, None)
    with TemporaryDirectory(prefix="steps-macos-smoke-") as directory:
        stage = Path(directory)
        for language in ("en", "de"):
            run = subprocess.run(
                [str(executable), "--headless", "--language", language],
                check=True, cwd=stage, env=environment, capture_output=True, text=True, timeout=30,
            )
            locale = json.loads((resources / f"app/locales/{language}.json").read_text(encoding="utf-8"))
            if locale["cli.ready"] not in run.stdout:
                raise ValueError(f"Packaged application did not start with the {language} catalog")
        midi = stage / "smoke.mid"
        subprocess.run(
            [str(executable), "--language", "en", "--export-midi", str(midi)],
            check=True, cwd=stage, env=environment, capture_output=True, text=True, timeout=30,
        )
        parsed = SMFParser.parse(midi.read_bytes())
        note_counts = [len(track.notes) for track in parsed.tracks]
        if len(note_counts) != 3 or note_counts[0] or not all(note_counts[1:]):
            raise ValueError("Packaged MIDI export did not produce conductor, chord and bass tracks")
        midi_hash = _digest(midi)
    return {
        "checkout_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "checkout_has_tracked_changes": bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT,
        )),
        "bundle_identifier": plist["CFBundleIdentifier"],
        "executable_sha256": _digest(executable),
        "resource_sha256": fingerprints,
        "headless_languages": ["en", "de"],
        "validated_pilot_examples": [example.progression.prog_id for example in pilot],
        "midi_export": {"notes_by_track": note_counts, "sha256": midi_hash},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.bundle), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
