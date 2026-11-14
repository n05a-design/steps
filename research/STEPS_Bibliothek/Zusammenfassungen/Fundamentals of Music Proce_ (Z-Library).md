---
werk: "Fundamentals of Music Processing – Audio, Analysis, Algorithms, Applications"
autor: "Meinard Müller"
verlag: "Springer"
isbn: "978-3-319-21944-8"
seiten: 509
quelle_pdf: "research/STEPS_Bibliothek/Fundamentals of Music Proce_ (Z-Library).pdf"
herkunft: "Dateiname nennt Z-Library, also eine nicht autorisierte Quelle. Nicht weiterverbreiten; ggf. durch eine lizenzierte Ausgabe ersetzen."
quelle_sha256: feb755b854a0683cccd611545f4298a9e9d90dcce5839bbde92f14eea27e4767
rechteklasse: E
original: restricted_local (per .gitignore ausgeschlossen)
grundlage: "Docling-Extrakt vom 14.11.2026; vollständige Gliederung, Kapitel 5 (Akkorderkennung) gelesen"
stand: 2026-11-14
fachliche_freigabe: false
---

# Meinard Müller: Fundamentals of Music Processing

> Zusammenfassung in eigenen Worten. Formeln und Abbildungen sind nicht wiedergegeben. **Herkunftshinweis:** Die Datei im Repository stammt laut Dateiname aus einer nicht autorisierten Quelle (Z-Library). Für eine weitere Verwendung ist eine lizenzierte Ausgabe zu beschaffen.

## Einordnung

Das Standardlehrbuch des Fachs Music Information Retrieval (MIR) zur Verarbeitung von Musiksignalen. Es verbindet Signalverarbeitung (Fourier-Analyse) mit musikalischen Fragestellungen. Jedes Kapitel ist um eine **Aufgabe** aufgebaut (Synchronisation, Struktur, Akkorde, Tempo, Retrieval, Zerlegung) und endet mit „Further Notes“ zu Literatur und Varianten. Der Autor ist Professor an den International Audio Laboratories Erlangen. Zum Buch gibt es öffentlich die „FMP Notebooks“ (Python/Jupyter) mit Implementierungen. Diese sind nicht Teil der Datei.

## Gliederung und Kerninhalte

### 1. Musikrepräsentationen
- Noten, Tonhöhen, westliche Notation.
- Symbolisch: Piano-Roll, MIDI, Partiturformate, Optical Music Recognition (OMR).
- Audio: Wellenform, Frequenz und Tonhöhe (gleichstufige Stimmung, Referenz 440 Hz), Dynamik, Intensität, Lautheit, Klangfarbe.

### 2. Fourier-Analyse
- Fourier-Transformation für analoge und digitale Signale, Signalräume.
- Diskrete Fourier-Transformation (DFT) und FFT.
- **Kurzzeit-Fourier-Transformation (STFT)** und Spektrogramm.

### 3. Musiksynchronisation
- **Audiomerkmale:** logarithmisches Frequenzspektrogramm und **Chroma-Merkmale**. Die Energie wird auf die zwölf Tonklassen einer Oktave zusammengefasst und ist damit unabhängig von der Oktavlage.
- **Dynamic Time Warping (DTW)** zur Ausrichtung zweier Aufnahmen oder von Partitur und Aufnahme, mit Varianten.
- Anwendungen: multimodale Navigation, Tempokurven.

### 4. Strukturanalyse
- Prinzipien der Segmentierung: Wiederholung, Homogenität, Neuheit.
- **Selbstähnlichkeitsmatrizen** und Verbesserungsstrategien.
- **Audio-Thumbnailing** (repräsentativster Abschnitt) mit Fitnessmaß und Scape-Plot.
- Neuheitsbasierte Segmentierung, Strukturmerkmale.
- Evaluation: Precision, Recall, F-Maß, Grenz- und Labelbewertung.

