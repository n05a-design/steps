#!/usr/bin/env python3
"""Inventory literal UI text in active application modules."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT / "app"
UI_WIDGETS = {"Label", "Button", "Radiobutton", "Checkbutton", "Menu", "OptionMenu", "create_button"}
INVENTORY_CALLS = {"title", "showinfo", "showerror", "askyesno", "askyesnocancel"}


def literal_string(node: ast.AST) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def check() -> int:
    findings: list[str] = []
    for path in sorted(APP_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func_name = None
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                func_name = node.func.id

            keywords = {
                keyword.arg: keyword.value
                for keyword in node.keywords
                if keyword.arg
            }
            candidate = None
            if func_name in UI_WIDGETS:
                candidate = keywords.get("text")
            elif func_name in INVENTORY_CALLS:
                candidate = node.args[0] if node.args else keywords.get("title")
            elif isinstance(node.func, ast.Attribute) and node.func.attr == "configure":
                candidate = keywords.get("text")

            if candidate is not None:
                value = literal_string(candidate)
                if value and value.strip():
                    findings.append(f"{path.relative_to(ROOT)}:{node.lineno}: {func_name}: {value}")

    if findings:
        print("HARD-CODED ACTIVE UI TEXT FOUND")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("UI TEXT INVENTORY PASS: no literal active widget/dialog text found")
    return 0


def main() -> int:
    if "--check" not in sys.argv:
        print("Usage: python -B scripts/check_ui_text_inventory.py --check")
        return 2
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
