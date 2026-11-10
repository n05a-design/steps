> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Harmonieanalyse nach Stil und musikalischem Kontext

## 1. Warum „ein richtiges Roman-Numeral-Ergebnis“ nicht genügt
Tonart, lokales Zentrum, Taktposition, Stil, melodischer Kontext, Umkehrung und Form beeinflussen die Analyse. In C-Dur lässt sich `C–F–G–C` relativ unkompliziert als `I–IV–V–I` lesen. Dagegen muss `C–B♭–F–C` in einer Pop-/Rock-Schleife nicht als bloße Abweichung von einem klassischen Dominantmodell behandelt werden: `I–♭VII–IV–I` kann modal-mixolydisch, riffgebunden oder durch Bewegung der Oberstimmen beschrieben werden. **Keine** einzelne Lesart ist allein durch die Akkordsymbole bestätigt.

## 2. Fünf Analyse-Linsen
| Linse | Gegenstand | Prüffrage | Typische Grenze |
|---|---|---|---|
| Roman/Scale degree | Akkordgrundtöne relativ zum Zentrum | Welche Stufen liegen vor? | Zentrum nicht immer eindeutig |
| Function | tonikale, prädominante und dominante Tendenzen | Welche Auflösung wird kontextuell vorbereitet? | Blues/Pop-Vamps nicht immer sinnvoll funktional |
| Modal/collection | Beziehung zu Modi und Tonvorräten | Welche Töne prägen den Klangraum? | gleiche Töne beweisen nicht modale Praxis |
| Voice leading | Stimmenbewegung, gemeinsame Töne, Halbtöne | Wie wird Spannung realisiert? | kleiner Weg ist kein Qualitätsurteil |
| Corpus/style | beobachtete Häufigkeiten in definierten Samples | Wie typisch ist das Muster im Korpus? | unrepräsentative Korpora |

## 3. Worked analyses – eigene abstrakte Beispielsätze
**Funktionen und Sekundärdominante:** `Cmaj7 – A7 – Dm7 – G7 – Cmaj7`, Zentrum C. Eine plausible funktionale Lesart ist `Imaj7 – V7/ii – ii7 – V7 – Imaj7`. A7 enthält C♯ als Zielspannung zu D; eine bloße Quintfall-Beschreibung allein erfasst diese Tonika-Beziehung nicht. In Pop-/Jazzpraxis darf A7 dennoch ausbleibend oder anders weitergeführt werden; Zielauflösung ist Tendenz.

**Mixolydische Farbgebung:** `G – F – C – G`: als `I–♭VII–IV–I` über G zentriert, sofern Melodie/Phrase G stützt. Eine C-durbezogene `V–IV–I–V`-Lesart bleibt theoretisch möglich; ohne Kontext darf Steps keinen sicheren globalen Tonikaentscheid ausgeben.

**Blues-Syntax:** `C7 – F7 – C7 – G7 – F7 – C7`. Die Dominantseptimen auf I und IV sind im 12-Bar-/Blues-Kontext nicht automatisch sekundäre Dominanten, die im klassischen Sinn „eigentlich“ aufgelöst werden müssen. Rhythmus, Bluestonvokabular und Form sind notwendige Erklärungsdimensionen.

**Minor harmony:** `Am – Dm – E7 – Am`. Als `i–iv–V7–i` in A-Moll enthält der E7 das Leitton-G♯; dies zeigt, warum „A-Moll = nur natürliche Molltonleiter“ fachlich zu eng ist.

**Jazz substitute:** `Dm7 – D♭7 – Cmaj7`. D♭7 kann als Tritonussubstitution von G7 erklärt werden (Tritonustöne B und F erscheinen in D♭7 enharmonisch als C♭ und F). Diese Interpretation benötigt Kontext; sie ist keine universelle Kennzeichnung jedes ♭II7.

## 4. Agent- und Datenvertrag
Ein Analyseergebnis enthält `{chords[], hypothesized_centers[], lens, roman_labels[], chord_functions[], supporting_evidence[], competing_analyses[], unsupported_claims[], confidence_qualitative}`. Die Tonikawahl ist eine begründete Hypothese; absolute numerische `confidence` ist ohne kalibrierte Referenzdaten zu vermeiden. Bei modaler, bluesbezogener oder klangflächenbasierter Praxis kann eine neutrale Beschreibung genauer sein als erzwungene Funktion.

## 5. Negativfälle
- Eine gleichbleibende E7-Klangfarbe in einem modalen E-Vamp beweist nicht automatisch A als globales Zentrum.
- Ein E♭-Dur-Dreiklang in C-Dur kann ♭III/mediant relation sein; Satz- und Melodiekontext entscheiden.
- Der gleiche Grundton in Slash-Chords ist keine Aussage über den tatsächlichen Bass.
- Ein Korpuswert ohne Corpus-ID, Samplesize, Genre und Methodik darf nicht „typisch für Rock“ heißen.

### Nachweise
music21 RomanNumeral API: https://music21.org/music21docs/moduleReference/moduleRoman.html . Open Music Theory: https://openmusictheory.github.io/contents . Vorhandene V5-Fachkapitel zu Harmonie und Progressionen: historische Synthesen. Alle musikalischen Mini-Beispiele hier sind eigene schematische Beispielsätze, keine Aussagen über konkrete Songs.
