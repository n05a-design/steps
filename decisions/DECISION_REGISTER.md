# Steps – neues Entscheidungsregister (nicht unberechtigt beschlossen)


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

Die historische Entscheidungsüberlieferung von Glide D01–D77 bleibt im originalen Glide-Repo und in den Hochladungen. Steps trifft keine automatischen Produktentscheidungen. Jeder neue Entscheidungsdatensatz erhält `ADR-ID`, Status `proposed/accepted/rejected/superseded`, Datum, Owner, Quellbelege, Alternativen, Trade-offs, Impact, Tests, Rücknahmeplan.

| ID | Status | Entscheidungsthema | Empfohlene Richtung, ohne Ownerfreigabe |
|---|---|---|---|
| ADR-001 | proposed | Zwei Fenster | ein Root, zwei Panes; separater Modal-/Inspector nur bei Bedarf |
| ADR-002 | proposed | Vision und MVP Chords/Drums | Chords zuerst im testbaren Kern; Drums explizit nachfolgenden Meilenstein |
| ADR-003 | proposed | Glide-Code-Quelle | lokaler 3.53.0-Stand nur nach vollständigem Commit/Backup und QA |
| ADR-004 | proposed | License/Brand | MPL für eigene kompatible Dateien; Fremdassets einzeln prüfen, eigenes Steps-Logo |
| ADR-005 | proposed | Fachmodell | Pitch-Class vs Spelling, Harmonic Interpretation als eigenständige Objekte |
| ADR-006 | proposed | Datenhaltung | JSON + Schema + atomarer Writer für MVP; DB erst nach gemessenem Bedarf |
| ADR-007 | proposed | Audio/MIDI | Ports zuerst, Backend nach Plattform-/Lizenzbenchmark |
| ADR-008 | proposed | KI-Skill | Router + indexierte Originalreferenzen + Claim-Registry, keine Volltext-Promptkopie |
| ADR-009 | proposed | Historische 21/39-Verzeichnisse | zunächst beibehalten, Alias-/Mergeentscheidung nach Inhaltsaudit |
| ADR-010 | proposed | Public-Repository-Medien | sofort Rechts-/History-Audit, keine neuen Fremd-Bytes pushen |

**Abgleich:** `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` für ältere W- und G-Register sowie aktuelle `docs/project/CONFLICTS_AND_GAPS.md` für Delta-Befunde. Eine Entscheidung löst einen Konflikt erst nach `accepted` samt nachprüfbarem Ownerhinweis und aktualisierten Verweisen auf.
