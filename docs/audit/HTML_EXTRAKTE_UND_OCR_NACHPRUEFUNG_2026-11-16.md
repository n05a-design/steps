# Nachprüfung der 18 eindeutigen HTML-Extrakte und der 2 OCR-Neuläufe

- **Prüfdatum:** 2026-11-16
- **Bezug:** `manifests/html_markdown_2026-11-14.csv` (26 Pfade / 18 eindeutige HTML-zu-Markdown-Paare) sowie die zwei Vollseiten-OCR-Neuläufe `Music_Theory_Advanced_Level.md` und `Understanding_Basic_Music_Theory.md` (je 2 Pfade).
- **Methodik:** Vollständiger Hashabgleich aller 26 HTML-Quellen und 26 Markdown-Extrakte gegen `manifests/html_markdown_2026-11-14.csv`, struktureller Abgleich von Hauptinhalt, Überschriften, Tabellen, Listen, Links und eingebetteten Elementen gegen die gespeicherten HTML-Dateien sowie Zeilen- und Fehlerprofilanalyse der beiden OCR-Neuläufe. `fachliche_freigabe` bleibt in allen Dateien `false`.

---

## 1. Integritätsprüfung `manifests/html_markdown_2026-11-14.csv` (26 Pfade / 18 Unikate)

Alle 26 Zeilen in `manifests/html_markdown_2026-11-14.csv` sind im Arbeitsbaum vorhanden; sowohl `html_sha256` (26/26) als auch `md_sha256` (26/26) stimmen exakt mit den gespeicherten Dateien überein.

Die 8 Dateipaare unter `research/competitors/Source Code/` sind bitidentische Kopien derselben 8 Dateipaare unter `research/STEPS_Bibliothek/Wettbewerb & Konkurrenz/Source Code/`. Es handelt sich somit um **18 eindeutige HTML-Quellen** und **18 eindeutige Markdown-Extrakte**.

---

## 2. Einzelprüfung der 18 eindeutigen HTML-zu-Markdown-Extrakte

### 2.1 Zehn Ableton-Blog-Artikel (`research/STEPS_Bibliothek/Ableton & Max for Live/Praxis & Produktion/`)

