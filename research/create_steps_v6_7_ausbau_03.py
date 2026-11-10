
#!/usr/bin/env python3
# STEPS V6.7 – Ausbau 03
# Eigenständiger ZIP-Generator, Python 3.9+
# Übernimmt Ausbau 02 und ergänzt neue Lernmaterialien.

import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = "STEPS_V6_7_ERWEITERUNG"
OUT = Path("STEPS_V6_7_ERWEITERUNG_AUSBAU_03.zip")

BASIS = Path(
    sys.argv[1] if len(sys.argv) > 1
    else "STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials.zip"
)

VORHER = Path(
    sys.argv[2] if len(sys.argv) > 2
    else "STEPS_V6_7_ERWEITERUNG_AUSBAU_02.zip"
)

QUELLEN = [
    (
        "AB-V67-026",
        "Strike a Chord: Making Melodic Progressions with Feeling",
        "https://www.ableton.com/en/blog/chords-theory-racks-push/",
        "Harmonik und Akkordfolgen",
        "Septakkorde, Umkehrungen und harmonische Bewegung",
        "Schreibe Cmaj7–Am7–Dm7–G7. Erstelle eine Version "
        "in Grundstellung und eine mit möglichst kleinen "
        "Stimmbewegungen. Vergleiche beide.",
        "Zwei MIDI-Versionen mit notierten Akkordtönen."
    ),
    (
        "AB-V67-027",
        "Dubspot's Pat Cupo on Chord Progressions in Live",
        "https://www.ableton.com/en/blog/dubspots-pat-cupo-chord-progressions-live/",
        "Musiktheorie und Akkordfolgen",
        "Aufbau und Anordnung von Akkordfolgen",
        "Entwickle eine eigene viertaktige Folge aus vier "
        "Dreiklängen. Notiere Grundtöne, Akkordqualitäten "
        "und Stufen. Tausche danach zwei Akkorde aus.",
        "Zwei Akkordfolgen mit Stufenanalyse."
    ),
    (
        "AB-V67-028",
        "Afriqua's Principles of Black Music: Polyrhythms",
        "https://www.ableton.com/en/blog/afriqua-presents-principles-of-black-music-polyrhythms/",
        "Rhythmik und Polyrhythmik",
        "Überlagerung rhythmischer Zyklen und ihre musikalische Wirkung",
        "Erstelle sechs gleich große Zeitunterteilungen. "
        "Setze eine Stimme auf die Positionen 0, 2 und 4 "
        "und eine zweite auf 0 und 3. Wiederhole das "
        "Pattern und variiere Klangfarbe und Akzent.",
        "Ein reproduzierbares 3-gegen-2-Pattern."
    ),
    (
        "AB-V67-029",
        "Marina Herlop: Voice and Piano Extended to Infinity",
        "https://www.ableton.com/en/blog/marina-herlop-voice-and-piano-extended-to-infinity/",
        "Komponieren und Harmonik",
        "Kompositorische Beschränkungen und die Übertragung von Harmonien auf andere Klangfarben",
        "Entwickle eine viertaktige Klavierharmonie mit "
        "höchstens drei Akkorden. Übertrage die Stimmen "
        "auf Synthesizer und eigene Vocal-Aufnahmen.",
        "Drei Klangfassungen derselben harmonischen Idee."
    ),
    (
        "AB-V67-030",
        "Celia Hollander Sculpts Time With Sound",
        "https://www.ableton.com/en/blog/ropes-fields-and-waves-celia-hollander-sculpts-time-with-sound/",
        "Komposition und Klanggestaltung",
        "Offene harmonische Strukturen und Zeitgestaltung",
        "Komponiere einen 30-sekündigen Abschnitt mit "
        "drei eng benachbarten Tönen. Verändere nur "
        "Einsatzzeit, Dauer und Klangfarbe.",
        "Eine Klangminiatur mit dokumentierter Entwicklung."
    ),
]

# Zwölf eigenständige STEPS-Module.
# Diese zählen NICHT als neue Ableton-Artikel.

