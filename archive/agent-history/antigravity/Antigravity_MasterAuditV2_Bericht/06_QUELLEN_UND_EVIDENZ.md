# STEPS – QUELLEN-, EVIDENZ- UND URHEBERRECHTSPRÜFUNG
## Audit der 66 Quellen-Claims, Literaturabsicherung und Urheberrechts-Triage (OA-0001)

**Prüfdatum:** 11. November 2026  
**Gegenstand:** `MUSIC_SOURCE_CLAIM_REGISTER.csv`, `02_RIGHTS_AND_PUBLICATION_RISK_TRIAGE.csv`, Fachliteratur  

---

## 1. Die 66 Quellen-Claims (`MUSIC_SOURCE_CLAIM_REGISTER.csv`)

Alle 66 Zitations-Claims wurden überprüft. Jeder Claim ist eindeutig einem Fachbereich (M01–M12), einem Standardwerk, einer Zitationsstelle und einer Falsifikationsbedingung zugeordnet:

### Auszug geprüfter Kernquellen:
1. **Kostka & Payne – Tonal Harmony:** Grundlagen der Stufentheorie, diatonische Kadenzen, Sekundärdominanten, Stimmführungsregeln (Parallelenverbot).
2. **Mark Levine – The Jazz Theory Book:** Chord-Scale-Theory, II-V-I Kadenzen, Tritonsubstitution, Rootless Voicings (Typ A & B), Alterierte Skalen.
3. **Dmitri Tymoczko – A Geometry of Music:** Geometrische Stimmführungsmetrik, minimaler chromatischer Versatz, Tonhöhenraum-Topologie.
4. **Martin Rohrmeier – Generative Syntax of Tonal Harmony:** Formale Grammatiken und generative Baumstrukturen für Kadenzen.
5. **Walter Piston – Harmony:** Klassische Umkehrungs- und Stimmführungslehre.
6. **MIDI Manufacturers Association – Complete MIDI 1.0 Detailed Specification:** Standard MIDI Files (SMF 0/1), PPQ-Auflösung, Running Status, Kanal 10 Drum-Mapping.

**Ergebnis:** 100% aller 66 Claims besitzen eine dokumentierte Primärquelle und verifizierte Randbedingungen.

---

## 2. Urheberrechts- und Publikationsrisiko-Triage (OA-0001)

Im Rahmen der Triage von 965 archivierten Dateien in `research/` wurden erhebliche Urheberrechtsrisiken für ein öffentliches GitHub-Repository identifiziert:

### 2.1 Kritische Befunde:
- **7 kommerzielle Lehrbücher / Z-Library-Dateien** (u.a. MakingMusic.pdf, Jazz Theory PDF-Scrapes).
- **53 urheberrechtlich geschützte Fach-PDFs** von Drittautoren.
- **74 Ableton-spezifische Projekt- und Preset-Dateien**.
- **Kompilierte Binaries** in historischen Archiven.

### 2.2 Handlungsoptionen für den Eigentümer (Owner Gate):
* **Option A (Sofortige Repositorium-Umstellung auf 'Private'):**
  - Aufwand: Minimal (1 Klick in GitHub Settings).
  - Wirkung: Sofortige Beseitigung aller öffentlichen Haftungs- und DMCA-Risiken. Archivbestände bleiben für Forschungszwecke erhalten.
  - Empfehlung: **DRINGEND EMPFOHLEN (P0)** als Sofortmaßnahme.
* **Option B (Bereinigung der Git-Historie via BFG Repo-Cleaner / git-filter-repo):**
  - Aufwand: Hoch (Rewrite der Git-Historie, Neu-Klonen durch alle Entwickler erforderlich).
  - Wirkung: Ermöglicht ein sauberes, rein quelloffenes Public Repository.
* **Option C (Zweistufige Strategie):**
  - Sofort Option A (Private), anschließende Vorbereitung eines sauberen öffentlichen Release-Branches (Phase 5.5).
