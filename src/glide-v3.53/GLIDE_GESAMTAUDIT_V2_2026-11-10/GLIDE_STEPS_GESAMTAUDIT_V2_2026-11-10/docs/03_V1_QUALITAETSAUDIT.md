# 03 — Qualitätsrevision des ursprünglichen 48-Dateien-Pakets

## Tatsächlich durchgeführte Dateiprüfung

**Artefakt:** `history/V1_originalpaket_unveraendert.zip`. Die Originaldatei wurde vor dieser Prüfung weder verändert noch repariert. Mit `zipfile.testzip()` geprüft (kein defekter ZIP-Eintrag), `MANIFEST.json` verifiziert: 47 aufgelistete Nutzdateien, alle vorhanden und SHA-256 korrekt; zusammen mit Manifest 48 Dateien. Ein relativer Markdownlink-Check der im Paket enthaltenen Markdown-Dateien meldete **keinen** fehlenden relativen Zielpfad. Das sind reale *technische* Teilchecks und keinesfalls ein Endorsement der inhaltlichen Analyse.

| Kennzahl | Ergebnis | Revisionsbedeutung |
|---|---:|---|
| Dateien insgesamt | 48 | Durch ZIP/Manifest nachgewiesen |
| Markdown-Dateien | 36 | Zwei große beigefügte Forschungsoriginale sorgen für einen Großteil der Textmenge |
| CSV-Dateien | 10 | Aus dem historischen XLSX exportiert; keine Aktualisierung auf V1.15 |
| Original-XLSX | 1 | Historischer Stand vom 07.11.2026, nicht aktuelles Glide-Inventar |
| Agentenaufträge | 17 | Etwa 390–420 Wörter je Hauptprompt, jeweils 44 Zeilen |
| V1-Gesamtübersicht | 78 Zeilen / ca. 911 Wörter | Unzureichend für produkt- und architekturübergreifende Tiefenanalyse |
| V1-Quellenindex | 37 Zeilen / ca. 648 Wörter | Überblick, kein vollständiges Evidence-Mapping |
| V1-Roadmap | 27 Zeilen / ca. 400 Wörter | Gates mit Schwerpunktfolge, wenige echte Abhängigkeits-/Entscheidungstests |
| V1-Knowledge-/Skill-Strategie | 23 Zeilen / ca. 314 Wörter | Kein Source-Level-Provenienz-, Lizenz- oder Evaluationsplan |
| 17 Prompts | Vier umfangreiche Abschnitte jeweils identisch in allen Prompts | Hohe Textdopplung; spezialisierter Prüfungsteil zu kurz |

## Analyse der inhaltlichen Schwachstellen

