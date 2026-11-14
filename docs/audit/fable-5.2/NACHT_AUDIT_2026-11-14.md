# STEPS · Nacht-Audit nach PR #54

## Ergebnis und Freigabegrenze

Verifizierte Basis: `5d2d09cfba22fa137ef65da5ffcc31bcadf5194a`,
Merge von PR #54. Neuer Branch: `codex/audit-nacht-20261114`.
Der ursprüngliche Arbeitsbaum war sauber. Der Git-Remote `origin` dieses
Checkouts zeigt auf den älteren lokalen OneDrive-Klon; deshalb wurde
GitHub-main direkt per HTTPS geholt und dessen SHA zusätzlich über die
GitHub-Verbindung verifiziert. Der ältere Klon wurde nicht verändert.

Das Arbeitspaket erweitert die Prüfung aller 97 Originalkanten, untersucht
die sechs Definitionslücken mit gesonderten Vorschlägen, konsolidiert alle
27 offenen Benchmarkfälle und 66 Forschungsclaims, ergänzt berechenbare
Golden-Beispiele und prüft den lokalen MIDI-/PDF-Bestand. Zwei echte
Secret-Scanner-Fehler sind behoben. Der breitere Scan entdeckt dabei sechs
zusätzliche historische Funde und bleibt **FAIL**. Es wird kein insgesamt
grünes Audit oder uneingeschränkt mergefähiger Stand behauptet.

**OPERATIV ABGESCHLOSSEN:** die hier protokollierten Inventuren,
Korrekturen, Modellgegenproben und technische Bestandstests.
**TECHNISCH BESTANDEN:** die jeweils unten genannten Teilprüfungen.
**FACHLICH / RECHTLICH OFFEN:** menschliche Abnahmen, Quellen-/Korpusbelege,
CSS-/Drittinhaltsrechte und die Behandlung historischer Schlüsselfunde.
**NICHT ABGESCHLOSSEN:** das Gesamtaudit einschließlich Sicherheitsbereinigung,
vollständiger fachlicher Einzelabnahme, der verbleibenden
Spezifikations-/Architekturfragen und einer vollständigen Konsolidierung
aller lokalen Bestände. Eine nur teilweise untersuchte Quelle wird nicht
als ausgeschöpfter externer Blocker umetikettiert.

## Vorher und nachher

| Gegenstand | Basis nach PR #54 | Nachtstand |
| --- | ---: | ---: |
| Historische Originalkanten | 97 | 97, unverändert |
| Begrenzte gestützte Graphstichproben | 14 | 38 |
| Beanstandete Graphstichproben | 1 | 1, CDR-010 |
| Fachlich weiterhin offene Kanten | 82 | 58 |
| Vollständige menschliche Graphabnahmen | 0 | 0 |
| Fehlende historische Definitionen | 6 | 6; sechs zusätzliche Vorschläge getrennt |
| Kanten mit technischer Gegenprobe | keine gemeinsame Matrix | 45; 52 ohne ausführbare Probe |
| Neue Modellproben | — | 23 erfolgreich |
| Knowledge-Benchmark | 69 PASS / 0 FAIL / 27 PENDING | 92 PASS / 0 FAIL / 27 PENDING |
| Zusätzliche Golden-Berechnungen | — | 14; ursprüngliche Klassen unverändert |
| MIDI-Dateien vollständig technisch gegengeprüft | historischer Auftrag offen | 112 von 112 |
| PDF-Metadaten/Hash-Bestand | früherer Bestand | 60 erfasst, 58 lesbar, 2 beschädigt |
| Secret-Bestandsscan | nur erste Muster pro Zeile, breiter Verzeichnisausschluss | 48 quarantänisierte historische und 4 erlaubte synthetische plus 6 zusätzlich erkannte Vorkommen; FAIL |

