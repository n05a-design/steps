# PR #22 – Vorlage für die menschliche Fachfreigabe

**Vorlage, noch keine Freigabe.** Erst nach eigener Prüfung verwenden.
Der Quellenabschluss steht im [Quellenvotum](PR22_QUELLENVOTUM_2026-11-13.md).
Die sieben produktiven Claims und Fingerabdrücke wurden für diese Vorlage neu
berechnet. Die unveränderte Notationsfreigabe ist nicht erneut anzufordern.

## Erforderlicher menschlicher Schritt

Einen neuen normalen Conversation-Kommentar unter
[PR #22](https://github.com/n05a-design/steps/pull/22) mit allen sieben unten
stehenden Zeilen veröffentlichen. Nicht als Inline-Reviewkommentar oder reinen
Reviewtext abgeben: Der Verifier erwartet eine URL mit `#issuecomment-...`.
Das absendende menschliche GitHub-Konto muss nach dem aktuellen vertrauenswürdigen
Verifier `n05a-design` (ID 333259995) oder `timvontrostorff` (ID 331406730) sein und
von GitHub als OWNER, MEMBER oder COLLABORATOR zugeordnet werden.

Jede Freigabezeile muss unverändert in einer eigenen Zeile stehen, ohne
Aufzählungszeichen, Zitatpräfix oder zusätzliche Zeichen. Ein einziger Kommentar
kann alle sieben Zeilen enthalten. Nach Veröffentlichung nicht editieren;
Korrekturen erfordern einen neuen Kommentar, dessen neuer Permalink verwendet wird.
Die Entscheidung gilt nur für die genannten Fassungen und ist kein Mergeauftrag.

## Kopierbarer Kommentarinhalt

Ich gebe die folgenden sieben Claim-Fassungen innerhalb ihrer in der Abnahmeliste
genannten Gültigkeitsbereiche fachlich frei. Dies ist keine Mergefreigabe.

```text
STEPS-APPROVED PROG-001-HARMONY 7a9f0ca6312eaa8837c45a624a0ca50cdde3f9af323e8fc81094519cd7c53a63
STEPS-APPROVED PROG-001-TONAL-CENTER b39ac7b557f1d7846c3c7ec006ebec60b0fbc78b205ae1540d14817ee849a789
STEPS-APPROVED PROG-003-HARMONY f9224530c773e01d2da4ebc8136b7b10bdf073bc5079b866c003501441faec7a
STEPS-APPROVED PROG-003-VOICE-II-V 9dd3c60c8090e001841f83b29ca8c34f7071362ca6984fd107cfa9f3aadf2fcf
STEPS-APPROVED PROG-003-VOICE-V-I ae607536c2e00567c466a8367dbb30ffe24efc92c21fcce8a2237b25a05ba564
STEPS-APPROVED PROG-009-HARMONY adadf2ef5902cb9b2f115060361f224a6faf15c766dfee99967badac4a363969
STEPS-APPROVED PROG-009-VOICE-LEADING 051dca398ee6da3c5074a8390de246fe88733a4df17469582a1b09a0fbcf71bc
```

## Anschließend im produktiven Register zu erfassende Daten

Die Claim-ID ist jeweils der Schlüssel in `reviewed_progression_approvals.json`.
Pro Claim werden genau vier Felder benötigt:

| Feld | Herkunft |
| --- | --- |
| `fingerprint` | Vollständiger SHA-256 aus der jeweiligen Freigabezeile |
| `reviewer` | Tatsächlicher GitHub-Login des absendenden Menschen |
| `reviewed_on` | UTC-Kalenderdatum von GitHubs `created_at`, Format YYYY-MM-DD |
| `evidence_url` | Tatsächlicher neuer Kommentar-Permalink, z. B. `https://github.com/n05a-design/steps/pull/22#issuecomment-<ID>` |

Bei einem gemeinsamen Kommentar teilen alle sieben Einträge Reviewer, UTC-Datum
und Evidence-URL. Der Kommentar darf nicht nachträglich editiert oder gelöscht
werden. GitHub muss den Kommentar samt Autor-ID und Zeitstempeln abrufbar liefern.
Eine Bestätigung im Chat allein ersetzt den GitHub-Beleg des aktuellen Verifiers
nicht. Die frühere Freigabe für den Fingerabdruck `1b52fd68...` ist nicht übertragbar.

Erst nach Vorliegen des echten Kommentars die sieben Registereinträge aktualisieren,
den Renderer zur Neugenerierung der Lerntexte ausführen, die Coverage neu erzeugen
und die Online-Evidence sowie die übrigen Checks erneut prüfen. Keine dieser
produktiven Änderungen ist durch diese Vorlage bereits vorgenommen.
