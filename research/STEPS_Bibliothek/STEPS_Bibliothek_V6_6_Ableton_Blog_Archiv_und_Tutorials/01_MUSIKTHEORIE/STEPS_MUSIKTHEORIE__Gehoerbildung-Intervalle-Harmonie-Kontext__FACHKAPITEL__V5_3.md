> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Musiktheorie – Gehörbildung als überprüfbares Wissenssystem

## 1. Gegenstand und Abgrenzung
Gehörbildung darf nicht auf die Erkennung isolierter, gleich temperierter Intervalle reduziert werden. Ein Intervall hat eine **akustische Größe**, eine **notierte Intervallqualität**, eine **melodische Funktion** und eine **tonale Erwartung**. In einer C-Dur-Phrase kann der Ton F als vierte Stufe über der Tonika andere Erwartungen auslösen als derselbe Ton als kleine Septime von G7. Die Fähigkeit, einen Halbton zu hören, beweist nicht, dass der Hörer sein enharmonisches Spelling oder seine Tonart-Funktion sicher beurteilen kann. Für Steps müssen deshalb akustische Aufgaben und symbolische Theoriefragen getrennte Antworttypen sein.

## 2. Curriculare Abfolge
| Stufe | Wahrnehmungsziel | Kontext | Fortschrittsnachweis |
|---|---|---|---|
| 01 | Puls, Viertel, Achtel, Synkope unterscheiden | 4/4-Click + Noten | Onset-Klassifikation, nicht bloß MIDI-Quantisierung |
| 02 | Aufwärts/abwärts und Schritt/Sprung | kurze Monodie | Richtung und grobe Größe |
| 03 | Dur-, Moll-, verminderten und übermäßigen Dreiklang im Vergleich | gemeinsamer Grundton | Qualitätszuordnung mit Verwechslungsprotokoll |
| 04 | Diatonische Stufen hören | Tonika/Drone zuerst | Funktion mit Tonartangabe |
| 05 | ii–V–I und I–IV–V–I erkennen | gleicher Bassregisterbereich | Kadenzart und Bassweg getrennt erfassen |
| 06 | Dominantspannung vs. modaler Vamp | zwei stilistische Beispiele | alternative plausible Erklärung |
| 07 | Bassbewegung vs. gleichbleibender Chord | slash chords | richtige Trennung beider Ebenen |
| 08 | Swing, Shuffle, Mikroversatz | ein Drum-Pattern in A/B-Varianten | differenzierter Timingvergleich |
| 09 | Formgrenzen, Vorhalte, Wiederholung | acht Takte | Segmente mit Zeitmarkern |
| 10 | Mehrdeutige Progressionen | Loop ohne eindeutige Tonika | Unsicherheit begründen |

## 3. Vier Originalübungen
**E-01 (Klangidentität vs. Schreibweise):** Spiele in 12-TET erst F♯4 (MIDI 66), dann G♭4 (MIDI 66). Erwartung: akustisch derselbe Pitch unter gleichem Instrument und Tuning, notierte Funktion aber unterschiedlich. Der Klang allein unterscheidet die Notation nicht. **Negativtest:** Die Software darf nicht behaupten, F♯ und G♭ seien in jedem Tuning physikalisch identisch.

**E-02 (Funktion statt Klangqualität):** Vergleiche in C-Dur `Cmaj7–Dm7–G7–Cmaj7` mit `Cmaj7–Fmaj7–G7–Cmaj7`. Beide haben eine Dominante; die vorangehende Funktion ist im ersten Fall ii, im zweiten IV. Einzelakkorde allein beweisen keine „wahre“ Funktionsharmonik.

**E-03 (Bass-Exploration):** Spiele dieselbe Oberstimme E4–D4–C4 über C3–B2–A2 und dann C3–G2–A2. Lernziel: registriere Basslinie und melodische Linie unabhängig, bevor du Akkordbezeichnungen vergibst.

**E-04 (Rhythmus versus Tempo):** Ein 154-BPM-4/4-Pattern und ein 77-BPM-Pattern mit doppelt so vielen Unterteilungen können subjektiv verwandt wirken. **Nicht** als gleiche MIDI-Timingdaten oder gleiche Metertopologie ausgeben.

## 4. Evaluationsmetadaten
Jede Aufgabe speichert `task_id`, `heard_audio_id` (nur mit Lizenz), `symbolic_reference_id`, `transposition`, `tuning_id`, `tempo`, `meter`, `response_format`, `acceptable_answers[]`, `ambiguous`, `error_family`, `review_status`. Die Auswertung unterscheidet **richtige Klangdiagnose** und **plausible theoretische Interpretation**. Eine Nutzerantwort, die mehrere musikalisch tragfähige Lesarten begründet, ist bei einem Mehrdeutigkeitsfall nicht automatisch falsch.

## 5. Qualitätssicherung
Tonbeispiele lautheitsangepasst wiedergeben; Randomisierung von Tastenlage, Dauer und Timbre gegen reine Klangfarben- oder Registerheuristiken; keine geschützten kommerziellen Samples ohne Lizenz; Hinweise für Hörbeeinträchtigungen und alternatives textliches Lernen. Datensätze sind erst nach Hör- und Fachreview produktiv.

### Nachweise und Grenzen
- Open Music Theory, Inhaltsverzeichnis der Grundlagen und Stimmführungslehre: https://openmusictheory.github.io/contents (öffentliche didaktische Referenz, nicht als gesamtes Buch neu geprüft).
- music21, RomanNumeral-Dokumentation: https://music21.org/music21docs/moduleReference/moduleRoman.html (technische Vergleichsreferenz für Stufen und Akkorde).
- Nutzerseitige Steps-V5-Fachbände zu Notation und Pädagogik als historischer Arbeitsstand.
