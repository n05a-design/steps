# Markenidentität

Logo und App-Symbol von STEPS. Die SVG-Master in diesem Ordner sind die einzige Quelle aller Logo-Darstellungen in App, README und GitHub. Wortmarke und Typografie sind noch nicht festgelegt.

## Master

| Datei | Verwendung | SHA-256 |
| --- | --- | --- |
| [Logo_Steps-01.svg](Logo_Steps-01.svg) | Logo innerhalb der Anwendung. Zeichen mit Schatten auf transparentem Grund. | `52d8dd13bf891e8fda193331b515410ef21c4c4158b13e2714b868b5401ff8a5` |
| [Logo_Steps-03.svg](Logo_Steps-03.svg) | App-Symbol und Favicon, auch für Paket und README. Zeichen auf dunklem Feld mit Rahmen. | `3ef4e5b10dda816add78bfc404a6fb9e95651136c5dea0522a192cacc039efa9` |
| [Logo_Steps-02.svg](Logo_Steps-02.svg) | Weitere Markenvariante ohne Rahmen. Daraus wird derzeit keine Datei abgeleitet. | `7c055db3ed30897bfa735b4679ddf8542758bc4a5d59af1ae75057496f8b8304` |

Die Master verwenden drei Farben: `#209f95`, `#4ee4cd` und `#15243c`.

**Herkunft:** Eigene Gestaltung des Projektinhabers. Die Dateien sind bytegleiche Kopien aus dem [Grafik-Master von Glide](https://github.com/n05a-design/glide-to-do/blob/main/20_Grafik_Master/README.md) (`20_Grafik_Master/01_Logo/svg`), übernommen am 15. November 2026. Der Inhaber hat sie für App, README und GitHub bereitgestellt.

**Rechte:** Markenrechte und die Nutzung des Logos durch Dritte sind nicht gesondert geregelt. [ADR-004](../../decisions/DECISION_REGISTER.md) ist dazu noch nicht entschieden.

## Wo das Logo vorkommt

Die abgeleiteten Dateien liegen in [`app/assets/brand`](../../app/assets/README.md). Der Code greift nur über [`app.brand`](../../app/brand.py) darauf zu.

| Anzeige | Datei | Zugriff |
| --- | --- | --- |
| Root-README und GitHub-Startseite | `steps-app-icon-512.png` | Kopf der [Root-README](../../README.md) |
| Fenster, Taskleiste und Dialoge | `steps-app-icon-{16,32,64,256}.png` | `app.brand.apply_window_icon(root)` |
| Logo in der Oberfläche | `steps-logo-{64,128,256}.png` | `app.brand.logo_path(size)` |
| Windows-Programm und Verknüpfung | `steps.ico` mit 16 bis 256 px | `app.brand.app_icon_ico_path()` |

Die Desktop-Oberfläche steht aus. Ihr Fenster ruft beim Start `apply_window_icon` auf. Eine GitHub-Kartenvorschau ist nicht gesetzt (Repository → Settings → General → Social preview).

## Logo ändern

1. Master in diesem Ordner ersetzen. Keine Handkorrekturen an den abgeleiteten Dateien.
2. Neue SHA-256 in [`scripts/build_brand_assets.py`](../../scripts/build_brand_assets.py) und in der Tabelle oben eintragen.
3. `python -B scripts/build_brand_assets.py` ausführen.
4. `python -B scripts/build_brand_assets.py --check` und `python -B -m unittest tests.test_brand_assets` ausführen.

Der Generator liest Pfade mit Füllfarben aus Stilklassen. Verwendet ein neuer Master andere SVG-Elemente, Transformationen oder Bögen, bricht er mit einer Meldung ab.

| Einstieg | Inhalt |
| --- | --- |
| [Produktstrategie](../../docs/product/PRODUCT_STRATEGY_AND_MVP.md) | Maßgeblicher Projektkontext. |

[Zur Bereichsübersicht](../README.md)
