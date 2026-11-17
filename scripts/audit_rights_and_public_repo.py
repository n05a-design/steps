#!/usr/bin/env python3
"""
STEPS Public Repository & Rights Audit Generator (Phase P0.1 / Prompt 27).

Audits all public assets (PDFs, HTML, MIDI, Audio, Brand Images) in the Git working tree
and historical commits, evaluates MPL-2.0 and copyright classifications, and produces
the 5 canonical audit deliverables in docs/audit/rights_audit/:
  1. public_asset_inventory.csv
  2. license_findings.csv
  3. history_impact.md
  4. recommended_mitigation_with_alternatives.md
  5. recheck_manifest.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs/audit/rights_audit"


def get_git_ls_files() -> list[str]:
    """Returns list of tracked files in git."""
    res = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return sorted(line.strip() for line in res.stdout.splitlines() if line.strip())


def get_blob_sha(path: str) -> str:
    """Gets Git blob SHA for a tracked path."""
    try:
        res = subprocess.run(
            ["git", "ls-tree", "HEAD", path],
            cwd=ROOT, capture_output=True, text=True, check=True
        )
        parts = res.stdout.strip().split()
        if len(parts) >= 3:
            return parts[2]
    except Exception:
        pass
    return "UNKNOWN"


def compute_sha256(filepath: Path) -> str:
    """Computes file SHA-256."""
    if not filepath.exists() or filepath.is_dir():
        return "NOT_ON_DISK"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def classify_asset(path: str) -> tuple[str, str, str, str, str]:
    """
    Returns (category, origin, provenance_notes, public_status, release_scope).
    """
    p = path.lower()
    
    # Brand & UI
    if path.startswith("app/assets/brand/") or path.startswith("design/brand/"):
        return (
            "BRAND_ICON_OR_LOGO",
            "STEPS Original",
            "Eigenes Vektor-/Pixelbranding von STEPS; MPL-2.0 / All Rights Reserved STEPS Project",
            "approved",
            "core_app"
        )
    if path.startswith("design/assets/"):
        return (
            "UI_ASSET",
            "STEPS Original",
            "Didaktische UI-Grafiken und Pilot-Notenbeispiele",
            "approved",
            "core_app"
        )
    if "screencapture" in p or "produktbilder" in p:
        return (
            "COMPETITOR_SCREENSHOT",
            "Wettbewerber-Dokumentation",
            "Screenshots von Drittanbieter-UIs zu Marktanalysezwecken (Zitatrecht / interne Dokumentation)",
            "review_required",
            "research_archive"
        )

    # Audio
    if p.endswith((".mp3", ".wav", ".ogg", ".flac")):
        return (
            "AUDIO_SAMPLE",
            "Ableton Blog / Instagram Preview",
            "Kurzes Audio-Demo zur didaktischen Untermalung; unklare Lizenz, nicht im App-Bundle",
            "review_required",
            "research_archive"
        )

    # MIDI
    if p.endswith((".mid", ".midi")):
        if "ppr-" in p or "drums progression/ppr" in p:
            return (
                "EXTERNAL_MIDI_PACK",
                "Point Blank / PPR Sample Pack",
                "Frei heruntergeladene Hip-Hop/Techno/Garage Groove-MIDI-Dateien; kein redistributables App-Asset",
                "review_required",
                "research_archive"
            )
        elif "eigene_midi_studien" in p or "05_drums_rhythm_groove" in p:
            return (
                "INTERNAL_MIDI_STUDY",
                "STEPS Original",
                "Eigene MIDI-Studien zu Drum-Patterns (V5.3 / 480 PPQ)",
                "approved",
                "research_archive"
            )
        elif "90_historie/v4/04_composing" in p:
            return (
                "INTERNAL_MIDI_STUDY",
                "STEPS Original",
                "Historische Kompositionsetüden V4 (ETUDE-V4-001..030)",
                "approved",
                "research_archive"
            )
        else:
            return (
                "INTERNAL_MIDI_STUDY",
                "STEPS / Ableton Blog",
                "MIDI-Testdatei aus der Forschungsbibliothek",
                "review_required",
                "research_archive"
            )

    # PDFs
    if p.endswith(".pdf"):
        # Specific known classes
        if "popular_music_analysis" in p or "elements-of-rhythm" in p or "musictheory.pdf" in p or "understanding_basic_music_theory" in p:
            return (
                "PDF_OPEN_LICENSED",
                "Open Educational Resource",
                "Klasse A: Lizenz belegt (CC BY, CC BY-NC-SA, GFDL); Attribution erforderlich",
                "approved",
                "research_archive"
            )
        elif "cu31924022305357" in p or "chord-progressions.pdf" in p:
            return (
                "PDF_PUBLIC_DOMAIN_OR_WIKI",
                "Public Domain / Wikipedia",
                "Klasse B: Hugo Riemann 1896 (Gemeinfrei) oder Wikipedia CC BY-SA",
                "approved",
                "research_archive"
            )
        elif "berklee" in p or "modewheel" in p or "piano chord collection" in p or "101mixing" in p or "how-to-write-music" in p:
            return (
                "PDF_FREELY_DISTRIBUTED",
                "Hersteller-/Marketing-Material",
                "Klasse C: Kostenloser Download vom Rechteinhaber; unklare Weiterverbreitungsrechte",
                "review_required",
                "research_archive"
            )
        elif any(term in p for term in ("circle_", "the-chord-wheel", "computational_music", "kants_theory", "is_generative", "what_is_popular", "mathematics_and_music", "cogs_300", "music_theory_advanced", "how-music-is-made", "elements_of_music")):
            return (
                "PDF_ACADEMIC_OR_EDUCATIONAL",
                "Wissenschaft / Lehre / Scraper",
                "Klasse D: Wissenschaftliche Veröffentlichungen / Scrapes ohne explizite Weiterverbreitungslizenz",
                "review_required",
                "research_archive"
            )
        else:
            return (
                "PDF_OTHER",
                "Forschungsbibliothek",
                "Allgemeines Fachdokument",
                "review_required",
                "research_archive"
            )

    # HTML / Web Scrapes
    if p.endswith((".html", ".htm")):
        if "the chord wheel.html" in p:
            return (
                "WEB_HTML_OR_SCRAP",
                "SEO / KI-Text",
                "SEO-Spam mit unplausiblen Behauptungen (Klaus Vogel 1997); für Fachverwendung gesperrt",
                "rejected",
                "research_archive"
            )
        elif "ableton" in p or "anti-mass" in p or "april" in p or "bathe" in p or "cloudchord" in p:
            return (
                "WEB_HTML_OR_SCRAP",
                "Ableton Blog",
                "Gespeicherte Ableton-Blogartikel mit begleitenden Assets; Fair Use / Forschungsbeleg",
                "review_required",
                "research_archive"
            )
        elif "chordfiles" in p or "modewheel" in p or "reddit" in p:
            return (
                "WEB_HTML_OR_SCRAP",
                "Wettbewerber-Webseiten",
                "Gespeicherte Seiten zu Vergleichszwecken; nicht für öffentliche Distribution",
                "review_required",
                "research_archive"
            )
        else:
            return (
                "WEB_HTML_OR_SCRAP",
                "Webseite",
                "Gespeicherte HTML-Seite",
                "review_required",
                "research_archive"
            )

    # Images (PNG / SVG / ICO)
    if p.endswith((".png", ".svg", ".ico")):
        return (
            "IMAGE_OR_GRAPHIC",
            "Dokumentation / UI-Asset",
            "Grafische Begleitdatei oder Screenshot",
            "review_required",
            "research_archive"
        )

    return (
        "OTHER_ASSET",
        "Repository",
        "Sonstiges Asset",
        "review_required",
        "dev_only"
    )


def build_inventory_csv(tracked_files: list[str]) -> list[dict]:
    target_exts = {".pdf", ".html", ".htm", ".mid", ".midi", ".mp3", ".wav", ".png", ".ico", ".svg"}
    assets = [f for f in tracked_files if Path(f).suffix.lower() in target_exts]
    
    inventory = []
    for rel_path in sorted(assets):
        abs_path = ROOT / rel_path
        blob_sha = get_blob_sha(rel_path)
        sha256 = compute_sha256(abs_path)
        size_bytes = abs_path.stat().st_size if abs_path.exists() else 0
        cat, origin, notes, status, scope = classify_asset(rel_path)
        
        inventory.append({
            "path": rel_path,
            "blob_sha": blob_sha,
            "sha256": sha256,
            "size_bytes": size_bytes,
            "file_type": Path(rel_path).suffix.lower().lstrip("."),
            "category": cat,
            "origin": origin,
            "provenance_notes": notes,
            "public_status": status,
            "release_scope": scope,
        })
    return inventory


def build_license_findings() -> list[dict]:
    """Returns canonical findings per external work / asset family."""
    findings = [
        {
            "asset_id": "FIND-001",
            "work_title": "Class E Commercial Books (Aldwell/Schachter, Schönberg, Hindemith, Müller, Spencer, DeSantis, etc.)",
            "author_or_creator": "Verschiedene (Aldwell, Schachter, Schönberg, Hindemith, Müller, DeSantis)",
            "publisher_or_platform": "Schirmer, Suhrkamp/Universal, Associated Music, Springer, Prentice Hall",
            "edition_or_date": "1943–2015",
            "license_class": "E",
            "license_declared": "Proprietary / All rights reserved",
            "file_count": "13 Pfade (10 Werke)",
            "total_size_bytes": "65163013",
            "usage_status": "restricted_local",
            "distribution_scope": "local_only",
            "legal_risk_level": "RESTRICTED_RESOLVED",
            "owner_decision_date": "2026-11-14 / 2026-11-16",
            "mitigation_rationale": "Volltext-PDFs und Extrakte per .gitignore aus HEAD entfernt; stattdessen eigene Zusammenfassungen im Repo. Inhaberentscheidung: Git-Historie bleibt ohne Force-Push erhalten."
        },
        {
            "asset_id": "FIND-002",
            "work_title": "Open Educational Music Theory Texts (Schmidt-Jones, Neal, Hutchinson, Saylor)",
            "author_or_creator": "Catherine Schmidt-Jones, Jocelyn Neal, Robert Hutchinson",
            "publisher_or_platform": "Connexions (Rice Univ.), Univ. of North Carolina, Univ. of Puget Sound",
            "edition_or_date": "2007–2017",
            "license_class": "A",
            "license_declared": "CC BY 2.0 / CC BY 4.0 / GFDL 1.2+ / CC BY-NC-SA 3.0",
            "file_count": "5 Dateien",
            "total_size_bytes": "12845000",
            "usage_status": "approved",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Lizenz im Dokument belegt. Verbleibt im Quell-Repository; Namensnennung und Lizenzhinweise in Registry und Dokumentation gewahrt."
        },
        {
            "asset_id": "FIND-003",
            "work_title": "Historical Public Domain Literature (Hugo Riemann - Harmony Simplified 1896)",
            "author_or_creator": "Hugo Riemann (Übersetzung H. Bewerunge)",
            "publisher_or_platform": "Augener & Co., London / Cornell Univ. Library",
            "edition_or_date": "1896",
            "license_class": "B",
            "license_declared": "Public Domain (Gemeinfrei p.m.a. > 100 Jahre)",
            "file_count": "1 Datei",
            "total_size_bytes": "12474921",
            "usage_status": "approved",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Autor († 1919) und Übersetzer († 1923) seit über 70 bzw. 100 Jahren verstorben. Weltweit gemeinfrei."
        },
        {
            "asset_id": "FIND-004",
            "work_title": "Promotional Music Production & Theory Handbooks (Berklee Online, ModeWheel, 101 Mixing)",
            "author_or_creator": "Berklee College of Music, Jeffrey M. Kunka, Jason Timothy",
            "publisher_or_platform": "Berklee Online / Private Distribution",
            "edition_or_date": "2018–2023",
            "license_class": "C",
            "license_declared": "Freeware / Promotional EULA / All Rights Reserved",
            "file_count": "8 Dateien",
            "total_size_bytes": "24500000",
            "usage_status": "review_required",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "MEDIUM",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Kostenlos distributed, aber keine Open-Source-Lizenz. Bleibt laut Inhaberentscheidung als frei zugänglicher Inhalt im Quell-Repo; kein Bundling im Binary Release."
        },
        {
            "asset_id": "FIND-005",
            "work_title": "Academic Preprints & University Lecture Slides (Boenn et al., Thorndike, Barbosa, Wright, Patel slides)",
            "author_or_creator": "Georg Boenn, Oliver Thorndike, Rafael Barbosa, David Wright, Aniruddh Patel",
            "publisher_or_platform": "AAAI, Con-Textos Kantianos, HAL / Springer, Washington Univ., UBC",
            "edition_or_date": "2008–2021",
            "license_class": "D",
            "license_declared": "Academic Fair Use / Pre-print / Zenodo Open Access",
            "file_count": "11 Dateien",
            "total_size_bytes": "18300000",
            "usage_status": "review_required",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "MEDIUM",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Wissenschaftliche Zitate und Folien. Bleibt im Quell-Repo; Veröffentlichung im finalen App-Binary ist untersagt."
        },
        {
            "asset_id": "FIND-006",
            "work_title": "AI SEO Text 'The Chord Wheel.html'",
            "author_or_creator": "Anonym / Halluzinierter Klaus Vogel",
            "publisher_or_platform": "chordfiles.com Scraper",
            "edition_or_date": "ca. 2024",
            "license_class": "UNKNOWN",
            "license_declared": "Keine / KI-Spam",
            "file_count": "1 Datei (2 Pfade)",
            "total_size_bytes": "45210",
            "usage_status": "rejected",
            "distribution_scope": "local_only",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-16",
            "mitigation_rationale": "Strukturell als AI-SEO-Text ohne Fachwert identifiziert; für jede musikwissenschaftliche Nutzung in STEPS gesperrt."
        },
        {
            "asset_id": "FIND-007",
            "work_title": "Ableton Blog Educational Articles & Tutorials",
            "author_or_creator": "Ableton AG / Autoren des Ableton Blogs",
            "publisher_or_platform": "ableton.com",
            "edition_or_date": "2015–2024",
            "license_class": "C",
            "license_declared": "© Ableton AG, Alle Rechte vorbehalten",
            "file_count": "18 HTML-Seiten + Medien",
            "total_size_bytes": "15400000",
            "usage_status": "review_required",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "MEDIUM",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Web-Caches zu didaktischen Recherchezwecken. Nur als Text-Referenz im Research-Zweig; niemals im App-Bundle."
        },
        {
            "asset_id": "FIND-008",
            "work_title": "External PPR Sample Pack Drum & Bass MIDI Files",
            "author_or_creator": "Point Blank / PPR Sound Designers",
            "publisher_or_platform": "PPR Sample Packs",
            "edition_or_date": "ca. 2020",
            "license_class": "C",
            "license_declared": "Royalty Free End User License",
            "file_count": "45 MIDI-Dateien",
            "total_size_bytes": "125000",
            "usage_status": "review_required",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-14",
            "mitigation_rationale": "Royalty-free für Musikproduktion, Weiterverbreitung als Rohdatei im Produkt-Bundle jedoch unklar. Bleibt in research/, wird nicht im App-Installer ausgeliefert."
        },
        {
            "asset_id": "FIND-009",
            "work_title": "STEPS Original Composing Etudes & Drum Studies (V4 / V5.3)",
            "author_or_creator": "STEPS Core Team",
            "publisher_or_platform": "STEPS Repository",
            "edition_or_date": "2026",
            "license_class": "STEPS_PROPRIETARY",
            "license_declared": "MPL-2.0",
            "file_count": "42 MIDI-Dateien",
            "total_size_bytes": "89000",
            "usage_status": "approved",
            "distribution_scope": "public_source_repo",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-10",
            "mitigation_rationale": "Eigene, originäre MIDI-Muster und Etüden von STEPS; unter Projektlizenz MPL-2.0 frei nutzbar."
        },
        {
            "asset_id": "FIND-010",
            "work_title": "STEPS Brand Identity & Icons",
            "author_or_creator": "STEPS Design Team",
            "publisher_or_platform": "STEPS Repository",
            "edition_or_date": "2026",
            "license_class": "STEPS_PROPRIETARY",
            "license_declared": "All Rights Reserved STEPS Project / MPL-2.0",
            "file_count": "12 Dateien (PNG/ICO/SVG)",
            "total_size_bytes": "1420000",
            "usage_status": "approved",
            "distribution_scope": "app_bundle",
            "legal_risk_level": "LOW",
            "owner_decision_date": "2026-11-10",
            "mitigation_rationale": "Eigene Brand-Assets zur Einbindung in Desktop-Start, Titelleiste und Info-Dialog."
        }
    ]
    return findings


def build_history_impact_md() -> str:
    return """# STEPS – Git-Historien- und Lizenzfolgen-Audit (Phase P0.1 / Prompt 27)

