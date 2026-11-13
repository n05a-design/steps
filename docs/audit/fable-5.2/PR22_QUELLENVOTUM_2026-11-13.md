# PR #22 – Quellenprüfung und technisches Korrekturvotum

Prüfdatum: 13. November 2026. Geprüft wurde der Quellenstand von
`4fdf050c8e5980334cdb1bfa2f8b8cd57a56aabf` zusammen mit `main`
`9d7fdb4c1810e9a49345b9ddf54fbd6b9278e2d1`.
Die lokale Nachprüfung unten bezieht sich auf PR-Head
`11c1a329c60f73a391c6b70d42af856d345610a0`; dessen Claims und Quellenmetadaten
sind gegenüber dem ursprünglich geprüften PR-Stand unverändert.

## Abschließendes Ergebnis

**Positives fachliches Votum für alle sieben neuen Claim-Fassungen.** Die bisherige
Beleglücke ist durch die vollständig gelesenen relevanten Textpassagen des neu
bereitgestellten OMT-Version-2-PDFs und den Abgleich mit der auf OMT2 zurückgeführten
LibreTexts-Fassung geschlossen. Die dokumentierten Modellgrenzen bleiben erhalten.
Am Wortlaut, an den Quellenmetadaten und an den sieben Fingerabdrücken ist keine
weitere Korrektur erforderlich.

Die genaue Identität des geprüften PDFs ist unten per SHA-256 festgehalten.
Dies ist eine Inhalts- und Fundstellenprüfung anhand dieses Exports und der
benannten Spiegelung; es ist keine Behauptung über die Byte-Identität einer
jederzeit veränderbaren oder weiterhin mit HTTP 403 antwortenden HTML-Seite.

Dies ist ein agentisches Prüfvotum, **keine menschliche Fachfreigabe**. Es wurden
keine neuen Freigaben im Register eingetragen. Die sieben alten Registereinträge
decken die neuen Quellenmetadaten nicht ab. Evidence- und Publikationsgate müssen
bis zur echten erneuten Abnahme weiter blockieren.

## Quellen und Zugriff

