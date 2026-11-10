# STEPS V4 – Fachband: Composing

**Version:** 4.0.0-research-draft · **Status:** wissenschaftlich orientierte Redaktionsfassung; Quellenfamilien sind keine geprüften Seitenzitate.

Dieser Band ist als ausbaubare Fachgrundlage gedacht, nicht als vermeintlich endgültige Universaltheorie. Jedes Modul enthält ein eigenständiges, für STEPS formuliertes Beispiel, eine konkrete fachliche Grenze und einen Software-/Codex-Übertragungsauftrag.

## RESEARCH-V4-028 – Kompositionsbrief und bewusste Constraints

Komponieren beginnt mit einer Entscheidung über Ziel und Material, nicht zwangsläufig mit Akkorden. Eine kurze Szenenmusik, ein achtaktiges Klavierstück und ein Pop-Refrain besitzen verschiedene Anforderungen an Dauer, Energie, Instrumentation, formalen Kontrast und Wiedererkennbarkeit. Ein dokumentierter Brief erleichtert das spätere Revidieren: Welche Eigenschaft soll wiederkehren? Was darf sich verändern? Woran wird ein Entwurf hörend überprüft?

**Eigenes Arbeitsbeispiel:** Brief: 16 Takte, C-Dorisch, zwei kontrastierende Vierviertelphrasen, nur drei harmonische Zentren, Flöte und Klavier.

**Wichtige Grenze / Gegenfall:** Ein Brief ist kreatives Werkzeug, nicht eine wissenschaftliche Formel für gute Musik.

**Konkrete Anforderungen an Codex:** Objekt CompositionBrief mit goal, duration, audience, ensemble, motifs, invariants, review_criteria.

**Weiterführende Quellenfamilien:** EXT-V4-006, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-029 – Motiv als wiedererkennbare Gestalt

Ein Motiv kann durch Intervallkontur, Rhythmus, metrische Position, Artikulation oder Klangfarbe charakterisiert sein. Es ist nicht notwendig, dass alle Eigenschaften bei einer Wiederkehr identisch bleiben. Entscheidend ist vielmehr, welche Dimensionen als Identitätsträger dienen und durch Variation bewusst in den Vordergrund treten. Das erlaubt gezielte Entwicklung statt bloß neuer Tonfolgen.

**Eigenes Arbeitsbeispiel:** Motiv A: C4 Viertel, D4 Achtel, E4 Achtel, G4 Halbe; Variation: G4 Viertel, A4 Achtel, B4 Achtel, D5 Halbe.

**Wichtige Grenze / Gegenfall:** Beliebige Transposition erhält Kontur, kann Register und Spannung aber verändern.

**Konkrete Anforderungen an Codex:** Speichere rhythm_signature, interval_vector, accent_map, transformations und source_object.

**Weiterführende Quellenfamilien:** EXT-V4-006, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-030 – Variation, Wiederholung und Kontrast

Wiederholung stabilisiert musikalische Erwartung, Variation erzeugt Fortgang und Kontrast erlaubt größere formale Unterscheidung. Ein kontinuierlicher Wechsel sämtlicher Parameter erschwert die Wiedererkennbarkeit; eine endlose identische Wiederholung ohne Textur- oder Harmoniebewegung kann Stillstand erzeugen, sofern dies nicht bewusst gewollt ist. Praktisch sollte pro Wiederkehr ein Hauptparameter geändert und dessen Wirkung angehört werden.

**Eigenes Arbeitsbeispiel:** Takten 1–2 Motiv A; 3–4 transponiertes A; 5–6 fragmentiertes A mit Verdichtung; 7–8 cadenzielle Abrundung.

**Wichtige Grenze / Gegenfall:** Kein starres Verhältnis 'zwei Wiederholungen sind richtig'; Stil und Form zählen.

**Konkrete Anforderungen an Codex:** Dokumentiere transformation lineage und phrase_position.

**Weiterführende Quellenfamilien:** EXT-V4-007, EXT-V4-008; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-031 – Satzmodell und Fortsetzung

