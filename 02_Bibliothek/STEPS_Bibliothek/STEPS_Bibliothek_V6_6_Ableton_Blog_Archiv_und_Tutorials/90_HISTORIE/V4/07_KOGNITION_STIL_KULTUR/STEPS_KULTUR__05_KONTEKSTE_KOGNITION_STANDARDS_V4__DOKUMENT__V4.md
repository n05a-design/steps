# STEPS V4 – Fachband: Querschnitt

**Version:** 4.0.0-research-draft · **Status:** wissenschaftlich orientierte Redaktionsfassung; Quellenfamilien sind keine geprüften Seitenzitate.

Dieser Band ist als ausbaubare Fachgrundlage gedacht, nicht als vermeintlich endgültige Universaltheorie. Jedes Modul enthält ein eigenständiges, für STEPS formuliertes Beispiel, eine konkrete fachliche Grenze und einen Software-/Codex-Übertragungsauftrag.

## RESEARCH-V4-043 – Stilsensitives Wissen statt Universalgrammatik

Ein einzelner Stilbegriff deckt meist heterogene Repertoires und kulturelle Traditionen ab. In klassisch-tonalem Satz sind Stimmführungs- und Kadenznormen anders verankert als in Jazz, Rock, Gospel oder elektronischen Formen. STEPS muss Regeln anhand von Geltungsbereich, Entstehungskontext und Beleglage beschränken; die generische Antwort 'dieser Akkord ist falsch' ist methodisch unangemessen.

**Eigenes Arbeitsbeispiel:** Eine offene Quinte kann im klassischen Kontrapunkt unter bestimmten Übungsregeln kritisiert, im Rock-Power-Chord aber intentional sein.

**Wichtige Grenze / Gegenfall:** Genre-Labels sind keine formal ausreichenden musiktheoretischen Definitionen.

**Konkrete Anforderungen an Codex:** Jede Rule hat scope, provenance, exceptions, review_policy und genre_coercion_warning.

**Weiterführende Quellenfamilien:** EXT-V4-001, EXT-V4-009; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-044 – Raga, Maqam und nichtwestliche Systeme

Viele musikalische Traditionen organisieren Tonmaterial, modale Praxis und Zeitbeziehungen anders als die westliche dur-molltonale Harmonielehre. Ein Raga ist nicht bloß eine siebenstufige Skala, sondern wird durch charakteristische melodische Wege, performative Konventionen und kulturelle Überlieferung mitbestimmt. Für Maqam und weitere Systeme gilt ebenfalls: tonaler Inhalt allein modelliert die Praxis nicht. Diese Domänen sollten mit Fachberatung ergänzt werden statt Pseudo-ROMAN-Analysen zu erzwingen.

**Eigenes Arbeitsbeispiel:** Sichere zunächst die Datenfelder tradition, tonal_reference, typical_motion, ornaments, phrase_grammar; lasse Akkordfunktionen unbekannt.

**Wichtige Grenze / Gegenfall:** Keine Behauptung, alle Ragas oder Maqamat ließen sich als diatonische Modi abbilden.

**Konkrete Anforderungen an Codex:** Introduce theory_system_id, tradition_authority and cultural_review_required.

**Weiterführende Quellenfamilien:** EXT-V4-028; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-045 – Musikalische Erwartung und Psychologie

Wiederholung, metrische Muster, stilistische Erfahrung und lokale Tonstabilität beeinflussen musikalische Erwartungen; sie dürfen aber nicht als universelle emotionale Formel verstanden werden. Ein harmonischer Trugschluss kann erwartungsbezogen diskutiert werden, wobei Lernhintergrund und Aufführungskontext die Wirkung verändern. Die App sollte 'emotionale Labels' und 'theoretisch begründete Spannung' getrennt dokumentieren.

**Eigenes Arbeitsbeispiel:** V7→vi nach mehreren I–IV–V–I-Zyklen kann in einem passenden Tonalstil als Erwartungsabweichung dienen.

**Wichtige Grenze / Gegenfall:** Aus diesem Akkordweg folgt nicht bei allen Hörenden dieselbe Emotion.

**Konkrete Anforderungen an Codex:** Store expectation_model_id, listener_assumption, intended_effect und explicit_uncertainty.

**Weiterführende Quellenfamilien:** EXT-V4-013, EXT-V4-014; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-046 – Annotationen und Harmoniekorpora