MODULE = [
    (
        "MT-01", "Musiktheorie", "Intervalle und Halbtonabstände",
        "Ein Intervall beschreibt den Abstand zweier Tonhöhen.",
        "Erzeuge aus C4 nacheinander E4, Eb4, G4 und Bb4. "
        "Bestimme die Halbtonabstände 4, 3, 7 und 10.",
        "Vier korrekt bestimmte Intervalle."
    ),
    (
        "MT-02", "Musiktheorie", "Dorisch und natürlich Moll",
        "Die dorische Skala besitzt gegenüber natürlichem Moll eine große Sexte.",
        "Vergleiche A-Dorisch (A B C D E F# G) mit "
        "A-Äolisch (A B C D E F G). Schreibe je eine Melodie.",
        "Zwei Melodien, deren Unterschied an F/F# erkennbar ist."
    ),
    (
        "HA-01", "Harmonik", "Vier Arten von Septakkorden",
        "Septakkorde erweitern Dreiklänge um eine weitere Terz.",
        "Baue Cmaj7, Cm7, C7 und Cm7b5 und notiere "
        "die jeweiligen Akkordtöne.",
        "Vier korrekt aufgebaute Vierklänge."
    ),
    (
        "HA-02", "Harmonik", "Stimmführung und Umkehrungen",
        "Gemeinsame Töne und kleine Stimmbewegungen können Akkordwechsel verbinden.",
        "Schreibe C–Am–F–G in Grundstellung. "
        "Optimiere danach die drei Oberstimmen durch Umkehrungen.",
        "Zwei Voicing-Versionen mit vergleichbaren Stimmbewegungen."
    ),
    (
        "AF-01", "Akkordfolgen", "Tonika, Subdominante und Dominante",
        "In funktionaler Dur-Harmonik bilden I, IV und V zentrale Bezugspunkte.",
        "Schreibe C–F–G–C und ergänze eine eigene Melodie. "
        "Markiere Spannung und Auflösung.",
        "Eine viertaktige Kadenz mit Funktionsanalyse."
    ),
    (
        "AF-02", "Akkordfolgen", "Modal Interchange",
        "Ein entlehnter Akkord stammt aus einem parallelen modalen Kontext.",
        "Vergleiche C–Am–F–G mit C–Ab–F–G. "
        "Beschreibe die Wirkung des Ab-Dur-Akkords.",
        "Zwei harmonische Varianten mit begründeter Auswahl."
    ),
    (
        "KO-01", "Komponieren", "Motivische Entwicklung",
        "Ein kurzes Motiv kann durch Rhythmus, Lage und Kontur verändert werden.",
        "Schreibe ein viertöniges Motiv. Erzeuge "
        "Transposition, rhythmische Variation und Umkehrung der Kontur.",
        "Ein Grundmotiv und drei nachvollziehbare Variationen."
    ),
    (
        "KO-02", "Komponieren", "Musikalische Form",
        "Kontrast und Wiederkehr helfen, längere Abschnitte verständlich zu gestalten.",
        "Arrangiere 32 Takte in A–B–A'-Form. "
        "Nutze mindestens zwei bewusste Unterschiede zwischen A und A'.",
        "Eine 32-taktige Skizze mit dokumentierter Form."
    ),
    (
        "DR-01", "Drums und Groove", "Polyrhythmik 3 gegen 2",
        "Zwei rhythmische Ebenen können dieselbe Dauer unterschiedlich aufteilen.",
        "Erzeuge einen Sechserzyklus mit Impulsen "
        "auf 0, 2, 4 und einer zweiten Stimme auf 0, 3.",
        "Ein korrekt ausgerichtetes 3:2-Pattern."
    ),
    (
        "DR-02", "Drums und Groove", "Swing und Mikrotiming",
        "Die zeitliche Platzierung von Zwischenschlägen beeinflusst den Groove.",
        "Erstelle drei Hi-Hat-Versionen mit geraden Achteln, "
        "verspäteten Offbeats und wechselnder Velocity.",
        "Drei vergleichbare Grooves mit unverändertem Kick-Grundpuls."
    ),
    (
        "PR-01", "Produktion", "Sidechain und Hüllkurven",
        "Dynamische Pegeländerungen können Platz im Mix schaffen oder rhythmisch wirken.",
        "Erstelle einen Kick-Bass-Loop. Vergleiche "
        "Sidechain-Kompression mit kurzer und langer Release-Zeit.",
        "Zwei Mixvarianten mit dokumentierter Release-Einstellung."
    ),
    (
        "PR-02", "Produktion", "Parallele Kompression",
        "Ein stark komprimiertes Signal kann dem trockenen Signal beigemischt werden.",
        "Erstelle einen Drum-Bus und eine stark komprimierte Kopie. "
        "Vergleiche trocken, komprimiert und parallel gemischt.",
        "Drei lautheitsangepasste Hörvergleiche."
    ),
]


