# STEPS – Inhaltliche Fehleranalyse und Peer-Review des Wissensgraphen

> **Dokumentenstatus:** Offizieller Audit- und Revisionsbericht zur Bereinigung des STEPS-Wissensgraphen (Stand: 17. November 2026).  
> **Geltungsbereich:** Alle 97 Relationen (`38 CR-*`, `36 REL-*`, `23 CDR-*`) der Wissensmatrizen (`GRAPH_AUDIT_MATRIX.csv`, `GRAPH_HUMAN_REVIEW_v1.csv`, `GRAPH_HUMAN_REVIEW_v2.csv`).

---

## 1. Executive Summary: Bestätigte Befunde

Die unabhängige inhaltliche Fehleranalyse deckt gravierende musiktheoretische, ontologische und methodische Mängel im Ausgangsbestand und in den Revisionsstufen v1/v2 auf. Alle Befunde wurden rechnerisch und quellenkritisch nachvollzogen und bestätigt:

1. **Harte musiktheoretische Sachfehler:**
   * **`CDR-010` (Polychord $D/C \to C\text{maj13}(\sharp 11)$):**  
     Die Schichtung von $D$-Dur ($\{D, F\sharp, A\}$) über $C$-Dur ($\{C, E, G\}$) ergibt die Töne $\{C, E, G, D, F\sharp, A\}$. Bezogen auf den Grundton $C$ sind dies die Stufen $1, 3, 5, 9, \sharp 11, 13$. Es **fehlt die große Septime $B/H$**, womit kein $C\text{maj13}(\sharp 11)$ vorliegt, sondern ein $C^{6/9(\sharp 11)}$ bzw. maximal ein unvollständiges Teilvoicing (`PARTIAL_VOICING_OF`).
   * **`CR-024` (Puls vs. Frequenz / $M07-01 \text{ REQUIRES } M01-01$):**  
     Metrische Pulsgruppierung hängt physikalisch nicht von der akustischen Schwingungsfrequenz der Töne ab. Das Gegenmodell belegt, dass bei festem Tonhöhenparameter beliebige Pulsperioden darstellbar sind; metrische Gruppierung entspringt einem zeitlichen Ereignisstrom (`TEMPORAL_EVENT_STREAM`).

2. **Kategoriale Typfehler im Ursprungsbestand:**
   * `CR-002`: Eine Oktave (2:1) ist ein Referenzintervall, keine Variante eines Stimmungssystems (`IS_VARIANT_OF` $\to$ `DEFINES_EQUIVALENCE_IN`).
   * `CR-006`: Enharmonik ($C\sharp/D\flat$) widerspricht nicht dem Vorzeichenkonzept (`CONTRADICTS` $\to$ `USES_ACCIDENTAL_SPELLING`).
   * `CR-015`: Nichtakkordeigener Slash-Bass wie $C/F\sharp$ ist keine Umkehrung (`IS_VARIANT_OF` $\to$ `NON_CHORD_BASS_OVER`).
   * `CR-001`: Schall und Frequenz setzen nicht zwingend ISO 16 voraus (`REQUIRES` $\to$ `CALIBRATED_BY`).
   * `CR-004`: Vorzeichen existieren auch ohne Fünfliniensystem (`REQUIRES` $\to$ `VISUALIZED_IN`).
   * `CR-008`: Intervalle erfordern kein 12-TET (`REQUIRES` $\to$ `QUANTIZED_IN`).
   * `CR-017`: Riemann- und Stufentheorie bilden keine Bijektion (`IS_EQUIVALENT_UNDER` $\to$ `PRIMARY_TRIADS_I_IV_V_IN_MAJOR_ONLY`).
   * `CR-028`: Akustisches Drumkit implementiert nicht MIDI (`IMPLEMENTED_BY` $\to$ `MAPPED_IN_PROFILE`).

3. **Didaktische Heuristiken als harte Strukturgesetze missverstanden:**
   * Historische Fingersätze (`CR-034`), Linke-Hand-Bass (`CR-035`), Einstieg Klaviatur (`CR-037`), Reggae Skank (`REL-009`), Akkorderkennung (`REL-013`), Umkehrungs-Lerntransfer (`REL-019`) und Picardische Terz (`REL-025`) wurden fälschlich als `REQUIRES`- oder `FOUNDATIONAL_FOR`-Relationen deklariert.

