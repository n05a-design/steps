"""Generate the public Python API reference from the current STEPS checkout."""

from __future__ import annotations

import argparse
from dataclasses import is_dataclass
from enum import Enum
import inspect
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/theory/API.md"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import knowledge
from src import steps
from src.steps import progression, theory
from src.steps.progression.engine import ReviewedProgression


def render() -> str:
    lines = [
        "# Python-API von STEPS",
        "",
        "Erzeugt mit `python scripts/render_api_reference.py`.",
        "Der [Implementierungsstand](../IMPLEMENTATION.md) beschreibt Grenzen und Beispiele.",
        "",
        f"- Repository-Version `{(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}`",
        f"- Paketversion `{steps.__version__}`",
        "",
    ]
    domain_types = [ReviewedProgression]
    for module in (theory, progression, knowledge):
        lines += [f"## `{module.__name__}`", "", "| Export | Signatur |", "|---|---|"]
        for name in module.__all__:
            value = getattr(module, name)
            if isinstance(value, type) and issubclass(value, Enum):
                signature = ", ".join(f"`{member}`" for member in value.__members__)
            elif isinstance(value, type) and issubclass(value, Exception):
                signature = "Ausnahmetyp"
            elif callable(value):
                declaration = str(inspect.signature(value)).replace("|", r"\|")
                signature = f"`{declaration}`"
            else:
                signature = "Datenwert"
            if isinstance(value, type) and is_dataclass(value):
                domain_types.append(value)
            source = inspect.getsourcefile(value) if callable(value) else module.__file__
            path = Path(source).relative_to(ROOT).as_posix()
            lines.append(f"| [`{name}`](../../{path}) | {signature} |")
        lines.append("")
    lines += ["## Domänenobjekte", ""]
    for model in domain_types:
        path = Path(inspect.getsourcefile(model)).relative_to(ROOT).as_posix()
        signature = str(inspect.signature(model))
        lines += [f"### [{model.__name__}](../../{path})", "", f"`{model.__name__}{signature}`", ""]
        members = []
        for name, member in vars(model).items():
            if name.startswith("_"):
                continue
            if isinstance(member, property):
                members.append(f"- `{name}` (Eigenschaft)")
            elif inspect.isfunction(member):
                members.append(f"- `{name}{inspect.signature(member)}`")
        if members:
            lines.extend([*members, ""])

    lines += [
        "## Akkordqualitäten",
        "",
        "Intervalle sind Halbtöne relativ zum Akkordgrundton. `CLOSE` verwendet",
        "die Standardintervalle unter Berücksichtigung des expliziten Basses.",
        "",
        "| Qualität | Aliasse | Theoretische Intervalle | Standardintervalle |",
        "|---|---|---|---|",
    ]
    for name, template in theory.CHORD_TEMPLATES.items():
        aliases = ", ".join(f"`{alias}`" for alias in template["aliases"] if alias)
        lines.append(f"| `{name or '(leer)'}` | {aliases} | `{template['theoretical']}` | `{template['voiced']}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    content = render()
    if parser.parse_args().check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("API-Referenz veraltet. scripts/render_api_reference.py ausführen.")
    else:
        OUTPUT.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
