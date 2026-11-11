# 11 – Quellen- und Artefaktindex
**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

| ID | Typ | Quelle | Evidenz | Einschränkung |
|---|---|---|---|---|
| SRC-001 | Primär: aktuelle Nutzerbeiträge | Phase 4.17, Master-Audit, 4.18, 5.1 Abschlussberichte in diesem Chat | U | im aktuellen Chat, nicht vollständig wortgleich in diesem Paket |
| SRC-002 | Primär: aktueller Assistent | Master-Audit-, Phase-4.18-, Phase-5.1-Prompts und Bewertungen | A | aus aktuellem Chat rekonstruiert |
| SRC-003 | Primär: Upload | Pasted text(10).txt: 1541 Zeilen Master-Übergabeprompt | U | Original unter QUELLEN/ |
| SRC-004 | GitHub Repo Metadaten | https://github.com/n05a-design/steps | G | public; default branch main |
| SRC-005 | GitHub Commit | https://github.com/n05a-design/steps/commit/422ec962650e19a60b8c58520ea039a99c3befcb | G | 4.17 Commit und Nachricht |
| SRC-006 | GitHub Commit | https://github.com/n05a-design/steps/commit/918d0a7105fabecbdb015f6bfe9ccc876e7f8ce2 | G | Master-Audit Commit und Nachricht |
| SRC-007 | GitHub Commit | https://github.com/n05a-design/steps/commit/bb14fce85a8136560add49ff724a1b0d982f47ab | G | Phase 4.18 Commit und Diffauszüge |
| SRC-008 | GitHub Commit | https://github.com/n05a-design/steps/commit/fe6663747250bf73ff28f4b7c591e8cf42f799d0 | G | Phase 5.1 Commit, Parent und Dateiliste |
| SRC-009 | GitHub Merge Commit | https://github.com/n05a-design/steps/commit/02f3776b24be52e3f00a973b3ad50f82d95e4abd | G | PR #9 Merge in main |
| SRC-010 | GitHub PR | https://github.com/n05a-design/steps/pull/9 | G | closed/merged als Commit-Metadaten bestätigt |
| SRC-011 | GitHub Master-Audit-Bericht | https://github.com/n05a-design/steps/blob/918d0a7/knowledge/research/14_ABSCHLUSSBERICHT.md | G | Datei eingesehen; Inhalt berichtet Testergebnisse |
| SRC-012 | GitHub 4.18 Bericht | https://github.com/n05a-design/steps/blob/bb14fce/knowledge/research/PHASE4_18_MASTER_INTEGRATION_REPORT.md | G | Datei eingesehen |
| SRC-013 | GitHub 5.1 Bericht | https://github.com/n05a-design/steps/blob/fe66637/knowledge/research/PHASE5_1_COMPLETION_REPORT.md | G | Datei eingesehen; 115-Tests-Verteilung |
| SRC-014 | GitHub Workflow | https://github.com/n05a-design/steps/blob/fe66637/.github/workflows/python-tests.yml | G | Dateiinhalt 3.11/3.12 und Testkommandos |
| SRC-015 | GitHub Testcode | https://github.com/n05a-design/steps/blob/fe66637/tests/test_progression_engine.py | G | Testquelle und 12 deklarierte test_ Methoden |
| SRC-016 | GitHub Actions Run | https://github.com/n05a-design/steps/actions/runs/43097534590 | G | Python Matrix beim Abruf queued, kein Erfolgsbeleg |
| SRC-017 | GitHub Actions Run | https://github.com/n05a-design/steps/actions/runs/43097015761 | G | Python Matrix beim Abruf queued |
| SRC-018 | Historische ältere Chats | Gesprächszusammenfassungen ab 08.–11.11.2026 | K | keine vollständigen Originaltranskripte |
| SRC-019 | Historische lokale Audits | %LOCALAPPDATA%\StepsAudit\20261111T2100_Phase4_17 und 20261111T2130_MasterAudit | U/X | Pfade bekannt, lokale Bytes nicht zugänglich |
| SRC-020 | Historische Open Tasks | %LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md | K/X | Pfade bekannt, lokale Bytes nicht zugänglich |

