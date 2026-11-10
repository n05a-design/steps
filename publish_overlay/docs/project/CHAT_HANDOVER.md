# Projekt-interne Übergabe dieses Gesprächs – 10.11.2026


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Auftrag und Situation (USER)

Der Auftraggeber entwickelt **Glide**, einen Python/Tkinter-Desktop-Planer, weiter. Visual-Studio-Code/Copilot arbeitet aktuell an einem begonnenen Glide-Stand, um dessen Oberfläche und Infrastruktur als Ausgangspunkt für eine **eigenständige Musik-App Steps** vorzubereiten. Im hochgeladenen Screenshot ist Glide 3.53.0 als eine Fenstershell mit Seitenleiste und Start-/Arbeitsbereich sichtbar. Der Nutzer hat eine umfangreiche Glide-System- und Modulliste bereitgestellt und will möglichst viele technische Lösungen erhalten (Einstellungen, Logo-/Symboltechnik, Headline, Toolbar, Eingabefelder wie Suche, Fenster-/Seitenleiste einklappen/ausblenden, Fokus, Design-/Schriften, Hintergrundprozesse, QA, Entscheidungshistorie). Nur die spezifische Todo-Logik soll aus der zunächst schlanken Zwei-Bereiche-Ansicht verschwinden bzw. später auf Musikfunktionen umverteilt werden. **Alle Navigationspunkte zunächst ohne Funktionswirkung darstellen.** Nicht alle Alt-Funktionen sofort löschen: im Archiv dokumentieren, bei Bedarf adapterfähig konservieren.

Für Steps besteht eine noch wachsende Wissensbibliothek aus recherchierten Quellen, Beispielen, Konkurrenzunterlagen, Büchern, MIDI/Drum/Produktionsthemen. Sie soll durch neue Crawl-Aufträge und künftige Ordner erweiterbar sein; ein Skill soll während der Entwicklung wissenschaftliches und didaktisches Wissen abrufen. Frühere Overview und weitere Anhänge sind Basis und dürfen nicht durch eine kürzere, informationsarme Neufassung ersetzt werden.

Verfügbare KI-Umgebungen: ChatGPT (zwei Accounts), Claude, Gemini/Antigravity, GitHub Copilot in VS Code. Nutzeraussage am Dienstag 10.11.2026: ChatGPT-Tokens bis Mittwoch und Claude-Tokens bis Donnerstag erschöpft; Copilot verfügbar und für Glide verwendet. Ein zeitweiliges besonderes Modellguthaben bei Claude/Fable 5.2 wird vom Nutzer als Möglichkeit für den Repo-Abzweig eingeschätzt. **Produkt-/Tarif-/Modellverfügbarkeit wurde nicht unabhängig geprüft.** Projekte unabhängig vom Anbieter konzipieren und KI-Sitzungen anhand von HANDOVER, SHA und Qualitätsgates wechselbar halten.

## Konkrete Lieferwünsche

1. Sämtliche gelieferten Dokumente zuerst lesen/indexieren, zusammenführen, Dopplungen in der **kanonischen Darstellung** vermeiden, abweichende/historische Informationen aber verlustfrei archivieren.
2. Projekt-Overview, Widerspruchsregister, Nachweislücken, Roadmap, Chancen/Risiken und Entscheidungsdokumentation.
3. Genaue Prompts pro Arbeitsbereich, als Markdown-/README-Struktur, einschließlich kontrolliertem Rückbau auf zwei primäre Fenster/Bereiche.
4. Wiederverwendung des Glide-Fundaments möglichst breit, aber keine ungeprüfte Modulübernahme und keine automatischen Produktentscheidungen.
5. In GitHub dokumentieren, wenn sicher und möglich; alternativ vollständiges Download-ZIP. Bevorzugt eigener Branch/Draft-PR statt automatischer Änderung an `main`.

## Offene Interpretation

„Zwei Fenster“ kann entweder **eine Anwendung mit zwei vertikalen Hauptflächen** (Sidebar/Workspace, wie Screenshot) oder **zwei Tk-Toplevel-Fenster** meinen. Die technischen Prompts nehmen **erstere als reversiblen UI-Prototyp** an und benennen die zweite als Entscheidung, bevor top-level-Fenster umgebaut werden. „Alles außerhalb der zwei Fenster soll bestehen bleiben“ wird als „alle sonstigen cross-cutting technischen Fähigkeiten, nicht die inhaltliche Glide-Todo-Domäne“ interpretiert. Keine irreversiblen Codeänderungen ohne genauere Grenzziehung.

## Sonstige Kontextbelege

- Glide-Repo: https://github.com/n05a-design/glide-to-do
- Steps-Repo: https://github.com/n05a-design/steps
- Originalkonsolidierung vom 09.11.: Konflikte W-01–W-40, Lücken G-01–G-34, 89 Quellabdeckungszeilen, 39 unterschiedliche fenced blocks; alle im ZIP unverändert erhalten.
- Heute ergänzt: direkter Snapshot beider Git-Bäume, lokale AST des Glide-3.53.0-Skripts und Rechtewarnung wegen fremder Bücher im **öffentlichen** Steps-Repository.

## Übergabevertrag zwischen KI-Sitzungen

Jede Session endet mit `last_checked_date`, `repo`, `base_sha`, `work_branch`, `changed_paths`, `tests_run`, `tests_not_run`, `decisions_requested`, `risks_changed`, `next_prompt`, `blocked_by`, `copyright_status`; keine erfundenen Testerfolge. Der nächste Agent muss immer Repo-/Status-Diff und Quellen prüfen, bevor er an fremden Änderungen arbeitet.
