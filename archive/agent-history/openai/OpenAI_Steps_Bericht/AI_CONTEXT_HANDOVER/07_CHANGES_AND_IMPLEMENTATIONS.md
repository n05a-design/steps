# 07 – Änderungs- und Implementierungsregister (CHG)
**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

| ID | Phase | Änderung | Referenz | Evidenz |
|---|---|---|---|---|
| CHG-001 | T-04 / Phase 2 | Scaffold `src/steps/` | 078bc59/PR #4 | K |
| CHG-002 | Phase 3 | Knowledge Curation Skill, Quellenregister | 513fa9c/af6c0bc | K |
| CHG-003 | Phase 4 | M01–M12, Genre-/Piano-/Golden-Test-Wissensbasis | verschiedene Zwischenstände | K |
| CHG-004 | Phase 4.16 | Golden-/Secret-Baseline und Checkpoint | 1657339 | G Commit |
| CHG-005 | Phase 4.17 | ADR-002/005 Identität restauriert; ADR-011/012 registriert | 422ec96 | U/G Commit |
| CHG-006 | Phase 4.17 | PROG-021 Urfassung wiederhergestellt, PROG-028 getrennt | 422ec96 | U/G Commit |
| CHG-007 | Master Audit | 37 Fehlerregistereinträge, BOM/Header/Metadaten | 918d0a7 | U/G Bericht |
| CHG-008 | Phase 4.18 | Knowledge Relations +3 auf 97 Kanten | bb14fce | G Diff |
| CHG-009 | Phase 4.18 | Erste Theorie-Module und 17 neue Tests | bb14fce | U/G Diff |
| CHG-010 | Phase 5.1 | Exceptions, Pitch/Interval/Chord/VoiceLeading erweitert | fe66637 | G Diff/U Verhalten |
| CHG-011 | Phase 5.1 | Progression Engine und Tests hinzugefügt | fe66637 | G Diff |
| CHG-012 | Phase 5.1 | Python-Testworkflow 3.11/3.12 hinzugefügt | fe66637 | G Datei |
| CHG-013 | Integration | PR #9 merge in main | 02f3776 | G PR/Commit |

## Verifikationsregeln
Soweit Commitdiffs eingesehen wurden, belegen sie konkrete Dateipfade und Änderungen. Fachliche Vollständigkeit oder Betriebsbereitschaft ergibt sich daraus nicht. Vor neuer Umsetzung Änderungsumfang mit `git show --stat`, `git diff`, `git status` und Testprotokollen gegen aktuellsten Stand prüfen. Keine automatische Daten-/History-Migration.
