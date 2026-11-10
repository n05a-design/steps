# Band IV — COMPOSING: Vom Motiv zur Form, von der Skizze zur überprüfbaren Komposition

## 1. Composing ist eine eigene Domäne – nicht bloß Akkordauswahl

Komponieren bedeutet, musikalisches Material so zu wählen, zu gestalten, zu verbinden, zeitlich zu organisieren und auszuarbeiten, dass in einem gegebenen Kontext eine hörbare Form entsteht. Eine Akkordprogression kann diesen Prozess tragen, aber weder Melodie, Motividentität, Phrase, Textur, Register, Dramaturgie noch Instrumentierbarkeit ersetzen. Ein Steps-Kompositionssystem muss deshalb **vier Ebenen gleichzeitig** verwalten: (a) Idee/Material, (b) Transformation/Entwicklung, (c) Form/Zeit und (d) Realisation/Revision.

**Produktziel:** Ein „Compose“-Workflow darf einen Nutzer nicht durch ständige Akkordvorschläge unterbrechen. Er sollte z.B. eine Ausgangsmelodie fixieren, ihre motivische Beziehung zu einer Variation darstellen, Bassvarianten vorschlagen und die Formfunktion eines Übergangs erklären. Die kreative Entscheidung verbleibt beim Menschen.

## 2. Ein präziser kompositorischer Ausgangspunkt

Ein Projekt-Brief enthält Ziel, Dauer/Abschnitt, Besetzung, Spielniveau, Stilreferenz, tonales oder anderes Material, Text/Melodie, Spannungsverlauf, Einschränkungen und Erfolgskriterien. Beispiel: „32 Takte, langsame lyrische Miniatur für Piano und Cello, zwei kontrastierende Abschnitte, C-Dur mit Chromatik, Hauptmotiv von drei Noten, kein taktweiser Akkordzwang.“

Aus dem Brief werden **Constraints** (harte Grenzen: drei Stimmen, 32 Takte, bespielbare Register) und **Preferences** (lange Phrase, weit gespannter Höhepunkt, wenig Chromatik) getrennt. Das System kann mehrere Kompositionsvorschläge unter identischem Brief nachvollziehbar vergleichen, statt ein willkürliches Optimierungsschema durchzusetzen.

## 3. Motiv: kleinste wiedererkennbare Einheit

Originalmotiv M1: `C4(1/4) – D4(1/4) – E4(1/2)` in 4/4. Es besitzt den rhythmischen Vektor [1,1,2] in Viertelschlägen und das Intervallprofil [+2,+2] Halbtöne. Die melodische Kontur steigt; der dritte Ton erhält längere Dauer. Eine reine Transposition nach G ergibt `G4–A4–B4`, eine rhythmische Augmentation `[2,2,4]`, eine Inversion um C4 kann `C4–Bb3–Ab3` ergeben (chromatische Spiegelung in Halbtonabständen), eine Retrograde der Tonfolge `E4–D4–C4` verändert Richtung und Endgewichtung. Diese Operationen müssen **als unterschiedliche Transformationen** mit Bezug zum Original abgelegt werden.

Die Musikpsychologie bietet keine starre Grenze, wann eine Variation noch wiedererkannt wird. Kontur, Rhythmus, Tonhöhe, Repetition, Timbre und Zusammenhang interagieren. Ein Motiv-Ähnlichkeitsscore ist deshalb ein Hinweis, keine unanfechtbare fachliche Beurteilung.

## 4. Thema: Motiv, Kontrast und Fortsetzung

Ein vier- oder achttaktiges Thema verlangt mehr als eine einmalige Motivzelle. Eine mögliche achttaktige Satzskizze: Takte 1–2 M1 in C, Takte 3–4 M1 transponiert oder leicht verändert, Takte 5–6 Fragmentierung auf jeweils zwei Noten und beschleunigte Rhythmik, Takte 7–8 Kadenz mit längerer Zieltongestalt. Die Fortsetzung kann mit sequenzieller Bewegung, harmonischer Beschleunigung und registralem Anstieg arbeiten.

