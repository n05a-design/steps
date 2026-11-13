# PR #22 – Hashabgleich und vollständiger Prüfgegenstand

Geprüfter PR-Head: `16871f1e1609a1af0a28b2bdb999a6ad87f6d15b`.
Historischer Vergleich: `b0abd41`, die bereits eingegrenzte Fassung des Piloten.
Der hier dokumentierte damalige Übergang ist inzwischen durch die
[menschliche Freigabe vom 13. November 2026](https://github.com/n05a-design/steps/pull/22#issuecomment-6842512635)
abgeschlossen. Register und Lerntexte wurden auf die neuen Hashes gebracht.
Die unten genannten alten Ausgabestände beziehen sich auf den geprüften
Zwischenstand `16871f1`, nicht auf den aktuellen Abschlussstand.
Die aktuellen Hashes wurden mit direktem `hashlib.sha256` auf unabhängig aus
den Git-Blobs zusammengesetzten JSON-Payloads berechnet und anschließend mit
den Ergebnissen des produktiven Loaders verglichen. Alle acht Hashes stimmen
überein: sieben geänderte PROG-Claims und eine unveränderte Notationskonvention.

## Ergebnis für PROG-001-TONAL-CENTER

| Prüfstand | Vollständiger Fingerabdruck |
| --- | --- |
| Bereits eingegrenzte Aussage, alte Kopie-URL und alter Locator | `1b52fd68d6ef6e1aeecd3ed6062b9786e4c202d3a23ae425d4c648c8d3181429` |
| Zwischenrechnung: ausschließlich URL auf die Hauptausgabe umgestellt | `0e162dfc69933d36b09f49417d7c4a5c5b9d48d35bba750d3cef9c749ae2b7b3` |
| Aktueller PR: kanonische URL und korrigierter Locator | `b39ac7b557f1d7846c3c7ec006ebec60b0fbc78b205ae1540d14817ee849a789` |

Die Zwischenrechnung ist ein kontrollierter Gegencheck, keine freizugebende
Produktfassung. Zwischen altem und aktuellem Payload ändern sich genau:

1. `sources.omt-four-chord-schemas.url`: von
   `https://viva.pressbooks.pub/openmusictheorycopy/chapter/4-chord-schemas/`
   auf `https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/`.
2. `claim.references[0].locator`: von „Absatz nach Example 4“ auf
   „Absatz vor der Legende zu Example 4“, jeweils im bestehenden vollständigen
   Fundstellentext.

Wortlaut, Art, Gültigkeitsbereich, Gegencheck und Beispielkontext sind identisch.
`b39ac7b5...` bezeichnet damit dieselbe bereits sauber eingegrenzte musikalische
Aussage mit korrigiertem Quellenbezug, keine Rückkehr zu einer früheren unpräzisen
Aussage. Für den aktuellen PR ist dieser Fingerabdruck erforderlich.

## Warum im geprüften Zwischenstand noch 1b52fd68 stand

`knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md` ist eine generierte
Ausgabe des zuletzt freigegebenen Katalogs. Dort steht weiterhin `1b52fd68...`
zusammen mit Kopie-URL, altem Locator und der Entscheidung aus PR #11. Diese
Datei berechnet keine Fingerabdrücke und ist nicht die Eingabe des aktuellen
Claim-Hashs.

Auch `reviewed_progression_approvals.json` enthält noch den alten Beleg.
Die aktuelle `knowledge/benchmark/PILOT_ABNAHME.md` zeigt dagegen `b39ac7b5...`
und den Status „Erneute Prüfung erforderlich“. Das ist der noch nicht
abgeschlossene Übergang zur neuen Quellenfassung. Er erklärt die roten
Publikationsgates; er wird nicht durch ein Zurücksetzen des Freigabeblocks
auf den alten Hash repariert.

Der Gegencheck mit dem echten `_approve` weist den alten Registereintrag für den
aktuellen Claim erwartungsgemäß zurück. Neue Freigaben und neue Lerntexte dürfen
erst nach dem passenden menschlichen Kommentar erzeugt werden.

## Was der Fingerabdruck bindet

Der SHA-256 wird über UTF-8-JSON mit `ensure_ascii=False`, `sort_keys=True` und
`separators=(",", ":")` gebildet. Das Payload enthält genau:

- `format`: Hashformat 1;
- `example`: ID, Name, Tonart, Stufen, Akkordsymbole und Kontext des Beispiels,
  zusätzlich den Fingerabdruck der Notationskonvention;
- `claim`: ID, Art, Wortlaut, Gültigkeitsbereich, Gegencheck, Quellenreferenzen
  mit Locator und gegebenenfalls `voice_path`;
- `sources`: die vollständigen referenzierten Metadatensätze aus dem
  Produktquellenregister.

Die Benchmark-Prüffrage, deren `expected`-JSON und `basis`-Herleitung gehen
**nicht** in diesen Claim-Fingerabdruck ein. Auch die Bytes einer externen
Webseite oder eines PDFs werden damit nicht gehasht. Ein passender Hash beweist
die Identität des so definierten Datenstands, nicht dessen fachliche Richtigkeit
und nicht eine kryptografisch gesicherte Identität des externen Volltexts.

Die Sollantworten werden separat durch den Benchmark, die Abnahmeliste und die
fachliche Gegenprüfung beurteilt. Diese Nachweisgrenze wird nicht durch eine
stillschweigende Änderung des Hashformats aufgehoben; das würde selbst neue
Freigabegegenstände erzeugen.

## Exakte Datensätze zur menschlichen Prüfung

Das [Prüfpaket](PR22_FREIGABE_PRUEFPAKET_2026-11-13.json) enthält je Claim:

- `hashed_payload`: sämtliche tatsächlich gehashten Daten inklusive exakter
  Texte, Gültigkeitsbereiche, Fundstellen und Quellenmetadaten;
- `fingerprint`: unabhängig nachgerechneter Claim-Hash;
- `benchmark_case_not_in_claim_fingerprint`: den vollständigen zugehörigen
  Pilotbenchmarkfall, ausdrücklich außerhalb des Claim-Hashs;
- auf Dateiebene zusätzliche SHA-256-Werte der versionierten Eingabeblobs.

Die zusätzlichen Datei-Prüfsummen dienen dem dokumentierten Snapshot-Abgleich.
Sie sind keine neuen vom produktiven Verifier verlangten Freigabehashes.

## Abgleich der Notation und Sollwerte

| Datensatz | Geprüfter Stand |
| --- | --- |
| PROG-001-HARMONY | Internationale Akkordsymbole `C`, `G`, `Am`, `F`; korrekte Tonklassenmengen. |
| PROG-003-HARMONY | Internationale Akkordsymbole `Dm7`, `G7`, `Cmaj7`; deutsche Notennamen nur in erklärender Prosa; korrekte Tonklassenmengen. |
| PROG-009-HARMONY | Internationale Akkordsymbole `C`, `F`, `Fm`, `C`; korrekte Tonklassenmengen einschließlich As = Tonklasse 8. |
| PROG-003-VOICE-II-V | `C4` → `H3`, explizit als deutsche Notennamen gelesen; MIDI 60 → 59, Delta −1. |
| PROG-003-VOICE-V-I | `F4` → `E4`; MIDI 65 → 64, Delta −1. |
| PROG-009-VOICE-LEADING | `A4` → `As4` → `G4`, deutsche Notennamen; MIDI 69 → 68 → 67, Deltas −1/−1. Der Claim sagt „Halbtonschritte“, nicht pauschal „diatonische Schritte“. A→As ist chromatisch, As→G diatonisch. |

Die beiden Notationssysteme sind damit nach ihrer Rolle getrennt, nicht
versehentlich vermischt: internationale Akkordsymbole, deutsche benannte
Stimmen und numerische Tonklassen/MIDI-Werte. Die sechs berechenbaren
`expected`-Datensätze wurden vollständig gegen unabhängige Literalwerte
abgeglichen. Der siebte Claim lässt C, A und die Mehrdeutigkeit offen und
benennt die notwendigen Kontexthinweise.

PILOT-NOTATION-001 steht im selben Freigaberegister wie die sieben PROG-Claims.
Es fehlt im neuen Kommentar, weil sein Fingerabdruck weiterhin passt. Sein
Gegencheck nennt ausdrücklich H3/B3, deutsches B3/internationales B♭3 und
As4/A♭4. `C4=60` ist in der Benchmark-Herleitung dokumentiert. Dieser Satz steht
nicht zusätzlich im gehashten `scope`-Feld. Soll er dort ergänzt werden, würde
sich der Notationshash ändern und über `example.notation` alle sieben PROG-Hashes
mitändern. Eine solche Inhalts-/Schemaänderung wurde hier nicht vorgenommen.

## Kopierfassung

Die [Freigabevorlage](PR22_FACHFREIGABE_VORLAGE.md) enthält den kompletten
Kommentar in einem einzigen Codeblock mit genau einem Einleitungssatz.
Die separat bereitgestellte TXT-Fassung enthielt bereits genau einen solchen
Einleitungssatz. Nach dem ausdrücklichen Veröffentlichungsauftrag wurde der
Kommentar veröffentlicht und wurden die sieben neuen Freigaben mit dem echten
Permalink eingetragen. Die Hash-Eingaben selbst bleiben unverändert.
