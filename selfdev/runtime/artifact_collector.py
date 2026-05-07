"""Collect artifact_ready replies from agent outbox."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from selfdev.runtime.artifact_registry import ArtifactRecord, ArtifactRegistry
from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.state_manager import StateManager
from selfdev.tools.artifact_gate import validate_artifact_record, validate_required_artifacts


@dataclass
class ArtifactCollectionResult:
    task_id: str
    status: str
    registered_artifacts: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    state_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "registered_artifacts": self.registered_artifacts,
            "reasons": self.reasons,
            "state_path": self.state_path,
        }


def _now_run_id() -> str:
    return time.strftime("run-%Y%m%d-%H%M%S")


def load_reply(path: Path | str) -> dict[str, Any]:
    reply_path = Path(path)
    if not reply_path.exists():
        raise FileNotFoundError(f"Artifact reply not found: {reply_path}")

    data = json.loads(reply_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Artifact reply must be a JSON object")

    return data


def validate_reply_shape(reply: dict[str, Any]) -> list[str]:
    required = {
        "message_id",
        "from_agent",
        "to_agent",
        "task_id",
        "message_type",
        "status",
        "artifacts",
    }
    missing = sorted(required - set(reply))
    errors: list[str] = []

    if missing:
        errors.append("Missing reply fields: " + ", ".join(missing))

    if reply.get("message_type") != "artifact_ready":
        errors.append("Reply message_type must be artifact_ready")

    if reply.get("to_agent") != "siwa":
        errors.append("Artifact reply must be addressed to siwa")

    if not isinstance(reply.get("artifacts"), dict):
        errors.append("reply.artifacts must be a mapping")

    return errors


def collect_artifact_reply(
    reply_path: Path | str,
    workspace: Path | str = "data/agent_workspace",
    required_artifact_types: list[str] | None = None,
) -> ArtifactCollectionResult:
    workspace_path = Path(workspace)
    reply = load_reply(reply_path)
    errors = validate_reply_shape(reply)

    task_id = str(reply.get("task_id", "unknown"))
    agent_id = str(reply.get("from_agent", "unknown"))
    run_id = str(reply.get("run_id") or _now_run_id())

    state = StateManager(workspace_path)

    if errors:
        state_path = state.write_state(task_id, {
            "task_id": task_id,
            "run_id": run_id,
            "stage": "artifact_reply_invalid",
            "status": "blocked",
            "reason": errors,
            "retry_count": 0,
        })
        return ArtifactCollectionResult(
            task_id=task_id,
            status="blocked",
            reasons=errors,
            state_path=str(state_path),
        )

    registry = ArtifactRegistry(workspace_path)
    board = KanbanBoard(workspace_path)

    registered_ids: list[str] = []
    validation_records: list[dict[str, Any]] = []
    reasons: list[str] = []

    for artifact_type, artifact_path in reply["artifacts"].items():
        artifact_id = f"{task_id}.{agent_id}.{artifact_type}"

        record = ArtifactRecord(
            artifact_id=artifact_id,
            task_id=task_id,
            agent_id=agent_id,
            artifact_type=artifact_type,
            path=str(artifact_path),
            status="collected",
        )

        gate_result = validate_artifact_record(record.to_dict(), workspace=workspace_path)
        if not gate_result.passed:
            reasons.extend(gate_result.reasons)
            continue

        try:
            registry.register(record)
        except ValueError as exc:
            if "already registered" not in str(exc):
                reasons.append(str(exc))
                continue

        try:
            board.attach_artifact(task_id, artifact_type, artifact_id)
        except KeyError:
            reasons.append(f"Kanban task not found while attaching artifact: {task_id}")

        registered_ids.append(artifact_id)
        validation_records.append(record.to_dict())

    if required_artifact_types:
        required_result = validate_required_artifacts(validation_records, required_artifact_types)
        if not required_result.passed:
            reasons.extend(required_result.reasons)

    if reasons:
        try:
            board.update_status(task_id, "needs_revision")
        except KeyError:
            pass

        state_path = state.write_state(task_id, {
            "task_id": task_id,
            "run_id": run_id,
            "stage": "artifact_collection_failed",
            "status": "needs_revision",
            "current_agent": agent_id,
            "reason": reasons,
            "registered_artifacts": registered_ids,
            "retry_count": 0,
        })

        return ArtifactCollectionResult(
            task_id=task_id,
            status="needs_revision",
            registered_artifacts=registered_ids,
            reasons=reasons,
            state_path=str(state_path),
        )

    try:
        board.update_status(task_id, "ready_for_senior")
    except KeyError:
        pass

    state_path = state.write_state(task_id, {
        "task_id": task_id,
        "run_id": run_id,
        "stage": "artifact_collected",
        "status": "ready_for_senior",
        "current_agent": "senior_reviewer",
        "last_successful_checkpoint": "artifact_collected",
        "registered_artifacts": registered_ids,
        "retry_count": 0,
    })

    return ArtifactCollectionResult(
        task_id=task_id,
        status="ready_for_senior",
        registered_artifacts=registered_ids,
        reasons=[],
        state_path=str(state_path),
    )
