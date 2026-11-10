# Audio Engineering, Digital Audio & Signal Flow — STEPS Produktionsfachdossier V6.0

**Ablage:** `18_AUDIO_ENGINEERING_SIGNAL_FLOW`  
**Dokumentstatus:** redaktionelle Fachsynthese / Arbeits- und Forschungsrahmen; keine abschließende Peer-Review.  
**Taxonomie:** 32 benannte Einzelthemen; noch kein Nachweis, dass alle eine eigenständige geprüfte Quellenfundstelle besitzen.

## Gegenstand und Bedeutung
Audioentwicklung verlangt ein klares Modell von Abtastung, Quantisierung, Pegel, Wandlern, Zeitverhalten und Signalfluss. Ein numerisch korrekter DSP-Wert ist nicht automatisch ein optimaler Hörentscheid.

Im gesamten STEPS-Produktionssystem ist dieser Bereich eine **eigene fachliche Kompetenz** und nicht automatisch ein weiterer Akkordgenerator. Für die Anwendung sind drei unterschiedliche Nutzungsarten zu trennen: Theorie lernen, Produktionsentscheidungen vorbereiten und Dateien/Events tatsächlich maschinell verarbeiten. Jede Karte braucht einen klaren Output und die Frage, was beim Nutzer **hörbar** oder **nachvollziehbar** besser werden soll.

## Originaler Praxisfall: vollständig dokumentierbares Szenario
Eine Aufnahme vergleicht 44,1 kHz und 48 kHz, 24-bit PCM, interne Float-Verarbeitung und unterschiedliche Exportformate. Pegelveränderungen werden in dBFS, LUFS und True Peak getrennt analysiert.

### Forschungs- und Produktionsablauf
1. Ausgangslage und musikalisches Ziel benennen; stilistische Aussagen als Hypothesen markieren.
2. Die zugehörigen Audio-/MIDI-/Session-Eingaben sowie die tatsächlich erlaubte Datenverwendung erfassen.
3. Mindestens zwei unterschiedliche Produktionsmethoden unter kontrollierten Randbedingungen vergleichen.
4. Entscheidung nach musikalischer Funktion, Aufwand, Nebenwirkungen, Hörtest und reproduzierbaren Messwerten treffen.
5. Artefakte (Daten, Diagramm, Render, Aufgabenstellung, Beschreibung) getrennt von Drittanbieter-Originalmaterial speichern.
6. Musikalisch wertende Aussagen durch mindestens eine fachkundige Hörprüfung ergänzen; Testbedingungen dokumentieren.

## Typische Fehlinterpretationen und Risikoüberprüfung
Sample Rate mit Klangqualität gleichsetzen; Sample-Peak mit True Peak verwechseln; Nyquist-Frequenz als brauchbare Audio-Bandgrenze interpretieren; 32-bit Float als Clipping-Immunität für jede Ausgabestufe missverstehen.

**Review-Frage:** Kann der jeweilige Sachverhalt objektiv mit einem Zahlenwert bewiesen werden, oder ist das Ergebnis ein kontextabhängiges Hör-/Gestaltungsurteil? Das entscheidet über die Validierungsmethode.

## Fachliche Themenkarte
### Themencluster 1: Schall und Frequenz, Pegel dB SPL, dBFS, RMS, LUFS

**Was zu dokumentieren ist:** Für `Schall und Frequenz` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 2: True Peak, Crest Factor, Sample Rate, Bit Depth, PCM

**Was zu dokumentieren ist:** Für `True Peak` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 3: Quantization, Dither, Jitter, Aliasing, Oversampling

**Was zu dokumentieren ist:** Für `Quantization` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 4: Latency, Buffer Size, ADC DAC, Clock Synchronisation, Phase und Polarity

**Was zu dokumentieren ist:** Für `Latency` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 5: Summation, Mono Compatibility, Signal Flow, Gain Staging, Headroom

**Was zu dokumentieren ist:** Für `Summation` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 6: Cable Types, Balanced vs Unbalanced, DI Box, Digital Clipping, Resampling

**Was zu dokumentieren ist:** Für `Cable Types` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

**STEPS-Umsetzung:** Das Cluster erhält separat versionierbare Skills bzw. Lernkarten. Eine konkrete STEPS-Funktion wird nur dann implementiert, wenn sie sich aus vorhandenen Daten, Instrumenten- oder Clip-Informationen ableiten lässt. Bei reiner Hör-/Stilbeurteilung ist der Test ein menschlicher Hörvergleich, keine binäre Software-Assertion.

### Themencluster 7: Null Test, Reference Level

**Was zu dokumentieren ist:** Für `Null Test` und die benachbarten Konzepte wird jeweils (a) die Definition aus der konkreten musikalischen oder technischen Perspektive, (b) Ein- und Ausgangsdaten, (c) ein realistischer Hör- oder Editierkontext, (d) typische Grenzfälle, (e) mögliche Export-/Lizenzrestriktionen und (f) ein prüfbarer Gegenfall benötigt. Nicht jedes benannte Thema ist im vorliegenden Dossier schon vollständig erarbeitet.

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
Schall und Frequenz, Pegel dB SPL, dBFS, RMS, LUFS, True Peak, Crest Factor, Sample Rate, Bit Depth, PCM, Quantization, Dither, Jitter, Aliasing, Oversampling, Latency, Buffer Size, ADC DAC, Clock Synchronisation, Phase und Polarity, Summation, Mono Compatibility, Signal Flow, Gain Staging, Headroom, Cable Types, Balanced vs Unbalanced, DI Box, Digital Clipping, Resampling, Null Test, Reference Level.
