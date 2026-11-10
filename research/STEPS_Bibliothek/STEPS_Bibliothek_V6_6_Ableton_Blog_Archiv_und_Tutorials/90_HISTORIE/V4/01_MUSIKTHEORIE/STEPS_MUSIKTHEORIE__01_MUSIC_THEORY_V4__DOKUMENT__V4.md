# STEPS V4 – Fachband: Music Theory

**Version:** 4.0.0-research-draft · **Status:** wissenschaftlich orientierte Redaktionsfassung; Quellenfamilien sind keine geprüften Seitenzitate.

Dieser Band ist als ausbaubare Fachgrundlage gedacht, nicht als vermeintlich endgültige Universaltheorie. Jedes Modul enthält ein eigenständiges, für STEPS formuliertes Beispiel, eine konkrete fachliche Grenze und einen Software-/Codex-Übertragungsauftrag.

## RESEARCH-V4-001 – Tonhöhen, Oktaven und Schreibung

Die wahrgenommene Tonhöhe ist nicht mit der Frequenz einer einzelnen Sinuskomponente gleichzusetzen. In gleichstufiger Stimmung teilen oktavverwandte Töne dieselbe Pitch Class, während ihre Registerlage für Wahrnehmung, Stimmführung und Orchestration wesentlich bleibt. Schreibung ist ein zusätzlicher semantischer Layer: F# und Gb können im 12-TET denselben MIDI-Pitch repräsentieren, aber unterschiedliche Skalenstufen und Auflösungsrichtungen bedeuten.

**Eigenes Arbeitsbeispiel:** C#4 und Db4 sind 12-TET-äquivalent; als Leitton nach D ist C# analytisch plausibler.

**Wichtige Grenze / Gegenfall:** Nicht auf mikrotonale Stimmungen oder bloße Audiofrequenzen als universellen Schlüssel abbilden.

**Konkrete Anforderungen an Codex:** Speichere sounding_pitch, spelled_pitch, tuning_system und tonal_context getrennt; baue Kollisionstests für Enharmonik.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-026; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-002 – Intervallqualität und Vorzeichen

Intervallzahlen ergeben sich aus den Buchstabenabständen inklusive beider Endpunkte; die Qualität hängt von chromatischer Halbtonzahl und diatonischer Referenz ab. Deshalb ist C–F# eine übermäßige Quarte und C–Gb eine verminderte Quinte, obwohl beide im 12-TET sechs Halbtöne umfassen. Für korrekte musiktheoretische Rückmeldung müssen generische und chromatische Distanz gleichzeitig erhalten bleiben.

**Eigenes Arbeitsbeispiel:** C→F# = A4, C→Gb = d5; die Stimmführung in unterschiedlicher Satzumgebung trennt ihre Aufgaben.

**Wichtige Grenze / Gegenfall:** Pitch-Class-Distanz allein kann Intervallnamen nicht bestimmen.

**Konkrete Anforderungen an Codex:** Implementiere spelled_interval als eigenes Objekt mit diatonic_number, chromatic_semitones, quality.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-030; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-003 – Temperamente und Mikrotonalität

Zwölfstufige Gleichstufigkeit ermöglicht einfaches Transponieren und enharmonische Gleichsetzung in Standard-MIDI, ist aber weder geschichtliche Norm für alle Epochen noch universelles Hör- oder Kompositionssystem. Reine Stimmung orientiert Teilintervalle an Frequenzverhältnissen und kann je nach Tonzentrum andere Werte liefern. Mikrotonale Musik erfordert explizite Skalen- und Intonationsmodelle statt heimlicher Rundung auf zwölf Pitch Classes.

**Eigenes Arbeitsbeispiel:** Reine große Terz 5:4 unterscheidet sich von der 12-TET-Terz mit vier gleichstufigen Halbtönen.

**Wichtige Grenze / Gegenfall:** Aus einfachen Zahlenverhältnissen folgt keine universelle ästhetische Rangordnung.

**Konkrete Anforderungen an Codex:** Versioniere tuning_id, cent_offset, reference_frequency, temperament_metadata und render_policy getrennt.

**Weiterführende Quellenfamilien:** EXT-V4-001; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-004 – Rhythmus versus Metrum

Rhythmus beschreibt konkrete Ereignisabstände und Dauern; Metrum ist eine hierarchische, wahrnehmungsabhängige Erwartungsordnung über die Zeit. Eine Betonung auf einer schwachen Zählzeit kann dieselbe notierte Note in einer anderen metrischen Umgebung anders wirken lassen. Rubato verändert Zeitabstände, ohne notwendigerweise die Identität des wahrgenommenen Takts zu beseitigen.

