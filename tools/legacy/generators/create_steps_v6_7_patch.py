
#!/usr/bin/env python3
# STEPS V6.7 – eigenständiges Erweiterungspaket
# Python 3.9+, nur Standardbibliothek

import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

OUT = Path("STEPS_V6_7_ERWEITERUNG.zip")
ROOT = "STEPS_V6_7_ERWEITERUNG"

ARTIKEL = [
    {
        "id": "AB-V67-001",
        "titel": "DATSUNN: Habits That Make Better Beats",
        "url": "https://www.ableton.com/en/blog/DATSUNN-Habits-That-Make-Better-Beats/",
        "typ": "Künstlerinterview",
        "bereiche": ["Drums/Rhythmus/Groove", "Producer Tools"],
        "kern": "Vorbereitete Sessions und wiederholbare Übungsroutinen erleichtern spontane Beat-Performances.",
        "schritte": [
            "Erstelle eine leere Session mit Kick, Snare, Hi-Hat und einem selbst aufgenommenen Sample.",
            "Spiele ein zweitägiges Übungsprotokoll: je fünf Minuten Timing, Dynamik und Variation.",
            "Nimm vier Takte live auf und vergleiche unbearbeitete mit leicht quantisierten MIDI-Noten."
        ],
        "ergebnis": "Zwei MIDI-Grooves und eine kurze Reflexion über Timing und Spielfluss.",
        "pruefung": "Die Dynamik bleibt hörbar und mindestens eine Variation ist reproduzierbar."
    },
    {
        "id": "AB-V67-002",
        "titel": "Nathan Fake: Live, Reshape, Repeat",
        "url": "https://www.ableton.com/en/blog/nathan-fake-live-reshape-repeat/",
        "typ": "Künstlerinterview",
        "bereiche": ["Komponieren", "Drums/Rhythmus/Groove"],
        "kern": "Improvisierte Clips können durch Auswahl und Umformung zu einer festen Komposition werden.",
        "schritte": [
            "Baue vier unabhängige Clips für Drums, Bass, Harmonie und Textur.",
            "Nimm drei unterschiedliche Live-Durchgänge von je mindestens einer Minute auf.",
            "Wähle die stärksten Übergänge und forme daraus ein Arrangement mit Einleitung, Hauptteil und Schluss."
        ],
        "ergebnis": "Ein Arrangement von mindestens 32 Takten plus drei Rohdurchgänge.",
        "pruefung": "Die finale Form enthält mindestens zwei bewusst ausgewählte Live-Variationen."
    },
    {
        "id": "AB-V67-003",
        "titel": "Cinna Peyghamy: Tombak To The Future",
        "url": "https://www.ableton.com/en/blog/cinna-peyghamy-tombak-to-the-future/",
        "typ": "Künstlerinterview",
        "bereiche": ["Musiktheorie", "Drums/Rhythmus/Groove", "Sounddesign"],
        "kern": "Akustische Percussion kann über Klangbearbeitung zum Ausgangspunkt elektronischer Komposition werden.",
        "schritte": [
            "Nimm mindestens sechs eigene perkussive Klänge auf, etwa Klopfen, Reiben oder Schlagen.",
            "Programmiere ein neun Viertel langes Motiv und markiere seine interne Gruppierung.",
            "Erzeuge aus einer Aufnahme mit Resonanz, Filter oder Vocoder eine tonale Gegenstimme."
        ],
        "ergebnis": "Ein 9/4-Loop mit Percussion und einer aus Percussion abgeleiteten Tonspur.",
        "pruefung": "Der Neunerschlag ist nachvollziehbar, und die tonale Spur bleibt auf die Aufnahme zurückführbar."
    },
    {
        "id": "AB-V67-004",
        "titel": "The Black Dog: From Rothko to Roland to Ableton",
        "url": "https://www.ableton.com/en/blog/the-black-dog-rothko-to-roland-to-ableton/",
        "typ": "Künstlerinterview",
        "bereiche": ["Drums/Rhythmus/Groove", "Sounddesign", "Producer Tools"],
        "kern": "Ein Drum-Klang kann durch Tonhöhen- und Hüllkurvenänderungen mehrere musikalische Funktionen übernehmen.",
        "schritte": [
            "Erzeuge aus einer eigenen Drum-Aufnahme drei Varianten: tief, neutral und hoch.",
            "Lege sie in einem Drum Rack oder vergleichbaren Sampler auf getrennte Pads.",
            "Baue zwei Grooves mit identischem MIDI-Pattern, aber unterschiedlichen Klangvarianten."
        ],
        "ergebnis": "Ein kleines Drum-Kit und zwei vergleichbare Groove-Versionen.",
        "pruefung": "Der Unterschied entsteht hauptsächlich aus Klanggestaltung, nicht aus geänderten Noten."
    },
    {
        "id": "AB-V67-005",
        "titel": "Stoic: From Doechii’s Bullfrog to Cooking Up Paella",
        "url": "https://www.ableton.com/en/blog/stoic-from-doechiis-bullfrog-to-cooking-up-paella/",
        "typ": "Künstlerinterview",
        "bereiche": ["Komponieren", "Harmonik", "Producer Tools"],
        "kern": "Reduzierte Arrangements können durch klar verteilte Funktionen besonders prägnant wirken.",
        "schritte": [
            "Komponiere einen 16-Takt-Loop mit höchstens fünf Spuren.",
            "Verteile die Funktionen auf Rhythmus, Bass, Harmonie, Melodie und optional Textur.",
            "Erstelle eine zweite Version mit drei zusätzlichen Spuren und vergleiche die Klarheit."
        ],
        "ergebnis": "Zwei A/B-Versionen und eine kurze Begründung der bevorzugten Instrumentierung.",
        "pruefung": "In der reduzierten Version sind Bass, rhythmischer Puls und Hauptmotiv unterscheidbar."
    },
    {
        "id": "AB-V67-006",
        "titel": "JJJJJerome Ellis: Reshaping Time",
        "url": "https://www.ableton.com/en/blog/jjjjjerome-ellis-reshaping-time/",
        "typ": "Künstlerporträt",
        "bereiche": ["Komponieren", "Musiktheorie", "Sounddesign"],
        "kern": "Aufgenommene Klänge lassen sich durch Zeitdehnung und Granularbearbeitung neu strukturieren.",
        "schritte": [
            "Nimm zehn Sekunden einer eigenen Stimme oder eines selbst erzeugten Instruments auf.",
            "Erstelle drei Zeitvarianten: Original, stark gedehnt und granular fragmentiert.",
            "Komponiere eine 30-sekündige Miniatur mit einer klaren zeitlichen Entwicklung."
        ],
        "ergebnis": "Eine kurze Klangminiatur und eine Übersicht der verwendeten Zeittransformationen.",
        "pruefung": "Mindestens drei verschiedene Zeitskalen sind hörbar."
    },
    {
        "id": "AB-V67-007",
        "titel": "Lusine: Melting Into The Moment",
        "url": "https://www.ableton.com/en/blog/lusine-melting-into-the-moment/",
        "typ": "Künstlerinterview",
        "bereiche": ["Harmonik", "Komponieren", "Sounddesign"],
        "kern": "Arpeggios und akustische Aufnahmen können zu vielschichtigen Ambient-Texturen transformiert werden.",
        "schritte": [
            "Schreibe ein achttöniges Arpeggio über einem selbst gewählten Akkord.",
            "Bearbeite eine Kopie mit Reverb, Delay oder Granulartechnik, bis die Einzeltöne verschwimmen.",
            "Halte einen harmonischen Anker hörbar und entwickle daraus einen 45-sekündigen Spannungsbogen."
        ],
        "ergebnis": "Eine Ambient-Skizze mit erkennbarem harmonischem Bezug.",
        "pruefung": "Trotz Texturverdichtung ist ein musikalischer Orientierungspunkt erkennbar."
    },
    {
        "id": "AB-V67-008",
        "titel": "A Beginner’s Guide to Creating Chords, Arps and Basslines",
        "url": "https://www.ableton.com/en/blog/beginners-guide-to-chords-bass-melodies/",
        "typ": "Tutorial",
        "bereiche": ["Musiktheorie", "Harmonik", "Akkordfolgen"],
        "kern": "MIDI-Akkord- und Arpeggiator-Werkzeuge können aus einfachen Tonfolgen mehrstimmige Patterns erzeugen.",
        "schritte": [
            "Wähle C-Dur und schreibe die Grundtöne C, A, F und G in vier Takten.",
            "Ergänze die Akkorde C, Am, F und G mit korrekten Dreiklangstönen.",
            "Leite daraus eine Basslinie und ein Arpeggio ab; prüfe jede Note gegen die Harmonie."
        ],
        "ergebnis": "Eine viertaktige Akkordfolge mit Bass und Arpeggio.",
        "pruefung": "Die Akkordtöne sind korrekt benannt und die Basslinie unterstützt die Harmonie."
    },
    {
        "id": "AB-V67-009",
        "titel": "Create Your First Track in Ableton Live with Bad Snacks",
        "url": "https://www.ableton.com/en/blog/create-your-first-track-in-ableton-live/",
        "typ": "Tutorialserie",
        "bereiche": ["Musiktheorie", "Harmonik", "Akkordfolgen", "Komponieren"],
        "kern": "Ein Musikstück entsteht durch die Verbindung von Beat, Akkorden, Bass, Melodie und Arrangement.",
        "schritte": [
            "Entwirf eine viertaktige Akkordfolge und eine dazu passende Basslinie.",
            "Ergänze einen Drum-Groove und eine kurze Melodie mit mindestens einem Wiedererkennungsmotiv.",
            "Arrangiere mindestens 32 Takte mit Einleitung, Hauptteil und Kontrastabschnitt."
        ],
        "ergebnis": "Eine vollständige 32-Takt-Skizze mit dokumentierter Akkordfolge.",
        "pruefung": "Mindestens drei Formabschnitte und ein wiederkehrendes Motiv sind erkennbar."
    },
    {
        "id": "AB-V67-010",
        "titel": "Build a Contemporary Jazz Track from Scratch with Matt Wilde",
        "url": "https://www.ableton.com/en/blog/jazz-from-scratch-with-matt-wilde/",
        "typ": "Tutorial",
        "bereiche": ["Harmonik", "Akkordfolgen", "Komponieren"],
        "kern": "Akkordfarben, rhythmische Variation und ein kontrastierender B-Teil formen ein Jazz-inspiriertes Arrangement.",
        "schritte": [
            "Komponiere einen achttaktigen A-Teil mit mindestens zwei Septakkorden.",
            "Schreibe einen achttaktigen B-Teil mit verändertem harmonischem Rhythmus.",
            "Nutze eine eigene Aufnahme oder Resampling, um einen verbindenden Übergang zu gestalten."
        ],
        "ergebnis": "Eine A-B-Form mit Akkordsymbolen und einem selbst gestalteten Übergang.",
        "pruefung": "A- und B-Teil unterscheiden sich harmonisch und besitzen dennoch einen gemeinsamen Bezug."
    }
]


