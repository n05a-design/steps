# Unabhängiger Verifikationsplan für STEPS – von Text zu Nachweis

**Status:** hier definierte Quality Gates sind noch nicht als Steps-App-Tests ausgeführt. Ein Dokumentations-/CSV-Check kann ausschließlich die **Qualität von Dokumenten und Indizes**, nicht die Qualität einer musikalischen App nachweisen.

## 1. Vier Geltungsbereiche

| Bereich | Validierung | Nicht nachgewiesen durch |
|---|---|---|
| Fachwissenschaft | Source Locator + Fachreview + positive/negative Musikbeispiele | bloßes Konzept-README |
| Implementierung | Unit/Integration, IO, Performance, OS, Accessibility, Packaging | Glide-Historie, importfreie `app.pyw`-Analyse |
| Sicherheits-/Rechteprüfung | tatsächliches File-/License-/History-/Supply-Chain-Audit | Projekt `LICENSE` oder Dateiname |
| Dokumentationsprozess | linkbare IDs, Dateihashes, tracebare Anforderungen, überprüfte Snapshots | 24 Prompts oder ein ZIP allein |

## 2. Prüfgates und Stopbedingungen

- **Q0 – Baseline:** Repo-SHA, Branch, `git status`, präziser Lizenzscope, Quellmanifest, Originalhashes, fehlende Artefakte; bei dirty tree stoppen statt einen unprüfbaren Mix zu produzieren.
- **Q1 – Sicherheit/Rechte:** keine ungeprüften geschützten Assets als neue Downloads/ZIP; bestehendes öffentliches Archiv auf Risiken priorisiert prüfen; Security-Fall nicht mit Auto-Force-Push „lösen“.
- **Q2 – Shell:** Steps legt keine Glide-Files/Locks/Backups an, mutiert keine versteckten Todo-Objekte, alle 30 Shell-Szenarien (`S01–S30`) mit Laufstatus und Plattform; UI- und Code-Spikes unter gleichem Testvertrag gegeneinander prüfen.
- **Q3 – Musik-Domain:** notation, Pitch-Classes, enharmonisch, Chord-Qualitäten, Inversionen, Harmoniefunktionen und alternativer Kontext; Golden Tests + Counterexamples (`T01–T16` im Musik-Engineering-Dokument).
- **Q4 – Daten/Recovery:** Versionsmigration, Powerfail/Writefail/Lock/Read-only, Backuprestore, No-Glide-Touch, JSON/MIDI-Schemas.
- **Q5 – MIDI/Playback:** PPQ, delta→absolute and back, Tempoänderung, Taktwechsel, overlapping note-offs, missing device, channel mapping, SMF-0/1, DAW-Import. MIDI-Datei-Export beweist noch kein Playback.
- **Q6 – Knowledge:** mindestens ein *echter* legal zulässiger Batch durch Source→Claim→Concept→Test→Retrieval→Citation; Idempotenz bei zweimaligem Einlesen, History und alternativer Claim.
- **Q7 – OS/Release:** definierte Python/Tk-Version, Windows/macOS/Linux inkl. DPI/Accessibility, frische Datenroot, SBOM/Font-/Soundbank-Rechte, signierbarer Releaseprozess und menschliche Review.

**Keine Zahl von bestandenen Steps-End-to-End-Tests liegt in dieser Prüfung vor.** V2 registrierte bereits geplante 30 Shell-Szenarien, 16 Theorie-/Midi-Invarianten und 33 Untersuchungsdimensionen; diese sind keine Durchführungsbelege.

## 3. Standardisierte Evidence Record

```yaml
case_id: S01
product: steps
source_commit: null
snapshot_sha256: null
platform: null
python_version: null
tk_version: null
fixture_id: null
run_timestamp: null
command: null
result: NOT_RUN  # PASS | FAIL | BLOCKED | NOT_RUN
observed: null
expected: 'Start ohne Zugriff auf Glide-Benutzerdaten'
artifact_paths: []
reviewer: null
human_acceptance: PENDING
known_limitations: []
```

Ein Test ohne exakte Code-/Fixture-/Plattformzuordnung darf nicht als aktuelles Grün wiederverwendet werden. Automatische Tests, visuelle Abnahme, native OS-Tests, Produktfreigabe und rechtliche Zustimmung sind getrennte Statusachsen. Alte rote Befunde nicht aus Berichten herauskürzen.

## 4. Reproduzierbare Dokumentationsprüfung

`tools/verify_package_audit.py` prüft Vollständigkeit des Pakets, IDs, fehlerhafte *neue* interne Links, Core-Dokumente, 24 Prompts und SHA-MANIFEST. Historische Originaldateien haben erwartungsgemäß relative Links in ihre Original-Repositories; diese bleiben bytegenau erhalten und werden nicht als neue lokale Paketlinks bewertet. Der Scriptlauf ist **nur ein Paketintegritätstest**, keine Validierung aller Recherchebehauptungen. `manifests/REQUIREMENTS_TRACE_28.csv` muss für jede REQ-ID einen Quellenpfad und einen verbleibenden Prüfschritt enthalten. Neue Treffer oder 100% CSV-Befüllung erhöhen nicht automatisch die fachliche Testabdeckung.

## 5. Messmethodik statt zufälliger Benchmarks

- Gemessene Use Cases vor Änderung definieren, identisches Fixture und Tool-/OS-Set vor und nach Änderung, mehrere Läufe mit Warm-up, Median und p95 plus Rohdaten.
- Keine Glide-Performancewerte unkritisch zu Steps-SLOs machen. Für Steps werden cold start, 100/1.000/10.000 Events, Navigation/Redraw, Suche, MIDI-Export, Projekt-Load, Speicherpeak und UI-Responsiveness separat erhoben.
- Eine signifikante Regression ist bei gleichem Testprotokoll zu untersuchen; manuelle Sichtprüfung, Screenreader/Focus und Texteinhaltung sind nicht durch timing passes ersetzt.
- Test eines *ausstehenden* Features ist `NOT_RUN` oder `BLOCKED`, niemals `SKIP` ohne Grund und Freigabe.

## 6. Externer Audit ohne Bestätigungsbias

Audit-Reviewer erhalten vollständige Doku + **Gegenbelege**, nicht nur „grüne“ Ergebnisse. Die Prüffrage lautet nicht „ist der Plan überzeugend?“, sondern: „welche Behauptung ist falsch, unbegründet, nicht testbar oder zu teuer?“ Jeder P0-Eintrag erhält: Beleg, Gegenhypothese, alternatives Vorgehen, Testmethode, Entscheidungseigentümer und Restrisiko. Bei wesentlich neuer Evidenz ist ein ADR zu revidieren statt einen alten Text still umzuschreiben.

## 7. Abschlussstufen

**G0 dokumentarisch vollständig:** alle Anforderungen verlinkt, Source-Gaps ausdrücklich, keine ungewollten internen neuen Broken Links. **G1 technisch probiert:** zwei Shell-Spikes und Domain-Fixtures wirklich ausgeführt. **G2 MVP testbar:** hör-/exportierbare Progression, Save/Load, QA-Gates auf Zielplattform. **G3 veröffentlichungsfähig:** Rechte/Software-Supply-Chain, Benutzerabnahme, Release-Prozess. Aktueller STEPS-Stand: **G0 in Arbeit; G1–G3 NICHT ERREICHT**.
