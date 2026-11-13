"""Validate explicit graph correction proposals without rewriting historical edges."""

from urllib.parse import urlsplit


def validate(document, relations, known_nodes):
    if document.get("schema_version") != 1 or not isinstance(document.get("corrections"), list):
        raise ValueError("Invalid graph correction document")
    by_id = {row["relation_id"]: row for row in relations}
    result = {}
    for row in document["corrections"]:
        ident = row["historical_relation_id"]
        original = row["historical_edge"]
        replacement = row["replacement"]
        pcs = replacement["pitch_classes"]
        source = urlsplit(row["source_url"])
        if (ident in result or ident not in by_id
                or original != {key: by_id[ident][key] for key in ("source_id", "target_id", "relation_type")}
                or row["historical_assessment"] != "FAIL" or row["review_status"] != "REVIEW_REQUIRED"
                or row["production_use_allowed"] is not False
                or replacement["source_id"] != original["source_id"]
                or replacement["source_id"] not in known_nodes
                or replacement["target_id"] not in known_nodes
                or replacement["relation_type"] != "HAS_PITCH_CLASS_COLLECTION"
                or not isinstance(pcs, list) or not pcs
                or any(type(value) is not int or not 0 <= value < 12 for value in pcs)
                or pcs != sorted(set(pcs))
                or source.scheme != "https" or not source.hostname
                or not all(row[key].strip() for key in ("basis", "limitation"))):
            raise ValueError(f"Invalid or prematurely approved graph correction: {ident}")
        result[ident] = row
    return result
