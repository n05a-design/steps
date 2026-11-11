# Prompt – portablen Einzelbaustein prüfen und übernehmen

Arbeite **nach** der Freigabe der neutralen Shell, nicht parallel zu einem laufenden Glide-Release. Wähle aus `src/glide/README.md` **einen** konkret benannten Baustein, für den Glide und der leere Steps-Testhost tatsächlich einen Bedarf haben (erster Kandidat: `compact_mode.py` oder `save_result.py`; diese Empfehlung ist kein Freigabenachweis).

1. Stelle mit statischer Import-/Runtime-Analyse die vollständige Transitivkette fest, einschließlich versteckter Produktnamen, Global-States, Ressourcendateien, Environment-Variablen, Logging, Tk-Fenster-Bindung und Lizenztexten.
2. Schreibe einen produktneutralen, versionierten API-Vertrag plus Negativtests *vor* der Migration. Definiere Ownership, Fehlerstatus, Thread-/Tk-Regeln, Rückwärtskompatibilität und Seiteneffekte.
3. Extrahiere nur den minimalen vertragskonformen Teil, mit unverändertem Glide-Adapter und unabhängigem Steps-Demo-Adapter. Keine direkte Abhängigkeit `shared -> glide` oder `shared -> steps`.
4. Behalte Datei-/MPL-Verweise und Herkunfts-SHA, beachte Fremdlizenzen. Für eine neue gemeinsame Distribution erst nach Lizenz- und 2-Consumer-Abnahme entscheiden.
5. Teste pure Python, GUI wo relevant, Windows/macOS/Linux soweit verfügbar, Daten-/Cache- und Event-Lebensdauer, absichtliche Fehler und Reentrancy. Ein fehlender OS-Test ist offen.
6. Gib eine Entscheidung `ACCEPT`, `ADAPT`, `REWRITE` oder `REJECT` mit gemessener Kopplung, Regressionsquote, Teststand und Gesamtwartungskosten aus; kein automatischer Rollout.

**Fertigkriterium:** unabhängiger Import ohne `app.pyw`, zweifache Vertragsprüfung, keine Glide-Produktivdaten, dokumentierte Semantik, Lizenz und rückwärtskompatibler Glide-Betrieb.
