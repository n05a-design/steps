# STEPS – Wissenschaftliches Forschungsfundament V3

**Stand:** 08.11.2026 · **Dokumentklasse:** ausführliche Research-Synthese und umsetzbare Fachagenda · **Status:** `research_synthesis_with_draft_knowledge_records`, nicht peer-reviewed und nicht endgültige fachliche Abnahme.

## 0. Dokumentcharakter und Abgrenzung

Dieses Dokument erweitert das bestehende STEPS-Material wesentlich. Es setzt keine unbekannte Git-Repository-Struktur als existent voraus und behauptet nicht, die in Verlagskatalogen genannten Bücher vollständig gelesen zu haben. **Der vorliegende Evidenzstand umfasst echte öffentlich nachprüfbare Verlags-, Journal-, Standard- und Open-Textbook-Seiten, dazu bislang nicht fachgutachterlich geprüfte eigene Demonstrationsbeispiele.** Jeder Quellenregistereintrag muss daher einzeln nach `metadata_status`, `reading_status`, `license_note` und späteren exakten Fundstellen differenziert werden. Ein verifizierter Buchtitel begründet noch kein exakt nachgewiesenes Kapitelzitat.

**Vier tragende und gleichberechtigte Säulen** sind `MUSIC THEORY`, `HARMONY`, `CHORD PROGRESSIONS` und `COMPOSING`. Sie sind nicht einfach vier alternative Menüeinträge, sondern besitzen je eigene Erkenntnisobjekte, Validierungen, Zeit-/Stilparameter, Benutzeraufgaben und Kompositionsbeispiele. Querschnittsebenen sind Kognition, Geschichte, interkulturelle Grenzen, Information Retrieval, Wissensmanagement, Rechtsfragen und Produktentwicklung. **Composing ist ein eigenes Erkenntnisgebiet:** Es umfasst Materialerfindung, Gestaltbildung, entwickelnde Variation, Melodie, Form, Kontrapunkt, Instrumentation, Arrangement und Revision, nicht nur die Auswahl von vier Akkorden.

Die V1-Unterlagen und der vorhandene Handover werden unverändert archiviert. Dies ist ein **Addendum mit einem neuen Master-Prompt**, keine rückwirkende Umschreibung früherer Nutzerentscheidungen. Ebenso sind die früheren „Initial Sources v1.0“ eine im Research benannte 20-Dateien-Liste, nicht automatisch im öffentlichen Steps-Repo befindliche PDFs. Drum-/Groove-Engine, große Audio-Datensätze und vollständige App-Neuentwicklung bleiben außerhalb des jetzigen Umfangs; musikalischer Rhythmus, Takt, Phrasierung und Form bleiben dagegen zentrale kompositorische Grundelemente.

## 1. Wissenschaftlicher und musikpraktischer Erkenntnisansatz

**Beschreibung ≠ Vorschrift.** Musiktheoretische Modelle können den gleichen Vorgang unterschiedlich darstellen: Ein `G7–C` kann unter klassischer Funktionstheorie Dominante–Tonika sein, unter Jazz-Sicht eine Guide-Tone-Lösung, unter Voice-Leading eine konkrete Stimmenbewegung, unter Corpus-Sicht eine beobachtete Übergangsbeziehung und im Arrangement ein dynamischer Spannungs-/Registrierungswechsel. Diese Aussagen sind nicht äquivalent. STEPS muss sie unter getrennten `analytical_lens`-Identitäten speichern; der Benutzer soll bewusst wechseln können.

**Analyse ≠ Komposition.** Eine verlässlich notierte Akkordfolge und ihre Stufenanalyse können noch nicht erklären, weshalb ein Musikstück einen kohärenten Spannungsbogen hat. Komposition entsteht durch Kombination von Form, Rhythmus, Motivik, Instrumentation, Text/Prosodie und ausgebildeter zeitlicher Erwartung. Caplins *Classical Form* ist eine belegte Formlehre für spezifische klassische Repertoires, nicht automatisch eine universelle Pop-Formgrammatik [SRC-V3-0005]. Nobile verbindet dagegen Rock-/Pop-Form mit harmonischen Trajektorien und thematischen Funktionsbereichen [SRC-V3-0009]. Das impliziert unterschiedliche, nebeneinander gültige Modelle.

**Primärquelle ≠ Werkzugang.** Bei Caplin, Gjerdingen, Tymoczko, Lerdahl, Cohn, Rings, Huron, Meyer und Belkin wurden verifizierbare Verlagsinformationen ermittelt. Deren Buchinhalte wurden hier nicht vollständig geprüft. Vertiefte Aussagen sind deshalb als `research_direction`, `editorial_draft` oder `metadata_based_summary` zu erkennen. Offene Lehrwerke wie *Open Music Theory* und *Music Composition & Theory* liefern besonders nützliche Zugangsstellen, aber ihre konkreten Abschnitte und Bild-/Beispiellizenzen müssen für jede wiederverwendete Illustration separat geklärt werden [SRC-V3-0001; SRC-V3-0003].

