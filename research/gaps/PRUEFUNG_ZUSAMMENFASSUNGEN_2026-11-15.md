# Prüfung der Klasse-E-Zusammenfassungen (15.11.2026)

**Status:** Treueprüfung gegen die maschinellen Docling-Extrakte, keine Fachabnahme am gedruckten Original und keine Rechtsprüfung. Alle Zusammenfassungen behalten `fachliche_freigabe: false`.

## Vorgehen und Ergebnis

Jede der zehn [Zusammenfassungen](../STEPS_Bibliothek/Zusammenfassungen/README.md) wurde in Einzelaussagen zerlegt und gegen ihren lokalen Volltext-Extrakt geprüft (387 Aussagen: 6 FALSCH, 57 TEILWEISE, 14 NICHT BELEGT, 1 NICHT PRÜFBAR). Zählung je Werk, Fehlerarten, Notation, Mehrdeutigkeit und Grenzen der Prüfung stehen im [Prüfprotokoll](../STEPS_Bibliothek/Zusammenfassungen/PRUEFPROTOKOLL_FABLE_2026-11-15.md). Diese Datei hält fest, was danach offen bleibt.

Alle sechs FALSCH-Stellen und die beanstandeten TEILWEISE- und NICHT-BELEGT-Stellen sind in den Zusammenfassungen korrigiert. Bei Hindemith war die Leittonregel ins Gegenteil verkehrt: Übermäßige und verminderte Schritte zum Leitton sind erlaubt, das Verlassen so seltener. Die Kopfdaten tragen den Vermerk „korrigiert am 15.11.2026 nach PRUEFBERICHT.md“. Das Feld `seiten` ist dort, wo es die PDF-Seitenzahl und nicht den Buchumfang angibt, entsprechend kommentiert.

Die Spencer-Symboltabelle zu Kapitel 25 folgte in Auswahl und Reihenfolge der Tabelle des Originals. Sie ist auf Entscheidung des Inhabers durch eine knappe Aufzählung der Schreibvarianten ersetzt.

## Nicht übernommen

- Angaben, die nur aus Erinnerung stammen und im Extrakt nicht stehen (in den Prüfberichten als **[Außenwissen]** markiert): Erscheinungsjahr und ISBN von Aldwell/Schachter, Ausgabejahre der Schönberg-Übersetzung, Sterbejahr und Schutzfrist bei Hindemith und Schönberg sowie die Angaben „Professor“ und „FMP Notebooks“ bei Müller.
- Alle Punkte, die nur am gedruckten Original entscheidbar sind (siehe unten).

## Am Original-PDF geklärt (16.11.2026)

Die lokalen Original-PDFs (`restricted_local`) wurden an den betreffenden Stellen als Seitenbild angesehen. Die Bilder sind nicht versioniert. Die Zusammenfassungen sind entsprechend angepasst.

| Werk | Frage | Befund (PDF-Seite) |
| --- | --- | --- |
| Stuart | Zahl im Titel, Vollständigkeit | Der Titel nennt „1500 Chord progressions“. Das Inhaltsverzeichnis listet genau die 17 vorhandenen Tonartseiten (S. 2). Das Heft ist also vollständig; die Titelzahl liegt über den tatsächlichen 1270 Folgen. |
| Palmer/Manus/Lethco | Akkordfolge der Kadenzen | I–IV–I–V (oder V7)–I in drei Lagen (S. 21, C-Dur). |
| Palmer/Manus/Lethco | Bezug des verminderten Septakkords zu harmonisch Moll | Nicht vorhanden. Der Abschnitt leitet den Akkord nur aus dem Dominantseptakkord her und betont die Schreibung B𝄫 (deutsch: Heses) statt A (S. 17). |
| Spencer | Schreibweise der Alterationen und des Basstons | Gleichwertige Paare ohne 7 vor der Option: C−9/C♭9 und C+11/C♯11, dazu Cm7−5/Cm7♭5 für halbvermindert. Basston unter dem Symbol (als Bruch) oder rechts daneben mit Schrägstrich, für Umkehrung wie Orgelpunkt (S. 345). Die Zusammenfassung hatte die Beispiele fälschlich mit 7 geschrieben. |
| Spencer | Bedeutung von „changing tones“ (Kap. 12) | Das steht schon im Fließtext: Ein Paar von changing tones gilt als Verbindung von oberer und unterer Nebennote, also die Wechselnotengruppe. |
| Hindemith | Bandzählung | Die Titelseite nennt „Revised Edition“, © 1943, 1944, und keine Bandzählung (S. 1–2). |
| Aldwell/Schachter, Schönberg | Impressum | Auf das Titelblatt folgt direkt das Inhaltsverzeichnis; die Impressumseite fehlt im PDF selbst (S. 1–2). Jahr und ISBN lassen sich aus diesen Dateien nicht belegen. |
| DeSantis | Zeigen die Piano-Roll-Abbildungen Ableton Live? | Die Abbildungen zeigen einen schlichten Piano-Roll-Editor ohne Programmnamen (z. B. S. 205). Auch der Text bleibt werkzeugneutral und spricht von „most DAWs“. |
| Pejrolo | Beilage | Laut Rückseite eine CD-ROM mit MIDI-Dateien, Samples, Beispieltracks und Software-Demos. Der Anhang listet die Beispiele nach CD-Track (S. 309–311, 322). |
| Adorno | Ist die zweite Kopie bytegleich? | Ja, beide Dateien haben SHA-256 `3077b828…e39c`. |
| Spencer | Steht das Basston-Beispiel „C7/E“ so im Original? | Ja. Gedruckte S. 334 (PDF-S. 345) zeigt „C7 über E oder C7/E“ für die Umkehrung und „Cm7 über F oder Cm7/F“ für den Orgelpunkt. Das frühere „Cm/Bb“ stand dort nicht. Nachgeprüft am 16.11.2026, zweiter Durchgang. |
| Schönberg | Ist Kap. XI nur über Titel und Kapitelanfang belegt? | Nein: Das Kapitel liegt im PDF vollständig vor (gedruckte S. 202–206, PDF-S. 214–218) und wurde ganz gelesen. Die Zusammenfassung ist um Schönbergs Regel zum Quartsextakkord (kadenzierender auf betonter Zählzeit, durchgehender frei) und die Notation der Übungen (Halbe, zwei Akkorde pro Takt) ergänzt. Nachgeprüft am 16.11.2026, zweiter Durchgang. |

