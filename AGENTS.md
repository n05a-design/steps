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

Primärer Kontext: `docs/project/`; Fachbestand `knowledge/`; Workflows `SKILL.md`.
