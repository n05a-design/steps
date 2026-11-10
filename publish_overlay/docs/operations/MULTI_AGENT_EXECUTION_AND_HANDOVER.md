# Multi-Agent-Arbeitsbetrieb mit ChatGPT, Claude, Gemini/Antigravity, Copilot und Codex

**Status:** organisatorischer Lösungsvorschlag. **Ziel:** Token-/Account-Limits überstehen, ohne Kontextbruch, konkurrierende Dateimutationen oder scheinbar bestandene QA. Keine Aussage über heute verfügbare spezielle Claude-Modelle oder Guthaben; zeitabhängige Modell-/Planverfügbarkeit bei Anbieter bestätigen.

## 1. Arbeitsaufteilung nach Quellrecht, Toolfähigkeit und Ownership

| Workstream | Agententauglich | Grenzen |
|---|---|---|
| Glide Abschluss 3.53.0 | Copilot im bestehenden Glide-Checkout | keine parallele Steps-Modifikation derselben Dateien, QA nur mit eigenem SHA |
| Steps Code-Shell | Codex/Claude Code mit *separatem* Steps-Branch | erst nach Glide-Manifest, keine direkte Kopie des gesamten Monolithen |
| Fachforschung | ChatGPT/Claude/Gemini mit nachweislich nutzbaren Quellen | Bibliografie/Belege getrennt von Modellzusammenfassungen; kein ungeprüfter PDF-Upload |
| KB-Ingestion | lokaler deterministischer Code + reviewer-gestützte KI | Source-/Claim-IDs und Rechtsstatus nötig, keine selbstgenehmigten Quellen |
| Design/UX | Design-Agenten mit Repo-/Designvertrag | Screenshots nur Inspirationsmaterial, keine Kopie fremder Produkt-UI |
| QS/Release | unabhängiger Reviewer + GitHub-CI + Menschenabnahme | Auftraggeber muss Scope, Marken-/Releaseentscheidungen freigeben |

**Grundregel:** Zwei Agenten dürfen nicht zeitgleich denselben Dateibereich in unterschiedlichen Branches als *kanonisch* ändern. Stattdessen Integrationsreihenfolge mit `owns_paths`, `blocked_by`, `base_sha`, `output_sha`, `reviewer` definieren. Ein Agent, der auf Datenzugriff warten muss, kann Aufgaben- oder Test-Spezifikationen schreiben, jedoch keinen fiktiven „Abschluss“ behaupten.

## 2. Minimales Handover bei jedem Session-Ende

```yaml
project: STEPS
workstream: KB-INGEST
starting_commit: null
ending_commit: null
current_branch: null
files_changed: []
source_ids_used: []
claims_added_or_changed: []
checks_run: []
checks_not_run: []
open_decisions: []
blockers: []
rollback_steps: []
next_safe_action: null
owner_review_required: true
```

Aufgaben in `docs/roadmap/` bzw. GitHub Issues verlinken, kein Chat als alleiniger Projektstand. Prompts können aktualisiert werden, aber eine Änderung muss eindeutig versioniert sein. Keine automatisierten Eingriffe in fremde Modelleinstellungen oder Guthaben ohne Bestätigung.

## 3. Prioritäten unter knappen Tokens

1. **Jetzt ohne Cloudkapazität:** Quell-/Dateimanifeste, link-/hash checks, lokale Test-Fixtures, Readme-Audit, Reuse-Modulmap, P0-Rechteinventar und schriftliche ADR-Vorlagen.
2. **Wenn Claude-Guthaben zurückkommt:** aufgabenbasierter Architektur-Spike (`B` neutraler Glide-Extrakt vs. `D` kleine neue Tk-Shell) mit begrenztem Code-Scope und exakten Akzeptanzfällen; kein projektweiter Rewrite.
3. **Wenn ChatGPT-Guthaben zurückkommt:** Quellen-Review mit Nachweiskarten, unabhängiger Evaluation bereits entwickelter Golden Tests, Research-Synthese und Gap-Review.
4. **Copilot fortsetzen:** nur klar isolierte Glide-3.53.0-Finalisierung; aktuelle `main`-Merge-Lage vor Auftrag überprüfen – Arbeit nicht doppeln.

Die im Nutzertext genannten Wochentage beziehen sich auf einen berichteten Accountzustand, keine zeitlich verlässliche Scheduler-API. Fortschritt ist nicht an Modelle oder Token-Resets zu binden. Wiederholbare lokale Skripte + Git-Commits sind die nachhaltige Basis.

## 4. Kontrollpunkte zur Zusammenarbeit

Vor Aufgabenstart: `git status`, HEAD, erwartete Pfade/Dateihashes, Quelle und License Gate. Nach Aufgabe: Diff, automatisierte Tests samt Kommando und Logs, Regressionsliste, Rückbauplan, offene Reviewerfragen. Vor PR: Issues/ADRs/Schemaänderungen, Rechte-/Datenschutzprüfung; kein Merge durch Agenten. Nach Merge: README/Handovers/Prompts und Registry auf neuen SHA aktualisieren; Regression nur gegen genau diesen Stand als `PASS` kennzeichnen.

## 5. Erforderliche Prompt-Korrekturen

Die ursprünglichen 24 Prompts enthalten gemeinsam zahlreiche wiederholte Agentenregeln und nur kurze bereichsspezifische Prüfpassagen. Statt dieselbe gemeinsame Sicherheitsbelehrung 24-mal zu vervielfältigen: **ein kanonischer Agentenvertrag** in `AGENTS.md` bzw. hier, pro Prompt nur Scope, Eingaben/IDs, Deliverables, Entscheidungs- und Negativtests. Bestehende Prompts sind im Paket erhalten und bekommen in `prompts/README.md` eine Ergänzung mit konkreten neuen Prüfankern; eine planvolle Ersetzung gehört in einen kontrollierten eigenen Dokumentations-PR.
