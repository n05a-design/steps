# Integrationskarte V6.0 — 06_PRODUCER_TOOLS

**Status:** Querverweis und zukünftiger Datenvertrag; keine Änderung an historischen V5.4-Fachdateien.

Die bestehende Fachbibliothek bleibt zentral. Die Produktionsbereiche ergänzen konkrete Audio-/MIDI-/DAW-/Rechte- und Veröffentlichungsbedingungen, die im ursprünglichen Forschungsfokus nicht als eigenständige Fächer vorlagen.

- **Recording, Room Acoustics & Microphone Technique** (`19_RECORDING_ROOM_MICROPHONES`): Mikrofonaufnahme ist die Kombination aus musikalischer Performance, Raum, Mikrofontyp, Positionierung, Vorverstärker und Monitoring. Raumanteil und Übersprechen sind manchmal Störgrößen, manchmal gestalterische Entscheidungen.
- **Editing, Restoration, Comping & Audio Repair** (`21_AUDIO_EDITING_RESTORATION`): Editing greift in Timing, Tonhöhe, Pausen, Transienten und Klangkontinuität ein. Ein sauberer Edit bewahrt die Absicht der Performance und ist im Kontext hörbar geprüft, nicht nur optisch an der Wellenform.
- **Synthesis, Sampling, Instrument Design & Sound Design** (`22_SYNTHESIS_SAMPLING_SOUND_DESIGN`): Klangdesign beginnt mit Spektrum und Zeitverlauf: Oszillator oder Klangquelle, Filter, Hüllkurve, Modulation und nichtlineare Bearbeitung erzeugen einen funktionalen Klang für den musikalischen Kontext.
- **Audio Effects, DSP Chains & Creative Processing** (`25_FX_DSP_PROCESSING`): Effekte sind zeitliche, spektrale, dynamische und nichtlineare Transformationen. Die Auswahl orientiert sich an einem auditierbaren musikalischen Problem und einem hörbaren Ziel – nicht am Besitz möglichst vieler Plugins.
- **Mixing, Balance, Translation & Critical Listening** (`26_MIXING`): Mischen ist das Ausbalancieren von musikalischen Rollen unter kontrollierten Wiedergabebedingungen. Lautheit, Frequenzbalance, Dynamik, Tiefe, Stereo und Hüllkurven bestimmen den Mix gemeinsam.
- **Mastering, QC, Loudness & Release Deliverables** (`27_MASTERING_RELEASE_AUDIO`): Mastering prüft und finalisiert Mischungen für einen konkret benannten Veröffentlichungsweg. Lautheitsmessung ist eine Spezifikation bzw. Rückmeldung und keine universelle ästhetische Zielvorgabe.

## Konkrete Codex-Kopplung
- Eingabemodell von Fachtheorie und Produktionsobjekten zunächst getrennt halten.
- Gemeinsame Elemente: `pitch`, `timbre`, `time`, `harmonic_context`, `performance`, `source_rights`, `confidence`.
- Technische Parameterprüfung als deterministischen Test behandeln; stilistische Gewichtung als erklärbare Hypothese.
- Kein Live-DAW-/Audio-Plugin-Feature in STEPS implementieren, bevor bestehendes Repository und Architektur überprüft sind.
