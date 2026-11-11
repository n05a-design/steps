# STEPS – DUPLIKATE, MEHRFACHFASSUNGEN UND VERSIONEN
## Systematischer Abgleich redundanter Dateien und Identifikation kanonischer Nachfolger

**Prüfdatum:** 11. November 2026  

---

## 1. Typ-1-Duplikate (Byte-identische Dateien)

Im Repository wurden mehrere Gruppen von Dateien mit identischen SHA-256-Prüfsummen identifiziert:
* **Gruppe 1: Handover-Dossiers (`00_PROJECT_CONTEXT_HANDOVER.md` bis `14_ORIGINAL_CHAT_TRANSCRIPT.md`):**
  - Existierten bytegleich in `AI_CONTEXT_HANDOVER/`, `Antigravity Steps Bericht/AI_CONTEXT_HANDOVER/` und `archive/AI_CONTEXT_HANDOVER.zip`.
  - *Kanonische Behandlung:* Alle Markdown-Fassungen wurden nach `archive/agent-history/` verschoben und im Manifest referenziert; kein Byte ging verloren.
* **Gruppe 2: Master-Audit V2 Deliverables (`01_GESAMTBERICHT.md` bis `17_AUDIT_INDEX.md`):**
  - Lagen in `Antigravity_MasterAuditV2_Bericht/` und zusätzlich in `Antigravity Steps Bericht/MASTER_AUDIT_V2/`.
  - *Kanonische Behandlung:* Konsolidierung in `archive/agent-history/antigravity/Antigravity_MasterAuditV2_Bericht/` und gespiegelte Bereitstellung im lokalen Auditordner.

---

## 2. Typ-2-Duplikate (Inhaltlich verwandte Fassungen mit Versionsdrift)

* **`README.md` (Root) vs. realer Code-Stand:**
  - Alte Fassung (Stand 10.11.2026): Behauptete "kein lauffähiges Modulgerüst, keine Tests".
  - Reale Fassung in Phase 5.1: Pure Python Core in `src/steps/` mit 115 Tests und 28 Progressionen.
  - *Maßnahme:* Alte Fassung revisionssicher gesichert als `archive/documentation-history/previous-versions/README_v1_historical_2026-11-10.md`; neue Fassung im Root etabliert.
* **Aufgabenregister (`OFFENE_ARBEITSAUFFORDERUNGEN`):**
  - Lokale Masterdatei: `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`.
  - Repository-Snapshot: `docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md`.
  - *Kanonischer Status:* Die Datei in `%LOCALAPPDATA%` bleibt die einzige verbindliche Masterautorität; der Snapshot im Repository dient als schreibgeschützte historische Referenz.

---

## 3. Typ-3-Duplikate (Historische Entwicklungs- und Auditstufen)

* **V4-Auditbestände (10.11.2026):**
  - `Gesamtpruefung_V4_GitHub_2026-11-10/` und `Gesamtpruefung_V4_mit_Originalquellen_2026-11-10/`.
  - Sie stellen historische Arbeitsstände von vor PR #75 dar.
  - *Maßnahme:* Vollständig nach `archive/audit-history/earlier-audits/` verschoben.
* **Frühe Planungs- und Setup-Dokumente:**
  - `STEPS_Zielstruktur.md`, `bootstrap_steps.py`, `SHELL_EXTRACTION_DEEP_SPEC.md`, `HOW_TO_IMPORT_IN_GITHUB.md`.
  - *Maßnahme:* Vollständig nach `archive/project-history/` verschoben.
