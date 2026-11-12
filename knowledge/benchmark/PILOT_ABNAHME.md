# Pilot · fachliche Abnahmeliste

**Dokumentierte Freigaben im Register: 7 von 8.**

Je Aussage im Draft-PR entscheiden: freigegeben, Korrektur erforderlich oder Beleg fehlt.
Für jede Freigabe Claim-ID und vollständigen Fassungsfingerabdruck angeben.
Bei Korrektur oder fehlendem Beleg bitte die konkrete Passage benennen.

## PILOT-NOTATION-001

- Stand · Freigabe eingetragen
- Art · `convention`
- Fassung · `c7e2d362ebaf417bd7d1825eec0660d18ee9876cc519ecc3c2a9c47f7acd1d52`
- Wortlaut · Akkordsymbole verwenden internationale Schreibweise. In deutschen Notennamen entsprechen H und B dem internationalen B und B♭, As entspricht A♭.
- Gültigkeitsbereich · Schreibkonvention für die drei Pilotbeispiele. Die Zuordnung ändert keine Tonhöhe.
- Gegencheck · H3 und internationales B3 liegen bei MIDI 59. Deutsches B3 und internationales B♭3 liegen bei MIDI 58. As4 und A♭4 liegen bei MIDI 68.
- Fundstelle · [Yale University Library – The names of keys in French, German, Italian, and Spanish](<https://web.library.yale.edu/printpdf/cataloging/music/names-keys-french-german-italian-and-spanish>) · S. 1, Vergleichstabelle der Tonbuchstaben und Vorzeichen, Zeilen A flat, B flat und B
- Prüffrage · Welche internationalen Notennamen und MIDI-Werte entsprechen H3, B3 und As4 auf Deutsch?
- Sollantwort · `[59, 58, 68]`
- Herleitung · Yale University Library, The names of keys, S. 1, Zeilen A flat, B flat und B. C4=60, dann Halbtonabstände.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-001-HARMONY

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `7119ef6ba5e307541ddb848668f6cf9c7030cd252bc53279566f4c93a645e2ec`
- Wortlaut · Unter der Annahme C-Dur entsprechen C–G–Am–F den Stufen I–V–vi–IV.
- Gültigkeitsbereich · Dur-Stufenmodell mit C als Tonika. Akkorde in Grundstellung, ohne Aussage zur gehörten Tonika.
- Gegencheck · Die Grundtöne C, G, A und F belegen die Stufen 1, 5, 6 und 4. Die Sollakkordtöne sind C–E–G, G–H–D, A–C–E und F–A–C.
- Fundstelle · [Open Music Theory – Roman Numerals](<https://viva.pressbooks.pub/openmusictheory/chapter/roman-numerals/>) · Roman Numerals, Example 3 und Abschnitt zur Groß-/Kleinschreibung
- Fundstelle · [Open Music Theory – Four-Chord Schemas](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/4-chord-schemas/>) · Singer/Songwriter Schema, Key Takeaways: Rotation I–V–vi–IV
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-001 in C-Dur?
- Sollantwort · `{"stages": ["I", "V", "vi", "IV"], "chords": ["C", "G", "Am", "F"], "pitch_classes": [[0, 4, 7], [2, 7, 11], [0, 4, 9], [0, 5, 9]]}`
- Herleitung · C-Dur-Diatonik und Terzschichtung. Open Music Theory, Roman Numerals, Example 3 und Four-Chord Schemas, Singer/Songwriter Schema.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-001-TONAL-CENTER

- Stand · Ausstehend
- Art · `style_interpretation`
- Fassung · `a5341acfba10e95b2c46c463dae522a90ae22489b9726af4b7199405af1a9572`
- Wortlaut · Im Pop-Loop kann die Melodie die Wahrnehmung von C oder A als tonales Zentrum stützen.
- Gültigkeitsbereich · Interpretation eines zyklischen Pop-Schemas. Ohne Melodie und Phrasierung ist das wahrgenommene Zentrum hier offen.
- Gegencheck · Bei C als Zentrum liest sich die Folge als I–V–vi–IV. Bei A als Zentrum lässt sich dieselbe Akkordfolge als III–VII–i–VI in natürlichem Moll lesen. Die Akkordliste allein entscheidet nicht zwischen den Lesarten.
- Fundstelle · [Open Music Theory – Four-Chord Schemas](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/4-chord-schemas/>) · Singer/Songwriter Schema, Absatz nach Example 4 über relatives Moll und melodische Bezugstöne
- Prüffrage · Kann der Loop C–G–Am–F sowohl C als auch A als Zentrum nahelegen, und welche Hinweise entscheiden?
- Sollantwort · `{"centers": ["C", "A"], "minor_stages": ["III", "VII", "i", "VI"], "chords": ["C", "G", "Am", "F"], "required_context": "Melodie, Phrasierung und Loop-Grenzen. Ohne Kontext kein eindeutiges Zentrum."}`
- Herleitung · Open Music Theory, Four-Chord Schemas, Absatz nach Example 4. Das relative Moll ergibt sich aus natürlichem A-Moll.

## PROG-003-HARMONY

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `e58aae0c9337cc7d0d043e8ad8df35c411fe5dc4301153e6f5c14dcce8d75037`
- Wortlaut · Dm7–G7–Cmaj7 bildet in C-Dur die Jazzfolge ii⁷–V⁷–Imaj7.
- Gültigkeitsbereich · Dur-Variante des ii–V–I-Schemas mit Septakkorden in C-Dur.
- Gegencheck · Die Grundtöne D, G, C liegen auf 2, 5, 1. Die Sollakkordtöne sind D–F–A–C, G–H–D–F und C–E–G–H.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/ii-v-i/>) · Key Takeaways, Dur-Variante ii⁷–V⁷–Imaj7
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-003 in C-Dur?
- Sollantwort · `{"stages": ["ii^7", "V^7", "I^maj7"], "chords": ["Dm7", "G7", "Cmaj7"], "pitch_classes": [[0, 2, 5, 9], [2, 5, 7, 11], [0, 4, 7, 11]]}`
- Herleitung · Terzschichtung über D, G, C. Open Music Theory, ii–V–I, Key Takeaways zur Dur-Variante.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-003-VOICE-II-V

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `9afdbfa8083cb0817dcba7c5a263d96a0f79b36dae98617d3ff07ce8fb5c5f07`
- Wortlaut · Eine mögliche Stimme sinkt von C im Dm7 zu H im G7 um einen Halbton.
- Gültigkeitsbereich · Lokale Stimmführungsoption in 12-TET, etwa C4→H3. Die Aussage legt kein vollständiges Voicing fest.
- Gegencheck · C ist die kleine Septime von Dm7. H ist die große Terz von G7. In der angegebenen Lage ergibt 59 − 60 = −1 Halbton.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/ii-v-i/>) · Key Takeaways zur Folge Mollseptakkord–Dominantseptakkord–Durseptakkord. Die konkrete Stimme ist eine STEPS-Ableitung aus diesen Akkordtönen.
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[0, "C4"], [1, "H3"]], "midi": [60, 59], "delta": [-1]}`
- Herleitung · Dm7 enthält C, G7 enthält H. 59−60=−1. OMT ii–V–I stützt Akkordqualitäten, die konkrete Stimme ist abgeleitet.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-003-VOICE-V-I

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `f60c73fd68e282cbd83da983fb48eba09f967328a164c60f78379098a63f09ad`
- Wortlaut · Eine mögliche Stimme sinkt von F im G7 zu E im Cmaj7 um einen Halbton.
- Gültigkeitsbereich · Lokale Stimmführungsoption in 12-TET, etwa F4→E4. Die Aussage legt kein vollständiges Voicing fest.
- Gegencheck · F ist die kleine Septime von G7. E ist die große Terz von Cmaj7. In der angegebenen Lage ergibt 64 − 65 = −1 Halbton.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/ii-v-i/>) · Key Takeaways zur Folge Mollseptakkord–Dominantseptakkord–Durseptakkord. Die konkrete Stimme ist eine STEPS-Ableitung aus diesen Akkordtönen.
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[1, "F4"], [2, "E4"]], "midi": [65, 64], "delta": [-1]}`
- Herleitung · G7 enthält F, Cmaj7 enthält E. 64−65=−1. OMT ii–V–I stützt Akkordqualitäten, die konkrete Stimme ist abgeleitet.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-009-HARMONY

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `3c8871af475486fd2c6abf7ded583b5ca81d5d227fff85baec4ee0e47f21ed2b`
- Wortlaut · C–F–Fm–C realisiert in C-Dur I–IV–iv–I mit einer Mollsubdominante.
- Gültigkeitsbereich · Plagale Wendung in Dur mit gleichbleibendem Subdominantgrundton F.
- Gegencheck · Die Folge enthält C–E–G, F–A–C, F–As–C und C–E–G. Nur die Terz wechselt beim Übergang von F zu Fm.
- Fundstelle · [Open Music Theory – Blues-Based Schemas](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/blues-based-schemas/>) · Plagal Sigh, Beschreibung des Schemas IV–iv–I
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-009 in C-Dur?
- Sollantwort · `{"stages": ["I", "IV", "iv", "I"], "chords": ["C", "F", "Fm", "C"], "pitch_classes": [[0, 4, 7], [0, 5, 9], [0, 5, 8], [0, 4, 7]]}`
- Herleitung · Dreiklänge mit unverändertem F-Grundton und abgesenkter Terz. Open Music Theory, Blues-Based Schemas, Plagal Sigh.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12

