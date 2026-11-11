# STEPS – Projektstart, Glide-3.53-Baseline und KI-Übergabe (V6)

**Status:** ergänzende, additive und versionsgebundene Projektübersicht. **Kein Ersatz** für `docs/project/PROJECT_OVERVIEW.md`, die bestehenden Originale, `AGENTS.md` oder die ausgearbeiteten V1–V5-Audits.

## Verbindlicher Auftrag und Pfad

- **Aktives Entwicklungsprojekt:** STEPS (`n05a-design/steps`), lokale Projektwurzel `C:\Users\Timvo\OneDrive\Github\steps`.
- **Eingebettete technische Referenz:** `C:\Users\Timvo\OneDrive\Github\steps\src\glide-v3.53`; liegt **innerhalb von STEPS**. Nicht den separaten Glide-Checkout als Arbeitsprojekt öffnen.
- **Festgelegte Baseline:** Glide **3.53.0**, Upstream `n05a-design/glide-to-do@9e767bea5e21063466a28ac3a679406484ad5d5f`, Glide-Systemkatalog **V1.15**. Die GitHub-Hauptprüfung (Run 42822511966) und macOS-arm64-Paketjob (42822511486) sind erfolgreich. Glide **ist grün** auf diesem Commit; spezifische skips/Release-Gates bleiben getrennte Fakten.
- **STEPS-GitHub-Snapshot:** `n05a-design/steps@1fc07e230dc6a2fe92fd6662da43e332d596b376` (3.768 Git-Blob-Dateipfade, davon 1.580 in `src/glide-v3.53/`). Ein späteres lokales Delta hat Vorfahrt für den tatsächlichen Arbeitszustand, nicht für die historische Referenz.
- **Projektentscheidung:** Aus der fertigen Glide-3.53-To-do-App ein neutrales, komponentenweise wartbares Desktop-Fundament erzeugen und auf **diesem** Steps aufbauen. Glide selbst nicht rückbauen/umbenennen.

## Für jeden Wechsel des KI-Systems verpflichtend

**Alle Ergebnisse – insbesondere Analysen, allgemeine Ausgaben, frühere Untersuchungen, Entscheidungen, Codeschritte, Tests, Fehlversuche, Prompts und Kontextübergaben – dauerhaft, prüfbar und als Dateien dokumentieren.** Dies ist eine projektweite, modellunabhängige Arbeitsregel. ChatGPT/Claude/Copilot/Gemini/Antigravity und zukünftige Agenten lesen dieselben Quellen und den jeweils neuesten gesicherten Status. Details: [`AI_CONTINUITY_PROTOCOL_V6.md`](../../operations/AI_CONTINUITY_PROTOCOL_V6.md).

Jeder Lauf erzeugt wenigstens `STATE.json`, `NEXT_SESSION_HANDOVER.md`, `SESSION_LOG.md`, `OUTPUT_REGISTER.csv`, `SOURCE_COVERAGE.csv` im sicheren neuen Audit-Ausgabeordner. Nach genehmigter Integration wird daraus ein versionierter, git-tauglicher Steps-Bericht. Keine Lücke durch Umschreiben von Originalen verstecken. Bei unbekannter Quelle: `NOT_REVIEWED` bzw. `UNKNOWN`, nicht `PASS`.

## Tatsächlich bereits vorliegende Untersuchungen

