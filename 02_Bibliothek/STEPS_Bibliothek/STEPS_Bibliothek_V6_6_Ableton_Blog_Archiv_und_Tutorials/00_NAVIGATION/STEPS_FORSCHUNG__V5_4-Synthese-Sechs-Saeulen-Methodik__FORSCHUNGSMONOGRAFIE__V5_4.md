# STEPS V5.4 – Forschungs-Synthese: Harmonie, Komposition, Drums und Production

**Forschungsversion 5.4.0 · 8. November 2026 · selbständig entstandene Dokumentationssammlung.**

## 1. Warum die neue Bibliothek umfangreicher ist, ohne das Problem mit bloßen Zahlen zu kaschieren
V5.3 brachte wichtige Grundkapitel und zwölf originale Groove-Studien. Für eine Codex-taugliche Wissensbasis fehlte jedoch eine zusammenhängende Kette von fachlicher Behauptung zu konkretem musikalischen Gegenbeispiel, formaler Datenstruktur, technischem Test und offener Hörprüfung. V5.4 ergänzt deshalb einzelne Fachstudien und Original-MIDI, trennt Grundlagen von Interpretationen und legt eine Migrationsstrategie vor. Weder die zuvor erzeugten abgeleiteten Progressionsvarianten noch die neuen Beispiele dürfen als unabhängige wissenschaftliche Entdeckungen gezählt werden.

## 2. Die sechs Hauptsäulen und ihre unterscheidbaren Fragen

**Music Theory:** Welche Struktur ist unabhängig von einer einzelnen Interpretation notierbar? Pitch, Enharmonik, Intervall, Tuning, Metrik, Motivkontur und Gehörbildung benötigen teilweise verschiedene Repräsentationen.

**Harmony:** Welche Deutung einer Akkordverbindung ist mit einem bestimmten Repertoire, einer zeitlichen Umgebung und einer Theorie-Lens vereinbar? Tonalität und Funktionsharmonik sind weder identisch noch universal.

**Chord Progressions:** Welche Akkorde finden wann und über welcher Bass-/Melodiebewegung statt? Ein harmonischer String ohne Dauer, Voice Leading und Form ist als Songmodell unvollständig.

**Composing:** Welche Entscheidungen erzeugen aus minimalem Material Form, musikalische Entwicklung, Kontrast, Kadenz oder Ambiguität? Die Maschine soll Auswahlarbeit unterstützen, nicht ästhetischen Erfolg garantieren.

**Drums & Groove:** Welche Onsets, Akzente, Timingabweichungen und Klangreaktionen tragen zur Phrasenentwicklung bei? Eine Kick-/Snare-Matrix ist weder ein vollständig klingender Beat noch eine genormte Genredefinition.

**Producer Tools:** Wie werden Noten in tatsächlichen Klang verwandelt, wie wirkt eine Processing-Kette und welche Messungen sind nachweisbar? MIDI, Audio, Presetparameter, Normmessung und Hörurteil sind separate Schichten.

## 3. Repräsentationsprinzipien
Kanonisches musikalisches Datenmodell → interpretative Layer → soundbezogene Layer → Ergebnis-/Review-Layer. Eine Metrik darf eine Funktionsebene nicht stillschweigend substituieren. Das exportierte MIDI soll seine eigenen Timinginformationen prüfbar halten; die rein notierte Stimmenführung kann zusätzlich in MusicXML geführt werden. Die konkrete Roundtrip-Fähigkeit muss Codex erst im echten Projekt testen. [R06,R10,R11,R12]

## 4. Drei miteinander verknüpfte Originalfälle
**Fall A (Tonalität):** `Am–F–C–G`, vier Takte, 98 BPM. Die Pitchfolge allein belegt weder a-Moll noch C-Dur als zwingendes Zentrum. Ein A-orientierter Bass und eine Hook-Endnote A erzeugen andere Evidenz als die Endnote C. In der Bibliothek stehen beide Tonikalesarten und eine Aufgabe zur Unterscheidung. [R04,R05]

**Fall B (Groove):** Ein gerades Pattern mit 16tel-Raster kann durch 0,292 Step-Verschiebung bestimmter Ereignisse im konkreten Groove anders wirken. Bei 132 BPM sind das circa 33,18 ms. Ein anderer Sample-Transient oder ein zweiter Groove verändert das Ergebnis: Deshalb stehen Eventzeit und Velocity/Sound getrennt. [R13,R20]