Alternative: **Periode** mit ähnlich beginnendem Vordersatz, dessen Schluss in vielen klassisch geprägten Fällen offen bleibt, und Nachsatz mit stärkerem Schluss. Die Wortwahl `sentence`, `period`, `antecedent`, `consequent` referenziert hier klassische Formmodelle nach Caplin [V5-002] und ist nicht automatisch das strukturelle Raster für Hip-Hop-/Ambient- oder Popproduktionen.

## 5. Melodiekonstruktion ohne bloßes Scale-Running

Eine Melodie besteht aus Gestalt über Zeit: Spannungsbogen, Zielnoten, Intervallsprünge, Wiederholungen, Atem-/Singbarkeit, Phrasengrenzen und Beziehung zur Harmonie. Für eine achttaktige Melodie in C-Dur könnte die Struktur lauten: T1–2 Aufbau zum E5, T3–4 Abstieg/Antwort auf D5, T5–6 neue höchste Note G5, T7–8 Entspannung zur Tonika C5. Ein Generator muss echte Notenereignisse und Stimmregister herstellen, statt nur `scale_notes` zu permutieren.

**Melody–Harmony Case:** Eine Melodie hält auf starkem Beat das E5. `Cmaj7` stützt E als große Terz, `Am7` als Quinte, `Fmaj7` als große Septime – alle sind harmonisch interpretierbar, aber mit unterschiedlicher Spannung. `Db7` macht E zur #9, in spezifischem Jazzkontext möglicherweise beabsichtigt; ohne Dokumentation darf dies nicht pauschal als „melodieunverträglich“ markiert werden. **Auflösung und Zeit** bestimmen oft mehr als die bloße Chord-Tone-Boolean.

## 6. Variationstechniken mit maschinenlesbarer Semantik

| Operation | Was wird bewahrt? | Was verändert sich? | Gültigkeitsbedingung |
|---|---|---|---|
| Transposition | Intervalle und Rhythmus | absoluter Tonraum | Key-/Registerkontext |
| Chromatische Inversion | Spiegelung der Halbtonabstände | Richtung und Tonklassen | Pivot und Oktaven ausdrücklich wählen |
| Diatonische Inversion | diatonische Stufenkontur | chromatische Abstände können variieren | diatonische Skala nötig |
| Retrograde | Reihenfolge umgekehrt | Ton-/Zeitsequenz | rhythmische oder pitch-only Variante benennen |
| Augmentation | proportionsgleicher Rhythmus | absolute Dauer | Metrum/Form neu prüfen |
| Diminution | proportionsgleicher Rhythmus | absolute Dauer | Performance/Notationsauflösung prüfen |
| Sequenz | Pattern an neuer Stufe | Zielton/tonales Gewicht | diatonisch oder real spezifizieren |
| Fragmentierung | Teilmotiv bleibt | Länge/Form | Fragment-ID mit Ursprung verknüpfen |
| Elision | überlappende Phrase | Formgrenze | keine zufällige Eventüberlappung |
| Ornamentation | strukturelle Stützpunkte | Oberfläche | Zusatznoten als Non-Chord-Tones annotieren |
| Harmonic substitution | Melodie/Form | harmonischer Unterbau | Gültigkeit und Stil prüfen |
| Rhythmic displacement | Kontur/Intervallprofil | metrische Lage | Beat-Hierarchie bewerten |

Das Datenmodell darf mehrere Transformationen als geordnete Operationen aufnehmen. Eine Inversion nach Transposition ist nicht generell gleich einer Transposition nach Inversion, wenn sich Pivot/Skalenkontext unterscheiden.

## 7. Kontrapunkt und Polyphonie

