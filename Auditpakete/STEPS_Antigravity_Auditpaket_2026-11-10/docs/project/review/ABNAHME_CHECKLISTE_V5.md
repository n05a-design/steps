# Abnahmeliste: Antigravity-Gesamtaudit STEPS V5

## 0. Reproduzierbarkeit

- [ ] Lokalen und Remote-HEAD mit Datum, Commit und Branch dokumentiert; Änderungen während des Audits im Delta erfasst.
- [ ] Alle Dateipfade und Dateitypen erfasst, mit Scope-/Exclusion-/Fehlerstatus.
- [ ] Ungetrackte, ignorierte, LFS- und verschachtelte Repository-Bestände angemessen behandelt.
- [ ] Quelleninventar, Verzeichnisinventar, SHA-Register, Duplicate-Gruppen und Original-/Konsolidierungs-Trace erzeugt.

## 1. Inhalt und historische Traceability

- [ ] Jede verifizierbare Textquelle wirklich gelesen und mit Hash-/Zeilenankern versehen.
- [ ] Externe Binär-/Urheberrechtsquellen separat klassifiziert; `METADATA_ONLY` nicht als Lektüre ausgegeben.
- [ ] V1/V2/V4-Reviews, sechs Projektoriginale, Research-Handover, mindestens 29 aktuelle Prompts und alle Quellen-/Claim-Manifeste abgedeckt.
- [ ] 40 historische Konflikte, 34 Lücken, 28 REQs, 33 Auditdimensionen und neuere Registereinträge rückverfolgbar.
- [ ] Neue Konflikte von historischen Statuswechseln unterschieden; keine Informationen durch Deduplikation verloren.

## 2. Glide-3.53.0 → STEPS

- [ ] Nutzerentscheidung als **Zielrichtung** korrekt erfasst; Technik nicht vorab als implementiert behauptet.
- [ ] Origin und `src/glide-v3.53/` per vollständigem Hash-/Tree-/Asset-/Modulvergleich geprüft.
- [ ] UI-/Shell-/Daten-/Taskfunktionen konkret in Keep/Adapt/Isolate/Remove-later klassifiziert.
- [ ] STEPS-Datenroot von Glide isoliert; negativer Testplan für Taskaktionen/Dateischreiben spezifiziert.
- [ ] Alternative Shell-Strategien nach identischen Kriterien bewertet, ohne Baseline-Entscheidung zu ignorieren.
- [ ] `src/steps-0.00` vs `src/steps` und historische rote CI reproduziert beziehungsweise der neue Stand geprüft.

## 3. Produkt / Domain / Wissen

- [ ] Produktvision, Chord-/Drum-Scope, Didaktik, MusicTime/SMF, Offline-Prinzip und MVP als getrennte Statusachsen erfasst.
- [ ] Notations-/Enharmonik-/alternativen Theorieanalysen mit Gegenbeispielen abgesichert.
- [ ] KB-Registry und erste belegbare Ingestion-Möglichkeiten bewertet; Skill nicht mit Wissen verwechselt.
- [ ] Quellen-/Assetrechte und Git-Historienrisiken ausgewiesen, ohne pauschale Rechtsfreigabe.

## 4. Qualität / Abschluss

- [ ] Tatsächlich ausgeführte Prüfungen mit SHA, OS, Python/Tk, Befehlen, Exitcodes und Logs erfasst.
- [ ] `SKIP`, `FAIL`, `BLOCKED`, `NOT_RUN` nicht als `PASS` gezählt.
- [ ] Vollständige Befundmatrix, P0/P1/P2/P3, Zielstruktur, kontrollierter Migrationsplan, Rollback und Owner-Entscheidungen vorhanden.
- [ ] Persistenter Wiederaufnahmestand (`STATE.json`, `NEXT_SESSION_HANDOVER.md`) vorhanden.
- [ ] Erst bei nachgewiesener Quellenabdeckung vollständigen Abschluss behauptet.
