# Alternative Lösungsansätze – Entscheidungen nicht vorwegnehmen

**Stand:** 2026-11-10 · Alle folgenden Wege sind *Vorschläge*. Niemand hat aufgrund dieses Dokuments bereits einen Architekturwechsel, einen neuen MVP oder das Löschen bestehender Dateien beschlossen. **Mindeststandard für eine Auswahl:** gleicher Referenz-Commit, gleicher Benutzerfall, dieselben Testdaten, dokumentierte Risiken und Kosten einschließlich künftiger Wartung.

## A. Glide als Steps-Fundament: vier wirklich unterschiedliche Wege

| Ansatz | Vorgehen | Wesentliche Vorteile | Kritische Nachteile | Entscheidungsgate |
|---|---|---|---|---|
| **A – vollständiger Fork mit Rückbau** | Glide-Quellbaum vollständig in eigenen Steps-Branch übernehmen, Todo-Sichten deaktivieren und langfristig refactoren | schnelle visuelle Parität, wenig anfänglicher Widget-Neubau | massive `ListApp`-Abhängigkeit, Prozess-Globals, ungenutzte Sicherheits-/Formatoberfläche, hohe Regression, Lizenz-/Ressourcen-/QA-Last | nur sinnvoll, wenn Testaufwand und absehbare Wartung geringer sind als Extraktion |
| **B – gezielte Shell-Extraktion** | UI-Bausteine samt generischen Hilfsmodulen in neuen Steps-Einstieg übernehmen; Fachlogik/Datenmodelle neu aufbauen | klare Domänengrenze, weniger Runtime-Abhängigkeit, vorhandenes Design weitgehend wiederverwendbar | initiale Entkopplungsarbeit hoch; einige Widgets verstecken globale `ListApp`-Aufrufe | kleine vertikale Shell gegen Screenshots und 30+ UI-Tests prüfen |
| **C – Hybrid/Anti-Corruption-Adapter** | limitierter Glide-UI-Prozess/Wrapper als temporärer Host; Steps-Fachlogik als separates Paket über Ports | schneller Experimentierweg, reversible Migration, paralleles Theorie-Engineering | Adapter wachsen zu Schatten-Domain, doppelte Zustände, Shutdown/Undo/Serialization schwierig | max. zwei vertikale Slices; danach gemessene Komplexität evaluieren |
| **D – Steps neu mit eigenem UI (ggf. Tk/Qt)** | nur Design-/UX-/QA-Erkenntnisse übernehmen, Widgets/Programmstruktur neu entwerfen | schlanker Code, vollständige Identität, wenig Glide-Altlasten | viel UI-/Plattform-/Theme-Wiederholungsarbeit, größere optische Abweichungen | kleine Vergleichsshell bauen, nicht pauschal als einfacher darstellen |

**Arbeitsvorschlag:** Für die erste Untersuchung **B und D parallel als kleine Spikes** vergleichen, ohne Glide umzubauen. B extrahiert Titel/Logo, Seitenliste, einklappbaren Bereich, ein Suchfeld, ein Einstellungsfenster und Theme-Wechsel. D baut dieselbe sichtbare Shell als minimales neues Tk-Projekt unter dokumentiertem Designvertrag. Es wird nicht das gesamte Projekt parallel zweimal programmiert. Die Spikes werden mit denselben Kriterien verglichen: Start und Ende ohne Dateneinwirkung, Widget- und Source-Imports, Anzahl eigener Laufzeitmodule, Win/Linux/macOS-Risiken, Tastatur-/Fokusverhalten, Night/DPI, Paketierbarkeit und sichtbare Parität.

**Reversible Auswahl nach Probe:** B gewinnt, wenn die Glide-Fähigkeiten mit klarer Isolation und moderatem Adapteraufwand nachweisbar wiederverwendet werden können. D gewinnt, wenn der Monolith für diese geringe Shell-Größe unverhältnismäßig viele Nebenwirkungen erzwingt. C ist nur ein Übergang, kein unbefristetes Ziel. A bleibt bewusst möglich, wird aber nicht als Default aufgedrängt.

## B. Zwei Fenster oder zwei Bereiche – drei UI-Architekturen

1. **Eine `Tk`-Root, zwei Panes:** ein Hauptfenster mit Sidebar und Workspace. Screenshot-nah, einfachere Fokus-/Menü-/Geometriepolitik, kompatibel mit Kompaktmodus. Empfohlener *Testprototyp*, nicht bestätigte Owner-Entscheidung.
2. **Eine `Tk`-Root, zwei `Toplevel`-Fenster:** unabhängig andock-/verschiebbar, geeignet z.B. Workbench + Inspector; bedeutet aber zusätzliche Window-Lifecycle-, Fokus- und Dock-/Taskleistenfragen. Navigation ist nicht identisch zum Screenshot.
3. **Zwei `Tk`-Root-Interpreter:** zu vermeiden, bis ein nachgewiesener technischer Grund vorliegt; Python-Dokumentation beschreibt mehrere Interpreter in einem Thread als problematisch und empfiehlt praktisch einen Tk-Root. Externer Anker: https://docs.python.org/3/library/tkinter.html .

