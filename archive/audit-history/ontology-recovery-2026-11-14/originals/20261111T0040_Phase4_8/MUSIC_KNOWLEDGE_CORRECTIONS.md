# STEPS – Fachliche Fehlerkorrekturen: Phase 4.8 (ERR-024 bis ERR-027)

**Dokumenttyp:** FORMAL AUDIT OF THEORETICAL ERRORS & ACCURACY UPGRADES  
**Wissensdomänen:** M02 (Notation), M04 (Akkorde), M05 (Harmonielehre), M07 (Rhythmik), M10 (Klavier), M12 (Didaktik)  
**Status:** `FORMAL_VERIFIED` / `THEORY_SUPPORTED`

---

## ERR-024 – Swing-Verhältnis, Prozentwert und Tick-Offsets im UK Garage

### 1. Befund der Fehleranalyse:
In Phase 4.7 wurden im UK-Garage-Profil folgende Werte parallel genannt:
- „55–62% Swing“
- „Ratio $\rho \approx 1{,}32$“
- „Verschiebung um $+24$ Ticks“
- „Zweite 16tel auf Tick 144“
- „bei 480 PPQ“

Diese Angaben sind rechnerisch nicht konsistent.

### 2. Mathematische Grundlagen der 16tel-Swing-Quantisierung (480 PPQ):
Bei einer Division von 480 PPQ dauert eine Viertelnote 480 Ticks. Ein Paar von zwei Sechzehntelnoten umfasst:
$$T_{\text{pair}} = 240\text{ Ticks}$$
Ein Swing-Prozentsatz $P \in [50\%, 75\%]$ (wie in MPC-, Logic- oder Ableton-Groove-Pools definiert) teilt diesen Zeitraum so auf, dass die erste Note $t_1 = 240 \cdot P$ Ticks dauert und die zweite Note um $\Delta = t_1 - 120$ Ticks nach hinten verschoben wird:

| Swing % ($P$) | Dauer Note 1 ($t_1$) | Tick Note 2 ($t_1$) | Offset ($\Delta$) | Exakte Swing-Ratio ($\rho = \frac{t_1}{t_2}$) |
|---|---|---|---|---|
| **50 % (Straight)** | 120 Ticks | **Tick 120** | $0$ Ticks | **$1{,}00 : 1$** |
| **55 %** | 132 Ticks | **Tick 132** | $+12$ Ticks | **$1{,}22 : 1$** |
| **56,9 %** | 136,55 Ticks | **Tick 137** | $+17$ Ticks | **$1{,}32 : 1$** (Hier lag die Ratio 1,32!) |
| **58 % (Typisch UKG)** | 139,2 Ticks | **Tick 139** | $+19$ Ticks | **$1{,}38 : 1$** |
| **60 % (Tick-144)** | 144 Ticks | **Tick 144** | **$+24$ Ticks** | **$1{,}50 : 1$** |
| **62 %** | 148,8 Ticks | **Tick 149** | $+29$ Ticks | **$1{,}63 : 1$** |
| **66,7 % (Triolen)** | 160 Ticks | **Tick 160** | $+40$ Ticks | **$2{,}00 : 1$** (Ternärer Shuffle) |

### 3. Auflösung & Korrektur:
- Die Platzierung der zweiten Sechzehntel auf **Tick 144** entspricht exakt **$60\%$ Swing** ($\rho = 1{,}50$).
- Die Ratio **$1{,}32 : 1$** entspricht ca. **$57\%$ Swing** (Tick 137).
- Ein **$58\%$ Swing** landet auf **Tick 139** ($\rho \approx 1{,}38$).
- **Korrektur für STEPS:** Alle drei Größen werden in `GENRE_RESEARCH_UK_GARAGE.md`, `PAT-020` und `REF-0053` sauber getrennt. Wenn Tick 144 verwendet wird, ist dies verbindlich als **60% Swing ($\rho = 1{,}50$, Offset $+24$ Ticks)** deklariert.

---

## ERR-025 – Tonalitätsbestimmung der Fallstudie "Horizon Drift"

### 1. Befund der Fehleranalyse:
In Phase 4.7 wurde die Progression:
$$Dm^9 \;\longrightarrow\; B\flat^{\text{maj}7} \;\longrightarrow\; Gm^7 \;\longrightarrow\; C^{\text{add}9}$$
als „D-Dorisch / D-Aeolisch modale Sphäre“ beschrieben.

