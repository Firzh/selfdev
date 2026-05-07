from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.commit_readiness_flow import evaluate_task_commit_readiness
from selfdev.runtime.kanban import KanbanBoard


def setup_task(
    workspace: Path,
    task_id: str = "task-commit-001",
    status: str = "commit_ready",
    artifacts: dict[str, str] | None = None,
) -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Commit readiness test",
        "status": status,
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "commit_gate",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": artifacts if artifacts is not None else {
            "senior_review": f"{task_id}.senior_reviewer.senior_review",
            "safety_report": f"{task_id}.safety_gate.safety_report",
            "verification_report": f"{task_id}.verification_engine.verification_report",
            "runner_report": f"{task_id}.runner.runner_report",
        },
        "blocked_by": [],
    })


def test_commit_readiness_ready_writes_report_and_registers_artifact(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)

    result = evaluate_task_commit_readiness(
        task_id="task-commit-001",
        workspace=workspace,
    )

    assert result.commit_status == "READY"
    assert result.status == "commit_ready"
    assert result.missing == []
    assert result.artifact_id == "task-commit-001.commit_gate.commit_request"
    assert Path(result.report_path).exists()

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    task = board["tasks"]["task-commit-001"]
    assert task["status"] == "commit_ready"
    assert task["artifacts"]["commit_request"] == "task-commit-001.commit_gate.commit_request"

    registry = json.loads((workspace / "artifacts" / "index.json").read_text(encoding="utf-8"))
    assert "task-commit-001.commit_gate.commit_request" in registry["artifacts"]

    state = json.loads((workspace / "state" / "task-commit-001.state.json").read_text(encoding="utf-8"))
    assert state["stage"] == "commit_readiness_completed"
    assert state["commit_status"] == "READY"


def test_commit_readiness_blocks_missing_artifact(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace,
        task_id="task-commit-002",
        artifacts={
            "senior_review": "task-commit-002.senior_reviewer.senior_review",
            "safety_report": "task-commit-002.safety_gate.safety_report",
        },
    )

    result = evaluate_task_commit_readiness(
        task_id="task-commit-002",
        workspace=workspace,
    )

    assert result.commit_status == "BLOCKED"
    assert result.status == "blocked"
    assert "verification_report" in result.missing
    assert "runner_report" in result.missing

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    assert board["tasks"]["task-commit-002"]["status"] == "blocked"


def test_commit_readiness_blocks_task_not_commit_ready(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-commit-003", status="verified")

    result = evaluate_task_commit_readiness(
        task_id="task-commit-003",
        workspace=workspace,
    )

    assert result.commit_status == "BLOCKED"
    assert result.status == "blocked"
    assert any("not ready for Commit Gate" in reason for reason in result.reasons)


def test_evaluate_commit_readiness_cli_ready(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-commit-cli")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/evaluate_commit_readiness.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-commit-cli",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"commit_status": "READY"' in result.stdout
    assert '"status": "commit_ready"' in result.stdout


def test_evaluate_commit_readiness_cli_blocked(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(
        workspace,
        task_id="task-commit-cli-block",
        artifacts={
            "senior_review": "task-commit-cli-block.senior_reviewer.senior_review",
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/evaluate_commit_readiness.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-commit-cli-block",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert '"commit_status": "BLOCKED"' in result.stdout
    assert '"status": "blocked"' in result.stdout
