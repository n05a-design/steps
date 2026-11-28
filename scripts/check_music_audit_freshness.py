"""Read the most recent scheduled music validation from GitHub Actions."""

import argparse
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import subprocess
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_randomized_music import write_report

REPOSITORY = "n05a-design/steps"
WORKFLOW = "python-tests.yml"
JOBS = ("Continuous music validation", "External music validation")


def github_json(*args):
    result = subprocess.run(["gh", *args, "--repo", REPOSITORY], check=True,
                            text=True, encoding="utf-8", capture_output=True, timeout=30)
    return json.loads(result.stdout)


def current_main():
    output = subprocess.check_output(
        ["git", "ls-remote", f"https://github.com/{REPOSITORY}.git", "refs/heads/main"],
        text=True, encoding="utf-8", timeout=30,
    )
    revision, ref = output.strip().split()
    if ref != "refs/heads/main" or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Invalid default-branch revision.")
    return revision


def check(max_age, now, revision):
    runs = github_json("run", "list", "--workflow", WORKFLOW, "--branch", "main",
                       "--event", "schedule", "--limit", "1",
                       "--json", "databaseId,headSha,conclusion,startedAt,url")
    if not runs:
        return {"status": "NOT_RUN", "time_status": "NOT_RUN", "revision_status": "NOT_RUN",
                "required_revision": revision, "run": None}
    run = runs[0]
    started = datetime.fromisoformat(run["startedAt"])
    age = (now - started).total_seconds() / 3600
    detail = github_json("run", "view", str(run["databaseId"]), "--json", "jobs")
    job_statuses = {name: next((job["conclusion"] for job in detail["jobs"] if job["name"] == name), None)
                    for name in JOBS}
    time_status = "STALE" if age < 0 or age > max_age else "PASS"
    revision_status = "PASS" if run["headSha"] == revision else "REVISION_MISMATCH"
    if time_status != "PASS":
        status = time_status
    elif revision_status != "PASS":
        status = revision_status
    elif run["conclusion"] != "success" or any(value != "success" for value in job_statuses.values()):
        status = "BLOCKED"
    else:
        status = "PASS"
    return {"status": status, "time_status": time_status, "revision_status": revision_status,
            "required_revision": revision, "age_hours": round(age, 2), "run": run,
            "job_conclusions": job_statuses}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-hours", type=int, default=36)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--revision")
    args = parser.parse_args()
    if args.max_age_hours <= 0:
        parser.error("--max-age-hours must be positive")
    if args.revision and not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("--revision must be a full lowercase Git SHA")
    now = datetime.now(timezone.utc)
    try:
        report = check(args.max_age_hours, now, args.revision or current_main())
    except (KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError) as exc:
        report = {"status": "ERROR", "error_type": type(exc).__name__}
    report.update(checked_at=now.isoformat(), max_age_hours=args.max_age_hours)
    if args.json_out:
        write_report(args.json_out, report)
    print(json.dumps(report))
    return {"PASS": 0, "NOT_RUN": 1, "STALE": 1, "REVISION_MISMATCH": 1, "BLOCKED": 1, "ERROR": 3}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
