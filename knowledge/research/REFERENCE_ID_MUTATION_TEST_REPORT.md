# STEPS – Referenzintegritäts- & Mutationstestbericht (OA-0031 Härtung)

## 1. Testübersicht & Methodik

Zur Härtung des musikalischen Referenzintegritäts-Checkers (`scripts/verify_reference_integrity.py`) wurden 15 isolierte negative Mutationstests in `tests/test_reference_integrity.py` implementiert. 

Im Gegensatz zu trivialen Mengenabfragen (`assertNotIn`) wird in jedem Testfall in einer isolierten Arbeitsumgebung (`tempfile.mkdtemp`) exakt ein realer Fehler in die Wissensdaten injiziert. Der Validator verarbeitet die fehlerhafte Datei und muss den Fehler präzise erkennen und melden. Die kanonischen Bestände des Repositories bleiben dabei unberührt.

---

## 2. Detaillierte Mutationstest-Ergebnisse

| Test-ID | Injektions-Typ | Fehlerbeschreibung | Erkennungsmechanismus | Ergebnis |
|---|---|---|---|---|
| `test_00` | Basiskontrolle | Reales kanonisches Repository (PROG, PAT, P, REF, CR) | Vollständige Integritätsprüfung aller 5 Teilsysteme | **PASS (0 Fehler)** |
| `test_01` | Doppelte PROG-ID | Duplikation von `PROG-001` in Progression-Bibliothek | Zeilengenaue Tabellenextraktion ohne Set-Kollaps | **PASS (Erkannt)** |
| `test_02` | Doppelte PAT-ID | Duplikation von `PAT-001` in Drum-Bibliothek | Zeilengenaue Tabellenextraktion | **PASS (Erkannt)** |
| `test_03` | Doppelte Piano-Modul-ID | Duplikation von `P01` in Klavierpraxis-Bibliothek | Zeilengenaue Tabellenextraktion | **PASS (Erkannt)** |
| `test_04` | Doppelte REF-ID | Duplikation von `REF-0001` in `golden_reference_cases.json` | JSON Array Case-ID Duplikaterkennung | **PASS (Erkannt)** |
| `test_05` | Geänderte REF-Semantik | Titeländerung von `REF-0001` zu *Kammerton A4* | Abgleich gegen `REFERENCE_IDENTITY_BASELINE.json` | **PASS (Erkannt)** |
| `test_06` | Fehlende REF-ID | Löschung des Baseline-Falls `REF-0001` aus der Suite | Baseline-Vollständigkeitsprüfung | **PASS (Erkannt)** |
| `test_07` | Verwaiste Relation (PROG) | Relation mit Ziel `PROG-999` in Relations-CSV | Referenzielle Fremdschlüssel-Prüfung | **PASS (Erkannt)** |
| `test_08` | Verwaiste Relation (Piano) | Relation mit Ziel `P99` in Relations-CSV | Referenzielle Fremdschlüssel-Prüfung | **PASS (Erkannt)** |
| `test_09` | Ungültige Domäne `M010` | Injektion von `M010` in Domain Readiness Matrix | Strenger Abgleich gegen `{M01..M12}` | **PASS (Erkannt)** |
| `test_10` | Fehlende CSV-Spalte | Entfernung von `source_id` aus Relations-Header | CSV Schema-Pflichtfeldprüfung | **PASS (Erkannt)** |
| `test_11` | Malformierte MD-Tabelle | Zeile mit 3 statt 6 Spalten (ehem. PROG-016 Defekt) | Markdown Spaltenzähler-Konsistenzprüfung | **PASS (Erkannt)** |
| `test_12` | Golden Test Desync | Diskrepanz zwischen Source of Truth und Test-Mirror | SHA-256 Hashabgleich zwischen beiden Standorten | **PASS (Erkannt)** |
| `test_13` | Defektes Migrationsregister | Entfernung von Pflichtspalten im Migrationsregister | CSV Schema-Pflichtfeldprüfung | **PASS (Erkannt)** |
| `test_14` | Fehlerhafter JSON-Datentyp | Root ist Dictionary statt Array | JSON Typ- und Schemavalidierung | **PASS (Erkannt)** |
| `test_15` | Ungültiger Relationstyp | Unzulässiger Relationstyp `INVALID_INVENTED_...` | Ontologie-Vokabular-Prüfung gegen 46 Relationen | **PASS (Erkannt)** |

---

## 3. Abnahmeergebnis

* **Ausgeführte Tests:** 16 (1 kanonische Validierung + 15 negative Mutationstests).
* **Bestanden:** 16 / 16 (100 %).
* **Dauer:** 2.88 s.
* **Status:** `MUTATION_TESTING_VERIFIED_FAIL_CLOSED`.
