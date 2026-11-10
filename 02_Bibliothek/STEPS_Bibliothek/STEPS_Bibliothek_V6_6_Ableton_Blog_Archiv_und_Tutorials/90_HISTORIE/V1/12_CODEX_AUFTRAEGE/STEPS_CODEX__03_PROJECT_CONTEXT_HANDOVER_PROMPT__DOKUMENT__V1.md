# STEPS – PROJECT_CONTEXT_HANDOVER
## Prompt V1.0 | Vollständige Forschungs- und Projektübergabe

> **Anwendung:** Diesen Prompt im ursprünglichen Deep-Research-Chat ausführen, **nachdem** das abschließende Research Paper fertiggestellt ist. Der generierte Inhalt soll als `PROJECT_CONTEXT_HANDOVER.md` gespeichert und zusammen mit dem Research Paper an Codex übergeben werden.

### 1. Rolle und Ziel

Übernimm die Rolle eines Senior Research Documentation Architect, Knowledge Engineers und Technical Project Archivist.

Dein Auftrag ist, aus dem gesamten bisherigen Gesprächsverlauf und allen verfügbaren Projektunterlagen eine vollständige, nachvollziehbare und eigenständig verständliche Projektübergabe für das Open-Source-Projekt **Steps** zu erstellen.

**Projekt:** Steps – An independent, open-source chord progression app for exploring harmony & learning music theory.

**Ausgabedokument:** `PROJECT_CONTEXT_HANDOVER.md`

Dieses Dokument wird anschließend gemeinsam mit dem vollständigen Research Paper und den bestehenden Projektdateien an Codex übergeben.

Ziel ist nicht, das Research Paper zu ersetzen, sondern sämtliche Projektinformationen zu bewahren, die für eine spätere Weiterentwicklung, wissenschaftliche Wissensorganisation und technische Umsetzung wichtig sind.

Arbeite nach dem Prinzip:

**Preserve → Extract → Classify → Reconcile → Connect → Document → Transfer**

### 2. Vollständig auszuwertende Informationen

Untersuche, soweit tatsächlich verfügbar:

1. Den gesamten Gesprächsverlauf dieses Research-Chats.
2. Sämtliche ursprünglichen Nutzeranweisungen und nachträglichen Präzisierungen.
3. Den ursprünglichen `Master-Research-Prompt.md`.
4. Das abschließend erstellte Research Paper einschließlich Quellenverzeichnis und Anhängen.
5. Die bereits vorliegenden Forschungsdokumente:
   - `01_STEPS_Research_Foundation.md`
   - `02_STEPS_Knowledge_Base_Product_Blueprint.md`
6. Alle weiteren tatsächlich zugänglichen Anhänge, Bücher, PDFs, TXT-Dateien, Dokumentationen, Skill-Entwürfe, Links und Referenzen.
7. Relevante Zwischenentscheidungen, Korrekturen, Einschränkungen und Erkenntnisse aus der Diskussion.

Berücksichtige auch Informationen, die im finalen Research Paper nicht ausdrücklich wiederholt wurden.

Wenn Inhalte oder frühere Gesprächsteile nicht zugänglich sind, kennzeichne diese Lücke ausdrücklich. Rekonstruiere keine unbekannten Gesprächsinhalte.

### 3. Grundregeln der Dokumentation

**Keine relevante Information darf durch voreilige Verdichtung verloren gehen.**

Unterscheide konsequent zwischen:

- `CONFIRMED` – ausdrücklich bestätigte Projektentscheidung oder Anforderung
- `RESEARCH_SUPPORTED` – durch nachvollziehbare Forschung gestützte Erkenntnis
- `EXISTING` – nachweislich vorhandene Datei, Funktion oder Infrastruktur
- `PROPOSED` – vorgeschlagene, aber nicht beschlossene Lösung
- `HYPOTHESIS` – offene fachliche oder technische Annahme
- `CONFLICTING` – widersprüchliche Informationen oder Perspektiven
- `UNVERIFIED` – bislang nicht überprüfte Information
- `DEFERRED` – bewusst auf einen späteren Zeitpunkt verschobenes Thema
- `REJECTED` – ausdrücklich verworfener Vorschlag
- `UNKNOWN` – nicht feststellbarer Sachverhalt

