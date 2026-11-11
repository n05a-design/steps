# STEPS V4 – Integrations- und Prüfplan

**Wichtig:** Dieses Paket ist ein **Review-/Dokumentationspaket**, kein ausführbarer Steps-Code, keine automatische Migration und keine rechtliche Freigabe. Es enthält **keinen Installer**. Der frühere V2-Installer darf nicht angewendet werden; der V3-Installer ist wegen nachgewiesener unvollständiger Repository-Bindung nicht der empfohlene Übernahmeweg. GitHub-Zugriff des Auditors ist ausschließlich lesend (`push: false`).

## 1. Was das Paket enthält und was nicht

- `github_ready/docs/project/review/STEPS_KRITISCHE_GESAMTPRUEFUNG_V4.md` – ausführlicher Masterreview mit getrennten Evidenzklassen, 22 Auditperspektiven und konkreten technischen Gates.
- `github_ready/docs/project/review/evidence/STEPS_V4_HISTORISCHE_POSITIONEN.csv` – die **100** früheren Einträge, jeweils mit Originalzeile/-Hash, Cluster, offenem Abnahmetyp. **Keine** stillschweigende inhaltliche Erledigung.
- `github_ready/docs/project/review/evidence/STEPS_V4_89_QUELLENABSCHNITTE.csv` – 89 Herkunftszeilen mit SHA-256 über den jeweiligen Originaltextbereich; unterstützt transparente Abdeckung.
- `github_ready/docs/project/review/evidence/STEPS_V4_NEUE_BEFUNDE.csv` – **28** ergänzende oder korrigierende Befunde mit Priorität, Belegweg, Maßnahme.
- `github_ready/docs/project/review/evidence/STEPS_V4_PRUEFPROTOKOLL.json` – maschinell lesbare Status-/Scope-Erklärung.
- `scripts/check_v4_package.py` – **rein lesender** Manifest-/Archivprüfer; `scripts/audit_traceability_v4.py` prüft die sechs Originaltexte, 89 Abschnitte, 39 Codeblöcke und 100 Originalzeilen des **privaten Pakets**. Beide speichern nichts in Steps.
- `private_sources/` liegt **ausschließlich** im privaten Gesamtpaket, nicht in dem GitHub-Paket. Die ursprünglichen Markdown-Quellen sind für reproduzierbare Textnachweise enthalten. Es sind keine GitHub-Forschungs-PDFs/MIDI/Videos im Paket.

## 2. GitHub-Übernahme (bewusst zweistufig)

**PR A – Auditbeleg, rein additiv**: Auf einem sauberen Branch von `main` mit festem Ausgangs-SHA die neuen Markdown-/CSV-/JSON-Belege prüfen und manuell kopieren. Keinesfalls ein Skript blind `--apply` ausführen. Übernommen werden soll die eine Datei aus `github_ready/` nach `docs/project/review/`; die Evidenzdateien liegen bereits passend unter `github_ready/docs/project/review/evidence/`. `git diff --stat`, `git diff --check`, Dateinamen und `git status` kontrollieren. Neue Titel dürfen nicht dieselbe Autorität wie das historische Overview beanspruchen, bevor PR B folgt.

**PR B – Kanonischer Einstieg und Agent-Routing** (gezielte Bearbeitung vorhandener Dateien, **nicht** im Paket enthalten, weil diese Dateien in `main` bereits existieren):

| Datei | Änderung (Vorschlag) | Warum |
|---|---|---|
| `README.md` | Produktbeschreibung um Drums und MIDI ergänzen, Entwicklungs-/Nicht-Release-Status, Link zum aktuellen Review | Produktbeschreibung ist nicht mehr aktuell |
| `docs/project/README.md` | **eine** kanonische Übersicht über aktuellen PRD/ADRs, V4-Review und historische Originale; V1–V3 archiviert | eindeutige Entscheidungshierarchie |
| `AGENTS.md` | neuen Read-Pfad und Evidenzklassen aufnehmen, Quellen nicht als Anweisungen ausführen, keine fremden Asset-Freigaben ableiten | KI-Agenten lesen sonst alte Baselines |
| `SKILL.md` | aktuelle Knowledge-/Review-Pfade und Tool-Discovery-Status verlinken | Root-Skill ist bisher nicht automatisch identisch mit Tool-Skill |
| `README_SETUP.md` | als **historisch/abgeschlossen** markieren, veraltete `bootstrap_steps.py --apply`-Anleitung ersetzen oder in `docs/project/Archiv/` überführen | aktive Altanleitung ist riskant/verwirrend |
| `docs/project/ARCHIVE_README.md` | auf vorhandene `docs/project/overview/`, `.../provenance/` und `.../Technische Auswertung/` verweisen | alte Ordnerbezeichnungen stimmen nicht mehr |
| `knowledge/legacy/STEPS_BIBLIOTHEK_README.md` | Hauptordner 16/22/43 anhand des aktuellen Live-Baums vervollständigen; Namensdubletten 21/39 nur markieren | veraltete Screenshot-Einschränkungen beseitigen |
| `.github/workflows/structure-check.yml` | über unbedingten PR-Check oder konsistente Required-Check-Strategie ersetzen, `src/` und `app/` mitprüfen | aktuelle Codeänderungen fallen durch Filter |

