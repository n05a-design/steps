# STEPS – Modulares Musiktheorie- und Kompositionssystem

STEPS ist ein modulares, rein in Python implementiertes Open-Source-System für Musiktheorie, funktionale Harmonielehre, Kadenzanalyse, Stimmführung und Kompositionsunterstützung.

**Version:** 0.1.0-alpha (Headless Music Theory Core)  
**Lizenz:** Mozilla Public License 2.0 (MPL-2.0)  
**Projektstatus:** Phase 5.1 abgeschlossen / 100% verifizierter Theorie- und Progressionskern  

---

## 1. Systemübersicht & Kernarchitektur

STEPS trennt Fachmodell, Wissensbasis und spätere Nutzeroberflächen strikt nach ISO/IEC 25010 und Clean Architecture Grundsätzen:

```
steps/
├── .github/          # CI/CD Multi-OS & Multi-Python Workflows
├── .agents/          # Antigravity Curation & Development Skills
├── app/              # Desktop UI Shell Scaffold (v0.3)
├── archive/          # Revisionssicheres historisches Archiv
├── decisions/        # Kanonische Architekturentscheidungen (ADR-001..012)
├── docs/             # Entwicklungs- und Systemdokumentation
├── knowledge/        # Gepflegte Wissensbasis, Ontologie & Golden Cases
├── research/         # Musikologische Forschung & Korpora
├── scripts/          # Verifikations-, Test- und Kuratierungs-Tools
├── src/steps/        # Pure Python Musiktheorie- und Progressions-Kern
│   ├── theory/       # Pitch, Interval, Triad, Seventh, Chord Engine
│   └── progression/  # Stimmführung, 28 Progressionen, Harmonic Engine
└── tests/            # 115 automatisierte Unittests (100% grün)
```

---

## 2. Kernfunktionen des STEPS-Theoriekerns (`src/steps/`)

* **Mathematisches Domänenmodell ($Z_{12}$):** Modulo-12-Arithmetik, Frequenzberechnung ($A_4 = 440\,	ext{Hz}$), zyklische Gruppen und vollständige enharmonische Orthographie (diatonische Stufen und Alterationen).
* **Zwei-Wege-Notationssystem:** Vollständige Unterstützung internationaler ($B/Blat$) und deutscher Notenkonventionen ($H/B$).
* **Akkord-Engine:** Konstruktion und Parsen von Dreiklängen, Vierklängen, Sus-/Add-Akkorden, Extensions (9, 11, 13, alteriert), Slash Chords und Stufenakkorden.
* **28 kanonische Progressionen:** Vollständige Abdeckung aller klassischen, Jazz- und Pop-Archetypen (II-V-I, Andalusische Kadenz, Pop-Punk, Coltrane Changes, Rhythm Changes, Modal Vamps).
* **Stimmführungs-Solver:** Kontrapunktische Validierung (Parallelenvermeidung, Stimmkreuzungserkennung) und Optimierung nach der Tymoczko-Metrik $\sum |midi(v_{2,i}) - midi(v_{1,i})|$.
* **Zero External Dependencies:** Der Kern benötigt für Ausführung und Tests **ausschließlich die Python Standardbibliothek**.

---

## 3. Schnellstart & Testausführung

```bash
# 1. Repository klonen
git clone https://github.com/n05a-design/steps.git
cd steps

# 2. Kern-Unittests ausführen (90 Tests)
python -m unittest discover -s tests

# 3. Knowledge Curation Skill Tests ausführen (25 Tests)
python -m unittest discover -s .agents/skills/steps-knowledge-curation/tests

# 4. Golden Reference Suite ausführen (198 Fälle)
python knowledge/research/run_golden_test_suite.py
```

---

## 4. Qualitätssicherung & Metriken

* **Test-Abdeckung:** 115 Unittests (90 Core + 25 Skill) laufen in < 6 Sekunden mit 100% Erfolgsquote.
* **Golden Reference Cases:** 198 Referenzfälle (67 rechnerisch, 131 Spezifikation) verifiziert.
* **Fehlerbilanz:** 37 historische Musikfehler in `knowledge/research/MUSICAL_ERROR_REGISTER.csv` dokumentiert behoben.
* **Quellenevidenz:** 66 Zitations-Claims in `knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv` vollständig validiert.
* **Glide-Entkopplung:** Exakt **0 Importe** oder Abhängigkeiten zum isolierten Altsystem `src/glide-v3.53/`.

---

## 5. Dokumentation & Historisches Archiv

* **Aktive Dokumentation:** [`docs/`](docs/)
* **Architektur-Entscheidungen:** [`decisions/DECISION_REGISTER.md`](decisions/DECISION_REGISTER.md)
* **Historisches Archiv:** Frühere Arbeitsstände, Übergaben und Auditpakete befinden sich geordnet in [`archive/`](archive/).
