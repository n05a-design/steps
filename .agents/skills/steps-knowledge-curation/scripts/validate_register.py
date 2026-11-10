"""Validate the canonical master file OFFENE_ARBEITSAUFFORDERUNGEN.md."""
from __future__ import annotations
import sys, os, re

VALID_STATUSES = {
    "OPEN", "IN_PROGRESS", "BLOCKED", "OWNER_DECISION_REQUIRED",
    "DONE_UNVERIFIED", "DONE_VERIFIED", "SUPERSEDED", "NOT_APPLICABLE"
}

def validate_master_file(path: str) -> dict[str, int | list[str]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Master file not found at: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    oa_matches = re.findall(r"### (OA-\d{4}):\s*(.*)", content)
    # Match any status inside backticks following **Status:**
    status_matches = re.findall(r"\*\*Status:\*\*\s*`([A-Za-z0-9_]+)`", content)
    
    errors = []
    seen_ids = set()
    for oa_id, title in oa_matches:
        if oa_id in seen_ids:
            errors.append(f"Duplicate OA-ID found: {oa_id}")
        seen_ids.add(oa_id)
        if not title.strip():
            errors.append(f"Missing title for {oa_id}")
            
    for st in status_matches:
        if st not in VALID_STATUSES:
            errors.append(f"Invalid status value: {st}")
            
    return {
        "total_tasks_found": len(oa_matches),
        "unique_ids": len(seen_ids),
        "errors_count": len(errors),
        "errors": errors
    }

if __name__ == "__main__":
    default_p = os.path.expandvars(r"%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md")
    p = sys.argv[1] if len(sys.argv) > 1 else default_p
    res = validate_master_file(p)
    print("Master File Validation Result:")
    for k, v in res.items():
        print(f"  {k}: {v}")
    if res["errors_count"] > 0:
        sys.exit(1)
