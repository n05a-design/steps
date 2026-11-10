# V2-Korrekturregister: Was an V1 nicht trägt und wie es ersetzt wird

**Status:** 2026-11-10 · Unabhängige Zweitprüfung. Die früheren W-01–W-40, G-01–G-34 sowie N-01 ff. bleiben unter `source_archive/`, `archive/v1_docs/` und `docs/project/CONFLICTS_AND_GAPS.md` als historische Register erhalten. „Korrektur“ heißt, dass eine bisherige Aussage nach neuem Beleg modifiziert wird; „Offen“ heißt, dass keine gleichwertig belegte Ersatzbehauptung existiert. Einzelne ältere historische Aussagen dürfen gerade nicht rückwirkend überschrieben werden.

## A. Harte Befundkorrekturen

| ID | V1-Darstellung bzw. Unterlassung | Neue Evidenz und Abwägung | Aktueller Status | Verbindliche Maßnahme |
|---|---|---|---|---|
| K01 | Glide GitHub `main=3.50.7`; 3.53.0 nur lokal | `main=9e767bea...`, PR #74/#75 gemergt am 10.11.2026; `VERSION=3.53.0`, System=1.15 | **V – V1 veraltet** | Alle neuen Git-Arbeitsaufträge auf `9e767bea` pinnen; kein falscher 3.50.7-Ausgangsschnitt |
| K02 | lokaler 3.53.0-Code möglicherweise gegenüber Remote ungesichert | `git hash-object` lokaler Upload = `0fc522fb...`, gleicher Git-Blob des Remote-`app.pyw` | **V – Hauptdatei identisch** | Nur diese eine Datei als bytegleich kennzeichnen; 93 Module/Assets gesondert kontrollieren |
| K03 | fertiger Forschungs-Handover wurde nicht ausdrücklich gefunden | `research/notes/deep-research/legacy/PROJECT_CONTEXT_HANDOVER.md` vorhanden (83.203 Zeichen, datierter Entwurf 08.11.) | **V – vorhanden**, **O – Freigabe** | als Eingangsdokument in kanonischen Projektkontext integrieren; nicht nochmals unnötig generieren |
| K04 | 24 generische Arbeits-Prompts galten als umfassender Ausbau | Originale `03_PROJECT_CONTEXT_HANDOVER_PROMPT.md` (13.530 Zeichen) und `04_CODEX_KNOWLEDGE_BASE_FOUNDATION_PROMPT.md` sowie Master-Prompt sind spezifischer; V1-Prompts meist 360–390 Wörter | **V – qualitative Unterabdeckung** | zuerst Original-Codex-Vertrag als Hauptvorgabe, neue Prompts als *kleine Teilaufträge* ableiten |
| K05 | V1-Projektübersicht als „konsolidiert“ bezeichnet | neue Overview ca. 789 Wörter, ältere konsolidierte ca. 14.257 Wörter; einzig archiviert statt cross-linked | **V – unzureichend** | kanonisches Requirements-/Evidenzregister statt künstlich kurzer Ersatzübersicht |
| K06 | lokale 3.53.0-Code-Datei als ausreichender Glide-Freeze betrachtet | App enthält 121 Top-Level-Imports, 39 Klassen, 1.866 `ListApp`-Methoden, viele eigene Fremdmodule; alleine nicht startbar | **V – Abhängigkeitsrisiko** | gesamtes 94-Module- und Ressourcen-/Lizenz-/QA-Inventar aus Repository verwenden |
| K07 | „Rückbau auf zwei Fenster“ implizit als UI-Verkleinerung | Screenshot zeigt ein OS-Fenster mit zwei Bereichen; Userbegriff bleibt mehrdeutig | **A/O – Hypothese** | keine zwei `Tk`-Roots erzeugen; zuerst ADR über 2 Panes versus 2 Toplevels |
| K08 | `Noop` für Sidebar als bloßes Entfernen von Callbacks | `ListApp` enthält 118 Methoden mit `sidebar` im Namen, 64 `menu`, 26 `search`, 12 `compact`; Name-only-Abfrage, aber große Quervernetzung | **V – begründete Risikohypothese** | tatsächliche Event-/Action-/Hotkey-Graphen prüfen, Noop-Telemetrie in Testdaten, bei Noop kein Write |
| K09 | Schritte zu Lizenz/Historie eher allgemeine Warnung | öffentliche Steps-Tree-Daten enthalten 60 PDFs und Drittanbieter-Medien; Lizenz des eigenen Quellcodes deckt diese nicht | **V Dateibestand / O Rechte** | pro Asset Rights Record; kein weiterer unrechtssicherer Upload/Release; gesondertes History-Gutachten |
| K10 | `push:true` als voraussichtliche Git-Schreibfähigkeit | Integrationsabfrage meldete `push:true`, tatsächliche Branch-Anlage scheiterte HTTP 403 | **V – Tool-Aktionsgrenze** | keine entfernten GitHub-Schreibzugriffe behaupten; sichere lokale Übergabe; Schreibrechte vor jedem echten PR neu testen |
| K11 | V6.6/Bibliothek – 1.000/1.146/1.306 als Pauschalkonflikt | 1.000 = konkrete Dateien unter *einem* V6.6-Archivbaum; 1.146/≈1.166/1.306 = ältere, teils intern inkonsistente Tabellen/Gesamtansprüche | **V – getrennte Nenner** | Manifest/Snapshot/Scope-ID je Zahl, nie als Gesamtvollständigkeit behandeln |
| K12 | `docs/project` im Steps-Repo als aktuelle Freigabequelle vorausgesetzt | bestehende `docs/project/README.md` markiert Scaffold; alte Overview vom 09.11. und Handover vom 08.11. historisch | **V – historische Arbeitsunterlagen** | neue Entscheidungen explizit `accepted`/Owner; README kein Entschlussersatz |
| K13 | Skill-Status wird als einheitlicher Plan geführt | `SKILL.md` im Root ist Workflow-Router; echter Harmony-Coach liegt verschachtelt unter `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/`; `knowledge/sources/registry.yaml` leer | **V – zwei Skilltypen** | eine Adapterroute, autoritative KB unabhängig, eindeutige Skill-Version/Tests |
| K14 | generische MIDI-Roundtrips als Abnahme ausreichend | SMF enthält delta-Ticks, Tempo-Map, Meta-Events, Kanäle, zeitliche Überlappung; Playback-Scheduler ist eigenes Subsystem | **E + A** | separate SMF-/Live-Playback-Verträge, künstliche Clock-Tests, Backends prüfen |
| K15 | eine reine technische Phasenliste genügt als Projekt-Roadmap | Forschungsvorlagen enthalten separate 4 historische Gantts; Blueprint priorisiert Theorie/KB, User will parallel UI-Fundament | **V – echte Sequenzierung offen** | zwei miteinander verknüpfte Tracks: „UI-Shell“ und „Fach-/Knowledge-Vertikalschnitt“ |
| K16 | alle Glide-Systemkomponenten als langfristiges „Fundament“ | 94 Module sind Katalog, 25 Pakete *Kandidaten*, kein als Steps isoliert freigegebenes Framework | **D – kein Reuse-Beweis** | Nutzen nach Aufwand/Adapter/Testkosten messen, sonst kleine neue Implementierung |
| K17 | Konkurrenz-Analyse aus der 2026-Literatur genügt | Hookpad, Scaler 3, Chordbot und MuseScore bieten relevante Chord-/Harmonie-/MIDI-Funktionen; „Chord-Explorer“ alleine nicht automatisch einzigartig | **E – primäre Herstellerquellen** | Produktdifferenzierung mit nachprüfbaren Tasks und Nutzenhypothese untermauern |
| K18 | Hash-Deduplikate sind automatisch „Dopplungen“ | Git-Blob-Identität trennt keine absichtlichen historischen/versionierten Kopien; ähnlich benannte Ordner 21/39 können unterschiedliche Inhalte haben | **V/A – kein Löschauftrag** | erst funktionale Referenzen, Historie, Rechte und semantische Varianten abgleichen |
| K19 | „nichts auslassen“ durch ZIP-Sicherung erfüllt | 24 kurze Prompts und 789-Wörter-Overview ersetzen keinen ausführbaren Requirements-/Evidence Trace | **V – Qualitätsmangel** | Anforderungen einzeln nachweisen und Quellenabdeckung aktiv pflegen; Originale zusätzlich behalten |
| K20 | Sicherheit hauptsächlich Daten-/Lizenzproblem | neue zu importierende PDFs, HTML, ZIP, MIDI und untrusted KI-/Crawlertexte schaffen Parser-, Pfad-, Ressourcenkosten- und Prompt-Injection-Risiken | **A – zusätzliche Bedrohungsdimension** | eigene Threat-Modelle, Sandboxing/Checks vor Ingestion und Agent-Aktionen |