Maschinenlesbare Harmonieanalysen unterscheiden sich in Akkorddialekt, tonalem Kontext, Timing, Annotationstiefe und Lizenz. ChoCo vereinheitlicht Harte-/Roman-Familien, DCML spezifiziert funktionale Details und When in Rome sammelt unterschiedliche Analyseherkünfte. Um ihre Ergebnisse zu verknüpfen, müssen Quellschema, mögliche Konvertierungsverluste und ursprüngliche Annotatorentscheidungen erhalten bleiben.

**Eigenes Arbeitsbeispiel:** Ein RomanText V7/ii kann als Geltungsangabe mit lokaler Tonart notiert und in Harte ChordSymbol umgerechnet werden.

**Wichtige Grenze / Gegenfall:** Konvertierter ChordString ist kein Ersatz für historische Analyseintention.

**Konkrete Anforderungen an Codex:** Map source_format, converter_version, loss_flags, original_source_license and provenance_ids.

**Weiterführende Quellenfamilien:** EXT-V4-021, EXT-V4-022, EXT-V4-023; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-047 – Offene Standards und formatgebundene Unterschiede

MusicXML eignet sich für Noten- und harmonischen Austausch, MEI für reiche Dokument- und Forschungsrepräsentationen, JAMS für zeitliche Annotationen und MIDI für ausführbare Notenereignisse. Keine dieser Sprachen löst allein alle Anforderungen einer harmonischen Ontologie, analytischen Mehrdeutigkeit und menschlichen Quellenannotation. Import und Export müssen deshalb round-trip-Verlustgrenzen offenlegen statt 'verlustfrei' pauschal zu versprechen.

**Eigenes Arbeitsbeispiel:** Eine Viertelnotenmelodie lässt sich als MIDI exportieren; eine alternatives Formfunktionsanalyse braucht zusätzliche Daten.

**Wichtige Grenze / Gegenfall:** MIDI-Pitch allein enthält keine Schreibweise F# oder Gb; die Rückkonversion erfordert Kontext.

**Konkrete Anforderungen an Codex:** Prepare per-format capability matrix and loss_reports in export metadata.

**Weiterführende Quellenfamilien:** EXT-V4-024, EXT-V4-025, EXT-V4-026; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-048 – Quellenprüfung und Rechteketten

Wissenschaftliche Qualität beginnt mit der Unterscheidung zwischen einer Quelle, ihrer Metadaten-Seite, einem tatsächlich gelesenen Abschnitt und einer aus ihr hergeleiteten Aussage. Ein offen sichtbarer Verlagsabstract ist nicht die Erlaubnis, urheberrechtlich geschützte Textseiten oder Noten zu kopieren. Aggregatoren können unterschiedliche Teilkorpus-Lizenzen besitzen, sodass die Gesamt-Lizenz nicht ausreicht. Ein öffentliches Open-Source-Repository braucht klare Rechtepfade für jeden Inhalt.

**Eigenes Arbeitsbeispiel:** ChoCo nennt CC BY- und CC BY-NC-SA-Bestandteile; ein globales 'frei verwendbar'-Flag wäre falsch.

**Wichtige Grenze / Gegenfall:** Bibliografische Verifikation ≠ Volltextstudium ≠ freie Wiederverwendung.

**Konkrete Anforderungen an Codex:** Record claim_locator, read_status, license_for_annotations, license_for_scores and publication_gate.

**Weiterführende Quellenfamilien:** EXT-V4-022, EXT-V4-023; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.

## RESEARCH-V4-049 – Forschungs- und Codex-Validierung

Ein ausführlicher Research Text ist keine validierte Wissensdatenbank. Zuerst müssen Begriffe, Beispiele, Regeltypen, Quellen und Testfälle formal unterscheidbar werden; danach folgt musikfachliche Begutachtung. Automatische Tests können Halbtonabstände, Taktlängen, MIDI-Struktur und ID-Eindeutigkeit prüfen. Sie können die Angemessenheit einer stilistischen Interpretation oder kulturellen Einordnung jedoch nur begrenzt entscheiden.

**Eigenes Arbeitsbeispiel:** Validator prüft alle 16 Takte einer Etüde auf Dauer 4 Viertel; ein Fachreview prüft zusätzlich melodische Plausibilität.

**Wichtige Grenze / Gegenfall:** Ein maschinell gültiger Datensatz bleibt 'draft' bis Nachweise und Review vorliegen.

**Konkrete Anforderungen an Codex:** Use status transitions draft→source_checked→music_checked→approved with separate gates.

**Weiterführende Quellenfamilien:** EXT-V4-021, EXT-V4-026; Fundstellenstatus: *noch nicht als Einzelclaim verifiziert*.


**Modulzahl dieses Bandes:** 7. Historisches V3-Material ist zusätzlich in `00_HISTORISCH_V3/` enthalten.