4. **Modell- und Richtungsfehler:**
   * `CR-038`: Klaviermodul P12 ($Dm9$) vs. PROG-028 ($Em9$) kollidieren ohne explizite Ganztontransposition (`REQUIRES_TRANSPOSITION_TO_E_MINOR`).
   * `REL-004`: Drop-2 ist bei enger Ausgangslage nicht $L_1$-minimal (Distanz 7 vs. 3).
   * `CDR-011` / `CDR-012`: In PROG-024 löst $D7$ nach $Dm7$ auf (keine Sekundärdominanten-Auflösung nach $G$); der Knotenname `MODAL_SHIFT_TO_II7` dreht die tatsächliche Richtung ($II7 \to ii7$) fälschlich um.
   * `REL-012`: Das Jazz-Swing-Modul P09 / PAT-012 wurde paradoxerweise mit der UK-Garage-Probe `CHARLESTON_UKG_OVERLAY` geprüft.
   * `REL-020`: Vermengt P10 (Bass-First) und P11 (Umkehrungen) sowie zwei Versionen von `ERR-026`.

5. **Einheiten- und Bezugsraster beim Swing (480 PPQ):**
   * Die Ticks 139, 146 und 154 (58%, 61%, 64%) beziehen sich zwingend auf ein **16tel-Paar von 240 Ticks** (gerader Mittelpunkt 120). Auf ein 8tel-Paar (480 Ticks) bezogen ergäben 58%/61% 278/293 Ticks.

6. **Governance-Fehler in den Audit-Matrizen v1/v2:**
   * Bei 30 gepatchten Zeilen blieb in `relation_type` der widerlegte Ursprungstyp stehen.
   * 10 Zeilen mit `technical_status = NOT_EXECUTED` und 4 Zeilen mit ungelösten Knoten (`UNRESOLVED`: CDR-012, CDR-014, CDR-019, CDR-021) wurden fälschlich auf `production_use_allowed = True` gesetzt.

---

## 2. Detaillierte Synopse der fehlerhaften Relationen

