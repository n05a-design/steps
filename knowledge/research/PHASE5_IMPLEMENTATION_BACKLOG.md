# STEPS – Phase 5 Implementation Backlog & Module Specifications (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** SPECIFICATION-COMPLETE & READY FOR IMPLEMENTATION (Post-ADR)  
**Autor:** Leitender Software-Architekt  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil VIII (Abschnitt 8.2)  

---

## 1. Technischer Geltungsbereich (Scope STEPS v0.1 Core)

Gemäß `ADR-002` umfasst das erste Release (STEPS v0.1) ausschließlich den **reinen, testbaren und framework-unabhängigen Harmonielehre-Kern** unter `src/steps/theory/` und `src/steps/progression/`.

### Qualitäts- und Domänenregeln:
- **Null GUI-Abhängigkeiten:** Keine Imports von `tkinter`, `PyQt`, `wx` oder Web-Frameworks im Core.
- **Null Audio-Hardware-Abhängigkeiten:** Reine mathematische Logik in $\mathbb{Z}_{12}$ und wissenschaftlichen Datenstrukturen.
- **100 % Type-Annotiert:** Vollständige Python 3 Type-Hints mit `mypy`-Kompatibilität.
- **Direkte Rückführbarkeit:** Jede Funktion korrespondiert mit einem Golden Reference Case und einer formalen Regel.

---

## 2. Modul-Spezifikationen im Backlog

### Modul 1: `src/steps/theory/pitch.py` (Akustik, Pitch Classes & Enharmonik)
* **Fachliche Spezifikation:** M01, M02
* **Abhängige ADR:** `ADR-005` (Fachmodell Notationskonventionen)
* **Funktionen / Klassen:**
  - `class PitchClass(int)`: Modulo-12 Restklasse ($0 \le p \le 11$).
  - `class NoteSpelling`: Speichert Grundtonbuchstabe (`C`, `D`, `E`, `F`, `G`, `A`, `B` / `H`), Vorzeichen (`#`, `b`, `bb`, `x`, `n`) und Oktavlage ($m \in [0, 127]$).
  - `midi_to_pitch_class(midi_note: int) -> PitchClass`: $p = m \pmod{12}$.
  - `midi_to_frequency(midi_note: int, a4_ref: float = 440.0) -> float`: ISO 16 Berechnung $f = a_4 \cdot 2^{\frac{m-69}{12}}$.
  - `render_spelling(spelling: NoteSpelling, convention: str = 'INT') -> str`: Gibt je nach Konvention internationales `Bb` oder deutsches `B` bzw. `B` oder `H` aus.
* **Golden Reference Cases:** `REF-0001`, `REF-0002`, `REF-0107`, `REF-0108`, `REF-0111`, `REF-0112`.
* **Negative Gegenprobe:** Verletzung von Modulo-12 ($p \ge 12$) oder unzulässige enharmonische Verwechslung ($C\sharp \ne D\flat$ im Kontrapunkt) wirft `ValueError`.

### Modul 2: `src/steps/theory/interval.py` (Intervalle & Symmetrien)
* **Fachliche Spezifikation:** M03
* **Funktionen / Klassen:**
  - `class Interval(Enum)`: `P1` (0), `m2` (1), `M2` (2), `m3` (3), `M3` (4), `P4` (5), `TT` (6), `P5` (7), `m6` (8), `M6` (9), `m7` (10), `M7` (11), `P8` (12).
  - `semitones_between(n1: int, n2: int) -> int`: Absolute Halbtondistanz $|n_2 - n_1|$.
  - `invert_interval(semitones: int) -> int`: Modulo-12 Inversion $(12 - (s \pmod{12})) \pmod{12}$.
* **Golden Reference Cases:** `REF-0003`, `REF-0004`, `REF-0115` bis `REF-0122`.
* **Property-Based Invariante:** $i + \text{invert}(i) \equiv 0 \pmod{12}$.

### Modul 3: `src/steps/theory/triad.py` & `seventh.py` (Akkordkonstruktion & Voicings)
* **Fachliche Spezifikation:** M04
* **Funktionen / Klassen:**
  - `construct_triad(root: PitchClass, quality: TriadQuality) -> list[PitchClass]`: Erzeugt Dur `[0, 4, 7]`, Moll `[0, 3, 7]`, Vermindert `[0, 3, 6]`, Übermäßig `[0, 4, 8]`, Sus4 `[0, 5, 7]`, Sus2 `[0, 2, 7]`, Add9 `[0, 2, 4, 7]`.
  - `construct_seventh(root: PitchClass, quality: SeventhQuality) -> list[PitchClass]`: Erzeugt Dominantsept `[0, 4, 7, 10]`, Major7 `[0, 4, 7, 11]`, Minor7 `[0, 3, 7, 10]`, Halbvermindert `[0, 3, 6, 10]`, Vermindert `[0, 3, 6, 9]`, Lydisch Dominant $7\sharp 11$ `[0, 4, 6, 10]`.
  - `invert_chord(voicing: list[int], inversion: int) -> list[int]`: Akkordumkehrungen (Grundstellung, 1. Umkehrung, 2. Umkehrung, 3. Umkehrung).
* **Golden Reference Cases:** `REF-0012`, `REF-0013`, `REF-0035`, `REF-0050`, `REF-0138` bis `REF-0145`.

### Modul 4: `src/steps/progression/voice_leading.py` (Stimmführung & Metriken)
* **Fachliche Spezifikation:** M05, M06, M10
* **Funktionen / Klassen:**
  - `circular_pc_distance(v1: list[int], v2: list[int]) -> int`: Zirkuläre Distanz auf dem Tonklassenkreis nach Tymoczko (2011).
  - `absolute_semitone_distance(v1: list[int], v2: list[int]) -> int`: Euklidische Distanz im Halbtonraum $\sum |v_{2,i} - v_{1,i}|$.
  - `detect_voice_crossing(voicing: list[int]) -> bool`: Erkennt unzulässige Stimmkreuzungen ($v_i > v_{i+1}$).
  - `detect_parallel_fifths_octaves(c1: list[int], c2: list[int]) -> list[str]`: Erkennt verdeckte und parallele Quinten/Oktaven im vierstimmigen Satz.
* **Golden Reference Cases:** `REF-0019`, `REF-0095`, `REF-0096`, `REF-0097`.
