from __future__ import annotations

import importlib
import pytest

MODULES = [
    "selfdev.tools.safety_gate",
    "selfdev.tools.verification_engine",
    "selfdev.tools.runner",
    "selfdev.tools.commit_gate",
    "selfdev.runtime.state_manager",
    "selfdev.runtime.message_bus",
    "selfdev.runtime.kanban",
]


@pytest.mark.parametrize("module_name", MODULES)
def test_core_modules_import_without_side_effect(module_name: str):
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing module {module_name}: {exc}")