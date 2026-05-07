"""Action availability model for SelfDev.

This module decides which UI/API actions are currently available for a task.
It is read-only and does not mutate workspace state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CORE_ACTIONS = [
    "approve_for_runner",
    "request_revision",
    "request_specialist_review",
    "run_safety_gate",
    "run_verification",
    "request_runner",
    "evaluate_commit_readiness",
    "approve_human_gate",
    "reject",
]


REQUIRED_COMMIT_ARTIFACTS = {
    "senior_review",
    "safety_report",
    "verification_report",
    "runner_report",
}


@dataclass
class ActionAvailabilityResult:
    task_id: str
    exists: bool
    status: str | None
    available_actions: dict[str, bool] = field(default_factory=dict)
    reasons: dict[str, str] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "exists": self.exists,
            "status": self.status,
            "available_actions": self.available_actions,
            "reasons": self.reasons,
            "artifacts": self.artifacts,
        }


def _default_actions() -> dict[str, bool]:
    return {action: False for action in CORE_ACTIONS}


def _default_reasons() -> dict[str, str]:
    return {action: "Action is not available for current task state." for action in CORE_ACTIONS}


def _load_board(workspace: Path) -> dict[str, Any]:
    board_path = workspace / "kanban" / "board.json"
    if not board_path.exists():
        return {"tasks": {}}

    data = json.loads(board_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Kanban board must contain JSON object: {board_path}")

    return data


def get_action_availability(
    task_id: str,
    workspace: Path | str = "data/agent_workspace",
) -> ActionAvailabilityResult:
    if not task_id:
        raise ValueError("task_id is required")

    workspace_path = Path(workspace)
    board = _load_board(workspace_path)
    tasks = board.get("tasks", {})

    actions = _default_actions()
    reasons = _default_reasons()

    if task_id not in tasks:
        for action in CORE_ACTIONS:
            reasons[action] = "Task does not exist."
        return ActionAvailabilityResult(
            task_id=task_id,
            exists=False,
            status=None,
            available_actions=actions,
            reasons=reasons,
            artifacts={},
        )

    task = tasks[task_id]
    status = task.get("status")
    artifacts = task.get("artifacts", {})
    if not isinstance(artifacts, dict):
        artifacts = {}

    if status in {"ready_for_senior", "needs_review"}:
        actions["approve_for_runner"] = True
        reasons["approve_for_runner"] = "Task is ready for Senior Reviewer decision."

        actions["request_revision"] = True
        reasons["request_revision"] = "Reviewer can request revision."

        actions["request_specialist_review"] = True
        reasons["request_specialist_review"] = "Reviewer can request specialist review."

        actions["reject"] = True
        reasons["reject"] = "Reviewer can reject the task."

    if status in {"needs_revision", "verification_failed"}:
        actions["request_revision"] = True
        reasons["request_revision"] = "Task needs revision."

    if status == "ready_for_verification":
        if "safety_report" not in artifacts:
            actions["run_safety_gate"] = True
            reasons["run_safety_gate"] = "Safety report is missing and task is ready for safety check."
            reasons["run_verification"] = "Safety report is required before verification."
        else:
            actions["run_verification"] = True
            reasons["run_verification"] = "Safety report exists and task is ready for verification."
            reasons["run_safety_gate"] = "Safety report already exists."

    if status == "verified":
        if "verification_report" in artifacts:
            actions["request_runner"] = True
            reasons["request_runner"] = "Verification report exists and task is verified."
        else:
            reasons["request_runner"] = "Verification report is missing."

    if status == "commit_ready":
        actions["evaluate_commit_readiness"] = True
        reasons["evaluate_commit_readiness"] = "Task is ready for Commit Gate readiness evaluation."

        missing_commit_artifacts = sorted(REQUIRED_COMMIT_ARTIFACTS - set(artifacts))
        if missing_commit_artifacts:
            reasons["evaluate_commit_readiness"] = (
                "Task is commit_ready, but Commit Gate may block because artifacts are missing: "
                + ", ".join(missing_commit_artifacts)
            )

    if status == "human_required":
        actions["approve_human_gate"] = True
        reasons["approve_human_gate"] = "Task requires Human Owner approval."

        actions["reject"] = True
        reasons["reject"] = "Human Owner can reject the task."

    if status == "blocked":
        actions["reject"] = True
        reasons["reject"] = "Blocked task can be rejected or manually resolved."

    return ActionAvailabilityResult(
        task_id=task_id,
        exists=True,
        status=status,
        available_actions=actions,
        reasons=reasons,
        artifacts=artifacts,
    )
