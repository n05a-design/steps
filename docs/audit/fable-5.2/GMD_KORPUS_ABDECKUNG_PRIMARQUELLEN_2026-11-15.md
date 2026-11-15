# Korpusabdeckung und CDR-019-Primärquellen nach PR #80

Stand: 15.11.2026. Dieses Paket setzt das STEPS-Audit nach dem externen Merge von PR #80 auf der aktuellen Basis `72234f1f1bbccd63c60e7ce910d6c05171d18276` fort.

## 1. GMD-Genreabdeckung aller 14 Korpusrelationen

Das neue Messmodul `scripts/audit_gmd_coverage.py` erfasst die expliziten Genre- und Subgenrelabels im Groove MIDI Dataset (GMDv1.0.0, 1.150 Metadatenzeilen, SHA-256 `3e17eef2...`) für alle 14 in `knowledge/relations/GRAPH_CORPUS_REVIEW.json` geführten Korpusfälle.

| Relation | Modus | Selektor | GMD 4/4 Beat Takes | Label-Geltungsbereich | Status |
| --- | --- | --- | ---: | --- | --- |
| CR-029 | primary | pop | 15 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| CR-030 | primary | house | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| CR-031 | primary | pop | 15 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| CR-032 | primary | house | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-001 | primary | pop | 15 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| REL-005 | exact | jazz/swing | 11 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| REL-006 | primary | funk | 53 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| REL-007 | primary | funk | 53 | EXPLICIT_LABEL_COMPONENT_ONLY | OPEN |
| REL-014 | primary | dnb | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-015 | primary | ukg | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-017 | exact | dnb/jumpup | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-026 | primary | dnb | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-032 | exact | afrocuban/chacha | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |
| REL-035 | exact | soul/neosoul | 0 | NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY | OPEN |

### Bounded Soul-Proxy für REL-035 (PAT-030 Neo-Soul Dilla Drag)
Da `soul/neosoul` in GMDv1.0.0 nicht als eigenständiges Subgenre vorkommt, wurden alle 28 GMD-Aufnahmen mit primärem Genre `soul` (4/4, beat; 598 vollständige Takte) als begrenzter explorativer Proxy analysiert:
- Kick 36 auf 1 und 3+: 62 Takte (±0.04) / 91 Takte (±0.1)
- Snare 38 auf Beat 3: 37 Takte (±0.04) / 71 Takte (±0.1)
- Snare 38 vorgeschlagener Drag-Anker auf 2+: 32 Takte (±0.04) / 84 Takte (±0.1)
- Gleichzeitige Kick/Snare-Kernkoinzidenz: 9 Takte (±0.04) / 20 Takte (±0.1)
- Gemeinsames Raster mit Drag-Anker: 0 Takte (±0.04) / 1 Takt (±0.1)

Grenzen: Ein Proxy ist kein Nachweis für Neo-Soul oder PAT-030. GMD enthält keine harmonischen Annotationen. REL-035 bleibt OPEN.

## 2. CDR-019 – Volltext-Abruf Walter Garcia 2013

Der zuvor nur unvollständig übertragene Aufsatz wurde legitim und vollständig über das Open-Access-Portal der Universidade de São Paulo (USP) abgerufen:
- **Werk:** Walter Garcia, *Radicalismos à brasileira*, Celeuma 1(1), 2013, S. 20–31, DOI: 10.11606/issn.2318-7875.v1i1p20-31
- **Fundort:** `https://revistas.usp.br/celeuma/pt_BR/article/view/68015/70585`
- **Umfang:** 286.707 Bytes (100% der deklarierten Verlagsgröße), 12 Seiten
- **SHA-256:** `400e09368af09df303e965894f7068ab9a134b0346d84f2864bf183862d8ae8a`
- **Inhaltliche Analyse:** Kulturkritischer Essay über die Ästhetik von João Gilberto („o trabalho de síntese e de estilização do samba“) und Kordialität im brasilianischen Modernismus im Dialog mit Antonio Candido. Zitiert sein Buch *Bim Bom* (1999) auf S. 12 in der Autorennotiz. Enthält keine Notentranskriptionen und keine Belege für die gesuchte Tamborim-/Surdo-Synthese-These. Ersetzt nicht die älteren Monographien.

## 3. CDR-019 – Zeitgenössische Primärquelle: Revista O Cruzeiro (13.04.1960, pim079)

Über das digitale Archiv des Instituto Antônio Carlos Jobim (IACJ) wurde die historische Primärquelle aus der Entstehungszeit der Bossa Nova ermittelt und vollständig gesichert:
- **Quelle:** Álvares da Silva (Text), Indalécio Wanderley (Fotos), *Música de Bossa Nova: Os Moços do samba estereofônico*, Revista O Cruzeiro, Rio de Janeiro, 13. April 1960
- **IACJ-Handle:** `https://www.jobim.org/jobim/handle/2010/8983` (Serie Publicação na Imprensa / Pim-079)
- **PDF-Umfang:** 1.693.721 Bytes, 8 Druckseiten, SHA-256 `8701544af8382d246973b94d21d5090c8774ee17995b443e1cf55c079f2f5d4b`
- **Visuell verifizierte Notenbeispiele:**
  1. Seite 1: *BATIDA BOSSA-CLÁSSICA / OU TELECOTECO* (José Henrique) – 2/4-Takt
  2. Seite 1: *BATIDA BOSSA-NOVA / COM SÍNCOPE / ANTES* (Normando Santos) – 2/4-Takt
  3. Seite 2: *BATIDA BOSSA-NOVA MISTA / ANTES & DEPOIS* (Bebeto do Sax) – 2/4-Takt
- **Zeitgenössischer Befund:**
  - João Gilbertos Genese in Juazeiro („estudando, meses, só êle e o violão... até que ouve um disco de Bonfá... 'Hôbalalá' e 'Bim-Bom' são composições originalíssimas“).
  - Zeitzeugen-Definitionen: Normando Santos betont „Essa diferença no samba é um aumento de síncope“; Bebeto do Sax formuliert „BN é aplicação nova de ritmo e melodia ao que já existia há muito tempo“.
  - Baden Powell wird im „colegiado paternal“ genannt; die spätere theoretische Zuschreibung einer Tamborim-auf-Surdo-Synthese taucht in diesem zeitgenössischen 1960er Bericht nicht auf.

## 4. Reily 1996 – Zugriffsstatus

Beim Aufruf von ResearchGate (`https://www.researchgate.net/publication/231840415_Tom_Jobim_and_the_Bossa_Nova_Era`) griff eine DataDome-Bot-Prüfung (`geo.captcha-delivery.com`). Gemäß Sicherheitsrichtlinie wurde keine Umgehung vorgenommen; der Host-Fakt BROWSER_HOST_FACTS bestätigt den Status.

## 5. Prüfbilanz

- Kerntests: 402 erfolgreich (alle 9 neuen Coverage- und Quellensicherheitstests PASS)
- Korpusskripte: `audit_gmd_coverage.py --check` und `audit_graph_corpus.py --check` PASS
- Graph: 97 Kanten, 41 SAMPLE_SUPPORTED, 1 FAIL (CDR-010), 55 OPEN; technische Proben 58 PASS
- Unabhängige menschliche Fach-, Hör-, Spiel-, Didaktik- und Coach-Abnahmen, CSS-Rechte sowie Sicherheitsfreigaben bleiben ausdrücklich **OFFEN**.