**Fall C (808-Note-Off):** Die MIDI-Note Eb1/27 über einen achtelartigen Impuls ist eine Eingabe, keine Garantie für entsprechende Audioamplitude. In OneShot- und gated-Samplerzuständen können identische MIDI-Dauern zu unterschiedlichen Klangenden führen. Die tatsächliche Audiohüllkurve bleibt zu messen. [R12,R14]

## 5. Qualitätsklassen
**Mechanical:** Formate, Intervalle, negative Dauern, MIDI Note-Events, Id-Referenzen, Hash-Abgleich. **Theory:** stimmführungs-, notations- und stilbezogene Fachprüfung. **Corpus:** Quellenstatus, Annotationsvarianten, Leakage. **Production:** DAW-, Patch- und Audio-Renderprüfung. **UX:** tatsächliches Lernverständnis. Es ist ein Fehler, technische Einzelprüfungen als musikwissenschaftliche Peer Reviews zu zählen.

## 6. Lizenz- und Rechtegate
Open Music Theory wird von der Website als CC BY-SA 4.0 beschrieben; Edinburghs Lehrbuch führt CC BY-NC-SA 4.0; Belkins frei lesbare Lehrmaterialien sind dennoch urheberrechtlich geschützt. Als Reuse-Kriterium gilt die Lizenz der konkreten Ausgabe und des konkreten Items, nicht die generelle Abrufbarkeit. Geschützte PausePlayRepeat-Originallektionen werden in dieser weitergabefähigen Bibliothek nicht vollständig wiedergegeben. [R01,R02,R19]

## 7. Grenzen der Genreabdeckung
Die vier bereitgestellten Drum-Stile (UK Garage, D&B, Techno, Rage) sind didaktische Referenzen, keine Vollständigkeitsliste. Weitere Felder wie reggaeton/dembow, amapiano, baile funk, footwork/juke, breakcore, jungle, dancehall, funk, afrobeats, UK funky, jersey club, gqom, house-Unterarten, dubstep und cross-cultural rhythm practice müssen quellenkritisch separat erschlossen werden. Die existierenden STEPS-MIDI-Studien belegen keine Genre-Authentizität.

## 8. Die vier ergänzenden Querschnittsdisziplinen
**Kognition und Kultur:** Hörwahrnehmung ist weder vollständig mathematisch noch kulturübergreifend identisch. Für modale Traditionen und Genrezuordnungen werden qualifizierte Kontextquellen und gegebenenfalls Review aus den jeweiligen Traditionen gebraucht.

**Computational Music:** DCML/MusicXML/MEI/music21 sind wertvolle Referenzen, aber heterogene Standards. Kein einzelner ist vollständiger Ersatz für ein versionsfähiges, zeitliches Steps-Datenmodell.

**Produktdidaktik:** Erklären, Hören, Vergleichen, Verändern, Wiederholen und eigenes Komponieren sind eigenständige Kompetenzziele. Gute Quizmetriken dürfen nicht als Kompositionsqualität missverstanden werden.

**Governance:** Quelle→Claim→Wissensobjekt→Test→Review→Implementierung; Status und Lizenz je Glied. Das Quellenschema bleibt gegenüber lokalen privaten MIDI-Repositories offen.

## 9. Konkreter Codex-Entwicklungsweg
1. Repo lesen und Quellrechte prüfen. 2. Alte Wissensobjekte nach IDs und Typen kartieren. 3. Kanonische Events und Annotationen mit Migrationsadapter entwickeln. 4. Harte Invarianten zuerst testen. 5. Lehrmodule und Analysis-Lenses stufenweise in die UI integrieren. 6. Hör-/Fachreviews als gesondertes Gate. 7. Änderungen als nachvollziehbaren PR bereitstellen, nicht automatisch mergen.

## 10. Verbleibende zentrale Lücken
Kein lokaler Original-PPR-MIDI-Ingest, keine authentifizierten DAW-Projekte, kein Audio-Bounce-/Loudness-Test, keine verifizierte vollständige Lektüre der urheberrechtlich geschützten Fachbücher, keine unabhängige empirische Hörer-Studie und keine tatsächliche Integration in das Nutzer-Repository. Auch die neue 16-Takt-MIDI-Gruppe sind didaktisch generierte Studien, keine ausgefeilten Produktionen.

## 11. Prüfbasis der 43 Einzelstudien

