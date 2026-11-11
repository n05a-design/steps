# Vorlagen und Minimal-Dateien je Agentenlauf

Alle Dateien zunächst in einem **neuen externen Auditordner** neben dem STEPS-Checkout ablegen. Gültig für Antigravity, Claude, ChatGPT, Copilot und andere Agenten.

## STATE.json (Beispielschema, Werte sind nicht Testbelege)

```json
{
  "project": "STEPS",
  "workspace_root": "C:\\Users\\Timvo\\OneDrive\\Github\\steps",
  "glide_reference_subtree": "src/glide-v3.53",
  "glide_upstream_sha": "9e767bea5e21063466a28ac3a679406484ad5d5f",
  "steps_reference_sha": "1fc07e230dc6a2fe92fd6662da43e332d596b376",
  "actual_local_sha": null,
  "actual_local_status": "NOT_CHECKED",
  "session_id": "SET_AT_RUNTIME",
  "audit_mode": "read_only_product_sources",
  "snapshot_drift": "UNKNOWN",
  "completed_phases": [],
  "in_progress_file_ids": [],
  "unreviewed_file_ids": [],
  "coverage_counts": {"FULL": 0, "PARTIAL": 0, "METADATA_ONLY": 0, "BLOCKED": 0, "NOT_REVIEWED": 0},
  "outputs": [],
  "tests": [],
  "decisions_open": [],
  "known_repo_drift": [],
  "next_exact_steps": ["Lokalen Git-Stand überprüfen", "V5-Vorbefunde und Glide-Bestandsaufnahme registrieren"]
}
```

**Wichtig:** `steps_reference_sha` und `glide_upstream_sha` sind Referenzen dieses Handovers, nicht beweisende Aussagen über den heute geöffneten lokalen Workspace. `actual_local_sha` erst nach Ausführung eintragen.

## NEXT_SESSION_HANDOVER.md

```markdown
# STEPS – Handover <session-id>
- Datum/Modell/Tool/Projekt: ...
- Workspace: STEPS; Glide-Referenz: `src/glide-v3.53/`
- Lokaler SHA/Branch/Status, Remote-SHA, Diff: ...
- Source- und Output-Register: ...
- Bereits analysiert, inkl. Hash und Abdeckungsgrad: ...
- Ergebnisse (auch nicht implementierte, negative und allgemeine): ...
- Tatsächlich erstellte oder geänderte Dateien: ...
- Tests PASS/FAIL/SKIP/NOT_RUN/BLOCKED mit OS, Kommando, SHA, Logs: ...
- Entscheidungen des Owners vs. eigene Vorschläge: ...
- Offene Fragen/Blocker/Drift/Risiken: ...
- Exakter nächster Schritt und Einstiegsdatei: ...
- Rücknahme-/Sicherheitsgrenzen: ...
```

## Register-CSV Header

`OUTPUT_REGISTER.csv`:

```csv
artifact_id,created_at,producer_tool,producer_model_or_account,session_id,artifact_type,project,repo_path_or_private_uri,source_ids,base_repo_sha,artifact_sha256,claim_status,implementation_status,test_status,coverage_status,canonical_ref,supersedes,privacy_class,license_status,summary,reviewer,notes
```

`SOURCE_COVERAGE.csv`:

```csv
source_id,path,repo_sha,blob_sha_or_sha256,medium,size_bytes,review_level,range_checked,method,parser,findings_ids,rights_status,blocked_reason,reviewed_at
```

`DECISIONS_AND_QUESTIONS.csv`:

```csv
decision_id,topic,proposal_or_owner_decision,status,owner_source,decision_date,source_refs,options_considered,reasons,related_requirements,revisit_trigger
```

`SESSION_LOG.md`: jeder Befund mit Zeit, tatsächlichem Befehl/Parser/Tool, Inputhash, Output, Fehlerklasse, Nicht-Abdeckung und Referenz in `OUTPUT_REGISTER.csv`.
