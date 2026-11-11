#!/usr/bin/env python3
"""
STEPS Master Inventory Builder (Phase A)
Indexes every active file in the repository (excluding .git and __pycache__),
determines SHA-256, content type, domain, status, authority, quality, and action.
"""

import os
import sys
import hashlib
import csv

def get_sha256(path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return f"ERR:{e}"

def classify_file(rel_path):
    p = rel_path.replace("\\", "/").lower()
    ext = os.path.splitext(p)[1]
    
    # Content type
    if ext == '.md':
        content_type = 'Markdown-Dokumentation'
    elif ext == '.csv':
        content_type = 'Strukturierte Tabelle / CSV'
    elif ext == '.json':
        content_type = 'Strukturierte Daten / JSON'
    elif ext in ('.yaml', '.yml'):
        content_type = 'Konfiguration / YAML'
    elif ext in ('.py', '.pyw'):
        content_type = 'Python-Quellcode'
    elif ext == '.pdf':
        content_type = 'Fachliteratur / PDF'
    elif ext == '.mid':
        content_type = 'Standard-MIDI-Datei'
    elif ext in ('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp', '.avif'):
        content_type = 'Grafik / Medien'
    elif ext in ('.ttf', '.woff', '.woff2'):
        content_type = 'Schriftart / Asset'
    elif ext in ('.txt', '.patch', '.rst'):
        content_type = 'Text / Patch'
    else:
        content_type = f"Sonstiges ({ext or 'none'})"
        
    # Domain / Fachgebiet
    if p.startswith('src/glide-v3.53'):
        domain = 'GLIDE_LEGACY_CORE'
    elif p.startswith('src/steps'):
        domain = 'STEPS_THEORY_CORE'
    elif p.startswith('decisions/'):
        domain = 'ARCHITEKTUR_ADR'
    elif p.startswith('knowledge/concepts/chords') or p.startswith('knowledge/concepts/intervals'):
        domain = 'M01_M04_PITCH_INTERVAL_CHORD'
    elif p.startswith('knowledge/concepts/progressions'):
        domain = 'M05_PROGRESSION_CADENCE'
    elif p.startswith('knowledge/concepts/styles'):
        domain = 'M07_M08_M09_RHYTHM_DRUM_GENRE'
    elif p.startswith('knowledge/instruments'):
        domain = 'M10_PIANO_PRACTICE'
    elif p.startswith('knowledge/relations'):
        domain = 'ONTOLOGIE_GRAPH_RELATIONS'
    elif p.startswith('knowledge/research/golden_cases') or p.startswith('tests/golden_cases'):
        domain = 'M01_M12_GOLDEN_CASES'
    elif p.startswith('tests/'):
        domain = 'TESTS_QUALITY_ASSURANCE'
    elif p.startswith('scripts/'):
        domain = 'AUTOMATION_TOOLING'
    elif p.startswith('research/steps_bibliothek'):
        domain = 'FORSCHUNGSARCHIV_BIBLIOTHEK'
    elif p.startswith('docs/'):
        domain = 'PROJEKT_DOKUMENTATION'
    else:
        domain = 'ALLGEMEIN_PROJEKT'
        
    # Status
    if 'archive' in p or 'legacy' in p or 'gesamtpruefung_v4' in p or p.startswith('research/steps_bibliothek'):
        status = 'HISTORISCH_ARCHIVIERT'
    elif p.startswith('src/glide-v3.53'):
        status = 'ISOLIERT_GLIDE'
    elif p.startswith('tests/') or p.startswith('scripts/') or p.startswith('knowledge/') or p.startswith('decisions/'):
        status = 'AKTIV_KANONISCH'
    else:
        status = 'AKTIV_PROJEKT'
        
    # Authority
    if p.startswith('knowledge/concepts/') or p.startswith('knowledge/relations/') or p.startswith('decisions/') or p == 'agents.md':
        authority = 'KANONISCH'
    elif p.startswith('knowledge/research/') or p.startswith('tests/'):
        authority = 'ABGELEITET_VERIFIKATION'
    elif p.startswith('src/glide-v3.53'):
        authority = 'GLIDE_REFERENZ'
    elif p.startswith('research/'):
        authority = 'EXTERN_FORSCHUNG'
    else:
        authority = 'PROJEKT_BASIS'
        
    # Quality state
    if p.startswith('src/glide-v3.53'):
        quality = 'ISOLIERT_UNVERAENDERT'
    elif p in ('decisions/decision_register.md', 'knowledge/relations/music_concept_relations.csv', 'knowledge/concepts/progressions/chord_progression_reference_library.md'):
        quality = 'VERIFIZIERT_KANONISCH'
    elif p.startswith('research/steps_bibliothek') and ext in ('.pdf', '.mid'):
        quality = 'METADATEN_PROPRIETAER'
    elif p.startswith('tests/') or p.startswith('scripts/'):
        quality = 'VERIFIZIERT_AUTOMATISIERT'
    else:
        quality = 'PRUEFSTAND'
        
    # Action need
    if p.startswith('src/glide-v3.53'):
        action = 'ISOLIERT_LASSEN_P2_4'
    elif p.startswith('knowledge/') or p.startswith('decisions/') or p.startswith('tests/'):
        action = 'PRUEFEN_UND_SYSTEMATISCH_AUSBAUEN'
    elif p.startswith('research/steps_bibliothek'):
        action = 'RECHTE_PRUEFEN_METADATEN_PFLEGEN'
    else:
        action = 'BEIBEHALTEN'
        
    return content_type, domain, status, authority, quality, action

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_csv = os.path.join(repo_root, "knowledge", "research", "01_BESTANDSINVENTAR.csv")
    out_md = os.path.join(repo_root, "knowledge", "research", "01_BESTANDSINVENTAR.md")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    
    rows = []
    domain_counts = {}
    type_counts = {}
    status_counts = {}
    authority_counts = {}
    quality_counts = {}
    
    for root, dirs, files in os.walk(repo_root):
        if '.git' in dirs:
            dirs.remove('.git')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_root)
            c_type, dom, stat, auth, qual, act = classify_file(rel_path)
            size = os.path.getsize(full_path)
            
            # For non-Glide files, calculate hash
            if not rel_path.startswith("src\\glide-v3.53") and size < 20000000:
                sha = get_sha256(full_path)
            else:
                sha = "GLIDE_OR_OVERSIZED"
                
            row = {
                'dateipfad': rel_path.replace("\\", "/"),
                'groesse_bytes': size,
                'sha256': sha,
                'inhaltstyp': c_type,
                'fachgebiet': dom,
                'status': stat,
                'autoritaet': auth,
                'qualitaetszustand': qual,
                'handlungsbedarf': act
            }
            rows.append(row)
            
            domain_counts[dom] = domain_counts.get(dom, 0) + 1
            type_counts[c_type] = type_counts.get(c_type, 0) + 1
            status_counts[stat] = status_counts.get(stat, 0) + 1
            authority_counts[auth] = authority_counts.get(auth, 0) + 1
            quality_counts[qual] = quality_counts.get(qual, 0) + 1
            
    # Write CSV
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'dateipfad', 'groesse_bytes', 'sha256', 'inhaltstyp',
            'fachgebiet', 'status', 'autoritaet', 'qualitaetszustand', 'handlungsbedarf'
        ])
        writer.writeheader()
        writer.writerows(rows)
        
    # Write Markdown summary
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write("# STEPS – Vollständiges Bestandsinventar (Phase A Audit)\n\n")
        f.write(f"**Gesamtzahl inventarisierter Dateien:** {len(rows)}\n\n")
        
        f.write("## 1. Verteilung nach Fachgebiet / Domäne\n\n")
        f.write("| Fachgebiet | Dateianzahl | Anteil (%) |\n|---|---:|---:|\n")
        for dom, cnt in sorted(domain_counts.items(), key=lambda x: -x[1]):
            f.write(f"| `{dom}` | {cnt} | {cnt/len(rows)*100:.1f} % |\n")
            
        f.write("\n## 2. Verteilung nach Inhaltstyp\n\n")
        f.write("| Inhaltstyp | Dateianzahl | Anteil (%) |\n|---|---:|---:|\n")
        for ct, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            f.write(f"| `{ct}` | {cnt} | {cnt/len(rows)*100:.1f} % |\n")
            
        f.write("\n## 3. Verteilung nach Status & Autorität\n\n")
        f.write("| Status / Autorität | Dateianzahl | Anteil (%) |\n|---|---:|---:|\n")
        for st, cnt in sorted(status_counts.items(), key=lambda x: -x[1]):
            f.write(f"| Status: `{st}` | {cnt} | {cnt/len(rows)*100:.1f} % |\n")
        for au, cnt in sorted(authority_counts.items(), key=lambda x: -x[1]):
            f.write(f"| Autorität: `{au}` | {cnt} | {cnt/len(rows)*100:.1f} % |\n")
            
        f.write("\n## 4. Qualitätszustand & Handlungsbedarf\n\n")
        f.write("| Qualitätszustand | Dateianzahl | Anteil (%) |\n|---|---:|---:|\n")
        for q, cnt in sorted(quality_counts.items(), key=lambda x: -x[1]):
            f.write(f"| `{q}` | {cnt} | {cnt/len(rows)*100:.1f} % |\n")
            
        f.write("\n---\n*Generiert durch `scripts/build_master_inventory.py`*\n")

    print(f"Inventory successfully built: {len(rows)} files indexed.")
    print(f"CSV: {out_csv}")
    print(f"MD:  {out_md}")

if __name__ == "__main__":
    main()
