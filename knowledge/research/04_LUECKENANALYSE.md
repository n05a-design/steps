# STEPS – Vollständigkeits- & Lückenanalyse (Phase D Audit)

**Dokumenttyp:** SYSTEMATISCHE VOLLSTÄNDIGKEITS- & DEEP-RESEARCH-LÜCKENANALYSE  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Domänen M01 bis M12, Typologie A bis I, Schließungsstrategie  
**Status:** `AUDITED & STRATIFIED`  

---

## 1. Klassifikation der Lückentypologie (Typ A bis Typ I)

Um oberflächliche Pauschalurteile zu vermeiden, werden alle im Wissensbestand identifizierten Unvollständigkeiten nach neun disjunkten Fehler- und Lückentypen klassifiziert:

| Typ | Bezeichnung | Definition | Status im STEPS-Projekt |
|:---:|:---|:---|:---|
| **Typ A** | Fehlendes Thema | Ein musikalischer Standardbereich fehlt vollständig im Datenbestand. | *Beispiel:* Bebop-Skalen in M03; 32-Bar AABA Form in M09. |
| **Typ B** | Unvollständige Erklärung | Thema ist angelegt, aber unzureichend tief oder ohne Sonderfälle ausgeführt. | *Beispiel:* Alterierte Skala in M03 (Bezug zu $V^7(\text{alt})$ unvollständig formalisiert). |
| **Typ C** | Fehlende Quelle | Behauptung ohne zitierte Primär- oder Sekundärquelle. | *Beispiel:* Unbelegte Slang-Bezeichnungen in früheren Drum-Patterns (behoben in Phase 4.10). |
| **Typ D** | Fehlende Beziehung | Wissensobjekt ist isoliert und besitzt keine Relation zu Skala/Akkord/Genre. | *Beispiel:* Fehlende Kante zwischen Quartal-Voicings und Dorischem Modus. |
| **Typ E** | Fehlende technische Repräsentation | Konzept ist nur als Prosa beschrieben, nicht als maschinenlesbarer Vektor/JSON. | *Beispiel:* Walking Bass Voice Leading Regeln als imperative Python-Logik. |
| **Typ F** | Fehlendes Lernmaterial | Thema existiert als Theorie, besitzt aber keine didaktische Reduktion für Anfänger. | *Beispiel:* Drop-2 Voicings für kleine Hände (in P08 partiell gelöst). |
| **Typ G** | Fehlender Test | Musiktheoretische Invariante wird nicht durch automatisierten Test geprüft. | *Beispiel:* Zirkuläre Tymoczko-Metrik in Golden Tests (REF-0065 vorhanden, mehrstufige Permutationen fehlen). |
| **Typ H** | Widersprüchliche Darstellung | Gleiches Phänomen wird an zwei Stellen unterschiedlich definiert. | *Beispiel:* Header 27 vs. 28 Progressionen (in ERR-035 behoben). |
| **Typ I** | Ungenaue / ungeeignete Kategorisierung | Konzept ist einer falschen Domäne oder übergeordneten Klasse zugeordnet. | *Beispiel:* Voicings vermischt zwischen M04 (Akkorde) und M10 (Piano) (in Phase B entflochten). |

---

## 2. Detaillierte Lückenmatrix nach Wissensdomänen (M01 bis M12)

