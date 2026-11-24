# STEPS – Designvertrag (STEPS Music × Glide Shell 0.6.2)

Stand 24.11.2026 · STEPS 0.7.0-dev · Glide Shell 0.6.2 (Glide v1.0.2, Commit `7dcd8dc04366f88943fa17827882cef4d81421b8`)

Dieses Dokument verbindet den portablen Gestaltungs- und Interaktionsvertrag der **Glide Shell** ([`glide_shell/DESIGN_RICHTLINIEN.md`](../../glide_shell/DESIGN_RICHTLINIEN.md)) mit der Musik-, UI- und Markenarchitektur von **STEPS** ([`ADR-001`](../../decisions/ADR-001-ein-fenster-zwei-bereiche.md), [`ADR-003`](../../decisions/ADR-003-glide-nur-shell-und-infrastruktur.md), [`design/tokens/tokens.json`](../../design/tokens/tokens.json)).

---

## 1. Universelle Gestaltungsgrundsätze P1–P6 für STEPS

| Grundsatz | Bedeutung für STEPS | Konkrete Umsetzung |
|---|---|---|
| **P1 Funktioniert selbstverständlich** | Musikalische Workflows folgen intuitiven Desktop-Konventionen | 10 barrierefreie Themes (`dark`, `light`, `glass-dark`, `glass-light`, `dopamine`, `pixel`, `contrast-dark`, `contrast-light`, `minimal-dark`, `minimal-light`) plus `system_appearance`; `Escape` schließt Dialoge und verlässt den Kompaktmodus nicht destruktiv; `Tab`/`Shift+Tab` navigiert zyklisch zwischen Timeline, Akkordliste und Explorer; Standardkürzel (`⌘`/`Ctrl+N`, `O`, `S`, `Z`, `Y`, `B`, `Shift+B`, `,`) über `app_host` |
| **P2 Form folgt Funktion** | Farbe kennzeichnet harmonische Rollen, Typografie drückt Rang aus | `ThemeColors` trennt Hintergrundflächen (`bg_window`), Trägerkarten (`bg_surface`), Hover (`bg_surface_hover`), aktive Auswahl (`bg_active`) und harmonische Funktionsfarben (`harmonic_tonic`, `harmonic_subdominant`, `harmonic_dominant`, `harmonic_altered`, `harmonic_minor`); Okabe-Ito CVD-Palette für Kontrastmodi; 8 wählbare Akzentfarben |
| **P3 Keine Funktion doppelt** | Ein primärer, verlässlicher Interaktionsweg | Menüleiste (`app_host.attach_menubar`), Tastaturkürzel und Symbolleisten rufen dieselben Controller-Methoden auf; ausgerichtete Menü-Häkchen (D71) |
| **P4 Kein Platz verschwenden** | Noten, Akkordtimeline und Stimmführung dominieren das Fenster | 2-Bereiche-Architektur (ADR-001): Obere Timeline/Arbeitsbereich und unterer Info-/Theoriebereich; linke Navigationsspalte mit Schmalmodus (64-px-Symbolleiste mit Schnellaktionen `▸`, `◈`, `≣`, `☷`, `⤓`) oder komplettem Ausblenden für 100 % Arbeitsbreite |
| **P5 Nur das Wesentliche** | Übersichtlicher Ausgangszustand ohne Überladung | Fokus auf Progression und nächste Akkordempfehlungen; Kompaktmodus (`520 × 720` bis `480 × 560`) für paralleles Arbeiten neben DAWs mit Geometriewiederherstellung |
| **P6 Geringe Komplexität** | Stabile musikalische Begriffe und ergonomische UI-Muster | Durchgängig lokalisierte DE/EN-Kataloge (`app/locales/`), 24-Zeichen-Knopfbeschränkung (D63 `clip_button_text`), einheitliche modale Dialogführung über `glide_shell.modal_session` |

---

## 2. Verbindliche Einzelvorgaben (B-Regeln)

