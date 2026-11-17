# ADR-014: Umgang mit widersprüchlichen Musiktheorien – Perspektivenmodell mit Kontextpriorisierung

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, schriftliche Architekturentscheidung vom 17.11.2026; beantwortet „Wissensbasis: Fachtheorien/Quellenpriorität“ in [`PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) §8

## Kontext
Der Kern soll mehrdeutige Deutungen abbilden (`AGENTS.md` Regel 5). Die Quellen der Bibliothek (Aldwell/Schachter, Schönberg, Hindemith, Spencer/DeSantis/Stuart, Müller) beschreiben unterschiedliche musikalische Dimensionen. Zur Wahl standen eine globale Quellenrangfolge und die ungefilterte Gleichwertigkeit aller Deutungen.

## Entscheidung
Beides wird verworfen. Eine globale Rangfolge zerstört die Mehrdeutigkeit und erzeugt stilistische Fehlurteile, etwa parallele Dominantseptakkorde im Blues als Satzfehler oder einen kadenzierenden Quartsextakkord bei Bach als C/G-Slash-Akkord. Ungefilterte Gleichwertigkeit erzeugt in Abfragen und Oberfläche Rauschen. Stattdessen gilt ein **Schichtenmodell mit Kontextpriorisierung**:

| Ebene | Inhalt |
| --- | --- |
| **0 · Invariante Kernschicht** | Nur mathematisch-akustische Fakten: Tonklassen, MIDI-Nummern, PPQ-Ticks, Intervallvektoren. Je akustischem Ereignis oder Muster genau ein kanonischer Kernknoten. |
| **1 · Deutungskanten (`InterpretationEdge`)** | Theoretische Benennungen und Funktionen als parallele, typisierte Kanten, nie als überschreibende Attribute am Kernknoten. Pflichtfelder `paradigm` und `source`. |
| **2 · Kontextpriorisierung (`StyleContext`)** | Zur Laufzeit bestimmt ein Kontextprofil die Primärdeutung; alle anderen Deutungen bleiben abrufbar. |

**Paradigmen:**

| `paradigm` | Quellen | Fokus |
| --- | --- | --- |
| `classical_voice_leading` | Aldwell/Schachter | Lineare Stimmführung; Quartsextakkorde meist als Dissonanzbewegung (Vorhalt, Durchgang, Wechselnote) über dem Bass |
| `classical_harmonic` | Schönberg | Stufentheorie, Fundamentbass, Monotonalität, vagierende Akkorde |
| `acoustic_hindemith` | Hindemith | Akustisches System (Reihe 1 und 2, harmonisches Gefälle), Akkordgruppen nach Spannungsgrad und Grundton |
| `jazz_functional` | Spencer, DeSantis, Stuart | Klangfarbe, Tensions, lokale Funktion (ii–V, Tritonussubstitution, Modal Interchange), pragmatische Enharmonik |
| `mir_signal` | Müller (FMP) | Chroma-Features, Obertonspektren, Template-Matching |

**Kontextprofile (`StyleContext`):**

| Kontext | Primär | Sekundär | Hintergrund |
| --- | --- | --- | --- |
| Barock / Klassik / Romantik | `classical_voice_leading` + `classical_harmonic` | `mir_signal` | `jazz_functional` (Lesehilfe), `acoustic_hindemith` |
| Jazz / Bossa / Afro-Cuban | `jazz_functional` | `classical_voice_leading` | `acoustic_hindemith`, strenge Stufenlehre |
| Moderne / Post-Tonal | `acoustic_hindemith` + Pitch-Class-Sets | `classical_harmonic` | Klassische Kadenzlehre |
| MIR / Audio-Pipeline | `mir_signal` | `jazz_functional` | Historische Satzregeln |

**Verbindliche Regeln:**
1. **Speicherregel:** Alle fachlich gültigen Deutungen werden gleichwertig und parallel gespeichert, mit `paradigm` und `source`. Keine Theorie überschreibt eine andere im Kern.
2. **Konflikt im selben Paradigma:** Die granularere, funktional präzisere Aussage erhält den Hauptknoten; die pauschalere bleibt als Alias erhalten. Beispiel: Aldwell/Schachters Dreiteilung der Quartsextakkorde ist Hauptstruktur, das pauschale I⁶₄ bleibt Alias.
3. **Ausgaberegel:** Der aktive `StyleContext` bestimmt die Reihenfolge. Ohne übergebenen Kontext gilt der Standardkontext des Ursprungsbeispiels (BWV 846: klassische Stufen + MIR-Chroma; D7 → Dm7: Jazz-/Funktionsdeutung).

**Beispiel G–C–E auf schwerer Zeit vor G–B–D** (Kern: Tonklassen `[7, 0, 4]`, Bass 7, Intervallvektor `[0, 0, 1, 1, 1, 0]`):

| `paradigm` | `source` | Label | Funktion |
| --- | --- | --- | --- |
| `classical_voice_leading` | Aldwell/Schachter | V⁶₄ (kadenzierend) | dissonante Verzierung |
| `classical_harmonic` | Schönberg | I⁶₄ | Tonika-Umkehrung mit Dominantwirkung |
| `jazz_functional` | Spencer/DeSantis | C/G bzw. G7sus4(add6) | Slash- bzw. sus-Dominante |
| `acoustic_hindemith` | Hindemith | Gruppe I,2 (Grundton C über dem Bass G) | labile Grundtonwirkung |

> **Entschieden (17.11.2026, Inhaber):** Nach Hindemiths *Unterweisung im Tonsatz* enthält Untergruppe I,1 Dreiklänge ohne Tritonus mit Grundton im Bass, I,2 deren Umkehrungen (Terz oder Quinte im Bass). Bei G–C–E bestimmt die Quarte G–C den Grundton C, der Bass ist G, also **I,2**. Die erste Fassung dieses ADR nannte nach der Vorlage I,1. Die *Unterweisung* liegt nicht im Repository; die Zuordnung beruht auf der Inhaberentscheidung, nicht auf einer Seitenprüfung.

## Auswirkungen
- Datenmodell: `InterpretationEdge` (Pflichtfelder `paradigm`, `source`, `label`, `function`, optional `granularity`) und `StyleContext` werden Teil der Domänenverträge ([`DOMAIN_AND_STORAGE_CONTRACTS.md`](../docs/architecture/DOMAIN_AND_STORAGE_CONTRACTS.md)); Umsetzung in eigenem PR.
- Bestehende Graphkanten mit Theorieaussagen brauchen schrittweise eine `paradigm`-Zuordnung. Kanten der Kernschicht (z. B. Tonklassengleichheit) brauchen keine.
- Für v0.1 ([ADR-013](ADR-013-v01-umfang-akkorde-und-midi-export.md)) genügt der Kontext „Jazz/Pop“ als Standard für Produzierende; weitere Profile folgen.
- Rückfall: Ein Kontextprofil ist reine Sortierung; es löscht keine Deutung und kann ohne Datenmigration geändert werden.

## Links
- [`ABNAHMEBOGEN_2026-11-16.md`](../docs/audit/fable-5.2/ABNAHMEBOGEN_2026-11-16.md) (B4, B6, B9 als belegte Grundlagen)
- [`knowledge/relations/README.md`](../knowledge/relations/README.md)
