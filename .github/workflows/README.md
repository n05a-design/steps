# Automatisierte GitHub-Prüfungen

Die Workflows prüfen unterschiedliche Eigenschaften der jeweils geprüften Revision.

| Einstieg | Inhalt |
| --- | --- |
| [Python-Tests](python-tests.yml) | Python 3.11–3.14, Skill-Smoke, API-/Golden-Abgleich, Pilot und Coverage. |
| [Struktur](structure-check.yml) | Verzeichnisstruktur, JSON und Tests bei passenden Pfadänderungen. |
| [Pilotbelege](pilot-evidence.yml) | Prüft GitHub-Belege mit dem Prüfer aus dem Basiscommit. |
| [Secret-Scanner](secret-scan.yml) | Prüft den Diff auf versehentlich versionierte Zugangsdaten. |

[Lokale Prüfungen](../../tests/README.md) · [GitHub Actions](https://github.com/n05a-design/steps/actions)

[Zur Bereichsübersicht](../README.md)
