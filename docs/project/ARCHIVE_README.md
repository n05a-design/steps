# Steps – konsolidierter Dokumentensatz (09.11.2026)

Die Ordnernamen unter „Inhalt“ stammen aus dem ursprünglichen ZIP-Paket.
Im Repository findest du die vorhandenen Bestandteile hier.

| Pfad im ZIP | Pfad im Repository |
| --- | --- |
| `01_Overview/` | [Projektübersicht](overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md) |
| `02_Technischer_Anhang/` | [Technischer Anhang](Technische%20Auswertung/Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md) |
| `03_Quellenabdeckung/` | [Quellenabdeckung](provenance/Steps_Quellenabdeckung_2026-11-09.csv) |
| `04_Originaldokumente/` | [Fünf Originaldokumente](Archiv/). Der im ZIP-Manifest genannte sechste Eingang ist als [offene Lücke](../../research/gaps/OPEN_GAPS.md) dokumentiert. |
| `SHA256SUMS.txt` | [Historische ZIP-Prüfsummen](provenance/HISTORIC_SHA256SUMS.txt) |

Weitere frühere Dokumentfassungen stehen im [Archivindex](../../archive/INDEX.md).

## Inhalt des ZIP-Pakets

- `01_Overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` – zentrale, deduplizierte Projekt-Overview (Produkt, Forschung, Glide-Transfer, Quelleninventare, Entscheidungen, 40 Konfliktpunkte, 34 Lücken, Roadmaps und Gate-Kriterien).
- `02_Technischer_Anhang/Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md` – sämtliche 39 unterschiedlichen Original-Codeblöcke aus den sechs hochgeladenen Markdown-Dateien, inklusive Originalzeilen.
- `03_Quellenabdeckung/Steps_Quellenabdeckung_2026-11-09.csv` – Zeilenabdeckung aller sechs Eingänge (2.612 Originalzeilen in 89 Abschnittszuordnungen).
- `04_Originaldokumente/` – sechs unveränderte Markdown-Originale als revisionssichere Rückfallbasis.
- `SHA256SUMS.txt` – SHA-256-Checksummen aller übrigen Archiv-Einträge zur Dateiintegrität.

Die Angaben in den Originalberichten wurden **nicht** gegen externe GitHub-Repositories, PDFs, CSV-Archive oder Live-Websites nachgeprüft. Die Overview stellt historische Behauptungen, belegte Quellenaussagen, Vorschläge und offene Nachweise getrennt dar.

## Prüfen

Alle im `SHA256SUMS.txt` gelisteten Pfade beziehen sich auf das ZIP-Wurzelverzeichnis. Zum Prüfen die ZIP-Datei extrahieren und im Ausgabeverzeichnis `sha256sum -c SHA256SUMS.txt` ausführen (Linux/macOS mit passenden Coreutils). Unter Windows `Get-FileHash` verwenden. Die externe Prüfsummendatei für ZIP und Einzeldokumente liegt neben der herunterladbaren ZIP-Datei.

**Wichtiger Hinweis:** Das Paket enthält die Originaldokumente zur vollständigen Nachvollziehbarkeit. Diese können historische, nicht abschließend überprüfte Aussagen sowie vereinfachte oder unsichere Beispielbefehle enthalten. Die bereinigte und bewertete Fassung ist die Overview.
