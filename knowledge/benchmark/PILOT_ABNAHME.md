# Pilot · fachliche Abnahmeliste

**Dokumentierte Freigaben im Register: 1 von 8.**

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

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `7a9f0ca6312eaa8837c45a624a0ca50cdde3f9af323e8fc81094519cd7c53a63`
- Wortlaut · Unter der Annahme C-Dur entsprechen C–G–Am–F den Stufen I–V–vi–IV.
- Gültigkeitsbereich · Dur-Stufenmodell mit C als Tonika. Akkorde in Grundstellung, ohne Aussage zur gehörten Tonika.
- Gegencheck · Die Grundtöne C, G, A und F belegen die Stufen 1, 5, 6 und 4. Die Sollakkordtöne sind C–E–G, G–H–D, A–C–E und F–A–C.
- Fundstelle · [Open Music Theory – Roman Numerals](<https://viva.pressbooks.pub/openmusictheory/chapter/roman-numerals/>) · Roman Numerals, Example 3 und Abschnitt zur Groß-/Kleinschreibung
- Fundstelle · [Open Music Theory – Four-Chord Schemas](<https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/>) · Singer/Songwriter Schema, Key Takeaways: Rotation I–V–vi–IV
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-001 in C-Dur?
- Sollantwort · `{"stages": ["I", "V", "vi", "IV"], "chords": ["C", "G", "Am", "F"], "pitch_classes": [[0, 4, 7], [2, 7, 11], [0, 4, 9], [0, 5, 9]]}`
- Herleitung · C-Dur-Diatonik und Terzschichtung. Open Music Theory, Roman Numerals, Example 3 und Four-Chord Schemas, Singer/Songwriter Schema.

## PROG-001-TONAL-CENTER

- Stand · Erneute Prüfung erforderlich
- Art · `style_interpretation`
- Fassung · `b39ac7b557f1d7846c3c7ec006ebec60b0fbc78b205ae1540d14817ee849a789`
- Wortlaut · Der Pop-Loop aus C, G, Am und F kann C oder A als tonales Zentrum nahelegen oder mehrdeutig bleiben. Melodie und Phrasierung, Loop-Beginn, metrische Betonung und benachbarte Formteile beeinflussen die Wahrnehmung.
- Gültigkeitsbereich · Gilt für das zyklische Popschema einschließlich seiner Rotationen. Für die gehörte Tonika kann etwa entscheidend sein, ob C oder Am am Beginn einer betonten Taktgruppe steht, auf welchem Ton eine Phrase endet und welches Zentrum ein benachbarter Formteil etabliert.
- Gegencheck · Bei C als Zentrum liest sich die Folge als I–V–vi–IV. Bei A als Zentrum lässt sich dieselbe Akkordfolge als III–VII–i–VI in natürlichem Moll lesen. Die Akkordliste allein entscheidet nicht zwischen den Lesarten.
- Fundstelle · [Open Music Theory – Four-Chord Schemas](<https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/>) · Singer/Songwriter Schema, Absatz vor der Legende zu Example 4 über relatives Moll und melodische Bezugstöne
- Fundstelle · [Music Theory Online – Tonal Ambiguity in Popular Music’s Axis Progressions](<https://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html>) · Abs. [1] zu Rotationen, [9]–[11] und Anm. 10 zu Loop-Beginn und Hypermetrik, [29]–[30] zu Phrasierung und Formkontext
- Prüffrage · Wie kann der Loop C–G–Am–F C oder A als tonales Zentrum nahelegen, und welche Hinweise prägen die Wahrnehmung?
- Sollantwort · `{"centers": ["C", "A"], "minor_stages": ["III", "VII", "i", "VI"], "chords": ["C", "G", "Am", "F"], "required_context": "Melodie und Phrasierung, Loop-Beginn, metrische Betonung und benachbarte Formteile können C oder A als Zentrum stützen. Die Akkordfolge allein lässt das gehörte Zentrum offen."}`
- Herleitung · Open Music Theory, Four-Chord Schemas, Abschnitt Tonal ambiguity, Absatz vor der Legende zu Example 4. Die Moll-Lesart folgt aus natürlichem A-Moll. Richards (2017), Abs. [1], [9]–[11] und [29]–[30], belegt die Kontexthinweise an Axis-Progressionen.

## PROG-003-HARMONY

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `f9224530c773e01d2da4ebc8136b7b10bdf073bc5079b866c003501441faec7a`
- Wortlaut · Dm7–G7–Cmaj7 bildet in C-Dur die Jazzfolge ii⁷–V⁷–Imaj7.
- Gültigkeitsbereich · Dur-Variante des ii–V–I-Schemas mit Septakkorden in C-Dur.
- Gegencheck · Die Grundtöne D, G, C liegen auf 2, 5, 1. Die Sollakkordtöne sind D–F–A–C, G–H–D–F und C–E–G–H.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/>) · Key Takeaways, Dur-Variante ii⁷–V⁷–Imaj7
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-003 in C-Dur?
- Sollantwort · `{"stages": ["ii^7", "V^7", "I^maj7"], "chords": ["Dm7", "G7", "Cmaj7"], "pitch_classes": [[0, 2, 5, 9], [2, 5, 7, 11], [0, 4, 7, 11]]}`
- Herleitung · Terzschichtung über D, G, C. Open Music Theory, ii–V–I, Key Takeaways zur Dur-Variante.

## PROG-003-VOICE-II-V

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `9dd3c60c8090e001841f83b29ca8c34f7071362ca6984fd107cfa9f3aadf2fcf`
- Wortlaut · Eine mögliche Stimme sinkt von C im Dm7 zu H im G7 um einen Halbton.
- Gültigkeitsbereich · Lokale Stimmführungsoption in 12-TET, etwa C4→H3. Die Aussage legt kein vollständiges Voicing fest.
- Gegencheck · C ist die kleine Septime von Dm7. H ist die große Terz von G7. In der angegebenen Lage ergibt 59 − 60 = −1 Halbton.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/>) · Key Takeaways zur Folge Mollseptakkord–Dominantseptakkord–Durseptakkord. Die konkrete Stimme ist eine STEPS-Ableitung aus diesen Akkordtönen.
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[0, "C4"], [1, "H3"]], "midi": [60, 59], "delta": [-1]}`
- Herleitung · Dm7 enthält C, G7 enthält H. 59−60=−1. OMT ii–V–I stützt Akkordqualitäten, die konkrete Stimme ist abgeleitet.

## PROG-003-VOICE-V-I

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `ae607536c2e00567c466a8367dbb30ffe24efc92c21fcce8a2237b25a05ba564`
- Wortlaut · Eine mögliche Stimme sinkt von F im G7 zu E im Cmaj7 um einen Halbton.
- Gültigkeitsbereich · Lokale Stimmführungsoption in 12-TET, etwa F4→E4. Die Aussage legt kein vollständiges Voicing fest.
- Gegencheck · F ist die kleine Septime von G7. E ist die große Terz von Cmaj7. In der angegebenen Lage ergibt 64 − 65 = −1 Halbton.
- Fundstelle · [Open Music Theory – ii–V–I](<https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/>) · Key Takeaways zur Folge Mollseptakkord–Dominantseptakkord–Durseptakkord. Die konkrete Stimme ist eine STEPS-Ableitung aus diesen Akkordtönen.
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[1, "F4"], [2, "E4"]], "midi": [65, 64], "delta": [-1]}`
- Herleitung · G7 enthält F, Cmaj7 enthält E. 64−65=−1. OMT ii–V–I stützt Akkordqualitäten, die konkrete Stimme ist abgeleitet.

