# Steps – konsolidierte Projekt-Overview

**Stand der Quellenprüfung:** 9. November 2026  
**Dokumentstatus:** Konsolidierte Arbeits- und Entscheidungsgrundlage, **keine** Produktfreigabe  
**Quellenumfang:** sechs vollständig gelesene, vom Auftraggeber bereitgestellte Markdown-Dokumente  
**Methode:** systematischer Inhaltsabgleich, Auflösung von Wiederholungen, Kennzeichnung abweichender Aussagen, Erhalt einzigartiger Inhalte und Quellenrückverfolgbarkeit  
**Wichtig:** Es wurden **nur die sechs angehängten Dokumente** geprüft, nicht die darin erwähnten tatsächlichen Repositories, Archive, PDF-Originale, CSVs, JSONLs, Logs oder Websites. Diese Unterscheidung gilt in jedem Abschnitt.

## Lesehilfe und Evidenzregeln

**Quellenkürzel:**

| Kürzel | Originaldokument | Schwerpunkt |
|---|---|---|
| **A** | `STEPS Project Export.md` | Umfassende V6.6-Produktionsbibliothek, Datei-/Exportplanung, QA und Codex-Aufträge |
| **B** | `Projekt Overview.md` | V6.6-Projektbericht, Artefakte, Zahlen, Qualitätsbehauptungen, Lieferplanung |
| **C** | `Glide Kontext für Fable(2).md` | Gesprächsexport mit tatsächlichen Arbeits-/Prüfstandsmeldungen zu Glide und geplanter Steps-Abzweigung |
| **D** | `Project Definition & Positioning.md` | Markt, Positionierung, Wettbewerber, Open-Source-App, frühes MVP |
| **E** | `Forschungs- und Projektgrundlage.md` | Tiefe musiktheoretische Konzeption, 20 Quellen, Knowledge-Base-Architektur, Forschungsroadmap |
| **F** | `Projektstatus- und Projektstartbericht.md` | Ableton-Interviewarchiv, Provenienz, Projektstartkriterien, offene Definition |

Quellenstellen werden als `[A:24–70]` usw. bezeichnet; die Zahlen sind **Zeilennummern der hochgeladenen Originaldatei**. `BESTÄTIGT IM DOKUMENT` heißt: Aussage ist tatsächlich in einer Quelle vorhanden, **nicht** dass ihr Realitätsgehalt unabhängig geprüft ist. `ÜBEREINSTIMMEND` heißt: Mehrere Quellen vertreten dieselbe Behauptung. `UNGEKLÄRT` heißt: Die vorliegenden Unterlagen erlauben keine definitive Entscheidung. `VORSCHLAG` heißt: noch nicht als verbindlich nachgewiesen. `NACHWEIS FEHLT` heißt: konkrete Datei, Testreport, Freigabe oder Repository-Stand liegt nicht vor. `HISTORISCH` bezieht sich auf einen dokumentierten früheren Zwischenstand. `ABGELEITET` kennzeichnet eine hier vorgenommene Schlussfolgerung oder Berechnung. 

Diese Fassung trifft **keine stillschweigenden Entscheidungen** über Projekttyp, Lizenz, Veröffentlichung, Feature-Zeitpunkt oder Architektur. Sie empfiehlt eine handlungsfähige Struktur und belässt alle nicht belegten Entscheidungen offen. Anderslautende Angaben der sechs Ursprungsdokumente bleiben im Konfliktregister erhalten. Wiederholungen sind **inhaltlich** zusammengeführt; verschiedene Zahlenstände, Alternativen und historisch relevante Einzelbefunde werden ausdrücklich **nicht** als Duplikate gelöscht.

---

# 1. Management Summary und Projektidentität

**Am stärksten belegtes Zielbild von Steps:** eine unabhängige, lokal nutzbare, quellennachvollziehbare und perspektivisch quelloffene Anwendung für das **Erkunden, Erstellen, Analysieren, Anhören und Verstehen von Akkorden und Akkordfolgen**. Das Alleinstellungsmerkmal soll nicht die Menge der Akkorde, sondern der **erklärbare Übergang zwischen harmonischen Zuständen** sein. Steps verknüpft musikalische Exploration, theoretische Erklärungen und didaktische Vermittlung und nutzt die technische Glide-Vorarbeit als mögliche Anwendungsgrundlage. Diese Produktdefinition ist in den beiden auf Steps-Harmonik spezialisierten Dokumenten D und E explizit; sie ist deshalb die **bevorzugte Arbeitshypothese**, nicht jedoch ein formell vom Auftraggeber neu bestätigter Produktsteckbrief. [D:1–7; E:3–29; C:1–6]

Die anderen Unterlagen beschreiben zwei **andere, teils ergänzende Gegenstände**:

1. Eine breite, bereits als „STEPS“ bezeichnete **Musikproduktionsbibliothek V6.6** mit Musiktheorie, Drums, DAW, Mixing, Mastering, Distribution und weiteren Themen. Sie wird mit 1.146 Dateien und 199 beziehungsweise 262 Ableton-Blogeinträgen beschrieben, ist aber als echtes Dateisystem hier nicht prüfbar. [A:1–20; B:1–33]
2. Eine separate **Ableton-Interview-/Künstlerarchiv-Recherche** mit Kandidaten, Crawler und CSV/JSONL-Export. Dokument F stellt selbst ausdrücklich fest, dass ihre Gleichsetzung mit Steps nicht bestätigt wurde. [F:11–58]

**Empfohlene Projektabgrenzung (VORSCHLAG):**

| Ebene | Inhalt | Rolle im Steps-Projekt | Freigabe-/Bestandsstand |
|---|---|---|---|
| **P1 Produkt Steps** | Chord Progression Explorer, Theory Tutor, Harmonienavigation, Akkordfolgen und Audio | strategischer Kern | Zielbild in D/E konkret; Implementierung nicht nachgewiesen |
| **P2 Harmony Knowledge Base** | wissenschaftliche Quellen, Theorie-Taxonomie, Chord-/Progression-Modelle, Provenienz, Tests, Skill | fachliche Infrastruktur für P1 | Konzeption ausführlich; Intake/Validierung offen |
| **P3 Glide-System-Transfer** | Python/Tkinter-Anwendungstechnik, Designsystem, Tests, Packaging, Übergabeprozesse | technische Ausgangsbasis, **nicht** Harmony-Engine | zahlreiche historische Prüfungen dokumentiert, Gesamtfreigabe offen |
| **P4 Medien-/Ableton-Research** | Interviews, Produktionsartikel, Downloads, Beispiele und Metadaten | optionales ergänzendes Quellenmodul oder separates Nebenprojekt | Teilregister beschrieben; Zuordnung zu Steps offen |
| **P5 Breite STEPS-V6.6-Bibliothek** | Musikproduktion von Creative Direction bis Mastering/Distribution, Drum-/Producer-Tools, Game Audio usw. | mögliches eigenständiges Archiv und spätere Erweiterung | tatsächliche Existenz, Größe, Dateizählung und Status in den sechs Dokumenten nicht verifiziert |

Die Bezeichnungen „Steps“, „STEPS“, „Glide-System“ und „V6.6“ dürfen **nicht als austauschbare Versions-/Produktnamen** behandelt werden. Drei Namensdeutungen stehen im Material: *Steps* ohne Akronym (D/E/F); „**STructured Electronic Production System**“ (B:3); „**Structured Technical Education in Production Systems**“ (A:3). **Kein ausgeschriebenes Akronym ist freigegeben.** [A:1–5; B:1–7; D:1–7; F:36–58]

## 1.1 Strategische Leitprinzipien

- **Exploration:** Harmonien und mögliche nächste Akkorde durch Interaktion entdecken, ohne Fachtermini auswendig können zu müssen.
- **Explanation:** jede angezeigte Verbindung mit Analysemodell, stilistischem Kontext, nachvollziehbarer Begründung und gegebenenfalls mehreren Interpretationen erklären.
- **Education:** Akkordwahl, Tonarten, Stufen, Voice Leading und Notation mit Lernhilfen vermitteln; nicht nur Progressionen „generieren“.
- **Transposition statt starre Charts:** absolute und relative Darstellungen verlustfrei verwalten.
- **Quellenevidenz statt Prompt-Wissen:** `SKILL.md` als Zugang/Workflow, nicht als primärer Wissensspeicher.
- **Mehrere Modelle statt Dogmatik:** klassisch-funktionale, modale, jazz- und poporientierte sowie transformationale Perspektiven nebeneinander zulassen.
- **Offline/local-first, Datenschutz:** kein Konto oder Tracking als angestrebtes Designprinzip; reale Telemetrie-/Datenschutzprüfung noch nicht durchgeführt.
- **Reproduzierbarkeit:** Source Registry, klare Versionsstände, überprüfbare Fixtures/Tests, Lizenzregister, Sicherungen und Prüfsummen.
- **Preservation-first:** historische Nachweise, Originalquellen, Grafikvorlagen und lokale Zusatzmaterialien nie ohne inventarisierte und geprüfte Sicherung löschen.

## 1.2 Ziele, Nutzergruppen, Abgrenzung

**Zielgruppen:** Musikschüler und Anfänger, Hobby-Pianisten und -Gitarristen, Heimproduzenten, Songwriter, Musikpädagogen, Theorieinteressierte, Open-Source-Entwickler und datenschutzorientierte Offline-Nutzer. Konkrete Personas: Schüler, der harmonische Funktionen verstehen möchte; Gitarrist, der neue Progressionen übt; Lehrkraft, die Zusammenhänge interaktiv demonstriert; Produzent, der Reharmonisierungsmöglichkeiten testet. [D:38–50]

**Kernprobleme:** statische Akkorddiagramme zeigen Beziehungen nur eingeschränkt; viele Systeme sind kostenpflichtig oder plattformspezifisch; gängige Generatoren erklären stilistische Mehrdeutigkeit kaum; Musiktheoriequellen sind uneinheitlich und schlecht maschinell nachvollziehbar. [D:9–36; E:17–27; E:253–285]

**Aktueller bewusster Ausschluss:** Drum-/Genre-Pattern-Forschung und Drum-Engine **nicht** im unmittelbaren Harmony-Forschungs-MVP, ausdrücklich `DEFERRED`. **Keine rückwirkende Löschung** aus dem breiten Produktionsarchiv: Dessen Drum-Inhalte können als historische/adjazente Bestände bestehen bleiben. Weitere nachgelagerte Themen: umfangreiche Style-Erweiterung, vollwertige DAW, Audioerkennung, Spatial Audio, breite Produktionslehre, Mobile-App und öffentliches Content-Hosting. [E:29; E:45–58; E:607–611; A:30–68]

---

# 2. Funktionsmodell, Features und fachlicher Scope

## 2.1 Primäre Nutzungsfälle

| ID | Nutzung | Detaillierter Umfang | Status |
|---|---|---|---|
| U-01 | Akkordfolgen anlegen | Akkorde in Reihenfolge hinzufügen, entfernen, ersetzen; Tonart und Modus zuweisen; `C → Dm → G7 → C` eingeben | als MVP vorgeschlagen |
| U-02 | Explorieren | Akkord anklicken; diatonische Nachbarn, Dominant- und Borrowing-Beziehungen, funktionale Auflösungen anzeigen | Zielbild; keine Umsetzung nachgewiesen |
| U-03 | Akkorde analysieren | Root, Chord Quality, Extension/Alterations, Inversion, Bass, Roman Numeral, Funktion im Kontext | geplant |
| U-04 | Akkordfolgen analysieren | absolute Akkorde / relative Stufen, Kadenzen, Rhythmik, Phrasen, Stil, Alternativanalysen | geplant |
| U-05 | Transponieren | Folge um Halbton-/Tonintervalle und in andere Tonarten transponieren, Akkordschreibweise erhalten | geplant |
| U-06 | Vorschläge verstehen | nächste Akkorde und Substitutionen mit Begründung, Kontext, Zuverlässigkeit und Gegenbeispielen | Zielbild |
| U-07 | Hören und üben | Progression per MIDI/Instrument anhören, Loop-/Übungsmodus, ggf. Klavier-/Gitarren-Darstellung | ab Audio-Meilenstein geplant |
| U-08 | Speichern, laden, teilen | eigenes lokales Projektformat, JSON; später MIDI und MusicXML Import/Export, Beispielbibliothek | geplant |
| U-09 | Lernen | Theoriehinweise, Tonleiter-/Tonartbezug, Begriffsdefinitionen, Quellen und Übungen | geplant |
| U-10 | Expertise zuschalten | Fach-Skill/Codex-Abfragen über identische Knowledge-Base-Definitionen statt abweichende Prompt-Regeln | Skill-Prototyp geplant |
| U-11 | Kooperieren | GitHub-Issues/PRs, Community-Beispiele, transparente Lizenz-/Beitragsrichtlinien | strategisch vorgeschlagen |

Der frühe, UI-orientierte MVP-Entwurf in D enthält ausdrücklich **Erstellen/Bearbeiten, Wiedergabe, Darstellung, Save/Load und Theory Hints**. Die spätere, fachorientierte Forschungsgrundlage E priorisiert dagegen **sechs validierte Daten-/Engine-Artefakte vor weiterem UI-Ausbau**. Beide Anforderungen bleiben erhalten, sind aber eine **Reihenfolgeentscheidung**, keine gleichzeitige zugesicherte v0.1-Funktion. [D:76–108; E:661–670]

## 2.2 Harmony Explorer: Relation Layers

Eine Akkordinstanz erhält nicht nur ein Symbol, sondern eine Position in einem **mehrdimensionalen, erklärbaren Harmoniegraphen**. Vorgeschlagene Ebenen für beispielsweise `Am`:

| Ebene | Relationslogik | Quellenbeispiel |
|---|---|---|
| Diatonisch | Akkorde derselben Tonart/Skala | `Dm`, `Em`, `F`, `G`, `C` (kontextabhängig) |
| Dominantisch | Auflösung über Dominante/Zwischendominante | `E7 → Am`; sekundär, **wenn** `Am` als vi in C-Dur kontextualisiert ist; primäre Dominante in a-Moll |
| Modal Interchange | Entlehnungen aus Parallelmodi | `Fm`, `Ab`, `Bb` in C-Dur-Varianten; alterativer Kontext zu prüfen |
| Voice Leading | gemeinsame Töne, kleine Stimmbewegungen, Guide Tones | `C`, `Fmaj7`, `Am/C` (abhängig vom Voicing) |
| Transformational | relative/parallel/leading-tone exchange, Tonnetz, neo-Riemannian | Relationsoperatoren statt nur Funktionsanalyse |
| Reharmonization | Ersatz mit Melody-Chord-Kompatibilität, Spannung, Kadenzeffekt | Harmonievarianten zu einer Melodie |
| Teaching Layer | Erklärung, Alternative, Grenzen, Referenzen und Testfälle | nach Stil/Analysemodell gewichtet |

**Wichtiger Befund:** Der Beispieltext „`E7 → Am` als Secondary Dominant“ ist **ohne Tonart nicht allgemein korrekt**. In a-Moll steht E7 typischerweise als V7; in C-Dur kann E7 als V7/vi beschrieben werden. Das ist ein echter **Semantikkonflikt zwischen verkürzter Erklärung und kanonischem Kontextmodell**, nicht bloß Terminologie. [E:35–43; E:263–285; E:458–484; E:672–698]

## 2.3 Wissenschaftlich fundierte Wissensbereiche

**Fundamental Music Theory:** Pitch / pitch classes, Note Spelling, Enharmonik, Intervalle, Oktaväquivalenz, Stimmung/Temperierung und mathematische Intervallverhältnisse, Skalen/Modi, Vorzeichen, Tonzentren/Tonarten, Rhythmus, Metrum, Grundformen. **Unbedingt** akustische Pitch Class und theorieabhängige Schreibweise trennen (`F#` vs. `Gb`; deutsches `H` vs. `B`). [E:93–99]

**Chord Theory:** Dreiklänge, Septakkorde, Sixths, 9/11/13-Extensions, Added Notes, Sus-Akkorde, Alterations, Omissions, Umkehrungen, Slash Chords, Polychords, rootless Voicings, enharmonische Umdeutungen. Datenmodell trennt **Chord Identity / Chord Spelling / Chord Voicing / Chord Symbol / Harmonic Interpretation**. Beispielsweise `C–E–G–Bb` kann `C7` sein, während `V7/IV` einen Tonartkontext erfordert; konkrete Voicings speichern Oktaven, Doublings und Basslage. [E:101–119]

**Harmony-Familien (einzelne Taxonomieeinträge):** diatonische Harmonik; Funktionsharmonik; Roman-Numeral-Analyse; Kadenzsyntax; Tonikalisierung; Zwischendominanten; secondary leading-tone/diminished chords; Modal Interchange/borrowed chords; chromatische Mediante; Neapolitaner; übermäßige Sextakkordfamilien; Modulation; common-tone harmony; Orgelpunkt/pedal harmony; Sequenzmodelle; Blues-Harmonik; modale Harmonik; Jazz-Funktionsharmonik; Chord-Scale-Theorie; nonfunctional harmony; Planing; Transformations-/neo-Riemannian-Beziehungen. [E:121–149]

**Progression Theory:** Absolute Akkorde, relative Stufen, Tonikakontext, Modus, harmonic rhythm, phrase position, cadential role, Voice-Leading-Metriken, Quellenherkunft, Stil-/Kontexttags, mehrere Analysen und Konfidenz. Beispiel `C–G–Am–F` ist konkret, `I–V–vi–IV` transponierbar. Reharmonisierung berücksichtigt Melodietöne, Skalenidentität, Tension/Release und Kadenzen. [E:150–184; E:253–285]

**Voice Leading/Transformations:** Parsimonious movement, common-tone retention, guide-tone movement, minimale Bewegungen, Tonnetzräume; relations wie `functional_neighbors`, `diatonic_neighbors`, `modal_interchange_neighbors`, `secondary_dominant_targets`, `common_tone_neighbors`, `minimal_voice_leading_neighbors`, `transformational_neighbors`. [E:185–206]

**Stile als Theorie-Kontexte:** Klassisch tonal, romantisch chromatisch, Jazz, Blues, Gospel, Pop, Rock, Soul/R&B, Neo-Soul, Filmmusik/Cinematic, Modal/Folk. Nicht jeder Stil ist für MVP zu implementieren. `bVII → I` kann in verschiedenen Genres unterschiedlich normal und theoretisch deutbar sein. [E:208–218]

**Computational Music Theory:** strikt unterscheiden zwischen (a) **explizit formulierten Regeln**, (b) **empirischen/statistischen Häufigkeiten** und (c) **kreativen Empfehlungen**. Das UI darf kreative Optionen nicht als universelle harmonische Gesetze verkaufen. Material zu Renaissance-Counterpoint demonstriert nur einen **stilbezogenen** Regelansatz, kein universelles Harmoniewissen. [E:220–232]

## 2.4 Qualität der Analyse: Mehrdeutigkeit und Provenienz

Jede Analyse sollte folgende Fragen beantworten können: **Was? Nach wem? Quelle/Edition? In welchem Theorierahmen? Welche Stilgeltung? Wie sicher? Durch wen validiert? Von welchem Code und Test verwendet?** Einträge dürfen Alternativanalysen und widersprechende, aber kontextuell plausible Deutungen behalten. Niedrige Evidenz (YouTube-Transcript), empirische Häufigkeit und Peer-Review-Forschung sind zu unterscheiden. [E:486–525; E:543–554; E:613–619]

