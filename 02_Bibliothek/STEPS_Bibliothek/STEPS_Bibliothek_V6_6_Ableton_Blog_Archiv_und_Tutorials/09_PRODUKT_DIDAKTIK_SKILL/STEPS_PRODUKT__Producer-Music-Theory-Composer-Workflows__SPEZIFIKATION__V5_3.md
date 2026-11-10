> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# STEPS Workflows: Musikverständnis, Komposition und Producing kombinieren

## Drei konkret überprüfbare Nutzeraufgaben
**Composer:** Startet mit vier Takten Melodie und will drei verschiedene harmonische Unterlegungen. Steps zeigt pro Kandidat Tonika-Hypothese, Akkordton-Fit, Bassverlauf, Alternativanalyse und Notation. Der Nutzer wählt selbst; ein Score darf nicht als objektive Schönheit verkauft werden.

**Drum Producer:** Importiert zwei MIDI-Varianten eines Grooves (straight und swung) und will tatsächliche Timing-Offsets, Note-on/off, Velocity und ggf. CC-Ereignisse vergleichen. Ohne originales Drum-Kit bleiben `audible_effects=unknown`. Die Ausgabe verlinkt die eigenen Quellenpfade nur im lokalen Kontext, keine geschützten Download-Assets im öffentlichen Repo.

**Mixing-Learner:** Möchte wissen, warum EQ- und Kompressoränderungen den Track verbessern könnten. Steps bietet ein nachvollziehbares A/B-Protokoll, formuliert Hypothesen und erklärt dBFS, Frequenzgang, Attack/Release und Lautheitsmatch. Ohne Audioanalyse kann es konkrete LUFS-/True-Peak-Werte **nicht** berechnen.

## Navigation und Discovery
Die bisherigen Kategorien `01–15`, `90_HISTORIE`, `99_ORIGINALARCHIV` bleiben stabil. Filter über `domain`, `topic`, `filename_keywords`, `evidence_level`, `license`, `status`, `version`, `source_type`, `test_status`. Historische Dateien müssen erreichbar bleiben, dürfen aber in der aktiven Suche standardmäßig mit `historical` gekennzeichnet sein; sonst entstehen scheinbare Duplikate.

## UX-Warnungen
- Beat-Zahl/16-Step-Grid in der UI einsbasiert, Rohdaten nullbasiert.
- Ein `loudness_target` benötigt ein Zielformat; `-23 LUFS` ist ein Broadcast-Referenzfall, nicht Produktionsregel.
- `styles` sind Filter nach Kontext, kein Autocomplete einer kulturellen Authentizität.
- Unterschiedliche Deutungen derselben Akkordfolge sollen nebeneinander angezeigt werden.
- Git-/Repository-Nachweis erst nach echtem Codex-Audit; bis dahin keine „bereits integrierte“ Funktion vortäuschen.
