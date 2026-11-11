# Vorschlag für die bestehende `src/steps-0.00/README.md` (nicht automatisch überschreiben)

Die aktuelle README unter `src/steps-0.00/README.md` beginnt irreführend mit `# src/steps` und bezeichnet die Inhalte als künftiges importierbares Paket. Der vorhandene Strukturcheck fordert tatsächlich `src/steps`, während `src/steps-0.00` als normaler Python-Paketname nicht importierbar ist. Eine bestehende Datei soll nicht ohne Review ersetzt werden; der folgende vollständige Änderungsentwurf ist für einen separaten STEPS-Dokumentations-PR bestimmt.

---

# STEPS 0.00 – historischer Entwurfs- und Übergabebereich

**Projekt:** STEPS, eigenständige Musik-/Harmonieanwendung. **Status:** Entwicklungs-Scaffold, kein belegter Musik-/Shell-Release. Der Ordner `src/steps-0.00/` ist ein historisch versioniert benannter Entwicklungsbereich, **kein** importierbarer Python-Paketname. Ein künftiges echtes Paket `steps` gehört vorbehaltlich des Architektur-ADRs nach `src/steps/` (Version in `pyproject.toml`/`VERSION`, nicht im Importnamen).

## Verbindliche technische Herkunft

Die Baseline für die Shell ist die grün geprüfte **Glide-To-do-App 3.53.0**, ursprünglicher GitHub-Commit `9e767bea5e21063466a28ac3a679406484ad5d5f`, Glide-System V1.15. Ihre vollständige im STEPS-Repository abgelegte Referenz liegt unter `src/glide-v3.53/`. Das Entwicklungsprojekt ist **STEPS**, nicht das ursprüngliche `glide-to-do`-Repository. Der Baseline-Code darf nicht als bereits funktionierendes STEPS-Musikprogramm ausgegeben werden.

## Ziel und Erhaltung

Glide wird kontrolliert auf ein neutrales UI-/Infrastrukturgrundgerüst reduziert. Die grafische Shell um die beiden relevanten Arbeits-/Inhaltsbereiche bleibt erhalten: Seitenleiste und Seitenpunkte einschließlich Verbergen/Einklappen, Header, Logo, Titel, Symbolbuttons, Suche, Eingabe-/Bearbeitungsflächen, Menüs, Einstellungen, Schrift-/Designsystem, Layout-/Resize-/Fokus-/Keyboard-/Dialog-/Accessibility-Verhalten. Bestehende Save-/Backup-/Logging-/Lifecycle-/QA-Verträge werden fachneutral adaptiert. Alte To-do-Callbacks, Taskdaten, Locks und Backups werden vollständig abgetrennt. Zwei OS-Fenster versus zwei Inhaltsbereiche ist anhand echter Tk-Topologie/Owner-Entscheid als ADR zu klären; nicht aus dem Ausdruck „zwei Fenster“ ein zweites Tk-Root bauen.

STEPS erhält eigene App-/Bundle-IDs, Datenverzeichnisse, musikalische Domänenmodelle, Projektschemata, Import/Export, MIDI/Audio-/Drum-Logik und Tests. Der gemeinsame Core wird über versionierte `component_id`-/Contract-/ChangeLog-/Consumer-Verträge dauerhaft wartbar gestaltet, ist heute aber noch **kein isoliert geprüfter SDK-Release**.

## KI-übergreifende Langzeit-Dokumentation

**Alle sachlich relevanten Ergebnisse und Ausgaben, auch frühere technische/fachliche Analysen, Forschungsberichte, allgemeine KI-Antworten, Entscheidungen, Prompts, Code-/Test-/Fehlversuche und Übergaben müssen project-intern als dateibasierte, hashbare und versionierte Referenzen nachvollziehbar bleiben.** Die KI-Modelle Copilot, ChatGPT, Claude, Gemini/Antigravity und weitere nutzen denselben Kontext, ohne auf einen bestimmten Chat angewiesen zu sein. Siehe `docs/operations/AI_CONTINUITY_PROTOCOL_V6.md`, `docs/project/antigravity-handover/README.md` und `prompts/32_STEPS_ANTIGRAVITY_MASTER_AUDIT_V6.md`.

Projektinterne Audit-Artefakte zunächst in separaten lokalen Ordnern schreiben; ein geprüfter Übertrag ins Git-Repository erfordert einen eigenen Ownerfreigabe-/PR-Schritt. Bei Quell-/Test-/Fachlücken den Status `NOT_REVIEWED`/`BLOCKED` dokumentieren. Keine stillschweigende Löschung von Originalunterlagen oder historischen QA-Belegen.

## Abnahme vor der Umsetzung

- Upstream-vs.-STEPS-Referenzmanifest und Import-/Asset-/Lizenztabelle vorhanden.
- Modul-/UI-Erhaltungs- und Abhängigkeitsmatrix für die 30 Shell-Szenarien geprüft.
- `src/steps`/`src/steps-0.00`-Paketfrage und Struktur-CI als eigener PR geklärt.
- STEPS-Datenroot- und No-Glide-Read/Write-Tests vorgesehen.
- Aktuelle `STATE.json`, `OUTPUT_REGISTER.csv`, `SOURCE_COVERAGE.csv`, `NEXT_SESSION_HANDOVER.md` vorhanden.
- Erst nach genehmigtem ADR beginnt rückbaubasierte STEPS-Codeimplementierung.

---

**Änderungsmodus:** Vorschlag; V6 erstellt und liefert **keine** bereits gemergte `src/steps-0.00/README.md`. Bei Einbau bestehende Informationen erhalten und `git diff` kontrollieren.