Kontrapunktische Handwerkslehren modellieren die Relation **selbständiger Stimmen**. Erster Gattungs-Kontrapunkt kann als besonders strenge Übung verwendet werden: kontrollierte Intervallklassen, Bewegungsarten, Beginn/Schluss und Kadenzgestaltung. Daraus folgt aber nicht, dass alle historischen oder gegenwärtigen Kompositionen auf Species-Regeln reduziert werden sollten. Imitation, Kanon, motivische Verwandtschaft und invertierbarer Kontrapunkt erlauben andere Kompositionsstrategien.

**Originales Zweistimmen-Experiment in C:** Oberstimme `E4–F4–G4–C5`; Bass `C3–D3–E3–F3` ergibt zunächst C/E, D/F, E/G, F/C-Relationen mit beweglichen Intervallabständen. Die korrekte Fassung einer strengen kontrapunktischen Übung muss **Stimme für Stimme und über jeden Takt** geprüft werden, nicht allein chordifiziert. Dieses Experiment ist keine behauptete Species-Lösung.

**Codex-Abnahme:** Parallelbewegung, tatsächliche Stimmkreuzung, Dissonanz auf betontem/unbetontem Teil und melodische Sprungauflösung brauchen voneinander getrennte Testergebnisse und Stilkriterien.

## 8. Harmonischer Plan und großformaler Tonartenweg

Vor Ausnotierung kann ein Kompositionsplan Tonartenräume, lokale Zentren, Spannungsbögen und Kadenzpunkte skizzieren. Beispiel A in C-Dur, B um a-Moll zentriert, A' als Rückkehr nach C mit erweitertem IV–iv–I-Schluss. Das ist ein sinnvoller **Vorschlag**, keine erforderliche klassische Form. Andere Musik arbeitet bewusst ohne stark gerichtete Harmonie: ambient-meditative Textur kann durch Register/Timbre und Prozess die Form prägen, während Harmonien über viele Takte ruhen.

Die Form darf nicht ex post aus Akkordnamen halluziniert werden. Nutzer oder Analyst muss Phrasen, Einsatzpunkte, Instrumentenwechsel, melodische Kadenzgeste und Aufführungskontext belegen.

## 9. Klassische Formmodelle als nützliche, aber lokale Werkzeuge

Sentence, Period, Binary, Ternary, Rondo, Sonata, Theme and Variations sind keine ineinander verschachtelten Pflichtstufen jeder Komposition. Ein Klassik-Miniatur-Satz arbeitet mit Satzfunktion und Kadenz; ein Sonatenhauptsatz besitzt überregionale thematisch-tonale Aufgaben; ein Rock-Chorus kann schon mit seinem Beginn ankommen; eine improvisierte freie Passage kann bewusst keine strikte Kadenz bilden. William Caplin [V5-002], Drew Nobile [V5-003], Gjerdingen [V5-004] und Sanguinettis Partimento-Forschung [V5-018] beschreiben historisch unterschiedliche Werkzeuge. Für V5 wurden nur die öffentlich verfügbaren Abstract-/Dokumentationsstellen geprüft, keine vollständige Buchdurcharbeitung.

## 10. Partimento und Bass als kompositorische Grammatik

Partimento ist historisch eine Übungsform der Improvisation und Komposition aus einer Bassvorlage, oft mit bezifferten Hinweisen. Das ist nicht identisch mit einem automatischen „neuen Akkord hinzufügen“. Eine Basslinie kann harmonische, rhythmische und stimmführungsbezogene Möglichkeiten *implizieren*, die in verschiedenen Stimmen auskomponiert werden. Beim Szenario `C3–B2–A2–G2` könnte Codex vier unterschiedliche Oberstimm-Lösungen erzeugen und deren Stimmführung gegenüber einem klar beschriebenen Genre vergleichen. Gjerdingen [V5-004] und Sanguinetti [V5-018] sind dafür Forschungsanker, nicht frei kopierbare Übungen.

## 11. Arrangement und Instrumentierung