Behandle Aussagen aus Research Papers nicht automatisch als verbindliche Projektentscheidungen.

Unterscheide den behaupteten Entwicklungsstand vom tatsächlich überprüften Entwicklungsstand.

Nutze die ursprüngliche Terminologie, soweit sinnvoll, und dokumentiere alternative Fachbegriffe.

### 4. Erwartete Dokumentstruktur

Erstelle die folgenden Abschnitte vollständig.

#### 01 – Executive Project Context

- Projektname und Leitidee
- Zielsetzung und langfristige Vision
- Aktueller Schwerpunkt
- Nutzen für die Zielgruppen
- Eigenständige Positionierung
- Abgrenzung gegenüber bestehenden Anwendungen
- Erwarteter Mehrwert der Wissensdatenbank
- Verhältnis zwischen Anwendung, Forschung und AI-/Codex-Skill

#### 02 – Project Origin & Evolution

Rekonstruiere die Entstehung und Entwicklung des Projekts innerhalb des verfügbaren Gesprächsverlaufs.

Dokumentiere ursprüngliche Motivation, initiale Anforderungen, später hinzugekommene Anforderungen, veränderte Schwerpunkte, inhaltliche Präzisierungen, frühere und aktuelle Prioritäten sowie verworfene oder verschobene Ideen.

Erstelle eine chronologische Entwicklungshistorie, soweit die Daten nachvollziehbar sind.

#### 03 – Requirements Register

Erstelle ein vollständiges Register der bekannten Anforderungen. Jede Anforderung erhält:

- Stabile ID, beispielsweise `REQ-001`
- Präzise Beschreibung
- Herkunft
- Priorität, falls festgelegt
- Status
- Abhängigkeiten
- Akzeptanzkriterium, soweit bestimmbar
- Verweise auf verwandte Entscheidungen

Gruppiere die Anforderungen in Forschungs-, Wissens-, Produkt-, Software-, Dokumentations- und Qualitätsanforderungen.

#### 04 – Existing Project State

Erfasse den bekannten technischen und organisatorischen Ausgangszustand:

- Python und Tkinter
- Bestehende Projektdateien
- Vorhandene Dokumentation
- Existierende `SKILL.md`-Entwürfe
- Bekannte Repository- oder Verzeichnisstrukturen
- Bestehende Funktionen und Komponenten
- Noch nicht implementierte Konzepte

Eine im Research Paper vorgeschlagene Datei oder Architektur ist kein Nachweis dafür, dass sie bereits existiert. Wenn der tatsächliche Repository-Zustand nicht geprüft werden kann, kennzeichne ihn als ungeprüft.

#### 05 – Research Foundation

Fasse den Stand der untersuchten Forschungsbereiche zusammen:

- Grundlagen der Musiktheorie
- Akkordtheorie
- Funktionale Harmonik
- Modalität und modale Harmonik
- Jazzharmonik
- Pop-/Rockharmonik
- Bluesharmonik
- Chromatische Harmonik
- Akkordprogressionen
- Reharmonisierung
- Voice Leading
- Computational Music Theory
- Algorithmische Harmonieanalyse
- Wissensrepräsentation
- Musikpädagogik
- Produkt- und Wettbewerbsforschung

Dokumentiere je Bereich Forschungsstand, wichtige Erkenntnisse, verbleibende Lücken und relevante Quellen. Verweise auf Kapitel des Research Papers, statt größere Abschnitte zu duplizieren.

#### 06 – Source & Reference Handover

Erstelle ein Übergaberegister aller identifizierten Quellen. Unterscheide:

1. Tatsächlich bereitgestellte und gelesene Quellen
2. Nur teilweise ausgewertete Quellen
3. Bibliografisch identifizierte, aber nicht beschaffte Quellen
4. Vorgeschlagene zukünftige Quellen
5. Technische Dokumentationen und Repositories
6. Forschungsdatensätze und musikalische Korpora
7. Produkt- und Inspirationsmaterial

