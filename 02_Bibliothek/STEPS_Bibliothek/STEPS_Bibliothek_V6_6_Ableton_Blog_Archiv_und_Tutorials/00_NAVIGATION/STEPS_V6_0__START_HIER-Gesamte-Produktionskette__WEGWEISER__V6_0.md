# STEPS V6.0 — Gesamtsystem moderne und zeitgenössische Musikproduktion

**Version:** 6.0 — 2026-11-09. **Basis:** offizielles V5.4-ZIP (551 Dateien), SHA-256-identisch erhalten. **Erweiterung:** eigenständige Vollproduktions-Architektur ab `16_…`; alle ursprünglichen Ordner 00–15 sowie 90/99 bleiben bestehen.

## Wozu die Bibliothek dient
Dieses Paket soll langfristig eine nachvollziehbare **Research Library**, **Learning Library**, **Production Workflow Library** und **Codex Implementation Foundation** sein. Es ist **KEINE fertige DAW**, enthält nicht alle externen Fachbücher im Volltext und ersetzt keine künstlerische Bewertung.

## Drei Ebenen
1. **Musik & Komposition:** 01–05 (Theory, Harmony, Progressions, Composing, Rhythm/Drums), 07 (Cognition/Stil/Kultur).
2. **Produktionspraxis:** 06 (bestehende Producer Tools) sowie 16–44 (neue detaillierte Fachgebiete). Es wird ausdrücklich zwischen Musikkonzept, Softwarehandlung und Audiotechnik unterschieden.
3. **System & Qualität:** 08–15 (Computational/Skills/Quellen/Validierung/Task/Governance/Data/Tools), 90/99 (Historie und Original).

## Navigationsdateien
- `STEPS_V6_0__PRODUKTIONSLANDKARTE__TAXONOMIE__V6_0.md` — vollständige Kategorienmatrix.
- `STEPS_V6_0__THEMENREGISTER__DATEN__V6_0.json` — strukturierte Kategorien und Stichwörter, **nicht** als fachlich vollständig reviewed ausgeben.
- `STEPS_V6_0__LUECKENPRUEFUNG__GAPREGISTER__V6_0.md` — echte Lücken, Stand und Abhängigkeiten.
- `STEPS_V6_0__DATEIINDEX__AKTIV_UND_HISTORISCH__V6_0.csv` — jede physische Datei, Kategorie, Stichwörter, Status, Hash, Nutzen.
- `10_QUELLEN_LIZENZEN/STEPS_QUELLEN__Produktionsstandards-Hersteller-Curricula__REGISTER__V6_0.json` — kontrollierte externe Referenzen.
- `12_CODEX_AUFTRAEGE/STEPS_CODEX__Gesamtproduktion-Architektur-Implementierung__MASTER_AUFTRAG__V6_0.md` — phasenbasierter Codeauftrag.
- `11_VALIDIERUNG_QUALITAET/STEPS_V6_0__TECHNISCHE_PRUEFUNG__REPORT__V6_0.json` — welche strukturellen Tests wirklich gelaufen sind.

## Dateinamen
`STEPS_<BEREICH>__<STICHWORT1-STICHWORT2>__<DOKUMENTTYP>__V6_0.md`. Hauptdateien werden nicht still überschrieben; historische V5.4-Daten bleiben erhalten. Neue Verzeichnisse liegen alphabetisch nach Nummer sortiert.

## Ehrlicher Status
**Abdeckung als Taxonomie ≠ fachliche Vollständigkeit ≠ technische Fertigstellung.** Alle neuen Fachkarten sind redaktionell erstellte Forschungssynthesen und Lern-/Entwurfsobjekte, die einer Fachprüfung bedürfen. Einzelne externe Standards wurden anhand offizieller Webseiten geprüft; die Volltexte vieler Standards und Bücher **wurden nicht vollständig gelesen**. Die Rechte an Kursinhalten/MIDI aus fremden Quellen sind gesondert zu prüfen.

## Ausgangskonflikt V5.4
Im Arbeitscontainer gibt es zusätzlich einen V5.4-Entpackordner mit **677** Dateien, das offiziell gelieferte ZIP enthält jedoch **551**. V6 übernimmt ausschließlich das nachprüfbare ZIP, nicht die ungeklärten zusätzlichen Arbeitskopien. Ein Abgleich ist als offene Governance-Aufgabe dokumentiert.

## Forschungssammlung vs Softwareprodukt
Die Aufnahme eines Fachgebiets in die Bibliothek **autorisiert nicht automatisch** seine Implementierung in Steps. Kriterien sind Nutzwert, vorhandene Codebasis, Lizenzlage, Testbarkeit, Wartbarkeit, UX, Plattformfähigkeit und Freigabe.
