# Struktur-, Versions- und Zählmodelle der Bibliothek V3–V6.7 sowie Fachordner 21 und 39 (16.11.2026)

**Status:** Lesende Bestands- und Strukturprüfung auf `main` bei `a1ac518`. Es wurden keine Ordner verschoben, umbenannt oder zusammengeführt (`AGENTS.md`, Preservation-first). Schließt den Prüfpunkt aus der Bestandsaufnahme vom 10.11.2026: „V6.6/V6.7: mehrere Versionen, Fachordner 21 und 39 doppelt benannt; unterschiedliche Struktur-/Zählmodelle.“

## 1. Überblick

In `research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/` und `tools/legacy/generators/` überlagern sich **vier historische Strukturmodelle** (V3/V4, V5.0–V5.4, V6.0–V6.6, V6.7-Delta) sowie mehrere Zählweisen (Inhaltsdateien ohne eigene Manifest-/Prüfsummendateien vs. Gesamtarchiv inkl. Vorversions-Manifesten vs. Themen-/URL-Zählungen).

- **Doppelt vergebene Ordnernummern 21 und 39:** Die Ordnerpaare `21_AUDIO_EDITING_RESTORATION` / `21_EDITING_RESTORATION` sowie `39_INTEROPERABILITY_FORMATS` / `39_AUDIO_FORMATS_INTEROPERABILITY` haben **keinerlei Datei-, Hash- oder URL-Überschneidung**. Die älteren Namen stammen aus der V6.0-Taxonomie, die beiden kürzeren/abweichenden Namen entstanden beim V6.6-Ingest für zusammen drei neue V6.6-Dateien (davon zwei im Repository, eine unter den 148 seit `a14c3f3` fehlenden V6.6-Dateien).
- **V6.6-Istbestand im Repository:** Heute liegen exakt **1.000 Dateien** in **49 Hauptordnern** (`00`–`44` mit doppelt vergebenen Nummern `21` und `39`, dazu `90_HISTORIE` und `99_ORIGINALARCHIV`) sowie **5 Wurzeldateien**. Das V6.6-Manifest nennt **1.145 Dateien**; die Differenz erklärt sich vollständig aus **148 fehlenden Dateien** ([Nachprüfung der Indizes](INDIZES_NACHPRUEFUNG_2026-11-16.md)) und **3 nicht im Manifest selbst geführten Dateien** (dem V6.6-Manifest selbst sowie den am 10.11.2026 ergänzten `Ordnerliste.py` und `README_STEPS_BIBLIOTHEK.md`: `1.145 − 148 + 3 = 1.000`).
- **V6.7-Delta (`tools/legacy/generators/`):** Im Repository liegen nur die drei Generatorskripte ([Seiteneffekt-Analyse](GENERATOREN_SEITENEFFEKTE_2026-11-16.md)), kein entpackter Ordner `STEPS_V6_7_ERWEITERUNG`. V6.7 verwendet keine 47/49-Fachordner-Struktur, sondern ein eigenes **Delta-Paketmodell** (`00_START_HIER.md`, `10_QUELLEN_LIZENZEN/`, `20_QUELLENKARTEN/`, `30_PRAXISLABORE/`, `40_INTEGRATION/`, ab Ausbau 03 zusätzlich `50_ORIGINALMODULE/`). Von den zusammen 30 Ableton-Blog-Kandidaten (`AB-V67-001` bis `AB-V67-030`) sind 23 bereits unter den 262 URLs des V6.6-Registers enthalten; übrig bleiben genau die in `README_STEPS_BIBLIOTHEK.md` genannten **7 neuen Quellenkarten**, **7 Praxislabore** und **12 eigenständigen STEPS-Wissensmodule**.

---

## 2. Vier Strukturmodelle von V3 bis V6.7

