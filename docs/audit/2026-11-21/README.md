# STEPS-Gesamtaudit vom 21. November 2026

**Fachliche Gesamtfreigabe ausstehend.** Die Prüfung fand bestätigte Abweichungen in der Akkord- und Voicing-Ausgabe, in Bibliotheksaussagen, im Wissensabruf und in der Kurationsprüfung. Die veröffentlichte Pilotfreigabe betrifft acht Aussagen zu drei Beispielen.

**Prüfstand:** GitHub-`main` `b47ffc27654d5e1df26316b466049f68000d81c6`, lokaler Commit `99dd53c4ca3376212edcb339b08bef3828d75333`, gemeinsamer Git-Baum `3fe6f904f4d4703b545ba4dd115228c6daf8723b`. Der lokale Arbeitsbaum war zum Prüfzeitpunkt sauber. Die [Prüfdaten](evidence.json) halten die Ergebnisse für genau diesen Stand fest.

## Ablage und Dokumentation

| Prüfbereich | Ergebnis |
| --- | --- |
| Git-Inventar | 3.078 Pfade auf beiden Seiten. 3.064 lokale Dateien bytegenau wie der Remote-Blob, 14 ausschließlich mit abweichenden LF-/CRLF-Zeilenenden. Kein Inhaltsunterschied und kein fehlender Pfad gegenüber dem geprüften Git-Baum. |
| Markdown | 1.607 Dokumente und 5.748 erkannte Links oder Bildziele. 2.190 Ziele im Git-Baum, 30 interne Fragmentlinks, 2.506 externe Ziele, 331 Pfade außerhalb des Git-Baums und 691 Vorkommen mit fehlendem relativem Ziel. HTML-Links, Heading-Anker und Erreichbarkeit aller externen Seiten waren außerhalb dieses Scans. |
| Fehlende relative Ziele | 690 Vorkommen in archivierten oder Forschungsunterlagen, eines in einem historischen [Audit unter `docs/`](../fable-5.2/PR22_QUELLENVOTUM_2026-11-13.md). Der dort als entfernt beschriebene PDF-Pfad lässt sich aus dem aktuellen Checkout nicht öffnen. Die 691 Treffer sind Linkvorkommen. Pro Treffer bleibt offen, ob das Ziel in seinem ursprünglichen Paket vorhanden war. |
| Dateisyntax | 2.120 Markdown-, Python-, JSON- und YAML-Dateien verarbeitet, ein Fehler in einer als `.py` abgelegten historischen PowerShell-Datei. Der Befund war [bereits dokumentiert](../../../research/gaps/OPEN_GAPS.md). Die drei Python-Auditgeneratoren mit Escape-Warnungen liegen außerhalb des Produktkerns. |
| Historisches Dateiregister | 1.895 Zeilen gegen *denselben Pfad und die Rohbytes* in `origin/main` verglichen. 1.557 Größen- und Hash-Treffer, 189 Abweichungen am selben Pfad, 149 Pfade außerhalb des Baums. Historische Versionen, entfernte lokale Quellen und bereits dokumentierte Migrationen erfordern eine Prüfung gegen ihren jeweiligen Referenzstand. |
| Aktive technische Dokumente | [ADR-017](../../../decisions/ADR-017-midi-export-v01.md) und der [Entscheidungsindex](../../../decisions/DECISION_REGISTER.md) führen die Umsetzung noch als offen. Die [Implementierungsübersicht](../../IMPLEMENTATION.md) nennt den eingerichteten und getesteten Sessionexport. |

Zusätzlich zählte Git 10.287 ignorierte lokale Dateien. Sie lagen außerhalb des Remote-Inventars. Der Audit hat private Ablagen, Browser-Downloads und externe Originaldateien außerhalb des Git-Baums nicht gehasht. Byteidentität, Herkunft und Nutzungsrechte haben eigene Nachweise.

## Produktlogik und musikalische Ausgaben

