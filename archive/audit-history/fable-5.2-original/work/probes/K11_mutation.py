# K11: Mutationsversuche NUR in der Arbeitskopie. Aufruf: cd ~/steps-fable-pack/work/copy && PYTHONPATH=. python -B .../K11_mutation.py
import json, os, shutil, sys, importlib
assert os.path.abspath(os.getcwd()).endswith("steps-fable-pack/work/copy"), "nur in der Arbeitskopie ausführen"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _h import chk, summary
import src.steps.progression.reviewed as rv
FILES = [rv.CATALOG, rv.APPROVALS, rv.REGISTRY]
BAK = {p: p.read_text(encoding="utf-8") for p in FILES}
def restore():
    for p, t in BAK.items(): p.write_text(t, encoding="utf-8")
def load():
    return "OK:" + ",".join(e.progression.prog_id for e in rv.load_reviewed_catalog())
def edit(path, fn):
    d = json.loads(BAK[path]); fn(d); path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
def self_approve(reviewer="fable-agent", url="https://github.com/n05a-design/steps/pull/999999#issuecomment-1", day="2099-12-31"):
    _, claims = rv._candidates()
    doc = {"schema_version": 1, "approvals": {i: {"fingerprint": c.fingerprint, "reviewer": reviewer, "reviewed_on": day, "evidence_url": url} for i, c in claims.items()}}
    rv.APPROVALS.write_text(json.dumps(doc), encoding="utf-8")
def case(label, expected, mutate, note=""):
    restore()
    def run():
        mutate(); return load()
    chk("K11", label, expected, run, note); restore()
OK = "OK:PROG-001,PROG-003,PROG-009"
case("Ausgangszustand lädt", OK, lambda: None)
case("Fingerabdruck 1 Zeichen geändert -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: d["approvals"]["PROG-003-HARMONY"].__setitem__("fingerprint", "0"*64)))
case("Freigabe entfernt -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: d["approvals"].pop("PROG-009-HARMONY")))
case("Link auf fremdes Repo -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: d["approvals"]["PROG-003-HARMONY"].__setitem__("evidence_url", "https://github.com/evil/steps/pull/11#issuecomment-1")))
case("Claimtext geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.CATALOG, lambda d: d["examples"][1]["claims"][0].__setitem__("text", "Geändert.")))
case("Akkorde geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.CATALOG, lambda d: d["examples"][1].__setitem__("chords", "Dm7 - G7 - Cm7")))
case("voice_path geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.CATALOG, lambda d: d["examples"][1]["claims"][1]["voice_path"][1].__setitem__("note", "B3")))
case("Quelle: Titel geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.REGISTRY, lambda d: d["sources"][2].__setitem__("title", "Anderer Titel")))
case("Quelle: URL geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.REGISTRY, lambda d: d["sources"][2].__setitem__("url", "https://example.org/x")))
case("Quelle: rights_status pending -> Sperre", "ERR", lambda: edit(rv.REGISTRY, lambda d: d["sources"][2].__setitem__("rights_status", "pending")))
case("Locator geändert, Freigabe alt -> Sperre", "ERR", lambda: edit(rv.CATALOG, lambda d: d["examples"][1]["claims"][0]["references"][0].__setitem__("locator", "S. 999")))
# Ab hier: Was die Sperre NICHT erkennen kann. Sollwert = was ein ausreichender Nachweis verlangen würde (Sperre).
case("Link auf nicht existierenden PR/Kommentar (#999999, issuecomment-1) -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: [r.__setitem__("evidence_url", "https://github.com/n05a-design/steps/pull/999999#issuecomment-1") for r in d["approvals"].values()]), "Existenz wird nicht geprüft")
case("Reviewer beliebiger Name 'x' -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: [r.__setitem__("reviewer", "x") for r in d["approvals"].values()]), "Name nicht an Link/Person gebunden")
case("Freigabedatum 2099-12-31 (Zukunft) -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: [r.__setitem__("reviewed_on", "2099-12-31") for r in d["approvals"].values()]))
def false_claim():
    edit(rv.CATALOG, lambda d: (d["examples"][1]["claims"][0].__setitem__("text", "Dm7–G7–Cmaj7 bildet in C-Dur die Folge IV–V–vi."), d["examples"][1].__setitem__("chords", "Dm7 - G7 - F#m7b5")))
    self_approve()
case("Falsche Aussage + falsche Akkorde, Freigabe selbst eingetragen -> Sperre", "ERR", false_claim, "Agent berechnet Fingerabdruck über _candidates()/--review-manifest")
def bad_path():
    edit(rv.CATALOG, lambda d: d["examples"][1]["claims"][1]["voice_path"][1].__setitem__("note", "Quatsch"))
    self_approve()
case("voice_path-Note 'Quatsch' + Selbstfreigabe -> Sperre", "ERR", bad_path, "Notenname wird nicht geparst")
def wrong_src():
    edit(rv.CATALOG, lambda d: d["examples"][1]["claims"][0]["references"][0].__setitem__("source_id", "yale-key-names"))
    self_approve()
case("Aussage auf thematisch fremde Quelle umgehängt + Selbstfreigabe -> Sperre", "ERR", wrong_src, "Inhalt der Quelle wird nicht geprüft")
case("Doppelte JSON-Schlüssel -> Sperre", "ERR", lambda: rv.APPROVALS.write_text(BAK[rv.APPROVALS].replace('"schema_version": 1,', '"schema_version": 1, "schema_version": 1,'), encoding="utf-8"))
case("Zusätzliche Freigabe für unbekannten Claim -> Sperre", "ERR", lambda: edit(rv.APPROVALS, lambda d: d["approvals"].__setitem__("PROG-002-HARMONY", d["approvals"]["PROG-001-HARMONY"])))
case("Viertes Beispiel im Katalog -> Sperre", "ERR", lambda: edit(rv.CATALOG, lambda d: d["examples"].append(dict(d["examples"][0], id="PROG-002"))))
restore(); summary()
