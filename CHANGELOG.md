# Änderungsprotokoll

## Unreleased – Python-Kern

- Tonhöhen, Intervalle, Akkordauflösung, Stufenparser und Stimmführung sind als Python-Schnittstellen verfügbar.
- Dur- und Moll-Aliasse mit `M` und `m` werden unterschieden. Unlösbare Voicing-Vorgaben melden einen Fehler.
- App-Adapter und Lernmaterial verwenden dieselbe kuratierte Progressionsdatei.
- Der [Implementierungsstand](docs/IMPLEMENTATION.md) und die [generierte API-Referenz](docs/theory/API.md) beschreiben den Entwicklungsstand und die verfügbaren Funktionen.

## Frühere Architekturvorbereitung

- Zielstruktur für App, Domäne, Wissensbasis, Forschung, Design, Entscheidungen und Tests beschrieben.
- Konservative, auditierbare Migration vorbereitet; **keine Aussage über fertigen App-Code**.
- Historische Wissensbibliothek wird als Legacy-Facharchiv abgegrenzt.

> Dieser Abschnitt dokumentiert die frühere Strukturvorbereitung.
