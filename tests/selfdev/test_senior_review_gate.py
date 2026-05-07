from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.senior_review_gate import write_senior_review


def setup_ready_task(workspace: Path, task_id: str = "task-review-001") -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Senior review test",
        "status": "ready_for_senior",
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "senior_reviewer",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {
            "docs_plan": f"{task_id}.adit.docs_plan"
        },
        "blocked_by": [],
    })


def test_senior_review_approve_updates_kanban_state_and_registry(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_ready_task(workspace)

    result = write_senior_review(
        task_id="task-review-001",
        decision="approve_for_runner",
        reasons=["Artifacts complete for skeleton phase."],
        workspace=workspace,
    )

    assert result.status == "ready_for_verification"
    assert result.artifact_id == "task-review-001.senior_reviewer.senior_review"
    assert Path(result.review_path).exists()

    board_path = workspace / "kanban" / "board.json"
    board = json.loads(board_path.read_text(encoding="utf-8"))
    task = board["tasks"]["task-review-001"]
    assert task["status"] == "ready_for_verification"
    assert task["artifacts"]["senior_review"] == "task-review-001.senior_reviewer.senior_review"

    registry_path = workspace / "artifacts" / "index.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert "task-review-001.senior_reviewer.senior_review" in registry["artifacts"]

    state_path = workspace / "state" / "task-review-001.state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["stage"] == "senior_review_completed"
    assert state["decision"] == "approve_for_runner"


def test_senior_review_request_revision_updates_status(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_ready_task(workspace, task_id="task-review-002")

    result = write_senior_review(
        task_id="task-review-002",
        decision="request_revision",
        reasons=["Missing required rationale."],
        workspace=workspace,
    )

    assert result.status == "needs_revision"

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    assert board["tasks"]["task-review-002"]["status"] == "needs_revision"


def test_senior_review_blocks_task_not_ready(tmp_path: Path):
    workspace = tmp_path / "workspace"
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": "task-review-003",
        "title": "Not ready",
        "status": "in_progress",
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "adit",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {},
        "blocked_by": [],
    })

    result = write_senior_review(
        task_id="task-review-003",
        decision="approve_for_runner",
        reasons=["Trying too early."],
        workspace=workspace,
    )

    assert result.status == "blocked"
    assert any("not ready for senior review" in reason for reason in result.reasons)


def test_write_senior_review_cli(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_ready_task(workspace, task_id="task-review-cli")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_senior_review.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-review-cli",
            "--decision",
            "approve_for_runner",
            "--reason",
            "CLI review approved for skeleton phase.",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"status": "ready_for_verification"' in result.stdout
    assert '"decision": "approve_for_runner"' in result.stdout
