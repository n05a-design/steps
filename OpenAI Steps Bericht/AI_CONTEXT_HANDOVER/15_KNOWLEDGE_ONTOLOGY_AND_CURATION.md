# 15 – Wissensbibliothek, Taxonomie, Kuration

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Kanonische Inhalte (aus dem Master-Audit berichtet)

| Bestand | Umfang | Prüfungstiefe dieser Übergabe |
|---|---:|---|
| M01–M12-Domänen | 12 Domains | Bericht/Architektur, nicht alle Quelldaten selbst geprüft |
| Akkordprogressionen | PROG-001–028 | Phase-5.1-Testquelle teilweise eingesehen; alle 28 im Bericht |
| Drum-Grooves | PAT-001–031 | nicht nochmals jeden Pattern-Inhalt geprüft |
| Piano-Module | P01–P19 | didaktische Abdeckung als Agentenmeldung |
| Wissensgraph | 97 Kanten (CR 38, REL 36, CDR 23) | +3 Kanten im Diff G, Grundbestand U |
| Genres | 9 | Details aus Master-Audit U |
| Quellen | 1.895 | 344 voll, 26 teil, 1.525 Metadaten; eigene Vollprüfung nein |
| Claims | 66 | registerbezogen gemeldet; einzelner Claim-Belegtest ausstehend |
| Golden Reference Cases alt | 198 | 67 rechnerisch + 131 spezifikatorisch |

## Domänen und Schnittstellen

Die dokumentierte Ontologie unterscheidet Wissensgrundlagen (u. a. Pitch/Notenschrift, Intervalle, Akkorde, Voicing, Progression, Stimmführung, Rhythmus, Stil und Piano-Pädagogik) und technische Modellierung. Im Master-Audit wurde laut Bericht eine disjunkte Entflechtung vorgenommen: M04 abstraktes Voicing-/Akkordwissen, M06 Stimmführung, M10 Klavierergonomie. Prüfe den tatsächlich im Repository definierten vollständigen M01–M12-Katalog, bevor IDs semantisch verändert werden.

## Dauerhafte Identitätsanker

- PROG-021: `Dm9 - Gm9 - Bbmaj9 - A7(b9)`, historisch minor/Neo-Soul; nicht mit PROG-028 überschreiben.
- PROG-028: `Em9 - Am9 - D9 - Gmaj9`, Circle of Fifths Soul Cycle.
- CR-038: PROG-028 → P12, `VOICED_BY` (gemeldet).
- REL-035: PROG-028 → PAT-030, `COMMONLY_PAIRED_WITH`.
- REL-036: PAT-031 → PROG-025, `COMMONLY_PAIRED_WITH`.

## Reale fachliche Grenzen

Evidenzkennzeichen in einem Dateiregister sind nicht dasselbe wie tatsächliches Quellenlesen. Genre-Tendenzen dürfen nicht als zwingende Regeln kodiert werden. Ein automatisiertes Vollständigkeitslabel darf sich nur auf definierte Baselines und Prüfkriterien beziehen; das Wachstum zu weiteren Genres/Instrumenten bleibt ein eigener begründeter Scope.
