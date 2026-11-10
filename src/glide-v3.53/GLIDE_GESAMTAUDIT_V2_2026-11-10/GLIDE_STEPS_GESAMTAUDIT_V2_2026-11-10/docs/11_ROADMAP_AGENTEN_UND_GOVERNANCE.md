# 11 — Neue Roadmap, Ressourcen und Agenten-Governance

## Gegenüber V1 geänderte Sequenz

V1 hatte G0–G8 mit Release-/Baseline-/Erprobungsabhängigkeiten, die teilweise unnötig seriell wirkten. V2 trennt vier *parallel mögliche* Arbeitsstränge (A Glide-Stabilität, B Rechts-/Quellenprüfung, C Core-/Shell-Architektur, D Musik-Domain-/Knowledge-Entwurf) von **harten Integrationsgates**. Ein Prototyp ist mit bekanntem Risikostand möglich, aber keine gemeinsame Packagefreigabe ohne bilaterale Prüfungen.

| Phase | Arbeitsprodukt | Eingang | Exit- und Nichtfreigabe-Grenze |
|---|---|---|---|
| P0 Audit einfrieren | Git-SHA, Test-/Rights-/Doku-Inventar, zuständige Quellen, offene Tasks | lesender Zugriff | vollständige Baseline dokumentiert; lokaler Copilot-Stand gesondert, nicht geschätzt |
| P1 Glide stabilisieren (eigener Strang) | Glide 3.53-Release-Matrix, bekannte Fehler und finale Version/Commit | `P0`, Copilot-Branch | keine falsche neue Releasefreigabe; rote/skipplige Gates getrennt |
| P2 Rights/Knowledge Triage (parallel) | Dateibasiertes Rechte-/Hash-/Korpusregister, Quellstatus | Steps-Tree | kein neu verteiltes Fremdmaterial, erste validierte SourceIDs |
| P3 Zwei-Fenster/Shell RFC | Zustandsautomat, Komponentenmatrix, 3 UX-Varianten, Schnittstellen | Glide UI-Doku + Nutzerauftrag | `W1/W2/W3` vom Inhaber entschieden vor produktiver UI-Implementierung |
| P4 Core-Spike | minimaler Port, neutraler Import und Regression in isolierten Checkouts | P0/P3, Portauswahl | kein Glide-Datenkontakt, keine neue UI-Domainkopplung, isolierte Tests |
| P5 Steps-Domain-Vertical Slice | deterministischer Pitch/Chord/Time/Step + save/load, golden tests | P0, initiale Schema-RFC | reine Domain, passender Schema-/Undo-/Migrationstest |
| P6 Shell + Domain Integration | Produktidentität, 2 Views, Commands, Datenisolation, Save/Undo | P3–P5 | UI-Akzeptanz und Sicherheit, keine Cross-App-Abhängigkeit |
| P7 Drum-/MIDI-Vertical Slice | Drumgrid, gemeinsame Zeitbasis, SMF-Export/Import | P5/P6 | expliziter Exportvertrag und negative Parser-/Timingtests |
| P8 Knowledge/Skill-Evidence | Source Registry + 10–20 kontrollierte Concepts und Evaluation | P2/P5 | Recht/Bibliographie/Schema/Relevance-Halluzinationsgates |
| P9 Shared Core Decision | eigenes `desktop_core` oder bewusstes selektives Vendoring | P4/P6, **zwei Consumer** | API-/Lizenz-/Version-/Upgradeplan genehmigt |
| P10 Steps RC/Release | Paket, native Tests, Schrift/Rechte/Accessibility, Bedienabnahme | P6–P9 nach gewähltem MVP | echte Produkt-/QA-Freigabe, keine falsche Repo-Structure-Green-Klausel |

## Technische kritische Pfade

- `P0 → P3 → P4 → P6` ist der sichere Shell-Pfad.
- `P0 → P2 → P8` ist die unabhängige Knowledge-/Rechtekette.
- `P0 → P5 → P7` ist musikalische Domain/SMF-Kette; erst wenn Zeit-/Duration-/Tempo-Schema stabil ist, MIDI implementieren.
- `P4 + P6 → P9` schützt vor dem Fehler, ein ungetestetes Framework zu veröffentlichen.
- Die vollständige Glide-3.53-Freigabe `P1` ist **kein harter Blocker** für dokumentierte experimentelle Steps-Spikes, aber ein Risikotransfer mit Vorsicht, und für eine gemeinsam freigegebene Core-Version ist eine belastbare Glide-Integration nötig.

