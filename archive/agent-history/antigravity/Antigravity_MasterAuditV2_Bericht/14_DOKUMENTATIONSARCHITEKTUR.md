# STEPS – DOKUMENTATIONSARCHITEKTUR UND REPO-ZIELSTRUKTUR
## Bereinigungs- und Konsolidierungsvorschlag nach dem Diátaxis-Framework

**Prüfdatum:** 11. November 2026  

---

## 1. Das Diátaxis-Framework für STEPS

Zur Vermeidung von Informationsredundanz und historischem Dokumentenwildwuchs wird die Dokumentation künftig streng nach vier Nutzerbedürfnissen gegliedert:

1. **Tutorials (Lernorientiert):** Erste Schritte mit dem STEPS-Theoriekern, Akkordkonstruktion für Anfänger.
2. **How-To Guides (Problemorientiert):** Wie transponiert man eine Progression? Wie analysiert man Stimmführung?
3. **Reference (Informationsorientiert):** Vollständige API-Referenz der Module in `src/steps/`, Register der 28 Progressionen.
4. **Explanation (Verständnisorientiert):** Mathematische Grundlagen ($Z_{12}$, Tymoczko-Metrik), Architekturprinzipien.

---

## 2. Bereinigte Zielstruktur des Repositories

```
steps/
├── .github/                  # CI/CD Workflows
├── docs/                     # Bereinigte Dokumentation (Diátaxis)
│   ├── tutorials/
│   ├── howto/
│   ├── reference/
│   └── explanation/
├── knowledge/                # Gepflegte Wissensbasis & Ontologie
│   ├── concepts/
│   ├── corpora/
│   └── research/
├── src/
│   └── steps/                # Reiner Produktivcode
│       ├── theory/
│       ├── progression/
│       └── midi/ (geplant)
├── tests/                    # Automatisierte Testsuiten
├── archive/                  # Isoliertes historisches Archiv
│   └── glide-v3.53/          # Vollständig isoliertes Glide-Archiv
├── pyproject.toml            # Python Packaging & Tool-Konfiguration
├── LICENSE                   # MPL 2.0
└── README.md                 # Zentraler Einstiegspunkt
```
