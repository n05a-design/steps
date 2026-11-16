# Entscheidung zu CDR-021 / Surdo-Akzent auf der Zwei (16.11.2026)

**Status:** Entscheidung des Inhabers über den Geltungsbereich, gestützt auf neu gelesene Sekundärquellen. Keine Fach-, Spiel- oder Hörabnahme, keine Produktionsfreigabe. Die Kante CDR-021 (`SURDO_PULSE` → `ACCENT_ON_BEAT_2_IN_2_4`) bleibt `OPEN`.

## Frage

Die Kante behauptet eine Aufführungsnorm: Akzent auf Zählzeit 2 im 2/4-Takt. Bisher war nur die **Onset-Rolle** belegt: Der Surdo de primeira spielt auf der Zwei, der Surdo de segunda auf der Eins (Florianópolis-Feldstudie 2010, siehe [`NODE_DEFINITION_PROPOSALS.json`](../../../knowledge/relations/NODE_DEFINITION_PROPOSALS.json)). Offen waren der Ensemblekontext und ein Beleg dafür, dass die Zwei **betont** ist.

## Neu gelesene Quellen

Alle vier Dateien sind frei abrufbar und wurden am 16.11.2026 als PDF abgerufen und als Text gelesen. Die Dateien liegen nicht im Repository.

| Quelle | Fundstelle | Aussage (eigene Übersetzung) | Kontext | SHA-256 der gelesenen Datei |
| --- | --- | --- | --- | --- |
| Luiz Augusto Lima Guimarães: *Proposta pedagógica ao ensino dos instrumentos de percussão da roda de samba …*, Abschlussarbeit (Licenciatura em Música), UNIRIO 2018. [PDF](https://www.unirio.br/cla/ivl/cursos/luizguimaraes.pdf) | S. 30 | Der Surdo de primeira spielt auf der Zwei, „tempo do acento característico do samba“. Der Surdo de terceira verstärkt diesen Akzent. In der Roda de samba vereint ein einzelner Surdo die drei Rollen. | Bateria der Escola de samba; Roda de samba gesondert | `3645f882d0aeba050e60e7479a2ed5e14d06073f9b375ef6d9cc7f9d239b5e6a` |
| Hélio Cunha: *A marcha e a síncope: dois elementos contrastantes na estrutura do ritmo de samba*, XXIII. ANPPOM-Kongress, Natal 2013. [PDF](https://anppom.org.br/anais/anaiscongresso_anppom_2013/2316/public/2316-7068-1-PB.pdf) | S. 3, 6 | Der Surdo markiert die Zwei regelmäßig. Tiefe Instrumente betonen die Zwei, hohe die Eins; daraus entsteht ein struktureller Gegensatz. | Samba allgemein | `2f345bf383f07ad4b68b1e0e126327d5036d51abf9e531e9a72a7cc01ffa261c` |
| Bernardo de Souza Dantas Mendonça Pinto: *O violão no acompanhamento do samba*, Abschlussarbeit (Licenciatura), UNIRIO 2001. [PDF](https://www.unirio.br/cla/ivl/cursos/bernardopinto.pdf) | S. 38 | Die Marcação schlägt immer auf der Zwei und verlagert damit die schwere Zeit. Der Surdo de segunda spielt auf der Eins. | Escola de samba | `1a400b491a84c28af28478553076e41194d29484762b568749f34feaeeb1d3fd` |
| Caio Fiori Bertazzoli: *A batucada de samba em Córdoba, Argentina*, Masterarbeit (Etnomusicologia), UFPB 2023. [PDF](https://repositorio.ufpb.br/jspui/bitstream/123456789/29864/1/CaioFioriBertazzoli_Dissert.pdf) | S. 38–39, Fig. 9 | Gleiche Rollenteilung im Viertelzyklus: primeira auf 2 und 4, segunda auf 1 und 3, terceira verstärkt die primeira. | Samba-Batucada außerhalb Brasiliens | `bcf6b4acdce0bfac340b976ee462d98bbb97555d70450b646167be03009060c0` |

Die Seitenzahlen folgen der Zählung des PDF-Texts. Der Text von Pinto 2001 ist ein OCR-Scan mit Erkennungsfehlern; die zitierte Aussage ist trotzdem eindeutig lesbar.

## Entscheidung

- `ACCENT_ON_BEAT_2_IN_2_4` gilt nur für den **Surdo de primeira (marcação) in der Bateria einer Escola de samba, im 2/4-Takt**. Der Akzent auf der Zwei ist dort als charakteristisch beschrieben (Guimarães 2018, Pinto 2001) und wird von Cunha 2013 strukturell gestützt.
- Die Aussage gilt **nicht** als Akzentgebot für alle Surdos, nicht für den Surdo de segunda und nicht für andere Gattungen. Für Samba-Reggae ist eine Rollenumkehr berichtet; sie ist hier nicht geprüft.
- Der historische Knoten wird nicht umbenannt. Die Vorschläge `SAMBA_SURDO_ROLE_SCOPED` und `SAMBA_MARCACAO_BEAT2_SCOPED` bleiben `REVIEW_REQUIRED`.

## Grenzen und weiterhin offen

- Die Quellen sind zwei Abschlussarbeiten (Licenciatura), ein Kongressbeitrag und eine Masterarbeit. Sie beschreiben den Akzent, messen ihn aber nicht. Eine Messung der Dynamik oder eine Aufnahmeanalyse fehlt.
- Die Fach- und Spielabnahme durch eine Person mit Bateria-Praxis steht aus.
- Weiterführende Literatur, die die Quellen nennen und die hier nicht eingesehen ist: D'Anunciação 2008 (*Melódica percussiva*), Bolão 2009, Oliveira Pinto 1999.