### MUSIKTHEORIE
**Tonhöhe, Schreibweise und Enharmonik.** MIDI-Pitch, klingende Frequenz, diatonischer Buchstabe und Vorzeichen sind getrennte Eigenschaften. In 12-TET können C# und Db gleich klingen, aber nicht dieselbe harmonische Rolle tragen. Ein Pitch-Objekt muss Notenname und Stimmungskontext speichern, nicht bloß pitch class. *Kritischer Gegenpunkt:* Es wäre ein Fehler, `midi=61` fest als `C#4` zu speichern und daraus jede notierte Lesart abzuleiten. DAW-Oktavnummern variieren zusätzlich. (Quellenanker R01, R02, R10).

**Intervalle nach Buchstaben und Halbtönen.** Intervallqualität folgt aus diatonischer Stufenzahl und chromatischem Abstand. C–E# ist eine übermäßige Terz, C–F eine reine Quarte; beide können in 12-TET denselben Abstand haben. *Kritischer Gegenpunkt:* Eine Halbtonzahl allein erklärt kein notiertes Intervall und keine stimmführungstechnische Auflösung. (Quellenanker R01, R02).

**Skalen, Modi und hörbare Zentren.** Modus ist nicht allein eine rotierte Liste von Tonklassen. Der Tonvorrat und die wahrgenommene Tonika/Finalis unterscheiden sich; melodische Betonung, Pedal, Kadenz und Arrangement schaffen Zentrum. *Kritischer Gegenpunkt:* Sieben C-Dur-Tasten und ein Dm-Akkord reichen nicht als Beweis für D-Dorisch. (Quellenanker R01, R02).

**Stimmungssysteme und Mikrotonalität.** Die Frequenzformel f=440·2^((m−69)/12) gilt für MIDI-Noten unter A4=440 und 12-TET; sie ist keine universale Beschreibung von Intonation. Andere Stimmungen benötigen Referenz, Interval-Mapping und ggf. per-note bends oder MTS. *Kritischer Gegenpunkt:* Die Vorzeichen-Schreibweise allein definiert keine reale mikrotonale Stimmung. (Quellenanker R01, R12).

**Puls, Takt, Metrum und Hypermetrik.** Metrum bildet mehrere Ebenen von Akzent und Gruppierung; eine 16-Step-Rasterposition ist keine vollständige metrische Analyse. Auftakte, Taktwechsel und Halftime/Doubled-Feel müssen separat geführt werden. *Kritischer Gegenpunkt:* Eine halbierte gefühlte Beat-Rate ist keine zwingende Änderung der gespeicherten Tempo-Events. (Quellenanker R01, R12, R21).

**Melodische Struktur und motivische Identität.** Ein Motiv kann durch Intervallfolge, Rhythmus, Kontur, Register, Artikulation oder Timbre wiedererkannt werden. Strikte Tonhöhenidentität ist nur eine von vielen Motivdefinitionen. *Kritischer Gegenpunkt:* Die automatische Erkennung gleicher Konturen ist keine hinreichende Aussage über künstlerische Wiedererkennbarkeit. (Quellenanker R03, R19).

**Aktive Gehörbildung und diagnostische Aufgaben.** Eine gute Übung trennt Hören, Benennen und Transfer in tatsächliche Musik. Referenzklänge, Stimmregister und Timbre können Erkennungsleistung beeinflussen; abstrakte Quizfragen allein sind nicht ausreichend. *Kritischer Gegenpunkt:* Eine falsche Ziffernantwort beweist kein fehlendes Gehör; es kann eine andere plausible theoretische Lesart vorliegen. (Quellenanker R01, R02).

### HARMONIE
**Funktion, Stufe und Satzkontext.** Funktion (T, PD, D) ist ein interpretatives Gerüst für bestimmte tonale Stile; eine Stufenangabe bezeichnet zunächst eine diatonische Wurzelrelation. Die Zuordnung darf nicht stilübergreifend erzwungen werden. *Kritischer Gegenpunkt:* Sehr lange Akkordschleifen brauchen keinen abschließenden Tonic-Event, obwohl C als Zentrum plausibel bleibt. (Quellenanker R01, R06, R08).

**Leittöne, Septimen und kontextabhängige Auflösung.** In der klassisch-tonalen Schreibpraxis sind 7→1 und die absteigende Akkordseptim häufige Zielbewegungen; in Rock/Jazz/Blues sind sie Tendenzen und keine universell zu erzwingenden Regeln. *Kritischer Gegenpunkt:* Ein Dominantseptakkord ohne folgende Tonika kann absichtlich offen bleiben; das ist nicht automatisch ein Kompositionsfehler. (Quellenanker R01, R09).

