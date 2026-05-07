from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.runner_flow import write_runner_report


def setup_task(workspace: Path, task_id: str = "task-runner-001", status: str = "verified") -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Runner test",
        "status": status,
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "runner",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {
            "senior_review": f"{task_id}.senior_reviewer.senior_review",
            "safety_report": f"{task_id}.safety_gate.safety_report",
            "verification_report": f"{task_id}.verification_engine.verification_report",
        },
        "blocked_by": [],
    })


def test_runner_accepts_safe_action_and_writes_report(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)

    result = write_runner_report(
        task_id="task-runner-001",
        action="git_apply_check",
        workspace=workspace,
    )

    assert result.runner_status == "ACCEPTED"
    assert result.status == "commit_ready"
    assert result.artifact_id == "task-runner-001.runner.runner_report"
    assert Path(result.report_path).exists()

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    task = board["tasks"]["task-runner-001"]
    assert task["status"] == "commit_ready"
    assert task["artifacts"]["runner_report"] == "task-runner-001.runner.runner_report"

    registry = json.loads((workspace / "artifacts" / "index.json").read_text(encoding="utf-8"))
    assert "task-runner-001.runner.runner_report" in registry["artifacts"]

    state = json.loads((workspace / "state" / "task-runner-001.state.json").read_text(encoding="utf-8"))
    assert state["stage"] == "runner_completed"
    assert state["runner_status"] == "ACCEPTED"


def test_runner_blocks_denied_action(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-runner-002")

    result = write_runner_report(
        task_id="task-runner-002",
        action="terraform_destroy",
        workspace=workspace,
    )

    assert result.runner_status == "BLOCKED"
    assert result.status == "blocked"
    assert any("terraform_destroy" in reason for reason in result.reasons)

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    assert board["tasks"]["task-runner-002"]["status"] == "blocked"


def test_runner_blocks_task_not_verified(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-runner-003", status="ready_for_verification")

    result = write_runner_report(
        task_id="task-runner-003",
        action="git_apply_check",
        workspace=workspace,
    )

    assert result.runner_status == "BLOCKED"
    assert result.status == "blocked"
    assert any("not ready for Runner" in reason for reason in result.reasons)


def test_write_runner_report_cli_accepts_safe_action(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-runner-cli")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_runner_report.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-runner-cli",
            "--action",
            "git_apply_check",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"runner_status": "ACCEPTED"' in result.stdout
    assert '"status": "commit_ready"' in result.stdout


def test_write_runner_report_cli_blocks_denied_action(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-runner-cli-block")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_runner_report.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-runner-cli-block",
            "--action",
            "terraform_destroy",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert '"runner_status": "BLOCKED"' in result.stdout
    assert '"status": "blocked"' in result.stdout
