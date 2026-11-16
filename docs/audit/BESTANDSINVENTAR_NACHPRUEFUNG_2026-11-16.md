# Nachprüfung des Bestandsinventars vom 11.11.2026

**Status:** Lesende Pfad- und Hashprüfung. Das Inventar [`knowledge/research/01_BESTANDSINVENTAR.csv`](../../knowledge/research/01_BESTANDSINVENTAR.csv) bleibt als historischer Stand unverändert. Geprüfter Stand: `main` bei `a96abb5` (16.11.2026).

## Frage

`OPEN_GAPS.md` vermerkt seit dem 10.11.2026: „Historische JSON-/CSV-Indizes benötigen Pfad- und Hashrevalidierung.“ `AGENTS.md` verlangt, dass keine Dateien unerwartet verloren gehen. Geprüft wurde, ob jede der 3.947 Zeilen des Inventars vom 11.11.2026 im heutigen Bestand wiederzufinden oder ihr Fehlen erklärt ist.

## Vorgehen

1. Für jeden Inventarpfad: Existiert die Datei, wird ihr SHA-256 mit dem Inventarwert verglichen, auch nach Umstellung der Zeilenenden (LF/CRLF).
2. Fehlt die Datei, wird geprüft, ob sie per `.gitignore` ausgeschlossen ist.
3. Sonst wird ihr Hash, auch in LF- und CRLF-Fassung, unter allen heute versionierten Dateien gesucht.
4. Was dann noch fehlt, wird einer dokumentierten Entfernung zugeordnet oder als ungeklärt markiert.

## Ergebnis

| Befund | Zeilen | Bedeutung |
| --- | ---: | --- |
| UNVERAENDERT | 1.714 | Pfad und Hash stimmen. |
| NUR_ZEILENENDEN | 341 | Gleicher Inhalt, nur andere Zeilenenden. |
| INHALT_GEAENDERT | 183 | Datei am selben Pfad seit dem 11.11. bearbeitet (z. B. README, Wissensdateien, Tests). |
| VERSCHOBEN | 116 | Byte- oder zeilenendengleich unter neuem Pfad wiedergefunden, alle unter `archive/` (61 `project-history`, 50 `audit-history`, 3 `documentation-history`, 2 `agent-history`). |
| ENTFERNT_GLIDE_37E691B | 1.580 | Der Glide-Referenzstand unter `src/glide-v3.53/`, bewusst entfernt mit Commit `37e691b` („Entferne den bisherigen Glide-Referenzstand“, 14.11.2026). In der Git-Historie erhalten. |
| RESTRICTED_LOCAL | 13 | PDFs der Rechteklasse E, seit 14.11.2026 per `.gitignore` nur lokal; siehe [Rechteinventar](../../research/gaps/RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md). |
| **UNGEKLAERT** | **0** | |
| Summe | 3.947 | |

Seit dem 11.11.2026 sind 712 versionierte Dateien hinzugekommen, die das Inventar naturgemäß nicht enthält.

**Folgerung:** Es gibt keinen unerwarteten Dateiverlust gegenüber dem Inventar vom 11.11.2026. Jede fehlende Datei ist verschoben, bewusst entfernt oder lokal ausgelagert.

## Zuordnungstabelle

[`BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.csv`](BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.csv) enthält die 312 Zeilen mit den Befunden VERSCHOBEN (mit heutigem Pfad), INHALT_GEAENDERT und RESTRICTED_LOCAL. Unveränderte, nur in den Zeilenenden abweichende und Glide-Zeilen sind nur gezählt, damit die Tabelle klein bleibt.

## Grenzen

- Geprüft ist nur dieses eine Inventar. Weitere historische Indizes, etwa unter `archive/manifests/` oder die Antigravity-Dateiinventare, sind nicht nachgeprüft.
- INHALT_GEAENDERT sagt nichts darüber, ob eine Änderung inhaltlich richtig war, nur dass sie stattfand.
- Die 13 Dateien unter `restricted_local` sind nur über `.gitignore` zugeordnet. Ob sie lokal vorhanden sind und ihr Hash stimmt, ist hier nicht geprüft.