Eine Stichprobe zählt einen eng begrenzten Modellnachweis und keine
vollständige Bestätigung des Relationstyps. Die Spalte „Fachlich“ der
bestehenden Coverage-Matrix bleibt deshalb immer mit „Stichprobe“ zu lesen.
Die neue Graphmatrix trennt diese Grenzen ausdrücklich.

## Sechs Definitionslücken

[NODE_DEFINITION_PROPOSALS.json](../../../knowledge/relations/NODE_DEFINITION_PROPOSALS.json)
enthält für alle sechs historischen IDs einen getrennten Vorschlag,
Originalfundstelle, Quellenumfang, Probe und Restblocker. Alle bleiben
`REVIEW_REQUIRED`, ohne Produktionsfreigabe. Der Validator verhindert,
dass Vorschläge die historischen Definitionen schließen oder eine
Produktfreigabe erhalten.

| Historische ID | Untersuchung, Vorschlag und Grenze |
| --- | --- |
| MODAL_SHIFT_TO_II7 | Original beschreibt II7→ii7, Name dagegen TO_II7. Der Vorschlag SAME_ROOT_MAJOR_TO_MINOR_SEVENTH bezeichnet D7→Dm7: gemeinsame Tonklassen 0/2/9, Fis→F. Rechnerisch geprüft; historische Richtung bleibt fachlich zu entscheiden. |
| PIANO_MONTUNO_GUAJEO | Original nennt keine vollständigen Notenereignisse. Ein ausdrücklich **neu geschriebenes** Cm–Fm–G7–Fm-Beispiel enthält 16 Tonereignisse mit Onsets/Dauern, 480 PPQ und 2:3-Clave-Overlay. Gemeinsames Raster ist kein Stil-/Clave-Passungsbeweis und keine historische Transkription. |
| BOSSA_BATIDA | Als Vorschlag eine Familie variierter Gitarrenbegleitungen; kein einzelnes Cross-Stick- oder Klavierpendelpattern. Inayatullahs Artikel beschreibt Variationen und die Zweischichtigkeit. Historische Aufnahme und Umfang der STEPS-ID fehlen. |
| BRAZILIAN_TAMBORIM_SURDO_SYNTHESIS | Der gelesene Inayatullah-Artikel überliefert die Baden-Powell-Deutung über Reily/Cabral. Das ist eine konkrete Quellenkette, aber kein hier gelesenes zeitgenössisches Entstehungsinterview. Vorschlag als zugeschriebene Analogie, nicht gesicherte alleinige Herkunft. |
| SURDO_PULSE | Vorschlag trennt primeira/marcação von segunda/resposta in benannter Samba-Besetzung. UFRJ-Direktabruf gesperrt; Grinnell-Direktabruf 403. Frühere Claim-Fundstelle und indexierter Rollenbeleg bleiben begrenzt. |
| ACCENT_ON_BEAT_2_IN_2_4 | Vorschlag beschränkt Akzent 2 auf die benannte marcação-Rolle; resposta auf 1 bleibt als Gegenkontext. Das STEPS-4/4-Bossa-Modell beweist keine universelle 2/4-Aufführungsnorm. |

