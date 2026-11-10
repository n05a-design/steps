> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Songwriting und Komposition: Topline, Prosodie und Form

## Die separate kompositorische Ebene
Ein Kompositionsmodell beginnt nicht mit einem Generator für vier Akkordsymbole. Es benötigt `creative_goal`, `structural_plan`, `melodic_motifs`, `phrases`, `lyrics/prosody` (wenn vorgesehen), `harmony`, `bass`, `rhythm`, `instrumentation`, `sections`, `revisions` und `production_notes`. Ein Song kann identische Akkorde über Verse und Hook verwenden und trotzdem eine deutlich andere Energie haben: durch Melodiehöhe, Register, Phrasenendpunkte, rhythmische Dichte, Instrumentation, Dynamik und Pausen.

## Eigenes 16-Takt-Songwriting-Labor
**Brief:** 100 BPM, 4/4, A-Moll, gesungene deutschsprachige Topline, achttaktige Strophe und achttaktiger Refrain. Die Akkordfolge ist ein bewusst schlichtes Mittel, damit melodische Unterschiede hörbar werden.

**Strophe (Takte 1–8):** `Am | F | C | G | Am | F | C | E7`. Melodisches Kernmotiv: A4(1/4), C5(1/4), B4(1/2) über Am. Wiederholung mit verändertem Schluss: A4–C5–D5 (halbe). Phrasen 1–4 und 5–8 als Frage/Antwort konzipieren, letzter Takt E7 mit G♯ als führungsrelevanter Ton, sofern Melodie ihn zulässt.

**Refrain (Takte 9–16):** `C | G/B | Am | F | C/E | G | E7 | Am`. Kerngeste: E5(1/4)–D5(1/4)–C5(1/2), höheres Startregister als in der Strophe. Takt 16 Schluss auf A4 (ganze) als mögliches Ziel. Das ist ein **origineller Rohentwurf**, keine zwingend performante endgültige Gesangsmelodie.

## Textmetrische Arbeit
Eine natürlich betonte deutsche Wortgruppe sollte nicht blind auf beliebige starke Zählzeiten verteilt werden. Prüfe Betonung, Vokallänge, Atemstelle, Konsonantenballung und Tonhöhe des vokal offenen Teils. Zum Beispiel kann ein viersilbiges Fantasiewort nicht sicher durch vier gleichlange Sechzehntel in hohem Register singbar sein. Eine textliche Silbentrennung und ein Beat-Raster sind Hilfsmittel; Verständlichkeit bleibt hör-/sprechpflichtig.

| Entscheidung | Fachlich prüfbar | Interpretativ |
|---|---|---|
| Tonumfang | z. B. A4–E5 in MIDI/Notation | angenehm für diese Stimme? |
| Atemstelle | Pause vor Taktgrenze vorhanden? | klingt die Phrase organisch? |
| Wiederholung | Motive teilen Intervallkontur? | besitzt der Hook Wiedererkennungswert? |
| Harmonie-Fit | Melodie-/Akkordton zum Zeitpunkt | erwünschte Dissonanz? |
| Abschnittskontrast | Register, Dichte, Tonlänge, Velocity verändert? | emotionale Wirkung? |

## Variantenwerkstatt
A. *Rhythmische Variante:* gleichen Tonhöhenvorrat, aber Synkope vor Takt 9; B. *harmonische Variante:* vierter Refrain-Takt `Fm` statt `F` nur nach Melodieprüfung; C. *Arrangement-Variante:* Synth-Bass und Pad in Strophe zurücknehmen, in Refrain verdichten; D. *Kontrast-Variante:* Takte 13–14 im Instrumentarium halbieren und erst Takt 15 ansteigen lassen. Alle Varianten benötigen Hörtests und klare Dateiversion, nicht bloß `AI-approved`.

## Speichermodell
`composition_id`, `section_id`, `lyric_line_id`, `syllables[{text,accent,beat_range}]`, `motif_id`, `note_events`, `phrase_boundaries`, `lead_vocal_register`, `arrangement_layers`, `transformations`, `render_revision`, `review_status`. Geschützte Songtexte nicht in offene Trainings-/Beispieldaten importieren.

### Nachweise
Open Music Theory (Phrase, Cadence, Form, Voice-leading): https://openmusictheory.github.io/contents . Eigene 16-Takt-Skizze als methodisches Werkstattbeispiel, keine behauptete Stiltranskription.
