# STEPS – Golden Test Negative & Mutation Verification (Phase 4.16)

**Datum:** 2026-11-11  
**Status:** VERIFIED & HARDENED  
**Referenzdokument:** Phase 4.16 Master Prompt, Teil III & IV  

---

## 1. Zweck & Fail-Closed Architektur

Ein Testsystem, das niemals fehlschlägt, besitzt keine wissenschaftliche Aussagekraft. Um Scheinerfolge und stille Regressionen auszuschließen, enthält die Golden-Test-Suite zwei Arten von negativen Kontrollprüfungen:
1. **Mutationstests (Falsifizierbarkeit):** Künstlich korrumpierte Erwartungswerte müssen reproduzierbar zu `AssertionError` führen.
2. **Fail-Closed Unmapped Execution:** Jeder rechnerische Testfall (`UNIT_TEST`, `PROPERTY_TEST`, `INTEGRATION_TEST`), der nicht über eine dedizierte Rechenlogik verfügt, muss zwingend mit einem `NotImplementedError` abbrechen. Es darf unter keinen Umständen ein Fallback auf `assertIsNotNone` oder ein stilles Überspringen erfolgen.

---

## 2. Implementierte Negative Testfälle

### 2.1 Mutation Detection (`test_mutation_detection_fails_on_corrupted_cases`)
- **Ziel:** Nachweis, dass fehlerhafte Berechnungsergebnisse oder korrumpierte Datensätze sofort anschlagen.
- **Methode:** Ein temporär kopierter und manipulierter Case (`REF-0001` mit gefälschtem Pitch-Class-Ergebnis `99`) wird an `evaluate_executable_case` übergeben.
- **Erwartetes Verhalten:** `AssertionError` wird ausgelöst.
- **Testergebnis:** Bestanden (`assertWithErrorHandling` fängt die AssertionError ab).

### 2.2 Unmapped Case Fail-Closed (`test_unimplemented_executable_case_strictly_raises_error`)
- **Ziel:** Nachweis, dass neue oder unvollständig implementierte rechenbare Testfälle nicht stillschweigend als bestanden gewertet werden.
- **Methode:** Ein synthetischer Case `REF-9999` mit `test_class='UNIT_TEST'` und leerem Rechenpfad wird an `evaluate_executable_case` übergeben.
- **Erwartetes Verhalten:** Löst zwingend `NotImplementedError` mit Meldung `Executable test case 'REF-9999' has no implementation!` aus.
- **Testergebnis:** Bestanden (`assertRaises(NotImplementedError)` bestätigt das Fail-Closed-Verhalten).

### 2.3 Stimmkreuzungs-Erkennung (`detect_voice_crossing`)
- **Ziel:** Nachweis, dass unzulässige Stimmkreuzungen im Kontrapunkt verlässlich erkannt werden.
- **Methode:**
  - Reguläres Voicing: `[48, 55, 60, 64]` -> `detect_voice_crossing` liefert `False`.
  - Gekreuztes Voicing (Alt tiefer als Tenor): `[48, 62, 59, 64]` -> `detect_voice_crossing` liefert `True`.
- **Testergebnis:** Bestanden.

---

## 3. Zusammenfassung der Gegenproben

| Testfunktion | Geprüfter Fehlermechanismus | Erwartete Ausnahme | Tatsächliche Reaktion | Status |
|---|---|---|---|:---:|
| `test_mutation_detection_fails_on_corrupted_cases` | Verfälschter Erwartungswert | `AssertionError` | Gefangen & bestätigt | PASS |
| `test_unimplemented_executable_case_strictly_raises_error` | Fehlende Rechenlogik bei Executable | `NotImplementedError` | Gefangen & bestätigt | PASS |
| `test_property_voice_leading_metrics_distinctiveness` | Unzulässige Äquivalenzannahme zirkulär vs absolut | Ungleiche Distanz | Bestätigt | PASS |
