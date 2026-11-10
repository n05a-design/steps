# STEPS V4 – 59 neue formale Regeln und musikalische Interpretationsheuristiken

**Status:** Entwurfsregister. Ein mathematischer Constraint ist mit Code testbar; eine stilistische Tendenz braucht Kontext und menschlichen Review. Die 77 V3-Regeln bleiben zusätzlich im Gesamtregister.

## RULE-V4-001 – 12TET MIDI-Klasse

**Typ:** `constraint` · **Bedingung:** Tuning=12TET

**Aussage:** pc(n)=n mod 12

**Gegenfall / Grenze:** Nicht auf 19-TET als gleicher Tonklassenbegriff übertragen.

## RULE-V4-002 – Oktave in Standard-MIDI

**Typ:** `constraint` · **Bedingung:** Tuning=12TET

**Aussage:** pc(n+12)=pc(n) innerhalb des gültigen Tonbereichs

**Gegenfall / Grenze:** Register und Klangfarbe bleiben verschieden.

## RULE-V4-003 – Durleiter-Intervallstruktur

**Typ:** `constraint` · **Bedingung:** 12TET; diatonische Durtonleiter

**Aussage:** Intervallmuster 2,2,1,2,2,2,1

**Gegenfall / Grenze:** Chromatik allein genügt nicht für enharmonische Schreibweise.

## RULE-V4-004 – Natürlich-Moll-Struktur

**Typ:** `constraint` · **Bedingung:** 12TET; aeolische Tonleiter

**Aussage:** Intervallmuster 2,1,2,2,1,2,2

**Gegenfall / Grenze:** Harmonisch-Moll verändert die siebte Stufe.

## RULE-V4-005 – Dorisches Profil

**Typ:** `constraint` · **Bedingung:** 12TET; D dorian

**Aussage:** Pitch Classes D,E,F,G,A,B,C

**Gegenfall / Grenze:** D als Zentrum nicht automatisch aus Menge bestimmbar.

## RULE-V4-006 – Phrygisches Profil

**Typ:** `constraint` · **Bedingung:** 12TET; E phrygian

**Aussage:** Pitch Classes E,F,G,A,B,C,D

**Gegenfall / Grenze:** Tonzentrum muss melodisch bestätigt sein.

## RULE-V4-007 – Lydisches Profil

**Typ:** `constraint` · **Bedingung:** 12TET; C lydian

**Aussage:** Pitch Classes C,D,E,F#,G,A,B

**Gegenfall / Grenze:** F# darf nicht blind als b5 identifiziert werden.

## RULE-V4-008 – Mixolydisches Profil

**Typ:** `constraint` · **Bedingung:** 12TET; G mixolydian

**Aussage:** Pitch Classes G,A,B,C,D,E,F

**Gegenfall / Grenze:** F ist b7 und keine diatonische Leitton-F#.

## RULE-V4-009 – Notenname in F#-Dur

**Typ:** `constraint` · **Bedingung:** Diatonic spelled major scale

**Aussage:** F#,G#,A#,B,C#,D#,E#

**Gegenfall / Grenze:** F als Tonklassenersatz verhindert diatonische E-Stufe.

## RULE-V4-010 – Übermäßige Quarte

**Typ:** `constraint` · **Bedingung:** notated C to F#

**Aussage:** Intervall A4 und 6 Halbtöne 12TET

**Gegenfall / Grenze:** C–Gb ist notiert d5.

## RULE-V4-011 – Verminderte Quinte

**Typ:** `constraint` · **Bedingung:** notated C to Gb

**Aussage:** Intervall d5 und 6 Halbtöne 12TET

**Gegenfall / Grenze:** C–F# ist notiert A4.

## RULE-V4-012 – Cmaj7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {C,E,G,B}

**Gegenfall / Grenze:** C7 hat Bb statt B.

## RULE-V4-013 – C7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {C,E,G,Bb}

**Gegenfall / Grenze:** Dominantseptakkord ohne Tonartfunktion.

## RULE-V4-014 – Cadd9 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {C,E,G,D}, ohne implizite Septime

**Gegenfall / Grenze:** Cmaj9 hat zusätzlich B.

## RULE-V4-015 – G7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {G,B,D,F}

**Gegenfall / Grenze:** Akkord allein legt Tonikaregion nicht fest.