- **B15 – Bedienelemente schützen:** Hauptfenster mindestens `860 × 600` (`NORMAL_MIN`), im Kompaktmodus bis `480 × 560` (`COMPACT_MIN`). Alle primären Knöpfe (Akkord hinzufügen, Ändern, Löschen, Verschieben, Transponieren, MIDI-Export, Explorer, Voicing Lab) bleiben vollständig sichtbar, erreichbar und unbeschnitten.
- **B11 – Informationshierarchie vor starrer Breite:** Akkordsymbole, Stimmführungsanalysen und Melodielinien haben stets Vorrang vor technischen Metadaten. Sekundäre Texte und Pfade werden mit `text_fit.clip` ergonomisch gekürzt. Knopfbeschriftungen sind auf 24 Zeichen begrenzt (D63 `clip_button_text`), Titellängen auf 40 Zeichen (`TITLE_MAX_CHARS`).
- **B05 / B07 – In-App-Logo & Kopfleisten-Anatomie:** Das transparente STEPS-Signet ist bündig in die linke Kopfleiste integriert. Daneben stehen der Arbeitsbereichstitel (`workspace.heading`) und die D66-Metrikenzeile mit Tonart, Tongeschlecht, Tempo (BPM) und Taktart.
- **D55 / D61 / D66 / D68 – Responsive Dichtestufen & Breakpoints:**
  - Breite: `≥ 1120 px` vollständige Kopfleiste mit allen Aktionen; `900..1119 px` kompakte Knöpfe; `< 900 px` Minimalleiste (Logo und Subtitel weichen für maximalen Platz).
  - Automatische Verschmälerung: Unterhalb von `760 px` Fensterbreite wechselt eine sichtbare Seitenleiste automatisch auf die 64-px-Symbolleiste und kehrt ab `≥ 860 px` in die volle Breite zurück.
  - Höhe: `≥ 850 px` volle Innenabstände (`12 px`); `780..849 px` kompakte Abstände (`8 px`); `< 780 px` Minimalabstände (`6 px`).
- **B01 / B16 – Unmittelbare Rückmeldung:** Keine blockierenden Schlafzeiten (`time.sleep`) im Tk-Thread; asynchrone Berechnungen (z. B. MIDI-Synthese, Export, Stimmführungsanalyse) laufen über Hintergrund-Worker und koppeln über `window_lifetime.AfterScope` zurück. Schaltflächen besitzen unmittelbares Hover-Feedback (`hover_bg` / `_glide_hover_bg`) und klare Aktivitätsmarkierungen (`set_button_active`).
- **B03 – Unterbrechbare, ergonomische Übergänge:** Visuelle Animationen und Übergänge dauern höchstens 150 ms (`motion.Transitions`) und brechen bei Fensterschließung über den Lebenszyklus sauber ab.
- **B10 / B12 / B14 – Semantische Symbole:** Standardisierte Glyphen (`▸`, `◈`, `≣`, `☷`, `⤓`, `«`, `»`, `☰`, `▴`, `▾`, `✓`) mit fester Bedeutung und Tastaturbedienung über Pfeiltasten.
- **B17 / B19 – Ruhige Trägerflächen & Flächenhierarchie:** Saubere Trennung von Fenstergrund (`colors.bg_window` als Trägerinsel), Inhaltskarten (`RoundedSurfaceCard` mit `colors.bg_surface` und `corner_radius`) und Unterleisten ohne unruhige Schmuckelemente.
- **Glide-Anpassungsparität (Customization & Geometrie):**
  - **Erscheinungsbild-Dialog (`AppearanceDialog`):** Modaler Einstellungsdialog (`⌘`/`Ctrl+,`) zur interaktiven Steuerung von Design, Akzentfarbe, Hintergrund, Eckenrundung, Schriftgröße und -gewicht mit scrollbarer Canvas-Fläche (`ThemedAutoScrollbar`) und Live-Vorschau.
  - **10 Themes:** Dark, Light, Liquid Glass Dark, Liquid Glass Light, Dopamin, Pixel, Kontrast Dunkel, Kontrast Hell, Minimal Dunkel, Minimal Hell sowie automatischer Systemmodus.
  - **Akzentfarben-Auswahl (`accent_color`):** Freie Wahl aus 8 Akzentfarben (Lila, Blau, Türkis, Grün, Gelb, Rot, Braun, Kontrastgrau).
  - **Hintergrund-Farbtöne (`BACKGROUND_CHOICES` & `with_background`):** 10 Farboptionen (`default`, `surface`, `accent`, `clear`, `due_action`, `export`, `flag`, `delete`, `import`, `muted`), bei denen der Hintergrund subtil getönt wird, während Trägerkarten und funktionale Farbkodierungen stabil bleiben.
  - **Eckenrundung (`RADIUS_CHOICES`):** Wählbar in Groß (18 px - Glide Standard), Standard (12 px), Dezent (6 px) und Scharf (0 px) für alle Oberflächenkarten.
  - **Schriftgrößenskalierung (`FONT_SCALE_CHOICES`):** Kompakt (90 %), Standard (100 %) und Groß (115 %) für optimale Lesbarkeit auf beliebigen Bildschirmen.
  - **Einstellungen-Persistenz (`app/settings.py`):** Atomare Persistenz in `settings.json` im Plattform-Datenordner (`platform_data_dir("STEPS")`) mit `STEPS_DATA_DIR`-Isolierung für Tests.