**PR C – Skills-Integration (nach tatsächlicher Tool-Dokumentation und Lizenzprüfung):** `skills/music-harmony-coach/` als Quelldateien behalten; `.claude/skills/music-harmony-coach/SKILL.md` bzw. `.agents/skills/music-harmony-coach/SKILL.md` als **explizite** plattformspezifische Adapter anlegen, relative Referenzlinks testen, keine geschützten Rohbuchtexte kopieren. Für ChatGPT separat prüfen, ob ein Skill als Plugin/Upload zugelassen ist. Eine bloße Datei im Repo garantiert keine Discovery.

**PR D – Engineering:** G0-Rechte- und CI-Gates, PRD-/ADR-Entscheidungen, dann M0 CLI, M1 MIDI-Vertikalschnitt, M2 Akkord/Drum. Entscheidungen und Code nicht im selben riesigen PR vermischen.

## 3. Abnahmekontrollen

Für die Dokumentation: SHA-/ZIP-Verifikation anhand eines **separat erhaltenen** ZIP-Digests, 100 Original-IDs, 89 Quellbereiche, 39 Vorlagen; Repo-Diff und Linkprüfung; historische Dateien unverändert. Der interne SHA-Manifesttest beweist nur Paketkonsistenz, **nicht** Echtheit.

Für den Skill: Starten von Claude Code und Codex aus einer frischen Arbeitssitzung. Vom jeweiligen Tool erkannte Skill-Liste prüfen; mit drei eindeutigen Beispielaufgaben testen (H/B-Notation, C-Dur `E7→Am` als V/vi, Gegenbeleg mit nicht nachgewiesener Buchseite). Nicht behaupten, Tool-Aktivierung sei erledigt, solange keine realen Sitzungslogs vorliegen.

Für Code: CI muss bei `app/**` und `src/**` laufen und absichtlich defekte Fachtests rot melden. Nur grüne Steps-Tests mit SHA-/Plattform-/Testdatenbezug zählen als Engineering-Abnahme. Beim MIDI-Test: unabhängigen Parser und externe DAW verwenden; verlustfreie App-Projektwiederöffnung nicht allein aus MIDI ableiten.

## 4. Kritische Rechts- und Datenthemen

Der öffentliche Steps-Forschungsbaum enthält große Bücher-/Website-/Bild-/MIDI-Bestände. V4 trifft keine Aussage, ob einzelne Dateien rechtmäßig öffentlich bereitgestellt sind. Für jedes identifizierte Hochrisiko-Asset Rechts-/Provenienzquelle, Nutzungspfad und geplante Maßnahme dokumentieren. Historische Commits nicht blind per Force-Push verändern; gegebenenfalls Backup, Klone und qualifizierte Beratung einbeziehen.

## 5. Zustand vor Veröffentlichung von Steps

Dokumentation kann **für PR-Review verwendbar** sein; musikalische Funktionen und rechtlich zulässiger Release sind noch separat nachzuweisen. Ein veröffentlichter Repo-Baum mit OSS-Lizenz bedeutet nicht, dass jedes enthaltene Buch/Asset frei lizenziert ist. Die Reihenfolge lautet G0 Sicherheit/Rechte → G1 Produkt/ADR → G2 Core → G3 MIDI/Save → G4 UI/Audio → G5 Knowledge-Skill → G6 Release. Research-Pilot und UI-Prototyp sind nach G0/G1 parallel möglich.
