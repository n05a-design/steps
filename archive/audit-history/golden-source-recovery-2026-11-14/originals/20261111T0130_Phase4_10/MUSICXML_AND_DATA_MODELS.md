# STEPS – Musikdatenmodelle, MusicXML-Spezifikation & Partitur-Architektur (Phase 4.10)

**Dokumenttyp:** TECHNICAL DATA MODEL & SPECIFICATION (M02 & M11)  
**Standard:** MusicXML 4.0 (W3C Community Group), Standard MIDI Files 1.0 (MMA)  
**Ziel:** Verlustfreie Repräsentation von Harmonik, Noten, Takten und Instrumentenrollen für STEPS

---

## 1. M11: Gegenüberstellung SMF (MIDI) vs. MusicXML vs. STEPS-Intern

| Anforderung | Standard MIDI File (SMF 1.0) | MusicXML 4.0 | STEPS Internes Datenmodell |
|---|---|---|---|
| **Primärer Fokus** | Performanz-Timing & Sound-Triggering | Graphische & semantische Notengravur | **Harmonisch-analytische Wissensrepräsentation** |
| **Tonhöhen-Codierung** | Ganze Zahlen 0–127 (Keine Enharmonik!) | Step (`C`), Alter (`1`, `-1`), Octave (`4`) | Pitch-Class (0–11) $+$ Spelling (`C#` vs `Db`) $+$ SPN |
| **Akkord-Semantik** | Reine simultane Note-On Events | `<harmony>` Element (Kind, Root, Bass, Degrees) | `ChordIdentity` mit Funktion, Stufe und Voicing |
| **Zeit-Darstellung** | Ticks je Viertelnote (z. B. 480 PPQ) | `<divisions>` je Viertelnote (rational) | Rationale Bruchteil-Zählzeiten ($1.0, 2.5$) $+$ Ticks |
| **Enharmonik ($C\sharp$ vs $D\flat$)** | **Verloren** (Beide sind MIDI Note 61) | **Vollständig erhalten** | **Vollständig erhalten** |

---

## 2. Kanonisches MusicXML Schema-Snippet für STEPS

Wenn STEPS später Notensätze oder Lead-Sheets exportiert, wird folgende kanonische XML-Struktur für Akkorde und Noten erzeugt:

```xml
<measure number="1">
  <attributes>
    <divisions>480</divisions>
    <key>
      <fifths>0</fifths>
      <mode>major</mode>
    </key>
    <time>
      <beats>4</beats>
      <beat-type>4</beat-type>
    </time>
    <clef>
      <sign>G</sign>
      <line>2</line>
    </clef>
  </attributes>

  <!-- STEPS Harmonie-Deklaration -->
  <harmony print-frame="no">
    <root>
      <root-step>D</root-step>
    </root>
    <kind text="m9">minor-ninth</kind>
    <bass>
      <bass-step>D</bass-step>
    </bass>
  </harmony>

  <!-- Einzelnote mit Notations- und Timing-Attributen -->
  <note>
    <pitch>
      <step>F</step>
      <octave>4</octave>
    </pitch>
    <duration>240</duration>
    <voice>1</voice>
    <type>eighth</type>
  </note>
</measure>
```

---

## 3. M02: Vorzeichen- und Tonartenlogik (Quintenzirkel-Berechnung)

Für die Notengravur und Tastaturanzeige implementiert STEPS folgende deterministische Regeln:
1. **Kreuz-Tonarten ($\sharp$):** Vorzeichenfolge: $F\sharp, C\sharp, G\sharp, D\sharp, A\sharp, E\sharp, B\sharp$ (dt. $H\sharp$).
2. **Be-Tonarten ($\flat$):** Vorzeichenfolge: $B\flat, E\flat, A\flat, D\flat, G\flat, C\flat, F\flat$.
3. **Enharmonische Äquivalenzprüfung:**
   Im C-Dur Kontext wird der Leitton zu D stets als $C\sharp$ notiert, niemals als $D\flat$, um die melodische Aufwärtsbewegung semantisch korrekt abzubilden.