Eine Akkordfolge als Pianoblock funktioniert nicht automatisch auf Gitarre, Streichquartett oder Holzbläsern. Register, Umfang, Atmung, Artikulation, Lagewechsel, offene Saiten, Doubling und Timbre sind eigenständige Kriterien. Eine Melodie für Solovioline kann einzelne Lagenwechsel und Bogenartikulation verlangen; eine Bläserlinie benötigt Phrasen/Atmung; ein Choral in vier Stimmen behandelt Stimmidentität anders als ein 1970er-R&B-Vocal-Cluster.

Ein **Arrangementplan** für `Cmaj7–Am7–Dm7–G7`: Bass spielt Grundtöne, Piano setzt Terzen/Septimen, Cello oder Pad hält gemeinsame Töne, Melodie bildet eine eigene Linie. Im weiteren Verlauf kann die Dichte steigen, ohne zusätzliche Akkorde zu benötigen. Produktfunktion „Density Lane“ wäre eine sinnvollere Kompositionshilfe als erzwungene Harmonisierung jedes Beats.

## 12. Pop-/Rock-Songwriting und Hook-Design

Songabschnitte haben konventionell bekannte Rollen (Verse, Prechorus, Chorus, Bridge), doch ein Chorus muss weder zwingend in neuer Tonart stehen noch am Ende kadenzieren. Ein „Hook“ kann rhythmisch, melodisch, textlich, harmonisch, klangfarblich oder produktionstechnisch sein. Nach Nobile [V5-003] kann ein Prechorus seine eigentliche harmonische Bewegung vor dem Chorus abschließen, während der Chorus die erreichte Tonika auskostet.

**Originales Song-Blueprint:** Verse `Am–F–G–Em`, melodiereiche tiefe Lage; Prechorus `Dm–F–G–G` steigender Bass und mehr harmonische Dichte; Chorus `C–G–Am–F` hoher melodischer Ankunftston C5/ G5 und dichteres Register. Die Progression ist ein Hilfsmittel – der eigentliche Unterschied entsteht in Melodie, Einsatz/Ankunft und Arrangement.

## 13. Jazz- und Blues-Komposition

Jazz-Komponieren kann aus Guide-Tone-Linien, Harmonic Rhythm, formalen Turnarounds und improvisationsfreundlichen Zielnoten entstehen. Ein erstes Konzept enthält `Dm7–G7–Cmaj7`, dann eine Contrafact-freie neue Melodie, die an geeigneten Stellen F→E bzw. B→C führt. Ein Blues-Stück braucht neben I7/IV7/V7 einen eigenständigen melodischen/bassbezogenen Gestus; ein statisches 12-Takt-Schema allein ist keine Komposition. Ein durchlaufender 4-Beat-Bass wäre eine *andere* Gestaltungsentscheidung als ein langsames Shuffle, selbst wenn beide die Akkordwurzeln teilen.

## 14. Film- und interaktive Musik

Bei Filmmusik oder interaktiven Games kann die Form durch **Ereignisse außerhalb der Musik** bestimmt sein. Ein 16-taktiger Cue kann einen ansteigenden Dichtebogen ohne Kadenz bilden; ein Gameplay-Loop muss Übergangsfähigkeit, Metrum und synchronisierte Layer beachten. „Episch“ oder „cinematic“ ist kein objektiver Akkordtyp. Konkrete Modelle sollten `transition_boundary`, `exit_point`, `stem_layer`, `harmonic_compatibility` und `narrative_event` separat ausdrücken. Vor produktiver Implementation braucht es eigene fachliche Quellen zur adaptiven Score-Praxis; die V5 trägt hierzu **Produkt- und Forschungsdesign**, keinen fachgutachterlich belegten Universalstandard bei.

## 15. Minimalistische, posttonale und algorithmische Kompositionsweisen

