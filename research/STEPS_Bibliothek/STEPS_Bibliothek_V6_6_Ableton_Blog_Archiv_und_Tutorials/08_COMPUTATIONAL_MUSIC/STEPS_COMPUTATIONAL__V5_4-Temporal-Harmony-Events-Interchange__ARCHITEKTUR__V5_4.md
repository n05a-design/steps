# Computational Music: ein kanonisches zeitliches Ereignismodell

## Primärdaten vor Interpretation
Das kanonische Objekt enthält neben Projektversion: `event_id`, `start_beats` (rational), `duration_beats`, `pitch` (MIDI optional), `spelling` (Buchstabe/Vorzeichen/Oktave optional), `velocity`, `part`, `instrument_id`, `tuning_id`, `source_id`. Harmonische Hypothesen liegen in einem separaten Segmentlayer, nicht als zwingende Eigenschaft jedes Note-On. [R06, R10, R11, R12]

## Unterschiedliche Austauschschichten
- **MIDI** übermittelt Performanceereignisse und teilweise Tempo/Controller; nicht zuverlässige enharmonische Schreibweise, Kompositionsform, Sample-Einstellung oder Audioklang.
- **MusicXML** kann westliche Partitur und Akkordsymbole transportieren; Rundlauf muss mit konkreter Version und realem Parser getestet werden.
- **MEI** ist für komplexere wissenschaftliche Encoding- und Editionsfälle interessant; nicht alle visuellen und semantischen Features sind ohne Verlust in MusicXML übertragbar.
- **DCML** ist eine harmonische Annotierung mit eigenen Konventionen; ein Lead-Sheet-Chordsymbol ist nicht automatisch ein valides DCML-Label.
- **Audiofeatures** (chroma, LUFS, onset times) gehören in eine andere Domäne mit Messalgorithmus/Prüfprovenienz.

## Erhaltungssätze
Bei jedem Parser-Roundtrip: Note-onsets in rationaler Beat-Zeit innerhalb Toleranz, Event-Reihenfolge, Stimmenanzahl, ID-Verweise, Zeitbasis, Vorzeichen soweit repräsentierbar. Nicht darstellbare Informationen werden in einem `loss_report` ausgegeben. Semantische Mehrdeutigkeit bleibt als alternatives Annotation-Set erhalten.

## Beispiel
Piano spielt G7/B; Lead-Note F4 liegt vorübergehend über dem Akkord. Kanonische Note-Events speichern genau die erklingenden Pitches und Dauern; Harmonieebene enthält `G7/B`, lokale Tonart C und optionale Funktionshypothese V6/5. Ein DCML-Export kann seine eigene Normalform bilden und muss verlustbehaftete Vereinfachungen dokumentieren.

## Codex-Verantwortung
Erst realen Steps-Repository-Bestand untersuchen; dann ein migrationsfähiges Schema/Adapterinterface vorschlagen; Testfälle vor neuen Generatoren; keine direkte Annahme, dass frühere V3-V5 JSONs dasselbe Kanonformat implementieren.

**Status:** Architekturentwurf; MusicXML-/MEI-/music21-Adapter nicht in diesem Paket implementiert.
