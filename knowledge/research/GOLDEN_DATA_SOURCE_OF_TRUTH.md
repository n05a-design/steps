# STEPS – Single Source of Truth für Golden Reference Cases

## 1. Verbindliche Architektur und Standorte

Zur Vermeidung von Datenfragmentierung und divergierenden Versionen gilt für die Golden-Reference-Cases folgende kanonische Architektur:

| Rolle | Dateipfad | Zweck |
|---|---|---|
| **Kanonischer Master (Source of Truth)** | `knowledge/research/golden_cases/golden_reference_cases.json` | Primärer, versionierter Wissensbestand im Forschungsbereich. Alle Änderungen und Erweiterungen finden ausschließlich hier statt. |
| **Ausführbarer Test-Spiegel** | `tests/golden_cases/golden_reference_cases.json` | Für die Unit- und Integrations-Testsuiten bereitgestellter deterministischer Spiegel. |
| **Validierungs-Register** | `knowledge/research/FINAL_REFERENCE_CASE_VALIDATION.csv` | Tabellarische Erfassung der formalen Verifikationsergebnisse, Testklassen und Belege. |
| **Historische Matrix** | `knowledge/research/HISTORICAL_REFERENCE_ID_MATRIX.csv` | Lückenlose Dokumentation der ursprünglichen und migrierten Bedeutungen aller Referenzfälle. |
| **Migrationsregister** | `knowledge/research/REFERENCE_ID_MIGRATION_REGISTER.csv` | Register aller historischen Identitätswiederherstellungen und ID-Neuzuweisungen. |

---

## 2. Bestandsübersicht (Phase 4.15)

Der konsolidierte Gesamtbestand umfasst **198 Golden Reference Cases**.
60 Fälle werden als Berechnung oder Produktprüfung ausgeführt. 138 Fälle sind
Spezifikationsbeispiele mit Strukturprüfung. Die historischen CSV-Matrizen
dokumentieren frühere Klassifizierungen. Die aktuelle Klasse steht im Golden-Master.

Die [Abdeckungsmatrix](../benchmark/COVERAGE.csv) dokumentiert für alle 198
Fälle eine formale Prüfung und für keinen eine fachliche Einzelabnahme.
Identitäts-, Hash- und Testprüfungen sichern Zuordnung, Spiegelung und
erwartetes Laufzeitverhalten. Aussagen, Sollwerte und Quellen bedürfen einer
eigenen fachlichen Prüfung.

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
   Wird der kanonische Bestand in `knowledge/` aktualisiert, generiert das Skript `scripts/build_unified_golden_cases.py` die Testfixture in `tests/` synchron neu. Eine manuelle Bearbeitung der gespiegelten Datei in `tests/` ist unzulässig.

3. **Identity-Lock:**
   Die Datei `knowledge/research/REFERENCE_IDENTITY_BASELINE.json` sichert die unveränderliche Zuordnung von `case_id`, `title`, `domain` und `expected_output` dauerhaft ab.
