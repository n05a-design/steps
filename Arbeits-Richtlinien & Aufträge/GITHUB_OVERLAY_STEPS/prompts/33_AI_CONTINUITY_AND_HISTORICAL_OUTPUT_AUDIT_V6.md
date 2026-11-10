# Ausführbarer Spezialprompt – dauerhafte KI-Kontext- und Historienpflege in STEPS

Arbeite ausschließlich im Projekt STEPS (`C:\Users\Timvo\OneDrive\Github\steps`), Quelle Glide 3.53 unter `src/glide-v3.53/`. Lies zuerst `docs/operations/AI_CONTINUITY_PROTOCOL_V6.md`, `docs/project/antigravity-handover/README.md`, `AGENTS.md`, alle vorhandenen Übergaben/Audits und die reale Verzeichnisstruktur.

Führe ein konservatives, **nicht-destruktives** Inventar sämtlicher vorhandener früherer und neuer KI-Outputs durch: alle Prompts V1–V5, Gesamtanalysen, Forschungsberichte, Wettbewerbs-/UI-Analysen, Tabellen, Code-/Test-/CI-/Releaseberichte, Designausgaben, allgemeine technische Antworten, Originalbenutzerentscheidungen, Quellarchive, Projekt-Overviews und Fable-/Copilot-/Antigravity-/Claude-/ChatGPT-Handover. Nicht verfügbare Ausgaben explizit als fehlend aufführen; keine unbekannten Inhalte oder vergangenen Tests erfinden.

Lege ein verlustarmes `HISTORICAL_OUTPUTS_REGISTER.csv` mit `artifact_id,source_id,path,hash,origin_model,created_at,referenced_sha,content_kind,coverage,exact_duplicate_of,derived_from,supersedes,status,missing_evidence,review_action` an. Lege ein `OUTPUT_REGISTER.csv`, `SESSION_LOG.md`, `STATE.json`, `SOURCE_COVERAGE.csv`, `NEXT_SESSION_HANDOVER.md` mit den Vorgaben aus dem Kontinuitätsprotokoll an. Dateinamen, Zeilen, Original-Hash-/Git-Blob-IDs erhalten; keine Originalfassung ersetzen.

Erstelle eine Crosswalk-Matrix von historischen W/G/K/N/REQ/DEC-IDs über V3/V4/V5 bis V6 und markiere offene und bestätigte Punkte. Für jedes fachlich relevante neue Analyseergebnis einen Output-Registereintrag, auch ohne Codeänderung. Prüfe Linkauflösung und dass jedes kanonische aktuelle Dokument eine nachverfolgbare Quelle besitzt. Primärquellen/Schutzrechte beachten.

**Modus:** Nur neue Auditoutputs in eigenen externen Sitzungsordner, keine produktive Repo-Datei ändern. Git-Integration später nur nach ausdrücklicher Freigabe auf Steps-Branch; keine Vermischung mit dem originären Glide-Repository. Abschließend eine nachweisbasierte Coverage-Bilanz und die nächste präzise Aufgabe ausgeben.
