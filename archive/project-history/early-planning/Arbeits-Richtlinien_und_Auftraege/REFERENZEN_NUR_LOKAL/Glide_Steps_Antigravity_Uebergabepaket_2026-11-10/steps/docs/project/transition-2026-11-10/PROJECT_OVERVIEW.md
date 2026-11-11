# STEPS – operative Projekt-Overview (Ergänzung zum Master 09.11. und Review V3)

## 1. Zielbild und Nutzenversprechen

Steps erlaubt das **Erstellen**, **Verstehen** und **Austauschen** von Akkord- und Drum-Progressionen. Der Lernwert entsteht aus zugänglicher Harmonie-/Stimmführungsanalyse mit Notation/Alternativdeutungen; der Produktionswert aus präzisem Zeitraster, bearbeitbaren Progressionen und DAW-fähigem MIDI. Beides ist durch konkrete Aufgaben zu validieren, nicht durch die Größe einer Bibliothek.

**Abgrenzung:** Nicht automatisch ein vollwertiger DAW-Klon, Noten-Editor, Sample-Händler, KI-Musikgenerator, Account-/Cloudplattform oder Glide-To-Do-Skin. Features, die außerhalb des ersten vertikalen Arbeitsflusses liegen, haben eigene Entscheidungs-Gates.

## 2. Momentaufnahmen – strikt getrennte Evidenzachsen

| Gegenstand | Beobachtung am 10.11.2026 | Nicht daraus ableiten |
|---|---|---|
| Steps `main` `75329fef...` | Git-Tree 2.219 Einträge, 1.931 Dateien, großes `research/` | voll geprüfte Bibliothek, sichere Rechte, ausführbare App |
| Steps Engineering | `app/` und `src/steps/` sind überwiegend README-Platzhalter; Struktur-CI erfolgreich | Chord-/Drum-/MIDI-/Audio-/UI-Tests bestanden |
| Steps Knowledge | bestehender `music-harmony-coach`-Skill und Grundschemas; Registry enthält `sources: []` | geprüfter Quellenindex, evaluierter Retriever oder fertiger Lehrinhalt |
| Glide `main` `9e767bea...` | 3.53.0 nach Merge #75, Systeminventar 1.15 | komplettes grünes Release, unabhängiges Framework, lokale Copilot-Arbeit eingeschlossen |
| Glide lokale Übergabe | finaler Windows-Vollmodus 130/131 (Bildsichtung SKIP), `release_ready=false`; Plattform- und manuelle Restgates | Steps-Eignung und nativer Release-Nachweis |
| Historische Forschung | umfangreiche V6.6-/V6.7-Behauptungen, sechs Originaldokumente, 100 historische Prüf-/Entscheidungspositionen | App-Versionsnummer oder eindeutige, lizenzierte, kuratierte Quelle |

## 3. Zielarchitektur: eigene Domäne, geliehener Shell-Vertrag

```text
Glide-App ── Glide-Adapter ──┐
                             ├── gemeinsame neutrale Kits (erst nach Abnahme)
Steps-App ── Steps-Adapter ──┘      Theme / Window / Navigation / Persistence contracts
   ├── src/steps/  (pure music domain, timeline, chords, drums, export contracts)
   ├── app/        (desktop shell, UI, adapters, OS/audio ports)
   ├── knowledge/  (geprüfte Konzepte, Claims, Quellen, Semantik)
   └── research/   (fremdes/historisches Originalmaterial; nicht Runtime)
```

Die „2 Fenster“ werden als zwei **inhaltliche Hosts** beschrieben, bis die tatsächliche Tk-Widgetstruktur belegt ist. Die umgebende Oberfläche muss einschließlich einklapp-/ausblendbarer Seitenliste, Kopf/Logo, Toolbar, Icons, Such-/Editorflächen, Settings, Themes, Schriften, Fokus/Hotkeys und Fenstergeometrie erhalten bleiben. Neutraler Shell-Testhost: Seitenliste mit inerten Einträgen, trotzdem alle Shell-Funktionen; Steps aktiviert neue, musikbezogene Einträge über Adapter. Glide behält seine vorhandenen Task-/Planer-Aktionen.

