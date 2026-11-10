> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Drum-Progressions – Genreatlas mit unabhängigen Originalstudien

**Schutzstatus:** Die MIDI-Übungen in `Eigene_MIDI_Studien/` sind neu erzeugte, generische Lernbeispiele; sie enthalten weder die PausePlayRepeat-MIDI-Downloads noch geschützte Audio-/Kit-Samples. Genrelabels dienen der didaktischen Orientierung. Ein einzelnes Raster ist kein musikwissenschaftlicher Beweis für ein Genre; Tempi und Synkopen variieren nach Substil, Epoche und Produktion.

## Architektur der Drum-Progression
Jedes Muster besitzt ein `beat_pattern` (beide Takte), `timbre_roles`, `velocity_shapes`, `humanization_policy`, `groove_policy`, `bass_relationship`, `phrasing_and_fills`, `section_role`, `inspiration_vs_source` und eigene Tests. Die rhythmische Entwicklung ist eine **Progression** von Dichte und Akzentbeziehungen über Zeit; sie ist nicht nur eine Akkordfolge mit Drums darunter.

## 12 genreorientierte Lehrfälle – eigene, bewusst schematische Ideen
| ID | Stil-Orientierung | Puls/Groove | Formidee | Analytische Warnung |
|---|---|---|---|---|
| DR53-01 | straight house | gleichmäßige Kick, Offbeat Hat | Open-Hat-Einsatz in B | kein universelles House-Rezept |
| DR53-02 | techno | gerader Puls mit 3er-Perkussionszyklus | Rim-Verschiebung, Ride als Kontrast | 3:4-Beziehung nicht automatisch afrikanischer Polyrhythmus |
| DR53-03 | UK garage | Kick Lücken auf Beat 3, Swing-Hat-Paare | 2-Takt-Frage/Antwort | Stil kein einziges Swing-Prozent |
| DR53-04 | halftime D&B | Halftime Backbeat bei 172 BPM | dichte Tops, sparsamer Bass-Attack | Geschwindigkeit ist nicht Schallfarbe |
| DR53-05 | two-step D&B | versetzter Kick, kräftige 2/4 Snare | Ghost-Hat-Antwort | keine Kopie des Sub-Focus-Kurses |
| DR53-06 | boom bap | langsame Backbeat-Orientierung, kleine Offsets | 4-Bar-Velocity-Bogen | „humanized“ heißt nicht zufällig alles verschieben |
| DR53-07 | trap / rage study | Half-Time Clap mit kurzen Hat-Figuren | Lücken vor Takt 2 | keine Transkription von Miss the Rage |
| DR53-08 | breakbeat | fragmentierte Kick/Snare-Gruppierung | dichtes Fill-Taktende | nicht als konkreter Samplebreak bezeichnet |
| DR53-09 | funk | synkopierte Kick, Snare-Ghost-Noten | Offbeat-Variation | Spielgefühl benötigt Instrument- und Hörkontext |
| DR53-10 | reggae-inspired | ausgesparte Downbeat-Kick, Offbeat-Akzente | 2-Takt-Pause | nicht als authentische Jamaika-Praxis ausgewiesen |
| DR53-11 | reggaeton-inspired | wiederkehrender dembow-ähnlicher Akzentzyklus | Kick-Antwort über zwei Takte | stilgeschichtliche und kulturelle Prüfung offen |
| DR53-12 | odd-meter study | 7/8 (2+2+3) | Pulsakzente im Gruppierungswechsel | kein automatischer „Balkan“-Stempel |

Alle Übungs-MIDI-Dateien besitzen ihre eigenen, dokumentierten Eventtabellen und einen Audit-Status `original_educational_not_style_validated`. Wo eine genaue Stilklassifikation wichtig ist, sind Fachquellen, Korpora und Reviewer aus dieser musikalischen Praxis nötig.

## Mikrostruktur und Unterschied der Materialebenen
**Tempo** definiert Notenrasterdauer, **Groove** verändert Onsets relativ zum Raster, **Velocity** beschreibt MIDI-Anschlag, **Envelope** verändert den hörbaren Anschlag/Ausklang, **Samplewahl** beeinflusst Lautstärke und Timbre und **Mixing** den Gesamteindruck. Gleiche MIDI-Velocity bedeutet nicht gleiche wahrgenommene Lautstärke unterschiedlicher Samples. In den vier bereitgestellten Kursstudien (UK Garage, Techno, D&B, Rage) wurden jeweils konkrete Herstellereinstellungen und Transkriptionsannahmen beschrieben; diese werden weiterhin im V5.1-Quellenregister geführt und nicht ungeprüft zu allgemeiner Genrepraktik erklärt.

## Arrangierte Variation statt bloß duplizierter Loops
A (Takte 1–4): Kernpuls. B (5–8): Hats und leiser Ghost-Layer. C (9–12): Bass-/Kick-Verzahnung und veränderte Akzentkontur. D (13–16): ein kurzer Fill plus Rückkehr/Break. Abweichungen von der Rasterstruktur sind explizit als Ereignisse oder Transformationsregeln zu speichern. **Kein** Generator soll durch Copy/Paste eines 1-Bar-Musters „eine vollständige Progression“ behaupten.

## Kulturelle und wissenschaftliche Prüfgrenzen
Rhythmusbilder dürfen nicht aus Weltregionen automatisch abgeleitet werden. Afrobeat, Highlife, Amapiano, Salsa/Clave, Baile Funk und traditionelle Spielweisen verlangen separate historische, rhythmologische und kulturelle Quellen. Hier nur als **Lücken im langfristigen Genreatlas**, nicht als ungeprüfte Muster. Keine identischen PPR-Texttabellen oder proprietären MIDI-Packs im öffentlichen Repo wiedergeben.

### Nachweise
Ableton Live 12 Groove Pool: https://www.ableton.com/en/live-manual/12/using-grooves/ . Drum Rack/Choke-Gruppen: https://www.ableton.com/en/manual/instrument-drum-and-effect-racks/ . Nutzerseitige fünf PPR-Lektionen und V5.1-Quellenregister bilden separate Referenz- und Provenienzschicht, nicht freie Redistributionserlaubnis.
