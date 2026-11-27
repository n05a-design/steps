"""Read the most recent scheduled music validation from GitHub Actions."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_randomized_music import write_report

REPOSITORY = "n05a-design/steps"
WORKFLOW = "python-tests.yml"
JOB = "Continuous music validation"


def github_json(*args):
    result = subprocess.run(["gh", *args, "--repo", REPOSITORY], check=True,
                            text=True, encoding="utf-8", capture_output=True, timeout=30)
    return json.loads(result.stdout)


def check(max_age, now):
    runs = github_json("run", "list", "--workflow", WORKFLOW, "--branch", "main",
                       "--event", "schedule", "--limit", "1",
                       "--json", "databaseId,headSha,conclusion,startedAt,url")
    if not runs:
        return {"status": "NOT_RUN", "run": None}
    run = runs[0]
    started = datetime.fromisoformat(run["startedAt"])
    age = (now - started).total_seconds() / 3600
    detail = github_json("run", "view", str(run["databaseId"]), "--json", "jobs")
    job = next((job for job in detail["jobs"] if job["name"] == JOB), None)
    if age < 0 or age > max_age:
        status = "STALE"
    elif run["conclusion"] != "success" or job is None or job["conclusion"] != "success":
        status = "BLOCKED"
    else:
        status = "PASS"
    return {"status": status, "age_hours": round(age, 2), "run": run,
            "job_conclusion": job["conclusion"] if job else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-hours", type=int, default=36)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    if args.max_age_hours <= 0:
        parser.error("--max-age-hours must be positive")
    now = datetime.now(timezone.utc)
    try:
        report = check(args.max_age_hours, now)
    except (KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError) as exc:
        report = {"status": "ERROR", "error_type": type(exc).__name__}
    report.update(checked_at=now.isoformat(), max_age_hours=args.max_age_hours)
    if args.json_out:
        write_report(args.json_out, report)
    print(json.dumps(report))
    return {"PASS": 0, "NOT_RUN": 1, "STALE": 1, "BLOCKED": 1, "ERROR": 3}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