| # | HTML-Quelle (`html_sha256` Präfix) | MD-Extrakt (`md_sha256` Präfix) | Container | MD-Zeilen | H / Listen / Links | Prüfbefund (Hauptinhalt, Listen, Warnhinweis) |
| --- | --- | --- | --- | ---: | ---: | --- |
| 1 | `ANTI-MASS_ Communal Composition.html` (`0ed02dd90c6a`) | `.md` (`a4911bc9d1cb`) | `semantic-main` | 150 | 8 / 6 / 19 | Vollständiger Artikeltext inkl. Tracklist, Bildern (`_files/`), SoundCloud-Iframe-Verweisen und Fußzeilen-Metadaten erfasst. |
| 2 | `April + VISTA_ Shifting the Atmosphere.html` (`6f600f6ef99f`) | `.md` (`4d1dc055dc5f`) | `semantic-article` | 145 | 8 / 4 / 15 | Vollständiges Interview, eingebettete Bilder und Links vollständig übernommen. |
| 3 | `Bathe_ R&B on the Sunny Side.html` (`44da429d61f8`) | `.md` (`67fd02da00fa`) | `semantic-article` | 141 | 6 / 4 / 10 | Vollständiger Interviewtext inkl. Bildern und YouTube-Iframe-Hinweisen sauber extrahiert. |
| 4 | `Cloudchord_ Lessons from the Loop Master.html` (`d096d1e042ad`) | `.md` (`c5a4db267bc1`) | `semantic-article` | 173 | 12 / 4 / 11 | Vollständiger Artikel inkl. 5 nummerierten Produktions-Tipps, Bildern und Video-Platzhaltern vollständig erfasst. |
| 5 | `Download a Live Set from Rob Garza (Thievery Corporation).html` (`5e846eb1d3ee`) | `.md` (`3d64f57054f9`) | `semantic-article` | 73 | 4 / 4 / 11 | Vollständiger Kurzartikel inkl. Download-Link (`rob_garza_follow_the_sun_ableton_9.5.alp`) und Audio-Beispiellinks. |
| 6 | `Download the Live Set of Artefakt's 'Tapestry'.html` (`ca46eb781a14`) | `.md` (`ba27a820a501`) | `semantic-article` | 115 | 4 / 4 / 9 | Vollständiger Interview- und Analyse-Text inkl. Download-Link (`Artefakt_-_Tapestry_Live_Set.zip`) und Bildern. |
| 7 | `Download the Live Set of DJ Gigola's "La Batteria".html` (`91865f44192a`) | `.md` (`550ce4b5f5c6`) | `semantic-article` | 145 | 4 / 4 / 12 | Vollständiger Artikel inkl. Video-Transkription, Audio-Beispielen und Live-Set-Download-Link. |
| 8 | `Download the Live Set of Merrin Karras' "Void".html` (`ebdc35340486`) | `.md` (`be00357b476e`) | `semantic-article` | 143 | 4 / 4 / 10 | Vollständiger Artikel inkl. Hardware-/Effektketten-Beschreibung und Download-Link (`Merrin_Karras_-_Void_Live_Set.zip`). |
| 9 | `Dummy_ Inside The Machine.html` (`568c72246a0a`) | `.md` (`ef9be6c96303`) | `semantic-article` | 149 | 6 / 4 / 17 | Vollständiger Artikel inkl. Track-by-Track-Kommentaren und Bandcamp-/Embed-Hinweisen. |
| 10 | `Machinedrum_ Finding Wait What.html` (`88156be9a5ac`) | `.md` (`75325bb40162`) | `semantic-article` | 169 | 4 / 4 / 16 | Vollständiges Interview inkl. Arbeitsprozess-Details und SoundCloud-/Bild-Verweisen. |

**Bewertung der 10 Ableton-Extrakte:**
- Der Hinweis `MathML/SVG vorhanden: Darstellung am Original prüfen` im YAML-Vorspann wird ausschließlich durch Layout-/Logo-`<svg>`-Icons der Ableton-Webseite ausgelöst; keiner der 10 Artikel enthält mathematische Formeln oder SVG-Notengrafiken.
- In `ANTI-MASS_ Communal Composition.md` griff der Selektor `semantic-main` statt `semantic-article`, wodurch am Ende 4 Zeilen verwandter Blog-Teaser (*„Keep reading“*) mitübernommen wurden; der Artikeltext selbst ist vollständig.

---

### 2.2 Acht Wettbewerbs- und Produktseiten (`Wettbewerb & Konkurrenz/Source Code/` + Duplikate in `research/competitors/Source Code/`)

