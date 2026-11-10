> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Swing, Microtiming und rhythmische Variation – begrifflich und technisch

## Zentrale Unterscheidungen
**Quantize**: Verschieben von Onsets auf Rasterwerte. **Swing**: systematische Ungleichzeitigkeit einer regelmäßigen Unterteilung (z. B. Paarungen). **Shuffle**: häufig triolisch geprägte Phrasierung, aber keine einzige universelle mathematische Einstellung. **Microtiming**: geringe Abweichungen vom gewählten Bezugsgitter. **Velocity**: MIDI-Anschlagstärke, nicht garantiert akustische Lautstärke. **Ghost Note**: stark zurückgenommener Schlag in musikalischem Kontext, nicht ein festgelegter MIDI-Wert. **Polyrhythmik**: gleichzeitige rhythmische Organisationsmuster; ein kurzer abweichender Perkussionszyklus kann zwar periodisch wandern, ohne bereits eine traditionsspezifische Polyrhythmik zu definieren.

## Mathematische Kontrollen
Bei Tempo `b` Vierteln/min ergeben sich `step16_ms = 15000 / b` und eine 4/4-Taktdauer `240000 / b` ms. Bei 132 BPM sind das ca. 113,636 ms pro Sechzehntel. Eine Verzögerung um 0,292 eines Sechzehntels ist 33,18 ms. Wird ein Swing-Level von 64% in einer beliebigen DAW eingestellt, folgt daraus **nicht**, dass es genau diesen Offset bewirkt; das hängt von Preset und Definitionsweise ab. In der Ableton-Referenz wirken Base, Quantize, Timing, Random, Velocity und Global Amount als getrennte Parameter.

## Reproduzierbarer A/B-Test
1. Originalmuster `straight`, gleiche Noten, Velocity und Timbre. 2. Kopie `swing`: nur ausgewählte „a“-Positionen um denselben dokumentierten Offset verschieben. 3. Kopie `velocity`: ursprüngliches Timing, aber Hihat-Akzente differenzieren. 4. Kopie `humanized`: konservative, **deterministisch geseedete** Timingvariation, Snare-Akzente und Kick/Hi-Hat-Gruppierungen nicht blind auseinanderreißen. 5. Hörvergleich bei angeglichener Lautheit. Damit ist identifizierbar, welcher Parameter die empfundene Veränderung tatsächlich auslöst.

## Drei originelle Testfälle
**P-01:** 130 BPM, Klick auf Beat 1–4, gerader 16tel-Hat-Puls. Nach Deaktivieren des Shuffles muss jeder Onset wieder auf den ganzzahligen Step zurückkehren. `Commit` schreibt dagegen neue MIDI-Zeiten in das Clipobjekt, sodass erneutes Zurückschalten ohne Vorversion die alten Zeitpositionen nicht wiederherstellt.

**P-02:** 7/8 in 2+2+3 mit Viertel bzw. Achtel als Beat-Einheit explizit definieren. Ein 16-Step-4/4-Grid ist dafür kein gültiger Container. Verwende `meter=7/8`, `grouping=[2,2,3]`, `tick_resolution` und `accent_positions=[0,2,4]` in Achteln.

**P-03:** gleiche Akzente mit 80 BPM und 160 BPM bei Half-Time-Feel. Wahrgenommene Metrik und tatsächliche Note-on-Zeiten dürfen nicht automatisch gleichgesetzt werden.

## Modell für Steps
`groove_id`, `source_status`, `grid_unit`, `offsets_beats`, `affected_roles[]`, `velocity_multipliers[]`, `seed`, `non_deterministic=false`, `target_tempo`, `swing_definition`, `history`, `commit_status`. Groove-Transformationen müssen idempotent oder explizit als kumulativ gekennzeichnet sein. Verschobene Offsets dürfen die absolute Reihenfolge musikalisch simultaner Choke-Events nicht unkontrolliert invertieren.

## Risiken
Blindes Randomizing zerstört Timingbeziehungen, einfache ML-Metriken belohnen fälschlich uniforme Lautstärke, und Genrebezeichnungen tragen kulturelle Vorannahmen. Ergebnisse werden deshalb als `educational_model` geführt und hörgetestet.

### Nachweise
Ableton Reference Manual 12, „Using Grooves“, Abschnitte Groove Pool/Commit: https://www.ableton.com/en/live-manual/12/using-grooves/ . Präzise Definitionen sind werkzeugspezifisch; eigenständige Verallgemeinerung muss geprüft werden.
