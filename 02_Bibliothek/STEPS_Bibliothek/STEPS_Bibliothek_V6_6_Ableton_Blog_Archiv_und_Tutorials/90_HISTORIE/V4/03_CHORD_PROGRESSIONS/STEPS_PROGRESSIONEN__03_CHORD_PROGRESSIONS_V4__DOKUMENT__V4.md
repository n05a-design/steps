# STEPS V4 – Fachband: Chord Progressions

**Version:** 4.0.0-research-draft · **Status:** wissenschaftlich orientierte Redaktionsfassung; Quellenfamilien sind keine geprüften Seitenzitate.

Dieser Band ist als ausbaubare Fachgrundlage gedacht, nicht als vermeintlich endgültige Universaltheorie. Jedes Modul enthält ein eigenständiges, für STEPS formuliertes Beispiel, eine konkrete fachliche Grenze und einen Software-/Codex-Übertragungsauftrag.

## RESEARCH-V4-022 – Zeitliche Akkordereignisse statt bloßer Strings

Eine Akkordfolge ist ein Zeitobjekt. Wenn Cmaj7 für zwei Takte und G7 für einen halben Takt erklingt, ist dies kompositorisch etwas anderes als eine gleichgewichtige Liste [Cmaj7,G7]. Metrische Position, Phrasenfunktion, Tonzentrum, Melodiepassung, Bass und Voicing müssen als eigenständige Felder modelliert werden. Dadurch können Analyse und Komposition aus derselben Quelle verschiedene Ansichten gewinnen.

**Eigenes Arbeitsbeispiel:** Cmaj7 (8 Viertel) – Dm7 (2 Viertel) – G7 (2 Viertel) – Cmaj7 (4 Viertel).

**Wichtige Grenze / Gegenfall:** Ohne Takt und Tempo darf STEPS keine vermeintlich exakten Spannungsverläufe ausgeben.

**Konkrete Anforderungen an Codex:** JSON Events mit offset, duration, meter, local_context, analysis_candidates, source_claims.

**Weiterführende Quellenfamilien:** EXT-V4-021, EXT-V4-022; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-023 – Harmonischer Rhythmus als Gestaltungsparameter

Die Dichte der Akkordwechsel kann formale Energie erzeugen, ohne dass neue Akkorde benötigt werden. Eine Verdichtung von ganzen Takten zu Halbtakten im Prechorus kann einen Chorus rhetorisch vorbereiten; eine Rückkehr zu längeren Liegezeiten kann Entspannung signalisieren. In Jazz und klassischer Satztechnik sind harmonischer Rhythmus und Phrasenposition auch für Funktionsdeutung wichtig.

**Eigenes Arbeitsbeispiel:** Verse: C je 4 Beats, Am je 4 Beats; Prechorus: Dm 2, G 2, C 4 Beats.

**Wichtige Grenze / Gegenfall:** Ein schneller Wechsel ist nicht automatisch mehr akustische Dissonanz.

**Konkrete Anforderungen an Codex:** Expose harmonic_change_density getrennt von chordal_tension und instrumentation_density.

**Weiterführende Quellenfamilien:** EXT-V4-009, EXT-V4-015; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-024 – Progressionsfamilie und Rotation

Progressions können im loopbasierten Repertoire als zyklische Familien untersucht werden. Eine Rotation der Akkordreihenfolge erhält zwar denselben gerichteten Kreis der Beziehungen, verändert aber Beginn, Schwerpunkt, Kadenzwirkung und möglicherweise die gehörte Tonika. Das ist wichtig für Composition DNA: eine mathematisch einfache Äquivalenz muss nicht musikalisch neutral sein.

**Eigenes Arbeitsbeispiel:** C–G–Am–F versus Am–F–C–G enthalten verwandte Zyklusübergänge, setzen aber andere Auftakte.

**Wichtige Grenze / Gegenfall:** Rotation ≠ identisches Hörerlebnis oder gleiche Funktion.

**Konkrete Anforderungen an Codex:** Representiere loop_class, rotation_index und perceptual_tonic_hypothesis unabhängig.

**Weiterführende Quellenfamilien:** EXT-V4-019, EXT-V4-002; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-025 – Reharmonisierung mit Invarianzvertrag

Eine Reharmonisierung ändert Akkorde unter bestimmten Erhaltungsbedingungen: Melodie, harmonischer Rhythmus, Bass, Tonzentrum oder Kadenzziel können fixiert oder freigegeben sein. Nur unter solchen Grenzen lässt sich eine Transformation sinnvoll vergleichen. STEPS sollte mehrere Antworten erzeugen und für jede angeben, welche Voraussetzung erhalten blieb und welcher Parameter verändert wurde.

**Eigenes Arbeitsbeispiel:** Festes Melodie-E: Cmaj7→Am9→Fmaj7 verändern den harmonischen Kontext, E bleibt Akkordton bzw. farbige große Septime.

**Wichtige Grenze / Gegenfall:** Melodieton als Akkordton ist nicht zwingend; Non-Chord Tones müssen differenziert geprüft werden.

**Konkrete Anforderungen an Codex:** Input contract: lock_melody, lock_bass, lock_meter, difficulty, tonal_scope.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-007; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-026 – Stimmführungsdistanz und musikalische Wahl

Die minimale Summe von Halbtonbewegungen kann eine nützliche Vergleichsmetrik für Voicings sein, aber sie erfasst nicht automatisch Stil, Stimmenführungsgesetze, Klangbalance oder melodische Zielwirkung. Ein großer Sprung in der Oberstimme kann bewusst hervorgehoben werden, auch wenn die Summe aller Stimmen dadurch wächst. Analysetools sollten metrische Scores in nachvollziehbare Teilwerte zerlegen statt sie als ästhetische Autorität anzugeben.

**Eigenes Arbeitsbeispiel:** Cmaj7 E4–G4–B4–C5 → Am7 E4–G4–A4–C5 hat kleine Bewegungen; ein anderes Register kann effektvoller sein.

**Wichtige Grenze / Gegenfall:** Oktav-/Stimmzuordnung muss festgelegt sein; Set-Abstand ist nicht Stimmenführungsabstand.

**Konkrete Anforderungen an Codex:** Offer cost_min, voicecross_penalty, melody_priority und explicit_user_weights.

**Weiterführende Quellenfamilien:** EXT-V4-016, EXT-V4-017; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-027 – Korpusvergleich und statistische Evidenz

Korpus-Häufigkeiten sind nur sinnvoll mit klarer Repertoireauswahl, Zeitspanne, Annotationstyp und Zählweise. Ein 20.000-Dateien-Korpus ist kein repräsentativer Querschnitt aller Musik, und mehrere Konvertierungen derselben Aufnahme können Datengewichtung verzerren. Anders als Theorieregeln müssen statistische Aussagen mit Datensatzversion, Filter und Nenner verbunden werden, sonst erscheinen Präferenzen als objektive Wahrheit.

**Eigenes Arbeitsbeispiel:** 'IV→I in Pop-Korpus X' benötigt Anzahl, Gesamtfälle, Tonartheuristik und Subset-Lizenz.

**Wichtige Grenze / Gegenfall:** Keine Prozentwerte schätzen und keine Rangfolge aus allgemeinem Modellwissen als Korpusdaten ausgeben.

**Konkrete Anforderungen an Codex:** Data object includes dataset_id, version, query, numerator, denominator, annotation_confidence.

**Weiterführende Quellenfamilien:** EXT-V4-022, EXT-V4-023; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.


**Modulzahl dieses Bandes:** 6. Historisches V3-Material ist zusätzlich in `00_HISTORISCH_V3/` enthalten.
