# 14 — Integration in Steps/Glide ohne Nebenänderungen

## Kein direkter Remote-Schreibstand

Während der V1-Arbeit meldete der GitHub-Branch-Erstellversuch `HTTP 403 Resource not accessible by integration`. V2 hat weder GitHub-Branches/Commits/PRs erstellt noch Originaldateien überschrieben. Andere in Repository-Metadaten angezeigte `push: true`-Berechtigungen widerlegen **nicht** den real gescheiterten Create-Ref-Aufruf. Ein unautorisiertes anderer Client-Token darf nicht angenommen werden.

## Klare Trennung von lokalem Reviewpaket und öffentlichem Repository

Dieses Paket ist **intern**: Die nachrichtlichen Anforderungen/Toolplanung, Risikoeinschätzungen und das ursprüngliche V1-Archiv enthalten Projekteigenheiten, die vor Veröffentlichung geprüft werden müssen. **Nicht das komplette ZIP nach Steps `main` hochladen.** Die Repo-Wurzel `README.md`, `AGENTS.md`, `SKILL.md`, `decisions/` und die etablierte `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` sind **bereits vorhanden**. Nicht automatisch überschreiben.

**Empfohlenes publizierbares Mapping nach Review:**

| Paketquelle | Steps-Ziel (nur Vorschlag, neu) | Besonderheit |
|---|---|---|
| `README.md` | `docs/project/glide-steps-audit/README.md` | fachlicher Navigator, nicht Root-README ersetzen |
| `docs/01_*.md` und `docs/02_*.md` | `docs/project/glide-steps-audit/` | Quellenstand, Auditbasis |
| `docs/03_*.md` | `docs/project/glide-steps-audit/` | Qualitätsaudit V1; keine öffentliche Personaldetails |
| `docs/04_*.md`, `docs/13_*.md` | `docs/project/glide-steps-audit/` | Requirements/Delta, nur zusammen mit Evidenz |
| `docs/05_*.md`–`07_*.md` | `docs/architecture/` mit Prefix `glide-steps-` | RFC, kein Accepted ADR |
| `docs/08_*.md`–`09_*.md` | `docs/theory/` und `knowledge/` als verlinkter Reviewtext | Duplikatquelle vermeiden, nicht als Knowledge-Primärquelle markieren |
| `docs/10_*.md`–`12_*.md` | `docs/roadmap/` und `research/gaps/` | nur nach Integration in bestehende Register, nicht zwei getrennte aktuelle Listen |
| `prompts/` | `docs/roadmap/agent_prompts/` | ein gemeinsamer Vertrag, keine Duplikation aus V1 |
| `audit/*.csv` | `docs/project/provenance/` | Datenschutz/CSV-Formelsicherheit/alte Quellen-IDs prüfen |
| `history/V1_originalpaket_unveraendert.zip` | **nicht** öffentlich in Steps | historisch, enthält Account-/Arbeitskontext und alte Referenzen |

## Bestehende Dokumente haben Vorrang

**Glide:** `01_Repository/Glide/src/glide/README.md` ist systemweit das einzige maßgebliche Modul-/Feature-/Test-Inventar; keine zweite 94-Dateien-Kanonizität in Steps behaupten. Glide-Designregeln/Entscheidungen D01–D77 verbleiben in Glide; Steps übernimmt begründete Prinzipien als eigene ADRs. **Steps:** `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` bleibt historisch vollständige Zusammenführung sechs in diesem Bericht benannter Dokumente; neue Gaps werden per Link/ADR nachgetragen statt ganze alte Berichte zu duplizieren. Öffentliches Wissen unter `knowledge/sources` nur nach Rights-Audit.

## Empfohlenes manuelles Verfahren mit Freigabe

1. Isolierte lokale Steps-Kopie, sauberer `git status`, bestätigter Referenz-SHA und eigener Reviewbranch. Kein paralleler Copilot-/Claude-Write auf Glide.
2. Für jeden V2-Text zunächst prüfen, ob ein entsprechender Abschnitt bereits in `docs/architecture`, `research/gaps`, `decisions` oder `AGENTS.md` liegt. Doppelte **Regeln** zusammenführen, historische **Quellen** lediglich referenzieren.
3. Privatinhalte/Screenshots/absolute Pfade und Materialrecht redigieren. YAML-/CSV-Quellen IDs gegen aktuelle Registry, Relativlinks und Markdown rendern/checken.
4. Nur im ausdrücklich genehmigten Scope editieren; `git diff --check`, manuelle Inhaltsprüfung, Satz-/Status-/Testnachweise; `pytest` und lokalen Strukturcheck nur in isolierter Umgebung.
5. Nach Besitzerreview einen Draft-PR erzeugen. Kein Merge/Push/Tag/History-Rewrite ohne separate Autorisierung. Wenn keine Schreibrechte bestehen, nur das ZIP als Review-Material verwenden.

## Datenschutz und Lizenz schon beim Dokumentenimport

Der Steps `README_SETUP.md` enthält absolute lokale Windows-Beispielpfade; diese sollten in einem gesonderten redaktionellen Review durch `${HOME}`/neutrale Platzhalter ersetzt werden, ohne historische Aussagen rückwirkend zu manipulieren. Falls es andere private Pfade gibt, vor öffentlichem Upload einen breit angelegten Privacy-Scan durchführen. Auch im V2-Paket enthaltene Repo-Verweise sind öffentliche URLs; sie stellen keinen Urheberrechtsnachweis für die Inhalte dahinter dar.
