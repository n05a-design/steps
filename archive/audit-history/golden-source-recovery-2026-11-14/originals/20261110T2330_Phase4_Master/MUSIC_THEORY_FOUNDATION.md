# STEPS – MUSIKTHEORETISCHE BASIS & AXIOME (MUSIC THEORY FOUNDATION)
**Status:** CANONICAL THEORY REFERENCE  
**Wissensdomänen:** M01 (Grundlagen), M02 (Notation), M03 (Intervalle), M04 (Akkorde), M05 (Harmonielehre)

---

## 1. Mathematische & Physikalische Axiome

### Axiom 1: Das Oktavverhältnis
Zwei Töne stehen genau dann im Oktavabstand zueinander, wenn sich ihre Schwingungsfrequenzen exakt wie $2:1$ verhalten:
$$f(p + 12) = 2 \cdot f(p)$$
wobei $p$ die Tonhöhe in Halbtonschritten darstellt.

### Axiom 2: Gleichstufige 12-Ton-Temperatur (12-TET)
Die Oktave wird in genau 12 logarithmisch gleich große Halbtonschritte unterteilt. Der Frequenzfaktor eines Halbtonschritts beträgt:
$$\alpha = \sqrt[12]{2} = 2^{1/12} \approx 1{,}059463094$$
Die Frequenz einer MIDI-Note $m \in \{0, 1, \dots, 127\}$ berechnet sich bezüglich des Standard-Kammertons $A_4$ (MIDI 69 = 440 Hz) wie folgt:
$$f(m) = 440 \cdot 2^{\frac{m - 69}{12}}\text{ Hz}$$

### Axiom 3: Tonklassen und die zyklische Gruppe $\mathbb{Z}_{12}$
Jede Tonhöhe induziert eine Tonklasse (Pitch Class) durch Projektion modulo 12:
$$\pi(m) = m \pmod{12} \in \mathbb{Z}_{12} = \{0, 1, 2, \dots, 11\}$$
Die Transposition um $k$ Halbtöne ist ein Gruppenautomorphismus in $(\mathbb{Z}_{12}, +)$:
$$T_k(x) = (x + k) \pmod{12}$$

---

## 2. Diatonik, Notenschreibung & Enharmonik

### Diatonische Schritte vs. Chromatische Halbtöne
Im Gegensatz zur reduzierten Tonklasse $\mathbb{Z}_{12}$ besitzt die westliche Musiknotation eine heptatonische Basis mit 7 diatonischen Stammtonschritten:
$$\text{DiatonicStep} \in \{\text{C}, \text{D}, \text{E}, \text{F}, \text{G}, \text{A}, \text{B}\}$$
Jeder Stammton kann durch ein Vorzeichen (Alteration $\delta \in \{-2, -1, 0, +1, +2\}$) modifiziert werden:
$$\text{Pitch}(s, \delta) = \text{BasePitch}(s) + \delta$$

### Der Leitsatz der Enharmonik
> **Satz (Enharmonische Nicht-Identität):**  
> Zwei Noten mit gleicher Tonklasse $\pi(n_1) = \pi(n_2)$ sind unter 12-TET **akustisch äquivalent**, aber in einem tonalen Kontext **syntaktisch und funktional distinkt**.  
> **Beispiel:**  
> In $D$-Dur ist $C\sharp$ der leittonartige 7. Skalengrad ($7\uparrow$), der sich aufwärts nach $D$ auflöst. Die Note $D\flat$ wäre eine erniedrigte Tonika ($\flat 1$), die syntaktisch im Dur-Kontext ungültig ist.

---

## 3. Intervalltheorie

Ein Intervall wird durch zwei orthogonale Eigenschaften bestimmt:
1. **Diatonischer Schrittabstand** (Prim, Sekunde, Terz, Quarte, Quinte, Sexte, Septime, Oktave).
2. **Intervallqualität** (Rein, Groß, Klein, Übermäßig, Vermindert).

| Diatonischer Name | Halbtonschritte | Standardqualität | Komplementär-Intervall (Umkehrung) |
| :--- | :--- | :--- | :--- |
| Reine Prime | 0 | Rein | Reine Oktave (12) |
| Kleine Sekunde | 1 | Klein | Große Septime (11) |
| Große Sekunde | 2 | Groß | Kleine Septime (10) |
| Kleine Terz | 3 | Klein | Große Sexte (9) |
| Große Terz | 4 | Groß | Kleine Sexte (8) |
| Reine Quarte | 5 | Rein | Reine Quinte (7) |
| Tritonus (überm. 4 / verm. 5) | 6 | Übermäßig / Vermindert | Tritonus (6) |
| Reine Quinte | 7 | Rein | Reine Quarte (5) |
| Kleine Sexte | 8 | Klein | Große Terz (4) |
| Große Sexte | 9 | Groß | Kleine Terz (3) |
| Kleine Septime | 10 | Klein | Große Sekunde (2) |
| Große Septime | 11 | Groß | Kleine Sekunde (1) |
| Reine Oktave | 12 | Rein | Reine Prime (0) |

