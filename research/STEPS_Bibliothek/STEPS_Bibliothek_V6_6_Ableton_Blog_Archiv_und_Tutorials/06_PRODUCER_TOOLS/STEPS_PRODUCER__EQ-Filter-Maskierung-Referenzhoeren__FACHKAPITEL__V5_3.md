> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Equalizer: Frequenzbezogene Pegelregelung und musikalischer Kontext

## 1. Eine präzise Arbeitsdefinition
Ein Equalizer verändert das Frequenzverhalten eines Audiosignals; er arbeitet nicht einfach auf einer Liste separater Noten. Ein parametrischer Bell-Filter wird durch zentrale Frequenz, Bandbreite/Q und Gain charakterisiert; ein Shelving-Filter wirkt über einen Frequenzbereich; High-/Lowpass haben Übergangsbereich und Flankensteilheit. Je nach Filterarchitektur treten Phasenverschiebungen, Latenz und Impulsantworten auf. **Nicht** alle EQs sind identisch mit einer rein amplitudenbezogenen Operation im Zeitbereich.

## 2. Maskierung ist kontextuell
Zwei Signale können im selben Frequenzbereich um Aufmerksamkeit konkurrieren. Daraus folgt nicht, dass jedes überlappende Frequenzband zwingend abgesenkt werden muss. Entscheidungskriterien: Signalrolle, Arrangement, spektraler Mittelwert, zeitliche Dynamik, Stereo-/Phasenverhalten, Klangquelle und gewünschte Ästhetik. Eine Bassgitarre und Kick können gleichzeitig denselben Frequenzbereich tragen, ohne dass ein „mathematisch konfliktfreier“ Trennpunkt existiert.

## 3. Übung: Kick gegen Bass
1. Originalkicksignal und unabhängige Bassspur vorbereiten; bei vergleichbarer Lautheit beurteilen. 2. Bass kurz muten: Kickgrundton und Attackcharakter hören. 3. In Bassspur eine kleine, reversible Bell-Veränderung rund um einen identifizierten Überlappungsbereich testen; nicht blind „50 Hz absenken“. 4. Bypass bei **ausgeglichenem Pegel**. 5. Arrangement-Alternative (Bassattack versetzen) vergleichen. 6. Ergebnis als Hörreview mit Genre und Playbackumgebung dokumentieren.

## 4. Vier Fehlinterpretationen
- Eine optische Frequenzspitze ist nicht automatisch eine Problemfrequenz.
- Einen EQ auf einer einzelnen Synthspur einzustellen beweist keine Verbesserung im Mix.
- Ein steiler Hochpass kann Nebenwirkungen haben; „alles außer Bass bei 120 Hz abschneiden“ ist keine allgemeine Regel.
- Lautheitsgewinn durch Processing verzerrt A/B-Urteile; deshalb Pegelangleichung.

## 5. Steps-Wissensobjekt
`producer_tip_id`, `concept_eq_filter`, `hypothesis`, `signal_role`, `filter_type`, `frequency_hz`, `q_or_slope`, `gain_db`, `prepost_level`, `audio_example_id`, `decision_context`, `evidence`, `verification`. Dezibel als dimensionsbezogenes Maß korrekt einordnen: dBFS für Digitalpegel, LUFS/LKFS für loudness und dB Gain für relative Veränderung sind nicht austauschbar.

### Nachweise
Ableton Live 12 Audio Effect Reference, EQ Eight: https://www.ableton.com/en/manual/live-audio-effect-reference/ . PausePlayRepeat „EQ Is a Volume Control for Frequencies“ als separate geschützte Lehrquelle; Abstract/Referenz nur aus V5.1-Audit, keine Reproduktion des privaten Originals.