**Beobachtung ≠ Universalregel.** Eine Rock-Korpusstatistik sagt nur unter bestimmten Repertoire-, Sampling-, Annotations- und Zählbedingungen etwas über Häufigkeiten aus. De Clercq/Temperley untersuchen Rock-Harmonik empirisch [SRC-V3-0017]. Richards analysiert die tonal mehrdeutige Achsenfolge `Am–F–C–G` unter variablen melodischen Zentren [SRC-V3-0019]. Duinker dokumentiert zusätzliche Hybrid-Tonika-Kontexte [SRC-V3-0020]. Daraus darf STEPS weder die eine „korrekte“ Tonika noch eine universelle Kompositionsformel ableiten.

## 2. Säule MUSIC THEORY: Schichten der musikalischen Repräsentation

### 2.1 Akustische, psychoakustische und symbolische Schicht

Eine Tonhöhe kann als physikalische Frequenz, Wahrnehmungskategorie, notierter Buchstabe, MIDI-Wert, Pitch Class und funktionale Stufe modelliert werden. Diese Schichten sind nicht verlustfrei austauschbar. Beispielsweise bezeichnet MIDI-Note 60 einen chromatisch quantisierten Ton in einem üblichen Mapping, während `C4` die Schreibweise und Oktavzuordnung trägt. In 12-TET können `Fis4` und `Ges4` gleiche Frequenzpositionen repräsentieren, doch eine harmonische Analyse benötigt die Schreibweise als eigene Information. STEPS sollte `spelling`, `pc`, `octave`, `tuning_system`, `reference_frequency`, `key_context` und `notation_locale` getrennt speichern.

Intervallbestimmung erfordert zugleich diatonische Zählung und chromatische Größe. `C–E` ist eine große Terz, `C–Es` eine kleine; `C–Dis` und `C–Es` können in 12-TET denselben Abstand besitzen, aber unterschiedliche Intervallnamen. Der häufige Datenmodellfehler wäre, eine Intervallqualität allein aus `mod12` zu erzeugen, wodurch z.B. die enharmonische Funktion verschwände. Ein späterer Parser muss relative Intervalle, enharmonische Äquivalenz und korrekt notierte Zieltonleitern getrennt testen.

Die Temperierung ist ein weiteres Scoping-Problem. Eine 12-TET-Stimmung setzt Halbtonschritte im Verhältnis `2^(1/12)`; eine reine große Terz zielt auf `5:4`. In mikrotonalen oder traditionell spezifischen Kontexten sind `pitch_class=0..11` und eine universelle `semitone_distance` nicht ausreichend. Deshalb sollte die V3-Ontologie eine klar abgegrenzte 12-TET-Implementierung neben abstrakten `TuningSystem`, `IntervalRatio` und `ScaleStep` vorsehen. Für raga/maqam/gamelan darf eine westliche Zwölftonskala nicht stillschweigend die Primärrepräsentation werden.

### 2.2 Musiknotation und professionelle Bezeichnungen

STEPS benötigt simultan römische Stufen, deutsche H/B-Notation, internationales B/Bb, internationale Chordsymbolsprache, Stimmnotation, Generalbass und optional Nashville Number System. In der V3-Beispielbibliothek werden **internationale Chordsymbole** verwendet: `B` = deutsches `H`, `Bb` = deutsches `B`. Eine globale Oberfläche darf lokale Anzeigen umschalten, ohne die zugrunde liegenden Klangobjekte zu verwechseln. Die Konverter müssen durch präzise Tests abgesichert werden.

Chordsymbole sind kein eindeutiges Raster: `Cadd9`, `C9`, `Cmaj9`, `Csus4`, `C/E`, `V/V`, `Ger+6` und Harte-Syntax repräsentieren verschiedene Ausdrucksformen. Ein Slash in `C/E` bezeichnet einen Bass, in `V/V` eine angewandte Dominante; ein einfacher regulärer Ausdruck, der beide Fälle gleich behandelt, ist fachlich falsch. Harte et al. liefern eine maschinenlesbare Chordsymbol-Syntax [SRC-V3-0027], während music21 eigene Key-aware Roman-Numeral-Objekte implementiert [SRC-V3-0034]. STEPS soll ein internes typisiertes Modell mit mehreren Frontends/Serialisierern verwenden, statt sämtliche Formate per Stringersetzung zu vermischen.

### 2.3 Tonleitern, Modi und tonale Identität

Die sieben üblichen Modi einer diatonischen Kollektion sind eine nützliche Lehreinheit, aber kein vollständiger Modusbegriff. Ein D-Dorisch-Demonstrationsvamp `Dm7–G` enthält die große Sexte `B` (deutsch `H`), doch das allein beweist noch nicht, dass ein Stück D als Tonika hört: Bass, Phrase, Dauer, Melodie und Abschnittshierarchie müssen mithelfen. Umgekehrt kann dieselbe weiße-Tasten-Sammlung als C-Ionisch oder A-Äolisch gehört werden. Das muss das Analyseobjekt durch `tonal_center_candidates` und `supporting_evidence` sichtbar machen.

