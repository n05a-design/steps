# GitHub-Abgleich und Pattern-Fortsetzung am 14.11.2026

## Ergebnis und geprüfte Basis

Vor jeder neuen Änderung wurde GitHub gegen die lokale Audit-Arbeitskopie
abgeglichen. GitHub-`main` steht auf
`cda6cb99bf3d4c6bc1bde29c4ffef1405a117c0f`. PR #62 wurde extern am
14.11.2026 um 18:43:23 UTC mit `99ca36aa1b2b1db4671edcd06e3eb97454d07496`
gemergt. Zum Abgleichzeitpunkt gab es nur den Remote-Branch `main` und keine
offenen PRs. Die vier Workflows auf dieser Revision waren erfolgreich:
Python `43638890624`, Secret `43638890655`, Struktur `43638890555`,
Pilot `43638890620`.

Die saubere lokale Audit-Arbeitskopie stand zuvor auf `8215cfb…`, hatte
keine eigenen zusätzlichen Commits und lag 18 Commits zurück. Ein neuer
Branch `codex/audit-abgleich-pattern-20261114` wurde exakt von der geladenen
GitHub-Revision angelegt. `origin` verweist hier weiterhin auf den lokalen
OneDrive-Klon; der Abgleich verwendete ausdrücklich die echte GitHub-URL.
Kein Merge nach main, kein Reset und keine Branchlöschung.

Der OneDrive-Hauptcheckout steht ebenfalls sauber auf `cda6cb9…`.
Der Worktree `knowledge-coverage-audit-41e979` ist sauber, aber älter
(`091f69a`). `steps-checkout-selbstcheck-03cfe9` steht auf `d7357f9` und hat
346 Statuszeilen, davon 169 Änderungen bereits versionierter Pfade.
Diese fremden Änderungen wurden nicht angefasst. Nicht vorhandene historische
Mac-/Windows-Worktreeeinträge wurden nicht bereinigt. Dies ist kein
Vollständigkeitsnachweis für sämtliche privaten Ordner oder ignorierten Dateien.

## Bereits durch die zwischenzeitlichen Arbeiten erledigt

| Paket | Tatsächlicher Fortschritt | Weiterhin offen |
| --- | --- | --- |
| PR #62 | RWC-/Jazz-Komponenten und Garcia2023 integriert | Exakte Pattern, ältere Originale, Fachabnahme |
| PR #63/#64 | PDF-Extrakte und korrigierte Abdeckungszählung integriert | OCR/Extraktion ist kein Noten- oder Quellenabnahmebeleg |
| PR #65/#66 | Glide-Kopie entfernt; vier registrierte Auditoriginale gesondert archiviert | Keine erneute Einspielung der entfernten Referenzkopie |
| PR #67 | MakingMusic-Reparatur in der Historie nachgewiesen | Volltext inzwischen durch PR #70 bewusst aus aktuellem Git genommen |
| PR #69/#70 | HTML-Extrakte, Rechteinventar, OCR und Zusammenfassungen; Klasse E jetzt restricted_local | Andere Rechteklassen und historische Exposition nicht pauschal freigegeben |

Der unveränderte neue main bestand lokal zunächst 318 Kerntests. Der alte
Restposten „zwei beschädigte MakingMusic-Kopien reparieren“ ist als aktuelle
Reparaturaufgabe überholt. Die Reihenfolge Reparatur → bewusste Herausnahme
ist erhalten; gelöschte aktuelle Git-Dateien sind kein erneuter Reparaturfehler.
Owner-Entscheidungen zur Ablage ersetzen keine Rechteinhaberfreigaben.

## REL-001 und REL-005: tatsächlich gemessene Patternkomponenten

Die [maschinenlesbare Beobachtung](REL_PATTERN_KOMPONENTEN_2026-11-14.json)
wird mit `scripts/audit_relation_patterns.py` aus den bereits hashgebundenen
lokalen RWC-/JazzSAMBA-Lieferungen reproduziert. Fremde MIDI-Dateien bleiben
außerhalb von Git. Die Prüfung zählt nur positive Note-ons auf Kanal 10
(nullbasiert 9), vollständige Takte und halb offene Zeitintervalle. Ein Ereignis
kann nicht mehrfach verwendet oder aus dem Nachbartakt geliehen werden.
Überlappende Harmoniefenster erzeugen keine mehrfach gezählten Takte.
Toleranz: ±0,1 lokale Viertelnote. RWC besitzt Beatzeiten; bei Jazz werden
Viertel aus Taktanfang/-ende interpoliert. Letzteres ist eine Modellannahme.

