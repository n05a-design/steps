# STEPS – vollständige vorgeschlagene Zielstruktur

Dies ist die **ergänzte Zielarchitektur** des Vorbereitungspakets. `README.md` in Fachverzeichnissen sind Platzhalter mit Zuständigkeit, **keine Implementierungsnachweise**. Historische Dateien bleiben teils vorerst in ihren alten Pfaden (siehe Migrationskonzept).

```text
steps/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   ├── workflows/
│   │   └── structure-check.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── app/
│   ├── adapters/
│   │   └── README.md
│   ├── audio/
│   │   └── README.md
│   ├── core/
│   │   └── README.md
│   ├── ui/
│   │   └── README.md
│   └── README.md
├── decisions/
│   ├── 0000-ADR-template.md
│   └── README.md
├── design/
│   ├── assets/
│   │   └── README.md
│   ├── brand/
│   │   └── README.md
│   ├── components/
│   │   └── README.md
│   ├── references/
│   │   └── README.md
│   ├── tokens/
│   │   └── README.md
│   ├── wireframes/
│   │   └── README.md
│   └── README.md
├── docs/
│   ├── architecture/
│   │   ├── architecture.md
│   │   ├── legacy-mapping.md
│   │   ├── migration.md
│   │   └── README.md
│   ├── handover/
│   │   ├── HANDOVER_CHECKLIST.md
│   │   └── README.md
│   ├── project/
│   │   ├── originals/
│   │   │   └── README.md
│   │   ├── overview/
│   │   │   └── README.md
│   │   ├── provenance/
│   │   │   └── README.md
│   │   ├── technical-appendix/
│   │   │   └── README.md
│   │   └── README.md
│   ├── roadmap/
│   │   └── README.md
│   ├── system_reuse/
│   │   ├── GLIDE.md
│   │   └── README.md
│   ├── theory/
│   │   └── README.md
│   ├── user/
│   │   └── README.md
│   └── README.md
├── knowledge/
│   ├── concepts/
│   │   ├── chords/
│   │   │   └── README.md
│   │   ├── harmony/
│   │   │   └── README.md
│   │   ├── intervals/
│   │   │   └── README.md
│   │   ├── progressions/
│   │   │   └── README.md
│   │   ├── scales/
│   │   │   └── README.md
│   │   ├── styles/
│   │   │   └── README.md
│   │   ├── voice_leading/
│   │   │   └── README.md
│   │   └── README.md
│   ├── corpora/
│   │   └── README.md
│   ├── examples/
│   │   └── README.md
│   ├── glossary/
│   │   └── README.md
│   ├── legacy/
│   │   ├── MAPPING.md
│   │   └── README.md
│   ├── relations/
│   │   └── README.md
│   ├── sources/
│   │   ├── extracted/
│   │   │   └── README.md
│   │   ├── README.md
│   │   ├── registry.yaml
│   │   └── RIGHTS_POLICY.md
│   └── README.md
├── research/
│   ├── ableton/
│   │   └── README.md
│   ├── bibliography/
│   │   └── README.md
│   ├── competitors/
│   │   └── README.md
│   ├── gaps/
│   │   ├── OPEN_GAPS.md
│   │   └── README.md
│   ├── notes/
│   │   └── README.md
│   ├── papers/
│   │   └── README.md
│   ├── production/
│   │   ├── drums/
│   │   │   └── README.md
│   │   └── README.md
│   └── README.md
├── schemas/
│   ├── analysis.schema.json
│   ├── chord.schema.json
│   ├── concept.schema.json
│   ├── progression.schema.json
│   ├── README.md
│   └── source.schema.json
├── skills/
│   ├── music-harmony-coach/
│   │   └── README.md
│   └── README.md
├── src/
│   └── steps/
│       ├── models/
│       │   └── README.md
│       ├── ports/
│       │   └── README.md
│       ├── progression/
│       │   └── README.md
│       ├── theory/
│       │   └── README.md
│       └── README.md
├── tests/
│   ├── chords/
│   │   └── README.md
│   ├── enharmonics/
│   │   └── README.md
│   ├── fixtures/
│   │   └── README.md
│   ├── integration/
│   │   └── README.md
│   ├── native_ui/
│   │   └── README.md
│   ├── progressions/
│   │   └── README.md
│   ├── theory/
│   │   └── README.md
│   ├── transposition/
│   │   └── README.md
│   ├── README.md
│   └── test_structure.py
├── tools/
│   ├── ingestion/
│   │   └── README.md
│   ├── legacy/
│   │   ├── generators/
│   │   │   └── README.md
│   │   └── README.md
│   ├── migration/
│   │   └── README.md
│   ├── packaging/
│   │   └── README.md
│   ├── validation/
│   │   ├── check_structure.py
│   │   └── README.md
│   └── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── README.md
├── SECURITY.md
├── SKILL.md
└── VERSION
```

**Bereits vorhanden:** `LICENSE`, mehrere tausend historische Bestandsdateien; diese erscheinen nicht automatisch als Dateien im Scaffold.
**Geplante Neuanlage:** nur die unter `scaffold/` enthaltenen Dateien; der Migrationslauf übernimmt ausgewählte vorhandene Artefakte.
