# Projektentscheidungen – neue Arbeitslogik, nicht rückwirkend beschlossene ADRs

## Statusmodell

`proposed` / `accepted` / `rejected` / `superseded` / `needs_evidence`. Jede Entscheidung führt `ID`, `Owner`, `Datum`, `Version/SHA`, Ausgangsoptionen, Auswirkungen auf Glide/Steps, wissenschaftliche Quelle und Testlink. Frühere 26 DEC-IDs bleiben historisch bestehen; neue IDs mit Präfix `STEP-ADR` dürfen nicht deren IDs überschreiben.

| ID | Entscheidung / Alternativen | Status | Freigabegate |
|---|---|---|---|
| STEP-ADR-01 | Steps eigenständig, nicht Glide in Musik-App umbenennen | proposed (Ziel des Nutzers, Architekturvertrag noch nicht final) | PRD + Datentrennung |
| STEP-ADR-02 | zwei austauschbare Inhalts-Hosts als Shell-Vertrag | proposed | Ist-Widgettopologie und Erhaltungsbaseline |
| STEP-ADR-03 | Shared-Kit erst nach zwei realen Verbrauchern | proposed | 2-Consumer-Spike und gemessene Integrationskosten |
| STEP-ADR-04 | M1 chord-only Engineering-Gate / M2 chord+drum Produkt-MVP | proposed | Produkt-Owner PRD |
| STEP-ADR-05 | Timeline: Events/PPQ/Tempo/Meter/Groove | needs_evidence | MIDI-/Drum-Goldentests |
| STEP-ADR-06 | Playback intern vs MIDI-Export vs externe DAW | needs_evidence | Nutzeraufgaben/Latenz/Lizenzen |
| STEP-ADR-07 | enharmonische Schreibweise, DE/EN, Oktaven, Kontext | needs_evidence | Musik-Fachreview |
| STEP-ADR-08 | eigenes Steps-Projektformat + migrationsfähige Schema-Version | proposed | Save-/Restore-Negativtests |
| STEP-ADR-09 | Harmony-Skill: kuratierter Retrieval-Pilot statt Volltext-Crawl | proposed | Rights, Claims, Eval |
| STEP-ADR-10 | Plattformen, Accessibility, reale native Builds | needs_evidence | QA-/Produkt-Gate |
| STEP-ADR-11 | Repo-Governance/PR-only und CI-Required-Checks | proposed | Owner-Einstellungen und PR-Durchstich |
| STEP-ADR-12 | endgültige Modul-Distribution (eigenes Repo/PyPI/Subtree/Vendor) | needs_evidence | zwei echte API-Konsumenten |

**Wichtig:** „proposed“ und „needs_evidence“ erteilen keine Implementierungs- oder Releasefreigabe. Keine unbemerkte Produktentscheidung auf Basis des jeweils verfügbaren KI-Modells treffen.
