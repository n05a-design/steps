# CODEX – STEPS Bibliothek V5.4: vollständiger Integrationsauftrag

**Keine Behauptung, dass Codex oder das tatsächliche Steps-Repository bereits ausgeführt wurde.** Dies ist ein konkreter Folgeauftrag für Codex; Bibliothekversion und Appversion strikt trennen.

## Verbindliche Randbedingungen
- Eigenständiger Projektbestand prüfen, bevor Code, Namen oder Pfade geändert werden. AGENTS.md hat Vorrang.
- V5.3-Bestand und 90_HISTORIE/99_ORIGINALARCHIV erhalten, keinen unkontrollierten Merge.
- PausePlayRepeat-Originaldownloads, kommerzielle Samples, geschützte Bücher und persönliche DAW-Sessions nicht ohne Rechte in Git committen.
- Jede neue Objektklasse erhält ID, Typ, Lens, Herkunft, Lizenzstatus, Reviewstatus, semantische Version und Migration.
- `technically_validated` ≠ `music_reviewed` ≠ `source_checked`. Offene Aufgaben nicht grün labeln.

## Arbeitspakete (Priorität und Akzeptanz jeweils vor Start konkretisieren)
- **A1:** Ermittle echtes Repo, Branch, Versionsstand, AGENTS.md, Zielsysteme und Testcommands.
- **A2:** Inventarisiere vorhandene Knowledge-Dateien mit Hash, Schema, Version, Lizenz und Autor.
- **A3:** Scan lokalen Steps-Ordner nach .mid, .mxl, .musicxml, .als, .flp und .zip: nur Bericht, keine ungefragte öffentliche Kopie.
- **A4:** Verifiziere 4 PausePlayRepeat-Drum-Referenzen und EQ-Kapitel gegen lokal vorhandene MIDI-/Lektionsdaten, Rechte beachten.
- **A5:** Prüfe V5.3→V5.4 Hash-Invarianten und Archivmanifest.
- **A6:** Identifiziere historische doppelte Dateien vs sachlich verschiedene Fassungen mit Begründung.
- **A7:** Lege aktive Referenz/Entwurf/Archiv getrennt fest, ohne alte IDs zu brechen.
- **B1:** Kanonisches Ereignisdatenschema Notes, Bass, Chord, Phrases, Grooves, Sound/Patch entwerfen.
- **B2:** Eindeutige Naming- und Temperament-IDs, enharmonisches Spelling und MIDI-Übersetzung implementieren.
- **B3:** Intervall- und Scale-Parser mit diatonischer und chromatischer Semantik testen.
- **B4:** Chord-Symbol-Parser inkl. slash/extended/sus, mit klaren Fehlermeldungen implementieren.
- **B5:** Roman Numeral und DCML Adapter in begrenztem Scope; Testfälle vorbreiten.
- **B6:** Time grid 4/4,6/8,7/8, Auftakte, Tempo-Map und PPQ roundtrip testen.
- **B7:** Mehrdeutige Harmonielesarten an einem Event speichern, Ranking transparent.
- **B8:** Voice-leading Reporter als kontextabhängige Heuristik, harte Range-Regeln getrennt.
- **B9:** 32 Progressionsfälle aus V5.4 JSON importieren und analysierbar machen.
- **B10:** Chords+melody+voice-leading Harmonisierungsvorschläge mit Gegenbeispiel-Log führen.
- **C1:** 16 neue Original-4-Track-MIDI-Studies importieren und Note-On/Off strukturell vergleichen.
- **C2:** Form/Funktionsschema: Verse, Chorus, AABA, Period, Sentence als unterschiedliche Analysis-Lenses.
- **C3:** Motiventwicklung: Transposition/Fragmentation/Sequence/Duration-scaling reproduzierbar machen.
- **C4:** Kompositionsprozess: Brief→Idee→Form→Melody→Harmony→Bass→Arrangement→Review UI.
- **C5:** Gemischte/generative Score-Daten streng von Originalaufnahme-Transkriptionen trennen.
- **D1:** Drum-Layer Onsets, Velocity, swing source, sample map, CC und choke groups modellieren.
- **D2:** Straight vs committed Groove-Versionen; doppelte Groove-Anwendung ausschließen.
- **D3:** Bass NoteOff vs hörbares Audioende durch optionalen DAW Render unterscheiden.
- **D4:** 16-Bar-Drumprogression mit Scene-/Fill-/Layer-Events modellieren.
- **D5:** Eigene V5.3 12 MIDI Drumstudien plus neue V5.4 Drums intern vergleichen.
- **E1:** Synth patch schema mit Oszillator, Envelope, LFO, Filter, Modulation definieren.
- **E2:** 808 one-shot/gated/glide-spezifische Fälle mit klarer Instrument-Dependency prüfen.
- **E3:** EQ/Compression/Sidechain parameterisiertes Diagnoseformat implementieren.
- **E4:** LUFS/TruePeak nur von tatsächlich gerendertem Audio und dokumentiertem Meter übernehmen.
- **E5:** Mix/Mono-Stereo-Check als optionalen Review ohne erfundene Audiomessungen darstellen.
- **F1:** Source→Claim→Exercise→Test→Review auf stabiler ID implementieren.
- **F2:** Externe Lizenz- und Corpus-Gates für ChoCo, McGill und kostenpflichtige Kurse prüfen.
- **F3:** UI-Lernpfade für Anfänger und Fortgeschrittene barrierearm entwerfen.
- **F4:** Historische Konvertierung mit reproduzierbaren Migration-Skripten und Rückbauplan.
- **F5:** Automatische Unit-/Property-/Roundtrip-Tests auf Windows/macOS/Linux ausführen.
- **F6:** Musiker- und Hörreview dokumentieren; ohne Fachprüfung keine `peer_reviewed`-Labels.
- **F7:** PR mit Änderungen, Risiken, Screenshots, Testlogs; Merge ausschließlich auf explizite Freigabe.

