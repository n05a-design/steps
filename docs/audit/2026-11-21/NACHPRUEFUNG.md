# Gesamtaudit · unabhängige Gegenproben

**Prüfstand:** GitHub-`main` `b47ffc27654d5e1df26316b466049f68000d81c6`, Baum `3fe6f904f4d4703b545ba4dd115228c6daf8723b`. Der Prüfstand ist identisch mit dem des [Gesamtaudits](README.md). Diese Nachprüfung verwendete einen frischen Checkout und führte die Katalogbeispiele durch die realen Session-, Speicher- und MIDI-Exportpfade. Die fachliche Gesamtfreigabe steht aus.

## Musiklogik von der Bibliothek bis zum Export

| Prüfbereich | Ergebnis |
| --- | --- |
| Katalog und laufendes Produkt | Namen, Stufenfolgen und Akkordbeispiele beider Bestände stimmen für 28 von 28 Progressionen überein. Eine unabhängige Tonklassenrechnung bestätigt die 116 Akkorde einschließlich der vier notierten Slash-Bässe. Bei PROG-028 stimmen die Akkorde, doch die Stufenangabe mischt Bezugsrahmen. |
| Transposition im Desktop-Pfad | In 336 Fällen stimmen die relativen klingenden Tonklassen. In 84 Fällen ändert sich die zum Grundton geschriebene Stufe eines Akkordgrundtons oder Slash-Basses. Geprüft wurden alle 28 Bestandsprogressionen bei zwölf Halbtonabständen. |
| Notationswechsel und Speichern | Alle 336 Fälle behalten beim Wechsel INT → DE ihre Tonklassen und diatonischen Buchstabenbezüge. Nach Speichern und Laden stimmen Akkorde, Notationskonvention, Tonart, Tempo und bearbeitete Ereigniszeiten mit dem gespeicherten Stand überein. |
| MIDI-Ausgabe | In 336 Fällen stimmen die unabhängig mit Mido 1.3.3 gelesenen Nachrichten und Ticks der INT- und DE-Exporte überein. In fünf Fällen änderte sich der Text eines ausgeschriebenen Slash-Basses erwartungsgemäß mit der Notationskonvention. |

