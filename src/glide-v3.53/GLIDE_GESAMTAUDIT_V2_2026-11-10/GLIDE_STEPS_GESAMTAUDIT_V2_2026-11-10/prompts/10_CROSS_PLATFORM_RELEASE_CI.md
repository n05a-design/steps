# CI, native Plattformmatrix, Packaging, Lizenz-/SBOM-Nachweise

**Prompt-ID:** `10_CROSS_PLATFORM_RELEASE_CI` · **Arbeitsart:** ANALYSE mit Test-/Buildplan; Ausführung nur wo Umgebung und Freigabe vorhanden · **Roadmap:** P10

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Glide `.github/workflows/`, `docs/05_QA_TESTPLAN.md`, `docs/07_QA_BERICHT.md`, Packaging/requirements, Steps `.github/workflows/structure-check.yml`, `pyproject.toml`, `tests/test_structure.py`.

## Fachlich konkreter Arbeitsauftrag

Markiere konkrete Prüfungslücken des Steps-Strukturworkflows: Musiktheorie, Domain-Import, MIDI, Datensicherheit, UI/Accessibility, native Packaging. Entwerfe Zielworkflows mit schneller reiner Domain-Suite, Parser-/Security-Kontrakten, Integrationstests, echten Tk-UI-Suites, Build-/SBOM-/Provenienzchecks und Human-Approval. Für Windows, macOS und Linux Python/Tcl/Tk-Versionen, Font-/Icon-/Materialrechte und Signierung/Zertifikate getrennt erfassen. Baue keine unautorisierte Releasepipeline, die heimlich Netzwerk/Accountabhängigkeiten in Offline-App einführt. Lerne aus Glide-Tests mit 130/131 Windows-Schritten: ein Erfolg mit Skip darf nicht zu 'vollständig grün' verkürzt werden. Kein Rückschluss von Mac-Paketerstellung auf Aqua-Focus/Screenreader/Geometrie. CI-Workflow-Lauf sollte die Quell-SHA, Artefakt-Hashes, Testdatenorte und `NOT_RUN`-Spezifikation exportieren.

## Reproduzierbare Abnahmen und Gegenproben

Schema-/Source-Integrity, MIDI-Roundtrip, Tk UI im offiziellen Desktopmodus, Font-Glyphfallback, Keyboard, Theme, Window geometry, Install/Start offline und signed/unsigned Unterschiede; kontrollierter Fail der falschen App-ID und fehlender OS-Runtime. Historische rote Glide-Tests nach Fehlerklassifizierung erhalten.

## Ergebnis und Übergabeformat

`CI_TARGET_MATRIX.csv`, `WINDOWS_MAC_LINUX_GATES.md`, `PACKAGING_CONTRACT.md`, `ARTIFACT_MANIFEST_SCHEMA.json`, `SOURCE_TO_BUILD_PROVENANCE.md`; offene echte Hardwareprüfungen getrennt benennen.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Keinen Release/Tag/Signierlauf ausführen ohne Secrets-/Plattformautorisation und menschliche Freigabe. Kein Testfall-Entfernen, um CI grün zu bekommen.
