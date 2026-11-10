# Tonhöhe, Schreibweise und Enharmonik

**STEPS-Kennung:** MUSIKTHEORIE-54-01  
**Status:** inhaltliche Fachstudie, keine abgeschlossene peer-reviewte Theorie  
**Geltungsbereich:** 01_MUSIKTHEORIE, kontextabhängige Interpretation.  
**Quellenanker:** R01, R02, R10; Quellenstatus im V5.4-Register.

## Begriff und fachliche Abgrenzung
MIDI-Pitch, klingende Frequenz, diatonischer Buchstabe und Vorzeichen sind getrennte Eigenschaften. In 12-TET können C# und Db gleich klingen, aber nicht dieselbe harmonische Rolle tragen. Ein Pitch-Objekt muss Notenname und Stimmungskontext speichern, nicht bloß pitch class.

## Eigenständig konstruiertes, nachprüfbares Fallbeispiel
In A-Dur ist der Leitton G#; in As-Dur heißt die vierte Stufe Db. Ein Export, der alles über chromatische Zahlklassen zurückübersetzt, kann musikalisch falsche Schreibungen erzeugen.

## Wo die Vereinfachung fehlschlägt
Es wäre ein Fehler, `midi=61` fest als `C#4` zu speichern und daraus jede notierte Lesart abzuleiten. DAW-Oktavnummern variieren zusätzlich.

## Arbeitsweg für Composing, Analyse und Produktion
1. Definiere Tonzentrum, Rhythmus-/Formkontext und Ziel des konkreten Beispiels.
2. Trenne notierbare Fakten, hörbaren Befund, Stilhypothese und kreativen Vorschlag.
3. Führe einen kontrollierten A/B-Vergleich durch: ändere nur einen musikalischen Parameter.
4. Dokumentiere beide Varianten mit MIDI/Partiturreferenz, Interpretations-Lens und offenem Reviewstatus.

## Konkrete Werkstattaufgabe
Erzeuge dieselbe MIDI-Tonhöhe mit zwei funktional verschiedenen Schreibungen. Erkläre, welche im gegebenen Akkord passender ist.

## Codex-Akzeptanz und Gegenprüfung
Test: Pitch-Class beider Schreibungen identisch, diatonische Stufen verschieden; Transposition bleibt korrekt spelled.

## Grenzen der Aussage und Quellenprüfauftrag
Der Abschnitt ist **eigenständig formuliertes STEPS-Arbeitswissen**, keine Abschrift der genannten Literatur. Die Quellenanker stützen den beschriebenen Themenbereich; sie sind nicht als Einzelseitenbeleg für jede kreative Empfehlung zu lesen. Vor `reviewed` sind Fachlektüre, genaue Fundstelle (falls für Claim nötig), maschinelle Reproduktion und musikalisches Hören zu ergänzen.
