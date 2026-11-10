# Music File Formats, APIs, Interoperability & Reproducibility — STEPS Produktionsfachdossier V6.0

**Ablage:** `39_INTEROPERABILITY_FORMATS`  
**Dokumentstatus:** redaktionelle Fachsynthese / Arbeits- und Forschungsrahmen; keine abschließende Peer-Review.  
**Taxonomie:** 40 benannte Einzelthemen; noch kein Nachweis, dass alle eine eigenständige geprüfte Quellenfundstelle besitzen.

## Gegenstand und Bedeutung
Ein Produktionsarchiv benötigt klar getrennte Formate für Audio, MIDI, Notation, Arrangement und Metadaten. Konvertierungen sind nicht immer verlustfrei; Semantik, Timing und Plugin-Zustände können verloren gehen.

Im gesamten STEPS-Produktionssystem ist dieser Bereich eine **eigene fachliche Kompetenz** und nicht automatisch ein weiterer Akkordgenerator. Für die Anwendung sind drei unterschiedliche Nutzungsarten zu trennen: Theorie lernen, Produktionsentscheidungen vorbereiten und Dateien/Events tatsächlich maschinell verarbeiten. Jede Karte braucht einen klaren Output und die Frage, was beim Nutzer **hörbar** oder **nachvollziehbar** besser werden soll.

## Originaler Praxisfall: vollständig dokumentierbares Szenario
Ein Original-MIDI exportiert Notennummer, Tickposition, Tempo-Map, CC, Program Change, Pitch Bend und Track-Namen. Nach dem Import werden diese Felder verglichen, nicht nur hörbare Noten.

### Forschungs- und Produktionsablauf
1. Ausgangslage und musikalisches Ziel benennen; stilistische Aussagen als Hypothesen markieren.
2. Die zugehörigen Audio-/MIDI-/Session-Eingaben sowie die tatsächlich erlaubte Datenverwendung erfassen.
3. Mindestens zwei unterschiedliche Produktionsmethoden unter kontrollierten Randbedingungen vergleichen.
4. Entscheidung nach musikalischer Funktion, Aufwand, Nebenwirkungen, Hörtest und reproduzierbaren Messwerten treffen.
5. Artefakte (Daten, Diagramm, Render, Aufgabenstellung, Beschreibung) getrennt von Drittanbieter-Originalmaterial speichern.
6. Musikalisch wertende Aussagen durch mindestens eine fachkundige Hörprüfung ergänzen; Testbedingungen dokumentieren.

## Typische Fehlinterpretationen und Risikoüberprüfung
MIDI-Note-Number mit MIDI-C-Oktavschreibweise verwechseln; MPE via gewöhnlichen Pitchbend-Track zusammenfalten; DAW-Projektdatei als universelles Austauschformat deklarieren.

**Review-Frage:** Kann der jeweilige Sachverhalt objektiv mit einem Zahlenwert bewiesen werden, oder ist das Ergebnis ein kontextabhängiges Hör-/Gestaltungsurteil? Das entscheidet über die Validierungsmethode.

## Fachliche Themenkarte
### Themencluster 1: MIDI 1.0 SMF, MIDI 2.0 UMP, MIDI CI, MPE, MIDI CC

**Was zu dokumentieren ist:** Für `MIDI 1.0 SMF` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 2: MusicXML, MEI, ABC Notation, LilyPond, WAV

**Was zu dokumentieren ist:** Für `MusicXML` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 3: BWF, AIFF, FLAC, MP3, AAC

**Was zu dokumentieren ist:** Für `BWF` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 4: Opus, Ogg, ADM BWF, JAMS, DAW Project Interchange

**Was zu dokumentieren ist:** Für `Opus` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 5: AAF, OMF, Stems, DAWproject, AudioUnit

**Was zu dokumentieren ist:** Für `AAF` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 6: VST3, CLAP, OSC, Ableton Link, Timecode

**Was zu dokumentieren ist:** Für `VST3` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 7: Metadata JSON, Checksums, Schema Versioning, Migration, Lossy Conversion

**Was zu dokumentieren ist:** Für `Metadata JSON` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 8: Roundtrip Tests, Cents, Pitch Spelling, Tempo Map, Controller Resolution

**Was zu dokumentieren ist:** Für `Roundtrip Tests` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.


## Lernpfad
**Einsteiger:** Identifiziere die relevanten Objekte, Signale und musikalischen Rollen ohne Spezialsoftware.  
**Fortgeschritten:** Baue zwei absichtlich kontrastierende Versionen und beschreibe ihre Konsequenzen.  
**Experten:** Dokumentiere den Grenzfall, einen Gegenbeleg und den Export in eine andere DAW / ein neues Wiedergabesystem.

## Daten- und Quellenpflicht
Jeder spätere atomare Wissenseintrag braucht `source_id`, `claim_type`, `confidence`, `review_status`, `license_status`, `tool_assumptions` und nach Möglichkeit eine `golden_test_id`. Ein Quellenlink in einem Sammelregister ersetzt keine Einzelclaim-Zitation. Berücksichtige dokumentierte Hersteller- und Standardunterschiede; stelle allgemeine Producing-Tipps nicht als universelle Standards dar.

## Codex-Abnahme (nur als Forschungsdatenbank)
- [ ] Eigene Domain-/Subtopic-IDs sind stabil und in der Taxonomie auffindbar.
- [ ] Jede eingeführte Softwarefunktion benennt Ein- und Ausgabe inklusive Fehlerfällen.
- [ ] Neue Quellenbelege sind einzeln nachvollziehbar, nicht nur thematisch genannt.
- [ ] Geschützte Tonaufnahmen und Presets werden nicht automatisch in ein öffentliches Projekt übertragen.
- [ ] Wahrnehmung und Stil werden qualitativ geprüft; technische Datenschemata automatisch.

## Fachbegriffe (indexiert; kein vollständiges Lehrbuch)
MIDI 1.0 SMF, MIDI 2.0 UMP, MIDI CI, MPE, MIDI CC, MusicXML, MEI, ABC Notation, LilyPond, WAV, BWF, AIFF, FLAC, MP3, AAC, Opus, Ogg, ADM BWF, JAMS, DAW Project Interchange, AAF, OMF, Stems, DAWproject, AudioUnit, VST3, CLAP, OSC, Ableton Link, Timecode, Metadata JSON, Checksums, Schema Versioning, Migration, Lossy Conversion, Roundtrip Tests, Cents, Pitch Spelling, Tempo Map, Controller Resolution.
