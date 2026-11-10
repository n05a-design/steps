# Steps – kritische Gesamtprüfung V4: Fachentscheidung statt weiterer Scheinkonsolidierung

**Stand:** 10.11.2026 · **Auditstatus:** belastbare, aber begrenzte Prüfung von Dokumenten, Artefakten und ausgewählten GitHub-Dateien; keine technische, wissenschaftliche, juristische oder Produktfreigabe. **Untersuchte Baselines:** STEPS `75329fef46878a5ac816cef3690e612a9e8fe52c` (öffentlich, main), Glide `9e767bea5e21063466a28ac3a679406484ad5d5f` (main). Alle Empfehlungen sind Vorschläge, bis sie in einem dokumentierten ADR/PR angenommen werden.

## 0. Ergebnis, korrigierte Schlussfolgerungen und echter Prüfungsumfang

Die Überarbeitungen V1–V3 verbesserten die Dokumentation, erzeugten aber **kein geschlossenes System aus Primärbeleg → Entscheidung → testbare Spezifikation → Umsetzung → Abnahmenachweis**. Entscheidend sind nicht die Zahl der Berichtskapitel oder die Anzahl der registrierten Dateien, sondern *der Nachweis der für eine Entscheidung wesentlichen Eigenschaften*. Das ist der Hauptfehler aller vorherigen Runden.

- **Bestätigt:** sechs ursprüngliche Texte A–F mit insgesamt 2.612 Textzeilen; 89 lückenlos abdeckende Bereichszuordnungen; 39 unterschiedliche fenced Original-Codeblöcke (alle im historischen technischen Anhang inhaltlich identisch); 100 historische Konflikt-/Lücken-/Entscheidungs-IDs mit passenden Originalzeilen. Diese Abdeckungen betreffen **Text und Zuordnung**, nicht fachliche Wahrheit.
- **Bestätigt:** STEPS enthält am GitHub-Snapshot 1.931 versionierte Blobpfade (1.810 unter `research/`), fünf JSON-Schemas, ein leeres Quellenregister und einen strukturellen CI-Test; keine ausführbare Steps-Harmonie-/Drum-Anwendung wird dadurch nachgewiesen. 160 Gruppen identischer Git-Blob-IDs erzeugen 426 zusätzliche Pfade; Git-Blobs sind kein Werk-/Lizenz-/Leistungszähler.
- **Bestätigt:** V3-Installer bestand neun eng abgegrenzte Tests, akzeptiert aber ein völlig anderes, lokales Git-Repository ohne Remote, wenn `--expected-head` auf dessen aktuellen Commit gesetzt wird (lokal nachgestellt); sein Head-Gate ist damit **keine echte Steps-Repo-/Baseline-Identitätsprüfung**. Die selbst beigefügte Hashliste beweist allein keine Herkunft/authentische Freigabe (Manipulationsprobe nach Rehash bestanden). Die Testmethode ist korrekt auf ihren Scope, nicht ihre Sicherheitswerbung.
- **Neu bestätigt:** Der vorhandene Skills-Entwurf ist in keinem der üblichen projektspezifischen Autodiscovery-Pfade `.claude/skills/<skill>/SKILL.md` bzw. `.agents/skills/<skill>/SKILL.md` eingetragen. V3-Dokumente würden bei rein additiver Installation nicht automatisch durch bestehende `README.md`, `AGENTS.md` und `SKILL.md` gefunden. **Die Bibliothek existiert, aber ihre operative Nutzung ist nicht belegt.**
- **Getrennte Freigaben:** (1) Quellen-/Dokumentenstatus, (2) technische Engineering-Freigabe, (3) rechtliche Öffnung/Publikation, (4) tatsächlicher Produktnutzen. Für Steps sind alle außer Teilaspekten von (1) offen.

**Kein Re-Upload-Versprechen:** Ein neutraler, gezielt verlinkter Informationsstand ist einem erneuten „alle bisherigen Dateien plus neue Dateien“-ZIP vorzuziehen. Das vorliegende V4-Paket ist eine geprüfte Ergänzung zu den unveränderten Originalen und V3-Historien, keine rückwirkende Behauptung, dass 60 PDFs, sämtliche 112 MIDI-/16 MusicXML-Dateien oder alle historischen Git-Commits vollständig geprüft wurden.

## 1. Quelle, Evidenz und Autorität strikt trennen

### 1.1 Evidenzklassen