## B. Forschungskanon: neu entdeckter Ordner und seine Bedeutung

**Bestätigter Pfad:** `https://github.com/n05a-design/steps/tree/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy`.

| Datei | Dokumentierte Rolle | Relevanter zusätzlicher Inhalt | Offene Frage |
|---|---|---|---|
| `00_README.md` | alte Paket-/Lesereihenfolge | enthält frühere Angabe, finales Handover noch nicht vorhanden | datiert, jetzt überholt |
| `01_STEPS_Research_Foundation.md` | Research Paper, 899 Zeilen | Regeln vs. empirische Modellierung vs. ML, stilistische Linsen, Voice Leading, music21/SMF, Quellen-/Benchmarkplan, Skill-Ableitung | Autor-/Quellenverifikation, Reviewqualität |
| `02_STEPS_Knowledge_Base_Product_Blueprint.md` | zweites Research Paper, 459 Zeilen | vier Engines Theory/Harmony/Generation/Pedagogy, Produktideen, Corpus-Bias, MIDI-/Audio-/Lernintegration, konkurrierende Produktbilder | welche Konzepte werden ins MVP übernommen? |
| `03_PROJECT_CONTEXT_HANDOVER_PROMPT.md` | ausführlicher Handover-Auftrag, 286 Zeilen | 17 geforderte Handover-Abschnitte samt Erhalt-/Abdeckungsprüfung | historisch, Ausführung ist erfolgt |
| `04_CODEX_KNOWLEDGE_BASE_FOUNDATION_PROMPT.md` | langfristiger Codex-Umsetzungsauftrag | verlangt *reale* Quellen- und Wissensobjekte, keine reine Repo-Struktur; strenge Quellen-/Rechte-/Test-Gates | welche Quelloriginale sind verfügbar und freigegeben? |
| `Master-Research-Prompt.md` | ursprüngliche Research-Anweisung, 261 Zeilen | explizit Breite vor Verdichtung, fachliches Retrieval, kultur- und methodenübergreifende Forschung | ob späterer Forschungsstand final und freigegeben ist |
| `PROJECT_CONTEXT_HANDOVER.md` | erzeugte Übergabe, 797 Zeilen, Status `draft` | REQ-/DOC-/SRC-/CTX-/DEC-IDs, 17 Handover-Kapitel, aktive Forschungslücken | nicht als Owner-„approved“ behaupten |

