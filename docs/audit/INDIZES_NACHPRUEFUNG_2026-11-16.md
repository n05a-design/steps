# Nachprüfung der historischen Datei-Indizes (16.11.2026)

**Status:** Lesende Pfad- und Hashprüfung von 14 historischen Indizes mit Pfad- und SHA-256-Spalte. Keiner der Indizes wird verändert. Geprüfter Stand: `main` bei `a96abb5`. Ergänzt die [Nachprüfung des Bestandsinventars](BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.md).

## Vorgehen

Je Indexzeile, in dieser Reihenfolge:

1. Liegt die Datei versioniert am angegebenen Pfad? Dann Hashvergleich, auch nach Umstellung der Zeilenenden.
2. Liegt sie nur lokal (per `.gitignore` ausgeschlossen) in der Hauptablage? Dann Hashvergleich mit der lokalen Datei.
3. Sonst Suche des Hashs, auch in LF- und CRLF-Fassung, unter allen heute versionierten Dateien.
4. Sonst Zuordnung zu einer dokumentierten Entfernung (Glide, `37e691b`), zu einer Zeile ohne Hash oder „ungeklärt“.

Indizes innerhalb der V6.6-Bibliothek wurden relativ zu deren Wurzel `research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/` gelesen.

## Ergebnis: Indizes auf Repository-Ebene

| Index | Zeilen | Unverändert | Nur Zeilenenden | Bearbeitet | Verschoben | Lokal, Hash gleich | Lokal, Hash anders | Glide entfernt | Ohne Hash | Ungeklärt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `archive/manifests/02_DATEIKLASSIFIZIERUNG.csv` | 4.126 | 1.749 | 347 | 181 | 237 | 39 | 2 | 1.571 | 0 | **0** |
| `archive/manifests/ARCHIVE_MANIFEST.csv` (Zielpfade) | 233 | 100 | 133 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| `archive/manifests/05_DURCHGEFUEHRTE_ARCHIVIERUNG.csv` (Zielpfade) | 229 | 96 | 133 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Antigravity `02_DATEIINVENTAR.csv` (MasterAuditV2) | 4.025 | 1.743 | 347 | 181 | 142 | 39 | 2 | 1.571 | 0 | **0** |
| `knowledge/sources/MUSIC_SOURCE_REVIEW_PROGRESS.csv` | 1.895 | 1.654 | 123 | 82 | 7 | 12 | 2 | 0 | 15 | **0** |
| `manifests/PACKAGE_FILES_SHA256.csv` | 223 | 183 | 25 | 14 | 1 | 0 | 0 | 0 | 0 | **0** |
| `manifests/restricted_local_2026-11-14.csv` | 26 | 0 | 0 | 0 | 0 | 26 | 0 | 0 | 0 | **0** |

Die zweite Kopie des Antigravity-Inventars (`Antigravity_Steps_Bericht/MASTER_AUDIT_V2/`) ist bytegleich und nicht doppelt gezählt.

**Erklärungen:**
- *Lokal, Hash anders* (je 2 zum Prüfzeitpunkt `a96abb5`): `MakingMusic.pdf` und die Kopie in `Dokumentation (unsortiert)/`. Die historischen Indizes nannten den Hash der früheren Null-Byte-Datei (`dba9fb9e…`). Der Inhaber hat sie am 14.11.2026 durch die intakte Fassung (`4c6ba38b…`) ersetzt (OA-0017, siehe `OPEN_GAPS.md`); in `MUSIC_SOURCE_REVIEW_PROGRESS.csv` (`F00626`, `F01046`) ist der reparierte Hash am 16.11.2026 nachgezogen.
- *Ohne Hash* (15): Webquellen ohne Datei im Quellenregister, etwa General MIDI 1.0 oder Friberg & Sundström 2002.
- Alle 26 Dateien unter `restricted_local` liegen lokal vor und stimmen per Hash.
- Alle 229 bzw. 233 Archivierungsziele sind vorhanden und unverändert, abgesehen von Zeilenenden.

**Folgerung:** Auf Repository-Ebene gibt es keinen ungeklärten Dateiverlust.

## Ergebnis: Indizes der V6.6-Bibliothek

| Index (in `00_NAVIGATION/`) | Zeilen | Vorhanden (auch nur Zeilenenden) | Bearbeitet | **Fehlt** |
| --- | ---: | ---: | ---: | ---: |
| `STEPS_DATEIENINDEX_ALLE_278.csv` | 278 | 278 | 0 | 0 |
| `STEPS_DATEIENINDEX_V5_3.csv` | 345 | 345 | 0 | 0 |
| `STEPS_DATEIENINDEX_V5_4.csv` | 546 | 546 | 0 | 0 |
| `STEPS_V6_0__DATEIINDEX__AKTIV_UND_HISTORISCH__V6_0.csv` | 809 | 774 | 1 | **34** |
| `STEPS_V6_1__DATEIINDEX__AKTIV_UND_HISTORISCH.csv` | 820 | 786 | 0 | **34** |
| `STEPS_DATEIENINDEX__V6_4-Archivbestand-Pruefsummen__MANIFEST__V6_4.csv` | 1.003 | 878 | 0 | **125** |
| `STEPS_DATEIENINDEX__V6_6-Historisch-und-Neu__MANIFEST__V6_6.csv` | 1.145 | 997 | 0 | **148** |

**Befund:** 148 verschiedene Markdown-Dateien, die die bibliothekseigenen Indizes V6.0 bis V6.6 nennen, fehlen im Repository. Sie stehen in keinem Commit der Git-Historie, und eine Spotlight-Suche nach Dateinamen findet sie auf diesem Mac nicht (nur andere Klone desselben Repositorys). Die Bibliothek kam mit `a14c3f3` bereits unvollständig ins Repository.

- Am stärksten betroffen: `06_PRODUCER_TOOLS` (29), `22_SYNTHESIS_SAMPLING_SOUND_DESIGN` (22), `16_CREATIVE_DIRECTION_PREPRODUCTION` (13), `04_COMPOSING` (8). Es sind überwiegend Quellenkarten (`ABLETON_BLOG_RECHERCHE_V6_4`), Themenindizes und Fachdossiers.
- 34 Dateien nennen alle vier Indizes V6.0–V6.6, 91 nur V6.4 und V6.6, 23 nur V6.6.
- Vollständige Liste mit Hash laut Index: [`BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv`](BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv)

Die Dateien sind projekteigene Notizen der Bibliothek, keine fremden Originale. Eine erweiterte Suche auf dem Mac (Benutzerverzeichnis per `find`, alle gefundenen ZIP-Archive) blieb ebenfalls ohne Treffer. Für den Windows-Rechner liegt ein [Suchauftrag](SUCHAUFTRAG_BIBLIOTHEK_V6_6_WINDOWS_2026-11-16.md) bereit.

## Grenzen

- Geprüft sind nur Indizes mit Pfad- und Hashspalte. Die V4-Quellenabschnittslisten (Zeilenbereiche statt Dateihashes), `PPR_MIDI_ARCHIVINVENTAR.csv` (Git-Revisionen) und `HISTORICAL_NODE_EVIDENCE.csv` (eigener Validator) sind ausgenommen.
- „Bearbeitet“ sagt nur, dass sich der Inhalt seit dem Index geändert hat, nicht ob die Änderung richtig war.
- Die Spotlight-Suche erfasst nur indizierte Orte; OneDrive-Dateien, die nur online liegen, und der Windows-Rechner sind nicht erfasst.
