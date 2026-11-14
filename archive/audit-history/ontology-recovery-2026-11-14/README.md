# Wiedergefundene historische STEPS-Originale

Am 14.11.2026 unter `%LOCALAPPDATA%/StepsAudit/` wiedergefundene,
projekterzeugte Arbeitsstände. Die zwölf Dateien unter `originals/` sind
bytegleich kopiert; ihre Zeilenenden werden nicht normalisiert.
[Manifest](RECOVERY_MANIFEST.json) enthält Originalpfade, Bytezahlen und
SHA-256. Keine fremden Buchvolltexte oder Web-Assets wurden ergänzt.

**Historisches Archiv, kein fachlich freigegebener Wissensbestand.**
Selbstbezeichnungen wie `CANONICAL`, `NORMATIVE`, `PRODUCTION_READY`,
`FULLY_CONCILIATED` oder `FORMAL_VERIFIED` bleiben als historischer
Wortlaut erhalten. Sie gelten nicht als heutige Abnahme. Die Dokumente
enthalten unter anderem pauschale Genre-/Didaktikaussagen, alte
Swing-Rechenfehler und widersprüchliche Domäneneinteilungen.

| Originalgruppe | Inhalt und Grenze |
| --- | --- |
| `20261110T2330_Phase4_Master` | Ontologie mit 90 ausdrücklich nummerierten Unterkonzepten; davon 41 im heutigen historischen Graphen. Dazu Pop-/House-Atlas und Klavier-Lernpfad. |
| `20261111T0005_Phase4_6` | Historische Korrekturen. |
| `20261111T0025_Phase4_7` / `20261111T0040_Phase4_8` | Getrennte Klaviermodul-Fassungen; spätere Fassung präzisiert P10 und Bass-/Grundtonunterscheidung. Keine externe Lernwirksamkeitsabnahme. |
| `20261111T0040_Phase4_8` | Weitere historische Korrekturen einschließlich ERR-026. |
| `20261111T0105_Phase4_9` | Anders gegliederte Ontologie ohne die expliziten Mxx-xx-Definitionen des Masters; kein stillschweigender Ersatz. |
| `20261111T0130_Phase4_10` | Latin-Projekttext und P14. Keine eigenständige Originalquellen- oder Aufführungsabnahme. |
| `20261111T0800_Phase4_12` | Historischer Generator mit den CDR-Vorläufertripeln. Nur archiviert, nicht ausgeführt. |
| `20261111T1000_Phase4_14` | Bericht mit erneut abweichenden Hauptdomänen; seine Statusbehauptungen bleiben ungeprüft. |

Prüfung aus dem Repository-Root:

```sh
python -B scripts/verify_historical_ontology.py
```

Das prüft Bytes und Definitionsanker, nicht die Wahrheit der Aussagen.
[Fundauswertung und acht Restknoten](../../../docs/audit/fable-5.2/ONTOLOGIE_WIEDERFUND_2026-11-14.md)
und [historischer Definitionsindex](../../../knowledge/relations/HISTORICAL_NODE_EVIDENCE.csv)
trennen die Beweisgrenzen.

[Zur Archivübersicht](../README.md)