In der klassisch orientierten Formtheorie ist die Satzstruktur häufig als Präsentation, Fortsetzung und Abschluss beschreibbar. Eine Präsentation stellt und bestätigt eine Grundidee, während die Fortsetzung durch Fragmentierung, Sequenz und rhythmische Verdichtung auf einen Schluss hinwirken kann. Das ist ein historisch und repertorial begrenztes Analyse- und Kompositionsschema, keine generische Formel für alle Pop-Songs.

**Eigenes Arbeitsbeispiel:** Takte 1–2 Grundidee; 3–4 Wiederholung; 5–6 Fragment/Sequenz; 7–8 Dominantvorbereitung und Zielton.

**Wichtige Grenze / Gegenfall:** Acht Takte allein beweisen keine Satzstruktur; harmonische und motivische Aufgaben prüfen.

**Konkrete Anforderungen an Codex:** CompositionGraph nodes presentation, continuation, cadence with evidence notes.

**Weiterführende Quellenfamilien:** EXT-V4-008, EXT-V4-004; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-032 – Periode und Kadenzhierarchie

Eine klassische Periode kontrastiert eine eröffnende mit einer beantwortenden Phrase, wobei die zweite typischerweise stärker schließt. Die melodische Ähnlichkeit der Phrasen und unterschiedliche Kadenzstärke sind diagnostisch wichtig; zwei gleichlange Blöcke sind nicht automatisch eine Periode. In der Praxis kann ein Komponist dieses Modell variieren, indem er den melodischen Beginn wiedererkennen lässt und den Schluss verändert.

**Eigenes Arbeitsbeispiel:** Antezedens: C–F–G (Halbschluss); Konsequens: C–Dm–G7–C mit deutlicherer Tonikawirkung.

**Wichtige Grenze / Gegenfall:** Ein Akkordschema ohne realisierte Melodie und Metrik belegt keine perfekte authentische Kadenz.

**Konkrete Anforderungen an Codex:** Speichere phrase_pairs, shared_motif, cadence_strength_annotation und metrical_boundary.

**Weiterführende Quellenfamilien:** EXT-V4-004, EXT-V4-008; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-033 – Melodie vom Akkord lösen

Eine Melodie ist nicht bloß die nacheinander abgefragte Folge von Akkordtönen. Durchgänge, Vorhalte, Wechselnoten und expressive Spannung brauchen metrische Lage und Auflösung; ihre Wirkung ergibt sich aus einer zeitlichen Linie. Ein motivischer Entwurf sollte zuerst gesungen oder gespielt und dann in mehreren harmonischen Umgebungen getestet werden, statt für jeden Ton einen neuen Akkord zu erzwingen.

**Eigenes Arbeitsbeispiel:** C4–D4–E4 über Cmaj7: D als neunte Farbe oder Durchgang; E als Zielton der Bewegung.

**Wichtige Grenze / Gegenfall:** Eine 'falsche Note' kann ein gewollter Vorhalt sein; UI benötigt Kontext statt roter Fehlermeldung.

**Konkrete Anforderungen an Codex:** Separate MelodyEvent von HarmonyEvent; add non_chord_tone_analysis_candidates.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-034 – Bass als zweite Kompositionsachse

Der Bass kann Harmonie stabilisieren, eine gemeinsame Pedaltonbasis bilden oder durch chromatische Linie einen Zusammenhang schaffen, der in Akkordsymbolen wenig sichtbar ist. Ein Bass-first-Entwurf hilft, große Formbewegungen zu planen, bevor Voicing und Melodie konkretisiert werden. Slash-Chords müssen dabei als tatsächliche Klangereignisse und nicht nur als Symboltricks behandelt werden.

**Eigenes Arbeitsbeispiel:** Bass C–B–A–G unter C–G/B–Am–C/G; absteigende Linie trägt die Phrase.

**Wichtige Grenze / Gegenfall:** Ein gewollter Pedalton muss nicht Grundton jedes darüber klingenden Akkords sein.

**Konkrete Anforderungen an Codex:** Create BassLineEvent with bass_pitch, register, rhythmic_position and harmonic_interpretation.

**Weiterführende Quellenfamilien:** EXT-V4-007, EXT-V4-026; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-035 – Kontrapunkt als eigenständige Stimmenlogik