def quellenschluessel(url):
    """Sprachunabhängiger Ableton-Blog-Slug."""
    teile = urlsplit(url).path.strip("/").lower().split("/")
    if len(teile) >= 3 and teile[1] == "blog":
        return teile[2]
    return urlsplit(url).path.rstrip("/").lower()


def lese_v66_register(zip_pfad):
    """Liest Blog-URLs aus passenden CSV-Registern der V6.6-ZIP."""
    if not zip_pfad:
        return set(), False

    datei = Path(zip_pfad)
    if not datei.is_file():
        raise FileNotFoundError(f"V6.6-ZIP nicht gefunden: {datei}")

    slugs = set()
    register_gefunden = False
    url_muster = re.compile(
        r"https?://(?:www\.)?ableton\.com/"
        r"(?:en|de)/blog/[^\s\"'<>,;]+",
        re.IGNORECASE
    )

    with zipfile.ZipFile(datei) as archiv:
        if archiv.testzip() is not None:
            raise ValueError("Die V6.6-ZIP ist beschädigt.")

        for name in archiv.namelist():
            upper = name.upper()
            if not upper.endswith(".CSV"):
                continue
            if not any(x in upper for x in
                       ("ABLETON", "QUELLEN", "REGISTER")):
                continue

            register_gefunden = True
            text = archiv.read(name).decode(
                "utf-8-sig", errors="replace"
            )

            for url in url_muster.findall(text):
                slugs.add(quellenschluessel(url))

    return slugs, register_gefunden