Harmonisch, melodisch und natürlich Moll unterscheiden sich in traditioneller Lehrdarstellung, während reale Mollmusik Stufen flexibel nutzt. Ein A-Moll-Satz kann `Am–Dm–E7–Am` mit `G#` in der Dominante enthalten, ohne dass jede Melodie ausschließlich die harmonische Mollskala nutzt. STEPS sollte die Operation `raise_leading_tone` als kontextabhängige Transformation statt als 'Moll gleich eine starre Leiter' verstehen. Jazz-Melodic-Minor-Familien und harmonisch-Dur-Varianten sind eigene Traditionsfelder; sie benötigen eigene Korpus-/Stilbelege und didaktisch explizite Mode-/Parent-Scale-Algorithmen.

### 2.4 Rhythmus, Metrum und zeitliche Hierarchie

Musiktheorie ist nicht nur Harmonik. Ein Akkordwechsel auf einer starken Zählzeit, auf der vorgezogenen `und` vor Beat 1 oder mitten in einer langen Vokalnote kann unterschiedliche formale Funktionen bekommen. Rhythmusobjekte müssen Beginn, Dauer, Taktart, Tempo, Hierarchiestufe und ggf. Microtiming getrennt modellieren. `harmonic_rhythm` beschreibt die Frequenz/Verteilung der Harmonieereignisse, nicht den Drum-Groove. Diese Unterscheidung erlaubt, die spätere Drum-Engine zu verschieben und dennoch korrekte kompositorische Form zu modellieren.

Hypermetrik gruppiert Takte, Phrasen überlagern Taktgrenzen, Synkopen verlagern Akzentwahrnehmung und polymetrische/polyrythmische Verfahren benötigen mehrere simultane Zeitraster. Diese Parameter sollten keine Dekoration sein: Sie beeinflussen Cadence Detection, Hook-Position, Songform und melodische Zielnoten. Lerdahl/Jackendoff modellieren Gruppierung und metrische Struktur auf hierarchischer Ebene [SRC-V3-0011], Temperley entwickelt computational preference-rule-Modelle für Metrum, Phrase und Pitch-Spelling [SRC-V3-0023]. Beide Programme sind kontextgebundene Theorieansätze, keine universellen Gesetze.

## 3. Säule HARMONY: mehrere Schulen, klare Geltungsgrenzen

### 3.1 Gemeinpraktische tonale Harmonik

Im häufigen Dur-Lehrmodell ergeben Stufenakkorde in C: `I=C`, `ii=Dm`, `iii=Em`, `IV=F`, `V=G`, `vi=Am`, `vii°=Bdim`. Das ist zunächst eine **Akkordklassifikation**. Funktionshierarchien beschreiben dagegen die Rolle von Akkorden in einem tonalen Ablauf: Tonika als Zentrum, Prädominante als Vorbereitung, Dominante als gerichtete Spannung, diverse Kadenzen als formale Schlusspunkte. Die Riemannsche Funktionslehre mit `T/S/D` ist nochmals ein eigenes Benennungssystem. Diese Ebenen sollen als getrennte Labels gespeichert werden.

Angewandte Dominanten wie `A7→Dm` in C (V7/ii) unterstreichen ein lokales Ziel, etablieren aber nicht ohne weiteres eine neue Tonart. Eine Modulation erfordert weitere Bestätigung, z.B. neue Kadenzen und ein plausibel anhaltendes Zentrum. Der chromatische Akkord `Db/F` vor `G7` kann in passendem klassischem Kontext als Neapolitaner `bII6` beschrieben werden; der gleiche bII-Klang könnte in Jazz als Substitute-Dominant oder in Film als chromatische Klangfläche erscheinen. Ein Kandidat darf nur innerhalb dokumentierten Kontextes als `neapolitan`, `tritone_substitution` oder `chromatic_planing` etikettiert werden.

Cadence-Recognition braucht mehr als eine Liste `G7,C`: wichtig sind Bass, Sopran, zeitliche Betonung und Phrasenposition. Caplins formal-function-basierter Zugang [SRC-V3-0005] und seine spätere spezifische Studie zum Kadenzbegriff [SRC-V3-0006] begründen die Notwendigkeit, Harmonieereignisse in eine Formhierarchie einzubetten. Ein 'cadence detected' sollte in STEPS von der bloßen Beobachtung `dominant_to_tonic` unterschieden werden.

### 3.2 Jazz- und Blues-Harmonik

Jazz-ii–V–I `Dm7–G7–Cmaj7` ist eine zentrale Grammatikfigur; ihre harmonische Aussage wird aber erst durch Voicing, Stimmführung, Alterationen, Tempo, melodischen Kontext und Phrasierung konkret. Ein im Jazz gebräuchlicher Ersatz `Dm7–Db7–Cmaj7` setzt `Db7` tritonusverwandt an die Stelle von `G7`, wobei `Db7` die beiden Guide-Tone-Pitch-Classes des G7 enharmonisch trägt. Das Beispiel ist deshalb nicht 'funktional identisch' in jeder metrischen oder stilistischen Hinsicht. Ebenso sind Backdoor-Dominants `Bb7→Cmaj7`, iiø–V–i, Tonicization-Ketten, Turnarounds, diminished passing chords, Upper Structures und reharmonische Varianten getrennte Mechanismen.