## PROG-009-HARMONY

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `adadf2ef5902cb9b2f115060361f224a6faf15c766dfee99967badac4a363969`
- Wortlaut · C–F–Fm–C realisiert in C-Dur I–IV–iv–I mit einer Mollsubdominante.
- Gültigkeitsbereich · Plagale Wendung in Dur mit gleichbleibendem Subdominantgrundton F.
- Gegencheck · Die Folge enthält C–E–G, F–A–C, F–As–C und C–E–G. Nur die Terz wechselt beim Übergang von F zu Fm.
- Fundstelle · [Open Music Theory – Blues-Based Schemas](<https://viva.pressbooks.pub/openmusictheory/chapter/blues-based-schemas/>) · Plagal Sigh, Beschreibung des Schemas IV–iv–I
- Prüffrage · Welche Stufen, Akkorde und Tonklassen enthält PROG-009 in C-Dur?
- Sollantwort · `{"stages": ["I", "IV", "iv", "I"], "chords": ["C", "F", "Fm", "C"], "pitch_classes": [[0, 4, 7], [0, 5, 9], [0, 5, 8], [0, 4, 7]]}`
- Herleitung · Dreiklänge mit unverändertem F-Grundton und abgesenkter Terz. Open Music Theory, Blues-Based Schemas, Plagal Sigh.

## PROG-009-VOICE-LEADING

- Stand · Erneute Prüfung erforderlich
- Art · `fact`
- Fassung · `051dca398ee6da3c5074a8390de246fe88733a4df17469582a1b09a0fbcf71bc`
- Wortlaut · Eine mögliche Stimme verbindet A in F-Dur, As in F-Moll und G in C-Dur durch zwei absteigende Halbtonschritte.
- Gültigkeitsbereich · Lokale Stimmführung des Schemas IV–iv–I in C-Dur bei gleichstufiger Stimmung, etwa A4→As4→G4.
- Gegencheck · A und As sind die Terzen von F und Fm. G ist die Quinte von C. MIDI 69→68→67 ergibt zweimal −1 Halbton.
- Fundstelle · [Open Music Theory – Blues-Based Schemas](<https://viva.pressbooks.pub/openmusictheory/chapter/blues-based-schemas/>) · Plagal Sigh, Skalenstufenbewegung la–le–sol (6–♭6–5)
- Prüffrage · Welche Akkorde tragen die angegebene Stimme und um wie viele Halbtöne sinkt sie je Übergang?
- Sollantwort · `{"path": [[1, "A4"], [2, "As4"], [3, "G4"]], "midi": [69, 68, 67], "delta": [-1, -1]}`
- Herleitung · Terzen von F/Fm und Quinte von C. OMT Blues-Based Schemas, Plagal Sigh, 6–♭6–5.
