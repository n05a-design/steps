# Seiteneffekte der Bibliotheks-Generatoren und -Werkzeuge (16.11.2026)

**Status:** Statische Analyse. **Kein Skript wurde ausgeführt.** Grundlage: Quelltext auf `main` bei `d4692aa`, Python-AST-Auswertung (Dateizugriffe, Lösch- und Umbenennungsaufrufe, Netz-Importe, Unterprozesse, feste Pfade) und gezieltes Lesen der Ein- und Ausgabezeilen. Schließt den Punkt aus der Bestandsaufnahme vom 10.11.2026: „Die bestehenden Bibliotheks-Generatoren wurden nicht ausgeführt und ihre Seiteneffekte sind nicht analysiert.“

## Gesamtbild

- **Kein Skript löscht, verschiebt oder benennt Dateien um.** Kein Skript startet Unterprozesse.
- **Netzzugriff hat nur der Ableton-Blog-Indexer.** Die V6.7-Generatoren enthalten Blog-URLs als Daten und zerlegen sie nur (`urllib.parse`), sie rufen sie nicht ab.
- **Überschreiben:** Die drei V6.7-Generatoren schreiben je ein ZIP mit festem Namen in das aktuelle Arbeitsverzeichnis. Eine vorhandene Datei gleichen Namens wird ohne Rückfrage ersetzt.
- **Schreiben ins Repository:** Fünf V5-Werkzeuge schreiben relativ zum eigenen Speicherort. Aus dem Repository gestartet, legen sie neue Dateien in der Bibliothek an.
- **Passung zum heutigen Ordneraufbau:** Mehrere V5-Werkzeuge erwarten Ordner, die es in der V6.6-Bibliothek nicht mehr gibt (`08_Validierung`, `04_Qualitaet`, `Partituren`, `/mnt/data/…`). Sie würden beim Schreiben abbrechen. Das Abbrechen ist kein Datenrisiko, aber ein Hinweis, dass sie nicht unverändert wiederverwendbar sind.

## Einzelbefunde

Pfade der Bibliothekswerkzeuge relativ zu `research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/`.

### V6.7-Generatoren (`tools/legacy/generators/`)

| Skript | Liest | Schreibt | Netz | Hinweise |
| --- | --- | --- | --- | --- |
| `create_steps_v6_7_patch.py` | optional das V6.6-ZIP (1. Argument) | `STEPS_V6_7_ERWEITERUNG.zip` im Arbeitsverzeichnis, überschreibt | nein | erzeugt Quellenkarten, Labore, Register und SHA-256 im ZIP |
| `create_steps_v6_7_ausbau_02.py` | wie Patch (importiert ihn als Modul) | `STEPS_V6_7_ERWEITERUNG_AUSBAU_02.zip` im Arbeitsverzeichnis, überschreibt | nein | läuft nur, wenn der Patch im Importpfad liegt (gleicher Ordner) |
| `create_steps_v6_7_ausbau_03.py` | V6.6-ZIP und Ausbau-02-ZIP (Argumente oder feste Namen im Arbeitsverzeichnis) | `STEPS_V6_7_ERWEITERUNG_AUSBAU_03.zip` im Arbeitsverzeichnis, überschreibt | nein | bricht ab, wenn die Eingabe-ZIPs fehlen |

### Werkzeuge der V6.6-Bibliothek (`15_TOOLS_SKRIPTE/`)

