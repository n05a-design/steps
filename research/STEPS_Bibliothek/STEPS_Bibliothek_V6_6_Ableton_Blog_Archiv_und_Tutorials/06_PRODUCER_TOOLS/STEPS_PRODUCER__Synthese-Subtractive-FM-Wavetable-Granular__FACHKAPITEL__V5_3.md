> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Synthese und Sound Design – vier Grundfamilien

## Signalfluss als eigener Typ
Ein Synth-Patch ist kein Audio-Sample und kein Akkordsymbol. Es ist ein **parametrisierter Signalgraph**, dessen Komponenten Oszillator, Hüllkurve, Filter, Modulation, Stimmenverwaltung und Effekte sein können. Für Steps ist eine dokumentierte Patch-Rezeptur vorerst Forschung; eine Audio-/Synthese-Engine ist nicht stillschweigend implementiert.

## Subtraktive Synthese
Beginne mit einer obertonreichen Wellenform wie Saw oder Pulse, verringere mit einem Lowpass die Hochfrequenzanteile und forme die zeitliche Lautstärke per ADSR. Das ist eine zweckmäßige Definition, keine universelle Rekonstruktion analoger Hardware. **Originalrezept PAD-01:** zwei leicht gegeneinander verstimmte Sägezähne, Lowpass, Attack ~180 ms, Release ~900 ms; danach hörend den Filter-Cutoff variieren. Keine dB- oder Spektralidentität ohne Synth/Unison-Modus angeben. **Kontrolle:** Oszillator-Lautstärke und Filtereffekt getrennt testen; Resonanz kann Pegelspitzen verstärken.

## FM-Synthese
Bei sinusförmiger Frequenzmodulation der Trägerschwingung entstehen Seitenbänder, deren Stärke vom Modulationsindex und deren Abstand vom Modulator bestimmt wird. **Originalrezept BELL-01:** Träger und Modulator im Frequenzverhältnis 1:2, Modulator-Envelope kurzer Decay, niedriger Sustain, längerer Amp-Release. Ergebnisse hängen stark von Algorithmus, Phasenlage und Pegelskala ab. Operator in Ableton erlaubt mehrere Algorithmen mit vier Oszillatoren; Herstellerdokumentation zum Vergleich heranziehen, keine Bedienwerte als universelle FM-Physik verkaufen.

## Wavetable-Synthese
Eine Wavetable enthält kuratierte periodische Wellenformen, zwischen denen ein Positionsparameter über die Zeit wechseln kann. **Originalrezept LEAD-01:** eine Wavetable mit unterschiedlich obertonreichen Frames, Position langsam per Hüllkurve verschieben, Filter zunächst neutral, dann nur Filtermodulation zum Vergleich hinzufügen. So wird hörbar, ob die Klangänderung aus Wave-Position oder Filter stammt. Anti-Aliasing ist implementierungsabhängig.

## Granular-Synthese
Kleine Audiokörner mit eigenen Startzeiten, Dauern, Hüllkurven und Wiedergabepositionen werden neu angeordnet. Wichtige Freiheitsgrade: grain size, density, position, pitch, randomness, envelope, overlap und ggf. freeze. **Originalrezept TEXTURE-01:** selbst erstellter kurzer, lizenzfreier Sprach-/Instrumentalton; Körner in moderater Dichte über eine Stelle verteilen, Position verändern, dann korrelierte/zufällige Variationen vergleichen. Längere Körner können stärkere Erkennbarkeit der Ausgangsquelle erhalten; Sampling-/Rechtesituation bleibt relevant.

## Vergleichstabelle
| Ansatz | Hauptquelle spektraler Variation | Typische Fehlannahme | Steps-Evidence |
|---|---|---|---|
| subtraktiv | Filter auf obertonreiche Eingangssignale | jeder Filter bewirkt nur leiser/lauter | Patch + Hörprobe + Filterkurve |
| FM | Verhältnis/Index/Envelope | „FM klingt immer metallisch“ | Sideband-/Ratio-Experiment |
| wavetable | Frame-Position/Modulation | jede Wavetable ist identisch mit Sampling eines Songs | dokumentierte Wavesets |
| granular | Korndichte/-länge/-position | „Granular = beliebiger Reverb“ | Timing-/Pitch-Experiment |

## Maschinenlesbarer Patch-Vorschlag
`patch_id`, `engine_family`, `oscillators[]`, `modulation_routes[]`, `envelopes[]`, `filters[]`, `effects[]`, `polyphony`, `output_gain`, `audio_demo_id`, `source_evidence`, `license`, `review`. Variablenwerte ohne Einheit oder Geltungsbereich sind nicht produktionsfähig. Eine UI kann später „Bass/Lead/Pad/Texture“ als Zielklassen zeigen, aber die Klassen sind ästhetische Gebrauchszwecke, keine universellen akustischen Kategorien.

### Nachweise
Ableton-Live-12-Handbuch, Instrumente (Operator, Simpler, Wavetable), https://www.ableton.com/en/manual/live-instrument-reference/ . Dokumentation des Herstellers, für die konkreten Devices maßgeblich; keine allgemeine Fachmonografie. Die verlinkte PausePlayRepeat-Kursübersicht „Synthesis and Sound Design“ ist im V5.1-Register nur als Themenhinweis erfasst; komplette Lektionen sind nicht frei übernommen.
