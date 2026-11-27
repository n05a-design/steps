"""Gate musical release areas with executable checks and independently reviewed evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import musical_release_checks as checks
from scripts import run_knowledge_benchmark as benchmark
from scripts import verify_pilot_review_evidence as pilot
from src.steps.progression import reviewed

AREAS = {
    "theory-core": (
        ("test_notation_contract", "test_harmonic_function_accuracy", "test_theory_properties",
         "test_progression_engine"), (),
    ),
    "desktop-voicing": (
        ("test_beginner_voicing", "test_voice_leading_styles"),
        ("Explain each offered style and verify its actual voicings and playable range.",),
    ),
    "keyboard": (
        ("test_keyboard_domain", "test_mvve_regressions"),
        ("Review contextual note names, written and sounding bass, and figures for the supported voicings.",),
    ),
    "recognition": (
        ("test_keyboard_engine.TestChordRecognition", "test_keyboard_engine.TestReviewRegressions"),
        ("Review ambiguous, standard and incomplete readings in the stated keyboard scope.",),
    ),
    "keyboard-practice": (
        ("test_keyboard_engine.TestPracticePilot", "test_mvve_regressions"),
        ("Review every included exercise, permitted answers and feedback against independent teaching criteria.",),
    ),
    "musical-integration": (
        ("test_keyboard_engine.TestWorkbenchSessionIntegration", "test_storage_recovery_io"),
        ("Verify recognition, explicit adoption, preview isolation, project recovery and exported output.",),
    ),
    "midi-export": (
        ("test_midi_export_service", "test_midi_golden_fixtures"), (),
    ),
    "recommendations": (
        ("test_harmonic_function_accuracy", "test_cross_domain_recommender"),
        ("Review competing functions, style suggestions and the limits of confidence labels.",),
    ),
    "learning-pilot": (
        ("test_reviewed_progressions", "test_pilot_publication"),
        ("Verify each lesson, its alternative readings and the stated source limits.",),
    ),
    "knowledge-adapter": (
        ("test_knowledge_adapter",),
        ("Verify the actual answers, citations and use of uncertainty across the evaluation prompts.",),
    ),
    "harmony-coach": ((), ()),
    "research-library": (
        ("test_reference_integrity",),
        ("Review the source-to-claim links and distinguish style observations from musical rules.",),
    ),
}


def curation_evidence() -> list[str]:
    tool = ROOT / ".agents/skills/steps-knowledge-curation/scripts/check_reference_ids.py"
    result = subprocess.run(
        [sys.executable, "-B", str(tool), "--json"], cwd=ROOT,
        capture_output=True, text=True, timeout=120, env=checkout_environment(),
    )
    if not result.returncode:
        return []
    try:
        errors = json.loads(result.stdout)["errors"]
    except (ValueError, KeyError, TypeError):
        errors = []
    return [f"Curation evidence: {error}" for error in errors] or ["Curation evidence check did not complete."]


AUTO_PROBES = {
    "theory-core": checks.randomized_theory,
    "research-library": curation_evidence,
    "desktop-voicing": checks.desktop_voicing,
    "midi-export": checks.midi_drop2,
    "knowledge-adapter": checks.knowledge_retrieval,
    "recommendations": checks.recommendations,
    "recognition": checks.exhaustive_recognition,
}
THEORY_SAMPLE = {"frequency", "enharmonic", "distance", "intervals", "degree"}


def case_area(case):
    if case["id"] == "KB-M12-PLAYABILITY":
        return "desktop-voicing"
    if case["scope"] in {"pilot", "publication"} or case["id"] == "KB-M09-LOOP-HEAR":
        return "learning-pilot"
    if case["scope"] == "api" or case["method"] in THEORY_SAMPLE:
        return "theory-core"
    if case["scope"] == "coach":
        return "harmony-coach"
    return "research-library"


def requirements(area, cases):
    area_criteria = AREAS[area][1]
    result = {"AREA": area_criteria} if area_criteria else {}
    for case in cases:
        if case["mandatory"] and case["method"] in {"manual", "coach"}:
            result[case["id"]] = tuple(case["expected"])
    return result


def template(area, cases, revision):
    extra = dict(response="", model="", skill_revision="") if area == "harmony-coach" else {}
    return {
        "area": area,
        "revision": revision,
        "independent": False,
        "reviews": {
            ident: {"criteria": dict.fromkeys(criteria, None), "observations": "",
                    "sources": [{"url": "", "locator": "", "supports": ""}],
                    "evidence_url": "", **extra}
            for ident, criteria in requirements(area, cases).items()
        },
    }


def reviewed_criteria(required, entry, *, coach=False):
    coach_fields = {"response", "model", "skill_revision"} if coach else set()
    expected_fields = {"criteria", "observations", "sources", "evidence_url"} | coach_fields
    if not isinstance(entry, dict) or entry.keys() != expected_fields:
        return False
    if not all(reviewed_text(entry[field]) for field in coach_fields):
        return False
    criteria = entry["criteria"]
    if (not isinstance(criteria, dict) or criteria.keys() != set(required)
            or any(value is not True for value in criteria.values())):
        return False
    if not reviewed_text(entry["observations"]) or not https_url(entry["evidence_url"]):
        return False
    sources = entry["sources"]
    return isinstance(sources, list) and bool(sources) and all(
        isinstance(source, dict) and source.keys() == {"url", "locator", "supports"}
        and https_url(source["url"]) and reviewed_text(source["locator"])
        and reviewed_text(source["supports"]) for source in sources
    )


def reviewed_text(value):
    return isinstance(value, str) and bool(value.strip()) and not reviewed.PLACEHOLDER.search(value)


def https_url(value):
    if not isinstance(value, str) or re.search(r"[\s<>\\]", value):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return bool(parsed.scheme == "https" and parsed.hostname and parsed.username is None)


def fetch_pull(number):
    return json.loads(subprocess.check_output(
        ["gh", "api", f"repos/{pilot.REPOSITORY}/pulls/{number}"],
        text=True, timeout=15,
    ))


def verified_submission(url, revision, *, fetch_comment=pilot.fetch_comment, fetch_pr=fetch_pull):
    match = pilot.URL.fullmatch(url)
    if not match:
        raise ValueError("Use a STEPS pull-request comment permalink.")
    pr_number, comment_id = map(int, match.groups())
    comment = fetch_comment(comment_id)
    pr = fetch_pr(pr_number)
    author = comment["user"]
    time = datetime.fromisoformat(comment["created_at"])
    if (
        comment["id"] != comment_id or comment["html_url"] != url
        or comment["issue_url"] != f"https://api.github.com/repos/{pilot.REPOSITORY}/issues/{pr_number}"
        or pr["number"] != pr_number or pr["base"]["repo"]["full_name"] != pilot.REPOSITORY
        or not (pr["head"]["sha"] == revision or (pr["merged"] is True and pr["merge_commit_sha"] == revision))
        or author["type"] != "User" or author["id"] not in pilot.REVIEWERS
        or author["id"] == pr["user"]["id"]
        or comment["author_association"] not in {"OWNER", "MEMBER", "COLLABORATOR"}
        or comment["created_at"] != comment["updated_at"]
        or time.utcoffset() is None or time > datetime.now(timezone.utc)
    ):
        raise ValueError("The comment does not prove an independent review of this revision.")
    payload = re.fullmatch(r"```steps-musical-review\n(.*)\n```", comment["body"].strip(), re.DOTALL)
    if not payload:
        raise ValueError("Expected a single steps-musical-review block.")
    record = json.loads(payload[1], object_pairs_hook=reviewed._unique_keys)
    if (not isinstance(record, dict) or record.keys() != {"area", "revision", "independent", "reviews"}
            or record["area"] not in AREAS or record["revision"] != revision
            or record["independent"] is not True or not isinstance(record["reviews"], dict)):
        raise ValueError("The review area, revision or independence declaration is invalid.")
    return record["area"], {"reviewer": author["login"], "url": url, "reviews": record["reviews"]}


def suites(modules):
    if not modules:
        return []
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", *(f"tests.{module}" for module in modules)],
            cwd=ROOT, check=False, timeout=120, env=checkout_environment(),
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
    except subprocess.TimeoutExpired:
        return ["Technical regression suite exceeded its time budget"]
    except OSError:
        return ["Technical regression suite could not start"]
    return ["Technical regression suite failed"] if result.returncode else []


def check_area(area, cases, automatic, acceptance, *, run_suites=suites, probes=AUTO_PROBES,
               verify_pilot=pilot.verify_catalog):
    blockers = list(run_suites(AREAS[area][0]))
    if area in probes:
        try:
            blockers.extend(probes[area]())
        except Exception as exc:
            blockers.append(f"Musical probe could not execute: {exc}")
    if area == "learning-pilot":
        try:
            verify_pilot(reviewed.load_reviewed_catalog())
        except reviewed.PublicationError as exc:
            blockers.append(f"Pilot evidence: {exc}")
    for case in automatic:
        if case["mandatory"] and case["status"] != "PASS":
            blockers.append(f'{case["id"]}: {case["status"]} ({case["observed"]})')
    required = requirements(area, cases)
    accepted = acceptance.get("reviews", {})
    if set(accepted) - set(required):
        blockers.append("Review contains unknown criteria for this area")
    for ident, criteria in required.items():
        if ident not in accepted:
            blockers.append(f"{ident}: independent musical review pending")
        elif not reviewed_criteria(criteria, accepted[ident], coach=area == "harmony-coach"):
            blockers.append(f"{ident}: independent musical review incomplete or rejected")
    return {"status": "BLOCKED" if blockers else "READY", "blockers": blockers,
            "automated_cases": len(automatic), "review": acceptance}


def checkout_environment() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


def checkout_state() -> tuple[str, bool]:
    env = checkout_environment()
    checkout = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=ROOT, env=env, text=True,
    ).strip()
    if Path(checkout).resolve() != ROOT.resolve():
        raise ValueError("The release verifier must run from its own STEPS Git checkout.")
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, env=env, text=True,
    ).strip()
    dirty = bool(subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, env=env,
    ))
    return revision, dirty


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", choices=("all", *AREAS), default="all")
    parser.add_argument("--review-comment", action="append", default=[])
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    try:
        revision, dirty = checkout_state()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.error(f"Cannot identify the STEPS checkout: {exc}")
    cases = benchmark.load_cases()
    if args.template:
        if args.area == "all" or dirty:
            parser.error("A review template requires one area and a clean tracked checkout.")
        print(json.dumps(template(args.area, [c for c in cases if case_area(c) == args.area], revision),
                         indent=2, ensure_ascii=False))
        return 0
    if dirty and not args.report_only:
        parser.error("A release check requires a clean tracked checkout.")
    areas = tuple(AREAS) if args.area == "all" else (args.area,)
    accepted = {}
    try:
        for url in args.review_comment:
            area, submission = verified_submission(url, revision)
            if area not in areas or area in accepted:
                parser.error("Supply at most one review comment per requested area.")
            accepted[area] = submission
    except (AttributeError, KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError,
            reviewed.PublicationError) as exc:
        parser.error(f"Review evidence rejected: {exc}")

    selected = [case for case in cases if case_area(case) in areas]
    automated = [case for case in selected if case["method"] not in {"manual", "coach"}]
    try:
        examples, claims = reviewed._candidates() if "learning-pilot" in areas else ({}, {})
    except reviewed.PublicationError:
        examples, claims = {}, {}
    results = benchmark.run(automated, examples, claims, {})
    status = {
        area: check_area(area, [c for c in selected if case_area(c) == area],
                         [c for c in results if case_area(c) == area], accepted.get(area, {}))
        for area in areas
    }
    report = {"revision": revision, "dirty": dirty, "report_only": args.report_only, "areas": status}
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for area, result in status.items():
        print(f"{area}: {result['status']}")
        for blocker in result["blockers"]:
            print(f"  - {blocker}")
    return int(not args.report_only and any(item["status"] == "BLOCKED" for item in status.values()))


if __name__ == "__main__":
    raise SystemExit(main())