**Abnahmedefinition:** „Zwei Fenster“ darf nicht in denselben Prompt sowohl als zwei unabhängige OS-Fenster *und* zwei Inhaltsbereiche eingehen. Vor Code-Extraktion zwei 1-Seiten-Wireframes und eine Nutzerentscheidung. Wenn der Nutzer keine zeitnahe Entscheidung trifft, nur den reversiblen Ein-Root-Prototyp bauen, nicht veröffentlichen.

## C. MVP-Vision: Hierarchie statt alles oder nichts

| MVP-Variante | Kernnutzen | Vorteile | Gefahr | Bedingung |
|---|---|---|---|---|
| **V1 Chord Explorer offline** | 4 Akkorde anlegen, transponieren, analysieren, speichern und testbar visualisieren | passt zu bestehender fachlicher Quelle und GitHub-Produktname; klare Erklärungstests | Drums zunächst sichtbar nicht nutzbar; frühes Hören könnte fehlen | musikalische Value-Tests mit mindestens 3 Aufgaben |
| **V2 Chords + simple MIDI-Audition** | obiger Editor plus Wiedergabe/Export | hörbarer Mehrwert; demonstriert Anwendung statt nur Schema | Audio-Device-/Scheduler-Aufwand; möglicherweise größer als Shellarbeit | MIDI-SMF zuerst, Playback später wenn Backends nachgewiesen |
| **V3 Chords + Minimal-Drum-Grid** | zwei Spuren teilen sich Transport/Takt, Export | Nutzerwunsch nach Chord+Drum sichtbar früh integriert | geteiltes Zeitmodell komplexer als MVP-UI; Didaktik rückt nach hinten | nur bei expliziter Owner-Priorität und grober Kapazitätszusage |
| **V4 Knowledge-first ohne App-MVP** | verifizierte KB + CLI-Theory-Tests + Skill | wissenschaftlich solide, produktunabhängige Basis | Nutzernutzen und UI-Hypothese bleiben lange ungetestet | für eigenständigen Research-Track, nicht als Ersatz für eine nutzbare App |

**Empfehlung als Arbeitshypothese:** V1 **mit exportierbarem neutralem Eventmodell**, sodass V2/V3 später kein Format-Redesign erfordern. Parallel: Research-Track für KB-Baseline und den **ersten real befüllten, reviewten** Concept/Claim-Satz. Die Entscheidung bleibt offen, da Nutzer ausdrücklich Drums erwähnt hat.

## D. Harmonie-Engine: deterministische Regeln, Korpusstatistik oder ML

| Technik | Zulässige Aussage | Vorzüge | Grenzfälle/Risiken |
|---|---|---|---|
| Typisierte, deterministische Regel/Relation | „Im gewählten Modell folgt daraus Beziehung X“ | testbar, erklärbar, stabil, offline | Theorievorannahmen, kulturelle Verengung; nicht universell |
| empirisches Korpusmodell | „In untersuchtem Korpus/Genre wurde Übergang X mit Häufigkeit Y annotiert“ | Stilnähe, quantitative Priorität, Vielfalt | Sample-/Annotations-Bias, Datenlizenzen, nicht theoretische Wahrheit |
| heuristisches Kreativranking | „Option X passt zu den gewählten Zielen“ | motivierende Vorschläge, kontrollierbare Regeln | Präferenzwert keine objektive Fachregel; Zielgewichtung offenlegen |
| generatives Sprach-/ML-Modell | „Vorschlag/Erklärung eines Modells, geprüft gegen Struktur“ | vielfältige Lernhilfe und Varianten | Halluzination, instabile Reproduktion, Datenschutz, Cloud/Token-Abhängigkeit |

**Reihenfolge aus Deep Research:** rule-based first → Korpusranking second → ML als Zusatz third. Für die App darf das lokale Basisszenario ohne externen Dienst funktionieren. Der Skill ist für Menschen/Entwicklungsagenten nützlich; die Produktengine darf nicht implizit von einem fremden Claude-/ChatGPT-Tokenbudget abhängen.

## E. Wissensbasis: Dateisammlung, relationale DB, Suchindex oder Graph