| Domäne | Identifizierte Lücke | Typ | Priorität | Fachliche Anforderung / Lösungsweg | Status & Blocker |
|:---:|:---|:---:|:---:|:---|:---|
| **M01** | Cent-Abweichungen historischer Stimmungen (Werckmeister, Mitteltönig) | Typ B | P3 | Formalisierung der Frequenzdifferenzen gegenüber 12-TET; mathematische Tabelle. | Für MVP unkritisch; Ausblick für MPE. |
| **M02** | Enharmonische Orthographie in modulierenden Kadenzen | Typ B | P1 | Regelwerk zur automatischen Wahl von $\sharp$ vs. $\flat$ basierend auf Quintenzirkel-Distanz. | Spezifiziert in Backlog; wartet auf ADR-005. |
| **M03** | Symmetrische Skalen (Halbton-Ganzton / Ganzton-Halbton) | Typ A | P1 | Intervallfolgen $[1, 2, 1, 2, 1, 2, 1, 2]$ und $[2, 1, 2, 1, 2, 1, 2, 1]$ als Skalenvektoren anlegen. | Spezifikation ausgearbeitet; Golden Cases erweiterbar. |
| **M04** | Quartal-Voicings (McCoy Tyner / "So What") | Typ A | P2 | Akkordaufbau aus reinen Quarten ($[0, 5, 10, 15, 20] \pmod{12}$); modale Eignung für Dorian. | Dokumentiert in M04-Forschung; Modul P20 Entwurf. |
| **M05** | Coltrane Changes (Symmetrische Großterz-Zyklen) | Typ B | P2 | PROG-016 existiert; formale Transformationsmatrix der 3 tonalen Zentren im Quintenzirkel. | Vollständig in PROG-016 spezifiziert. |
| **M06** | Kontrapunktische Bewegungsklassen (Motus rectus, contrarius, obliquus) | Typ E | P2 | Formaler Validator für zwei-/vierstimmigen Satz (`src/steps/progression/voice_leading.py`). | In OA-0021 verankert; Backlog-Task. |
| **M07** | Quintolen- und Septolen-Micro-Timing (J Dilla Feel) | Typ B | P2 | Erweiterung der 480 PPQ Arithmetik um 5er/7er Subdivisionen ($96 \text{ Ticks} \pm \Delta t$). | In REF-0047 (Septole) arithmetisch belegt. |
| **M08** | Lineares Drumming (Keine gleichzeitigen Gliedmaßen) | Typ A | P2 | Pattern-Validator, der Kollisionen auf demselben Tick verbietet ($\forall t: \sum \text{Hits}(t) \le 1$). | Konzeptionell vorbereitet für v0.2. |
| **M09** | Standard-Pop-Formen (32-Bar AABA, Verse-Pre-Chorus-Chorus) | Typ A | P1 | Formale Definition von Formblöcken mit typischer Taktlänge und Kadenzenverteilung. | Vorbereitet in Genre-Dossiers. |
| **M10** | Drop-3 Voicings am Klavier (Bass + Tenor + Alt + Sopran) | Typ A | P2 | Stimme 3 von oben fällt eine Oktave nach unten; Intervallanalyse und Handspannweiten-Check. | Konsistent zu Drop-2 (P08) erweiterbar. |
| **M11** | Variable PPQ-Skalierung (240 / 480 / 960 Ticks/Viertel) | Typ E | P1 | Unittest für zeitarithmetische Konvertierungen ohne Rundungsdrift. | Abgesichert in REF-0197/REF-0198. |
| **M12** | Formale DAG-Prüfung für Unterrichts-Voraussetzungen (Prerequisites) | Typ G | P1 | Graph-Prüfskript zur Erkennung zyklischer oder unbegründeter Lernsprünge im Klavierpfad. | Als Validierungsfunktion in `verify_reference_integrity.py` integrierbar. |

---

## 3. Maßnahmen zur Schließung priorisierter Lücken

### 3.1 Symmetrische Skalen (M03)
Die verminderte Skala (Octatonic Scale) besitzt zwei komplementäre Modi:
1. **Halbton-Ganzton (HTGT / Half-Whole):** Schrittmuster $[1, 2, 1, 2, 1, 2, 1, 2]$. Tonklassen auf C: $\{0, 1, 3, 4, 6, 7, 9, 10\}$. Einsatz: Über Dominantseptakkorden mit $b9$ und $\sharp 9$ ($C^7(b9,\sharp 9)$).
2. **Ganzton-Halbton (GTHT / Whole-Half):** Schrittmuster $[2, 1, 2, 1, 2, 1, 2, 1]$. Tonklassen auf C: $\{0, 2, 3, 5, 6, 8, 9, 11\}$. Einsatz: Über verminderten Septakkorden ($C^{\circ 7}$).

### 3.2 Quartal-Voicings (M04 / M10)
Quartal-Akkorde brechen mit der traditionellen Terzschichtung. Das klassische "So What"-Voicing über D-Dorisch besteht aus:
* Linke Hand: $D3 - G3 - C4$ (zwei reine Quarten: $5 + 5$ Halbtöne).
* Rechte Hand: $F4 - A4$ (eine große Terz: $4$ Halbtöne).
* Gesamtintervallik: $D - G - C - F - A$ (drei reine Quarten + eine große Terz = alle 5 Töne sind leitereigen in D-Dorisch).

---

## 4. Fazit des Lücken-Audits

Keine der identifizierten Forschungslücken blockiert die Implementierung des T-06 Theorie-Kerns oder des MVP v0.1. Alle hochpriorisierten Lücken (Typ A bis E) sind mit präzisen mathematischen Vektoren und Literaturverweisen hinterlegt und werden im Rahmen des kontinuierlichen Ausbaus in die Bibliothek integriert.
