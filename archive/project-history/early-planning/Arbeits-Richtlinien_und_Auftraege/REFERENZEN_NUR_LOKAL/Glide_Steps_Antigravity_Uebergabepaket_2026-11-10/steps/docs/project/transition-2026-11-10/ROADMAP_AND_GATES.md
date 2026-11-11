# Phasenroadmap – abhängigkeiten- statt tokengetrieben

**Prinzip:** Keine festen Kalenderdeadlines aus Modellquoten ableiten. Jede Phase schließt mit einem überprüften Ergebnis und einem expliziten Stop-Gate; erst dann die nächste. Bestehendes `docs/roadmap/README.md` ist ein Platzhalter, dieses Dokument dient als Vorschlag zum erstmaligen Ausbau.

| Phase | Ziel und wichtigste Arbeit | Gate / Artefakt | Voraussetzung |
|---|---|---|---|
| R0 Sicherer Wechsel | Copilot-Arbeitsbaum, SHA, Deltas, lokale Prozesse, QA und Antigravity-Kontext | verifizierte lokale Übergabe; keine Datenverluste | sofort |
| R1 Glide 3.53.0 schließen | CI auf finalem `main`-SHA, Linux/macOS/Windows, Paket-/Native-Start, manuelle UI, offene WA | exakt referenzierte Gate-Matrix; keine offenen P0 | R0 |
| R2 Scope/Legal | PRD „Chord+Drum“, Rights-Triage öffentlicher Rohquellen, Branchschutz, App-/Skill-Versionen | Owner-ADRs, freigegebene Pilotquellen und PR-Governance | parallel zu R1 ohne App-Fork |
| R3 Domain-M0/M1 | pure Steps-Models, Codec, Chord-UI-Minimalflow, Save/Reload, transposition, MIDI unabhängiger Parser | 20 Goldentests + Negativfälle + erste echte Nutzerreise | R2 |
| R4 Shell-Pilot | 2 Inhalts-Hosts, inerte Sidebar im neutralen Testhost, Theme/Settings/Focus, genau 1–2 Glide-Kits | zwei Consumer-/Isolations- und Regressionstests | R1 + Architektur-ADR |
| R5 Drum-M2 | Step-Pattern, Loop, Tempo/Meter, Velocity/Swing, gemeinsame Timeline, Type-1 MIDI | zwei Tracks in DAW interoperabel; Save-/Undo-/Playback-Scope | R3 + R4 |
| R6 Knowledge/Skill | Rechtegeprüfte 3–5 Quellen, 5 Konzeptkarten, Claim-Layer, Skill-Eval; danach 20-Quellen-Batch | fachlicher Review, Quell-Trace, 10+ Negativfälle, Rechteprüfung | R2, parallel zu R3–R5 |
| R7 Integration | UI-Inhaltsflächen, Chord/Drum Editor, Inspector, Suche, Hinweise, Keyboard/a11y | kompletter synthetischer Nutzerflow auf finalem Commit | R5 + R6 |
| R8 Releases/Community | Cross-OS, Installers, BOM/Rechte, Sicherheits-/Performancegrenzen, Contribution, Release-Prozess | Produkt-/Engineering-/Rechtefreigaben getrennt; Release-Tag | R7 |

## Risikoanalyse / Opportunitäten

| Risiko | Wahrscheinlichkeit / Auswirkung (qualitativ) | Gegenmaßnahme | Chance |
|---|---|---|---|
| Glide-Monolith bleibt gekoppelt | hoch / hoch | kein Big-Bang-Fork, ein Modulspike, API-Ports | dauerhafte shared shell |
| parallele KI-Edits zerstören lokale Deltas | mittel / sehr hoch | exklusiver Editor, Branch/Commit/Hash, Handover | Anbieterwechsel ohne Kontextverlust |
| Fremdrechte im öffentlichen Archiv | unklar / sehr hoch | Rechteinventar, getrennte private Raw-Assets, juristische Prüfung bei Bedarf | sauber zitierbarer Wissenskatalog |
| undeterministischer MIDI-/Audio-Timing-Fehler | hoch / hoch | Eventmodell, Golden- und negative DAW-Tests | robuste Produzententauglichkeit |
| „Struktur grün“ wird als Produktfreigabe verstanden | hoch / hoch | unabhängige Domain- und Native-Gates | verlässliche Community |
| Skill wird zum unkontrollierten Volltext-Speicher | hoch / mittel–hoch | Claim-Retrieval mit Rights-Filter | erklärbare Fachassistenz |
| hohe KI-/Tokenkosten | mittel / mittel | kleine Aufgaben, feste Context-Snapshots, modelagnostische Checklisten | bessere Kontrollierbarkeit |

## Kriterien für Start der 2-Fenster-Extraktion

(1) Glide 3.53.0 eindeutiger, gesicherter Source-SHA; (2) unveränderte Glide-Produktfunktion und Testbaseline; (3) G1-Gates dokumentiert und akzeptiert; (4) Architekturbranch unabhängig vom Release; (5) Shell-Invarianten/Screenshots/Keyboard- und Save-Schutz; (6) Lizenz/Marke/Provenienz. Fehlt eines, nur weiter dokumentieren/testen.