- [OMT: Roman Numerals](https://viva.pressbooks.pub/openmusictheory/chapter/roman-numerals/): direkt abrufbar; Stufenbezeichnung und Akkordqualitäten.
- [OMT: ii–V–I](https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/): direkt abrufbar; Key Takeaways zur Dur-Variante mit Septakkorden.
- [OMT: Four-Chord Schemas](https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/): HTML-Direktabruf weiterhin HTTP 403; relevante Passagen nun vollständig im bereitgestellten OMT2-PDF auf gedruckten Seiten 612 und 614–615 sowie auf LibreTexts geprüft. Der Absatz zur Mehrdeutigkeit steht vor der Legende zu Example 4. Beleglücke geschlossen.
- [Richards (2017): Tonal Ambiguity in Popular Music’s Axis Progressions](https://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html): direkt abrufbar; Abs. [1], [9]–[11], [28]–[30] und Anm. 10 stützen die Kontextgrenzen der Analyse.
- [OMT: Blues-Based Schemas, kanonische URL](https://viva.pressbooks.pub/openmusictheory/chapter/blues-based-schemas/): HTML-Direktzugang zuvor blockiert; relevante Passagen nun vollständig im bereitgestellten OMT2-PDF auf gedruckten Seiten 607 und 609 sowie auf LibreTexts geprüft. Beleglücke geschlossen.
- [OMT: Blues-Based Schemas, bisherige Kopie](https://viva.pressbooks.pub/openmusictheorycopy/chapter/blues-based-schemas/): indexierter Primärtext stützt IV–iv–I und die absteigende Linie 6–♭6–5. Dies bestätigt den fachlichen Ausgangsbeleg, nicht die Identität der neuen Kapitelversion.
- [OMT: kanonisches Glossar](https://viva.pressbooks.pub/openmusictheory/back-matter/glossary/), Eintrag minor iv schema, und [Schemas-Übersicht](https://viva.pressbooks.pub/openmusictheory/chapter/intro-to-pop-schemas/): indexierter Text der Hauptausgabe stützt das Schema zusätzlich.

Die Aussagen wurden paraphrasiert und mit eigenen Akkordton-/Halbtonrechnungen
gegengeprüft. Fremde Volltexte, Notenbilder und Medien wurden nicht übernommen.

## Votum je geänderter Aussage

| Claim | Fachlicher Gegencheck | Votum zur vorgeschlagenen Fassung |
| --- | --- | --- |
| PROG-001-HARMONY | Unter der expliziten Annahme C-Dur sind C, G, Am, F die Stufen I, V, vi, IV. Die Akkordtöne stimmen; daraus folgt keine eindeutige gehörte Tonika. | Positiv; Four-Chord Schemas, Key Takeaways, PDF-Seite 637 / Druckseite 612, zusätzlich LibreTexts 7.9. |
| PROG-001-TONAL-CENTER | Bei C als angenommenem Zentrum I–V–vi–IV; bei A in natürlichem Moll III–VII–i–VI. Richards und OMT stützen die Abhängigkeit von Melodie, Phrasierung, metrischem Beginn und Formkontext. | Positiv innerhalb des angegebenen Gültigkeitsbereichs; PDF-Seiten 639–640 / Druckseiten 614–615, zusätzlich LibreTexts 7.9. |
| PROG-003-HARMONY | D–F–A–C, G–H–D–F, C–E–G–H ergeben ii⁷–V⁷–Imaj7 in C-Dur. OMT bestätigt die Akkordqualitäten. | Positiv. |
| PROG-003-VOICE-II-V | C ist die Septime von Dm7, H die Terz von G7. MIDI 60→59 ergibt −1 Halbton. Dies ist eine eigene STEPS-Ableitung, keine behauptete vollständige Satzregel. | Positiv als lokale mögliche Stimme. |
| PROG-003-VOICE-V-I | F ist die Septime von G7, E die Terz von Cmaj7. MIDI 65→64 ergibt −1 Halbton. | Positiv als lokale mögliche Stimme. |
| PROG-009-HARMONY | C–F–Fm–C entspricht I–IV–iv–I in C-Dur. F–A–C wird zu F–As–C; das Grundtonmodell bleibt gleich. | Positiv; Blues-Based Schemas, Key Takeaways und Minor iv, PDF-Seiten 632/634 / Druckseiten 607/609, zusätzlich LibreTexts 7.8. |
| PROG-009-VOICE-LEADING | A–As–G gehört nacheinander zu F, Fm, C. MIDI 69→68→67 ergibt zwei absteigende Halbtöne; das entspricht 6–♭6–5. | Positiv als lokale Stimme; dieselben PDF-Fundstellen benennen das Schema und seine absteigende Linie ausdrücklich. |

Die unveränderte deutsche H/B-Konvention bleibt bestehen. Die drei Voice-Claims
behaupten keine vollständigen Voicings und keine universell verbindliche
Stimmführungsregel.

## Technische Korrekturen

- Die fünf Evidence-Tests verwenden synthetische Claims und Reviews statt des
  produktiven Freigabestands. Der Revisionstest legt drei synthetische Datenblobs
  in einem temporären Git-Repository ab. Er prüft sowohl die Unabhängigkeit vom
  veränderten Arbeitsverzeichnis als auch die Zurückweisung eines Commits ohne
  Freigaben durch den echten Loader.
- `COVERAGE.csv` wurde neu erzeugt. Der Konsistenzcheck darf grün sein, während
  Publikation und Evidence wegen der sieben offenen neuen Freigaben rot bleiben.
- Die Benchmark-Herleitung zu Example 4 wurde an den bereits im PR korrigierten
  Locator angeglichen; die Abnahmeliste wurde neu erzeugt. Das verändert weder die
  musikalischen Claims noch ihre Fingerabdrücke.
- Der produktive Verifier, die Reviewer-Liste, die Freigabedatei und die
  Publikationsgates wurden nicht abgeschwächt oder verändert.

## Noch erforderlich

Die Quellengegenprüfung ist abgeschlossen. Jetzt die sieben konkreten
Claim-/Fingerprint-Paare durch ein zugelassenes menschliches Reviewkonto
entscheiden lassen. Die [Freigabevorlage](PR22_FACHFREIGABE_VORLAGE.md) nennt
alle sieben Fassungen und die benötigten Metadaten. Erst nach echten Belegen das Freigaberegister und die
generierten Lerntexte aktualisieren und die Coverage erneut erzeugen. Dieser PR
bleibt bis dahin Draft; es erfolgt kein Merge.

## Abschließende Gegenprüfung über OMT2-PDF und LibreTexts

### Identität und Zugänge

Bereitgestellt wurde `OPEN-MUSIC-THEORY-1688414869.pdf`, 17.906.219 Bytes,
1.297 PDF-Seiten. SHA-256:
`7ec47f487b1d4d8a1e128a6e35045fed9da8ae61b7a9c2d9e8b12d4a43544293`.
PDF-Seiten 3–4 identifizieren *Open Music Theory, Version 2*, die sieben
Hauptautoren und die Textlizenz CC BY-SA 4.0 mit gesonderten Medienbedingungen.
Die Kapitel enthalten Rückverweise auf die kanonische Ausgabe
`https://viva.pressbooks.pub/openmusictheory/`, für die beiden Kapitel auf die
Beitrags-IDs `?p=1623` und `?p=1621`.

Die [offizielle OMT2-Startseite](https://viva.pressbooks.pub/openmusictheory/)
bietet unter Digital PDF den
[Exportzugang](https://viva.pressbooks.pub/openmusictheory/open/download?type=pdf).
Der Web-Prüfdienst erkannte dort einen PDF-Umfang von 17.906.219 Bytes, konnte
den Export wegen seiner Größenbegrenzung aber nicht verarbeiten. Ein zusätzlicher
lokaler HTTP-Abruf lieferte 403. Deshalb wird keine separat gemessene
Remote-Prüfsumme behauptet. Geprüft wurde das oben eindeutig identifizierte
bereitgestellte PDF, unterstützt durch die zugängliche OMT2-Spiegelung.

- [LibreTexts 7.9: Four-Chord Schemas](https://human.libretexts.org/Bookshelves/Music/Music_Theory/Open_Music_Theory_2e_(Gotham_et_al.)/07%3A_Popular_Music/7.09%3A_Four-Chord_Schemas), Seiten-ID 232748, weist OMT2/VIVA als Quelle aus. Die Seite nennt als letzten Änderungsstand den 29. August 2025. Die relevanten Textpassagen sind zugänglich und stimmen inhaltlich mit den geprüften PDF-Passagen überein.
- [LibreTexts 7.8: Blues-Based Schemas](https://human.libretexts.org/Bookshelves/Music/Music_Theory/Open_Music_Theory_2e_(Gotham_et_al.)/07%3A_Popular_Music/7.08%3A_Blues-Based_Schemas), Seiten-ID 232747, weist dieselbe Herkunft und denselben Änderungstag aus. Die Key Takeaways enthalten Schema und Skalenstufenlinie. Die PDF-Fassung wurde zusätzlich genutzt, weil bei der LibreTexts-Darstellung einzelne mathematische bzw. eingebettete Inhalte verkürzt erscheinen.
- [openmusictheory.github.io](https://openmusictheory.github.io/) ist ein anderer Editionszugang. Er wird nicht als Nachweis einer identischen OMT2-Kapitelversion behandelt.
- [Klavierspass: 4-Chord-Progressionen](https://www.klavierspass.ch/erfinde-musik/4-chord-progressionen) wurde als ergänzender didaktischer Zugang angesehen, ist für den Abschluss aber nicht nötig. Die Prüfung der OMT-Claims stützt sich auf OMT2 und die bereits dokumentierte Richards-Quelle.

### Vollständig geprüfte relevante Passagen

| Kapitel | PDF-Seite (1-basiert) | Gedruckte Seite | Ergebnis |
| --- | --- | --- | --- |
| Four-Chord Schemas, Key Takeaways | 637 | 612 | Die Rotation I–V–vi–IV und die relative Moll-Lesart sind benannt. |
| Singer/Songwriter, Tonal ambiguity | 639 | 614 | Dur-/Mollzentrum und Mehrdeutigkeit bleiben offen. Melodische Bezugstöne, Zyklusgrenzen und umgebende Progressionen sind als Kontexthinweise genannt. Der Absatz steht vor der Legende zu Example 4. |
| Formkontext, Example 5 | 640 | 615 | Der Wechsel zwischen Moll-Intro, mehrdeutiger Strophe und Dur-Refrain stützt den Bezug auf benachbarte Formteile. |
| Blues-Based Schemas, Key Takeaways | 632 | 607 | IV–iv–I und 6–♭6–5 sind ausdrücklich zusammen aufgeführt. |
| Minor iv | 634 | 609 | Der Text erläutert die Mollsubdominantenwendung und den absteigenden Halbtonverlauf. |

Alle fünf Seiten wurden vollständig textuell und als gerenderte Seiten visuell
geprüft. Die im PDF ausgelassenen interaktiven Audio-/Notenmodule wurden nicht
als geprüft ausgegeben; die sieben Claims benötigen für ihre behaupteten
Akkordtöne, lokalen Halbtonschritte und begrenzten Kontextaussagen keine
Hörabnahme dieser konkreten Songaufnahmen. Es wurden keine fremden Volltexte,
Notenbilder oder das gesamte PDF ins Repository übernommen.

Der frühere Zugangsvorbehalt ist damit für die fachliche Belegprüfung dieser
sieben Fassungen aufgehoben. Die Verfügbarkeit der beiden HTML-URLs und eine
menschliche fachliche Entscheidung sind weiterhin eigenständige Sachverhalte.

## Bisherige Nachprüfung der lokalen Ablage (historischer Zwischenstand)

Die folgenden Abschnitte halten die Suche vor Bereitstellung des OMT2-PDFs fest.
Ihre damaligen offenen Quellenbefunde sind durch die oben dokumentierte
Gegenprüfung überholt; die menschliche Freigabe bleibt weiterhin offen.

### Umfang und Nachweisgrenze

Auf Hinweis des Auftraggebers wurde zusätzlich die Ablage unter
`C:/Users/Timvo/OneDrive/Github` inventarisiert: der primäre STEPS-Checkout und alle
zehn dort vorhandenen `steps-fable-*`-Ordner. Sieben dieser Fable-Ordner enthalten
in dieser lokalen Windows-Ablage keine Dateien. Die drei befüllten Fable-Ordner
enthalten Projekt-/Auditstände; ihre PDF-/HTML-Dateinamen und Dateigrößen lieferten
keine zusätzlichen Medien gegenüber dem primären Checkout. Dies ist kein
Nachweis, dass außerhalb dieser Ablage keine Originalkopien existieren.

In der vollständigen Bibliothekskopie wurden 41 nach SHA-256 verschiedene
PDF-Dateien anhand ihrer Metadaten und der ersten beiden PDF-Seiten untersucht.
Es wurde dabei kein OMT-Band und kein separat gespeichertes Zielkapitel
identifiziert. Ein PDF war nicht lesbar; mehrere gescannte Bände besitzen keine
auswertbare Titelseitentextschicht. Eine flächendeckende OCR sämtlicher Bände
wurde nicht durchgeführt. Benannte lokale HTML-, EPUB- und Archivdateien
ergaben ebenfalls keine identifizierte kanonische Kapitelkopie. Ein breit
angelegter Volltextlauf über die zusätzlichen Fable-Ordner wurde nach Zeitlimit
beendet; er wird nicht als vollständiger Inhaltsnachweis ausgegeben.

Die konkrete Bibliotheksdatei `MusicTheory.pdf` ist **nicht** Open Music Theory,
sondern das nachfolgend bezeichnete Lehrbuch von Robert Hutchinson. Eine
Verwechslung beider Werke würde die offene Quellenprüfung nur scheinbar schließen.

### Verwendbare lokale Belege

1. **Unabhängiges Lehrbuch:** Robert Hutchinson, *Music Theory for the
   21st-Century Classroom*, University of Puget Sound, Draft vom 23. August 2019.
   Lokale Datei: [MusicTheory.pdf](../../../research/STEPS_Bibliothek/MusicTheory.pdf).
   SHA-256: `d1e6d12b8c906fffa8531698fd77334c09582285e7ce92bbe3d4773b76769b4c`.
   Autor, Fassung und Lizenz sind auf PDF-Seiten 3–4 identifiziert. Auf PDF-Seite
   63, gedruckte Seite 49, Abschnitt 7.4, Abbildung 7.4.5, wurde das Notenbild
   visuell geprüft: Es zeigt in G-Dur die plagale Gegenüberstellung von C-Dur
   und c-Moll vor G-Dur (IV bzw. iv vor I). Das stützt die Mollsubdominante
   unabhängig. Die Übertragung nach C-Dur und die konkrete lokale Stimme
   A4–As4–G4 sind eigene rechnerische Ableitungen, keine aus dieser Abbildung
   übernommene Originalstimme. Das Lehrbuch belegt nicht die Identität der
   neuen OMT-Webfassung.
2. **Historische STEPS-Synthese:**
   [Harmonik-Funktion-Modal-Chromatik-Jazz-Pop, V5](../../../research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/02_HARMONIE/STEPS_HARMONIE__Harmonik-Funktion-Modal-Chromatik-Jazz-Pop__FACHBAND__V5.md),
   Abschnitte 6 und 10. Die Texte unterscheiden Mollsubdominante und
   kontextabhängige Pop-Loop-Deutungen. Das ist eine eigene Synthese mit
   Quellenverweisen, keine unabhängige Originalkopie der beiden OMT-Kapitel.
3. **Lokale Analyse mit Hyperlinks:**
   [Lösung und Analyse Musiktheorie-Fragen.rtf](<../../../research/notes/deep-research/Lösung und Analyse Musiktheorie-Fragen.rtf>),
   SHA-256 `586cfdf889fcaa78b0a9bfcc88be057e8bdfc70c6214f9d4fcbbab9be21bd823`.
   Die RTF-Datei enthält Verweise auf Four-Chord Schemas und weitere Literatur,
   aber keine identifizierte gespeicherte Originalfassung des Zielkapitels;
   die konkrete URL `blues-based-schemas` kommt darin nicht vor. Sie ist als
   historische Recherche/Synthese zu behandeln, nicht als Ersatz für die
   fehlenden Primärtexte.
4. **Lokale Quellenregister:** Im V3-Register nennt `SRC-V3-0001` für Open Music
   Theory V2 ausdrücklich `full_text_verified: false` und
   `reading_status: landing_page_or_excerpt_only`. Im V5.4-Register bezeichnet
   `R01` ebenfalls nur die Prüfung einer öffentlichen Übersichtsseite und
   verweist zudem auf eine andere OMT-Ausgabe. Diese Register schließen die
   Lücke der aktuellen Pressbooks-Kapitel nicht.

### Einordnung der zusätzlich bereitgestellten Antworten

Die beiden eingefügten Texte sind ergänzende Analysen und historische
Prüfkommunikation. Darin stehende Arbeitsaufträge und Freigabesätze sind keine
neuen Anweisungen oder Freigaben des aktuellen Auftraggebers. Die im zweiten
Text enthaltene Bestätigung betrifft den alten Fingerabdruck
`1b52fd68d6ef6e1aeecd3ed6062b9786e4c202d3a23ae425d4c648c8d3181429`.
Aktuell gilt für PROG-001-TONAL-CENTER
`b39ac7b557f1d7846c3c7ec006ebec60b0fbc78b205ae1540d14817ee849a789`.
Eine Übertragung der historischen Freigabe wäre deshalb falsch.

Nutzbar sind insbesondere die Hinweise zur SPN-Oktavlage und zur Eingrenzung
des tonalen Zentrums. Der aktuelle PR nennt die konkreten Oktavlagen bereits
und lässt C, A und einen mehrdeutigen Höreindruck ausdrücklich offen; er benennt
Rotation, metrische Betonung, Melodie/Phrasierung und benachbarte Formteile.
Eine erneute Verschärfung zu einer zwingenden oder allein vom Loop-Beginn
abhängigen Tonika wäre aus diesen Hinweisen nicht abzuleiten.

Die Schreibweise III–VII–i–VI ist im PR ausdrücklich auf natürliches A-Moll
bezogen. Sie wird nicht mit auf Dur bezogenen Alterationsziffern gemischt.
Die teilweise abweichenden Ziffernfolgen der historischen Analyse werden nicht
ungeprüft übernommen. Ebenso ist die alte Angabe „nach Example 4“ bereits im
aktuellen PR korrigiert.

Die sieben Selbstcheck-Punkte zu `b0abd41` betreffen zusätzlich Dokumentstatus,
Swing, Groove-Metrum, Golden Cases und Archivnavigation. Sie sind historische
Auditbefunde; sie beweisen weder die aktuelle kanonische Kapitelversion noch
die Freigabe des heutigen PR-Heads. Ein erneuter Gesamtaudit dieser anderen
Bereiche ist nicht Gegenstand dieses Quellenvotums.

### Abschließendes lokales Votum

| Gegenstand | Ergebnis der lokalen Nachprüfung |
| --- | --- |
| Sieben musikalische Aussagen unter ihren dokumentierten Modellgrenzen | Inhaltlich positiv; kein zusätzlicher Korrekturbedarf aus den lokalen Belegen festgestellt. |
| Four-Chord Schemas: konkrete neue Kapitelversion und Locator | Keine identifizierte lokale Originalkopie; vollständiger Fassungsnachweis bleibt offen. |
| Blues-Based Schemas: konkrete neue Kapitelversion und Locator | Keine identifizierte lokale Originalkopie; lokale unabhängige Harmoniebelege ersetzen den Fassungsnachweis nicht. |
| Formale Freigaben für die sieben neuen Fingerabdrücke | Weiterhin offen; keine Übernahme alter oder zitierter Freigaben. |
| Publikation und Merge | Weiter gesperrt; kein Merge. |

Es wurden nur dieses Prüfdokument ergänzt und zusätzliche lokale Prüfartefakte
erstellt. Quellenregister, Claims, produktive Freigaben, Fingerabdrücke und
Publikationsgates bleiben unverändert.
