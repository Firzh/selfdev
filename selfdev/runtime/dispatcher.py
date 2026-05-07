"""Dispatch manifest into Kanban, State, and Message Bus."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import time

from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.message_bus import MessageBus
from selfdev.runtime.routing_gate import RoutingDecision, resolve_manifest_file
from selfdev.runtime.state_manager import StateManager
from selfdev.runtime.manifest_validator import load_manifest


@dataclass
class DispatchResult:
    task_id: str
    status: str
    decision: str
    target_agent: str | None = None
    message_path: str | None = None
    state_path: str | None = None
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "decision": self.decision,
            "target_agent": self.target_agent,
            "message_path": self.message_path,
            "state_path": self.state_path,
            "reasons": self.reasons,
        }


def _now_run_id() -> str:
    return time.strftime("run-%Y%m%d-%H%M%S")


def _create_or_update_task(board: KanbanBoard, task: dict[str, Any]) -> None:
    try:
        board.create_task(task)
    except ValueError as exc:
        if "already exists" not in str(exc):
            raise
        board.update_status(task["task_id"], task["status"])


def _build_kanban_task(manifest: dict[str, Any], decision: RoutingDecision, status: str) -> dict[str, Any]:
    return {
        "task_id": manifest["task_id"],
        "title": manifest["title"],
        "status": status,
        "priority": manifest.get("priority", "medium"),
        "risk_level": manifest["risk_level"],
        "target_id": manifest["target_id"],
        "owner_agent": decision.primary_agent or "human_owner",
        "assigned_by": "human_owner",
        "task_type": manifest["task_type"],
        "required_review": decision.required_review,
        "artifacts": {},
        "blocked_by": [],
    }


def _build_assignment_message(
    manifest: dict[str, Any],
    decision: RoutingDecision,
    run_id: str,
) -> dict[str, Any]:
    if not decision.primary_agent:
        raise ValueError("Routing decision has no primary_agent")

    return {
        "message_id": f"msg-{manifest['task_id']}-assignment",
        "run_id": run_id,
        "from_agent": "siwa",
        "to_agent": decision.primary_agent,
        "task_id": manifest["task_id"],
        "message_type": "task_assignment",
        "priority": manifest.get("priority", "medium"),
        "objective": manifest["objective"],
        "target_id": manifest["target_id"],
        "allowed_paths": manifest["allowed_paths"],
        "denied_paths": manifest["denied_paths"],
        "required_outputs": manifest["required_outputs"],
        "required_reviews": manifest["required_reviews"],
        "stop_conditions": manifest["stop_conditions"],
    }


def dispatch_manifest_file(
    manifest_path: Path | str,
    workspace: Path | str = "data/agent_workspace",
    routing_rules_path: Path | str = "config/selfdev/routing_rules.yaml",
) -> DispatchResult:
    manifest = load_manifest(manifest_path)
    decision = resolve_manifest_file(manifest_path, routing_rules_path)
    task_id = str(manifest.get("task_id", "unknown"))
    run_id = _now_run_id()

    board = KanbanBoard(workspace)
    state = StateManager(workspace)
    bus = MessageBus(workspace)

    if decision.decision == "manifest_invalid":
        state_path = state.write_state(task_id, {
            "task_id": task_id,
            "run_id": run_id,
            "stage": "manifest_invalid",
            "status": "blocked",
            "reason": decision.reasons,
            "retry_count": 0,
        })
        return DispatchResult(
            task_id=task_id,
            status="blocked",
            decision=decision.decision,
            state_path=str(state_path),
            reasons=decision.reasons,
        )

    if decision.decision == "human_required":
        kanban_task = _build_kanban_task(manifest, decision, "human_required")
        _create_or_update_task(board, kanban_task)

        state_path = state.write_state(task_id, {
            "task_id": task_id,
            "run_id": run_id,
            "stage": "waiting_for_human",
            "status": "human_required",
            "current_agent": decision.primary_agent,
            "reason": decision.reasons,
            "retry_count": 0,
        })

        return DispatchResult(
            task_id=task_id,
            status="human_required",
            decision=decision.decision,
            target_agent=decision.primary_agent,
            state_path=str(state_path),
            reasons=decision.reasons,
        )

    if decision.decision != "route":
        raise ValueError(f"Unsupported routing decision: {decision.decision}")

    kanban_task = _build_kanban_task(manifest, decision, "in_progress")
    _create_or_update_task(board, kanban_task)

    message = _build_assignment_message(manifest, decision, run_id)
    message_path = bus.send(message)

    state_path = state.write_state(task_id, {
        "task_id": task_id,
        "run_id": run_id,
        "stage": "dispatched",
        "status": "in_progress",
        "current_agent": decision.primary_agent,
        "last_successful_checkpoint": "message_dispatched",
        "message_id": message["message_id"],
        "retry_count": 0,
    })

    return DispatchResult(
        task_id=task_id,
        status="dispatched",
        decision=decision.decision,
        target_agent=decision.primary_agent,
        message_path=str(message_path),
        state_path=str(state_path),
        reasons=decision.reasons,
    )
