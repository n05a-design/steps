# STEPS – OFFENE RISIKEN, QUARANTÄNE UND BLOCKER
## Dokumentation nicht archivierter Bestände und ausstehender Eigentümerentscheidungen

**Prüfdatum:** 11. November 2026  

---

## 1. Risikobereich 1: Urheberrechtlich geschützte Buch-Scrapes (OA-0001)

* **Ort:** `research/STEPS_Bibliothek/` (7 kommerzielle Lehrbücher, 53 Fach-PDFs, 74 Ableton-MIDIs).
* **Risiko:** Urheberrechtsverletzung und DMCA-Risiko bei öffentlicher Zugänglichkeit auf GitHub.
* **Klassifizierung:** `SECURITY_OR_RIGHTS_RESTRICTED` / `OWNER_APPROVAL_REQUIRED`.
* **Archivierungsentscheidung:** **BEWUSST NICHT IN `archive/` VERSCHOBEN**.
  * Eine Verschiebung innerhalb desselben Repositories beseitigt weder das DMCA-Risiko noch die historischen Git-Blobs.
  * Der Bestand verbleibt bis zur formalen Owner-Entscheidung in Quarantäne.
* **Empfehlung an den Eigentümer (P0):**
  1. Sofortmaßnahme: Repository in den GitHub-Einstellungen auf **`Private`** setzen.
  2. Vor einem späteren Open-Source-Release: Sauberes BFG-Scrubbing der Git-Historie.

---

## 2. Risikobereich 2: Historische Google API Key Alerts (OA-0033)

* **Ort:** GitHub Secret Scanning Alerts #1, #2, #3 in historischen Commits.
* **Klassifizierung:** `SECURITY_OR_RIGHTS_RESTRICTED`.
* **Maßnahme:** Inaktive/historische Test-Schlüssel wurden in `scripts/pre-commit-secret-check.py` blockiert. Der Eigentümer muss die Schlüssel in der Google Cloud Console als widerrufen (revoked) bestätigen.

---

## 3. Risikobereich 3: Glide 3.53 Legacy Code (`src/glide-v3.53/`)

* **Ort:** `src/glide-v3.53/` (1.580 Dateien, ~301 MB).
* **Klassifizierung:** `OWNER_REVIEW_REQUIRED` (Glide-Schutz nach Regel 2.3).
* **Status:** Bleibt vollständig unberührt und physisch getrennt im Repository. Es existieren 0 Code-Importe in STEPS. Eine Verschiebung oder Auslagerung in ein eigenes Repo erfordert eine gesonderte Owner-Freigabe.
