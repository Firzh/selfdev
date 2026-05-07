from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.verification_flow import write_verification_report


def setup_task(workspace: Path, task_id: str = "task-verify-001", status: str = "ready_for_verification") -> None:
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": task_id,
        "title": "Verification test",
        "status": status,
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "verification_engine",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {
            "senior_review": f"{task_id}.senior_reviewer.senior_review",
            "safety_report": f"{task_id}.safety_gate.safety_report",
        },
        "blocked_by": [],
    })


def test_verification_pass_writes_report_and_registers_artifact(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace)

    required = workspace / "docs" / "ok.md"
    required.parent.mkdir(parents=True, exist_ok=True)
    required.write_text("# OK\n", encoding="utf-8")

    result = write_verification_report(
        task_id="task-verify-001",
        required_files=["docs/ok.md"],
        workspace=workspace,
    )

    assert result.verification_status == "PASS"
    assert result.status == "verified"
    assert result.artifact_id == "task-verify-001.verification_engine.verification_report"
    assert Path(result.report_path).exists()

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    task = board["tasks"]["task-verify-001"]
    assert task["status"] == "verified"
    assert task["artifacts"]["verification_report"] == "task-verify-001.verification_engine.verification_report"

    registry = json.loads((workspace / "artifacts" / "index.json").read_text(encoding="utf-8"))
    assert "task-verify-001.verification_engine.verification_report" in registry["artifacts"]

    state = json.loads((workspace / "state" / "task-verify-001.state.json").read_text(encoding="utf-8"))
    assert state["stage"] == "verification_completed"
    assert state["verification_status"] == "PASS"


def test_verification_fail_updates_status(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-verify-002")

    result = write_verification_report(
        task_id="task-verify-002",
        required_files=["docs/missing.md"],
        workspace=workspace,
    )

    assert result.verification_status == "FAIL"
    assert result.status == "verification_failed"
    assert any("Missing required file" in reason for reason in result.reasons)

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    assert board["tasks"]["task-verify-002"]["status"] == "verification_failed"


def test_verification_blocks_task_not_ready(tmp_path: Path):
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-verify-003", status="in_progress")

    result = write_verification_report(
        task_id="task-verify-003",
        required_files=[],
        workspace=workspace,
    )

    assert result.verification_status == "BLOCKED"
    assert result.status == "blocked"
    assert any("not ready for Verification Engine" in reason for reason in result.reasons)


def test_write_verification_report_cli_pass(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-verify-cli")

    required = workspace / "docs" / "ok.md"
    required.parent.mkdir(parents=True, exist_ok=True)
    required.write_text("# OK\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_verification_report.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-verify-cli",
            "--required-file",
            "docs/ok.md",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"verification_status": "PASS"' in result.stdout
    assert '"status": "verified"' in result.stdout


def test_write_verification_report_cli_fail(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    setup_task(workspace, task_id="task-verify-cli-fail")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/write_verification_report.py",
            "--workspace",
            str(workspace),
            "--task-id",
            "task-verify-cli-fail",
            "--required-file",
            "docs/missing.md",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert '"verification_status": "FAIL"' in result.stdout
    assert '"status": "verification_failed"' in result.stdout
