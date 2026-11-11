# STEPS – SICHERHEIT, COMPLIANCE UND LIZENZPRÜFUNG
## Sicherheitsaudit, GitHub Secret Scanning Alerts (#1–#3), Lizenzkompatibilität und OA-0033 Quarantäne

**Prüfdatum:** 11. November 2026  
**Gegenstand:** GitHub Alerts, Git-Historie, Lizenzen, Zugriffsrechte  

---

## 1. GitHub Secret Scanning Alerts (#1, #2, #3) und OA-0033

### Befund:
GitHub Secret Scanning meldet 3 aktive Alerts für historische Google API Keys in älteren Commits der Historie:
- **Alert #1:** Google API Key in historischem Commit (Phase 1 Archive).
- **Alert #2:** Google API Key in altem Testskript.
- **Alert #3:** Google API Key in Dokumentationsfragment.

### Quarantänestatus & Maßnahmen:
1. **Sofortmaßnahme:** Die betroffenen API-Schlüssel müssen in der Google Cloud Console als widerrufen (revoked/deleted) markiert werden, falls sie jemals aktiv waren.
2. **Git-Historie:** Sofern das Repository öffentlich bleiben soll, ist ein Rewrite der Historie mittels BFG Repo-Cleaner erforderlich, um die Strings aus alten Blobs zu entfernen.
3. **Pre-Commit-Guardrails:** In `scripts/pre-commit-secret-check.py` und `.gitignore` wurden Filterregeln etabliert, die ein erneutes Einchecken von API-Keys verhindern.

---

## 2. Lizenzprüfung und Urheberrecht (MPL 2.0 vs. Fremdassets)

### 2.1 Eigene Codebasis: Mozilla Public License 2.0 (MPL-2.0)
- Datei `LICENSE` im Root definiert die MPL 2.0 als primäre Projektlizenz.
- Alle Dateien unter `src/steps/` und `tests/` sind kompatibel und unterliegen dieser Open-Source-Lizenz.

### 2.2 Fremdkomponenten und Altlasten:
- **Glide 3.53 (`src/glide-v3.53/`):** Ursprünglich unter MIT/GPL entstanden. Liegt isoliert vor und wird nicht in STEPS kompiliert oder importiert.
- **Drittanbieter-PDFs in `research/STEPS_Bibliothek/`:** 7 kommerzielle Lehrbücher und 53 Fach-PDFs. Sie dürfen nach Urheberrechtsgesetz (§§ 60a ff. UrhG) nur zu privaten Forschungszwecken genutzt, keinesfalls jedoch in einem frei zugänglichen öffentlichen GitHub-Repository gehostet werden.
- **Empfehlung (P0):** Repositorium privat schalten oder den Ordner `research/STEPS_Bibliothek/` vollständig aus dem Git-Tracking entfernen.
