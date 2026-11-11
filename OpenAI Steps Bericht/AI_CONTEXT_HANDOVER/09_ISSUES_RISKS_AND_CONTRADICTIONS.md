# 09 – Offene Fehler, Risiken und Widersprüche

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

| ID | Priorität | Problem | Nachweisstand | Nächste Maßnahme |
|---|---|---|---|---|
| ISSUE-001 | P0 | Historische Google-/AWS-Fundstellen in öffentlichen Git-Blobs: 33 Stellen gemeldet | U, nicht als geschlossen belegt | Alle Alerts einzeln prüfen; Drittanbieter-/Eigentümerschaft, Exposition, Remediation und Owner-Freigabe |
| ISSUE-002 | P0 | Lizenz-/Urheberrechtsrisiko historischer Ableton-Web-/MIDI-Inhalte | U, OA-0001 offen | Rechts-/Lizenzbewertung, keine ungeprüfte Weiterverbreitung, ggf. genehmigter History-Cleanup |
| ISSUE-003 | P0 | Repo ist bei GitHub **public** trotz Empfehlung Option A (temporär privat) | G Repo-Metadaten | Eigentümerentscheidung ohne automatische Statusänderung |
| ISSUE-004 | P1 | Phase-5.1-Remote-Python-Matrix bei Abfrage nur `queued` | G API | CI-Runs/Jobs/Logs und Merge-Commit-Check erneut auslesen |
| ISSUE-005 | P1 | `main` hat PR #9 schon gemerged; frühere Branch-only-Aussagen überholt | G Commit/PR | `main` als aktuellen Code-Einstieg nehmen, Basis vor neuen Arbeiten aktualisieren |
| ISSUE-006 | P1 | 1.525 Quellen nur Metadaten; frühere „vollständig verifiziert“-Formulierungen überdehnt | U/G Bericht | Themenrisikobasierte Vollprüfungen, Claim-Belege einzeln kontrollieren |
| ISSUE-007 | P1 | 198 Golden Cases vs. 28 neue Golden-Testmethoden keine automatische 1:1-Abdeckung | U/G Report | Abdeckungsmatrix Fall→Prüfmethode→Assertion erstellen |
| ISSUE-008 | P1 | Metrikaxiome und globale Stimmführungsoptimierung mit Contraints semantisch unterschiedlich | D, Bericht behauptet metrische Beweise | Algorithmus/Definitionsbereich und musikwissenschaftliche Gegenproben prüfen |
| ISSUE-009 | P1 | ADR-001/002/005, OA-0001/OA-0033 formal nicht entschieden | U | Owner-Register mit signierten Optionen aktualisieren |
| ISSUE-010 | P1 | Original-Chattranskripte, externe Agenten-Logs und lokale Audits fehlen für 100%-Übergabe | X | Vollständigen Chat- und Auditexport bei Quelle besorgen |
| ISSUE-011 | P2 | `66 Claims` mit `46 E1 +20 E2` und später `26 Standardwerke` – verschiedene Maße | U/G Berichte | Claims, Werke und Quellenkennungen sauber als verschiedene Entitäten zählen |
| ISSUE-012 | P2 | Historische PROG-021-Überschreibung und ADR-ID-Kollisionen | U; als korrigiert gemeldet | Identitätsregressionen beibehalten und Commit/diff prüfen |
| ISSUE-013 | P2 | „0 Mojibake“/„0 Secrets“ gelten nur für Scannerdefinition, nicht universell | U | Prüfbereich und Suchregeln offenlegen; History/Binaries gesondert betrachten |
| ISSUE-014 | P2 | Hohe Readiness-Konfidenz („100 %“) suggeriert mehr Sicherheit als Testumfang | D | Risiko-/Feature-Matrix statt absoluter Sicherheit |

## Besonders kritische fachliche Fragen

**Enharmonik:** Pitch-Class-Äquivalenz ist keine notationsseitige Gleichheit. Eine API muss die Art der Gleichheitsprüfung explizit machen; Registertests dürfen nicht nur MIDI-Gleichheit prüfen.

**Stimmführung:** Bei gleichen geordneten Vektordimensionen kann die L1-Norm eine Metrik sein. Wird Stimmenzuordnung optimiert, Stimmenzahl verändert, auf PC-Äquivalenz quotientiert oder unter Verbotsregeln gefiltert, muss die mathematische Beweisführung angepasst werden. Zusätzlich sind stilabhängige Gegenbeispiele erforderlich.

**Security:** „Zero unmasked secrets“ im Working Tree bedeutet nicht „keine öffentlich verfügbaren historischen Secrets“, und ein Scanner-Guardrail ist keine Rechtefreigabe. Meldung von 27 Google- plus sechs AWS-Funden nicht mit „vier eindeutigen Schlüsseln“ oder anderen Zahlen gleichsetzen, wenn Zähleinheiten voneinander abweichen.
