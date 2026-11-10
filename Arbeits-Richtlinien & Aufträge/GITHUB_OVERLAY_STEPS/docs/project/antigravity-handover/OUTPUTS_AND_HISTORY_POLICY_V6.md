# Vergangenheit, allgemeine KI-Ausgaben und Ableitungen dauerhaft erhalten

## Was als Ergebnis gilt

Die Dokumentationspflicht gilt ausdrücklich auch für **frühere** KI-Ausgaben: Promptentwürfe, Chat-Zusammenfassungen, technische Fragen/Antworten, Repositoryprüfungen, Architekturvarianten, Konkurrentenrecherche, Fachanalysen, Warnungen, fehlgeschlagene Tests, Release-/Paketdiagnosen, Screenshots, Tabellen, ausführbare Skripte und nicht weiterverfolgte Hypothesen. Eine Ausgabe muss nicht zu geändertem Code geführt haben, um dokumentationswürdig zu sein. Pro Ergebnis werden Substanz, Evidenz, Gültigkeitszeitraum, Unsicherheit, Herkunft und Verweis auf das vollständige Original bewahrt.

## Keine fiktive Vollständigkeit

Die historische KI-Historie ist nicht automatisch vollständig aus Dateien rekonstruierbar. Agenten sollen alle auffindbaren Dokumente und bereits indizierten Quellen katalogisieren; Unbekanntes bleibt `NOT_AVAILABLE`. Keine 100-%-Bestätigung, solange nicht jedes relevante Artefakt in einem nachvollziehbaren Coverage-Register steht. Ein vorhandener Git-Tree, ein Dokument oder ein Bericht ist noch kein Nachweis vollständiger semantischer Lektüre.

## Historien- und Fortschreibungsgraph

`source_id` → `artifact_id` → `claim_id` → `decision_id` → `requirement_id` → `code_ref` → `test_run_id` → `release_id`; jede Kante optional mit bewusstem `unknown` statt fingiertem Nachweis. `supersedes`/`derived_from` verbinden neuere Fassungen; unterschiedliche Aussagen nebeneinander datiert halten. Exact-byte-Duplikate dürfen als separate Pfade im Inventar bleiben, erhalten aber `duplicate_of`.

## Live-Ausgaben vs. GitHub

Während Read-only-Audit: neue Ausgaben in externer lokaler Sitzungsspur. Nach Dokumentationsfreigabe: nachprüfbare Markdown-/CSV-/JSON-Resultate im STEPS-Repo unter `docs/audit/YYYY-MM-DD/` und ein Register-Update auf separatem Branch. Größere fremde Originale/Assets bleiben in zulässigen lokalen Archiven; in Git nur Hash, Lizenz, Fundstelle, Ableitungsbeziehung, erlaubte Auszüge und Rechteklassifikation. GitHub-Commit-/PR-Aktion nur auf ausdrücklichen Auftrag.

## Abgrenzung

Verboten ist ein blindes Volltext-Transkript sämtlicher Chats oder ein verlustbehaftetes Überschreiben alter Originale. Fachlich sinnvolle Ergebnis-Protokolle sind Pflicht; nicht autorisierte Geheimnisse und fremde Rohinhalte dürfen nicht versehentlich öffentlich werden. Archivumfang und Aufbewahrung werden als eigene Ownerentscheidung mit Datenschutz- und Speicherbudget begrenzt.
