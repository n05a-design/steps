# STEPS – Threat Model: Historical Secret Baseline & CI Guardrails (Phase 4.16)

**Datum:** 2026-11-11  
**Status:** IMPLEMENTED & VERIFIED  
**Sicherheitsstufe:** HIGH (Fail-Closed)  
**Referenzdokument:** Phase 4.16 Master Prompt, Teil V  

---

## 1. Ausgangslage & Bedrohungsszenarien

In STEPS wurden historische Assets (unter `research/STEPS_Bibliothek/`, insbesondere Drittanbieter-HTML-Dumps eines Ableton-Blogs) identifiziert, die in früheren Commits (z. B. `a14c3f3`) eingecheckt wurden. Diese enthalten verwaiste API-Keys (3 Google Cloud API Keys und 1 AWS Access Key ID über 33 Vorkommen).

### Bisherige Schwachstellen in Phase 4.15:
1. **Unzureichende Bindung (DEF-4.16-04):** Die Baseline war lediglich an `(file, line, pattern_desc)` gebunden. Ein Angreifer oder Entwickler hätte auf einer befreiten Zeile einen neuen, echten Secret-Key platzieren können, ohne dass der Scanner anschlägt.
2. **Directory-Whitelisting-Leak (DEF-4.16-05):** Das `.agents/`-Verzeichnis war pauschal von der Prüfung ausgenommen. Ein in eine Agenten-Konfiguration geschriebenes Geheimnis wäre unerkannt geblieben.
3. **Fail-Open bei Dateiverlust:** Bei Fehlen der Baseline-Datei gab es lediglich eine Warnung statt eines harten Abbruchs (`exit 1`).

---

## 2. Bedrohungsmodell & Gegenmaßnahmen (Phase 4.16)

| Bedrohungs-ID | Bedrohungsszenario | Angriffsvektor | Gegenmaßnahme in Phase 4.16 |
|---|---|---|---|
| **THREAT-01** | Secret Replacement auf befreiter Zeile | Austausch des historischen Schlüssels durch ein neues aktives Secret auf Zeile $N$ | **Kryptographische Bindung (`secret_sha256`):** Jeder Baseline-Eintrag vergleicht den SHA-256-Hash des Tokens. Ein abweichender Hash löst sofort Alarm aus (`TAMPERED_SECRET_ON_BASELINE_LINE`). |
| **THREAT-02** | Secret Migration / Verschiebung | Verschieben eines alten Schlüssels in eine andere Zeile oder Datei | **Strikte Positions- & Dateiprüfung:** Exemption gilt ausschließlich für das exakte Tupel `(file, line, desc, secret_sha256)`. Jede Verschiebung wird als `UNREGISTERED_SECRET_LEAK` blockiert. |
| **THREAT-03** | Injection in Agenten-Workflows | Platzierung von API-Keys in `.agents/skills/` oder Prompt-Dateien | **Beseitigung der `.agents`-Exklusion:** `.agents/` wird vollständig durchsucht. |
| **THREAT-04** | Unterdrückung der Baseline (Sabotage) | Löschen oder Beschädigen von `historical_secret_baseline.json` | **Fail-Closed Architecture:** Scanner bricht bei fehlender Datei (`FileNotFoundError`) oder fehlerhaftem JSON (`JSONDecodeError`) sofort mit Exit-Code 1 ab. |
| **THREAT-05** | Credential Harvesting via Log-Leaks | Ausgabe unmaskierter Secrets in CI-Logs oder Fehlerberichten | **Masking Enforcement:** Alle Meldungen maskieren Secrets strikt (z. B. `AIzaSy...XXXX`). Keine Klartextausgabe. |

---

## 3. Deduplizierte Token-Inventarisierung (Quarantine Baseline)

Unter den 33 historischen Fundstellen existieren genau 4 eindeutige Geheimniswerte:

| Token-Typ | Maskierter Wert | Token SHA-256 (Präfix) | Vorkommen | Referenz-Task |
|---|---|:---:|:---:|:---:|
| Google Cloud / Firebase API Key | `AIzaSy...oAnw` | `2bea43e3f40e...` | 24 Dateien | OA-0033 |
| Google Cloud / Firebase API Key | `AIzaSy...qcW8` | `31043aae8be2...` | 2 Dateien | OA-0033 |
| Google Cloud / Firebase API Key | `AIzaSy...bUhE` | `fb553538db18...` | 1 Datei | OA-0033 |
| AWS Access Key ID | `AKIAAE...FCAA` | `aee1c94d54a4...` | 6 Dateien | OA-0001 |

> [!IMPORTANT]
> Keine unmaskierten Tokens werden im Repository gespeichert oder ausgegeben.
> Die endgültige Bereinigung der historischen Dumps (durch Löschung oder Redaktion via BFG/git-filter-repo) verbleibt gemäß ADR-001/ADR-002 und Regel 2 (Preservation-First) unter expliziter Entscheidung des Project Owners (OA-0001 / OA-0033).
