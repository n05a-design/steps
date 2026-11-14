# Auftrag: Unabhängiges Gesamtaudit des STEPS-Musiktheoriekerns, der aktiven Skills und der Wissensbasis

## Rolle und Ziel

Du prüfst als unabhängiger Auditor für Musiktheorie und Software das Repository `n05a-design/steps` auf Revision `22f3f5f348d060abfd4e2ffc917d0c95a639441e`.
Du sollst nicht bestätigen, was die Dokumentation behauptet. Du stellst selbst fest, ob Implementierung, Tests, Skills und musikalische Aussagen korrekt sind, und belegst jede Feststellung.

Beigefügt sind:
- `STEPS_FABLE_5_2_CONTEXT_PACK.md`: verifizierte Baseline, Modul- und Skill-Landkarte, Register, ausgeführte Prüfungen
- `STEPS_FABLE_5_2_AUDIT_SCOPE.md`: Prüfmatrix mit IDs (K, S, W, T, A, H) und Prioritäten

## Verbindliche Regeln

1. **Prüfbasis.** Lies nur Dateien auf der genannten Revision. Weicht dein Checkout ab (`git rev-parse HEAD`), nenne die Abweichung und prüfe trotzdem gegen `22f3f5f`.
2. **Unabhängigkeit.** Abschnitt 7 des Kontextpakets und alle Aussagen in Repository-Dokumenten, Auditberichten, Statusfeldern (`VERIFIED_TRUE`, `PASS`, „100 %“) sind Behauptungen. Übernimm keine davon ohne eigene Prüfung. Leite Sollwerte aus Definitionen, mathematischen Herleitungen oder überprüfbaren Fachquellen ab, nicht aus STEPS-Code oder STEPS-Testdaten.
3. **Keine Erfindungen.** Nenne keine Datei, Funktion, Zeile, Quelle oder Seitenzahl, die du nicht gelesen hast. Hast du einen Test nicht ausgeführt, kennzeichne ihn als `NOT_RUN`.
4. **Keine Änderungen.** Ändere weder Produktivcode, Skills noch Wissensdaten. Erstelle keine Commits, Pushes oder PRs. Experimente nur in einer Kopie oder einem temporären Verzeichnis.
5. **Sicherheit und Rechte.** Lies und zitiere keine Werte aus `scripts/historical_secret_baseline.json`, `tests/fixtures/synthetic_secrets.json` oder Secret-Scan-Ausgaben. Übernimm aus Fachquellen höchstens kurze Belegstellen mit Fundort, keine Volltexte. `research/`, `archive/`, `source_archive/` und `src/glide-v3.53/` nur gezielt öffnen, wenn ein Prüfpunkt es verlangt.
6. **Notation.** Halte deutsches H/B und internationales B/B♭ in jeder Aussage auseinander. Enharmonische Schreibweisen sind verschiedene Objekte. Bei Mehrdeutigkeit nennst du alle vertretbaren Analysen.
7. **Bestanden ist nicht korrekt.** Ein grüner Test belegt nur seine Assertion. Eine aufgelöste Referenz belegt nur ihre Existenz.

## Vorgehen

Arbeite die Schritte in dieser Reihenfolge ab. Schreibe Zwischenergebnisse nur stichwortartig mit. Ausführlich wird nur der Abschlussbericht.

1. **Prüfbasis bestätigen.** Revision prüfen, Kernsuite ausführen (`python -B -m unittest discover -s tests -p "test_*.py"`), Python-Version notieren (CI: 3.11 und 3.12). Eigene Proben aus dem Repository-Root mit `python -B -c "from src.steps.progression import resolve_roman_degree; …"`. Das Paket ist nicht installierbar, Importe laufen über `src.steps`. Weicht ein Ergebnis von Abschnitt 3 des Kontextpakets ab, halte es als Befund fest.
2. **P0 prüfen** (K01, K02, K03, K05, K07, K11, W01, W08). Code lesen, Verträge gegen `docs/theory/API.md` und `docs/IMPLEMENTATION.md` abgleichen.
3. **Unabhängige Gegenproben.** Für jeden P0-Bereich mindestens 10 eigene Fälle mit hergeleitetem Sollwert ausführen, darunter Grenzfälle und ungültige Eingaben. Bei Verdacht ein minimales reproduzierbares Gegenbeispiel bauen, als Python-Einzeiler oder kurzes Skript.
4. **P1 prüfen** (K04, K06, K08–K10, S01, W02, W04, W06, W07, T01–T03, T05, A03). Danach P2 und P3, soweit das Budget reicht.
5. **Vorhandene Ergebnisse abgleichen.** Golden Cases, Benchmark, Claim-Register und frühere Audits (H01, H02) gegen deine Ergebnisse halten.
6. **Befunde, Abdeckung und Restrisiken dokumentieren.**

## Pflichtuntersuchungen