Zweistimmiger Kontrapunkt ist mehr als die Verteilung eines Akkords auf zwei Melodien. Jede Stimme soll eine nachvollziehbare eigene Kontur besitzen, während die gemeinsamen Intervalle stilistisch kontrolliert werden. In einer Species-Übung gelten strengere Regeln als im freien Film-/Pop-Arrangement. Eine App muss zwischen Übungssystem und allgemeinem Kompositionswerkzeug wählen können.

**Eigenes Arbeitsbeispiel:** Cantus C4–D4–E4–D4–C4; Kontrapunkt verlangt gezielte Konsonanzprüfung an den strukturellen Zählzeiten.

**Wichtige Grenze / Gegenfall:** Keine Species-Parallelverbot-Regeln als universelles Gesetz für Pop-Pads anwenden.

**Konkrete Anforderungen an Codex:** Separate contrapuntal_style_contract, independence_features und dissonance_treatment.

**Weiterführende Quellenfamilien:** EXT-V4-030, EXT-V4-001; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-036 – Instrumentation und Arrangement

Instrumentierung betrifft nicht nur die Auswahl von Timbres, sondern Register, Spielbarkeit, Dichte, Artikulation und die Rollenverteilung. Wenn Flöte und Klavier eine Melodie verdoppeln, kann dies die Hörbarkeit ändern, ohne Akkordfunktion zu verändern. Ein Arrangement sollte mehrere Zustände derselben Komposition erlauben: Solo, Duo, kleines Ensemble, Pad/Textur. Konkrete Besetzungsregeln brauchen instrumentenspezifische Quellen und realistische Tonumfänge.

**Eigenes Arbeitsbeispiel:** Eine Linie E4–G4–A4 in Flöte und Violine kann in anderem Register anders projiziert werden.

**Wichtige Grenze / Gegenfall:** Keine pauschalen Registergrenzen ohne Instrument, Technikstand und Transposition fest behaupten.

**Konkrete Anforderungen an Codex:** Define voice_role, playable_range_ref, transposition, articulation, density and balance.

**Weiterführende Quellenfamilien:** EXT-V4-007, EXT-V4-006; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-037 – Form als Entwicklung von Erwartung

Form entsteht durch Wiedererkennung, Variation, Kontrast und Schlusserwartung auf mehreren Zeitskalen. Ein Chorus kann durch stärkere melodische Höhe und dichtere Instrumentation hervortreten, auch wenn seine vier Akkorde bereits in der Strophe verwendet wurden. Klassische Themenform und populäre Songform benötigen jedoch verschiedene Begriffssysteme und Prüfkriterien.

**Eigenes Arbeitsbeispiel:** Verse auf zurückgenommenem Register über Am–F–C–G; Chorus gleiche Schleife, aber größere Tonlage, längere Zielnoten und andere Instrumentierung.

**Wichtige Grenze / Gegenfall:** Ein bloßes SectionLabel 'Chorus' beweist noch keine hörbare Formfunktion.

**Konkrete Anforderungen an Codex:** Expose formal_intent, observed_parameters and listener_test_questions.

**Weiterführende Quellenfamilien:** EXT-V4-009, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-038 – Pop-Songwriting und Textprosodie

Eine Textzeile besitzt Sprachakzente, Silbendauer, semantische Schwerpunkte und Phrasenlänge, die mit Melodierhythmus harmonieren oder bewusst dagegen arbeiten können. Die Refrain-Hook kann sich durch kleine wiedererkennbare rhythmische Motive stärker einprägen als durch große harmonische Vielfalt. Für STEPS sollten Lyrics nicht als reiner Textblock, sondern mit gesungenen Silben-Ereignissen verknüpfbar sein.

**Eigenes Arbeitsbeispiel:** Vier Silben auf einer rhythmischen Zelle können durch Dehnung der letzten Silbe einen Zeilenschluss bilden.

**Wichtige Grenze / Gegenfall:** Akzentmuster sind sprach- und kontextabhängig; nicht jede Abweichung ist ein Fehler.

**Konkrete Anforderungen an Codex:** LyricSyllable onset, stress, note_link, language, phonetic_duration as optional module.

**Weiterführende Quellenfamilien:** EXT-V4-009; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-039 – Leitmotiv und adaptive Medienmusik

