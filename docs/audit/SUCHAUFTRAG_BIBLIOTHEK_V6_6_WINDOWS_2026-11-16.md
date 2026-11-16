# Suchauftrag: fehlende Dateien der V6.6-Bibliothek auf Windows (16.11.2026)

**Status:** Auftrag für einen Agenten oder eine Person auf dem Windows-Rechner. Ausschließlich lesend: nichts verschieben, löschen, umbenennen oder committen.

## Hintergrund

Die [Nachprüfung der historischen Indizes](INDIZES_NACHPRUEFUNG_2026-11-16.md) hat ergeben: 148 Markdown-Dateien, die die bibliothekseigenen Indizes V6.0–V6.6 nennen, waren nie im Repository. Die [Liste mit Pfad und SHA-256 laut Index](BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv) ist die Suchgrundlage.

## Auf dem Mac bereits ohne Treffer durchsucht (16.11.2026)

- Git-Historie aller Branches dieses Repositorys, nach Dateiname
- Spotlight, nach Dateiname
- `find` über das gesamte Benutzerverzeichnis nach `STEPS_*V6_*.md`: 824 andere V6-Dateien in Klonen und Arbeitskopien, keine der 148
- ZIP-Archive: `99_ORIGINALARCHIV/STEPS_V5_1_UNVERAENDERT_ORIGINAL.zip` (284 Einträge), `archive/OpenAI Steps Bericht.zip` und `archive/Antigravity Steps Bericht.zip` (je 32 Einträge)

Nicht erfasst: der Windows-Rechner, OneDrive-Dateien, die nur online liegen, und die Ablage `OneDrive-SharedLibraries-feelDataGmbH`.

## Vorgehen auf Windows

1. Die Liste aus dem Repository holen (`docs/audit/BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv`).
2. Kandidatenorte durchsuchen, in dieser Reihenfolge:
   - `%LOCALAPPDATA%\StepsKnowledge\` und `%LOCALAPPDATA%\StepsAudit\` (dort lag auch die wiedergefundene Ontologie)
   - lokale Arbeitsordner und ZIP-Archive der Bibliothek, etwa mit „STEPS_Bibliothek“, „V6_4“, „V6_5“ oder „V6_6“ im Namen
   - lokale Klone mit älteren Ständen
3. Jeden Treffer per SHA-256 mit der Liste vergleichen. Nur bytegleiche Treffer zählen; Treffer mit gleichem Namen, aber anderem Hash getrennt melden.

PowerShell, nur lesend:

```powershell
$liste = Import-Csv '.\docs\audit\BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv'
$soll = @{}; foreach ($z in $liste) { $soll[$z.sha256_laut_index.ToLower()] = $z.pfad_relativ_zur_bibliothek }
$namen = @{}; foreach ($z in $liste) { $namen[[IO.Path]::GetFileName($z.pfad_relativ_zur_bibliothek)] = $z.pfad_relativ_zur_bibliothek }
$orte = @("$env:LOCALAPPDATA\StepsKnowledge", "$env:LOCALAPPDATA\StepsAudit", "$env:USERPROFILE")
Get-ChildItem -Path $orte -Recurse -File -Filter 'STEPS_*.md' -ErrorAction SilentlyContinue |
  ForEach-Object {
    $h = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
    if ($soll.ContainsKey($h)) { [pscustomobject]@{Befund='HASH_GLEICH'; Soll=$soll[$h]; Fund=$_.FullName; SHA256=$h} }
    elseif ($namen.ContainsKey($_.Name)) { [pscustomobject]@{Befund='NAME_GLEICH_HASH_ANDERS'; Soll=$namen[$_.Name]; Fund=$_.FullName; SHA256=$h} }
  } | Export-Csv -NoTypeInformation -Encoding UTF8 "$env:USERPROFILE\Documents\STEPS_V6_6_FUNDE.csv"
```

ZIP-Archive bitte nur auflisten (`[IO.Compression.ZipFile]::OpenRead(...).Entries`) und bei Namenstreffern den Eintrag in einen leeren Ordner außerhalb des Repositorys entpacken, dann wie oben hashen.

## Rückmeldung

- Die Ergebnisdatei `STEPS_V6_6_FUNDE.csv` mit Befund, Sollpfad, Fundpfad und Hash
- die durchsuchten Orte und was nicht zugänglich war
- keine Übernahme ins Repository; das geschieht danach in einem eigenen PR mit Hashnachweis