Dokumentiere pro Quelle soweit bekannt Titel, Autor/Organisation, Jahr, DOI/ISBN/stabile URL, ursprünglichen Dateinamen, Fachgebiete, Forschungsrelevanz, Zugriffsstatus, Prüfstatus, Lizenzangaben und offene Prüfungen.

Bewahre `Initial Sources v1.0` als vorgeschlagenen Ausgangsbestand. Behaupte nicht, dass alle Originaldateien bereits in einem Git-Repository vorhanden sind. Kennzeichne nicht lesbare Dateien ausdrücklich, insbesondere bisher gemeldete Probleme.

**Temporäre Quellenmarker aus ChatGPT-Recherchen sind keine dauerhaften bibliografischen Referenzen.** Markiere Verweise, die Codex später in überprüfbare Quellenangaben überführen muss.

#### 07 – Scientific Findings & Knowledge Gaps

Dokumentiere wichtige Forschungserkenntnisse und verbleibende Wissenslücken. Unterscheide gut dokumentierte Grundlagen, unvollständig erschlossene Fachgebiete, fehlende Primärquellen, wissenschaftliche Kontroversen, fehlende formale Regeln, fehlende maschinenlesbare Beispiele, fehlende Test- und Evaluationsdaten sowie fehlende Verbindungen zwischen Harmoniemodellen.

Erstelle ein priorisiertes Gap Register mit stabilen IDs.

#### 08 – Knowledge Base Vision

Beschreibe die geplante Steps Knowledge Base mit ihren Ebenen:

- Raw Source Library
- Source Registry
- Theory Knowledge Base
- Progression Library
- Research Notes
- Product Inspiration Library
- Decision Records
- Validation & Test Library
- Skill References
- Project Documentation

Erkläre je Ebene ihre Funktion und unterscheide beschlossene Architekturen von Vorschlägen.

#### 09 – Music Theory Principles

Bewahre die wesentlichen fachlichen Leitprinzipien:

- Verschiedene musiktheoretische Schulen müssen unterscheidbar bleiben.
- Theoretische Aussagen benötigen ihren musikalischen Kontext.
- Regeln, Tendenzen und Interpretationen sind unterschiedliche Kategorien.
- Harmonische Analysen dürfen mehrere plausible Ergebnisse besitzen.
- Enharmonische Schreibweisen sind fachlich relevant.
- Pop-, Jazz-, Blues-, Modal- und klassisch-funktionale Harmonik dürfen nicht unkritisch vereinheitlicht werden.
- Strukturierte Musikdaten müssen nachvollziehbar mit Quellen und Erklärungen verknüpft sein.
- Musikalische Korrektheit und Nachvollziehbarkeit haben Vorrang vor scheinbar einfachen Algorithmen.

Ergänze weitere tatsächlich entwickelte Projektprinzipien.

#### 10 – Decisions & Decision Register

Erstelle ein vollständiges Register bekannter Entscheidungen mit stabilen IDs `DEC-001` usw. Erfasse Status, Ursprung, Begründung, betrachtete Alternativen, Konsequenzen, Abhängigkeiten und Datum, sofern bekannt.

Trenne verbindliche Nutzerentscheidungen von Empfehlungen des Forschungsteams.

#### 11 – Conflicts & Reconciliation

Vergleiche ursprüngliche Anforderungen, Zwischenforschung und Research Paper. Identifiziere Widersprüche oder geänderte Prioritäten. Berücksichtige insbesondere:

- Forschungsauftrag versus Implementierung
- Wissensdatenbank versus kompakter Skill
- Deterministische versus probabilistische Modelle
- Theoretische Universalität versus stilistische Kontextabhängigkeit
- Öffentliche Zugänglichkeit versus Wiederverwendungsrechte
- Aktueller Forschungsumfang versus spätere Drum-/Groove-Erweiterungen

Löse Konflikte nur bei ausdrücklicher Entscheidung oder eindeutiger Quellenlage auf, sonst dokumentiere sie als offen.

#### 12 – Product & UX Inspiration

Dokumentiere Chord Files, ModeWheel, The Chord Wheel und weitere untersuchte Anwendungen. Unterscheide allgemeine Idee, beobachtete Funktion, UX-Muster, technisches Konzept, eigenständige Steps-Idee und ungeprüfte Annahmen. Fremde Produktfunktionen sind keine implementierten Steps-Funktionen.

