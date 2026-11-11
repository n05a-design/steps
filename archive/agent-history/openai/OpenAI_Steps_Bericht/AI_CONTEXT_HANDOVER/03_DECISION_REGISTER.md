# 03 – Entscheidungen, ADRs und Owner-Freigaben

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Offene verbindliche Entscheidungen

| ID | Problem | Dokumentierte Option und Empfehlung | Status | Änderungssperre |
|---|---|---|---|---|
| ADR-001 | Fenstermodell | Option A: ein Tkinter/ttk-Hauptfenster, zwei Panes (oben Akkord-Sequenzer, unten Voicing/Piano-Roll); Alternative Multi-Toplevel | **NICHT genehmigt** | GUI-Architektur und app/ui/ blockiert |
| ADR-002 | MVP-Scope Chords vs. Drums | Option A: Chords/Voicing v0.1, Drum ab v0.2+ | **NICHT genehmigt** | Drum-Umfang nicht vorziehen |
| ADR-005 | Interne Noten-/GUI-Darstellung | Option A: Z12 intern plus getrennte orthografische Repräsentation; B/Bb international, H/B deutsch wählbar | **NICHT genehmigt** | GUI-Präsentation gesperrt; fachliche Entkopplung zulässig |
| OA-0001 | Fremdmaterial in Git-Historie | Option A: bis Klärung Repo privat; Option C: nach Freigabe bereinigter History-Pfad | **NICHT entschieden** | öffentlicher Release/History-Rewrite gesperrt |
| OA-0033 | Alerts #1–#3 | Option A: nach belegter Third-Party-Einordnung schließen | **NICHT entschieden** | Alerts nicht eigenmächtig schließen |

**Wichtige Differenzierung:** `main` wurde bei der Repository-Abfrage als **public** gemeldet. Die frühere Empfehlung, das Repository vor Rechteklärung privat zu schalten, ist **keine umgesetzte Option**. Die Existenz historischer Inhalte in öffentlichen Blobs wird nicht durch lokale Secret-Scans behoben.

## Bewahrte ADR-Identitäten

- **ADR-001** – Fensterarchitektur, Fenster-/Pane-Entscheidung offen.
- **ADR-002** – MVP-Umfang (Chords v0.1 / Drums v0.2+), nicht umnummerieren.
- **ADR-005** – fachliches Harmonielehre-/Notationsmodell H/B vs. B/Bb, nicht umnummerieren.
- **ADR-011** – Release-Packaging (Wheel/PyInstaller), nach Phase-4.17-Meldung wiederhergestellte eindeutige ID.
- **ADR-012** – Aufbewahrungsrichtlinie rechtlich relevanter Web-/MIDI-Bestände, nach Phase-4.17-Meldung eindeutige ID.
- **ADR-003/004/006–010:** ihre vollständigen Titel und Entscheidungen wurden in dieser Übergabe **nicht** unabhängig aus dem Register ausgelesen. Keine Ergänzungen erfinden. Aktuelles `DECISION_REGISTER.md` im Repo lesen.

## Entscheidungen vs. Empfehlungen

Die bisherigen Agentenberichte nutzen Formulierungen wie „Empfohlen Option A“. Dies ersetzt keine unterschriebene Owner-Entscheidung. Headless-Implementierung und Tests sind mit den offenen GUI-Gates vereinbar; eine GUI-Implementierung wäre es nicht.

## Für jede Owner-Entscheidung zu protokollieren

Datum, konkrete Options-ID, Quelle und Entscheidungsträger, Geltungsbereich, Migrationsbedarf, Auswirkungen auf Phasen und Tests, aktualisiertes ADR, Follow-ups und Freigabe zum ggf. erforderlichen Release.
