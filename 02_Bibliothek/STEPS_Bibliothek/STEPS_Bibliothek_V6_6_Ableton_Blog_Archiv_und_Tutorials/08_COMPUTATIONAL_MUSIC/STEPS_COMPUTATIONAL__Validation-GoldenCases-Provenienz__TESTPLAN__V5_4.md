# STEPS V5.4 – Testarchitektur: vom Byte zur musikfachlichen Behauptung

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Vier unabhängig auszuweisende Gates
**G0 Struktur:** JSON lesbar, referenzierte IDs existent, MIDI parsbar, MusicXML Schema/Namespaces korrekt (wenn jeweiliger Validator tatsächlich installiert ist). **G1 Musikdaten:** erwartete Tonhöhenintervalle, Taktlängen, Tempo-Map, eventuelle Note-Offs, Symbol-Parser. **G2 Musiktheorie:** mehrere etablierte Interpretationslinsen, Gegenbeispiele, stilbezogene Constraints, Review. **G3 Audio/Kultur/Rechte:** Instrumentenrender und Hörtest, reproduzierbare Audioanalyse, rights clearing, Reviewer-Perspektiven. Grüne G0/G1 beweisen G2/G3 nicht.

## Goldener Kompositionsfall
Eigene 8-Takt-Etüde mit `A`-Teil und kontrastierendem `B`-Teil; Datenobjekte `form`, `events`, `chord_annotations` und Exportdateien. Golden tests: Takt 1 enthält Startnote, Summe Note-Dauern passt, Akkordlabel reproduzierbar, Bassstimme physisch vorhanden, Variant-History referenziert. Ein Harte/DCML-Parser-Test muss den Ziel-Dialekt explizit angeben und die Originalzeichenfolge bewahren.

## Teststrategien
Property-based: `transpose(k).transpose(-k)` liefert gleiche MIDI-Pitches für definierte 12-TET-Umgebung. Tempoänderung darf Beatpositionen nicht verschieben, aber Sekundenpositionen verändern. Auflösung von Duplikat-IDs muss deterministisch sein. Fuzzing für fehlerhafte Akkordsymbole, MIDI-VLQ und Unterlauf bei Note-Off. Beipackende Skripte in V5.4 sind **eigene** Tests und keine abgeschlossenen App-End-to-End-Tests.

## Review-Protokoll
Jeder Eintrag `test_id`, `type`, `input_hash`, `expected`, `observed`, `tool_version`, `run_date`, `status`, `known_limits`, `reviewer`. Für G2-Fälle darf die automatische Prüfung „ambiguous“ als korrektes Ergebnis ausgeben. Ein Code-Coverage-Prozentwert ohne musikalische Äquivalenzklassen ist als Qualitätsbeweis unzureichend.