Der Blues erfordert eine eigene Schicht: `C7` in einem C-Blues ist gewöhnlich ein tonikaler I7-Klang, nicht automatisch V7/IV in einem C-Dur-Satz. Damit würde eine rein klassische Funktionsmaschine systematisch falsche Erklärungen erzeugen. Auch Blue Notes sind keine einfache starre Zusatzskala; Performance, Artikulation und Mikrointonation prägen die Wirkung. Andere Bluesformen, Moll-Blues und verwandte Jazzharmonien sind als Varianten mit Repertoire-Scope zu modellieren.

### 3.3 Pop, Rock, R&B, Gospel, Soul, Neo-Soul und elektronisch geprägte Praxis

Pop- und Rock-Harmonik arbeitet häufig mit Loops, modalen Klängen, metrischen Schemata und Tonikamehrdeutigkeit. `Am–F–C–G` ist unter C-Dur als `vi–IV–I–V`, unter A-Äolisch als `i–bVI–bIII–bVII` beschreibbar; die plausiblere Lesart hängt wesentlich von Melodie und Metrik ab [SRC-V3-0019]. Die literarisch untersuchten 'plateau loops' `IV–V–vi` zeigen, dass in bestimmten Popkontexten IV/vi rhetorisch tonikaähnliche Funktionen gewinnen können [SRC-V3-0020]. Ein einziges 'richtiger Akkord' im UI wäre daher methodisch irreführend.

Weitere Stilfelder sollen als **repertoire-spezifische Module** statt per Genreschablone organisiert werden. Gospel-Passing-Diminished, Neo-Soul-Extensions, R&B-Bassharmonik, Soul-backdoor Bewegungen, Rock-power chords, EDM-pedals und filmische Chromatik können durch verwertbare Beispiele illustriert werden; ein einzelner Akkord beweist aber weder Genrezugehörigkeit noch eine homogene kulturelle Grammatik. Eine Aufnahme in den produktiven Canon erfordert Fachquellen, Fallbeispiele und gegebenenfalls musikwissenschaftliche Reviews. Besonders bei Hip-Hop, Gospel, Afro-diasporischer Musik und nicht-westlichen Systemen gilt: musikalischer Kontext und Tradition sind mehr als eine Sammlung Akkordsymbole.

### 3.4 Chromatische, transformationale und posttonale Modelle

Die klassische Frage 'zu welcher Tonart gehört dieser Akkord?' ist nicht immer am fruchtbarsten. Bei `C–Ab–E–C` kann ein analystischer Blick auf chromatische Medianten, gemeinsame Töne und Stimmführungswege nützlicher sein. Cohns *Audacious Euphony* [SRC-V3-0014], Rings' *Tonality and Transformation* [SRC-V3-0015] und Tymoczkos geometrische Modelle [SRC-V3-0013] liefern verwandte, aber nicht identische Theorieperspektiven. Die P/L/R-Operationen sind für Dur-/Moll-Dreiklänge wohldefiniert; eine Übertragung auf Vierklänge muss eigene mathematische Regeln festlegen.

Pitch-Class-Set-Theory, Intervallklassen, Inversionstransformationen und Zwölftontechnik erweitern den Bereich jenseits funktionaler Tonalität. Ein Pitch-Class-Set wie `{0,4,7}` verwirft Register und Schreibweise; für eine komponierende Anwendung braucht es daher eine Brücke zu **voiced pitch events**. Zwölftonreihen und Permutationsverfahren dürfen als kompositorische Systeme modelliert werden, aber 'atonal' ist nicht mit 'twelve-tone serial' gleichzusetzen. Eine algorithmische Kompositionsmaschine muss wissen, welche Parameter ihr Verfahren erhält und welche es bewusst aufgibt.

## 4. Säule CHORD PROGRESSIONS: Harmonie als zeitliche Handlung

Ein Akkord-String wie `C–G–Am–F` ist lediglich eine erste Repräsentation. Für eine echte Progression braucht STEPS mindestens `chord_event_id`, `onset`, `duration`, `bass`, `voicing` (falls vorhanden), `local_tonic`, `global_context`, `analysis_candidates[]`, `style_tags`, `source_ids`, `melody_constraints`, `phrase_position`, `harmonic_rhythm`, `tension_claim_status`. Ohne Dauer ist ein Achsen-Loop nicht von einer kurzen Durchgangsfolge zu unterscheiden; ohne Melodie lässt sich die relative Tonikafunktion oft nicht entscheiden.

### 4.1 Progressionsfamilien statt statischer Listen

Die V3-Progression-Atlas-Datei enthält **95 original formulierte Seed-Einträge** über klassische Tonalität, Moll, Modalität, Jazz, Blues, Pop/Rock, R&B/Neo-Soul, Gospel, Film, elektronische Texturen und transformationale Modelle. Mehrere Einträge sind bewusst Transpositions-/Variantenfälle. Daher sind **95 Datensätze nicht gleich 95 unabhängige Theorieerkenntnisse**. Jeder Eintrag hat Tonzentrum, Stufenlesart, Akkordsymbole, Begründung und Begrenzung. Sie sind fachlich **Drafts**, die Codex mit symbolischer Rechenprüfung, Quellenlage, Stil-/Korpusbezug und Review ergänzen muss.

