# STEPS – Historical Secret Baseline & Alert Reconciliation Audit (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** RECONCILED & FAIL-CLOSED SECURED (Gate 4 & Gate 5 Passed)  
**Autor:** Leitender Security Auditor & QA-Architekt  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil IV  

---

## 1. Executive Summary & Alert-Reconciliation

Eine detaillierte Rekonziliation zwischen den gemeldeten GitHub-Alerts und den tatsächlichen Fundstellen im Repository ergab ein klares, faktenbasiertes Bild:

1. **3 GitHub Secret Scanning Alerts:**
   - **Alert #1:** Google Cloud / Firebase API Key (`AIzaSy...qcW8`), vorkommend in 15 HTML- und JS-Dateien.
   - **Alert #2:** Google Cloud / Firebase API Key (`AIzaSy...bUhE`), vorkommend in 6 HTML-Dateien.
   - **Alert #3:** Google Cloud / Firebase API Key (`AIzaSy...oAnw`), vorkommend in 6 HTML-Dateien.
   - **Gesamt:** 27 Fundstellen für Google-Schlüssel.
2. **1 AWS Key Identifier (Scanner-Only):**
   - **AWS Key Identifier:** `AKIAAE...FCAA`, vorkommend in 6 HTML-Dateien.
   - **Befund:** Dieser Schlüssel wurde vom lokalen STEPS-Regex-Scanner erfasst, löste jedoch **keinen** GitHub-Secret-Scanning-Alert aus, da es sich um einen reinen statischen S3-CDN-Client-Key in Third-Party-HTML handelt (ohne zugehörigen Secret Access Key).
3. **Gesamtzahl:** $27 + 6 = 33$ Fundstellen, die sich auf genau **4 eindeutige Werte** reduzieren.

---

## 2. Herkunft & Eigentümerschaft (Third-Party Web Dumps)

Sämtliche 33 Fundstellen befinden sich ausschließlich in heruntergeladenen HTML- und JS-Archivdateien unter `research/STEPS_Bibliothek/`:
- **Ursprung:** Commit `a14c3f3da4f7a4bc8ebaa75f0ef4de15b625d2cb` (10.11.2026).
- **Inhalt:** Webseiten-Dumps von Ableton-Blogbeiträgen aus den Jahren 2018–2020 (z. B. *ANTI-MASS: From Uganda into the Unknown*, *Bathe: Inside The Inside Voice(s)*, *Cloudchord: Tending the Bloom Bap Garden*).
- **Zweck der Schlüssel:** Öffentliche Client-Keys für eingebettete YouTube-HTML5-Videoplayer (`base.js`, `9H9th5XDqjo.html`).
- **Risikobewertung:**
  - **Keine privaten Daten des Project Owners:** Kein Schlüssel gehört zum STEPS-Projekt oder zum persönlichen Google-/AWS-Konto des Entwicklers.
  - **Keine finanziellen Risiken für das Projekt:** Es existiert keine Verknüpfung zu Projektabrechnungen.
  - **Urheberrechts- und Datenhygiene-Problem:** Die Web-Dumps stellen Fremdmaterial dar und fallen unter die Bereinigungsentscheidungen `OA-0001`, `OA-0033` und `ADR-012`.

---

## 3. Grundsatz der Nicht-Interaktion (Rule 6 Compliance)

Gemäß Abschnitt 4.2 des Arbeitsauftrags und AGENTS.md (Regel 6: *Datenherkunft* und ethische Sicherheitsgrenzen):
- **Keine Verwendungsversuche:** Es wurden zu keinem Zeitpunkt externe API-Endpunkte mit diesen Schlüsseln aufgerufen.
- **Kein Live-Probing:** Es wurden keine Authentifizierungs- oder Berechtigungsprüfungen gegen Google Cloud oder AWS unternommen.
- **Keine Klartextausgabe:** Alle Logdateien, Commits und Berichte maskieren gefundene Token strikt (`AIzaSy...XXXX`).
- **Kryptographische Bindung:** Die Baseline sichert die Fundstellen rein mathematisch über SHA-256 Hashes (`secret_sha256`), ohne unmaskierte Geheimnisse im Repository zu speichern.

---

## 4. Technische Schutzmechanismen (Historical Baseline v1.1.0)

In `scripts/historical_secret_baseline.json` ist jeder der 33 Funde mit folgendem 5-Tupel verankert:
$$\text{Exemption} = (\text{norm\_path}, \text{line\_number}, \text{pattern\_name}, \text{secret\_sha256}, \text{line\_sha256})$$

### Fail-Closed Schutzgarantien:
1. **Kein Silent Pass bei veränderten Schlüsseln (DEF-4.16-04):** Wird auf einer befreiten Zeile ein anderes Secret platziert, weicht der SHA-256-Hash ab $\rightarrow$ Sofortiger Abbruch (`TAMPERED_SECRET_ON_BASELINE_LINE`).
2. **Keine Positionsverschiebung:** Wird ein alter Schlüssel in eine andere Datei oder Zeile kopiert $\rightarrow$ Sofortiger Abbruch (`UNREGISTERED_SECRET_LEAK`).
3. **Fail-Closed bei Dateiverlust:** Fehlt `historical_secret_baseline.json` oder ist das JSON beschädigt $\rightarrow$ Sofortiger Abbruch (`exit 1`).
4. **Vollständige Abdeckung (.agents gescannt):** Das Verzeichnis `.agents/` wird mit durchsucht; neue Schlüssel in Agenten-Prompts oder Skills werden sofort erkannt.

---

## 5. Handlungsempfehlung für den Project Owner (OA-0033)

1. **GitHub Secret Scanning Alerts #1–#3:** Im GitHub Security Tab als *„Won't fix / Public Third-Party Key“* schließen.
2. **Repository-Bereinigung:** Die betroffenen Blog-HTML-Dateien im Rahmen von `ADR-012` und `OA-0001` aus dem aktiven Git-Tracking entfernen.