**Zwischendominanten, Tonikalisierung und Modulation.** Eine Zwischendominante richtet sich vorübergehend auf einen diatonischen oder chromatischen Zielakkord; das Vorhandensein eines chromatischen Tons allein beweist keine Modulation. *Kritischer Gegenpunkt:* Nicht jedes E7 in einer C-Dur-Popproduktion ist zwingend eine klassisch geführte V/vi: Bass und Wiederholungsmuster zählen. (Quellenanker R06, R07, R08).

**Modal Interchange, Mixture und bVI/bVII/iv.** Geborgte Akkorde lassen sich als Austausch zwischen gleichnamigen Skalen erläutern, aber diese Erklärung ist nicht immer die einzige sinnvolle in populärer Musik. *Kritischer Gegenpunkt:* Eine Pop-Loop-Analyse mit dur/moll-basierten Roman Numerals verfehlt möglicherweise modale Zentrumseffekte. (Quellenanker R04, R05, R08).

**Blues ist mehr als Dominante-Tonika-Syntax.** Blues-Harmonik hat eigene Verbindungen zwischen Tonmaterial, Form, Melodie und Klang. I7 und IV7 müssen nicht in jedem Fall als funktionale Dominanten der nächstfolgenden Tonart gelten. *Kritischer Gegenpunkt:* Alle V7-Labels in einem 12-Bar-Blues rein funktional zu interpretieren, wäre eine systematische Fehlklassifikation. (Quellenanker R05, R17).

**Jazz-Voicings, Extensions und Spannung.** Akkordsymbole geben erlaubte bzw. gewünschte Klangklassen nicht eindeutig vor. Voicing, Register, Melodie, Bass, instrumentales Layout und Nachbarstimmen entscheiden über die Realisation. *Kritischer Gegenpunkt:* Bei enggesetzten tiefen Clustern kann eine theoretisch korrekte 9 farblich undeutlich werden. Das ist kein Syntaxfehler. (Quellenanker R08, R09).

**Neo-Riemannian, Transformation und Tonnetz.** Die P-, L- und R-Transformationen beschreiben Beziehungen zwischen Dur-/Moll-Dreiklängen unter bestimmten Annahmen. Sie ersetzen keine Funktionsanalyse und dürfen nicht als universeller künstlerischer Qualitätswert dienen. *Kritischer Gegenpunkt:* Die Analyse von Pop-Loops ausschließlich durch Tonnetz-Abstände kann Textur, Groove, Form und Spannungsauslegung ignorieren. (Quellenanker R08).

### PROGRESSIONS
**Harmonischer Rhythmus und Formfunktion.** Eine Progression besteht nicht nur aus Akkordnamen: Dauer, Taktposition, Wiederholung, Phrase und Struktur bestimmen, wie eine Folge gehört wird. *Kritischer Gegenpunkt:* Ein 4-Akkord-String ohne Durationsdaten kann weder Fill noch Kadenz-Position oder Bassartikulation bestimmen. (Quellenanker R06, R10, R04).

**Pop-Loops und doppelte Tonalität.** Eine viergliedrige Pop-Schleife kann mehrere Zentren plausibel machen, wenn Hook, Bass, Beginn/Ende und Melodie unterschiedlich gewichtet werden. *Kritischer Gegenpunkt:* Eine automatische Analyse, die nur den ersten Akkord zur Tonika erklärt, erzeugt systematisch Fehler. (Quellenanker R04, R05).

**Reharmonisieren unter einer gegebenen Melodie.** Die zulässigen Akkorde hängen nicht bloß von der Tonklasse eines Melodietons ab, sondern auch von Metrik, Dauer, Vorbereitung, Auflösung und Stil. *Kritischer Gegenpunkt:* Ein Melodieton als 9, 11 oder Vorhalt darf nicht schon wegen fehlender Drei-/Vierklangsmitgliedschaft abgewiesen werden. (Quellenanker R08, R09).

**Bassführung, Inversionen und Pedaltöne.** Der tiefste klingende Ton, der notierte Grundton und die funktionale Wurzel sind verschiedene Datenfelder. Pedalpunkte können Harmonie ohne Root-Änderung bewegen. *Kritischer Gegenpunkt:* Slash-Chords sind nicht automatisch Umkehrungen; Dm7/G kann je nach Kontext dominantisch gehört werden. (Quellenanker R08, R12).

