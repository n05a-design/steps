# STEPS V6.6 – Transferlabor: COMPOSING ChanceVsStructure

**Wissensgebiet:** `08_COMPUTATIONAL_MUSIC`  
**Forschungsauslöser:** Philip Meyer MIDI Tools; S1gns Of L1fe  
**Status:** von STEPS eigenständig entworfene, **nicht durchgeführte** Versuchsanordnung. Kein kopierter Quelltext, keine Ableton-Set-Datei.

## Forschungsfrage und Kontext

Wie beeinflusst die genannte Technik die musikalische Struktur, das Hörergebnis oder die technische Reproduzierbarkeit? Die Beobachtung an einzelnen Künstlern liefert Inspiration, keine allgemeingültige Norm.

## Konkretes Versuchsvorgehen

Zwei Takte 16-step Euclidean Pattern mit k=5 n=16 und Startoffset 0. Gleicher Seed produziert gleiche Ergebnisse; eine Variante besitzt nur zeitlich verteilte Ratchets, andere Shuffle. Ausgangspattern stets gespeichert.

## Mess- und Abnahmeprotokoll

Indexierte Onsets, Dichte, Seed, Transformationsreihenfolge und exakter Re-Render als JSON/MIDI.

## Negativfall und Gegeninterpretation

Bei gleichem Seed darf sich Ergebnis nicht ohne deklarierte algorithmische Version unterscheiden. Eine Stilaussage ist kein deterministischer Test.

## Testverantwortung

Codex soll ausschließlich Datentypen und deterministische Invarianten automatisiert prüfen. Klangqualität, stilistische Eignung und kreative Beurteilung sind mit dokumentierter Hörprüfung beziehungsweise Expertenfeedback zu erfassen. Assets dürfen ohne individuell nachgewiesenes Nutzungsrecht nicht in Ausgabepakete gelangen.
