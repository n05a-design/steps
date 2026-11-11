# Aktuelle Ergänzungen, Widersprüche und offene Prüfgegenstände (V6)

**Evidenz:** `GITHUB` = am 10.11.2026 direkt über Repository/CI bestätigt; `UPLOAD` = vom Nutzer übergeben, nicht unabhängig vollständig repliziert; `DECISION` = heutige ausdrückliche Nutzeranweisung; `HISTORICAL` = früherer datierter Bericht; `OPEN` = technische/inhaltliche Frage. Nicht stillschweigend in bestehende W-01..W-40, G-01..G-34, K-, N-, REQ- oder ADR-Nummern umnummerieren.

| Kennung | Befund / Widerspruch | Status | Folgeschritt |
|---|---|---|---|
| V6-01 | Ältere Übergabe „in Glide weiterentwickeln“ gegen neue Entscheidung: **STEPS** ist der aktive Workspace; `src/glide-v3.53/` die integrierte Ausgangsbasis | DECISION | frühere Aufforderung nicht mehr direkt ausführen, neue Startdatei nutzen |
| V6-02 | Glide vor PR #75 teils noch `3.50.7`/„lokaler 3.53 Kandidat“. Tatsächlich Upstream `main` **`9e767bea5e21063466a28ac3a679406484ad5d5f`**, App `3.53.0` | GITHUB | aktuelle Einstiegshilfen per datiertem Nachtrag korrigieren, Historie nicht umschreiben |
| V6-03 | Früherer STEPS-Stand `75329fef` / 1.931 Files vs. aktueller `main` **`1fc07e230dc6a2fe92fd6662da43e332d596b376`** / 3.768 Files | GITHUB | Stichtag/Nenner unterscheiden, Delta-Manifest erstellen |
| V6-04 | Glide 3.53 GitHub Hauptprüfung und macOS-Paket erfolgreich vs. frühere Warnung „CI in progress“ | GITHUB | Run `42822511966`, `42822511486`, genaue Skips separat; STEPS-QA unabhängig |
| V6-05 | Ältere Reviews prüften nur einzelne `app.pyw`; jetzt enthält STEPS `src/glide-v3.53/` ~1.580 Pfade | GITHUB | vollständiger Upstream/Downstream Source-/Asset-/Tests-/Import-Vergleich |
| V6-06 | Antigravity hat bereits `Glide_Projektbestandsaufnahme_2026-11-10.md` erstellt; ältere Prompts übergehen es | UPLOAD | als Vorbefund/Source-ID dokumentieren, Delta statt Doppelarbeit |
| V6-07 | Bisher keine durchgehende Pflicht, **alle bisherigen und neuen allgemeinen KI-Ausgaben** projektintern zu bewahren | DECISION | modellübergreifendes Output-/History-/Context-Register bindend machen |
| V6-08 | Zwei „Fenster“ versus eine Zwei-Bereiche-Shell/optional Inspector | OPEN | echte Tk-Topologie und Owner-Acceptance per ADR, nie unkontrolliert zweites Tk-Root |
| V6-09 | `src/steps-0.00/` existiert, Strukturvalidator erwartet `src/steps/` – alte Struktur-CI fehlgeschlagen | GITHUB/HISTORICAL | Python-Paketpfad-ADR und expliziter Steps-CI-Neutest |
| V6-10 | Original Glide-Bestandsaufnahme nennt sieben geänderte Docs und fünf Konfliktarten im separaten Glide-Checkout; STEPS enthält aber eingebettete Quelle | UPLOAD | nicht automatisch als aktuelles lokales STEPS-Delta ausgeben; Hash- und Pfadvergleich |
| V6-11 | Glide-Modulregister mit 94/147/25/311 ist **kein isoliertes Shared-SDK** | GITHUB/UPLOAD | Reuse-Matrix, import-/datenisolierte Pilotmodule und je Consumer Testnachweise |
| V6-12 | Forschungsbibliothek viele tausend Git-Dateien; Source-/Rights-/Claim-Register und fachlicher Wissenskern nicht automatisch validiert | GITHUB/HISTORICAL | Rechte- und 3–5-Source-Pilot, getrennte bibliografische und inhaltliche Coverage |
| V6-13 | V1–V5/Auditberichte/Overlays und historische W/G/K/N/REQ-Inhalte überschneiden sich | OPEN | `derived_from`/`supersedes` und lossless Crosswalk, keine ungeprüfte Deduplikation |
| V6-14 | Glide-Referenz kann eigene `.github`, `AGENTS.md`, Tests enthalten, die für Steps nicht automatisch Top-Level-gültig sind | OPEN | Scope- und Herkunftsbezug für verschachtelte Anweisungen/Workflows festlegen |
| V6-15 | MPL-2.0 der Software ≠ Publikations-/KI-Verarbeitungsrechte für fremde PDFs, Webcaches, Medien und Fonts | GITHUB/HISTORICAL | separate Asset-/Rights-/Git-History-Triage |
| V6-16 | Mehrere aktive Projektdarstellungen enthalten ältere SHA-Fakten; neue Parallel-Overview erzeugt neue Konflikte | GITHUB/HISTORICAL | nur neue datierte Delta-Dokumente und konkrete Patchvorschläge an aktuellen Kanon |

## Analysedokument Glide – konkret bekannte Nachträge

Die vom Nutzer beigefügte Bestandsaufnahme nennt unter anderem: veraltete Verweise auf noch fehlende `Glide_Entwicklungsplan §21.84`/`Glide_Analyse §13.32`, fehlende Entscheidungen D74–D77 im aktiven `ARBEITSRICHTUNG`-Register, D60- statt D77-Fonttabellen, Drift zwischen `CLAUDE.md` und `AGENTS.md`, sowie historische Falschaussage „Steps-Repository existiert nicht“. Diese Funde sind **dokumentierte Prüfhinweise** und müssen gegen die konkrete eingebettete STEPS-Kopie verifiziert werden; nicht blind ins separate Glide-Repository schreiben. Ältere Reviewbehauptung fehlender macOS-/Linux-Prüfungen ist mit der aktuellen erfolgreichen GitHub-Hauptprüfung neu abzugleichen.

## Nicht behauptet

Keine lokale STEPS-Git-Ausführung in dieser Unterhaltung, kein 3.768-Datei-Volltextreview, kein Code- oder UI-Refactoring, keine Steps-App-QA, kein rechtliches Asset-Clearance-Ergebnis, kein GitHub-Push. Die vollständige frühere Ergebnisliste der KI-Konten ist erst nach lokaler Inventur als Coverage nachweisbar.
