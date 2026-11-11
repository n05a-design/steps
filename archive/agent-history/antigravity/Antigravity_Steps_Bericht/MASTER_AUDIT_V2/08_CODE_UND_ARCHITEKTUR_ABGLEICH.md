# STEPS – IMPLEMENTIERUNGS- UND ARCHITEKTURABGLEICH
## Detaillierter Abgleich des Python-Theoriekerns, Einhaltung der ADRs und Entkopplung von Glide

**Prüfdatum:** 11. November 2026  
**Untersuchter Quellcode:** `src/steps/theory/` und `src/steps/progression/` (25 Python-Dateien)  

---

## 1. Architektur des STEPS-Kerns

```
src/steps/
├── theory/
│   ├── __init__.py           # Re-Exports der Domänenklassen
│   ├── exceptions.py         # Vollständige Exception-Hierarchie
│   ├── pitch.py              # PitchClass, Pitch, Frequenzen, Spelling
│   ├── interval.py           # Interval, Qualität, Umkehrung, Arithmetik
│   ├── triad.py              # Triad, TriadQuality, Umkehrungen
│   ├── seventh.py            # SeventhChord, SeventhQuality, Umkehrungen
│   └── chord.py              # Allgemeine Chord-Klasse, Stufen, Slash
└── progression/
    ├── __init__.py           # Re-Exports der Progressions-Engine
    ├── voice_leading.py      # Stimmführung, Parallelenprüfung, Tymoczko
    ├── canonical_progressions.py # 28 kanonische Archetypen (PROG-001..028)
    └── engine.py             # ProgressionEngine, Transposition, Validierung
```

---

## 2. Entkopplung von Glide 3.53 (Regel 4 & 9)

Ein zentraler Prüfpunkt war die vollständige Trennung von der Glide-Codebasis (`src/glide-v3.53/`):
- **Statische Codeanalyse:** Suche nach Importen von `glide`, `app.pyw`, `tkinter` in `src/steps/`.
- **Ergebnis:** **EXAKT 0 IMPORTE**.
- Der STEPS-Kern ist 100% rein, nutzt ausschließlich die Standardbibliothek (`math`, `re`, `enum`, `dataclasses`, `typing`) und läuft vollständig headless auf jedem Betriebssystem.

---

## 3. Entwurfsprinzipien und Code-Qualität

1. **Unveränderlichkeit (Immutability):** Alle Domänenobjekte (`Pitch`, `Interval`, `Triad`, `Chord`) sind als unmutable Dataclasses (`frozen=True`) oder zustandsfreie Rechenmodelle konzipiert.
2. **Defensive Programmierung & Exception-Design:** Keine stillschweigenden Rechenfehler. Spezialisierte Fehlerklassen (`PitchParseError`, `InvalidIntervalError`, `ChordConstructionError`, `ScaleDegreeError`) garantieren präzise Fehlermeldungen.
3. **Enharmonische Orthographie:** Strikte Wahrung des Unterschieds zwischen Tonklasse (Halbtonindex $0..11$) und musikalischer Schreibweise ($C\sharp$ vs. $Dlat$).
4. **Zwei-Wege-Konvertierung:** Unterstützung sowohl internationaler ($B/Blat$) als auch traditioneller deutscher Notation ($H/B$).
