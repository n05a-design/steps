# knowledge/sources

Quellregister und urheberrechtlich geprüfte abgeleitete Arbeit; externe Originale nicht ungeprüft versionieren.

[`registry.yaml`](registry.yaml) ist das App-Quellenregister. Es verwendet die JSON-kompatible
YAML-Schreibweise, damit der Generator das Register mit der Standardbibliothek
lesen kann. Die Freigabe eines Quelleneintrags gilt für die genannte Nutzungsart. Die fachliche Freigabe einer musikalischen Aussage wird gesondert in der [Pilotfreigabe](../concepts/progressions/README.md) erfasst.

[`curated_sources_registry.yaml`](curated_sources_registry.yaml) enthält das Recherche-Inventar mit historischen Einträgen, nachgetragenen
Fachquellen und ursprünglichen Statusbezeichnungen. Die Claim-CSV bleibt
als Forschungsbestand erhalten. Die Zuordnung von CLAIM-001 und CLAIM-002 zu
SRC-018 folgt Autor und Werkjahr. Die konkreten Fundstellen bleiben als
`SOURCE_REVIEW_REQUIRED` gekennzeichnet. Die 21 Platzhalter CLAIM-046 bis CLAIM-066 behalten IDs, Domänen und
historische Quellenzuordnungen. Ihre Felder kennzeichnen die fehlende
Aussage, Fundstelle und Gegenprobe. Der Wortlaut des früheren Imports
steht im [ursprünglichen Registerstand](https://github.com/n05a-design/steps/blob/918d0a7/knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv).
Der Status `PLACEHOLDER` hält sie aus fachlichen Freigaben heraus.

Bei [CLAIM-034](MUSIC_SOURCE_CLAIM_REGISTER.csv) sind Publikationsangabe und
Aussage anhand des Verlagsabstracts korrigiert. `KB-M07-SWING-SOURCE` prüft
die Zitierangabe. Der Claim bleibt mit `REVIEW_REQUIRED` gekennzeichnet.
Konkrete Verhältnisse bei einzelnen BPM erfordern einen Nachweis aus den Messdaten.

## Bestand und Pflege

| Datei | Rolle |
| --- | --- |
| [App-Register](registry.yaml) | Quellen, die der Pilot-Loader auflöst. |
| [Recherche-Register](curated_sources_registry.yaml) | Bibliografie, historische Angaben und neu belegte Fundstellen. |
| [Claim-Register](MUSIC_SOURCE_CLAIM_REGISTER.csv) | Fachliche Aussagen, Gegenproben und Prüfstatus. |
| [Dateiinventur](MUSIC_SOURCE_REVIEW_PROGRESS.csv) | Historische Pfade, Hashes und Sichtungstiefe. |
| [Eigene Auswertungen](extracted/README.md) | Ablage und Anforderungen an eigene Synthesen. |
| [Rechterichtlinie](RIGHTS_POLICY.md) | Zulässige Nutzung und Weitergabe. |

Neue Einträge mit Quell-ID, konkreter Fundstelle, Nutzungsrahmen und
Prüfstatus pflegen. Eine erreichbare Quelle, ihre Rechte und die fachliche
Freigabe einer konkreten Aussage haben jeweils eigene Nachweise.