Minimalistische Komposition kann durch graduellen Prozess, additive rhythmische Figuren, Phasenverschiebung und registrale Veränderungen strukturiert werden. Reihen-/Set-Ansätze strukturieren Tonklassen und Transformationen ohne klassische Tonika. Algorithmische Komposition kann Constraints, grammatische Regeln, Stochastik oder interaktive Steuerung nutzen. Das gemeinsame Softwarefundament ist deshalb eine *Kompositions-Constraint-Library*, nicht ein universeller tonaler Generator.

**Beispiel:** Originalphrasenzelle `[C4,E4,G4]` wird über acht Durchgänge erst rhythmisch verschoben, dann im Register gespiegelt; die Tonvorräte bleiben zunächst gleich. Das ist eine strukturierte Prozessidee, kein Beweis für harmonische Spannung.

## 16. Gehör, Hörvergleich und Revision

Ein guter Kompositionsassistent muss die Möglichkeit bieten, zwei Fassungen **unter identischem Tempo, Timbre und Ausgangslautstärke** vergleichen zu können. Sonst wird die Klangfarbe mit der Harmonik verwechselt. Validierung fragt nach motivischer Kohärenz, Atem-/Spielbarkeit, klarem Spannungs-/Entspannungsverlauf, stilistischem Kontext, formaler Zielsetzung und Qualität der Variation. Kein einzelner mathematischer Score ersetzt fachliches Hören und kompositorische Entscheidung.

## 17. Die zwölfstufige STEPS-Kompositionspipeline (Vorschlag)

1. **Brief:** Besetzung, Länge, Ziel, Form, Stil, Einschränkungen.
2. **Seed:** Motiv, rhythmische Zelle, Bassidee, Harmoniefarbe oder Textidee.
3. **Material:** Tonvorrat, Metrum, Register, erste Intervall-/Rhythmusstruktur.
4. **Motivnetz:** Original, Fragment, Variation, Wiederholung, kontrastierende Idee.
5. **Formplan:** Abschnitte, Funktionen, Energie- und Phrasenarchitektur.
6. **Harmonieplan:** lokale Zentren, Akkordmöglichkeiten, analytische Lenses.
7. **Bassplan:** Grundtöne, Inversionen, Pedale, Linienziel.
8. **Melodieentwicklung:** Kontur, Zielton, Phrase, Pausen, Wiedererkennung.
9. **Voice Leading:** Ober-/Mittelstimmen, Guide Tones, Dissonanz/Resolution.
10. **Instrumentation:** Spielbarkeit, Register, Dichte, Timbre, Layer.
11. **Playback/Notation:** korrekt exportierte Time/Note/Harmony-Events, MusicXML/MIDI nach Bedarf.
12. **Review/Iteration:** A/B-Vergleich, individuelle Fachkriterien, Begründung der Entscheidungen, Versionsfortschritt.

Die Pipeline ist nicht starr. Bei jazzorientiertem Songwriting kann eine Topline früh fixiert sein; bei Filmmusik kann der Timing-Plan vor Harmonik stehen; bei partimentoartigem Komponieren steht der Bass zuerst. Die einzelnen Schritte sind **Module**, keine universelle Reihenfolge.

## 18. Vollständiges eigenständiges Kompositionsbeispiel – Piano-Miniatur 16 Takte

**Brief:** C-Dur, 4/4, 88 BPM, Klavier, lyrische Einfachheit. Ein kurzes Motiv M wird zweimal präsentiert und dann sequenziert. Dynamik vom leisen A-Teil zum mittleren B und zurück.