**Wichtiger Fehler der Dokumentationshistorie:** `00_README.md` erklärt das Handover noch für „nicht enthalten“, obwohl `PROJECT_CONTEXT_HANDOVER.md` nun daneben liegt. Das ist als *zeitlicher Statusbruch* zu dokumentieren. Im Frontmatter des Handover ist `Master-Research-Prompt.md` als damals „nicht eigenständige Datei“ kommentiert, obwohl es heute neben dem Handover liegt. Keinesfalls die Originaldokumente rückwirkend verändern; aktuelle kanonische Registry darüberstellen.

## C. Weitere zu untersuchende Widerspruchsfamilien

1. **Produkt-Entwicklungsstatus:** Chord/Harmony-Ziel von GitHub-README vs. Nutzerwunsch Chord+Drum und Producing. Konfliktklasse: unterschiedlich breites Produktziel, kein Grund für Löschen von Drums.
2. **Wissensstand:** 1.000 Legacy-Dateien vs. `sources: []`: Archiv-Existenz vs. strukturierte Wissens-Integration. Keine automatische Gleichsetzung.
3. **Analysemodelle:** E7→Am als primäre oder sekundäre Dominante je Tonart; Stil-/Modus-Hypothese immer mit Kontext.
4. **Fach-/Datenarchitektur:** bestehende `schemas/chord.schema.json` mit Strings und Intervallsemitönen vs. Research-Forderung, Pitch/Spelling/Voicing/Interpretation zu trennen. Bestehendes JSON-Schema ist kein Beweis, dass damit enharmonische Relationen vollständig abbildbar wären.
5. **Daten-/Lizenzthema:** öffentliches Repository + privat recherchierte PDF-Originale; Code-MPL vs. zugelieferte Fremdrechte. Technisch mögliche Zugänglichkeit begründet keine legale Nachnutzung.
6. **Arbeitsmodus:** Copilot arbeitet an Glide; andere Agenten arbeiten an Steps-Shell. Gleichzeitiges Editieren eines unfertigen Glide-Kandidaten unterläuft eindeutige Regressions- und Herkunftsbelege.
7. **Design-/Plattformstatus:** 3.53.0 merged vs. QA-Text „main unverändert“; Commit-Status und Prüfnachweis gehören verschiedenen Zeitpunkten an. Keine Freigabe ohne aktuelle CI- und native Nachweise.
8. **Namenssystem:** STEP/Steps-Akronyme widersprechen sich; bis zur Inhaberentscheidung keine Akronymerklärung im Marketing.
9. **Crawlerzahlen:** 28 / 143 / 609 / ca. 123 / 199 / 262 / 462 müssen mit Datenart, Crawl-Scope, Batch-ID und Zeitstempel versehen werden; nicht als dieselbe Artikelmenge zusammenzählen.
10. **Dateiduplikate:** SHA-identische Dateien, inhaltlich ähnliche Markdown-Dokumente, mehrere Sprachfassungen, ältere Snapshots und echte redundante Dateien sind fünf unterschiedliche Kategorien.

