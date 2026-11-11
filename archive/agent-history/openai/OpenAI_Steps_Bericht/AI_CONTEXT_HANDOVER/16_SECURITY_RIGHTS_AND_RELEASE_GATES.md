# 16 – Sicherheits-, Rechte- und Release-Gates

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Historisch dokumentierte Befunde

Aus Phase 4.17 und Master-Audit: **33 Fundstellen** in archivierten HTML-/Web-Dumps (`research/STEPS_Bibliothek/`), davon 27 Google API Embed-Key-Treffer (Alerts #1–#3) und 6 AWS-/S3-Scannerfunde. Der Bericht behauptet 15 negative Mutationstests im Secret-Scanner. Scannerfunde sind zunächst Indizien; Eigentümer, tatsächliche Geheimnisqualität und Exposition sind getrennt zu klären.

## Kein Shortcut zur Freigabe

1. Fundstellen in **redigierter Form** inventarisieren, keine vollständigen Tokens ausgeben.
2. Prüfen, ob technisch funktionsfähige Secrets bzw. fremde Client-Keys vorliegen, ohne Live-Aufrufe oder Missbrauch.
3. Offenlegung in Working Tree **und** historischen Git-Blobs unterscheiden.
4. Rechtliche Herkunft und Lizenz der Ableton-Web-/MIDI-Bestände prüfen; Copyright-Rechte sind nicht durch Hash-basierte Isolation geklärt.
5. Besondere Vorsicht: Repository war bei Github-Abruf **public**. Eine vorgeschlagene Privatschaltung ist nicht umgesetzt.
6. Nur Owner darf über OA-0001/0033 entscheiden: History-Rewrite, Branch/Release, Repo-Privatsphäre, Alert-Schließen.
7. Geschützte Materialien nicht in diesen Bericht oder ZIP übernehmen. In dieser ZIP befinden sich nur eigene Dokumentationen und der vom Nutzer hochgeladene Prompt, keine kopierten fremden Musikdaten oder Key-Werte.

## Operative Folgeaufträge

- Sicherheitsreview mit Rohdatenzugriff nur in geeigneter autorisierter Umgebung; keine Secret-Echos in CI-Logs.
- Rechtliche Maßnahmen mit ggf. fachkundigem Rechtsrat, Lizenzprüfung und dokumentierter Entscheidung.
- Nach einer genehmigten Remediation ausführbare Guards lokal/remote und Git-Geschichte nachprüfen.
