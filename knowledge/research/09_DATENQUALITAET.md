# STEPS – Technische Datenqualität & Schemakonsistenz (Phase I Audit)

**Dokumenttyp:** SYSTEMATISCHES DATENQUALITÄTS- & SCHEMA-AUDIT  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Alle strukturierten Datenbestände (JSON, CSV, YAML, Markdown-Tabellen)  
**Status:** `AUDITED & 100% CLEAN`  

---

## 1. Übersicht der strukturierten Datenbestände & Entitätsklassen

STEPS verwaltet elf disjunkte Entitätsklassen mit strikt eindeutigen, unveränderlichen IDs:

| Entitätsklasse | Präfix | Speicherort | Anzahl | Primäre ID-Prüfung |
|:---|:---:|:---|:---:|:---|
| **Architecture Decision Records** | `ADR-` | `decisions/DECISION_REGISTER.md` | 12 | `scripts/verify_reference_integrity.py` |
| **Kanonische Progressionen** | `PROG-` | `knowledge/concepts/progressions/` | 28 | `scripts/verify_reference_integrity.py` |
| **Kanonische Drum-Patterns** | `PAT-` | `knowledge/concepts/styles/` | 31 | `scripts/verify_reference_integrity.py` |
| **Klavier-Praxismodule** | `P` | `knowledge/concepts/chords/` | 19 | `scripts/verify_reference_integrity.py` |
| **Unified Golden Cases** | `REF-` | `knowledge/research/golden_cases/` | 198 | `tests/test_golden_reference_cases.py` |
| **Theorie-Axiom Relationen** | `CR-` | `knowledge/relations/` | 37 | `tests/test_reference_integrity.py` |
| **Recommender Relationen** | `REL-` | `knowledge/relations/` | 34 | `tests/test_reference_integrity.py` |
| **Cross-Domain Relationen** | `CDR-` | `knowledge/relations/` | 23 | `tests/test_reference_integrity.py` |
| **Musikalisches Fehlerregister** | `ERR-` | `knowledge/research/` | 37 | `tests/test_reference_integrity.py` |
| **Wissenschaftliche Claims** | `CLAIM-` | `knowledge/sources/` | 66 | `tests/test_curation_tools.py` |
| **Offene Arbeitsaufträge** | `OA-` | `%LOCALAPPDATA%\StepsKnowledge\` | 27 | `tests/test_curation_tools.py` |

---

## 2. Befunde & Durchgeführte Datenqualitäts-Korrekturen

### 2.1 Beseitigung von UTF-8 Byte Order Marks (BOM / `\xef\xbb\xbf`)
* **Problem:** In älteren Windows-Umgebungen (PowerShell 5.1 / Excel) gespeicherte CSV-Dateien enthielten ein führendes BOM (`\xef\xbb\xbf`). Dies führte dazu, dass Standard-Python-Parser ohne `utf-8-sig` den ersten Header als `\ufefferror_id` bzw. `\ufeffclaim_id` einlasen, wodurch automatisierte Dictionary-Lookups mit `KeyError` abbrachen.
* **Behebung:** Bereinigung des BOM-Headers in:
  - `knowledge/research/MUSICAL_ERROR_REGISTER.csv`
  - `knowledge/research/MUSIC_KNOWLEDGE_COVERAGE_MATRIX.csv`
  - `knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv`
* **Ergebnis:** Standardkonforme RFC-4180 UTF-8 Kodierung; sauberes Einlesen unter allen Plattformen (Windows, Linux, macOS).

### 2.2 Prüfung auf Zeichenfehler & Mojibake
* Alle aktiven Wissens- und Testdateien wurden auf korrupte UTF-8 Bytefolgen (z. B. `Ã¤`, `Ã¶`, `Ã¼`, `ÃŸ`, `Ã©`) geprüft.
* **Ergebnis:** 0 Mojibake-Sequenzen im aktiven Datenbestand. Umlaute und Sonderzeichen ($\sharp, \flat, \circ, \to, \mathbb{Z}_{12}$) sind fehlerfrei enkodiert.

### 2.3 ID-Eindeutigkeit & Fremdschlüssel-Integrität
* Es existieren **keine doppelten IDs** innerhalb einer Entitätsfamilie ($|\text{IDs}| = |\text{Unique IDs}|$).
* Alle Fremdschlüssel (`source_id`, `target_id`) in `MUSIC_CONCEPT_RELATIONS.csv` verweisen auf tatsächlich existierende Entitäten (0 Dangling References).

---

## 3. Protokoll für künftige Datenmigrationen

Sollte in künftigen Phasen eine Schemamigration erforderlich sein, gilt das folgende 7-Stufen-Verfahren:
1. **Ausgangszustand sichern:** Snapshot der betroffenen Dateien mit SHA-256 Hashes in `REFERENCE_IDENTITY_BASELINE.json`.
2. **Zielstruktur spezifizieren:** Definition der neuen Pflichtfelder und Datentypen im entsprechenden Schema (`schemas/`).
3. **Migrationsskript implementieren:** Deterministischer Konverter in `scripts/`.
4. **Prüfung an isolierter Kopie:** Validierung an temporären Testdateien ohne Berührung des Produktivbestands.
5. **Verlustanalyse:** Mathematischer Nachweis, dass keine bestehenden Attribute oder Notationen verloren gehen.
6. **Rückwärtskompatibilität:** Sicherstellung, dass bestehende Tests nicht ohne Baseline-Update brechen.
7. **Dokumentation & Freigabe:** Eintrag im Änderungsprotokoll und Aktualisierung der Baseline-Versionsnummer.
