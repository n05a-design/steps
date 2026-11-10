> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Arrangement- und Formgestaltung für elektronische und adaptive Musik

## Harmonie versus Arrangement
Eine achtaktige Akkordfolge kann drei unterschiedliche Abschnitte tragen: nur Bass und sparsames Motiv, anschließend denselben Akkordbestand mit dichterem Drum-Groove, schließlich mehrere kontrapunktische Layer. Ohne separate `arrangement_sections` und `layer_events` könnte Steps diese strukturellen Entscheidungen nicht darstellen. **Drum-Engine** bleibt optional; ihre rhythmischen Beziehungen zu Komposition und Form sind jedoch bereits Forschungsthema.

## Ein originelles 24-Takt-Arrangementkonzept
Tempo 128 BPM, 4/4, A-Moll, harmonische Basis `Am–F–C–G` in Vier-Takt-Zyklus. 1–8: reduzierte Textur, tonales Zentrum nur über Pad und Subbass angedeutet, sparsame Zwei-Ton-Motivik A–C. 9–16: Dichte, Hi-Hat-Unterteilungen und Bassakzente steigen, Akkorde bleiben gleich; die stärkste Veränderung ist rhythmisch/klanglich. 17–24: Kontrast durch offenes Register, harmonische Umkehrungen (`Am/C`, `F/A`), verlängerte Melodietöne, optionale Pause vor Takt 21. Fills sollten nicht „jede achte Bar muss Snare-Roll“ als harte Regel sein: Effekt muss aus Abschnittsziel folgen.

## Form als Plan für kontrollierbare Übergänge
In einer Kompositionsbibliothek sollten `section_function` (intro, statement, intensification, transition, return, outro), `target_energy`, `layer_count`, `pitch_register`, `harmonic_change_rate`, `drum_density`, `accent_profile`, `transition_type` und `carryover_motif` getrennt sein. Der Begriff „Drop“ bezeichnet im elektronischen Produktionskontext meist eine Arrangement-Funktion, nicht eine eindeutig bestimmte harmonische Kadenz.

## Adaptives Scoring
Für Spiele/Interaktion wird ein **zustandsabhängiger Cue-Graph** benötigt: `state_id` → zulässige Layer und Übergangspunkte. Musikalische Kompatibilität beim Übergang hängt von Tempo/Metrum, Beatposition, Akkordzentrum, Tonalität, Instrumentenausklang und Motividentität ab. Eine Stems-Umschaltung kann das Audio ohne Akkordwechsel verändern. Ein experimenteller Graph darf nicht behaupten, dass jeder Transition-Mix musikalisch bruchfrei ist.

**Beispielzustände:** exploration (wenige Layer; Am), urgency (zusätzliche rhythmische Unterteilungen, Am), resolution (harmonische Rückkehr über E7–Am). Ein optionaler Übergang erst auf nächstem Taktanfang ist eine technische **Entwurfsentscheidung**, nicht musikalischer Standard.

## Tests und Schutzgrenzen
1. Arrangements enthalten durchgängige globale Taktkoordinaten. 2. Layer mit ausgeschaltetem Audio dürfen die Harmoniedaten nicht vernichten. 3. Übergänge erhalten Ausklang-/Tail-Metadaten. 4. Gleiche Akkordfolge heißt nicht gleicher Abschnitt. 5. Cue-Graph darf Zyklen haben, aber nicht mit unerreichbaren Zielzuständen als vollständig ausgegeben werden. 6. Lizenzen für Stems und Samples separat dokumentieren.

### Nachweise
Ableton Live 12 Referenz zu Clip-/Arrangement-, MIDI- und Groove-Funktionen: https://www.ableton.com/de/live-manual/12/ . Musikalische Formkonzepte aus der vorhandenen Steps V5-Composing-Basis; Systemmodell hier eigener Entwurf, nicht verifizierte Produktfunktion.
