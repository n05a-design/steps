---
werk: "Fundamentals of Music Processing – Audio, Analysis, Algorithms, Applications"
autor: "Meinard Müller"
verlag: "Springer (Cham u. a.), © Springer International Publishing Switzerland 2015"
isbn: "978-3-319-21944-8"
seiten: 509   # PDF-Seiten, nicht Buchumfang
quelle_pdf: "research/STEPS_Bibliothek/Fundamentals of Music Proce_ (Z-Library).pdf"
herkunft: "Dateiname nennt Z-Library. Der Inhaber hat am 16.11.2026 entschieden, mit dieser Zusammenfassung normal weiterzuarbeiten."
quelle_sha256: feb755b854a0683cccd611545f4298a9e9d90dcce5839bbde92f14eea27e4767
rechteklasse: E
original: restricted_local (per .gitignore ausgeschlossen)
grundlage: "Docling-Extrakt vom 14.11.2026; vollständige Gliederung, Kapitel 5 (Akkorderkennung) gelesen; korrigiert am 15.11.2026 nach PRUEFBERICHT.md; Abbildungen zu Kapitel 5 am Original-PDF nachgeprüft am 16.11.2026"
stand: 2026-11-16
fachliche_freigabe: false
---

# Meinard Müller: Fundamentals of Music Processing

> Zusammenfassung in eigenen Worten. Formeln und Abbildungen sind nicht wiedergegeben. Tonnamen und Akkordsymbole folgen dem Original (englisch: B = deutsches H, Bb = deutsches B; C = C-Dur-Dreiklang, Cm = c-Moll-Dreiklang). **Herkunftshinweis:** Die zugrunde liegende Datei stammt laut Dateiname von Z-Library. Nach Entscheidung des Inhabers vom 16.11.2026 wird die Zusammenfassung trotzdem normal verwendet.

## Einordnung

Ein Lehrbuch des Fachs Music Information Retrieval (MIR) zur Verarbeitung von Musiksignalen, gedacht für fortgeschrittene Bachelor- und beginnende Masterkurse. Es verbindet Signalverarbeitung (Fourier-Analyse) mit musikalischen Fragestellungen. Nach zwei Grundlagenkapiteln ist jedes Kapitel um eine **Aufgabe** aufgebaut (Synchronisation, Struktur, Akkorde, Tempo, Retrieval, Zerlegung); alle Kapitel enden mit „Further Notes“ zu Literatur und Varianten sowie Übungen. Der Autor arbeitet an den International Audio Laboratories Erlangen. Außerhalb des Buchs (nicht aus dem Extrakt belegt): Zum Buch gibt es öffentlich die „FMP Notebooks“ (Python/Jupyter) mit Implementierungen. Diese sind nicht Teil der Datei.

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
- **Grundlagen der Harmonielehre:** Intervalle, Akkorde, Skalen, Quintenzirkel, funktionale Beziehungen. Akkorde werden als Tonklassenmengen behandelt, ausdrücklich ohne Unterscheidung enharmonisch gleicher Töne.
- **Vorlagenbasierte Erkennung:** Für jedes Zeitfenster wird ein Chromavektor mit binären Vorlagen der 24 Dur- und Molldreiklänge verglichen. Der ähnlichste Akkord wird zugeordnet.
- **Evaluation:** Vergleich mit einer Referenzannotation von Experten. Das Buch zeigt am Beispiel der ersten vier Takte von „Let It Be“ (Fig. 5.1, S. 238; Fig. 5.16, S. 258), dass schon Experten auf unterschiedlichen zeitlichen Ebenen annotieren: halbtaktig als `C – G – Am – F | C – G – F – C` oder feiner als `C – C – G – G | Am – Am – Am7 – Fmaj7 – F6 | C – C – G – G | F – C – Dm7 – C – C` (mit den Durchgangstönen E und D im vierten Halbtakt).
- **Mehrdeutigkeiten** in vier Arten:
  1. *Akkordmehrdeutigkeit (Fig. 5.17, S. 261):* Verwandte Akkorde teilen Töne. C (`C, E, G`) teilt je zwei Töne mit Am (`A, C, E`), Cm (`C, Eb, G`) und Em (`E, G, B`). Cmaj7 (`C, E, G, B`) enthält vollständig C und Em (gleiche Ähnlichkeit $s(t_{\mathrm{Cmaj7}}, t_{\mathrm{C}}) = s(t_{\mathrm{Cmaj7}}, t_{\mathrm{Em}})$) und wird bei nur 24 Klassen leicht einem der beiden zugeordnet. Mehr Akkordklassen verringern dieses Problem, erhöhen aber die Verwechslungsgefahr.
  2. *Akustische Mehrdeutigkeit (Fig. 5.18, S. 263):* Obertöne verteilen Energie auf andere Tonklassen. Ein einzelner tiefer Ton C2 erzeugt über seine ersten acht Teiltöne (`C2, C3, G3, C4, E4, G4, Bb4, C5`) Energie auf C, G, E und Bb. Er wird dann leicht als C erkannt, obwohl er musikalisch auch Grundton von Cm oder Quinte von F sein kann. Beim Dreiklang C bündelt das Chroma-Band G besonders viel Energie (eigener Akkordton plus dritter Teilton von C), sodass das obertongewichtete Muster näher an der binären Vorlage für G als für C liegt. Aus demselben Grund werden Dur und Moll häufig verwechselt (E-Oberton über C konkurriert mit Eb in Cm).
  3. *Stimmung (Fig. 5.19, S. 264):* Aufnahmen weichen von 440 Hz ab (im Beispiel um 50 Cents nach oben verschoben) und verteilen Energie zwischen benachbarten Chroma-Bändern.
  4. *Segmentierung (Fig. 5.20, S. 265):* Gebrochene Akkorde werden als eine harmonische Einheit gehört, obwohl ein kurzes Analysefenster (200 ms, je Sechzehntel höchstens ein Anschlag) nur ein oder zwei Töne enthält (Beispiel: die ersten vier Takte von Bachs Präludium C-Dur BWV 846, taktweise annotiert als `C – Dm – G – C`, wobei Takt 2 in der 24-Klassen-Referenz auf `Dm` vereinfacht ist). Ohne zeitliche Glättung zerfällt die Erkennung in den Takten 2 und 3; erst eine Vorfilterung über 20 Fenster (ca. 2 s) stellt die Taktsegmente her. Die zeitliche Einheit der Analyse entscheidet mit über das Ergebnis.
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
- **Chroma als Tonklassenvektor:** Das Modell ist mit der Darstellung von Akkorden als Tonklassenmengen verwandt und wäre für eine spätere Audioanalyse der natürliche Einstieg. Müller arbeitet dabei ausdrücklich ohne Unterscheidung enharmonisch gleicher Töne; STEPS muss die Schreibweise deshalb getrennt führen.
- **Tempo und Beat (Kap. 6)** sowie **harmonisch-perkussive Trennung (Kap. 8)** sind Grundlagen für ein mögliches Groove- oder Drum-Analysemodul.

## Grenzen

- Mathematisch anspruchsvoll. Formeln sind im Extrakt teilweise fehlerhaft.
- Fokus auf Audio. Symbolische Harmonieanalyse (wie STEPS sie heute betreibt) wird nur in den Grundlagenabschnitten berührt.
- Rechtlich problematische Herkunft der Datei (siehe oben).
