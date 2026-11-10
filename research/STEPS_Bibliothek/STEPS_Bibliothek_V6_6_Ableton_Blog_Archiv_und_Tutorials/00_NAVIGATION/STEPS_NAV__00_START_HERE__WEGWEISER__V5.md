# STEPS – Research Library V5 (Großausbau)

**Stand:** 8. November 2026 · **Version:** `5.0.0-research-draft` · **Zweck:** Wissenschaftlich orientiertes Forschungs-, Musikbeispiel- und Entwicklungsfundament für Codex. **Keine** fertige Anwendung, peer-reviewte Enzyklopädie oder vollständig erschlossene Originalbibliothek.

## Was an V5 tatsächlich neu ist

Die V5 ist eine **inhaltliche Vertiefung** der vorhandenen V1–V4 und zugleich eine neue Datenbasis, die vier gleichberechtigte Wissenssäulen ausbaut: **Music Theory, Harmony, Chord Progressions, Composing**. Die historischen V4-Dateien (einschließlich des V3/V1-Bestands) liegen **unverändert** in `00_ARCHIV_V4_Unveraendert/` und bleiben als frühere Forschungszustände erkennbar. Die neue Version ersetzt ihre Behauptungen nicht stillschweigend, sondern ergänzt und korrigiert sie anhand externer Referenzen und eigener nachvollziehbarer Beispiele.

**Enthalten in V5:** sieben neue fachliche Monographiekapitel, zwölf ausführlich diskutierte Analyse-Werkstattfälle, 27 einzeln inventarisierte extern überprüfte Veröffentlichungen/Webressourcen mit ihrem **wirklichen Evidenzstatus**, 53 redaktionell festgelegte originale didaktische Akkordprogressionsfamilien, daraus abgeleitete 1.378 Tonart-/Zeitvarianten, 16 zusätzliche originale vierstimmige 32-taktige Lehrskizzen mit MIDI/MusicXML/JSON und Begleitbeschreibung sowie 60 bewusst positiv/negativ formulierte fachliche Test-Anforderungen. Der frühere V4-Umfang ist zusätzlich archiviert.

**Wichtig:** 1.378 Transpositionen entsprechen nicht 1.378 eigenständig untersuchten progressionalen Traditionen. Die neuen 16 Kompositionsskizzen sind algorithmisch elaborierte Originalstudien, nicht externe musikalische Gutachten. Die 60 konzeptionellen Referenzfälle sind für Codex spezifiziert, **noch nicht als ausführbarer Fachtest implementiert**. Eine URL oder Abstractprüfung beweist keine vollständige Buchlektüre.

## Navigationsplan

