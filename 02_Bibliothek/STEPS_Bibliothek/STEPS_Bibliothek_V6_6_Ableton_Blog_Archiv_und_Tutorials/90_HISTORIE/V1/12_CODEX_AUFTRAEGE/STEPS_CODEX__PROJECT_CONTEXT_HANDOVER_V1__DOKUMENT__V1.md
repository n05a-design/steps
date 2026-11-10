---
document_id: STEPS-PROJECT-CONTEXT-HANDOVER
version: 1.0.0
project: Steps
document_type: project-context-handover
status: draft
language: de
created_at: 2026-11-08
source_cutoff: 2026-11-08
maintainer: unassigned
supersedes: null
related_documents:
  - 01_STEPS_Research_Foundation.md
  - 02_STEPS_Knowledge_Base_Product_Blueprint.md
  - Master-Research-Prompt.md  # im aktuellen Materialbestand nicht als eigenständige Datei nachgewiesen
---

# STEPS — PROJECT_CONTEXT_HANDOVER

**Version:** 1.0.0 · **Stand:** 8. November 2026 · **Status:** DRAFT — Arbeitsübergabe, noch nicht vom Projektverantwortlichen freigegeben  
**Projektleitbild:** *Steps — An independent, open-source chord progression app for exploring harmony & learning music theory.*  
**Adressat:** Codex beziehungsweise ein zukünftiges Forschung-/Entwicklungs-Team.  
**Funktion:** Vollständige Übergabe der bekannten Anforderungen, Entscheidungen, Ausgangsquellen, Forschungsrichtungen, offenen Fragen und Umsetzungsgrenzen. **Dieses Dokument ersetzt weder die Research Papers noch Originalquellen.**

## Dokumentationsregeln, Belege und Leseschlüssel

Der Erkenntnisstand stammt aus (a) dem in dieser Unterhaltung verfügbaren Projektverlauf; (b) den tatsächlich in dieser Sitzung bereitgestellten Anhängen; (c) den zwei abgeschlossenen Deep-Research-Berichten und deren Quellenexporten; (d) dem vorhandenen `SKILL.md`-Entwurf. **Eine Prüfung eines Git-Repositories oder der lokal auf dem Nutzerrechner vorhandenen Python-/Tkinter-Anwendung ist nicht erfolgt.** Ein im Research vorgeschlagener Pfad ist keine existierende Datei und eine Empfehlung ist keine Entscheidung.

| Status | Exakte Bedeutung | Verwendung |
|---|---|---|
| `CONFIRMED` | Explizite Nutzeranforderung oder bestätigte Projektrichtung | Bindend, bis der Nutzer sie ändert |
| `RESEARCH_SUPPORTED` | Durch benannte Forschungsquellen beziehungsweise überprüfbare Unterlagen gestützt | Fachbefund, nicht automatisch Produktentscheidung |
| `EXISTING` | In dieser Arbeitsumgebung als Datei oder konkreter Inhalt tatsächlich nachgewiesen | Existiert **hier**; kein Repository-Nachweis |
| `PROPOSED` | Empfohlene Architektur, Methode oder Funktion ohne Freigabe | Nicht als bereits beschlossen implementieren |
| `HYPOTHESIS` | Plausible, noch nicht belegte Annahme | Prüfen, nicht als Fakt ausgeben |
| `CONFLICTING` | Nicht vereinbare oder unterschiedlich formulierte Angaben | Widerspruch mit Verweisen erhalten |
| `UNVERIFIED` | Behauptung oder bibliografische Information ohne ausreichende aktuelle Prüfung | Validierung ausstehend |
| `DEFERRED` | Ausdrücklich später vorgesehen oder aufgeschoben | Nicht in aktuellen Forschungsumfang ziehen |
| `REJECTED` | Explizit abgelehnte Möglichkeit | Nicht stillschweigend erneut einführen |
| `UNKNOWN` | Nicht bestimmbarer Zustand | Offen benennen |

**Quellenreferenzierungsregel:** In diesem Handover bezeichnet `CTX-*` einen dokumentierten Gesprächsbefund, `DOC-*` eine Hauptunterlage, `SRC-*` eine ursprüngliche Datei, `WEB-*` eine recherchierte externe Quelle, `DEC-*` eine Entscheidung und `REQ-*` eine Anforderung. Diese IDs sind **Handover-IDs**, noch nicht die endgültigen IDs einer produktiven Knowledge Base. Externe URLs in der Research-Exportliste sind lediglich Recherchefundstellen, bis eine Einzelprüfung erfolgt. Flüchtige Chat-Zitate wie `turn0file...` oder `turn...search...` gelten **nicht** als dauerhafte Nachweise; sie sind anhand Dateiname, Autor/DOI/URL, Ausgabe und Abschnitt zu ersetzen.

**Maßgebliche Dokumente im bereitgestellten Paket:**

| ID | Dokument | Verifizierter Status | Rolle |
|---|---|---|---|
| `DOC-001` | `01_STEPS_Research_Foundation.md` | `EXISTING`, in der Sitzung als Markdown vorhanden und gesichtet | Jüngster ausführlicher Research-Bericht zu Theorie, Architektur, Daten und Skill |
| `DOC-002` | `02_STEPS_Knowledge_Base_Product_Blueprint.md` | `EXISTING`, vorhanden und gesichtet | Frühere vertiefende Produkt-, Funktions- und Knowledge-Base-Recherche |
| `DOC-003` | `SKILL.md` | `EXISTING`, in dieser Sitzung eingesehen | Vorläufiger Music-Harmony-Coach-Skill, **kein** finaler Steps-Skill |
| `DOC-004` | `Pasted text(8).txt` | `EXISTING`, vollständig eingesehen | Handover-Erstellungsauftrag V1.0, Grundlage dieses Dokuments |
| `DOC-005` | `Master-Research-Prompt.md` | `UNVERIFIED`: als Name im Handover-Prompt referenziert, hier **nicht** als selbstständige Datei vorliegend | Nur verwenden, sobald physisch verfügbar |
| `DOC-006` | `01_STEPS_Research_Foundation.json` / `_URLs.csv` | `EXISTING`, im Research-Export vorhanden | Originale Research-Metadaten und Web-Quellenliste |
| `DOC-007` | `02_STEPS_Knowledge_Base_Product_Blueprint.json` / `_URLs.csv` | `EXISTING`, im Research-Export vorhanden | Frühere Research-Metadaten und Web-Quellenliste |