**Proponierte Relations-Typen:** `DOMINANT_OF`, `RESOLVES_TO`, `BORROWED_FROM`, `DIATONIC_WITH`, `COMMON_TONE_WITH`, `VOICE_LEADING_NEAR`, `TRANSFORMATION_OF`, `SUBSTITUTES_FOR`. Eine echte Graphdatenbank ist für den MVP nicht nötig; YAML/JSON mit typisierten Relationen reicht zunächst. [E:578–598]

---

# 3. Forschungsbestand: die 20 namentlich erfassten Ausgangsquellen

Die folgenden **20 Einträge** sind aus E vollständig und inhaltlich **einmalig** übernommen. „Parsed“ bezieht sich auf berichtete frühere Textextraktion, **nicht** auf eine heutige unabhängige Kontrolle oder vollständige kapitelweise Ingestion. Die eigentlichen PDFs/TXTs liegen dieser Prüfaufgabe nicht bei. Urheber, Fassungen und Rechte bleiben wie in den Ursprungsquellen teilweise ungeklärt. [E:60–87]

| Nr. | Quelldatei | Urheber, Jahr, Art | Thema und dokumentierter Erkenntniswert | Status / Rechte |
|---:|---|---|---|---|
| 1 | `ModeWheel_Manual_1.21.pdf` | ModeWheel/NewPsyc; Autor offen; 2023; Handbuch | vier Scale Families, Tonic/Mode Selection, Scale Steps, Root Chord, II–V–I, Playback | 9 Seiten reported parsed; Version 1.2.1 (Mai 2023); Rechte offen |
| 2 | `Music_Theory_Advanced_Level.pdf` | vermutlich Eowyn/Mysongbook-Kompilation; Jahr unbekannt | fortgeschrittene Harmonik und Progressionen | partial/metadata only; Original-Match und Rechte offen |
| 3 | `Music_theory_handbook.pdf` | Berklee Online; u. a. Beth Denisch, Steve Rochinski, Paul Schmeling, Michael Rendish | Counterpoint, Reharmonization, Rhythm, Seventh Chords, Blues | Inhaltsverzeichnis parsed; wahrscheinlich proprietär |
| 4 | `Name_Music_Theory_Worksheet_Music_Theory.pdf` | Serenade Music Publishing, 2015 | Notation, Schlüssel, Grundtheorie-Aufgaben | parsed; Copyright-Hinweis, Rechteprüfung nötig |
| 5 | `Popular_Music_Analysis_in_American_Music.pdf` | Jocelyn Neal, 2005, Fachartikel, DOI `10.31751/524` | Methodik und Entwicklung US-amerikanischer Popular-Music-Analyse | parsed/high value; **CC BY 4.0 behauptet** |
| 6 | `Scales with 4 smart tools.txt` | Oliver Prehn/NewJazz-Konzept, Transkript; Jahr unbekannt | vier Wheels à sieben Modi = 28-Scale-Navigation | parsed; Herkunft/Lizenz offen |
| 7 | `THE_ELEMENTS_OF_MUSIC.pdf` | Autor/Ausgabe unbekannt | Rhythm, Dynamik, Melodie, Harmonie, Timbre, Textur, Form | parsed; bibliografische Identität offen |
| 8 | `the-chord-wheel.pdf` | Jim Fleser/Hal Leonard; Ausgabe offen | Tonartbeziehungen, Transposition, Improvisation, Komposition | Auszug parsed; proprietär |
| 9 | `Understanding_Basic_Music_Theory.pdf` | Catherine Schmidt-Jones, teils Russell Jones, 2007 | Notation, Intervalle, Skalen, Tonarten, Akkorde, Harmonie | parsed mit Encoding-Schäden; Originalfassung CC BY behauptet, exakte Version offen |
| 10 | `What_is_popular_music_And_what_isn_t_An.pdf` | Franco Fabbri, 2010, *Musiikki* 2/2010 | Genre-/Popular-Music-Definition und Abgrenzung | parsed; Lizenz zu prüfen |
| 11 | `7 levels of reharmonising Eleanor Rigby.txt` | Autor/Videoquelle offen | Dorian/Harmonic Minor, Reharmonisierung, Melodie-Akkord-Kompatibilität, Cadence/Tension, Skalenwechsel | parsed; Originalnachweis/Rechte offen |
| 12 | `Chord FIles 2026 Showcase.txt` | Chord Files/Jaka, 2026-Kontext | Progressions, Dark Harmony, Scales/Blues, Secondary Dominants, Modal Interchange, Harmonic Minor, Neapolitan, Secondary Diminished | parsed, proprietäre Produktreferenz |
| 13 | `Computational_Music_Theory.pdf` | Georg Boenn, Martin Brain, Marina De Vos, John ffitch; 2012; DOI `10.1609/aiide.v8i4.12559` | Answer Set Programming, formalisierte Theorie/Komposition, stilgebundene Regeln | parsed/high value; AAAI-Rechte offen |
| 14 | `harmony as a student.txt` | Nari Sol laut Transkript; Jahr unbekannt | intuitives Lernen, Scale/Chord, Tension und Kontext | parsed; didaktisch, keine normative Theorie; Lizenz offen |
| 15 | `How to use chord files.txt` | Chord Files/Jaka; Jahr unbekannt | Main Chords, Secondary Dominants, Modal Interchange, Diagramme | parsed; proprietär |
| 16 | `Is_Generative_Theory_Misleading_for_Music.pdf` | Rafael Barbosa, 2019, HAL-ID `hal-02184441` | Kritik generativer Theorie, GTTM, Schenker, Kognition | parsed; Open Access, konkrete Nachnutzung offen |
| 17 | `Kants_Theory_of_Music.pdf` | Oliver Thorndike, 2021, DOI `10.5281/zenodo.5776100` | Kant, absolute Musik, Affekt, ästhetische Ideen | parsed; Journal-/Zenodo-Rechte offen |
| 18 | `L-0002916879.pdf` | Theodor W. Adorno, engl. Hrsg. Robert Hullot-Kentor; Ausgabe 2009 | *Current of Music: Elements of a Radio Theory*, eher periphere Philosophie | partial parsed; all rights reserved |
| 19 | `MakingMusic.pdf` | Dennis DeSantis/Ableton, 2015 | *Making Music: 74 Creative Strategies for Electronic Music Producers* | Attachment laut E nicht zuverlässig parsed; bibliografisch beschrieben, proprietär |
| 20 | `Mathematics_and_Music.pdf` | David Wright, 2009, AMS | Verhältnisse, Logarithmen, Intervalle, chromatische Skalen, Stimmung | parsed; AMS-Rechtevorbehalt |

**Abhängigkeiten:** Ohne Originaldateien können wir weder alle bibliografischen Angaben noch tatsächliche Byte-Hashes, einzelne Seitenbezüge, lokale Speicherorte, Metadaten oder Lizenztexte bestätigen. Die historischen Referenzmarker im Research-Bericht (`filecite...`, `cite...`) sind **keine in diesem sechsteiligen Export selbst auflösbaren Quellbelege**. Sie müssen beim späteren Ingest durch überprüfbare URLs/DOIs/Dateipfade samt Fundstellen ersetzt werden. [E:9–23; E:60–87; E:525]

## 3.1 Priorisierte wissenschaftliche Erweiterung

**Forschungslücken:** Parsimonious Voice Leading, Common Tones, Guide Tones, jazz harmonic syntax inklusive Tritonus-Substitution, Backdoor Dominants, Altered Dominants, Diminished Substitution und Modal Jazz; moderne Pop-/Rock-Harmonik; chromatische Harmonik; Tonnetz/Transformations-/neo-Riemannian-Theorie; Chord-Symbol-Syntax; Chord-Scale-Theorie; corpusbasierte Progressionen; maschinenlesbare symbolische Austauschformate. Mehr generische Anfängerlehrbücher sind im Verhältnis dazu gering priorisiert. [E:87; E:529–541; E:892–900]

**Referenzsysteme zur Evaluation, nicht als bereits integrierte Komponenten:**

- **ChoCo – the Chord Corpus:** laut Quelle mehr als 20.000 zeitbezogene Akkordanmerkungen; Normalisierung unterschiedlicher Notationen, Provenienz, JAMS-Ausgabe und Knowledge Graph als Architekturvorbild.
- **McGill Billboard Corpus:** Titel, Interpret, Metrum, Tonika, Tonartwechsel, Phrasen und Akkordanmerkungen zur Popularmusik-Empirie.
- **MusicXML:** strukturiertes `<harmony>`-Element für Chord Symbols, Funktionsinformationen und veränderte/ergänzte Stufen.
- **Harte chord notation / JAMS:** normalisierte Akkordsymbole und zeitbezogene Annotationsformate.
- **`music21`:** Roman Numeral, Chord/Chord Symbol und Harmonic Analysis als Testoracle/Adapter, nicht zwingend als Engine-Kern.
- **Weitere Referenzen:** Open Music Theory, Boenn et al., primäre Standardstellen für MIDI, EBU, ITU, DDEX.

[E:11–23; E:181–183; E:362–363; E:539–541; E:894–900]

---
# 4. Ableton-, Kurs- und Produktionsquellen: getrennte Bestände

## 4.1 Ableton-Zahlen: nicht dieselbe Grundgesamtheit

**Die im Material vorkommenden Bestände sind erst nach einem Datensatzabgleich zusammenzählbar.** Alle Zahlen im Folgenden sind **berichtete Zwischenstände**, keine neu verifizierten Live-Abrufe. [A:3–20; B:13–33; B:147–158; F:21–32; F:96–126]

| Bestand / Behauptung | Genannte Zahl | Richtige Interpretation / Grenze |
|---|---:|---|
| Erstes **Künstler-/Interview-Starterarchiv** | 28 Kandidaten | frühe Auswahl; keine 28 validierten Interviews |
| Erweitertes **Interview-/Artist-Quellenregister** | 143 eindeutige Links | laut F Summe früherer + zusätzlicher Kandidaten; Datensätze nicht mitgegeben |
| Besuchter **englischer Künstler-Archivbereich** | 34 Seiten | Seitenzahl des Suchlaufs, nicht Gesamtabdeckung des Blogs |
| Identifizierte Artikel im untersuchten Künstlerarchiv | 609 unterschiedliche Beiträge | Grundgesamtheit eines Archivbereichs; nicht zwangsläufig relevant für Akkord-App |
| Interviews/Künstlerprofile unter diesen Beiträgen | ca. 123 Kandidaten | Klassifikation noch nicht verifiziert; 143 Links können weitere frühere Quellen enthalten |
| Frühe V6.6-Blog-Auswertung | 199 katalogisierte URLs | B nennt 199 und 169 heruntergeladene/„verifizierte“ Artikelseiten |
| Davon Seiten geprüft/abgerufen laut B | 169 | Art der Prüfung und Beleg fehlen; verbleiben 30 von 199 ohne gleichartigen Status |
| Genannte Zielmenge in B | 462 unique posts | 199/462 ≈ **43,07 %**; unbekannte Abgrenzung der 462 |
| Spätere V6.6-Auswertung laut A/B-Anhang | 262 katalogisierte Artikel | A meldet 63 „added in V6.6“; 199+63=262, möglicher Versionsfortschritt, aber Kataloge fehlen |
| Gesamter Ableton-Blog | **unbekannt** | keine der Zahlen erlaubt eine vollständige Abdeckungsquote |

Es wäre methodisch falsch, **143**, **199**, **262**, **462**, **609** und **123** als gleiche Art von Objekt oder als eindeutigen Widerspruch zu interpretieren. Sicher widersprüchlich ist hingegen, dass **B innerhalb desselben Berichts** sowohl 199 als aktuellen Katalogstand und später 262 als „finalen“ Stand nennt, **ohne nachvollziehbare Snapshot-Identifikation**. Möglicher Erklärungsansatz: 199 vor Ergänzung, +63 neu. **Erst CSVs, Zeitstempel, Kanonisierung und Datei-Hashes** können dies belegen. [B:13–14; B:31; B:149–156; A:3–5]

**Zu übernehmende Normalisierung:** `canonical_url`, `source_language`, `translation_group_id`, `article_type` (`interview`, `profile`, `tutorial`, `download`, `video`, `podcast`, `other`), `crawl_batch_id`, `first_seen`, `last_checked`, `source_status`, `license_status`, `download_asset_ids`, `source_hash`, `dataset_membership` und Status der manuell geprüften Klassifizierung. Fremdsprachige Artikel können dieselbe redaktionelle Arbeit in anderer Sprachfassung sein. [F:114–126; F:179–204; A:96–103]

## 4.2 Namentlich genannte Ableton-Beispiele

**Künstler-/Interview-Recherche, als Quellen-URLs gemeldet:** [F:128–134]

