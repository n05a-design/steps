# KI-übergreifender Dokumentations- und Fortsetzungsvertrag – STEPS

**Geltung:** dauerhaft für alle Agenten, Menschen und Tools, unabhängig von Modell, Konto, Tokenkontingent, Editor oder Betriebssystem. **Steuerndes Projekt:** STEPS, **nicht** Glide. Regeln dieser Datei ergänzen die bestehenden `AGENTS.md`, `SKILL.md`, `docs/operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md` und Git-/Rechte-Gates; sie ersetzen sie nicht.

## 1. Was zwingend dauerhaft dokumentiert wird

Jeder fachlich relevante Output: (a) neue und frühere Nutzerentscheidungen und Änderungsaufträge, (b) Produkt-, UX-, Modul- und Architekturvorschläge, (c) Analysen, technische Audits, allgemeine Zusammenfassungen, Vergleiche und Optionen, (d) Recherche, Konkurrenten-/Markt-/Musiktheoriefunde einschließlich Negativbefunde, (e) Dateiindizes, Hashvergleiche, Migrations-/Lizenz-/Quellanalysen, (f) Implementierungen, Code-Diffs, Commit-/PR-IDs und revertierte Versuche, (g) Tests mit genauen Methoden, Logs, Skips, Fehlern und Performance-Budgets, (h) Skizzen, Screenshots, Diagramme, UI-/Brandingentscheidungen und Visualisierungen, (i) erstellte/überarbeitete Prompts und Skills, (j) noch offene Entscheidungen und verworfene Alternativen, (k) KI-Zusammenfassungen und Übergaben, auch aus der Vergangenheit. **Auch eine allgemeine Antwort ohne Dateiedit kann ein dauerhaft relevantes Ergebnis sein.** Dann mit Datum, Themenbezug, Erkenntnissen, Quelle, Unsicherheit und nächster Aktion ins Ergebnisregister/Projektlog aufnehmen.

Nicht erforderlich ist die Speicherung privater Modellgedankengänge oder jeder Chat-Floskel. Vollständigkeit bedeutet **Erhalt jedes fachlichen Ergebnisses** und seiner Quellen, nicht unkontrollierte Übernahme vertraulicher oder lizenzgeschützter Rohdaten.

## 2. Dokumentautorisierung und Schutz vor konkurrierenden Wahrheitsquellen

- Gegenwartsdarstellung: vorhandene kanonische Projektübersicht und Architektur-/Produkt-ADRs; neue Audits verlinken sie und schlagen **präzise Änderungen** vor.
- Vergangenheitsnachweise: unveränderte historische Originaldateien/Reports/Chat-Exporte, soweit rechtlich zulässig; Metadaten und Prüfsumme auch bei lokal gehaltenen Dateien.
- Sitzungs-/Arbeitsnachweise: `docs/audit/YYYY-MM-DD/<session-id>/` nach Review. Vor Freigabe externer lokaler Ordner `STEPS_AUDIT_OUTPUT_<timestamp>` neben dem Repository.
- Register: konsolidierbarer, maschinenlesbarer **Output-/Quellen-/Entscheidungsindex**; gleiche Version/gleicher Hash darf verlinkt statt kopiert werden.
- In der Read-only-Auditphase keine existierenden Dateien, `AGENTS.md`, Git-Metadaten, Produktcode, Daten, Schriften, Screenshots oder historische Berichte ändern. Read-only **der Produktquelle** schließt das Schreiben neu erzeugter Auditoutputs in einem *ausdrücklich eigenen* Ordner nicht aus.
- Bei dokumentationsbasiertem Integrationsauftrag: nur geprüfte, sichere Berichte in STEPS-Branch übernehmen, Link-/Schema-/Rechteprüfung und PR. Keine automatische Veröffentlichung oder Bearbeitung der ursprünglichen Glide-App.

## 3. Ausführungs- und Nachweisstatus

Separate Spalten: `claim_status` (`verified`, `reported`, `proposal`, `unknown`, `contradicted`, `superseded`), `implementation_status` (`planned`, `in_progress`, `implemented`, `reverted`, `blocked`), `test_status` (`PASS`, `FAIL`, `SKIP`, `NOT_RUN`, `BLOCKED`, `NOT_APPLICABLE`), `source_coverage` (`FULL`, `PARTIAL`, `METADATA_ONLY`, `NOT_REVIEWED`, `BLOCKED`). Kein Umcodieren von Rot/Skip in Grün. Git-Commit und Testumgebung für jeden tatsächlichen Pass.

Die Zustände sind **unabhängig**: Eine Architekturidee kann gut dokumentiert und trotzdem nicht implementiert sein; eine implementierte Funktion kann getestet, aber noch nicht freigegeben sein; eine erfasste PDF-Datei kann nur `METADATA_ONLY` haben.

## 4. Minimaler Sitzungsvertrag (immer)

**Vor Beginn:** Workspaceroot, `git rev-parse HEAD`, Branch/Status/Remote, aktive parallele Agenten, bestehende `STATE.json`-/Handover-/Outputregister, letzte Decision-IDs, konkrete Arbeitsaufgabe und Rechtescope lesen. Jede Quellenbearbeitung trägt SHA/Hash/Seitengrenze und Methode. Auch historische Analyseberichte lesen und deren unveränderte Erkenntnisse wiederverwenden, wenn Snapshot/Hash identisch sind.