- **Kontrast & Typografie (WCAG 2.2 AA):**
  - Normaler UI-Text erreicht mindestens **4,5:1** Kontrastverhältnis zum Hintergrund über alle 10 Themes.
  - Große Schrift (Titel, Akkordkarten) und Platzhalter erreichen mindestens **3:1**.
  - Farbenfehlsichtigkeit (CVD): Okabe-Ito-Palette sichert Unterscheidbarkeit bei Deuteranopie, Protanopie und Tritanopie.

---

## 3. Schutz der STEPS-Markenidentität & Domänengrenze

Glide Shell fungiert ausschließlich als neutrales technisches Desktop-Fundament. Die musikalische Fachdomäne und Markenidentität gehören ungeteilt zu **STEPS**:

1. **Reiner Musikkern (`src/steps/`):**
   - Völlig frei von `tkinter`, `ttk`, `glide_shell` und `app/`.
   - Reine, deterministische und testbare Musiktheorie: Akkorde, Voicings, Stimmführung, Skalen, MIDI-Export und rationale Zeitmodelle.
2. **Markenzeichen & Identität:**
   - STEPS-Wortmarke und App-Icon ([`app/brand.py`](../../app/brand.py), [`design/brand/`](../../design/brand/)).
   - Spezifische harmonische Farbakzente für Tonika (`#C66CF3` / `#9E4AC8`), Subdominante (`#30D158` / `#22813A`) und Dominante (`#FF5950` / `#D43128`), harmonisiert mit den Farbakzenten der 10 Glide-Themes.
3. **Ausdrücklich ausgeschlossen:**
   - Keine Übernahme von Glide-To-do-Fachlogik (`ListApp`, `.glideexchange`, `GLIDE_DATA_DIR`).
   - Keine Glide-Icons oder Gismo-Maskottchen.

---

## 4. Automatisierte Nachweise & Verifikation

- **Kontrastprüfung:** `tests/test_theme_tokens.py` verifiziert mathematisch WCAG 2.2 AA ($\ge 4{,}5:1$) für alle 10 Themes und 8 Akzentfarben.
- **Shell-Selbsttest:** `tests/test_glide_shell_integration.py` führt alle 13 Checks der Glide Shell aus.
- **Persistenzprüfung:** `tests/test_settings_persistence.py` verifiziert atomare Einstellungen-Speicherung und -Wiederherstellung.
- **Geometrie & Schutz:** B15-Buttonschutz, 64-px-Symbolleiste, Tastaturbedienung und Kompaktmodus sind in `test_glide_shell_integration.py` automatisiert abgedeckt.
- **Laufzeit-Isolation:** AST-Prüfungen sichern die Importfreiheit von `src/steps/`.
