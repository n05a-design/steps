# Steps – Produktstrategie, Funktionsgrenzen und MVP-Validierung

**Status:** analytischer Entwurf, keine Eigentümerfreigabe. **Stand:** 10.11.2026. **Referenzen:** `research/notes/deep-research/legacy/{01_STEPS_Research_Foundation.md,02_STEPS_Knowledge_Base_Product_Blueprint.md,PROJECT_CONTEXT_HANDOVER.md}` bei Steps `75329fe`; Original-Overview `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`; aktuelle Nutzerbeschreibung.

## 1. Worum es bei Steps eigentlich geht

Drei Zielbilder dürfen nicht fälschlich verschmolzen werden: **A – Harmony-Labor** (Akkorde erkunden, analytisch verstehen, lernen); **B – kompositorisches Sketchpad** (Akkord- und Drum-Progressionen erstellen, hören, MIDI exportieren); **C – umfassende Produktionswissensbibliothek** (breite V6.6/6.7-Forschung von Musiktheorie bis Mastering). B ist in der expliziten Steps-Projektbeschreibung angelegt; die ältere Forschung legt A als wissenschaftlichen Kern nahe. C ist bisher primär ein Archiv bzw. Forschungs-/Erweiterungsraum, kein bewiesener Funktionsumfang der ersten App. **A und B sind keine Alternativen auf Produktebene**, sondern unterschiedliche Nutzenerlebnisse mit gemeinsamen Datenmodellen. Ob Drums schon in der ersten Version oder später erscheinen, ist **eine echte offene Scope-Entscheidung**: Das Handover REQ-024 setzt Drum-Forschung vorläufig `DEFERRED`, die aktuelle Nutzerbeschreibung nennt Drums ausdrücklich als Kernfunktion. Keine von beiden Aussagen rückwirkend löschen.

**Arbeits-Hypothese (nicht beschlossen):** Steps hilft einem Nutzer, in unter fünf Minuten eine musizierbare Folge anzulegen, bei Bedarf eine *belegbare* harmonische Erklärung zu erhalten, zu transponieren, zu speichern und als MIDI auszugeben – ohne Benutzerkonto. Unterschied zu reinen Generatoren: transparentes Kontextmodell, alternative Lesarten und Nachprüfbarkeit. Diese Differenzierung muss getestet werden; bestehende Konkurrenz verfügt bereits über Theorie-/Akkord-/Exportfunktionen.

## 2. Zielgruppen, Aufgaben und echte Nutzennachweise

| Persona / Job | Durchführung (synthetisches Testszenario) | Erfolg | Abbruch-/Negativfall |
|---|---|---|---|
| Anfänger | Vier Akkorde eingeben, Tonart wählen, Stufenhinweis ansehen | nennt einen musikalisch sinnvollen Zusammenhang in eigenen Worten | Erklärung verwendet unbekannte Fachbegriffe ohne Hilfe |
| Songwriter | `C–G–Am–F` um 2 Halbtöne verschieben und MIDI speichern | `D–A–Bm–G`, Datei öffnet extern | enharmonische Schreibweise oder Taktlängen gehen verloren |
| Produzent | 4/4-Folge mit Kick-/Snare-/HiHat-Idee kombinieren | Chords und Groove teilen Takt-/Temporaster | Drift, blockierende Wiedergabe, falscher MIDI-Kanal |
| Lehrkraft | gleiche Harmonie als a-Moll und C-Dur deuten lassen | E7 wird kontextabhängig richtig bezeichnet | Tool verkauft sekundäre Dominante als immer gültig |
| Gitarrist/Pianist | Voicings und Basston gegenüber Akkordidentität unterscheiden | hört/liest nachvollziehbaren Unterschied | UI behauptet „minimaler Voice Leading“ ohne Register/Voicing |
| datenschutzbewusster Nutzer | Start, Speichern, Schließen offline | null externe Netzanforderungen ohne Aktivierung | Zugriff auf Glide-Nutzerdaten oder externe Cloud-API |

**Forschungslücke:** keine echten Nutzungsdaten, Interviews oder formale Aufgaben-Erfolgsquoten vorliegend. Fünf moderierte repräsentative Tests sind eine erste explorative Stichprobe, keine statistisch repräsentative Marktforschung. Vor jedem größeren Produktentscheid zunächst Aufgaben ohne Erklärung vorgeben, Beobachtungen, Dauer, Fehlentscheidungen und Nutzerworte protokollieren.

## 3. Vergleich von vier vertikalen MVP-Schnitten

| Variante | Funktionierende End-to-End-Kette | Vorteile | Kosten/Risiken | Go-/No-Go-Gate |
|---|---|---|---|---|
| **M1 Theory-only** | Akkordeditor → erklärbare Beziehung → Speichern | fachlich enger, gute Unit-Tests | Nutzer hört keinen unmittelbaren Musikwert; kein MIDI | 3 realistische Erklärungsaufgaben bestanden |
| **M2 Chord + SMF-Export** | Akkorde → Transposition → Timeline → MIDI → externe DAW | hörbarer/exportierbarer Nutzen ohne Live-Audio | Datenmodell, Takt- und Notenlängen müssen stimmen | 10 goldene Exportfälle und 2 unabhängige Importprogramme |
| **M3 Chords + Minimales Drum-Grid** | Akkord- und Drumspur → gemeinsames Zeitmodell → MIDI | direkter Bezug zur eigenen Produktbeschreibung | deutlich mehr UI-, Groove-, Undo- und Timingtests | Scope durch Owner bestätigt, keine Datenformat-Sackgasse |
| **M4 Research-first** | Quellen → kanonischer Claim → Regel → Test → Skillantwort | wissenschaftlich robust und unabhängig von UI | Gefahr einer unbegrenzt wachsenden Bibliothek ohne reale App | 20 reviewte Claims und End-to-End-Auskunft ohne erfundenes Zitat |