#### 13 – Risks & Constraints

Dokumentiere Risiken aus Urheberrechten, Lizenzkompatibilität, fehlenden/beschädigten Quellen, ungeprüften Aussagen, musiktheoretischen Generalisierungen, Datenmodellinkompatibilität, Wissensduplikaten, Provenienzlücken, technischer Komplexität und verfrühten Architekturentscheidungen.

Erstelle ein Risk Register mit Priorität und möglichen Maßnahmen.

#### 14 – Research-to-Development Traceability

Erstelle eine Verbindungsmatrix:

**Research Finding → Quelle → Wissensobjekt → Anwendungsfall → Validierung → Status**

Mache nachvollziehbar, wie Forschung zu verwertbaren und testbaren Projektbestandteilen werden kann.

#### 15 – Next-Step Codex Brief

Formuliere einen kompakten Übergabeauftrag für Codex: Eingangsdokumente, erster Repository-Check, vorhandene Forschung, Behandlung bestehender Dokumentation, aufzubauende Wissensstrukturen, fachliche Prioritäten, offene Entscheidungen, Quellenverifizierung, Versionierung und Qualitätssicherung.

**Der nächste Auftrag besteht darin, die bestehende Wissensbasis real aufzubauen, mit belastbaren Inhalten zu füllen und systematisch zu erweitern – nicht lediglich einen weiteren Architekturvorschlag zu schreiben.**

#### 16 – Open Questions & Backlog

Erstelle einen priorisierten Backlog mit stabilen IDs aus offenen Forschungsfragen, fehlenden Quellen, ungeprüften Behauptungen, ausstehenden Entscheidungen, nötiger Validierung und späteren Erweiterungen.

#### 17 – Handover Manifest

Dokumentiere Name, Version, Erstellungsdatum, berücksichtigte Eingaben, nicht zugängliche Materialien, maßgebliche Entscheidungen, Konflikte, offene Quellenprüfungen, verknüpfte Papers, unerfüllte Anforderungen und Voraussetzungen für den Codex-Auftrag.

### 5. Vollständigkeitsprüfung

Prüfe vor Abschluss:

1. Sind alle ausdrücklichen Nutzeranforderungen erfasst?
2. Sind spätere Präzisierungen erhalten?
3. Sind Vorschläge und Entscheidungen getrennt?
4. Sind Quellenbestände und Quellenstatus korrekt dargestellt?
5. Sind wichtige Widersprüche dokumentiert?
6. Sind Forschungsgebiete und Wissenslücken abgebildet?
7. Ist die technische Ausgangsbasis richtig eingeordnet?
8. Kann Codex ohne Zugriff auf diesen Chat weiterarbeiten?
9. Sind wichtige Informationen auf ihre Ausgangsmaterialien rückführbar?
10. Ist der folgende Codex-Auftrag eindeutig?

Fehlende Informationen dürfen nicht erfunden werden.

### 6. Ausgabeanforderungen

Erstelle das Dokument vollständig in deutscher Sprache mit geeigneten englischen Fachbegriffen. Verwende Markdown, Kapitel, stabile IDs, Tabellen und Querverweise.

Beginne mit folgendem YAML-Frontmatter:

```yaml
document_id: STEPS-PROJECT-CONTEXT-HANDOVER
version: 1.0.0
project: Steps
document_type: project-context-handover
status: draft
language: de
```

Setze den Status erst nach tatsächlicher Überprüfung auf `reviewed`.

Die Übergabe darf umfangreich sein. Kürze keine relevanten Entscheidungen, Anforderungen oder Forschungszusammenhänge allein zugunsten einer kurzen Zusammenfassung. Vermeide dennoch unnötige Wiederholungen des Research Papers und nutze Querverweise.

**Erwartetes Ergebnis:** Ein vollständig eigenständig nutzbares `PROJECT_CONTEXT_HANDOVER.md`, das zusammen mit dem Research Paper die maßgebliche Grundlage für den folgenden Codex-Auftrag bildet.

**Erstelle diese Übergabe jetzt vollständig anhand der tatsächlich verfügbaren Informationen.**