## D. Unaufgelöste Nachweisfragen mit höchstem Entscheidungswert

- Sind alle **93** Glide-Quellmodule und **165** Ressourcen in der lokalen Arbeitskopie bytegleich zum verifizierten 3.53.0-HEAD? Der QA-Bericht nennt einen Prüfstand mit 93/165; hier wurde *nur* die hochgeladene Hauptdatei unabhängig bytegleich nachgewiesen.
- Gibt es schon nach Merge #75 eine vollständige Linux-/macOS-Vollmatrix für genau `9e767bea`? Der zuletzt gelesene QA-Report führt noch offene Freigabetore und alte Zeitform. Abfrage der konkreten Action-Runs/Artifacts bleibt notwendig.
- Welches ist das autoritative finale Research Paper neben zwei bereits existierenden Forschungsberichten? Die genaue finale Freigabe/Version wird aus den Pfaden allein nicht ersichtlich.
- Welche Originalbücher, Ableton-Quellen, Groove-MIDI/ZIP und Lizenzen sind tatsächlich zur Weiterverarbeitung und öffentlichen Abgabe freigegeben?
- Bedeutet die gewünschte Zweiteilung eine **sichtbare Sidebar + Workspace** oder zwei getrennte OS-Fenster? Ein Testprototyp kann die Entscheidung erleichtern, aber nicht ersetzen.
- Welche Funktionen sind *für v0.1* tatsächlich Pflicht: Editing, Playback, MIDI, Erklärung, Drums? „Langfristig gewünscht“ ist keine Akzeptanzdefinition.
- Wie wird die Zusammenarbeit der vielen KI-Umgebungen dokumentiert, wenn jeder Anbieter einen getrennten Chatkontext hat? Quellensicherung in Git und maschinenlesbare Handovers sind erforderlich.

**Vermerk:** Dieses Dokument nimmt *keine* heimliche Owner-Entscheidung vor. Vorhandene Quellen können untereinander widersprechen; der Bericht nennt die jeweilige Evidenzklasse, ohne alle Perspektiven zu einer einzigen Behauptung glattzubügeln.
