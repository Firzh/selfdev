from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.artifact_collector import collect_artifact_reply
from selfdev.runtime.kanban import KanbanBoard


def setup_task(workspace: Path, task_id: str = "task-collect-001") -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Collect artifacts",
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


def write_reply(workspace: Path, task_id: str = "task-collect-001") -> Path:
    artifact = workspace / "docs" / f"{task_id}.adit_docs_plan.md"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("# Adit Documentation Plan\n", encoding="utf-8")

    reply_dir = workspace / "agents" / "adit" / "outbox"
    reply_dir.mkdir(parents=True, exist_ok=True)
    reply_path = reply_dir / "msg-artifact-ready.json"

    reply_path.write_text(
        json.dumps({
            "message_id": "msg-artifact-ready",
            "run_id": "run-test",
            "from_agent": "adit",
            "to_agent": "siwa",
            "task_id": task_id,
            "message_type": "artifact_ready",
            "status": "completed",
            "artifacts": {
                "docs_plan": f"docs/{task_id}.adit_docs_plan.md"
            }
        }, indent=2),
        encoding="utf-8",
    )

    return reply_path


def test_collect_artifact_reply_registers_artifact_and_updates_state(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)
    reply_path = write_reply(workspace)

    result = collect_artifact_reply(
        reply_path,
        workspace=workspace,
        required_artifact_types=["docs_plan"],
    )

    assert result.status == "ready_for_senior"
    assert result.registered_artifacts == ["task-collect-001.adit.docs_plan"]

    registry_path = workspace / "artifacts" / "index.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert "task-collect-001.adit.docs_plan" in registry["artifacts"]

    board_path = workspace / "kanban" / "board.json"
    board = json.loads(board_path.read_text(encoding="utf-8"))
    task = board["tasks"]["task-collect-001"]
    assert task["status"] == "ready_for_senior"
    assert task["artifacts"]["docs_plan"] == "task-collect-001.adit.docs_plan"

    state_path = workspace / "state" / "task-collect-001.state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["stage"] == "artifact_collected"
    assert state["status"] == "ready_for_senior"


def test_collect_artifact_reply_needs_revision_when_required_artifact_missing(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)
    reply_path = write_reply(workspace)

    result = collect_artifact_reply(
        reply_path,
        workspace=workspace,
        required_artifact_types=["docs_plan", "doc_gap_report"],
    )

    assert result.status == "needs_revision"
    assert any("doc_gap_report" in reason for reason in result.reasons)


def test_collect_artifact_reply_blocks_invalid_shape(tmp_path: Path):
    workspace = tmp_path / "workspace"
    reply_path = workspace / "bad-reply.json"
    reply_path.parent.mkdir(parents=True, exist_ok=True)
    reply_path.write_text(json.dumps({"message_type": "wrong"}), encoding="utf-8")

    result = collect_artifact_reply(reply_path, workspace=workspace)

    assert result.status == "blocked"
    assert any("Missing reply fields" in reason for reason in result.reasons)


def test_collect_artifacts_cli(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace)
    reply_path = write_reply(workspace)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/collect_artifacts.py",
            str(reply_path),
            "--workspace",
            str(workspace),
            "--required-artifact-type",
            "docs_plan",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"status": "ready_for_senior"' in result.stdout
