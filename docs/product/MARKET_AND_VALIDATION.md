# Wettbewerber, Positionierung und Validierung – Fakten von Hypothesen trennen

**Stand:** 10.11.2026. **Quellenart:** Herstellerdokumentation, nicht unabhängige Produkttests. Die Originalquellen im historischen Overview-Kapitel 6 bleiben erhalten; aktuelle Produkte und Preise wurden **nicht** vollständig neu vermessen.

## 1. Methodik

Wettbewerb wird nicht nach Markenname oder Screenshots, sondern nach reproduzierbaren Aufgaben verglichen: Akkordeingabe; Tonart-/Moduswechsel; erklärbare Relation; alternative funktionale Lesart; Voice Leading; Drum-/Rhythmusspuren; MIDI/SMF; Offline und quelloffene Architektur; Übertragung von Daten und Lernmaterial. Für jedes Feld getrennt: `supplier_claim`, `tested_behavior`, `unknown`, `pricing_plan` und `date_checked`. Eine Produktseite mit Featureliste belegt nur eine *Herstelleraussage*.

## 2. Verifizierte öffentliche Herstellerbeispiele (keine Funktionsabnahme)

- **Hookpad / Hooktheory:** Herstellerdokumentation beschreibt tonartbewusste Chord-/Melody-Eingabe, Chord-Empfehlungen (Magic Chord), Playback-Kanäle einschließlich Drums und Export als Format-1-MIDI; Tonartfarben und songbezogene Vorschläge werden erklärt. Quellen: https://www.hooktheory.com/support/hookpad und https://www.hooktheory.com/hookpad . **Konsequenz:** „Akkordvorschläge“, „MIDI-Export“ oder „Theory-aware“ sind für Steps nicht automatisch einzigartig. Die konkrete Differenzierung müsste die nachvollziehbare Mehrdeutigkeit, überprüfbare Quellen, Offline-/Open-Source-Ziele und eine bessere UX bei gezielten Nutzerfällen sein.
- **Chord Files/Chord Wheel/ModeWheel:** In der Quellen-Overview und in den 20 Ausgangsquellen als relevante Inspiration beschrieben. Funktionsumfang der *aktuellen* Produkte ist hier nicht vollständig mittels Hersteller- oder Hands-on-Test verifiziert. Visuelle Nachbildung charakteristischer Darstellungen darf nicht als Implementierungsauftrag verstanden werden.
- **Scaler, Chordbot, MuseScore, music21:** in bisherigen Forschungsunterlagen als Kategorien für Produkttests, Interoperabilität und fachliche Testorakel genannt. Dieses Audit bestätigt **keine vollständige Versions-/Preismatrix** und keine Lizenz-/Kompatibilitätsfreigabe für die Nutzung von deren Code oder Daten.

## 3. Zu testende Alleinstellung

**Differenzierungs-Hypothese:** In Steps kann eine Person *warum* eine harmonische Verbindung plausibel ist verstehen, auch wenn sich die Analyse nach Stil, Tonart oder Voicing ändert. Das Produkt schafft einen Mehrwert gegenüber Systemen, die vor allem einen nächsten Akkord oder eine generische Sammlung vorschlagen. **Zu falsifizieren:** Wenn bei gleichen Aufgaben etablierte Tools gleich verständliche bzw. bessere Erklärungen liefern oder Nutzer die Quellen-/Mehrdeutigkeitsansicht ignorieren, ist die Positionierung anzupassen.

## 4. Vergleichsversuch – gleiche Musikaufgaben in drei bis fünf Produkten

| Test-ID | Aufgabe | Bewertungsbogen (0/1/2, belegte Beobachtung) |
|---|---|---|
| C01 | 4 Akkorde eingeben ohne Handbuch | Zeit, Bedienfehler, Undo/Redo, Undo-Verständnis |
| C02 | Progression transponieren und Schreibung prüfen | Note- und Chord-Spelling, Zwischenschritt |
| C03 | `E7→Am` unter a-Moll/C-Dur analysieren | korrekte Kontextkennzeichnung |
| C04 | Nichtfunktionale/modal entlehnte Akkorde anbieten | Theorierahmen und begründete Alternativen |
| C05 | Kick/Snare ergänzen, Tempo ändern | synchrones Zeitmodell oder explizit fehlend |
| C06 | in MIDI exportieren und in externer App öffnen | Dateien, Timing, Trackzuordnung, Tempo-Map |
| C07 | Offline öffnen, Daten anlegen, speichern | Internetzwang/Account, reale Datenhaltung |
| C08 | Quellenbeleg und nachvollziehbare Regel untersuchen | Quellen- und Geltungsangaben oder keine |

Die Skala ist nur bei nachvollziehbarer Beobachtung verwendbar. `unbekannt` bleibt unbekannt und wird nicht als 0 gewertet. Version, Datum, Plattform, Planstufe und Quelle pro Ergebnis festhalten.

## 5. Fehlende Forschung und nächste Entscheidungen

1. Wettbewerbermatrix der historischen Dokumente neu prüfen: Herstellerfakten vs. Datumsstände vs. Wertung.
2. Benutzergeführte Testaufgaben mit 5–8 echten Zielpersonen; erst dann Prioritäten aus Nutzwert ableiten.
3. Lizenz-/Urheberrechtsprüfung sämtlicher verwendeter Referenzbilder, Audio- und Musikbeispiele.
4. Erfolgsmessung: task completion, explain-back, Fehlannahmen, gewünschte Exportformate und bevorzugter Workflow.
5. Danach Positionierungs-ADR (Open Source + offline + fachlich nachvollziehbar vs. Umfang klassischer DAW-/Generatorfunktionen).

**Grenze:** Diese Datei stellt keine laufend aktualisierte Preis-/Featurevergleichstabelle dar. Preise, Verfügbarkeit und neu eingeführte Funktionen müssen im jeweiligen Recherchebatch erneut belegt werden.
