# STEPS – Project Context Handover V4 · Codex Übergabe

**Status:** Research-Arbeitspaket, Entwurf, keine verbindliche Projekt-/Codefreigabe. **Historisches Voll-Handover:** `../00_HISTORISCH_V3/00_Archiv_V1/PROJECT_CONTEXT_HANDOVER_V1.md`. **Maßgeblicher Ausführungsauftrag:** `CODEX_MASTER_EXECUTION_V4.md`.

## 1. Projektvision und aktueller fachlicher Anspruch

Steps soll eine unabhängige Open-Source-App zur explorativen Arbeit mit Akkorden und Musiktheorie sein. Die ursprüngliche Zielsetzung bleibt erhalten. **Die explizite neuere Nutzeranforderung erweitert das Vorhaben um ein gleichberechtigtes Composing-Fundament:** Das zukünftige System muss neben Ton- und Harmoniewissen auch Motiv, Melodie, Zeit, Form, kompositorische Verarbeitung, Stimmführung, Arrangement und Werkentwicklung nachvollziehbar repräsentieren. Der unmittelbare Schwerpunkt ist eine umfassende strukturierte Research/Knowledge Base und ausführbare, prüfbare Codex-Integration – **nicht** die sofortige Neuentwicklung der GUI oder das ungeprüfte Einführen eines generativen ML-Modells.

## 2. Historische Dokumentation und Korrekturen

V3 wird unverändert unter `00_HISTORISCH_V3/` bewahrt. Dort liegen auch die **sieben ursprünglichen Markdown-Dateien** von V1, darunter der Master-Research-Prompt und das fertig erzeugte Projekt-Handover. Die ältere Aussage in einem früheren Handover, `Master-Research-Prompt.md` fehle, ist mittlerweile durch den vorhandenen Dateibestand widerlegt; dieser historische Text ist aus Gründen der Provenienz **nicht stillschweigend verändert** worden. Ein separat finalisiertes, ursprüngliches umfassendes Deep-Research-Paper außerhalb der V1/V3-Berichte ist nicht nachgewiesen. Der tatsächliche Zustand des STEPS-Git-Repositories ist hier nicht verifiziert. Keine Aussagen zu Branch, CI, Tests, Releases und vorhandenen Python-Engines ableiten.

## 3. Neues V4-Material – was fertig und was offen ist

Vorhanden: 49 neue umfangreicher erläuterte Research Modules, 15 Werkstattanalysen, 163 kontrollbedürftige Themen, 131 weitere Progressionsfälle (226 mit Historie), 59 neue Rule Drafts (136 mit Historie), 65 neue Kompositionstechniken (134 mit Historie), 30 neue originale 16-bar MIDI-Studien mit zeitlich vollständigen Note Events, 77 Quellen-/Editionsdatensätze, JSON-Schemata, Validator, Prüfungsergebnis, ausführbarer Codex-Masterauftrag. Dies sind echte Dateien, nicht bloße geplante Produkte. **Offen:** Exakte wissenschaftliche Einzelnachweise, umfassender Expertenreview, Lizenzfreigabe jeder fremden Quelle und realer Repository-Einbau.

## 4. Priorität bei konkurrierenden Informationen

- `CONFIRMED`: vier fachliche Säulen, große Wissensdatenbank vor kompaktem Skill, Erhaltung der älteren Quellen und Ideen, Nachvollziehbarkeit, eigenständige Produktidentität, Drum-Engine/Drum-Dataset nur später.
- `EXISTING_IN_PACKAGE`: V4-Dateien, 30 tatsächliche MIDI-Files, JSON-Objekte, Test-Skript/Report, archiviertes V3/V1.
- `RESEARCH_CANDIDATE`: Bücher, Corpus- und Standardreferenzen, soweit nur Metadaten/Abstracts geprüft.
- `PROPOSED`: konkrete Technologie-, UX-, Engine- und Repo-Pfadentscheidungen. Nicht als bereits implementiert ausgeben.
- `UNVERIFIED`: Einzelclaim, fehlender Source Locator, Genre-Authentizität, vollständige Lektüre, Lizenzfreigabe und Code-Bestand.

## 5. Quellenverzeichnis und Arbeitsregel

`05_Quellen/QUELLENREGISTER_V4.json` enthält 77 Registerzeilen, **nicht 77 verschiedene abschließend geprüfte wissenschaftliche Werke**. `05_Quellen/QUELLENKOMMENTAR_V4.md` erläutert besonders die neuen externen Titel und tatsächliche Lesetiefe. Benutze `09_Governance/CLAIM_PROVENANCE_AND_LEGAL_GATE.md`: Erhebe Verifikationsstatus erst nach Lesen des konkreten Inhalts und dokumentierter Edition/Passage. Veröffentliche keine geschützten Buchkopien, Notenseiten, fremden Audioaufnahmen oder nicht lizenzierten Datensätze.

## 6. Daten- und Theoriewahrheit

Trenne (a) Klang/Tonklasse, (b) enharmonische Schreibweise, (c) Akkordqualität, (d) harmonische Funktion, (e) real registrierte Stimmführung, (f) zeitliche/formale Rolle, (g) kompositorische Intention, (h) wissenschaftliche Quelle. Die Daten dürfen Mehrdeutigkeit abbilden. `C7` ist als Blues-I7 nicht automatisch V7/IV; eine Pop-Axis-Loop hat ohne Melodie/Form eventuell mehrere Zentren. Bei Composing können gleiche Harmonien durch Register, Satzdichte, Bass, Motiv und Form gegensätzliche dramaturgische Wirkungen hervorbringen.

## 7. Codex-Definition of Done und Ausführung

Zuerst read-only Bestand prüfen, dann vorhandene KB-/Skill-Struktur respektieren. Mindestens ein fachliches Modul end-to-end **quellengebunden, versioniert, mit Gegenbeispielen und tatsächlich ausgeführten Tests** in das reale Repository integrieren; danach nach Priorität erweitern. Führe die gelieferte `validate_v4.py` aus und die bestehenden Projekt-Tests. Dokumentiere sämtliche Fehler, Quellen-/Rechtslücken und human review. Einen 'reviewed' Status nicht allein aus Schemavalidität oder KI-Modellwissen ableiten. Erhalte Provenienz und ältere Versionen. **Nicht ohne explizite Anweisung nach main mergen**.

## 8. Empfohlene Entscheidungsgates

1. `GATE-REPO`: Quelle und aktueller Stand des echten STEPS-Repositories nachgewiesen.
2. `GATE-REUSE`: Fremdmaterial darf im gewählten Zielrepo rechtlich verwendet werden.
3. `GATE-SOURCE`: wissenschaftliche Einzelclaims mit überprüften Quellenlocators.
4. `GATE-MUSIC`: Notation, Harmonie und Musikbeispiel fachlich geprüft.
5. `GATE-TECH`: Parser, Schemas, MIDI/Eventprüfung und Regressionstests bestanden.
6. `GATE-SKILL`: Skills verwenden echte KB-Objekte, sind keine kopierte Enzyklopädie.
7. `GATE-PUBLICATION`: README, Changelog, Coverage-Report und Statuswerte sachlich korrekt.

**Start:** Volltext von `CODEX_MASTER_EXECUTION_V4.md` verwenden und AP-00 bis AP-02 beginnen; keine bloße erneute Konzeptphase.