## RULE-V4-016 – Dm7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {D,F,A,C}

**Gegenfall / Grenze:** D-moll-Dreiklang enthält kein C.

## RULE-V4-017 – Am7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {A,C,E,G}

**Gegenfall / Grenze:** A7 hat C# statt C.

## RULE-V4-018 – F#m7 Bestand

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {F#,A,C#,E}

**Gegenfall / Grenze:** Doppelte Vorzeichen anderer Tonarten brauchen eigenen Speller.

## RULE-V4-019 – Half-diminished Bm7b5

**Typ:** `constraint` · **Bedingung:** default 12TET chord symbol

**Aussage:** {B,D,F,A}

**Gegenfall / Grenze:** Bdim7 enthält Ab statt A in dieser Schreibung.

## RULE-V4-020 – Taktlänge 4/4

**Typ:** `constraint` · **Bedingung:** Notated 4/4, quarter-beat clock

**Aussage:** Summe der Ereignisdauern pro Stimme/Takt ≤4 mit vollständigem Stimmenrhythmus =4

**Gegenfall / Grenze:** Sustains können Taktgrenzen überschreiten, falls explizit notiert.

## RULE-V4-021 – MIDI Tonhöhenbereich

**Typ:** `constraint` · **Bedingung:** Standard MIDI1 note number

**Aussage:** 0 ≤ note ≤ 127

**Gegenfall / Grenze:** MIDI2 kann andere Expressivität transportieren, nicht neue hier erfundene Zahl.

## RULE-V4-022 – MIDI Velocity 7bit

**Typ:** `constraint` · **Bedingung:** standard note-on velocity

**Aussage:** 0 ≤ velocity ≤ 127

**Gegenfall / Grenze:** Velocity 0 in NoteOn wird häufig als NoteOff behandelt.

## RULE-V4-023 – Transponieren um Oktave

**Typ:** `constraint` · **Bedingung:** 12TET; note-number-valid

**Aussage:** n→n+12 behält pc

**Gegenfall / Grenze:** Register und Instrumentengrenzen ändern sich.

## RULE-V4-024 – Dauer und Start

**Typ:** `constraint` · **Bedingung:** positive timed note event

**Aussage:** duration>0 und onset≥0

**Gegenfall / Grenze:** Auftakte können relativ zu taktbezogenem Nullpunkt modelliert werden.

## RULE-V4-025 – Source ID eindeutig

**Typ:** `constraint` · **Bedingung:** source registry

**Aussage:** Jede ID kommt nur einmal vor

**Gegenfall / Grenze:** Editionen dürfen eigene IDs bekommen.

## RULE-V4-026 – Theory claim provenance

**Typ:** `constraint` · **Bedingung:** claim marked verified

**Aussage:** Exakter Locator und Quelle notwendig

**Gegenfall / Grenze:** Quellenfamilienlink allein ist keine überprüfte Seite.

## RULE-V4-027 – License reuse gate

**Typ:** `constraint` · **Bedingung:** öffentliches Repo

**Aussage:** Ohne erlaubte Redistribution keine Originalkopien öffentlich übernehmen

**Gegenfall / Grenze:** Forschung darf bibliografisch zitieren.

## RULE-V4-028 – Roman numeral contextual key

**Typ:** `constraint` · **Bedingung:** functional roman analysis

**Aussage:** Tonal center oder expliziter unknown-Status nötig

**Gegenfall / Grenze:** Der gleiche Am-Akkord ist vi in C, i in a.

## RULE-V4-029 – SKILL ist kein Quellenarchiv

**Typ:** `constraint` · **Bedingung:** agent reference architecture

**Aussage:** Lange Wissensartikel bleiben in KB, Skill enthält Verfahren

**Gegenfall / Grenze:** Kleine dynamisch geladene Referenzen sind zulässig.

## RULE-V4-030 – Progression Event context

**Typ:** `constraint` · **Bedingung:** sequenced chord data

**Aussage:** Onset, duration, chord und ggf. analysis_candidates vorhanden

**Gegenfall / Grenze:** Auftrag kann nur lose Akkordliste liefern, dann pending timing.

## RULE-V4-031 – Leittonbewegung zur Tonika

**Typ:** `tendency` · **Bedingung:** klassisch-tonaler V–I-Kontext

**Aussage:** Stufe 7 kann nach 1 steigen

**Gegenfall / Grenze:** Jazz und Pop können Bewegung anders führen.

## RULE-V4-032 – Sekundärdominante

**Typ:** `tendency` · **Bedingung:** tonal context C; A7 before Dm

**Aussage:** A7 plausibel V7/ii

**Gegenfall / Grenze:** Ohne Dm-Auflösung bleibt alternative Analyse offen.

## RULE-V4-033 – Minor V7

**Typ:** `tendency` · **Bedingung:** A minor and E7→Am

**Aussage:** G# kann Leitton nach A sein

**Gegenfall / Grenze:** In Äolisch ist Em ohne G# ebenfalls möglich.

## RULE-V4-034 – Trugschluss

**Typ:** `tendency` · **Bedingung:** C major; G7→Am

**Aussage:** V7–vi kann klassisch als Trugschluss wirken

**Gegenfall / Grenze:** Nicht jedes V→vi in einem Pop-Loop ist klassische Kadenz.

## RULE-V4-035 – Mollsubdominante

**Typ:** `tendency` · **Bedingung:** C major; Fm→C

**Aussage:** Ab→G kann chromatische Stimmführung betonen

**Gegenfall / Grenze:** Nicht jedes Fm verlangt Borrowed-Chord-Erzählung.

## RULE-V4-036 – Guide tones in ii-V-I

**Typ:** `tendency` · **Bedingung:** jazz C; Dm7-G7-Cmaj7

**Aussage:** F→F→E und C→B→B als mögliche Stimmenbewegungen

**Gegenfall / Grenze:** Nicht die einzig mögliche Voicing-Wahl.

## RULE-V4-037 – Tritonussubstitution

**Typ:** `tendency` · **Bedingung:** jazz G7→C

**Aussage:** Db7→C als chromatische Alternative bei kompatibler Melodie

**Gegenfall / Grenze:** Nicht für jeden Stil/Beat und jede Melodie sinnvoll.

## RULE-V4-038 – Plagaler Rückgang

**Typ:** `tendency` · **Bedingung:** IV→I in tonalem Kontext

**Aussage:** Kann Schluss- oder Ruhefarbe tragen

**Gegenfall / Grenze:** Authentische Kadenz ist im klassischen Modell anders definiert.

## RULE-V4-039 – Rhythmische Verdichtung

**Typ:** `tendency` · **Bedingung:** kompositorische Fortsetzung

**Aussage:** Kürzere Motiveinsätze können dynamisieren

**Gegenfall / Grenze:** Wiederholung bei geringem Tempo kann auch Ruhe erzeugen.

## RULE-V4-040 – Registeröffnung

**Typ:** `tendency` · **Bedingung:** orchestration

**Aussage:** Breitere registrale Anlage kann den Höhepunkt unterstützen

**Gegenfall / Grenze:** Leises, enges Register kann absichtlich intensiver wirken.

## RULE-V4-041 – Metrische Platzierung

**Typ:** `tendency` · **Bedingung:** Phrasenschluss

**Aussage:** Starker Zielbeat kann Schlusserwartung stützen

**Gegenfall / Grenze:** Nicht jeder Downbeat schließt eine Phrase.

## RULE-V4-042 – Modaler Ruhepunkt

**Typ:** `tendency` · **Bedingung:** D dorian with Dm-G

**Aussage:** D kann als Zentrum gehört werden

**Gegenfall / Grenze:** gleiche Sammlungstöne können andere Tonalität tragen.

## RULE-V4-043 – Basslinie abwärts

**Typ:** `tendency` · **Bedingung:** C–G/B–Am–C/G

**Aussage:** C–B–A–G kann strukturelle Kohäsion stützen

**Gegenfall / Grenze:** Die Akkorde haben nicht alle dieselbe Funktion.

## RULE-V4-044 – Melodieton bei Reharmonisierung

**Typ:** `tendency` · **Bedingung:** Melodie E über Cmaj7→Am9

**Aussage:** E bleibt in beiden Akkorden vertretbar

**Gegenfall / Grenze:** Aus Akkordton-Vorkommen folgt nicht musikalische Qualität.

## RULE-V4-045 – Chromatische Medianten

**Typ:** `tendency` · **Bedingung:** C–Ab

**Aussage:** Gemeinsamer Ton C und kleine Stimmenbewegungen können Verbindung erklären

**Gegenfall / Grenze:** Funktionsanalyse ist nicht automatisch ausgeschlossen.

## RULE-V4-046 – Axis zwei Tonalitäten

**Typ:** `interpretation` · **Bedingung:** Am–F–C–G

**Aussage:** vi–IV–I–V in C oder i–bVI–bIII–bVII in A

**Gegenfall / Grenze:** Melodie und Form müssen Entscheidung stützen.

## RULE-V4-047 – Blues I7

**Typ:** `interpretation` · **Bedingung:** C blues; C7

**Aussage:** I7 kann tonikaler Bluesklang sein

**Gegenfall / Grenze:** Klassisches V7/IV kann in anderem Kontext sinnvoll sein.

## RULE-V4-048 – Plateau Loop

**Typ:** `interpretation` · **Bedingung:** F–G–Am under C context

**Aussage:** IV–V–vi als potenziell tonikal ambiguose Schleife

**Gegenfall / Grenze:** Nicht jede identische Akkordreihenfolge erzeugt Hybrid-Tonicity.

## RULE-V4-049 – Nichtfunktionale Medianten

**Typ:** `interpretation` · **Bedingung:** C–Ab–E–C

**Aussage:** Gemeinsame Töne/Stimmführung vor dominanter Deutung

**Gegenfall / Grenze:** Andere Linsen sind je Kontext möglich.

## RULE-V4-050 – Harmonic Rhythm

**Typ:** `interpretation` · **Bedingung:** same chords, different durations

**Aussage:** Unterschiedliche Wechselfrequenzen verändern formale Interpretation

**Gegenfall / Grenze:** Keine lineare universelle Spannungsmetrik.

## RULE-V4-051 – Cadence requires phrase

**Typ:** `interpretation` · **Bedingung:** isolated G7→C

**Aussage:** nur potenzielles Kadenzfragment

**Gegenfall / Grenze:** Ohne Metrik, Melodie und Form keine PAC-Zusage.

## RULE-V4-052 – Motividentität

**Typ:** `heuristic` · **Bedingung:** variierte Motivfolge

**Aussage:** Rhythmus oder Kontur bewusst stabil halten

**Gegenfall / Grenze:** Originalität und Erkennbarkeit sind nicht mechanisch garantiert.

## RULE-V4-053 – Kompositorischer Kontrast

**Typ:** `heuristic` · **Bedingung:** second section

**Aussage:** einen Hauptparameter ändern und hören

**Gegenfall / Grenze:** Mehr gleichzeitige Änderungen können künstlerisch beabsichtigt sein.

## RULE-V4-054 – Orchestration-Pass

**Typ:** `heuristic` · **Bedingung:** instrument role assignment

**Aussage:** Leitstimme, Bass und Dichte getrennt überprüfen

**Gegenfall / Grenze:** Instrumentenbereich braucht spezielle validierte Referenz.

## RULE-V4-055 – Voice-Leading-Ranking

**Typ:** `heuristic` · **Bedingung:** voiced chords

**Aussage:** Stimmenbewegung als ein Kriterium unter mehreren

**Gegenfall / Grenze:** Minimal movement != best music.

## RULE-V4-056 – Quellenauswahl

**Typ:** `heuristic` · **Bedingung:** open source learning content

**Aussage:** offene Texte für Paraphrasen und Beispiele bevorzugen

**Gegenfall / Grenze:** CC BY-SA darf nicht unbesehen mit proprietärem Lizenzcode zusammenfließen.

## RULE-V4-057 – Composing review

**Typ:** `heuristic` · **Bedingung:** 16-bar etude

**Aussage:** Motiv, Form, Schluss, Register und Aufführbarkeit hören

**Gegenfall / Grenze:** Auto-Checks belegen nur Datenintegrität.

## RULE-V4-058 – Korpusstatistik

**Typ:** `heuristic` · **Bedingung:** dataset-backed query

**Aussage:** Nenner, Filter, Stil und Version ausgeben

**Gegenfall / Grenze:** Kein frei erfundener Popularity Score.

## RULE-V4-059 – Cultural system boundary

**Typ:** `heuristic` · **Bedingung:** raga/maqam etc

**Aussage:** als tradition-specific model mit Expertenreview führen

**Gegenfall / Grenze:** Keine Reduktion zu westlichen Dur/Moll-Stufen.