Der Basiskanon soll folgende Familien unterscheiden: `diatonic_linear`, `tonic_expansion`, `functional_cadential`, `applied_dominant`, `circle_progression`, `minor_key_functional`, `modal_vamp`, `modal_mixture`, `tritone_substitution`, `backdoor`, `chromatic_mediant`, `plagal_rock`, `axis_loop`, `plateau_loop`, `blues_12_bar`, `minor_blues`, `jazz_turnaround`, `harmonic_rhythm`, `pedal_bass`, `voiceleading_neighbor`, `sequence`, `reharmonization`, `transformational_triads`, `textural_ambient`. Diese Familien sind nicht gegenseitig exklusiv; ein Ereignis kann in mehrere Beziehungen passen.

### 4.2 Reharmonisierung als kontrollierte Transformation

Reharmonisierung sollte den jeweiligen **Invarianzvertrag** explizit machen: Wird die Melodie festgehalten? Bleiben Bass oder Rhythmus unverändert? Sind Tonikaregion und Phrasenschluss zu erhalten? Welches Chromatik-Niveau ist erlaubt? `Cmaj7→Am9` kann für eine Melodie E auf beiden Akkorden plausibel sein, weil E in Cmaj7 die Terz und in Am9 die Quinte ist. `Fmaj7` mit E bietet einen Maj7-Melodieton, der eine andere Klangspannung erzeugen kann. Aus einem bloßen 'Melody pitch ∈ chord tones' folgt jedoch kein allgemeines Qualitätsurteil.

Eine **Reharmonization Ladder** kann in Stufen arbeiten: (1) Umkehrungen und reine Registeränderung, (2) 7ths/9ths, (3) angewandte Dominanten, (4) modale Entlehnung, (5) tritone/backdoor/diminished substitutions, (6) chromatic/transformational, (7) experimentelle freiere Neubewertung. Jede Stufe muss Herkunft, Anwendungsbedingungen, Nebenwirkungen und mindestens einen Gegenfall dokumentieren. Der Nutzer soll die Änderung hören und sehen, nicht nur einen Neuen-Akkord-Knopf bekommen.

### 4.3 Ranking ist kein musikalisches Wahrheitsmaß

Ein Kandidat kann parallel nach funktionaler Plausibilität, Stimmführungsaufwand, Melodieverträglichkeit, stilistischer Repertoirebeobachtung, chromatischer Distanz, Formrolle und Instrumentierbarkeit bewertet werden. Diese Kriterien sind teilweise widersprüchlich. Die App sollte statt einer versteckten universellen Score-Gewichtung transparente Achsen oder Presets anbieten. Korpusfrequenzen benötigen stets eine Quelle, Abfrage, Genre, Zeitraum, Zählweise und den Nenner; unbewiesene Werte wie '83 % kompatibel' gehören nicht in die Wissensbasis.

## 5. Säule COMPOSING: eigenständige Theorie und Praxis des musikalischen Erfindens

### 5.1 Vom Einfall zur kompositorischen Aufgabe

Eine Komposition kann mit einer Melodie, Bassfigur, Harmonie, Textzeile, Klangfarbe, rhythmischen Zelle oder formalen Constraint beginnen. Daraus ergibt sich ein **Creative Brief** mit Kontext (`genre_tradition`, `ensemble`, `duration`, `difficulty`, `intended_form`, `source_of_material`, `rights`, `constraints`). Eine gute Workbench muss Entwurfsentscheidungen sichtbar halten: 'Was bleibt invariant?', 'Was wird variiert?', 'Welche Alternative wurde verworfen und warum?'. Im Unterschied zu einem Generator soll STEPS nicht vorgeben, das Stück automatisch 'richtig' zu schreiben, sondern Varianten begründen und kompositorische Kontrolle erhalten.

Belkins *Musical Composition: Craft and Art* behandelt nach offizieller Verlagsbeschreibung das Entwickeln und Verbinden von Ideen, den Aufbau von Höhepunkten und die formale Gesamtgestaltung, bewusst über verschiedene Stilfelder hinweg [SRC-V3-0004]. Das macht das Werk besonders relevant als **Quellenkandidat** für ein universell einsetzbares kompositorisches Arbeitsverfahren. Caplins Formlehre [SRC-V3-0005] und Gjerdingens historische Schemata [SRC-V3-0007] sind dazu komplementäre, stilistisch enger begrenzte Blickwinkel. Das neue offene *Music Composition & Theory* von Rubin [SRC-V3-0003] zeigt außerdem, dass sich Komposition als sequenziell aufbauende Übungs- und Modellmethode dokumentieren lässt, statt lediglich Harmonielehre zu wiederholen.

### 5.2 Motiv- und Themenentwicklung

Ein Motiv kann durch Rhythmus, Kontur, Intervalle, Register, Harmonie, Timbre oder artikulatorische Besonderheiten erkennbar sein. `C–D–E` ist als nacktes Pitch-Triple wenig individuell; eine rhythmische Gestalt `q e e` und ein charakteristisches Pausenmuster sind oft zentral. Entwicklungstechniken umfassen `sequence`, `transposition`, `inversion`, `retrograde`, `fragmentation`, `liquidation`, `augmentation`, `diminution`, `interval expansion`, `interval compression`, `register shift`, `rhythmic displacement`, `variation`, `permutation` und `combined transformation`. Die V3-Technikbibliothek enthält diese Verfahren als **69 operative Karten** mit definiertem Schritt, eigenem Beispiel und Gegenprüfung.