**Motiv M:** C5 Viertel, D5 Viertel, E5 Halbe; Takt 2 G5 Viertel, E5 Viertel, D5 Halbe. Harmonischer Unterbau Cmaj7 → Am7. A-Teil T1–4: `Cmaj7 | Am7 | Fmaj7 | G7`; T5–8 variierte Rückkehr `C/E | Am7 | Dm7 G7 | Cmaj7`. Melodie T3–4: `F5–E5–D5–C5` je Viertel, dann `B4(2)–D5(1)–C5(1)`. Die Eignung der tatsächlich notierten Melodietöne zu jedem harmonischen Ereignis ist zu prüfen; insbesondere müssen nichtakkordeigene Töne, metrische Akzente, ihre Vorbereitung und Auflösung im konkreten Stimmverlauf beurteilt werden. Es wird keine automatisierte Qualitätsbehauptung getroffen.

**B-Teil T9–12:** `Am | E7 | Am | Fm6` mit dunklerer Tonikaebene, G# als Dominant-Leitton zu A und Ab als chromatische Farbe. Motivfragment T9: `E5(1)–D5(1)–C5(2)`; T10: `B4(1)–G#4(1)–E5(2)`; T11: `A4(4)`; T12: `Ab4(1)–G4(1)–F4(2)`.

**Rückkehr T13–16:** `C/E | Dm7 | G7 | Cmaj7`. Motiv M als kürzere Diminution oder rhythmische Variation; Schluss C5 als ganzer Ton. Bass E–D–G–C, Endtonika stark im Grundton. Optionales Gegenstück: Schluss `Fm6→C` statt `G7→C`, um die formale Wirkung zu vergleichen.

**Prüfprogramm:** (a) 16 Takte exakt? (b) jede Melodiedauer je Takt 4? (c) Bass-/Oberstimmenregister konsistent? (d) motivische Rückbezüge annotiert? (e) jedes Akkordsymbol hat notierte Töne? (f) Mischung/Dominante an geeigneter Stelle, aber nicht irreführend als Musikgesetz? (g) Hörreview. Die in V5 separat erzeugten maschinenlesbaren Etüden sind zusätzliche Beispiele und werden eigenständig validiert.

## 19. Ein kontrastierendes Pop-/Rock-Kompositionsbeispiel

**Brief:** 32 Takte, 4/4, ~110 BPM, Vers–Prechorus–Chorus–Tag, einen großen Anfang des Chorus inszenieren. Verse 8 Takte wiederholt `Am–F–G–Em`, niedrige melodische Lage (A3–E4). Prechorus 8 Takte `Dm–F–G–G`, Steigerung der harmonischen und rhythmischen Aktivität, melodische höchste Note B4 am Ende als vorgehaltener Zielton. Chorus 12 Takte `C–G–Am–F` dreimal, das C am Chorus-Anfang als große Ankunft. Tag 4 Takte `F–Fm–C–C`, zurückgenommene Besetzung und Halbton A→Ab→G. Aus diesen Akkorden **allein** entsteht noch kein Song; es müssen Hook, Bassgroove, Melodiegestalt, Textakzente und Arrangement realisiert werden. Die Ziel-Ankunftskonzeption ist mit Nobile [V5-003] und Spicer [V5-005] als Forschungsrahmen verknüpft; die Skizze ist originär.

## 20. Drei Kategorien musikalischer Qualitätssicherung

| Prüftyp | Automatisierbar? | Beispiel | Verantwortlichkeit |
|---|---|---|---|
| Formal/technisch | Ja | Taktlängen, Tonhöhenbereiche, Event-IDs, MusicXML-Syntax | CI/Validator |
| Theoretisch mit Scope | Teilweise | Regel der klassischen Kadenz, Mischung, sekundäre Dominante | Fachreview + Test-Lens |
| Kompositorisch/ästhetisch | Nicht abschließend algorithmisch | dramaturgische Wirkung, Hook-Qualität, stilistische Authentizität | hörende Musiker, Testpersonen, Nutzer |

**Forschungsanker:** [V5-002] Caplin, [V5-003] Nobile, [V5-004] Gjerdingen, [V5-005] Spicer, [V5-018] Sanguinetti, [V5-014] Huron und [V5-001] OMT. Für das genaue jeweilige Belegniveau das Quellenregister einsehen.
