# STEPS – STRUKTURVERGLEICH VORHER / NACHHER
## Dokumentation der Bereinigung und Konsolidierung der Verzeichnisarchitektur

**Prüfdatum:** 11. November 2026  

---

## 1. Wurzelverzeichnis (Root) im direkten Vergleich

```text
VORHER (28 Ordner, 24 lose Dateien)             NACHHER (20 Ordner, 11 gepflegte Dateien)
=====================================             =========================================
.agents/                                          .agents/
.github/                                          .github/
app/                                              app/
archive/                                          archive/
decisions/                                        decisions/
design/                                           design/
docs/                                             docs/
knowledge/                                        knowledge/
manifests/                                        manifests/
prompts/                                          prompts/
publish_overlay/                                  publish_overlay/
research/                                         research/
schemas/                                          schemas/
scripts/                                          scripts/
skills/                                           skills/
source_archive/                                   source_archive/
src/                                              src/
templates/                                        templates/
tests/                                            tests/
tools/                                            tools/

[VERSCHOBEN NACH archive/:]                       [BEREINIGT:]
- AI_CONTEXT_HANDOVER/                            -> archive/agent-history/handovers/
- Antigravity Steps Bericht/                      -> archive/agent-history/antigravity/
- Antigravity_MasterAuditV2_Bericht/              -> archive/agent-history/antigravity/
- OpenAI Steps Bericht/                           -> archive/agent-history/openai/
- Auditpakete/                                    -> archive/audit-history/earlier-audits/
- Gesamtpruefung_V4_GitHub_.../                   -> archive/audit-history/earlier-audits/
- Gesamtpruefung_V4_mit_Original.../              -> archive/audit-history/earlier-audits/
- Arbeits-Richtlinien & Aufträge/                 -> archive/project-history/early-planning/

[LOSE ROOT-DATEIEN BEREINIGT:]                    [KANONISCHE ROOT-DATEIEN:]
- 30_ANTIGRAVITY_MASTER_AUDIT_...                 .gitignore
- ANALYSE_REPOSITORY.md                           AGENTS.md
- Antigravity_Startprompt_Glide_...               CHANGELOG.md
- Steps – kritische Gesamtprüfung...              CONTRIBUTING.md
- STEPS_Masterreview_V4_...                       EXECUTION_BACKLOG.md
- Steps_Projektuebersicht_...                     LICENSE (MPL 2.0)
- STEPS_V4_HISTORISCHE_...                        pyproject.toml
- STEPS_V4_NEUE_BEFUNDE.csv                       README.md (aktualisiert auf v0.1)
- STEPS_V4_PACKAGE_SHA256.txt                     SECURITY.md
- STEPS_Zielstruktur.md                           SKILL.md
- SHELL_EXTRACTION_DEEP_SPEC.md                   VERSION
- HOW_TO_IMPORT_IN_GITHUB.md
- README_SETUP.md
- bootstrap_steps.py
```

---

## 2. Struktur des konsolidierten `archive/` Verzeichnisses

```text
archive/
├── README.md                                     # Erläuterung und Nutzungsregeln
├── INDEX.md                                      # Zentraler Navigationsindex
├── manifests/
│   ├── ARCHIVE_MANIFEST.csv                      # Lückenloses Verschiebe-Protokoll mit Hashes
│   ├── ARCHIVE_PLAN.csv                          # Vollständiger Genehmigungsplan
│   ├── ARCHIVE_ACTION_LOG.md                     # Detailliertes Aktionslog
│   ├── ARCHIVE_RESTORE_GUIDE.md                  # Reversible Wiederherstellungsanleitung
│   └── 02_DATEIKLASSIFIZIERUNG.csv               # Vollständige 8-Stufen-Klassifizierung
│
├── project-history/
│   ├── early-planning/                           # Arbeitsrichtlinien, bootstrap, Zielstruktur
│   ├── architecture-drafts/                      # Shell extraction, Glide Shell report
│   └── superseded-overviews/                     # Ältere Projektübersichten
│
├── documentation-history/
│   ├── previous-versions/                        # Historische README_v1, Setup-Guides
│   └── superseded-documents/                     # Frühere Analyse-Dateien
│
├── audit-history/
│   └── earlier-audits/                           # Auditpakete, V4-Prüfungen, historische CSVs
│
├── agent-history/
│   ├── antigravity/                              # Master-Audit V2, Antigravity-Berichte
│   ├── openai/                                   # OpenAI Handover- und Prüfpaket
│   └── handovers/                                # AI_CONTEXT_HANDOVER Dossiers
│
└── legacy/
    ├── v1_docs/                                  # Historische Originaldokumente
    └── v1_prompts/                               # Historische Prompts
```
