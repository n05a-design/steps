# Nachprüfung der JSON-/TXT-Hashmanifeste, V4-Quellenlisten und des PPR-MIDI-Inventars (16.11.2026)

**Status:** Lesende Ergänzungsprüfung zu [`INDIZES_NACHPRUEFUNG_2026-11-16.md`](INDIZES_NACHPRUEFUNG_2026-11-16.md) auf `main` bei `a1ac518`. Prüft die 14 JSON- und TXT-Prüfsummen-/Paketmanifeste unter `00_NAVIGATION/` der V6.6-Bibliothek sowie die im ersten Indexbericht noch ausgenommenen Dateien `PPR_MIDI_ARCHIVINVENTAR.csv`, `STEPS_V4_89_QUELLENABSCHNITTE.csv` (samt `Steps_Quellenabdeckung_2026-11-09.csv`) und `STEPS_V4_HISTORISCHE_POSITIONEN.csv`. Keine historische Indexdatei wurde verändert.

## 1. JSON- und TXT-Hashmanifeste der V6.6-Bibliothek (`00_NAVIGATION/`)

Pfade relativ zu `research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/`. Bei Textdateien gelten LF- und CRLF-Variante desselben Inhalts als inhaltlich identisch.

| Manifest / Prüfsummenliste | Format | Einträge | Am selben Pfad (inkl. LF/CRLF) | In `99_ORIGINALARCHIV/` (V5.1-ZIP) bzw. nach V5.2 migriert | Inhalt geändert | **Fehlt (Teil der 148)** | Ungeklärt |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `STEPS_NAV__PACKAGE_MANIFEST_V5__DATEN__V5.json` | JSON | 260 | 0 | 260 | 0 | 0 | **0** |
| `STEPS_NAV__SHA256SUMS__ALTE_PRUEFSUMMEN__V5.txt` | TXT | 260 | 0 | 260 | 0 | 0 | **0** |
| `STEPS_NAV__MANIFEST_V5_1__DATEN__V5_1.json` | JSON | 276 | 0 | 276 | 0 | 0 | **0** |
| `STEPS_NAV__SHA256SUMS_V5_1__ALTE_PRUEFSUMMEN__V5_1.txt` | TXT | 276 | 0 | 276 | 0 | 0 | **0** |
| `STEPS_DATEIENINDEX_ALLE_278.json` | JSON | 278 | 278 | 0 | 0 | 0 | **0** |
| `STEPS_SHA256SUMS_V5_2.txt` | TXT | 288 | 288 | 0 | 0 | 0 | **0** |
| `STEPS_MANIFEST_V5_3.json` | JSON | 347 | 347 | 0 | 0 | 0 | **0** |
| `STEPS_SHA256SUMS_V5_3.txt` | TXT | 347 | 347 | 0 | 0 | 0 | **0** |
| `STEPS_BASE_HASHES_V5_3__V5_4.json` | JSON | 349 | 349 | 0 | 0 | 0 | **0** |
| `STEPS_DATEIENINDEX_V5_4.json` | JSON | 546 | 546 | 0 | 0 | 0 | **0** |
| `STEPS_SHA256SUMS__V5_4-Files__HASHES__V5_4.txt` | TXT | 550 (+ 1 `#`-Kopfzeile) | 550 | 0 | 0 | 0 | **0** |
| `STEPS_V6_0__SOURCE_BASE_HASHES__MANIFEST__V6_0.json` | JSON | 551 | 551 | 0 | 0 | 0 | **0** |
| `STEPS_MANIFEST__AbletonBlog-V6_3-Erweiterung-Dateihashes__DATEN__V6_3.json` | JSON | 927 (`829` V6.2-Basis + `98` V6.3-Neu) | 864 | 0 | 0 | **63** (`34` V6.2-Basis + `29` V6.3-Neu) | **0** |
| `STEPS_V6_5__MANIFEST_SHA256.json` | JSON | 1.061 | 926 | 0 | 0 | **135** | **0** |

### Präzisierung der 148 fehlenden V6.6-Dateien nach Entstehungsversion

