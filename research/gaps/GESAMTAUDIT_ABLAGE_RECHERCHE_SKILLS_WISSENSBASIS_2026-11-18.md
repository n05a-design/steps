# Ganzheitlicher Audit: Ablage, Recherche, Skills und Wissensbasis

- **Stand:** 18.11.2026
- **Prüfbasis:** `origin/main` bei `bfcb9b4f48beef36d723b1156ba71d85ce8967f1`. Der lokale Arbeitszweig steht bei `84f2c2c` und ist nicht mit diesem Stand gleichzusetzen.
- **Status:** Bestands-, Struktur-, Integritäts- und Stichprobenaudit. Keine vollständige unabhängige Fachprüfung jeder Musikbehauptung und keine Rechtsberatung.

## Ergebnis in Kürze

Die formalen Referenz- und Skillprüfungen bestehen. Das belegt weder die inhaltliche Richtigkeit des gesamten Forschungsbestands noch dessen Rechtefreigabe. Für die Vollständigkeit des Archivs, der Quellenclaims und der offenen Aufgaben fehlen weiterhin menschliche Reviews und ein verfügbarer kanonischer Aufgabenbestand. Besonders kritisch sind (1) öffentlich versionierte Volltext-Extrakte mit offenem Rechteprüfstatus, (2) ein Knowledge-Adapter, der Freigabe- und Quellenprüfungen umgeht, sowie (3) nicht aufgelöste Hash-/Pfadabweichungen im historischen Dateiregister. Es wurden keine Forschungsquellen, Claims, historischen Versionen oder Git-Objekte entfernt oder umgeschrieben.

## Befunde

### Hoch: Fremde Volltexte und Rechteinventar sind nicht synchron

- Im geprüften `origin/main` gibt es keine PDF-Dateien. Der [PDF-zu-Markdown-Migrationsindex](../../manifests/pdf_docling_markdown_2026-11-14.csv) enthält jedoch 60 Pfadzuordnungen: 47 zugehörige Markdown-Dateien liegen weiterhin im öffentlichen Git-Baum und sind sämtlich als `REVIEW_REQUIRED` markiert. 13 Zuordnungen fehlen; alle 13 tragen im Manifest den Marker `RESTRICTED_LOCAL_GITIGNORE`.
- Die 47 vorhandenen Markdown-Dateien sind extrahierte Volltexte, nicht bloß Zusammenfassungen. Das Entfernen der PDF-Binärdateien hat deren Textinhalt daher nicht aus dem aktuellen Repository entfernt. Der Index zählt Pfade, nicht eindeutige Werke.
- [`RIGHTS_POLICY.md`](../../knowledge/sources/RIGHTS_POLICY.md) verlangt für Fremdvolltexte und Fremdassets grundsätzlich eine lokale, `.gitignore`-geschützte Ablage. Dagegen dokumentieren das [datierte Rechteinventar](RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md) und der [Maßnahmenplan](../../docs/audit/rights_audit/recommended_mitigation_with_alternatives.md) eine Inhaberentscheidung, Klassen A–D und gespeicherte Webseiten weiter zu versionieren. Die Berichte stellen selbst klar, dass Rechte pro Quelle offen sind; die Begründung „öffentlich zugänglich“ ist kein Nachweis einer Weiterverbreitungslizenz.
- Der [aktuelle Rechtegenerator](../../scripts/audit_rights_and_public_repo.py) inventarisiert nur `.pdf`, `.html`, `.htm`, `.mid`, `.midi`, `.mp3`, `.wav`, `.png`, `.ico` und `.svg`. Ausgeschlossen sind unter anderem `.md`, `.css`, `.zip` und `.docx`. `origin/main` enthält 1.544 Markdown-, 52 CSS-, 6 ZIP- und 3 DOCX-Dateien. Nicht alle davon sind Fremdmaterial, aber der Bericht kann mit diesem Filter nicht behaupten, alle relevanten Assets seien geprüft.
- [`history_impact.md`](../../docs/audit/rights_audit/history_impact.md) grenzt seine Aussage ausdrücklich auf die Klasse-E-Volltexte im aktuellen Arbeitsbaum ein und weist auf fortbestehende Forks und Caches hin. Das ist von der weiter offenen Frage zu den Klassen A–D und den Web-Extraktionen zu unterscheiden.

### Hoch: Retrieval-Skill verspricht stärkere Grounding-Garantien als der Adapter umsetzt