**Übergänge, Pivot-Akkorde und Key-Change.** Ein Modulationsübergang benötigt mehr als ein fremdes Vorzeichen. Die Behauptung neuer Tonika muss durch Dauer, Kadenz, Melodie, Bass und Wiederholung getragen werden. *Kritischer Gegenpunkt:* Kurzzeitige Zwischendominante E7→Am und permanente Modulation dürfen nicht automatisch gleichgesetzt werden. (Quellenanker R03, R06).

**Regelbasierte Generierung und Nutzerkontrolle.** Ein Generator soll harte Bedingungen erfüllen (Metrik, Tonumfang, erlaubte Akkorde) und weiche Präferenzen transparent gewichten (Überraschung, Dichte, Stimmführung). *Kritischer Gegenpunkt:* Eine hohe Wahrscheinlichkeit aus einem populären Korpus macht eine Folge nicht objektiv besser; auch Daten sind genre-, jahrgangs- und annotationsabhängig. (Quellenanker R05, R17, R18).

**Korpusstatistik, Duplikate und Leakage.** Eine statistische Akkordfolge ist nur im Verhältnis zu Korpus, Annotationseinheit, Stil und Split interpretierbar. Wiederholte Songversionen können Evaluation verzerren. *Kritischer Gegenpunkt:* Seltene Tonarten oder Epochen können im Datensatz unterrepräsentiert sein; ein generierter Trend ist keine allgemeine musikalische Norm. (Quellenanker R05, R17, R18).

### COMPOSING
**Von der Idee zur überprüfbaren Kompositionsaufgabe.** Ein Kompositionsbrief definiert ästhetische Absicht, Länge, Besetzung, Schwierigkeitsgrad, Stilreferenzen und überprüfbare technische Bedingungen. Kreativität bleibt offen: Constraints unterstützen Entscheidungen, ersetzen sie nicht. *Kritischer Gegenpunkt:* Ein Brief darf nicht nur „erzeuge emotionale Progression“ enthalten; Emotion ist kultur- und kontextabhängig. (Quellenanker R19, R03, R04).

**Motivkern und entwickelnde Variation.** Motivische Entwicklung arbeitet mit wiederkehrenden Gestalten unter kontrollierter Veränderung von Intervallen, Rhythmus, Register und Tonhöhenklassen. Rückbezüge und Kontrast sind gemeinsam relevant. *Kritischer Gegenpunkt:* Augmentation und Retrograde sind nicht bloß MIDI-Events rückwärts drehen, wenn die Harmonie- und Taktsituation angepasst werden muss. (Quellenanker R19, R03).

**Satz, Periode, Phrase und formale Funktionen.** Die klassisch-tonale Theorie formaler Funktionen beschreibt Präsentation, Fortspinnung/Fortsetzung und Kadenz mit konkreten Beziehungen zwischen Material und Harmonik. Pop-Songabschnitte haben andere Strukturlogiken. *Kritischer Gegenpunkt:* Ein achttaktiger Loop ist nicht automatisch ein klassischer Satz; der Funktionsnachweis muss hör-/notierbar sein. (Quellenanker R03, R19).

**Verse, Prechorus, Chorus und Energieverlauf.** In Pop/Rock formt nicht allein Harmonie die Großform; Textposition, Hook, Register, Arrangementdichte und tonale Erwartung wirken zusammen. *Kritischer Gegenpunkt:* Der Chorus braucht nicht zwingend eine andere Akkordfolge oder eine höhere Lautheit. „Mehr Energie“ ist designbar, aber nicht universal. (Quellenanker R04, R19).

**Kontrapunkt, Register und Instrumentenrolle.** Stimmen erhalten eigene melodische Logik und müssen hinsichtlich Umfang, Dichte und Kreuzung beurteilt werden. Klassische Verbote paralleler Quinten sind modell-/stilabhängig und keine Regel für jede Produktion. *Kritischer Gegenpunkt:* Eine automatisch optimierte minimal bewegte Voicing-Folge kann ausdruckslos wirken; Bewegung und Kontrast dürfen absichtlich erhalten bleiben. (Quellenanker R09, R19).