def csv_text(zeilen, spalten):
    puffer = io.StringIO()
    writer = csv.DictWriter(
        puffer, fieldnames=spalten, delimiter=";"
    )
    writer.writeheader()
    writer.writerows(zeilen)
    return puffer.getvalue()


def quellenkarte(a):
    return f"""# {a['titel']}

- STEPS-ID: {a['id']}
- Quelle: {a['url']}
- Quellentyp: {a['typ']}
- Bereiche: {', '.join(a['bereiche'])}
- Herkunft: Ableton Blog
- Status: Link recherchiert; Medien nicht archiviert

## Eigenständige didaktische Zusammenfassung

{a['kern']}

## Bezug zur STEPS-Wissensbibliothek

Diese Quelle dient als Ausgangspunkt für eine eigene
Lernaufgabe. Die fachlichen Begriffe sollen in STEPS
mit Musiktheorie, Harmonik, Akkordfolgen, Komposition
oder Produktionspraxis verknüpft werden.

## Zugehöriges Praxislabor

Siehe 30_PRAXISLABORE/{a['id']}.md

## Rechte und Quellenabgrenzung

Kein Artikelvolltext, kein Video, kein Audiomaterial,
kein Ableton Live Set und keine Drittanbieter-Presets
sind in diesem Erweiterungspaket enthalten.
Die Zusammenfassung und Lernaufgabe sind eigenständig.
"""