- [`KnowledgeAdapter._load_data()`](../../src/steps/knowledge/adapter.py) lädt `reviewed_progressions.json` direkt, nicht über [`load_reviewed_catalog()`](../../src/steps/progression/reviewed.py). Letzteres prüft die getrennte [menschliche Freigabedatei](../../src/steps/progression/reviewed_progression_approvals.json), Fingerprints, Quellen-IDs, Rechte-Status und Musikdaten. Der Adapter setzt Claims stattdessen unmittelbar auf `verified=True`, weist ihren Zitaten `rights_status="approved"` zu und fängt Lade-/Parsingfehler mit `except Exception: pass` still ab. Heute sind Freigaben für die Pilotclaims vorhanden; der direkte Ladeweg umgeht die Sicherung aber bei künftigen oder beschädigten Daten.
- Die Sonderantworten für verminderte Septakkorde und `bVII` liefern im aktuellen Lauf alternative Deutungen ohne Claims oder Quellen. Der Smoke-Test `Bdim7` ergab `ALTERNATIVE_INTERPRETATIONS`, aber null Claims und null Quellen. Das widerspricht der [Skillvorgabe](../../skills/steps-knowledge/SKILL.md), fachliche Aussagen mit Source-ID und Locator zu belegen.
- Die Suche verwendet Teilstringvergleiche. Der kurze, mehrdeutige Prompt `C` lieferte die Claims zur Progression C–G–Am–F statt eine Rückfrage oder eine disambiguierte Antwort.
- [`test_twenty_five_eval_cases_matrix`](../../tests/test_knowledge_adapter.py) prüft, dass die 25 Eval-Einträge vorhanden und formal plausibel sind; es führt die Prompts nicht gegen den Adapter aus und vergleicht keine Antworten. Die sechs Adapter-Unit-Tests bestehen, decken aber nur wenige feste Prompts ab. „Zero Hallucination“ ist damit kein nachgewiesenes Testergebnis.
- [`registry.yaml`](../../knowledge/sources/registry.yaml) enthält sieben Produktquellen. Die Coverage-Prüfung führt alle sieben fachlich als offen. `rights_status: approved` bedeutet daher nicht, dass die aus diesen Quellen abgeleiteten Musikbehauptungen fachlich abgenommen sind. Historische Statuswerte in [`curated_sources_registry.yaml`](../../knowledge/sources/curated_sources_registry.yaml) sind laut Dateiheader ebenfalls keine Produkt- oder Distributionsfreigaben.

### Hoch: Quellenregister und Dateiinventar haben ungeklärte Abweichungen

- [`MUSIC_SOURCE_REVIEW_PROGRESS.csv`](../../knowledge/sources/MUSIC_SOURCE_REVIEW_PROGRESS.csv) enthält 1.895 Datensätze. Bei 1.862 Datensätzen mit prüfbaren Größen- und Hash-Metadaten stimmen 1.543 mit Pfad, Git-Blob, Größe und SHA-256 im geprüften `origin/main` überein; 134 Pfade fehlen und 185 vorhandene Dateien weichen bei Größe oder Hash ab. Ein Teil der fehlenden Pfade passt zu dokumentierten historischen Entfernungen; die Gesamtheit ist damit nicht automatisch als Verlust oder Beschädigung zu werten. Die verbleibenden Fälle müssen gegen die jeweiligen Migrations- und Versionsnachweise aufgelöst werden.
- Weitere 33 Registerzeilen erfüllen die Dateimetadaten-Voraussetzung nicht: 13 verweisen auf tatsächlich versionierte Null-Byte-Scraperdateien bzw. Textstubs mit dem korrekten Hash der leeren Datei; 15 `WEB-*`-Einträge sind konzeptionelle Online-Quellen statt Dateipfade; fünf weitere Null-Byte-Dateipfade sind im geprüften Baum nicht vorhanden. Dateiprotokoll und konzeptionelle Quellenrecords brauchen getrennte Typen; Null-Byte-Dateien dürfen nicht still als normale Quellen behandelt werden.
- Das externe kanonische Aufgabenregister ist nicht verfügbar: `STEPS_KNOWLEDGE_REGISTER` ist in dieser Umgebung nicht gesetzt, und der protokollierte Windows-Fallback im [Registerprotokoll](../../.agents/skills/steps-knowledge-curation/references/work_instructions_protocol.md) ist auf diesem macOS-Lauf nicht anwendbar. Der Repository-Snapshot ist datiert und kein Ersatz für die aktuelle Masterdatei. Das vorhandene `knowledge/sources/registry.yaml` ist das Produktquellenregister, nicht das Aufgabenregister.

### Hoch: Forschungs- und Fachreview sind trotz grüner Strukturprüfungen unvollständig

- Der Benchmark ergibt **92 PASS, 0 FAIL, 27 PENDING**. Offen bleiben unter anderem Meter/Spielbarkeit, alle zwölf Coach-Fälle, Provenienz, Graph-Knoten, historische Dateien und vier PPR-MIDI-Fälle. `PENDING` wurde nicht zu `PASS` umgedeutet.
- Die Coverage-Prüfung weist 66 Forschungsclaims aus: vier fachlich untersucht, 62 offen; 21 formale Befunde sind markiert. Von 97 Graphrelationen sind 41 begrenzte Stichproben gestützt, eine beanstandet und 55 offen. Die getrennte [Owner-Review-v2](../../knowledge/relations/GRAPH_HUMAN_REVIEW_v2.csv) dokumentiert 41 zustimmende Entscheidungen im jeweiligen Scope, 40 Patchvorschläge, 14 Vertagungen und zwei Ablehnungen. Die erzeugte [Graphmatrix](../../knowledge/relations/GRAPH_AUDIT_MATRIX.csv) bleibt bewusst `REVIEW_REQUIRED`/`AUSSTEHEND` und erlaubt keine Produktionsnutzung; die getrennte Review-Schicht wird noch nicht in Plan und Generator übernommen.
- 1.787 Research-Dateien, 347 Archivdateien, 9 Dateien im Quellenarchiv, drei Legacy-Wissensdateien und 74 historische Wissensaudits sind in der Coverage-Ausgabe inventarisiert, aber nicht als vollständig fachlich geprüft ausgewiesen. Diese Bereiche enthalten überschneidende historische Bestände; ihre Summen sind keine Anzahl eindeutiger Werke.