## Definition of Done je Phase
- **A / Audit:** Reale Fundstellen und SHA, Quellrechte und lokale Datei-Zugriffslage dokumentiert; keine implizite neue Bibliothek in den falschen Root kopiert.
- **B / Datenmodell:** Schema-/Propertytests, Note/Chord-/Roman Parser-Gegenbeispiele, strukturierte Alternative Interpretationen; Migrationsplan lesbar.
- **C / Komposition:** Eigene MIDI-Studien importierbar; ein Nutzer kann ein Motiv verändern, Fortschritt zurücknehmen und eine Variation exportieren; Musikreview separat.
- **D / Rhythmus:** Timing, Groove, Velocity und CC getrennt; kein Doppel-Swing; Original-PPR-MIDI-Quellenstatus explizit.
- **E / Producer:** realer Audio-Render oder `not_executed`; keine fiktiven Messwerte; Patchrechte und Sample-Abhängigkeit offen.
- **F / Release:** OS-Matrix, Testlogs, Artefaktmanifest, Lizenzprüfung, PR und Rollback; kein stiller Merge.

## Empfohlene Erstkommandos
```bash
python 15_TOOLS_SKRIPTE/STEPS_TOOLS__validate_v54__WERKZEUG__V5_4.py
```
Das Prüftool validiert nur die mit V5.4 gelieferten Datensätze und Hash-Invarianten. Ein echtes Projekt-CI oder Musikerreview ist gesondert auszuführen.

## Gegen unzulässige Abkürzungen
- Nicht automatisch alle durch Transposition erzeugten Tonartvarianten als eigenständige Progressionsforschung ausgeben.
- Keine starre Emotion-Zuordnung eines Akkords. Keine universellen Genreschwellen bei BPM/Syncopation.
- Source-/Lizenzstatus nie allein aus öffentlichen Downloadlinks ableiten.
- Belege für Tonalität und Genre immer im konkreten zeitlichen Kontext.
- Datenimport und Parsererfolg nicht als musikalischen Qualitätsscore verwenden.
