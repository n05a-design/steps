# STEPS – Restrisiken, Offene Punkte & Blocker-Register (Phase L Audit)

**Dokumenttyp:** SYSTEMATISCHES RISIKOREGISTER & BLOCKER-KATALOG  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Architektur, Sicherheit, Rechte, Scope & Zukünftige Entwicklungsphasen  
**Status:** `AUDITED & STRATIFIED`  

---

## 1. Klassifikation der verbleibenden Risiken

Gemäß den Abschlusskriterien des Master-Auftrags wird jedes Thema streng in eine von fünf Kategorien eingestuft:

| Statusklasse | Bedeutung | Anzahl |
|---|---|:---:|
| **ERLEDIGT UND VERIFIZIERT** | Vollständig bearbeitet, durch Tests oder Primärquellen nachgewiesen. | 22 |
| **ERLEDIGT, ABER EINGESCHRÄNKT VERIFIZIERT** | Fachlich ausgearbeitet; finale Validierung benötigt Audio-Engine oder GUI-Test. | 4 |
| **FREIGABE ERFORDERLICH** | Betrifft Architekturgrundsatz, Sicherheit oder Rechtsfragen; bedarf Project-Owner-Beschluss. | 5 |
| **BLOCKIERT** | Technische Umsetzung durch eine externe oder vorgelagerte Entscheidung gesperrt. | 2 |
| **OFFEN** | Für spätere Entwicklungsstufen (Phase 5+) terminierte Roadmap-Aufgabe. | 6 |

---

## 2. Freigabebedarf & Architekturentscheidungen (Project Owner)

Folgende fünf Punkte erfordern eine formale Beschlussfassung durch den Project Owner und können nicht autonom durch Agenten entschieden werden:

1. **`ADR-001` (Fensterarchitektur für STEPS Desktop):**
   - *Option A (Empfohlen):* Ein einziges Hauptfenster (Single-Window) mit vertikaler 2-Pane-Teilung (oben Akkord-Sequenzer / Harmonie-Timeline; unten Voicing-Inspektor / Piano-Roll).
   - *Option B:* Zwei separate Top-Level-Fenster (Akkordfenster getrennt von Piano-Inspektor).
   - *Blockiert:* GUI-Entwicklung in `app/ui/`. (Headless Core in `src/steps/theory/` ist **nicht** blockiert!).

2. **`ADR-002` / `OA-0012` (Produktstrategie & Scope v0.1):**
   - *Option A (Empfohlen):* Strikte Fokussierung auf Harmonielehre, Voicings und Progressionen für Release v0.1; vollständige Zurückstellung der Drum-Groove-Engine auf Version v0.2+.
   - *Option B:* Simultane Entwicklung von Akkord- und Drum-Sequenzer in v0.1.

3. **`ADR-005` (Notationskonventionen & Fachmodell Enharmonik):**
   - *Option A (Empfohlen):* Interne Speicherung ausschließlich über mathematische Tonklassen $\mathbb{Z}_{12}$ ($0..11$) und internationale Notennamen (`B / Bb`); konfigurierbare Anzeige im GUI für deutsche Notenkonvention (`H / B`).
   - *Option B:* Duale Speicherung im Datenmodell.

4. **`OA-0001` (Urheberrechtlicher Umgang mit Fremdmaterial in der Git-Historie):**
   - *Option A (Empfohlen):* Beibehaltung des Repositories als `Private` bis zum vollständigen Abschluss der Kernentwicklung.
   - *Option C:* Bereinigung der Git-Blobs vor der ersten öffentlichen Bereitstellung via BFG Repo-Cleaner.

5. **`OA-0033` (GitHub Security Leak Alerts #1 bis #3):**
   - *Option A (Empfohlen):* Schließen der 3 Alerts im GitHub Security Tab mit der Begründung: *"Third-party embedded client keys in historical 2018 Ableton documentation dumps; no repository credential exposure"*.

---

## 3. Technische & Inhaltliche Restrisiken

| Risiko-ID | Bereich | Risikobeschreibung | Wahrscheinlichkeit | Auswirkung | Minderung / Handhabung |
|---|---|---|:---:|:---:|---|
| **RSK-01** | `M01` Akustik | Railsback-Spreizung und Inharmonizität bei Klaviersaiten sind nicht in einfachen mathematischen Sinustönen abbildbar. | Mittel | Gering | Für die symbolische Harmonielehre irrelevant; betrifft erst die Synthesizer-Engine in Version v0.3. |
| **RSK-02** | `M07` Rhythmik | Micro-Timing-Unterschiede im Millisekundenbereich können durch Windows-Timer-Jitter bei der Live-Wiedergabe schwanken. | Hoch | Mittel | Verwendung hochpräziser Multimedia-Timer (z. B. `time.perf_counter_ns()`) bei der künftigen Audio-Wiedergabe. |
| **RSK-03** | `M11` MIDI | Konvertierung komplexer polyphoner Tuplets (z. B. 11:8 Septolen) zwischen MIDI und MusicXML bleibt prinzipbedingt verlustbehaftet (`ERR-032`). | Mittel | Gering | Transparente Dokumentation der Rundungsgrenzen; interner Speicherstandard bleibt exaktes 480 PPQ Tick-Raster. |
| **RSK-04** | `src/glide-v3.53` | Unbeabsichtigte Modifikation des Glide-Legacy-Bestands bei globalen Refactorings. | Niedrig | Hoch | Strikte Isolationsregel (AGENTS.md Regel 9 & Prompt Grundsatz 2.4). CI-Prüfungen sichern Unveränderlichkeit ab. |
