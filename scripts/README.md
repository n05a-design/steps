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