**Adaptive Form und Übergangszustände.** Interaktive Musik braucht Zustandsmodell, Übergangslogik und rhythmisch/melodisch sinnvolle Rejoin-Punkte. Vertikales Layering und horizontales Rescoring sind andere Eingriffe. *Kritischer Gegenpunkt:* Ein crossfade im Audio ist kein Ersatz für harmonische Kompatibilität; mehrere gleichzeitig laufende Tonika-Schichten können kollidieren. (Quellenanker R19, R12).

**Kompositionsrevision mit Hörprotokoll.** Mehrstufige Revision trennt technische Fehler (Takt, Stimmen, Range), musikalische Diagnose (Wiedererkennung, Kontrast, Spannungsbogen), production-abhängige Faktoren (Klang, Mix) und persönliche Präferenz. *Kritischer Gegenpunkt:* Eine automatisierte Note-Wahl ersetzt keinen Hörvergleich; Originalität ist nicht aus einer Metrik beweisbar. (Quellenanker R19, R20, R21).

### DRUMS
**16-Step-Grid, Tempo und mathematische Zeit.** Bei 4/4 umfasst ein Takt in 16tel-Auflösung sechzehn Positionen. Ein 16tel dauert bei Tempo B BPM genau 60·1000/(4B) ms. Swing verschiebt Ereignisse relativ zum Raster; Samples haben zusätzliche Latenzen. *Kritischer Gegenpunkt:* Eine 16-Step-Darstellung ist für 12/8, Quintolen oder freie Rubato-Zeit nicht vollständig; Grid-Level muss konfigurierbar sein. (Quellenanker R12, R13).

**Swing-Deskriptor statt starrer Stilregel.** Swing kann ein wiederholbares Verschiebungsmuster sein. Timing, Velocity und Sample-Response sind getrennte Größen. Ableton kann Grooves nicht-destruktiv anwenden und anschließend committen. *Kritischer Gegenpunkt:* Die Prozentbezeichnungen verschiedener Swing-Implementierungen sind nicht immer gleich. Keine magische Umrechnung ohne Definition des Paares. (Quellenanker R13, R12).

**Kick–Sub-Bass, Transienten und Hüllkurven.** Kollisionen im Low-End können durch gleichzeitige Transienten, lange Ausklingzeiten, Phasenlage, Frequenzüberdeckung und Arrangement entstehen. MIDI-Notenstarts allein zeigen nicht die tatsächlichen Audiohüllkurven. *Kritischer Gegenpunkt:* MIDI 27 beschreibt Eb1 im wissenschaftlichen Octave-Convention; DAW-Anzeigen können anders zählen. Nicht „Sub ist phasenrichtig“ ohne Audiosignal behaupten. (Quellenanker R12, R14).

**Velocity, Ghost Notes und Sampling-Mappings.** Velocity ist MIDI-Performanceinformation, nicht automatisch identisch mit Lautheit. Unterschiedliche Sampler können Sample Layer, Filter, Hüllkurve oder Lautstärke steuern. *Kritischer Gegenpunkt:* Gleiche Velocity-Werte mit unterschiedlichen Samples lassen sich nicht als gleiche akustische Lautheit interpretieren. (Quellenanker R12, R20, R21).

**Genres als Vergleichsrahmen statt hartes Klassensystem.** UK Garage, Techno, D&B und Rage unterscheiden sich häufig durch Pulsverteilung, Artikulation, Klangdesign und Arrangement – keine einzige Kick-Position definiert den gesamten Stil. *Kritischer Gegenpunkt:* Ein Fan-Remake ist keine authentische Original-Session. Nutzertexte sind Lernmaterial; private Samples/MIDI nicht ohne Rechte redistribuieren. (Quellenanker R13, R20, R21).

**Polyrhythmik, polymetrische Akzente und zyklische Phasen.** Ein Rim alle drei 16tel gegen Kick alle vier 16tel wandert relativ zum Beat; das ist ein 3-gegen-4-Zyklus auf dem 16tel-Raster, nicht zwingend eine echte notierte 3:4-Tuplet-Polyrhythmik. *Kritischer Gegenpunkt:* Die Bezeichnungen Polymetrik, Polyrhythmik und Cross-Rhythm sind abhängig von metrischem Bezugssystem. (Quellenanker R12, R21).

