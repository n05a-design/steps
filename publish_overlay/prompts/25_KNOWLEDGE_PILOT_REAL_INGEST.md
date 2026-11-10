# Auftrag 25 – Erster echter Knowledge-Base-Batch (kein weiterer Scaffold)

**Verwendung:** Codex/Work/Claude Code mit lokalem Zugriff auf legal zugängliche Originalquellen; **kein** Rückgriff nur auf eine KI-Zusammenfassung oder Downloadnamen. Maßgeblich sind der historische `04_CODEX_KNOWLEDGE_BASE_FOUNDATION_PROMPT.md`, `PROJECT_CONTEXT_HANDOVER.md`, `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`, `knowledge/sources/RIGHTS_POLICY.md` und das aktuelle `knowledge/sources/registry.yaml`.

## Arbeitsauftrag

Prüfe zu Beginn `main`, `git status`, tatsächliche `sources: []`-Datei, vorhandene Source-/Concept-/Schema-IDs, alle 20 Initialquellen, sieben Research-Dokumente und aktuell zugängliche Originale. **Trenne** Quellen, die überhaupt im Git-Baum stehen, von bytegeprüften Originalen und von rechtlich zur jeweiligen Verarbeitung und Veröffentlichung geeigneten Quellen. Erstelle das Intake zunächst auf einem kleinen, kontrollierten Satz (Ziel fünf nachweislich nutzbare Quellen; weniger, falls Rechte dies nicht erlauben). Keine Rechtsannahme aus PDF-Titel, DOI oder Git-Verfügbarkeit ableiten. Verarbeite keine ungeprüften Volltexte ins öffentliche Repo.

Für jede Quelle: stabile ID, bibliografische Identität, Edition, Original-URL/DOI, Hash, Rechte-/Freigabestatus, genutzte Passage mit page/section locator, Parserfehler, Thema, Framework. Extrahiere kurze, eigenständig formulierte Claims, bilde Concept-/Relation-/Rule-/Example-Kandidaten mit positiven und negativen musikalischen Beispielen, erhalte alternative Interpretationen. `E7→Am` darf nicht pauschal Zwischendominante heißen. Importierte Änderungen in einer Reviewqueue mit `accepted`, `needs_review`, `restricted_local` kennzeichnen. Die App-/Skill-Schicht darf `needs_review` nicht als kanonische Tatsache ausgeben.

Führe **zweimal** denselben Batch aus; der zweite Lauf erzeugt keine zusätzlichen unreviewten Quellen-/Claim-Datensätze. Ändert sich eine Source, erzeuge konkreten Diff statt stiller Mutation. Prüfe Quellen-ID- und Claim-ID-Links, Lizenzrechte, Regressionstests und ein Retrieval-Testset mit mindestens einem belegten Treffer, einer Mehrdeutigkeit und einer korrekten „keine geprüfte Quelle“-Antwort.

## Ausgabe/Abnahme

Liefere `ingestion_batch_manifest`, `sources_delta`, `source_cards`, `claims`, `concepts`, `relations`, `tests`, `license_review`, `unresolved`, `retrieval_evals` und `INGESTION_REPORT`, jeweils mit Zeit/Commit/Hash. Der Reviewer muss jeden Claim vom Query/Skilltext über Claim- und Locator-ID zum Original zurückverfolgen können. **Als abgeschlossen gilt nicht** die Existenz von 10 README- oder YAML-Platzhaltern: mindestens ein tatsächlich lesbarer, prüfbarer Source→Rule→Test→Query-Durchstich ist Pflicht. Falls wegen Rechten/fehlenden Originalen nur Metadaten möglich sind: `BLOCKED` mit fehlenden Belegen melden, nicht künstliche Claims erfinden.
