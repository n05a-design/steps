# Theory-API · bestätigte Regeln und offene Verträge

`Voicing.invert(n)` rotiert nach aufsteigender Tonhöhe. Die untersten
`n % len(notes)` Stimmen wandern nacheinander in die nächstmögliche
Oktave oberhalb der bisherigen Oberstimme. Tonklassen und Stimmenzahl
bleiben erhalten. Bei Überschreiten von MIDI 127 wird ein
`VoiceLeadingError` ausgelöst. Für `(48, 67, 76)` ergibt Rotation 1
`(67, 76, 84)` mit G im Bass. Eine fachliche erste Akkordumkehrung
setzt die Terz des Akkords in den Bass und erfordert den Akkordgrundton.
Die Suche nach Aufrufern in `src/steps/`, `app/` und `tests/` fand vor
der Korrektur keinen produktiven Aufrufer dieser Methode. Die vorhandenen
`DiatonicInterval.invert()`-Aufrufe betreffen eine andere API.

| Offen | Gegenprobe | Entscheidungsvorschlag |
|---|---|---|
| AUTO-Notation | `Cis` und `Es` werden in AUTO abgewiesen, `Es7` wird erkannt. In DE werden alle drei gelesen. | Eindeutige deutsche Vorzeichennamen auch ohne Akkordqualität erkennen. Mehrdeutiges B im bestehenden AUTO-Dialekt gesondert dokumentieren und DE/INT bei kuratierten Daten explizit setzen. |
| Stimmführungsanalyse | Leere und mehrstimmige Folgen verwenden unterschiedliche Schlüssel für Kreisdistanz und L1-Durchschnitt. | Stabile Ergebnisfelder und Nullwerte für fehlende Übergänge festlegen. Vor Umbenennung Verbraucher und Übergangsaliasse prüfen. |
| Zusammengesetzte Intervalle | `Cadd9` und `C7(#11)` liefern 2 und 6, `C9` liefert die None als 14. | Die theoretische Intervallgröße als 14 bzw. 18 modellieren. Tonklassen separat modulo 12 führen. add2 und add9 als Schreib- und Registerfrage klären. |
| DROP2 bei erweiterten Akkorden | `C13` enthält in CLOSE A; DROP2 kürzt die Auswahl vor der Rotation und lässt A weg. | Bei Auswahl von vier Stimmen die qualitätsbestimmende Spannung erhalten oder für die betreffende Kombination einen ausdrücklichen Fehler melden. |

Ausführbar mit `python -B scripts/run_knowledge_benchmark.py --scope api`.
Die vier offenen Proben dokumentieren den beobachteten Vertrag und
blockieren keine Veröffentlichung mit einer noch unbeschlossenen Regel.