- **Versionierte YAML/JSON/Markdown-Karten**: ideal für die ersten hundert reviewten Konzepte; PR-Diffs, Quellenreferenzen, niedrige Setupkosten. Nachteil: Konsistenzreferenzen müssen in CI geprüft werden.
- **SQLite**: nützlich für große Suchbestände, Indizes und strukturierte Transaktionen; erhöht Schema-/Migration-/Packaging-Aufwand, während die Basis noch leer ist. Erst einsetzen, wenn ein realer Volumen-/Suchprofilbefund vorliegt.
- **Volltext/Retrieval**: einfacher lexical/BM25-Index als erste Messbaseline; semantischer Embedding-Index erst, wenn exemplarische Nutzerfragen damit messbar besser beantwortet werden und Rechte/Datenschutz geklärt sind.
- **Graphdatenbank**: Beziehungen sind wichtig, eine separate Graph-DB ist es für den MVP nicht zwingend. Typisierte edges in versionierten Dateien reichen bis ihre Abfragen messbar an Grenzen stoßen.
- **Rohquellenarchiv**: explizit getrennt, ggf. privat; eine öffentliche Datenbank darf keine nicht freigegebenen Volltexte enthalten.

**Entscheidungsmethode:** 20 echte Nutzer-/Researchfragen, die gleichen Testfragen in beiden Datenvarianten, Retrieval-Precision und Citation-Fidelity, Speicher-/Updatekosten, deterministischer Indexbau und Rechtebelege. So wird die Architektur nicht aus dem Schlagwort „AI/Graph“ gewählt.

## F. MIDI/Audio: kleines Abhängigkeitsbudget

- **SMF-Export zunächst**: deterministisches Eventmodell mit `tempo`, `time_signature`, `note_on/off`, Track/Channel und PPQ; Dateibau kann mit einer überprüften Bibliothek oder eng begrenztem eigenen Writer erfolgen. Standard: https://midi.org/standard-midi-files .
- **Live-Playback später**: Port zu einem austauschbaren MIDI-Device/Synthese-Backend; Headless Tests mit künstlicher Clock. UI-Eventloop niemals durch Audio-Sleep blockieren. Bei fehlendem Ausgabegerät klare Fehlermeldung ohne Datenverlust.
- **Soundbank/WAV**: SoundFont-Lizenz, Lautstärkeschutz, Latenz und OS-Packaging zusätzlich; nicht als „MIDI-Funktion inklusive“ behaupten.
- **Import**: Ablehnung von fehlerhaften, extrem großen, unerwarteten oder zeitlich inkonsistenten MIDI-Dateien; Path- und Ressourcengrenzen für `.zip`/`.mid`.

**Proof of value:** Nutzer kann vier Akkorde eingeben, sauber transponieren, als MIDI in einer zweiten Software öffnen und ein verständliches Playback erhalten; Artefakt- und Zeitwertgleichheit prüfen.

## G. Repository- und Projektorganisation

| Form | Nutzen | Risiken | Entscheidung |
|---|---|---|---|
| Gleicher Repo für Glide und Steps | leicht gemeinsam editierbarer UI-Kern | gekoppelte Releases, Lizenz-/Quellmix, große Tools/Assets | **nicht empfohlen** als Standard; zwei Produkte sind bereits eigene Repos |
| Zwei Repos mit 1:1 kopierten Modulen | schnell, lokal unabhängig | Drift, zweimalige Fehlerpflege, Copyright-/Attribution- und Vendor-Fragen | nur zeitweise und mit Herkunftsregister |
| Reuse-Extrakt als drittes kleines Paket | gemeinsame Fehlerpflege, saubere API | dritte Release-Abhängigkeit, Abnahme-/Packaginglast | erst wenn mehrere wiederverwendbare Module tatsächlich isoliert sind |
| Git Submodule/Subtree | Herkunft und Versionspin sichtbar | Bedienkomplexität, unpassende monolithische Struktur | nur für bereits modular freigegebene Teilpakete |

**Konsequenz:** erst konkrete reuse-Kandidaten isolieren; unabhängig von ihrer ursprünglichen Dateigröße. `25 Bausteinpakete` im Glide-Systemkatalog sind **keine 25 fertigen Libraries**. Das Dokument `manifests/GLIDE_25_PACKAGES_AUDIT_V2.csv` kennzeichnet den Status daher einheitlich als Kandidat.

## H. Abnahme einer Architekturentscheidung

Jeder ADR benötigt: Problem mit Benutzerfall; belastbare Referenz-SHA; mindestens zwei realistische Alternativen; nichtfunktionale Anforderungen; Rechte-/Datenauswirkungen; Aufwand samt Regression/Unterhalt; explizit *nicht* entschiedene Fragen; Test-Fixture; Rollback; Reviewer-/Owner-Status; Datum. Für die ersten drei ADRs (Shell, MVP, Domain/Storage) sind Probeskizzen im Ordner `decisions/` als vorgeschlagen dokumentiert. **Keine dieser Optionen ist ohne Owner-Beschluss verbindlich.**
