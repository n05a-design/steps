# Verbindlicher Vertrag für sämtliche KI-Aufträge (keine doppelte Kopie pro Prompt)

## Ziel und Quellenhierarchie

**Zuerst** das jeweilige Git-Repository selbst, auf einem nachgewiesenen Commit; **danach** die kanonischen Dokumente: Glide `01_Repository/Glide/AGENTS.md`, `src/glide/README.md`, `docs/ARBEITSRICHTUNG.md`, `docs/DESIGN_RICHTLINIEN.md`, QA/Architektur/Plan; Steps `AGENTS.md`, `docs/architecture/`, `docs/project/`, `schemas/`, `knowledge/sources/`, `research/gaps/`. Die neue V2-Dokumentation ist ein **Audit und ein RFC**, keine automatisch verbindliche Entscheidung. Alte Prompts/Handover mit ihrem jeweiligen Datum lesen, aber nicht gegen aktuelle Code-/Owner-Entscheidungen als 'heutige Wahrheit' verwenden.

## Verbindlicher Eingangsnachweis pro Auftragsrunde

`repo`, `main SHA`, `Arbeitsbranch SHA`, `git status`, vorhandene geänderte Dateien, Python/Tcl/Tk-Versionen wo anwendbar, relevanter Datenformatstand, dokumentierte fremde Rechte, CI-Status und Quell-/Liefer-Hash. Ohne direkten Zugriff `UNAVAILABLE` deklarieren und keine eigens erdachten Code-/Testbeweise ausgeben. Keine Dateien mit echten Nutzer-/Privatpfaden in Berichten oder Tests. Keine unautorisierten Netzwerkaufrufe bei Offline-Evaluierung.

## Arbeitsgrenzen

Wenn ein Auftrag `ANALYSE` heißt: **keine Code-, Doku- oder Git-Änderungen**, nur Befund/Entwurf/Prüfspezifikation. Wenn `IMPLEMENTIERUNG NACH FREIGABE` heißt: nur in isoliertem Worktree/Branch und beauftragtem Dateiscope, keine unbeabsichtigten Nebenarbeiten. Keine irreversiblen Operationen (`git reset --hard`, force push, merge, tag, release, Löschung von Quellen/Tests, History Rewrite, Änderung öffentlicher Assets) ohne ausdrückliche Besitzerfreigabe. Keine automatischen Migrations- oder Publishskripte auf echten Nutzerdaten.

**Rechtsgrenze:** Fremde Bücher, PDFs, kommerzielle MIDI, Third-Party-Screenshots/-HTML nicht ohne einzeln belegte Rechte kopieren, zusammenfassen oder als öffentliche Fachdaten ausgeben. Rechteprüfung ist ein Gate, keine stillschweigende Legal-Freigabe. Bei sichtbarem Rechtsrisiko nur Metadaten und Beobachtung, keinerlei zusätzliche Redistribution.

## Pflichtprüflogik

- Anforderungen nach `USER_REQUIREMENT`, Bestand nach `VERIFIED_REPO`, Tests nach `ACTUALLY_EXECUTED` (mit Commit/Command/OS/Runtime, Exit, Skips), historische Berichte `DOCUMENTED_QA`, Ideen `PROPOSED` und offene Punkte `UNKNOWN` trennen.
- Vor Implementierung eine reproduzierbare **rote Gegenprobe** für den eigentlichen Defekt/Vertrag definieren; Tests nicht weichmachen.
- Tk-Widgets und UI-/Eventloop-Zugriffe nur im zuständigen Interpreterthread, `after`/Eventhandler/Focus/Font/DPI/Modalität/Teardown prüfen.
- Jede Datenmutation über den vorgesehenen Produktpfad; Undo/Redo, SaveResult, Cacheinvalidierung, neue Object-IDs/Tests und Migration beurteilen.
- Keine globalen Daten-/Cache-/Lock-/Settings-Pfade im Core; Testroot **vor** Import injizieren, Dateizugriffe auf Glide-Produktionsverzeichnisse untersagen.
- CI-Produktprüfung, Native-UI-Paket, menschliche Bedien- und Rechtsabnahme sind getrennte Tore; nicht 'alle Tests bestanden' behaupten, wenn relevante Achsen fehlen.

## Verbindliche Übergabeform

1. **Scope:** Auftrag/Excluded; Quell-SHA/Branch/Runtime, Inputs mit Pfaden.
2. **Befunde:** Tabelle Hypothese → Primärbeleg (Datei/Zeile) → Auswirkung → Schwere → Test.
3. **Entscheidungen:** `ACCEPTED` nur nach Owner-Freigabe; Alternativen/Aufwand/Gegenargumente dokumentiert.
4. **Änderungen:** exakte `git diff --stat`, geänderte Dateien und Funktionen, keine stillen Side Effects.
5. **Prüfung:** `PASSED`, `FAILED`, `SKIPPED`, `NOT_RUN`, Befehl, Testdatenort, Python-/Tk-/OS, Commit/Hashes; rote Gegenprobe.
6. **Gates:** Ergebnis `READY_FOR_REVIEW / BLOCKED / READY_FOR_RELEASE` mit Gründen und ausdrücklich offenen manuellen Prüfungen; keinen unautorisierten Releaseclaim.
7. **Nächster kleinster Schritt:** eine begrenzte, delegierbare Folgeaufgabe mit zugeordnetem Risiko, Verantwortlichem und Abnahmekriterium.

**KI-Rolle:** Architekturvarianten kritisch vergleichen; keine bloße Übernahme früherer Assistenz-Empfehlungen. Jede wichtige These mit mindestens einem gezielten Gegenbeispiel angreifen. Ergebnisse im passenden kanonischen Dokument statt als zweite parallele Gesamtübersicht festhalten.
