# CSS-Provenienz · Archivkette und Live-Gegenprobe

Basis: `9c7b8eb3fabdf09e41f26d589a892c25bc051f87`, Merge von
[PR #51](https://github.com/n05a-design/steps/pull/51). Der PR wurde von
`n05a-design` freigegeben und am 13.11.2026 um 23:58 Uhr Europe/Berlin
gemergt. Seine zwölf Check-Läufe und die vier nachfolgenden Main-Workflows
sind erfolgreich. Die vorliegende Fortsetzung datiert vom 14.11.2026.

## Technisch bestätigte Herkunftskette

Der [Hashfund aus PR #51](STEPS_FABLE_5_2_ARCHIVNACHWEISE.md) lässt sich
inzwischen mit einer konkreten Auslieferungsquelle verbinden. Der lokale
Baum `5f1dea83c437aa54267e5f2ca9259a196f141852` enthält neben den sechs
CSS-Pfaden insgesamt 17 passende gespeicherte Bandcamp-Playerseiten.
Jede dieser Seiten nennt ihre Embed-URL im Browser-Speicherkommentar und
referenziert die CSS-Datei als Stylesheet im selben Ordner.

| Register-ID | Passende gespeicherte Playerseiten | Lokaler Blob | Live-CDN |
| --- | ---: | --- | --- |
| F00412 | 5 | MATCH | MATCH |
| F00571 | 2 | MATCH | MATCH |
| F00704 | 2 | MATCH | MATCH |
| F00768 | 5 | MATCH | MATCH |
| F00937 | 2 | MATCH | MATCH |
| F01002 | 1 | MATCH | MATCH |

Für jeden der sechs Registereinträge wurde eine der zugehörigen Embed-URLs
live geöffnet. Alle sechs identifizieren dasselbe Stylesheet unter
[Bandcamps CDN](https://s4.bcbits.com/client-bundle/1/trackpipe/embedded_player-d605d516704fd10722142526feae0317.css).
Die heruntergeladenen Antwortbytes stimmen jeweils mit dem Register überein:

- Größe: **63.332 Bytes**.
- SHA-256: `32289d8747feddbc21cccedc6522f0f1ab2b18bf2a0c5d9a65356f8fdc9f5f29`.
- Lokaler Git-Blob: `a1c1bd8389455e29e6124186a9a7108ca6c56fad`.

Der [strukturierte Bericht](CSS_PROVENIENZ_2026-11-14.json) nennt die
17 HTML-Zeugen mit Pfad, Blob-ID, SHA-256 und Embed-URL sowie die sechs
Live-Vergleiche mit Abrufzeit. Er enthält keine HTML- oder CSS-Volltexte.
Ein HTTP-Last-Modified-Wert ist ein Servermetadatum, kein Beleg für den
historischen Zeitpunkt der lokalen Speicherung.

## Reproduktion

Der [Prüfer](../../../scripts/verify_css_provenance.py) liest Rohblobs,
extrahiert nur die relevante Stylesheet-Referenz und die gespeicherte
Bandcamp-Embed-URL und vergleicht optional die Live-CDN-Bytes. Er führt
keinen heruntergeladenen Code aus. `--online` muss ausdrücklich gesetzt
werden; die Test-Suite verwendet synthetische HTTP-Antworten.

```sh
python -B scripts/verify_css_provenance.py --repository <lokales-Objektarchiv> --tree 5f1dea83c437aa54267e5f2ca9259a196f141852 --online --json-out css-provenance.json
python -B -m unittest tests.test_css_provenance -v
```

Ergebnis je Eintrag: lokaler Hash MATCH, gespeicherte Herkunftskette MATCH,
Live-Quelle MATCH. Ein fehlender oder abweichender Nachweis liefert Exit 1;
ein nicht lesbarer lokaler Git-Baum Exit 2. Der lokale Sicherungsbaum
gehört weiterhin nicht automatisch zu einem frischen GitHub-Clone.

## Rechte und Abnahme bleiben offen

Der Blob enthält einen jQuery-UI-1.9.2-Komponentenhinweis mit MIT-Vermerk.
Weitere Abschnittsmarker verweisen auf Player-, Layout-, Dialog- und
Sharing-Styles unter `trackpipe/public/`. Der
[jQuery-Lizenztext](https://jquery.com/license/) beschreibt die Lizenz
der betreffenden Projekte. Daraus lässt sich keine Lizenz für die übrigen
Bestandteile des Bandcamp-Bundles ableiten.

Die sechs Registerzeilen nennen deshalb nun Bandcamp als technisch
belegte Auslieferungsquelle und den jQuery-Komponentenhinweis. Die bisherige
Annahme eigenen Projekttexts ist durch
`THIRD_PARTY_WEB_ASSET_RIGHTS_UNREVIEWED` ersetzt. Pfad, Größe, Hash und
`METADATA_ONLY` bleiben erhalten. Das Bundle wurde nicht in die
veröffentlichten Projektdateien übernommen.

Die technische Quellenzuordnung ist geklärt. Rechte am vollständigen
Bundle, dauerhafte Archivzuordnung und erforderliche Fachabnahme sind
weiterhin offen. Die sechs manuellen Benchmarkfälle bleiben PENDING;
ihre nächsten Schritte nennen jetzt diese verbliebenen Anforderungen.
