# Rechteinventar der Volltext-Extrakte (Stand 14.11.2026)

**Status:** Arbeitsgrundlage, keine Rechtsprüfung und keine Freigabe. Die Einordnung stützt sich auf Copyright-, Lizenz- und Herkunftshinweise, die in den Docling-Extrakten selbst stehen, und ist an den Originalen zu bestätigen. Wo kein Hinweis gefunden wurde, steht „kein Hinweis im Extrakt“.

## Ausgangslage

- Das Repository `n05a-design/steps` ist öffentlich. Die 40 eindeutigen PDFs liegen dort bereits seit `a14c3f3` (10.11.2026). Seit PR #63 kommen ihre Volltext-Extrakte hinzu, ebenso die Markdown-Extrakte von 18 gespeicherten Webseiten.
- [`knowledge/sources/RIGHTS_POLICY.md`](../../knowledge/sources/RIGHTS_POLICY.md) sieht für fremde Volltexte den Status `restricted_local` und eine Ablage außerhalb von Git vor. Der Inhaber hat die Versionierung der Extrakte am 14.11.2026 trotzdem entschieden ([OPEN_GAPS](OPEN_GAPS.md)).
- **Umsetzung am 14.11.2026:** Für die zehn Werke der Klasse E (13 Dateipfade) sind Original-PDFs und Volltext-Extrakte per `.gitignore` aus dem Repository genommen und liegen nur noch lokal (`restricted_local`). Im Repository stehen stattdessen eigene [Zusammenfassungen](../STEPS_Bibliothek/Zusammenfassungen/README.md).
- Ein Entfernen aus dem aktuellen Stand nimmt die Dateien nicht aus der Git-Historie. Dafür wäre ein Umschreiben der Historie nötig, das `AGENTS.md` nur nach gesonderter Prüfung, mit Backup und abgestimmt mit allen Klonen erlaubt.

## Einordnung der PDFs

Klassen: **A** offene Lizenz im Dokument belegt · **B** vermutlich gemeinfrei oder offen, nicht vollständig belegt · **C** vom Rechteinhaber frei verteiltes Material ohne offene Lizenz · **D** wissenschaftliche oder Lehrveröffentlichung mit unklarer Lizenz · **E** kommerzielles Werk, alle Rechte vorbehalten.

