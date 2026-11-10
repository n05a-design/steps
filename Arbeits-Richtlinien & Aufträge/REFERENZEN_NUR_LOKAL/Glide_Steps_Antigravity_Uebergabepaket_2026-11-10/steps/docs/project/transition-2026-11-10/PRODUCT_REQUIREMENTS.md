# Steps – PRD-Arbeitsfassung (Produktauftrag, nicht genehmigt)

## Produktziel

Lernende und Producer sollen eine kurze Akkordfolge und ein dazu synchrones Drum-Pattern erstellen, deren Harmonie nachvollziehbar analysieren, sicher speichern und als MIDI in eine DAW übertragen können. Ziel ist **funktionierender kreativer Workflow mit transparentem Musikmodell**, nicht möglichst viele integrierte Theorietexte.

## Personas und zu überprüfende Aufgaben

- Einsteiger: „Ich baue C–G–Am–F und verstehe Tonart, Akkordtöne und mögliche alternative Deutungen.“
- Hobbyproducer: „Ich erstelle 4–8 Takte inkl. Drum-Pattern, Tempo, Groove und exportiere sauber nach Ableton/Reaper oder andere DAW.“
- Lehrende: „Ich kann Transposition, Stimmführung, Progressionsvariante und fachliche Belege verständlich demonstrieren.“

## Muss-/Kann-Kriterien

| Stufe | Muss | Nicht automatisch enthalten |
|---|---|---|
| M0 Technisches Fundament | CLI/Start, AppContext, zwei Hostplätze als Testvertrag, isolierte Nutzerdaten, atomar gespeicherte Projektstruktur, Tests/CI | volle GUI, Playback |
| M1 Chord-Vertikalschnitt | Akkorde mit Tondauern/Voicings, vier Takte, DE/EN-Notation, Transposition, Undo/Redo, Save/Reload, unabhängiger Type-1-/MIDI-Test | fertiger Drum-MVP |
| M2 Chord+Drum | Step-/Pattern-Editing, Velocity, Quantize, Loop, gemeinsame Tempo-/Meter-Basis, MIDI-Spuren, realer DAW-Import | eigene Samplelibrary oder DAW-Klon |
| M3 Erklärbarkeit | Tonart/Modus/Stilkontext, Ambiguität, nachvollziehbare Quellen, UI-Erläuterung, Negativfälle | Aussagen ohne Review oder generative Musikfakten ohne Beleg |
| Release | native Starts, Crash-/Migrationstests, Legal-/Rights-Clearance, a11y, menschliche UX, Installer/Hashes | „CI grün“ allein |

## Explizite Scope-Entscheidungen nötig

1. Drum = Steps-/Pattern-Sequencer, Percussion-Progression, Groove-Editor oder alles?
2. Muss Nutzersession lokal hörbar sein oder genügt zunächst MIDI-Export? Falls Playback: welcher Backendtyp und SoundFont-Rechte?
3. Windows/macOS/Linux als erste echte Zielplattformen; Tablet/iOS nur gesonderte Technologie-/Produktentscheidung.
4. Wie werden musiktheoretisch mehrdeutige Labels gezeigt und manuell korrigiert?
5. Wie detailliert sind Swing/Tuplets, Meters, Tempo-Maps, Pitch-Cents/Tuning/Spelling im ersten Projektformat?
6. Datenformat, Dateiendung, Sicherheitsbudget, Backups, Medienreferenzen, Rechte für Demo-Material.

## Definition of Done pro Nutzerreise

Vier Takte, überprüfbare Akkordtöne, Timing und Drum-Events; ein sichtbarer GUI-Workflow ohne stillschweigende Mutation; Undo/Redo und Save/Reload liefern byte-/semantikgeprüft denselben Zustand; MIDI mit unabhängiger Parserbibliothek und in einer externen DAW auf Pitch/Length/Tempo/Tracks kontrolliert; fachliche Hilfetexte mit Quellen-ID; keine Produktivdaten anderer App gelesen; Abbruch/Fehler wird angezeigt. **Kein Release ohne Test auf dem finalen SHA.**