| Entwicklungsstufe | Ablageort im Repository | Ordnermodell | Hauptordner |
| --- | --- | --- | --- |
| **V1 / V3 / V4** (Historie) | `90_HISTORIE/V1/` (7 Dateien), `90_HISTORIE/V3/` (29 Dateien), `90_HISTORIE/V4/` (127 Dateien) | Ursprünglich nach Arbeitsphasen nummeriert (u. a. `04_Qualitaet` in V3, `08_Validierung` in V4); seit V5.2 unter `90_HISTORIE/` in die 16er-Domänenordner (`00_NAVIGATION`..`15_TOOLS_SKRIPTE`) einsortiert | 3 (V1), 13 (V3), 12 (V4) in `90_HISTORIE/` |
| **V5.0 – V5.4** | In die Ordner `00`–`15`, `90`, `99` der V6.6-Bibliothek migriert; V5.1 zusätzlich als ZIP in `99_ORIGINALARCHIV/` | Sechs musikalische Kernbereiche (`01_MUSIKTHEORIE` bis `06_PRODUCER_TOOLS`), neun Querschnittsbereiche (`07`–`15`), Steuerung (`00_NAVIGATION`), Historie (`90_HISTORIE`), Originalarchiv (`99_ORIGINALARCHIV`) | **18** (`00`–`15`, `90`, `99`) |
| **V6.0 – V6.5** | `STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/` | Ausbau auf 15 Produktionsphasen (`STEPS_V6_0__PRODUKTIONSLANDKARTE__TAXONOMIE__V6_0.md`): Fachordner `16_CREATIVE_DIRECTION_PREPRODUCTION` bis `44_PRODUCTION_ETHICS_CULTURE` (mit `21_AUDIO_EDITING_RESTORATION` und `39_INTEROPERABILITY_FORMATS`) | **47** (`00`–`44`, `90`, `99`) |
| **V6.6** | `STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/` | Wie V6.0–V6.5, jedoch legt der V6.6-Ingest für Nummer 21 und 39 zwei abweichend benannte Zusatzordner an (`21_EDITING_RESTORATION`, `39_AUDIO_FORMATS_INTEROPERABILITY`) | **49** (`00`–`44` mit `21` und `39` doppelt, `90`, `99`) |
| **V6.7 (Patch, Ausbau 02, Ausbau 03)** | Nur als Generatoren unter `tools/legacy/generators/` (`create_steps_v6_7_*.py`) | Eigenständiges Delta-Archiv unter `STEPS_V6_7_ERWEITERUNG/` mit Paketordnern nach Artefakttyp statt Fachgebiet (`10_QUELLEN_LIZENZEN`, `20_QUELLENKARTEN`, `30_PRAXISLABORE`, `40_INTEGRATION`, `50_ORIGINALMODULE`); Ziel-Fachbereiche stehen nur als Textfeld in den Karten | **4** bzw. **5** Paketordner im Delta-ZIP |

---

## 3. Zählmodelle und rechnerischer Zusammenhang (V5.0 bis V6.7)

Die scheinbar widersprüchlichen Dateizahlen in den Wegweisern, Changelogs und Manifesten unter `00_NAVIGATION/` folgen einer durchgängigen Regel: Jede Version erzeugt am Schluss ein eigenes Manifest und/oder eine eigene SHA-256-Prüfsummendatei, die sich selbst nicht mitzählen, in der Folgeversion aber als Teil des übernommenen Altbestands mitgezählt werden.