- [Flying Lotus – From the Sketchbook to the Stage](https://www.ableton.com/en/blog/flying-lotus-from-the-sketchbook-to-the-stage/)
- [Joris Voorn – Tools that Serve the Idea](https://www.ableton.com/en/blog/joris-voorn-tools-that-serve-the-idea/)
- [Flava D – The Evolution of a Producer](https://www.ableton.com/en/blog/flava-d-evolution-of-a-producer-interview/)
- [Sudan Archives – Vintage Strings, Modern Gadgets](https://www.ableton.com/en/blog/sudan-archives-vintage-strings-modern-gadgets/)
- [Robert Henke – Lumière and Lasers](https://www.ableton.com/en/blog/robert-henke-lumiere-lasers-interview/)

**Einschränkungsbeispiele für Downloads, nicht pauschale rechtliche Einstufung aller Assets:** [F:138–175]

- [Machinedrum – Planting Seeds](https://www.ableton.com/en/blog/machinedrum-planting-seeds/)
- [April + VISTA – Making Traditional Noise](https://www.ableton.com/en/blog/april-vista-making-traditional-noise/)
- [Artefakt – Undertow / Live Set](https://www.ableton.com/en/blog/download-the-live-set-of-artefakts-new-track/)
- [DJ Gigola – Unfolding Practice II / Live Set](https://www.ableton.com/en/blog/download-the-live-set-of-dj-gigolas-new-track-unfolding-practice-ii/)
- [ANTI-MASS – From Uganda into the Unknown](https://www.ableton.com/en/blog/anti-mass-from-uganda-into-the-unknown/)

Einige dieser Inhalte sollen laut F nur für Bildungs-/Studienzwecke und nicht kommerzielle Nutzung bereitgestellt worden sein. **Je Asset separat prüfen**; ein allgemeiner Link zur Ableton-EULA belegt nicht die Lizenz eines konkreten Downloadpakets. **Nicht** öffentlich verfügbare oder proprietäre Blogvolltexte, Originalbilder, Live Sets, Audio-Packs und private PDF-/MIDI-Kursdateien ungeprüft in die App oder ein öffentliches ZIP kopieren. [F:138–175; A:18–20; B:94–102]

## 4.3 Ergänzende Lernmaterialien und Musikproduktionsstandards

- **PausePlayRepeat:** vom Nutzer stammende Textlektionen zu Drum Programming plus EQ-Guide; zugehörige MIDI-Beispiele/ZIPs werden zwar erwähnt, aber weder als Dateien noch mit Importnachweis mitgeliefert. Schlagzeugbeispiele umfassen potenziell Swing, Velocity, Step-Zahlen, Tempo und Taktstruktur; dies ist eine **spätere Produktionsbibliothek-/Drum-Layer-Aufgabe**, nicht Teil des aktuellen Harmony-MVP. [A:11–20; A:94–103; B:29]
- **DeSantis, *Making Music*:** 74 Creative Strategies; verschiedene Berichte behaupten, Kapitelübersichten/Metadaten, Übungen und `04_COMPOSING/`-Inhalte seien erfasst. E beschreibt das lokale PDF dagegen als nicht zuverlässig parsed. Deshalb unterscheiden: **Bibliografie berichtet**, **verifizierter Volltextimport offen**, **eigene Übungen unüberprüft**, **Original-PDF nicht öffentlich bündeln**. [A:15–20; B:15; E:84]
- **MIDI 2.0 / MIDI Association:** moderne Interoperabilität; historische MIDI-1.0-Kompatibilität thematisiert.
- **EBU R128 / ITU-R BS.1770:** Lautheitsmessung/Normalisierung; in A wird **–23 LUFS** für einen R128-Kontext erwähnt. **Kein universeller Zielwert für jedes Musikmaster!** Der konkrete Anwendungsfall/Standard ist zu unterscheiden.
- **DDEX:** standardisierte Musik-/Distributions-Metadaten.
- **Dolby / immersive audio:** späterer Produktionsbereich, nicht die Harmony-MVP-Baseline.
- **Ableton Blog „One Thing“**, Interviews, Podcasts, Videos und Downloads: zusätzliche Quellen, teils unvollständig erfasst.

[A:3–20; A:96–103; A:283–296; B:1–33]

## 4.4 Gesonderter Status der Ableton-Interviewdatenbank

Nach F ist die Kette **Quellensuche → Abruf → Metadatenextraktion → Normalisierung → Dublettenprüfung → Datenbankimport → Suche** vorbereitet. Gemeldet sind: CSV, JSONL und Markdown-Index, Python-Crawler-Grundgerüst, README und Datenschema, erste Lizenzrecherche sowie Deep-Research-Auswertung. **Nicht nachgewiesen:** vollständiger Crawl beider Sprachen, alle 143 URL-Prüfungen, automatische Interviewklassifikation, de/en-Abgleich, eine betriebsbereite Datenbank, semantische Suche, echte Nutzerfrage-Abnahmen, laufende Aktualisierung. Ein früheres Downloadproblem über ChatGPT wird erwähnt. [F:96–126; F:179–225]

**Empfehlung:** dieses Register als **`research/ableton/` mit eigener Version, Datenherkunft, Rechten und Abnahmekriterien** pflegen oder als separates Projekt erhalten, bis die Zuordnung zum Harmony-Produkt freigegeben ist. JSONL ist als portables Austauschformat erwähnt; relationale Datenbank und Vektorsuche sind **Optionen**, keine beschlossene Architektur. [F:179–206; F:339–349]

---

# 5. Berichteter Umfang der umfassenden STEPS-Produktionsbibliothek V6.6

## 5.1 Vollständiges aus A extrahiertes Ordnerinventar

Das folgende Verzeichnisinventar umfasst **37 angegebene Top-Level-Positionen**. Die Zahlen sind geschätzte/berichtete Einzelwerte, nicht gemessene Dateizahlen. In A stehen gleichzeitig **1.146 Dateien** und **„≈1.166“**. Die hier selbst errechnete Summe der Tabellenwerte ist aber **1.306**. Differenz: **+160** zu 1.146 beziehungsweise **+140** zu ≈1.166. Das ist ein **rechnerischer Widerspruch** innerhalb von A. Die Mermaid-Tortengrafik von A zählt wiederum nur **686** Einheiten und kann keine Gesamtdateiverteilung darstellen. [A:24–86]

| Verzeichnis laut A | Gemeldete Dateien | Unterordner | Erhaltener Inhaltsfokus |
|---|---:|---:|---|
| `00_NAVIGATION` | 20 | — | Navigation, Indizes, Metadaten |
| `01_MUSIC_THEORY` | 40 | 2 | Intervalle, Stimmung, Modi, Übungen |
| `02_HARMONY` | 50 | 3 | Funktions-/modale Harmonik |
| `03_CHORD_PROGRESSIONS` | 50 | 4 | Progression Atlases, Reharmonization |
| `04_COMPOSING` | 111 | 5 | Formen, Motive, Top Lines, MIDI Labs |
| `05_DRUMS_RHYTHM_GROOVE` | 90 | 4 | Drum Patterns, Swing, Fills |
| `06_PRODUCER_TOOLS` | 80 | 6 | EQ, Kompression, Synths, Sidechain |
| `16_CREATIVE_DIRECTION` | 40 | 2 | Planung, kreative Identität |
| `17_DAW_AUTOMATION` | 40 | 3 | DAW-Features und Automationsstrategie |
| `18_AUDIO_TECHNIQUE` | 40 | 3 | Signalfluss, Pegel und Messung |
| `19_RECORDING_ACOUSTICS` | 40 | 2 | Mikrofonierung, Raumakustik |
| `20_VOCAL_PRODUCTION` | 20 | 1 | Vocal Recording/Processing |
| `21_EDITING_RESTORATION` | 20 | 1 | Audio-Cleanup, Sampleschnitt |
| `22_SYNTHESIS_SAMPLING` | 60 | 4 | Synthese, Sampler, 808s |
| `23_BEATMAKING_808` | 50 | 3 | Groove und 808-Design |
| `24_ARRANGEMENT_TRANSITION` | 40 | 3 | Songform, Übergänge, Skizzen |
| `25_AUDIO_EFFECTS` | 40 | 2 | Reverb, Delay, Modulation |
| `26_MIXING` | 60 | 5 | Mixing, Gain Staging |
| `27_MASTERING` | 40 | 2 | Lautheit, Mastering-Finishing |
| `28_SPATIAL_AUDIO` | 15 | 1 | Immersive/Spatial Audio |
| `29_LIVE_PERFORMANCE` | 15 | 1 | Live-/DJ-Setups |
| `30_COLLABORATION` | 10 | 1 | Zusammenarbeit |
| `31_RIGHTS_DISTRIBUTION` | 20 | 2 | Lizenzen und Distribution |
| `32_AI_MUSIC` | 20 | 1 | KI-/Generative Methoden |
| `33_GAME_AUDIO` | 10 | 1 | Adaptive/game audio |
| `34_REFERENCE_ANALYSIS` | 40 | 3 | Referenztracks, Stems |
| `35_GENRE_STYLES` | 30 | 3 | Genreprofile, kultureller Kontext |
| `36_HARDWARE_PLUGINS` | 20 | 2 | Hardware, Plugins |
| `37_VIDEO_PODCAST` | 10 | 1 | Video/Podcasts |
| `38_ACCESSIBILITY` | 20 | 1 | Gehörschutz, Barrierefreiheit |
| `39_FORMATS_INTEROP` | 20 | 1 | MIDI, DAW-, Audioformate |
| `40_EXERCISES_TRAINING` | 20 | 2 | Übungen und Lernprojekte |
| `41_INSTRUMENT_PERF` | 20 | 1 | Instrumentalspiel im DAW-Kontext |
| `42_SONIC_BRANDING` | 20 | 1 | Klangmarken/Identität |
| `43_ARCHIVING` | 20 | 1 | Archivierungsstrategie |
| `90_ARCHIVE` | 60 | 2 | historische Stände/Backups |
| `99_TEMP/QA` | 5 | 1 | temporäre QA-Dateien |
| **Summe aller aufgeführten Zeilen** | **1.306** | — | **selbst berechnet, nicht verifiziert** |

**Klassifikationslücke:** `07–15` fehlen in A als Ordnerzeilen; B nennt aber u. a. `10_QUELLEN_LIZENZEN/` und `12_CODEX_AUFTRAEGE/`. Das kann ein unvollständiger Auszug oder eine uneinheitliche Verzeichnisversion sein, ist aber **nicht** als leer oder nicht existent nachweisbar. Für den Export muss das reale Dateisystem rekursiv inventarisiert werden. [A:30–70; B:13–17]

**Historische Bibliotheksansprüche:** V5.1 bis V6.6 und V6.0–V6.6 werden genannt, etwa 3,8 MB Dateigröße, Markdown/CSV/JSON/MusicXML/Code und MIDI-Mockups, SHA-256-Register, angeblich **36.538 erfolgreiche automatisierte Checks**, kein Fehler. Das belegt weder den aktuellen Status noch die Abdeckung aller MIDI-/Audioinhalte. A behauptet gleichzeitig, automatisierte QA sei noch nicht erfolgt. **Richtiges Ergebnis:** QA-Behauptungen bleiben **ungeprüfte historische Angaben verschiedener Testumfänge**. [A:1–7; A:24–103; B:13–33; B:147–158]

## 5.2 Zwei unterschiedliche Nutzungsebenen der Bibliothek

**Harmony-Kernrelevanz für Steps:** `01_MUSIC_THEORY`, `02_HARMONY`, `03_CHORD_PROGRESSIONS`, Teile von `04_COMPOSING`, `34_REFERENCE_ANALYSIS`, `39_FORMATS_INTEROP`, `40_EXERCISES_TRAINING`, einige `35_GENRE_STYLES`-Kontexte und `00_NAVIGATION`. Übernahme **nach Sichtung** der echten Dateien, Lizenz, fachlicher Gültigkeit und widerspruchsfreier Schemaanpassung. [A:30–68; E:89–232]

**Erweiterte Produktion/optional:** `05`–`06`, `16`–`33`, `36`–`38`, `41`–`43`, historische Sicherungen/QA. Fachlich wertvoll für ein breiteres STEPS-Archiv, aber kein Beleg für eine beschlossene Integration in die Harmony-App. Die ältere Behauptung einer vom Auftraggeber ausdrücklich gewünschten „gesamten Produktionskette“ in B bleibt als **quelleninterner Verweis auf nicht mitgelieferte Gespräche** erhalten, ohne das explizite Drum-Deferral in E stillschweigend aufzuheben. [B:147–158; E:29; E:607–611]

---

# 6. Markt, Wettbewerb, Produktpositionierung

## 6.1 Zusammengeführtes Konkurrenzinventar

Die folgende Tabelle erhält die unterscheidbaren Anbieter aus D und ergänzt die **speziellen visuellen Referenzen** aus E. Preis-, Nutzer-/Rating- und Plattformdaten sind **historische, nicht live verifizierte Behauptungen des jeweiligen Dokuments**; sie eignen sich nicht ungeprüft als aktuelle Veröffentlichung oder Marktprognose. [D:9–50; E:234–251]

| Produkt/Projekt | Plattform/Modell laut D/E | Differenzierender Nutzen bzw. Stärke | Schwäche / Steps-Lernpunkt |
|---|---|---|---|
| [Guitar Pro](https://www.guitar-pro.com) | Windows, macOS; kommerziell ca. €80 | Noten/Tabulatur, Multitrack, MIDI | mächtig, teuer/komplex, wenig Fokus auf Theorieerklärung |
| [Band-in-a-Box](https://www.pgmusic.com) | Windows, macOS; ab ca. US$300 | Auto-Arrangement, Style-Bibliothek | Preis/Komplexität; eigene Nische |
| [ChordPulse](http://www.chordpulse.com) | Windows; ca. €45 | einfache Begleittracks und Sequenzen | veraltete UI, Windows-only |
| [ChordChord](https://chordchord.com/) | Web/iOS/Android über Web; freemium | genreorientierte/AI-Progressionsgenerierung, MIDI | Export teils im Abo |
| [Chordify](https://chordify.net/) | Web/iOS/Android; freemium | Songchords/automatische Transkription, große Sammlung | begrenztes selbstständiges Editieren; Genauigkeit variiert |
| [iReal Pro](https://irealpro.com/) | iOS/Android/Windows/macOS; ca. US$21,99 | Backing Band, anpassbare Songcharts | Übungs-/Performance- statt Erklärfokus |
| [Hookpad / Hooktheory](https://www.hooktheory.com/hookpad) | Web; freemium; ca. US$7,99–8/Monat bzw. US$199 Lifetime im Text | intuitive Harmonie/Melodiebearbeitung, Theorie und Songsammlung | kostenpflichtige Pro-Funktionen, proprietär |
| [Scaler](https://www.pluginboutique.com/products/2707-Scaler) | VST/AU/AAX Windows/macOS; ca. US$50 | umfangreiches Theory-/Scale-Plugin | plugin-/hostgebunden, nicht primär freier Tutor |
| [Autochords](https://apps.apple.com/app/autochords/id788423364) | iOS, free + In-App-Purchase | stimmungsbasierte Vorschläge, Gitarren/Piano/Ukulele | iOS-only, begrenzte Tiefe |
| [Chord AI](https://chordai.net/) | iOS/Android, laut Quelle gratis | Audio-Akkorderkennung | primär Analyse von Songs statt Erzeugen von Progressionen |
| [OtoTheory](https://ototheory.com/) | iOS, freemium | Progression Builder, Begleitung, Stems | iOS-only, steile Lernkurve |
| [Piano Chords & Scales](https://apps.apple.com/app/piano-chords-and-scales/id714086944) | iOS/iPad/Mac, free + IAP | Skalen/Akkorddatenbank, Composer, MIDI I/O | breites, teilweise überladenes UI |
| [Chord Progression Helper](https://f-droid.org/packages/de.metaviewsoft.chordprogressionhelper/) | Android/F-Droid, Apache 2.0 laut D | frei, offline, ohne Tracking, Progression/Melodie/Drums | Android-only, einfachere Oberfläche |
| [Chords – Ajay Parihar](https://github.com/ajayparihar/chords) | Android, quelloffen/Java laut D | einfacher Chord Builder | älteres Projekt, begrenzte Plattform |
| [ChordBud 2](https://apps.apple.com/app/chordbud-2-auv3-midi-sequencer/id1526221230) | iOS AUv3, ca. US$5,99 | MIDI-Chord-Sequencing | braucht Host für Tonerzeugung |
| **Chord Files** | analoge Produktfamilie/teilweise weitere Versionen | sichtbare Beziehungen: Main Chords, Secondary Dominants, Modal Interchange, Secondary Diminished, Neapolitan, Harmonic Minor, Chord/Scale | **Ideen**, keine proprietären Texte, Bilder, Anordnung oder Markenwirkung kopieren |
| **ModeWheel / NewModeWheel** | visualisiertes rotierendes Scale-/Mode-System | Major, Melodic Minor, Harmonic Minor, Harmonic Major; Tonic, Scale Steps, Root Chord, II–V–I und Audio | erklärende, eigene Visualisierung statt Klon |
| **4 × Wheels of 7 / NewJazz** | didaktische 4×7-Modi-Konzepte | vernetzte Scale-Familien | taxonomisches Vorbild; Lizenz/Quellen offen |
| **The Chord Wheel** | Tonart-/Transpositionssystem; teils digitale Ausgabe | unmittelbare Key-Relationships, Improvisation, Transposition, Playback | Steps muss über einfache Circle-of-Fifths-Navigation hinausgehen |
| **Modelwheel** | lokale Referenz erwähnt | **noch nicht identifiziert** | ohne Sichtung keine Funktions-/Lizenzaussage |
| **Weitere Vergleichsklassen** | Captain Chords, Xfer Cthulhu, Landr Composer, Ableton Live, ChatGPT | DAW/Plugins, Web/AI und Spezial-Tools | teils komplex, proprietär oder anderes Marktsegment |

**Wettbewerbsdaten und Nachfrageindikatoren laut D, ohne heutige Prüfung:** Chordify: 36 Mio. Songkatalogeinträge, rund 34.000 Bewertungen, Ø 4,7/5; Chord AI: „500k+ Nutzer“; Autochords: Ø 4,8/5 bei 34 Reviews; Hookpad: „80k Songs“ im Vergleich und an anderer Stelle eine **offenbar defekte Angabe „0+ songs“**; iReal Pro als Einmalkauf; Chord Progression Helper laut Text seit September 2026 bei F-Droid. Diese Kennzahlen sind **Marketing-/Markt-Snapshots**, nicht aktuelle Messungen. Ihr Datum, Zählweise und Primärnachweis fehlen; sie dürfen **nicht** als verifizierte TAM-/Nutzerprognose fungieren. [D:13–50]

**Distribution und Community (VORSCHLAG):** GitHub-Quellcode und Releases; optional PyPI, gebündelte Installer, später GitHub Pages/Wiki; Foren wie LinuxMusicians, Reddit (Musictheory/Gamemusic), Hacker News; mögliche freiwillige Spenden/Pay-what-you-want, aber **keine** bestätigte Monetarisierungsentscheidung. Product-Story: frei, lokal, lehrorientiert, kein erzwungenes Nutzerkonto/Tracking, modular erweiterbar, gemeinschaftlich beitragsfähig. [D:38–50; D:110–190]

## 6.2 Klare Differenzierung und Designprinzip

**Produktthese:** „Steps zeigt mehrere musikalisch begründete Wege von einem harmonischen Zustand zum nächsten und erklärt, warum diese Wege funktionieren.“ Keine Übernahme fremder Chord Files-Grafik, sondern **eigene Informationsarchitektur** mit Source/Framework/Confidence-Layer. UI muss nicht nur Akkordchips, sondern eine verständliche Relationsnavigation, interaktive Transposition, Audio und progressive Offenlegung von Details unterstützen. [E:253–285]

---
# 7. Glide als technische Ausgangsbasis und Steps-Abzweigung

## 7.1 Gewünschter Wiederverwendungsumfang

C dokumentiert eine **explizite Absicht, eine neue Anwendung auf der monatelangen Glide-Arbeit aufzubauen**, nicht bloß einen Wunsch nach ähnlichem Aussehen. Erhalten und für Steps auf Adaptierbarkeit geprüft werden sollen:

- **Softwarearchitektur:** Python-/Tkinter-/Tcl-Basis, Modulschnittstellen, Initialisierung, Fenster-/Unterfenster-/Dialogsteuerung, App Lifecycle, Abbau der Oberfläche, Event-/Callback-/Timer-Verwaltung, Datenmodelltrennung, Adaptergrenzen.
- **Funktionale Infrastruktur:** Dateioperationen, sichere Ein-/Ausgabe, Import-/Export-Logik, Speicherformate, Zustandserhalt, Fehlerbehandlung, Debugging, Updates/Migration, Undo-/Redo-Patterns soweit vorhanden, Einstellungen und lokale Datenhaltung.
- **GUI-/UX-System:** Light-/Dark-Modus, alternative Pixel-/Designvarianten, Themenfarben, Typografie und Schriftstile, Designabstände, responsive Fenster und Breakpoints, Seiten-/Hauptansicht, Pinnwand-/Listen-/Ordnerkomponenten, Dialoge, Toolbar/Buttons, Menüs, Scrollen, Fokus, Hinweise und Karten, Accessibility.
- **Brand/Design Governance:** Naming, Branding, Logo-Logik, Grafik-Master, Richtlinien für Gestaltung, Bild-/Icon-Verwendung, Screenshots, Inspiration und Konkurrenzabgrenzung.
- **Entwicklungsprozess:** Quellstruktur, Tests, native UI-Regressionsmatrix, Testwerkzeuge, Fehler-/Rückrufauswertung, Leistungsbenchmarks, CI-Workflows, plattformübergreifende Prüfung, Versionierung, Releasepflege.
- **Bau und Betrieb:** Packaging, Windows-/Linux-/macOS-Bereitstellung, Bestand und Lizenzbeigaben, CycloneDX-SBOM, Paketprüfsummen, Quell-/Buildabgleich, Installation/Startproben.
- **Nachweis- und Übergabeprozesse:** Git-Historie, Archivierungs- und Aufbewahrungsregeln, Übergabevertrag, README-Featureübersicht, Wiederverwendungsinventar, Lizenz-/Abhängigkeitsstatus.

Der Gesprächsexport meldet eine Erweiterung der Glide-Featureübersicht um **20 zusätzliche technische Systemfähigkeiten**. Deren **konkrete 20 Titel** stehen im Export nicht. Sie werden hier nicht erfunden; das tatsächliche `Glide-System`-Verzeichnis, Featureübersicht und Übernahmevertrag müssen vor der Implementation gelesen und als Inventar eingetragen werden. [C:1–6; C:74–83; C:130; C:139]

## 7.2 Technische Kopplung: nicht einfach die App umbenennen

Im geprüften Gespräch wird als Inventarstand **94 Quelldateien**, davon **88 ohne direkten `tkinter`-Import**, gemeldet. Die zentrale `ListApp` umfasst jedoch laut Gespräch immer noch **1.863 Methoden**. Daraus folgt: lose gekapselte Hilfsmodule sind ein Übernahmevorteil, aber Fenster-, Dialog- und Ablaufsteuerung sind **nach wie vor stark an ListApp gekoppelt**. Weder die Anzahl der Dateien ohne Tk-Import noch die Featureliste beweist eine entkoppelte Bibliothek. Für Steps sind **Wiederverwendungsbedingungen, Adapter, Glide-Domänenabhängigkeiten, Tests und Extraktionsaufwand pro Baustein** erforderlich. [C:74–83; C:130]

| Klasse | Beispiele und Reuse-Muster | Empfehlung / Evidence-Gate |
|---|---|---|
| **I. generische Bausteine** | Dateihilfen, Prüfroutinen, Farben/Theming, Basiskomponenten, Packaging, Version/Docs | übernehmen nach isoliertem Import-/Lizenz-/Regressionstest |
| **II. adaptierbare Bausteine** | Seiten-/Dialogsteuerung, Layout, Präferenzen, Datensicherung/Import, Render-/Aktualisierungsprozesse | Adapter implementieren; UI-Zustandsabhängigkeiten und Lebensdauer prüfen |
| **III. domänenspezifische Glide-Bausteine** | Aufgaben-/Wochenplanungs-/Pinnwand-/Pixelzeichen-Fachlogik | nicht als Harmony-Engine übernehmen; höchstens Muster/Widget wiederverwenden |
| **IV. noch nicht sauber isolierte Teile** | `ListApp`-Methoden und globale UI-Koordination | modulweise extrahieren, nicht blind mitkopieren |
| **V. Prozesse/Nachweise** | CI, UI-Matrix, Dokumentationsregeln, SBOM und Releasekontrollen | als verbindliches **System-Template**, neu gegen Steps absichern |

Diese Einteilung ist eine **hier abgeleitete Arbeitsklassifizierung**, keine in C bereits vollständig belegte modulgenaue Bewertung. Die tatsächliche Liste der Bausteine, Importierbarkeit, Version und Commitbindung bleibt offen.

## 7.3 Chronologie der gemeldeten Glide-Arbeit und wichtigen Fehlerbehebung

Die folgende Tabelle bewahrt **alle in C sachlich unterschiedlichen Zwischenstände** – Testzahlen dürfen zwischen Commits nicht addiert oder als gleicher Prüfstand vermischt werden. Ohne GitHub-Replay sind sie Statusmeldungen aus einem Gesprächsexport. [C:1–659]

| Bereich / Entwicklungsstand | Dokumentierter Befund | Konsequenz/Statusgrenze |
|---|---|---|
| Frühfehler: Fensterabbau | unter Windows überlebten geplante Tk/Tcl-Rückrufe geschlossene Testfenster trotz Exitcode 0 | Callback-Abbau korrigiert; Prüfharness soll solche Fehler trotz Exitcode 0 rot melden [C:25–65] |
| Früher Layoutfehler Linux | Pinnwandleiste in einer Konfiguration um **8 Pixel** zu eng | Anpassung im **4-Pixel**-Designraster, Beschriftungen erhalten [C:47–65] |
| Pinnwandleistenprobe | **1.250 Knopfprüfungen**; 3 Anordnungen, 4 Fensterbreiten, Listen/Ordner, Hinweise an/aus, Hell/Dunkel | gezielter Windows-Nachweis berichtet [C:65] |
| Erste gezielte Nachprüfungen | 6 Gruppen (u. a. Import, Themewechsel, Aufgabenbedienung) erfolgreich; keine unbehandelten Rückruffehler | nur gezielte, keine globale Freigabe [C:83] |
| Workflow-Test | optionale Mac-Vollprüfung erweiterte Shell-Schritte von **6 auf 7**; 6 Workflow-Tests grün | `AGENTS`/CI-Vertrags- und Shell-Syntaxprüfungen angepasst [C:92] |
| Commit `a4c34b8` in **PR #71** | 19 strenge Grundstufen, 265 Werkzeugtests (1 Skip), zweimal 1.155 Fachtests, bytegleiche Python-Lieferung | damals grün **lokal**; Windows/Linux/Mac-Vollmatrix noch offen [C:101] |
| Benchmarks 1.000 Aufgaben | Abhaken inkl. Speichern und Update **~54 ms Median**, reines Speichern **~32 ms Median** | kein gemessener Vorher-Nachher-Gewinn [C:110] |
| Benchmarks 10.000 Aufgaben | Abhaken inkl. Speichern/Update **~380 ms Median**; bestimmte Ansichtswechsel bei 1.000 Aufgaben **>1 s** | Optimierung erst nach reproduzierbarer Profiler-Ursachenanalyse [C:119] |
| Historische Evidenzsicherung | **225** vorher zur Altersbereinigung vorgesehene QA-Dateien wiederhergestellt, Git-Blobs passend zu main | Prüfbelege sind schützenswert [C:121] |
| Mac-Geometrie | angeforderte **960 Punkte** Höhe, Runner liefert zunächst **700**, später **954** | Runner-/Tcl-Geometrie- und Testumgebungsproblem, zeitweise rot; keine pauschale Abschwächung der Assertion [C:130; C:447] |
| Glide-System- und README-Inventar | **20** technische Fähigkeiten ergänzt; Steps-Übernahmevertrag mit Abhängigkeiten/Prüfgrenzen gemeldet | Dateien selbst liegen hier nicht vor [C:130] |
| Öffentliche Github-Darstellung | Beta-/„3.50“-Marketing und Versionsbadge aus READMEs entfernt, technische Versionsbezüge als Nachweis erhalten; **15 Github-Topics** gesetzt/gelesen | zwischen öffentlichem Marketing und erforderlichen Versionsmetadaten unterscheiden [C:110; C:139] |
| CycloneDX/SBOM | Paketbuilder erzeugt Komponenten-/Lizenzinventar und nimmt es in Prüfungen/Hashes auf; vollständiger Abhängigkeitsgraph **nicht** vorhanden | SBOM nicht als vollständige Supply-Chain-Freigabe ausgeben [C:148–157] |
| README-Vertrag | Versionsnummer soll in Einstiegs-README nicht werben; deshalb wird dort `VERSION`-Dateiverweis erlaubt, aber Datum/Standprüfung bleibt | intentionaler Konflikt mit altem Standtest behoben, Nachweise zu prüfen [C:166] |
| Linux-Vollprüfung alter Fixstand | auf `a4c34b8` einmal vollständig grün; Defektgegenproben liefen noch | commitgebundener Teilnachweis [C:175] |
| Commit `967f84f` | 19 Schritte, **279** Werkzeugtests (1 Skip), zweimal **1.155** Fachtests, bytegleicher Python-Lieferabgleich; Arbeitsbaum sauber | neue Gesamtmatrix erforderlich [C:184] |
| Mac-Paket auf `967f84f` | gebaut und isoliert gestartet; historische Komponentenbasis/Ablage geprüft | Paket-/Starttest ist **kein** nativer UI-Volltest [C:193] |
| Reuse/Git-Ablage | lokale Git-/Dateiablagestände driften auseinander; lokale README/License anfänglich fehlen, Grafik-/Steps-Unterlagen nur lokal | kein pauschales „alles auf GitHub“; Sicherungs-/Diff-Plan [C:209–236] |
| Auftragsfreigabe Ablage | Archiv **E:**, später frische lokale Arbeitskopie am bisherigen **C:-Pfad**; erst nach **PR #71 grün + Merge auf neuem main** | bewusste Reihenfolge; kein durchgeführter Neu-Klon belegt [C:248–273] |
| Erstinventar lokal | ca. **7,9 GiB**, **35.381 Dateien**, davon ca. 3,3 GiB `.git`-Metadaten und 3,1 GiB zusätzliche Arbeitskopien | anderes Messstadium als spätere Archivzahlen [C:282] |
| Grafik-Master-Abweichungen | **91 Dateien**, ca. **257 MiB**, nur lokal oder abweichend; Logos, Referenz-/Inspirationsmaterial | Originale gesondert sichern, Quellen/Rechte zuordnen [C:293] |
| Lokaler Windows-Vollprozess | ohne Abschlussprotokoll beendet; Neustart um **13:16 Uhr** erkannt, **keine Ursache** abgeleitet | kein valider voller Erfolg / Absturzursache offen [C:295] |
| E:-Zwischensicherung | Grafik-Master und Vorbereitung per SHA-256 Quell-/Zielgleichheit gemeldet | Teilbeleg, Archivabnahme folgt [C:322] |
| Textdateienabgleich | **99** aktive neue/geänderte Textdateien in GitHub-Historie gefunden, **18** weitere sind erzeugte historische Paketmetadaten | ersetzt keine komplette Dateiabnahme [C:333] |
| Symbolersatztexte | mehrdeutige Texte korrigiert und Rollenvertrag per Regression abgesichert | isolierte Änderung/Prüfung berichtet [C:335] |
| Windows-PR-Fehler | „Gelesen“-Knopf ragt **3 Pixel** über; 900-Sek.-Gesamtbudget, davor **895,28 s** verbraucht; `fensterende3507` erst vorbereitet, einzeln ~10 s | Testlauf organisatorisch splitten, Assertions beibehalten [C:384–386] |
| Neuerungskarte | **48** Konfigurationen: 4 Schriftstile, mittel/groß, Hell/Dunkel/Pixel, 2 Fenstergrößen; drei Versionseinträge bleiben; Gelesen sichtbar/wirksam | gezielte Prüfung gemeldet [C:403] |
| Späteres E:-Backup | **35.380 Dateien**, ca. **8,28 GB**, kopiert und via Hash geprüft; temporärer Logo-Prüfrest entfernt, ~**197 MiB** freigegeben | keine abschließende Git-Metadaten-/Archivabnahme gemeldet [C:405] |
| Nachtests nach Kartendarstellung | UI/UX **17/17**, native Bedienprobe und neue Abschlussgruppe inkl. Pinnwandleiste, **300 Themenfarbenprüfungen**, Rücktaste, Restflächen, Root-Abbau | lokale Teilprüfungen [C:414] |
| Git-Stashes | **4** lokale Stashes als separate Änderungen exportiert | Bereinigung nur mit Sicherungsinventar [C:416] |
| Commit `17d268f` | 19/19 Grundstufe, **284 Werkzeugtests**, zweimal **1.156 Fachtests**, **343 Dokumentverweise**, bytegleicher Python-Abgleich | Fix in PR #71; Gesamtmatrix erneut erforderlich [C:425–427] |
| Git-Schaden | lokal beschädigtes Objekt; später klargestellt, dass es ein **Commit**, kein Datei-Blob war; richtig angefordert und wiederbeschafft | restliche Git-Lücken nicht abschließend freigegeben [C:416; C:436] |
| Steps Audio-Umorganisation | **21 Audio-Unterlagen** in Steps-Unterordner verschoben, mit erster Sicherung bytegleich; neue Pfade zusätzlich gesichert | wichtiger **lokaler** Quellbestand, aktuelle Dateien nicht vorgelegt [C:438] |
| Weitere Mac-Geometrie | verfügbare Höhe **954 statt 960**; Tk begrenzt die bei Displayöffnung erfasste Arbeitsfläche; separater Diagnosezweig | kein dauerhafter Mac-Fix im Bericht bestätigt [C:447] |
| Linux UI-Fail | nach UI-Rebuild wurde zerstörter Seiteneditor weiter referenziert | gezielte Gegenprobe **199 Knopfprüfungen** in **5 Konfigurationen**; Inhalte und Seitenziel erhalten [C:486–488] |
| Regression auf Editorbereich | betroffene Gruppe lokal **13/13**; nativ Linux UI/UX **17/17**, Arbeitsmodi **63/63** | gezielt grüner Nachweis [C:497; C:517] |
| Windows Timer-Fix | Fensterfarben-Timer verlor nach Dialogschluss Callback; Hauptfenster als Eigentümer | Gegenprobe und lokale Kernprüfung grün [C:506] |
| Mac Historienmigrationsprobe | historischer Lieferstand erst unvollständig; Workflow auf vollständige Git-Historie vereinheitlicht | Vorprüfungen nachgebessert [C:519] |
| Commit `f3408de` | zusammengeführte Fixes in PR #71; Linux-/Windows-/Mac-Vollprüfungen erneut gestartet | ein weiterer **neuer Prüfstand**, nicht mit älteren verwechseln [C:528] |
| Mac-Toast/„Erledigt!“ | Mac-Geometrieprobe lief zu früh, kurzlebige Anzeige nach starrer **1,1-s-Wartezeit** noch sichtbar | Test wartet nach Korrektur auf tatsächliches Ende der Animation; Overlap-Assertions erhalten [C:561; C:588] |
| Startseiten-Gegenprobe | lokal **459 Knopfprüfungen**, inklusive künstlich verzögerter Animation | auf Diagnosezweig; native Mac-Nachprüfung dann erfolgreich [C:597–628] |
| Spätester Berichtseintrag | auf bisherigem PR-Commit **beide Linux-Vollprüfungen grün**; Mac-Zielproben **Bedienung, Startseite, historischer Import grün**, Mac-Vollprüfung weiterhin aktiv; **beide Windows-Läufe ohne Endergebnis**; PR unverändert | **kein vollständiger grüner Multi-OS-Endstand, kein nachgewiesener Merge** [C:616–648] |

**Arbeitsprozess-Lektion aus C:** Fehler zuerst isoliert reproduzieren und den konkreten Nachtest abschließen; nicht bei jedem Nebenfund sofort alle Langläufe erneut starten. Auf demselben Commit die verpflichtende Matrix kontrolliert ausführen. Ausgangsstände, rote Belege, Folgefixes und Testgrenzen nachvollziehbar konservieren. Der Gesprächsexport enthält eine explizite Priorisierung auf die Pflichtmatrix, nachdem Zusatzarbeiten und wiederholte teure Läufe zu erheblichem Zeitaufwand geführt hatten. [C:455–488; C:528–648]

## 7.4 Verbindliche Preservation-first-/Archivierungslogik aus C

**Explizit dokumentierter Wunsch:** altes lokales Glide-Verzeichnis archivieren, neue lokale Kopie **erst nach grün geprüfter und nach `main` gemergter PR #71** aus GitHub am bisherigen C:-Pfad erzeugen. Archiv und schützenswerte Zusatzmaterialien auf Laufwerk **E:**; früheren C:-Bestand erst nach Archiv-/Hash-/Vollständigkeitsabnahme und geklärter Git-Sicherung entfernen. [C:209–273]

**Schützenswerte Bestandteile:** Grafik-Master, Logos, Inspirationen von Wettbewerbern, Originalbilder/Screenshots, Steps-Unterlagen, 21 Audio-Unterlagen, 4 exportierte Stashes, Git-Historie einschließlich wiederbeschaffter Commit-Objekte, historische QA-Nachweise einschließlich 225 wiederhergestellter Dateien, Lizenz- und Paketbelege. **Nicht jedes visuelle Referenzmaterial ist für ein öffentliches Repo redistributable.** [C:209–215; C:282–293; C:405–438]

**Löschen/Bereinigen erst mit Freigabekette:** (1) `main`/PR-Stand und Merge per konkretem SHA bestimmen; (2) Pfad-/Datei-/Hash-Inventar der lokalen und GitHub-Dateien; (3) Git-Objekte und Stashes prüfen; (4) separat geschützte Assets kopieren; (5) Hashes vergleichen und Restore-Probe; (6) klassifizierte löschbare Prüf-/Cache-Dateien gesondert auflisten; (7) Nutzerfreigabe; (8) Bereinigung; (9) frischer Klon und unabhängige Start-/Tests; (10) alte Kopie erst danach entfernen. In C sind Teile der Sicherung erfolgt, **aber weder Schlussabnahme noch Neu-Klon noch vollständige Bereinigung nachgewiesen**. [C:209–333; C:405–438; C:616–648]

## 7.5 GitHub-Projektseite und Dokumentation

C meldet bereinigte öffentliche Glide-Marketingtexte zu **Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen** und Entfernung von aktiver Beta-/Erstversion-Werbung sowie allgemeinen „3.50“-Anpreisungen. **Technische Versionsnummern** in `VERSION`, Paketbelegen, Changelogs, alten Fehlerfällen und Bildpfaden müssen erhalten bleiben. Die Featureübersicht darf nicht nur Glide-Fachfunktionen, sondern auch die 20 gemeldeten Systembausteine enthalten; die genaue Liste ist beim Repo-Audit zu extrahieren. Nicht Teil dieses Auftrags ist eine erneute direkte Änderung der GitHub-Seite. [C:1–6; C:130–166]

---

# 8. Zielarchitektur: Steps-App, Knowledge Base und AI-Skill

## 8.1 Entkopplungsprinzip

**`SKILL.md` ≠ Knowledge Base ≠ App Logic ≠ Tests.** Der vorhandene Fachskill-Entwurf soll nicht gelöscht, sondern später als schmale Schnittstelle über einer durch Quellen, Schemas und Tests verifizierten KB verwendet werden. Die Harmony-Engine soll vollständig unabhängig von Tkinter funktionieren, damit dieselben Theoriefunktionen CLI, Skill, Tests und GUI verwenden können. `music21` eignet sich als Adapter/Testreferenz, aber seine Nutzung als Kern ist noch nicht beschlossen. [E:9–27; E:503–525; E:558–605]

## 8.2 Vorgeschlagene Verzeichnisstruktur (konsolidiert)

Die folgenden Verzeichnisse sind **ein Architekturentwurf**, kein Nachweis ihrer Existenz. Sie vereinigen D (`steps/`-Package), E (`app/`, `knowledge/`, `research/`, `schemas/`, `decisions/`, `tests/`) und C (Glide-System-Inventar, Preservation, QA und Übergabe) unter einer konsistenten Basis. [D:110–146; E:289–363; C:1–6]

```text
steps/
├── README.md                      # DE/EN, Produkt und Einrichtungsstatus
├── LICENSE                        # nach eigenständiger Lizenzentscheidung
├── AGENTS.md                      # Codex-Arbeitsvertrag
├── SKILL.md                       # nur Zugang/Workflows; kein Primärwissen
├── CONTRIBUTING.md
├── CHANGELOG.md
├── VERSION                        # technischer Stand, kein Marketing-Badge
├── pyproject.toml
├── .gitignore
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── app/
│   ├── __main__.py
│   ├── core/                       # lifecycle, settings, storage adapters
│   ├── theory/                     # pure pitch/chord/scale/transposition engine
│   ├── progression/                # progression models, typed relations
│   ├── audio/                      # später MIDI/playback
│   ├── ui/                         # Glide-basierte oder eigene Tkinter-Widgets
│   └── adapters/                   # music21, MIDI, MusicXML, Glide
├── knowledge/
│   ├── README.md
│   ├── sources/
│   │   ├── registry.yaml
│   │   ├── raw/                     # nur lokal zulässige Originale
│   │   └── extracted/               # lizenzkonforme eigene Aufbereitung
│   ├── concepts/
│   │   ├── intervals/
│   │   ├── scales/
│   │   ├── chords/
│   │   ├── harmony/
│   │   ├── progressions/
│   │   ├── voice_leading/
│   │   └── styles/
│   ├── relations/
│   ├── examples/
│   ├── corpora/
│   └── glossary/
├── research/
│   ├── papers/
│   ├── notes/
│   ├── competitors/
│   ├── gaps/
│   ├── bibliography/
│   └── ableton/                   # bis Projektscope geklärt separat
├── decisions/                    # ADRs mit Status und Beschlussbeleg
├── schemas/
│   ├── source.schema.json
│   ├── concept.schema.json
│   ├── chord.schema.json
│   ├── progression.schema.json
│   └── analysis.schema.json
├── tests/
│   ├── theory/
│   ├── chords/
│   ├── progressions/
│   ├── transposition/
│   ├── enharmonics/
│   ├── fixtures/
│   ├── integration/
│   └── native_ui/
├── docs/
│   ├── architecture/
│   ├── theory/
│   ├── user/
│   ├── roadmap/
│   ├── system_reuse/
│   └── handover/
└── tools/
    ├── ingestion/
    ├── validation/
    ├── packaging/
    └── migration/
```

**Unterschied zum frühen D-Entwurf:** dort lagen `steps/__init__.py`, `ui.py`, `chord.py`, `playback.py`, `analysis.py`, `data/`, `examples/` direkt unter einem kleinen Python-Paket. Diese Struktur ist für eine Demo legitim; die ausdifferenzierte E-Struktur ist bei wachsender KB besser geeignet. Python-Paketname, `app`-Importpfad, `python -m steps` vs `python -m app` und tatsächlicher Repo-Baum müssen vor Implementierung einmal verbindlich festgelegt werden. [D:123–146; D:150–190; E:289–363]

## 8.3 Minimale kanonische Datenmodelle und Prüfregeln

**Source Record**, zum Beispiel mit IDs, Autor(en), Jahr, Original-URL, DOI, Sprachcode, lokalem Pfad, Hash, Lizenz, `reuse_status`, Ingestionsmethode, Reviewed-Status, Themen, Evidence Quality und Notizen. Ein konkretes historisches Beispiel aus E: `src_neal_2005_popular_music_analysis`; DOI `10.31751/524`, CC BY 4.0, `parsed`, `reviewed: false`, `confidence: high`; Beispielpfad `knowledge/sources/raw/Popular_Music_Analysis_in_American_Music.pdf`, **SHA-256 noch `null`**. Dies ist ein **Schema-/Beispieldatensatz**, keine heutige Inventarbestätigung. [E:364–407]

**Concept Record**, etwa `harmony.secondary_dominant` / `Zwischendominante`: Definition, Prerequisites (`chord.dominant_seventh`, `harmony.dominant_function`, `theory.scale_degree`), Broader/Related Relations, Roman Numeral `V7/ii`, Stilstufung (`classical_tonal: common`, `jazz: common`, `pop_rock: context_dependent`), Quellen-IDs, Validierungsfälle und Status. E setzt den Beispieldatensatz auf `reviewed`, obwohl der produktweite Review der KB offen ist; **nur Beispielcode**, keine allgemeine Abnahme. [E:409–456]

**Progression Record:** ID, Tonika mit separater `pitchClass` und `spelling`, Modus, Akkorde mit Symbol und Roman Numeral, optional mehrere Analysen samt Framework/Confidence, Provenienztyp und künftig Timing/Phrasen/Stil/Voice Leading. Konkretes E-Beispiel: C-Dur: `C (I) – E7 (V7/vi) – Am (vi) – F (IV)`, `framework: functional`, `confidence: 0.95`, `provenance: constructed_example`. Der Konfidenzwert **0,95 ist ein Musterwert**, kein empirisch kalibriertes Modell. [E:458–484]

**Kanonische Integritätsregeln:** Tonart/Spelling von klingender Pitch Class trennen; Chord Symbol getrennt vom Voicing; Harmonic Interpretation stets an Kontext binden; jedes Claim `source_id`, `style_context`, `theory_framework`, `confidence`, `review_status`, `validation_case` und ggf. `alternative_analyses`; Präferenz für maschinenprüfbare JSON-/YAML-Schemas; keine Vererbung ungeprüfter Bibliografien aus Transkripten. [E:93–119; E:486–554]

## 8.4 Ingestion-Pipeline und Skill-Prozesse

**Spezialisierte Theory-Kette (E):** `Source Intake → Metadata Normalization → Concept Extraction → Claim Extraction → Cross-Source Reconciliation → Canonical Knowledge Entry → Test Generation → App Integration`. Ergänzt um: Rechteprüfung, Hash, Validierungsstatus, systematische Golden Tests. [E:503–525]

**Ableton-Interviewkette (F):** `Source Discovery → Fetch → Metadata Extraction → Normalization → Deduplication → Import → Search`. Ergänzung: Sprache/Translation Group, Interview-vs.-Künstlerprofil und Lizenz für Downloadassets. [F:179–204]

**Frühe MVP-UX (D):** Progression anlegen → speichern → optional Klang/Keyboard/Fretboard → Theoriehinweise. **Implementierungsreihenfolge empfohlen:** zuerst korrektes Harmoniemodell samt Ingestion und Tests, dann GUI mit Glide-adaptierten Komponenten; Audio dort einführen, wo definierte MIDI-Semantik und Rechte vorliegen. [D:76–108; E:25–29; E:661–670]

## 8.5 Technische Optionen statt voreiliger Festlegung

| Bereich | Genannte Optionen | Entscheidungsstatus |
|---|---|---|
| Desktop-UI | vorhandenes **Python/Tkinter**; alternativ PyQt/PySide, Kivy, Electron/Web/React | Tkinter als vorläufige Prototyp-Basis vorgesehen; Migration nur mit funktionalen Kriterien |
| MIDI | `mido`, `python-rtmidi`, `pygame.midi`; alternativ `pretty_midi` | Bibliotheken evaluieren, nicht alle zwangsläufig installieren |
| Audio Playback | `pygame`, `pyaudio`, `fluidsynth`/`pyfluidsynth`, ggf. System-MIDI/Instrumente | Latenz, Plattform und Audioqualität offen |
| Theorie | `music21`, `mingus`, `chordparser`, eigener Python-Core + Adapter | ADR-002 offen; Empfehlung eigener Core + `music21`-Adapter |
| Grafiken | Tk Canvas, PIL/Pillow, matplotlib; alternativ Web-Canvas | UI-Prototyp nach Nutzerforschung |
| Speicherung | JSON für Progressionen, YAML/JSON Knowledge Base, JSONL für Roh-/Austauschdaten, ggf. später SQLite/relational/Graph | keine DB-Entscheidung; Graph-Semantik ohne Graph-DB vorgeschlagen |
| Export | MIDI, MusicXML, ggf. weitere DAW-Formate | Integration nach Kernfunktion |
| Distribution | GitHub Releases, Installer/PyInstaller, ggf. PyPI und später mobile Web/Kivy | nicht freigegeben, Designziel plattformübergreifend |
| Betrieb | offline/local-first; kein Pflichtkonto/Anzeigen/Telemetry | Zielanforderung, noch keine unabhängige Privacy-Abnahme |

[D:52–66; D:76–89; E:21–27; E:568–605; F:200–206]

**Technischer Fehler im alten Onboarding-Beispiel:** `pip install tkinter` aus D ist **keine verlässliche plattformübergreifende Installationsanweisung**. Tkinter kommt bei vielen Python-Distributionen mit und benötigt unter Linux ggf. das OS-Paket `python3-tk`. Statt sämtliche vorgeschlagenen Pakete auf Verdacht zu installieren: pro Zielplattform reproduzierbare `pyproject.toml`-/Lockfile-Abhängigkeiten und einen Tk-Smoketest definieren. Auch `cd C:\Users\…\OneDrive\Github` ist ein **nutzerspezifisches Beispiel**, kein portabler Standard. [D:150–166]

---
# 9. Qualitätssicherung, Validierung und Abnahmekriterien

## 9.1 Qualität ist ein Nachweis pro Commit, Asset und Teilsystem

**Wichtigste Regel:** Eine grüne lokale Testgruppe, ein erfolgreicher ZIP-Bau, ein Mac-Paket-Start, ein historischer 36.538-Check-Vermerk oder eine erfolgreiche Linux-Vollprüfung **ersetzt nicht** eine aktuelle, einheitlich SHA-gebundene vollständige Freigabematrix. Auch fehlerfreier Prozess-Exitcode 0 allein genügt nicht, wenn Tcl/Tk-Callbacks nach Fensterschluss Fehler auslösen. [A:184–201; B:25–33; C:25–65; C:616–648]

| Prüfebene | Prüfinhalt | Erforderlicher Evidenznachweis |
|---|---|---|
| **Q0 Projekt-/Artefaktidentität** | Repo, Branch, Commit, Version, SHA-256, Betriebssystem/Interpreter/Tk | maschinenlesbarer Prüfmanifest, festgehaltener Code-Freeze |
| **Q1 Quelldaten** | Existenz, Größe, Encoding, Titel/Autor/Datum, DOI/URL, Duplikat/Übersetzung, Lizenz | `source_registry`, Quellbeleg, Hash, Rights-Status |
| **Q2 Theoriemodell** | Pitch/Enharmonik, Chords/Voicings, Tonarten, Funktionen, multiple Analysen | Golden Fixtures und nachvollziehbarer Testoracle-Abgleich |
| **Q3 Daten-/Schemaqualität** | JSON/YAML/CSV/JSONL/MusicXML, Pflichtfelder, IDs, Referenzen, Links | Schemaprüfungen, Cross-Link-Checks und Negativtests |
| **Q4 Import-/Export-Qualität** | Round-trip, Unicode, Spelling, Takt/Tempo, Controller-Events, MIDI-Parse, ZIPs | Fixture-Hash, semantischer Round-trip, Fehlerfalllisten |
| **Q5 Native GUI** | Tk-Lifecycle, Timer, Callback-Cleanup, Fensterflächen, Themes, Pixel/Light/Dark, Fonts, Breakpoints | native Linux/Windows/macOS-Testmatrix und Abbild-/Logbelege |
| **Q6 Performance** | Startup, große Datenbestände, Progressionen, Render/Ansichtswechsel, Speicherwege | reproduzierbare Workloads/Baselines mit Median/Quantilen |
| **Q7 Rechte/Supply Chain** | Herkunft, Weitergabe, Drittanbieter-Bibliotheken, Assets, SBOM/License Beigaben | Lizenzregister, CycloneDX, Abhängigkeitsgraph oder explizite Restlücke |
| **Q8 Delivery** | reproduzierbares Paket, Report-Format, Manifeste, Hashprüfung, isolierter Start | verifiziertes ZIP, PDF/DOCX (wenn benötigt), Installationsprobe, Rückrollstrategie |
| **Q9 Benutzerabnahme** | Echte Tonarten/Akkordfolgen, didaktische Verständlichkeit, Audio-Latenz, Accessibility | protokollierte Nutzer-/Expertentests, signierte Freigabe |

## 9.2 Theorie-Golden-Tests aus E – vollständig erhalten

Die Forschungsgrundlage nennt folgende konkreten Start-Fixtures; als **Entwurfsfälle**, nicht als bereits ausgeführte Tests: [E:661–700]

| Gegenstand | Testfall / Erwartung |
|---|---|
| C-Dur-Skala | `C D E F G A B` |
| A natürlich Moll | `A B C D E F G` |
| C harmonisch Moll | `C D Eb F G Ab B` |
| C-Dur-Dreiklang | `C E G` |
| C-Dominantseptakkord | `C E G Bb` |
| Slash-Bass | `C/E` → `E` |
| Funktion im Kontext | `C7` in F-Dur → `V7` |
| Zwischendominante | `E7` in C-Dur → `V7/vi` |
| Transposition | `C–G–Am–F`, +2 Halbtöne → `D–A–Bm–G` |
| Deutsche Notation | `H` = englisch `B natural` |
| Deutsche Notation | `B` = englisch `Bb` |
| Zwischendominante II | `V7/ii` in C-Dur → `A7` |
| Auflösung | `A7` (als V7/ii) → `Dm` |
| Entlehnung C-Dur | `iv` → `Fm` |
| Entlehnung C-Dur | `bVI` → `Ab` |
| Entlehnung C-Dur | `bVII` → `Bb` |

Weitere erforderliche Fälle: enharmonisch gleiche Töne mit unterschiedlichen Funktionen, alternate spellings, Modulation, Inversionen, Polychords, fehlender Kontext, mehrere plausible Stilanalyse-Frameworks, Nicht-4/4-Metrik, negative/ambivalente Musiktheorie-Fälle, Codec/Encodingfehler, generative Empfehlungen mit nachgewiesenem Geltungsbereich. **Mindestens 100 deterministische Tests** sind als frühester fachlicher Meilenstein vorgeschlagen; Zahl und Umfang dürfen nach konkreter Engine-Implementierung wachsen. [E:661–700]

## 9.3 Zusätzliche QA-Anforderungen der älteren Produktionsbibliothek

A/B verlangen: rekursive Dateisuche und Inhaltsindizes, SHA-256 für Dateien/ZIP, alle Dateien genau einmal im Index, Typ-/CSV-Schemaprüfung, keine verwaisten Links, MIDI-Lesbarkeit und Event-Integrität, Tempo/Taktzahl/Step-Checks (bei Drum-Loops als Beispiel 16/32 Schritte pro 4/4-Takt), ZIP-Inhalte separat validieren, Ablage-/Import-Rechte überprüfen, Broken-URL-Meldungen, Vollständigkeit der 74 DeSantis-Strategien, Formatvergleich von Markdown zu PDF/DOCX, Text-/Bild-/Mermaid-Renderkontrolle, kein `.tmp`/`.bak`/VCS-Rest im **öffentlichen Liefer-ZIP**, Audio-Listening-Test soweit Audio geliefert wird, und Restore-Test einer Sicherung. [A:105–159; A:184–201; B:35–47; B:104–124]

**Zu korrigierende Altbeispiele:**

1. `find "$STEPS_DIR" -type f -exec sha256sum {} \; > ...` darf sein Ausgabeverzeichnis nicht unbewusst **im gescannten Stamm** anlegen: andernfalls entsteht ein sich selbst aktualisierender Bestand oder ein veränderter Hashsatz. Die genaue relative Pfadbasis muss fixiert sein.
2. `sort CSV | uniq` ist **kein zuverlässiger Duplikattest** für Datensätze; nach kanonischen Pfad-IDs und Inhaltshashes prüfen, unter Beachtung bewusst mehrfach referenzierter identischer Dateien.
3. Ein CSV-`find -printf` ohne korrektes Quoting/Encoding/Header kann bei Kommas, Newlines und Sonderzeichen in Pfaden fehlerhaft sein; besser `csv` aus Python verwenden.
4. Der in B dargestellte Ablauf `sha256sum archiv.zip > SHA256SUMS.txt; dann gegen SHA256SUMS.txt prüfen` beweist **keine Authentizität**: Der Prüfwert muss von einem **separat vertrauenswürdigen veröffentlichten Release-/Manifesthash** stammen.
5. `wget http://server/...` ist ein Platzhalter über **unverschlüsseltes HTTP**, kein geeignetes offizielles Verteilungs-/Integritätsmodell; HTTPS oder geprüfte sichere Ablage vorsehen.
6. Der erste MIDI-Python-Codeblock in A verwendet `msg.bytes()`: **Meta-Events können dabei Probleme verursachen**, und MIDI-Ticks sind ohne korrektes Tempo-/Auflösungsmodell noch keine Zeit in Sekunden. Für einen verlustarmen Import sämtliche Delta-/Absolute-Ticks, Track-Identität, Tempoevents, Controller, Meta- und Sysex-Daten und korrektes MIDI-Event-Encoding erfassen; nicht aus einem Demo-Snippet Produktionsreife ableiten.
7. Der zweite MIDI-Demoansatz in A akkumuliert `msg.time` und serialisiert `msg.dict()`; das ist für eine Ausgangsextraktion plausibler, benötigt aber ebenfalls Schema-/Round-trip-Tests, Time-Base und proprietäre Rechteprüfung.
8. `unzip -t` prüft Containerintegrität, aber weder gesetzlich erlaubte Weitergabe noch semantisch korrektes MIDI. Für Archive zusätzlich Path Traversal, Zip Bombs, Symlinks und Hash-/Größenlimits berücksichtigen.
9. Die V6.6-Formulierung „keine QA durchgeführt“ ist wegen B und C zu **„unterschiedliche QA-Ebenen; nicht gesamthaft nachgewiesen“** zu präzisieren.

## 9.4 Abnahmegates für Steps auf Glide-Basis

**Gate G0 — Scope-Freeze:** Steps-P1 vs P4/P5 und Drum-/Produktions-Roadmap explizit trennen; Produktsteckbrief signieren.

**Gate G1 — Glide-Baseline:** PR #71 oder andere gewählte Codebasis **auf einem tatsächlichen finalen Git-SHA** identifizieren; Pflichtmatrix Windows/Linux/Mac und Paketbeigaben grün oder dokumentiert begründete Plattformgrenze; frischen Klon gegen Archive prüfen.

**Gate G2 — Wissensquellen:** 20 Ausgangsquellen vollständig inventorisiert und mit Rights-Status versehen; nicht alle dürfen zwangsläufig in öffentliche Repo-Dateien kopiert werden. Originalhashes und bibliografische Qualität dokumentieren.

**Gate G3 — KB-Schemas:** Source Registry, Theory Taxonomy, Canonical Pitch/Chord/Progression Records und typed relations mit Schema-Validatoren, explizit erlaubter Mehrdeutigkeit.

**Gate G4 — Theory Engine:** 100+ fachliche Golden Tests, negative Beispiele, Deutsches H/B, V7/vi-Kontext und beliebige Tonarten/Modi, deterministisch offline.

**Gate G5 — App/Skill Integration:** Skill und UI liefern identische Ergebnisse aus **einer** Engine/KB; nativer UI-Lifecycle und Save/Load robust; Quellenbelege im Lernmodus sichtbar.

**Gate G6 — Audio/Delivery:** MIDI-/Audio-Rechte und Sound-Ausgabe plattformübergreifend validiert, CLI/GUI-Paket reproduzierbar, SHA-/SBOM-Beigaben, Neuinstallation/Release-Handover dokumentiert. Erst danach öffentliche Beta-Ankündigung.

Alle Gates sind **neu konsolidierte Vorschläge**, nicht bereits vereinbarte Freigaben.

---

# 10. Rechte, Lizenzierung und Open-Source-Governance

## 10.1 Unterschiedliche Rechteobjekte konsequent trennen

| Objekt | Denkbarer Lizenz-/Rechtestatus | Maßgabe |
|---|---|---|
| **Steps-Anwendungscode** | OSS gewünscht, konkrete Lizenz nicht bestätigt | bestehende Codeherkunft/Glide-Lizenz und Third-Party-Lizenzen prüfen; getrennten Lizenzbeschluss für Steps fassen |
| **Glide-Code, der übernommen wird** | die sechs Dokumente nennen eine vorhandene `LICENSE`-Datei, jedoch **nicht** deren vollständigen Wortlaut, ihren Geltungsbereich oder einen aktuellen Lizenzscan | File-Level-Copyleft-/Notice-/Modifikationspflichten und Komponentenrechte bei Wiederverwendung prüfen; nicht als frei von Verpflichtungen behandeln |
| **Eigene Steps-Knowledge-Base-Texte/Fixtures** | selbst geschaffen; geeignete Daten-/Content-Lizenz erst wählen | Code-, Daten-, Dokumentations- und Materiallizenzen getrennt festhalten |
| **Wissenschaftliche PDFs, Bücher** | CC BY, Open Access, proprietär, unbekannt je Werk | PDF-Vervielfältigung/Verbreitung nicht aus Zugriffsmöglichkeit ableiten |
| **Transkripte von Videos/Interviews** | teils proprietär, Rechte offen | Quellenangaben/Neuschöpfungen statt umfangreiche ungeklärte Übernahme |
| **Ableton-Artikel und Medien** | öffentlich lesbar, aber nicht automatisch frei weiterzugeben | Metadaten und eigene rechtmäßig erstellte Zusammenfassungen; Lizenz je Bild/Download |
| **Ableton Live Sets, Samples, Presets, Packs** | separate, teils bildungs-/privatnutzungsbezogene Beschränkungen | vor öffentlichem Import rechtlich einzeln freigeben |
| **PausePlayRepeat-MIDI/Audio** | Nutzereingang ohne Weitergaberecht-Prüfung | zunächst privat analysieren, nicht automatisch veröffentlichen |
| **Konkurrenzscreenshots, Grafiken, Logos, Chord Files** | fremde Rechte/Marken möglich | nur interne Inspiration mit dokumentierter Herkunft; eigene Gestaltung |
| **Kanonische Akkordfolgen** | abstrakte Akkordfolgen häufig nicht eigenständig geschützt; jedoch Werk-/Arrangement-/Aufnahme-Rechte je Einzelfall | keine pauschale Aussage „alles frei“; besonders wiedererkennbare Werke und Samples separat prüfen |

[D:68–74; B:94–102; E:60–87; E:543–554; E:875; F:138–175; C:148–157; C:209–293]

## 10.2 Widersprüchliche oder ungesicherte Lizenzvorschläge

D empfiehlt **MIT oder Apache-2.0** als permissive Lizenz und für freie Daten **CC0 oder CC BY**, E nennt Open Source, entscheidet aber keine konkrete neue Lizenz. B schlägt **CC BY-SA für Code** vor; CC-Lizenzen werden jedoch üblicherweise **nicht** als primäre Softwarecode-Lizenzen empfohlen. Der aus Glide bekannte MPL-2.0-Hintergrund muss zusätzlich berücksichtigt werden. **Es existiert in den sechs Dateien keine belastbar bestätigte einheitliche „Steps ist MIT/Apache/MPL/CC BY-SA“-Lizenzentscheidung.** Die konkrete Lizenz des tatsächlich übernommenen Glide-Codes muss anhand der `LICENSE`-Datei geprüft werden. Die Entscheidung gehört ins eigene ADR- und Lizenzregister, getrennt nach App, KB, Assets, Dokumentation und Beispielen. [D:68–74; D:194–208; B:100–102; E:45–58; C:209–273]

**Rechtefelder mindestens:** Original-URL, Verlag/Urheber, Datum, Medientyp, Lizenztext/Version/Quelle des Nachweises, kommerzielle Nutzung `YES|NO|UNKNOWN`, Weitergabe `YES|NO|UNKNOWN`, Bearbeitung/abgeleitete Texte erlaubt `YES|NO|UNKNOWN`, Attributionspflichten, User-uploaded oder Drittquelle, Prüfer, geprüft am, Hash, Verwendungszweck, Review-Status. `UNKNOWN` ist **kein** „erlaubt“. [E:702–748; F:162–175]

## 10.3 Privater Forschungsbestand und öffentlicher Export

**Private/Vault-Zone:** lokale Copyright-PDFs, Originaltranskripte, Packs/Live Sets, Screenshots, fremde Audio-/MIDI-Dateien mit unbekannter Lizenz; mit Manifest und Zugriffsschutz. **Öffentliche Zone:** originaler Steps-Code unter geklärter Lizenz, eigene Texte/Beispiele, verlinkte bibliografische Metadaten, selbst erstellte und rechtsgeprüfte Analysemodelle, freigegebene Drittassets mit Lizenz- und Attribution-Dateien. Ein „Free Download“ darf nicht unbesehen zu „Free Redistribution“ werden. [A:18–20; A:283–290; B:19–23; B:94–102; F:138–175]

**Open-Source-Community:** README auf Deutsch und Englisch, Beitragsschema via Fork/Branch/PR, Issues für Bugs/Features, CI, Conventional Commits als Vorschlag, Lizenzhinweise, klarer Maintainer und Roadmap. Vor externer Veröffentlichung Namen-/Markenkollision „Steps“, Namespace, Paketnamen, Third-Party Notices und Provider-URLs prüfen. [D:68–74; D:110–190]

---

# 11. Artefakte, Exporte und dokumentierte Lieferalternativen

## 11.1 Drei Paketzwecke – keine Dateinamen durcheinanderwerfen

| Artefakttyp | Nutzungszweck | In den Quellen auftretende Namen | Konsolidierte Behandlung |
|---|---|---|---|
| **I. Harmony-Research-Handover** | Quelleninventar, Modelle, SKILL-Entwurf, ADRs und Codex-Pläne | `Steps_Research_Foundation_v1.zip` | eigenes internes Forschungs-/Übergabepaket, keine produktive App |
| **II. Bibliotheks-/Produktionsarchiv V6.6** | vollständiger geprüfter Bestand der breiten Produktionsbibliothek | `STEPS_Bibliothek_V6.6.zip`, `STEPS_Packaged_V6.6.zip`, `STEPS_Project_20261109.zip` | nur nach Realinventar vereinheitlichen; ggf. getrennte private/public Editionen |
| **III. Produktrelease Steps** | tatsächlicher App-Code, Installer/Package, KB und freigegebene Daten | in D/E noch nicht fest benannt | erst nach Produkt- und Lizenzfreigabe versionieren; nicht V6.6 ungeprüft übernehmen |
| **IV. Glide-Archiv-/System-Template** | unveränderte historische Entwicklung, Reuse-Inventar, Stashes, Grafik-Master, Belege | laut C Sicherung E: / neuer lokaler Klon nach PR #71 | eigenes internes Langzeitarchiv; keine Vermischung mit öffentlichem Steps-Release |

## 11.2 Im V6.6-Bericht erwartete Lieferdateien

B/A nennen folgende **Soll-Artefakte**, nicht unabhängig nachgewiesene fertige Downloads: [A:138–180; B:19–23; B:49–60; B:137–146]

- Markdown-Quellbericht (bezeichnet als `STEPS_Report.md` oder Master Markdown), PDF-Datei `STEPS_Project_Report.pdf` bzw. `STEPS_Report.pdf`, Word-Datei `STEPS_Project_Report.docx` bzw. `STEPS_Report.docx`.
- ZIP mit fachlichen MD-/CSV-/JSON-/MusicXML-/Code-/zulässigen MIDI-Dateien; Arbeitsnamen `STEPS_Bibliothek_V6.6.zip`, `STEPS_Packaged_V6.6.zip` oder datierte Variante.
- `STEPS_Index.csv`/`STEPS_index.csv` (Name, Pfad, Größe, Datum, Hash, Versions-/Themenfelder), `STEPS_checksums.sha256`, `SHA256SUMS.txt`.
- `QUELLENREGISTER.md`, `LICENSE.txt`/NOTICES, etwaiges `STEPS_QUALITAET__...__AUDIT.md`, `Install_Instructions.md`, `Command_Scripts.txt`, README/Archiv-Inhaltsverzeichnis.
- Optionale Audio-/MIDI-Assets **nur wenn Rechte geklärt**; keine privaten DeSantis-PDFs, originalen Ableton-Kurspdfs, fremde Live Sets oder proprietäre Samples im Public ZIP.
- B gibt als Planungsgrößen ca. **3,8 MB** ZIP, **0,8 MB** PDF, **1,2 MB** DOCX an; an anderer Stelle stehen `X MB`/`Y MB`. Das sind Platzhalter/Schätzungen, **keine geprüften Dateigrößen**. [B:49–60; B:137–146]

## 11.3 Spezifischer Inhalt des Research-Handover aus E

Das konzeptionell beschriebene `Steps_Research_Foundation_v1.zip` soll enthalten: `00_README.md`, `01_PROJECT_REPORT.md`, `02_PROJECT_CONTEXT_HANDOVER.md`, `03_RESEARCH_BIBLIOGRAPHY.md`, `04_SOURCE_INVENTORY.csv`, `05_DECISION_REGISTER.md`, `06_RESEARCH_GAPS.md`, `07_ROADMAP.md`, außerdem `skill/SKILL_DRAFT.md`, `schemas/{source,concept,chord,progression}.schema.json`, `templates/{SOURCE_TEMPLATE,CONCEPT_TEMPLATE,ADR_TEMPLATE,CODEX_PROMPTS}.md`, `competitors/COMPETITOR_MATRIX.md` und `competitors/NOTES/`, `sources/README.md`, `sources/LOCAL_SOURCE_MANIFEST.yaml`. Original-PDFs **nur mit entsprechender Berechtigung**. [E:835–890]

## 11.4 Überprüfbare Herstellung und Bereitstellung

**Einheitlicher Releaseprozess:** Quelleninventar + statische Lizenz-/Copyrightfilter → schema-/inhaltliche QA → geschützte/private Assets separieren → reproduzierbaren Masterindex generieren → Formatexporte (falls beauftragt) → öffentliches oder internes ZIP erstellen → Container-/Inhalts-/Rechteprüfungen → SHA-256 mit Release-Manifest → isolierter Install-/Öffnen-Test → sicherer Link/Archivbeleg → Upgrade-/Restore-Hinweise und endgültiges Übergabeprotokoll. [A:105–159; A:184–201; B:35–47]

**Optionale Bereitstellungsalternativen aus B:** Browserdruck als PDF für einen Webbericht, Google Drive/Dropbox, SFTP/SSH/SCP oder als letzte Möglichkeit physisches Speichermedium. **FTP ohne sichere Übertragung nicht als Standard empfehlen.** Diese Methoden waren **Optionen**, nicht nachweislich bereits eingerichtete Kanäle. [B:126–135]

**Überprüfungsbefehle, plattformabhängig** (nur mit vorhandenem externen Referenzhash):

```bash
sha256sum -c SHA256SUMS.txt           # Linux; vom Releaseherausgeber stammende Manifestdatei
unzip -t STEPS_Project_RELEASE.zip    # Archivstruktur prüfen
unzip -l STEPS_Project_RELEASE.zip    # Inhalte nachvollziehen
```

```powershell
Get-FileHash .\STEPS_Project_RELEASE.zip -Algorithm SHA256
# Alternativ aus B: CertUtil -hashfile <datei> SHA256
# 7z l <datei> mit installiertem 7-Zip
```

**Rohskripte als historische Beispiele:** A verwendet `find`, `sha256sum`, `zip -r`, `pandoc`, ein `mido`-Python-Skript für Tick-/Eventdaten und einen Beispielpfad `$STEPS_DIR`. Diese Befehle sind **keine hier ausgeführten Tests**. Vor produktiver Codex-Ausführung sind Pfade, Manifest-Ausschlüsse, CSV-Quoting, MIDI-Metadaten und Rechtechecks wie in §9.3 zu korrigieren. [A:109–144; A:227–290]

---
# 12. Roadmaps und realistische Sequenzierung

## 12.1 Vier verschiedene historische Pläne, keine verbindliche Gesamttimeline

| Quelle / Plan | Originalplanung | Wesentliche Schritte | Status / Einordnung |
|---|---|---|---|
| **D: schneller Produkt-MVP** | Alpha v0.1 ca. **2–3 Wochen**, v0.2 **3–4 Wochen**, v0.3 **3–4 Wochen**; Gantt mit Dez. 2026–Frühjahr 2027 | Datenmodell/UI → Audio/Visualisierung/Übungsloop → Roman Numerals, Suggestions, MIDI/MusicXML | GUI-first; fachliche Quellen-/Golden-Test-Freigabe nicht als erster Gate integriert [D:76–108] |
| **E: Research-to-Product** | Startvorschlag **10.11.2026**, Entwicklung bis mindestens **Frühjahr/Sommer 2027** | Registry (14d), bibliografische Lizenzprüfung (10d), Theory Taxonomy (21d), Pitch/Chord/Relations/Progressionsmodelle, Golden/Corpus-Tests, Skill v0.2, Adapter/Explorer/Teaching; Style und Drums später | fachlich-strukturiert, **ausdrücklich nur Vorschlag** [E:621–659] |
| **B: Archiv-/Exportplan** | als **4–6 Wochen** bezeichnet; Phasentabelle rechnet **3 + 1 + 2 + 3 + 1 + 2 = 12 Arbeitstage**; Gantt etwa 10.–26.11.2026 | Dokumentfinalisierung, PDF/DOCX, Files, Lizenzen, ZIP/Hash, Review/Publish | **Dauerrechnung und Terminplan nicht konsistent**; archivorientiert, kein Produkt-MVP [B:62–92] |
| **A: Codex-Exportplan** | Gantt **09.–26.11.2026** mit einigen als `done`/`active` markierten Folgeschritten | Bestand, CSV, Ableton-Katalog, Ingestion, MIDI/ZIP, QA, Report, ZIP | als Momentaufnahme/Ideenplan behandeln; zukünftige `done`-Markierung ist ohne Beleg unzuverlässig [A:203–225] |
| **F: vier Wochen ab Freigabe** | Woche 1 Definition, 2 Rechte/Datenmodell, 3 Import/Suche, 4 Qualitäts-/Startentscheidung | zunächst **Ableton-Interviewdatenbank**, nicht explizit Steps-Harmony | nur relevant für P4; F warnt vor Produktgleichsetzung [F:244–321] |

**Mehr Details zu E, ohne Termine als fix zu deklarieren:**

- `Source Registry & Checksums` ab 10.11.2026 (14 Tage), `Bibliographic & License Audit` danach (10 Tage), `Theory Taxonomy v1` ab 17.11.2026 (21 Tage).
- `Canonical Pitch/Interval Model` ab 01.12.2026 (14 Tage); `Scale & Chord Knowledge` danach (18 Tage), `Harmony Relations` danach (21 Tage); `Progression Schema` ab 15.12.2026 (21 Tage).
- `Golden Theory Tests` ab 15.12.2026 (28 Tage), `Corpus Cross-Checks` danach (21 Tage).
- `Skill Prototype v0.2` ab 15.01.2027 (14 Tage), `Retrieval & Citation Tests` danach (14 Tage).
- `Theory Engine Adapter` ab 01.02.2027 (21 Tage), `Explorer Prototype` danach (28 Tage), `Learning Explanations` danach (21 Tage).
- `Style Expansion` ab 01.04.2027 (45 Tage), `Drum/Groove Research` erst danach (30 Tage). **Laufende Abhängigkeiten überschneiden sich im Gantt teilweise**, daher ist das nur ein Planungsmodell. [E:623–659]

**Frühere B-Termine:** Dokument 10.–12.11., Referenzprüfung nach Dokument, PDF/DOCX 16.11., Aggregation 17.–18.11., Rechteprüfung 19.–21.11., ZIP/Hash 24.11., Review/Deployment 25.–26.11. Die in B genannte 4–6-Wochen-Dauer deckt sich nicht mit diesem 17-Tage-Kalenderfenster. [B:62–92]

**A-Plan (ebenfalls Vorschlag):** Bestand 09.11. (`done`), Index 10.11. (`done`, damals Zukunft), Ableton-URLs ab 11.11. (`active`), Ingestion 14.–16.11., MIDI 17.–19.11., Ableton 20.–22.11., QA 23.–24.11., Report 25.11., ZIP 26.11.2026. **Kein `done` als realer Nachweis übernehmen.** [A:203–225]

## 12.2 Ein integrierter, empfohlener Arbeitsplan – Abhängigkeiten statt falscher Terminsicherheit

| Sequenz / Priorität | Arbeit | Ergebnis/Definition of Done | Abhängigkeit |
|---|---|---|---|
| **P0-A** | Scope-/Produktentscheidung, Akronym und Namensprüfung | signierter Steps-Steckbrief, P1–P5 freigegeben oder separat | keine |
| **P0-B** | Originaldaten vollständig verfügbar machen | tatsächliche Glide-/Steps-/V6.6-Bestände inkl. 20 PDFs, Ableton-CSVs, Code/QA und Grafik-/MIDI-Assets lesbar | sichere Bereitstellung |
| **P0-C** | Glide PR #71 und archivierte lokale Basis final prüfen | identifizierter finaler Git-SHA, einheitliche Pflichtmatrix, E:-Backup und Restore-Test, ggf. gemergter main | Repo + Logs + C:-/E:-Zugriff |
| **P0-D** | Lizenz-/Quellenfreigabe | Rechte- und Quellregister, öffentlich/privat-Zuordnung, Steps-Code-Lizenzentscheidung | P0-A/B |
| **P1** | Canonical Source Registry und Theory Taxonomy | 20 Quellen + Research-Erweiterungen mit Provenienz, Schema und offenen Rechtefällen | P0-B/D |
| **P2** | Canonical Pitch/Chord/Progression Engine + typed relations | definitionsgetestete Pure-Python-Domänenschicht | P1 |
| **P3** | Goldene Testmatrix und alternierende Frameworks | 100+ Tests, nachvollziehbare negative/ambivalente Fälle | P2 |
| **P4** | Fachskill und GUI-Adapter | eine gemeinsame Quelle für Skill, Engine und Tk-App; keine direkte Theorie in ListApp | P0-C, P2/P3 |
| **P5** | Playback, Editor, Theorie-Learning, Save/Load/Export | cross-platform lauffähiger Nutzerfluss, Round-trip und Lizenzabnahme | P4 |
| **P6** | Releases/Community/Erweiterungen | verifizierter Installer, OSS-Governance, dokumentierte Release-Gates | P5 |
| **Separate Spur** | Ableton-Interview- und vollständige Produktionsbibliothek | eigenständige Reconciliation und Entscheidung, ob/was in Steps übernommen wird | P0-A/B/D |

---

# 13. Decision Register – bewusste Trennung von Festlegung und Option

Die ID-Tabelle kombiniert die sechs in E vorgeschlagenen ADRs mit zusätzlichen Konflikt-/Produktentscheidungen. **„Belegt“** bedeutet nur, dass ein Dokument die Entscheidung ausdrücklich als Ziel oder Auftrag enthält, **nicht** dass die heute maßgebliche Projekt-Governance sie formell ratifiziert hat. [E:556–619; D:68–89; F:325–349; C:209–273]

| ID | Thema | Quelle / Alternativen | Status hier | Erforderliche Entscheidung |
|---|---|---|---|---|
| `DEC-001` | Was ist „Steps“? | D/E Harmony-App; A/B Produktionsbibliothek; F Interview-KB | **OFFEN – kritisch** | P1/P4/P5 offiziell trennen oder explizit verschmelzen |
| `DEC-002` | Markenname / Akronym | Steps; 2 widersprüchliche STEPS-Akronyme | **OFFEN** | offizieller Produktname, Schreibweise, Trademark/Repo prüfen |
| `DEC-003` | App-Kernnutzen | Explore/Explain/Educate statt bloßer Generator | **ZIELBILD – gut belegt** | als Produktmission freigeben |
| `DEC-004` | Drums/Groove im ersten MVP | E explizit deferred; A/B im breiten Archiv | **FÜR HARMONY-MVP ZURÜCKGESTELLT** | separate spätere Roadmap / Archivrolle klären |
| `ADR-001` | Knowledge Base außerhalb `SKILL.md` | E empfiehlt KB, Skill nur Retrieval/Workflow | **PROPOSED, hohe Priorität** | annehmen/Alternative dokumentieren |
| `ADR-002` | Canonical harmonic model | A eigener Core; B `music21`; C eigener Core + Adapter | **OPEN; C empfohlen** | Core-/Adapter-Schnittstellen und Testorakel festlegen |
| `ADR-003` | Harmonie als Graph | typed Relations vs lineare Tabellen; JSON/YAML statt Graph-DB zunächst | **PROPOSED** | Relationsschema und Traversal-API freigeben |
| `ADR-004` | Tkinter behalten | EXISTING/temporär vs PyQt/Kivy/Web | **VORLÄUFIG** | Tk-Baseline und Migrationskriterien festhalten |
| `ADR-005` | Drum Engine | E deferred | **DEFERRED** | kein aktueller Forschungs-/Implementierungsauftrag |
| `ADR-006` | Multiple Analyses | Interpretationspluralität nach Theorie/Stil | **PROPOSED** | Kanonisierung und UI für Widersprüche entwerfen |
| `DEC-005` | MIDI/Audio-Terminierung | D MVP früh; E fachlicher Start vor UI | **OFFEN** | MVP-Definition / Gate-Reihenfolge beschließen |
| `DEC-006` | Lizenz Steps-Code | MIT/Apache (D), CC BY-SA (B), Glide-Herkunft mit noch zu prüfender tatsächlicher Originallizenz | **OFFEN – rechtlich kritisch** | Eigentum/Reuse/Lizenzkompatibilität prüfen und beschließen |
| `DEC-007` | Lizenz von KB / Docs / Beispielen | CC0, CC BY u. a. vorgeschlagen | **OFFEN** | getrennte Lizenz- und Attribution-Dateien |
| `DEC-008` | Ableton-Inhalte | Hauptinhalt (F-Hypothese), Nebenarchiv, späteres Steps-Modul | **OFFEN** | Datensatz-/Feature-Verhältnis festlegen |
| `DEC-009` | Externe PDFs/Assets | privat vs öffentlich, Unbekannt/Restricted | **RECHTEPRÜFUNG PFLICHT** | konkrete Asset-Liste freigeben |
| `DEC-010` | Glide-Codebasis | PR #71 nach vollständig grünem Lauf und Merge auf `main` | **BEDINGT BEAUFTRAGT; noch nicht nachgewiesen** | finalen SHA/Merge und Prüfgrenzen belegen |
| `DEC-011` | Archive C:/E: | E: Archiv, C: später frischer Klon, alte Kopie erst nach Abnahme | **im Gespräch explizit festgelegt** | Restore + Git-/Hash-Vollprüfung dokumentieren |
| `DEC-012` | Glide-Module | nur generisch/adapterfähig direkt wiederverwenden | **VORSCHLAG mit technischer Evidenz** | pro Modul Katalogentscheidung |
| `DEC-013` | GUI-/Branding-System | Themes, Styles, Breakpoints, Logos, Anpassungen | **als Reuse-Wunsch belegt** | Steps-eigenes Designsystem definieren |
| `DEC-014` | Speicherformat Progressionen | lokal JSON/Text, später MusicXML/MIDI | **OFFEN** | Schema-Versionierung, Migration, Kompatibilität |
| `DEC-015` | KB-Speicher | YAML/JSON, ggf. SQLite/Graph | **OFFEN** | Ingestion-/Query-Anforderungen messen |
| `DEC-016` | Sprach-/Notationspolitik | Deutsch H/B, internationale B/Bb, englische Quellen | **fachlich notwendig; Definition offen** | kanonisches Parsing/UI-Display festlegen |
| `DEC-017` | Barrierefreiheit/Audio-Latenz | E/D und Glide-Reuse | **NACHWEIS OFFEN** | plattformübergreifende Akzeptanzkriterien |
| `DEC-018` | CI-/Freigabevertrag | 19-step local vs Multi-OS; native Tk/Tcl Assertions | **in C historisch bearbeitet** | aktuelle freigabefähige Matrix definieren |
| `DEC-019` | Öffentliche GitHub-Texte | keine Beta-/3.50-Werbung, Version technisch erhalten | **für Glide als Gesprächsauftrag belegt** | Regeln für Steps-README übernehmen oder neu entscheiden |
| `DEC-020` | CycloneDX-SBOM | 24 Komponenten/37 Mac-Lizenzbeigaben; Dependency-Graph fehlt | **TEILFERTIG IN GLIDE-BERICHT** | vollständigen Steps-Graph oder dokumentierte Restgrenze |
| `DEC-021` | Release-/ZIP-Konvention | mehrere Dateinamen und Paketzwecke | **OFFEN** | drei Artefaktklassen und eindeutige Namenskonvention |
| `DEC-022` | Projektreife/Start | F noch nicht freigegeben; D/E planen; C Glide-Tests offen | **KEIN GESAMT-STARTNACHWEIS** | formelle Produkt-/Technik-/Rechtefreigabe |
| `DEC-023` | Verantwortliche/Budget | F offen | **OFFEN** | Owner, fachlicher Reviewer, Lizenzreview, QA-Verantwortung und Mittel |
| `DEC-024` | Community & Monetarisierung | kostenlos/werbefrei, optionale Spenden, GitHub/Installer/PyPI | **ZIEL/OPTION** | Business-, Community- und Release-Policy |
| `DEC-025` | Performance-SLOs | historische Medianwerte ohne Baseline | **OFFEN** | messbare Ziele für Steps und Regressionstoleranzen |
| `DEC-026` | Archivbereinigung | Schutz historischer Belege, 4 Stashes, Grafik-Master | **SICHERUNG VOR LÖSCHUNG** | Löschfreigabe nur nach validiertem Inventar |

---
# 14. Widerspruchs-, Differenz- und Unschärferegister

**Bewertungscodes:** **H** = harter Widerspruch (gleiche Aussage/Grundgesamtheit nicht zugleich richtig); **K** = Kontext-/Versionsdifferenz oder verschiedene Bestände, nur scheinbarer Widerspruch; **U** = unbelegte/zu starke Aussage oder ungeklärter Sachverhalt; **T** = technischer/logischer Fehler in Plan, Beispiel oder Termin. Die Tabelle dokumentiert bewusst **auch falsche Konfliktheuristiken**, damit spätere Bereinigung nicht einzigartige Informationen löscht.

| ID | Typ / Priorität | Befund mit Quellstellen | Klärung, ohne Inhalte zu vernichten |
|---|---|---|---|
| **W-01** | **H – kritisch** | Name „STEPS“ wird als **Structured Technical Education in Production Systems** [A:3] und **STructured Electronic Production System** [B:3] ausgeschrieben; D/E verwenden Steps ohne Akronym. | Kein Akronym als offiziell ausgeben; Naming-/Brand-ADR nötig. |
| **W-02** | **H/K – kritisch** | A/B definieren STEPS als volle Musikproduktion [A:3–18; B:1–7], D/E als Harmony-/Akkord-App [D:1–7; E:3–29], F kennt keine bestätigte Steps-Definition [F:36–58]. | P1/P4/P5 separat dokumentieren; Zieldefinition aus D/E als bevorzugte **Hypothese** – Freigabe offen. |
| **W-03** | **H – kritisch** | A meldet **1.146** Dateien [A:24–26], die dortige Tabellensumme ist **1.306** [A:30–68], Schlusszeile behauptet **≈1.166** [A:70]. | Reales Manifest, definierte Scope-/Duplikatregeln, Hash-/Pfadzählung. |
| **W-04** | **T – mittel** | Das Mermaid-Coverage-Pie in A summiert sich auf nur **686** [A:74–84], wird aber als Coveragedarstellung der Gesamtbibliothek eingeführt. | Diagramm erst nach realer Manifestmessung neu erstellen; Überlappungen/Restkategorie klären. |
| **W-05** | **U – hoch** | B nennt **1.146 Dateien**, ca. **3,8 MB** und V6.6 als bestehenden konsistenten Bestand [B:13–27]. Keine Dateien/Hashes in diesem Auftrag. | Als berichtete, nicht unabhängige Bestandsdaten labeln. |
| **W-06** | **H/K – hoch** | B nennt 199 katalogisierte Ableton-Artikel [B:13–14; B:31], im Anhang 262 als finalen Katalog [B:149–156]; A nennt 262 und +63 in V6.6 [A:3–5]. | 199+63=262 ist plausible Versionsfolge; CSV-/Snapshottimestamps und kanonische URLs prüfen. |
| **W-07** | **K – mittel** | F: 28/143/123/609/34 [F:21–32; F:114–126], B: 169/199/462 [B:13–31], A: 262 [A:3–5]. | Unterschiedliche Grundgesamtheiten: Artist-Kandidaten, Archivartikel, Produktions-Tutorials; **nicht** automatisch addieren oder gegeneinander verrechnen. |
| **W-08** | **U – hoch** | A: QA/Audiotests/Lizenzen „noch zu tun“ [A:5; A:96–103], B: **36.538** Checks erfolgreich, Formate/MIDI/Links validiert [B:16; B:27]. | QA-Ebenen und konkrete Testliste/Hash unterscheiden; keine Gesamtabnahme ableiten. |
| **W-09** | **U – hoch** | A sagt „all source materials cross-referenced by checksum“ [A:20], fordert aber gerade das erstmalige Index-/Hashing [A:109–118]; B behauptet vorhandene Checksum-Indizes [B:13]. | Nur Dateien mit überprüfbarem SHA-Manifest als `verified` markieren. |
| **W-10** | **K/U – hoch** | B nennt MIDI-Mockups und eine geplante ZIP mit MIDI [B:13; B:19–23; B:55], gleichzeitig wurden lokale PausePlayRepeat-MIDI nie importiert [B:17; B:29]; A nimmt lokalen MIDI-/ZIP-Bestand nur an [A:5]. | Eigene Demo-Mockups, behauptete lokale Kurs-MIDIs und für Distribution lizenzierte MIDI unterscheiden. |
| **W-11** | **K – mittel** | A/B breite Drum-/Groove-Bibliothek [A:37; B:5–7], E Drum-Forschung **deferred** [E:29; E:607–611]. | Kein zwingender Konflikt, wenn breite Archivbestände von aktuellem Harmony-MVP getrennt bleiben. |
| **W-12** | **K/U – hoch** | B berichtet aus DeSantis-Kapiteln erstellte Übungen [B:15], E markiert `MakingMusic.pdf` als nicht zuverlässig parsed [E:84]. | Buchbibliografie, Übungen, Kapitelabdeckung und Original-Parsing separat belegen. |
| **W-13** | **H/U – hoch** | D empfiehlt **MIT/Apache 2.0** für Steps [D:68–74], B schlägt **CC BY-SA für Code** vor [B:100–102], die Lizenz der aus Glide übernommenen Bestandteile ist ebenfalls zu berücksichtigen; E entscheidet nur OSS-Richtung [E:45–58]. | Eigener rechtsgeprüfter Code-/Daten-/Docs-Lizenzbeschluss; CC-Codeempfehlung nicht übernehmen. |
| **W-14** | **U – hoch** | D: „Akkordfolgen nicht urheberrechtlich geschützt“ [D:70; D:204] ist zu pauschal, wenn konkrete Werke/Arrangements/Recordings vorliegen. | Unterscheidung abstrakte Harmoniefolge vs geschützte konkrete Ausdrucksform/Materialien. |
| **W-15** | **H/U – kritisch** | F behauptet mangels eigenem Kontext, Produktfunktion/Plattform seien unbekannt [F:40–50]; D/E bieten eine ziemlich konkrete App-Definition [D:4–7; E:33–58]. | F als **kontextbeschränkten Parallelbericht**, nicht als Beweis fehlender Produktidee verwenden; formale Freigabe trotzdem offen. |
| **W-16** | **H/K – mittel** | D plant UI-first v0.1 mit späteren erweiterten Theorie-Features [D:76–89]; E fordert Source→Taxonomy→Core→Tests **vor** GUI [E:25–29; E:661–670]. | fachliche Fundament-Gates vor nutzerseitigem Feature-Release priorisieren. |
| **W-17** | **T – hoch** | E erklärt `E7 → Am` pauschal als Secondary Dominant [E:39]; E selbst verwendet `E7` in C-Dur als V7/vi [E:469–471; E:684], während in a-Moll E7 die Dominante ist. | Tonart und Rahmen verpflichtend; Beispieltext fachlich präzisieren, nicht kanonische Relation verlieren. |
| **W-18** | **U – mittel** | D stellt Chord Files teilweise als statisch/analog dar [D:4–7], E beschreibt neue dynamische Progression-/Analyse-/Transpositionsversionen [E:15; E:247–251]. | Version/Format je Chord-Files-Produkt differenzieren; Marktpositionierung nicht auf veralteter Annahme bauen. |
| **W-19** | **T – mittel** | In D steht Hookpad bei **US$8/Monat** [D:21] und **US$7,99/Monat** [D:46]; außerdem „0+ songs“ [D:42]. | nur als ungeprüfte historische Preise, „0+“ ist offensichtlich keine nutzbare Nachfragezahl. |
| **W-20** | **T – mittel** | D-Gantt markiert Dezember 2026/Januar 2027 schon als `done` [D:91–106], während Dokumentstand 09.11.2026. A-Gantt markiert den 10.11. als `done` [A:211–214]. | Planstatus von tatsächlichen Logs trennen; rückwirkend nicht „erledigt“ übernehmen. |
| **W-21** | **H/T – hoch** | B beansprucht **4–6 Wochen**, addiert aber 12 Arbeitstage und legt Termine grob 10.–26.11. fest [B:62–92]. | abgestimmte Aufwandsschätzung nach Dependencies; keine präzise Endfrist vorspiegeln. |
| **W-22** | **K – mittel** | A exportiert `STEPS_Project_20261109.zip`, B `STEPS_Bibliothek_V6.6.zip` / `STEPS_Packaged_V6.6.zip`, E ein Research-Handover. [A:138–180; B:19–23; B:44; E:835–890] | nach Pakettyp standardisieren, nicht als ein identisches vorliegendes Artefakt behandeln. |
| **W-23** | **U – hoch** | B spricht von fertigem „unified ZIP“ [B:19–23], derselbe Text beschreibt Herstellung/Upload als zukünftige Schritte [B:35–47] und Downloadlinks nur als Platzhalter [B:158]. | `planned`, `created`, `verified`, `published` als getrennte Artefaktstatus. |
| **W-24** | **H/U – mittel** | A nennt keine `07–15`-Ordner in seiner „Top-Level“-Tabelle [A:30–68], B referenziert `10_QUELLEN_LIZENZEN` und `12_CODEX_AUFTRAEGE` [B:14–16]. | realen Tree inventarisieren, fehlende Zeilen ergänzen und Zählung neuberechnen. |
| **W-25** | **U – mittel** | E nennt **20** lokale PDFs/TXTs und einen ersten `SKILL.md`-Entwurf [E:9; E:60–87], aber keine dieser Originaldateien ist unter den sechs Uploads. | benannte Quellen **nur als bibliografische Hinweise** mit Verifikationsflag. |
| **W-26** | **U – hoch** | C meldet 20 zusätzliche Glide-Systemfähigkeiten [C:130], das eigentliche Feature-Inventar ist nicht beigefügt; C gibt ListApp mit 1.863 Methoden an [C:83]. | Reuse nach Code-/Modulabhängigkeitsanalyse, 20 Punkte nicht erfinden. |
| **W-27** | **K – hoch** | In C gibt es zahlreiche grüne Teilprüfungen, aber spätester Status: Linux Vollprüfungen grün, Mac nur Zieltests grün, Windows noch ohne Abschluss [C:616–648]. | keine Gesamtfreigabe/PR-Merge behaupten; Commit-spezifischen Release-Gate führen. |
| **W-28** | **K – mittel** | C nennt lokales Inventar **35.381 Dateien / ~7,9 GiB** [C:282], später Backup **35.380 / ~8,28 GB** [C:405]. | Messzeitpunkt, Einheiten, Filter, bereinigter Logo-Rest und neue Dateien unterscheiden; kein direkter Fehlernachweis. |
| **W-29** | **K – mittel** | Mac-Höhe **700** vs **954** Punkte zu Soll 960 [C:130; C:447], später Toast-Timing [C:561–597]. | verschiedene Fehlerstände und Ursachen; nicht in einen einzigen „Mac-Fix“ zusammenfassen. |
| **W-30** | **K – mittel** | Früh beschädigtes Git-Objekt war nicht nachladbar [C:416], später als Commit identifiziert und wiederbeschafft [C:436]. | neuerer Befund supersediert die pauschale Objekt-Fehlermeldung; weitere Integritätsprüfung offen. |
| **W-31** | **T – mittel** | Alte Skripte erzeugen eigene SHA-Datei und vergleichen sie dann mit derselben Datei [B:108–121], teils `find`-Index im gescannten Bestand [A:231–248]. | externe Checksum-Referenz/manifestierte Pfad-Basis und sichere CSV-Erzeugung. |
| **W-32** | **U – mittel** | B schreibt pauschal von einem Ableton-Live-EULA-Verbot kommerzieller Demo-Projekt-Nutzung [B:100], F nennt assetbezogene Bedingungen [F:138–175]. | allgemeine EULA-Aussage nicht ungeprüft auf alle Downloadassets verallgemeinern. |
| **W-33** | **K – mittel** | E Source-Example hat Neal `reviewed: false` [E:388–391], Concept-Example `status: reviewed` [E:455]. | keine Kollision: zwei unterschiedliche Objekttypen; dennoch Reviews unabhängig protokollieren. |
| **W-34** | **U – hoch** | B/A sprechen von Komplettheit der V6.6-Bibliothek [A:5; B:27], nennen aber zugleich MIDI-/Audio-/Lizenz-/Referenz-/Bloglücken [A:88–103; B:25–33]. | höchstens **Struktur-/Themenabdeckung laut Bericht**, nicht fachlich/operativ vollständiges Release. |
| **W-35** | **U – mittel** | C meldet CycloneDX mit 24 Komponenten und 37 Lizenzbeigaben [C:284], aber vollständiger Dependency-Graph fehlt [C:148]. | SBOM als partiell und plattformspezifisch markieren. |
| **W-36** | **K – mittel** | B spricht von „nur Metadaten“ zu Drittassets [B:33], A/B nennen eigene derived notes, exercises, Textlektionen [A:15–20; B:15–16]. | Metadaten von **Drittassets** und eigene **abgeleitete Lerninhalte** getrennt inventarisieren. |
| **W-37** | **U – mittel** | Der Inhalt in E nutzt historische, außerhalb der Uploads nicht auflösbare `filecite`- und `search`-Marker [E:9–23; E:64–85]. | alle bibliografischen und Marktaussagen für ein neues Quellenregister erneut nachweisen. |
| **W-38** | **K – mittel** | F dokumentiert persönlichen/private Nutzungskontext [F:78–92]; D plant kostenlose öffentliche OSS-App [D:4–7; D:48–50]. | private Forschungsablage und spätere Public App **trennen**; kein Automatismus für öffentliches Weitergaberecht. |
| **W-39** | **U – mittel** | A nennt die breite Bibliothek einschließlich aktueller V6.x und historischer Backups als „alle Dateien“ [A:11–15], fordert aber Entfernen von Temp-/Workfiles [A:198–199] und Rechteausschluss [A:20]. | Vollständigkeitsdefinition: **alle zulässigen, freigegebenen, eindeutig manifestierten Artefakte** – nicht jedes lokale Original im öffentlichen ZIP. |
| **W-40** | **K/U – mittel** | D enthält lokale `C:\Users\…`-Klonbefehle und `pip install tkinter` [D:150–166]; C verlangt frische Kopie erst nach grünem PR-Merge [C:248–273]. | D-Onboarding ist generisches, teils technisch zu korrigierendes Beispiel; C-Reihenfolge für diesen konkreten Reuse-Plan vorrangig. |

**Interpretation:** Mindestens **7 substantielle harte bzw. methodische Kernkonflikte** verlangen eine explizite Entscheidung oder neue Evidenz: Produktidentität, Dateizahlen, Ableton-Snapshots, QA-Status, Lizenzierung, Roadmap-Dauer und Releasefreigabe. Alle 40 registrierten Punkte bleiben nachvollziehbar, auch wenn einige nur **abweichende Kontexte** statt falsche Aussagen betreffen.

---

# 15. Lücken- und Nachweisregister – konkrete offene Arbeit

Prioritäten: **P0 blockierend**, **P1 für verlässlichen Projektstart notwendig**, **P2 nachrangig/Erweiterung**. Ein „Owner“ bezeichnet hier eine **empfohlene Rolle**, keine bereits zugewiesene Person.

| Gap-ID | Priorität | Fehlende Grundlage / noch nicht nachgewiesen | Prüfschritt und Abnahmekriterium | Zuständigkeitsrolle |
|---|---|---|---|---|
| G-01 | **P0** | Freigegebener Steps-Produktsteckbrief; Trennung P1–P5 | Zielgruppe, Kernnutzen, Nicht-Ziele, Produktname, Releaseumfang schriftlich beschließen | Product Owner |
| G-02 | **P0** | Vollständige Originale der sechs Dokumente allein reichen nicht für echtes Dateirepo | tatsächliche Repos, V6.6-ZIPs, CSVs, 20 PDFs/TXTs, Audio/MIDI, Screenshots und Artefaktlisten sicher bereitstellen | Project Owner / Archiv |
| G-03 | **P0** | finaler Status/Commit/Merge von PR #71 | GitHub-PR/Merge-SHA und letzte Windows/Linux/Mac-Pflichtmatrix prüfen | Engineering/QA |
| G-04 | **P0** | archivierter C:-/E:-Stand, Git-Objekte, Stashes/Restore abschließend bestätigt | Quell-/Zielhashs, separate Git-FSCK-/Merge-/Restore-Probe und Bereinigungsfreigabe | Engineering/Archiv |
| G-05 | **P0** | Steps-Softwarelizenz und Glide-Code-Übernahmerechte | Codeherkunft und Lizenzen inkl. File Notices, neue LICENSE-Policy | Recht/Owner |
| G-06 | **P0** | Publikationsrechte für PDFs, Blogartikel, MIDI/Samples/Artwork | rights manifest für alle Release-Assets, `UNKNOWN` bleibt ausgeschlossen | Recht/Content |
| G-07 | **P1** | eindeutige V6.6-Dateizählung und fehlende 07–15-Ordner | Dateisystemscan mit Pfaden, Größen, Hashes, Filter-/Archivvarianten und Summenkontrolle | Daten/QA |
| G-08 | **P1** | echte Snapshots der 199/262/462 Ableton-Kataloge | CSV-Import, URL-Normalisierung, Quellen-/Sprachen-/Versionsabgleich mit Diffbericht | Research/Data |
| G-09 | **P1** | echte Daten der 28/143/609/123-Artist-Auswertung | Kategorisierung, Language-Pairs und Validierung jeder URL | Research/Data |
| G-10 | **P1** | 169 „verified pages“ technisch definieren | Status/HTTP, Content Hash, Aktualität, manuelle Inhaltsprüfung getrennt ausweisen | Research/QA |
| G-11 | **P1** | 20 lokale Ausgangsquellen nur referenziert | Scan mit SHA-256, Bibliografie, Verlag/Ausgabe, Parse-/OCR-/Review-Status | Research/Archiv |
| G-12 | **P1** | erster `SKILL.md`-Entwurf nicht selbst einsehbar | Original sichten und auf KB/Source-Policy prüfen; Regeln erhalten | Skill/Research |
| G-13 | **P1** | Theory Taxonomy und fachlicher Canonical Core nicht gebaut/nachgewiesen | definierte IDs, Spelling-/Pitch-/Roman-Logik, public API und Schematests | Theory Engineering |
| G-14 | **P1** | fehlendes Golden Corpus, keine prüfbaren Entscheidungen zur Mehrdeutigkeit | ≥100 deterministische Cases inkl. Gegenbeispiele und Frameworks | Theory/QA |
| G-15 | **P1** | fehlende Relation Schema/API, unkalibrierte Confidence | typed edges, style scope, provenance, Testoracle, klare Anzeige | Theory/Research |
| G-16 | **P1** | unvollständige wissenschaftliche Abdeckung | Voice Leading, Jazz, Popular Harmony, Tonnetz, Notation und Corpora nach Primärbelegen ergänzen | Research |
| G-17 | **P1** | reale Glide-Modul-/Featureübersicht mit 20 Systemfähigkeiten fehlt | Modulmatrix mit Pfad, API, Abhängigkeit, Stand, Tests und Steps-Adapter | Engineering |
| G-18 | **P1** | Last-/Performancebaseline für Steps fehlt | deterministische Benchmarks für 1k/10k Progressions/Nodes; Ziele/Quantile | Engineering/QA |
| G-19 | **P1** | Mac-Geometrie-, Toast- und Callback-Regressionen erst teilweise geschlossen | native Pflichtmatrix auf **genau einem SHA**, rote Fälle sichtbar | UI/QA |
| G-20 | **P1** | aktueller vollständiger SBOM-Dependency-Graph fehlt | transitive Dependencies und Lizenzen/Hashes aus Build reproduzierbar | Build/Security |
| G-21 | **P1** | MIDI-/MusicXML-Formate nicht spezifiziert | Events, Tempo/Ticks, Meta/Controller, Round-trip, Schemas, Rechte prüfen | Audio/Data |
| G-22 | **P1** | keine echte Cross-Platform-Audio- und UX-Abnahme | Latenz/Metronom/Soundbank/Barrierefreiheit pro OS testen | Audio/UI QA |
| G-23 | **P1** | keinerlei bestätigter Release-/ZIP-Endbestand und sichere öffentliche Links | manuell und automatisiert prüfbarer Release-Lauf mit Manifest/Hashes/Restore | Release/Archiv |
| G-24 | **P1** | Reports enthalten Platzhalter, unrenderte Mermaid-Gantts, widersprüchliche Dateinamen | Master Markdown → bei Bedarf PDF/DOCX visuell geprüft; eindeutige Release-IDs | Documentation |
| G-25 | **P1** | konkrete Zuständigkeiten, Budget und offizielle Startfreigabe fehlen | RACI, Ressourcen-/Risiko- und Abnahmeprotokoll | Product Owner |
| G-26 | **P1** | externe Marktdaten/Preise/Ratings teils fehlerhaft bzw. veraltet | neue Primärquellen/Zeitstempel/vergleichbare Preisangaben | Product Research |
| G-27 | **P1** | gesicherte Provenienz des Grafik-Masters, Screenshots und Inspirationsmaterial | Copyright und Verwendungsstatus je Datei, interne vs öffentliche Nutzung | Design/Legal |
| G-28 | **P1** | Datenmigrations-/Dateischema-Versionierung offen | lokale Save/Load Round-trip-Fixtures, Backups und negative Migrationstests | Engineering/Data |
| G-29 | **P2** | Option Mobil/Web und alternative UI-Stacks nicht evaluiert | Nutzer-/UX-/Packaging-Anforderungen vor Framework-Wechsel | Product/Tech |
| G-30 | **P2** | kulturell/geografisch diverse bzw. non-Western Referenzen fehlen | kuratierten Source-Plan zur Diversifizierung erstellen | Research |
| G-31 | **P2** | Vollständigkeit Ableton-Archiv inkl. „One Thing“, älterer Sprachseiten, Podcasts/Videos | nach legalem Crawl und definierter Scope-Policy inkrementell erweitern | Research |
| G-32 | **P2** | umfangreiche Drum-/Genre-, Recording-, Spatial- und Distribution-Module | als separate Roadmap oder eigene Archivedition priorisieren | Product/Research |
| G-33 | **P2** | Community-/Finanzierungsmodell, GitHub Pages, PyPI/Installer-Kanal offen | nach MVP-Validierung externe Release- und Contribution-Strategie festlegen | Product/Community |
| G-34 | **P2** | semantische Suche in der Ableton-Research-KB fehlt | realen Suchbedarf nach Artist/Topic/Source validieren, erst dann DB-/RAG-Ausbau | Research/Engineering |

**Empfohlener nächster belastbarer Status:** „**Research-/Projektvorbereitung konsolidiert; fachliche Produktdefinition und technische Übernahmelinie noch nicht formal freigegeben; originäre Daten und Integritäts-/Lizenznachweise ausstehend**“. Weder „Steps vollständig entwickelt“ noch „V6.6 komplett geprüft“ noch „Glide-Basis freigegeben“ wird durch die hier vorgelegten sechs Markdown-Dateien allein bewiesen.

---
# 16. Wiederverwendbare Templates und konkrete Codex-Aufträge

Die **vollständig originalgetreuen Markdown-/YAML-/JSON-/Python-/Shell-/Mermaid-Beispiele** sind in der separaten Datei **`Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md`** mit Ausgangsdokument, Zeilennummern und Codeblock-Hash dokumentiert. Der Anhang enthält die **39 unterschiedlichen** in den sechs Quellen vorhandenen Codeblöcke, darunter mehrere historische Gantts sowie die beiden unterschiedlichen MIDI-Demos. Dies verhindert, dass technische Details stillschweigend wegfallen, ohne sie in der eigentlichen Overview mehrfach abzudrucken.

## 16.1 Source-Intake – vorgeschriebene Felder aus E

Der in E bereitgestellte `Source Record` soll enthalten:

- **Identity:** ID, Titel, Autor(en), Jahr, Verlag/Institution, DOI, URL.
- **Local:** Dateipfad, SHA-256, Importdatum, Parser.
- **Rights:** Copyright, Lizenz, `Redistribution allowed`, `Derived-text allowed`, Status `VERIFIED|UNKNOWN|RESTRICTED`.
- **Classification:** Source Type, Theory Areas, Style Contexts, Evidence Quality.
- **Extraction:** Parsed, Reviewed, relevante Kapitel/Seiten.
- **Claims:** Claim, Confidence, Concept IDs.
- **Notes:** Konflikte, offene Fragen.

**Sinnvolle Ergänzungen aus F und hier:** Original-URL/Canonical URL, Language/Translation Group, Download-Asset, tatsächlicher Rechtebeleg, Last Checked, Nutzerupload/extern, Versions-/Editionsidentität, tatsächliche Dateihash-Klassifikation. [E:702–748; F:162–175]

## 16.2 Concept Template aus E

Das Konzeptbeispiel `harmony.modal_interchange` mit Aliases `borrowed chords` und `modal borrowing` enthält: **Definition**, Preconditions, Canonical Examples, Alternative Interpretations, Style Scope, Computational Representation, UI Representation, Common Misconceptions, Tests und Sources; initial `status: draft`. Damit werden fachliche Erklärungen, Code, Test und UI aus demselben strukturierten Ursprung gespeist. [E:750–782]

## 16.3 Zwei Codex-Agent-Aufträge aus E

**Ingestion-Agent:** eine vom Nutzer bereitgestellte Quelle in rückverfolgbares Wissen überführen, Originalmetadaten bewahren, Autor/Jahr/Rechte/Seiten nie erfinden, Claim von Interpretation trennen, bestehende Concept IDs benutzen, neue IDs vorschlagen, Widersprüche melden, nur bei expliziten Regeln Tests generieren, keine längeren proprietären Textpassagen kopieren. **Output:** Source Record, Concept-Kandidaten, Claims, ungeklärte Fragen, Konflikte, Testkandidaten. [E:784–811]

**Concept Review-Agent:** für eine `concept_id` alle registrierten Quellen vergleichen und Consensus, Theoriedifferenzen, Stilgeltung, Edge Cases, Beispiele und Gegenbeispiele, computational model, Tests und Confidence liefern; **keine** echten Interpretationskonflikte löschen oder stilistische Häufigkeiten zu Universalgesetzen erheben. [E:813–833]

## 16.4 Vorrangige konkrete Codex-Arbeitsaufträge (VORSCHLAG)

1. **Inventur (read-only):** alle hier nicht vorliegenden Repos, ZIPs, Source-PDFs, Asset-Ordner, Ableton-Register, Glide-Modul- und QA-Dokumente auflisten, SHA-256 und Lizenz-/Statusmetadaten erheben; **keine** automatische Bereinigung.
2. **Conflict Reconciliation:** `W-01`–`W-40` gegen die echten Primärartefakte prüfen, jede Entscheidung über ADR oder ausstehende Frage dokumentieren. Kein „plausibler“ Stand wird allein durch höheres Datum zum Beweis.
3. **Glide-Preservation:** `main`, PR #71, C:/E:-Archive und Git-Historie abgleichen; pro Test Commit, OS, Python/Tk, Zeitstempel, Status und Rohlogs sichern; nach formeller Freigabe Steps-Abzweigung vorbereiten.
4. **Source Registry:** die 20 lokalen Harmony-Quellen und separat alle Ableton-Kataloge ingestieren; `UNKNOWN`-Rechte bei der öffentlichen Paketierung sperren.
5. **Harmony Core:** Pitch/Spelling, Intervall, Scale/Mode, Chord, Progression, Analysis/Relation mit stabilen APIs und mindestens 100 Golden Tests, mehrdeutige Interpretationen einschließen.
6. **Skill/UI-Adapter:** vorhandenen `SKILL.md`-Entwurf und Glide-Systemfunktionen ohne redundante Regel-/Datenhaltung verknüpfen; Testmatrix mit Windows/Linux/Mac und Theme-/Fenster-/Lifecycle-Prüfungen übernehmen.
7. **Delivery Audit:** README/AGENTS/CONTRIBUTING, License/Notices, SBOM, README-Versionverweis, reproduzierbares Packaging, Hash-/Restore-Checks und sicheres Release-Manifest.

---

# 17. Dokumentenabdeckung und Quellenrückverfolgung

## 17.1 Quellenvollständigkeit auf Ebene der gelieferten Dokumente

| Original | Vollständig gelesen? | In dieser Overview konsolidierte einzigartige Bereiche | Besonderer Erhalt |
|---|---|---|---|
| **A – STEPS Project Export** | **Ja**, 297 Zeilen | Bibliotheksarchitektur; 37 Ordner/Dateizahlen; Ableton 262; MIDI/ZIP/Codex; Lizenz, Qualität, Gantt, Export, Standards | konkrete Skripte und Diagramme im technischen Anhang; Zahlenkonflikt W-03 |
| **B – Projekt Overview** | **Ja**, 159 Zeilen | V6.6-Behauptungen, 199/169/462/262; 36.538 Tests, Reporting/ZIP, Zeitplan, Download- und Rechteoptionen | eigene Prüf-/Lieferhistorie und Kennzahlen getrennt dokumentiert |
| **C – Glide Kontext für Fable(2)** | **Ja**, 659 Zeilen | Reuse-Anforderungen, alle dokumentierten Commit-/QA-/Performance-/Mac/Windows/Linux-Stände, lokale Archivierung, Grafik-Master, Stashes, Steps-Audio | Stand und **nicht** erreichte Endfreigabe klar getrennt; Sachinformationen aus Zwischenmeldungen konserviert |
| **D – Project Definition & Positioning** | **Ja**, 221 Zeilen | Harmony-Produkt, komplette Konkurrentenlandschaft, Pricing, Personas, Tech-Stack, frühes MVP, OSS-/GitHub-Start | Marktbehauptungen und Demo-Vorschläge als verifikationsbedürftig markiert |
| **E – Forschungs- und Projektgrundlage** | **Ja**, 900 Zeilen | 20 PDFs/TXTs, sämtliche Theorie-/Style-Familien, Provenienz, KB/Repos, YAML-/JSON-Schemas, 6 ADRs, Phasenplan, Golden Tests, Codex-Vorlagen | alle Originalvorlagen und die langen Schemabeispiele im technischen Anhang |
| **F – Projektstatus-/Projektstartbericht** | **Ja**, 376 Zeilen | Ableton-Interview-Research mit 28/143/609/123/34; Quellen und Rechte, Datenformate, Startgates, Ressourcen/Entscheidungen | ausdrücklich dokumentierte Unsicherheit der Ableton↔Steps-Zuordnung bleibt erhalten |

**Gesamt:** **2.612 Zeilen** Originaldokumente (einschließlich Leerzeilen, Logs, Tabellen und Codeblöcken). Die sechs Originaldateien sind im gesonderten Quellarchiv **unverändert** beigefügt; die konsolidierte Overview ersetzt die inhaltlichen Wiederholungen, nicht die revisionssichere Aufbewahrung der Eingänge. Für die methodische Abschnittszuordnung liegt zusätzlich `Steps_Quellenabdeckung_2026-11-09.csv` bei.

## 17.2 Referenzstellen der Quellberichte

**A:** [A:1–20] Definition/Sources; [A:24–86] Struktur und Zählung; [A:88–103] Gaps; [A:105–159] Codex; [A:163–201] Archiv/QA; [A:203–296] Zeitplan/Skripte/Grenzen.  
**B:** [B:1–33] Scope/Status/Zahlen; [B:35–60] Herstellung; [B:62–92] Plan; [B:94–124] Lizenzen/Verifikation; [B:126–158] alternative Bereitstellung, historische Entscheidungen.  
**C:** [C:1–208] Glide-System, UI/CI/Packaging, Benchmarks; [C:209–355] Archiv/Backup/PR; [C:358–454] weitere Reparaturen; [C:455–648] Fokussierung auf Regressionen, aktueller PR-Status; [C:659] Gesprächsende durch Nutzungslimit, **kein technischer Abschlussbeleg**.  
**D:** [D:1–7] Positionierung; [D:9–50] Wettbewerb/Markt; [D:52–74] Technik/Rechte; [D:76–108] MVP; [D:110–190] Repo/Start; [D:194–220] deutschsprachige Wiederholung, inhaltlich integriert.  
**E:** [E:1–87] Mission/20 Quellen; [E:89–232] Theorie; [E:234–285] Inspiration; [E:287–525] KB/Schemas/Ingestion; [E:527–619] Gaps/ADRs; [E:621–900] Roadmap, Golden Tests, Vorlagen, Übergabe.  
**F:** [F:1–58] Status/Begriffsgrenze; [F:62–126] Recherche; [F:128–175] Beispiele/Rechte; [F:179–240] Technischer Stand/Risiken; [F:244–349] Phasen/Entscheidungen; [F:353–376] Quellen/Grenzen.

## 17.3 Zusätzliche in den Quellen genannte Referenzportale

- [Ableton Künstlerarchiv](https://www.ableton.com/en/blog/categories/artists/)
- [Ableton Downloadarchiv](https://www.ableton.com/en/blog/categories/downloads/)
- [Ableton EULA](https://www.ableton.com/en/eula/)
- [Ableton robots.txt](https://www.ableton.com/robots.txt)
- [Glide-to-do](https://github.com/n05a-design/glide-to-do) – laut D/C technischer Ausgangskontext; **in diesem Dokumentenaudit nicht live untersucht**.

Die einzelnen Produkt-/Marktlinks stehen bereits an den betreffenden Wettbewerbern in §6, die zehn Ableton-Beispiellinks in §4, die akademischen DOI-/Source-Belege in §3. **Nicht überprüfte externe Verweise bleiben ein Arbeitspunkt.** Die aus E übernommenen historischen KI-Zitatmarker werden als nicht selbständig verifizierbar behandelt und sind keine vollwertige wissenschaftliche Zitierung dieses Projektreports.

## 17.4 Deduplizierungs- und Verlustvermeidungsregeln

- **Wiederholte Claims** in D (Englisch + deutsche Zusammenfassung), A/B (ähnliche Exportaufträge) und C (fortlaufende Statusmeldungen) erscheinen in der Overview **einmal in ihrer maßgeblichen Sachrubrik**.
- **Verschiedene Aussagen zum selben Aspekt** (Dateizahlen, Katalogstände, Lizenzen, Tests, Zeitpläne, Begriffe) werden **nebeneinander** als Varianten/Konflikt erhalten, nicht zu einem unbelegten Mittelwert vereinigt.
- **Einzigartige Detaildaten** wie DOI, Quellenstatus, Mac-Abbruchursachen, konkrete Counts, 21 umsortierte Audioquellen, 4 Stashes, 91 Grafikdateien, 20 technische Glide-Fähigkeiten oder alte ZIP-Namen bleiben erhalten.
- **Skripte, Baumstrukturen und Beispielschemata** sind verlustarm in den **technischen Anhang** ausgelagert – nicht vom Projektwissen abgeschnitten.
- **Originaldokumente** werden **bytegetreu** in einem Quellarchivelement mit SHA-256 geführt, damit jede spätere Interpretation überprüfbar bleibt.
- **Unbelegte Tatsachenbehauptungen** werden **nicht gelöscht**, sondern als unbestätigter Projektkontext oder fehlender Nachweis beschrieben.
- **Nicht-sachliche Gesprächsmetadaten** wie „Ran command“, Nutzungswarnungen und Leerzeilen aus C bleiben nur im unveränderten Original erhalten, weil sie keinen eigenständigen fachlichen Projektinhalt besitzen.

---

# 18. Schlussbewertung und verbindlicher nächster Gate

**Konsolidierte Arbeitsdefinition:** Steps soll eine unabhängige, modulare Harmony-/Chord-Progression-Anwendung mit nachvollziehbarer, mehrfach interpretierbarer Music-Theory Knowledge Base werden; Glide ist die potenzielle technische Systemgrundlage, nicht die fachliche Wissensquelle. Die umfangreiche Produktionsbibliothek und die Ableton-Interviews werden als **zusätzliche, erst zuzuordnende Recherche-/Archivbestände** behandelt. [D:1–7; E:3–29; C:1–6; F:19]

**Der nächste sachlich belastbare Schritt ist keine neue Featureentwicklung**, sondern die **Freigabe von Produktidentität, realem Quellbestand und Glide-Quellbaseline einschließlich Lizenz-/Archiv-/CI-Nachweis**. Danach können Canonical Theory Engine, Source Registry, Golden Tests, Skill und GUI ohne strukturellen Widerspruch aufgebaut werden. Bis dahin gelten Umfangs-, Vollständigkeits-, Veröffentlichungs- und Testbehauptungen in den sechs Ursprungsdokumenten als **historische Aussagen mit konkreten Evidenzlücken**.

*Ende der konsolidierten Projekt-Overview – Quellenstand 09.11.2026.*
