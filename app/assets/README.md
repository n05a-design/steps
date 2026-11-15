# App-Ressourcen

Laufzeitdateien der Desktop-Schicht.

| Ordner | Inhalt |
| --- | --- |
| `brand` | Logo (`steps-logo-*.png`), App-Symbol (`steps-app-icon-*.png`) und Windows-Symbol (`steps.ico`). |

Die Dateien in `brand` erzeugt [`scripts/build_brand_assets.py`](../../scripts/build_brand_assets.py) aus den [Logo-Mastern](../../design/brand/README.md). Sie werden nicht von Hand geändert. Der Code liest sie über [`app.brand`](../brand.py).

[Zur Bereichsübersicht](../README.md)