| Klasse | Datei (Kopien) | Hinweis im Extrakt | Anmerkung |
| --- | --- | --- | --- |
| A | `Popular_Music_Analysis_in_American_Music.pdf` (2) | Jocelyn Neal, CC BY 4.0 | Namensnennung erforderlich. |
| A | `s06-the-elements-of-rhythm-sound-s.pdf` | CC BY-NC-SA 3.0 | Nicht kommerziell; Weitergabe unter gleicher Lizenz. |
| A | `MusicTheory.pdf` | © 2017 Robert Hutchinson, GNU Free Documentation License 1.2+ | Lizenztext muss beiliegen. |
| B | `cu31924022305357.pdf` | Cornell University Library: keine bekannten US-Beschränkungen; Hugo Riemann, *Harmony Simplified* (Übers. H. Bewerunge, Augener, London 1896) | Autor († 1919) und Übersetzer († 1923) seit über 100 Jahren verstorben; gemeinfrei. |
| B | `Chord-Progressions.pdf` | Englischer Wikipedia-Artikel *Chord progression* (`oldid=441402396`, S. 7–8), CC BY-SA 3.0 Unported | Autorenliste und Bildlizenzen stehen auf S. 7–8 des Extrakts. |
| A | `Understanding_Basic_Music_Theory.pdf` (2) | nach OCR lesbar: © 2007 Catherine Schmidt-Jones (Co-Autor Russell Jones), Connexions (Rice University, `col10363/1.3`), CC BY 2.0 | Namensnennung erforderlich; Lizenzversion 2.0 auf S. 4 bestätigt. |
| C | `berklee-online-*-handbook.pdf` (3), `Music_theory_handbook.pdf` (2) | Berklee Online (*Digital Handbooks*, ca. 2018–2025) | Werbe-Handbücher; Download erlaubt, Weiterverbreitung nicht belegt. |
| C | `ModeWheel_Manual_1.21.pdf` (2) | Jeffrey M. Kunka, Mai 2023; Endbenutzer-Lizenzvertrag (S. 8–9) im Dokument | Software-Handbuch mit EULA (untersagt Weiterverbreitung der Software über Drittseiten). |
| C | `The Piano Chord Collection HI RES.pdf` | © Pianochord.org, Alle Rechte vorbehalten (S. 2) | |
| C | `the-chord-wheel.pdf` (2), `Circle_*_Modes.pdf` (4 × 2) | 4-seitiger Scraper-Flyer zu Jim Fleser / Hal Leonard bzw. 4 Drehscheiben von Oliver Prehn (`newjazz.dk`) & „nupfe“ | Herstellermaterial / Lehrbögen. |
| C | `101mixing&productiontips.pdf`, `How-to-Write-Music-Guide.pdf` | Jason Timothy (`MusicSoftwareTraining.com`) bzw. Guy Michelmore (`ThinkSpace Education`), keine Lizenz | Werbe-E-Books. |
| D | `Computational_Music_Theory.pdf` (2) | Georg Boenn, Martin Brain, Marina De Vos, John ffitch; © 2012 AAAI, alle Rechte vorbehalten | Konferenzbeitrag. |
| D | `Kants_Theory_of_Music.pdf` (2) | Oliver Thorndike, *Con-Textos Kantianos* 14 (2021), S. 416–438, DOI `10.5281/zenodo.5776100` | Open-Access-Zeitschrift; Lizenz im Original prüfen. |
| D | `Is_Generative_Theory_Misleading_for_Music.pdf` (2) | Rafael Barbosa, HAL-Preprint (`hal-02184441`, 2019) eines Springer-LNCS-Beitrags | Lizenz der HAL-Fassung prüfen. |
| D | `What_is_popular_music_And_what_isn_t_An.pdf` (2) | Markus Mantere (Vorwort) & Franco Fabbri, *Musiikki* 2/2010, S. 3–5, 72–92 | Zeitschriftenbeitrag. |
| D | `Mathematics_and_Music.pdf` (2) | David Wright, Washington University, 2009 | Vorlesungsskript. |
| D | `COGS_300_13_1_Rhythm_in_music.pdf` | Vorlesungsfolien (`COGS 300`) zu Aniruddh D. Patel (2008), Kap. 3.1–3.2 | Folien mit Buchinhalten. |
| D | `How-music-is-made-JOHN-VOJTOVITCH_EN.pdf`, `music-fundamentals-2-rhythm-and-meter.pdf`, `Name_Music_Theory_Worksheet_Music_Theory.pdf` (2), `THE_ELEMENTS_OF_MUSIC.pdf` (2) | Nachprüfung 16.11.2026: `music-fundamentals-2-rhythm-and-meter.pdf` stammt aus Catherine Schmidt-Jones’ Connexions-Kurs (CC BY, identisch mit Kap. 1.2 in `Understanding_Basic_Music_Theory.pdf`); `How-music-is-made` ist von John Vojtovitch (ohne Lizenz); die beiden übrigen sind ein britisches Arbeitsblatt-Heft (Worksheet 1–10) und ein US-College-Handout (Kap. 1 *The Elements of Music*) ohne Autorenangabe | Einzelbelege siehe [Quellenmetadaten-Bericht](../../docs/audit/fable-5.2/QUELLENMETADATEN_UND_CLAIMS_W01_W03_2026-11-16.md). |
| D | `Music_Theory_Advanced_Level.pdf` (2) | nach OCR lesbar: Zusammenstellung von Forenbeiträgen der Nutzerin „Eowyn“ auf mysongbook.com, Juni 2005 | Keine Lizenz genannt; Forenbeiträge bleiben urheberrechtlich bei der Verfasserin. |
| E | `Fundamentals of Music Proce_ (Z-Library).pdf` | Springer, ISBN 978-3-319-21944-8; Dateiname nennt Z-Library | **Höchstes Risiko:** kommerzielles Buch aus einer nicht autorisierten Quelle. |
| E | `Schachter_Aldwell-Harmony_Voice_Leading.pdf` | Lehrbuch (Aldwell/Schachter) | Kommerziell, Verlagsangabe im Extrakt nicht gefunden. |
| E | `Schoenberg_Arnold_Theory_of_Harmony_1983.pdf` | englische Übersetzung, Ausgabe 1983 | Übersetzung urheberrechtlich geschützt. |
| E | `the_practice_of_harmony_3rd_ed_peter_spencer.pdf` | © 1996 Prentice-Hall, alle Rechte vorbehalten | |
| E | `The-Complete-Book-of-Scales-Chords-Arpeggios-Cadences.pdf` | © 1994 Alfred Publishing, alle Rechte vorbehalten | |
| E | `Creative Sequencing Techniques for Music Production_ ….pdf` | © 2005 Andrea Pejrolo, alle Rechte vorbehalten | |
| E | `MakingMusic_DennisDeSantis.pdf`, `MakingMusic.pdf` (2) | alle Rechte vorbehalten, ISBN 978-3-9817165-0-4 | Drei Pfade, ein Blob. |
| E | `L-0002916879.pdf` (2) | © Suhrkamp 2006 / Polity Press 2009 | Leseprobe oder Auszug eines Verlagsbuchs. |
| E | `IMSLP342443-PMLP552428-hindemithTraditionalHarmonyBook.pdf` | © 1943/1944 Associated Music Publishers | Über IMSLP bezogen; Hindemith starb 1963, in der EU bis Ende 2033 geschützt. |
| E | `1500-chord-progressions-walter-1.pdf` | © 1958 New Sounds in Modern Music | US-Schutzstatus hängt von der Verlängerung ab; prüfen. |