### 2. Harmonische Tonleiterprüfung:
- Tonvorrat der Akkorde:
  - $Dm^9$: $\{D, E, F, A, C\}$
  - $B\flat^{\text{maj}7}$: $\{B\flat, D, F, A\}$
  - $Gm^7$: $\{G, B\flat, D, F\}$
  - $C^{\text{add}9}$: $\{C, D, E, G\}$
- Vereinigungsmenge aller Tonklassen:
  $$\text{PC}_{\text{total}} = \{D, E, F, G, A, B\flat, C\}$$
- **Skalenvergleich:**
  - **D-Aeolisch (Reines Moll):** $D - E - F - G - A - \mathbf{B\flat} - C$ (exakte Übereinstimmung!).
  - **D-Dorisch:** $D - E - F - G - A - \mathbf{B\natural} - C$.
- Da $B\flat^{\text{maj}7}$ und $Gm^7$ zwingend die kleine Sexte $B\flat$ erfordern, schließt die harmonische Progression die dorische Skala aus. Ein $B\natural$ kommt in den Akkorden nirgends vor.
- **Korrektur:** Die Fallstudie „Horizon Drift“ wird eindeutig als **D-Aeolisch** ($\text{i}^9 - \flat\text{VI}^{\text{maj}7} - \text{iv}^7 - \flat\text{VII}^{\text{add}9}$) klassifiziert. Der irreführende Begriff „Dorisch“ wird ersatzlos gestrichen.

---

## ERR-026 – "Bass First" und funktionale Mehrdeutigkeit (Modul P10)

### 1. Befund der Fehleranalyse:
In Modul P10 wurde die didaktische Aussage getroffen: „Der Bass ist der Dirigent der Harmonie. Wenn der Bassist vom Grundton C nach F springt, weißt du sofort: Die Reise geht zur 4. Stufe (Subdominante)!“  
Dies vermittelt Anfängern ein falsches Absolutheitsgefühl, da der Basston allein die harmonische Funktion nicht eindeutig festlegt.

### 2. Musiktheoretische Einschränkungen des Basstons:
1. **Akkordumkehrungen:**  
   Ein Basston $E$ kann der Grundton von $Em$ ($iii$) sein, aber ebenso die Terz von $C$-Dur in 1. Umkehrung ($C/E$, Tonika) oder die Quinte von $Am$ in 2. Umkehrung ($Am/E$).
2. **Pedalbass (Orgelpunkt):**  
   Ein liegender Basston $C$ unter $F/C \to G/C \to C$ ändert seine harmonische Funktion trotz statischem Bass kontinuierlich von Tonika zu Subdominante zu Dominante.
3. **Slash-Chords & Durchgangsnoten:**  
   Ein Bassist spielt häufig chromatische Durchgangstöne oder Quintentriolen, die rein melodischer Natur sind.

### 3. Didaktische Korrektur in P10:
Die „Bass-First“-Regel wird präzisiert:
- Der Bass liefert die **fundamentale Bewegungslinie** (die tonale Verankerung).
- Die **tatsächliche harmonische Funktion** ergibt sich erst aus der **Kombination des Basstons mit der Terz (Dur/Moll) und den Oberstimmen** (Erkennung von Umkehrungen).

---

## ERR-027 – Wissensgraph-Vollständigkeit & Relationen-Konsolidierung

### 1. Befund der Fehleranalyse:
In Phase 4 Master existierten **37 fundamentale Konzeptrelationen** (`CR-001` bis `CR-037`), die theoretische Invarianten zwischen den Modulen M01–M12 formal abbildeten.  
In Phase 4.7 wurde eine neue Datei `MUSIC_CONCEPT_RELATIONS.csv` erstellt, die jedoch nur **13 objektbezogene Relationen** (`REL-001` bis `REL-013`) enthielt. Die 37 früheren Relationen wurden dabei versehentlich nicht mitgeführt.

### 2. Korrektur & Vereinigung:
In Phase 4.8 werden beide Bestände in einer gemeinsamen, vollständigen Wissensgraph-Datei `MUSIC_CONCEPT_RELATIONS.csv` vereint:
1. **37 Konzept-Relationen (`CR-001` bis `CR-037`):** Axiomatische und theoretische Abhängigkeiten zwischen Konzepten M01-M12.
2. **13 Cross-Domain-Objekt-Relationen (`REL-001` bis `REL-013`):** Relationen zwischen PROG, PAT und P-Modulen.
3. **7 neue Relationen aus Phase 4.8 (`REL-014` bis `REL-020`):** Einbindung von D&B- und UKG-Grooves in den Wissensgraphen.
- **Gesamtbestand:** **57 lückenlos erhaltene und validierte Relationen!**
