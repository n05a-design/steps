# STEPS Audit: MIDI Export Loss Report & Theorie-Abbildungsanalyse

**Datum:** 2026-11-17  
**Status:** Abgeschlossen  
**Prüfauftrag:** Prompt 11 (`prompts/11_MIDI_AUDIO.md`), REQ-026, ADR-007  
**Referenzdateien:** `src/steps/midi/`, `tests/test_midi_golden_fixtures.py`, `schemas/project.schema.json`

---

## 1. Zweck und Zielsetzung

Standard MIDI Files (SMF 1.0) sind der universelle Industriestandard für den Austausch musikalischer Aufführungs- und Steuerungsdaten zwischen DAWs, Sequenzern und Synthesizern.
Gemäß Prompt 11 und REQ-026 erfordert der STEPS-Arbeitsvertrag (`AGENTS.md`) einen expliziten **Loss Report**, der dokumentiert, welche musiktheoretischen Domänenkonzepte bei der Übersetzung eines hochgradig typisierten STEPS-Projekts in eine reine MIDI-Datei **vollständig erhalten bleiben** und welche **systembedingt verloren gehen** (und deshalb ausschließlich im STEPS-Projektformat `.stepsproj` / JSON-Schema verbleiben).

---

## 2. Erhaltene Dimensionen (100% verlustfrei in SMF 1.0)

| Dimension | STEPS Datenmodell | SMF 1.0 Repräsentation | Verifikation |
|---|---|---|---|
| **Musikalische Zeit** | Ganzzahlige Ticks (480 PPQ) | Header `MThd` Division (480) & Track Delta-Times (`VLQ`) | Bitgenau getestet in `test_midi_export_service.py` |
| **Metrum / Taktart** | `TimeSignature(numerator, denominator)` | Meta-Event `0x58 Time Signature` (z. B. `04 02 18 08` für 4/4) | Geprüft in Golden Test `GOLD_01` bis `GOLD_10` |
| **Tempo & Tempoverläufe** | `TempoMap` mit Multi-Tempo-Points | Meta-Event `0x51 Set Tempo` (Mikrosekunden pro Viertelnote) | Geprüft in `GOLD_09_MULTI_TEMPO_METER` (T15) |
| **Klingende Tonhöhen** | 12-TET Notenbereich 0..127 | Channel Voice `0x90 Note On` / `0x80 Note Off` | 1:1 Note-Pairing validiert (T14) |
| **Lautstärke / Dynamik** | Note Velocity (0..127) | MIDI Velocity Byte | Erhalten (Default 75–80) |
| **Track-Struktur** | Multi-Track (`tracks[]`) | Format 1 Conductor Track (0) + Instrument/Chords Tracks (1..N) | 2-Track-Struktur via `scripts.audit_midi_files.envelope` verifiziert |

---

## 3. Systembedingter Verlust (Nicht nativ in SMF 1.0 abbildbar)

Standard-MIDI-Kanalnachrichten übertragen ausschließlich physikalische Tastendrücke (Notennummer + Anschlagsdynamik), keine musiktheoretische Semantik:

| Domänenkonzept in STEPS | STEPS Semantik (`src/steps/`) | Verlust bei SMF-Export | Auswirkung & Gegenmaßnahme |
|---|---|---|---|
| **Note Spelling & Enharmonik** | `NoteSpelling` unterscheidet strikt `C#` (diatonisch Leitton zu D) von `Db` (tiefalterierte None in C) | Beide werden zu MIDI Note `61`. Das Vorzeichen geht verloren. | **Gegenmaßnahme:** Notation und Enharmonik verbleiben in `project.schema.json`. Für Notendruck wird später MusicXML als nativer Notationsadapter bereitgestellt. |
| **Harmonische Funktionsanalyse** | `HarmonicAnalysis` mit Stufen (`I`, `ii`, `V7/vi`), Kadenzen und funktionaler Mehrdeutigkeit | MIDI besitzt keine Syntax für Stufen- oder Funktionsbezeichnungen. | **Gegenmaßnahme:** Optionaler Export als Meta-Textevent `0x01 Text` oder `0x06 Marker` an Taktgrenzen für DAWs. |
| **Akkordidentität vs. Voicing** | `ChordDefinition` speichert Grundton, Struktur und Intent; `Voicing` speichert die konkrete Realisierung | Die MIDI-Datei sieht nur simultane Einzelnoten (`60, 64, 67`), verliert aber die abstrakte Akkordformel `Cmaj` | **Gegenmaßnahme:** Analyse-Engine kann aus MIDI-Noten Voicing ableiten, die originäre Intention liegt jedoch nur in STEPS vor. |
| **Slash-Bass vs. Inversion** | Unterscheidung: Echter Akkordton im Bass (`C/E` = 1. Umkehrung) vs. fremder Basston (`C/D` = D-Pedalton/Slash) | MIDI erzeugt nur eine tiefe Note `D` (MIDI 50) neben `C, E, G`, ohne funktionale Relation. | **Gegenmaßnahme:** Semantische Unterscheidung bleibt im Datenmodell erhalten. |
| **Stimmführung & Satzlehre** | Sopran-, Alt-, Tenor-, Bass-Stimmenzuordnung; Stimmkreuzungs- und Parallelenprüfung | Wenn alle Noten auf einem Kanal liegen, geht die Stimmenidentität verloren. | **Gegenmaßnahme:** Getrennte Kanäle/Tracks pro Stimme bei erweitertem Voicing-Export. |
| **Kulturelle Konvention (DE vs. INT)** | `notation_convention`: Deutsches `H`/`B` vs. internationales `B`/`Bb` | MIDI-Notennummern sind sprachneutral. | **Gegenmaßnahme:** Im UI-Presenter und Projektmodell gekapselt. |

---

## 4. Deterministische Verifikation

Die 10 kanonischen Golden MIDI-Dateien (`tests/test_midi_golden_fixtures.py`) belegen:
1. **SMF Format 0 & Format 1:** Alle Kadenzen, Jazz-, Blues- und Modalprogressionen werden syntaktisch valide erzeugt.
2. **Keine hängenden Noten (T14):** 100% aller erzeugten Noten besitzen einen zeitlich passenden Note-Off-Partner auf demselben Kanal.
3. **Multi-Tempo-Integrität (T15):** Tempowechsel mitten im Stück werden exakt an den berechneten Ticks im Conductor-Track platziert.
4. **Automated SMF validity:** Independent Header- and envelope audit (`scripts.audit_midi_files.envelope`) verifies Format 0/1 structure and loss-report fixtures. It does not replace an independent DAW import acceptance.

---

## 5. Fazit

Der Export nach SMF 1.0 ist durch automatisierte Writer-, Parser-, Envelope- und Roundtrip-Prüfungen belegt. Ein tatsächlicher DAW-Import gilt erst nach dem dokumentierten manuellen Reimport in mindestens zwei unabhängig benannten Anwendungen als bestanden. Da Standard-MIDI kein Harmonielehre-Austauschformat ist, bleibt `schemas/project.schema.json` die maßgebliche Quelle für alle nicht in SMF abbildbaren Metadaten.
