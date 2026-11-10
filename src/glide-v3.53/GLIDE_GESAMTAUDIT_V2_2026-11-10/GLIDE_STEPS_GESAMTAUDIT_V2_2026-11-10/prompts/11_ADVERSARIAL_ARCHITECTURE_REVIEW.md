# Unabhängiges Red-Team: alle Architekturthesen widerlegen versuchen

**Prompt-ID:** `11_ADVERSARIAL_ARCHITECTURE_REVIEW` · **Arbeitsart:** ANALYSE, keinerlei Code- oder Git-Änderungen · **Roadmap:** P0/P9

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Glide/Steps aktuelle Primärquellen, dieses V2-Audit, V1-Originalpaket, konkrete Ergebnisse der Prompts 02–10 und alle bezeichneten Quell-SHAs.

## Fachlich konkreter Arbeitsauftrag

Agiere als ausdrücklich skeptischer Principal Engineer. Prüfe für jede Behauptung: 'Core ist generisch', 'nur zwei Flächen', 'Datenmigration trivial', 'MPL deckt alles', 'alle Plattformen grün', 'MIDI ist einfach', 'Knowledge = Dateien', 'Skill vermeidet Halluzination', 'natives Tk ist überall identisch'. Suche jeweils Primärbeleg, Gegenbeispiel, versteckte Kosten und Widerlegungsprüfung. Vergleiche 5 Strategien: Big-bang Kopie, Framework zuerst, Strangler, Subtree/Vendor und Steps-Neu-UI. Lege alternative Prioritäten fest, wenn das öffentliche Rechtsrisiko höher ist als Shell-Feinschliff. Untersuche nicht nur Code, sondern Owner-Zeit, PR-/Branch-Kollisionen, Offline-Verfügbarkeit, Datenkorruption, OSS-Community, Versionierungsaufwand, Folgen künftiger Tk-Versionen, technische Schulden durch KI-Output und Benutzerzugänglichkeit. Verwende kein früheres Assistenzurteil ohne Prüfung. Widersprich ausdrücklich, wenn eine bisherige Empfehlung keine Evidenz hat.

## Reproduzierbare Abnahmen und Gegenproben

Reproduziere mindestens 10 verifizierbare Negativhypothesen oder markiere sie `NOT_RUN` und liefere ein prüfbares Testdesign. Wenn externe Belege fehlen, keine erfundenen Metriken. Erstelle drei Szenarien (best case, likely, high-risk) mit Abhängigkeits-/Stopgates statt erfundener Stundenfestlegungen.

## Ergebnis und Übergabeformat

`RED_TEAM_REPORT.md`, `FALSIFIED_CLAIMS.csv`, `ASSUMPTION_LEDGER.csv`, `ARCHITECTURE_ALTERNATIVES.md`, `PRIORITIZED_NEXT_3_ACTIONS.md`, Bewertung ob erst Architekturschnitt oder Rights-Triage erforderlich.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Keine Produktentscheidung als accepted eintragen. Keine Eigenschaft als fehlerfrei bezeichnen, nur weil der Quelltext/Testrunner sie nicht sichtbar macht.
