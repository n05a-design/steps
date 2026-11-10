# STEPS – geplanter Python-Domain-Paketpfad (OPTIONALER STRUKTURVORSCHLAG)

Dieser Ordner ist ein **optionaler, noch nicht freigegebener Vorschlag** zur Stabilisierung der geplanten importierbaren Python-Paketidentität `steps` unter `src/steps/`. Er enthält **keinen ausführbaren Produktcode** und bestätigt keine STEPS-Implementierung.

**Hintergrund:** Ein früherer CI-Strukturcheck erwartete `src/steps` und scheiterte, nachdem die Arbeitsstruktur `src/steps-0.00/` umbenannt worden war. Die Python-Importidentität sollte langfristig `steps` heißen, während `0.0.0-dev` als Appversion separat geführt wird. In diesem Paket wird der Vorschlag bewusst *nicht* in den automatisch einzuspielenden Overlay-Baum gelegt.

Vor Übernahme: `src/steps-0.00/` vollständig prüfen, Architekturentscheid treffen, `pyproject.toml`/Importe/Tests abstimmen, alle relevanten Verweise aktualisieren und neuen Struktur-CI-Lauf ausführen. Das reine Erstellen dieses README-Verzeichnisses kann einen Strukturtest grün machen, aber nicht die Produktimplementierung validieren.