def slug(url):
    teile = urlsplit(url).path.strip("/").split("/")
    if "blog" not in teile:
        return ""
    i = teile.index("blog")
    return teile[i + 1].lower() if i + 1 < len(teile) else ""


URL_REGEX = re.compile(
    r"https?://(?:www\.)?ableton\.com/"
    r"(?:[a-z]{2}(?:-[a-z]{2})?)/blog/"
    r"[a-z0-9-]+",
    re.IGNORECASE
)


def alte_slugs(zip_path):
    result = set()
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip():
            raise ValueError("V6.6-ZIP beschädigt.")
        for name in z.namelist():
            if not name.lower().endswith(".csv"):
                continue
            if not any(x in name.lower() for x in
                       ("ableton", "quellen", "register")):
                continue
            raw = z.read(name).decode(
                "utf-8-sig", errors="replace"
            )
            result.update(
                slug(url) for url in URL_REGEX.findall(raw)
            )
    return result


def csv_ausgeben(rows, fields):
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=fields,
        delimiter=";", extrasaction="ignore"
    )
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def main():
    if not BASIS.is_file() or not VORHER.is_file():
        raise FileNotFoundError(
            "V6.6-ZIP oder Ausbau-02-ZIP nicht gefunden."
        )

    basis_slugs = alte_slugs(BASIS)

    with zipfile.ZipFile(VORHER) as z:
        if z.testzip():
            raise ValueError("Ausbau-02-ZIP beschädigt.")
        files = {
            n: z.read(n)
            for n in z.namelist() if not n.endswith("/")
        }

    register_pfad = (
        f"{ROOT}/10_QUELLEN_LIZENZEN/"
        "ABLETONBLOG_V6_7_DELTA.csv"
    )
    if register_pfad not in files:
        raise ValueError(
            "Quellenregister in Ausbau 02 nicht gefunden."
        )

    rows = list(csv.DictReader(
        io.StringIO(
            files[register_pfad].decode("utf-8-sig")
        ),
        delimiter=";"
    ))

    existing_ids = {r["id"] for r in rows}
    existing_slugs = {
        slug(r["url"]) for r in rows
    }

    neu = 0
    duplikate = 0

    for sid, titel, url, bereich, thema, aufgabe, ziel in QUELLEN:
        key = slug(url)

        if key in basis_slugs or key in existing_slugs:
            duplikate += 1
            continue

        if sid in existing_ids:
            raise ValueError(f"ID-Konflikt: {sid}")

        karte = f"""# {titel}

STEPS-ID: {sid}
Quelle: {url}
Themenbereich: {bereich}
Quellentyp: Ableton-Blogbeitrag

## Didaktischer Fokus
{thema}

## Eigenständige Praxisaufgabe
{aufgabe}

## Erwartetes Ergebnis
{ziel}

## Rechte
Nur Link, eigene Zusammenfassung und eigene Übung.
Keine fremden Artikeltexte oder Mediendateien enthalten.

## Prüfstatus
URL über offizielle Ableton-Webquelle recherchiert.
Eingebettete Medien nicht vollständig ausgewertet.
"""

        labor = f"""# Praxislabor {sid}

## Lernziel
{thema}

## Durchführung
{aufgabe}

## Abgabe
{ziel}

## Selbstkontrolle
Dokumentiere die verwendeten Noten, Parameter
oder rhythmischen Entscheidungen. Erstelle
mindestens einen nachvollziehbaren A/B-Vergleich.

## Quelle
{url}
"""

        files[
            f"{ROOT}/20_QUELLENKARTEN/{sid}.md"
        ] = karte.encode("utf-8")

        files[
            f"{ROOT}/30_PRAXISLABORE/{sid}.md"
        ] = labor.encode("utf-8")

        rows.append({
            "id": sid,
            "titel": titel,
            "url": url,
            "quellentyp": "Ableton-Blogbeitrag",
            "bereiche": bereich,
            "rechte": "Nur Link und eigene Lernmaterialien",
            "deduplizierung": "V6.6 und V6.7 geprüft"
        })

        existing_ids.add(sid)
        existing_slugs.add(key)
        neu += 1

    modul_neu = 0

    for mid, bereich, titel, grundlage, aufgabe, ziel in MODULE:
        path = f"{ROOT}/50_ORIGINALMODULE/STEPS-V67-{mid}.md"

        if path in files:
            continue

        content = f"""# {titel}

Modul-ID: STEPS-V67-{mid}
Bereich: {bereich}
Herkunft: Eigenständiges STEPS-Lernmaterial

## Fachliche Grundlage
{grundlage}

## Praxis
{aufgabe}

## Erwartetes Ergebnis
{ziel}

## Qualitätsprüfung
Prüfe die musikalische Richtigkeit,
reproduzierbare Durchführung und klare
Dokumentation des Ergebnisses.

## Weiterführende Aufgabe
Verändere genau einen musikalischen Parameter
und vergleiche beide Ergebnisse.
"""
        files[path] = content.encode("utf-8")
        modul_neu += 1

    fields = [
        "id", "titel", "url", "quellentyp",
        "bereiche", "rechte", "deduplizierung"
    ]
    files[register_pfad] = csv_ausgeben(rows, fields)

    readme = f"""# STEPS V6.7 – Ausbau 03

Dieses Paket ist ein vollständiger Ersatz für das
bisherige V6.7-Delta, NICHT für die V6.6-Basis.

## Inhalt
- {len(rows)} Quellenkarten im V6.7-Delta-Register
- {len(rows)} zugehörige Praxislabore
- 12 eigenständige STEPS-Wissensmodule
- Rechtehinweise, Register und Prüfsummen

## Ausbau 03
- Neue Ableton-Quellen: {neu}
- Gegen vorhandene Register ausgeschlossene Kandidaten: {duplikate}
- Neu erzeugte Originalmodule: {modul_neu}

## Integration
1. V6.6 als Basis behalten.
2. Dieses ZIP in den entpackten V6.6-Ordner entpacken.
3. Den vorhandenen Ordner STEPS_V6_7_ERWEITERUNG
   durch die aktualisierte Delta-Version ersetzen.
4. Das Delta-Register für die STEPS-Suche importieren.
5. Die Originalmodule in die Lernnavigation einbinden.

## Rechte
Keine fremden Artikelvolltexte, Videos,
Sample-Packs oder Live Sets enthalten.

## Hinweis
Der Duplikatabgleich nutzt die CSV-Register.
Er ersetzt keine vollständige Inhaltsprüfung.
"""

    files[f"{ROOT}/00_START_HIER.md"] = (
        readme.encode("utf-8")
    )

    manifest = {
        "projekt": "STEPS",
        "version": "6.7-ausbau-03",
        "basis": "6.6",
        "quellenkarten_delta": len(rows),
        "praxislabore_delta": len(rows),
        "originalmodule": len(MODULE),
        "neue_quellen_ausbau03": neu,
        "duplikate_ausbau03": duplikate,
        "enthaelt_v66_gesamtarchiv": False,
        "enthaelt_fremde_medien": False
    }

    files[f"{ROOT}/QA_MANIFEST.json"] = (
        json.dumps(
            manifest, indent=2, ensure_ascii=False
        ).encode("utf-8")
    )

    hash_path = f"{ROOT}/DATEIEN_SHA256.csv"
    files.pop(hash_path, None)

    checksums = [
        {
            "pfad": name,
            "sha256": hashlib.sha256(data).hexdigest()
        }
        for name, data in sorted(files.items())
    ]

    files[hash_path] = csv_ausgeben(
        checksums, ["pfad", "sha256"]
    )

    with zipfile.ZipFile(
        OUT, "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9
    ) as z:
        for name, data in sorted(files.items()):
            z.writestr(name, data)

    with zipfile.ZipFile(OUT) as z:
        if z.testzip():
            raise RuntimeError("ZIP-Integrität fehlgeschlagen.")

        for row in checksums:
            data = z.read(row["pfad"])
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError(
                    "Prüfsummenfehler: " + row["pfad"]
                )

    print("Erstellt:", OUT.resolve())
    print("Quellenkarten gesamt:", len(rows))
    print("Praxislabore gesamt:", len(rows))
    print("Neue Quellen Ausbau 03:", neu)
    print("Ausgeschlossene Duplikate:", duplikate)
    print("Eigenständige STEPS-Module:", len(MODULE))
    print("ZIP-Integrität und SHA256: OK")


if __name__ == "__main__":
    main()