| Kürzel | Bedeutung | Zulässige Schlussfolgerung |
|---|---|---|
| **V** | Eigene Messung/Dateibefund am angegebenen SHA oder reproduzierter lokaler Test | Genau diese Eigenschaft im angegebenen Scope belegt |
| **D** | Schriftliche Behauptung aus historischem Original/README/PR | Behauptung ist dokumentiert, Ergebnis noch nicht validiert |
| **A** | Technisch/fachlich begründete Hypothese | Muss durch alternativen Test/Entscheidung geprüft werden |
| **O** | Wichtige Information fehlt oder Zugriff nicht gegeben | Weder positive noch negative Behauptung zulässig |
| **E** | Entwurfsentscheidung/Empfehlung | Nicht beschlossen, nicht implementiert |

**Quellenhierarchie:** Nutzerwunsch und expliziter Entscheidungsbeschluss für Ziel/Anforderungen; aktueller versionierter Code und zugehörige Tests für Funktionalität; fachliche Primärquellen und Originaldateien für Fachbehauptungen; Lizenztext und konkret genehmigte Weitergabe für Rechte; historische Reports für Entstehung/Alternativen; eigene Audit-Schlussfolgerungen nur mit Gegenprobe.

### 1.2 Nachweisbare Original-Abdeckung und ihre Grenzen