**Eigenes Arbeitsbeispiel:** Notiere vier Viertel gleichmäßig; verschiebe den zweiten Akzent auf die Und von 2 und vergleiche wahrgenommene Synkope.

**Wichtige Grenze / Gegenfall:** Akkorddauer und musikalische Betonung dürfen nicht allein aus der Taktstrichposition abgeleitet werden.

**Konkrete Anforderungen an Codex:** Speichere event_onset, notated_duration, beat_strength, meter_hypothesis und expressive_timing separat.

**Weiterführende Quellenfamilien:** EXT-V4-015, EXT-V4-029; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-005 – Skalen als geordnete Stufenstruktur

Ein Modus ist mehr als die unsortierte Menge von Pitch Classes: Grundtonbezug, Stufenfunktionen, charakteristische Töne und melodische Bewegung sind für den Höreindruck relevant. A-Dorisch und G-Dur besitzen dieselben Töne, aber nicht denselben modalen Schwerpunkt. Bei der Generierung ist entscheidend, welche Tonstufen als Ruhepunkt, Reibung oder Leitbewegung inszeniert werden.

**Eigenes Arbeitsbeispiel:** A-Dorian = A B C D E F# G; ein A-moll-Zentrum mit F# als charakteristische großer Sexte.

**Wichtige Grenze / Gegenfall:** Gleiche Tonmenge beweist keine gleiche Tonalität oder Funktion.

**Konkrete Anforderungen an Codex:** Trenne pitch_collection, mode_final, melodic_emphasis und cadence_strategy.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-030; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-006 – Tonleitern und diatonische Schreibweise

Eine diatonische Durtonleiter benutzt jeden der sieben Stammtonbuchstaben genau einmal und ordnet Ganztöne und Halbtöne nach einem definierten Muster an. Eine rechnerisch korrekte Pitch-Class-Ausgabe kann in der Notation unbrauchbar sein, wenn sie enharmonisch falsch geschrieben wird. Bei komplexeren Tonarten sind auch Doppelvorzeichen möglich; eine Anwendung darf sie nicht willkürlich durch bequemere Buchstaben ersetzen.

**Eigenes Arbeitsbeispiel:** F#-Dur: F# G# A# B C# D# E# F#; E# nicht F.

**Wichtige Grenze / Gegenfall:** Andere Notationssysteme brauchen eigene Konventionen; 12-TET-Audiogleichheit ersetzt keine theoretische Schreibweise.

**Konkrete Anforderungen an Codex:** Implementiere diatonic_letter_cycle und accidentals als getrennte Operationen.

**Weiterführende Quellenfamilien:** EXT-V4-001; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-007 – Akkordsymbole als Mehrdeutigkeitsschnittstelle

Ein Akkordsymbol beschreibt in der Regel einen Tonvorrat oder Voicing-Zielraum, aber nicht automatisch Akkordfunktion, Lage, Instrumentation oder rhythmische Umsetzung. Cmaj9, Cadd9, C9 und C7b9 unterscheiden sich in ihrer Septime und in ihrer Bedeutung. Slash-Akkorde beschreiben oft einen Bass, nicht zwingend eine Inversion eines klassischen tertiären Akkords.

**Eigenes Arbeitsbeispiel:** Cadd9: C E G D; Cmaj9: C E G B D; C9: C E G Bb D.

**Wichtige Grenze / Gegenfall:** Hersteller-Chord-Syntax kann Akkordsuffixe anders interpretieren; Parser benötigen Dialektangabe.

**Konkrete Anforderungen an Codex:** Erzeuge ChordSymbol AST mit root, quality, seventh, extensions, alterations, bass und spelling.

**Weiterführende Quellenfamilien:** EXT-V4-026, EXT-V4-021; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-008 – Konsonanz, Funktion und Kultur

Akustische Rauigkeit, Satzdissonanz und harmonisch-rhetorische Spannung sind nicht identisch. Eine Septime kann als auflösungsbedürftig behandelt, als stiltypischer stabiler Bluesklang genutzt oder in Jazz-Voicings zur Klangfarbe werden. Historische Normen müssen als Stilkonvention modelliert sein, damit eine Software experimentelle oder andere kulturelle Praxis nicht als Fehler klassifiziert.

**Eigenes Arbeitsbeispiel:** C7 in C-Blues kann Tonikaqualität tragen; G7 in C-Dur kann vor C eine dominante Funktion ausbilden.

**Wichtige Grenze / Gegenfall:** Vermeide die binäre Systemmeldung 'dissonant = verboten'.

**Konkrete Anforderungen an Codex:** Definiere getrennte Felder acoustic_roughness, style_dissonance_role und local_function.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-009; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.


**Modulzahl dieses Bandes:** 8. Historisches V3-Material ist zusätzlich in `00_HISTORISCH_V3/` enthalten.