### 5. Akkorderkennung (für STEPS zentral)
- **Grundlagen der Harmonielehre:** Intervalle, Akkorde, Skalen.
- **Vorlagenbasierte Erkennung:** Für jedes Zeitfenster wird ein Chromavektor mit binären Vorlagen der 24 Dur- und Molldreiklänge verglichen. Der ähnlichste Akkord wird zugeordnet.
- **Evaluation:** Vergleich mit einer Referenzannotation von Experten. Das Buch zeigt am Beispiel der ersten Takte von „Let It Be“, dass schon Experten auf unterschiedlichen zeitlichen Ebenen annotieren (halbtaktig oder feiner).
- **Mehrdeutigkeiten** in drei Arten:
  1. *Akkordmehrdeutigkeit:* Verwandte Akkorde teilen Töne. C-Dur teilt je zwei Töne mit a-Moll, c-Moll und e-Moll. Cmaj7 enthält C-Dur und e-Moll und wird bei nur 24 Klassen leicht einem der beiden zugeordnet. Mehr Akkordklassen verringern dieses Problem, erhöhen aber die Verwechslungsgefahr.
  2. *Akustische Mehrdeutigkeit:* Obertöne verteilen Energie auf andere Tonklassen. Ein einzelner tiefer Ton C erzeugt Energie auf C, G, E und Bb. Er wird dann leicht als C-Dur erkannt, obwohl er musikalisch auch Grundton von c-Moll oder Quinte von F-Dur sein kann.
  3. *Stimmung:* Aufnahmen weichen von 440 Hz ab und verschieben Energie zwischen Chroma-Bändern.
- **Verbesserungen:** Vorlagen mit Obertönen, aus Beispielen gelernte Vorlagen, spektrale Aufbereitung, zeitliche Vorfilterung (Glättung).
- **HMM-basierte Erkennung:** Markov-Ketten mit Übergangswahrscheinlichkeiten zwischen Akkorden, Hidden-Markov-Modelle, Viterbi-Dekodierung. Damit wird die zeitliche Kontinuität von Akkorden modelliert und die Fehlklassifikation einzelner Fenster verringert.

### 6. Tempo- und Beat-Tracking
- **Onset-Erkennung:** energie-, spektral-, phasen- und komplexbasierte Neuheitsfunktionen.
- **Tempogramme:** Fourier-, Autokorrelations- und zyklisches Tempogramm.
- Beat-Tracking: vorherrschender lokaler Puls (PLP), Beat-Tracking per dynamischer Programmierung, adaptive Fensterung.

### 7. Inhaltsbasierte Audiosuche
- **Audio-Identifikation** (Fingerprints aus spektralen Spitzen, Indizes, invertierte Listen).
- **Audio-Matching** (diagonal, DTW-basiert).
- **Versionserkennung** (Cover-Versionen) mit Evaluationsmaßen.

### 8. Musikalisch informierte Audiozerlegung
- **Harmonisch-perkussive Trennung** (horizontale und vertikale Strukturen im Spektrogramm).
- **Melodieextraktion:** instantane Frequenz, Salienzdarstellung, informierte Grundfrequenzverfolgung.
- **Nichtnegative Matrixfaktorisierung (NMF)** zur Zerlegung von Spektrogrammen, auch partiturinformiert.

## Nutzen für STEPS

- **Begründung für Mehrdeutigkeit:** Kapitel 5 belegt fachlich, warum STEPS Akkorde nicht auf eine einzige Deutung reduzieren darf. Schon bei Dreiklängen und Septakkorden überlappen sich die Tonmengen.
- **Evaluationsdenken:** Referenzannotationen sind selbst mehrdeutig und haben eine zeitliche Auflösung. Für die STEPS-Golden-Cases folgt daraus: Sollwerte brauchen eine explizite Granularität und gegebenenfalls Alternativen.
- **Chroma als Tonklassenvektor:** Das Modell entspricht der STEPS-Darstellung von Akkorden als Tonklassenmengen. Für eine spätere Audioanalyse wäre es der natürliche Einstieg.
- **Tempo und Beat (Kap. 6)** sowie **harmonisch-perkussive Trennung (Kap. 8)** sind Grundlagen für ein mögliches Groove- oder Drum-Analysemodul.

## Grenzen

- Mathematisch anspruchsvoll. Formeln sind im Extrakt teilweise fehlerhaft.
- Fokus auf Audio. Symbolische Harmonieanalyse (wie STEPS sie heute betreibt) wird nur in den Grundlagenabschnitten berührt.
- Rechtlich problematische Herkunft der Datei (siehe oben).