1. **Antigravity-Analyse Glide:** `Glide_Projektbestandsaufnahme_2026-11-10.md`; 215 Zeilen, untersucht das separate Glide-Repository als Referenz, dokumentiert u.a. 7 lokale Dokumentnachträge, 5 Widerspruchsklassen und offene Prüfgrenzen. Datiert, nicht als aktueller STEPS-Git-Status ausgeben.
2. **STEPS V5-Master-Audit:** `30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md` und `STEPS_Antigravity_Masterprompt_und_Befunde.docx`; 3.768 Git-Dateien *inventarisiert* ≠ inhaltlich gelesen. 42 bisherige Output-Spezifikationen, Sicherheits- und Coverage-Gates.
3. **V5-Meta-Prompt:** `31_META_PROMPT_ANTIGRAVITY_2026-11-10.md` verlangt unabhängigen Prompt-Review. **V6** ist eine ergänzte ausführbare Fassung mit dokumentierter Quellen-/Anforderungszuordnung; V5 bleibt als historische Quelle.
4. **Vorherige Überarbeitung:** `Glide_Steps_Antigravity_Uebergabepaket_2026-11-10.zip` (34 MD-Dateien); veraltete Arbeitsrichtung „Glide separat öffnen“ gilt für STEPS **nicht mehr**. V1-Paket nur historisch referenzieren, nicht direkt in Glide importieren.
5. **Vorhandene STEPS-Quellen:** `docs/project/PROJECT_OVERVIEW.md`, `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, `prompts/01_*` bis `29_*`, `research/`, `knowledge/`, `skills/`, `manifests/`, historische W/G/K/N/REQ-Register. Sie bleiben die eigentliche Fachbasis.

## Richtige Reihenfolge

1. [`00_START_IN_ANTIGRAVITY.md`](00_START_IN_ANTIGRAVITY.md) lesen und Workspace-Root bestätigen.
2. `AGENTS.md`, `SKILL.md`, derzeitige kanonische Projekt-Overview und vorige Bestandsaufnahme lesen; lokalen Git-Snapshot aufnehmen.
3. [`32_STEPS_ANTIGRAVITY_MASTER_AUDIT_V6.md`](../../../prompts/32_STEPS_ANTIGRAVITY_MASTER_AUDIT_V6.md) für vollständige, abdeckungsgeführte Analyse nutzen – **zunächst read-only**.
4. Alle bisherigen Ergebnisse/Analysen in das nachhaltige Register überführen; dann ein überprüfbares Delta-/Widerspruchs-/Risikoportfolio erstellen.
5. Rückbau erst nach eigenem Owner-Auftrag/ADR, auf separatem STEPS-Branch. [`SHELL_AND_REUSE_CONTRACT_V6.md`](SHELL_AND_REUSE_CONTRACT_V6.md) und die 30 bestehenden Shell-Szenarien sind verbindlich.

## Quellstatus und wichtige Widersprüche

- `src/steps-0.00/` ist historischer Versions-/Arbeitsordner; `import steps-0.00` funktioniert nicht als normales Python-Modul. Der Strukturcheck erwartet `src/steps/`. Letzte gemeldete Struktur-CI für Schritte nach dem Umzug fehlgeschlagen (Run 42842449461); erneute Prüfung nur auf tatsächlichem aktuellem Steps-SHA.
- Glide `3.53.0` grün ist **nicht** Steps grün. Musikkern, MIDI/Audio und Steps-Shell verlangen eigene Tests.
- Glide-`app.pyw` hat starke `ListApp`-/Import-Nebenwirkungs-Kopplungen. 94/147/25 und 311 sind dokumentierte Glide-Systemregisterbestände, keine isolierten SDK-Freigaben.
- Öffentlich abgelegte externe Fachbücher, Web-Caches, Drittgrafiken und Musikdateien brauchen eigenes Rechte-/Verwendungsregister; ein MPL-Quellcode-Lizenztext genehmigt keine fremden Inhalte.

## Ergebnisse dieses Übergabepakets

| Datei | Zweck |
|---|---|
| `00_START_IN_ANTIGRAVITY.md` | kopierbarer sofortiger Steps-Prompt, auf bestehender Analyse aufbauend |
| `AI_CONTINUITY_PROTOCOL_V6.md` | Pflichtvertrag für *alle* künftigen KI-Modelle und bisherigen Ergebnisse |
| `REQUIREMENTS_COVERAGE_V6.csv` | jeder bekannte Nutzerwunsch mit V6-Mapping und Evidenz-/Implementierungsgrenze |
| `SOURCE_AND_CONFLICT_DELTAS_V6.md` | historische Korrekturen und nicht aufgelöste Widersprüche |
| `SHELL_AND_REUSE_CONTRACT_V6.md` | volle Erhaltungsliste, zwei Fenster/Bereiche, gemeinsame Modulpflege |
| `STATE_AND_HANDOVER_TEMPLATES.md` | konkrete Dateien und JSON-/CSV-Schemafelder für neue Sitzungen |
| `OUTPUTS_AND_HISTORY_POLICY_V6.md` | Quell-/Ergebnis-Historisierung auch von früheren generischen Ausgaben |
| `SRC_README_PATCH_PROPOSAL_V6.md` | vollständiger, sicherer Entwurf für bestehende `src/steps-0.00/README.md` |
| `GOVERNANCE_AND_INDEX_PATCH_PLAN_V6.md` | präziser PR-Plan für Root-`AGENTS.md`, README, SKILL und Promptindex |
| `V5_TO_V6_CHANGELOG_AND_GAP_REVIEW.md` | unabhängige Änderungsliste und offen gebliebene Ausführungsschritte |

**Veröffentlichungsgrenze:** Dieses V6-Dokument liegt zunächst nur als Importvorschlag vor. Beim Schreiben in GitHub darf kein bestehendes Dokument überschrieben und kein historischer Bericht stillschweigend gelöscht werden.