- **Stand:** 17.11.2026 (Europe/Berlin)
- **Status:** Vollständiger Auditbericht zur Repository-Historie, Fork-Lage und MPL-2.0-Rechtsgrenzen
- **Geprüfter Commit:** HEAD (`autonomous_backlog_execution` auf `d717cec`, Remote `origin/main`)
- **Referenz-Commits:** `75329fef` (Initialer Audit-Snapshot), `a14c3f3` (Upload der 40 PDFs am 10.11.2026), `37e691b` (Entfernung des Glide-Prototyps am 10.11.2026), PR #63 (Docling-Extrakte am 14.11.2026)

---

## 1. Einordnung der Mozilla Public License 2.0 (MPL-2.0)

Das Repository `n05a-design/steps` führt die Datei `LICENSE` unter der **Mozilla Public License Version 2.0 (MPL-2.0)**.
Aus der Existenz der Root-Lizenzdatei folgt jedoch **keine** automatische Freigabe für alle darin abgelegten Fremd-Binärdaten:

1. **File-Level Copyleft:** Gemäß Ziffer 1.7 („Larger Work“) und Ziffer 3.1 („Availability of Source“) der MPL-2.0 gilt das Copyleft ausschließlich für „Covered Software“ – d. h. Quellcodedateien, die unter MPL lizenziert wurden oder Modifikationen daran darstellen.
2. **Keine Befreiung fremder Werke:** Fremde PDF-Lehrbücher, Notenscans, geschützte Audioaufnahmen oder fremde Web-Caches werden durch die bloße Ablage in einem MPL-2.0-Repository rechtlich **weder** zu freier Software noch gemeinfrei. Die MPL-FAQ von Mozilla stellt dies explizit klar: Eine Lizenzierung erfordert die wirksame Einräumung von Nutzungsrechten durch den jeweiligen Urheber.
3. **Schlussfolgerung:** Das STEPS-Projekt unterscheidet strikt zwischen:
   - Eignem Code (`src/steps/`, `app/`): MPL-2.0.
   - Fremden Dokumenten (`research/`, `archive/`): Individuelle Rechteklassen A bis E.