| Relation-ID | Ursprüngliche Kante | Bestätigter Fachbefund | Korrigierte Kante (v3) | Produktionsfreigabe (v3) |
|---|---|---|---|:---:|
| **CDR-010** | `POLYCHORD_D_OVER_C EXPRESSES C_MAJ13_SHARP11` | D/C enthält kein H (7). Ist $C^{6/9(\sharp 11)}$ oder Teilvoicing. | `POLYCHORD_D_OVER_C PARTIAL_VOICING_OF C_MAJ13_SHARP11` | `False` (gesperrt) |
| **CR-024** | `M07-01 REQUIRES M01-01` | Metrische Pulsgruppierung unabhängig von Schwingungsfrequenz. | `M07-01 EMERGES_FROM TEMPORAL_EVENT_STREAM` | `False` (gesperrt) |
| **CR-001** | `M01-01 REQUIRES M01-02` | Schall/Frequenz setzt nicht ISO 16 voraus. | `M01-01 CALIBRATED_BY M01-02` | `True` (mit Scope) |
| **CR-002** | `M01-03 IS_VARIANT_OF M01-05` | Oktave ist Basisintervall, kein Stimmungssystem. | `M01-03 DEFINES_EQUIVALENCE_IN M01-05` | `True` (mit Scope) |
| **CR-004** | `M02-04 REQUIRES M02-01` | Vorzeichen existieren ohne Liniensystem. | `M02-04 VISUALIZED_IN M02-01` | `True` (mit Scope) |
| **CR-006** | `M02-05 CONTRADICTS M02-04` | Enharmonik widerspricht Vorzeichen nicht. | `M02-05 USES_ACCIDENTAL_SPELLING M02-04` | `True` (mit Scope) |
| **CR-008** | `M03-01 REQUIRES M01-04` | Intervalle erfordern kein 12-TET-Raster. | `M03-01 QUANTIZED_IN M01-04` | `True` (mit Scope) |
| **CR-015** | `M04-08 IS_VARIANT_OF M04-02` | Nichtakkordeigener Bass ist keine Umkehrung. | `M04-08 NON_CHORD_BASS_OVER M04-02` | `True` (mit Scope) |
| **CR-017** | `M05-02 IS_EQUIVALENT_UNDER M05-01` | Riemann und Stufen bilden keine Bijektion. | `M05-02 IS_EQUIVALENT_UNDER M05-01` (Scope: Primary Triads) | `True` (mit Scope) |
| **CR-028** | `M08-01 IMPLEMENTED_BY M08-02` | Akustisches Drumkit implementiert kein MIDI. | `M08-01 MAPPED_IN_PROFILE M08-02` (GM1 Ch. 10) | `True` (mit Scope) |
| **CR-038** | `PROG-028 VOICED_BY P12` | P12 auf Dm9, PROG-028 auf Em9. | `PROG-028 VOICED_BY P12` (Scope: Transposition needed) | `True` (mit Scope) |
| **REL-004** | `PROG-003 VOICED_BY P08` | Drop-2 nur im vorgegebenen Suchraum minimal. | `PROG-003 VOICED_BY P08` (Scope: DROP2_SEARCH_SPACE) | `True` (mit Scope) |
| **REL-012** | `P09 TRAINS_RHYTHMIC_INTERACTION PAT-012` | Mit UKG-Probe geprüft statt Jazz-Swing. | `P09 PRACTICE_PAIRING PAT-012` (Probe korrigiert) | `False` (bis Swing-Probe) |
| **REL-020** | `P11 PREVENTS_ERROR ERR-026` | P10 vs P11 und Doppelbelegung ERR-026. | `P11 PREVENTS_ERROR_IN_VERSION ERR-026@v4.8` | `False` (Review nötig) |
| **CDR-011** | `PROG_024 HARMONIC_FUNCTION APPLIED_DOMINANT` | D7 löst nach Dm7 auf, nicht nach G. | `PROG_024 CHORD_MORPHOLOGY V7_OF_V` | `True` (mit Scope) |
| **CDR-012** | `PROG_024 VOICE_LEADING MODAL_SHIFT_TO_II7` | Richtung ist II7 nach ii7; Name verdreht. | `PROG_024 VOICE_LEADING SAME_ROOT_DOMINANT_TO_MINOR_SEVENTH` | `False` (unresolved) |
| **CDR-014** | `PROG_025 RHYTHMIC_EXECUTION MONTUNO` | Montuno als STEPS-Übung ohne Clave-Anspruch. | `PROG_025 STEPS_OWN_EXERCISE PIANO_MONTUNO` | `False` (Hörprobe offen) |
| **CDR-019** | `BOSSA_BATIDA HISTORICAL_ORIGIN SYNTHESIS` | O Cruzeiro pim079 erwähnt keine Tamborim-Synthese. | `BOSSA_BATIDA ATTRIBUTED_INTERPRETATION SYNTHESIS` | `False` (unbeschafft) |
| **CDR-021** | `SURDO_PULSE PERFORMANCE_NORM ACCENT_ON_2` | Marcelino 2010 beschreibt Escola-Rolle, keine Norm. | `SURDO_PULSE ROLE_IN_BATERIA SURDO_DE_PRIMEIRA` | `False` (Dynamik offen) |

---

## 3. Umsetzung und Bereinigung in `GRAPH_AUDIT_MATRIX_v3.csv`

Die folgenden konkreten Korrekturschritte wurden formal und technisch umgesetzt:

1. **Typ-Synchronisation:** In allen Zeilen mit vorliegendem Patch wurde `proposed_relation_type` direkt in die Primärspalte `relation_type` übernommen.
2. **Freigabe-Härtung (Schutz vor fehlerhaftem Import):** Alle 10 `NOT_EXECUTED`-Zeilen sowie alle 4 `UNRESOLVED`-Knoten (CDR-012, CDR-014, CDR-019, CDR-021) wurden auf `production_use_allowed = False` gesetzt.
3. **Sperrung der Sachfehler:** CDR-010 und CR-024 verbleiben strikt auf `False` (`DEPRECATED` / `REJECTED`).
4. **Entkopplung der Testprobe in REL-012:** `CHARLESTON_UKG_OVERLAY` wurde entfernt und durch die geplante Jazz-Swing-Probe `CHARLESTON_SWING_OVERLAY` ersetzt.
5. **Klarstellung des Swing-Bezugssystems:** Ergänzung der Scope-Definitionen für alle Microtiming-Kanten (16tel-Paar = 240 Ticks).
