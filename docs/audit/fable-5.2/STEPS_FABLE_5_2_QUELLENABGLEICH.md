# Fable-Audit · Quellenabgleich und historische Gegenproben

Geprüfter Ausgangsstand `38a1544bb28acde9997128da5b8b89c739ea8c97`.
Die Ergebnisse betreffen Forschungsclaims. Die Quellenfreigabe für die
App erfolgt weiterhin über das Produktregister.

| Claim | Nachprüfung | Fundstelle |
| --- | --- | --- |
| 003 | Zwölf reine Quinten ergeben relativ zu sieben Oktaven den Quotienten 531441/524288. Mit 1200 × log₂ ergibt sich 23,4600 Cent. | [Jonathan Walker, I.4–I.5](https://www.mtosmt.org/issues/mto.96.2.6/mto.96.2.6.walker.html) |
| 004 | 5:4 und 6:5 über demselben Grundton bezeichnen die reine große bzw. kleine Terz. Die reine Quinte hat 3:2. Ob ein fester Tonvorrat diese Verhältnisse in jedem Dreiklang erreicht, hängt von seiner Stimmung ab. | [Roger Wibberley, Abs. 20 und vorangehende Rechnung](https://www.mtosmt.org/retrofit/mto.04.10.1/mto.04.10.1.wibberley1.php) |
| 005 | Ein Viertel des syntonischen Kommas 81:80 ergibt 5,3766 Cent. Die reguläre Quinte misst 696,5784 Cent. Vier reguläre Quinten abzüglich zwei Oktaven ergeben 5:4. Bei elf solchen Quinten misst die Schließungsquinte 737,6373 Cent. | [Kenneth P. Scholtz, §§6.1–6.4](https://www.mtosmt.org/issues/mto.98.4.4/mto.98.4.4.scholtz.html) |
| 006 | C–E überspannt drei verengte Quinten und eine reine Quinte. Daraus ergeben sich 390,225 Cent. F♯–B♭ über vier reine Quinten ergibt 407,820 Cent. B♭ belegt hier dieselbe Taste wie A♯. | [Dave Benson, §5.11](https://www.lpthe.jussieu.fr/~talon/MUSIC5.PDF) · [Ausgabe bei Cambridge University Press](https://doi.org/10.1017/CBO9780511811722.007) |
| 023 | C/E und C/G haben Akkordtöne im Bass und zeigen erste bzw. zweite Umkehrung. C/F♯ zeigt einen akkordfremden Slash-Bass. | [Megan Lavengood, Chord Symbols, Bass notes](https://viva.pressbooks.pub/openmusictheory/chapter/chord-symbols/) |
| 028 | G7 hat H und F, D♭7 hat F und C♭ als Terz und Septime. In 12-TET sind H und C♭ dieselbe Tonklasse. | [Megan Lavengood, Substitutions](https://viva.pressbooks.pub/openmusictheory/chapter/substitutions/) |
| 043 | MusicXML erfasst Zeitverhältnis und grafische Auszeichnung mit unterschiedlichen Elementen. Die Beispielnotation verwendet getrennte Start- und Stop-Attribute. | [W3C, time-modification](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/time-modification/) · [W3C, tuplet](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/tuplet/) |

Die OMT-Fundstellen waren im Suchindex lesbar. Der direkte Abruf
lieferte in dieser Sitzung zeitweise HTTP 403. Die Referenzen verweisen
auf die kanonischen Kapitel. Die alten Buchseiten sind als historische
Zuschreibungen erhalten. Die Existenz der unter SRC-033 angegebenen
Publikation bleibt ungeklärt. Im Claim-Register stehen weiterhin
21 Platzhalter mit eigener ID und ohne überprüfbare Aussage.

## H02 · OpenAI-Übergabebericht

Stichprobe gegen die Git-Objekte `fe66637`, `22f3f5f` und `38a1544`.
Die historischen Aussagen stehen im
[OpenAI Steps Bericht](../../../archive/agent-history/openai/OpenAI_Steps_Bericht/OpenAI%20Steps%20Bericht.md).

- Die Merge-Eltern von `02f3776` enthalten `fe66637`. Dessen Elterncommit
  ist `bb14fce`. Die Abstammung reicht bis zum aktuellen `main`.
- `git ls-tree -r` bestätigt 3975 versionierte Pfade und 1580 Glide-Pfade
  auf `fe66637`. Die 1580 Glide-Pfade sind auch auf `22f3f5f` vorhanden.
- Das Quellenregister listet 344 `REVIEWED_FULL`, 26 `PARTIAL` und
  1525 `METADATA_ONLY` auf `fe66637` und `22f3f5f`. Das bestätigt
  die historischen Labelzahlen. Die Zahl tatsächlich fachlich abgenommener
  Quellen lässt sich daraus allein nicht ableiten.
- Beide Stände führen 97 Relationen. PROG-021 und PROG-028 haben in den
  Katalogen die im Bericht genannten verschiedenen Akkordfolgen.
- Der historische Golden-Master umfasst 63 UNIT, 3 PROPERTY, 1
  INTEGRATION und 131 SPEC. Auf `38a1544` sind es 60 ausgeführte
  Berechnungs- oder Produktfälle und 138 Strukturprüfungen.
- Die GitHub-Abfrage für `fe66637` zeigt die damaligen Läufe als
  `queued`. Für `38a1544` sind Python-Matrix, Skill, Struktur,
  Secret-Scan und Pilotbelege im Zielcommit bestätigt.
  [Historischer Python-Lauf](https://github.com/n05a-design/steps/actions/runs/43097534590)
  · [Aktuelle Python-Matrix](https://github.com/n05a-design/steps/actions/runs/43361781637)

## M2 · Registermigration aus dem bereitgestellten Snapshot

Der Export unter `docs/operations` und die lokale Kopie im
OneDrive-Hauptcheckout sind bytegleich. SHA-256
`dd27e30cfc706d6d2aa8b0a94bcd245e9c4f8804fb272db0c0665096f1cdc7f3`.
Der Snapshot enthält 33 unterschiedliche OA-IDs. Backup, Restore,
Sicherung des Vorzustands und dessen Rücksicherung wurden mit dieser
Kopie bytegleich geprüft.

Die heutige strikte Prüfung meldet bei OA-0002, OA-0011 und OA-0013
je vier fehlende strukturierte Abschlussfelder. Eine getrennte lokale
Migrationskopie ergänzt die Belege zu CI-Pfadfiltern, Curation-Skill und
Package-Scaffold. Die Zusammenfassung folgt für OA-0002 und OA-0011
dem bereits vorhandenen Status der Detailblöcke. Die Kopie enthält
33 IDs, besteht die strikte Validierung und wurde in ein temporäres Ziel
bytegleich zurückgesichert. Der Export bleibt als historischer Beleg
erhalten. Ein Zugriff auf einen neueren produktiv genutzten Master war
mit dem Export nicht verbunden.

[CI-Pfadfilter PR #6](https://github.com/n05a-design/steps/pull/6)
· [Curation-Härtung PR #15](https://github.com/n05a-design/steps/pull/15)
· [Package-Scaffold PR #4](https://github.com/n05a-design/steps/pull/4)