| Version | Primärer Index / Manifest in `00_NAVIGATION/` | Gezählte Einheiten laut Index | Gesamtzahl beim Übergang in die Folgeversion | Ableton-Blog-URLs (kumulativ) | Erläuterung der Zähldifferenz |
| --- | --- | ---: | ---: | ---: | --- |
| **V5.0** | `STEPS_NAV__PACKAGE_MANIFEST_V5__DATEN__V5.json`, `STEPS_NAV__SHA256SUMS__ALTE_PRUEFSUMMEN__V5.txt` | 260 Dateien | 264 (laut V5.1-Manifest) | – | 260 Nutzdateien ohne eigenes Manifest und Hashliste; enthält das unveränderte V4-Archiv. |
| **V5.1** | `STEPS_NAV__MANIFEST_V5_1__DATEN__V5_1.json`, `STEPS_NAV__SHA256SUMS_V5_1__ALTE_PRUEFSUMMEN__V5_1.txt` | 276 Dateien | 278 Dateien (`STEPS_DATEIENINDEX_ALLE_278.csv/.json`) | – | 276 Paketdateien + V5.1-Manifest + V5.1-Hashliste = 278 Dateien (identisch mit den 278 Dateien im ZIP `99_ORIGINALARCHIV/STEPS_V5_1_UNVERAENDERT_ORIGINAL.zip`, das 284 ZIP-Einträge inkl. 6 Ordner-Einträgen enthält). |
| **V5.2** | `STEPS_PACKAGE_MANIFEST_V5_2.json`, `STEPS_SHA256SUMS_V5_2.txt` | 278 migrierte Dateien / 288 Hashes | 290 Dateien | – | 278 migrierte V5.1-Dateien (163 historisch in `90_HISTORIE/`, 115 aktiv) + 10 neue V5.2-Navigationsdateien = 288 Zeilen in `STEPS_SHA256SUMS_V5_2.txt` (+ Manifest und Hashliste selbst = 290). Daneben zählt `STEPS_ABDECKUNG_ALLE_BEREICHE.csv` **53 Fachthemen**. |
| **V5.3** | `STEPS_DATEIENINDEX_V5_3.csv`, `STEPS_MANIFEST_V5_3.json`, `STEPS_SHA256SUMS_V5_3.txt` | 345 Indexzeilen / 347 Hashes | 349 Dateien (laut V5.4-Manifest) | – | 345 Inhaltsdateien im CSV-Index; 347 physische Dateien in `STEPS_MANIFEST_V5_3.json` und `STEPS_SHA256SUMS_V5_3.txt` (+ diese beiden Dateien selbst = 349). |
| **V5.4** | `STEPS_DATEIENINDEX_V5_4.csv/.json`, `STEPS_MANIFEST__V5_4-Bibliotheksstruktur-Zaehlung__MANIFEST__V5_4.json`, `STEPS_SHA256SUMS__V5_4-Files__HASHES__V5_4.txt` | 546 Indexzeilen / 548 vor Manifest / 551 Hashes | 551 Basisdateien (laut V6.0-Basismanifest) | – | 349 übernommene V5.3-Dateien + 199 neue V5.4-Dateien = 548 vor Manifest; 546 im Sachindex; 551 in `STEPS_SHA256SUMS__V5_4-Files__HASHES__V5_4.txt`. |
| **V6.0** | `STEPS_V6_0__DATEIINDEX__AKTIV_UND_HISTORISCH__V6_0.csv`, `STEPS_V6_0__THEMENREGISTER__DATEN__V6_0.csv/.json` | **809 Dateien** (davon 775 im Repo, **34 fehlend**) | 809 Dateien | – | Baut auf 551 V5.4-Dateien (`STEPS_V6_0__SOURCE_BASE_HASHES__MANIFEST__V6_0.json`) auf. **Achtung Zählmodell:** `STEPS_V6_0__THEMENREGISTER__DATEN__V6_0.csv/.json` zählt **878 Fachthemen** in 29 Domänen, keine Dateien. |
| **V6.1** | `STEPS_V6_1__DATEIINDEX__AKTIV_UND_HISTORISCH.csv` | **820 Dateien** (davon 786 im Repo, **34 fehlend**) | 820 Dateien | – | 809 V6.0-Dateien + 11 DeSantis-Querverweis- und Navigationsdateien = 820. |
| **V6.2** | `STEPS_START__AbletonBlog-Vollarchiv-Teilindex-Lizenzen__WEGWEISER__V6_2.md`, `10_QUELLEN_LIZENZEN/...V6_2.csv` | 829 Dateien (laut V6.3-Manifest) | 829 Dateien | **23** | Erste Ableton-Blog-Integration (23 verifizierte Blog-URLs). |
| **V6.3** | `STEPS_MANIFEST__AbletonBlog-V6_3-Erweiterung-Dateihashes__DATEN__V6_3.json` | 829 Basis + 98 neu = 927 (ohne Manifest) | 928 Dateien (`V6_3_UNCHANGED` in V6.4) | **97** (23 + 74) | 829 Basisdateien + 98 neue Dateien + V6.3-Manifest selbst = 928 Dateien. |
| **V6.4** | `STEPS_DATEIENINDEX__V6_4-Archivbestand-Pruefsummen__MANIFEST__V6_4.csv` | **1.003 Dateien** (`928 V6_3_UNCHANGED` + `75 V6_4_NEW`; 878 im Repo, **125 fehlend**) | 1.004 Dateien (laut `00_START_HIER_V6_5.md`) | **156** (97 + 59) | 1.003 Zeilen im V6.4-Manifest + das V6.4-Manifest selbst = 1.004 Dateien. |
| **V6.5** | `STEPS_V6_5__MANIFEST_SHA256.json`, `00_START_HIER_V6_5.md` | **1.061 Dateien** im JSON-Manifest | 1.063 Dateien (`V6_5 preserved` in V6.6) | **199** (156 + 43) | 1.004 V6.4-Dateien + 57 neue V6.5-Dateien = 1.061 im JSON-Manifest + JSON-Manifest selbst + `00_START_HIER_V6_5.md` = 1.063 Dateien. |
| **V6.6** | `STEPS_DATEIENINDEX__V6_6-Historisch-und-Neu__MANIFEST__V6_6.csv`, `00_START_HIER_V6_6.md` | **1.145 Dateien** (`1.063 V6_5 preserved` + `82 V6_6 added`; 997 im Repo, **148 fehlend**) | **1.000 Dateien im Repo** | **262** (199 + 63) | Im Repo vorhanden: `1.145 − 148 = 997` Manifest-Dateien + `MANIFEST__V6_6.csv` selbst + `Ordnerliste.py` + `README_STEPS_BIBLIOTHEK.md` = **1.000 Dateien**. |
| **V6.7** (Delta) | `tools/legacy/generators/create_steps_v6_7_*.py`, `README_STEPS_BIBLIOTHEK.md` | Patch: 3 neu (aus 10)<br>Ausbau 02: 4 neu (aus 25)<br>Ausbau 03: **7 neu** (aus 30) + **12 Originalmodule** | Separates Delta-ZIP (nicht im Repo entpackt) | **269** (262 + 7) | Von 30 Kandidaten (`AB-V67-001`..`030`) stehen 23 URLs bereits im V6.6-Register (262 Slugs); übrig bleiben 7 neue Quellenkarten (`AB-V67-003`, `006`, `007`, `019`, `026`, `027`, `028`), 7 Praxislabore und 12 eigenständige Wissensmodule (`STEPS-V67-MT-01`..`PR-02`). |