| Skript | Schreibt | Netz | Bei heutigem Aufbau |
| --- | --- | --- | --- |
| `…AbletonBlog-metadaten-indexer__INDEXER__V6_2.py` | `--out` (Standard `ableton_blog_metadata.csv`) und `….audit.json` im Arbeitsverzeichnis | **ja**: `requests` gegen `www.ableton.com`, prüft `robots.txt`, Standard 150 Seiten mit 2,5 s Pause, nur Metadaten | braucht `requests` und `beautifulsoup4` |
| `…audit_midi_library__WERKZEUG__V5_3.py` | JSON an `--output`, legt Elternordner an | nein | lauffähig mit Argumenten |
| `…build_codex_prompt__WERKZEUG__V5.py` | `CODEX_MASTER_EXECUTION_V5.md` neben sich | nein | legt eine neue Datei in `15_TOOLS_SKRIPTE/` an |
| `…build_progressions_v5__WERKZEUG__V5.py` | drei Dateien neben sich (`KURATIERTE_PROGRESSIONSFAMILIEN_V5.json`, `TRANSPONIERTE_PROGRESSIONSVARIANTEN_V5.json`, `ATLAS_V5.md`) | nein | legt neue Dateien in `15_TOOLS_SKRIPTE/` an |
| `…build_reference_tests__WERKZEUG__V5.py` | zwei Dateien neben sich (`CONCEPTUAL_GOLDEN_AND_NEGATIVE_CASES_V5.json/.md`) | nein | legt neue Dateien in `15_TOOLS_SKRIPTE/` an |
| `…build_scores_v5__WERKZEUG__V5.py` | `Partituren/*.json/.md`, `STUDIENREGISTER_V5.json` und `README.md` neben sich | nein | bricht beim ersten Schreiben ab (`Partituren/` fehlt) |
| `…build_sources_v5__WERKZEUG__V5.py` | drei Dateien unter dem festen Pfad `/mnt/data/STEPS_Research_Library_V5/06_Quellen_und_Rechte` | nein | bricht ab, solange der Pfad fehlt |
| `…validate_v5__WERKZEUG__V5.py` | `08_Validierung/PRUEFBERICHT_V5.json` | nein | bricht beim Schreiben ab (Ordner fehlt) |
| `…validate_v53__WERKZEUG__V5_3.py` | nichts, nur Ausgabe | nein | braucht `mido` und `jsonschema` |
| `…validate_v54__WERKZEUG__V5_4.py` | nichts, nur Ausgabe | nein | |
| `STEPS_V6_0__audit_library.py` | nichts, nur Ausgabe | nein | |
| `90_HISTORIE/V3/…validate_v3__WERKZEUG__V3.py` | `04_Qualitaet/STRUCTURAL_AUDIT_EXECUTED_V3.md` unter `90_HISTORIE/V3/` | nein | bricht beim Schreiben ab (Ordner fehlt) |
| `90_HISTORIE/V4/…validate_v4__WERKZEUG__V4.py` | `08_Validierung/MECHANISCHER_PRUEFBERICHT_V4.json` unter `90_HISTORIE/V4/` | nein | bricht beim Schreiben ab (Ordner fehlt) |

### Sonderfall

`Ordnerliste.py` im Wurzelordner der Bibliothek ist **kein Python, sondern PowerShell**. Es schreibt `README_ORDNERLISTE_EXAKT.md` in einen Ordner `.\STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials` relativ zum Arbeitsverzeichnis. Mit Python gestartet bricht es mit einem Syntaxfehler ab. Die Datei bleibt unverändert; ein Umbenennen wäre eine eigene Entscheidung.

## Empfehlung für einen späteren Lauf

1. Nur in einer getrennten Arbeitskopie außerhalb des Repositorys und außerhalb von OneDrive laufen lassen. Das empfiehlt schon `tools/legacy/generators/README.md`.
2. Bei den V6.7-Generatoren vorher prüfen, ob gleichnamige ZIPs im Arbeitsverzeichnis liegen.
3. Den Indexer nur bewusst starten: Er greift auf eine fremde Website zu.
4. Die V5-Werkzeuge nicht für den heutigen Bestand verwenden, ohne ihre Pfade anzupassen.

## Grenzen

Statische Analyse erkennt keine dynamisch zusammengesetzten Pfade außerhalb der gelesenen Zeilen und keine Seiteneffekte in importierten Fremdbibliotheken. Ob die Skripte fachlich richtige Ergebnisse erzeugen, ist nicht geprüft.
