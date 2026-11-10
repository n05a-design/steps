
#!/usr/bin/env python3
# STEPS V6.7 – Ausbau 02
# Ergänzt den bestehenden V6.7-Generator.
# Python 3.9+, keine zusätzlichen Pakete.

from pathlib import Path
import create_steps_v6_7_patch as basis


def quelle(nummer, titel, url, bereiche, kern,
           schritte, ergebnis, pruefung):
    return {
        "id": f"AB-V67-{nummer:03d}",
        "titel": titel,
        "url": url,
        "typ": "Ableton-Blog-Tutorial",
        "bereiche": bereiche,
        "kern": kern,
        "schritte": schritte,
        "ergebnis": ergebnis,
        "pruefung": pruefung,
    }


ZUSAETZE = [
    quelle(
        11,
        "A Beginner's Guide to Looping Guitar and Vocals",
        "https://www.ableton.com/en/blog/beginners-guide-to-looping-guitar-and-vocals/",
        ["Komponieren", "Producer Tools", "Arrangement"],
        "Live-Looping verbindet Aufnahme, Timing, Signalrouting und musikalische Form.",
        [
            "Nimm eine eigene vier- oder achttaktige Gitarren-, Keyboard- oder Stimmphrase auf.",
            "Ergänze zwei weitere Loop-Ebenen mit unterschiedlichen musikalischen Funktionen.",
            "Erstelle zwei Formvarianten, indem du die Loops gezielt ein- und ausschaltest."
        ],
        "Zwei Live-Loop-Arrangements mit dokumentierter Signalführung.",
        "Alle Loop-Ebenen bleiben synchron und besitzen unterscheidbare Funktionen."
    ),
    quelle(
        12,
        "A Step-by-Step Guide for Designing Melodic Ear Candy",
        "https://www.ableton.com/en/blog/step-by-step-guide-for-designing-ear-candy/",
        ["Komponieren", "Sounddesign", "Arrangement"],
        "Kurze tonale Klangereignisse können Übergänge und melodische Akzente verstärken.",
        [
            "Nimm drei eigene Alltagsgeräusche auf und wähle ein geeignetes Ausgangsmaterial.",
            "Erzeuge daraus drei Varianten mit Tonhöhenbearbeitung, Resonanz oder Resampling.",
            "Setze die Varianten an drei unterschiedlichen Stellen eines 16-Takt-Arrangements ein."
        ],
        "Ein Arrangement mit drei eigens erzeugten melodischen Akzenten.",
        "Jeder Akzent unterstützt eine hörbare musikalische Funktion."
    ),
    quelle(
        13,
        "Design Hyperpop-Style Metallic Clanks with Voel",
        "https://www.ableton.com/en/blog/design-metallic-clanks-with-voel/",
        ["Sounddesign", "Drums/Rhythmus/Groove"],
        "Resonanz, Verzerrung und Delay können kurze Impulse in komplexe metallische Klänge verwandeln.",
        [
            "Erzeuge einen kurzen perkussiven Impuls mit einem selbst aufgenommenen Klang.",
            "Bearbeite ihn in drei Varianten: resonant, verzerrt und granuliert oder verzögert.",
            "Baue ein achttaktiges Pattern und automatisiere mindestens einen Effektparameter."
        ],
        "Ein eigenes metallisches Percussion-Kit mit drei Klangvarianten.",
        "Die Klangvarianten bleiben trotz Bearbeitung rhythmisch kontrollierbar."
    ),
    quelle(
        14,
        "Explore Push 3's Rhythm Generator with Andri Søren",
        "https://www.ableton.com/en/blog/explore-push-3-rhythm-generator/",
        ["Drums/Rhythmus/Groove", "Komponieren"],
        "Generative Sequenzierung liefert rhythmische Varianten, die anschließend bewusst ausgewählt werden.",
        [
            "Programmiere ein 16-Schritt-Grundpattern mit Kick, Snare und Hi-Hat.",
            "Erzeuge vier Varianten mit veränderten Ereigniswahrscheinlichkeiten oder Notenpositionen.",
            "Wähle zwei Varianten aus und begründe ihre Wirkung auf Groove und Spannung."
        ],
        "Ein Grundpattern, vier Varianten und zwei begründete Favoriten.",
        "Die Unterschiede zwischen Zufall und bewusster musikalischer Auswahl sind nachvollziehbar."
    ),
    quelle(
        15,
        "A Step-by-Step Guide for Designing Sub Bass, Chords and FX",
        "https://www.ableton.com/en/blog/step-by-step-guide-for-sub-bass-chords-and-fx/",
        ["Harmonik", "Akkordfolgen", "Sounddesign"],
        "Subbass, Akkordklang und Effekte können aus einer gemeinsamen Syntheseidee entwickelt werden.",
        [
            "Schreibe die Akkordfolge Am–F–C–G und notiere die enthaltenen Akkordtöne.",
            "Erstelle dazu einen Subbass, der die harmonischen Grundtöne klar unterstützt.",
            "Erzeuge einen kontrastierenden Effektklang und setze ihn an zwei Akkordwechseln ein."
        ],
        "Eine viertaktige Harmonieskizze mit Subbass, Akkorden und Übergangseffekten.",
        "Bass und Akkorde stimmen harmonisch überein; die Übergänge bleiben verständlich."
    ),
    quelle(
        16,
        "A Beginner's Guide to Generating Acid Basslines",
        "https://www.ableton.com/en/blog/a-beginners-guide-to-generating-acid-basslines/",
        ["Akkordfolgen", "Drums/Rhythmus/Groove", "Sounddesign"],
        "Acid-Basslines entstehen durch das Zusammenspiel von Tonfolge, Akzenten, Slides und Filterbewegung.",
        [
            "Schreibe ein eigenes 16-Schritt-Basspattern in A-Moll.",
            "Erstelle drei Varianten mit unterschiedlichen Akzenten, Slides und Pausen.",
            "Automatisiere Filterfrequenz und Resonanz über 16 Takte."
        ],
        "Drei Bassline-Varianten und eine 16-taktige Entwicklung.",
        "Rhythmische Variation und Klangmodulation sind getrennt erkennbar."
    ),
    quelle(
        17,
        "A Step-by-Step Guide on Harmonizing and Layering Vocals",
        "https://www.ableton.com/en/blog/a-step-by-step-guide-on-harmonizing-and-layering-vocals/",
        ["Harmonik", "Komponieren", "Producer Tools"],
        "Mehrstimmige Gesangsschichten erfordern kontrollierte Intervalle und klare Stimmführung.",
        [
            "Nimm eine eigene viertaktige Melodie in C-Dur auf.",
            "Ergänze eine zweite Stimme und prüfe die Intervalle an jedem Akkordwechsel.",
            "Erstelle eine dritte Stimme und vergleiche enge mit weiten Stereo-Positionen."
        ],
        "Ein dreistimmiger Vocal-Satz mit notierten Intervallen.",
        "Die Stimmen passen zur Harmonie und sind einzeln nachvollziehbar."
    ),
    quelle(
        18,
        "A Step-by-Step Guide to Remixing a Track",
        "https://www.ableton.com/en/blog/a-step-by-step-guide-to-remixing-a-track/",
        ["Komponieren", "Arrangement", "Producer Tools"],
        "Remixing verbindet Audiozerlegung, rhythmische Neuinterpretation und eigenständige Arrangement-Entscheidungen.",
        [
            "Nimm eine eigene acht- bis sechzehntaktige Audioskizze auf.",
            "Zerlege sie in rhythmische, melodische und harmonische Elemente.",
            "Baue daraus eine zweite Version mit anderem Tempo, neuer Drumspur und verändertem Formverlauf."
        ],
        "Originalskizze und eigenständige Remix-Version.",
        "Mindestens drei musikalische Veränderungen sind eindeutig dokumentiert."
    ),
    quelle(
        19,
        "Chopping It Up: Make a Classic-Sounding Jungle Track with Drum Sampler",
        "https://www.ableton.com/en/blog/make-a-classic-sounding-jungle-track-with-drum-sampler/",
        ["Drums/Rhythmus/Groove", "Komponieren"],
        "Jungle-Rhythmen nutzen zerteilte Breaks, Synkopen und gezielte Variation.",
        [
            "Programmiere einen eigenen zweitaktigen Break bei 165 BPM.",
            "Zerteile ihn in mindestens acht einzelne Drum-Ereignisse.",
            "Erzeuge eine A- und B-Variante mit unterschiedlichen Ghost Notes und Fills."
        ],
        "Ein 16-taktiges Jungle-Arrangement mit zwei Break-Varianten.",
        "Der Grundpuls bleibt trotz Synkopen und Fills nachvollziehbar."
    ),
    quelle(
        20,
        "Discover Advanced Reharmonizing Techniques with Live 12.1's Auto Shift",
        "https://www.ableton.com/en/blog/discover-advanced-reharmonizing-techniques-with-live-121s-auto-shift/",
        ["Harmonik", "Akkordfolgen", "Sounddesign"],
        "Reharmonisierung verändert den harmonischen Kontext eines bestehenden Klangereignisses.",
        [
            "Erzeuge eine eigene viertaktige Melodie über C–Am–F–G.",
            "Harmonisiere dieselbe Melodie alternativ über Am–Dm–F–G.",
            "Vergleiche beide Versionen und notiere die veränderten Akkordton- und Spannungstonbeziehungen."
        ],
        "Zwei Harmonisierungen derselben Melodie mit kurzer Analyse.",
        "Mindestens vier Töne werden in ihrer harmonischen Funktion korrekt beschrieben."
    ),
    quelle(
        21,
        "A Beginner's Guide to Generating Techno Drum Patterns",
        "https://www.ableton.com/en/blog/generating-techno-drum-patterns/",
        ["Drums/Rhythmus/Groove", "Producer Tools"],
        "Generierte Drum-Patterns werden durch kontrollierte Fills und Klangvariationen musikalisch geformt.",
        [
            "Erstelle einen viertaktigen Techno-Groove mit konstantem Kick-Puls.",
            "Entwickle drei Fill-Varianten mit unterschiedlichen Ereignisdichten.",
            "Vergleiche zwei Drum-Kits bei unverändertem MIDI-Pattern."
        ],
        "Ein Groove, drei Fills und zwei Drum-Kit-Versionen.",
        "Die Wirkung von Pattern und Klangwahl lässt sich getrennt vergleichen."
    ),
    quelle(
        22,
        "Watch dnksaus Experiment with Live 12.4's Updated Delay",
        "https://www.ableton.com/en/blog/watch-dnksaus-experiment-with-the-updated-delay/",
        ["Sounddesign", "Producer Tools", "Arrangement"],
        "Delay kann neben räumlicher Tiefe auch rhythmische und tonale Veränderungen erzeugen.",
        [
            "Nimm einen kurzen eigenen Synth- oder Percussion-Klang auf.",
            "Erstelle drei Delay-Versionen: synchron, moduliert und experimentell.",
            "Automatisiere die Effektintensität über einen acht Takte langen Übergang."
        ],
        "Drei Klangversionen und ein gestalteter Arrangement-Übergang.",
        "Die Delay-Varianten besitzen klar unterscheidbare musikalische Wirkungen."
    ),
    quelle(
        23,
        "How to Streamline Your Sampling Workflow in Live 12.3 with ZW Buckley",
        "https://www.ableton.com/en/blog/paste-bounced-audio-with-zw-buckley/",
        ["Komponieren", "Sounddesign", "Producer Tools"],
        "Resampling verwandelt vorhandene eigene Klangideen in neues musikalisches Ausgangsmaterial.",
        [
            "Erzeuge einen eigenen viertaktigen Synth- oder Percussion-Loop.",
            "Rendere fünf Varianten mit unterschiedlichen Effekten oder Parameterwerten.",
            "Kombiniere mindestens drei Varianten zu einem neuen acht- bis sechzehntaktigen Abschnitt."
        ],
        "Eine selbst erstellte Sammlung aus fünf Samples und eine neue Komposition.",
        "Alle Samples lassen sich auf das eigene Ausgangsmaterial zurückführen."
    ),
    quelle(
        24,
        "Reverb Reflections: Learn How to Get Reverb Right in this Beginner Mixing Tutorial",
        "https://www.ableton.com/en/blog/reverb-beginner-mixing-video-tutorial/",
        ["Producer Tools", "Sounddesign", "Arrangement"],
        "Predelay und frequenzabhängige Bearbeitung helfen, räumliche Tiefe ohne unnötige Maskierung zu erzeugen.",
        [
            "Erstelle einen kurzen Mix aus Kick, Snare, Bass und Lead-Synth.",
            "Vergleiche drei Hallräume bei identischer Lautstärke.",
            "Verändere Predelay und EQ des Hallwegs, bis die Lead-Stimme klarer wahrnehmbar wird."
        ],
        "Drei Mixversionen mit dokumentierten Hallparametern.",
        "Räumlichkeit und Sprach- oder Lead-Verständlichkeit werden bewusst abgewogen."
    ),
    quelle(
        25,
        "Three Creative Tips for Live 12.2 – Roar, Meld and Auto Filter",
        "https://www.ableton.com/en/blog/three-things-to-try-in-ableton-live-12-2/",
        ["Harmonik", "Sounddesign", "Producer Tools"],
        "Verzerrung, mehrstimmige Synthese und Filtermodulation erfüllen unterschiedliche Klangfunktionen.",
        [
            "Schreibe einen vier Takte langen Akkord- und Bassloop.",
            "Erstelle je eine Klangvariante mit Verzerrung, zusätzlicher Oszillatorstimme und Filtermodulation.",
            "Vergleiche die drei Versionen nach harmonischer Klarheit, Bewegung und Klangdichte."
        ],
        "Drei A/B/C-Klangvarianten mit schriftlichem Vergleich.",
        "Jede Bearbeitung besitzt eine nachvollziehbare klangliche Funktion."
    ),
]


def main():
    # Die ursprünglichen 10 Kandidaten bleiben erhalten.
    basis.ARTIKEL.extend(ZUSAETZE)

    # Schutz vor versehentlich doppelten IDs und URLs.
    ids = [a["id"] for a in basis.ARTIKEL]
    slugs = [
        basis.quellenschluessel(a["url"])
        for a in basis.ARTIKEL
    ]

    if len(ids) != len(set(ids)):
        raise ValueError("Doppelte STEPS-IDs entdeckt.")

    if len(slugs) != len(set(slugs)):
        raise ValueError("Doppelte Blog-URLs entdeckt.")

    # Neue Ausgabedatei: Das erste Delta bleibt erhalten.
    basis.OUT = Path(
        "STEPS_V6_7_ERWEITERUNG_AUSBAU_02.zip"
    )

    print("STEPS V6.7 – Ausbau 02")
    print(f"Gesamte Quellenkandidaten: {len(ids)}")
    print("Abgleich mit V6.6 wird gestartet ...")

    # Nutzt den bewährten ZIP-Generator:
    # CSV-Abgleich, Quellenkarten, Praxislabore,
    # Register, QA und SHA256.
    basis.main()


if __name__ == "__main__":
    main()