---

## 4. Akkordqualitäten und mathematische Terzschichtung

Ein Dreiklang besteht aus Grundton (Root), Terz (Third) und Quinte (Fifth).  
Die Akkordqualität ergibt sich strikt aus den Intervallabständen zum Grundton:

| Akkordtyp | Symbol | Intervallstruktur (Halbtöne) | Intervallnamen | Tonklassen-Vektor (auf C) |
| :--- | :--- | :--- | :--- | :--- |
| **Dur** (Major) | C, Cmaj | `[0, 4, 7]` | Grundton, große Terz, reine Quinte | `[0, 4, 7]` (C, E, G) |
| **Moll** (Minor) | Cm, C- | `[0, 3, 7]` | Grundton, kleine Terz, reine Quinte | `[0, 3, 7]` (C, Eb, G) |
| **Vermindert** (Diminished) | Cdim, C° | `[0, 3, 6]` | Grundton, kleine Terz, verminderte Quinte | `[0, 3, 6]` (C, Eb, Gb) |
| **Übermäßig** (Augmented) | Caug, C+ | `[0, 4, 8]` | Grundton, große Terz, übermäßige Quinte | `[0, 4, 8]` (C, E, G#) |
| **Suspendiert 4** | Csus4 | `[0, 5, 7]` | Grundton, reine Quarte, reine Quinte | `[0, 5, 7]` (C, F, G) |
| **Suspendiert 2** | Csus2 | `[0, 2, 7]` | Grundton, große Sekunde, reine Quinte | `[0, 2, 7]` (C, D, G) |

### Vierklänge / Septakkorde

| Akkordtyp | Symbol | Intervallstruktur | Tonklassen-Vektor (auf C) |
| :--- | :--- | :--- | :--- |
| **Dur-Septakkord** | Cmaj7, CΔ | `[0, 4, 7, 11]` | `[0, 4, 7, 11]` (C, E, G, B) |
| **Dominantseptakkord** | C7 | `[0, 4, 7, 10]` | `[0, 4, 7, 10]` (C, E, G, Bb) |
| **Moll-Septakkord** | Cm7 | `[0, 3, 7, 10]` | `[0, 3, 7, 10]` (C, Eb, G, Bb) |
| **Halbvermindert** | Cm7b5, Cø | `[0, 3, 6, 10]` | `[0, 3, 6, 10]` (C, Eb, Gb, Bb) |
| **Vollvermindert** | Cdim7, C°7 | `[0, 3, 6, 9]` | `[0, 3, 6, 9]` (C, Eb, Gb, Bbb/A) |

---

## 5. Harmonische Funktionen & Kadenzen

### Diatonische Stufenakkorde in Dur
In einer Dur-Tonleiter (z. B. $C$-Dur) ergeben die Terzschichtungen auf den 7 Skalengraden:

| Stufe | Römisch | Grundton (C-Dur) | Dreiklangstyp | Septakkord | Riemann-Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **I** | C | Dur | Maj7 | **Tonika (T)** |
| 2 | **ii** | D | Moll | m7 | **Subdominant-Parallele (Sp)** |
| 3 | **iii** | E | Moll | m7 | **Dominant-Parallele / Tonika-Gegenklang (Dp/Tg)** |
| 4 | **IV** | F | Dur | Maj7 | **Subdominante (S)** |
| 5 | **V** | G | Dur | 7 | **Dominante (D)** |
| 6 | **vi** | A | Moll | m7 | **Tonika-Parallele (Tp)** |
| 7 | **vii°** | B (dt. H) | Vermindert | m7b5 | **Verkürzter Dominantseptakkord ($\rlap{/}D^7$)** |

### Grundregeln der Stimmführung (Voice Leading)
1. **Gemeinsame Töne:** Bleiben nach Möglichkeit in derselben Stimme liegen.
2. **Kürzester Weg:** Bewegte Stimmen schreiten vorzugsweise in Sekundschritten (Halb- oder Ganzton) fort.
3. **Leittonauflösung:** Der 7. Skalengrad (Leitton) strebt mit starker melodischer Energie aufwärts in den Grundton ($7 \to 8/1$).
4. **Septimauflösung:** Die Dissonanz der Septime in Dominantakkorden löst sich stufenweise abwärts auf ($4 \to 3$).
