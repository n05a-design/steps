# Beitragen zu STEPS

- Vor Änderungen ein Issue mit **Problem, Scope, erwarteten Ergebnissen und Quellen** eröffnen.
- Ändere Domänenlogik in [`src/steps/`](src/steps/) und App-Integrationen in [`app/`](app/). Neue Wissensinhalte benötigen Quellenregister und Lizenzstatus. Prüfe bei API-Änderungen die [generierte Referenz](docs/theory/API.md) und aktualisiere betroffene [Funktionsgrenzen](docs/IMPLEMENTATION.md).
- Externe PDFs, Webseiten-Snapshots, Audio, MIDI, Screenshots oder Fremdquellcode **nicht** ungeprüft hochladen.
- Jede PR enthält Beschreibung, gegebenenfalls Migration-Manifest, Auswirkungen auf Dateipfade, Tests und offengelegte Einschränkungen.
- Tests müssen deterministisch/offline reproduzierbar sein. Bei Notation H/B/Bb und harmonischer Mehrdeutigkeit explizite Testfälle vorsehen.
- Alte und neue Bibliotheksversionen nicht durch reine Dateinamenähnlichkeit zusammenführen; fachliche Unterschiede dokumentieren.
- MPL-2.0 beachten; für fremde Inhalte eigenständige Nutzungsrechte vorlegen.
