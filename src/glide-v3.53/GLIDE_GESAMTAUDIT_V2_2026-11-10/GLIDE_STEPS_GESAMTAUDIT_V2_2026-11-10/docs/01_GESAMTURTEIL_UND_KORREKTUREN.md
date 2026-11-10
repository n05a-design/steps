# 01 — Gesamturteil und entscheidende Korrekturen

## Ergebnis in einem Satz

Glide bietet eine reichhaltige und dokumentierte **Anwendungsbasis**, aber **noch keinen unabhängig geprüften, versionierten Desktop-Kern**. Steps hat ein umfangreiches, teils problematisches **Forschungsarchiv**, aber noch keine geprüfte Musik-App und nur eine begrenzt nutzbare Knowledge Base. Die Verbindung ist aussichtsreich, wenn zuerst **Verhalten und Zustandsgrenzen**, danach **austauschbare Adapter**, schließlich **bewährt gemeinsame Pakete** entstehen.

## Verifizierte Bestände und Beobachtungseinheiten

| Beobachtung | Status | Konsequenz |
|---|---|---|
| Glide `main` am untersuchten SHA `9e767bea...`: `VERSION=3.53.0`, `GLIDE_SYSTEM_VERSION=1.15` | VERIFIED_REPO | Versionsangabe ist keine vollständige Releasefreigabe |
| Glide: 1.542 Dateien / 172 Verzeichnisse, ca. 315,12 MB unkomprimierte Git-Dateigrößen, davon 94 direkt unter `src/glide/` liegende Python-Hauptmodule | VERIFIED_REPO, Tree API | Kein Beleg, dass alle Dateien fachlich analysiert oder alle Module portierbar sind |
| Glide-Systemregister: 147 Features, 25 Kandidatenpakete, 311 Test-/Werkzeugdateien; `app.pyw` ist zentrale Monolithklasse | VERIFIED_REPO / Dokumentinventar | Keine automatische Framework-Freigabe |
| Schritte: `main` `75329fef...`, `VERSION=0.0.0-dev`, 1.931 Dateien / 288 Verzeichnisse, etwa 668,68 MB | VERIFIED_REPO | Musikimplementierung / Release nicht nachgewiesen |
| Steps: 60 PDFs, ca. 452 MB, 160 Gruppen identischer Git-Blobs mit 426 zusätzlichen identischen Pfaden und ~115,69 MB logischer Duplikatdateigröße | VERIFIED_REPO (Git-Tree-SHA und Größe) | Rechte-/Provenienz- und Speicherstrategie dringend, ohne pauschale Löschung |
| Steps `knowledge/sources/registry.yaml` enthält `sources: []`; `src/steps` / `app` haben README-Platzhalter; CI prüft Struktur/JSON-Syntax | VERIFIED_REPO | Grün der Strukturprüfung ist **kein** musikalischer oder UI-Funktionstest |
| Glide Dokument-QA: Windows 130/131 Schritte, ein Bild-Sichtschritt ausgelassen, `release_ready=false`; einige Plattformgates offen | DOCUMENTED_QA | Nicht als vollständiger `3.53 grün`-Abschluss ausgeben |
| Live-GitHub-Actions-Sichtung: Main-Prüfung am oben genannten SHA zuletzt `in_progress`, macOS-Paketworkflow `success` | VERIFIED_REPO (Zeitpunkt der Abfrage, dynamisch) | Vor Freeze den endgültigen Workflow-Status neu abfragen |

## Korrektur K1: Projekt-Freeze ist nicht gleich Produkt-Release

**V1:** Die erste Roadmap behandelte vollständige Windows-/Linux-/macOS-Abnahme, native Pakete und menschliche Sichtmatrix faktisch als Voraussetzung für jede Steps-Entkopplung. Das vermeidet Risiken, ist aber als **technische Abhängigkeitsregel zu streng**. Ein experimenteller, isolierter Steps-Branch darf an einem bekannten, eingefrorenen Glide-SHA beginnen, selbst wenn noch nicht jedes Release-Gate erfüllt ist, **wenn** die offenen Plattformrisiken explizit übernommen, alle betroffenen Schnittstellen getestet und keine Veröffentlichung oder Framework-Freigabe behauptet werden. Für eine **freigegebene** gemeinsame Bibliothek gelten dagegen strengere bilaterale Tests.

**V2:** drei getrennte Zustände: `BASELINE_SELECTED`, `SAFE_TO_EXPERIMENT`, `RELEASE_APPROVED`. Keinen durch anderen ersetzen. Die Entwicklung kann in getrennten Arbeitskopien parallel stattfinden; das Risiko bleibt transparent.

## Korrektur K2: Steps' Produktauftrag ist breiter als ein reiner Harmony Explorer

Die aktuell vom Inhaber beschriebene App umfasst **Chord- und Drum-Progressions, Harmonieforschung, MIDI-Export und Lernen**. Historische Research-Handovers verschoben Drum-Arbeiten für die damalige **Forschungsphase** nach hinten. Dies ist keine Erlaubnis, Drums und MIDI dauerhaft aus der Produktdefinition zu streichen. **V2 trennt Produktziel, erste technische Vertical Slice, MVP-Entscheidung und langfristiges Produktionsarchiv.** Der konkrete MVP ist noch nicht autorisiert. Musikproduktions-/DAW-Vollfunktionsansprüche der V6.x-Bibliothek sind ein eigener möglicher Ausbaubereich und dürfen nicht still zum App-Scope werden.

