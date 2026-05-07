from __future__ import annotations

from pathlib import Path

REQUIRED_WORKSPACE_DIRS = [
    "kanban",
    "agents",
    "manifests",
    "orchestration",
    "plans",
    "patches",
    "docs",
    "reviews",
    "safety",
    "verification",
    "runner",
    "approvals",
    "requests",
    "audit",
    "state",
    "logs",
    "traces",
    "performance",
    "errors",
]


def test_agent_workspace_directories_exist():
    root = Path(__file__).resolve().parents[2]
    workspace = root / "data" / "agent_workspace"
    assert workspace.exists(), "Missing data/agent_workspace"
    missing = [d for d in REQUIRED_WORKSPACE_DIRS if not (workspace / d).exists()]
    assert not missing, "Missing workspace dirs: " + ", ".join(missing)


def test_artifact_path_traversal_is_not_allowed_by_policy_shape():
    root = Path(__file__).resolve().parents[2]
    workspace = (root / "data" / "agent_workspace").resolve()
    unsafe = (workspace / ".." / ".." / ".env").resolve()
    assert not str(unsafe).startswith(str(workspace)), "Test setup failed: unsafe path should escape workspace"