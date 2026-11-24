# STEPS – Arbeitsvertrag für Codex und andere Agenten

1. **Erst inventarisieren, dann verändern:** aktuelle `main`-SHA, `git status`, Quelle, Lizenz, Dateihashes, interne Verweise, offener Review.
2. **Preservation-first:** keine stillschweigende Löschung, kein Force-Push, kein Rewrite der Historie, keine automatische Entfernung historisch verschiedener Versionen. Exact duplicates sind nur Kandidaten.
3. **Verifikation:** Produkt-, Forschungs- und Archivstand nicht vermischen. `V6.6/V6.7` ist nicht automatisch die App-Version. Keine erfundenen APIs oder Testresultate.
4. **Domänengrenze:** `src/steps/` enthält später die pure und testbare Harmonielehre; `app/` ausschließlich Desktop-Start, UI und Integrationen; `knowledge/` enthält Fakten mit Provenienz.
5. **Musikmodell:** deutsches H/B vs. internationales B/Bb explizit, Enharmonik, Kontext, funktionale Mehrdeutigkeit und alternative Analysen bewahren.
6. **Datenherkunft:** eigene Notizen von fremden Originalen unterscheiden. Keine urheberrechtlich geschützten Volltexte, Screenshots, heruntergeladenen Web-Assets oder Drittanbieter-Quellcodes ungeprüft übernehmen.
7. **Arbeiten in PRs:** Branch, differenzierbare Schritte, Bericht zu Mappings/Integrität, Test-/Linkchecks, Review durch Menschen. Kein direktes Merge nach `main`.
8. **Qualitätsgates:** Syntax, Schemata, Tests, Indexe, Migration-Manifest, keine unerwarteten Dateiverluste und keine neuen binären Großdateien.
9. **Glide:** nur als möglicher technischer Reuse; externe Lizenzbedingungen prüfen, referenzieren statt unkontrolliert kopieren.
10. **Kritische offene Fragen:** markieren und in `research/gaps/` dokumentieren, nicht als entschiedenen Stand ausgeben.
11. **Sprachen und Notation:** neue sichtbare UI-/CLI-Texte sind lokalisierungspflichtig. Zielsprachen sind Englisch (`en`) und Deutsch (`de`); die UI-Sprache ist strikt von `INT`/`DE`-Notationskonvention, Tonhöhe und Projektdaten getrennt. Bis ein getesteter i18n-Kern existiert, keine ungetestete zweite Übersetzungslogik anlegen.
12. **Dokumentationspflege:** bei jedem PR die Cross-Domain-Matrix in [`docs/governance/CONTINUOUS_MAINTENANCE.md`](docs/governance/CONTINUOUS_MAINTENANCE.md) prüfen. Öffentliche neue Dokumente sind standardmäßig englisch; bestehende deutsche Originale und historische Quellen nicht still ersetzen. Dokumentation, Tests, menschliche Fachprüfung und Release getrennt ausweisen.

Primärer Kontext: `docs/project/`; Fachbestand `knowledge/`; Workflows `SKILL.md`.

## Glide Shell 0.6.2 (Desktop-Fundament aus Glide v1.0.2)

- **Paket & Herkunft:** Die produktive Desktop-Schicht (`app/`) baut auf der übernommenen [`glide_shell/`](glide_shell/__init__.py) (`SHELL_VERSION` `0.6.2`, Glide `v1.0.2`, Quell-Commit `7dcd8dc04366f88943fa17827882cef4d81421b8`, Systemversion `V1.86`, Lizenz `MPL-2.0`) auf.
- **Manifest & Unveränderlichkeit:** Dateien unter [`glide_shell/`](glide_shell/__init__.py) werden niemals manuell editiert. Integrität und Herkunft stehen in [`glide_shell/SHELL_MANIFEST.json`](glide_shell/SHELL_MANIFEST.json). Updates erfolgen ausschließlich über `shell_uebernehmen.py`; Verifikation lokal über `python3 -m glide_shell.selftest` (13 Checks).
- **Verbindliche Leitfäden & Portabler Designvertrag:** [`glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md`](glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md) (EN: [`glide_shell/AI_GUIDE_NEW_PROJECTS.md`](glide_shell/AI_GUIDE_NEW_PROJECTS.md)), [`glide_shell/STARTPROMPT_KI.md`](glide_shell/STARTPROMPT_KI.md) und [`glide_shell/DESIGN_RICHTLINIEN.md`](glide_shell/DESIGN_RICHTLINIEN.md) (P1–P6, B15, B11, B01/B16, B03, B10/B12/B14, WCAG AA, Fokus & Tastaturbedienung).
- **Framework-Skill:** [`.agents/skills/glide-shell/SKILL.md`](.agents/skills/glide-shell/SKILL.md) (Claude-Adapter: [`.claude/skills/glide-shell/SKILL.md`](.claude/skills/glide-shell/SKILL.md)).
- **Architekturgrenze:** `STEPS UI (app/) → STEPS-Adapter → Glide Shell (glide_shell/) / Music Core (src/steps/)`. `src/steps/` bleibt vollständig frei von `tkinter`, `glide_shell` und `app`. Keine Übernahme von Glide-Todo-Fachlogik (`ListApp`, `.glideexchange`, `GLIDE_DATA_DIR`).