**Empfehlung:** M2 als *zu untersuchender* erster vertikaler Produktschnitt, M4 parallel als eigenständiger Forschungs-Schnitt; M3 im Daten-/Zeitmodell von Anfang an zulassen, den sichtbaren Drum-Sequencer erst nach Scope-Beschluss bauen. M1 alleine erscheint für den praktischen Produktanspruch zu trocken; M4 alleine darf nicht als fertige Steps-App bezeichnet werden.

## 4. Roadmap-Abhängigkeit und Entscheidungsökonomie

**P0 Vorentwicklung:** Lizenz-/Datenexpositionsprüfung, konsistenter Source Snapshot, Anforderungen mit IDs, klarer Shell-ADR. **P1 vertikaler Durchstich:** eine Chord-Progression speichern und wieder laden, deterministische Transposition, ein korrektes annotiertes Beispiel; noch kein komplexer Harmoniegraph. **P2 Nutzen:** MIDI-Export, nachvollziehbare Relation und Erklärungen. **P3 Ausbau:** alternative Analysen, Arbeitsmodi, Drums, Stilkontext, Bildungsworkflows. Reihenfolge ist *abhängigkeitsbasiert*, kein verbindlicher Terminplan; die bekannten Token-Reset-Tage sind Kapazitätsinformation, keine verlässliche Sprintgeschwindigkeit.

## 5. Interaktionsvertrag für zwei Bereiche

**Offener Grundsatz:** „zwei Fenster“ kann zwei Panels in einer Tk-Root oder zwei unabhängige OS-Toplevels bedeuten. Der Screenshot spricht für Sidebar + Arbeitsfläche, beweist aber keine beabsichtigte endgültige Fensterarchitektur. In einem Prototyp je einen Wireframe der beiden Varianten erstellen, Fokus-/Resize-/Menüverhalten vorführen und Entscheidung als ADR dokumentieren. Navigationspunkte dürfen zunächst **deaktiviert** sein, aber vollständige, erreichbare Bedienmethoden für Ein-/Ausklappen, kompakte Leiste und Rücksprung sind Pflicht.

## 6. Messbare Produkthypothesen statt Marketingannahmen

- `H1`: Lernende verstehen den Unterschied zwischen **Akkordname** und **harmonischer Funktion im Kontext** bei Beispielen mit alternativen Deutungen. Test: Vorher/Nachher-Aufgabe, kein Feedback-Leak.
- `H2`: Ein Nutzer kann vier Akkorde ohne Handbuch eingeben, transponieren und speichern; die Zahl der Fehler und Hilfeaufrufe wird dokumentiert.
- `H3`: Mindestens die kritisch bewerteten Glide-UX-Fähigkeiten (Theme, Typografie, Sidebar, Fokus, Suche, Settings) sind bei der isolierten Shell vorhanden; die alten Todo-Aktionen sind nicht mehr erreichbar.
- `H4`: Open-Source/offline sind im tatsächlich installierten Steps-Build überprüfbar (SBOM, Netzprobe, frische Datenroots), nicht nur Beschreibungstext.
- `H5`: Ein exemplarischer theoretischer Vorschlag zeigt Quelle, Geltungsbereich, Alternative und Grenzen, statt undifferenzierte „KI-Sicherheit“.

## 7. Explizite Nicht-Ziele des ersten, noch nicht freigegebenen Schnitts

Keine vollwertige DAW, kein Audiodatei-Mastering, keine automatische transkribierende Audioanalyse, kein KI-Cloudzwang, keine ungeprüfte Übernahme fremder Chord-Files-/ModeWheel-Darstellung, kein automatischer Rohquellen-Upload, keine öffentliche V6.7-Archivfreigabe und kein Anspruch, dass empirische Chordhäufigkeiten Musiktheorie ersetzen. Diese Abgrenzungen sind eine **Empfehlung**, kein rückwirkend beschlossener Produktvertrag.

## 8. Owner-Entscheidungen mit Vorlage

1. **ADR-PROD-01:** M2/M3, inkl. Drums im v0.1? Kriterien Nutzennachweis, Aufwand, Wissen/Engine-Testbarkeit und Zeitbudget.
2. **ADR-UI-01:** eine Root/zwei Bereiche vs. Root + Toplevel; Demo-Bilder, Betriebs- und Fokusrisiken.
3. **ADR-PROD-02:** welche drei Zielgruppen haben im MVP Vorrang? Entsprechende Nutzertests.
4. **ADR-LICENSE-01:** Rechteinventar und öffentlicher Repository-Bestand – unabhängig vom App-MVP.

**Definition of Done dieses Dokuments:** Es enthält überprüfbare Hypothesen und Freigabefragen. Es bestätigt **weder** eine UX-Validierung **noch** eine Implementierung. Eine Owner-Unterschrift, Aufgaben-/Testprotokoll und testbarer MVP-Commit fehlen weiterhin.
