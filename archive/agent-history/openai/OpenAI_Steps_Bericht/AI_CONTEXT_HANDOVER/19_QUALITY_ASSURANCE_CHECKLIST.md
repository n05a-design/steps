# 19 – Für künftige Reviews: verbindliche Checkliste

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Quell-/Agentenintegrität

- [ ] Aktuelle Quellen vollständig zugänglich; ggf. Unterschied zwischen Summary und Original markieren.
- [ ] Tatsächlicher aktueller `main`-Commit und Arbeitsbaum dokumentiert.
- [ ] Jeder behauptete Code-/Testabschluss dem ausführenden Commit und Log zugeordnet.
- [ ] Jede Quelle als voll/teil/Metadaten (oder unbekannt) klassifiziert.
- [ ] Keine nicht gestützten 100%-Labels.

## Fachliche Korrektheit

- [ ] Enharmonische Schreibweisen einschließlich Doppelvorzeichen, Oktavgrenzen, Transpositionsrundläufe.
- [ ] Intervallqualität vs. Halbtonzahl und Intervallumkehr.
- [ ] ChordDefinition vs. Voicing; reduziertes `7#11` nicht als vollständiges Intervallset.
- [ ] Unterschied L1-Produktmetrik vs. Stimmführungsoptimierung mit Constraints.
- [ ] PROG-021/028 identitätsgetreu.
- [ ] Wissensgraph-Relationssemantik, Genretendenz vs. Regel.

## Security/Release

- [ ] Alle 33 historischen Findergebnisse und 3 Alerts sicher/redigiert untersucht.
- [ ] OA-0001/OA-0033 nicht ohne formale Owner-Freigabe geschlossen.
- [ ] Keine Lizenz-/Secret-Rohdaten in Archiv oder Commit.
- [ ] UI nur nach ADR-001; v0.1-Scope nach ADR-002; Notennamen nach ADR-005.

## Test-/Dokumentation

- [ ] Python 3.11/3.12-Runs und Logs tatsächlich grün.
- [ ] 115 Testmethoden nachvollziehbar zählen und Commit fixieren.
- [ ] 198 Golden-Referenzfälle nicht mit 28 Testmethoden verwechseln.
- [ ] Dokumentationslinks und Quellenregistrierungen gültig.
- [ ] Ungeprüfte Informationen ausdrücklich als solche benannt.
