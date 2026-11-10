# Integrationskarte V6.0 — 01_MUSIKTHEORIE

**Status:** Querverweis und zukünftiger Datenvertrag; keine Änderung an historischen V5.4-Fachdateien.

Die bestehende Fachbibliothek bleibt zentral. Die Produktionsbereiche ergänzen konkrete Audio-/MIDI-/DAW-/Rechte- und Veröffentlichungsbedingungen, die im ursprünglichen Forschungsfokus nicht als eigenständige Fächer vorlagen.

- **DAW, Sequencing, Automation & Project Management** (`17_DAW_SESSION_MIDI_AUTOMATION`): In-the-box-Produktion verbindet MIDI-Ereignisse, Audiodateien, Softwareinstrumente und Automation. Eine robuste Session trennt Quellmaterial, Bearbeitung, Renderstand, Sidechain-/Bus-Routing und Export und ist auf Fremdrechnern wiederherstellbar.
- **Critical Listening, Reference Analysis & Measurement** (`34_REFERENCE_ANALYSIS_LISTENING`): Ein Referenztrack ist ein Vergleichsinstrument für musikalische Eigenschaften. Analysen müssen Tempo, Arrangement, Tonhöhe, Energie, Timbre und Mixing getrennt erfassen und Urheber-/Quellstatus berücksichtigen.
- **Music File Formats, APIs, Interoperability & Reproducibility** (`39_INTEROPERABILITY_FORMATS`): Ein Produktionsarchiv benötigt klar getrennte Formate für Audio, MIDI, Notation, Arrangement und Metadaten. Konvertierungen sind nicht immer verlustfrei; Semantik, Timing und Plugin-Zustände können verloren gehen.

## Konkrete Codex-Kopplung
- Eingabemodell von Fachtheorie und Produktionsobjekten zunächst getrennt halten.
- Gemeinsame Elemente: `pitch`, `timbre`, `time`, `harmonic_context`, `performance`, `source_rights`, `confidence`.
- Technische Parameterprüfung als deterministischen Test behandeln; stilistische Gewichtung als erklärbare Hypothese.
- Kein Live-DAW-/Audio-Plugin-Feature in STEPS implementieren, bevor bestehendes Repository und Architektur überprüft sind.
