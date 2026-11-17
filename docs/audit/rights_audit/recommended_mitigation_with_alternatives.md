# STEPS – Maßnahmenplan und Alternativenbewertung für Fremdmaterialien (Phase P0.1)

- **Stand:** 17.11.2026 (Europe/Berlin)
- **Status:** Konsolidierter Richtlinien- und Entscheidungsbericht
- **Referenzdokumente:** `prompts/27_PUBLIC_REPO_RIGHTS_HISTORY_AUDIT.md`, `docs/governance/RIGHTS_SECURITY_AND_RELEASE.md`, `research/gaps/RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md`

---

## 1. Systematische Bewertung der 4 Lösungsalternativen

| Option | Beschreibung | Vorteile | Nachteile / Risiken | Status |
|---|---|---|---|---|
| **Option 1: Repository privat stellen** | Das gesamte GitHub-Repository wird von öffentlich auf privat umgestellt. | Sofortige Beseitigung jeglicher externer Download-Möglichkeit für die gesamte Historie. | Open-Source-Projektziel, Sichtbarkeit und CI-Workflows werden eingeschränkt. | Als Fallback-Option dokumentiert |
| **Option 2: Working-Tree-Isolation via `.gitignore` + eigene Zusammenfassungen** | Klasse E aus aktuellem Stand entfernen; Klasse A–D als offene Bildungsinhalte führen; eigene Zusammenfassungen versionieren. | Erhält volle Git-Integrität und Prüfbarkeit; keine SHA-Brüche; sauberer MVP-Zweig. | Historische Blobs bleiben in früheren Commits der Objektdatenbank auffindbar. | **Vom Inhaber am 14.11.2026 gewählt und umgesetzt** |
| **Option 3: Coordinated History Rewrite via `git filter-repo`** | Nachträgliches Umschreiben der Git-Historie zur Tilgung aller Klasse-E-Blobs aus allen Commits. | Vollständige Tilgung der Binärdaten aus dem gesamten Repository. | Zerstört alle Commit-SHAs, bricht Prüfberichte, PRs und Forks; hohes Risiko von Synchronisationsfehlern. | **Vom Inhaber am 14.11.2026 explizit verworfen** |
| **Option 4: Frischer v2-Release-Tree** | Für den offiziellen Release (v0.1.0) wird ein sauberes, neues Repository ohne historische Forschungsdaten initialisiert. | 100% sauberer Release-Baum ohne jegliche historische Altlasten; minimale Downloadgröße. | Getrennte Repositories müssen gepflegt werden; Verlust der einheitlichen Historie. | **Empfohlener Pfad für Release Phase 5 / Packaging** |

---

## 2. Künftige Ingestion-Policy: „Zero New Copyrighted Bytes“

Um künftig jeglichen rechtlichen Konflikt von vornherein auszuschließen, gilt für alle Entwicklungsagenten und Mitwirkenden folgende **verbindliche Ingestion-Pipeline**:

```
+-------------------------------------------------------------+
| 1. LOKALE QUARANTÄNE (Außerhalb Git)                        |
|    - Downloads & Scrapes verbleiben im lokalen Scratch-Pfad |
|    - Absolutes Git-Schreibverbot für externe Volltexte      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 2. STRUKTUR- & QUELLEN-EXTRAKTION                           |
|    - Erfassen bibliografischer Metadaten (Autor, Jahr, DOI) |
|    - Zuordnung der Rechteklasse (A, B, C, D, E)             |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 3. PARAPHRASE & EIGENE AUSSAGENFORMULIERUNG                |
|    - Erstellung prägnanter didaktischer Claims in eigenen   |
|      Worten (keine 1:1 Kopien von Textblöcken)              |
|    - Angabe genauer Fundstellen (Seitenzahl / Kapitel)       |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 4. COMMIT INS REPOSITORY (Ausschließlich strukturierte Daten)|
|    - Nur YAML/JSON-Metadaten und Markdown-Zusammenfassungen |
|    - CI-Gate prüft Dateiendungen und Binärgrößen vor Commit |
+-------------------------------------------------------------+
```

---

## 3. Konkrete Entscheidungsliste und nächstentscheidbare Fälle

1. **Klasse E:** Vollständig unter `restricted_local` isoliert. Keine weitere Aktion im Arbeitsbaum erforderlich.
2. **Klasse A & B:** Freigegeben für Forschungs- und Bildungsreferenzen im Quell-Repository.
3. **Klasse C & D (Handbücher, Scrapes, Vorlesungsfolien):** Dürfen im `research/`-Ordner verbleiben, sind jedoch für jedes Endnutzer-Packaging (PyInstaller / PyPI) strikt ausgeschlossen.
4. **AI-Text `The Chord Wheel.html`:** Eindeutig als Junk klassifiziert und für jede Ableitung von Musikregeln gesperrt.
5. **Externe MIDI-Packs (`ppr-*`):** Verbleiben ausschließlich als stilistische Analysebeispiele in der Forschungsbibliothek; dürfen nicht im Installationspaket von STEPS ausgeliefert werden.
