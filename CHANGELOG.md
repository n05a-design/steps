# Änderungsprotokoll

## Unreleased – Python-Kern

- **Verhaltensänderung:** `NoteSpelling.transpose_diatonic` löst bei Stufen- und Halbtonwerten, die kein Intervall bilden, `InvalidAlterationError` aus, statt still die Oktave zu verschieben (zuvor C4 `(0, 11)` → Cb5). Gültige Intervalle sind unverändert.
- **Verhaltensänderung:** `knowledge/research/run_golden_test_suite.py` schreibt ohne Argumente keine Dateien mehr; `--output-dir` exportiert, `--update-baseline` erneuert die versionierten Berichte.
- Entscheidungen ADR-001, 003, 004, 006, 007 und 013–017 angenommen (v0.1 = Akkorde + MIDI-Export, Lizenz MPL-2.0/CC BY 4.0); siehe [Register](decisions/DECISION_REGISTER.md). Der MIDI-Export ist spezifiziert, aber noch nicht implementiert.
- Tonhöhen, Intervalle, Akkordauflösung, Stufenparser und Stimmführung sind als Python-Schnittstellen verfügbar.
- Dur- und Moll-Aliasse mit `M` und `m` werden unterschieden. Unlösbare Voicing-Vorgaben melden einen Fehler.
- App-Adapter und Lernmaterial verwenden dieselbe kuratierte Progressionsdatei.
- Logo und App-Symbol liegen als [Master](design/brand/README.md) im Repository. `app.brand` stellt sie der App zentral bereit, die Root-README zeigt das App-Symbol.
- Die Root-README ist als Projektseite neu gegliedert und erscheint auf der GitHub-Startseite. Die frühere `.github/README.md` heißt jetzt [`GITHUB_UND_CI.md`](.github/GITHUB_UND_CI.md).
- Der [Implementierungsstand](docs/IMPLEMENTATION.md) und die [generierte API-Referenz](docs/theory/API.md) beschreiben den Entwicklungsstand und die verfügbaren Funktionen.

## Frühere Architekturvorbereitung

- Zielstruktur für App, Domäne, Wissensbasis, Forschung, Design, Entscheidungen und Tests beschrieben.
- Konservative, auditierbare Migration vorbereitet; **keine Aussage über fertigen App-Code**.
- Historische Wissensbibliothek wird als Legacy-Facharchiv abgegrenzt.

> Dieser Abschnitt dokumentiert die frühere Strukturvorbereitung.