## 4. Produktmodule in fachlicher Reihenfolge

**M0: reproduzierbarer Projektstart.** Steps-eigene Datei-/Cache-/Log-/Lockpfade; CLI/Starttest; Daten- und Domänenschemas; sicherer Exportpfad. **M1: Chord-Vertikalschnitt.** Akkordfolge, Transposition, Erklärungen, Undo, Speichern/Neuladen und unabhängige MIDI-Verifikation. **M2: Drum + gemeinsame Zeitachse.** Pattern, Loop, Velocity, Events, 4/4- und Tempo-Map, zusammen mit Akkorden als Type-1-MIDI. **M3: Erklär-/Wissensfunktionen.** Kontext, alternative Deutungen, belegte Quellen und didaktische Tests. Audio-Playback bedarf eigenem Umfangsentscheid vor fertigem MVP. Erweiterungen: DAW-Rundlauf, zusätzliche Theorie-/Stilbereiche, Vorlagen/Community, Audioengine, Accessibility/Performance und später Cross-Platform.

## 5. Quellenbibliothek und AI-Skill

Die Dateimenge ist kein Qualitätsindikator. Benötigt werden separate Schlüssel für **Werk → Edition → Asset/Datei → fachlicher Claim → Konzept/Übungsfall → Test**. Für jeden Claim: konkrete Quelle und Originalstelle, Rechte/Verwendungszweck, Fachprüfer, Notation/Stilkontext, Konflikte und Revisionsdatum. Skill liefert begrenzte kontextbezogene Retrieval-Hilfe, keine unüberprüfbare autoritative Musiklehre. Zunächst 3–5 Pilotsources und 5 komplexe Konzeptkarten, danach 20 geprüfte Ausgangsquellen, dann weitere Bestände – jeweils ohne neue öffentliche Fremdvolltexte.

## 6. Reuse-Strategie

**Schneller Weg:** Glide-Oberfläche in einer **separaten** Kopie als Testhost verwenden, ohne sofort ein Shared Framework auszuliefern. **Sicherer langfristiger Weg:** UI-/System-Verträge aus 1–2 realen zwei-seitigen Integrationen ableiten und unabhängig versionieren. **Zu vermeiden:** komplette `ListApp` als dauerhaftes SDK, Kopieren aller 25 Bausteine ohne Tests, Tasks-Modell für Musik missbrauchen, automatisch beide Repos synchronisieren.

## 7. Qualitätsziele (keine willkürlich erfundenen Messwerte)

Deterministische Domain-Goldentests, unabhängiger MIDI-Parser für Export, verifizierter Save-/Reload-Roundtrip und atomare Fehlerbehandlung, Plattformtests pro tatsächlichem Build, manuelle Tastatur-/Fokus-/DPI-Abnahme, klare Lizenz- und Provenienznachweise, keine leisen Datenverluste, messbare GUI-Performance und vollständige Traceability von Entscheidungen zu Code und Tests. Releasefreigaben fachlich, technisch und rechtlich getrennt.

## 8. Nicht abschließend entschieden

- Exakte Scope-Formulierung und Rolle der Drums (Step-Sequencer vs. Pattern-Ketten vs. Groove-Labor).
- Desktop-Zielplattformen und ob früh interne Audiowiedergabe zwingend ist.
- Repräsentation von Zeit, Tuning, Oktaven, Enharmonik, Slash-Chords und MIDI-Datenverlust.
- Lizenz-/Rechtekatalog aller bereits öffentlich abgelegten Drittressourcen.
- Shared Kit Packaging / Versionierungsstrategie / 2-Consumer-Gates.
- Public Release/Signierung, Formatmigration, Markenzeichen, GitHub-Regeln, Human QA.

**Arbeitsregel:** Die 40 W-, 34 G- und 26 DEC-IDs der früheren V3-Historie sind nicht mit den hier genannten acht Themen erledigt. Entscheidungen benötigen eigene IDs, Owner, Quellen-SHA, Status, Test und Restpunkt.