Eine wesentliche theoretische Trennung betrifft Inversion: `melodic inversion` verändert Richtungen von Intervallen um eine Achse; `chord inversion` ändert den Basston; `pitch-class inversion TnI` ist eine modulo-12-Transformation; `functional inversion` ist wieder eine andere Sache. Codex darf diese Operationen niemals unter einem undifferenzierten `invert()` implementieren. Die gleiche Präzision braucht `sequence`: Wiederholt das System eine diatonisch angepasste Melodie, eine exakt chromatisch transponierte Gestalt, nur den Rhythmus oder einen harmonisch ähnlichen Verlauf?

### 5.3 Phrasierung und Formfunktionen

Komposition braucht ein Modell zeitlicher Funktion. Ein achttaktiger **Sentence** kann modellhaft 2+2+4 mit Präsentation, Fortspinnung/Continuation und Kadenzbereich arbeiten; eine **Period** arbeitet typischerweise mit verwandtem Antecedent und Consequent, dessen Schluss stärker ist. Die differenzierten Formfunktionen sind bei Caplin explizit ausarbeitet [SRC-V3-0005]. Doch ein beliebiges achttaktiges Pop-Pattern als klassischen Sentence zu etikettieren, wäre methodisch falsch. STEPS sollte deshalb nicht nur `measures=8`, sondern `formal_unit_kind`, `formal_function`, `cadence_evidence` und `status` führen.

Für Pop und Rock sind Verse–Chorus-/Verse–Prechorus–Chorus-Modelle sowie Bridge, Break, Instrumental/Outro und ihre Wechselwirkungen mit Harmonik, Textur, Melodie und Text eigenständige Beschreibungen. Nobile entwickelt einen Ansatz, der Form über harmonische und thematische Anlage analysiert [SRC-V3-0009]. Daraus folgt eine App-Bedienidee: derselbe Akkordloop kann im Verse und Chorus wiederkehren, während Hook, Register, Dichte und Prosodie den Abschnittscharakter verändern. Ein Formgenerator, der immer neue Akkorde für einen Chorus fordert, wäre zu eingeschränkt.

### 5.4 Melody Writing, Topline und Textprosodie

Eine Melodie lässt sich entlang von Kontur, Zieltönen, Spannungsverlauf, Range, Atemlänge, motivischer Wiederholung, Rhythmik, Sprachakzent und Harmony Fit entwickeln. Ein verse motif mit niedriger Lage kann im Chorus leicht erweitert, rhythmisch verschoben oder auf einen anderen melodischen Zielton geführt werden. Textprosodie verlangt eine separate Repräsentation von Silben, Betonungen und Wortphrasen – sonst entstehen trotz korrekter Harmonik unnatürliche Gesangslinien. STEPS sollte in der ersten Wissensbank sowohl instrumentale Motive als auch vokale Phrasen abbilden; Lyrics selbst unterliegen bei übernommenen Songs gesonderten Urheberrechten.

Ein `melody-note` braucht Onset, Dauer, Pitch-Spelling, Phrasenrolle, Betontheitsgrad und kontextuelle Akkordfunktion; ohne zeitliche Überlappung ist die Aussage 'passt zu Akkord X' fachlich nutzlos. Im Reharmonizer muss eine Melodienote als Chord Tone, Extension, vorbereitetes Suspension-Tone, Passing Tone, Appoggiatura oder freie Dissonanz analysierbar sein. Eine harte Restriktion 'nur Chord Tones erlaubt' würde viele musikalische Lösungen unrechtmäßig ausschließen.

### 5.5 Bass, Stimmführung, Gegenstimmen, Arrangement, Orchestrierung

Eine attraktive chord progression ist noch kein ausnotiertes Stück. Das kompositorische Ergebnis hängt von Basslinien und ihrer Rhythmik, inneren Stimmen, Melodiestimmen, Lage, Register, Instrumenten, Kontrapunkt und Artikulation ab. Eine `Cmaj7`-Sonorität kann als eng gesetztes Klavier-Voicing, weit gesetzter Streicherakkord, Gitarren-Shape oder synth pad verschiedene Möglichkeiten und Grenzen besitzen. Deshalb trennt das Modell `harmony_symbol` von `realized_voicing`, `instrumental_role` und `articulation`.

Kontrapunkt verfolgt Unabhängigkeit und Wechselbeziehungen von Stimmen. Species Counterpoint ist eine hilfreiche historische Übungsdisziplin, aber Parallelquintenregeln gelten nicht universell für Power-Chord-Riffs. Partimento und galante Schemata demonstrieren historische Methoden des komponierenden Improvisierens und bassbasierten Satzes [SRC-V3-0007; SRC-V3-0008]. Jazz-Arrangement wiederum kann Guide-Tones, Drop-2-Voicings und chromatische Enclosures nutzen. Jedes Arrangementmodul muss seinen Stil und seine Annahmen deklarieren.

### 5.6 Repetition, Prozess und Kompositionsästhetik

