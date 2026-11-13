# PR #22 – Quellenprüfung und technisches Korrekturvotum

Prüfdatum: 13. November 2026. Geprüft wurde der Quellenstand von
`4fdf050c8e5980334cdb1bfa2f8b8cd57a56aabf` zusammen mit `main`
`9d7fdb4c1810e9a49345b9ddf54fbd6b9278e2d1`.

## Ergebnis und Grenzen

Die sieben musikalischen Aussagen sind innerhalb ihrer ausdrücklich genannten
Modellgrenzen nachvollziehbar. Es wurde kein fachlicher Widerspruch festgestellt.
Für die drei ii–V–I-Claims ist das Votum positiv. Für die vier Claims zu Pop-Loop
und Mollsubdominante ist es hinsichtlich der konkreten neuen Quellenfassungen
bedingt: Die beiden neuen Kapitel-URLs lieferten beim direkten Abruf HTTP 403.
Indexierter Primärtext bzw. weitere Seiten desselben Lehrbuchs stützen die
Aussagen, ersetzen aber keinen vollständigen aktuellen Direktvergleich der
beiden Kapitel.

Dies ist ein agentisches Prüfvotum, **keine menschliche Fachfreigabe**. Es wurden
keine neuen Freigaben im Register eingetragen. Die sieben alten Registereinträge
decken die neuen Quellenmetadaten nicht ab. Evidence- und Publikationsgate müssen
bis zur echten erneuten Abnahme weiter blockieren.

## Quellen und Zugriff

- [OMT: Roman Numerals](https://viva.pressbooks.pub/openmusictheory/chapter/roman-numerals/): direkt abrufbar; Stufenbezeichnung und Akkordqualitäten.
- [OMT: ii–V–I](https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/): direkt abrufbar; Key Takeaways zur Dur-Variante mit Septakkorden.
- [OMT: Four-Chord Schemas](https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/): Direktabruf HTTP 403; indexierter Text der kanonischen URL, Crawl laut Suchdienst etwa fünf Monate alt. Die Abschnitte Singer/Songwriter und Tonal ambiguity stützen Rotation und kontextabhängiges Dur-/Mollzentrum. Der Absatz zur Mehrdeutigkeit steht vor der Legende zu Example 4. Aktueller Direktvergleich offen.
- [Richards (2017): Tonal Ambiguity in Popular Music’s Axis Progressions](https://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html): direkt abrufbar; Abs. [1], [9]–[11], [28]–[30] und Anm. 10 stützen die Kontextgrenzen der Analyse.
- [OMT: Blues-Based Schemas, kanonische URL](https://viva.pressbooks.pub/openmusictheory/chapter/blues-based-schemas/): Direktabruf HTTP 403. Das Zielkapitel ist im kanonischen Inhaltsverzeichnis gelistet; sein aktueller Volltext wurde nicht direkt geprüft.
- [OMT: Blues-Based Schemas, bisherige Kopie](https://viva.pressbooks.pub/openmusictheorycopy/chapter/blues-based-schemas/): indexierter Primärtext stützt IV–iv–I und die absteigende Linie 6–♭6–5. Dies bestätigt den fachlichen Ausgangsbeleg, nicht die Identität der neuen Kapitelversion.
- [OMT: kanonisches Glossar](https://viva.pressbooks.pub/openmusictheory/back-matter/glossary/), Eintrag minor iv schema, und [Schemas-Übersicht](https://viva.pressbooks.pub/openmusictheory/chapter/intro-to-pop-schemas/): indexierter Text der Hauptausgabe stützt das Schema zusätzlich.

Die Aussagen wurden paraphrasiert und mit eigenen Akkordton-/Halbtonrechnungen
gegengeprüft. Fremde Volltexte, Notenbilder und Medien wurden nicht übernommen.

## Votum je geänderter Aussage

| Claim | Fachlicher Gegencheck | Votum zur vorgeschlagenen Fassung |
| --- | --- | --- |
| PROG-001-HARMONY | Unter der expliziten Annahme C-Dur sind C, G, Am, F die Stufen I, V, vi, IV. Die Akkordtöne stimmen; daraus folgt keine eindeutige gehörte Tonika. | Inhaltlich positiv; neuer Four-Chord-Kapitelbeleg nur indexiert geprüft. |
| PROG-001-TONAL-CENTER | Bei C als angenommenem Zentrum I–V–vi–IV; bei A in natürlichem Moll III–VII–i–VI. Richards und der indexierte OMT-Abschnitt stützen die Abhängigkeit von Melodie, Phrasierung, metrischem Beginn und Formkontext. | Inhaltlich positiv mit den vorhandenen Kontextgrenzen; aktuelle kanonische OMT-Passage noch direkt zu vergleichen. |
| PROG-003-HARMONY | D–F–A–C, G–H–D–F, C–E–G–H ergeben ii⁷–V⁷–Imaj7 in C-Dur. OMT bestätigt die Akkordqualitäten. | Positiv. |
| PROG-003-VOICE-II-V | C ist die Septime von Dm7, H die Terz von G7. MIDI 60→59 ergibt −1 Halbton. Dies ist eine eigene STEPS-Ableitung, keine behauptete vollständige Satzregel. | Positiv als lokale mögliche Stimme. |
| PROG-003-VOICE-V-I | F ist die Septime von G7, E die Terz von Cmaj7. MIDI 65→64 ergibt −1 Halbton. | Positiv als lokale mögliche Stimme. |
| PROG-009-HARMONY | C–F–Fm–C entspricht I–IV–iv–I in C-Dur. F–A–C wird zu F–As–C; das Grundtonmodell bleibt gleich. | Inhaltlich positiv; aktueller kanonischer Kapiteltext noch direkt zu vergleichen. |
| PROG-009-VOICE-LEADING | A–As–G gehört nacheinander zu F, Fm, C. MIDI 69→68→67 ergibt zwei absteigende Halbtöne; das entspricht 6–♭6–5. | Inhaltlich positiv als lokale Stimme; Vorbehalt zur neuen Kapitelversion bleibt. |

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

Die beiden kanonischen Kapitel direkt prüfen, danach die sieben konkreten
Claim-/Fingerprint-Paare durch ein zugelassenes menschliches Reviewkonto
entscheiden lassen. Erst nach echten Belegen das Freigaberegister und die
generierten Lerntexte aktualisieren und die Coverage erneut erzeugen. Dieser PR
bleibt bis dahin Draft; es erfolgt kein Merge.