| Befund | Reproduzierbarer Nachweis |
| --- | --- |
| Slash-Bass in der Anfängeransicht | In allen 72 Testfällen wichen die Anfänger-Voicings vom ausgewiesenen Slash-Bass ab. Inspektor, Voice Leading Lab und MIDI-Ausgabe verwendeten den richtigen Bass in denselben 72 Fällen. |
| Akkordreduktion | Bei 24 `7b5`-Varianten fügte die Reduktion eine im Symbol unzulässige reine Quinte ein. Bei 48 Sextakkordvarianten bezeichnete sie die Sexte als entfernte Septime. |
| Drop-2 | 64 von 144 Septakkordbeispielen ergeben dieselben MIDI-Noten wie `CLOSE`. Bei 34 dieser 64 Fälle passt die korrekte Drop-2-Form durch gemeinsame Oktavverschiebung in den Tonumfang. Beispiel `Cmaj7`: Close und Drop-2 liefern beide `[48, 52, 55, 59]`. Die Absenkung der zweithöchsten Stimme ergibt `[43, 48, 52, 59]`, eine passende Oktavverschiebung `[55, 60, 64, 71]`. [Jazz Arranging, Abb. 22.21](https://www.ithaca.edu/sites/default/files/2021-03/2019-book-chapter-school-jazz-arranging.pdf) |
| Enge Lage und Zusatztöne | 152 von 720 `CLOSE`-Varianten spannten in der oberen Akkordspur mehr als eine Oktave. `Cadd2` und `Cadd9` ergaben beide `[48, 50, 52, 55]`. Open Music Theory beschreibt die Platzierung des D innerhalb des Dreiklangs für `add2` und oberhalb für `add9`. [Open Music Theory, Chord Symbols](https://viva.pressbooks.pub/openmusictheory/chapter/chord-symbols/) |
| Stilprofile | Bei allen 484 getesteten Progressionspaaren erzeugten Pop, Power und Quartal dieselben MIDI-Töne. Das strikte Profil wich in 155 Fällen ab. Sein Parallelentest fand in dieser Stichprobe keine entsprechenden Warnungen. |
| Erweiterte Schreibweisen | Drei von fünf geprüften Explorer-Eingaben mit zulässigen doppelten Vorzeichen führten beim Vorschlag zu einem Fehler. |
| Bibliotheksaussagen | Alle [79 Einträge in `voice_leading_features`](voice-leading-statements.csv) ausgewertet. 44 im angegebenen Umfang belegt, 22 kontextabhängig, sieben mit konkretem Gegenbeispiel, sechs mit fehlendem Quellenbeleg. Gegenbeispiele betreffen PROG-004, -012, -013, -015, -020, -021 und -026. Die übrigen Metadatenfelder wurden nicht jeweils vollständig fachlich bewertet. |

Positiv belegt sind 2.064 Akkordalias-Prüfungen, 96 von 96 Jazz-Fortsetzungen in erwarteter Schreibweise und 1.368 MIDI-Optionen, die keine fremden Tonklassen und keinen falsch gesetzten Exportbass für die Testeingabe enthielten. Das Auslesen erfolgte unabhängig mit Mido 1.3.3. Die Voicing- und Bezeichnungsfehler oben bleiben damit reproduzierbar.

## Skills und Wissensabruf

Der Audit umfasste die 25 versionierten Dateien unter `.agents/skills/steps-knowledge-curation/` mit Runbook, Dokumentation, Referenzen, Vorlagen, sieben Python-Helfern und vier Testsuiten. Zusätzlich betrachtet wurden der [Projekt-Workflow](../../../SKILL.md), der [Knowledge-Skill](../../../skills/steps-knowledge/SKILL.md) mit Index und Eval-Datei sowie der [historische Harmony Coach](../../../skills/music-harmony-coach/README.md) mit Arbeitsablauf, Referenzen und Schema.

| Prüfpunkt | Befund |
| --- | --- |
| Referenz-IDs und Identitätsschutz | Der Skill meldet 390 IDs und „100% … VERIFIED“. Eine Kopie von PROG-001 mit Stufen `I–I–I–I` und Akkorden `C–C–C–C` wird mit Exit 0 und ohne Warnung akzeptiert. Der strengere Repository-Prüfer meldet an derselben Kopie geänderte Harmonik und einen Hash-Konflikt. Der Skill akzeptiert außerdem doppelte PROG-001-Zeilen. |
| Fehlende Referenzdateien | Eine fehlende Baseline oder ein fehlender Golden-Testspiegel ergibt jeweils Exit 0. Die Warnung erscheint im JSON-Bericht. Die Standardausgabe zur fehlenden Baseline meldet weiterhin vollständige Integrität. |
| Aufgabenregister und Restore | Das echte kanonische Register enthält sieben eindeutige Aufgaben und besteht die Prüfung. In einer Testkopie wurde `OA-10000` mit Status `UNKNOWN` still übergangen. Der Validator meldete nur die gültige Aufgabe. Restore akzeptierte den fehlerhaften Block als Teil des Snapshots. Der Wiederherstellungsversuch lief in einem temporären Verzeichnis. |
| Quellenprüfung und Extraktion | Hash und Kandidat für identische Bytes reproduziert. Der Extraktor findet „must be tested“ und übersieht „must first be tested“. Das Runbook definiert die Ausgabe als Kandidatenliste für manuelle Prüfung. |
| Knowledge-Skill-Index | `doo-wop` zeigt auf PROG-001, dessen Akkorde `C–G–Am–F` sind. Die Doo-Wop-Folge `C–Am–F–G` steht unter PROG-004. `axis` im Index zeigt auf PROG-009, dessen Akkorde `C–F–Fm–C` sind. Der laufende Adapter liefert bei `axis` den passenden PROG-001. Bei `doo-wop` antwortet er `NO_EVIDENCE`; der Datensatz PROG-004 gehört zum Bestandskatalog. [Open Music Theory, Pop-Schemata](https://viva.pressbooks.pub/openmusictheory/chapter/intro-to-pop-schemas/) [Richards, Axis Progressions](https://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html) |
| Wissensabruf und Notation | `query("", convention="INT")` und eine reine Leerzeicheneingabe liefern `GROUNDED` für PROG-001. „dimension“ liefert Deutungen verminderter Septakkorde. Die Rückgaben zu `Bdim7` und `bVII` enthalten keine registrierten Belege, obwohl der Skill einen Beleg verlangt. `ii-V-I` mit `INT` enthält die deutsche Note H. `bVII` mit `DE` enthält das internationale Bb. |
| Freigabegrenze im Adapter | Der [Audit vom 18.11.](../../../research/gaps/GESAMTAUDIT_ABLAGE_RECHERCHE_SKILLS_WISSENSBASIS_2026-11-18.md) dokumentierte den direkten Ladeweg. Er ist im geprüften Code weiterhin vorhanden. `KnowledgeAdapter` setzt den geladenen Claim auf `verified=True` und die Quellenrechte auf `approved`. Der geprüfte App-Lernkatalog hat einen getrennten Freigabeweg mit Fingerprints und Belegen. |

Die zwölf Coach-Prüfungen decken M01–M12 ab und warten auf bewertete Antworten. Technische Tests der Rubrik ersetzen diese fachlichen Bewertungen nicht.

## Wissensdatenbank, Herkunft und Abnahme

- `--scope all` ergab **92 PASS, 0 FAIL, 27 PENDING**, Exit 1. Offen sind zwölf Coach-Fälle, drei Stichproben und zwölf Backlogfälle. `--scope pilot` bestand 8 von 8, `--scope publication` 3 von 3. Die acht GitHub-Freigabebelege wurden für den geprüften Commit erneut verifiziert.
- Der generierte Abdeckungsbericht verzeichnet 66 historische Forschungsclaims und 97 Graphrelationen. Für 21 Claims nennt er formale Befunde. Alle 97 Relationen bleiben im getrennten Forschungsregister `REVIEW_REQUIRED`. Der strukturelle Identitätstest zählt 198 Golden-Fälle. Der Lauf für die 64 verbliebenen historischen Golden-Fälle meldet 43 ausgeführte Modellprüfungen und 21 nicht ausgeführte Fälle sowie null menschliche Freigaben für diesen Lauf.
- Die Gegenprobe zum Cross-Domain-Recommender fand 28 `HIGH`-Einstufungen. 21 geprüfte Zuordnungen erreichten Modell-Confidence 1,0 bei offener fachlicher Prüfung. Der Explorer erzeugte aus den 28 Bestandsprogressionen 552 Kandidaten mit 17 Provenienzlabels. Drei davon sind als gleichlautende IDs im Produktquellenregister vorhanden. Ein Modelllabel allein belegt keine externe Fundstelle.
- Die [Quellen- und Rechteprüfung](../../governance/RIGHTS_SECURITY_AND_RELEASE.md) bleibt für offene Forschungsbestände datei- und ausgabenbezogen. Keine neue Freigabe für Rechte, historische Aussagen oder Veröffentlichungen wurde erteilt.

## Ausgeführte Prüfungen und Nachvollziehbarkeit

- Lokal bestanden 841 Produkttests mit erzwungenem Desktop-Tk und 40 Skill-Tests. 35 weitere Prüfungen bestanden, einschließlich Struktur, ID-Integrität, Lokalisierung, generierter Dokumentation, Referenzkontrolle, Pilotfreigaben und Korpus-Checks. Counts und Prüfbefehle stehen in [evidence.json](evidence.json).
- GitHub meldete vier erfolgreiche Läufe für den geprüften Commit. Die Python-Suite enthielt zwölf erfolgreiche Jobs, darunter UI-Smoke-Tests auf macOS, Windows und Linux. [Python- und Verifikationssuite](https://github.com/n05a-design/steps/actions/runs/44871205445) · [Pilotbelege](https://github.com/n05a-design/steps/actions/runs/44871205435) · [Struktur](https://github.com/n05a-design/steps/actions/runs/44871205398) · [Secret-Scan](https://github.com/n05a-design/steps/actions/runs/44871205420)
- Die [Skill-Gegenprobe](verify_skill.py) lässt sich aus dem Repository-Wurzelverzeichnis mit `python3 -B docs/audit/2026-11-21/verify_skill.py` wiederholen. Sie ändert ausschließlich temporäre Kopien. Für den Ablageabgleich wurden Git-Blob-IDs, SHA-256, ein CommonMark-Parser und statische Syntax-Parser verwendet.
- Die App wurde über die vorhandenen automatisierten Workflows geprüft. Manuelle plattformübergreifende Bedienabnahme, vollständige Prüfung archivierter Quellen am Original und endgültige musikalische Fachabnahme stehen aus. Ableton und andere DAWs waren zurückgestellt.

**Abnahmereihenfolge:** Zuerst fehlerhafte Nutzer-Ausgaben und irreführende Wissensrückgaben korrigieren. Danach die strengere Identitätsprüfung in den Kurationsablauf einbinden, Skill-Index und Register synchronisieren und die fachlichen Pflichtfälle mit belastbaren Quellen und menschlichen Bewertungen schließen.
