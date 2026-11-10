# Auftrag 28 – Verifikation aller Research-Requirements, Entscheidungen und Testnachweise

**Rolle:** externer Reviewer; prüfe gegen die Originalsourcen, nicht nur gegen die erste Steps-Overview. **Quellen:** `PROJECT_CONTEXT_HANDOVER.md` (28 REQs), zwei Forschungsarbeiten, Master-Research-Prompt, Codex-KB-Prompt, sieben Uploads, aktueller Steps-/Glide-Git-Tree, die 40+34 historisch nummerierten Konflikte/Gaps, `manifests/REQUIREMENTS_TRACE_28.csv` und `manifests/INVESTIGATION_COVERAGE_33_V2.csv`.

## Methode

Jede REQ und jede Auditdimension erhält `authoritative_source`, `observed_state`, `counterevidence`, `decision_owner`, `missing_inputs`, `next_proof`, `risk`, `status`. Entlarve insbesondere die Umwandlung von *dokumentiert* in *implementiert*, das unzulässige Zählen unterschiedlicher Ableton-Katalogstände, die Gleichsetzung von Skill und KB, und eine unbewiesene Glide-Portabilitätsbehauptung. Prüfe, ob Referenzbelege und Links im tatsächlichen Repo-Commit existieren, und kennzeichne historische, aber inzwischen überholte Aussagen.

Stelle mindestens zwei gegensätzliche Architekturhypothesen nebeneinander (Glide-Extrakt vs. kleine neue Tk-Shell) und dokumentiere ihre Falsifikationsversuche. Prüfe mindestens fünf Source/Claim-/Theoriefälle **gegen Originale**; wenn Quellen fehlen, `BLOCKED` statt Quellbehauptungen auf andere Bücher übertragen. Zu jeder P0-These wird ein gegenläufiger Test oder Negativbeispiel vorgeschrieben.

## Erforderliches Endergebnis

Eine maschinenlesbare diffbare Audit-Matrix mit allen 28 REQs und 33 Dimensionen, Versionierungs-/Fehlquellenregister, Status jedes Q0–Q7 Gates (PASS/FAIL/BLOCKED/NOT_RUN), konkrete Maßnahmen A0–A11, Gap- und Risiko-Korrekturen sowie ein unabhängiges Urteil über *Quelle, Wissenschaft, Produkt, Technik, Legal, QA, Organisation*. Kein „vollständig“, solange relevante Originale, Menschentests, private Quellenrechte oder Codeausführung fehlen. Abschließend: was früher falsch/zu optimistisch war, was neu tatsächlich überprüft wurde und was weiterhin **nur Empfehlung** ist.
