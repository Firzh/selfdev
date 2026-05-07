from __future__ import annotations

from pathlib import Path
import ast

EXPECTED_SCRIPTS = [
    "scripts/selfdev/run_contract_tests.py",
]


def test_expected_scripts_exist():
    root = Path(__file__).resolve().parents[2]
    missing = [s for s in EXPECTED_SCRIPTS if not (root / s).exists()]
    assert not missing, "Missing scripts: " + ", ".join(missing)


def test_scripts_have_main_guard():
    root = Path(__file__).resolve().parents[2]
    missing_guard = []
    for rel in EXPECTED_SCRIPTS:
        path = root / rel
        ast.parse(path.read_text(encoding="utf-8"))
        source = path.read_text(encoding="utf-8")
        if 'if __name__ == "__main__"' not in source and "if __name__ == '__main__'" not in source:
            missing_guard.append(rel)
    assert not missing_guard, "Scripts missing main guard: " + ", ".join(missing_guard)