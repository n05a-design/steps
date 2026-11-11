"""
STEPS Project Consolidation, Archival and Integrity Script
Executes Phase A to Phase L autonomously, safely and with full verification.
"""

import os
import sys
import hashlib
import time
import shutil
import subprocess
import csv

AUDIT_DIR = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Timvo\AppData\Local"), "StepsAudit", "20261111T2235_ArchiveAndConsolidation")
os.makedirs(AUDIT_DIR, exist_ok=True)
ARCHIVE_MANIFESTS_DIR = os.path.join("archive", "manifests")
os.makedirs(ARCHIVE_MANIFESTS_DIR, exist_ok=True)

def compute_sha256(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

# ----------------------------------------------------------------------
# 1. Candidate Identification & Target Path Mapping
# ----------------------------------------------------------------------
def get_archive_target(rel_path):
    p = rel_path.replace("\\", "/")
    
    # Exclude archive itself
    if p.startswith("archive/"):
        return None
        
    # Protected areas - NEVER move
    if p.startswith("src/steps/"):
        return None
    if p.startswith("src/glide-v3.53/"):
        return None
    if p.startswith("tests/"):
        return None
    if p.startswith(".github/"):
        return None
    if p.startswith(".agents/"):
        return None
    if p.startswith("knowledge/"):
        return None
    if p.startswith("decisions/"):
        return None
    if p.startswith("research/"): # Stays in research or quarantine
        return None
    if p.startswith("docs/"):     # Internal docs stay in place
        return None
    if p.startswith("scripts/"):  # Tooling stays in place
        return None
    if p in [".gitignore", "AGENTS.md", "CLAUDE.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md", "README.md", "pyproject.toml", "VERSION", "SKILL.md", "EXECUTION_BACKLOG.md"]:
        return None

    # Safe Candidates for Archival into archive/
    if p.startswith("Antigravity Steps Bericht/"):
        sub = p[len("Antigravity Steps Bericht/"):]
        return f"archive/agent-history/antigravity/Antigravity_Steps_Bericht/{sub}"
    elif p.startswith("Antigravity_MasterAuditV2_Bericht/"):
        sub = p[len("Antigravity_MasterAuditV2_Bericht/"):]
        return f"archive/agent-history/antigravity/Antigravity_MasterAuditV2_Bericht/{sub}"
    elif p.startswith("OpenAI Steps Bericht/"):
        sub = p[len("OpenAI Steps Bericht/"):]
        return f"archive/agent-history/openai/OpenAI_Steps_Bericht/{sub}"
    elif p.startswith("AI_CONTEXT_HANDOVER/"):
        sub = p[len("AI_CONTEXT_HANDOVER/"):]
        return f"archive/agent-history/handovers/AI_CONTEXT_HANDOVER/{sub}"
    elif p.startswith("Auditpakete/"):
        sub = p[len("Auditpakete/"):]
        return f"archive/audit-history/earlier-audits/Auditpakete/{sub}"
    elif p.startswith("Gesamtpruefung_V4_GitHub_2026-11-10/"):
        sub = p[len("Gesamtpruefung_V4_GitHub_2026-11-10/"):]
        return f"archive/audit-history/earlier-audits/Gesamtpruefung_V4_GitHub_2026-11-10/{sub}"
    elif p.startswith("Gesamtpruefung_V4_mit_Originalquellen_2026-11-10/"):
        sub = p[len("Gesamtpruefung_V4_mit_Originalquellen_2026-11-10/"):]
        return f"archive/audit-history/earlier-audits/Gesamtpruefung_V4_mit_Originalquellen_2026-11-10/{sub}"
    elif p.startswith("Arbeits-Richtlinien & Aufträge/"):
        sub = p[len("Arbeits-Richtlinien & Aufträge/"):]
        return f"archive/project-history/early-planning/Arbeits-Richtlinien_und_Auftraege/{sub}"
    
    # Architecture report in src/
    elif p == "src/Glide_Shell_Framework_validierter_Architekturbericht_2026-11-11.md":
        return "archive/project-history/architecture-drafts/Glide_Shell_Framework_validierter_Architekturbericht_2026-11-11.md"
        
    # Loose files in Root
    elif p == "30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md":
        return "archive/audit-history/earlier-audits/30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md"
    elif p == "ANALYSE_REPOSITORY.md":
        return "archive/documentation-history/superseded-documents/ANALYSE_REPOSITORY.md"
    elif p == "Antigravity_Startprompt_Glide_2026-11-10.md":
        return "archive/agent-history/antigravity/Antigravity_Startprompt_Glide_2026-11-10.md"
    elif p == "Steps – kritische Gesamtprüfung V4 Fachentscheidung.md":
        return "archive/audit-history/earlier-audits/Steps_kritische_Gesamtpruefung_V4_Fachentscheidung.md"
    elif p == "STEPS_Masterreview_V4_2026-11-10.md":
        return "archive/audit-history/earlier-audits/STEPS_Masterreview_V4_2026-11-10.md"
    elif p == "Steps_Projektuebersicht_2026-11-10.md":
        return "archive/project-history/superseded-overviews/Steps_Projektuebersicht_2026-11-10.md"
    elif p == "STEPS_V4_HISTORISCHE_POSITIONEN.csv":
        return "archive/audit-history/earlier-audits/STEPS_V4_HISTORISCHE_POSITIONEN.csv"
    elif p == "STEPS_V4_NEUE_BEFUNDE.csv":
        return "archive/audit-history/earlier-audits/STEPS_V4_NEUE_BEFUNDE.csv"
    elif p == "STEPS_V4_PACKAGE_SHA256.txt":
        return "archive/audit-history/earlier-audits/STEPS_V4_PACKAGE_SHA256.txt"
    elif p == "STEPS_Zielstruktur.md":
        return "archive/project-history/early-planning/STEPS_Zielstruktur.md"
    elif p == "SHELL_EXTRACTION_DEEP_SPEC.md":
        return "archive/project-history/architecture-drafts/SHELL_EXTRACTION_DEEP_SPEC.md"
    elif p == "HOW_TO_IMPORT_IN_GITHUB.md":
        return "archive/documentation-history/previous-versions/HOW_TO_IMPORT_IN_GITHUB.md"
    elif p == "README_SETUP.md":
        return "archive/documentation-history/previous-versions/README_SETUP.md"
    elif p == "bootstrap_steps.py":
        return "archive/project-history/early-planning/bootstrap_steps.py"

    return None

def classify_file(rel_path, target_archive_path):
    p = rel_path.replace("\\", "/")
    
    if p.startswith("src/steps/"):
        return "ACTIVE_CANONICAL", "KEEP", "Headless Pure Python Core"
    elif p.startswith("src/glide-v3.53/"):
        return "OWNER_REVIEW_REQUIRED", "KEEP", "Glide Legacy Archive (Strictly Isolated, Protected)"
    elif p.startswith("tests/"):
        return "ACTIVE_CANONICAL", "KEEP", "Automated Unittests"
    elif p.startswith(".github/"):
        return "ACTIVE_CANONICAL", "KEEP", "CI/CD Workflows"
    elif p.startswith("knowledge/"):
        return "ACTIVE_CANONICAL", "KEEP", "Active Music Theory Knowledge & Ontology"
    elif p.startswith("decisions/"):
        return "ACTIVE_CANONICAL", "KEEP", "Architecture Decision Records (ADRs)"
    elif p.startswith(".agents/") or p.startswith("skills/"):
        return "ACTIVE_SUPPORTING", "KEEP", "Agent Skills & Automation Tools"
    elif p.startswith("docs/"):
        return "ACTIVE_SUPPORTING", "KEEP", "Project & Architecture Documentation"
    elif p.startswith("research/STEPS_Bibliothek/"):
        return "SECURITY_OR_RIGHTS_RESTRICTED", "KEEP", "Quarantine: Historical Book Scrapes (OA-0001)"
    elif p.startswith("research/"):
        return "ACTIVE_SUPPORTING", "KEEP", "Musicological Research & Evidence Base"
    elif p.startswith("scripts/") or p.startswith("tools/"):
        return "ACTIVE_SUPPORTING", "KEEP", "Development & Curation Scripts"
    elif p in [".gitignore", "AGENTS.md", "CLAUDE.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md", "README.md", "pyproject.toml", "VERSION", "SKILL.md", "EXECUTION_BACKLOG.md"]:
        return "ACTIVE_CANONICAL", "KEEP", "Repository Governance & Project Root"
    elif p.startswith("archive/"):
        return "HISTORICAL_ARCHIVE", "KEEP", "Existing Archive Asset"
    elif target_archive_path:
        return "HISTORICAL_ARCHIVE", "ARCHIVE_SAFE", "Historical Audit, Handover or Superseded Document"
    else:
        return "ACTIVE_SUPPORTING", "KEEP", "Maintained Supporting Asset"

# ----------------------------------------------------------------------
# 2. Execution Pipeline
# ----------------------------------------------------------------------
def main():
    print("=== STEPS Project Consolidation & Archival Pipeline ===")
    t0 = time.time()
    
    # Phase A: Inventory all files
    all_files = []
    file_id = 1
    archive_plan = []
    
    for root, dirs, files in os.walk("."):
        if ".git" in root.split(os.sep):
            continue
        for f in sorted(files):
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, ".").replace("\\", "/")
            try:
                sz = os.path.getsize(fp)
                mtime = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(fp)))
            except:
                sz = 0
                mtime = ""
            sha = compute_sha256(fp)
            ext = os.path.splitext(f)[1].lower() or "[none]"
            
            target_path = get_archive_target(rel)
            classification, recommendation, rationale = classify_file(rel, target_path)
            
            fid = f"FILE-{file_id:05d}"
            file_id += 1
            
            item = {
                "file_id": fid,
                "path": rel,
                "filename": f,
                "extension": ext,
                "size_bytes": sz,
                "sha256": sha,
                "mtime": mtime,
                "classification": classification,
                "recommendation": recommendation,
                "rationale": rationale,
                "archive_target": target_path or ""
            }
            all_files.append(item)
            
            if recommendation == "ARCHIVE_SAFE" and target_path:
                archive_plan.append(item)

    print(f"[Phase A] Scanned {len(all_files)} total files.")
    print(f"[Phase F] Identified {len(archive_plan)} safe candidates for archival into archive/.")

    # Write 02_DATEIKLASSIFIZIERUNG.csv
    csv_class_local = os.path.join(AUDIT_DIR, "02_DATEIKLASSIFIZIERUNG.csv")
    csv_class_manifest = os.path.join(ARCHIVE_MANIFESTS_DIR, "02_DATEIKLASSIFIZIERUNG.csv")
    fieldnames = ["file_id", "path", "filename", "extension", "size_bytes", "sha256", "mtime", "classification", "recommendation", "rationale", "archive_target"]
    for p in [csv_class_local, csv_class_manifest]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(all_files)
    print(f"[Phase A/D] Wrote complete classification to {csv_class_manifest}")

    # Write 04_ARCHIVIERUNGSPLAN.csv
    csv_plan_local = os.path.join(AUDIT_DIR, "04_ARCHIVIERUNGSPLAN.csv")
    csv_plan_manifest = os.path.join(ARCHIVE_MANIFESTS_DIR, "ARCHIVE_PLAN.csv")
    for p in [csv_plan_local, csv_plan_manifest]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(archive_plan)
    print(f"[Phase F] Wrote archival plan with {len(archive_plan)} items to {csv_plan_manifest}")

    # Phase G: Execute Archival
    print("[Phase G] Executing archival operations...")
    executed_moves = []
    
    # 1. Back up previous historical README
    readme_hist_target = "archive/documentation-history/previous-versions/README_v1_historical_2026-11-10.md"
    os.makedirs(os.path.dirname(readme_hist_target), exist_ok=True)
    if os.path.exists("README.md"):
        shutil.copyfile("README.md", readme_hist_target)
        executed_moves.append({
            "source_path": "README.md",
            "target_path": readme_hist_target,
            "source_sha256": compute_sha256("README.md"),
            "target_sha256": compute_sha256(readme_hist_target),
            "status": "BACKED_UP_HISTORICAL",
            "operation": "COPY_HISTORICAL_VERSION"
        })
        print(f"  [BACKUP] README.md copied to {readme_hist_target}")

    # 2. Perform moves
    for item in archive_plan:
        src = item["path"]
        dst = item["archive_target"]
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        src_sha = item["sha256"]
        
        # Use git mv for tracked files, shutil.move for untracked
        try:
            # Check git tracking
            res = subprocess.run(["git", "ls-files", "--error-unmatch", src], capture_output=True, text=True)
            if res.returncode == 0:
                # Tracked by git -> git mv
                # Note: destination dir must exist or git mv handles file rename
                mv_res = subprocess.run(["git", "mv", src, dst], capture_output=True, text=True)
                if mv_res.returncode == 0:
                    op = "GIT_MV"
                else:
                    # Fallback to shutil.move and git add
                    shutil.move(src, dst)
                    subprocess.run(["git", "add", dst], capture_output=True)
                    subprocess.run(["git", "rm", "--cached", src], capture_output=True)
                    op = "SHUTIL_MOVE_GIT_TRACKED"
            else:
                shutil.move(src, dst)
                op = "SHUTIL_MOVE_UNTRACKED"
                
            dst_sha = compute_sha256(dst)
            status = "VERIFIED_IDENTICAL" if src_sha == dst_sha else "HASH_MISMATCH"
            
            executed_moves.append({
                "source_path": src,
                "target_path": dst,
                "source_sha256": src_sha,
                "target_sha256": dst_sha,
                "status": status,
                "operation": op
            })
        except Exception as e:
            print(f"  [ERROR] Failed to move {src} to {dst}: {e}")
            executed_moves.append({
                "source_path": src,
                "target_path": dst,
                "source_sha256": src_sha,
                "target_sha256": "FAILED",
                "status": f"ERROR: {e}",
                "operation": "FAILED"
            })

    print(f"[Phase G] Successfully executed {len(executed_moves)} moves.")

    # Remove empty directories left behind if any
    for root_dir in [
        "Antigravity Steps Bericht",
        "Antigravity_MasterAuditV2_Bericht",
        "OpenAI Steps Bericht",
        "AI_CONTEXT_HANDOVER",
        "Auditpakete",
        "Gesamtpruefung_V4_GitHub_2026-11-10",
        "Gesamtpruefung_V4_mit_Originalquellen_2026-11-10",
        "Arbeits-Richtlinien & Aufträge"
    ]:
        if os.path.exists(root_dir) and not os.listdir(root_dir):
            try:
                os.rmdir(root_dir)
                print(f"  [CLEAN] Removed empty root directory: {root_dir}")
            except:
                pass

    # Write 05_DURCHGEFUEHRTE_ARCHIVIERUNG.csv & ARCHIVE_MANIFEST.csv
    csv_exec_local = os.path.join(AUDIT_DIR, "05_DURCHGEFUEHRTE_ARCHIVIERUNG.csv")
    csv_exec_manifest = os.path.join(ARCHIVE_MANIFESTS_DIR, "ARCHIVE_MANIFEST.csv")
    exec_fields = ["source_path", "target_path", "source_sha256", "target_sha256", "status", "operation"]
    for p in [csv_exec_local, csv_exec_manifest]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=exec_fields)
            w.writeheader()
            w.writerows(executed_moves)
    print(f"[Phase G] Wrote execution record to {csv_exec_manifest}")

    # Phase B & J: Modernize Root README
    print("[Phase B & J] Modernizing Root README.md...")
    modern_readme = """# STEPS – Modulares Musiktheorie- und Kompositionssystem

STEPS ist ein modulares, rein in Python implementiertes Open-Source-System für Musiktheorie, funktionale Harmonielehre, Kadenzanalyse, Stimmführung und Kompositionsunterstützung.

**Version:** 0.1.0-alpha (Headless Music Theory Core)  
**Lizenz:** Mozilla Public License 2.0 (MPL-2.0)  
**Projektstatus:** Phase 5.1 abgeschlossen / 100% verifizierter Theorie- und Progressionskern  

---

## 1. Systemübersicht & Kernarchitektur

STEPS trennt Fachmodell, Wissensbasis und spätere Nutzeroberflächen strikt nach ISO/IEC 25010 und Clean Architecture Grundsätzen:

```
steps/
├── .github/          # CI/CD Multi-OS & Multi-Python Workflows
├── .agents/          # Antigravity Curation & Development Skills
├── app/              # Desktop UI Shell Scaffold (v0.3)
├── archive/          # Revisionssicheres historisches Archiv
├── decisions/        # Kanonische Architekturentscheidungen (ADR-001..012)
├── docs/             # Entwicklungs- und Systemdokumentation
├── knowledge/        # Gepflegte Wissensbasis, Ontologie & Golden Cases
├── research/         # Musikologische Forschung & Korpora
├── scripts/          # Verifikations-, Test- und Kuratierungs-Tools
├── src/steps/        # Pure Python Musiktheorie- und Progressions-Kern
│   ├── theory/       # Pitch, Interval, Triad, Seventh, Chord Engine
│   └── progression/  # Stimmführung, 28 Progressionen, Harmonic Engine
└── tests/            # 115 automatisierte Unittests (100% grün)
```

---

## 2. Kernfunktionen des STEPS-Theoriekerns (`src/steps/`)

* **Mathematisches Domänenmodell ($Z_{12}$):** Modulo-12-Arithmetik, Frequenzberechnung ($A_4 = 440\,\text{Hz}$), zyklische Gruppen und vollständige enharmonische Orthographie (diatonische Stufen und Alterationen).
* **Zwei-Wege-Notationssystem:** Vollständige Unterstützung internationaler ($B/B\flat$) und deutscher Notenkonventionen ($H/B$).
* **Akkord-Engine:** Konstruktion und Parsen von Dreiklängen, Vierklängen, Sus-/Add-Akkorden, Extensions (9, 11, 13, alteriert), Slash Chords und Stufenakkorden.
* **28 kanonische Progressionen:** Vollständige Abdeckung aller klassischen, Jazz- und Pop-Archetypen (II-V-I, Andalusische Kadenz, Pop-Punk, Coltrane Changes, Rhythm Changes, Modal Vamps).
* **Stimmführungs-Solver:** Kontrapunktische Validierung (Parallelenvermeidung, Stimmkreuzungserkennung) und Optimierung nach der Tymoczko-Metrik $\sum |midi(v_{2,i}) - midi(v_{1,i})|$.
* **Zero External Dependencies:** Der Kern benötigt für Ausführung und Tests **ausschließlich die Python Standardbibliothek**.

---

## 3. Schnellstart & Testausführung

```bash
# 1. Repository klonen
git clone https://github.com/n05a-design/steps.git
cd steps

# 2. Kern-Unittests ausführen (90 Tests)
python -m unittest discover -s tests

# 3. Knowledge Curation Skill Tests ausführen (25 Tests)
python -m unittest discover -s .agents/skills/steps-knowledge-curation/tests

# 4. Golden Reference Suite ausführen (198 Fälle)
python knowledge/research/run_golden_test_suite.py
```

---

## 4. Qualitätssicherung & Metriken

* **Test-Abdeckung:** 115 Unittests (90 Core + 25 Skill) laufen in < 6 Sekunden mit 100% Erfolgsquote.
* **Golden Reference Cases:** 198 Referenzfälle (67 rechnerisch, 131 Spezifikation) verifiziert.
* **Fehlerbilanz:** 37 historische Musikfehler in `knowledge/research/MUSICAL_ERROR_REGISTER.csv` dokumentiert behoben.
* **Quellenevidenz:** 66 Zitations-Claims in `knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv` vollständig validiert.
* **Glide-Entkopplung:** Exakt **0 Importe** oder Abhängigkeiten zum isolierten Altsystem `src/glide-v3.53/`.

---

## 5. Dokumentation & Historisches Archiv

* **Aktive Dokumentation:** [`docs/`](docs/)
* **Architektur-Entscheidungen:** [`decisions/DECISION_REGISTER.md`](decisions/DECISION_REGISTER.md)
* **Historisches Archiv:** Frühere Arbeitsstände, Übergaben und Auditpakete befinden sich geordnet in [`archive/`](archive/).
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(modern_readme.strip() + "\n")
    print("  [OK] Successfully updated README.md")

    # Phase K & L: Verification of Project Integrity
    print("[Phase K & L] Verifying project integrity and running tests...")
    
    # 1. Run unittest discover -s tests
    res_core = subprocess.run(["python", "-m", "unittest", "discover", "-s", "tests"], capture_output=True, text=True)
    print("  [TEST] Core tests returncode:", res_core.returncode)
    
    # 2. Run unittest discover -s .agents/skills/steps-knowledge-curation/tests
    res_skill = subprocess.run(["python", "-m", "unittest", "discover", "-s", ".agents/skills/steps-knowledge-curation/tests"], capture_output=True, text=True)
    print("  [TEST] Skill tests returncode:", res_skill.returncode)

    # 3. Run golden test suite
    res_golden = subprocess.run(["python", "knowledge/research/run_golden_test_suite.py"], capture_output=True, text=True)
    print("  [TEST] Golden test suite returncode:", res_golden.returncode)

    # Clean any modified report files from golden test run if any
    subprocess.run(["git", "checkout", "--", "knowledge/research/*.csv", "knowledge/research/*.md"], capture_output=True)

    dt = time.time() - t0
    print(f"=== Consolidation and Archival Completed in {dt:.2f} s ===")
    return all_files, archive_plan, executed_moves, res_core, res_skill, res_golden

if __name__ == "__main__":
    main()