Alle Zeilen der Klasse E sind seit dem 14.11.2026 nicht mehr versioniert; ihre Zusammenfassungen stehen unter [`research/STEPS_Bibliothek/Zusammenfassungen/`](../STEPS_Bibliothek/Zusammenfassungen/README.md).

## Gespeicherte Webseiten

Die 18 HTML-Seiten und ihre Extrakte sind Artikel des Ableton-Blogs, Seiten von chordfiles.com und modewheel, eine Produktseite zur Chord Wheel und eine Reddit-Diskussion. Für keine liegt eine offene Lizenz vor. Die `_files`-Ordner enthalten zusätzlich fremde Bilder, Skripte und Stylesheets.

## Qualität der Extrakte

- `Understanding_Basic_Music_Theory.pdf` und `Music_Theory_Advanced_Level.pdf` lieferten im ersten Docling-Lauf fast nur Zeichensalat (Schriftkodierung ohne Unicode-Zuordnung). Beide Extrakte sind am 14.11.2026 durch OCR-Neuläufe ersetzt: `Music_Theory_Advanced_Level` mit Docling und erzwungener Vollseiten-OCR, `Understanding_Basic_Music_Theory` per Direkt-OCR auf gerenderten Seiten, weil die Docling-OCR dort leer blieb. Die Methode steht jeweils im Frontmatter; OCR-Text bleibt prüfpflichtig.
- `1500-chord-progressions-walter-1.pdf` hat einen niedrigen Buchstabenanteil, weil das Dokument überwiegend aus Akkordsymbolen besteht. Die Akkordsymbole sind am Original zu prüfen.

## Entscheidungsoptionen für den Inhaber

1. **Repository privat stellen.** Das wirkt sofort für den aktuellen Stand und die Historie und erhält alle Nachweise. Externe Kopien, die bereits entstanden sind, bleiben davon unberührt.
2. **Klasse E aus dem aktuellen Stand entfernen** und lokal unter `restricted_local` führen. Die Historie enthält die Dateien weiterhin. *(Am 14.11.2026 umgesetzt.)*
3. **Historie bereinigen** für Klasse E und ggf. D. Das erfordert die gesonderte Prüfung nach `RIGHTS_POLICY.md`, ein Backup, einen Force-Push und neue Klone auf allen Rechnern.
4. **Status quo** mit Nachweis je Quelle. Das kommt nur für Klasse A und eingeschränkt B und C in Betracht.

Unabhängig davon sollte `Fundamentals of Music Proce_ (Z-Library).pdf` zuerst behandelt werden.

## Entscheidungen des Inhabers (14.11.2026)

- **Git-Historie:** bleibt unverändert; kein Umschreiben, kein Wechsel auf privat. Begründung des Inhabers: Die Inhalte sind nicht bekannt gemacht, und eine spätere automatische Löschung wird erwartet. Die Historie enthält die Klasse-E-Dateien bis dahin weiterhin.
- **Klasse E:** Option 2 umgesetzt (lokal, per `.gitignore`), Zusammenfassungen versioniert.
- **Klassen A–D und gespeicherte Webseiten:** bleiben versioniert. Der Inhaber stuft sie als frei zugängliche öffentliche Inhalte ein. Die Lizenzhinweise oben bleiben als Dokumentation bestehen.

## Entscheidungen des Inhabers (16.11.2026)

- **Müller, `Fundamentals of Music Proce_ (Z-Library).pdf`:** Die Herkunft wird in diesem Fall nicht weiter verfolgt. Mit der Zusammenfassung wird normal weitergearbeitet; eine lizenzierte Ausgabe wird nicht beschafft. Der Herkunftshinweis bleibt als Tatsache in den Kopfdaten stehen.
- **Hindemith, Schönberg:** Die unbelegten Rechtsaussagen (Schutzfristen, Gemeinfreiheit) sind aus den Zusammenfassungen gestrichen. Die Einordnung in der Tabelle oben bleibt als Stand vom 14.11.2026 erhalten.
