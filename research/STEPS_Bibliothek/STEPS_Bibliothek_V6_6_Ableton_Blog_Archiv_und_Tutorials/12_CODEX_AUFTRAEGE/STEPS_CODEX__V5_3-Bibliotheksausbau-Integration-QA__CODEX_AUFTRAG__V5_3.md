# STEPS – Codex Folgeauftrag V5.3: geprüfte Erweiterung und lokale Integration

**Status:** Ausführbarer Auftrag an Codex/Work **mit tatsächlichem Zugriff auf das Steps-Repository und den lokalen Steps-Ordner**. V5.3 wurde hier nur als eigenständiges Forschungsarchiv erstellt; keine Repo-Änderung, kein PR, keine lokal behauptete MIDI-Auswertung.

## Oberauftrag
Integriere die V5.3-Erweiterung in die vorhandene STEPS Knowledge Base, ohne V5.2 und historische Versionen zu verlieren. Fülle die sechs Hauptdomänen *Music Theory, Harmony, Chord Progressions, Composing, Drum Programming, Producer Tools* mit verknüpften Quellen, Beispielen, formalen Daten und Qualitätssicherung. Fachfelder 07–15 als Querschnitt beibehalten. Die hier produzierten 12 Lehr-MIDI-Beispiele sind **eigene** Cases, nicht mit den heruntergeladenen PPR-MIDI-Dateien zu verwechseln.

## Arbeitsphase C0 – Baseline
- `AGENTS.md`, git status, branch, aktuelle Tests, vorhandene KB, Datenmodelle und Originaldateien prüfen.
- Bestehende Änderungen und Rechte schützen; weder reset noch ungefragter Merge.
- Die 278 historischen V5.2-Dateien gegen das neue `00_NAVIGATION/STEPS_DATEIENINDEX_V5_3.csv` mappen und anhand SHA verifizieren. Beachte: zusätzliche Navigations-/Archivdateien können die physische ZIP-Eintragszahl gegenüber 278 erhöhen.

## Arbeitsphase C1 – Quellen und lokale Daten
- 20 ursprüngliche Fachquellen, Original-/Kursdateien und MIDI-Pakete **nur an vorhandenen realen Pfaden** suchen. Vorab keine Pfade erfinden.
- `15_TOOLS_SKRIPTE/STEPS_TOOLS__audit_midi_library__WERKZEUG__V5_3.py` auf einer **explizit autorisierten** lokalen Directory ausführen; ZIP-Dateien nur read-only inspectieren; Source-ID, SHA, Note-on/off, CC7, Tempo, Timing und GM-/Kit-Mapping prüfen.
- PPR-Remakes als transkribierte bzw. didaktisch rekonstruierte Beispiele dokumentieren, nicht als authentische Original-Sessions; kommerzielle MIDI/Samples niemals ungeprüft öffentlich committen.

## Arbeitsphase C2 – Sechs Hauptsäulen
1. Music Theory: Gehörbildung, Tuning, Enharmonik mit konkreten Übungen und Tonart-Testfällen.
2. Harmony: funktionsharmonische, modale, jazz-, blues-, pop- und elektronische Lenses und Gegenbeispiele.
3. Progressions: Melodie/Bass/Harmonic Rhythm/Voicing zeitlich konsistente Reharmonization.
4. Composing: Songwriting, Textbetonung, Topline, elektronische Form und adaptive Cues.
5. Drum Progressions: V5.3-MIDI-Studien, Groove/Velocity/Microtiming und verifizierte Quell-MIDI vergleichen; jede Stilkategorisierung als Hypothese.
6. Producer: Synthese, Sampling/808, EQ, Kompression/Sidechain, Stereo/Raum, Mastering/LUFS in dokumentierten Arbeits- und Quellenkarten.

## Arbeitsphase C3 – Typisierte Knowledge Objects
`Concept`, `Rule`, `Interpretation`, `Progression`, `DrumPattern`, `SynthPatch`, `ProducerTip`, `ComposingPattern`, `AudioMeasurement`, `Source`, `TestCase`; Feldschema/IDs/Versionen abgleichen. Produktive Datenschemata aus realem Repo bestimmen; V5.3-Schema ist ein testbarer Vorschlag. Keine neuen leeren Verzeichnisse als Fortschritt zählen.

## Arbeitsphase C4 – Qualität
- V5.3-Parser und Testdateien tatsächlich ausführen; Testergebnisse mit Tool-/Versionen protokollieren.
- V5.2-Material, das bisher nur auf Index- oder Abstract-Ebene „geprüft“ war, nicht zu `reviewed` aufwerten.
- Fachesperren: Musikstil, Gehörqualität, Audiopegelmessungen und kulturelle Traditionen brauchen menschliche oder belastbar audiodatenbasierte Review-Prozesse.
- Vor jedem öffentlichen Commit Lizenz- und Quellenprüfungen. Herstellerhandbücher belegen Funktionen, keine allgemeinen Ästhetiknormen.

## Arbeitsphase C5 – Konkrete Übergabe
Liefern: Git-Diff, Versions-/Migrationsmatrix V1–V5.3, Quellenauflösung, Read-only-MIDI-Audit mit privaten Source-Pfaden geschützt, Tests mit realem Exitcode, dokumentierte F-Gates, Abdeckungsmatrix, verbleibende P0/P1-Lücken. Keine automatische Veröffentlichung/PR-Merge ohne ausdrücklichen Auftrag. Änderungen unter dem eigens dafür vorgesehenen Branch.

## Definition of Done
Die relevanten Dateien sind verlinkt, Source-IDs geklärt, eigene MIDI-Studien technisch überprüft, lokale Fremd-MIDI korrekt eingeordnet, mindestens ein vollständiger End-to-End-Lernfall pro Fachsäule mit Gegenbeispiel und Evaluation dokumentiert. Ein Plan oder eine geerbte Zahl von „53.967 Checks“ zählt nicht als Nachweis eines gegen die Steps-Anwendung ausgeführten Tests.