**D1 Musiktheorie.** Leite unabhängig her und vergleiche mit der Ausgabe von STEPS: Notennamen und MIDI (inkl. Cb, B#, Doppelvorzeichen, Oktavgrenzen), deutsche und internationale Schreibweise, Intervalle und Umkehrungen, Akkordrezepte aller `CHORD_TEMPLATES`, Stufenakkorde in Dur und Moll, Zwischendominanten, Slash-Bässe, Umkehrungen und Generalbassfiguren, Transpositionsinvarianz (Tonklassen und Schreibweise), Stimmführung, mehrdeutige tonale Deutung (PROG-001).

**D2 Algorithmik.** Prüfe Invarianten, Rundung (`frequency_to_midi`), Off-by-one bei Oktaven und MIDI 0/127, ungültige Zustände, unerwartete Eingabetypen (`bool`, `float`, Leerzeichen, Unicode-Vorzeichen), Determinismus und Optimalität des Stimmführungssolvers, verschluckte Ausnahmen, Widersprüche zwischen Docstring, API-Referenz und Verhalten.

**D3 Tests und Golden Cases.** Prüfe, ob Assertions die beabsichtigte Eigenschaft treffen und ob Sollwerte eine von STEPS unabhängige Herkunft haben. Teilen Referenz-Evaluator und Laufzeitkern gemeinsame Fehlerquellen? Welche Fehlerklassen aus D1/D2 würden unentdeckt bleiben? Prüfe mindestens 20 Golden Cases aus allen Domänen M01–M12 fachlich, davon mindestens 10 `SPECIFICATION_EXAMPLE`. Prüfe dazu den Benchmark-FAIL `KB-M11-ALTER`.

**D4 Skills.** Prüfe für `steps-knowledge-curation`, `SKILL.md` (Router) und den historischen `music-harmony-coach`: fachliche Korrektheit, widerspruchsfreie Anweisungen, Ein- und Ausgabeschemata, Pfad- und Quellenverweise, Validierungsregeln, Unsicherheitsbehandlung, Halluzinationsanreize, Prompt-Injection über importierte Inhalte, Überschreib- und Datenverlustrisiken, Reproduzierbarkeit. Kernfrage: Kann ein Skill oder Agent Inhalte als `VERIFIED`, `DONE_VERIFIED` oder freigegeben markieren, ohne dass ein ausreichender Nachweis vorliegt? Prüfe das auch für die Freigabe in `src/steps/progression/reviewed.py`.

**D5 Datenkette.** Verfolge für PROG-003 und PROG-009 den Weg Quelle → Claim → Konzept → Relation → Skill → Algorithmus → Test → Ausgabe von `app/knowledge.py`. Prüfe Referenzidentitäten, Schemaverträge, Notationskonvention, Fingerabdruck- und Versionsbindung, konkurrierende Deutungen, Verhalten bei fehlendem Beleg.

**D6 Architektur.** Bewerte die Eignung für Chord-Editor, Progression-Editor, Drums/Rhythmus, Piano-Lernmodule, MIDI, Wissensadapter, Harmony Coach und Desktop-Integration. Trenne nachgewiesene Probleme (mit Gegenbeispiel oder fehlender Fähigkeit) von Designpräferenzen. Schlage Refactorings nur mit nachweisbarem Nutzen vor.

**D7 Historische Behauptungen.** Prüfe drei bis fünf Aussagen wie „100 % verifiziert“, „vollständig“, „alle Tests bestanden“ oder „unabhängig validiert“ aus `docs/audit/` und den über `archive/INDEX.md` verlinkten Berichten. Prüfe sie gegen `22f3f5f` und gib ihre tatsächliche Reichweite an.

## Befundstandard

Jeder Befund folgt diesem Schema:

```yaml
- id: F-<Bereich>-<Nr>          # z. B. F-K07-01
  priority: P0|P1|P2|P3
  severity: kritisch|hoch|mittel|niedrig
  scope_id: K07                  # aus der Prüfmatrix
  location: src/steps/progression/engine.py:resolve_roman_degree (Zeile)
  revision: 22f3f5f
  description: <ein Satz>
  reproduction: <Befehl oder Code>
  actual: <beobachtet>
  expected: <unabhängig hergeleitet>
  rationale: <musikalische oder technische Begründung>
  reference: <Definition, Herleitung oder Quelle mit Fundstelle>
  impact: <betroffene Komponenten>
  fix: <konkrete Korrektur>
  regression_test: <Testidee mit Ein- und Ausgabe>
  evidence: CONFIRMED|STRONGLY_INDICATED|HYPOTHESIS|NOT_VERIFIED|NOT_APPLICABLE
  test_status: RUN_PASS|RUN_FAIL|NOT_RUN
```

`CONFIRMED` erfordert eine ausgeführte Reproduktion oder eine eindeutige Codelesung mit Herleitung. Was du vermutest, aber nicht reproduziert hast, ist `HYPOTHESIS`.

## Abschlussbericht

Gliedere ihn so, ohne Wiederholungen:

1. **Managementzusammenfassung** (höchstens 15 Zeilen): Gesamturteil je Bereich, Anzahl Befunde je Priorität, wichtigste drei Risiken.
2. **Prüfbasis:** Revision, Umgebung, ausgeführte Befehle mit Ergebnis.
3. **Befunde** nach Priorität im Schema oben.
4. **Unabhängige Gegenproben:** Tabelle mit Fall, Sollwert, Herleitung, Ist-Wert, Status. Auch bestandene Fälle aufführen.
5. **Abdeckungsmatrix:** jede ID aus der Prüfmatrix mit Status `GEPRÜFT`, `TEILWEISE`, `NICHT_GEPRÜFT` und Grund.
6. **Historische Behauptungen:** Aussage, Fundort, tatsächliche Reichweite.
7. **Restrisiken und nicht prüfbare Bereiche.**
8. **Fortsetzung:** Gibt es offene Prüf-IDs, liste sie mit dem Grund, warum sie offen sind, und dem nächsten Schritt.

Behaupte keine vollständige Abnahme, solange ein Bereich `TEILWEISE` oder `NICHT_GEPRÜFT` ist. Rohlogs nur auszugsweise, wenn sie einen Befund belegen.

## Budget

Richtwert: Lies vor allem Code, Tests und Daten der P0- und P1-Bereiche. Öffne Kataloge und Golden-Case-Daten gezielt statt vollständig. Halte den Abschlussbericht bei etwa 8.000–15.000 Tokens. Reicht das Budget nicht, kürze P2 und P3, niemals P0. Nenne im Abschnitt „Fortsetzung“, was offen blieb.