| Prüfung | Messbestand | Ergebnis |
| --- | --- | --- |
| REL-001: strenge PROG-001-Harmonieformen | 6 RWC-Stücke, 64 eindeutige vollständige Takte in ihren Fenstern | 4 Takte mit 35/36 auf 1/3; 31 mit 38 auf 2/4; 1 mit 42 auf allen Achteln; **0 gemeinsame Kernrastertreffer** |
| REL-005: strenge PROG-003-Chartformen | 18 Jazz-Takes, 880 eindeutige vollständige Takte in passenden Fenstern | 136 Takte mit 44 auf 2/4, davon 115 ohne zusätzliche Note-44-Ereignisse; 0 mit 51 auf allen Vierteln; **0 gemeinsame Kernrastertreffer** |

Die frühere RWC-Beobachtung erlaubte 38 **oder** 40 und zusätzliche Ereignisse;
PAT-001 nennt ausdrücklich 38. Der damalige P084-Teilmusterkandidat bleibt
historisch gültig im damals deklarierten Umfang, liefert aber keinen Nachweis
des engeren jetzigen Kernrasters. Keine nachträgliche Korrektur seines Originals.

Für REL-001 ist „3e+“ im historischen Katalog nicht als eindeutiger Tickwert
formalisiert; die zusätzliche Synkope ist daher nicht als erfüllt behauptet.
Für REL-005 ist die ebenfalls gemessene ternäre Skip-Figur ein gesonderter
Vorschlag, keine universelle Friberg-Ratio oder historische Definition.
`same_note_grid` betrifft nur eine jeweilige Notengruppe. Es bedeutet nie
Identität des ganzen Arrangements. Zusätzliche Instrumente, Dynamik,
Feathering, exakte 115/130 BPM, authentifizierte Instrumentbelegung, gespielte
Harmonie, Audioausrichtung und repräsentative Häufigkeit bleiben ungeprüft.

Die Nulltreffer sind **keine Widerlegung der Genre-/Paarungsbehauptungen**.
Jazz-MIDI enthält insgesamt auch Note 51; sie erfüllt nur das geprüfte
Viertelraster nicht. Andere häufige native Notennummern wurden nicht allein
wegen ihrer Häufigkeit zu Ride umbenannt. Beide Relationen und alle 14
historischen Korpusbehauptungen bleiben OPEN.

Eine getrennte technische Gegenrechnung prüfte RWC_P084 und Jazz-Take 3:
158 beziehungsweise 237 Takte, insgesamt 1.580 direkte Rastervergleiche.
Direkte Intervallsuche und Sekundeniterator stimmen mit Raster-/Tickrechnung
überein. Der Mido-Parser ist gemeinsam; dies ist keine unabhängige menschliche
Fachabnahme. Die Gegenrechnung liegt im lokalen Nachweisordner.

## CDR-019: ältere Originalquellen erneut gesucht