Minimalistische und prozessorientierte Komposition kann Wiederholung, additive Subtraktion, Phasenverschiebung, Permutation und Klangtextur zur Formbildung nutzen, ohne starke funktionale Akkordwechsel. Algorithmische und generative Komposition bietet kontrollierbare Constraints und Alternativen; ihre musikalische Güte muss zusätzlich gehört, kontextualisiert und evaluiert werden. Die Codex-Datenmodelle sollen deshalb `compositional_operation`, `preserved_properties`, `changed_properties`, `evaluation_procedure` und `authorial_decision` enthalten. Ein Algorithmus darf nicht behaupten, mathematisch die einzige schöne Lösung gefunden zu haben.

### 5.7 Originäre Kompositionsstudien

Die **19 `ORIGINAL-STUDY-V3`-Einträge** im Paket sind eigenständige Skizzen über klassische, modale, Jazz-, Pop-, Blues-, Film-, Minimal-, R&B- und kontrapunktische Ansätze. Sie verknüpfen Startmotiv, harmonischen Plan, Formvorgabe, Besetzung, Entwicklungsschritt, Bass-/Voice-Leading-Plan und methodische Grenzen. Sie sind **keine vollständigen, aufgeführten Kompositionen** und enthalten keine aus geschützten Songs übernommenen Melodien. Ein späterer Codex-Lauf soll daraus mit überprüfter Pitch-/Rhythmusgrammatik testbare MusicXML-/MIDI-Modelle generieren und musikalisch reviewen; solange der Ausführungsschritt fehlt, dürfen sie nicht als 'produced scores' bezeichnet werden.

## 6. Querschnitt: Musikpsychologie, Erwartung, Analyse, Kultur

Huron untersucht musikalische Erwartung psychologisch [SRC-V3-0024]; Meyer verknüpft Muster, Erwartung, Interpretation und Emotion [SRC-V3-0025]; Temperleys computational-cognitive Modell beschäftigt sich mit Meter, Harmonie, Pitch-Spelling und Präferenzregeln [SRC-V3-0023]. Diese Ansätze können den Nutzer bei Begriffen wie Antizipation, Stabilität, überraschender Fortsetzung und Wiederholung unterstützen, aber sie legitimieren kein universelles `mood=nostalgic`-Abbildungsgesetz. Eine Musiklern-App sollte emotionale oder genrebezogene Wörter als beschreibende Benutzerkategorien führen, nicht als wissenschaftlich endgültige Aussagen über jeden Hörer.

Bei nichtwestlichen Theorie- und Kompositionskonzepten ist methodische Selbstbeschränkung zentral. **Raga** umfasst über bloße Tonvorräte hinaus melodische Verläufe, charakteristische Gesten und Aufführungskontexte. **Maqam** ist traditionsspezifisch, verwendet differenzierte Intonation und melodische Wege und kann nicht automatisch als 'phrygian with quarter tones' übersetzt werden. Gamelan-Stimmungen sind ensemble- und traditionsgebunden. Auch die Rede von 'afrikanischem Rhythmus' im Singular wäre eine unzutreffende Homogenisierung. Hier führt V3 ausdrücklich eine **Acquisition Queue** statt fingierter Vollabdeckung. Die Implementierung einer globalen Theoretik sollte nur traditionell verifizierte Datenmodelle aufnehmen.

## 7. Computational Music Theory und Knowledge Engineering

### 7.1 Architekturphilosophie

STEPS sollte Theorie- und Kompositionswissen nicht ausschließlich als lange SKILL-Anweisung speichern. Eine kuratierte Knowledge Base führt Versionen, Quellen, Begriffe, Regeln, Beispiele, Gegenbeispiele, relationale Bezüge und Tests. Ein kompakter Skill benutzt sie kontrolliert: Er normalisiert Benutzeranfragen, ruft passende Fachbereiche ab, wählt Analyse-Lenses, trennt sichere Aussagen von Interpretation und referenziert die geprüfte Evidenz. Der GUI-Code darf keine fachlichen Wahrheiten in Button-Callbacks verstecken.

Datenfluss: `Raw Source (rechtlich kontrolliert) → Source Metadata → Claim/Concept → Rule/Pattern → Example/Test → Review → Skill Reference → App Service`. Ein Gap Register führt unprüfbare oder widersprüchliche Claims zurück in die Recherche. Änderungen sind mit alter/neu-Version, Scopeänderung, Quellenstatus und Reviewentscheidung dokumentiert. Die V3-JSON-Sammlungen bilden **einen umfangreicheren Seed**, nicht das bereits endgültig reviewte Produktmodell.

### 7.2 Formate und Interoperabilität

`Harte` repräsentiert Chordsymbole in maschinenlesbarer Syntax [SRC-V3-0027]. `music21` kann Roman Numerals und Key-Context als eigene Objekte behandeln [SRC-V3-0034]. `DCML` liefert Harmonieannotierungen mit eigener Syntax [SRC-V3-0031], `ChoCo` harmonisiert unterschiedliche chord-annotation Korpora [SRC-V3-0028], `When in Rome` bewahrt funktionale Analysevielfalt statt eine einzige ground truth zu unterstellen [SRC-V3-0030]. `MusicXML 4.0` ist Notationsaustausch [SRC-V3-0035] und `MEI 5.1` bietet besonders differenzierte Editions-/Notationsebenen [SRC-V3-0036]. MIDI transportiert andere Informationen als eine Musiknotation; Transkription und Export müssen als verlustbehaftete Roundtrips getestet werden.

