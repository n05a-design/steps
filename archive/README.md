# STEPS – Historisches Projekt- und Dokumentenarchiv

Dieses Verzeichnis enthält alle historisch gewordenen, durch neuere Versionen ersetzten oder abgeschlossenen Dokumentationen, Forschungsunterlagen, Auditpakete und Agentenberichte des STEPS-Projekts.

## 1. Verzeichnisstruktur

* **`manifests/`:** Lückenlose Nachweise aller Archivierungen (`ARCHIVE_MANIFEST.csv`, `ARCHIVE_PLAN.csv`, `ARCHIVE_ACTION_LOG.md`, `ARCHIVE_RESTORE_GUIDE.md`).
* **`project-history/`:** Frühere Planungsunterlagen, Arbeitsrichtlinien, Bootstrapskripte und Architekturkonzepte.
* **`documentation-history/`:** Frühere Dokumentversionen (z.B. historische `README_v1`) und abgelöste Spezifikationen.
* **`audit-history/`:** Frühere Gesamtrevisionen, Auditpakete (Phase 1, Phase 2, V4-Prüfungen) und Testberichte.
* **`agent-history/`:** Vollständige Berichte und Übergabedossiers beteiligter KI-Agenten (`antigravity/`, `openai/`, `handovers/`).
* **`legacy/`:** Frühe unveränderte Originalstrukturen (`v1_docs/`, `v1_prompts/`).

## 2. Nutzungsregeln

1. **Preservation-First:** Dateien in diesem Verzeichnis dienen ausschließlich der Dokumentation, Revision und Nachvollziehbarkeit. Sie werden nicht gelöscht.
2. **Keine aktive Verwendung:** Inhalte im Archiv stellen **nicht** den aktuellen Produkt-, Release- oder Architekturstand dar. Verbindliche aktive Spezifikationen befinden sich in `docs/` und `src/steps/`.
3. **Reversibilität:** Alle Verschiebungen sind in `manifests/ARCHIVE_MANIFEST.csv` protokolliert und können bei Bedarf anhand von `manifests/ARCHIVE_RESTORE_GUIDE.md` exakt an ihren ursprünglichen Pfad zurückgeführt werden.