Die neuen Bibliotheks-Markdown-Dateien enthalten keinen Treffer für
Reily, Cabral, Bim Bom, Schreiner oder Garcia. Das ist eine begrenzte
Volltextsuche, kein Nachweis über Bilder, OCR-Fehler oder alle Privatablagen.
Die [Nachprüfung](CDR019_KATALOG_NACHPRUEFUNG_2026-11-14.json) ergänzt eine
konkrete institutionelle Beschaffungsspur: CAPH/USP führt Garcias
1998er Dissertation unter Referenz **4195N**. Das Register liefert keinen
gelesenen Volltext; die Dissertation ist nicht automatisch die Ausgabe 1999.
[CAPH-Katalog](https://caph.fflch.usp.br/teses-e-dissertacoes?combine=&field_nodebase_ano_value=All&field_nodebase_departamento_value=Letras+Cl%C3%A1ssicas+e+Vern%C3%A1culas&field_nodebase_grau_value=All&order=field_nodebase_nreferencia&page=11&sort=desc).

Reilys institutioneller Publikationseintrag bestätigt Autorin, Jahr,
Zeitschrift und Seiten 1–16; ein Volltext war dort nicht angeboten.
[Queen's University Belfast](https://pure.qub.ac.uk/en/publications/tom-jobim-and-the-bossa-nova-era/).
Erforderlich bleiben Reily1996 S.5/Fig.1, Cabral Band2 S.10–17 insbesondere
S.12, Garcia1999 S.21–22/25–38/45–49 und eine konkrete Schreiner1993-Seite.
Garcia2023 bleibt ein eigener begrenzter Autorenbeleg. Keine ältere
Originalseite wurde neu als gelesen oder verifiziert markiert.

## Restbestand und nächste Voraussetzungen

Diese Übersicht ist ein Evidenzindex, kein zweites Aufgabenregister.

1. **14 Korpusbehauptungen:** Quellinstrumentmapping und präzise Zielraster
   festlegen; passende gemeinsame Annotationen gegen diese Definitionen messen.
   Für Häufigkeitsbehauptungen zusätzlich den Sampling-Rahmen und Nenner vorab
   bestimmen. Neue Nullmessungen schließen keine historische Behauptung.
2. **CDR-019/CDR-021 und sechs Definitionen:** genannte ältere Originalseiten
   berechtigt beschaffen; CDR-021 benötigt weiterhin einen belegten dynamischen
   Akzentkontext. Vorschläge unabhängig fachlich bewerten.
3. **Graph:** 97 Originalkanten erhalten, 41 begrenzte Stichproben, 1 FAIL,
   55 OPEN; CDR-010 bleibt FAIL. Keine vollständige neue Graphfachabnahme.
4. **27 Benchmark-PENDING:** menschliche Coach-/Hör-/Spiel-/Fachabnahmen,
   Quellenprovenienzen und sechs CSS-Pflichtfälle gemäß bestehender Einzelmatrix.
5. **Sicherheit/Rechte:** historische Schlüsselexposition, Owner-/Rechtefreigaben,
   CSS-Bundle und dauerhafte Archivzuordnung offen. Ein grüner Scan erteilt
   diese Freigaben nicht. Neue Rechteentscheidungen nicht zurückdatieren.
6. **Weitere technische/Quellenposten:** SRC-033, vier PPR-Provenienzen,
   Forschungsclaim-Locatoren, Paket-/Publikationsnachweis und der vollständige
   Abgleich aller weiteren lokalen Bestände gemäß bestehendem Restblockerindex.

Gesamtaudit: **NICHT ABGESCHLOSSEN**. Die vorliegende eng begrenzte
Patternmessung ist operativ umgesetzt; fachliche und rechtliche Abnahmen bleiben offen.

## Reproduktion

```powershell
python -B scripts/audit_relation_patterns.py --check
python -B scripts/audit_relation_patterns.py --rwc-archive <lokales-RWC-ZIP> --jazz-manifest <lokales-Jazz-Manifest> --check
python -B scripts/audit_graph_corpus.py --check
python -B -m unittest discover -s tests -p 'test_relation_patterns.py'
```

Nur die optionale Quellenmessung benötigt das vorhandene Auditpaket Mido.
Die normale CI prüft Beobachtung und Regressionen offline. Vollständige
Prüfergebnisse und exakte Commitzuordnung werden im lokalen Nachweisordner
`Auditnachweise-2026-11-14/abgleich-pattern/` gesichert.

## Abschlussprüfung dieses Änderungspakets

| Prüfung | Ergebnis |
| --- | --- |
| Kerntests | 329 bestanden, einschließlich 11 neuer Rasterregressionen; Basis vor Änderungen 318 |
| Skilltests | 36 bestanden |
| Wissensbenchmark, scope all | 92 PASS / 0 FAIL / 27 PENDING; Exit1 wegen Pflichtnachweisen erwartet, kein Gesamt-PASS |
| 18 weitere Integritäts-/Generatorprüfungen | Alle Exit0, einschließlich Originalontologie, Graph, Semantik, Follow-up, Korpus, Golden, Coverage, Referenzen, Secret-Bereinigung, API und Lernmaterial |
| Vollständiger Secret-Scan | 0 quarantänisierte / 0 neue Funde, Exit0; Sicherheitsfreigabe bleibt offen |
| Dokumentationslinks | 978 interne Links in 164 Markdown-Dateien, keine neuen aktiven Fehler, 25 bekannte historische Archivfehler |
| Optionale Quellenreproduktion | Identische versionierte Beobachtung aus lokalem RWC-Archiv und Jazz-Manifest erneut erzeugt und verglichen |
| Technische Gegenrechnung | 1.580 direkte Rastervergleiche an zwei Original-MIDIs erfolgreich; gemeinsamer Parser ausdrücklich benannt |

Der erste lokale Linkprüfer meldete einen scheinbar defekten Link, weil er
bei einer korrekt mit `<…>` geklammerten Adresse am inneren `)` abbrach.
Der echte Dateipfad existiert. Die korrigierte lokale Prüfauswertung behandelt
diese Markdown-Syntax; die gültige Produktdokumentation wurde nicht umgeschrieben.

Die GitHub-Prüfungen oben gelten für den abgeglichenen main. Die neuen lokalen
Änderungen werden auf dem separaten Branch als Commit gesichert. Für dieses
Paket wird ohne neuen Upload kein neuer Remote-CI-Lauf behauptet. Historische
97 Kanten, Golden-Originale und Secret-Baseline bleiben unverändert. Fach-,
CSS- und Sicherheitsfreigaben werden weder aus Testgrün noch aus einer
Owner-Entscheidung über die lokale Ablage abgeleitet.
