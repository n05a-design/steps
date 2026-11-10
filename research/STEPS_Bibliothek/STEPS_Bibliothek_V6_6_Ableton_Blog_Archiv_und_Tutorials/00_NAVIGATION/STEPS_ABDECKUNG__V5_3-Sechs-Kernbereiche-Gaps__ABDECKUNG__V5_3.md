# STEPS – Coverage Delta V5.3: tatsächliche Erweiterung der V5.2-Bibliothek

**Prüfbasis:** V5.2-Archiv mit dokumentierten 278 Nutzdateien, zusätzlich Navigations- und Originalarchivdateien; V5.3 ist ein *nicht-destruktiver* wissenschaftlicher Ausbau im separaten Verzeichnis. Keine Prüfung des lokalen Steps-Repositories oder der proprietären Nutzer-MIDI erfolgt.

| Domäne | V5.2-Lücke | Neuer V5.3-Inhalt | Was weiterhin fehlt? | Einstufung |
|---|---|---|---|---|
| Music Theory | Gehörbildung, Temperament, Micropitch | Lernpfad, 4 Originalübungen, Tuning-/Enharmonikmodell | Audiomaterial, echter fachlicher Hörtest, traditionsbezogene Tuning-Quellen | Arbeitsstand vertieft |
| Harmony | Pop/Blues/Jazz-Lenses ungleich tief | fünf Analyse-Perspektiven und konkrete alternative Lesarten | wissenschaftliche Primärquellen je Genre, Reviews der V5-Rule Cards | Arbeitsstand vertieft |
| Chord Progressions | Reharmonisierung ohne zeitliche Melodieprüfung | Vier-Takt-Originalmotiv mit 5 Varianten | ausgerechnete echte Voicings für Instrumente, Hörreview | Arbeitsstand vertieft |
| Composing | Lyrics/Prosodie, Electronic Arrangement | 16-Takt-Topline-Workflow und 24-Takt-Arrangementkonzept | gesungene Audioaufnahme, instrumentale Orchestration, Komponistenreview | Arbeitsstand vertieft |
| Drum Programming | nur vier externe Kursstile | 12 eigene 2-Takt-Studies MIDI+JSON, Stil-/Timingkapitel, MIDI-Scan-Methodik | tatsächliche PPR-MIDI aus lokalem Ordner, weitere traditionsbezogene Genrequellen | echte technische Prüfdaten; Stilreview offen |
| Producer Tools | nahezu nur EQ | 7 eigenständige Kapitel: Synth, Sampling, EQ, Dynamics, Stereo, Loudness, DAW/Exports | testbare Synth-Patches, unabhängige Audiodemos, Plugin-/Gerätevergleiche | fachliche Arbeitskapitel vorhanden |
| Cognition/Culture | empirische Hörbelege, kulturbezogene Tiefe | methodische Evidenzgrenzen | Primärforschung, Reviewer aus jeweiligen Traditionen | nur methodisch erweitert |
| Computational | mehrere inkompatible Datenmodelle | explizite Schichten, JSON-Schema und technische Unit-Gates | App-End-to-End, reale Parser, Migrationsentwurf | Schematests, keine Appintegration |
| Sources | schwierige Einzelbelege | 12 zusätzliche namentlich identifizierte Technik-/Standardquellen; geprüfte Abschnitte benannt | umfassende Bibliografie/DOI/ISBN, Originalmedien und Quellen-Reuse | Quellenstatus transparenter, kein Peer-Review |

## Weiterhin offene höchste Prioritäten
1. **P0:** Git/Projektbestand und tatsächliche Dateipfade ermitteln; `AGENTS.md` beachten; keine unkontrollierte Überschreibung.
2. **P0:** Originalquellen einschließlich der 20 anfänglichen Bücher/TXT und privater lokaler MIDI/ZIP kontrolliert inventarisieren; gerade MIDI-Lektionen nicht als bereits überprüft ausgeben.
3. **P0:** Quellenstellen/Claims/Review nachvollziehbar verknüpfen; nicht nur 12 registrierte URLs als „Wissenschaftsbibliothek“ ausgeben.
4. **P1:** Fachliche und akustische Review der neuen Muster; die Pattern-Stilnamen sind didaktisch orientierend.
5. **P1:** Samples, Synth-Patches und Audiometriken gegen echte Engines und Tools prüfen, weil MIDI alleine keine Soundqualität zeigt.
6. **P1:** Historische V1–V5.2-Schemata und IDs über Migrationstabelle vereinen; keine versteckte Dublettenbereinigung.
7. **P2:** Musikpädagogik/Gehörbildung, Instrumentation, kulturübergreifende Modelle und Genreanalyse nachhaltig vertiefen.

## Anzahl vs. Bedeutung
Die 12 neuen MIDI-Patterns zählen als **12 original erstellte technische Studien**, nicht als 12 wissenschaftlich validierte Genredefinitionen. Zahlreiche historische Varianten sind algorithmisch abgeleitet. Ein grüner Parser-Test validiert Dateiintegrität, nicht musikalische Interpretationsgüte oder Quellenrecht.
