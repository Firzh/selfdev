from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.api.action_availability import get_action_availability
from selfdev.runtime.kanban import KanbanBoard


def setup_task(
    workspace: Path,
    task_id: str,
    status: str,
    artifacts: dict[str, str] | None = None,
) -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Action availability test",
        "status": status,
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "siwa",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": artifacts or {},
        "blocked_by": [],
    })


def test_missing_task_has_no_available_actions(tmp_path: Path):
    result = get_action_availability(
        task_id="task-missing",
        workspace=tmp_path / "workspace",
    )

    assert result.exists is False
    assert all(value is False for value in result.available_actions.values())
    assert result.reasons["approve_for_runner"] == "Task does not exist."


def test_ready_for_senior_enables_review_actions(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-001",
        status="ready_for_senior",
        artifacts={
            "docs_plan": "task-actions-001.adit.docs_plan",
        },
    )

    result = get_action_availability(
        task_id="task-actions-001",
        workspace=workspace,
    )

    assert result.exists is True
    assert result.status == "ready_for_senior"
    assert result.available_actions["approve_for_runner"] is True
    assert result.available_actions["request_revision"] is True
    assert result.available_actions["request_specialist_review"] is True
    assert result.available_actions["run_safety_gate"] is False


def test_ready_for_verification_enables_safety_before_verification(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-002",
        status="ready_for_verification",
        artifacts={
            "senior_review": "task-actions-002.senior_reviewer.senior_review",
        },
    )

    result = get_action_availability(
        task_id="task-actions-002",
        workspace=workspace,
    )

    assert result.available_actions["run_safety_gate"] is True
    assert result.available_actions["run_verification"] is False
    assert "Safety report is required" in result.reasons["run_verification"]


def test_ready_for_verification_with_safety_report_enables_verification(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-003",
        status="ready_for_verification",
        artifacts={
            "senior_review": "task-actions-003.senior_reviewer.senior_review",
            "safety_report": "task-actions-003.safety_gate.safety_report",
        },
    )

    result = get_action_availability(
        task_id="task-actions-003",
        workspace=workspace,
    )

    assert result.available_actions["run_safety_gate"] is False
    assert result.available_actions["run_verification"] is True


def test_verified_enables_runner_when_verification_report_exists(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-004",
        status="verified",
        artifacts={
            "verification_report": "task-actions-004.verification_engine.verification_report",
        },
    )

    result = get_action_availability(
        task_id="task-actions-004",
        workspace=workspace,
    )

    assert result.available_actions["request_runner"] is True


def test_commit_ready_enables_commit_readiness(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-005",
        status="commit_ready",
        artifacts={
            "senior_review": "task-actions-005.senior_reviewer.senior_review",
            "safety_report": "task-actions-005.safety_gate.safety_report",
            "verification_report": "task-actions-005.verification_engine.verification_report",
            "runner_report": "task-actions-005.runner.runner_report",
        },
    )

    result = get_action_availability(
        task_id="task-actions-005",
        workspace=workspace,
    )

    assert result.available_actions["evaluate_commit_readiness"] is True
    assert "ready for Commit Gate" in result.reasons["evaluate_commit_readiness"]


def test_human_required_enables_human_approval(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-006",
        status="human_required",
    )

    result = get_action_availability(
        task_id="task-actions-006",
        workspace=workspace,
    )

    assert result.available_actions["approve_human_gate"] is True
    assert result.available_actions["reject"] is True


def test_show_actions_cli(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(
        workspace=workspace,
        task_id="task-actions-cli",
        status="ready_for_senior",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/show_actions.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-actions-cli",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["exists"] is True
    assert payload["available_actions"]["approve_for_runner"] is True
