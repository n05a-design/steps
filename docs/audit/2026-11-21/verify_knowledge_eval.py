"""Execute the published knowledge skills fixtures and compare source decisions."""
from collections import Counter
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from src.steps.knowledge import KnowledgeAdapter
from src.steps.progression.reviewed import PublicationError, load_reviewed_catalog

CASES = Path("skills/steps-knowledge/skill_eval_cases.json")
REGISTRY = Path("knowledge/sources/registry.yaml")


def audit():
    adapter = KnowledgeAdapter()
    rows = []
    for case in json.loads(CASES.read_text())["cases"]:
        answer = adapter.query(case["prompt"])
        rows.append({
            "case": case["id"], "category": case["category"], "prompt": case["prompt"],
            "expected_status": case["expected_status"], "actual_status": answer.status,
            "status_correct": case["expected_status"] == answer.status,
            "expected_source": case["expected_source"],
            "actual_source_ids": [source.source_id for source in answer.sources],
            "explanation": answer.explanation,
        })
    env = json.loads(REGISTRY.read_text())
    source = next(row for row in env["sources"] if row["id"] == "omt-ii-v-i")
    source["rights_status"] = "review_required"
    with TemporaryDirectory(prefix="steps-review-audit-") as directory:
        modified = Path(directory) / "registry.yaml"
        modified.write_text(json.dumps(env))
        try:
            load_reviewed_catalog(registry_path=modified)
        except PublicationError as error:
            gate = str(error)
        else:
            gate = "ACCEPTED"
        altered = KnowledgeAdapter(product_registry=modified).query("ii-V-I")
        counterexample = {
            "registry_status": source["rights_status"],
            "curated_catalog": gate,
            "adapter": altered.status,
            "adapter_citation_rights": sorted({s.rights_status for s in altered.sources}),
            "adapter_claim_verified": sorted({claim.verified for claim in altered.claims}),
        }
    return {
        "counts": sorted(Counter(("status_match" if r["status_correct"] else "status_mismatch")
                                 for r in rows).items()),
        "publication_counterexample": counterexample,
        "cases": rows,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