| # | Dateiname (`html_sha256` Präfix) | MD (`md_sha256` Präfix) | Container | MD-Zeilen | Tabellen (HTML → MD) | Prüfbefund (Hauptinhalt, Duplikate, Artefakte) |
| --- | --- | --- | --- | ---: | ---: | --- |
| 11 | `-chordfiles.com.html` (`a50fc9df4d83`) | `.md` (`daaf67e07730`) | `heuristic-container` | 200 | 0 → 0 | Alle Produkttexte und Links zu Chordfiles (25 Kategorien, 13.000 MIDI-Dateien) vorhanden. **Einschränkung:** Wegen responsiver Desktop-/Mobil-Blöcke im WordPress/Elementor-DOM ist der Abschnitt `# Master the Fretboard` samt den 4 Feature-Blöcken doppelt im Markdown enthalten; außerdem wurden Audio-Player-Bedienelemente (`00:00`, `Use Up/Down Arrow keys…`) mitextrahiert. |
| 12 | `-examples.html` (`1a88ac4898fa`) | `.md` (`99a9807be73e`) | `heuristic-container` | 309 | 0 → 0 | Alle 3 Progressionsbeispiele (`CM – GM – Am – FM`, `CM – B7 – Em – G`, `CM – EbM – AbM – Fm`) inkl. MP3-Links (`_files/*.mp3`) vorhanden. **Einschränkung:** Auch hier sind die Blöcke `# The examples` und `# Master the Fretboard` wegen des doppelten Desktop-/Mobil-DOMs im HTML zweimal hintereinander im Markdown abgebildet, ergänzt um MediaElement.js-Player-UI-Zeilen. |
| 13 | `-store.html` (`39a5552d265a`) | `.md` (`dcbb667794a0`) | `heuristic-container` | 150 | 0 → 0 | Produktbeschreibung (*All-Access Pass*, \$29, 13.000 MIDI-Dateien, 84 Genres) vollständig erfasst; `# Master the Fretboard` erscheint am Ende wegen des responsiven DOMs ein zweites Mal. |
| 14 | `-upcoming.html` (`aaacde8f2e91`) | `.md` (`b73de8a2e62e`) | `heuristic-container` | 115 | 0 → 0 | Geplante Features (Guitar Tab Integration, Extended Chord Libraries, Interactive Fretboard Tool, Educational Content) vollständig erfasst; die 4 Punkte erscheinen wegen Desktop-/Mobil-DOM zweimal. |
| 15 | `Reddit-Users-chat-about-chord-files.html` (`8a136bd97bb3`) | `.md` (`9dd2c20c5be7`) | `semantic-main` | 290 | 0 → 0 | Reddit-Thread aus `r/AcousticGuitar` (*„Wait… people actually buy midi chord packs?“*, `u/Itz_Ya_Boi25`) inkl. aller Nutzerkommentare (`u/Yeargdribble`, `u/slap_happy_dude`, `u/vanillastarfish` u. a.) vollständig erfasst. **Einschränkung:** Drei im gespeicherten Reddit-DOM eingebettete Werbeblöcke (`u/WildTangent_Games`, `u/ConductorAEO`, `u/SwellGamesLLC`) wurden als Teil von `<main>` mitextrahiert. |
| 16 | `The Chord Wheel.html` (`b778323e45f1`) | `.md` (`2de081497fa5`) | `semantic-article` | 222 | 1 → 1 (5 Zeilen) | Vollständiger Text und die HTML-Vergleichstabelle (`Chord Progression` / `Emotional Impact` / `Genre Application`, 5 Zeilen) sind im Markdown vollständig abgebildet. **Wichtiger Quellenbefund:** Die gespeicherte HTML-Datei besteht aus zwei aneinandergehängten SEO-/KI-Texten über „The Chord Wheel“ und enthält im Abschnitt *Historical Development and Evolution* frei erfundene Angaben (*„Klaus Vogel's 1997 breakthrough“*, Messingscheiben in den 1930er Jahren in Deutschland und Frankreich). Das reale Buch *The Chord Wheel* stammt von **Jim Fleser** (Hal Leonard, ISBN 978-0-634-02142-8). Diese Datei darf **nicht** als historische Quelle verwendet werden. |
| 17 | `_modewheel-start.html` (`4442429c462f`) | `.md` (`9ac1fa1c27a6`) | `semantic-main` | 91 | 0 → 0 | Komplette Startseite von `modewheelapp.newpsyc.com` (7 Modi, 3 Schritte, App-Link) sauber und ohne Duplikate extrahiert. |
| 18 | `_modewheel.html` (`a496f52c7f7c`) | `.md` (`143a24fc89af`) | `semantic-main` | 92 | 0 → 0 | Komplette Funktionsübersicht der ModeWheel-Web-App (Key Features, Instructions, Credits) sauber und ohne Duplikate extrahiert. |

---

## 3. Nachprüfung der 2 Vollseiten-OCR-Neuläufe (`OPEN_GAPS.md` Zeile 120 / 129)

Beide Dateien lagen im ersten Docling-Lauf wegen defekter PDF-Schriftkodierung (`ToUnicode`-Map fehlte) nur als Zeichensalat vor und wurden am 14.11.2026 per Bild-OCR neu konvertiert. Beide liegen jeweils an zwei Pfaden (Hauptpfad in `research/STEPS_Bibliothek/` und identisches Duplikat in `research/STEPS_Bibliothek/Dokumentation (unsortiert)/`).

### 3.1 `Music_Theory_Advanced_Level.md` (`ab07da055f90d9ca`, 1.551 Zeilen, 33 PDF-Seiten)

- **Quelle & Metadaten:** `Music_Theory_Advanced_Level.pdf` (`914ea586df8d7892…`, 33 Seiten, Juni 2005). Laut Einleitung auf Seite 3 eine Zusammenstellung von Forenbeiträgen des Autors **Eowyn** auf `www.mysongbook.com` (Teil 3 nach *Basic* und *Intermediate Music Theory*, Korrekturlesung durch Arnold und Blackiel). Lizenzhinweis im Dokument: freier Download zum Eigengebrauch, kommerzielle Nutzung untersagt (`restricted_local`, Rechteklasse E).
- **Konvertierungsverfahren:** Docling 2.150.0 mit erzwungener Vollseiten-OCR (`RapidOCR`, Torch) in 4 Abschnitten (`1–10`, `11–20`, `21–30`, `31–33`).
- **Struktur & Nutzbarkeit:**
  - Alle 33 Seiten und alle Kapitelüberschriften (*Defining modes*, *Most Important Modes*, *Using Modes for Improvisation*, *Using Modes for Composition*, *Dorian*, *Phrygian*, *Lydian and Mixolydian*, *Locrian*, *Modulation*, *Inter-tonal Exchanges*) sind vollständig lesbar.
  - Die Intervall- und Modustabellen (Ionian bis Locrian, Modi von Harmonisch Moll inkl. *Altered Phrygian / Major Dominant Phrygian* sowie *Bartok*-Modus) sind als Markdown-Tabellen (69 Tabellenzeilen) erhalten.
- **Dokumentiertes OCR-Fehlerprofil:**
  1. **16 Platzhalter `<!-- formula-not-decoded -->`:** Docling hat kurze Buchstaben-/Akkordfolgen, die im PDF abgesetzt gedruckt sind (z. B. die Tonleiter `A B C D E F G (A)` auf S. 5, Zeile 210), als Formelblöcke klassifiziert und ausgelassen.
  2. **12 Zeilen mit mehrspaltigen Wortaussetzern:** An Stellen mit Kursiv- oder Fettdruck mitten im Fließtext (z. B. Zeile 130 `The n ds i  b      y    bu`, Zeile 136 `sts s  s  uts t snd e d    tily`, Zeile 214 `'wo      s    l y   yem`, Zeile 316 `or        t        or`) hat RapidOCR einzelne hervorgehobene Wörter fragmentiert.
  3. **Tabellen-Kleinschreibung/Großschreibung:** In Zeile 246 wurde in der Bartók-Skala `b7` als `B7` erkannt; in Zeile 242 steht `Altered Myxolyian` (Tippfehler bereits im Original-PDF).

### 3.2 `Understanding_Basic_Music_Theory.md` (`20ee5717b2b3573a`, 11.011 Zeilen, 277 PDF-Seiten)

- **Quelle & Metadaten:** `Understanding_Basic_Music_Theory.pdf` (`b78a30736cc91a0e…`, 277 Seiten). Sammelband hrsg. von **Catherine Schmidt-Jones** (mit Beiträgen von Catherine Schmidt-Jones und Russell Jones), Rice University **Connexions** (`http://cnx.org/content/col10363/1.3/`), © 2007 Catherine Schmidt-Jones, lizenziert unter **Creative Commons Attribution License (CC BY 2.0)** (`http://creativecommons.org/licenses/by/2.0/`, belegt in `Understanding_Basic_Music_Theory.md` Zeilen 29–46).
  - *Hinweis zur Rechteklasse:* Im YAML-Vorspann ist vorsorglich `rechte: restricted_local` eingetragen; tatsächlich weist Seite 4 des Werks explizit **CC BY 2.0** aus (analog zu den Connexions-Modulen von Catherine Schmidt-Jones in Klasse B).
- **Konvertierungsverfahren:** Direkt-OCR über `pypdfium2` (Skalierungsfaktor 2,5) und `RapidOCR` (Torch), zeilenweise mit exakten Seitenankern `<!-- PDF-Seite 1 -->` bis `<!-- PDF-Seite 277 -->` (alle 277 Seiten lückenlos vorhanden).
- **Struktur & Nutzbarkeit:**
  - Das gesamte Inhaltsverzeichnis (Kapitel 1 *Notation*, 2 *Definitions*, 3 *The Physical Basis*, 4 *Notes and Scales*, 5 *Harmony and Form*, 6 *Challenges*, inkl. *Solutions* und *Attributions*) sowie der englische Lehrtext aller 277 Seiten sind seitengetreu durchsuchbar.
- **Dokumentiertes OCR-Fehlerprofil:**
  1. **Keine Markdown-Überschriftenhierarchie:** Da der Lauf zeilenweise über `RapidOCR` ohne Layout-Parser erfolgte, sind Kapitel- und Abschnittsüberschriften (`Chapter 1`, `1.1 Pitch`, `5.4 Beyond Triads: Naming Other Chords`) als normale Textzeilen ohne `#`-Präfix abgelegt; die vier zufälligen `#`-Zeilen (`#9`, `#`, `#P/q`, `#8`) stammen aus erkannten Kreuz-Vorzeichen (`#`) in Notengrafiken.
  2. **115 Zeilen mit OCR-Fragmenten aus Notengrafiken und Fettdruck:** Eingebettete Notoliniensysteme, Taktstriche und fetter Fließtext führten an rund 115 Stellen (von 11.011 Zeilen, ca. 1 %) zu Buchstaben-Fragmentzeilen wie `n me nn n    m     n mos` (Zeile 201) oder `osss s ss    n  ss n  s s n oe` (Zeile 499, Versuch der Texterkennung auf Notenlinien).
  3. **Leichte Buchstabentrennungen bei `th`/`st`:** Durch das Kerning der Connexions-PDF-Schrift fügte RapidOCR gelegentlich ein Leerzeichen nach `t` ein (`Rhyt hm`, `alt hough`, `furt her`, `wit hout`, `eit her`, `st udents`).

---

## 4. Gesamtergebnis

1. **Alle 18 eindeutigen HTML-Extrakte (26 Pfade)** sind strukturell gegen ihre HTML-Quellen geprüft:
   - **12 von 18** (`10` Ableton-Artikel + `2` ModeWheel-Seiten) bilden den Hauptinhalt ohne Duplikate vollständig ab (die SVG-Warnung bei Ableton betrifft nur UI-Icons).
   - **4 von 18** (`chordfiles.com`-Seiten) enthalten den vollständigen Text und alle Akkordbeispiele, verdoppeln aber einzelne Sektionen wegen des responsiven Desktop-/Mobil-DOMs im Quell-HTML.
   - **1 von 18** (`Reddit-Users-chat-about-chord-files.md`) enthält den vollständigen Reddit-Thread inkl. 3 eingebetteter Werbe-Posts aus dem Original-DOM.
   - **1 von 18** (`The Chord Wheel.md`) gibt das Quell-HTML samt Tabelle exakt wieder, entlarvt die HTML-Datei selbst aber als KI-/SEO-Text mit halluzinierter Historie (*„Klaus Vogel 1997“*), die nicht in `knowledge/` übernommen werden darf.
2. **Beide OCR-Neuläufe** (`Music_Theory_Advanced_Level.md` und `Understanding_Basic_Music_Theory.md`) sind für die Volltextsuche und Quellenprüfung voll nutzbar; ihre spezifischen Artefakte (`16` ausgelassene Formelblöcke bzw. `115` Notenlinien-/Fettdruck-Fragmente und fehlende `#`-Überschriften) sowie die Lizenz von `Understanding_Basic_Music_Theory.pdf` (**CC BY 2.0**, Catherine Schmidt-Jones / Connexions 2007) sind hiermit dokumentiert.
