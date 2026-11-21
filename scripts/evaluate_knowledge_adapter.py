"""Execute the knowledge questions and report runtime regressions and coverage gaps."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.steps.knowledge import KnowledgeAdapter
from src.steps.progression.reviewed import _unique_keys

FIXTURE = ROOT / "skills/steps-knowledge/skill_eval_cases.json"
STATUSES = {"GROUNDED", "ALTERNATIVE_INTERPRETATIONS", "NO_EVIDENCE", "RESTRICTED_LOCAL", "AMBIGUOUS_REJECTION"}


def evaluate(cases, adapter):
    """Return exact retrieval observations for each case in input order."""
    results = []
    for case in cases:
        target = case["expected_status"]
        expected = case.get("runtime_status", target)
        claim_ids = case.get("approved_claim_ids", [])
        source_ids = case.get("approved_source_ids", [])
        if target not in STATUSES or (expected != target and expected != "NO_EVIDENCE"):
            raise ValueError(f"{case['id']}: invalid status expectation")
        found = expected in {"GROUNDED", "ALTERNATIVE_INTERPRETATIONS"}
        if found != bool(claim_ids and source_ids):
            raise ValueError(f"{case['id']}: approved claim and source IDs are required for a grounded expectation")
        answer = adapter.query(case["prompt"])
        claims = [claim.claim_id for claim in answer.claims]
        sources = [(source.source_id, source.locator) for source in answer.sources]
        cited = tuple(dict.fromkeys(citation for claim in answer.claims for citation in claim.citations))
        publication_matches = all(claim.verified and claim.citations and claim.summary for claim in answer.claims)
        publication_matches &= all(source.rights_status == "approved" and source.locator.strip() and source.url
                                   for source in answer.sources)
        passed = (answer.status == expected and answer.found is found and claims == claim_ids
                  and {source_id for source_id, _ in sources} == set(source_ids)
                  and answer.sources == cited and publication_matches)
        results.append({
            "id": case["id"], "target_status": target, "runtime_expected": expected,
            "actual_status": answer.status, "runtime_pass": passed,
            "coverage_pending": expected != target, "claim_ids": claims, "citations": sources,
        })
    return results


def run():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"), object_pairs_hook=_unique_keys)
    cases = fixture["cases"]
    if (fixture["schema_version"] != "1.1.0" or fixture["total_cases"] != len(cases)
            or len({case["id"] for case in cases}) != len(cases)):
        raise ValueError("Knowledge evaluation fixture has an invalid version, count or duplicate case ID")
    return evaluate(cases, KnowledgeAdapter())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Include the observed result of every case.")
    args = parser.parse_args()
    results = run()
    counts = Counter("PASS" if item["runtime_pass"] else "FAIL" for item in results)
    summary = {"runtime_pass": counts["PASS"], "runtime_fail": counts["FAIL"],
               "coverage_pending": sum(item["coverage_pending"] for item in results)}
    if args.json:
        print(json.dumps({"summary": summary, "cases": results}, indent=2, ensure_ascii=False))
    else:
        print(f"Runtime: {counts['PASS']} PASS, {counts['FAIL']} FAIL. Target coverage: {summary['coverage_pending']} pending.")
        for item in results:
            if not item["runtime_pass"]:
                print(f"{item['id']}: expected {item['runtime_expected']}; observed {item['actual_status']}, "
                      f"claims {item['claim_ids']}, citations {item['citations']}.")
    return int(bool(counts["FAIL"]))


if __name__ == "__main__":
    raise SystemExit(main())