## KI-Agentenverteilung als überprüfbares Arbeitsmodell

**Copilot / laufende VS-Code-Arbeitskopie:** nur bestehende Glide-Fortsetzung und regressionssichere Schlussabnahme. Kein Steps-Code und kein zweiter Agent mit Schreibzugriff auf denselben Arbeitsbaum. Der aktuelle lokale Branch/Working Tree ist uns nicht zugänglich: Keine Rückschlüsse aus GitHub als Ersatz.

**Claude Fable 5.2:** Nach Nutzervorgabe verfügbar ab persönlichem Reset; Anthropic veröffentlichte Fable 5.2 am 09.11.2026, gesonderte Kontingente/Accountberechtigungen sind nicht von uns verifizierbar. Für schwierigen bounded Task (z. B. `ListApp` dependency/side-effect audit oder Shell-RFC) sinnvoll; *nicht* unbegrenzt „baue alles“ ohne Gate/Kontext. Hochwertige, begrenzte Inputs + klare Outputdiagnose statt Tokenbudget unkontrolliert in redundante Dokumente investieren.

**Gemini/Antigravity:** unabhängig red-teamendes Design-/Architekturreviews oder fachliche Musik-/Lizenzquellenprüfung. Kein Merge eigener Experimente in Glide ungeprüft.

**ChatGPT/Kodex und zweiter Account:** Requirements-/Source-Trace, Testspezifikationen, Gegenargumente, Dokument-Governance und getrennte Auswertung. Reuse derselben Kerninformationen durch versioniertes Artifact Manifest, nicht durch erneutes Erzählen des gesamten Chats. Unterschiedliche Modelle sind **keine** unabhängigen Fachquellen; nur unterschiedliche Prüfperspektiven.

## Parallele Entwicklungsarbeit

Jeder Agent besitzt **ein benanntes Epic**, einen eindeutigen SHA, Branch/Worktree und erlaubte Pfade. Keine zwei Agenten bearbeiten dieselbe Source-Datei gleichzeitig; gegenseitige Codeabhängigkeiten durch Stub-Port/RFC/Contract mit versioniertem Schema klären. CI/Git-Push/Merge/Tag/Releases werden nicht automatisch ausgeführt. Outputs: `scope`, `quellen`, `designentscheidung`, `diff`, `testmatrix`, `negativtest`, `nicht_geprüft`, `risiken`, `human_gate`. Ungeprüfte Änderungen sind Kandidaten, keine Umsetzungserfolge.

## Governance für Änderungen am Core nach Steps

- Produktwartung unabhängig: Ein Core-Release definiert Breaking Changes und Migrations-/Deprecation-Window; Glide und Steps können verschiedene gepinnte Versionen nutzen.
- Core-Autosync ist untersagt: Upgrade-PR je Produkt, CI-/UI-/Datenmatrix je Produkt, unabhängige Veröffentlichung.
- Für Bugfixes, die nur Steps betreffen, nicht übermäßig generisch werden; kein Core-Package-Zuwachs ohne zweiten Consumer / bewusstes Architekturreview.
- Aufbewahrung/History: Original-Belege und betroffene frühere Prüffehler bleiben datiert. Kein Stashing/Reset/Cleanup fremder Arbeitsbäume ohne Auftrag.
- Source of Truth je Thema: Glide-Systeminventar in Glide, Steps-Domain-Verträge in `src/steps`/`schemas`, Assets in Lizenzregistern, zentrale ADRs in `decisions`, Source Registry in `knowledge/sources`, Prüfstand in QA mit Commit/Runtime.

## Stop-Kriterien

`STOP-1` Cross-App-Nutzdatenpfad wird gelesen/geschrieben; `STOP-2` Regression in Glide-Produktfunktion durch Core-Refactor; `STOP-3` Agent kann Versions-/Quellstand nicht beweisen; `STOP-4` unbekannte Rechte an weiteren öffentlich zu übernehmenden Inhalten; `STOP-5` nichtfreigegebene W1/W2/W3-Entscheidung in produkthaltigem Code; `STOP-6` fehlende Migrations-/Backups bei Schemaänderung; `STOP-7` Tk-Thread-/Focus-Lifecycle unsicher; `STOP-8` vermeintlich 'grüner' Test wurde nicht ausgeführt oder hat relevante Skips. Diese Stopps gelten nur für die betroffene Änderung, kein pauschaler Stillstand aller parallelen unabhängigen Dokument-/Forschungsarbeiten.
