# Fable 5.2 · Originaler Auditlauf vom 12. November 2026

Der Lauf bezieht sich auf STEPS `22f3f5f348d060abfd4e2ffc917d0c95a639441e`.
Die Dateien dokumentieren diesen historischen Prüfstand. Aktuelle Einordnung
und behobene Abweichungen stehen in der [STEPS-Nachprüfung](../../../docs/audit/fable-5.2/STEPS_FABLE_5_2_NACHPRUEFUNG.md).

| Datei | Inhalt |
| --- | --- |
| [Startauftrag](STEPS_FABLE_5_2_STARTAUFTRAG.md) | Ursprünglicher Auftrag mit Umfang und Grenzen. |
| [Originalbericht](results/FABLE_AUDIT_REPORT_2026-11-12.md) | Befunde, Abdeckungsmatrix und offene Gegenproben. |
| [Rohausgabe](results/GEGENPROBEN_ROHAUSGABE_2026-11-12.txt) | 477 Einzelproben des damaligen Laufs. |
| [Arbeitsnotizen](results/ARBEITSNOTIZEN.md) | Prüfablauf und Zwischenstände. |
| [Probeskripte](work/probes/) | Historische Auswertung für den damaligen Checkout. |
| [Arbeitsfassungen](arbeitsfassungen/) | Drei lokale Vorfassungen aus dem Fachnachweise-Worktree bei `3dcd6b5`. |
| [Register-Migrationsentwurf](arbeitsfassungen/AUFGABENREGISTER_MIGRATIONSENTWURF.md) | Prüffassung aus dem historischen Snapshot mit 33 Aufgaben. |
| [SHA-256](SHA256SUMS.txt) | Prüfsummen aller 18 archivierten Dateien. |

Auditbericht, Rohausgabe und Arbeitsnotizen stimmen bytegleich mit den
Hashes in der Nachprüfung überein. Das Paket enthält Arbeitsmaterial von
STEPS und bibliografische Verweise. Für referenzierte Drittquellen gilt
die [Rechterichtlinie](../../../knowledge/sources/RIGHTS_POLICY.md).

Historische Befehle verwenden die damalige Verzeichnisstruktur und
Schnittstellen. Mutierende Proben, insbesondere `K11_mutation.py`, nur in
einer entbehrlichen isolierten Kopie der historischen Revision ausführen.
Die drei Arbeitsfassungen behalten ihre Originalbytes. Ihre relativen
Verweise beziehen sich auf die damaligen Pfade unter `knowledge/` und
`research/`.

Die Register-Prüffassung dokumentiert die Testmigration. Der produktive
Registerpfad und die Abnahmebedingungen stehen im
[Registerprotokoll](../../../.agents/skills/steps-knowledge-curation/references/work_instructions_protocol.md).
