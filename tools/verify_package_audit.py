"""Static integrity checks for the STEPS independent audit package, NOT app tests."""
from __future__ import annotations
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
 'README.md','HOW_TO_IMPORT_IN_GITHUB.md',
 'docs/project/PROJECT_OVERVIEW.md',
 'docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md',
 'docs/audit/00_GESAMTBEWERTUNG_UND_METHODIK.md',
 'docs/audit/01_UNTERSUCHUNGSDIMENSIONEN.md',
 'docs/audit/02_KORREKTUREN_UND_WIDERSPRUECHE.md',
 'docs/audit/03_ALTERNATIVEN_UND_ENTSCHEIDUNGEN.md',
 'docs/audit/05_VALIDIERUNGSBERICHT.md',
 'docs/operations/EXECUTION_BACKLOG.md',
 'tools/audit/verify_glide_code_and_originals.py',
 'manifests/PACKAGE_FILES_SHA256.csv',
 'docs/product/PRODUCT_STRATEGY_AND_MVP.md',
 'docs/product/LEARNING_AND_EXPERIENCE.md',
 'docs/product/MARKET_AND_VALIDATION.md',
 'docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md',
 'docs/engineering/MUSIC_DOMAIN_AND_MIDI.md',
 'docs/engineering/DATA_STORAGE_AND_PORTABILITY.md',
 'docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md',
 'docs/governance/RIGHTS_SECURITY_AND_RELEASE.md',
 'docs/operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md',
 'docs/quality/VERIFICATION_PLAN_V2.md',
 'docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md',
 'manifests/REQUIREMENTS_TRACE_28.csv',
 'manifests/DEEP_RESEARCH_REFS.csv',
 'manifests/INVESTIGATION_COVERAGE_33_V2.csv',
 'manifests/GLIDE_94_MODULE_REUSE_AUDIT_V2.csv',
 'manifests/GLIDE_25_PACKAGES_AUDIT_V2.csv',
]

def csvrows(rel):
 with (ROOT / rel).open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def check():
    missing=[x for x in REQUIRED if not (ROOT / x).is_file()]
    if missing:raise AssertionError(f'Missing expected artifacts {missing}')
    req=csvrows('manifests/REQUIREMENTS_TRACE_28.csv')
    dims=csvrows('manifests/INVESTIGATION_COVERAGE_33_V2.csv')
    mods=csvrows('manifests/GLIDE_94_MODULE_REUSE_AUDIT_V2.csv')
    packs=csvrows('manifests/GLIDE_25_PACKAGES_AUDIT_V2.csv')
    refs=csvrows('manifests/DEEP_RESEARCH_REFS.csv')
    conflicts=csvrows('manifests/ORIGINAL_CONFLICTS_40.csv')
    gaps=csvrows('manifests/ORIGINAL_GAPS_34.csv')
    externals=csvrows('manifests/EXTERNAL_PRIMARY_REFERENCES.csv')
    assert len(req)==28 and len({x['requirement_id'] for x in req})==28
    assert len(dims)==33 and len({x['id'] for x in dims})==33
    assert len(mods)==94 and len(packs)==25 and len(refs)==7
    assert len(conflicts)==40 and len({x["id"] for x in conflicts})==40
    assert len(gaps)==34 and len({x["id"] for x in gaps})==34
    assert len(externals)==8
    prompts=sorted((ROOT/'prompts').glob('[0-9][0-9]_*.md'))
    assert len(prompts)==29,[x.name for x in prompts]
    assert [int(x.name[:2]) for x in prompts]==list(range(1,30))
    archived=sorted((ROOT/'archive/v1_prompts').glob('[0-9][0-9]_*.md'))
    assert len(archived)==24
    originals=list((ROOT/'source_archive').glob('*'))
    assert len(originals)==8
    for x in originals: assert x.is_file() and x.stat().st_size>0
    bad=[];links=0
    for f in ROOT.rglob('*.md'):
        if any(x in f.relative_to(ROOT).parts for x in ('source_archive','archive')):continue
        content=f.read_text(encoding='utf-8')
        for url in re.findall(r'\]\(([^)]+)\)',content):
            if url.startswith(('https:','http:','mailto:','#')):continue
            rel=url.split('#',1)[0].replace('%20',' ')
            if not rel:continue
            links+=1
            if not (f.parent/rel).exists():bad.append((str(f.relative_to(ROOT)),url))
    if bad:raise AssertionError(f'Broken links count={len(bad)} sample={bad[:10]}')
    assert not list(ROOT.rglob('*.pdf')),'No external book PDFs belong in audit ZIP'
    assert not list(ROOT.rglob('*.ttf')),'Never bundle font binaries'
    assert not list(ROOT.rglob('*.mid')),'No private/external MIDI files in audit ZIP'
    # Recomputed in final package build. The manifest excludes itself to avoid a
    # recursive hash definition, and covers the review-only publish overlay too.
    listed = csvrows('manifests/PACKAGE_FILES_SHA256.csv')
    lookup = {row['relative_path']: row for row in listed}
    actual = {p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*')
              if p.is_file() and p.relative_to(ROOT).as_posix() != 'manifests/PACKAGE_FILES_SHA256.csv'}
    assert lookup.keys() == actual.keys(), (len(lookup),len(actual),list(actual.keys()-lookup.keys())[:8])
    for rel, p in actual.items():
        row = lookup[rel]
        assert str(p.stat().st_size) == row['bytes'], rel
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256'], rel
    return {'status':'STATIC_PACKAGE_PASS','date':'2026-11-10','requirements':len(req),
            'dimensions':len(dims),'modules':len(mods),'packages':len(packs),
            'research_references':len(refs),'external_primary_references':len(externals),
            'historical_conflicts':len(conflicts),'historical_gaps':len(gaps),'new_prompts':len(prompts),
            'original_v1_prompts_archived':len(archived),'uploaded_originals':len(originals),
            'new_internal_md_links_checked':links,'total_package_files_with_manifest':len(listed)+1,
            'app_tests_executed':0,'knowledge_claim_reviews_executed':0,
            'native_app_tests_executed':0,'license_legal_approvals_executed':0}

if __name__=='__main__':
    print(json.dumps(check(),ensure_ascii=False,indent=2))
