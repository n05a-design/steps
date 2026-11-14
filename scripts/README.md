# Prüf- und Pflegebefehle

Die regulären Befehle werden aus dem Repository-Root mit Python aufgerufen. Die Tabelle nennt, welche Dateien dabei geprüft oder erzeugt werden.

| Einstieg | Inhalt |
| --- | --- |
| [verify_reference_integrity.py](verify_reference_integrity.py) | Referenz-IDs und kontrollierte Korrekturen abgleichen. |
| [verify_registered_git_files.py](verify_registered_git_files.py) | Registerpfade, Bytezahlen und SHA-256 gegen einen ausdrücklich gewählten Git-Baum prüfen; keine Herkunfts- oder Rechtefreigabe. |
| [verify_css_provenance.py](verify_css_provenance.py) | Gespeicherte Bandcamp-Player als CSS-Herkunftskette prüfen; mit `--online` Live-CDN-Bytes vergleichen. Keine Freigabe des CSS-Bundles. |
| [run_knowledge_benchmark.py](run_knowledge_benchmark.py) | Wissensfälle prüfen, Berichte und Abnahmevorlagen erzeugen. |
| [audit_knowledge_coverage.py](audit_knowledge_coverage.py) | Wissensinventur prüfen oder mit `--write` aktualisieren. |
| [graph_corrections.py](graph_corrections.py) | Historisch gebundene Korrekturvorschläge auf Identität, Tonklassenschema und ausdrücklich ausstehende Freigabe prüfen; wird von Benchmark und Inventur verwendet. |
| [verify_historical_ontology.py](verify_historical_ontology.py) | Wiedergefundene Originalbytes, 41 historische Definitionsanker und Reviewgrenzen prüfen; keine Fachabnahme. |
| [audit_graph.py](audit_graph.py) | Alle 97 Originalkanten samt Namensraum, Prüfstatus, Blocker und getrennten Vorschlägen inventarisieren; `--check` sichert die Matrix. |
| [graph_probes.py](graph_probes.py) | Begrenzte musikalische Modellrechnungen und neu geschriebene Ereignisübung; keine historischen Transkriptionen oder Fachfreigaben. |
| [audit_remaining.py](audit_remaining.py) | PENDING-Fälle und die 33 Fable-Befunde mit ihren Evidenzgrenzen konsolidieren. |
| [audit_midi_files.py](audit_midi_files.py) | Lesende SMF-Hüllenprüfung und unabhängiger Eventreader für den Forschungsbestand. Optionaler Auditreader: `python -m pip install mido==1.3.3`; keine Produktabhängigkeit. |
| [audit_golden_supplements.py](audit_golden_supplements.py) | 14 zusätzliche begrenzte Rechnungen neben den unveränderten historischen Golden-Klassen; sämtliche 198 Fälle inventarisiert. |
| [build_unified_golden_cases.py](build_unified_golden_cases.py) | Kanonischen Golden-Master mit Testspiegel synchronisieren oder prüfen. |
| [render_api_reference.py](render_api_reference.py) | API-Referenz erzeugen oder mit `--check` vergleichen. |
| [render_reviewed_progressions.py](render_reviewed_progressions.py) | Freigegebene Pilotdaten in Lernmaterial umsetzen. |
| [verify_pilot_review_evidence.py](verify_pilot_review_evidence.py) | Echte Freigabebelege per GitHub-API prüfen. |
| [Hörproben erzeugen](render_audit_listening_examples.py) | Eigene WAV-Signale ausgeben. |
| [Hörproben messen](analyze_audit_listening_examples.py) | Akzente, Melodie- und Begleittöne der WAV-Dateien messen. |
| [Git-Hooks](git-hooks/README.md) | Lokaler Secret-Check. |
| [Übergabewerkzeuge](handover/README.md) | Historische Berichte, Register und Paketgenerierung. |

Skripte zu historischen Audits, Baselines und Konsolidierungen gehören zu den datierten Nachweisen. Vor Änderungen oder erneutem Lauf Eingabepfade und Ausgabeziele prüfen. [Testanleitung](../tests/README.md)

[Zur Bereichsübersicht](../README.md)