def praxislabor(a):
    schritte = "\n".join(
        f"{i}. {s}"
        for i, s in enumerate(a["schritte"], 1)
    )
    return f"""# Praxislabor {a['id']}

## Thema
{a['titel']}

## Lernziel
{a['kern']}

## Durchführung

{schritte}

## Abgabe
{a['ergebnis']}

## Erfolgskriterium
{a['pruefung']}

## Transferfrage
Wie verändert sich das Ergebnis, wenn du genau einen
Parameter oder eine musikalische Entscheidung änderst?

## Quellenhinweis
{a['url']}

Dieses Praxislabor ist eine eigenständige STEPS-Aufgabe
und keine Abschrift des Ableton-Beitrags.
"""


def main():
    basis = sys.argv[1] if len(sys.argv) > 1 else None
    vorhanden, register_ok = lese_v66_register(basis)

    # Ohne lesbares Register keine bestätigte Deduplizierung.
    if register_ok:
        neu = [
            a for a in ARTIKEL
            if quellenschluessel(a["url"]) not in vorhanden
        ]
        duplikate = [
            a for a in ARTIKEL
            if quellenschluessel(a["url"]) in vorhanden
        ]
        status = "Mit V6.6-CSV-Registern abgeglichen"
    else:
        neu = list(ARTIKEL)
        duplikate = []
        status = "Deduplizierung gegen V6.6 nicht bestätigt"

    dateien = {}

    def add(pfad, inhalt):
        dateien[f"{ROOT}/{pfad}"] = inhalt.encode("utf-8")

    add("00_START_HIER.md", f"""# STEPS V6.7 – Delta-Erweiterung

Dies ist KEINE vollständige STEPS-Bibliothek.
Die Erweiterung ist für die bestehende V6.6 gedacht.

## Inhalt
- {len(neu)} Quellenkarten
- {len(neu)} eigenständige Praxislabore
- Quellenregister als CSV
- Rechte- und Integrationshinweise
- QA- und SHA256-Manifeste

## Prüfung
{status}

Ausgeschlossene URL-Duplikate: {len(duplikate)}

## Installation
1. Entpacke diese ZIP.
2. Kopiere den Ordner STEPS_V6_7_ERWEITERUNG
   in das Hauptverzeichnis deiner V6.6-Bibliothek.
3. Prüfe das Delta-Quellenregister gegen dein
   bestehendes kumulatives Register.
4. Übernimm bestätigte neue Datensätze in die
   STEPS-Suchindizes und Navigationsstruktur.
5. Behalte die ursprünglichen V6.6-Dateien unverändert.

## Wichtig
Dieses Delta enthält keine fremden Medien,
keine Ableton-Artikelvolltexte und keine
kommerziell eingeschränkten Downloads.
""")

    register = []
    for a in neu:
        register.append({
            "id": a["id"],
            "titel": a["titel"],
            "url": a["url"],
            "quellentyp": a["typ"],
            "bereiche": " | ".join(a["bereiche"]),
            "rechte": "Nur Link und eigene Lernmaterialien",
            "deduplizierung": (
                "V6.6-Register geprüft"
                if register_ok else "Noch gegen V6.6 prüfen"
            )
        })
        add(
            f"20_QUELLENKARTEN/{a['id']}.md",
            quellenkarte(a)
        )
        add(
            f"30_PRAXISLABORE/{a['id']}.md",
            praxislabor(a)
        )

    spalten = [
        "id", "titel", "url", "quellentyp",
        "bereiche", "rechte", "deduplizierung"
    ]
    add(
        "10_QUELLEN_LIZENZEN/ABLETONBLOG_V6_7_DELTA.csv",
        csv_text(register, spalten)
    )

    add("10_QUELLEN_LIZENZEN/RECHTE_AUDIT.md",
"""# Rechte-Audit V6.7

## Im Paket enthalten
- bibliografische Angaben und Original-URLs
- eigene kurze didaktische Zusammenfassungen
- eigenständig formulierte Praxislabore
- Register und technische Integrationshinweise

## Nicht enthalten
- urheberrechtlich geschützte Artikelvolltexte
- Videos, Podcasts und Bilder
- fremde Audio- oder MIDI-Dateien
- Live Sets, Presets oder Sample-Packs

## Offene Prüfungen
- Nutzungsrechte bei jedem späteren Mediendownload
- Verfügbarkeit und Lizenzbedingungen externer Assets
- eventuelle Titel- oder URL-Duplikate im Gesamtregister
- technische Eignung für die bestehende STEPS-Struktur

Links auf öffentliche Webseiten sind keine
Lizenz zur Weiterverbreitung der dortigen Dateien.
""")

    add("40_INTEGRATION/CODEX_AUFTRAG.md",
"""# Codex-Auftrag: STEPS V6.7 integrieren

1. Bestehende V6.6-Struktur nur lesend analysieren.
2. Dateiliste und Quellenregister inventarisieren.
3. Delta-CSV laden und URLs kanonisieren.
4. Doppelte Blog-Slugs und Titel abgleichen.
5. Nur neue Quellenkarten und Praxislabore übernehmen.
6. Suchindex und Themen-Navigation aktualisieren.
7. Vier Kernpfeiler getrennt ausweisen:
   Musiktheorie, Harmonik, Akkordfolgen, Komponieren.
8. Drums/Rhythmus/Groove sowie Producer Tools als
   eigenständige Themenbereiche führen.
9. Herkunft, Rechte und Lernaufgaben verknüpfen.
10. Tests für IDs, URLs, Duplikate und Navigation
    ergänzen und Änderungen dokumentieren.

Keine bestehende Datei ohne vorherige Prüfung
überschreiben. Keine Live Sets oder Medien nachladen.
""")

    add("40_INTEGRATION/QUALITAETSPRUEFUNG.md",
"""# Qualitätssicherung

- [ ] V6.6-Dateien unverändert
- [ ] Keine doppelten kanonischen Blog-URLs
- [ ] Keine doppelten STEPS-IDs
- [ ] Alle Quellenkarten haben gültige Quell-URLs
- [ ] Alle Quellenkarten besitzen ein Praxislabor
- [ ] Vier STEPS-Kernpfeiler sind auffindbar
- [ ] Drum/Groove und Producer Tools sind eigenständig
- [ ] Keine fremden Mediendateien eingebettet
- [ ] Rechtehinweise in der Navigation zugänglich
- [ ] Suchindex nach Import neu aufgebaut
""")

    manifest = {
        "projekt": "STEPS",
        "version": "6.7-delta",
        "basis": "6.6",
        "kandidaten": len(ARTIKEL),
        "aufgenommene_quellen": len(neu),
        "ausgeschlossene_duplikate": [
            {"id": a["id"], "url": a["url"]}
            for a in duplikate
        ],
        "register_pruefstatus": status,
        "enthaelt_v66_gesamtarchiv": False,
        "enthaelt_drittmedien": False
    }
    add(
        "QA_MANIFEST.json",
        json.dumps(
            manifest, ensure_ascii=False, indent=2
        ) + "\n"
    )

    # Prüfsummen aller Nutzdateien, außer der
    # Prüfsummenliste selbst.
    hash_zeilen = []
    for pfad, daten in sorted(dateien.items()):
        hash_zeilen.append({
            "pfad": pfad,
            "sha256": hashlib.sha256(daten).hexdigest()
        })

    add(
        "DATEIEN_SHA256.csv",
        csv_text(hash_zeilen, ["pfad", "sha256"])
    )

    with zipfile.ZipFile(
        OUT, "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9
    ) as z:
        for pfad, daten in sorted(dateien.items()):
            z.writestr(pfad, daten)

    # ZIP-Integrität und Datei-Prüfsummen prüfen.
    with zipfile.ZipFile(OUT) as z:
        fehler = z.testzip()
        if fehler:
            raise RuntimeError(
                f"ZIP-Integritätsfehler: {fehler}"
            )
        for eintrag in hash_zeilen:
            daten = z.read(eintrag["pfad"])
            ist = hashlib.sha256(daten).hexdigest()
            if ist != eintrag["sha256"]:
                raise RuntimeError(
                    f"SHA256-Abweichung: {eintrag['pfad']}"
                )

    print(f"Erstellt: {OUT.resolve()}")
    print(f"Neue Quellenkarten: {len(neu)}")
    print(f"Praxislabore: {len(neu)}")
    print(f"Ausgeschlossene Duplikate: {len(duplikate)}")
    print(f"Registerstatus: {status}")
    print("ZIP-Integrität und SHA256: OK")


if __name__ == "__main__":
    main()
