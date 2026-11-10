# 13 — Gegenüberstellung des bisherigen und neuen Untersuchungsstands

| Untersuchungsfeld | V1: bisheriger Stand | Defizit / korrigierte Annahme | V2: tatsächliche Erweiterung | Verbleibende Unsicherheit | Nächste konkrete Maßnahme |
|---|---|---|---|---|---|
| Gesamtübersicht | ~911-Wörter-Overview, großer historischer Anhang als Link | zu stark verdichtet, fehlende Anforderungsrückverfolgung | 14 kanonische Audit-Dokumente plus Tabellen und Risiko-/Entscheidungsmatrix | tatsächliche lokale Änderungen unbekannt | Anforderung→Code→Test→Abnahme in Worktree koppeln |
| Repository-Bestand | Git-Tree-Zählungen, Dokumentenlinks | keine detaillierte Größen-/Duplikatdimension | Glide 1.542 Dateien/315 MB; Steps 1.931/669 MB, 60 PDFs/452 MB, 160 sha-Dupgruppen | History/LFS/echte Dateiinhalte/Legality | lokales Metadaten-, Rights- und Inhaltsaudit |
| Codebasis | 94 Module, 25 Paketkandidaten | abstrakter Hinweis, unzureichender Importnachweis | viele separate Module direkt auf importierte Glide-Pakete geprüft, kritische Ketten beschrieben | vollständiger App-Monolith AST/Runtime fehlt | AST-/side-effect-/UI-mutation Graph mit Prüfprogramm |
| Shared-Core-Strategie | 'erst alle Release-Gates, dann Shell/Core' | experimentelle Iterationen unnötig blockiert | Base Freeze, Core candidate und Release strikt getrennt; 5 Architekturoptionen | reale Aufwands-/Performancekosten | kleiner Spikereview A-vs-C/D mit synthetischer Regression |
| Zwei-Fenster-UX | zwei interne Slots als Default | Nutzerentscheidung vorweggenommen | W1/W2/W3 plus Zustands- und Layoutverträge | tatsächlicher gewünschter OS-Fenstertyp | vom Nutzer visuell/technisch bestätigen lassen, bevor produktiv implementiert |
| Glide-Verhalten erhalten | allgemein 'Shell bewahren' | wenig komponentengenaue Erhalt-/Entfernungsregel | UI-Komponentenmatrix, Commands, Action-/Lifecycle- und Negativtests | konkrete Widget-IDs/Visuals aus aktuellem Python | kontrollierter UI-Tree-/Screenshot-/Bedienlauf |
| Produktumfang Steps | Harmony-MVP, Drums/MIDI später | neuer Nutzerauftrag nicht vollständig widergespiegelt | Ziel Chord+Drum+MIDI+Lernen, research/MVP/vertical slice getrennt | finale MVP-Grenze | Scope-ADR mit Prioritäten/Benutzerflüssen |
| Musikmodelle | allgemeiner Theory-Vorschlag | Schemas nicht einzeln bewertet, musikalische Zeit fehlt | 5 Schema-Findings; Pitch/Chord/Voicing/Time/Drum/SMF-Roundtrip-Tests | noch kein ausführbarer Domain-Code | Versionierte Schema-RFC + golden fixtures |
| Knowledge | Archiv, Registry, Skill grob | Rechte/Claim/Migrationskonflikte | vier Reifegrade und Ingestion-/Eval-Pipeline, Public-/Private-Filter | Einzelquellenrechte/fachliche Zitierqualität | 20 repräsentative SourceCards mit Rechtsprüfung |
| Bibliothek/Urheberrechte | pauschale Warnung | öffentliches Fremdmaterial unterschätzt | 60 PDF/452 MB, Third-Party-Assets und History als dringendes eigenständiges Gate | juristische Bewertung pro Datei | Rights-Triage vor weiterem Upload |
| Tests | Glide QA + Steps CI erwähnt | CI-Grün semantisch überschätzt | tatsächlichen Steps-Strukturtest gelesen, Testpyramide und Freigabeachsen beschrieben | keine hier ausgeführten Produkt-/GUI-Tests | isolierte lokale CI-/native Läufe zum konkreten SHA |
| Agenten | 17 fast gleich lange Prompts | breite Textduplikation, wenige spezifische Input-/Diff-/Negativtestcontracts | neue aufgabenspezifische, sequenzierte Prompts + ein gemeinsamer Vertrag | Toolkontext, tatsächliche Agenten-Berechtigungen | jeden Prompt auf einem realen kleinen Epic evaluieren |
| Privacy/Open Source | Uploadwarnung, MPL-Hinweis | keine filewise Veröffentlichungsberechtigung | Public/Private-Grenzen, persönliche Pfade, Git-Historie | Rechts-/Sicherheitsprüfung | getrennt redaktionierter Docs-PR nur nach Human-Review |
| Dokumentenpflege | neue Markdown-Dateien neben historischen | Gefahr zweiter Autorität | alte ZIP unverändert archiviert, V2 als Audit-Layer, kanonische Repo-Quellen referenziert | Repoübernahme kann Konflikte erzeugen | GitHub-Mapping, Links, Status und Owner abnehmen |
| Langfristige Nachhaltigkeit | Core-Versionierung erwähnt | kein Upstream/Downstream-Supportmodell | API-Version/Deprecation/Pin-/Cross-Consumer-Test und unabhängige Releases | Aufwand unbekannt | Governance-ADR nach zweitem Consumer |

## Ehrliche Restgrenzen

**Kein Volltext-Claim:** Das ganze Research-Archiv wurde nicht seitenweise gelesen; zahlreiche PDFs/Buchoriginale/Zips und ältere Library-Dateien sind zwar im Tree sichtbar, aber nicht einzeln fachlich geprüft. **Kein Code-Test-Claim:** Glide/Steps wurden in dieser Audit-Umgebung nicht ausgeführt; die vollständige `app.pyw` nicht AST-validiert; Windows/Linux/macOS UI und echte Nutzerdaten nicht getestet. **Kein Rechtsgutachten:** Aus Dateinamen und öffentlichen Metadaten lässt sich keine einzelne Lizenz abschließend beurteilen. **Kein Produktentscheid:** W1/W2/W3, MVP, Core-Release und exakte Steps-Bundle-ID sind nicht freigegeben.

## Was die Qualität von V2 überprüfbar verbessert

- Empirische Dateizahlen/Hashes statt Vermischung mit historischen Reports.
- Explizite Verifikationsstufen für Repo, dokumentierten Test, Plan und fehlende Information.
- Konkrete negative Testfälle und Daten-/Thread-/Windows-/macOS-/Linux-Risikoverträge.
- Gegenprüfung konkurrierender Architektur-, Scope- und Timing-Alternativen.
- Einzeldatei-Schemaanalyse und klare Grenze zwischen strukturellem CI und Fach-Implementierung.
- Klarer menschlicher Entscheidungspfad und striktere öffentliche Quellen-/Rechteprüfung.
- Originale V1-Paket bytegleich bewahrt, im neuen aktuellen README als Historie markiert.

**Fazit:** V2 ist deutlich belastbarer als **Entscheidungs- und Arbeitsgrundlage**, aber keine vollständige Anwendungscode-, Lizenz- oder Forschungs-Peer-Review. Der nächste Qualitätssprung erfordert lokale Lauf-/Quellenprüfung mit echten isolierten Tests und per-File-Rechte-Review, nicht ein weiteres generisches Textdokument.