Die produktive interne Normalisierung soll daher verschiedene Klassen halten: `SpelledPitch`, `PitchClass`, `Interval`, `Scale`, `Mode`, `KeyContext`, `ChordSymbol`, `Voicing`, `HarmonicEvent`, `AnalysisLens`, `FormalUnit`, `Motif`, `MelodyPhrase`, `CompositionPlan`, `ArrangementPlan`, `Transformation`, `SourceEvidence`, `ReviewRecord`, `ValidationCase`. Jedes Objekt trägt ausdrücklich ein `scope`-Feld für Repertoire und Stil, und jede fachlich streitbare Analyse darf `alternatives` besitzen.

### 7.3 QA: syntaktisch und musiktheoretisch

Ein JSON-Schema kann prüfen, dass `source_candidates` Arrays sind, aber nicht, ob ein bII als Neapolitaner in einem Beispiel musikalisch plausibel ist. Deshalb braucht die Wissensdatenbank drei Prüfarten: **maschinelle Strukturtests** (IDs, Typen, Referenzen, Dateien, Spelling, Mod-12-Arithmetik), **musikalische Golden Cases** (Tonleitern, Akkorde, enharmonische Details, Roman Numerals, Kadenzen, Transformationsoperationen) und **human/peer review** (Stilgerechtigkeit, musikalische Mehrdeutigkeit, kompositorische Stringenz, Rechte/Ethik). Die V3-Datei `VALIDATION_CASES_V3.json` enthält **110 spezifizierte Tests**, davon ein Teil bewusst menschlich oder später engine-abhängig. Ein Testfall in einer Datei ist nicht dasselbe wie ein tatsächlich bestandener Testlauf.

Beispiel für eine Pflichtprüfung: `H3 → C4` = Halbton in 12-TET, international `B3 → C4`. Ein Codex-Lauf soll zusätzlich prüfen, ob `B` mit falscher Locale als deutsches `B` missverstanden werden kann. In der Jazz-Syntax muss `Db7` aus `Db-F-Ab-Cb` bestehen, während `Cmaj7` aus `C-E-G-B` besteht. Eine gleichklingende Note darf nicht durch bloßes `sharp/flat`-String-Replacement eine andere Funktion vortäuschen. Ebenso ist ein vierbarriger `G7–C`-Übergang nur dann eine Kadenz, wenn Formfunktion und Stimmenführung dies stützen.

## 8. Recht, Versionierung und Wissenschaftlichkeit

Die öffentliche Steps-Knowledge-Base darf keine nicht freigegebenen vollständigen Lehrbücher, kommerziellen Chord-Wheel-Grafiken, urheberrechtlich geschützte Songtexte oder proprietäre Datenbankexporte aufnehmen. **Lesezugriff ist kein Recht zur Weiterveröffentlichung.** Verlagsseiten und Research-Papers dürfen bibliografisch verlinkt und sachlich paraphrasiert werden, aber exakte umfangreiche Übernahmen brauchen eigene Lizenzprüfung. Selbst bei CC BY und CC BY-SA muss die konkrete Ausgabe, Attribution, Rechtekette und gegebenenfalls ShareAlike-Trennung zwischen Text und Software geprüft werden.

Die Quellenbibliothek ist absichtlich größer als das distributierbare Paket. Detaillierte Source Records erhalten Status `catalogued`, `access_verified`, `text_reviewed`, `claim_location_verified`, `license_checked`, `reviewed`. Kein automatischer Übergang durch bloßes Vorhandensein eines URL-Feldes. Open-source Softwarecode kann permissiv lizenziert sein, während zugehörige Notendaten und Audioaufnahmen gesondert geschützt sind. Ein Research-Claim ohne bestätigte Primärfundstelle bleibt als Candidate markiert.

## 9. Unmittelbare Schlussfolgerung und weitere Forschung

Die vier Säulen verlangen eigene Forschungsbreite und technische Bewertungsmaßstäbe. **Music Theory** braucht präzise interdisziplinäre Modelle, **Harmony** mehrere kompatible und inkompatible Analyseschulen, **Chord Progressions** zeitliche und melodisch-formale Daten und **Composing** vollständige Entwurfs-/Entwicklungs-/Form-/Arrangementprozesse. Die V3-Sammlung schafft dafür eine substanzielle, jedoch noch nicht vollständig fachlich verifizierte Seed-Infrastruktur. Das folgende Codex-Briefing soll die Daten nicht einfach übernehmen, sondern source-by-source prüfen, schema-validieren, fachlich reviewen und versionsgebunden in das tatsächliche Repository integrieren.

**Zentraler Forschungsbeitrag:** Der theoretische Wert von STEPS ist nicht eine immer größere Liste potenzieller Nachfolgeakkorde, sondern ein *erklärbares, stilbewusstes Kompositions- und Harmonie-Wissenssystem*, das Begriffe, Möglichkeiten, Entscheidungen und musikalische Resultate verknüpft.
