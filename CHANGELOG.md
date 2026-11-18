# Änderungsprotokoll

## Unreleased – App und Python-Kern

- **Verhaltensänderung:** `NoteSpelling.transpose_diatonic` löst bei Stufen- und Halbtonwerten, die kein Intervall bilden, `InvalidAlterationError` aus, statt still die Oktave zu verschieben (zuvor C4 `(0, 11)` → Cb5). Gültige Intervalle sind unverändert.
- **Verhaltensänderung:** `knowledge/research/run_golden_test_suite.py` schreibt ohne Argumente keine Dateien mehr; `--output-dir` exportiert, `--update-baseline` erneuert die versionierten Berichte.
- Entscheidungen ADR-001, 003, 004, 006, 007 und 013–017 angenommen (v0.1 = Akkorde + MIDI-Export, Lizenz MPL-2.0/CC BY 4.0); siehe [Register](decisions/DECISION_REGISTER.md). Der MIDI-Export ist im Kern und in den Prototyp-Pfaden implementiert und Bestandteil des v0.1.0-Releases; externe DAW-Abnahme und vollständiger Desktop-Produktablauf bleiben getrennte Nachweise.
- Tonhöhen, Intervalle, Akkordauflösung, Stufenparser und Stimmführung sind als Python-Schnittstellen verfügbar.
- Dur- und Moll-Aliasse mit `M` und `m` werden unterschieden. Unlösbare Voicing-Vorgaben melden einen Fehler.
- App-Adapter und Lernmaterial verwenden dieselbe kuratierte Progressionsdatei.
- Logo und App-Symbol liegen als [Master](design/brand/README.md) im Repository. `app.brand` stellt sie der App zentral bereit, die Root-README zeigt das App-Symbol.
- Die Root-README ist als Projektseite neu gegliedert und erscheint auf der GitHub-Startseite. Die frühere `.github/README.md` heißt jetzt [`GITHUB_UND_CI.md`](.github/GITHUB_UND_CI.md).
- Der [Implementierungsstand](docs/IMPLEMENTATION.md) und die [generierte API-Referenz](docs/theory/API.md) beschreiben den Entwicklungsstand und die verfügbaren Funktionen.
- 1.0.0-Zielbild, Ist-Stand und offene Freigabegates konsolidiert; Produkt- und GitHub-Dokumentation gegen den aktuellen Stand ergänzt.
- Der Desktop-Prototyp ergänzt projektbezogenes Öffnen/Speichern mit Dateiauswahl, Rückfrage bei ungespeicherten Änderungen und sichtbaren Fehlern. Session-Dateien bewahren Tonart und Mollmodus; fehlerhafte Akkordsymbole werden vor einem Zustandswechsel abgewiesen.
- Der Desktop-Prototyp bietet einen persistierten Sprachschalter für Englisch/Deutsch/System, lokalisierte Desktop- und CLI-Texte sowie eine MIDI-Dateiauswahl mit sichtbarem Exportfehler. Notationskonvention und Projektdaten bleiben unabhängig von der UI-Sprache; native Plattform- und Übersetzungsabnahme stehen aus.
- Die Oberfläche verbindet Akkord-Ändern/Entfernen/Verschieben und Undo/Redo mit der Progressionssession. Ungültige Akkorde und das Entfernen des letzten Akkords werden mit lokalisierten Hinweisen abgewiesen; Tastenkürzel sind unter Windows/Linux und macOS verfügbar.
- Tonart, Dur-/Mollmodus, Tempo und Taktart können gemeinsam im Desktop gesetzt und als eine Session-Änderung rückgängig gemacht werden. Eingaben werden validiert und in Projekten sowie MIDI-Metadaten gespeichert. Pro Akkordereignis lässt sich die Startposition als `Takt:Zählzeit:Tick` eingeben; Dauer und gespeicherter/exportierter Zeitpunkt bleiben absolute Tickwerte. Ein Taktartwechsel ändert nur die Positionsprojektion, nicht die Ereigniszeit.
- Beim Öffnen eines beschädigten Projekts meldet die Desktop-Oberfläche jetzt EN/DE lokalisiert, dass ein gültiges Backup geladen wurde. Die Storage-API liefert parallel einen kompatiblen Load-Status mit Backup-Pfad; bestehende `load_project()`-Aufrufe behalten ihren Rückgabewert.
- Projektdateien werden über einen expliziten 0.x→1.0.0-Migrationspfad und dokumentierte 1.x-Normalisierungen geladen. Zukunftsschemas mit höherer Major-Version werden weiterhin abgewiesen. Der Load-Status nennt die angewendeten Migration-IDs; fehlende Projekttitel bleiben ein Fehler statt still aufgefüllt zu werden.
- Beim Öffnen eines migrierten Legacy-Projekts zeigt die Desktop-Oberfläche eine lokalisierte EN/DE-Meldung mit den angewendeten Migration-IDs. Die Meldung unterscheidet Projektwiederherstellung aus einem Backup von Schema-Normalisierung.
- Der Projektname lässt sich in der Desktop-Oberfläche editieren und wird gemeinsam mit Tonart, Mollmodus, Tempo und Taktart als eine undo-/redo-fähige Kontextaktion gespeichert.
- Das Python-Wheel enthält jetzt die Desktop-App, Locale-Kataloge, Design-Tokens und Markenressourcen, damit der konfigurierte `steps`-Einstieg und seine Laufzeitressourcen gemeinsam installiert werden.
- GitHub Issue- und PR-Vorlagen, Dependabot-/Release-Notizkonfiguration und ein YAML-/Issue-Form-Prüfworkflow ergänzt. GitHub-Wiki, Projects, Labels und Funding bleiben explizite Inhaberhandlungen.

## Frühere Architekturvorbereitung

- Zielstruktur für App, Domäne, Wissensbasis, Forschung, Design, Entscheidungen und Tests beschrieben.
- Konservative, auditierbare Migration vorbereitet; **keine Aussage über fertigen App-Code**.
- Historische Wissensbibliothek wird als Legacy-Facharchiv abgegrenzt.

> Dieser Abschnitt dokumentiert die frühere Strukturvorbereitung.
