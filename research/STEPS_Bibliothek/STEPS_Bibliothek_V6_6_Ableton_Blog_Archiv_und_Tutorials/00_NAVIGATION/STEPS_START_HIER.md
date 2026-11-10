# STEPS Bibliothek V5.2 – nach Stichworten strukturiert

**Stand:** 08.11.2026 · **Art:** Dateistruktur-, Such- und Abdeckungs-Audit · **Bibliotheksversion:** 5.2.0 (keine Steps-App-Version).

## Erledigt

- **278 Dateien** aus dem tatsächlich vorhandenen V5.1-Archiv als inhaltlich unveränderte Kopien neu eingeordnet; SHA-256 zu jeder Ursprungsdatei wird 1:1 geführt.
- Lesbare, thematische Dateinamen: `STEPS_<FACHGEBIET>__<STICHWORTE>__<FUNKTION>__<VERSION>.<EXT>`.
- Aktuelle V5- und V5.1-Arbeitsstände sind in den Fachordnern direkt erreichbar; V1/V3/V4 liegen in `90_HISTORIE/`, nicht versehentlich als Hauptreferenz.
- `00_NAVIGATION/STEPS_DATEIENINDEX_ALLE_278.csv` und `.json`: sämtliche alten Pfade, neue Pfade, Keywords, Zwecke, Versionen, Quellhashes und Prüfstatus.
- `00_NAVIGATION/STEPS_ABDECKUNG_UND_LUECKEN.md`: 53 Unterthemen mit Evidenz, Lücken und Priorität.
- Exakte ursprüngliche V5.1-Dateien stehen zusätzlich als ZIP in `99_ORIGINALARCHIV/`.

## Navigation nach sechs fachlichen Kernbereichen

1. `01_MUSIKTHEORIE/` – Notation, Intervalle, Skalen, Modi, Rhythmus und Theorie.
2. `02_HARMONIE/` – Harmonik, Funktionen, Modalität, Jazz, Pop und stilistische Lesarten.
3. `03_CHORD_PROGRESSIONS/` – Akkordprogressionen, Variationen, Harmonischer Rhythmus und Reharmonisierung.
4. `04_COMPOSING/` – Motivik, Themen, Form, Kompositionstechniken, Partituren und MIDI-Studien.
5. `05_DRUMS_RHYTHM_GROOVE/` – separat gehaltene Drum-Progressions und Genre-Programming.
6. `06_PRODUCER_TOOLS/` – separat gehaltene EQ-, Sounddesign-, Sampling- und Produktionsforschung.

Ergänzende Ebenen: `07_KOGNITION_STIL_KULTUR`, `08_COMPUTATIONAL_MUSIC`, `09_PRODUKT_DIDAKTIK_SKILL`, `10_QUELLEN_LIZENZEN`, `11_VALIDIERUNG_QUALITAET`, `12_CODEX_AUFTRAEGE`, `13_GOVERNANCE`, `14_DATENMODELLE`, `15_TOOLS_SKRIPTE`.

## Arbeitsprinzip und Relevanz

**Weshalb eine Datei geführt wird**, steht bei jedem Datensatz im Dateiverzeichnis (`why_in_library`). Dateien werden nicht allein nach dem Namen einer Methode eingruppiert: eine MIDI-Datei ist ein musikalisches Artefakt; ein Forschungsbericht ist ein Befund/Arbeitsstand; ein Codex-Prompt ist ein Auftrag; eine Bibliografie liefert Metadaten, keine zwangsläufig gelesenen Primärquellen.

**Wichtig:** Die zeitliche „historisch/aktuell“-Klassifikation beschreibt nur, ob die Datei in dieser Dokumentationssammlung der jüngste Arbeitsstand ist. `aktuell` bedeutet ausdrücklich nicht `wissenschaftlich geprüft` oder `in Steps implementiert`.

**Nicht enthalten:** die privaten HTML-Originale und Lehrtexte aus dem authentifizierten Kursportal (nur Register und selbstständig formulierte Notizen); die tatsächlich lokal im Steps-Projektordner angekündigten originalen Kurs-MIDIs; die 20 ursprünglichen PDF/TXT-Originale; das verifizierte Git-Repository oder eine vollumfänglich geprüfte wissenschaftliche Bibliografie.

## Wo anfangen?

1. `00_NAVIGATION/STEPS_STICHWORT_INDEX.md` – aktive Dateien und ihr Zweck.
2. `00_NAVIGATION/STEPS_ABDECKUNG_UND_LUECKEN.md` – welche Domänen nur teilweise vorhanden sind.
3. `00_NAVIGATION/STEPS_PRIORISIERTES_LUECKENREGISTER.md` – nächste Arbeitspakete.
4. `12_CODEX_AUFTRAEGE/` und `00_NAVIGATION/STEPS_CODEX_UEBERNAHME_V5_2.md` – reale Repo-Integration der neuen Dateistruktur.

## Kein stillschweigender Eingriff ins echte Projekt

Es wurde **kein lokaler Steps-Ordner und kein GitHub-Repository geändert**. Dieses ZIP ist eine eigenständige, nachvollziehbare Arbeitskopie. Codex soll die Struktur zunächst mit dem echten Repo vergleichen und erst anschließend nach Review integrieren.