Ein Leitmotiv kann bei einer Figur oder Idee wiederkehren, aber seine Registerlage, Instrumentation, Tempo und Harmonik kontextabhängig wechseln. In interaktiver Medienmusik müssen Übergänge zudem auf Spielzustände reagieren; eine lineare achtaktige Komposition reicht dafür oft nicht. Formale Zustandsgraphen, synchronisierte Transitionen und Stinger sind daher andere Objekte als ein Film-Cue.

**Eigenes Arbeitsbeispiel:** Das Intervallmotiv C–Eb–G erklingt in ruhiger C-Moll-Fassung und später schneller über Ab–Bb–Cm.

**Wichtige Grenze / Gegenfall:** Ähnlichkeit zu bekannten Filmscores vermeiden; Stiletikett belegt keine Urheberschaft.

**Konkrete Anforderungen an Codex:** Map motif_id to scene_state, transition_rule and tempo/beat alignment, ohne sofort Game Engine zu bauen.

**Weiterführende Quellenfamilien:** EXT-V4-027, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-040 – Minimalismus und Prozessmusik

Eine Komposition kann eine klare Transformationsregel über längere Zeit hörbar machen, etwa additive Rhythmen, graduelle Tonverschiebungen oder streng begrenzte Pattern-Reihen. Die Regel allein ist noch nicht das fertige Stück; Tempo, Register, Dichte, Dauer und Wahrnehmbarkeit des Prozesses bestimmen die musikalische Form. STEPS sollte kompositorische Prozesse als ausführbare Vorschriften plus dramaturgischen Bogen beschreiben können.

**Eigenes Arbeitsbeispiel:** Start C–D–E Achtelpattern; füge in jeder zweiten Wiederholung einen Ton G an und reduziere später wieder.

**Wichtige Grenze / Gegenfall:** Nicht jede ostinate Wiederholung ist automatisch Minimal Music im historischen Sinn.

**Konkrete Anforderungen an Codex:** CompositionProcess: rule, iterations, tempo, transformation_history, termination_condition.

**Weiterführende Quellenfamilien:** EXT-V4-006; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-041 – Algorithmische Komposition und Validierung

Ein Algorithmus kann harmonische Constraint-Kandidaten erzeugen, aber nicht ohne weiteres Stilverständnis, expressives Timing oder ästhetische Absicht garantieren. Eine robuste Pipeline trennt Hard Constraints von weichen Prioritäten, formale Strukturplanung von konkretem Voicing und nachvollziehbare menschliche Auswahl von statistischer Rangfolge. Jeder Lauf benötigt einen Seed und versionierte Regelparameter, damit Ergebnisse reproduzierbar sind.

**Eigenes Arbeitsbeispiel:** Erzeuge vier Akkorde unter Constraints: tonales Zentrum C, höchstens ein Borrowed Chord, Schluss auf C, Bass ohne Sprung größer als Quinte.

**Wichtige Grenze / Gegenfall:** Ein technisch gültiger Output ist nicht automatisch interessant oder abwechslungsreich.

**Konkrete Anforderungen an Codex:** Protokolliere random_seed, satisfied_constraints, violated_preferences und user_selection.

**Weiterführende Quellenfamilien:** EXT-V4-021, EXT-V4-022; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-042 – Revision durch gezielte Diagnose

Komposition lässt sich mit Diagnosefragen verbessern: Ist das Motiv erkennbar? Kommt die stärkste Änderung zum gewünschten Zeitpunkt? Unterstützt der Bass die Kadenz? Ist die Melodie spielbar und singbar? Gibt es ungewollte Wiederholungen oder übermäßig gleichmäßige Klangdichte? Eine Revision sollte Änderungen einzeln protokollieren, um hörbare Auswirkungen vergleichen zu können.

**Eigenes Arbeitsbeispiel:** Version A: acht Takte mit jedem Akkord einen Takt; Version B: letzte zwei Takte G7 zwei Beats, C sechs Beats und motivische Verlangsamung.

**Wichtige Grenze / Gegenfall:** Keine automatische Schönheitsnote aus einer Summe algorithmischer Teilwerte.

**Konkrete Anforderungen an Codex:** Versionierte CompositionRevision mit rationale, before/after und listener_notes.

**Weiterführende Quellenfamilien:** EXT-V4-006, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.


**Modulzahl dieses Bandes:** 15. Historisches V3-Material ist zusätzlich in `00_HISTORISCH_V3/` enthalten.
