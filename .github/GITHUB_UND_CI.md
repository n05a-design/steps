# GitHub und CI

Hier liegen die Vorlagen und Workflows für die technische Prüfung und Reviewzuständigkeiten.

| Einstieg | Inhalt |
| --- | --- |
| [Workflows](workflows/README.md) | Kern- und Skill-Matrix, Struktur, Secret-Scan und Pilotnachweise. |
| [PR-Vorlage](PULL_REQUEST_TEMPLATE.md) | Prüf- und Beschreibungspunkte für Änderungen. |
| [Issue-Vorlagen](ISSUE_TEMPLATE/README.md) | Fehler und Funktionswünsche. |
| [CODEOWNERS](CODEOWNERS) | Reviewzuständigkeit für die Publikationskette. |

Die erforderlichen Statuschecks und Reviewregeln werden in GitHub verwaltet. Der [Publikationsablauf](../knowledge/concepts/progressions/README.md) erklärt die fachlichen Belege.

## Projektseite

GitHub zeigt auf der Startseite des Repositorys eine `README.md` aus `.github` vor der Root-README an. Diese Übersicht heißt deshalb nicht `README.md`; ein [Test](../tests/test_project_page.py) verhindert, dass eine solche Datei zurückkehrt.

Die [Root-README](../README.md) ist die Projektseite. Ihr Aufbau folgt dem [GitHub-Auftritt von Glide](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt):

| Baustein | Zweck |
| --- | --- |
| App-Symbol, Leitsatz, ein Satz Nutzen | Der erste Bildschirm sagt, was STEPS ist und wie weit es ist. |
| Abzeichen und zwei Linkzeilen | Stand, Lizenz und Prüfung auf einen Blick; „Loslegen“ steht zuerst. |
| „Warum STEPS?“ und „Ein Blick hinein“ | Nutzen vor Technik. Die Abbildung stammt aus echter Kernausgabe, solange es keine Oberfläche gibt. |
| „Was STEPS heute kann“ und „Was noch nicht geht“ | Funktionen in wenigen Gruppen und ehrliche Grenzen. |
| Startwege als Tabelle | Verfügbarkeit je Weg, ohne Download zu versprechen. |
| Häufige Fragen, Rückmeldung, Entwicklung, Lizenz | Klare Kanäle für Besucher und Mitwirkende. |
| Englische Kurzfassung | Deutsches Haupt-README, englischer Einstieg für die Suche. |

Bei Funktionsänderungen die Projektseite zusammen mit dem [Implementierungsstand](../docs/IMPLEMENTATION.md) pflegen. Die Abbildung erzeugt [`render_project_page_figure.py`](../scripts/render_project_page_figure.py). Beschreibung, Topics und Kartenvorschau des Repositorys werden in den GitHub-Einstellungen gepflegt.

[Zur Projektübersicht](../README.md)
