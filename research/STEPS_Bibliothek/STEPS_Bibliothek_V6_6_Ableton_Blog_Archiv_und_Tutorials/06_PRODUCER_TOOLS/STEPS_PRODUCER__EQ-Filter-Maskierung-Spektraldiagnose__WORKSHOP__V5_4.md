# STEPS V5.4 – EQ als frequenzselektiver Pegelverlauf: konkrete Diagnose

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Grundmodell
Ein Equalizer implementiert einen frequenzabhängigen Verstärkungs- und Phasenverlauf. Glockenfilter, Shelf, Hochpass und Tiefpass sind nicht austauschbar; Parameter wie Mittenfrequenz, Güte Q und Flankensteilheit sind konfigurationsabhängig. Der Titel der vom Nutzer eingebrachten Lektion „EQ Is a Volume Control for Frequencies“ ist eine nützliche didaktische Reduktion, aber als technische Beschreibung nicht vollständig, weil Phasengang, Dynamik/EQ-Interaktion und Latenz ebenfalls relevant sein können.

## Vier Diagnosefälle
**Bass vs. Kick:** Bei gleichzeitigem Grundtonbereich (z. B. 45–65 Hz) ist ein pauschaler 60-Hz-Cut keine belegte Lösung. Erst Instrument einzeln hören, Spektren über Zeit messen, Phase/Transienten und Arrangement-Offbeats vergleichen. Variable Amp-Hüllkurve oder musikalische Tonlage ist oft eine Alternative zu statischem EQ.

**Vocal vs. Pad:** Zwei Stimmen konkurrieren im Präsenzband. Gegenmaßnahme kann Registeränderung, dynamischer EQ in der Begleitung oder kurzzeitige Arrangementlücke sein. Entscheide mit Hörtest und Pegelabgleich, nicht nur einer graphischen Kurve.

**High-pass auf Drums:** Einen Filter unterhalb der musikalisch relevanten Kick-Energie einsetzen; selbst ein HPF bei 30 Hz kann je nach Resonanz/Phase den Kick verändern. Vorher-nachher lautheitsabgleichen.

**Stereo-Balance:** Mid-Side-EQ kann breite Instrumente vom Lead trennen, birgt Monokompatibilitäts- und Korrelationsrisiken; nur unter überprüften Mixbedingungen einsetzen.

## Kontrollierter A/B-Versuch
Verwende Referenzsignal A (ungefiltert), B (EQ), C (EQ + neutraler Pegelausgleich). Vergleiche nur B vs. C nicht blind als „besser“, denn Pegelunterschied ist ein eigener Faktor. Messgrößen: Spektren pro 200-ms-Fenster, Integrated-Loudness (nur bei geeigneter Länge und Messalgorithmus), Peak und True Peak, Gruppenlaufzeit optional. Eine automatisierte Empfehlung braucht `reason`, `source`, `confidence`, `before_after_audio` und manuelle Freigabe.

## Herkunft
PPR-Kapitel als private Primärquelle des Nutzers, keine Rechte zur Reproduktion vorausgesetzt; externe EQ-Claims nur als technische Arbeitshypothesen ohne eigens gemessene Audio-Beispiele gekennzeichnet.
