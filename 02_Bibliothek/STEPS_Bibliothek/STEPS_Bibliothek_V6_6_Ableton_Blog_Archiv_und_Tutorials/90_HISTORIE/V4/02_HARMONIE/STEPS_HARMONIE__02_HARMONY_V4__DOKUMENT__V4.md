# STEPS V4 – Fachband: Harmony

**Version:** 4.0.0-research-draft · **Status:** wissenschaftlich orientierte Redaktionsfassung; Quellenfamilien sind keine geprüften Seitenzitate.

Dieser Band ist als ausbaubare Fachgrundlage gedacht, nicht als vermeintlich endgültige Universaltheorie. Jedes Modul enthält ein eigenständiges, für STEPS formuliertes Beispiel, eine konkrete fachliche Grenze und einen Software-/Codex-Übertragungsauftrag.

## RESEARCH-V4-009 – Funktion, Stufe und Bass unterscheiden

Die Stufenbezeichnung benennt einen Akkord relativ zu einem tonalen Kontext, während Funktion eine interpretierte Rolle im Satzverlauf darstellt. Ein IV-Akkord kann prädominant auftreten, einen eigenen Ruhepunkt stützen oder in Pop-Loops metrisch tonikal wirken. Grundton, notierter Bass und harmonische Funktion sind daher drei voneinander zu trennende Dimensionen.

**Eigenes Arbeitsbeispiel:** F–G7–C in C kann IV–V7–I sein; ein wiederholtes F–C über F-Pedal kann andere Zentrierung nahelegen.

**Wichtige Grenze / Gegenfall:** Aus isolierten Akkordsymbolen lässt sich Funktion nicht eindeutig beweisen.

**Konkrete Anforderungen an Codex:** Gib roman_candidates[], function_candidates[], bass_line[] und confidence_rationale aus.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-009, EXT-V4-019; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-010 – Kadenz und formale Schlusswirkung

Eine Kadenz ist nicht einfach die aufeinanderfolgende Nennung zweier Akkordsymbole, sondern ein musikalisch formulierter Schluss mit metrischer, melodischer, stimmführungstechnischer und formaler Einbindung. Eine Dominante-Tonika-Verbindung mitten im Takt ohne phrasalen Abschluss ist nicht zwingend eine authentische Kadenz. In klassischem Instrumentalsatz beeinflussen Sopran- und Basslage die Klassifikation.

**Eigenes Arbeitsbeispiel:** G7→C auf starker Zählzeit mit Sopran D→C und Bass G→C kann ein starkes Schlussmodell bilden.

**Wichtige Grenze / Gegenfall:** Nicht jede V–I-Folge PAC nennen; Inversion, Melodie, Metrum und Kontext prüfen.

**Konkrete Anforderungen an Codex:** Erzeuge CadenceEvent als Kontextobjekt statt Regex auf zwei Chord Labels.

**Weiterführende Quellenfamilien:** EXT-V4-008, EXT-V4-003; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-011 – Sekundärdominante als gerichtete Tonikalisierung

Eine Zwischendominante ist funktional relativ zu einem zeitweiligen Ziel zu verstehen, nicht bloß als chromatischer Nicht-Diatonik-Akkord. Die Schreibweise V7/ii bezeichnet einen Akkord, der die ii-Stufe anvisiert; seine übliche Auflösung ist eine Tendenz, keine notwendige Vorbedingung. Wiederholte oder strukturelle Verschiebung kann eine echte Modulation begünstigen, aber die Grenze hängt vom Satzkontext ab.

**Eigenes Arbeitsbeispiel:** In C-Dur: A7→Dm, zu deuten als V7/ii→ii; die chromatische Terz C# zielt nach D.

**Wichtige Grenze / Gegenfall:** Ein unaufgelöstes A7 in einem Pop-Loop ist nicht zwangsläufig funktional V/ii.

**Konkrete Anforderungen an Codex:** RuleType=tendency, target_degree=ii, observed_resolution separat.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-021; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-012 – Zwischenleittonakkord und chromatische Annäherung

Ein verminderter Septakkord kann die Leittonfunktion eines lokalen Ziels verstärken und verschiedene enharmonische Deutungen erlauben. Der gleiche gleichstufige Tonvorrat kann vor mehreren Zielen auftreten; seine Schreibweise und tatsächlichen Stimmenbewegungen müssen deshalb dokumentiert werden. Die klangliche Symmetrie ersetzt nicht die Analyse von Leitbewegungen.

**Eigenes Arbeitsbeispiel:** In C-Dur: C#°7→Dm als vii°7/ii→ii; die konkrete enharmonische Notation muss vier Akkordtöne korrekt angeben.

**Wichtige Grenze / Gegenfall:** Vier gleichabständige Pitch Classes begründen nicht automatisch die gelesene Funktion.