## Offen

### Am Original zu klären

| Werk | Frage |
| --- | --- |
| Aldwell/Schachter | Jahr und ISBN (Impressumseite fehlt im PDF). Teile des Inhaltsverzeichnisses und die Aufzählung der drei Quartsextakkord-Arten (Unit 19 §2) sind im Extrakt verstümmelt bzw. ausgefallen. Sequenzmuster und Literaturbeispiele liegen nur als Notenbild vor. |
| Schönberg | Jahr und ISBN (Impressumseite fehlt im PDF). Mehrere Jahreszahlen sind OCR-gestört. |
| Hindemith | Stimmumfänge, die alterierten Dominantformen in Kap. XIII und die Auflösungstabellen liegen nur als Notenbild vor. Die Kapitelzuordnung verschobener Randbemerkungen (Terzverdopplung, Zäsurregel) ist zu bestätigen. |
| Palmer/Manus/Lethco | Fingersätze und Vorzeichen. |
| Stuart | Die fehlerhaft erkannten Zellen der Akkordtabelle und einzelne verrutschte Katalognummern. |
| DeSantis | Das Stufendiagramm zu den Tendenzregeln fehlt im Extrakt. |
| Müller | Abbildungen und Beispiele zu Kapitel 5 liegen nur als Bild vor. |

### Zu den Quelldateien

- **Aldwell/Schachter:** Dem PDF fehlen die Impressumseite, Anhang II und beide Register. Gedruckte Seitenzahlen und PDF-Seiten laufen auseinander (Unit 6, S. 83 in PDF 91–100; Anhang I, S. 619 in PDF 601–610). Dem PDF fehlen also vermutlich auch im Buchinneren Seiten.
- **Schönberg:** Dem PDF fehlt die Impressumseite.
- **Müller:** Der Dateiname verweist auf Z-Library, also eine nicht autorisierte Quelle. Die Beschaffungsfrage ist nicht erledigt; siehe [Rechteinventar](RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md).
- **Adorno:** Nur ein 30-seitiger Auszug, Herkunft offen (Verlagsleseprobe?).
- **Hindemith, Schönberg:** Rechtsaussagen zu Schutzfrist und Gemeinfreiheit (bei Hindemith im Feld `rechtehinweis`) stehen nicht in den Quellen. Sie sind Projektannahmen, keine geprüfte Rechtslage.

### Strukturnähe (entschieden)

Zwei Stellen kamen einer Strukturübernahme nahe. Der Inhaber hat am 16.11.2026 entschieden:

- **Aldwell/Schachter, Gliederung:** Die Zusammenfassung gab ein fast vollständiges übersetztes Inhaltsverzeichnis mit Unterabschnitten wieder. Jetzt stehen nur noch die 32 Einheiten mit eigenem Kurztitel, ohne Unterabschnitte. Die wichtigen Konzepte stehen weiter unter „Nutzen für STEPS“.
- **Stuart, Musterlisten:** Die Zusammenfassung nannte rund 35 Folgen, die sich einzelnen Katalognummern zuordnen ließen (etwa ein Viertel des Grundkatalogs). Jetzt bleiben die Musterfamilien mit je ein bis zwei typischen Beispielen.

Die früheren Fassungen sind in der Git-Historie erhalten (Stand `5139760`).

Wörtliche Passagen von mehr als etwa 15 Wörtern wurden in keiner Zusammenfassung gefunden. Das ist ein fachlicher Hinweis, keine Rechtsberatung.

### Prüfberichte

Die Gesamtübersicht ist als [Prüfprotokoll](../STEPS_Bibliothek/Zusammenfassungen/PRUEFPROTOKOLL_FABLE_2026-11-15.md) versioniert. Die zehn Einzelberichte und eine Sicherung der Zusammenfassungen vor der Korrektur liegen nur lokal im Prüfpaket außerhalb des Repositorys, weil sie zur Belegführung aus den Extrakten zitieren. Der Vermerk „nach PRUEFBERICHT.md“ in den Kopfdaten verweist auf diese lokalen Berichte. Die Fassungen vor der Korrektur sind zusätzlich in der Git-Historie erhalten (Stand `4feb3db`).

[Zur Übersicht der offenen Evidenz](README.md)