1. **Vorbereitung ≠ Entscheidung:** Die erste Overview war mehr ein Startleitfaden als die vertragliche Master-Overview mit verbindlichem Requirements-Trace. Fehlende Zuordnung: Nutzeranforderung → Quelle → UI/Code → Test → Status → Freigabe.
2. **Unzureichende Quellentiefe:** Der vollständige `app.pyw`-Callgraph, `ListApp`-Mutationspfade und tatsächliche UI-Bestandserhaltung wurden nicht eigenständig getestet. Es wurden zu viele Architekturannahmen aus dem Katalog statt aus ausführbarem Code abgeleitet.
3. **Unvollständige Ausgangszeitlinie:** Historische und aktuelle Stände sind zwar getrennt, aber nicht als systematischer *Provenienzgraph* mit Vorher-/Nachher-Quellstand, ZIP-Asset-/Dokumentationsrevision und Freigabekette geführt.
4. **Zu enges Zielbild:** Harmony-MVP und zwei interne Slots wurden faktisch zur einzigen Architektur-/Produktinterpretation. Drum-, MIDI- und Produktionsscope sowie echtes Zwei-Toplevel wurden nicht unabhängig bewertet.
5. **Unzulänglicher Framework-Lebenszyklus:** Versionierbarkeit, Modulschnittstellen, Codeownership, Schemaänderungen, Releasekanäle, Downstream-Pins und Backports wurden erwähnt, aber kaum gegen echte Migrationsfälle geprüft.
6. **Rechtsfolgen der bereits öffentlichen Bibliothek:** Vorherige Warnung richtig, aber nicht ausreichend dringlich angesichts 60 öffentlich im Git-Baum enthaltener PDFs.
7. **Knowledge-Reife und Schemas:** Source-Registry leer; JSON-Schema-Verträge können musikalische Zeit und Drum-Events noch nicht abbilden. Historischer Skill ist an vielen Stellen nur ein Startindex.
8. **Unscharfe Gate-Priorität:** Alle Plattformtests vor jedem experimentellen Schritt als Blocker zu fordern ist operativ unnötig strikt. Release und Experimente müssen separate Tore haben.
9. **Testnachweise nicht reproduziert:** Der Vergleich V1→V2 muss klar sagen: Wir haben keinen Code ausgeführt oder aktuelle CI selbst re-runnen können; historische Windows-Berichte sind Dokumente.
10. **Agenten-Prompt-Spezifik:** Ein Satz von 17 nahezu gleichen Aufträgen ohne präzise Input-/Output-Schemata, Risikoinjektion und Abnahmefälle führt zu schwacher Delegation. Wiederholte Hinweise sollten in **einen** verbindlichen Agentenvertrag ausgelagert werden.
11. **Privacy und Publikationsfähigkeit:** V1-ZIP enthält private Konto-/Arbeitszeit-Kontexte; für ein öffentliches Repository ist vor jedem Upload redaktionelle Aufbereitung nötig. Das wurde zwar in `APPLY_TO_STEPS.md` warnend behandelt, nicht jedoch per automatisierter Vertraulichkeitsklasse je Dateigruppe geprüft.
12. **Deduplikation mit Informationsverlust-Risiko:** Die V1-Overview verweist nur auf ältere konsolidierte Quellen; das ist sinnvoll als kanonische Referenz, kann aber die behauptete Erfassung „aller Informationen“ nicht beweisen. Originale müssen per Path/Blob/Abschnitt verfolgbar bleiben.

## Was V1 richtig machte und erhalten bleibt

- Nichtdestruktive Arbeit und keine ungefragten Git-Mutationen.
- Ein aktuelleres Glide-Systemregister 1.15 wurde der alten Arbeitsmappe vorgezogen.
- Kein unautorisierter Steps-Code aus fremden Quellen kopiert.
- Keine MIDI-/Audio-/UI-Funktionalität als bereits implementiert ausgegeben.
- Kenntlich gemachte offene 3.53-Freigabegates und sensible Nutzerkontentdaten.
- 48 Dateien mit korrekten SHA256-Prüfsummen und intaktem ZIP.

## Neue Prüflogik statt Verdichtung auf Scheingenauigkeit

- Jede Architekturannahme bekommt einen **Widerlegungsfall** (z. B. Import öffnet echten Datenordner; zwei Slots konkurrieren um Fokus; Undo mutiert alte Referenzen).
- Jede Kernanforderung bekommt eine **Akzeptanzmatrix**, nicht nur einen Absatz im README.
- Eine Baseline ist **nur für ihren ursprünglichen Quellstand** gültig; kein Legacy-Testresultat wandert auf Steps über.
- Neue Agenten-Prompts haben weniger gemeinsame Wiederholung, aber deutlich mehr aufgabenspezifische Analyse-/Prüfmethoden.

## Interne Schwellen dieser erneuten Revision

Technische Abgabe gilt nur als **nachprüfbares Dokumentenpaket**, wenn: V2-README auf alle kanonischen Docs/Prompts verweist; vollständiger SHA-Manifest-Check grün; relative Linkprüfung ohne tote Ziele; CSVs intern konsistent; V1-Original unverändert im Archiv; Status und Quellstände sichtbar; keine erfundenen App-/OS-Testgrüns; fachliche Unterschiede und offene Risiken nachvollziehbar. Damit wird noch keine produktionsfähige Software oder rechtlich freigegebene Forschungsbibliothek bestätigt.
