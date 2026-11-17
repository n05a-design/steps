# ADR-015: Kernverträge – Intervalle über der Oktave, add2/add9, DROP2 bei 13-Akkorden, deutsche Notennamen

**Status:** accepted (Umsetzung offen)
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, schriftliche Spezifikationsentscheidung vom 17.11.2026; schließt drei der vier offenen Proben in [`API_VERTRAEGE.md`](../docs/theory/API_VERTRAEGE.md)

## Kontext
[`API_VERTRAEGE.md`](../docs/theory/API_VERTRAEGE.md) führt beobachtete, noch nicht beschlossene Verträge: `Cadd9` und `C7(#11)` liefern 2 und 6, `C9` liefert 14; DROP2 lässt bei `C13` die 13 (A) weg; `Cis` und `Es` werden in AUTO abgewiesen. Die vierte Probe (Ergebnisfelder der Stimmführungsanalyse) ist nicht Gegenstand dieses ADR.

## Entscheidung

### 1. Intervalle über der Oktave
- Intervallfunktion und Tonklasse werden strikt getrennt. Gespeichert wird der **unreduzierte** Halbtonabstand (`C9`: None = 14, `C7(#11)`: 18, `11` = 17); die Tonklasse wird abgeleitet: `(root_pc + offset) % 12`.
- Begründung: Nur so bleiben große Sekunde (2) und große None (14), `sus4` (5) und 11 (17), kleine Sekunde (1) und kleine None (13) unterscheidbar. Voicing- und Stimmführungsregeln brauchen den unreduzierten Wert.

### 2. `add2` und `add9`
- Als Tonklassenmenge `{0, 2, 4, 7}` identisch. Beide verweisen auf **einen** harmonischen Kernknoten (`MAJOR_TRIAD_ADD_9`, Intervalle `{0, 4, 7, 14}`).
- `add2` bleibt **Notationsalias** mit optionalem Voicing-Hinweis `preferred_register: close_cluster`, `add9` mit `open_tension`. Der Hinweis ist weich: Ein Voicing, das bei `add2` das D oktaviert, ist kein Fehler.
- Bestand: `add2` ist im Kern schon Alias von `add9` mit theoretischen Intervallen `(0, 4, 7, 14)` ([`chord.py`](../src/steps/theory/chord.py)); neu ist nur der Voicing-Hinweis.

### 3. DROP2 bei 13-Akkorden: Reduktion vor dem Drop
Ein vierstimmiges DROP2-Voicing eines 13-Akkords ist Jazzpraxis und darf **keinen Fehler** auslösen. Neue Transformationsregel `VOICING_REDUCTION_4_VOICE`, angewandt **vor** dem mechanischen DROP2 (zweitoberste Stimme eine Oktave tiefer):
- **Pflicht:** 3, ♭7 und 13. Die 13 fällt nie weg, sonst wird der Akkord zu C7 oder C9.
- **Vierte Stimme:** Standard 9 (rootless, z. B. E–A–B♭–D); mit Grundton (C–E–A–B♭), wenn kein Bass mitspielt.
- **Streichreihenfolge:** zuerst 11 (immer), dann 5, dann 1 zugunsten der 9.

### 4. Deutsche Notennamen ohne Akkordqualität
- `Cis`, `Es`, `As`, `Fis`, `Ges`, `Des`, `H` und `B` (= B♭) werden auch ohne Suffix als deutsche Namen erkannt (Dur-Dreiklang bzw. Einzelton im Melodie- oder Basskontext). Sonst scheitert jedes deutsche Leadsheet wie `| C | Am | Fis | H7 |`.
- **Einzige echte Kollision `B`:** Dokumentweite Umschaltung. Taucht im selben Dokument bzw. derselben Spur mindestens ein eindeutig deutscher Marker auf (`H`, `Hm`, `H7`, `Fis`, `Cis`, `Es`, `As`, `Des`, `Ges`), gilt `locale: de` (`B` = B♭, `H` = B). Ohne Marker bleibt `locale: en` (`B` = B).
- **Kleinschreibung:** In älterer deutscher Lehre bedeuten `cis`, `es` Moll. Unterstützung als konfigurierbare Option mit Warnung, nicht als Standard.
- Kuratierte Daten setzen DE/INT weiterhin ausdrücklich (bestehender Vorschlag in `API_VERTRAEGE.md`).

## Auswirkungen
- Code (eigene PRs mit Tests): unreduzierte Offsets für `add9`/`#11`-Pfade prüfen und angleichen; `VOICING_REDUCTION_4_VOICE` vor DROP2; dokumentweite Locale-Erkennung im Parser. Jede Änderung braucht Golden-Fälle und eine Gegenprobe am alten Verhalten.
- Daten: Tonklassen bleiben abgeleitet, daher keine Migration bestehender Pitch-Class-Felder.
- Rückfall: Die Locale-Umschaltung ist abschaltbar (`DE`/`INT` explizit setzen).

## Links
- [`docs/theory/API_VERTRAEGE.md`](../docs/theory/API_VERTRAEGE.md)
- [ADR-014](ADR-014-theorie-perspektiven-und-kontext.md) (Intervall- und Tonklassenfakten gehören zur Kernschicht)