## PROG-009-VOICE-LEADING

- Stand · Freigabe eingetragen
- Art · `fact`
- Fassung · `b8f2c236c4c034d449003c57235bf5d1f60655dcc201ab23e19c3fd75182f39d`
- Wortlaut · Eine mögliche Stimme verbindet A in F-Dur, As in F-Moll und G in C-Dur durch zwei absteigende Halbtonschritte.
- Gültigkeitsbereich · Lokale Stimmführung des Schemas IV–iv–I in C-Dur bei gleichstufiger Stimmung, etwa A4→As4→G4.
- Gegencheck · A und As sind die Terzen von F und Fm. G ist die Quinte von C. MIDI 69→68→67 ergibt zweimal −1 Halbton.
- Fundstelle · [Open Music Theory – Blues-Based Schemas](<https://viva.pressbooks.pub/openmusictheorycopy/chapter/blues-based-schemas/>) · Plagal Sigh, Skalenstufenbewegung la–le–sol (6–♭6–5)
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[1, "A4"], [2, "As4"], [3, "G4"]], "midi": [69, 68, 67], "delta": [-1, -1]}`
- Herleitung · Terzen von F/Fm und Quinte von C. OMT Blues-Based Schemas, Plagal Sigh, 6–♭6–5.
- Entscheidung · [n05a-design](https://github.com/n05a-design/steps/pull/11#issuecomment-6833747279) · 2026-11-12