**Drum-Progression als mehrtaktiger Formverlauf.** Die Entwicklung einer Drum-Phrase ergibt sich aus add/remove, Soundwechsel, Dichte, Fill, Low-End und Übergängen. Der Begriff Drum-Progression wird hier als Arrangementprozess verwendet, nicht als genormter Theoriebegriff. *Kritischer Gegenpunkt:* Mehr Drum-Noten pro Takt bedeuten nicht zwangsläufig mehr Energie; Dynamik und Klangfarbe können wichtiger sein. (Quellenanker R13, R20).

### PRODUCER
**Oszillator, Filter, Hüllkurve und Signalfluss.** Klassisch subtraktive Synthese beginnt oft mit spektral reichem Oszillatormaterial und formt es mit Filter und Hüllkurven. Andere Synthesearten (FM, granular, wavetable, additive) nutzen andere Strukturen. *Kritischer Gegenpunkt:* Oszillatortyp alleine legt Klang nicht fest. Cutoff und Resonanz interagieren mit Notenhöhe und Eingangspegel. (Quellenanker R14).

**Sampling, One-Shot und 808-Artikulation.** Sampler können Note-Off ignorieren (One-shot) oder über Amp-Hüllkurve ausklingen. Gleich lange MIDI-Blöcke bedeuten deshalb nicht gleich lange Audiosignale. *Kritischer Gegenpunkt:* Ein MIDI-Remake kann die tatsächliche 808-Hüllkurve einer Aufnahme nicht eindeutig rekonstruieren. (Quellenanker R12, R14).

**EQ als frequenzabhängiger Pegel plus Phase.** Ein Equalizer verändert typischerweise den frequenzabhängigen Übertragungsbetrag und – abhängig von Filtertyp – Phasengang/Transienten. Ein Boost ist oft lauter und daher nicht automatisch besser. *Kritischer Gegenpunkt:* Nicht aus „EQ ist Lautstärke pro Frequenz“ folgern, dass lineare und minimum-phase Filter immer dasselbe Signal liefern. (Quellenanker R16, R14).

**Kompression, Attack, Release und Gain Reduction.** Kompression ist zeit- und pegelabhängige Dynamikbearbeitung. Attack/Release sind keine einfachen geometrischen Notenlängen: Detector, Knee, Sidechain und Signalform beeinflussen die Reaktion. *Kritischer Gegenpunkt:* Messwert 2dB Gain Reduction an einem Kit gilt nicht universal für andere Samples. Make-up Gain getrennt vom Regelverhalten vergleichen. (Quellenanker R13, R16).

**Sidechain als zeitliche Maskierungssteuerung.** Sidechain-Ducking ist eine mögliche Lösung für Kick/Bass-Konkurrenz, aber nicht zwingend. Routing und Trigger müssen reproduzierbar sein; auch dynamischer EQ oder Arrangement können helfen. *Kritischer Gegenpunkt:* Ein voreingestellter Releasewert bei 130 BPM ist keine garantiert rhythmische Optimallösung. (Quellenanker R13, R16).

**Stereoabbildung, Mono-Foldown und Phasenkorrelation.** Stereo-Breite ist frequenz- und phasenabhängig. M/S-Technik trennt Mitte und Seitensignal, ist aber nicht automatisch „mono kompatibel“; eine Mono-Gegenprobe muss erfolgen. *Kritischer Gegenpunkt:* Ein Korrelationswert ohne Zeitfenster oder Frequenzband kann irreführend sein. (Quellenanker R16).

**LUFS, True Peak, Delivery und Mastering.** ITU-R BS.1770-5 beschreibt Messalgorithmen für Loudness/True Peak; EBU R128 enthält einen Broadcast-Normalisierungsrahmen. Die -23 LUFS Empfehlung ist kein weltweites Ziel für jede Club- oder Streaming-Produktion. *Kritischer Gegenpunkt:* Kein seriöser Schluss „ein Track ist professionell, weil er X LUFS hat“. Distortion, Transienten und Musikstil bleiben entscheidend. (Quellenanker R15, R16).

**DAW-Sessions, Routing und reproduzierbarer Export.** Seine Produktionsentscheidung in Steps nachvollziehbar zu machen erfordert Song-State, Tempo-Map, Clip-Onsets, Instrumenten-IDs, Patch-Versionen und Exportkontext. Eine MIDI-Datei allein enthält keine Plug-in-Kette. *Kritischer Gegenpunkt:* Ein Screenshot aus Live ist kein portabler Projektzustand, und Marken-/Versionseinstellungen können sich ändern. (Quellenanker R12, R13, R10).