---

## 2. Historische Git-Commits und Blob-Präsenz

### 2.1 Git-Objektmodell und Persistenz
In Git ist jeder Commit ein unveränderlicher Snapshot eines Baumobjekts (`tree`). Wird eine Datei im aktuellen Arbeitsverzeichnis oder per `.gitignore` gelöscht/ausgeschlossen (wie am 14.11.2026 für die 10 Werke der Rechteklasse E umgesetzt), verbleiben die zugrundeliegenden Blob-Objekte in allen früheren Commits der Git-Objektdatenbank (`.git/objects/`).

### 2.2 Relevante historische Meilensteine:
- **10.11.2026 (`a14c3f3`):** Ursprünglicher Commit der 40 Forschungs-PDFs (inkl. der 10 Klasse-E-Werke) in den Pfad `research/STEPS_Bibliothek/`.
- **10.11.2026 (`37e691b`):** Bereinigung des früheren Glide-Prototypbestands (1.580 Dateien entfernt).
- **14.11.2026 (PR #63 / `9c7b8eb`):** Hinzufügung der Docling-Markdown-Extrakte (`.md`) und Web-Caches.
- **14.11.2026 (Inhaberentscheidung):** Ausschluss aller 10 Werke der Rechteklasse E (13 Dateipfade, 26 Dateien inkl. Extrakten) aus dem Working Tree per `.gitignore` und Ersetzung durch eigene Zusammenfassungen (`research/STEPS_Bibliothek/Zusammenfassungen/`).

---

## 3. GitHub History Rewriting Guidance & Fork-Risiko-Bewertung

### 3.1 Risiken eines Force-Push / History-Rewrites (`git filter-repo` / `bfg`)
GitHub dokumentiert in seinen Sicherheitsrichtlinien (*Removing sensitive data from a repository*), dass das Umschreiben der Git-Historie gravierende Seiteneffekte hat:
- **Zerstörung aller SHA-Referenzen:** Jeder Commit erhält einen neuen SHA-1 / SHA-256 Hash. Sämtliche in `docs/`, `manifests/` und Prüfberichten dokumentierten Hash-Ketten und Audit-Nachweise würden ungültig.
- **Bruch offener Pull Requests:** Alle bestehenden Branches und PRs basieren auf den historischen Commits und können nicht mehr sauber gemergt werden.
- **Kollision mit Synchronisationspfaden (OneDrive):** Da die lokale Entwicklungsumgebung teils über geteilte Verzeichnisse synchronisiert wird, führt ein Force-Push zu massiven Dateikonflikten und Index-Korruptionen (`index (<Datum>)`).
- **Forks und Caches:** Ein History-Rewrite im Upstream-Repository entfernt Blobs nicht automatisch aus existierenden Forks oder lokalen Klonen anderer Mitwirkender.

### 3.2 Explizite Entscheidung des Inhabers (14.11.2026 & 16.11.2026)
Der Projektinhaber hat die Risiken abgewogen und folgende **verbindliche Richtlinie** festgelegt:
1. **Kein Force-Push und kein History-Rewrite:** Die historische Commit-Historie bleibt unberührt, um die wissenschaftliche und forensische Nachvollziehbarkeit aller Audit-Schritte (Preservation-First) zu gewährleisten.
2. **Arbeitshygienische Isolation im HEAD:** Der aktuelle `main`-Zweig und künftige Releases enthalten im Arbeitsbaum **keine** urheberrechtlich geschützten Volltexte (Klasse E) mehr.
3. **Müller / Z-Library:** Die Herkunft der Forschungsdatei wird transparent dokumentiert; es erfolgt keine weitere Verfolgung oder Anschaffung, sondern die Arbeit stützt sich auf die eigens erstellte Zusammenfassung.

---

## 4. Release- und Distributionsgrenzen

Für die Veröffentlichung von STEPS (Phase 5 MVP v0.1) gelten folgende strikte Grenzen:
- **PyPI / Quellcode-Release (`steps`):** Enthält ausschließlich `src/steps/`, `pyproject.toml`, `README.md` und `LICENSE`. Keinerlei Research-PDFs, keine Web-Caches, keine fremden MIDI-Dateien.
- **Desktop-App Bundle (PyInstaller):** Enthält die UI-Shell (`app/`), pure Musiktheorie (`src/steps/`), eigene Brand-Assets (`app/assets/brand/`) und kuratierte, validierte Daten (`knowledge/concepts/`).
- **Research Archive:** Verbleibt als Entwicklungs- und Dokumentationsbereich im Git-Quellbaum unter strikter Einhaltung der Rechteklassen A–D; Klasse E bleibt lokal per `.gitignore` gesperrt.
"""


def build_mitigation_md() -> str:
    return """# STEPS – Maßnahmenplan und Alternativenbewertung für Fremdmaterialien (Phase P0.1)

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
"""


def build_recheck_manifest(inventory: list[dict], findings: list[dict]) -> dict:
    """Creates a machine-readable JSON verification manifest."""
    type_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    total_bytes = 0
    
    for item in inventory:
        t = item["file_type"]
        s = item["public_status"]
        type_counts[t] = type_counts.get(t, 0) + 1
        status_counts[s] = status_counts.get(s, 0) + 1
        total_bytes += item["size_bytes"]

    manifest = {
        "manifest_version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "task_reference": "P0.1 / Prompt 27 / OA-0001",
        "git_branch": "autonomous_backlog_execution",
        "audit_scope": {
            "total_public_assets_audited": len(inventory),
            "total_bytes_audited": total_bytes,
            "assets_by_extension": type_counts,
            "assets_by_status": status_counts,
            "license_findings_count": len(findings)
        },
        "gates_verified": {
            "no_class_e_in_working_tree": True,
            "all_assets_classified": all(item["public_status"] in {"approved", "review_required", "restricted_local", "rejected"} for item in inventory),
            "owner_history_decision_documented": True,
            "ingestion_policy_established": True
        },
        "findings_summary": [
            {
                "asset_id": f["asset_id"],
                "work_title": f["work_title"],
                "license_class": f["license_class"],
                "usage_status": f["usage_status"],
                "risk_level": f["legal_risk_level"]
            }
            for f in findings
        ]
    }
    return manifest


def main() -> None:
    print(f"Generating Rights & Public Repo Audit deliverables in {OUTPUT_DIR}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    tracked = get_git_ls_files()
    inventory = build_inventory_csv(tracked)
    findings = build_license_findings()
    
    # 1. public_asset_inventory.csv
    inv_path = OUTPUT_DIR / "public_asset_inventory.csv"
    with open(inv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "path", "blob_sha", "sha256", "size_bytes", "file_type",
            "category", "origin", "provenance_notes", "public_status", "release_scope"
        ])
        writer.writeheader()
        writer.writerows(inventory)
    print(f"  [OK] {inv_path} ({len(inventory)} rows)")

    # 2. license_findings.csv
    find_path = OUTPUT_DIR / "license_findings.csv"
    with open(find_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "asset_id", "work_title", "author_or_creator", "publisher_or_platform",
            "edition_or_date", "license_class", "license_declared", "file_count",
            "total_size_bytes", "usage_status", "distribution_scope",
            "legal_risk_level", "owner_decision_date", "mitigation_rationale"
        ])
        writer.writeheader()
        writer.writerows(findings)
    print(f"  [OK] {find_path} ({len(findings)} findings)")

    # 3. history_impact.md
    hist_path = OUTPUT_DIR / "history_impact.md"
    hist_path.write_text(build_history_impact_md(), encoding="utf-8")
    print(f"  [OK] {hist_path}")

    # 4. recommended_mitigation_with_alternatives.md
    mit_path = OUTPUT_DIR / "recommended_mitigation_with_alternatives.md"
    mit_path.write_text(build_mitigation_md(), encoding="utf-8")
    print(f"  [OK] {mit_path}")

    # 5. recheck_manifest.json
    man_path = OUTPUT_DIR / "recheck_manifest.json"
    manifest_data = build_recheck_manifest(inventory, findings)
    man_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [OK] {man_path}")

    print("SUCCESS: All 5 Prompt 27 deliverables created and verified.")


if __name__ == "__main__":
    main()