Originale: A `STEPS Project Export.md` (297 Zeilen), B `Projekt Overview.md` (159), C `Glide Kontext für Fable(2).md` (659), D `Project Definition & Positioning.md` (221), E `Forschungs- und Projektgrundlage.md` (900), F `Projektstatus- und Projektstartbericht.md` (376). Historische Übersicht `Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, Quellenabdeckung `Steps_Quellenabdeckung_2026-11-09.csv`, technischer Anhang `Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md`. Die 39 Codeblöcke wurden mit einem Parser für bündig und bis zu vier Leerzeichen eingerückte Markdown-Fences gezählt; der einfache Parser ohne Einrückung würde fälschlich 29 melden. Gerade daran zeigt sich, dass **Prüfsoftware ebenso wie Produktcode negative Gegenproben benötigt**.

Das V3-Historienregister enthält die 40 W-, 34 G- und 26 DEC-IDs mit je einer Originalzeile. Ein eigener Abgleich bestätigt 100/100 Textankern, **aber nicht**, dass diese Positionen individuell erledigt sind. Eine erneute „Umbenennung auf V4“ schließt keinen offenen Punkt. Das V4-Evidenzregister nennt für jede der 100 Positionen eine Prüfdomäne, einen Nachweistyp und ein individuelles Abschluss-Gate; bis auf separat belegte historische Sachstandsänderungen wird keine Entscheidung als genehmigt behauptet.

### 1.3 Fachbibliothek – sechs Mengen auseinanderhalten

1. **Dateipfade:** 1.931 Git-Blobs in Steps, 1.810 davon unter `research/` (Snapshot).
2. **Archivversionen:** z. B. 1.000 Blobpfade im eigenständigen V6.6-Teilbaum, eine andere Population als Repo-Gesamtbestand.
3. **Physische Inhalte:** 160 Git-Blob-Gruppen mit 426 zusätzlichen Dateipfaden; identisch heißt nicht entbehrlich.
4. **Bibliografische Werke/Ausgaben:** 20 benannte Ausgangsquellen, die als Dateien jeweils an zwei Pfaden nachweisbar sind; das ist weder 40 unabhängige Werke noch ein Rechtenachweis.
5. **Quellen/Claims:** Aussagen mit Werk, Ausgabe, Seite/URL, Abrufstand, Kontext, Gegenbeleg, Reviewer und Rechteverwendungsart. Bisher keine durchgängige Registrierung.
6. **Validierte Produktfunktionen:** separat an einem Steps-Commit und an echten Musikereignissen gemessen; aus 1–5 nicht ableitbar.

Insbesondere die historischen 28/143/199/262/462/609/123 Ableton-Werte sind verschiedenen Stichproben, Zeitpunkten und Definitionsregeln zuzuordnen. Sie dürfen weder addiert noch ohne Quellpopulation als gemeinsamer Fortschrittsprozentsatz dargestellt werden. Das V6.4-Fachstatistik-CSV enthält bei den dort **aufgeführten** Fachgebieten `reviews_fully_approved = 0`; daraus darf nicht rückwirkend auf jede andere Version oder jedes Einzelwerk geschlossen werden.

## 2. Was bisher methodisch zu kurz kam

| Untersuchungsdimension | V1–V3 | Kritische V4-Korrektur | Noch nötiger Primärbeleg |
|---|---|---|---|
| Produktidentität | mehrfach beschrieben, aber unterschiedliche Schritte | ein explizites PRD mit problemzentrierter Nutzeraufgabe, nicht nur Features | reale Persona-/Workflow-Beobachtung und Owner-Entscheid |
| Wettbewerb | lange Feature-/Preislisten | gleicher konkreter Task über Alternativen: Zeit, Fehler, Lerngewinn, Exportqualität | frische Produktdokumentation und reale Testversuche |
| Geschäfts-/Community-Modell | OSS und Beiträge genannt | Governance, Wartungskosten, Drittanbieterasset-Limits, Fork-/Markenpolitik unterscheiden | angenommene CONTRIBUTING-/Maintainer-Policy |
| Musiktheorie | Konzeptordner + Beispiele | Notation, enharmonisches Spelling, modale/tonale Mehrdeutigkeit, Stil- und Nicht-Western-Kontext prüfen | fachlich geprüfte Golden-Fälle samt Quelle |
| Harmonie vs. Drum | separate Funktionsfelder | gemeinsames Zeitmodell und Ereignisidentitäten vor UI und MIDI | ausführbarer M2-Vertikalschnitt |
| MIDI | „exportfähig“ als Ziel | SMF-Format, Tempo-Events, Tickauflösung, Note-On/Off-Reihenfolge, Kanalbelegung, DAW-Probe | unabhängiger Parser plus DAW-Import |
| MusicXML | archiviert/erwähnt | Notations- und Performancedaten getrennt; quantifizierte Verlustklassen | Roundtrip-Matrix |
| Playback/Audio | mit MIDI vermengt | Entscheidung Audio-Backend/Soundbank/Monitoring/Latenz und Lizenz | nativer Hör- und Gerätewechseltest |
| Persistenz | Glide-Reuse als Möglichkeit | atomisches Schreiben, unveränderliche Backups, Migration, Undo, Exporte, Absturzfälle | Stromausfall-/Schreibfehler-Simulation und Wiederöffnung |
| App-UX | Glide-GUI als Vorteil | echtes Einsteiger-/Fortgeschrittenen-Szenario, Keyboard, Kontrast, Audiofeedback, Screenreader | beobachtete Nutzer- und Plattformtests |
| Ausführbarkeit | Python-Scaffold | definierter `python -m steps`-/CLI-Start, dependency lock, Windows/macOS-Einstieg | frischer Clone, isolierter Test, Packaging |
| Glide-Reuse | 25 Pakete katalogisiert | erst ein isolierter, transparenter Reuse-Spike; App-Version nicht als SDK-Freigabe verwenden | Importgraph und Steps-Regression auf festem Glide-SHA |
| GitHub-CI | Strukturprüfung | Prüfjobs ohne riskante `paths`-Filter, alle Musikcodepfade; unerwartete Skips verhindern | echter PR-Check/Required-Check-Konfiguration |
| Sicherheitsprozess | Installer v2→v3 | kein automatischer Installer notwendig; V3 ohne remote-/externen SHA-Anker | manuell geprüfter Patch/PR |
| Skills/Agenten | `SKILL.md` als vorhanden bewertet | plattformspezifische Discovery, Quellretrieval, Injection-Isolation, stichprobenartiger Abruf | Aktivierungstest je Claude/Codex/ChatGPT |
| Bibliothek | „alles wachsen lassen“ | intakte Rohbestände privat, versionierte Metadaten, inkrementeller Ingestion-Job, Quarantäne | 3–5 echte Pilotquellen und Reproduzierbarkeit |
| Quellenrechte | Urheberrecht allgemein erwähnt | per Asset, Ausgabe, Nutzungszweck, Verbreitungspfad und Historie prüfen | Rechtebeleg/Einwilligung oder Sperrentscheidung |
| QA | Testzähler/ZIP-Hashes | Fehler-orientierte Tests mit unabhängigen Oracles und Fault Injection | SHA-gebundene Logs und negative Gegenprobe |
| Betrieb/Kosten | Tokenkonten statt Prozess | KI-Toolkosten, Agent-Koordination, Review-Fähigkeit, keine doppelte Arbeit | Arbeitsbudget und CI-Zeiten gemessen |
| Organisation | viele Dokumente | eine aktive Wahrheit je Entscheidung, ein Issue/ADR je offener Blocker | Owner, Datum, Beschluss, Referenz |
| Portabilität | Mac/Windows/Linux in historischen Glide-Proben | musiktheoretischer Core portabel, GUI/Playback austauschbar; mobile Apps später eigener Client | Plattform-ADR plus separater Build |
| Langzeitarchiv | Dateien/Archiv-Erhaltung | stable Source IDs, Linkmigrationen, Legacy-Redirects, externe Nachweis-Hashes | End-to-End Restore aus historischem Bestand |

## 3. Reproduzierte Kritik an V3-Werkzeugen

**Test R1 – falsches Repository nicht erkannt (V/P1):** lokales Git-Repository `UNRELATED_PROJECT` ohne `git remote` auf eigener Testbranch, sauber, ein Seed-Commit. V3-Installer mit V3-Paket, `--repo UNRELATED_PROJECT`, `--expected-head <dessen SHA>` lief im Dry-Run mit Exitcode 0 und meldete sieben geplante Additionen. Es gibt keinen `origin`-/Repository-Identifier-Gate und keinen package-seitig fest eingetragenen geprüften SHA. **Nicht daraus ableiten:** Der Installer habe hier außerhalb des Repositories geschrieben; getestet wurde nur der akzeptierte Dry-Run. **Abhilfe:** V4 enthält überhaupt keinen Installationsautomatismus. Für PR-Verwendung ist das korrekte GitHub-Repo vom Maintainer zu prüfen.

**Test R2 – Selbstmanifest ist kein Authentizitätsbeweis (V/P1 bei falscher Sicherheitswerbung):** isolierte Kopie des V3-Pakets, README mit neuer Zeile verändert, zugehörige SHA-Zeile im *selben* Paket angepasst. Der V3-Verifier meldete dennoch `MANIFEST 11 files SHA256-pass; HISTORY 100/100 IDs present`, Exitcode 0. Das ist erwartetes Verhalten bei einem Self-Hash, kein Programmierfehler des Hashalgorithmus. **Abhilfe:** extern bekannter, unabhängiger Digest und ggf. signierte Provenienz; Paketverifikation niemals als Echtheitsbeweis vermarkten.

**Test R3 – neun grüne Tests, aber nicht neun Sicherheitsgarantien:** alle neun V3-Unittests wurden erneut erfolgreich ausgeführt. `test_apply_and_idempotence_in_clean_repo` ruft jedoch nur **einmal** `--apply` auf; Idempotenz ist durch diesen Test nicht belegt. Testnamen und Wirkversprechen künftig gegen die konkreten Assertions prüfen.

**Test R4 – Quellenintegrität (positiv, V):** sechs Originaldateien sind in der V3-Privatlieferung unverändert lesbar; 89 Coverage-Ranges decken alle 2.612 Zeilen ab; 39 der 39 Original-Fenced-Blöcke liegen im technischen Appendix inhaltlich identisch vor; 100 historisch verzeichnete Beschreibungen passen jeweils zur angegebenen Originalzeile. Dies beweist formale Erhaltung, nicht wissenschaftliche Korrektheit.

**Sicherheitskonsequenz:** V2-Installer nicht anwenden. V3-Installer ebenfalls nicht als vertrauenswürdige Standardinstallation nutzen. Ein kontrollierter, manuell sichtbarer Git-Diff/PR ist für **wenige neue Markdown-Dateien** verhältnismäßiger als neue Installationsautomatik. Bestehende Dateien dürfen nur über separaten Review-Commit aktualisiert werden.

## 4. Neue, direkt überprüfte Repository- und Integrationsbefunde

1. **Schutzunterschied:** Steps `main` meldet `protected:false`; für Steps werden keine Rulesets über den abgefragten API-Endpunkt zurückgegeben. Glide `main` meldet `protected:true`. Ein detaillierter Steps-Protection-API-Endpunkt war zuvor 403; die Repo-Owner-Oberfläche muss die exakten Regeln bestätigen. P1-Gate vor großem Agentenbetrieb.
2. **PR-Prozess:** Steps zeigt derzeit ein gemergtes PR #1, aber die acht PR-Template-Checkboxen im Body sind nicht markiert; daraus ist **nicht** ableitbar, ob andere Prüfbelege existierten. Es fehlen nach der verfügbaren Issues-Suche aktuell selbständige Steps-Issues; das ist kein Beweis, dass keiner der 100 Altgaps bearbeitet wurde. Für kommende Arbeit Issue/ADR/PR verknüpfen.
3. **CI-Scope:** `.github/workflows/structure-check.yml` beschränkt Trigger auf bestimmte Pfade, ohne `app/**` und `src/**`. Die einzige ausgeführte Python-Anweisung des Jobs ruft die Strukturprüfung auf; `tests/test_structure.py` wiederholt diesen Check. Der Validator kontrolliert Ordner und JSON-/Required-Felder, weder vollständige JSON-Schema-Semantik noch Musikcode, MIDI, Save, UI oder Sicherheit. Required Checks können bei Workflow-Pfadskips ausbleiben/pending bleiben (GitHub-Doku).
4. **Skill-Erkennung:** Repository-Tree enthält genau `SKILL.md` in Root und `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md`; keine `.claude/skills/` und keine `.agents/skills/`. Claude Code und Codex dokumentieren unterschiedliche Discovery-Pfade. Ein Root-`SKILL.md` ist als Projekt-Dokument nützlich, aber keine nachgewiesene automatische Skill-Aktivierung in beiden Werkzeugen.
5. **Operativer Einstieg:** Root-`README.md` enthält nur ein Chord-Produkt ohne Drums und das Literal `&amp;`. `README_SETUP.md` enthält einen früheren `b42a990...`-Stand und historische Anweisungen für `bootstrap_steps.py --apply`, obwohl `main` bereits weiterentwickelt wurde. `docs/project/ARCHIVE_README.md` nennt ehemalige `01_Overview/`, `02_Technischer_Anhang/` etc., die im aktuellen Repository unter `docs/project/overview/`, `.../Technische Auswertung/` und `.../provenance/` liegen. V3 hatte weder Root-Index noch verbindliche Verlinkung dieser neuen Dokumente vorgesehen. Dies ist eine konkrete **Wahrheitsquellen-/Navigationslücke**.
6. **Quellenregister/Schema:** `knowledge/sources/registry.yaml` ist leer. `schemas/source.schema.json` fordert `id/title/kind/rights_status`, aber **keine belegte Ausgaberechtequelle**, bibliografische Edition oder Claim-ID. Ein Eintrag mit `rights_status: approved` kann dem JSON-Schema nach ohne Nachweis entstehen; ein Reviewprozess muss deshalb jenseits des Schemas sicherstellen, dass „approved“ echt ist. Eine spätere schema-v2-Migration ist sinnvoller als stummes Überschreiben.
7. **Musikmodell:** `schemas/progression.schema.json` beschreibt Takte und Strings von Akkorden; es fehlen notenscharfe Events, Start-/Endticks, Velocity, Drum-Spuren und Tempo-/Taktwechsel. Daher nicht als kanonisches Live-Musikprojekt verwenden, bevor der Funktionsumfang entschieden ist.
8. **Archivzählung:** V6.6-Unterbaum enthält **49 echte nummerierte Hauptverzeichnisse** und 1.000 Blobpfade; die in der Legacy-README aus Screenshots abgeschnittenen Namen 16, 22 und 43 lassen sich aus dem Live-Tree konkret auflösen. Nummern 21 und 39 sind jeweils doppelt benannt. Das ist eine Reparatur der Dokumentationsaktualität, **keine Löschfreigabe**.
9. **Ältere Abnahmen:** Glide `3.53.0`, Systemkatalog `1.15` und 25 Reuse-Kandidaten sind belegte Metadaten. Glide-Tests und QA-Claims anderer SHAs sind keine aktuelle unabhängige SDK-Abnahme für Steps.
10. **Öffentliches Roharchiv:** PDFs, Web-Snapshots, Bilder, `.download`, MIDI und MusicXML liegen sichtbar im öffentlichen Forschungsbaum. Große Dateien von ~53/52/47 MB sind im Tree vorhanden; daraus folgen organisatorische/Repository- und mögliche Lizenzrisiken, **keine rechtskräftige Beurteilung** einzelner Inhalte. Geheimnisse und personenbezogene Daten müssten ebenfalls gesondert geprüft werden.

## 5. Architekturentscheidung als falsifizierbarer Versuch

| Alternative | Vorteile | Kosten/Gefahren | Geeignet, wenn ... |
|---|---|---|---|
| **A: komplettes Glide-Fork** | schnell viele sichtbare UI-Funktionen | geerbte Task-Domain, Persistenz und `ListApp`-Kopplung, hohe Regression und Releasekosten | nur bei realem Vorteil nach repräsentativem Spike |
| **B: eigenständiger Core + selektive Glide-Adapter (präferierter Versuch)** | stärkste Trennung von Musik, UX, Herkunft, Testbarkeit; vorhandene Investition nutzbar | Adapterarbeiten und neue UI-Integration nötig | ein Testmodul und ein Widget isoliert laufen, ohne `glide`-App zu importieren |
| **C: vollständiger Neubau mit neutralem Desktop-Toolkit** | langfristig saubere App-Identität | Zeitkosten und Rückfall auf unbewiesene neue UI-Komponenten | Glide-Spike wirtschaftlich scheitert oder UX grundlegend anders sein muss |
| **D: gemeinsames Glide-/Steps-Framework vor App** | mögliches langfristiges Wiederverwendungspotenzial | verfrühte Abstraktion, hoher Pflege-/Kompatibilitätsaufwand | mindestens zwei echte Abnehmer mit stabilem Schnittstellenvertrag existieren |

**Entscheidungsvorschlag:** Zwei begrenzte Spikes statt Glaubenssatz. SPIKE-1 pure Funktion aus Glide übernehmen (Importgraph, Ressourcen, 10 Regressionen, Lizenzhinweise, keine Seiteneffekte, separater Steps-Datenpfad). SPIKE-2 ein GUI-Element einschließlich Light/Dark, Resize, Fokus, Keyboard, DPI, Lebensdauer mit künstlichen Daten. Scheitert einer der Spikes am definierten Gate, alternative UI-Shell dokumentieren statt endlose Glide-Reparaturen als Voraussetzung zu machen. **Glide muss nicht „für immer fertig“ sein, um Steps an einem pinnten Commit zu starten.**

### 5.1 Musik- und Laufzeit-Schnittstellen

Die primäre interne Sequenz ist **mehr** als eine Folge von Strings: `Project(id,schema_version)`, `Track(id,kind,instrument)`, `Event(id,track_id,start_tick,duration_tick,pitch_or_drum,velocity)`, `TempoMap`, `MeterMap`, optional `ChordInterpretation` und `NoteSpelling`. Positive Dauern, nichtnegative Startticks, eindeutige IDs, erlaubte MIDI-Tonhöhen [0,127], klare Takt-/PPQ-Konventionen und Fehlerkategorien sind festzulegen. Nicht nur Akkorde, sondern auch Drums, Pausen, längere Note-Holds, Mehrfachnotensätze, Überlagerungen und Tonartwechsel müssen abbildbar sein. Transposition ändert **Noten** nach expliziten Schreibweisenregeln, Percussion-Mapping nicht versehentlich.

**MIDI:** Standard MIDI File Type 1 als erster interoperabler Mehrspur-Kandidat; die tatsächlich gewählte Version, PPQ, Kanalbelegung, Tempo- und Meter-Metaevents, Track-Enden, gleichzeitige Note-Off/-On-Reihenfolge, Velocity-0-Notenabschlüsse, Laufzeit-/Exportverlustliste und General-MIDI-Percussionmapping schriftlich spezifizieren. MIDI-Export allein liefert ohne Synthesizer, Soundbank und Scheduling keine hörbare Audio-Preview. Ein Song-Metadaten-/Harmonie-Roundtrip muss über ein internes Steps-Projektformat garantiert werden, nicht durch Behauptungen über MIDI-/MusicXML-Verlustfreiheit.

**Daten:** Versioniertes, atomisch gespeichertes Projekt mit Checksums/Backup, Schema-Migrationsstrategie, `Undo/Redo` mit stabilen Event-IDs, kontrollierten Importfehlern und einer klaren Unterscheidung zwischen Harmonieinterpretation und notengenauer Performance. Keine automatische Migration des bestehenden Glide-Produktivordners.

**Produkt-MVP:** M1 Chord-only ist ein *technischer Durchstich*, nicht das endgültige Produkt. M2 enthält Chords **und** Drums, speichert/öffnet beide, exportiert einen gemeinsamen MIDI-Zeitraum und bietet entweder echtes Playback oder eine explizit anders lautende Produktbeschreibung. M3 Erklärungen müssen Evidenz/Interpretation auseinanderhalten; auch fachlich bestrittene/mehrdeutige Fälle getestet.

## 6. Wissensbibliothek/Skill – vom Datenlager zum prüfbaren Instrument

Fünf Typen: `Work` (Werk), `Edition` (Ausgabe), `Asset` (konkrete Datei/URL, SHA), `Claim` (Aussage mit Provenienz und Geltungsbereich), `Concept` (eigene Lehreinheit/Relationsmodell). Ergänzend `Review` (Prüfer, Zeitpunkt, fachliche Prüfung) und `UsagePermission` (welche Art Nutzung/Veröffentlichung). Keine ungebremste Kopie fremder Bücher in öffentliche Skill-Referenzen. Bei Claims mit gegensätzlichen Lehrtraditionen mehrere Lesarten statt harmonischer Mehrheitsbeschluss. Scores nur mit ausdrücklich getesteter Kalibrierung, ansonsten Erklärung/Unsicherheit ohne Scheingenauigkeit.

Eine erste Pipeline ist **3–5 sorgfältig freigegebene Beispielquellen**, nicht die theoretisch sofortige Erfassung von 60 PDFs und 1000 Archivdateien. `discover -> rights_gate -> work/edition ID -> raw asset hash -> extraction evidence -> claim/concept -> peer review -> negative example -> search index -> skill evaluation`. Jeder Schritt ist idempotent per Source-ID/Content-Hash; fehlende Rechte verhindern Weitergabe, nicht das Festhalten von Metadaten. Es muss geklärt sein, ob der Nutzer nur lokal forscht oder öffentlich publizieren will; Crawler müssen Quelle/robots/terms und Urheber-/Datenschutzaspekte beachten.

**Skill-Implementierung ist zielsystemspezifisch**: Quell-Skill als ein versionsgepflegter Master, wenige dünne Adapterkopien/Links zu Claude (`.claude/skills/music-harmony-coach/SKILL.md`) und Codex (`.agents/skills/music-harmony-coach/SKILL.md`) nur nach echter Toolprobe; ChatGPT-Upload-/Pluginpfad separat nach tatsächlichen Berechtigungen. Die Skills steuern Recherche und Prüfmethoden, „trainieren“ das Modell nicht persistent. Skill-Eval: Erfolg bei Quellen-Nachweis, deutsche B/H-Notation, Mehrdeutigkeit, Negativbeispielen, Prompt-Injection-Fällen, nicht nur sprachlicher Eleganz.

## 7. Governance, Veröffentlichung und OSS

Schutzregel für `main`: PR-Pflicht, Review/Owner-Freigabe, nicht überspringbare relevante Statuschecks, Force-Push-/Löschschutz nach Owner-Abwägung. Pflichtchecks sollten bei jedem PR anwendbar sein; Github Actions mit `paths`-Filter können einen verlangten Check im Status `Pending` lassen. Für übermäßig große Bibliothek kann eine zusätzliche *nicht erforderliche* Research-Prüfung selective sein. Direkte Zusammenführung ohne überprüfbaren Commit/Testbezug vermeiden.

MPL-2.0: Änderungen an unter MPL fallenden Quelltextdateien und deren Weitergabe haben ihre eigenen Pflichten; neu entstandene separate Dateien und fremde Bücher/Fonts/Artworks sind jeweils gesondert zu beurteilen. Software-Open-Source ist kein Freibrief für das gesamte Material. Rechtsbewertung mit einschlägig qualifizierter Stelle klären; insbesondere bei öffentlichen Rohbuchkopien, ZIP-/Downloadmaterial und alten Git-Commits. Reproduzierbare Metadaten aus eigener Beschreibung können bleiben, auch wenn Rohmaterial privat bleiben muss.

Dokumentation braucht **eine aktive Eingangstür**: Root README mit aktueller Produktdefinition + Review-Grenzen; `docs/project/README.md` als Index; `AGENTS.md`/`SKILL.md` als Agenten-Routing; historische Overview explizit als Quelle, nicht als parallele Entscheidung. Überholte `README_SETUP.md` / `docs/project/ARCHIVE_README.md` korrigieren beziehungsweise als Historie kennzeichnen. *Neue V4-Dokumente allein sind noch keine vollständige Aktivierung; dazu sind bestehende Dateien bewusst in einem getrennten PR zu ändern.*

## 8. Kritischer Pfad mit Freigabekriterien (keine fiktiven Daten)

| Gate | Lieferobjekt | Beweis, der Go rechtfertigt | Blockierende Ausgangsfrage |
|---|---|---|---|
| **G0** | Rechts-/Repository-Triage | file-level Risiko- und Maßnahmenregister; Owner sieht Schutzregeln; kein blindes Löschen/Force-Push | Darf das veröffentlichte Rohmaterial im Git-Bestand bleiben? |
| **G1** | Produkt-PRD und fünf ADRs | Chord+Drum-Scope, Zielplattform, Playback, Tempo/MIDI, Projektformat, Glide-Reuse explizit akzeptiert | Was ist der tatsächlich erste verwendbare Nutzerworkflow? |
| **G2** | Versionsfähiger musikalischer Domain-Core | unabhängige Goldenfälle für Tonhöhe, Notation, Akkordtöne, Mehrdeutigkeit, Drum-Events, Zeitmap, Negativfälle | Was ist die kanonische musikalische Wahrheit? |
| **G3** | Chord+Drum→MIDI→Save→Reload | getrenner externer Parser und mindestens eine reale DAW-Gegenprobe; keine Datenverluste/ungeprüfte Migration | Was kann ein Nutzer bereits zuverlässig tun? |
| **G4** | UI/Audio und Glide-Spike | zwei isolierte Glide-Spikes oder dokumentierte Alternativlösung; Keyboard/Fokus/Resize/Playback im Zielsystem | Ist die UI-Übernahme wirklich wirtschaftlich? |
| **G5** | Knowledge-/Skill-Pilot | 3–5 Quellen mit Werk→Edition→Claim→Concept→Rechte→Review→Skill-Nachweis und Negativtests | Wird Wissen zuverlässig gefunden und korrekt verwendet? |
| **G6** | Veröffentlichung | reale Plattformbauten, Lizenz/SBOM, fremde Medien geklärt, Restore, Accessibility und Produktnutzerprobe | Kann Steps öffentlich verantwortet werden? |

Kleine, nicht überlappende KI-Aufträge mit festem Repository-SHA und konkretem Test-Orakel sind günstiger als mehrere Modelle, die dieselben Dokumente oder die große UI gleichzeitig verändern. Zweitmeinungen ohne unabhängige Testdaten zählen nicht als Validierung. Kein Konto-Reset, Fable-Zugriff oder Tokenlimit wurde für den Nutzer selbst überprüft.

## 9. Gegenüberstellung und Korrekturübersicht

| Bisher | Nachgewiesenes Defizit | V4-Änderung | Verbleibendes Risiko | Nächster tatsächlicher Nachweis |
|---|---|---|---|---|
| V3 als sicherer Installer | fremdes Repo im Dry-Run akzeptiert; 9 Tests zu schmal; Self-Hash veränderbar | keine neue Installationsautomatik, reproduzierte Gegenproben | manuelle Übernahme kann weiterhin Fehler enthalten | PR-Diff, separate SHA und lokaler Git-Status |
| 100 Alt-IDs als „abgedeckt“ | nur Herkunft und Beschreibung geprüft, nicht Status/Resolution | jede Alt-ID in evidenztypisierter V4-Matrix | viele Fälle weiter offen | Issues/ADRs mit Original- und Live-Beleg |
| Skills vorhanden | nicht an Claude-/Codex-Projektpfaden, keine Aktivierungsprobe | konkrete Discovery-Gates | Agentenumgebung kann eigene Regeln haben | `/skills`/Skill-Test in jeder Umgebung |
| V3-Review erstellt | kein Einstiegspfad im Repository | kanonische Docs-Routing-Vorgabe | bis zum PR ist V4 ebenfalls nur Ergänzung | README/AGENTS/Docs-Index-Änderung |
| Glide als Fundament | Reuse-Kandidaten keine zertifizierten Komponenten | zwei isolierte falsifizierbare Spikes | Adapteraufwand noch ungemessen | Importgraph plus UI-Lifecycle/Test |
| 20 Quellen/Massenindex | Dateien statt geprüfter Claims | 3–5 vollständige Pilot-Datensätze | Fachreview/Rechte noch offen | Reviewprotokoll je Claim |
| Produktplanung | Harmony-first oder Produktion in einem Topf | Chord-only M1, Chord+Drum M2 mit gemeinsamem Zeitmodell | Nutzerwert/Audioentscheidung offen | beobachtete Nutzerreise und MIDI/Save |
| CI grün | nur Strukturcheck; Pfade schließen Musikcode aus | definierte GitHub-/Domain-/Release-Gates | keine aktive CI-Implementierung | echte PR-Checks auf Steps SHA |
| Open Source geklärt | nur Code-Lizenz geklärt | differenzierte Asset-/Provenienzkette | Rechtsstatus einzelner Dateien offen | Assetbezogene Publikationsentscheidung |
| „umfassend geprüft“ | PDFs/MIDI/HTML semantisch nicht vollständig untersucht | exakt benannte Coverage- und Unverified-Grenzen | vollständiges Fach-/Legal-Audit ausstehend | lokale Datei-/Rechte-/Parser-/Contentaudits |

## 10. Offene Entscheidung, wann die Prüfung vollständig wäre

Eine echte *End-to-End-Freigabe des Forschungsarchivs* würde einen lokal verfügbaren, vollständig auflösbaren Snapshot aller relevanten Originaldateien, stabile Hashes, Klarheit über den Quellen-/Versionsumfang, Rechte pro veröffentlichtem Asset und systematische Inhaltsauswertung erfordern. Sie ist weder durch Textkonsolidierung noch durch die vorliegenden Verbindungsrechte erreichbar. Eine *Freigabe der Software* benötigt unabhängig davon echte Builds und Tests am Steps-Commit. Ohne diese Belege bleibt „vollständig“ auf die gerade genannte formale A–F-Abdeckung beschränkt. Die 100 alten Punkte bleiben in `STEPS_V4_HISTORISCHE_POSITIONEN.csv`; die neuen Funde in `STEPS_V4_NEUE_BEFUNDE.csv`.

### Quellen und feste Belege

- GitHub STEPS Baseline: https://github.com/n05a-design/steps/tree/75329fef46878a5ac816cef3690e612a9e8fe52c
- GitHub Glide Baseline: https://github.com/n05a-design/glide-to-do/tree/9e767bea5e21063466a28ac3a679406484ad5d5f
- Steps CI: https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/.github/workflows/structure-check.yml
- Steps Registry: https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/knowledge/sources/registry.yaml
- Steps Skill: https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/SKILL.md
- Claude Code Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Codex Skills: https://learn.chatgpt.com/docs/build-skills
- GitHub skipped required checks: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs
- GitHub Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Mozilla MPL FAQ: https://www.mozilla.org/en-US/MPL/2.0/FAQ/
- § 44b UrhG: https://www.gesetze-im-internet.de/urhg/__44b.html

Diese Quellen belegen jeweils nur die unmittelbar zugeordneten Aussagen. Insbesondere enthalten die öffentlichen Rechts- und Normdokumente keine Einzelfreigabe der in Steps gespeicherten Dateien. 