**Währenddessen:** nach jeder substanziellen Analyse, Entscheidung, Dateiänderung oder Testserie ein dateibasiertes Ergebnis sichern, den Registereintrag nachführen und die offenen Abdeckungsgrenzen notieren. Vollständige bekannte Befunde auch bei abgebrochener/fehlgeschlagener Arbeit hinterlassen. Keine erfundenen Tests oder Zeitprognosen.

**Vor Abschluss oder Kontextlimit:** `STATE.json`, `NEXT_SESSION_HANDOVER.md`, `SESSION_LOG.md`, `OUTPUT_REGISTER.csv`, `SOURCE_COVERAGE.csv`, `DECISIONS_AND_QUESTIONS.csv` aktualisieren. Eindeutige nächste Datei/ID, exaktes Kommando, Blocker und unveränderte Basis referenzieren; neue Session darf das gesamte ursprüngliche Chatprotokoll nicht benötigen.

## 5. Erforderliche maschinenlesbare Registerfelder

**OUTPUT_REGISTER.csv:** `artifact_id,created_at,producer_tool,producer_model_or_account,session_id,artifact_type,project,repo_path_or_private_uri,source_ids,base_repo_sha,artifact_sha256,claim_status,implementation_status,test_status,coverage_status,canonical_ref,supersedes,privacy_class,license_status,summary,reviewer,notes`.

**SOURCE_COVERAGE.csv:** `source_id,path,repo_sha,blob_sha_or_sha256,medium,size_bytes,review_level,range_checked,method,parser,findings_ids,rights_status,blocked_reason,reviewed_at`.

**DECISIONS_AND_QUESTIONS.csv:** `decision_id,topic,proposal_or_owner_decision,status,owner_source,decision_date,source_refs,options_considered,reasons,related_requirements,revisit_trigger`.

**STATE.json:** `project,workspace_root,source_glide_path,steps_sha,glide_upstream_sha,baseline_manifest_sha,audit_mode,session_id,completed_phases,in_progress_file_ids,unreviewed_file_ids,coverage_counts,decisions_open,known_failures,last_verified_claim_id,outputs,changed_paths,tests,known_repo_drift,next_exact_steps`.

## 6. Modellwechsel und Arbeitsteilung

ChatGPT: Recherche-/Konsolidierungs-/Review-/Prompt-Arbeit; Gemini/Antigravity: lokale Code-/Datei-/Repo-Analyse und Umsetzung; Copilot VS Code: editornahe Implementierung; Claude/Fable: zusätzliche Analyse/Architektur-/UX-Gegenprobe. Diese Rollen sind **Empfehlungen, keine technischen Entitlements**. Quoten und Verfügbarkeit nicht als Projektzustand speichern. Modelle erhalten gleichen Einstieg und gegenseitige schriftliche Ergebnisse; sie arbeiten nur parallel bei getrennten Pfad-/Branch-Ownerships, ohne gemeinsame ungeschützte Arbeitskopie.

**Keine Selbstbestätigung:** Ein zweites KI-Modell ist nicht automatisch unabhängige QA. Entscheidend sind getrennte Quellen, ausführbare Tests, Hash-Nachweise und menschliche Review.

## 7. Historischer Rückstand – Nachdokumentation ohne Erfindungen

1. V1-/V2-/V3-/V4-/V5-Projektpakete, Reporte, 29+ Fachprompts, sechs Originalquellen, W-/G-/K-/N-/REQ-Register, frühere Test-/CI-Läufe und neue Glide-Bestandsaufnahme katalogisieren.
2. `artifact_id` pro eigenständigem Dokument oder Ergebnis, `source_id` pro Ursprungsquelle; mehrere Kopien gleicher Bytes mit `duplicate_of`, unterschiedliche Editionen mit `supersedes` verknüpfen.
3. Für nicht mehr auffindbare alte Chat-Ausgaben `NOT_AVAILABLE` mit ermitteltem Datum/Thema/Fundort, nicht mit phantasiertem Inhalt erfassen.
4. Fachliche unique Claims aus alten Fassungen vollständig in `HISTORY_CROSSWALK.csv` referenzieren; keine originale Analyse löschen, auch wenn die aktuelle Entscheidung ihr widerspricht.
5. Nach Abschluss jeder Iteration neue Erkenntnisse in *bestehende kanonische* Projekt-, Design-/Architektur-/Modul-/QA-Dokumente als gezieltes reviewed Diff vorschlagen; alle alten Register-IDs bleiben auflösbar.

## 8. Sicherheit und Lizenz

Niemals Credentials oder private Nutzerdaten in öffentliche Register/Logs. Keine fremden Volltexte, PDFs, Media/Artwork oder sonstiges Drittmaterial ungeprüft mit neuen KI-Konten teilen oder ins öffentliche Git kopieren. `MPL-2.0` der Software gilt nicht automatisch für fremde Assets. Eine lokale Pfadangabe mit privat wirkendem Namen in öffentlichen Berichten auf abstrahierte Repository-relative Pfade reduzieren; den exakten Windows-Pfad nur in **lokalen** Start-/Übergabedokumenten verwenden.

## 9. Akzeptanztest

Ein unbeteiligtes Modell kann allein aus `AGENTS.md`, kanonischer Overview, diesem Protokoll, `STATE.json`, `NEXT_SESSION_HANDOVER.md`, Registern, Quell-SHAs und referenzierten Dateien **nachvollziehen**, warum die letzte Entscheidung getroffen wurde, welche Analysen bereits durchgeführt wurden, welche Quellen nur inventarisiert wurden, welche Tests tatsächlich liefen und was als nächstes exakt ansteht. Fehlende Dokumente => kein vollständiges Handover.
