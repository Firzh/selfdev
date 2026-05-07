from __future__ import annotations

from pathlib import Path

from selfdev.runtime.state_manager import StateManager
from selfdev.runtime.message_bus import MessageBus
from selfdev.runtime.kanban import KanbanBoard
from selfdev.tools.safety_gate import check_action, check_paths
from selfdev.tools.verification_engine import verify_required_files
from selfdev.tools.runner import validate_runner_request
from selfdev.tools.commit_gate import evaluate_commit_readiness


def test_state_manager_write_and_read(tmp_path: Path):
    manager = StateManager(tmp_path)
    manager.write_state("task-001", {"task_id": "task-001", "status": "in_progress"})
    state = manager.read_state("task-001")
    assert state["task_id"] == "task-001"
    assert state["status"] == "in_progress"


def test_message_bus_send_and_read(tmp_path: Path):
    bus = MessageBus(tmp_path)
    bus.send({
        "message_id": "msg-001",
        "from_agent": "siwa",
        "to_agent": "adit",
        "task_id": "task-001",
        "message_type": "task_assignment",
    })
    message = bus.read("adit", "msg-001")
    assert message["from_agent"] == "siwa"
    assert message["to_agent"] == "adit"


def test_kanban_create_and_update(tmp_path: Path):
    board = KanbanBoard(tmp_path)
    board.create_task({
        "task_id": "task-001",
        "title": "Test task",
        "status": "todo",
    })
    board.update_status("task-001", "in_progress")
    task = board.get_task("task-001")
    assert task["status"] == "in_progress"


def test_safety_gate_blocks_denied_action():
    result = check_action("git_push")
    assert result.status == "BLOCK"


def test_safety_gate_blocks_denied_path():
    result = check_paths([".env"])
    assert result.status == "BLOCK"


def test_verification_engine_checks_required_files(tmp_path: Path):
    existing = tmp_path / "ok.txt"
    existing.write_text("ok", encoding="utf-8")
    result = verify_required_files([str(existing), str(tmp_path / "missing.txt")])
    assert result.status == "FAIL"
    assert result.checks[str(existing)] == "PASS"


def test_runner_blocks_denied_action():
    result = validate_runner_request("terraform_destroy")
    assert result.status == "BLOCKED"


def test_commit_gate_requires_all_requirements():
    result = evaluate_commit_readiness({
        "senior_review": True,
        "safety_gate": True,
        "verification": False,
    })
    assert result.status == "BLOCKED"
    assert "verification" in result.missing
