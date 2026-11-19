#!/usr/bin/env python3
"""Detect literal user-facing CLI text outside the LocaleManager contract."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT / "app"


def is_catalog_lookup(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "i18n"
        and node.func.attr == "translate"
    )


def check() -> int:
    findings: list[str] = []
    for path in sorted(APP_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func_name = (
                node.func.attr
                if isinstance(node.func, ast.Attribute)
                else node.func.id
                if isinstance(node.func, ast.Name)
                else None
            )

            if func_name in {"print"}:
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        findings.append(
                            f"{path.relative_to(ROOT)}:{node.lineno}: print literal: {arg.value}"
                        )

            if func_name == "add_argument":
                for keyword in node.keywords:
                    if keyword.arg not in {"description", "help"}:
                        continue
                    if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                        findings.append(
                            f"{path.relative_to(ROOT)}:{node.lineno}: CLI {keyword.arg} literal: {keyword.value.value}"
                        )
                    elif not is_catalog_lookup(keyword.value):
                        findings.append(
                            f"{path.relative_to(ROOT)}:{node.lineno}: CLI {keyword.arg} is not i18n.translate"
                        )

            if func_name == "ArgumentParser":
                for keyword in node.keywords:
                    if keyword.arg == "description" and not is_catalog_lookup(keyword.value):
                        findings.append(
                            f"{path.relative_to(ROOT)}:{node.lineno}: CLI description is not i18n.translate"
                        )

    if findings:
        print("CLI TEXT INVENTORY FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("CLI TEXT INVENTORY PASS: active CLI text routes through i18n")
    return 0


def main() -> int:
    if "--check" not in sys.argv:
        print("Usage: python -B scripts/check_cli_text_inventory.py --check")
        return 2
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