Die [Variations-/Quellenkettenpassage bei Inayatullah (2016)](https://www.scielo.br/j/cint/a/3TTy5RCKtKQDJLghWzb833b/?lang=en)
wurde gelesen. Das Forschungs-PDF von Victor Rocha Pólo zu Lula Galvão
war textlich teilweise erreichbar, enthält aber Extraktionsfehler;
die zusätzliche grafische Abfrage scheiterte am Timeout. Daraus wurde
keine genaue Notentranskription übernommen. Vurkaçs Originalauszug bestätigt,
dass die Akkorde aus der Rhythmusfigur entfernt sind; der Direktzugriff
blieb geschützt. Keine dieser Grenzen wurde durch erfundene Noten ersetzt.

## Alle 97 Originalkanten

- [Vollständige maschinenlesbare Kantenmatrix](../../../knowledge/relations/GRAPH_AUDIT_MATRIX.csv)
- [Individuelle Prüfnotizen, Originalfingerabdrücke und Proben](../../../knowledge/relations/GRAPH_AUDIT_PLAN.json)

Jede Zeile nennt ursprüngliche Endpunkte und Richtung, Definitionsstatus,
Namensraum/Locator, Quellenstand, technische Probe, Relationsbefund,
ausstehende menschliche Abnahme und nächste Maßnahme. Kandidaten-Claim-IDs
sind Zuordnungshinweise, keine behauptete Bestätigung der ganzen Kante.
Die ursprüngliche Relationszeile ist mit einem SHA-256 gebunden.

Zusätzliche Befunde betreffen unter anderem zu starke REQUIRES-Typen,
fehlenden Kontext bei Funktion/Stufe und Enharmonik, die falsche
IS_VARIANT_OF-Kategorie Oktave/Stimmung, unbewiesene Genre-Häufigkeiten,
ROOTLESS gegenüber einer ganzen Zweihandlage, ERR-026 in unterschiedlichen
historischen Fassungen und die uneinheitlichen Hauptdomänen. Diese
Semantikfragen wurden dokumentiert und nicht durch Eingriffe in die
Originalkanten beseitigt.

CDR-010 bleibt in beiden Matrizen FAIL. Der bereits vorhandene
C6/9(#11)-Korrekturvorschlag bleibt unverändert und ohne Produktionsfreigabe.

## Claims, PDF-Quellen und Golden-Bestand

[Alle 66 Claims](../../../knowledge/sources/CLAIM_AUDIT_MATRIX.csv) haben
einen Einzelbefund und eine Aussagegrenze. 21 reservierte Platzhalter
enthalten keine substantielle Aussage und werden nicht als geprüftes
Wissen verwendet. Eine menschliche Quellenfreigabe wurde nicht eingetragen.

Konkrete Korrekturen stehen im
[Quellenkorrekturprotokoll](NACHT_QUELLENKORREKTUREN_2026-11-14.json):

- CLAIM-001 und CLAIM-010: lokale Müller-Ausgabe (ISBN 978-3-319-21945-5),
  Druckseite 22 / PDF-Seite 48, Gleichungen 1.1 bzw. 1.4. Text und
  gerenderte Seite gegengeprüft; alte Locator dokumentiert, keine Quelle
  neu veröffentlicht.
- CLAIM-016: Das Originalchart hat eine PDF-Seite; Locator berichtigt.
- CLAIM-042: Keine zwingende linke Hand und kein allgemeines Verbot einer
  Drop-Operation bei anderer Stimmenzahl behauptet. Das konkrete
  Vierstimmenbeispiel bleibt erhalten; Levine-Seite weiterhin ungeprüft.
- CLAIM-007: Druckseite 12 der vorhandenen Hindemith-Ausgabe behandelt
  Sextakkorde, nicht die behauptete akustische Rangfolge. Locatorwiderspruch
  dokumentiert; damit ist nicht jede denkbare Rangfolgenaussage widerlegt.
- CLAIM-033: Die Zuschreibung Linn1988/MPC3000 bleibt bibliografisch offen;
  [Linns eigene Produktgeschichte](https://www.rogerlinndesign.com/about/about-museum)
  nennt das MPC3000 für 1994. Die 146-Tick-Modellrechnung ist davon getrennt.

[60 PDF-Dateien](NACHT_PDF_INVENTAR_2026-11-14.json) sind mit Bytes,
SHA-256, Seitenzahl/Fehler und Metadaten erfasst. Beide beschädigten
MakingMusic.pdf-Dateien wurden erhalten. Eine andere vorhandene Datei,
MakingMusic_DennisDeSantis.pdf, ist lesbar (293 Seiten); sie wurde nicht
stillschweigend als identischer Ersatz behandelt. Docling ist nicht
installiert. pypdf und pdftoppm wurden genutzt. Bei pypdf traten
Font-Encoding-Warnungen auf; relevante Formeln wurden deshalb visuell
gegengeprüft. Das Inventar ist keine Volltextprüfung aller 60 PDFs.

[Alle 198 Golden-Fälle](NACHT_GOLDEN_2026-11-14.csv) sind inventarisiert.
120 behalten ihre vorhandene ausführbare Klasse, 78 ihre historische
Spezifikationsklasse. Für 14 der letzteren existieren nun zusätzliche
Berechnungen aus den Eingaben, mit Sollwert- und Eingabemutationen.
Damit bleiben 64 Beispiele ohne diesen zusätzlichen ausführbaren Nachweis.
Die A/B-Beispiele behalten die theoretische Quinte; das reduzierte
Runtime-ROOTLESS-Layout darf nicht irrtümlich damit gleichgesetzt werden.
Kein Ergebnis erteilt eine historische Levine- oder Spielabnahme.

## MIDI und verbliebene Pflichtfälle

[112 SMFs](NACHT_MIDI_INVENTAR_2026-11-14.json) bestehen die eigene
Chunk-/Headerprüfung und den unabhängigen Decoder Mido 1.3.3 mit
deaktiviertem Clipping. Geprüft sind Typ, Trackzahl, Division,
Chunklängen, Ereignisdekodierung, Deltazeiten, End-of-Track und Tempo.
Das belegt keine Lizenz, Klangqualität, Aufführbarkeit oder vollständige
Zuordnung zu den vier PPR-README-Lieferungen. Mido wurde nur in der lokalen
Auditumgebung installiert, keine neue Produktabhängigkeit eingeführt.

[Die 27 PENDING-Fälle](NACHT_PENDING_2026-11-14.csv) bleiben einzeln offen:
12 Coach-, drei Hör-/Spiel-, ein bibliografischer, ein Graph-, sechs
CSS-Rechte-/Archiv- und vier MIDI-Liefernachweise. Die Graph-Rubrik wurde
von der veralteten 49er-Zahl auf den aktuellen Definitionsstand berichtigt.
Die CSS-Rubrik verlangt jetzt ausdrücklich Bundle-Rechte und dauerhafte
Archivautorität, damit reine Hashprüfungen sie nicht schließen können.

## Ursprüngliche Fable-Befunde und lokaler Aufgabenmaster

[Alle 33 Fable-Befunde](NACHT_FABLE_ABGLEICH_2026-11-14.csv) sind mit
Originalfundstelle, Paket und heutigen technischen Referenzen erfasst.
Diese Zuordnung ist kein pauschaler Nachweis, jede historische Probe
erneut isoliert reproduziert zu haben. Quellen-, Spiel-, Architektur-
und Publikationsgrenzen bleiben sichtbar.

Der echte lokale Aufgabenmaster enthielt 33 Aufgaben und 15 formale
Pflichtnachweisfehler. Vor Änderung wurde eine bytegleiche Sicherung
außerhalb des Repositories angelegt. OA-0002/0011/0013/0031 sind wegen
fehlender Verifikationsfelder auf DONE_UNVERIFIED zurückgestuft; ihre
früheren Behauptungen bleiben in der Sicherung. OA-0034 erfasst diesen
Nachtauftrag. Der Validator meldet danach 34 eindeutige Aufgaben und
null Strukturfehler. Kein fachlicher Abschluss wurde unterschrieben.

## Re-Audit und reproduzierbare Prüfungen

Die Schlussprüfung beruht nicht allein auf den neu geschriebenen Tests:

1. Der unabhängige MIDI-Decoder prüft alle 112 bestehenden Dateien.
2. Eine direkte Gegenrechnung aller 28×12 Progressionstranspositionen
   bestätigt Tonmengen, Qualität und Bassfunktion in 336 Kombinationen.
3. Gerenderte PDF-Seiten decken einen Locatorwiderspruch auf und bestätigen
   zwei konkrete Formelanker; maschinelle Extraktion wurde nicht allein
   für Notengrafiken verwendet.
4. Die vollständigere Sicherheitsprüfung entdeckt sechs zusätzliche
   historische Funde, statt die bisherige grüne CI-Bewertung zu übernehmen.
5. Original-Git-Bytes, Ontologiehashes, Golden-Spiegel, API und bestehende
   Publikationsvalidatoren werden erneut geprüft; Gegenbeispiele bleiben rot.

```sh
python -B scripts/audit_graph.py --check --json-out graph-audit.json
python -B scripts/verify_historical_ontology.py
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/audit_knowledge_coverage.py --check --details coverage.csv
python -B scripts/verify_reference_integrity.py
python -B scripts/build_unified_golden_cases.py --check
python -B scripts/render_api_reference.py --check
python -B scripts/render_reviewed_progressions.py --check
python -B scripts/pre-commit-secret-check.py --scan-all
python -B scripts/audit_midi_files.py --json-out midi-audit.json
python -B scripts/audit_golden_supplements.py --csv-out golden-supplements.csv
```

Der vollständige Benchmark erwartet Exit 1 wegen offener Pflichtfälle.
Der Secret-Scan liefert ebenfalls Exit 1, aber aus einem **anderen Grund**:
sechs konkrete Sicherheitsfunde. Diese Exitcodes werden nicht als
uneingeschränkt bestandene Gesamtprüfung ausgegeben.

Abschließender lokaler Lauf: **195 Kerntests und 36 Skilltests erfolgreich**.
Die neuen und bestehenden Validatoren für Graphmatrix, Ontologie,
Referenzidentitäten, Golden-Spiegel, API und Pilot-Lernmaterial bestehen.
756 interne Dateilinks in 134 aktiven README/betroffenen Markdown-Dateien
haben keine fehlenden Zielpfade. Anker, externe Erreichbarkeit und die
vollständige historische Archivnavigation sind davon ausgenommen.
Ein direkter Git-Bytevergleich bestätigt unveränderte 97 Kanten,
unveränderten CDR-010-Korrekturvorschlag und unveränderten Golden-Master.
Die gestagten neuen Änderungen enthalten keine neu erkannten Secretmuster;
der vollständige Bestandsscan bleibt aus dem dokumentierten Grund rot.

Die beiden aktiven GitHub-Rulesets wurden gelesen: main verlangt eine
menschliche Freigabe einschließlich Codeowner-Review und den geschützten
Pilot-Evidenzcheck. Keine Bypass-Akteure sind eingetragen. Der Secret-Scan
und die übrigen Python-Checks sind darin **nicht** als erforderliche
Statuschecks verzeichnet. Eine Änderung der Rulesets wurde nicht
vorgenommen; das ist eine zusätzliche Owner-Maßnahme vor einer
uneingeschränkten Merge-Empfehlung.

## Git-Übergabe und nächste Arbeit

Änderungen werden in größeren Arbeitsblöcken mit Signed-off-by committed und
als Draft-PR bereitgestellt. Kein Merge nach main, keine Baseline-Ausweitung,
kein History-Rewrite und keine Änderung der historischen Originalkanten.
Die ältere OneDrive-Arbeitskopie und die Originaldateien unter AppData
bleiben unverändert; nur der gesicherte kanonische Aufgabenmaster wurde
nachweistreu korrigiert.

[Priorisierte Restblocker und ausführbare nächste Schritte](NACHT_RESTBLOCKER_2026-11-14.md)
unterscheiden externe Entscheidungen von noch nicht vollständig geprüften
Spezifikationen und lokalen Beständen. Dieser Bericht ist ausdrücklich
keine Erklärung eines vollständig bestandenen Gesamtaudits.
