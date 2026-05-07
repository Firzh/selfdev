from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.api.read_api import ReadApi
from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.state_manager import StateManager


def test_read_api_health_uses_config_files():
    api = ReadApi()
    payload = api.health()

    assert payload["service"] == "selfdev-read-api"
    assert payload["mode"] == "read_only"
    assert payload["config"]["agents.yaml"] is True
    assert payload["config"]["tools.yaml"] is True


def test_read_api_agents_and_tools():
    api = ReadApi()
    agents = api.agents()
    tools = api.tools()

    assert "agents" in agents
    assert "siwa" in agents["agents"]
    assert "opung" in agents["agents"]

    assert "tools" in tools
    assert "read_file" in tools["tools"]


def test_read_api_kanban_reads_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": "task-api-001",
        "title": "API read test",
        "status": "todo",
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "siwa",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {},
        "blocked_by": [],
    })

    api = ReadApi(workspace=workspace)
    payload = api.kanban()

    assert "task-api-001" in payload["tasks"]
    assert payload["tasks"]["task-api-001"]["status"] == "todo"


def test_read_api_artifacts_returns_empty_when_missing(tmp_path: Path):
    api = ReadApi(workspace=tmp_path / "workspace")
    payload = api.artifacts()

    assert payload == {"artifacts": {}}


def test_read_api_state_existing_and_missing(tmp_path: Path):
    workspace = tmp_path / "workspace"
    manager = StateManager(workspace)
    manager.write_state("task-api-state", {
        "task_id": "task-api-state",
        "status": "in_progress",
    })

    api = ReadApi(workspace=workspace)

    existing = api.state("task-api-state")
    missing = api.state("task-missing")

    assert existing["exists"] is True
    assert existing["state"]["status"] == "in_progress"

    assert missing["exists"] is False
    assert missing["state"] is None


def test_read_api_summary(tmp_path: Path):
    workspace = tmp_path / "workspace"
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": "task-api-summary",
        "title": "API summary test",
        "status": "todo",
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "siwa",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {},
        "blocked_by": [],
    })

    api = ReadApi(workspace=workspace)
    payload = api.summary()

    assert payload["service"] == "selfdev-read-api"
    assert payload["mode"] == "read_only"
    assert payload["task_count"] == 1
    assert payload["agent_count"] >= 7


def test_read_api_cli_health():
    root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "health",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["service"] == "selfdev-read-api"
    assert payload["mode"] == "read_only"


def test_read_api_cli_state_requires_task_id(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "state",
            "--workspace",
            str(tmp_path / "workspace"),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--task-id is required" in result.stderr