## Nicht verfügbare, aber bekannte weitere Dateien
`STEPS_Antigravity_Masterprompt_V6_2026-11-10.md`, `30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md`, `Steps_Projektuebersicht_2026-11-10.md`, `STEPS_Masterreview_V4_2026-11-10.md`, `Master-Research-Prompt.md`, Projekt-Auditpakete unter `%LOCALAPPDATA%`, Antigravity-Sitzungslogs, vollständige vorherige Chattranskripte. Existenz/Bedeutung aus früheren Nachrichten, **nicht** Teil des vorliegenden Dateipakets.

## Source-of-Truth-Regel
Bei Konflikten besitzt ein tatsächlich eingesehener Dateistand zum angegebenen Commit Vorrang vor zusammenfassender Statusmeldung für den engen überprüften Fakt. Wissenschaftliche Korrektheit bleibt getrennt und ist nicht durch Commit-Existenz belegt.

## Nachtrag – Master Audit V2

- **SRC-021 (U):** Vom Nutzer im Chat übermittelter Text „STEPS – MASTER-AUDIT V2 GESAMTBERICHT“, Prüfdatum 11.11.2026, lokales Originalpaket `%LOCALAPPDATA%\StepsAudit\20261111T2200_MasterAuditV2\` / `Antigravity_MasterAuditV2_Bericht.zip` **nicht direkt zugänglich**.
- **SRC-022 (G):** `https://github.com/n05a-design/steps/blob/main/README.md` – am 11.11. abgefragt; Root-README veraltet.
- **SRC-023 (G):** `https://github.com/n05a-design/steps/blob/main/decisions/DECISION_REGISTER.md` – zwölf `proposed`-Einträge.
- **SRC-024 (G):** `https://github.com/n05a-design/steps/blob/main/docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md` – ausdrücklich nicht-kanonischer Snapshot mit 33 OA-Zeilen (1 erledigt, 1 in Arbeit, 5 Owner-Entscheidung, 26 offen) zu älterem Stand.
- **SRC-025 (G):** GitHub `main` Git-Tree-Snapshot: 3.975 versionierte Blobs, davon 1.580 Legacy-Glide und 14 Dateien in `src/steps/`.
- **SRC-026 (W):** `https://www.iso.org/standard/78176.html` – ISO/IEC 25010:2023 (neun Merkmale).
- **SRC-027 (O/D):** Kritischer Vergleich und Matrix: `23_ANTIGRAVITY_MASTERAUDIT_V2_ABGLEICH.md`, `24_MASTER_AUDIT_V2_EVIDENCE_MATRIX.csv`.

## Nachtrag – Master Audit V2

- **SRC-021 (U):** Vom Nutzer im Chat übermittelter Text „STEPS – MASTER-AUDIT V2 GESAMTBERICHT“, Prüfdatum 11.11.2026, lokales Originalpaket `%LOCALAPPDATA%\StepsAudit\20261111T2200_MasterAuditV2\` / `Antigravity_MasterAuditV2_Bericht.zip` **nicht direkt zugänglich**.
- **SRC-022 (G):** `https://github.com/n05a-design/steps/blob/main/README.md` – am 11.11. abgefragt; Root-README veraltet.
- **SRC-023 (G):** `https://github.com/n05a-design/steps/blob/main/decisions/DECISION_REGISTER.md` – zwölf `proposed`-Einträge.
- **SRC-024 (G):** `https://github.com/n05a-design/steps/blob/main/docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md` – ausdrücklich nicht-kanonischer Snapshot mit 33 OA-Zeilen (1 erledigt, 1 in Arbeit, 5 Owner-Entscheidung, 26 offen) zu älterem Stand.
- **SRC-025 (G):** GitHub `main` Git-Tree-Snapshot: 3.975 versionierte Blobs, davon 1.580 Legacy-Glide und 14 Dateien in `src/steps/`.
- **SRC-026 (W):** `https://www.iso.org/standard/78176.html` – ISO/IEC 25010:2023 (neun Merkmale).
- **SRC-027 (O/D):** Kritischer Vergleich und Matrix: `23_ANTIGRAVITY_MASTERAUDIT_V2_ABGLEICH.md`, `24_MASTER_AUDIT_V2_EVIDENCE_MATRIX.csv`.
