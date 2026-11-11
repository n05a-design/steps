# STEPS – PROG-021 Historical Reconciliation & Concept Preservation (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** RECONCILED & CANONICALLY RESOLVED (Gate 2 Passed)  
**Autor:** Leitender Musiktheorie-Analyst & Knowledge Architect  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil II  

---

## 1. Sachverhalt & Historische Befundlage

Im Rahmen der externen Plausibilitätskontrolle wurde auf eine historische Diskrepanz bei der Akkordprogression `PROG-021` hingewiesen:
- **Phase 4.14 Commit `d7d7f1e`:**
  - Titel: *Neo-Soul Rootless Minor Cycle*
  - Stufen: `i^9 - iv^9 - bVII^9 - III^maj9`
  - Akkorde: `Em9 – Am9 – D9 – Gmaj9`
- **Phase 4.9 bis 4.13 sowie Phase 4.15 und 4.16:**
  - Titel: *Neo-Soul Rootless Minor Cycle*
  - Stufen: `i^9 - iv^9 - bVI^maj9 - V^7(b9)`
  - Akkorde: `Dm9 – Gm9 – Bbmaj9 – A7(b9)`

Diese beiden harmonischen Strukturen sind musikalisch grundverschieden und dürfen nicht unreflektiert aufeinander abgebildet werden.

---

## 2. Detaillierte Chronologie & Ursachenanalyse

| Phase / Commit | Dokumentierter Zustand | Harmonische Analyse | Befund / Ursache |
|---|---|---|---|
| **Phase 4.9 (20261111T0105)** | `Dm9 - Gm9 - Bbmaj9 - A7(b9)` | $i^9 - iv^9 - \text{bVI}^{\text{maj}9} - V^7(\text{b}9)$ in D-Moll | **Authentische Urfassung:** Klassischer Moll-Zyklus mit chromatischer Leitton-Auflösung von $A^7(\text{b}9)$ nach $Dm^9$. Korrespondiert 1:1 mit `REF-0069`. |
| **Phase 4.13 (`a4b87f6`)** | `Dm9 - Gm9 - Bbmaj9 - A7(b9)` | $i^9 - iv^9 - \text{bVI}^{\text{maj}9} - V^7(\text{b}9)$ in D-Moll | Unverändert beibehalten. |
| **Phase 4.14 (`d7d7f1e`)** | `Em9 - Am9 - D9 - Gmaj9` | $i^9 - iv^9 - \text{bVII}^9 - \text{III}^{\text{maj}9}$ in E-Moll / G-Dur | **Versehentliche Überschreibung:** Während der Konsolidierung von Progressionstabellen wurde ein vierstimmiger Quintfall-Zyklus fälschlich unter der ID `PROG-021` eingetragen. |
| **Phase 4.15 (`7cc8705`)** | `Dm9 - Gm9 - Bbmaj9 - A7(b9)` | $i^9 - iv^9 - \text{bVI}^{\text{maj}9} - V^7(\text{b}9)$ in D-Moll | **Korrektur:** Wiederherstellung der Urfassung gemäß `REQ-4.15-10`, um Konsistenz mit Golden Case `REF-0069` zu wahren. |
| **Phase 4.16 (`c4313ba`)** | `Dm9 - Gm9 - Bbmaj9 - A7(b9)` | $i^9 - iv^9 - \text{bVI}^{\text{maj}9} - V^7(\text{b}9)$ in D-Moll | Als kanonischer Identity-Lock v1.1.0 gesichert. |

---

## 3. Musikalische Gegenüberstellung der beiden Konzepte

### Konzept A: Authentisches `PROG-021` (Neo-Soul Minor Dominant Turnaround)
- **Akkordfolge:** `Dm9 – Gm9 – Bbmaj9 – A7(b9)`
- **Funktion:** Modale Kadenz mit echter funktionsharmonischer Dominante ($A^7(\text{b}9)$).
- **Stimmführung:** Die Terz ($C\sharp$) und Septime ($G$) der Dominante lösen sich streng in Grundton ($D$) und Quinte/Terz ($F$) des $Dm^9$ auf.
- **Didaktischer Fokus:** Einführung von Rootless-Voicings der rechten Hand über Bassnoten; Spannung und Entspannung im Contemporary R&B / Neo-Soul.
- **Referenzen:** Mulholland (2013), Pease (2003).

### Konzept B: Das in Phase 4.14 aufgetauchte Konzept (Circle of Fifths Soul Cycle)
- **Akkordfolge:** `Em9 – Am9 – D9 – Gmaj9`
- **Funktion:** Reine Quintfallkette: $Em^9 \rightarrow Am^9 \rightarrow D^9 \rightarrow G^{\text{maj}9}$ (Dorian/Aeolian nach Dur-Tonika).
- **Charakter:** Sehr verbreiteter Lo-Fi- und Jazz-Funk-Loop (bekannt u. a. aus Modal-Jazz-Standards und 90er-Jahre Neo-Soul-Produktionen).
- **Eigenständigkeit:** Stellt ein vollständig eigenständiges musikalisches Werkzeug dar, das keinesfalls verloren gehen darf.

---

## 4. Verbindliche Phase-4.17 Lösung & Verankerung

Gemäß Regel 2 (*Preservation-first*) wird weder die historische Urfassung überschrieben noch die musikalisch wertvolle Phase-4.14-Variante verworfen:

1. **`PROG-021` bleibt unverändert die kanonische Urfassung:**
   - ID: `PROG-021`
   - Titel: `Neo-Soul Rootless Minor Cycle`
   - Stufen: `i^9 - iv^9 - bVI^maj9 - V^7(b9)`
   - Akkorde: `Dm9 - Gm9 - Bbmaj9 - A7(b9)`
   - Bindung an `REF-0069` bleibt 100 % stabil und verifiziert.
2. **Die Phase-4.14-Variante erhält die freie neue kanonische ID `PROG-028`:**
   - ID: `PROG-028`
   - Titel: `Circle of Fifths Soul Cycle`
   - Stufen: `i^9 - iv^9 - bVII^9 - III^maj9`
   - Akkorde: `Em9 - Am9 - D9 - Gmaj9`
   - Genre: `Neo-Soul, Jazz-Funk, Contemporary R&B`
   - Quellen: `Mulholland (2013), Levine (1995)`
   - In `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md` als Zeile 28 ergänzt.
3. **Auswirkungen auf den Identity-Lock:**
   - Der Identity-Lock wird deterministisch auf **28 Progressionen** erweitert (`PROG-001` bis `PROG-028`).
   - Alle 28 Progressionen sind in `REFERENCE_IDENTITY_BASELINE.json` mit SHA-256 Hashes versiegelt.