## Korrektur K3: Zwei 'Fenster' sind nicht hinreichend bestimmt

V1 entschied praktisch für zwei interne Arbeitsflächen. Aus den Nutzerangaben lässt sich aber **auch** lesen: zwei Hauptflächen, ein Fenster plus Nebenansicht oder zwei unabhängige Betriebssystemfenster. Technisch haben diese Varianten unterschiedliche Fokus-, Geometry-, Ownership-, DPI-, Lifecycle- und Persistenzverträge. V2 dokumentiert alle drei, wählt **nur als Referenzentwurf** ein `Tk`-Hauptfenster mit zwei austauschbaren Slots; eine Implementierung, die diese Entscheidung vorwegnimmt, erhält keine UX-Freigabe.

## Korrektur K4: 'Modulweise wiederverwenden' hat mehrere mögliche Betriebsmodelle

Dateien über Projekte kopieren ist nicht automatisch langfristige Wiederverwendung. Eine sofort veröffentlichte Framework-Library ist angesichts `ListApp` und WA-49 aber ebenfalls verfrüht. V2 bevorzugt ein **strangler-/adapterbasiertes Refactoring** mit gemeinsamer, zunächst interner Kern-API. Unabhängige Release-Zyklen, versionierte Abhängigkeits-Pins und Kompatibilitätsprüfungen sind Pflicht; kein automatisches Synchronisieren von `main`-Branches.

## Korrektur K5: Schema-Dateien sind keine fertige Musikdomäne

Die fünf Steps-JSON-Schemata enthalten Startstrukturen; `progression.schema.json` hat Akkorde nur als Strings und keine Positionen/Dauern, Rests oder Timingevents. `chord.schema.json` verlangt nur `root` und `quality`, ohne Tonhöhen-/Spelling-Garantien. `source.schema.json` definiert Metadaten, aber die Registry ist leer. Daraus folgen **keine** bereits belastbaren Akkordalgorithmen, MIDI-Roundtrips, Quellenbelege oder Migrationsverträge.

## Korrektur K6: Public-Repository-Rechte sind nicht bloß eine spätere Dokumentationsaufgabe

Im öffentlich sichtbaren Steps-Git-Baum befinden sich bereits zahlreiche fremde PDF-/Web-/Bildmaterialien. Die MPL 2.0 für Quellcode deckt diese fremden Inhalte nicht automatisch ab. Ein Rechteaudit sollte daher **vor weiterer Veröffentlichung, Redistribution oder zusätzlichem Ingest** stattfinden. Ein `git rm` entfernt historische Git-Blobs nicht aus Klonen/Commits. Keine destruktive Git-Historienoperation ohne separate Rechtsbewertung, Backup und ausdrückliche Autorisierung.

## Korrektur K7: Wissensbibliothek und Skill dürfen sich nicht als Wahrheitsschichten duplizieren

`research/` = Material/Fragen; `knowledge/` = eigene geprüfte, provienzierte Aussagen; `src/steps` = deterministische Regeln; `SKILL.md` = Routen, Aufgaben, Lese-/Antwortverfahren. Ein Skill ohne gefüllte Quell- und Konzeptregister hat keine automatisch validierte Wissensbasis. AI sollte analytische Unsicherheit sichtbar machen und nicht die deterministische Fachlogik ersetzen.

## Korrektur K8: Trennung von drei Schnittstellen- und Versionsachsen

1. **Produktversion** Glide 3.53 bzw. Steps 0.0.0-dev.
2. **Glide-System-Katalogversion** 1.15 (Dokumentationsstand, nicht Distributionsversion).
3. **Shared-Core-API-Version** existiert noch nicht. Sie darf erst nach implementiertem öffentlichen API-Vertrag und Bilateraltests eingeführt werden.

Zusätzlich getrennt: **Datenformat-Version**, **Skill-Version**, **Wissensbasis-Snapshot**, **Quelle-/Schema-Version** und **Build-/Release-Commit**. Falsche Gleichsetzung erzeugt stille Migrations- und Pflegefehler.

## Neue strategische Priorität

1. Nicht noch ein bloßes 1.500-Zeilen-Overview-Dokument produzieren: **tracebare Anforderungen, Entscheidungen und Nachweise** statt Textmasse.
2. Rechte-/Sicherheitsfragen des bestehenden öffentlichen Steps-Bestands parallel zu Glide-Release-Audit einschätzen.
3. Shell-Verhaltensvertrag vor Code, aber keinen Big-Bang-Refactor.
4. Eine einzige vertikale Funktion (z. B. leere Shell + persistenter Akkordwechsel) durch die komplette Architektur führen und daran Qualität zeigen.
5. Erst danach die gemeinsame Kern-API über **beide** Produkte testen und versionieren.

**Gesamturteil:** Die Architekturvision ist stimmig; der aktuelle Reifegrad von Code-Reuse, Knowledge-Qualität, Reproduzierbarkeit und Release-Abnahme liegt jedoch deutlich hinter der Dokumentationsfülle zurück. Das größte Managementrisiko ist das Verwechseln von *viel vorhandenem Material* mit *einem getesteten, wiederverwendbaren System*.