Durch die Einbeziehung der JSON-Manifeste von **V6.3** (inkl. dessen `original_base_hashes` für **V6.2**) und **V6.5** lässt sich für jede der 148 fehlenden Dateien aus [`BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv`](BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv) exakt bestimmen, in welcher Bibliotheksversion sie erstmals verzeichnet war:

| Erstmals im Index von | Anzahl fehlender Dateien | Kumulativ fehlend | Enthaltene Indexstände (`genannt_in`) |
| --- | ---: | ---: | --- |
| **V6.0** | **34** | 34 | `V6_6;V6_5;V6_4;V6_3;V6_2;V6_1;V6_0` |
| **V6.1** | **0** (alle 11 V6.1-Zugänge im Repo vorhanden) | 34 | – |
| **V6.2** | **0** (alle 9 V6.2-Zugänge im Repo vorhanden) | 34 | – |
| **V6.3** | **29** (von 98 V6.3-Zugängen) | 63 | `V6_6;V6_5;V6_4;V6_3` |
| **V6.4** | **62** (von 75 V6.4-Zugängen) | 125 | `V6_6;V6_5;V6_4` |
| **V6.5** | **10** (von 57 V6.5-Zugängen) | 135 | `V6_6;V6_5` |
| **V6.6** | **13** (von 82 V6.6-Zugängen) | **148** | `V6_6` |

Über die bereits bekannten 148 Dateien hinaus fehlt in keinem der 14 JSON- und TXT-Manifeste eine weitere Datei.

---

## 2. Prüfung der zuvor ausgenommenen Spezialindizes

| Indexdatei | Zeilen | Prüfgegenstand | Ergebnis |
| --- | ---: | --- | --- |
| [`docs/audit/fable-5.2/PPR_MIDI_ARCHIVINVENTAR.csv`](fable-5.2/PPR_MIDI_ARCHIVINVENTAR.csv) | 36 | SHA-256 und Dateigröße der 36 PausePlayRepeat-MIDI-Dateien (`PPR-MIDI-01` bis `PPR-MIDI-05`, Referenz-Commit `b42a990`) | **36 / 36** bytegleich im aktuellen Arbeitsbaum unter `research/STEPS_Bibliothek/Drums Progression/` vorhanden. |
| `archive/.../STEPS_V4_89_QUELLENABSCHNITTE.csv` (und `private_sources/Steps_Quellenabdeckung_2026-11-09.csv`) | 89 | Existenz der 6 referenzierten Originaldateien unter `private_sources/` und Gültigkeit der Zeilenbereiche (`Zeile_von`..`Zeile_bis`) | **89 / 89** Zeilenbereiche liegen innerhalb der realen Dateilängen der 6 Originaldokumente (`STEPS Project Export.md`: 297 Zeilen, `Projekt Overview.md`: 159, `Glide Kontext für Fable(2).md`: 659, `Project Definition & Positioning.md`: 221, `Forschungs- und Projektgrundlage.md`: 900, `Projektstatus- und Projektstartbericht.md`: 376). |
| `archive/.../STEPS_V4_HISTORISCHE_POSITIONEN.csv` | 100 | Referenzierte Originaldateien (`W-01`..`W-40`, `G-01`..`G-34`, `K-01`..`K-26`) | **100 / 100** verweisen auf vorhandene Originaldokumente unter `private_sources/`. |
| [`knowledge/relations/HISTORICAL_NODE_EVIDENCE.csv`](../../knowledge/relations/HISTORICAL_NODE_EVIDENCE.csv) | 41 | Historische Graphknoten `Mxx-xx` mit Datei-SHA-256 und Zeilennummer | **41 / 41** durch den automatisierten CI-Check (`scripts/audit_graph_followup.py --check`) geprüft. |

[Zum ersten Indexbericht](INDIZES_NACHPRUEFUNG_2026-11-16.md) · [Zum Windows-Suchauftrag](SUCHAUFTRAG_BIBLIOTHEK_V6_6_WINDOWS_2026-11-16.md)