---

## 4. Einzelfallprüfung der doppelt vergebenen Ordnernummern 21 und 39

### 4.1 Nummer 21: `21_AUDIO_EDITING_RESTORATION` vs. `21_EDITING_RESTORATION`

| Merkmal | `21_AUDIO_EDITING_RESTORATION` | `21_EDITING_RESTORATION` |
| --- | --- | --- |
| Eingeführt in | V6.0 (`STEPS_V6_0__PRODUKTIONSLANDKARTE__TAXONOMIE__V6_0.md`) | V6.6 (`STEPS_DATEIENINDEX__V6_6-Historisch-und-Neu__MANIFEST__V6_6.csv`) |
| Dateien im V6.6-Manifest | **7** (1 Fachdossier + 6 Themencluster `Cluster-01` bis `Cluster-06`) | **1** (`ABLETON_BLOG_V6_6/STEPS_21__good-timing-beatmaking-with-auto-warp-in-live-113__QUELLENKARTE__V6_6.md`) |
| Dateien heute im Repository | **6** (`Cluster-05-Multitrack-Drum-Editing`, SHA-256 `b15b89d3812e…`, gehört zu den 148 fehlenden Dateien) | **1** (SHA-256 `ffe9b666d3c8…`, `ABLETON-204`) |
| Inhaltliche / technische Überschneidung | Allgemeine Produktions- und Restaurations-Themenindizes (Comping, Time-Stretch, De-Crackle, Noise Gates, Restore vs. Recreate) | Einzelne V6.6-Quellenkarte zum Ableton-Blogbeitrag *Good Timing – Beatmaking with Auto-Warp in Live 11.3* |
| Interne Verweise im Repository | 25 Dateien (u. a. V6.0-, V6.1-, V6.3-, V6.4-, V6.6-Indizes, `01_BESTANDSINVENTAR.csv`, `MUSIC_SOURCE_REVIEW_PROGRESS.csv`) | 25 Dateien (u. a. V6.3/V6.4-Tabellen, V6.6-Leseroute, V6.6-Manifest, Projekt-Übersichten, `MUSIC_SOURCE_REVIEW_PROGRESS.csv`) |

**Befund zu 21:** Keine Dublette und keine Inhaltsüberschneidung. In `STEPS_ABLETONBLOG__NEUE-QUELLEN-FACHGEBIETE__LESEROUTE__V6_3.md` und `STEPS_ABLETONBLOG__V6_4-Fachstatistik-und-Status__COUNTS__V6_4.csv` wurde das Kurzlabel `21_EDITING_RESTORATION` bereits als Tabellenbezeichnung genutzt, während die Dateien bis V6.4 im Ordner `21_AUDIO_EDITING_RESTORATION` lagen. Erst beim V6.6-Export wurde aus dem Kurzlabel ein eigener physischer Ordner für `ABLETON-204`.

