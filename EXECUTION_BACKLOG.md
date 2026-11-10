# STEPS – operativer Startbacklog mit unabhängigen Abschlussbedingungen

**Stand:** 10.11.2026. **Status:** Priorisierter, dokumentierter Vorschlag; **kein** gestarteter Sprint, keine automatisch freigegebene Produkt-/Lizenzentscheidung. Dieser Backlog übersetzt [`ROADMAP_AND_RESOURCE_PLAN.md`](../roadmap/ROADMAP_AND_RESOURCE_PLAN.md) in einzelne Übergabeaufträge. Die vorhandene Glide-To-do-Planung bleibt unter eigenen IDs erhalten.

| Reihenfolge | Auftrag / Prompt | Tatsächlich benötigter Eingang | Erfolgskriterium | Blocker / Übergabe |
|---|---|---|---|---|
| **P0.1** | Rechte- und Public-Repository-Prüfung (`prompts/27_*`) | Steps Git-Tree `75329fef`, Original-/Lizenzregister, sachkundige Rechteentscheidung | kritische PDF-/MIDI-/HTML-Assets einzeln klassifiziert; Git-Historienrisiko und Veröffentlichungspfad protokolliert | Keine neue öffentliche Weitergabe ungeprüfter Originale |
| **P0.2** | Glide 3.53.0 Source Freeze (`prompts/02_*`) | **Vollständige lokale Glide-Arbeitskopie**, nicht nur hochgeladenes `app.pyw`; Commit `9e767bea` als Vergleichs-Snapshot | SHA pro Laufzeitmodul/Asset, Version, CI-/Native-/menschliche QA und offener Rest separat | Fehlende lokale Module/Fonts/Assets blockieren behauptete Vollfreigabe |
| **P0.3** | Produkt-ADR und Fensterbegriff (`docs/product/PRODUCT_STRATEGY_AND_MVP.md`) | Owner-Präferenzen, zwei Wireframes, 4 MVP-Optionen | schriftlicher ADR für 2-Pane/2-Toplevel, v0.1 Scope, Drums-Zeitpunkt, Zielnutzungsfall | Bis Owner-Beschluss nur reversible Spikes |
| **P0.4** | Erster Knowledge-Ingest (`prompts/25_*`) | rechtlich nutzbare Quellen und Volltext- bzw. Seitenbelege, aktuelle Source Registry | mindestens **ein tatsächlich belegter** Source→Extract→Claim→Concept→Test→Query-Durchstich, zweiter Import idempotent | Bei fehlenden Originalen/unklarer Lizenz: BLOCKED + begründete Registry-Metadaten, keine erfundenen Claims |
| **P0.5** | Reiner Music-Domain-Core (`prompts/08_*`) | genehmigte Notations-/Pitch-/Time-ADRs, Golden-Fälle | reproduzierbare T01–T16-Musiktests auf neutralen Objekten, keine GUI-/Cloud-Abhängigkeit | Anstehende Datenmodellentscheidungen explizit dokumentieren |
| **P1.1** | UI-Migrationsspikes B vs D (`prompts/26_*`) | Freeze, Fenster-ADR, Designregeln, definierte 30 Negativ-/Positivfälle | zwei begrenzte Shells mit identischer Abnahme; dokumentierte Kosten-/Risikoentscheidung | Kein voreiliger Full-Fork, keine Glide-Datenzugriffe |
| **P1.2** | Datenspeicher / Undo (`prompts/12_*`) | Music-Domain-Core + Migrations-ADR | 16 künstliche Speicher-/Recovery-Fälle bestanden, Projektdatei außerhalb Glide-UserData | keine Rückwirkung auf Glide-Daten |
| **P1.3** | Ein funktionaler Vertikalschnitt (`prompts/09_*`) | Core + UI + Storage | 4 Akkorde bearbeiten, transponieren, speichern/laden, beobachtbarer Nutzerablauf | keine 10 parallel ungetesteten Features |
| **P1.4** | MIDI-Dateiexport (`prompts/11_*`) | Ereignismodell + Format-/DAW-Testsetup | SMF importiert in zweite Software und Roundtrip der Ticks/Dauern belegt | Audioplayback ist **nicht** mit Dateiexport gleichzusetzen |
| **P1.5** | Wissensadapter (`prompts/15_*`) | geprüfte KB, 20+ Evaluationsfragen | korrekte Quellenauflösung, Alternativdeutungen, no-evidence-Resultate | Keine ungeprüften Claimtexte als Wahrheit ausgeben |
| **P2** | Drum-Grid/Audio und Release | explizite Owner-Scope-Freigabe, realer Proof of Value, Rechte-/QA-Gates | portable Funktion und Win/Mac/Linux-/Menschenabnahme | kein Releaseversprechen ohne Nachweis |

**Pflicht für jede Aufgabe:** `git status`, Commit-SHA, Quellreferenzen, `implemented/tested/released` als getrennte Statusachsen, Ausgabe-/Diff-Liste, neu/alt-Pfadmapping, Datensicherheits-Negativtest, `NOT_RUN`-Liste, Reviewername und offene Freigaben. Parallel arbeiten nur an unabhängigen Paths. Bei fehlendem Repo-Schreibzugriff: lokal auf Feature-Branch vorbereiten, nicht GitHub-Erfolg melden.

**Empfohlener einzelner Start:** P0.1 und P0.2 parallel starten; P0.3 nach Wireframe-/Prioritätsreview; P0.4 darf mit einer einzigen nachweislich verwendbaren Quelle beginnen. Erst nach bestandenem P0.2/P0.3 die beiden UI-Spikes.
