from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.safety_flow import write_safety_decision
from selfdev.tools.safety_gate import check_paths


def setup_task(workspace: Path, task_id: str = "task-safety-001", status: str = "ready_for_verification") -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Safety test",
        "status": status,
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "safety_gate",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {
            "senior_review": f"{task_id}.senior_reviewer.senior_review"
        },
        "blocked_by": [],
    })


def test_safety_gate_matches_env_star_pattern():
    result = check_paths([".env.local"])
    assert result.status == "BLOCK"


def test_safety_pass_writes_report_and_registers_artifact(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)

    result = write_safety_decision(
        task_id="task-safety-001",
        requested_actions=["write_artifact"],
        changed_paths=["docs/README.md"],
        workspace=workspace,
    )

    assert result.safety_status == "PASS"
    assert result.status == "ready_for_verification"
    assert result.artifact_id == "task-safety-001.safety_gate.safety_report"
    assert Path(result.report_path).exists()

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    task = board["tasks"]["task-safety-001"]
    assert task["status"] == "ready_for_verification"
    assert task["artifacts"]["safety_report"] == "task-safety-001.safety_gate.safety_report"

    registry = json.loads((workspace / "artifacts" / "index.json").read_text(encoding="utf-8"))
    assert "task-safety-001.safety_gate.safety_report" in registry["artifacts"]

    state = json.loads((workspace / "state" / "task-safety-001.state.json").read_text(encoding="utf-8"))
    assert state["stage"] == "safety_completed"
    assert state["safety_status"] == "PASS"


def test_safety_blocks_denied_action(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-safety-002")

    result = write_safety_decision(
        task_id="task-safety-002",
        requested_actions=["git_push"],
        changed_paths=["docs/README.md"],
        workspace=workspace,
    )

    assert result.safety_status == "BLOCK"
    assert result.status == "blocked"
    assert any("git_push" in reason for reason in result.reasons)

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    assert board["tasks"]["task-safety-002"]["status"] == "blocked"


def test_safety_blocks_denied_path(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-safety-003")

    result = write_safety_decision(
        task_id="task-safety-003",
        requested_actions=["write_artifact"],
        changed_paths=[".env"],
        workspace=workspace,
    )

    assert result.safety_status == "BLOCK"
    assert result.status == "blocked"
    assert any(".env" in reason for reason in result.reasons)


def test_safety_blocks_task_not_ready(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-safety-004", status="in_progress")

    result = write_safety_decision(
        task_id="task-safety-004",
        requested_actions=["write_artifact"],
        changed_paths=["docs/README.md"],
        workspace=workspace,
    )

    assert result.safety_status == "BLOCK"
    assert any("not ready for Safety Gate" in reason for reason in result.reasons)


def test_write_safety_decision_cli_pass(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-safety-cli")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_safety_decision.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-safety-cli",
            "--action",
            "write_artifact",
            "--changed-path",
            "docs/README.md",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"safety_status": "PASS"' in result.stdout


def test_write_safety_decision_cli_blocks(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-safety-cli-block")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_safety_decision.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-safety-cli-block",
            "--action",
            "git_push",
            "--changed-path",
            "docs/README.md",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert '"safety_status": "BLOCK"' in result.stdout