### 4.2 Nummer 39: `39_INTEROPERABILITY_FORMATS` vs. `39_AUDIO_FORMATS_INTEROPERABILITY`

| Merkmal | `39_INTEROPERABILITY_FORMATS` | `39_AUDIO_FORMATS_INTEROPERABILITY` |
| --- | --- | --- |
| Eingeführt in | V6.0 (`STEPS_V6_0__PRODUKTIONSLANDKARTE__TAXONOMIE__V6_0.md`), ergänzt in V6.5 | V6.6 (`STEPS_DATEIENINDEX__V6_6-Historisch-und-Neu__MANIFEST__V6_6.csv`) |
| Dateien im V6.6-Manifest | **10** (1 Fachdossier + 8 Themencluster `Cluster-01` bis `Cluster-08` aus V6.0 + 1 Quellenkarte `ABLETON-183` *Live 12.4 is out now* aus V6.5) | **2** (1 Transferlabor `STEPS_39__INTEROP_MIDI_CV__TRANSFERLAB__V6_6.md` + 1 Quellenkarte `STEPS_39__midi-cv-link-sync-many-ways-connecting-modular-gear-live__QUELLENKARTE__V6_6.md`) |
| Dateien heute im Repository | **10** (alle 10 vorhanden; `ABLETON-183` hat SHA-256 `6b23c32c24c6…`) | **1** (`STEPS_39__INTEROP_MIDI_CV__TRANSFERLAB__V6_6.md`, SHA-256 `d29ed1661cb0…`; die zugehörige Quellenkarte `319cbf847640…` gehört zu den 148 fehlenden Dateien) |
| Inhaltliche / technische Überschneidung | Dateiformate und Austauschstandards (MIDI 1.0 SMF, MusicXML, BWF, Opus, AAF, VST3, Metadata-JSON, Roundtrip-Tests) sowie Link Audio in Live 12.4 | V6.6-Transferlabor (und fehlende V6.6-Quellenkarte) zur Kopplung von MIDI, CV und Ableton Link mit Modular-Hardware |
| Interne Verweise im Repository | 25 Dateien (V6.0–V6.6-Indizes, V6.5-Leseroute, `01_BESTANDSINVENTAR.csv`, `MUSIC_SOURCE_REVIEW_PROGRESS.csv`) | 13 Dateien (V6.6-Leseroute, V6.6-Manifest, kumulatives V6.6-Blogregister, `BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv`) |

**Befund zu 39:** Ebenfalls keine Dublette und keine Inhaltsüberschneidung. Der V6.5-Zugang (`ABLETON_BLOG_V6_5/STEPS_39__live-12-4-is-out-now__QUELLENKARTE__V6_5.md`) wurde noch in den bestehenden V6.0-Ordner `39_INTEROPERABILITY_FORMATS` gelegt; erst der V6.6-Generator vergab für die beiden V6.6-Artefakte den abweichenden Ordnernamen `39_AUDIO_FORMATS_INTEROPERABILITY`.

---

## 5. Folgerung für Repository und Migration

1. **Keine Umbenennung im Archivbestand:** Beide Ordnerpaare (`21_*` und `39_*`) bleiben an ihren historischen Pfaden unverändert, damit alle Prüfsummen- und Pfadmanifeste (`STEPS_DATEIENINDEX__V6_6-Historisch-und-Neu__MANIFEST__V6_6.csv`, `01_BESTANDSINVENTAR.csv`, `02_DATEIKLASSIFIZIERUNG.csv`, `MUSIC_SOURCE_REVIEW_PROGRESS.csv`) ohne Bruch gültig bleiben.
2. **Kanonische Zuordnung bei einer späteren Übernahme nach `knowledge/`:** Fachlich gehören beide `21_*`-Ordner zur selben Domäne *Audio Editing & Restoration* und beide `39_*`-Ordner zur Domäne *Interoperability & Audio/MIDI Formats*.
3. **V6.7-Status:** Da V6.7 nur als Generator-Code unter `tools/legacy/generators/` vorliegt und im Repository kein `STEPS_V6_7_ERWEITERUNG`-Ordner versioniert ist, entsteht im aktuellen Arbeitsbaum kein Versionskonflikt zwischen V6.6 und V6.7.
