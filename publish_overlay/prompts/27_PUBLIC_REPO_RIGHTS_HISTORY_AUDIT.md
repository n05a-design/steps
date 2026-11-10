# Auftrag 27 – Rechtescope und veröffentlichte Fremdmaterialien kritisch prüfen

**Auftrag an unabhängiges Audit-Team; keine Rechtsberatung durch KI ersetzen.** Quelle: aktueller Steps-Git-Tree `75329fef`, LICENSE MPL-2.0, Originaldateien/History-/Branch-/Release-Lage, `docs/governance/RIGHTS_SECURITY_AND_RELEASE.md`. Es existieren 60 PDFs, zahlreiche Web-Caches sowie Audio-/MIDI-Daten. Git-Verfügbarkeit ist kein Nutzungsrecht; „Copyright unknown“ ist nicht „CC BY“.

## Vorgehen

1. Dateibaum mit Blob-SHAs, Größen, Dateitypen, Version/Archivzugehörigkeit und ursprünglichen Herkunftsnamen inventarisieren; vorhandenes Duplikatregister nutzen.
2. Fremdwerke nach Identität/Edition/Autor/Verlag/URL/Hash/License, Verwendungszweck und Änderungsrecht priorisieren. Besonders problematische oder unklare PDF-Dateien *zunächst nur mit Metadaten* prüfen; keine urheberrechtlich geschützten Volltexte in den Auditreport oder Cloudmodell-Inputs kopieren.
3. Für jeden priorisierten Posten Status `approved`, `review_required`, `restricted_local`, `rejected` mit rechtlichem Nachweis oder fehlendem Beleg erfassen. Unterscheide lokale private Analyse, öffentliche Source-Distribution, eingebettetes App-Asset und CI-Download.
4. Prüfe historische Commits, Branch-/PR-/Release-Referenzen, Fork-Risiken und Versionssnapshots. Löschen aus `main` ist nicht History-Löschung. Verweise auf Mozilla MPL FAQ und GitHub History Guidance; keine einseitige Pauschalentscheidung zu allen PDFs.
5. Bei fraglichem öffentlichen Material erst die verantwortliche Person und ggf. juristische Beratung informieren. **Keine** Force-Pushes, Repo-History-Rewrites, Massenlöschungen oder öffentlichen Rechtseinstufungen ohne ausdrückliche Freigabe.

## Liefergegenstände

`public_asset_inventory.csv`, `license_findings.csv`, `history_impact.md`, `recommended_mitigation_with_alternatives.md`, `recheck_manifest.json` und ein separater Plan, wie künftige Ingestion externe Quellen im privaten Rohbereich hält und nur frei verwendbare eigene Paraphrasen/Metadaten publiziert. Erfasst werden auch Font-/Symbol-/Musik-/Soundbankdateien und ihr Release-Scope. Die Liste endet bei **konkreten nächstentscheidbaren Fällen**, nicht bei einer unprüfbaren Rechtsfreigabe.
