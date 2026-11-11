# STEPS – Quellen-, Literatur- & Rechtecharta (Phase F Audit)

**Dokumenttyp:** SYSTEMATISCHES QUELLENREGISTER & RECHTE-AUDIT  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** `knowledge/sources/`, Zitierstandard, Evidenzhierarchie & Urheberrecht (P0-1)  
**Status:** `AUDITED & VERIFIED COMPLIANT`  

---

## 1. Evidenzhierarchie & Quellenklassifikation

Zur Sicherung höchster wissenschaftlicher und didaktischer Zuverlässigkeit werden alle in STEPS verwendeten Fachquellen in fünf Evidenzklassen unterteilt:

| Evidenzklasse | Bezeichnung | Beschreibung & Relevanz | Anzahl im Projekt |
|:---:|:---|:---|:---:|
| **E1** | Primäre wissenschaftliche Fachwerke & Standards | Mathematisch/akustische Standardwerke, Peer-Reviewed Papers, offizielle technische Spezifikationen (z. B. MMA MIDI 1.0, W3C MusicXML 4.0, Müller FMP, Friberg/Sundström 2002, Tymoczko 2011). | 46 verifizierte Claims |
| **E2** | Etablierte akademische Lehrbücher | Standardwerke der Musikhochschulausbildung (z. B. Kostka & Payne *Tonal Harmony*, Mark Levine *Jazz Theory Book*, Diether de la Motte *Harmonielehre*, Persichetti *Twentieth-Century Harmony*). | 20 verifizierte Claims |
| **E3** | Fachlich geprüfte Musikpraxis & Curricula | Verifizierte Ausbildungsunterlagen, Fachanalysen und Lehrmaterialien (z. B. New Jazz / Oliver Prehn, Berklee College of Music Handbücher, Mauleón *Salsa Guidebook*). | 344 Vollprüfungen |
| **E4** | Externe Recherche-Artefakte & Community-Archive | Historische Tutorials, Blog-Dumps (z. B. Ableton Blog Archiv V6.6), Hersteller-Handbücher. Ausschließlich als Metadaten und Kontextbelege geführt. | 1.525 Metadaten-Einträge |
| **E5** | Ungeprüfte Webquellen | Forenbeiträge, anonyme Tabs, ungeprüfte KI-Synthesen. **Im STEPS-Fachbestand strikt unzulässig.** | 0 Einträge |

---

## 2. Kanonisches Verzeichnis der Hauptreferenzwerke

1. **Akustik & Signalverarbeitung:**
   - Müller, Meinard (2015): *Fundamentals of Music Processing*. Springer Verlag. (M01, M11)
   - International Organization for Standardization (ISO 16:1975): *Standard tuning frequency (Standard music pitch)*. (M01)
   - MIDI Manufacturers Association (1996): *The Complete MIDI 1.0 Detailed Specification*. MMA. (M08, M11)

2. **Klassische Harmonielehre & Kontrapunkt:**
   - Kostka, Stefan / Payne, Dorothy / Almén, Byron (2013): *Tonal Harmony with an Introduction to Twentieth-Century Music*. 7th Edition, McGraw-Hill. (M02, M04, M05, M06)
   - de la Motte, Diether (1976): *Harmonielehre*. Bärenreiter Verlag. (M02, M05, M06)
   - Aldwell, Edward / Schachter, Carl (1989): *Harmony and Voice Leading*. Harcourt Brace Jovanovich. (M02, M05, M06)
   - Fux, Johann Joseph (1725): *Gradus ad Parnassum*. (M06)

3. **Jazz-, Pop- & Modale Harmonik:**
   - Levine, Mark (1995): *The Jazz Theory Book*. Sher Music Co. (M03, M04, M05, M10)
   - Tymoczko, Dmitri (2011): *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*. Oxford University Press. (M05, M06)
   - Persichetti, Vincent (1961): *Twentieth-Century Harmony: Creative Aspects and Practice*. W. W. Norton & Company. (M03, M04, M05)
   - Prehn, Oliver (2017): *Scales with 4 Smart Tools & Four Scale Families*. New Jazz System. (M03, M04)

4. **Rhythmik, Timing & Genre-Traditionen:**
   - Friberg, Anders / Sundström, Andreas (2002): *Swing Ratios and Ensemble Timing in Jazz Performance: Evidence for a Common Explanation*. Journal of the Acoustical Society of America. (M07)
   - Roger Linn Design (1994): *Akai MPC 3000 Operator's Manual & Timing Engine Notes*. (M07, M08)
   - Mauleón, Rebeca (1993): *Salsa Guidebook: For Piano & Ensemble*. Sher Music Co. (M07, M08, M09, M10)
   - Peñalosa, David (2009): *The Clave Matrix: Afro-Cuban Rhythm: Its Principles and African Origins*. Bembe Books. (M07, M08)

---

## 3. Urheberrechtliche Trennung & P0-1 Konformität

In Übereinstimmung mit **AGENTS.md Regel 6** und **OA-0001** gilt für das STEPS-Repository:
1. **Keine urheberrechtlich geschützten Volltexte:** Fremde Lehrbücher, PDF-Bände (z. B. *MakingMusic.pdf*) oder Notensammlungen dürfen nicht in neuen Commits veröffentlicht oder ungeprüft reproduziert werden.
2. **Eigenständige wissenschaftliche Synthese:** STEPS dokumentiert mathematische Formeln, Halbtonvektoren, Tick-Raster, Notenorthographie und prägnante didaktische Zusammenfassungen unter Angabe präziser Zitate (Autor, Jahr, Kapitel, Seite).
3. **Schutz der historischen Git-Historie:** Urheberrechtlich sensible Alt-Dateien im Branch-Verlauf werden im Rahmen von OA-0001 (Handlungsoption A oder C) durch den Project Owner final ratifiziert.
