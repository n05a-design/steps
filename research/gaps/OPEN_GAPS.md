# Aktuelle Lücken (Repository-Bestandsaufnahme 2026-11-10)

- Projektkonsolidierung nennt sechs Originaldokumente, im Originalarchiv liegt derzeit kein `Glide Kontext für Fable(2).md` (5 Markdown-Originale vorhanden); Nachweis/Fundort prüfen.
- Kein ausführbarer `app/`- oder `src/steps/`-Musikcode im analysierten `main`-Baum.
- Urheberrechte zahlreicher Fach-PDFs, heruntergeladener Web-Seiten und Drittanbieterbilder offen.
- V6.6/V6.7: mehrere Versionen, Fachordner 21 und 39 doppelt benannt; unterschiedliche Struktur-/Zählmodelle.
- Historische JSON-/CSV-Indizes benötigen Pfad- und Hashrevalidierung.
- Externe Integration von Glide nur Vorschlag, konkrete Code-/Lizenzübernahme nicht geprüft.
- Die bestehenden Bibliotheks-Generatoren wurden nicht ausgeführt und ihre Seiteneffekte sind nicht analysiert.

## Fachprüfung des Progressionskerns (2026-11-11)

- Der App-Katalog umfasst die einzeln geprüften PROG-001, PROG-003 und
  PROG-009. Weitere Beispiele brauchen eine eigene Prüfung und Quellenreferenz.
- PROG-020 und PROG-027 enthalten im Bestandskern vereinfachte Dominanten.
  Für eine Freigabe die konkrete Alterationskombination und die beabsichtigte
  Realisierung ausweisen. Das mehrdeutige Stufensuffix `alt` benötigt dafür
  eine ausdrückliche Interpretation.
- Der Voicing-Solver prüft Tonklassen, Bass, MIDI-Grenzen, Stimmenreihenfolge und
  im strikten Modus parallele Quinten und Oktaven. Eine vollständige
  kontrapunktische Prüfung und stilbezogene Spielbarkeitsprüfung bleiben offen.

## Offene Fachnachweise (2026-11-12)

- Bei [PAT-031](../../knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md#pat-031--offene-taktgrenze) fehlen Taktgrenzen und die Hörprüfung der beiden Lesarten.
- Für die [198 Golden Cases](../../knowledge/research/GOLDEN_DATA_SOURCE_OF_TRUTH.md#2-bestandsübersicht-phase-415) fehlt eine dokumentierte fachliche Einzelabnahme. Die Test- und Integritätsnachweise liegen vor.

## PDF-Konvertierung mit Docling (2026-11-14)

- Neben 58 PDF-Kopien (40 eindeutige Dateien) liegen jetzt gleichnamige Docling-Extrakte (`.md`). Zuordnung und Hashes: [`manifests/pdf_docling_markdown_2026-11-14.csv`](../../manifests/pdf_docling_markdown_2026-11-14.csv). Alle Extrakte sind `REVIEW_REQUIRED`, ohne OMR und ohne fachliche Freigabe.
- `research/STEPS_Bibliothek/MakingMusic.pdf` und die bytegleiche Kopie in `Dokumentation (unsortiert)/` beginnen mit Null-Bytes und sind keine gültige PDF (Docling: `INVALID_PDF`). Möglicherweise defekter Download oder OneDrive-Synchronisationsschaden. Eine lesbare Fassung liegt vermutlich als `MakingMusic_DennisDeSantis.pdf` vor. Das ist nicht per Inhaltsvergleich bestätigt.
- Der Inhaber hat am 14.11.2026 entschieden, die Extrakte wie die Original-PDFs in Git zu versionieren. Damit weicht der Bestand von `knowledge/sources/RIGHTS_POLICY.md` ab, nach der fremde Volltexte lokal und per `.gitignore` geschützt bleiben. Die Rechteprüfung je Quelle bleibt offen. Vor einer Veröffentlichung des Repositorys muss sie abgeschlossen sein.
- 82 Markdown-Dateien (78 in `STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials`, 4 in `source_archive`) konnten lokal nicht gelesen werden (`Errno 22`). Wahrscheinlich hängt das mit OneDrive zusammen. Derselbe Fehler bricht `git status` ab.