Weitere Primäranhänge sind in [Abschnitt 06](#06--source--reference-handover) katalogisiert. Die Originaldateien und Research-Exporte befinden sich **nicht automatisch** im zukünftigen öffentlichen Git-Repository; Codex muss ihren tatsächlichen Ablageort vor Verwendung verifizieren.

---

## 01 — Executive Project Context

### 01.1 Mission und Positionierung

`CONFIRMED` — Steps soll eine **unabhängige Open-Source-Anwendung** für das Entdecken, Entwickeln, Verstehen und Erkunden von Akkordprogressionen und Harmonik sein. Die Kernidee ist nicht bloß eine Akkordliste, sondern eine musikalisch verständliche Exploration: Der Nutzer soll Beziehungen sehen und nachvollziehen, weshalb ein Akkord in einem gegebenen Kontext zu einem anderen führen *kann*.

`CONFIRMED` — Drei Wissensdomänen sind jetzt der eindeutige fachliche Schwerpunkt:

1. **Music Theory:** von Notation, Intervallen, Tonsystemen, Skalen, Akkordbildung und Modalsystemen bis zu fortgeschrittenen analytischen Konzepten.
2. **Chord Progressions:** Progressionsfamilien, Funktions-/Stufenbeziehungen, Analyse, Varianten, Harmonisierung und Reharmonisierung, Stimmführung, Spannung und Auflösung, Harmonic Rhythm sowie Generations- und Transformationsverfahren.
3. **Harmony:** funktionale, modale, chromatische, klassische, jazzbezogene und popularmusikalische Harmonielehre; unterschiedliche Schulen und ihre Grenzen.

`CONFIRMED` — Zunächst wird eine **breite, möglichst wenig vorgefilterte Rohquellenbibliothek** aufgebaut. Erst nach Katalogisierung, Vergleich, fachlicher Validierung und Verknüpfung dürfen Teilbestände zu einem gezielt einsetzbaren Agent-/Codex-Skill verdichtet werden. Die Wissensbasis soll dauerhaft erweiterbar bleiben.

`DEFERRED` — Genre-spezifische **Drum-Progressions/Drum-Patterns** sind aktuell kein Rechercheauftrag, sondern ausschließlich ein optionaler späterer Roadmap-Eintrag. Allgemeine Takt-, Timing- und Harmonic-Rhythm-Konzepte bleiben als Teil des harmonischen Datenmodells relevant, nicht als Einstieg in Drum-Datensätze.

### 01.2 Adressaten und Nutzen

| Perspektive | Erwarteter Nutzen | Entscheidungslage |
|---|---|---|
| Musiker und Songwriter | Akkordverbindungen entdecken und ausprobieren | `PROPOSED`: Zielgruppen noch nicht verbindlich segmentiert |
| Musiklernende | Musikalische Zusammenhänge visuell und verständlich erklärt bekommen | `PROPOSED` auf Basis des bestätigten Lernziels |
| Fortgeschrittene, Komponisten, Arrangeure | Reharmonisierung, alternative Lenses, Voice Leading, modale/chromatische Exploration | `PROPOSED` |
| Entwickler / Codex | Quellengebundene, testbare Fachgrundlagen statt ungeprüfter Prompt-Behauptungen | `CONFIRMED` als wesentlicher Zweck des Skills |
| Forschende / Maintainer | Nachvollziehbare Herkunft, kontrollierte Begriffe, reproduzierbare Entscheidungen | `CONFIRMED` als Wissensbankziel; Ausführung noch offen |

### 01.3 Drei miteinander verbundene, getrennt verwaltete Ebenen

- **Research Library:** unveränderte und bibliografisch beschriebene Quellen, Widersprüche, Versionen und Rechercheprotokolle. `CONFIRMED` als Ziel.
- **Music Knowledge Base:** fachlich geprüfte, strukturierte Concepts, Claims, Rules, Progressions, Beispiele, Gegenbeispiele, Verknüpfungen und Tests. `CONFIRMED` als Ziel; konkretes Schema `PROPOSED`.
- **Steps Application und Codex Skill:** Produkt-UI, künftige Engines und eine dünne Agent-Arbeitsanweisung, die relevantes Wissen abruft, prüft und für Entwicklung und Inhalte verwendet. Trennung als Architektur **`PROPOSED`**, nicht als implementierte Tatsache.

Die Forschung soll Antworten begründen; die App soll musikalische Optionen zeigen; Codex soll Entwicklung und Erweiterung auf dokumentierte Quellen und Tests zurückführen können. **Forschung ≠ Wissen nach Review ≠ Skill-Anweisung ≠ Produktfunktion.**

---

## 02 — Project Origin & Evolution

### 02.1 Überlieferte Motivation

`CTX-001` — Der Nutzer hatte zunächst eine lokale Python-/Tkinter-GUI-Basis und erste Wettbewerbsanalysen beziehungsweise Materialien gesammelt. Die App soll sich insbesondere von **Chord Files** inspirieren lassen, aber als eigenständige, offene Software entstehen. Ein erster Skill-Entwurf existiert.

`CTX-002` — Zusätzlich wurde eine Sammlung von PDF-Fachliteratur, Videoskripten und Produktunterlagen zur Musiktheorie, Harmonik, Mathematik, Reharmonisierung, Mode Wheels und zur Popularmusik angelegt; die 20 Dateien wurden in zwei Uploadblöcken bereitgestellt.

`CTX-003` — Der Nutzer stellte später klar, dass **breite Referenzen und vollständiges Domänenverständnis** wichtiger sind als eine sofortige Feature- oder Drum-Recherche. Er verlangte eine große Wissensbibliothek **vor** Filterung und Kondensierung auf den Skill.

`CTX-004` — Daraufhin wurde Deep Research mit dem Auftrag gestartet, wissenschaftliche/technische Quellen, Inspirationsprodukte, Wissensstruktur und einen Codex-Blueprint zu sammeln. Es entstanden zwei Berichte, die später als Markdown, JSON und URL-CSV in einem ZIP-Paket bereitgestellt wurden.

`CTX-005` — Danach bat der Nutzer um einen Master-Research-Prompt, dessen Ergebnis das Codex-Fundament bilden soll: Quellen, Richtungen, Entscheidungen, Planung und Wissensarchitektur auswerten und daraus dauerhafte Dokumentation schaffen.

`CTX-006` — Der zuletzt als Datei übergebene Prompt `STEPS – PROJECT_CONTEXT_HANDOVER`, Version V1.0, verlangt explizit eine separate **`PROJECT_CONTEXT_HANDOVER.md`** als Ergänzung zu den Research Papers und als Basis für den nächsten Codex-Auftrag.

### 02.2 Chronologische Ereignisse (nur belegbare Reihenfolge)

| Zeitraum | Ereignis | Überlieferung / Status |
|---|---|---|
| Vor dem 08.11.2026 | Lokale Python-/Tkinter-Basis, erste Skill-Datei, Konkurrenzrecherche, PDF-/TXT-Sammlung | `CONFIRMED` vom Nutzer berichtet; tatsächlicher lokaler Code `UNVERIFIED` |
| 08.11.2026 | Projektvision „Steps — An independent, open-source chord progression app ...“ genannt | `CONFIRMED`, `CTX-001` |
| 08.11.2026 | Große, quellenbasierte Bibliothek und Deep Research als Ausgangspunkt festgelegt | `CONFIRMED`, `CTX-002/003` |
| 08.11.2026 | Drums ausdrücklich auf Roadmap verschoben, Kernfokus nochmals eingegrenzt | `CONFIRMED`, `CTX-003` |
| 08.11.2026 | Uploads `1/2` und `2/2`: insgesamt 20 ursprüngliche PDF-/TXT-Dateien | `EXISTING`, siehe Quelleninventar |
| 08.11.2026 | Rechercheberichte `01_STEPS_Research_Foundation` und `02_STEPS_Knowledge_Base_Product_Blueprint` verfügbar | `EXISTING`, `DOC-001/002` |
| 08.11.2026 | Exportproblem beim Deep-Research-Download; ZIP-Ausgabe mit Markdown/JSON/CSV | `EXISTING` als Chat-Ausgabe, nicht gleichbedeutend mit Git-Commit |
| 08.11.2026 | Handover-Prompt V1.0 als Datei übergeben; Erstellung dieser Übergabe | `EXISTING`, `DOC-004` |

**Unbekannt:** offizielles Startdatum, Repository-Adresse, Branch, Commit, Lizenzentscheidung, Releases, bereits implementierte GUI-Funktionen, Teamgröße und Meilensteintermine. Keine Datierung dieser Sachverhalte ohne Repo-/Projektbeleg.

### 02.3 Prioritätswandel

Früher wurden optionale Rhythmus-/Drum-Ideen zusammen mit Harmonie- und Technikthemen erwähnt. Der spätere ausdrückliche Nutzerwunsch hat Vorrang: **Drum-Forschung jetzt aus dem Scope**. Die letzten Research-Paper-Vorschläge für Drum-Datensätze und Drum-Implementierungsphasen sind historische *Vorschläge*, keine verbindliche aktuelle Vorgabe. Die aktuelle Reihenfolge lautet: Rohbestand sichern → weitere fachliche Quellen sammeln → normalisieren und verknüpfen → validieren → Skills und App-Entwicklung fundieren.

---

## 03 — Requirements Register

**Prioritätssystem:** `P0` = aktuelle zwingende Forschungs-/Übergabegrundlage; `P1` = wesentlich für die anschließende KB-Aufbauphase; `P2` = spätere Ausarbeitung. Diese Prioritäten sind, sofern nicht aus dem Nutzerwortlaut abgeleitet, **Arbeitsprioritäten des Handovers**, nicht bereits verbindlich beschlossene Sprint-Prioritäten. In der Spalte „Beleg“ stehen `CTX-*`, `DOC-*` oder Entscheidungen.

| ID | Kategorie | Präzise Anforderung | Status | Prio | Beleg / Abhängigkeit | Prüfkriterium |
|---|---|---|---|---|---|---|
| `REQ-001` | Produkt | Eigenständige, offene Chord-Progression-App „Steps“ entwickeln | `CONFIRMED` | P0 | CTX-001 | Leitbild in Dokumentation erhalten |
| `REQ-002` | Forschung | Musiktheorie systematisch, einschließlich fortgeschrittener und konkurrierender Schulen, abdecken | `CONFIRMED` | P0 | CTX-003 | Themeninventar, Quellen und Lücken je Fachgebiet |
| `REQ-003` | Forschung | Chord Progressions einschließlich Aufbau, Zusammenhang, Variation und Analyse umfassend erschließen | `CONFIRMED` | P0 | CTX-003 | Progressions-Taxonomie mit Beispielen/Gegenbeispielen |
| `REQ-004` | Forschung | Harmonielehre inklusive modaler, chromatischer, klassischer, Jazz- und Pop-Perspektiven erfassen | `CONFIRMED` | P0 | CTX-003 | Separate, verknüpfte Harmonie-Lenses |
| `REQ-005` | Quellen | Vor Filterung eine umfangreiche Rohbibliothek samt zusätzlichen Referenzen aufbauen | `CONFIRMED` | P0 | CTX-002/003 | Bewahrte Quellen + erweiterbarer Index |
| `REQ-006` | Quellen | Die 20 Initialdateien und zusätzlichen Wettbewerbsanhänge als Bestand aufnehmen | `CONFIRMED` | P0 | DOC-001, SRC-001–020 | Datei-Manifest mit Zustand und Quellenpfaden |
| `REQ-007` | Quellen | Verfügbarkeit, Lesbarkeit, Lizenz und bibliografische Metadaten je Quelle unterscheiden | `CONFIRMED`/`PROPOSED` | P0 | DOC-001, DOC-004 | Kein `reviewed` ohne Prüfnachweis |
| `REQ-008` | Wissensbasis | Fakten, Konzepte, Regeln, Ausnahmen und Alternativanalysen strukturiert verbinden | `CONFIRMED` als Ziel | P1 | CTX-003, DOC-001 | Konzepte mit dauerhaften IDs und Evidenzlinks |
| `REQ-009` | Wissensbasis | Forschungswissen, Rohquellen und Skill-Regeln voneinander trennen | `CONFIRMED` als Zweck; Struktur `PROPOSED` | P1 | CTX-005, DOC-001 | Datenfluss dokumentiert; keine Rohbuch-Kopien in `SKILL.md` |
| `REQ-010` | Wissensbasis | Datenbank kontinuierlich erweitern, aktualisieren und versionieren | `CONFIRMED` | P0 | CTX-005/006 | Ingestion-, Änderungs-, Review-Prozess dokumentiert |
| `REQ-011` | Wissenschaft | Eigene Quellen, Forschung, Hypothesen und Empfehlungen unterscheidbar halten | `CONFIRMED` | P0 | DOC-004 | Jedes entscheidungserhebliche Claim hat Status und Quelle |
| `REQ-012` | Wissenschaft | Widersprüchliche Theorie-Modelle und mehrere plausible Analysen bewahren | `CONFIRMED`/`RESEARCH_SUPPORTED` | P1 | DOC-001, DOC-003 | Testfälle mit alternativen Lenses vorhanden |
| `REQ-013` | Qualität | Fachlich überprüfbare Tonarten-, Akkord-, Intervall-, Transpositions- und Progressionsbeispiele sichern | `PROPOSED` | P1 | DOC-001 | Reproduzierbare Testfälle und erwartete Ergebnisse |
| `REQ-014` | Qualität | Lizenz-, Urheber- und Provenienzprüfungen vor Veröffentlichung durchführen | `CONFIRMED` als Dokumentationsziel | P0 | DOC-004 | Public-/Private-Scope je Quelle nachvollziehbar |
| `REQ-015` | Produktresearch | Chord Files als zentrale Inspirationsquelle untersuchen | `CONFIRMED` | P0 | CTX-001, SRC-005, HTML | Feature-/Interaktionsanalyse mit Eigentumsabgrenzung |
| `REQ-016` | Produktresearch | ModeWheel, 4× Wheels of7, Chord Wheel und weitere Anwendungen einbeziehen | `CONFIRMED` | P0 | CTX-001, SRC-011/016/018 | Produktmatrix und Verifikationsstatus |
| `REQ-017` | Produkt | Harmonische Möglichkeiten sichtbar und verständlich machen | `CONFIRMED` als Produktziel | P1 | CTX-001 | UX-Anwendungsfälle, keine vorgetäuschte Implementierung |
| `REQ-018` | Software | Vorhandene Python-/Tkinter-Basis zuerst prüfen, nicht voraussetzungslos ersetzen | `CONFIRMED` als Ausgangslage / `PROPOSED` Vorgehen | P0 | CTX-001 | Codex hat Code und Abhängigkeiten inventarisiert |
| `REQ-019` | Software | Theorie-/Generierungslogik von der GUI trennen | `PROPOSED` | P1 | DOC-001 | ADR und technischer Test, noch keine Vorgabe |
| `REQ-020` | Skill | Vorhandenen `SKILL.md`-Entwurf bewahren und später zur KB-Zugriffsschicht weiterentwickeln | `CONFIRMED` als Ziel | P1 | DOC-003, DOC-001 | Unterschiede Alt-/Neuversion und Tests dokumentiert |
| `REQ-021` | Dokumentation | Vollständigen, eigenständig verständlichen Projektkontext übergeben | `CONFIRMED` | P0 | DOC-004 | `PROJECT_CONTEXT_HANDOVER.md` mit Registern |
| `REQ-022` | Dokumentation | Research Papers, Quelleninventar und ursprüngliche Entscheidungen querverlinken | `CONFIRMED` | P0 | DOC-001/002/004 | Stabile Crosslinks und fehlende Dokumente markiert |
| `REQ-023` | Codex | Nach Übergabe tatsächlich KB füllen, nicht nur weitere Architektur skizzieren | `CONFIRMED` | P0 | DOC-004 | Abnahme anhand angelegter Inhalte und Prüflogs |
| `REQ-024` | Roadmap | Drums nur als spätere Option führen; keine Drum-Pattern-Recherche jetzt | `CONFIRMED`, `DEFERRED` | P0 | CTX-003 | Aktuelle Aufträge ohne Drums-Datensätze |
| `REQ-025` | Governance | Jede Quelle, Regel und Entscheidung langfristig auffindbar und veränderungssicher pflegen | `CONFIRMED` als Ziel | P1 | CTX-005/006 | ID-/Versions-/Review-Konzept umgesetzt |
| `REQ-026` | Software | Interchange, Audio, MIDI/MusicXML und spätere Engine-Integration auf Eignung prüfen | `PROPOSED` | P2 | DOC-001/002 | Technische Spikes erst nach Repo-/Scope-Check |
| `REQ-027` | Produkt | Keine 1:1-Übernahme charakteristischer fremder Gestaltung oder geschützter Inhalte | `CONFIRMED` als rechtliche Grenze | P1 | DOC-001 | Eigenständige Designs, Nachweis pro Drittquelle |
| `REQ-028` | Forschung | Zusätzliche Standardwerke, Korpora, wissenschaftliche Papers und Tools einbeziehen | `CONFIRMED` | P0 | CTX-002/003 | Bibliografisches Register mit Quellenqualität und Lizenz |

**Offene Priorisierungsentscheidung:** Die Reihenfolge der späteren App-Features, das UX-Layout, der Umfang einer ersten funktionierenden Version und konkrete Implementierungsbibliotheken sind noch nicht durch den Nutzer bestätigt. Nur Forschungs- und Erschließungsprioritäten lassen sich zuverlässig ableiten.

---

## 04 — Existing Project State

### 04.1 Beobachtete Zustände versus Berichte

| Gegenstand | Nachweis | Status | Grenze |
|---|---|---|---|
| Python + Tkinter als GUI-Basis | Nutzeraussage | `CONFIRMED` als vorhandener Ausgangspunkt, **Code `UNVERIFIED`** | Keine Repo-, GUI- oder Testprüfung |
| Lokale Konkurrenzanalyse, Quellen und Referenzen | Nutzerangabe + Anhänge | Material `EXISTING` im Chat | Lokaler vollständiger Codex-Dateibaum ungeprüft |
| `SKILL.md` „music-harmony-coach“ | 4,9-KB-Markdown im Chat | `EXISTING`, Inhalt eingesehen | Darin verlinkte `references/...` und `assets/...` nicht als Dateien nachgewiesen |
| 20 PDF-/TXT-Initialquellen | Uploads Teil 1/2 und Teil 2/2 | `EXISTING` im Chat | Lese-/Lizenzstatus variiert; siehe Tabelle |
| Chord-Files-/ModeWheel-/Wheel-HTML | Weitere Anhänge | `EXISTING` im Chat | Webseiten-Snapshots, keine Aussage über aktuellen Live-Stand |
| Zwei Deep-Research-Berichte | Markdown und Forschungsdatenexport | `EXISTING` | Wissenschaftliche Einzelclaims weiter zu prüfen |
| Vollständiger `Master-Research-Prompt.md` | Im Handover-Prompt erwähnt | `UNVERIFIED` | Separater Originaltext nicht bereitgestellt |
| Repository, Branches, PRs, CI, Releases | Keine verifizierte Steps-Repo-Verbindung | `UNKNOWN` | Keine Erfindung von URL/Verzeichnis/Versionsnummer |
| Produktionsfähiger Musik-Engine-Code | Nicht vorgelegt | `UNKNOWN` | Research-Architektur ist keine vorhandene Implementierung |

### 04.2 Relevante Funktionen des bestehenden Skill-Entwurfs

`DOC-003` zeigt bereits **Arbeitsschritte** für Erklärung, Akkordfolgenanalyse, Progressionsentwicklung, Reharmonisierung, Unterricht und MIDI-/Notationsexport. Positiv und unbedingt zu bewahren sind:

- Explizite Unterscheidung **deutsch H/B** versus internationale B/B♭-Schreibung;
- Bestimmung von Tonart, Modus, Stil, Tempo, Besetzung und Komplexität;
- Prüfung konkreter Akkordtöne sowie enharmonischer und römischer Schreibungen;
- mehrere plausible funktionsharmonische/modale Lesarten statt erfundener Eindeutigkeit;
- Quellennachweise nur, wenn in tatsächlichen Referenzen belegt; keine erfundenen Seitenzahlen;
- strukturiertes Ergebnis vor weiterführender Theorie und separate MIDI-/MusicXML-Ausgabe, wenn die Laufzeit sie erlaubt.

Die `SKILL.md` verweist auf `references/music-theory.md`, `references/harmonic-analysis.md`, `references/chord-progressions.md`, `references/voice-leading.md`, `references/sources.md`, `references/ingestion-guide.md` und `assets/progression.schema.json`. **Es wurde nicht belegt, dass diese Dateien bereits existieren.** Daher nicht als fertig aufgebauten Skill darstellen.

### 04.3 Was ausdrücklich nicht als bestehend gelten darf

`steps/theory/`, `steps/harmony/`, `sources/raw/initial-v1.0/`, `normalized/`, `datasets/adapters/`, `tests/`, die benannten `AGENTS.md`- und Produktions-Skill-Dateien sowie JSON-/YAML-Schemata werden in den Research Papers überwiegend **vorgeschlagen**, nicht als existierende Dateien nachgewiesen. Gleiches gilt für Graph-UI, Generator, Playback, Korpusadapter und fortgeschrittene Reharmonisierungs-Engine.

---

## 05 — Research Foundation

Die beiden Reports bilden eine umfangreiche Forschungsgrundlage, keine vollzogene Implementierung. `DOC-001` ist Hauptreferenz für Theorie, Computational Music, Formate und Governance; `DOC-002` ergänzt Produktkonzepte, Wettbewerber, Erweiterungsoptionen und Lern-UX. Folgende Übersicht ist ein **Research-Coverage-Register**, keine Behauptung, dass jeder Themenbereich wissenschaftlich abschließend geklärt wäre.

| Bereich | Vorhandener Beitrag / Anschlusspunkt | Wichtige offene Arbeit | Hauptbezug |
|---|---|---|---|
| Notation, Pitch, Intervalle, Enharmonik | Grundlagenquellen, Skill-Notation-Regeln, Mathematik/Intervall-Dokumente | Normalisiertes Notationsmodell, Korrektur-/Grenztests | DOC-001 „Core representations“, SRC-009/019 |
| Skalen, Modalität, Familien | 4×7 Skalen, ModeWheel, Modi-Visualisierung | Modal- und Scale-Family-Taxonomie, diatonische Schreibweisen, Konflikte | SRC-011, SRC-016, DOC-001 |
| Akkordkonstruktion und Symbole | Theoriebücher; Chord-Files-Material | Chord-Symbol-Grammatik, Extensions, Alterationen, Slash-Bass | DOC-001, DOC-003 |
| Funktionale Harmonik / Stufen | Kadenz, Dominanten und Zwischendominanten in der Sammlung | Schule/Satzkontext, lokale Tonika und Modulation sauber trennen | DOC-001, SRC-005 |
| Modal Interchange / Mixture | Chord-Files-Praxis, Theorieabschnitte | Alternative Herkunft/Lenses und überprüfbare Beispiele | SRC-005, DOC-001 |
| Chromatische Harmonik | Research-Vorschläge: Neapolitaner, Augmented Sixths, Tritonussubstitution | Canonical cases und nicht-funktionale Lesarten | DOC-001 |
| Jazzharmonik | Research-Bücher, Chord-Scale-Beziehungen, ii–V–I | Eigener Jazz-Kontext, passende Referenzwerke, Voicings | DOC-001/002 |
| Pop/Rock und Blues | Jocelyn Neal, Fabbri, Harmonie-Perspektiven, Blues-Module | Loop-/rifforientierte Analysen ohne klassisches Funktionsschema | SRC-015/020, DOC-001 |
| Chord Progressions | Chord-Files-Visualisierung, Wheels, Reharmonisierung | Regeltypen, probabilistische Häufigkeit, Progression-Objekte | SRC-001/005/018, DOC-001 |
| Reharmonisierung | Sieben progressive Unterrichtsbeispiele als Transkript | Melody constraints, Substitutionen, Contra-Examples und Evaluationskorpus | SRC-001, DOC-002 |
| Voice Leading / Voicings | Skill-Grundregeln und Forschungsrichtungen | Spacing, Stimme, Register, Instrumente, Distanzmetriken | DOC-001; Tymoczko als externe Quelle |
| Computational Music Theory | AAAI-Paper zu formalisierten Regeln; Graph/Constraint-Ansatz im Report | Typisierte Rules + ausführbare Benchmarks, keine universellen Scores | SRC-003, DOC-001 |
| Harmonische Analyse / mehrere Lenses | Klassisch, Jazz, Pop, modal, chromatisch, Transformation | Formalisierte konkurrierende Analysen und Confidence-Policy | DOC-001/002 |
| Mathematik / Tonnetz / Neo-Riemannian | David Wright und Forschungsbibliografie | Formale Transformationen und Relevanz zu App-Interaktion | SRC-010, DOC-001 |
| Didaktik / Übungen | Berklee-Handbook, Theory Worksheets, Video-Lektionen | Prerequisite graph, Lernerfolg, Evaluationsaufgaben | SRC-004/012/014, DOC-002 |
| Produkt-/UX-Forschung | Chord Files, ModeWheel, Wheel-Ansätze, weitere Tools | Funktionsvergleich, eigenständige Interaktionshypothesen | DOC-001/002, HTML-Anhänge |
| Forschungsdatensätze | ChoCo, When in Rome, DCML und andere Kandidaten | Lizenzprüfung, Formate, Quality Audit, Korpus-Bias | DOC-001/002 |
| Ethik/Urheberrecht | Dokumentierte Unterscheidung Zugriff vs. Redistribution | Per-Datei-/Dataset-/UI-Rechte dokumentieren | DOC-001 „Licensing and IP“ |

**Fachlicher Kernbefund des Research (`RESEARCH_SUPPORTED` im Sinne von „als Forschungsergebnis im Bericht beschrieben“):** Eine erweiterbare App benötigt mehr als einen Einzeltonart-Algorithmus. Sie muss Repräsentation, musiktheoretische Analysemethoden, auslegbare Regeln, musikalische Beispiele und Provenienz verbinden. Der Bericht empfiehlt einen regelbasierten, erklärbaren Ausgangspunkt; corpus-/ML-basierte Rankings sind mögliche spätere zusätzliche Ebenen. Das ist **eine Empfehlung**, keine bereits getroffene Architekturentscheidung (`DEC-010`).

---

## 06 — Source & Reference Handover

### 06.1 `Initial Sources v1.0` — 20 tatsächlich hochgeladene PDF-/TXT-Dateien

**Bestandsstatus:** Alle folgenden Namen wurden als Anhänge bereitgestellt. Ein vollständiges wissenschaftliches Kapitel-für-Kapitel-Review der 20 Dokumente wurde **nicht** durchgeführt. „Sichtung“ bedeutet, dass Anfang/Inhaltsüberblick oder relevante Passagen in dieser Sitzung bzw. den Research-Berichten zugänglich waren; nicht, dass alle Aussagen bereits validiert sind. Lizenzangaben nur, wenn in der Quelle belegbar; ansonsten `ungeklärt` beziehungsweise `copyright presumed, reuse unverified`.

| ID | Originaldatei | Autor/Herkunft soweit erkennbar | Fachlicher Schwerpunkt / Rolle | Prüfstatus | Rechtehinweis |
|---|---|---|---|---|---|
| `SRC-001` | `7 levels of reharmonising Eleanor Rigby.txt` | Video-/Skripttranskript, genaue Herkunft nachtragen | Progressive Reharmonisierung; Melody-Note-Alignment; modale Varianten | TXT lesbar, inhaltlich ausschnittsweise gesichtet | Autor/Originalvideo und Reproduktionsrechte ungeklärt |
| `SRC-002` | `Chord FIles 2026 Showcase.txt` | Chord Files / Produktvideo, Sprecher im Skript | Produktphilosophie, Progressions, „Dark Harmony“, Scale-Lernen | TXT lesbar, inhaltlich gesichtet | Vermutlich Herstellerinhalt; Rechte prüfen |
| `SRC-003` | `Computational_Music_Theory.pdf` | Georg Boenn, Martin Brain, Marina De Vos, John ffitch; AAAI-Workshop 2012 | Logische Formalisierung musikalischer Regeln, ANTÓN/ASP, Gegenpunkt | PDF-Text und Titel/Abstract gesichtet | Lizenz der konkreten Ausgabe prüfen |
| `SRC-004` | `harmony as a student.txt` | Unterrichts-/Video-Transkript; vollständige Zuordnung nachtragen | Niedrigschwellige Harmonieerklärung, Spannung/Auflösung | TXT lesbar, gesichtet | Rechte ungeklärt |
| `SRC-005` | `How to use chord files.txt` | Chord Files / Jaka (laut Transkript) | Main Chords, Secondary Dominants, Modal Interchange, Resolution Arrows | TXT lesbar, fachlich besonders relevant | Hersteller-/Transkriptrechte ungeklärt |
| `SRC-006` | `Is_Generative_Theory_Misleading_for_Music.pdf` | Rafael Barbosa, 2019 | Kritik generativer Ansätze, GTTM, Musiktheorie und Kognition | PDF-Abstract/Einleitung gesichtet | HAL-Zugänglichkeit ≠ Freigabe aller Nutzungen; Lizenz prüfen |
| `SRC-007` | `Kants_Theory_of_Music.pdf` | Oliver Thorndike, 2021 | Musikästhetik, Affekt und Philosophie | PDF-Abstract gesichtet | Publikations-/Archivlizenz prüfen |
| `SRC-008` | `L-0002916879.pdf` | Theodor W. Adorno, *Current of Music*, engl. Ausg. Polity 2009 | Musik-, Medien- und Gesellschaftstheorie; Rahmenperspektive | Bibliografische Seiten gesichtet | **Expliziter Copyright-Hinweis, keine freie Redistribution nachgewiesen** |
| `SRC-009` | `MakingMusic.pdf` | nicht zuverlässig aus Originaldatei bestimmbar | Titel weist auf Musik-/Kompositionsmaterial hin; Inhalt offen | **DATEI BESCHÄDIGT/KEIN LESBARES PDF**: `file` meldet `data`, `pdfinfo` scheitert an Trailer/XRef; Ersatz beschaffen | unbekannt |
| `SRC-010` | `Mathematics_and_Music.pdf` | David Wright, 2009 | Intervalle, Frequenzverhältnisse, Intonation, Chromatik, Mathematik | Titel/Inhaltsverzeichnis gesichtet, Text zugänglich | Nutzungs-/Redistributionserlaubnis prüfen |
| `SRC-011` | `ModeWheel_Manual_1.21.pdf` | ModeWheel, Handbuch v1.2.1, Mai 2023 | Major/Melodic Minor/Harmonic Minor/Harmonic Major, Wheel, Keyboard, Playback, ii–V–I | Handbuchstruktur und Seiten gesichtet | Lizenzabschnitt gesondert prüfen |
| `SRC-012` | `Music_Theory_Advanced_Level.pdf` | Juni 2005; Autor nicht verlässlich erfasst | Fortgeschrittene Theorie, genaue Fachkapitel prüfen | PDF vorhanden, Text teilweise fehlerhaft extrahiert; visuelle Seitenprüfung erforderlich | ungeklärt |
| `SRC-013` | `Music_theory_handbook.pdf` | Berklee Online; Beiträge u.a. Denisch, Rochinski, Schmeling, Rendish | Kontrapunkt, Reharmonisierung, Rhythmus, Septakkorde, Blues | Inhaltsverzeichnis und Ausschnitte gesichtet | Herausgeber-/Autorenrechte prüfen |
| `SRC-014` | `Name_Music_Theory_Worksheet_Music_Theory.pdf` | Serenade Music Publishing, 2015 | Anfänger-Notation, Übungen, Curriculum | Anfang und Übungen gesichtet | Copyright, Wiederverwendung ungeklärt |
| `SRC-015` | `Popular_Music_Analysis_in_American_Music.pdf` | Jocelyn Neal, ZGMTH, 2003/05 | Geschichte und Methoden der Popularmusik-Analyse | Metadaten/Textanfang gesichtet | **CC BY 4.0 laut PDF**; Umfang/Attribution später bestätigen |
| `SRC-016` | `Scales with 4 smart tools.txt` | Video-/Lektionstranskript; Oliver-Prehn-/NewJazz-Bezug prüfen | Vier Siebenerfamilien, 28 Skalen, Akkord-Skalen-Beziehung, DIY-Wheels | TXT lesbar, gesichtet | Video-/Layoutrechte ungeklärt |
| `SRC-017` | `THE_ELEMENTS_OF_MUSIC.pdf` | Lehrkapitel; genaue Autorenschaft prüfen | Rhythmus, Melodie, Harmonie, Klangfarbe, Textur, Form | PDF-Einstieg und Tabelle gesichtet | ungeklärt |
| `SRC-018` | `the-chord-wheel.pdf` | Jim Fleser, Hal Leonard | Wheel-/Quintenzirkel-Konzept, Transposition, Komposition | Titel-/Illustrationsseiten gesichtet | Verlags-/Abbildungsrechte prüfen |
| `SRC-019` | `Understanding_Basic_Music_Theory.pdf` | Catherine Schmidt-Jones und Russell Jones (laut PDF) | Grundlagen, Tonhöhen/Notation, Harmonielehre | Umfangreiches PDF, Frontmatter und Inhaltsüberblick gesichtet | **CC BY 2.0 laut PDF-Frontmatter**, Original und Attribution erneut verifizieren |
| `SRC-020` | `What_is_popular_music_And_what_isn_t_An.pdf` | Franco Fabbri, *Musiikki* 2/2010 | Genres, Popularmusikdefinitionen, Kultur- und Analysekategorien | PDF-Inhaltsangabe gesichtet | Nutzungsrechte nachtragen |

**Spezifische Arbeitsmarkierung:** `SRC-009` nicht automatisch mit OCR bearbeiten oder in Fach-Claims überführen; zuerst Dateiherkunft, Format und Neu-Download prüfen. `SRC-012` benötigt gegebenenfalls visuelle Prüfung, da die Textextraktion deutliche Zeichensatzprobleme zeigte.

### 06.2 Produkt-/Web-Anhänge aus der ursprünglichen Konkurrenzrecherche

| ID | Lokaler Dateiname | Herkunft / Aussageart | Status | Nächste Aufgabe |
|---|---|---|---|---|
| `SRC-W01` | `-chordfiles.com.html` | Chord-Files-Startseite als HTML-Snapshot | `EXISTING` | Text/Datierung und Features gegen Live-Seite abgleichen |
| `SRC-W02` | `-examples(2).html` | Chord-Files-Beispiele | `EXISTING` | Beispiele strukturiert erfassen, nicht Layout kopieren |
| `SRC-W03` | `-store(2).html` | Chord-Files-Produkte/Varianten | `EXISTING` | Angebotsumfang und Editionshistorie prüfen |
| `SRC-W04` | `-upcoming(2).html` | Chord-Files-Produkt-/Neuheitenübersicht | `EXISTING` | Veröffentlichung vs. Roadmap unterscheiden |
| `SRC-W05` | `_modewheel.html` | ModeWheel-Website/Snapshot | `EXISTING` | Funktionen gegen PDF-Handbuch abgleichen |
| `SRC-W06` | `_modewheel-start.html` | ModeWheel-Startseite/Snapshot | `EXISTING` | Doppelung zu W05 markieren |
| `SRC-W07` | `Reddit-Users-chat-about-chord-files.html` | Communitydiskussion zu Chord Files | `EXISTING` | Meinungen als subjektive UX-Signale, nicht technische Tatsachen erfassen |
| `SRC-W08` | `The Chord Wheel.html` | Drittseiten-Artikel über Chord Wheel | `EXISTING` | Autorität und Primärquellen prüfen; SEO-/Sekundärquelle |

### 06.3 Externe akademische, offene und technische Referenzen aus dem Research

Diese Auswahl wird als **Acquisition Queue** übergeben. Eine Nennung im Research-Bericht bedeutet **nicht**, dass Werk oder Datensatz heruntergeladen, lizenziert, vollständig gelesen oder in die Steps-KB integriert wurde.

| ID | Quelle / konkrete Referenz | Relevanz für Steps | Bezug / Status |
|---|---|---|---|
| `WEB-001` | [Open Music Theory](https://viva.pressbooks.pub/openmusictheory/) / [About](https://viva.pressbooks.pub/openmusictheory/about/) | Breite Theorie, curricularer Aufbau, Stimmführung, Jazz/Pop; Lizenz und konkrete Edition prüfen | `PROPOSED` Acquire/Review; Research nennt CC BY-SA 4.0 für die Pressbooks-Ausgabe |
| `WEB-002` | [music21](https://github.com/cuthbertLab/music21) / [Roman Numerals](https://music21.org/music21docs/moduleReference/moduleRoman.html) | Vergleichsimplementierung für Symbol-/Stufen-/Tonartmodelle, Analyse | `PROPOSED`; Code-Lizenz getrennt von Corpus-Rechten prüfen |
| `WEB-003` | [ChoCo — Chord Corpus](https://github.com/smashub/choco) / [Fachpublikation](https://www.nature.com/articles/s41597-023-02410-w) | Heterogene Chord-Annotationen, Provenienz und interoperable Datenschemata | `PROPOSED`; Datensätze einzeln lizenzieren |
| `WEB-004` | [When in Rome — Meta-Corpus of Functional Harmony](https://reference-global.com/article/10.5334/tismir.165) | Functional-Harmony-Benchmark und mehrdeutige Roman-Analysen | `PROPOSED`; Lizenz-/Datensatzstand prüfen |
| `WEB-005` | [DCML/Harmonic Annotation — im Research beschrieben](https://github.com/DCMLab) | Formale Roman-/Harmonieannotierung, interoperable Vokabulare | `PROPOSED`; genaues Schema und Repo bestimmen |
| `WEB-006` | [Harte-Chord-Syntax — Forschungs-/Formatbezug](https://github.com/marl/jams) | Maschinenlesbare Akkord-Symbolsysteme; JAMS-Annotationen (nicht identisch mit Harte) | `PROPOSED`; Original-Harte-Spezifikation separat suchen |
| `WEB-007` | Fred Lerdahl & Ray Jackendoff, *A Generative Theory of Tonal Music* | Musikalische Hierarchie, gruppierende/zeitliche Strukturen | `PROPOSED`, Buch nicht in Initialbestand |
| `WEB-008` | Fred Lerdahl, *Tonal Pitch Space* | Harmonische Distanz, Spannung und Tonalraum | `PROPOSED`, Beschaffung und Rechte prüfen |
| `WEB-009` | Dmitri Tymoczko, *A Geometry of Music* | Geometrische Stimmführung und Akkordbeziehungen | `PROPOSED`, Rechte prüfen |
| `WEB-010` | Richard Cohn, *Audacious Euphony* | Chromatische Dreiklangbeziehungen, Neo-Riemannian Theory | `PROPOSED`, Rechte prüfen |
| `WEB-011` | Martin Rohrmeier, Arbeiten zur grammatischen Syntax tonaler Harmonik; [Forschungs-PDF](https://musicweb.ucsd.edu/~sdubnov/Mu270d/Harmony/Rohrmeier2011.pdf) | Hierarchische Regeln versus reine Markov-Prognosen | `PROPOSED`, Bibliografie/Version prüfen |
| `WEB-012` | Trevor de Clercq & David Temperley, Arbeiten zu Rock-/Pop-Harmonik-Korpora | Pop/Rock-Loop-Theorie und empirische Übergangsmuster | `PROPOSED`, Artikel und Datensatz einzeln identifizieren |
| `WEB-013` | [MIDI Association](https://midi.org/) | MIDI-Standard für spätere Wiedergabe/Export | `PROPOSED`, technische Phase |
| `WEB-014` | [W3C MusicXML](https://www.w3.org/2021/06/musicxml40/) | Notationsaustausch | `PROPOSED`, technische Phase |
| `WEB-015` | [Mido](https://github.com/mido/mido) / [pretty_midi](https://github.com/craffel/pretty-midi) | MIDI-Events und Export; keine alternative Harmonielehre | `PROPOSED`, Technikentscheidung offen |
| `WEB-016` | [Python Tkinter](https://docs.python.org/3/library/tkinter.html) | GUI-Baseline, nach bestehendem Repo-Check | `PROPOSED` als Dokumentationsreferenz |

**Wichtige Differenzierung:** Ein Formatstandard, eine Implementierungsbibliothek, ein Korpus und ein Theorie-Lehrbuch sind verschiedene Evidenztypen. ChoCo kann z.B. Häufigkeiten/Annotationen liefern, aber keine universellen musiktheoretischen Normen. Fachbücher liefern Konzepte, jedoch nicht automatisch offen lizenzierte Beispieldaten.

### 06.4 Quellen- und Lizenzregeln für Codex

- Für **jedes** Original: Dateiname, SHA-256, Größe, Typ, Erstelldatum/Importdatum (falls bekannt), `source_id`, Primär-URL, Autor, Titel, Auflage, Jahr, DOI/ISBN, Veröffentlichungs-/Nutzungsstatus dokumentieren.
- Zuerst `access_status` (besitzt die Datei?) und `read_status` (inhaltlich überprüft?) trennen; danach `license_status`, `redistribution_allowed`, `review_status` und `claim_ids` pflegen.
- Bücher und Produkt-Snapshots im privaten/rechtegeprüften Archiv belassen. **Nicht** automatisch in ein öffentliches Open-Source-Repository committen.
- Nur eigene Paraphrasen, zulässige Kurzbelege und offen lizenzierte, korrekt attribuierte Inhalte in öffentliche Lernmaterialien übernehmen.
- Anhänge mit unklarer Lizenz bleiben `REUSE_BLOCKED_PENDING_REVIEW`; technische Sichtbarkeit ist **keine** Nutzungserlaubnis.
- Dauerhafte Bibliografien statt `turn...`-Referenzen. Berichtsdateien und URL-CSVs gelten als Fundlisten, nicht als abgeschlossene Verifikation.

---

## 07 — Scientific Findings & Knowledge Gaps

### 07.1 Was bisher gut abgedeckt ist — mit Einschränkung

Die Initialsammlung liefert gute **Startpunkte** für musikalische Grundbegriffe, Skalen- und Wheel-Visualisierung, praktische reharmonisierende Beispiele, Popmusik-Methodendiskussion und eine mathematisch/computational Perspektive. Das bedeutet **nicht**, dass diese Gebiete bereits mit kanonischen Definitionen, zitierfähigen Seitenstellen, maschinenlesbaren Regeln und Tests erschlossen wären.

### 07.2 Wissenschaftliche Grenzen

1. **Nicht alle Harmonielehren sind kompatibel.** Eine klassische Funktion, eine Jazz-Chord-Scale-Lesart und eine modal/loopbasierte Pop-Analyse können dieselbe Progression unterschiedlich beschreiben.
2. **Klanggleichheit ist nicht Analysegleichheit.** Enharmonische Gleichheit in gleichstufiger Stimmung beseitigt nicht unterschiedliche Schreib-, Tonart- oder Funktionsbedeutungen.
3. **Regeln, Tendenzen, Statistiken und Präferenzen sind nicht austauschbar.** Ein typischer Dominantweg ist keine technische Pflicht für jedes Stück.
4. **Harmonischer Kontext umfasst Zeit, Melodie, Bass, Phrasierung, Stil und Form.** Bloße Akkord-Strings können mehrdeutig sein.
5. **Ästhetische Wirkungen sind kein universeller musikalischer Messwert.** Eine „dunkle“ oder „cinematische“ Progression kann als Nutzervorliebe modelliert werden, nicht als absoluter wissenschaftlicher Beweis.
6. **Korpora sind Stichproben.** Genre, Epoche, Annotation und Lizenz beeinflussen beobachtete Häufigkeiten.

### 07.3 Priorisiertes Gap Register

| ID | Wissenslücke | Auswirkung | Status | Vorgeschlagene Schließung | Prio |
|---|---|---|---|---|---|
| `GAP-001` | Vollständige Erschließung und SHA-/Lizenzprüfung Initialbestand fehlt | Fehlende belastbare Ausgangsdaten | `CONFIRMED` als Lücke | Source Audit, Defektliste, Autoren-/DOI-Check | P0 |
| `GAP-002` | Fehlender Zugriff auf ursprünglichen Master-Prompt als eigenständige Datei | Möglicher Kontextverlust | `UNVERIFIED` | Datei beim Codex-Handover ergänzen oder als nicht vorhanden belassen | P0 |
| `GAP-003` | Keine festgelegte Ontologie mit IDs und Relationships | Inkonsistente Fachbegriffe | `PROPOSED` | Controlled vocabulary + Konzeptkarten | P0 |
| `GAP-004` | Enharmonisches Spelling / regionale Symbolsysteme nicht formalisiert | Falsche Akkord- und Intervallausgaben | `PROPOSED` | Pitch-/Spelling-Regeln + Fixtures | P0 |
| `GAP-005` | Chord-Symbol-Grammatik/AST noch nicht nachgewiesen | Fehler bei alterierten/Slash-Akkorden | `PROPOSED` | Standards vergleichen + Parser-Testkatalog | P0 |
| `GAP-006` | Begrenzte Primärquellen zur Jazz-/Popular-/Modal-/Chromatik-Abgrenzung | Dominanz eines unpassenden Funktionsmodells | `RESEARCH_SUPPORTED` als Recherche-Lücke | Originalbibliografie + Lens-Notizen | P0 |
| `GAP-007` | Kein formaler Satz funktionaler/chromatischer Progressionsregeln | Unklare Engine-Logik | `PROPOSED` | Typisierte Rule Cards mit Vorbedingungen und Ausnahmen | P1 |
| `GAP-008` | Keine standardisierte Reharmonisierung mit Melodie-/Voicing-Constraints | Generierte Alternativen schlecht begründbar | `PROPOSED` | Melody-Note-/Guide-Tone-Testfälle | P1 |
| `GAP-009` | Fehlende Bewertungs-/Benchmarkcases und Gegenbeispiele | Fehlinterpretationen bleiben unerkannt | `PROPOSED` | Positive, negative und mehrdeutige Golden Cases | P0 |
| `GAP-010` | Korpus-/Annotation-Mapping und Dataset-Lizenz noch nicht geprüft | Statistiken und Integration unklar | `PROPOSED` | ChoCo/When-in-Rome/DCML-Evaluationsmatrix | P1 |
| `GAP-011` | Produktfeature-Katalog und UX-Evidenz nicht systematisch normalisiert | Unklarer Abstand zu Wettbewerbern | `PROPOSED` | Feature-Matrix, UX-Beobachtungen, Eigenständigkeit | P1 |
| `GAP-012` | Tatsächlicher Python-/Tk-Code- und Repo-Stand unbekannt | Falscher Codex-Ausgangszustand | `UNKNOWN` | Read-only Repo-Audit als erste Codex-Phase | P0 |
| `GAP-013` | Öffentliche Lizenzwahl und Quell-Veröffentlichungsstrategie offen | Rechts-/Community-Risiko | `UNKNOWN` | Lizenz-ADR und Legal Review | P1 |
| `GAP-014` | RAG/Suchindex-Versionierung und Reviewer-Workflow unbestimmt | Wissenswachstum ohne Qualitätssicherung | `PROPOSED` | Ingestion-/Review-/Conflict-Protokoll testen | P1 |
| `GAP-015` | Erfolgskriterien für App-MVP und erste Benutzergruppe nicht entschieden | Beliebiger Feature-Scope | `UNKNOWN` | Nutzungsfälle/UX-Prototypen getrennt evaluieren | P2 |
| `GAP-016` | Mehrfach begründbare Analysen nicht als Datenvertrag modelliert | Überkonfidente Erklärungen | `PROPOSED` | Multi-Lens-Outputschema + Gegenbeispiele | P1 |

---

## 08 — Knowledge Base Vision

### 08.1 Zielbild: dauerhaftes, differenziertes Wissenssystem

Die folgende Architektur ist **`PROPOSED`** und darf nach Repository-Audit angepasst werden. Sie entspricht den zehn vom Nutzer gewünschten Wissensebenen:

| Ebene | Zweck | Artefakte | Qualitätssicherung |
|---|---|---|---|
| Raw Source Library | Unveränderte Originale, soweit rechtlich zulässig | Checksums, nicht-öffentliche Dateien oder nur Manifeste | Immutable Manifest |
| Source Registry | Metadaten, Identitäten, Versionen, Rechte, Beziehungen | `sources.yaml`/CSV/SQLite | Pflichtfelder, Lizenz-Ampel |
| Theory Knowledge Base | Begriffe, Schulen, Regeln, Ausnahmen, Wissensgraph | Concept/Rule Cards | fachlicher Review + Gegenbeispiele |
| Progression Library | Analysierte Akkordfolgen, Transformationsketten, Timing | Progression-Objekte | Theorie-/Notationstests |
| Research Notes | Hinweise, Hypothesen, Unklarheiten, neue Papers | Notizen/Claims | Status, Review, Provenienz |
| Product Inspiration Library | Wettbewerber, UX-Patterns, eigenständige Ideen | Matrizen/Snapshots | Trennung Beobachtung ↔ Idee |
| Decision Records | Begründete technische und produktbezogene Entscheidungen | ADRs `DEC-*` | nachvollziehbare Freigabe |
| Validation & Test Library | Fachliche Goldens, Regressionen, Datenqualitätschecks | Testfälle und erwartete Werte | reproduzierbare Testläufe |
| Skill References | Kuratierte abrufbare Fachbasis für Agenten | `references/`, `SKILL.md`, Eval-Cases | Skill-Evals und Quellenbindung |
| Project Documentation | Roadmap, Architecture, Backlogs, Changelogs | Markdown, Versionen, Übersichten | PR-Review / Pflegeprozess |

### 08.2 Mögliche, **noch nicht angelegte** Dateistruktur

```text
Steps/                              # BESTEHENDEN Repo-Root ZUERST ERMITTELN
├── README.md
├── docs/
│   ├── context/PROJECT_CONTEXT_HANDOVER.md
│   ├── research/01_STEPS_Research_Foundation.md
│   ├── research/02_STEPS_Knowledge_Base_Product_Blueprint.md
│   ├── decisions/                     # ADRs
│   ├── roadmap/
│   └── architecture/
├── knowledge/
│   ├── registry/sources.yaml
│   ├── registry/concepts.yaml
│   ├── sources/manifest-initial-v1.0.yaml
│   ├── concepts/
│   ├── rules/
│   ├── progressions/
│   ├── theory-lenses/
│   ├── research-notes/
│   └── product-inspirations/
├── tests/
│   └── theory-fixtures/
└── .agents/skills/steps-music-theory/  # nur als Beispiel, tatsächliche Umgebung prüfen
    ├── SKILL.md
    ├── references/
    └── evals/
```

**Nicht-öffentliches Quellenarchiv:** proprietäre PDF-Originale, vollständige Buchkopien, urheberrechtlich geschützte Abbildungen/Transkripte und ungeprüfte Rohdatensätze **nicht** ungefragt in diesen öffentlich vorgesehenen Baum kopieren. Für sie zunächst ein außerhalb des veröffentlichten Repos geführtes Archiv und Repo-Manifeste erwägen; genaue Lösung bedarf eines ADR.

### 08.3 Datenobjekte und Beziehungen

Empfohlener minimaler Provenienzgraph:

```text
Source --supports/contradicts--> Claim --formalizes--> Rule
  |                              |                    |
  +--describes----------------> Concept <---uses----- ProgressionExample
                                     |                   |
                                     +--related_to-------+
                                     |
                                     +--evaluated_by--> TestCase
                                                            |
FeatureIdea --derived_from--> Inspiration/Claim --traced_to--> Decision
                                             |
                                             +--implemented_by--> CodeReference [nur wenn nachgewiesen]
```

Pflichtfelder einer **Source Card**: `source_id`, `title`, `author`, `year`, `source_type`, `local_path_or_url`, `sha256` (bei lokaler Datei), `license`, `read_status`, `review_status`, `topics`, `source_version`, `extracted_claims`, `review_notes`.

Pflichtfelder einer **Claim/Concept Card**: `id`, `canonical_term`, `aliases`, `definition`, `theoretical_lens`, `style_scope`, `conditions`, `counterexamples`, `evidence` mit *dauerhafter* Quelle/Abschnitt, `confidence_status`, `reviewed_by`, `review_date`.

Pflichtfelder einer **Rule Card**: `rule_id`, `rule_type` (`invariant`/`constraint`/`tendency`/`heuristic`/`interpretation`), `antecedent`, `consequent`, `scope`, `exceptions`, `evidence`, `tests`.

Pflichtfelder einer **Progression Card**: `progression_id`, `source_status`, `key/mode`, `chord_events` (Position/Dauer), `symbols`, `roman_degrees`, `analyses[]`, `style_scope`, `transformations`, `provenance`, `license`, `tests`.

Jedes Objekt erhält stabile IDs, Creation-/Review-Datum, Status und Backlinks. Ein schreibender Agent darf eine ungesicherte Forschungsnotiz **nicht** ohne Review in eine „kanonische“ Rule Card umklassifizieren.

### 08.4 Ingestion Lifecycle

1. Quelle finden oder Upload erhalten → eindeutige `SRC`-ID und Rohdaten-Checksum erzeugen.
2. Rechte/Originalzugang prüfen; Quelltyp und Lesestatus dokumentieren.
3. Titel-/Metadaten-Duplikate erkennen, aber getrennte Auflagen nicht wegwerfen.
4. Struktur und Kapitel indexieren; Abschnitte und zitierfähige Locators erfassen.
5. `Claims`, Definitionen, Beispiele, kontrastierende Analysen als **abgeleitete** Notizen anlegen.
6. Fachgebiete, Schulen, Schwierigkeitsgrade und Verknüpfungen zuordnen.
7. Vergleich mit bestehenden Claims: unterstützt / widerspricht / andere Scope / Duplikat.
8. Für überprüfbare Regeln Testfälle einschließlich Gegenbeispielen erzeugen.
9. Review-Gate: Quellenstelle, Theorie-Kontext, Rechte und Teststatus prüfen.
10. Erst danach Skill-Referenzen, Projekt-Dokumentation oder Produktanforderungen aktualisieren.
11. Änderungen mit `CHANGELOG`, IDs, versioniertem Manifest und Begründung protokollieren.

### 08.5 Recherche-Ausweitung ohne Wissensverlust

Aufnahme darf breit und redundanzfreundlich sein, Konsolidierung muss später **explizit** erfolgen. Mehrere Definitionen gleicher Begriffe dürfen nach Schule/Autor nebeneinander bestehen. Für Überarbeitungen den alten Claim nicht heimlich überschreiben, sondern mit `supersedes`, `scope_changed` und Version markieren. Ein RAG-/Index-Ansatz ist **Option**, nicht Voraussetzung für den initialen KB-Aufbau; Volltext-/Dateisuche kann zuerst genügen.

---

## 09 — Music Theory Principles

Die folgenden Leitlinien sind im Skill-Entwurf angelegt und/oder durch die vorliegenden Research-Berichte als sachlich geboten begründet. Sie sind **fachliche Qualitätsgrundsätze für die geplante KB**, nicht Beleg einer bereits fertiggestellten Engine.

1. **Kontext vor Etikett:** Ohne Tonart, Modus, Zeit/Position, Melodie, Bass und Stil ist eine Funktionsdeutung oftmals unbestimmt.
2. **Schulensensitivität:** Klassische Funktionen, Stufenharmonik, Jazz-Chord-Scale, Blues, Pop/Rock-Loops und Transformationsmodelle nicht unterschiedslos zusammenführen.
3. **Mehrdeutigkeit ist kein Fehler:** Bei mehreren plausiblen Analysen Alternativen mit Begründung angeben; nicht künstlich „eine richtige Antwort“ erzwingen.
4. **Regeltyp explizit:** Unveränderliche Notations-/Intervall-Definitionen von typischen stilistischen Tendenzen, Corpus-Häufigkeiten und Präferenzen trennen.
5. **Enharmonik ernst nehmen:** Klanggleichheit F♯/G♭ bei 12-TET ist nicht dieselbe Theorie-/Funktionsschreibung.
6. **Regionalnotation explizit:** Deutsch `H`/`B` und international `B`/`Bb` nicht stillschweigend vermischen.
7. **Voice Leading nicht auf Grundtonbewegung reduzieren:** Berücksichtige gemeinsame Töne, Guide Tones, Halbtonbewegung, Register, Besetzung, Dopplungen und Gegenbewegung.
8. **Melodie-Harmonie-Beziehung bedingt:** Melodieton als Akkordton ist oft hilfreich, aber bewusste Dissonanz und Auflösung sind legitim.
9. **Tonalität und Modulation nicht überinterpretieren:** Einzelne Zwischendominante ≠ zwingender Modulationsnachweis.
10. **Mood ≠ Wissenschaft:** „dunkel“, „nostalgisch“, „cinematic“ sind stilistische/psychologische Beschreibungen und keine objektiven formalen Akkordkategorien.
11. **Erklärbarkeit:** Bei automatischen Empfehlungen wenn möglich die Entstehungsbeziehung, Regel, Evidenz und Grenzen anzeigen.
12. **Provenienz:** Eine aus einer Quelle abgeleitete Regel benötigt einen überprüfbaren Beleg; Modellallgemeinwissen nicht als Buchzitat ausgeben.
13. **Bestand ist kein Wahrheitsbeweis:** Lehrbuch, Website oder Korpus können Fehler, systematische Auslassungen und kontextgebundene Aussagen enthalten.
14. **Offene Produkte ≠ freie Fremdtexte:** Forschung, Data Ingestion, UI-Gestaltung und Redistribution juristisch trennen.
15. **Komposition als Möglichkeitsraum:** Nutzerentscheidungen nicht als „theoretisch einzig beste nächste Akkorde“ verengen.
16. **Reproduzierbare Berechnung:** Tonhöhe, Intervall, Akkordtöne, römische Stufen und Transformationen mit Golden Cases prüfen; KI-Deutungen getrennt halten.

---

## 10 — Decisions & Decision Register

Die Tabellenzeilen sind die übergebenen Entscheidungen **und** Vorschläge; der Status verhindert eine Verwechslung. Kein Eintrag mit `PROPOSED` gilt als vom Nutzer freigegeben.

| ID | Entscheidung / Richtung | Status | Herkunft, Begründung und Alternativen | Nächste Konsequenz |
|---|---|---|---|---|
| `DEC-001` | Projektname und Vision „Steps … independent, open-source chord progression app“ | `CONFIRMED` | CTX-001; Name und Ziel vom Nutzer | In README/Projektbrief beibehalten |
| `DEC-002` | Der unmittelbare Forschungsfokus ist Musiktheorie, Chord Progressions, Harmonie | `CONFIRMED` | Spätere ausdrückliche Nutzerpräzisierung CTX-003 | Andere Domänen zunächst zurückstellen |
| `DEC-003` | Rohwissen möglichst breit sammeln, **vor** Kondensierung zum Skill | `CONFIRMED` | CTX-002/003; Alternative: sofortige kompakte Skill-Datei nicht gewünscht | Archiv + Registry zuerst |
| `DEC-004` | Drum-Patterns ausschließlich als zukünftige Roadmap-Option | `CONFIRMED` / `DEFERRED` | CTX-003, nachträgliche Korrektur des Research-Auftrags | Keine aktuelle Drum-Research-Workstream |
| `DEC-005` | Chord Files als besonders wichtige Inspiration | `CONFIRMED` | CTX-001; Produktinspiration statt Nachbau | Strukturierte Funktions-/UX-Analyse |
| `DEC-006` | ModeWheel, 4x7 Wheels und Chord Wheel mit betrachten | `CONFIRMED` | CTX-001/002 | Wheel-/Modus-Interaktionen katalogisieren |
| `DEC-007` | Vorhandene Python + Tkinter-Basis in Codex berücksichtigen | `CONFIRMED` als Nutzeraussage | CTX-001; tatsächlicher Code noch ungeprüft | Read-only Codeaudit vor Architekturentscheidung |
| `DEC-008` | Research Paper und Kontextübergabe als getrennte, komplementäre Unterlagen | `CONFIRMED` | CTX-005/006 | Handover auf Research verlinken, nicht duplizieren |
| `DEC-009` | Breite Knowledge Base bleibt unabhängig von kompakter Skill-Anweisung | `CONFIRMED` als strategisches Ziel; konkrete Pfadwahl `PROPOSED` | CTX-005/006, DOC-001 | KB zuerst real aufbauen |
| `DEC-010` | Deterministischer, erklärbarer Rule-/Graph-Ansatz zuerst; Statistik/ML später | `PROPOSED` | Empfehlung DOC-001; Alternative: probabilistisch/ML-first | ADR + Spike nur nach Prüfung |
| `DEC-011` | Theorie-Engine unabhängig von Tk-GUI strukturieren | `PROPOSED` | Empfehlung DOC-001; Alternative: bestehende monolithische Tk-Struktur | Nach Code-Audit entscheiden |
| `DEC-012` | `music21` als erste fachliche Referenzbibliothek untersuchen | `PROPOSED` | DOC-001, Kosten/Kompatibilität/Abhängigkeiten ungeprüft | Vergleich und Lizenzcheck |
| `DEC-013` | ChoCo und When in Rome als erste Korpus-/Benchmark-Kandidaten | `PROPOSED` | DOC-001/002, Datenrechte/Qualität offen | Acquisition- und Schema-Audit |
| `DEC-014` | Harmonische Beziehungen als begründeter Graph sichtbar machen | `PROPOSED` | DOC-001/002; Alternative: feste Wheels, Listen, Tabellen | Eigenständige UX-Konzepte vergleichen |
| `DEC-015` | „Why does this work?“, Multi-Lens-Erklärung, Progression DNA, Reharmonization Ladder | `PROPOSED` | DOC-002; kein MVP-Beschluss | Produktideen im Backlog führen |
| `DEC-016` | Interne Datenmodelle mit Chord-/Progression-Objekten plus Timing und Provenienz | `PROPOSED` | DOC-001; JSON/YAML-Schema noch nicht beschlossen | Spezifikations-/Testprototyp |
| `DEC-017` | Public Repo ohne ungeprüfte urheberrechtlich geschützte Rohquellen | `CONFIRMED` als Sicherungs-/Rechtsgrenze | Allgemeine Rechts-/Quellenpflicht, DOC-001 | Private/Public-Speicherentscheidung offen |
| `DEC-018` | Das aktuelle Dokument übernimmt den Handover-Prompt V1.0 in Dokumentform | `CONFIRMED` | DOC-004 | Als `draft` auf Richtigkeit prüfen |

### 10.1 ADR-Regel

Neue verbindliche Architekturentscheidungen brauchen mindestens `DEC-...`, Kontext, Optionen, Konsequenzen, Quellen/Testevidenz, `status: proposed/accepted/rejected/superseded`, Datum und Freigabeinstanz. Ein automatisierter Codex-Lauf darf `accepted` nicht allein deshalb setzen, weil ein Research Paper eine Lösung empfiehlt.

---

## 11 — Conflicts & Reconciliation

| ID | Beobachtete Abweichung / Spannung | Maßgeblicher Umgang | Status |
|---|---|---|---|
| `CON-001` | Frühere Drum-/Groove-Recherchevorschläge vs. später expliziter Ausschluss aus aktueller Recherche | **Spätere Nutzerpräzisierung gilt:** Drum-Grooves nur Roadmap | Aufgelöst, `DEFERRED` |
| `CON-002` | Research-Roadmap enthält modellhafte Gantt-Daten ab 09.11.2026 | Termine nicht als zugesagte Meilensteine interpretieren | Aufgelöst, `PROPOSED` |
| `CON-003` | Research empfiehlt Implementierungssprints, Nutzer verlangt zuerst breiten KB-Aufbau | Aktueller Auftrag: Quellenkorpus/KB tatsächlich erschließen, App-Implementierung zurückstellen | Aufgelöst, `CONFIRMED` |
| `CON-004` | Bestehender Skill-Entwurf verweist auf mehrere `references/*.md`, aber Dateien nicht vorgelegt | Links als beabsichtigte Struktur, nicht als vorhandenes Wissen behandeln | Offen, `UNVERIFIED` |
| `CON-005` | „Python + Tkinter vorhanden“ vs. fehlende Repository-Einsicht | Nutzeraussage erhalten, konkrete Implementierung erst durch Codex belegen | Offen, `UNKNOWN` |
| `CON-006` | Open Source als Produktziel vs. kommerzielle Bücher/Produktseiten im Quellenbestand | Private Rohquelle, öffentliche Paraphrase/Metadaten, Lizenz-Audit | Offen, Rechteklärung erforderlich |
| `CON-007` | Ein Bericht verwendet „Modelwheel“, „ModeWheel“ und „4× Wheels of7“ im Umfeld | Namen nicht ohne Hersteller/URL gleichsetzen; 4×7 als Lehrkonzept belegt, „Modelwheel“ als eigenständiges Produkt ungeklärt | Offen, `UNVERIFIED` |
| `CON-008` | Deterministische Regeln vs. heuristische/probabilistische/ML-Empfehlungen | Unterschiedliche Ebenen mit transparenter Evidenz; keine finale Engine-Architektur angenommen | Offen, ADR `DEC-010` |
| `CON-009` | Eine „richtige“ Analyse vs. harmonische Mehrdeutigkeit | Mehrere kontextgebundene Lesarten zulassen; Confidence/Scope dokumentieren | Fachliches Prinzip, Architektur offen |
| `CON-010` | Forschungsquelle online erreichbar vs. frei in öffentliches Repo kopierbar | Zugriff und Veröffentlichungsrecht getrennt prüfen | Offen bis Lizenzprüfung |
| `CON-011` | Research nennt `MakingMusic.pdf` als unlesbar | Aktuell bestätigt: Datei ist kein korrekt parsebares PDF; keine Inhalte daraus ableiten | Datei-Befund bestätigt, Reparatur offen |
| `CON-012` | Recherche enthält temporäre Chat-Zitatmarker in Markdown und URLs im CSV | Dauerhafte bibliografische Links und Seitenstellen vor kanonischer KB-Aufnahme nachreichen | Offen, `UNVERIFIED` |

### 11.1 Regeln für spätere Konflikte

Widersprüche nicht in „best of both“-Formulierungen verstecken. Je Konflikt eine `CON-*`-ID, genaue Quellenpositionen, Kontext, Gültigkeitsbereich, Alternative, Entscheidungsvorbehalt und Resolution-Status anlegen. Wenn zwei Schulen verschiedene Begriffe verwenden, auf Begriffs-/Scope-Ebene verbinden statt einen Ansatz zu löschen.

---

## 12 — Product & UX Inspiration

Der Produktvergleich dient der **eigenständigen Ideengenerierung**. Ein genanntes Konkurrenz-Feature wird damit weder technisch verifiziert noch Bestandteil der vorhandenen Steps-App.

| Inspirationsquelle | Tatsächlich aus bereitgestelltem Material ableitbar | Für Steps interessanter Einfluss | Status neuer Idee |
|---|---|---|---|
| **Chord Files** | Physische Navigation mit Main Chords, Secondary Dominants, Modal Interchange, Auflösungspfeilen, instrumentbezogenen Griffdiagrammen; `SRC-005` | Kontextabhängige harmonische Nachbarn, „mögliche Wege“ statt Pflichtkette | `CONFIRMED` Inspiration; konkrete digitale Nachbarschaft `PROPOSED` |
| **Chord Files „Dark Harmony“ / Varianten** | Im Showcase weitere harmonische Themen wie harmonic minor und Neapolitaner erwähnt; `SRC-002` | Erweiterbare Theoriemodule nach Komplexität statt starrer Akkordliste | `PROPOSED` |
| **ModeWheel** | Vier modale Familien, Tonika/Mode-Auswahl, Scale Steps, Root Chord, II–V–I und Keyboard/Playback; `SRC-011` | Skalensysteme, Modi und Tastaturdarstellung synchronisieren | `CONFIRMED` Inspiration; UI-Übertragung `PROPOSED` |
| **4× Wheels of7 / vier Smart Tools** | Vier Familien à sieben Skalen in `SRC-016` | Verwandte Modi/Familien als dynamische, vernetzte Modelle | `PROPOSED` |
| **The Chord Wheel (Fleser)** | Ring-/Quintenzirkel-Visualisierung und Transposition, `SRC-018` | Sofortiges tonartbezogenes Umschalten | `PROPOSED` |
| **Hookpad / Hooktheory** | In Research als Vergleich vorgeschlagen, direkter Produktstand hier nicht unabhängig neu geprüft | Stufenbasierte Progressions-/Melodie-Exploration | `PROPOSED` |
| **Scaler** | Laut Research umfangreiche Harmonie- und Vorschlagsfunktionen, bei Übergabe nicht direkt verifiziert | Fortschrittliche Referenz für Funktionsumfang; Steps differenziert sich durch Erklärbarkeit | `PROPOSED` |
| **Tonaly / Chordbot / iReal Pro** | Im Research als Vergleichsfeld erwähnt | Unterschiedliche Workflows: Circular UI, Playback, Begleitung und Progressionsarbeit | `PROPOSED`, Einzelbelege nachtragen |
| **5thsFlow / More Than Modes / Mode Wheel portal** | Zusätzliche Research-Fundstellen, Produktdetails erst verifizieren | Harmonic Map, interaktive Theorieansichten | `PROPOSED` |
| **Modelwheel** | Im Research unter diesem exakten Produktnamen nicht sicher verifiziert | Rechercheplatzhalter; nicht mit ModeWheel verwechseln | `UNVERIFIED` |

**Konkrete Ideen aus `DOC-002` zur späteren Bewertung** (nicht beschlossen): Harmonic Explorer; **„Why does this work?“** mit mehreren Erklärungslinsen; **Progression DNA** als transpositionsunabhängige Struktur; kontrollierbare Harmonic Distance/Tension/Chromaticism/Voice Movement; **Reharmonization Ladder** mit nachvollziehbaren Transformationsstufen; optionale Play-/Exportfunktionen. Alle dürfen als Kandidaten im Ideen-Backlog bleiben, ohne die erste Forschungsphase auf ein UI-MVP zu verengen.

**Rechtliche Trennlinie:** Allgemeine abstrakte Funktionen und theoretische Beziehungen können untersucht werden. Markante Produktgrafiken, Kartenlayouts, Originaltexte, Beispielaufnahmen und fremder Code dürfen nicht ohne entsprechende Berechtigung übernommen werden.

---

## 13 — Risks & Constraints

| ID | Risiko | Eintritt/Schaden (qualitativ) | Gegenmaßnahme | Status |
|---|---|---|---|---|
| `RISK-001` | Rechtlich geschützte Roh-PDFs werden öffentlich committet | hoch / hoch | Rechte-/Public-Check vor Git-Add; getrenntes Archiv | offen |
| `RISK-002` | Forschungs-URLs als überprüfte Belege behandelt | mittel / hoch | Bibliografische Einzelvalidierung; DOI/Originalabschnitt | offen |
| `RISK-003` | Nicht lesbares `MakingMusic.pdf` beeinflusst Claims | hoch / mittel | Quarantäne; Ersatzdatei, dann Audit | offen |
| `RISK-004` | Kapitel-/Textextraktion ist bei `Music_Theory_Advanced_Level.pdf` fehlerhaft | mittel / mittel | Seitenabbildung prüfen; kein blindes OCR als Primärwahrheit | offen |
| `RISK-005` | Chat-Zitatmarker gehen in dauerhafte KB | hoch / hoch | Cite-Migration zu Source-ID/Seitenstelle | offen |
| `RISK-006` | Classical-Harmony-Regeln werden auf Pop/Blues/Modal übergeneralisiert | hoch / hoch | Lens-/Scope-Felder und Gegenbeispiele | offen |
| `RISK-007` | Enharmonik/Deutsch-H/B-Verwechslungen | mittel / hoch | Spelling-Policy, Tests, explizite Locale | offen |
| `RISK-008` | Nächster Codex-Lauf baut nur Architekturpapier statt Knowledge Base | mittel / hoch | Inhaltliche Deliverables, Mindestprüfobjekte, DoD | offen |
| `RISK-009` | Unbekannter Repo-Stand führt zu destruktiven oder doppelten Ordnern | mittel / hoch | Read-only Discovery, Diffs, keine ungefragten Überschreibungen | offen |
| `RISK-010` | Proprietäre UI oder Produkt-Trade-Dress unbewusst geklont | mittel / hoch | Abstraktion und eigenes Visual Design; Rechtsprüfung | offen |
| `RISK-011` | Korpus-Bias wird als universelle Harmonieregel ausgegeben | mittel / hoch | Stil- und Corpus-Scope, Beobachtung/Norm-Trennung | offen |
| `RISK-012` | Wissensduplikate und widersprechende Concept Cards | hoch / mittel | IDs/Aliases, Conflict-Links, Dedup-Protokolle | offen |
| `RISK-013` | Skill wird zum alleinigen, schwer pflegbaren Wissensspeicher | mittel / mittel | References + KB + Retrieval, schlanke `SKILL.md` | offen |
| `RISK-014` | Vorzeitiger Ausbau von Drum-/ML-Funktionen verschiebt Kernfokus | mittel / mittel | `DEFERRED`, Scope-Gate | offen |
| `RISK-015` | Unechte Sicherheit durch Agenten-Confidence-Werte | mittel / hoch | Qualitative Confidence-Kategorien und Evidenzpflicht | offen |
| `RISK-016` | Unlizenzierte Noten-/Songbeispiele in Testdaten | mittel / hoch | Eigene Beispiele oder rechtsgeprüfte/public-domain Corpora | offen |

**Änderungs-/Freigabegrenze:** Ohne technische Projektprüfung sind nur neue, nicht-destruktive Dokumentationsdateien sichere Default-Ausgaben. Änderungen an bestehendem Produktcode, Lizenzwahl und öffentlichen Dateiveröffentlichungen brauchen einen separaten freigegebenen Arbeitsschritt.

---

## 14 — Research-to-Development Traceability

Ziel ist eine Kette **Finding → Quelle → Knowledge Object → potenzieller Use Case → Test → Status**. Die untenstehenden Knowledge-IDs sind zunächst **Vorschläge**, keine schon bestehenden Dateien.

| Finding | Quellen/Belege | Vorgeschlagenes Wissensobjekt | Anwendungsfall | Nachweis/Test | Status |
|---|---|---|---|---|---|
| Harmonik ist kontextgebunden | DOC-003; DOC-001, Multi-Lens-Kapitel | `CONCEPT-HARMONIC-CONTEXT` | Akkordanalyse | Gleiche Akkorde, andere Tonika/Lens → zulässige andere Lesart | `PROPOSED` |
| Sekundärdominanten haben Zielbeziehung, nicht zwingende Auflösung | SRC-005; DOC-001 | `RULE-APPLIED-DOMINANT` | Nächster Akkord / Erklärung | V/ii mit und ohne tatsächliche Auflösung | `PROPOSED` |
| Modal Interchange verwendet parallele tonale/modalen Quellen | SRC-005; DOC-001 | `CONCEPT-MODAL-MIXTURE` | Borrowed-Chord-Explorer | C–Fm–C und Alternativ-Lens | `PROPOSED` |
| Vier modale Familien lassen sich systematisch rotieren | SRC-011, SRC-016 | `CONCEPT-MODE-FAMILIES` | Mode Explorer | Modus/Root-Transposition in mehreren Tonarten | `PROPOSED` |
| Enharmonische Schreibungen tragen funktionale Bedeutung | SRC-010, DOC-003 | `RULE-ENHARMONIC-SPELLING` | Chord Parser / Transposition | F# major/Gb major richtig buchstabieren | `PROPOSED` |
| Melody-Harmony-Constraint darf dissonante Absicht zulassen | SRC-001 | `RULE-MELODY-CHORD-FIT` | Reharmonization Ladder | Akkordton/Tension/Passing Note Fälle | `PROPOSED` |
| Musikregeln können formalisiert werden | SRC-003 | `CONCEPT-COMPUTATIONAL-RULES` | Regelsystem | Regeln maschinenlesbar + Gegenbeispiele | `PROPOSED` |
| Pop/Rock benötigt eigene Analysemodelle | SRC-015; WEB-012 | `LENS-POPULAR-HARMONY` | Style-specific explanation | I–bVII–IV als Rock-Loop vs Klassik | `PROPOSED` |
| Voice Leading ist mehrdimensional | SRC-010; WEB-009 | `CONCEPT-VOICE-LEADING` | Voicing-Vergleich | Common tones, register, crossing | `PROPOSED` |
| Harmonische Korpora enthalten beobachtete Pattern-Häufigkeiten | WEB-003/004 | `CONCEPT-CORPUS-EVIDENCE` | Style Ranking | Corpus-Quelle und Stichprobe mitausgeben | `PROPOSED` |
| Visuale Akkordnachbarn erleichtern Exploration | SRC-005, SRC-011, DOC-002 | `FEATURE-HARMONIC-EXPLORER` | UI | Nutzertest/Protodemo statt spekulative Gewissheit | `PROPOSED` |
| Erklärbarer Skill braucht dauerhafte Provenienz | DOC-003; DOC-001 | `POLICY-SOURCE-CITATION` | Skill & Docs | Quelle inklusive Kapitel/URL verifizierbar | `PROPOSED` |

---

## 15 — Next-Step Codex Brief

> **Sofort ausführbarer Arbeitsauftrag für Codex:** Prüfe zuerst den tatsächlichen lokalen und Git-Projektbestand von Steps **read-only**. Übernimm danach die im Chat bereitgestellten Research Papers, `PROJECT_CONTEXT_HANDOVER.md`, `SKILL.md` und zugänglichen Originalquellen kontrolliert in eine von dir dokumentierte Forschungs- und Knowledge-Base-Struktur. **Erstelle echte, nachvollziehbare Inhalte** — Source-Registry-Einträge, geprüfte Concept Cards, formal überprüfbare Rules, Progression-Beispiele, Gegenbeispiele, Quellenlinks, Tests und Gap-/Decision-Register — statt nur einen neuen Architekturentwurf. Übernimm keine fremden geschützten PDFs ungeprüft in ein öffentliches Repo. Suche offene neue Quellen gezielt zur Abdeckung der Wissenslücken. Bewahre Unterschiede zwischen Nutzerentscheidungen, Research-Empfehlungen und noch offenen ADRs. Drums bleiben eine spätere Roadmap-Option. Prüfe deine Ergebnisse, liefere Diffs und dokumentiere alle nicht erledigten Teilbereiche.

### 15.1 Eingangsmaterial und Hierarchie

1. **Bindend:** explizite aktuelle Nutzerentscheidungen, dieses Handover (`DEC-001` bis `DEC-009` soweit `CONFIRMED`) und nachfolgende konkrete Freigaben.
2. **Research-Basis:** `DOC-001` und `DOC-002` inklusive Quellenlisten/Original-JSON; Ergebnisse sind Vorschläge oder dokumentierte Forschungserkenntnisse, keine automatische Entscheidung.
3. **Bestand:** die 20 Originaldateien, `SKILL.md`, HTML-/Video-Transkripte, soweit vor Ort zugänglich und rechtlich verwendbar.
4. **Repository-Realität:** per `git status`, Dateibaum, Paket-/Test-Konfiguration und Dokumentation verifizieren; sie hat Vorrang vor bloß vorgeschlagenen Report-Dateipfaden hinsichtlich dessen, **was existiert**.
5. **Externe Ergänzungen:** nur mit überprüfbarer Bibliografie, URL/DOI, Quellenstand und Lizenzstatus.

### 15.2 Phasen und konkrete Outputs

| Phase | Arbeitsinhalt | Konkrete Deliverables | Gate/Definition of Done |
|---|---|---|---|
| `C0` Read-only Discovery | Repo/Branch, Dateien, GUI-Struktur, vorhandene Skills/Docs, Rechte und Konflikte erfassen | `EXISTING_STATE_AUDIT.md`, Dateibaum-/Testübersicht, aktualisiertes Risk/Gaps | Keine modifizierten bestehenden Dateien ohne Auftrag; Unbekanntes kenntlich |
| `C1` Ingestion Scaffold | Ordnerlayout an Bestand anpassen, Source/License-Manifeste schaffen | `SOURCE_REGISTRY`, `SOURCE_LICENSES`, `INITIAL_SOURCES_V1_0` + Checksums/Status | Jeder der 20 Titel exakt einmal eindeutig referenzierbar; Defekte/Unbekannte markiert |
| `C2` Bibliografie & Rechts-Sichtung | Externe Empfehlungen und Originalquellen bibliografisch prüfen; Rohdateien trennen | `SOURCES_BIBLIOGRAPHY.md`/strukturierte Registry, Reuse-Gates | Keine Quellenfiktion; Public/Private klar |
| `C3` Theory Ontology | Taxonomie, Aliase, Lenses, Beziehungen, Voraussetzungen aufbauen | Controlled Vocabulary, Concepts-Index, erste **substanziell gefüllte** Concept Cards | Jedes Concept mit Definition, Scope, Quellen, Gegenbeispielen/offenen Fragen |
| `C4` Rules & Examples | Fundierte diatonische, modale, dominante, enharmonische, Voice-Leading- und Reharmonization-Regeln mit Beispielen | Rule Cards, Progression Library, Testfixtures | Regeltyp, Scope, Exceptions und Test nachvollziehbar |
| `C5` Research Expansion | Lückenbezogene Papers/Korpora/Wettbewerbsquellen ergänzen | dokumentierte neue SRC-/WEB-Einträge, Gap-Matrix-Vergleich | Neue Quelle nachvollziehbar überprüft, keine bloße Link-Sammlung |
| `C6` Review & Skill Interface | Qualität, Zitierbarkeit und Skill-Nutzung prüfen; erst danach kompakte Skill-Referenzen vorschlagen | QA-Report, Skill-Reference-Map, offenes ADR-Register | Kein Verweis auf nicht existierende `references/`; Tests/Evidence verknüpft |
| `C7` Handover | Ergebnis und nächste Schritte dokumentieren | `CHANGELOG`, Gap-Backlog, Diff-/Testbericht, Übergabemanifest | Nichts als „fertig“ deklariert, was nicht implementiert und geprüft wurde |

**Wichtig:** `C0` kann ohne Anwendungscode keine Bestandsfakten erzeugen; `C1–C7` sind ein Implementierungsplan für einen späteren Codex-Lauf, keine bereits erledigten Arbeitsschritte. Falls der unmittelbare Codex-Auftrag ausdrücklich nur die Datenbank betrifft, App-Engine/UI **nicht** zugleich entwickeln.

### 15.3 Minimale fachliche Musterdeliverables (nicht als Produktivdaten ausgeben)

**Source Record (schematisches Beispiel):**

```yaml
source_id: SRC-003
filename: Computational_Music_Theory.pdf
source_type: academic_paper
title: Computational Music Theory
authors: [Georg Boenn, Martin Brain, Marina De Vos, John ffitch]
year: 2012
access_status: local_attachment
read_status: partial_review
license_status: needs_verification
redistribution_allowed: unknown
topics: [computational-music-theory, rule-formalization]
claims_extracted: []
review_status: pending
```

**Concept Record (Muster, wissenschaftlich noch zu prüfen):**

```yaml
concept_id: CONCEPT-MODAL-INTERCHANGE
term: modal interchange
aliases: [modal mixture, borrowed chord]
analytical_lenses: [functional, modal, pop-rock, jazz]
definition_status: draft
scope: context-dependent
evidence:
  - source_id: SRC-005
    locator: "Transkriptabschnitt zu Modal Interchange; genauer Zeitcode nachtragen"
validation:
  test_case_ids: [TEST-MIXTURE-001]
  reviewer: null
status: unreviewed
```

**Validation Case (Muster):**

```yaml
test_id: TEST-APPLIED-DOMINANT-001
context: {key: C-major, lens: common-practice}
input: [C, A7, Dm, G7]
expected_roman: [I, V7/ii, ii, V7]
expected_claims: ["A7 tonicizes ii (Dm)"]
allowed_alternative_analyses: []
source_requirement: true
status: draft_not_executed
```

**Definition of Done pro Wissensobjekt:** `id`, Begriff/Sachverhalt, Geltungsbereich, Quellentyp, dauerhafter Beleg, Urheberrechts-/Reuse-Status, formale Beispiele und ggf. Gegenbeispiele, Abhängigkeiten/Aliase, Review-Status, Datum, Tests oder expliziter Grund, weshalb keine Ausführungstests möglich sind. Bei nicht bestätigten Sachverhalten `draft/unverified` statt `reviewed`.

### 15.4 Stop-/Review-Gates

- **Kein Eingriff in fremde oder vorhandene Dateien** ohne Ist-Zustandsvergleich und Backup-/Diff-Plan.
- **Kein Public Commit** urheberrechtlich geschützter Lehrbuchkopien/Noten/Produktgrafiken bei unklaren Rechten.
- **Keine fingierten Quellen oder scheinpräzisen Confidence-Scores.**
- **Keine Finalisierung von ADRs** über Engine/GUI/Skill-Standort, bevor Repo und Ausführungsumgebung geprüft sind.
- **Kein Drum-Research, keine Drum-Datenimporte** im aktuellen Arbeitspaket.
- **Keine Zusammenlegung der zwei Research-Berichte unter Verlust von Varianten und Konflikten**; Querverweise statt bloßer Überschreibung.

---

## 16 — Open Questions & Backlog

| ID | Frage / konkrete Aufgabe | Art | Priorität | Bezug / Abnahmekriterium |
|---|---|---|---|---|
| `TASK-001` | Steps-Repo-URL, Branch, Code-Stand, Python-/Tk-Version und Tests feststellen | Audit | P0 | GAP-012; belegter Repo-Report |
| `TASK-002` | Quelle `Master-Research-Prompt.md` lokalisieren und Version feststellen | Dokument | P0 | GAP-002; vorhanden oder eindeutig nicht vorhanden |
| `TASK-003` | Initial Sources v1.0 manifestieren, Checksums/Lizenzen/Lesestatus | Ingestion | P0 | GAP-001; 20 Records |
| `TASK-004` | Beschädigtes `MakingMusic.pdf` identifizieren und Ersatzquelle klären | Reparatur | P0 | GAP-001; funktionierendes Original oder dokumentierter Blocker |
| `TASK-005` | Zeichenkodierung/Seitenbild `Music_Theory_Advanced_Level.pdf` überprüfen | Datenqualität | P0 | GAP-001; überprüfbare Lesefassung oder Sperrstatus |
| `TASK-006` | Transkripte auf Originalvideo, Autor, Lizenz, Timecodes zurückführen | Quellenprüfung | P1 | SRC-001/002/004/005/016 |
| `TASK-007` | Research-Chatmarker durch bibliografische Dauerverweise ersetzen | Quellenprüfung | P0 | CON-012; keine toten Research-Marker in canonical Claims |
| `TASK-008` | Open Music Theory Ausgabe/Lizenz und einzelne Abschnitte aufnehmen | Literatur | P0 | WEB-001 |
| `TASK-009` | Chord-Syntax- und Notation-Standards auswählen/evaluieren | Fachmodell | P0 | GAP-004/005 |
| `TASK-010` | Controlled Theory Vocabulary einschließlich deutscher/englischer Aliase | KB | P0 | GAP-003 |
| `TASK-011` | Multi-Lens-Funktionsharmonik-/Modal-/Pop-/Jazz-Kontext als Schema | KB | P1 | GAP-006/016 |
| `TASK-012` | Positive/negative/bewusst mehrdeutige Testfälle aufbauen | QA | P0 | GAP-009 |
| `TASK-013` | Reharmonization-Melody-Constraint-Beispiele katalogisieren | Fachmodell | P1 | SRC-001, GAP-008 |
| `TASK-014` | ChoCo, When in Rome, DCML: Dataset-/Schema-/Lizenz-Audit | Daten | P1 | WEB-003/004/005 |
| `TASK-015` | Wichtige Standardwerke zur Tonal- und Voice-Leading-Theorie beschaffen | Literatur | P1 | WEB-007–012 |
| `TASK-016` | Chord Files/ModeWheel/Wheels klar vergleichbar als Funktionen statt Layout klassen | Product Research | P1 | DEC-005/006 |
| `TASK-017` | Tatsächliche `SKILL.md`-Referenzpfade prüfen und Skill-Evals definieren | Skill | P1 | DOC-003, GAP-014 |
| `TASK-018` | Open-Source-Lizenz, geschützte Quellen und Speicherstruktur entscheiden | ADR/Recht | P1 | GAP-013 |
| `TASK-019` | App-Zielgruppen, erste UX-Workflows und MVP später entscheiden | Produkt | P2 | GAP-015 |
| `TASK-020` | Rule Engine vs. probabilistische Erweiterungen als ADR evaluieren | Technik | P2 | DEC-010 |
| `TASK-021` | Konzept-Duplikate, Quellenkonflikte und Versionsmigration mit Testdaten simulieren | Governance | P1 | GAP-014 |
| `TASK-022` | Langfristige Drum-Progressions als optionale Roadmap-Erweiterung führen | Roadmap | Later | DEC-004; **kein** heutiger Research-Auftrag |

**Explizit offene Nutzerfragen, nur falls künftig benötigt:** Gibt es ein konkretes Steps-Git-Repository und welcher Branch ist maßgeblich? Welche öffentliche Softwarelizenz ist gewünscht? Darf Codex einen privaten Quellenordner anlegen? Was ist die exakte Herkunft der defekten `MakingMusic.pdf`? Welche Zielgruppe soll eine erste Version bedienen? Diese Fragen sind keine Voraussetzung für das Erstellen dieses Handover-Dokuments, jedoch für bestimmte spätere Schreib-/Veröffentlichungsschritte wichtig.

---

## 17 — Handover Manifest

| Metadatum | Wert |
|---|---|
| Handover-ID | `STEPS-PROJECT-CONTEXT-HANDOVER` |
| Version | `1.0.0` |
| Dokumentstatus | `draft`, **nicht** `reviewed` |
| Erstellungsstand | 2026-11-08 |
| Leitbild | Steps — An independent, open-source chord progression app for exploring harmony & learning music theory |
| Primärkontext | In dieser Unterhaltung sichtbare und abrufbare Nutzeranweisungen, Präzisierungen und Uploads |
| Research Reports | `DOC-001`, `DOC-002` |
| Entwurf des vorhandenen Skill | `DOC-003` |
| Erstellungsauftrag | `DOC-004`, Handover-Prompt V1.0 |
| Ursprüngliche initiale PDF-/TXT-Sammlung | 20 Dateien, `SRC-001` bis `SRC-020` |
| Zusätzliche Konkurrenz-/HTML-Anhänge | 8 Einträge `SRC-W01` bis `SRC-W08` |
| Wissenschaftliche Erwerbs-/Validierungsquellen | Auswahl `WEB-001` bis `WEB-016`, vollständige Listen in Research-URL-CSVs |
| Nicht zugängliches Dokument | `Master-Research-Prompt.md` als eigenständige Datei (`DOC-005`) |
| Nicht lesbarer Anhang | `MakingMusic.pdf` (`SRC-009`), kein gültiger PDF-Parser-Output |
| Teilweise schlecht extrahierbarer Anhang | `Music_Theory_Advanced_Level.pdf` (`SRC-012`) |
| Ungeprüft | Tatsächlicher lokaler Tk-Quellcode, Repo/Branch/CI, vorhandene Skill-Referenzen, sämtliche externen Lizenzdetails |
| Verbindliche Scope-Vorgabe | Music Theory, Chord Progressions, Harmony; breiter Quellenbestand und wachsender KB-Aufbau |
| Ausgeschlossen aus dieser Forschungsphase | Genre-spezifische Drum-Patterns/Drum-Datensätze (Roadmap only) |
| Maßgebliche Entscheidungen | `DEC-001`–`DEC-009` soweit `CONFIRMED`; sonst Status je Eintrag beachten |
| Offene Forschung/Arbeit | `GAP-001`–`GAP-016`, `TASK-001`–`TASK-022` |
| Nächster Codex-Lauf | `C0` Repo-/Material-Audit; dann `C1–C4` **reale KB-Füllung**, nicht nur Design-Papier |

### 17.1 Prüfung der Übergabeanforderungen aus dem Handover-Prompt

| Prüfpunkt | Ergebnis |
|---|---|
| Explizite Projektvision, Forschungsumfang, Priorisierung und Drum-Verschiebung | Erfasst in §§01–03, 10–11 |
| Tatsächliche Bestandsunterlagen von vorgeschlagenen Artefakten getrennt | §§04, 06 |
| 20 Initialdateien samt Zugriffs-/Lesestatus | §06.1 |
| Bestehender Skill-Entwurf und dessen relative Referenzlücken | §04.2 |
| Zwei Research-Berichte und zusätzlicher nicht gesicherter Master-Prompt | Einleitung, §§06, 17 |
| Fachliche Forschungsrichtungen und Gaps | §§05, 07 |
| Langfristige Knowledge Base, getrennte Layer und Kontrollmechanismen | §08 |
| Musiktheoretische Qualität, konkurrierende Schulen, Mehrdeutigkeit | §09 |
| Verbindliche Entscheidungen vs. Vorschläge, Konflikte, Risiken | §§10–13 |
| Research → Knowledge → Feature/Test-Verfolgbarkeit | §14 |
| Codex erhält ausführbaren Arbeitsauftrag und realen Inhaltsfokus | §15 |
| Backlog und Übergabemanifest | §§16–17 |
| Unbekannte Stellen ohne Erfindungen markiert | Ja, insbesondere Repo, Master-Prompt, `MakingMusic.pdf` |

**Restunsicherheit:** Die Herkunft und Vollständigkeit jeder historischen Chat-Nachricht außerhalb des hier verfügbaren Gesprächsausschnitts wurde nicht unabhängig geprüft. Die im Research enthaltenen wissenschaftlichen Einzelbehauptungen und Web-URLs wurden nicht nochmals vollständig fachgutachterlich verifiziert. Die Handover-Dokumentation ist deswegen bewusst `draft`.

### 17.2 Benötigte Begleitdateien bei der Übergabe an Codex

- `PROJECT_CONTEXT_HANDOVER.md` — dieses Dokument;
- `01_STEPS_Research_Foundation.md` und `02_STEPS_Knowledge_Base_Product_Blueprint.md`;
- `01_STEPS_Research_Foundation_URLs.csv` und `02_STEPS_Knowledge_Base_Product_Blueprint_URLs.csv`;
- soweit möglich beide Research-Original-JSON-Dateien;
- tatsächlicher `SKILL.md`-Entwurf und **vorhandene** `references/`/`assets/`, falls sie wirklich existieren;
- Originalquellen oder ein rechtskonformes privates Quellenarchiv plus alle Quellmanifeste;
- ggf. nachträglich `Master-Research-Prompt.md`, wenn tatsächlich vorhanden;
- geprüfter Code-/Repo-Zugang für `C0`.

### 17.3 Übergabe- und Versionspolitik

`1.0.0` bezeichnet die **Version dieses Übergabedokuments**, nicht den Entwicklungsstand der Steps-App und nicht die Version der zukünftigen Wissensdatenbank. Weiterentwicklung dieses Dokuments: `PATCH` für Korrekturen/Links, `MINOR` für neue Erkenntnisse/Register, `MAJOR` für Struktur- oder Entscheidungsumbauten. Jede Änderung erhält Datum, Grund, Quellen-/Decision-IDs und Reviewer. `status: reviewed` erst nach nachweisbarer menschlicher beziehungsweise freigegebener fachlicher Review.

---

## Anhang A — Research- und Kontextbelege (dauerhaft lesbare Referenzen)

| Handover-Beleg | Nachweisform | Wo weiter prüfen? |
|---|---|---|
| `DOC-001` | Lokaler exportierter Research-Bericht | `01_STEPS_Research_Foundation.md`, insbesondere „Executive summary“, „Initial Sources v1.0“, „Knowledge architecture“, „Technical architecture“, „Research-library governance“, „Acquisition plan“ und „SKILL.md derivation“ |
| `DOC-002` | Lokaler exportierter Research-Bericht | `02_STEPS_Knowledge_Base_Product_Blueprint.md`, insbesondere „Strategic direction“, „High-value corpora“, „Competitive landscape“, „A much larger knowledge-library design“, „Product concepts“ |
| `DOC-003` | Tatsächlich gelesener Entwurf | `SKILL.md`, Frontmatter und Workflows |
| `DOC-004` | Nutzerauftrag | `Pasted text(8).txt`, Handover-Prompt V1.0 |
| `CTX-001`–`CTX-006` | Verfügbarer Projektverlauf | Bei Codex-Übergabe diesen Handover plus gegebenenfalls Chat-Export beifügen; Kontext nicht behaupten, wenn Chat nicht exportiert wurde |
| `SRC-*` | Originaldateien | Lokale Anhänge/Quellenarchiv, zunächst Prüfen/Hashen |
| `WEB-*` | Forschungs-URLs / Bibliografie | Research Papers, `_URLs.csv`, offizielle DOI-/Projektseiten, dort nachprüfen |

**Letzter verbindlicher Arbeitsgrundsatz:** Die nächste Tätigkeit soll die ursprünglichen Quellen und Forschungsergebnisse **wirklich in eine durchsuchbare, fachlich nachvollziehbare, versionierbare und stetig ausbaufähige Knowledge Base überführen**, die Codex sowie die spätere unabhängige Steps-App nutzen können. Die Dokumentation bildet den Arbeitsrahmen, **nicht** das Endprodukt.