### Mittel: Relative Markdown-Links brauchen eine gezielte, preservation-first Nachprüfung

Ein heuristischer Scan des `origin/main`-Baums fand in 1.544 Markdown-Dateien 3.015 relative Linkziele und 681 Ziele, die im aktuellen Baum nicht aufgelöst wurden. Davon entfallen 384 auf `archive/` und `source_archive/`, 294 auf `research/`, zwei auf `docs/` und eines auf `skills/`. Historische Snapshots und ausgelagerte Quellen erklären einen Teil der Treffer; der reguläre Ausdruck ist kein vollständiger Markdown-Parser und die Zahl ist eine Kandidatenliste, keine Fehlerquote. Zwei konkrete historische Auditverweise zeigen auf nicht mehr versionierte `MusicTheory.pdf`- bzw. RTF-Pfade. Diese Verweise sollten als historische/extern geführte Quellen kenntlich gemacht werden, nicht durch Wiederherstellung fremder Volltexte „repariert“ werden.

## Durchgeführte Verifikation

| Prüfung | Ergebnis | Aussagegrenze |
| --- | --- | --- |
| Curation-Helper-Tests: `python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v` | 40 bestanden | Struktur, IDs und Recovery; keine musikalische oder rechtliche Freigabe |
| Referenzintegrität: `python3 -B .agents/skills/steps-knowledge-curation/scripts/check_reference_ids.py` | 390 Identitäten, 100 % | Identität und Referenzstruktur, nicht fachliche Wahrheit |
| Benchmark: `python3 -B scripts/run_knowledge_benchmark.py --scope all` | 92 PASS, 0 FAIL, 27 PENDING; Exit 1 wegen offener Fälle | PENDING bleibt blockierend |
| Coverage: `python3 -B scripts/audit_knowledge_coverage.py --check` | erfolgreich | Macht Inventar- und Reviewgrenzen sichtbar; kein Ersatz für Einzelreview |
| Knowledge-Adapter: `python3 -B -m unittest discover -s tests -p test_knowledge_adapter.py -v` | 6 bestanden | Eval-Datei wird hier nur strukturell geprüft; Grounding-Lücken siehe oben |
| Quelleninventar und PDF-Migrationsindex | Dateiregister gegen Git-Pfad/Blob/Größe/SHA-256 abgeglichen; alle 60 PDF-Manifestzeilen auf Extrakt-Präsenz und Status geprüft | Historisch fehlende Pfade bleiben einzeln aufzulösen |

## Priorisierte nächste Schritte

1. Rechteentscheidung je öffentlich versioniertem Volltext/Extrakt und Web-Asset mit Beleg festhalten; bis dahin weder `REVIEW_REQUIRED` als Freigabe behandeln noch automatisch löschen. Inventar und Policy auf dieselben Dateitypen erweitern.
2. Den Retrieval-Adapter an die geprüfte Veröffentlichungs-/Freigabepipeline anbinden, stille Datenfehler sichtbar machen, ungeprüfte/fehlende Quellen nicht als `approved` ausgeben und Eval-Prompts tatsächlich ausführen. Die inhaltlichen Claims dabei nicht automatisch ändern.
3. Die 134 fehlenden und 185 abweichenden Dateizeilen einzeln gegen historische Entfernungen, Neu-Versionen und Provenienzbelege auflösen; 13 Null-Dateien und 20 Nicht-Datei-Records separat typisieren.
4. Den Speicherort und die plattformübergreifende Erreichbarkeit des kanonischen Aufgabenregisters klären; den Repository-Snapshot ausdrücklich als historischen Snapshot belassen.
5. Graph-Owner-Entscheidungen nur mit eigener Prüfung in Plan/Generator übernehmen; die 27 Benchmarkfälle, Quellenclaims und Forschungs-/Archivbestände in begrenzten, belegten Review-Paketen abarbeiten.
6. Linkkandidaten nach aktivem Dokument, historischem Snapshot und bewusst ausgelagerter Quelle klassifizieren. Keine historische Datei oder Version ohne ausdrückliche Entscheidung ersetzen oder entfernen.

Die Musikmodell-Grenzen aus [`AGENTS.md`](../../AGENTS.md) bleiben verbindlich: DE/INT-Notation, Enharmonik, Kontext und funktionale Alternativen sind ausdrücklich zu erhalten. Dieser Audit erklärt offene Fragen; er erteilt keine fachliche, rechtliche oder Release-Freigabe.