| Teil | Inhalt | Zuerst lesen? |
|---|---|---|
| `RESEARCH_SYNTHESIS_V5.md` | Fachliche Forschungserkenntnisse, Belegstatus und wichtige Grenzen | Ja |
| `01_Neuforschung/00_FORSCHUNGSSTAND_V5.md` | Wissenschaftliches Zielbild und neues Erkenntnismodell | Ja |
| `02_Fachbaende/01_MUSIKTHEORIE_V5.md` | Akustik, Tonhöhen, Notation, Skalen, Modi, Instrumente, Zeit | Je nach Domäne |
| `02_Fachbaende/02_HARMONIE_V5.md` | Funktionale, modale, chromatische, Jazz-, Blues-, Rock-, Pop-Harmonik | Je nach Domäne |
| `02_Fachbaende/03_CHORD_PROGRESSIONS_V5.md` | Progressionstypen, zeitliche Form, Reharmonisierung, Alternativanalysen | Je nach Domäne |
| `02_Fachbaende/04_COMPOSING_V5.md` | Motivik, Melodik, Kontrapunkt, Form, Recomposition, Arrangement | **Ja, für Composing** |
| `02_Fachbaende/05_KOGNITION_KULTUR_STIL_V5.md` | Wahrnehmung, Erwartung, musikethnologische Grenzen, Genre | Ergänzend |
| `02_Fachbaende/06_COMPUTATIONAL_MUSIC_V5.md` | Repräsentation, Parsing, Wissensgraph, Tests, Formate | Für Entwickler |
| `02_Fachbaende/07_PRODUKT_DIDAKTIK_SKILL_V5.md` | Lernen, UX, Agent-Skill, Kompositionswerkbank | Für Produktarbeit |
| `03_Analysewerkstatt/` | Zwölf sorgfältig diskutierte eigene Theorie- und Grenzfälle | Ja |
| `04_Kompositionslabor/` | 16 eigene 32-taktige vierstimmige Lehrskizzen als MIDI, MusicXML und JSON | Für Musiker und Codex |
| `05_Wissensobjekte/` | 53 Progressionsfamilien und 1.378 systematische Varianten | Für Datenintegration |
| `06_Quellen_und_Rechte/` | Quellenstatus, Literaturprüfung, Rechtsgrenzen | **Pflicht vor fachlicher Freigabe** |
| `07_Codex/PROJECT_CONTEXT_HANDOVER_V5.md` | Aktuelle Projektübergabe | **Ja** |
| `07_Codex/CODEX_MASTER_EXECUTION_V5.md` | Konkreter Auftrag in 35 überprüfbaren Arbeitspaketen | **Ja** |
| `08_Validierung/` | Ausgeführte Strukturprüfung plus offene Expertenprüfungen | **Pflicht** |
| `09_Governance/` | Gaps, Entscheidungen, Nachverfolgbarkeit, Reviewverfahren | **Pflicht** |
| `00_ARCHIV_V4_Unveraendert/` | Historischer V4-/V3-/V1-Bestand | Bei Konflikten |

## Arbeitsschritte mit Codex

1. `07_Codex/PROJECT_CONTEXT_HANDOVER_V5.md` und `07_Codex/CODEX_MASTER_EXECUTION_V5.md` gemeinsam übergeben.
2. Das **echte** STEPS-Repository in einem neuen Codex-Lauf zuerst read-only inventarisieren: Branch, Git-Status, AGENTS-/SKILL-Text, vorhandene Module, Tests und vorhandene Knowledge Base. Es wurde hier **kein** Steps-Repo geöffnet oder geändert.
3. Fachbände, Source Register und eigenständige Lehrbeispiele getrennt verarbeiten; Inhalte bei fehlenden Belegen als `research_draft`, `pedagogical_synthesis` oder `review_required` kennzeichnen.
4. Wissen verknüpfen: `Source → Claim → Definition/Rule → Theory Lens → Progression/Composing Technique → Test/Counterexample → App/Skill Use Case`.
5. Mechanische Tests **und danach** echte musikfachliche Review-Schritte ausführen. Nur freigegebene Teile in die kanonische KB verschieben.
6. Offene Quellen, Lizenzen und divergierende Interpretationen im Gap-Register belassen. Keine geschützten Rohbücher in ein öffentliches Git-Repo kopieren, keinen automatischen Merge.

## Verbindliche Einschränkungen

- **Vier gleichrangige Domänen**, wobei Composing nicht mit Akkordkombination verwechselt wird.
- Rhythmus, Metrum und Harmonic Rhythm sind fachlich relevant; **keine Drum-Groove-Engine oder Drum-Korpusimplementierung** im gegenwärtigen Umfang.
- Externe Werke werden nur im Status der tatsächlichen Einsicht zitiert; keine erfundenen Buchseiten, kein 100%-Korrektheitsversprechen.
- Korpusstatistik ist keine universelle Ästhetik; wissenschaftliche Mehrdeutigkeit bleibt erhalten.
- Softwarerechte und Datensatz-/Musikrechte sind unabhängig zu prüfen.
- Ohne tatsächlich überprüften Repository-Zustand gibt es keinen vermeintlich vorhandenen Steps-Code, keine technischen Releases und keine als fertig deklarierte Engine.

**Das Paketmanifest** enthält SHA-256 der tatsächlich verpackten Dateien. Siehe `PACKAGE_MANIFEST_V5.json` und `SHA256SUMS.txt`.
