from __future__ import annotations

from pathlib import Path


def test_required_repository_directories_exist():
    root = Path(__file__).resolve().parents[2]
    required_dirs = [
        "docs",
        "docs/agents",
        "docs/knowledge_base",
        "config/selfdev",
        "schemas/selfdev",
        "selfdev",
        "selfdev/agents",
        "selfdev/tools",
        "selfdev/runtime",
        "selfdev/policies",
        "scripts/selfdev",
        "tests/selfdev",
    ]
    missing = [d for d in required_dirs if not (root / d).exists()]
    assert not missing, "Missing directories: " + ", ".join(missing)


def test_required_documentation_files_exist():
    root = Path(__file__).resolve().parents[2]
    required_files = [
        "README.md",
        "CHANGELOG.md",
        "docs/DEV_PLAN_SHORT_TERM.md",
        "docs/SPECIFICATION.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/TEST_PLAN.md",
    ]
    missing = [f for f in required_files if not (root / f).exists()]
    assert not missing, "Missing documentation files: " + ", ".join(missing)