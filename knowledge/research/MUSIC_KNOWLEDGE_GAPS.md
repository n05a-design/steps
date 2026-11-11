# STEPS – Musikalisches Lückenregister & Domänen-Status (Phase 4.12)

**Audit-Zeitpunkt:** 2026-11-11T08:00:00+01:00  
**Geltungsbereich:** Wissensdomänen M01 bis M12, Ordnerstrukturen, offene Fachfragen  
**Referenzgrundlage:** 37 kuratierte Standardwerke (SRC-001 bis SRC-037), 130 Claims, 94 Golden Cases  

---

## 1. Übersicht: Geschlossene Lücken in Phase 4.12

In Phase 4.12 wurden wesentliche theoretische, mathematische und didaktische Lücken geschlossen:

| Domäne | Geschlossene Wissenslücke (Phase 4.12) | Primäre Nachweise & Quellen | Referenz-IDs |
|---|---|---|---|
| **M01** | Mathematische Cent-Modellierung ungleichstufiger historischer Stimmungen (Pythagoreisches Komma 23,46 Cents, Reine Terz 386,31 Cents, Werckmeister III, Mitteltönige Temperatur). | Prehn (SRC-033), Hindemith (SRC-015), Müller (SRC-018) | `CLAIM-003..006`, `REF-0089`, `REF-0090` |
| **M02** | Vollständige orthografische Regeln für doppelte Vorzeichen ($\sharp\sharp / \times$, $\flat\flat$), Enharmonik-Kontext und internationales vs. deutsches System. | Kostka & Payne (SRC-019), W3C MusicXML 4.0 (SRC-028) | `CLAIM-011..015`, `REF-0003..0009`, `REF-0080` |
| **M03** | Vollständige Taxonomie der Jazz-Skalen (Altered Scale / Super Locrian, Lydian Dominant, Bebop Dominant, Symmetrische verminderte Skalen HW/WH). | Mark Levine (SRC-020), Vincent Persichetti (SRC-030) | `CLAIM-016..020`, `REF-0067` |
| **M04** | Schichten-Architektur für erweiterte Jazz-Voicings: Zweihändige Rootless Voicings (Typ A `3-5-7-9` vs. Typ B `7-9-3-5`), Drop-2 Voicings, Upper Structure Triads. | Mark Levine (SRC-020), Vincent Persichetti (SRC-030) | `CLAIM-021..025`, `REF-0093`, `REF-0094` |
| **M05** | **Korrektur ERR-033:** Sekundärdominante zur Dominante ($V^7/V$ bzw. Doppeldominante $II^7$) mit modalem Tongeschlechtswechsel (Modal Shift) zu $ii^7$ über identischer Bassstufe. Modal Interchange (bIII, iv, bVI, bVII) und chromatische Medianten. | Aldwell & Schachter (SRC-013), Peter Spencer (SRC-016) | `CLAIM-026..030`, `REF-0077` |
| **M06** | Stimmführungsökonomie (L1-Distanz), Deceptive Resolutions von Sekundärdominanten, systematische Konsolidierung aller 25 Progressionsarchetypen (`PROG-001` bis `PROG-025`). | Aldwell & Schachter (SRC-013), Dennis DeSantis (SRC-017) | `CLAIM-031..032`, `REF-0065`, `REF-0077` |
| **M07** | **Korrektur ERR-034:** Mathematisch exakte 16tel-Swing-Quantisierung bei 480 PPQ für 61 % (Tick 146, Offset +26 Ticks, 36,11 ms bei 90 BPM). Additive ungerade Metren ($5/8 = 3+2$ und $7/8 = 2+2+3$). | Roger Linn (SRC-032), Dennis DeSantis (SRC-034), Friberg (SRC-031) | `CLAIM-033..036`, `REF-0071`, `REF-0083..0088`, `REF-0091..0092` |
| **M08** | Vollständige General MIDI 1.0 Kanal-10-Zuordnung, authentischer brasilianischer Surdo-Puls im 2/4-Takt (Betonung auf Schlag 2) vs. 4/4-Transkription (Betonung auf Schlag 3), Ghost Note Dynamic Shading. | MMA (SRC-027), Claus Schreiner (SRC-035), Ed Thigpen (SRC-022) | `CLAIM-037..038`, `REF-0045`, `REF-0076`, `REF-0078` |
| **M09** | Kulturhistorische Entflechtung: Brasilianische Samba-Batida (Tamborim/Surdo-Ursprung) sauber von kubanischer Clave getrennt; Afro-Kubanischer Montuno/Guajeo als synkopierte Klavierfigur definiert. | Claus Schreiner (SRC-035), Rebeca Mauleón (SRC-021) | `CLAIM-039..040`, `REF-0075`, `REF-0082` |
| **M10** | Umfassende Klavierpraxis-Bibliothek mit 14 Modulen (`P01` bis `P14`), ergonomische Händekoordination, Drop-2 und Rootless Voicing Praxis. | Alfred (SRC-024), Mark Levine (SRC-020), Mark Harrison (SRC-037) | `CLAIM-041..042`, `REF-0043`, `REF-0057`, `REF-0093..0094` |
| **M11** | Spezifikation der Konvertierungsverlustbehaftung zwischen MIDI 1.0 und MusicXML 4.0; Tuplets-Repräsentation (`<time-modification>`), variable PPQ-Grids (240, 480, 960). | W3C MusicXML 4.0 (SRC-028), MMA MIDI 1.0 (SRC-027) | `CLAIM-043..044`, `REF-0047`, `REF-0074`, `REF-0079` |
| **M12** | Bass-First Gehörbildungs-Curriculum, Guide-Tone-Hören und systematische didaktische Stufenfolge für Tastenlernende. | Jerry Coker (SRC-036), Berklee Online (SRC-025) | `CLAIM-045`, `REF-0058` |

---

## 2. Verbleibende Wissenslücken & Langfristige Forschungsagenda

Obwohl alle 12 Domänen nun über verifizierte Quellen, Claims und Referenzfälle verfügen, verbleiben spezialisierte Themen, die in künftigen Implementierungsphasen vertieft werden sollen:

### 1. M01 – Akustik & Tuning:
- **Lücke:** Praktische Audio-Synthese mit mikrotonalen Tuning-Dateien (Scala `.scl` und `.kbm`) und MPE (MIDI Polyphonic Expression).
- **Priorität:** P2 (für spätere Sound-Engine).

### 2. M03 / M09 – Außereuropäische Tonsysteme:
- **Lücke:** Indische Raga-Systeme (That-Systematik, 72 Melakarta-Ragas) und arabische Maqamat (Viertelton-Neutralsekunden).
- **Priorität:** P3 (Erweiterung nach MVP).

### 3. M07 – Komplexe Polyrhythmik & Metrische Modulation:
- **Lücke:** Verschachtelte Polyrhythmen (z. B. 5 gegen 4, 7 gegen 3) und Elliott-Carter-artige metrische Modulationen.
- **Priorität:** P2 (für experimentelle Drum-Tools).

### 4. M11 – Softwaretechnischer MusicXML-Parser (T-06):
- **Lücke:** Eigener C++/Python/Rust-Parser zur verlustarmen Überführung von MusicXML in interne STEPS-Datenstrukturen.
- **Priorität:** P1 (Kernbestandteil der anstehenden Entwicklungsphase T-06).

### 5. M12 – Interaktive Gehörbildungs-Algorithmen:
- **Lücke:** Gamifizierte App-Übungen mit adaptivem Schwierigkeitsgrad für Akkord- und Intervallerkennung.
- **Priorität:** P2 (Bestandteil der UI- und Anwendungsphase).