**Desktop-Beispiel:** `C–G–Am–F` zeigt zunächst `I–V–vi–IV`. Nach einem Halbton aufwärts setzt die Session C♯ als Tonika, schreibt aber `C♯–A♭–B♭m–F♯` und zeigt `I–bbVI–bbvii–IV`. Bei der gewählten Tonika C♯ lauten die entsprechenden Stufenakkorde `C♯–G♯–A♯m–F♯`. Die normale Desktop-Aktion ruft diesen Session-Pfad auf. [Open Music Theory, Roman Numerals](https://human.libretexts.org/Bookshelves/Music/Music_Theory/Open_Music_Theory_2e_%28Gotham_et_al.%29/01%3A_Fundamentals/1.19%3A_Roman_Numerals_and_SATB_Chord_Construction)

**API-Grenzfall:** `transpose(-52)` auf `C–G/B` speichert `Ab-–Eb/G-` und die Tonart `Ab-`. Die anschließende Stufenanalyse scheitert am erzeugten Bassnamen `G-`. Die transponierten MIDI-Noten liegen vor dem Rendern im gültigen Bereich. Der Fall betrifft den direkten Session-Aufruf mit großem Halbtonabstand. Der normale Desktop-Knopf transponiert jeweils um einen Halbton.

**PROG-028:** `Em9–Am9–D9–Gmaj9` ist klanglich korrekt hinterlegt. Die Katalogzeile schreibt in e-Moll `i9–iv9–♭VII9–IIImaj9`. Bezogen auf natürliches Moll ist D die VII. Stufe und G die III. Stufe, genau wie in der App-Analyse. Bei Bezug auf die Durtonleiter stehen D und G auf ♭VII und ♭III. Der Katalog verbindet beide Schreibkonventionen innerhalb derselben Zeile. [Open Music Theory, Triads and seventh chords](https://open-musictheory.github.io/docs/fundamentals/triads/)

Die erneute Prüfung der ursprünglichen Ausgabeproben bestätigte die bereits dokumentierten Slash-Bass-, Akkordreduktions- und Drop-2-Abweichungen. Tonklassen- und Dateirundläufe belegen hier die Datenübertragung zwischen den geprüften Komponenten. Die eigentlichen Voicing-Bezeichnungen brauchen eigene Prüffälle.

## Wissens-Skill, Freigabeweg und Kurationswerkzeuge

- Die **25 hinterlegten Eval-Prompts** wurden direkt gegen `KnowledgeAdapter.query` mit seiner Standardkonvention ausgeführt. **16 Antwortstatus weichen von den erwarteten Zuständen ab.** Neun Status stimmen überein. Darunter ist die Frage nach Swing bei 130 BPM: Sie erhält eine sachfremde, als `GROUNDED` markierte Erklärung der Jazzkadenz Dm7–G7–Cmaj7 samt Kadenzquelle. Zwei weitere statusgleiche Antworten zu harmonischen Deutungen liefern keine Quellen-IDs. Die 25/25 im [gespeicherten Eval-Bericht](../../../skills/steps-knowledge/review_report.md) sind mit dieser tatsächlichen Ausführung nicht reproduzierbar.
- In einer temporären Kopie des Quellenregisters wurde die Quelle `omt-ii-v-i` auf `review_required` gesetzt. Der App-Lernkatalog verweigert die Freigabe. Der Knowledge-Adapter liefert denselben Claim mit `GROUNDED`, `verified=True` und Quellenstatus `approved`. Damit ist die im Gesamtaudit identifizierte Abweichung des Freigabewegs durch eine kontrollierte Gegenprobe belegt. Die echte Quelle und die acht Pilotfreigaben waren von diesem Versuch unberührt.
- Der gesamte Kurations-Skill wurde erneut über seine 40 Tests und die [vorhandenen Negativproben](verify_skill.py) geprüft. Die bekannten Lücken bei verfälschten Progressionen, doppelten IDs, fehlender Baseline und ungültigen Registerblöcken sind weiter reproduzierbar. Die strengere Repository-Referenzprüfung erkennt die manipulierte PROG-001.
- Der vollständige Wissensbenchmark ergibt erneut **92 PASS, 0 FAIL, 27 PENDING**, Exit 1. Alle acht Pilotbelege sind über GitHub bestätigt. Die 27 offenen Fälle betreffen unter anderem alle zwölf Coach-Bewertungen, Hörpraxis, Spielbarkeit und Quellenbelege.

## Ablage, Dokumentation und Prüfumfang

- Der frische Checkout enthält **3.078 von 3.078 Dateien bytegleich** zu GitHub-`main`. Die 14 Zeilenendenabweichungen im ursprünglichen lokalen Checkout traten im frischen Checkout nicht auf. Die Inventarsumme, der Git-Baum und sämtliche Dateihashes wurden neu berechnet.
- Über **1.607 Markdown-Dateien** ergeben sich erneut 691 fehlende relative Linkziele als Vorkommen, davon 690 in Archiv- und Forschungsbeständen und eines im historischen Audit unter `docs/`. Die historische PowerShell-Datei mit Endung `.py` bleibt der einzige Syntaxbefund der 2.120 gescannten Dateien. Gescannte Formate und Prüfgrenzen stehen im [Gesamtaudit](README.md).
- Das historische Quellenregister ergibt beim Rohbytevergleich am eingetragenen Pfad erneut 1.557 Übereinstimmungen, 189 Hash-/Größenabweichungen und 149 Pfade außerhalb des geprüften Baums. Die Herkunft der einzelnen Abweichungen bleibt gegen die jeweilige historische Referenz zu klären.
- Im frischen Checkout bestanden **841 Produkttests** mit erzwungenem Desktop-Tk und **40 Skill-Tests**. Dokumentationskonsistenz und Repository-ID-Prüfung bestanden. Die Gegenproben liefen mit temporären Testdateien. Rechteprüfung externer Originale, manuelle Plattformabnahme und Ableton waren außerhalb dieser Nachprüfung.

Die [Workflow-Gegenprobe](verify_workflows.py) lässt sich vom Repository-Wurzelverzeichnis mit `PYTHONPATH=. python3 -B docs/audit/2026-11-21/verify_workflows.py` und Mido 1.3.3 ausführen. Für die [Knowledge-Evaluation](verify_knowledge_eval.py) genügt `PYTHONPATH=. python3 -B docs/audit/2026-11-21/verify_knowledge_eval.py`. Die [Prüfergebnisse](recheck.json) enthalten die Einzelfälle der Transposition und die Antwortstatus der 25 Wissensabfragen.
