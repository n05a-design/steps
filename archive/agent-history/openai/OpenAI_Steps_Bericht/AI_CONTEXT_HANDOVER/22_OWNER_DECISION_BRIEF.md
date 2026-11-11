# 22 – Entscheidungsvorlage für den STEPS Project Owner

**Status:** Alle fünf Entscheidungen stehen laut bisher übermittelten Berichten noch aus. Die folgenden Empfehlungen sind **nicht** genehmigt.

## ADR-001 – Fensterarchitektur

**Problem:** Soll STEPS ein Hauptfenster mit zwei Kernpanes oder mehrere Toplevel-Fenster verwenden? **Empfohlene Option A aus Phase 4.17:** Tkinter/ttk Single Window mit Akkord-Sequenzer oben, Voicing-/Piano-Roll-Inspektor unten. **Konsequenz:** GUI-Implementierung noch blockiert. **Zu entscheiden:** Bedienlogik, Docking/Responsive-Verhalten, Wiederverwendbarkeit der Shell, plattformübergreifender Testumfang.

## ADR-002 – MVP Chords vs. Drums

**Empfohlene Option A:** v0.1 Harmonielehre/Voicings, Drum-Sequenzer ab v0.2+. **Zu entscheiden:** konkrete MVP-Abnahmekriterien und Abhängigkeit Drum-Groove-Reference-Library von der ersten Oberfläche.

## ADR-005 – Internes Fachmodell/Notation

**Empfohlene Option A:** getrennte Tonklasse modulo 12 und Notenschreibweise, international B/Bb standardmäßig, deutsch H/B optional. **Zu entscheiden:** verbindliche API-/UI-Konvention und gespeicherte Benutzereinstellungen; musiktheoretische Orthographie nie auf bloße Tonklasse reduzieren.

## OA-0001 – Urheberrecht und historische Git-Blobs

**Meldung:** Historische Web-/MIDI-Bestände, insbesondere fremde Archive. **Empfehlungsalternativen:** Repository vorübergehend privat oder nach Freigabe gezielt Git-Blobs bereinigen (mit BFG o. ä.), jeweils mit rechtlicher und technischer Folgenabschätzung. **Keine dieser Maßnahmen wurde in der Übergabe als beschlossen bestätigt.** Public-Status bei GitHub-Abfrage ist belegt.

## OA-0033 – GitHub Security Alerts #1–#3

**Meldung:** 27 Google-API-bezogene Treffer plus sechs AWS-/S3-Scannerfunde in historischen Archiven. **Frühere Empfehlung:** bei tatsächlich öffentlichen Drittanbieter-Clientkeys ggf. Alerts begründet als fremd/öffentlich einstufen. Dies ist **keine automatische Entwarnung**. Vor Schließung jedes Alerts Eigentümerschaft, Exposition, technische Einordnung und Remediation dokumentieren.

## Vorschlag für dokumentierte Freigabe

Pro Entscheidung festhalten: Datum, verantwortliche Person, Option und Alternativen, betroffene Dokumente, Rückwirkungsbedarf, Risikoeigentümer, Testfolgen, Implementierungsfreigabe. Änderungen im bestehenden kanonischen ADR-/OA-Register, nicht in parallelen Schattenregistern.
