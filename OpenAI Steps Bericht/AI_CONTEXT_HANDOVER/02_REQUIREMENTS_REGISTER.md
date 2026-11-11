# 02 – Anforderungsregister (REQ)
**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

| ID | Herkunft | Anforderung | Zustand / Sicherheit | Nachweisbezug |
|---|---|---|---|---|
| REQ-001 | Nutzer | Evidenzbasierte, tiefgegliederte Musikbibliothek vor Featureentwicklung | teilweise / Bibliothek gemeldet | Master-Audit, 01-14 |
| REQ-002 | Nutzer | Musiktheoretische Korrektheit, Belege, Terminologie und Didaktik | teilweise / Prüfclaims | Master-Audit; 66 Claims |
| REQ-003 | Nutzer | Vollständige Bestandsinventarisierung inkl. nicht versionierter Quellen | gemeldet, lokal X | 3.947 Dateien laut Agent |
| REQ-004 | Nutzer | Klare kanonische Kategorien und M01–M12 Wissensontologie | gemeldet | Wissensaudit 02, 06 |
| REQ-005 | Nutzer | Beziehungen referenziell und semantisch prüfen | gemeldet, Quellcode teilweise G | 97 Relationen |
| REQ-006 | Nutzer | Fehler korrigieren, nicht nur auflisten | gemeldet | ERR-001–037 |
| REQ-007 | Nutzer | Wissenslücken nach Typ A–I schließen, Quellen nachliefern | teilweise | 04_LUECKENANALYSE; 1.525 Metadaten |
| REQ-008 | Nutzer | Duplikate und Widersprüche ohne Informationsverlust konsolidieren | gemeldet | 10_DOKUMENTATION |
| REQ-009 | Nutzer | Genre-Atlas mit fachlicher Trennung von Tendenz/Regel | gemeldet | 9 Kern-Genres |
| REQ-010 | Nutzer | Piano Learning Path mit Abhängigkeiten und abgestufter Didaktik | gemeldet | P01–P19 |
| REQ-011 | Nutzer | Akkord- und Drum-Referenzbibliotheken kanonisch halten | gemeldet | PROG-001–028/PAT-001–031 |
| REQ-012 | Nutzer | ADR-IDs unverändert und nachvollziehbar | Phase 4.17 gemeldet/G Commit | ADR-002/005/011/012 |
| REQ-013 | Nutzer | PROG-021 Urfassung und PROG-028 getrennt erhalten | Phase 4.17/5.1 gemeldet | PROG021_HISTORICAL_RECONCILIATION |
| REQ-014 | Nutzer | Headless Python-Kern von GUI und GLIDE getrennt | G Dateien, U Tests | src/steps/theory, progression |
| REQ-015 | Nutzer | H/B-, B/Bb-, enharmonische Schreibweisen korrekt | U/G Implementierungsdateien | pitch/interval/chord |
| REQ-016 | Nutzer | Chord-/Voicing-/Stimmführungsengine erstellen | U/G Commit | chord.py, voice_leading.py |
| REQ-017 | Nutzer | 28 Progressionen programmatisch erschließen | U/G Testquelle | engine.py/test_progression_engine.py |
| REQ-018 | Nutzer | Golden Cases ehrlich nach Ausführung vs. Spezifikation trennen | gemeldet, Dokument G | 67/131; später 28 Tests |
| REQ-019 | Nutzer | Tests reproduzierbar unter Python 3.11/3.12 in CI | Workflow G; Run queued | python-tests.yml |
| REQ-020 | Nutzer | Schlüssel-Alerts sicher behandeln, keine Secrets im Bericht | offene Freigabe | OA-0033, 33 Fundstellen |
| REQ-021 | Nutzer | Fremdmaterial und Git-Historie vor Release rechtlich klären | offene Freigabe | OA-0001 |
| REQ-022 | Nutzer | Keine direkten Änderungen nach main ohne kontrollierte Freigaben | Arbeitsregel; PR #9 bereits gemerged | Git-Prozess |
| REQ-023 | Nutzer | GLIDE-Verzeichnis unangetastet lassen | gemeldet/inhaltlicher Ausschluss | Rule 9 |
| REQ-024 | Nutzer | Vollständige Chat-Arbeitsrekonstruktion beider Seiten inkl. Agenten | teilweise, Informationslücke | hochgeladener Masterprompt |
| REQ-025 | Nutzer | Behauptungen, Umsetzung und Tests sauber unterscheiden | in Bericht umgesetzt | Evidenzlegende |
| REQ-026 | Nutzer | Übergabemappe mit Reifeprüfung, Startprompt und Quellenregister | in diesem ZIP umgesetzt | 12,13,MANIFEST |
| REQ-027 | Nutzer | ZIP-Dateiname OpenAI Steps Bericht.zip | umgesetzt | Archivdatei |
| REQ-028 | Assistentenvorschlag | Phase 5.2 Chord-/Voicing-/Recommendation-Ausbau | nicht genehmigt / Vorschlag | frühere Assistentenantwort |
| REQ-029 | Nutzer | Keine GUI-Codierung vor ADR-001-Entscheidung | offene Freigabe | ADR-001 |
| REQ-030 | Nutzer | Drum-Scope nicht vor ADR-002 formell erweitern | offene Freigabe | ADR-002 |

## Prüfregel
„gemeldet“ bedeutet keine unabhängige Abnahme. Anforderungen REQ-001 bis REQ-027 und REQ-029/030 wurden aus Nutzerwünschen oder übergebenen Berichten rekonstruiert; REQ-028 ist **nur** ein Assistentenvorschlag. Für formale Entscheidungen siehe 03.