**Konkrete Anforderungen an Codex:** Stelle enhanced_diminished_spellings als Kandidaten mit lokalem Ziel bereit.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-021; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-013 – Modal Interchange mit expliziter Herkunft

Ein geborgter Akkord stammt aus einem auf denselben tonalen Mittelpunkt bezogenen anderen Modus oder Tongeschlecht, sofern diese Interpretation im Kontext sinnvoll ist. Das verwechselt sich leicht mit chromatischer Mediantenbeziehung, tonicization oder fremdem modalen Schwerpunkt. Die Herkunft einer Borrowed-Chord-Deutung sollte als Hypothese und nicht als ontologischer Wahrheitsstempel gespeichert werden.

**Eigenes Arbeitsbeispiel:** C–Fm–C: Fm als iv aus C-Moll, mit Ab als charakteristischer Farbe; Ab→G mögliche Halbtontendenz.

**Wichtige Grenze / Gegenfall:** Der gleiche Akkord kann auch als reine Stimmführungsfarbe ohne modale Herkunft verstanden werden.

**Konkrete Anforderungen an Codex:** Speichere donor_mode_candidate und voiceleading_evidence, nicht nur borrowed=true.

**Weiterführende Quellenfamilien:** EXT-V4-001; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-014 – Blues und das tonikale Dominantseptimmodell

In vielen Bluesformen erscheint der I7-Akkord als Grundklang; er muss nicht als angewandte Dominante zum IV-Akkord aufgelöst werden. Die Bluesharmonik verbindet Formschema, melodische Blue-Note-Praxis, rhythmische Phrasierung und Klangfarbe, die ein ausschließlich klassisch-funktionaler Parser nicht abbilden kann. Varianten von acht, zwölf oder sechzehn Takten benötigen separate Formkontexte.

**Eigenes Arbeitsbeispiel:** C7–F7–C7–G7–F7–C7 als schematische Bluesfunktion; Details ergeben erst die Taktstruktur.

**Wichtige Grenze / Gegenfall:** Blues-Praxis ist keine homogene Liste starrer 'klassischer' Kadenzen.

**Konkrete Anforderungen an Codex:** Führe blues_form, tonic_seventh_role und performance_features als getrennte Entitäten.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-002; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-015 – Jazz II–V–I und Guide Tones

Im tonalen Jazz bildet ii–V–I eine häufige zielgerichtete Folge, die durch Sekundärdominantenketten, tritonische Substitutionen, Backdoor-Bewegungen und Alterationen erweitert werden kann. Stimmführung zwischen Terzen und Septimen liefert ein anderes Erklärungsmodell als reine Grundtonabstände. Extensions können melodisch oder harmonisch gezielt eingesetzt werden, aber sind nicht per se zwingender Bestandteil jedes Voicings.

**Eigenes Arbeitsbeispiel:** Dm7–G7–Cmaj7: F und C in Dm7, B und F in G7, E und B in Cmaj7 als ausgewählte Stimmführungsziele.

**Wichtige Grenze / Gegenfall:** 'Jeder jazzige Akkord muss eine 9 haben' ist kein musiktheoretisches Gesetz.

**Konkrete Anforderungen an Codex:** Modelliere chord_function und guide_tone_voiceleading getrennt von optionalen voicing choices.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-026; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-016 – Tritonussubstitution als mehrere Linsen

Eine dominante Tritonusverwandtschaft kann über gleiche Guide-Tone-Pitch-Classes erklärt werden, obwohl die Bassbewegung und der konkrete akkordische Tonvorrat anders wirken. Bei G7→C kann Db7→C als chromatische Annäherung fungieren; die Gleichsetzung ist nicht vollständig, denn Grundton, Skalenoptionen und Stimmführung unterscheiden sich. Eine Harmoniebibliothek muss daher 'verwandt' und 'identisch' trennen.

**Eigenes Arbeitsbeispiel:** G7: G B D F; Db7: Db F Ab Cb, mit Cb enharmonisch B; beide teilen F/B als Pitch Classes.

**Wichtige Grenze / Gegenfall:** Die Auswechslung braucht stilistischen und melodischen Kontext, nicht nur den Tritonus-Abstand.

**Konkrete Anforderungen an Codex:** Expose shared_guide_tone_classes und semitone_bass_approach als Begründungsachsen.

**Weiterführende Quellenfamilien:** EXT-V4-001; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-017 – Chromatische Medianten und Stimmführung

Große oder kleine Dreiklänge mit mediantischer Grundtonrelation können bei unterschiedlichem diatonischem Bezug durch gemeinsame Töne und kleine Stimmenbewegungen verbunden sein. Diese Beziehungen sind oft analytisch ergiebiger als eine erzwungene dominantische Funktion. Ein Transformationsmodell sollte aber die genaue Relation je Paar benennen und nicht sämtliche chromatischen Akkorde in eine Familie werfen.

**Eigenes Arbeitsbeispiel:** C-Dur C–E–G und Ab-Dur Ab–C–Eb teilen C; E→Eb und G→Ab sind Halbtonbewegungen.

