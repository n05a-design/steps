# Governance: Quellenclaim, Wissen, Implementierung und Review

## Claim-Arten
1. **Fakt / technisch prüfbar:** `midi_note=69` ist A4=440 Hz unter 12-TET A440.
2. **Spezifikation/Norm:** MIDI 1.0 Nachrichtenformate; BS.1770-5 Messalgorithmus.
3. **Kontextuelle Theorie:** G7 als V7 in C, abhängig vom Tonalitätskontext.
4. **Interpretation:** Am–F–C–G mit C oder A als vermuteter Tonika.
5. **Didaktische Heuristik:** „Versuche beim Chorus höheres Register“; nicht universell.
6. **Produktentscheidung:** Welche Vorschlagsheuristiken standardmäßig aktiv sind, entscheidet der Nutzer/Projektinhaber.

## Versionierung
Die Version einer Forschungsbibliothek ist von der Appversion verschieden. Wissensobjekte erhalten stabile `knowledge_id`, `schema_version`, `content_revision`, `source_ids`, `review_status`, `deprecation_reason`. Rückwärtskompatibilität wird durch Migration und Regressionstest belegt, nicht durch stille Überschreibung.

## Rechte und Herkunft
Links auf privat zugängliche Lehrinhalte sind Referenzen, keine Nachnutzungslizenz. Kursbilder, Samples, MIDI-Downloads, Stems und DAW-Projects dürfen nicht aufgrund ihrer Abrufbarkeit frei im öffentlichen Repo erscheinen. Für open corpora gelten Lizenzgrenzen einzelner Teilbestände; bei McGill Billboard gilt CC0 für die Annotationen laut Projektseite, nicht für die Original-Audios. [R17,R18,R19]

## Freigabekriterien
`draft`→`technically_validated` (Parser und Struktur)→`source_checked` (Fundstelle und Rechte)→`music_reviewed` (Fachperson, Stilhörtest)→`approved_for_app` (Projektentscheidung, Plattformtests). Die Reihenfolge kann bei Designentwürfen variieren, aber Statusfelder sind getrennt.

## Streitfälle
Widersprechende Lenses werden nicht zu einem falschen Konsens reduziert. Annotationsstreit wird mit alternativen Quellen, Stilkorpus, Audio-/Notentext und Editorentscheidung dokumentiert. Transparente Unsicherheit ist Teil von STEPS.
