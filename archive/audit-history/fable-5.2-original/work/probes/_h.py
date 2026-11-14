"""Gemeinsamer Helfer: Sollwert steht im Aufruf, bevor der Ist-Wert berechnet wird."""
ROWS = []
def chk(pid, case, expected, fn, note=""):
    try:
        actual = fn()
    except Exception as exc:  # Fehlerklasse wird als Ist-Wert geführt
        actual = "ERR:" + type(exc).__name__
    if isinstance(expected, str) and expected == "ERR":
        ok = isinstance(actual, str) and actual.startswith("ERR:")
    elif isinstance(expected, float):
        ok = isinstance(actual, (int, float)) and not isinstance(actual, str) and abs(actual - expected) < 1e-6
    else:
        ok = actual == expected
    ROWS.append((pid, case, expected, actual, ok, note))
    print(f"{'PASS' if ok else 'FAIL'} | {pid} | {case} | soll={expected!r} | ist={actual!r} {('| ' + note) if note else ''}")
def summary():
    f = [r for r in ROWS if not r[4]]
    print(f"--- {len(ROWS)} Fälle, {len(ROWS)-len(f)} PASS, {len(f)} FAIL")