**Wichtige Grenze / Gegenfall:** Nicht jeder Terzschritt ist chromatisch und nicht jede ähnliche Stimmführung erfordert Neo-Riemannian Interpretation.

**Konkrete Anforderungen an Codex:** Speichere common_tones, semitone_moves und referential_key separat.

**Weiterführende Quellenfamilien:** EXT-V4-016, EXT-V4-017; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-018 – Neo-Riemannsche P/L/R Transformationen

P, L und R sind wohldefinierte Beziehungen zwischen Dur- und Molldreiklängen unter einer gemeinsamen Transformationskonvention. P verändert die Terz chromatisch bei festem Grundton und Quinte; L bewahrt zwei Töne und bewegt einen Ton halbtonweise; R verbindet relative Dur- und Molldreiklänge über zwei gemeinsame Töne. In einer kompositorischen Umgebung sind diese Funktionen Beziehungskarten, keine automatische Erklärung für metrische Form oder Tonika.

**Eigenes Arbeitsbeispiel:** C major→C minor (P), C major→E minor (L), C major→A minor (R).

**Wichtige Grenze / Gegenfall:** Die Operationen auf Septakkorde oder mikrotonale Pitch Sets sind nicht automatisch definiert.

**Konkrete Anforderungen an Codex:** Representiere triad_quality und reversible_operation statt universeller Chord Regex.

**Weiterführende Quellenfamilien:** EXT-V4-016, EXT-V4-018; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-019 – Pop-Axis und Tonikamehrdeutigkeit

Eine vi–IV–I–V-Folge in C-Dur ist klanglich identisch mit i–bVI–bIII–bVII bei A-äolischem Zentrum; die Stufenbezeichnung ist an eine interpretierte Tonika gekoppelt. Melodie, Beginnposition, Phrasenende und formale Wiederholung beeinflussen die Tonikazuschreibung. Für STEPS sollte deshalb eine Progression Kandidaten mitsamt Begründung tragen und beim Anhören des gleichen Materials unterschiedliche Analysesichten erlauben.

**Eigenes Arbeitsbeispiel:** Am–F–C–G: C-Ionisch vi–IV–I–V; A-Äolisch i–bVI–bIII–bVII.

**Wichtige Grenze / Gegenfall:** Keine Tonikawahl allein aus dem ersten Akkord erzwingen.

**Konkrete Anforderungen an Codex:** Gib alternative_tonal_centers[] und evidentiary_factors[] aus.

**Weiterführende Quellenfamilien:** EXT-V4-019; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-020 – Plateau-Loops und rhetorische Tonika

Bestimmte IV–V–vi-Loops erzeugen funktionale Räume, in denen Tonika nicht immer als harmonisches I tatsächlich erscheint. In den untersuchten Popkontexten kann eine rhetorische Tonikafunktion auf IV oder vi liegen; melodische Tonstufen, metrische Platzierung und größere Form sind dafür entscheidend. Das widerspricht der Vereinfachung, die harmonische Stufe alleine bestimme ihre Funktion.

**Eigenes Arbeitsbeispiel:** F–G–Am bei angenommenem C-Dur kann als IV–V–vi fungieren, ohne C-Dur als Akkord zu präsentieren.

**Wichtige Grenze / Gegenfall:** Ein Plateau-Loop ist keine unstrittige Funktionsetikette für jedes Vorkommen dieser drei Akkorde.

**Konkrete Anforderungen an Codex:** Stelle global_tonic, actual_tonic_presence und rhetorical_tonic_candidate nebeneinander.

**Weiterführende Quellenfamilien:** EXT-V4-020, EXT-V4-005; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-021 – Posttonale Set-Theory und Klangorganisation

Ein Pitch-Class-Set fasst Töne modulo Oktavlage zusammen und kann Transpositions- und Inversionsverwandtschaften aufdecken. Damit sind weder ein realer Akkordklang noch eine Voicing-Lösung vollständig repräsentiert: Register, Reihenfolge, Dauer und klangliche Ausgestaltung fehlen. In einem Kompositionstool kann die Set-Ebene Materialfamilien erzeugen, muss aber mit Event- und Registerebene verbunden werden.

**Eigenes Arbeitsbeispiel:** {0,1,4} und seine Transpositionen teilen die gleiche Intervallstruktur, können aber in anderen Lagen verschieden klingen.

**Wichtige Grenze / Gegenfall:** Pitch-Class-Set-Gleichheit ist nicht Gleichheit von Klang, Form oder Bedeutung.

**Konkrete Anforderungen an Codex:** Implementiere pc_set_family getrennt von ordered_pitch_events.

**Weiterführende Quellenfamilien:** EXT-V4-018; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.


**Modulzahl dieses Bandes:** 13. Historisches V3-Material ist zusätzlich in `00_HISTORISCH_V3/` enthalten.
