# STEPS – Single Source of Truth für Golden Reference Cases

## 1. Verbindliche Architektur und Standorte

Zur Vermeidung von Datenfragmentierung und divergierenden Versionen gilt für die Golden-Reference-Cases folgende kanonische Architektur:

| Rolle | Dateipfad | Zweck |
|---|---|---|
| **Kanonischer Master (Source of Truth)** | `knowledge/research/golden_cases/golden_reference_cases.json` | Primärer, versionierter Wissensbestand im Forschungsbereich. Alle Änderungen und Erweiterungen finden ausschließlich hier statt. |
| **Ausführbarer Test-Spiegel** | `tests/golden_cases/golden_reference_cases.json` | Für die Unit- und Integrations-Testsuiten bereitgestellter deterministischer Spiegel. |
| **Validierungs-Register** | `knowledge/research/FINAL_REFERENCE_CASE_VALIDATION.csv` | Historischer Auszug früherer Testklassen und Belege. |
| **Historische Matrix** | `knowledge/research/HISTORICAL_REFERENCE_ID_MATRIX.csv` | Lückenlose Dokumentation der ursprünglichen und migrierten Bedeutungen aller Referenzfälle. |
| **Migrationsregister** | `knowledge/research/REFERENCE_ID_MIGRATION_REGISTER.csv` | Register aller historischen Identitätswiederherstellungen und ID-Neuzuweisungen. |

---

## 2. Bestandsübersicht (Phase 4.15)

Der konsolidierte Gesamtbestand umfasst **198 Golden Reference Cases**.
120 Fälle werden als Berechnung oder Produktprüfung ausgeführt. 78 Fälle sind
Spezifikationsbeispiele mit Strukturprüfung und ggf. Quellenabgleich. Die historischen CSV-Matrizen
dokumentieren frühere Klassifizierungen. Die aktuelle Klasse steht im Golden-Master.

Die [Abdeckungsmatrix](../benchmark/COVERAGE.csv) dokumentiert für alle 198
Fälle eine formale Prüfung und für keinen eine fachliche Einzelabnahme.
Identitäts-, Hash- und Testprüfungen sichern Zuordnung, Spiegelung und
erwartetes Laufzeitverhalten. Aussagen, Sollwerte und Quellen bedürfen einer
eigenen fachlichen Prüfung.

Die General-MIDI-Drumbeispiele REF-0022 bis REF-0025 sowie REF-0033
und REF-0045 sind mit Tabelle 3 auf Druckseite 6 (PDF-Seite 8)
abgeglichen. MIDI-Kanal 10 ordnet 36 dem Bass Drum 1, 37 dem Side Stick,
38 der Acoustic Snare sowie 42, 44 und 46 den geschlossenen,
pedalbetätigten und offenen Hi-Hats zu. Die Falltitel „Kick Drum“
und „Snare Drum“ bezeichnen diese konkreten Varianten. Die Tabelle
führt 35 als Acoustic Bass Drum und 40 als Electric Snare separat.
Die Tests vergleichen Instrument und Sollwert mit dieser Fundstelle.
Die sechs Fälle dokumentieren eine Spezifikation für GM1-Geräte.
[The MIDI Association, General MIDI System Level 1, Tabelle 3](https://drive.google.com/file/d/1TTM2HI2JAp_XiTJYEJ8gPNvuJpIjJiTP/view)

REF-0177 bis REF-0186 prüfen die zweite Sechzehntelposition im Paar,
ihren Versatz zum geraden Raster und die Zeitumrechnung. Die STEPS-Formel
rundet den Anteil an einem Halbviertel auf ganze Ticks. Das Handbuch
beschreibt den Parameterbereich in MPC Standalone OS 3.6. Die
Sollwerte gelten für das STEPS-Rechenmodell. [Akai, Timing Correct](https://cdn.inmusicbrands.com/Software/36/MPC%20Standalone%20OS%20-%20User%20Guide%20-%20v3.6.pdf)

57 Prozent sind ein Übungswert ohne belegte Zuschreibung zu einzelnen
Musikern. Der Anteil zwei Drittel modelliert die triolische Gruppierung.
Die beobachteten Swingverhältnisse in Jazzaufnahmen ändern sich mit dem
Tempo. [Friberg und Sundström, Music Perception 19(3), Abstract](https://doi.org/10.1525/mp.2002.19.3.333)

REF-0126 bis REF-0137 berechnen die Schrittfolgen aus notierten Skalen
über eine Oktave. Die Modi verwenden die jeweiligen Stammtöne ab ihrem
Grundton. Für harmonisch und aufsteigend melodisch Moll sind die
erhöhten Stufen in A notiert. Bei der Pentatonik verwenden Dur und
relatives Moll denselben Tonvorrat mit unterschiedlichen Grundtönen.
Die Ganztonfolge schließt die Oktave in sechs gleich großen Schritten.
[Open Music Theory, Collections and Scales](https://openmusictheory.github.io/scales2.html)
· [Music Theory for the 21st-Century Classroom, § 3.1 Minor Scales](https://musictheory.pugetsound.edu/mt21c/MinorScales.html)

* **REF-0001 bis REF-0094 (Historischer Kernbestand Phase 4.1 bis 4.12):**
  Historische Fallzuordnungen wiederhergestellt (Tonklassen C4/A4, 12-TET Enharmonik, Intervalle, Kadenzen, Swing-Ratios, GM-Percussion-Mappings, Tuplet-Quantisierung, Rootless Voicings).
* **REF-0095 bis REF-0100 (Phase 4.13 Multi-Domain & Erweiterungen):**
  Harmonisierte und wiederhergestellte komplexe Fälle (Backdoor-Leittonauflösung, chromatische Sekundärdominanten-Basslinie, Coltrane Großterz-Zyklus, Neo-Soul 57% Swing, Bembé 12/8 Bell-Invariante, Multi-Domain-Synthese).
* **REF-0101 bis REF-0198 (Phase 4.14 Akustik- & Theoriefallstudien):**
  In Phase 4.14 neu eingeführte Testfälle (Kammerton A4, Frequenzverhältnisse, Cent-Berechnungen, Skalenintervalle, MIDI-Zeitarithmetik), die zur Vermeidung semantischer Kollisionen mit den historischen IDs auf freie IDs oberhalb von `REF-0100` migriert wurden.

---

## 3. Synchronisations- & Integritätsgarantie

1. **Deterministische Hash-Gleichheit:**
   `scripts/verify_reference_integrity.py` und die Testsuite `tests/test_reference_integrity.py` berechnen bei jedem Lauf den SHA-256-Hash beider Dateien:
   $$\text{SHA256}(\text{knowledge/.../golden_reference_cases.json}) \equiv \text{SHA256}(\text{tests/.../golden_reference_cases.json})$$
   Eine Abweichung führt unmittelbar zum Abbruch mit Exit-Code 1 (Fail-Closed).

2. **Automatisierte Spiegelung:**
   Nach einer Änderung am Master übernimmt
   `python -B scripts/build_unified_golden_cases.py` dessen Bytes in den
   Testspiegel. Mit `--check` prüft der Befehl die Übereinstimmung
   schreibfrei. Der Generator verwendet nur den Master als Datenquelle und
   prüft die Fall-IDs gegen die Baseline. Die historischen CSV-Berichte
   bleiben als Belege ihrer jeweiligen Phase erhalten.

3. **Identity-Lock:**
   Die Datei `knowledge/research/REFERENCE_IDENTITY_BASELINE.json` sichert die unveränderliche Zuordnung von `case_id`, `title`, `domain` und `expected_output` dauerhaft ab.
