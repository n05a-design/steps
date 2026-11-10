
$basis = ".\STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials"
$ziel = Join-Path $basis "README_ORDNERLISTE_EXAKT.md"

$ordner = Get-ChildItem -LiteralPath $basis -Directory |
    Sort-Object Name

$inhalt = @(
    "# STEPS – Exakte Hauptordnerliste"
    ""
    "Erstellt: $(Get-Date -Format 'dd.MM.yyyy HH:mm')"
    ""
    "Anzahl der Hauptordner: $($ordner.Count)"
    ""
    '```text'
)

$inhalt += $ordner | ForEach-Object { $_.Name + "/" }

$inhalt += @(
    '```'
    ""
    "Diese Liste wurde direkt aus dem Dateisystem erstellt."
    "Es wurden keine Ordner umbenannt oder verändert."
)

$inhalt | Set-Content -LiteralPath $ziel -Encoding UTF8

Write-Host "README erstellt: $ziel"
Write-Host "Gefundene Hauptordner: $($ordner.Count)"
