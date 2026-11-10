# P08 – Music Harmony Coach als quellgebundenes Skill-System

## Direkt nutzbarer Prompt

Überprüfe den bestehenden Entwurf `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md`, seine `references/` und den Root-Einstieg `SKILL.md`. Der vorhandene Skill ist ein Workflow-Entwurf, **kein trainiertes Modell**, und seine Existenz garantiert weder Discovery/Indexierung noch fachlich richtige Antworten. Der produktive Musikcode darf nicht unkontrolliert von einem LLM abhängen.

Definiere getrennte Fähigkeiten: (1) deterministisches Domain-Modell für Akkord-/Intervallberechnung, (2) Wissenssuche in rechtlich freigegebenen Claims, (3) didaktische Erklärung mit Quellanker/Unsicherheit, (4) optional kreative Vorschläge mit dokumentierten Defaults. Kein automatisches Zitieren aus ungelesenen PDFs, keine erfundenen Buchseiten, keine Wiedergabe fremder Notenfolgen oder geschützter Songs. Eingangsquellen mit `restricted_local` dürfen nicht an externe KI übertragen werden.

Implementiere (nach Quellenfreigabe) einen skillinternen Index über Source-/Claim-IDs, minimale strukturierte Responses, deterministische Golden-Test-Fragen für Cmaj7/C7/Cm7, H/B/Bb, Stufenfunktionen, Voice Leading, Modalität und Tonartwechsel, Konfliktfragen und 10 Negativfälle ohne Beleg. Plane 30 Evaluationen mit Grounding-Score, Halluzinationsrate, korrekt zitierter Fundstelle, Latenz/Kosten und manueller Review. Eval-Korpus muss eigene oder freigegebene Inhalte verwenden.

Schreibe eine Installations-/Discovery-Anweisung für Antigravity/andere Agenten **nach tatsächlich geprüfter Runtime-Unterstützung**, keine erfundenen Toolnamen. Eine versionierte Skillschnittstelle erlaubt Austausch des Providers; keine Geheimnisse oder API-Schlüssel ins Repo. Architekturentscheidungen und künftige Upgrades im Decision Register.

## Akzeptanz

Skill-Pilot mit belegbaren Claims, evalbarem Korpus, getrenntem Offline-Fallback und klaren Retrieval-/Rechtegrenzen; nicht nur ein längerer Markdown-Skill.
