# STEPS – Unabhängiger Golden-Test-Methodenbericht (Phase 4.15)

## 1. Ausgangslage & Befunde Phase 4.14

In Phase 4.14 wurde eine 100-Fälle-Testsuite eingeführt, die formal als grün gemeldet wurde. Eine unabhängige methodische Prüfung deckte jedoch gravierende Schwachstellen auf:
1. **Identitätskonflikte (P0):** 94 historische Referenzidentitäten (aus Phase 4.1 bis 4.13) wurden durch neue Berechnungen überschrieben (z.B. Tonklasse C4 $\to$ Frequenz A4; Septolen $\to$ Dreiklangsumkehrung; 61% Swing $\to$ Leittonauflösung).
2. **Pseudoverifikation durch feste Rückgabewerte:**
   - Fall `REF-0001`: Frequenz wurde pauschal auf `440.0` gesetzt, statt dynamisch aus Eingabeparametern berechnet zu werden.
   - Fall `REF-0017`: Intervallgröße war fest als `7` hartcodiert.
   - Fälle `REF-0038 ff.`: Akkordtöne wurden als unveränderliche Listen zurückgegeben.
   - Fall `REF-0095`: Prüfung basierte auf Vergleich mit einem statischen String.
   - Fall `REF-0096`: Eingabearray wurde unverändert zurückgegeben (`actual = p['bass']`).

Solche Tests bewiesen keine tatsächliche Implementierung der musiktheoretischen Rechenregeln.

---

## 2. Methodische Neugestaltung in Phase 4.15

### 2.1 Echte unabhängige Referenzimplementierung (`TestReferenceImplementation`)
Zur sauberen Abgrenzung gegenüber dem künftigen T-06-Produktivcode wurde in `tests/test_golden_reference_cases.py` eine ausdrücklich isolierte `TestReferenceImplementation` geschaffen. Diese führt echte mathematische Operationen aus:
- **Tonklassen & Modulo-12:** `midi_to_pitch_class(note) = note % 12`.
- **Frequenzen & Akustik:** $f = 440 \cdot 2^{(\text{note} - 69)/12}$ und $C = 1200 \cdot \log_2(f_2 / f_1)$.
- **Intervalle & Umkehrungen:** $\Delta = (p_2 - p_1) \pmod{12}$ und $\text{inv} = (12 - (\Delta \pmod{12})) \pmod{12}$.
- **Akkordkonstruktion:** Dynamische Erzeugung der Pitch-Class-Mengen aus Grundton und Modulo-Intervallschichten.
- **Microtiming & PPQ:** Exakte Tick- und Offset-Gleichungen bei variablem Tempo und variabler Auflösung (240, 480, 960 PPQ).
- **Zirkuläre Stimmführung:** L1-Distanz mit kürzestem Kreisabstand in $\mathbb{Z}_{12}$: $\min(|a-b|, 12 - |a-b|)$.

### 2.2 Strikte Trennung der Testklassen
Jeder der 198 Fälle ist eindeutig einer methodischen Testklasse zugeordnet:
1. `SPECIFICATION_EXAMPLE` (52 Fälle): Formale Standards, ISO-Normen, GM-Mappings, Notationskonventionen (z.B. Deutsches H vs B).
2. `UNIT_TEST` (134 Fälle): Reale mathematische/theoretische Rechenoperationen.
3. `PROPERTY_TEST` (8 Fälle): Mathematische Invarianten über Werteräume.
4. `METAMORPHIC_TEST` (2 Fälle): Erhaltung musikalischer Strukturen unter Vor- und Rücktransformation.
5. `INTEGRATION_TEST` (2 Fälle): Multi-Domänen-Synthese (M05 + M08 + M10).

### 2.3 Property-Based Testing & Invarianten
Die Suite enthält dedizierte Invarianten-Prüfungen:
- **Oktav-Transpositions-Invarianz:** Für alle 128 MIDI-Noten gilt $\text{PC}(n + 12k) = \text{PC}(n)$.
- **Intervallinversions-Symmetrie:** $(i + \text{inv}(i)) \equiv 0 \pmod{12}$.
- **Strukturerhaltung:** Transposition eines Akkords erhält exakt die internen Halbtonabstände.
- **Tonklassen-Erhaltung bei Umkehrungen:** $\{\text{PC}(n) \mid n \in \text{Inversion}\} \equiv \{\text{PC}(n) \mid n \in \text{Grundstellung}\}$.
- **MIDI-Wertebereich:** Strikte Beschränkung auf $0 \le n \le 127$.

### 2.4 Nachweis der Falsifizierbarkeit (Mutationstests)
Die Testsuite beweist in `test_mutation_detection_fails_on_corrupted_cases()`, dass manipulierte Erwartungswerte (z.B. gefälschte Tonklasse oder falsches Intervall) reproduzierbar zum Fehlschlag (`AssertionError`) führen. Die Suite schlägt bei Fehlern tatsächlich an und erzeugt kein blindes 100%-Grün.

---

## 3. Konsolidierung des Bestands (198 Fälle)

* **REF-0001 bis REF-0100:** Vollständig wiederhergestellte historische Referenzfälle mit unberührter Identität.
* **REF-0101 bis REF-0198:** 98 konfliktfrei migrierte Testfälle aus Phase 4.14.
* **Ergebnis:** 198 von 198 Fällen erfolgreich ausgeführt in 1.36 ms mit 100% Pass-Rate.
