# 11 – Quellen- und Artefaktverzeichnis (SOURCE_AND_ARTIFACT_INDEX)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Dokumenttyp:** Nachweis aller untersuchten Quellen, Dateien, Commits und Artefakte  

---

## 1. Primäre Quellensysteme

| Quellen-ID | Typ | Pfad / Referenz | Inhalt / Abdeckung | Zugriffsstatus |
|---|---|---|---|:---:|
| `SRC-001` | Transkript | `C:\Users\Timvo\.gemini\antigravity\brain\...\transcript.jsonl` | 40 USER_INPUT Schritte, 2149 Planner-Antworten | Vollständig ausgewertet |
| `SRC-002` | Git Repo | `C:\Users\Timvo\OneDrive\Github\steps` | Vollständige Git-Historie, Branches, Commits | Vollständig ausgewertet |
| `SRC-003` | Remote Git | `https://github.com/n05a-design/steps` | GitHub Actions, Pull Requests #4, #5, #6 | Verifiziert |
| `SRC-004` | Paket-Code | `src/steps/theory/`, `src/steps/progression/` | Reiner Python-Theoriekern (6 Module) | Vollständig auditiert |
| `SRC-005` | Test-Suiten | `tests/` | 90 Unittests (Theory, Progression, Golden, Secret, Structure) | 100% PASS |
| `SRC-006` | Skill-Tests | `.agents/skills/steps-knowledge-curation/tests/` | 25 Unittests für Wissensskill | 100% PASS |
| `SRC-007` | Referenzfälle | `knowledge/research/canonical/GOLDEN_REFERENCE_CASES_CANON.json` | 198 arretierte Referenzfälle mit Hashes | Integrität gesichert |
| `SRC-008` | Progressionen | `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md` | 28 kanonische Progressionen (PROG-001..028) | Vollständig integriert |
| `SRC-009` | Graph-Rel. | `knowledge/research/canonical/KNOWLEDGE_GRAPH_RELATIONS_CANON.json` | 97 Relationen (CR, REL, EXT) | Baseline v1.3.0 intakt |
| `SRC-010` | Fehlerregister | `knowledge/research/MUSICAL_ERROR_REGISTER.csv` | 37 behobene Fachfehler (ERR-001..037) | Bereinigt & verifiziert |
| `SRC-011` | ADRs | `knowledge/architecture/` | 12 Architecture Decision Records (ADR-001..012) | Vollständig gepflegt |
| `SRC-012` | Abschlussbericht | `knowledge/research/PHASE5_1_COMPLETION_REPORT.md` | Dokumentierter Abschlussstand Phase 5.1 | Erstellt & gepusht |
