"""Minimal file-based Kanban board."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VALID_STATUSES = {
    "todo",
    "picked",
    "in_progress",
    "blocked",
    "needs_review",
    "needs_revision",
    "ready_for_senior",
    "ready_for_verification",
    "verification_failed",
    "verified",
    "commit_ready",
    "done",
    "rejected",
    "human_required",
}


class KanbanBoard:
    def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
        self.workspace = Path(workspace)
        self.board_dir = self.workspace / "kanban"
        self.board_dir.mkdir(parents=True, exist_ok=True)
        self.board_path = self.board_dir / "board.json"
        if not self.board_path.exists():
            self._write({"tasks": {}})

    def _read(self) -> dict[str, Any]:
        return json.loads(self.board_path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self.board_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def create_task(self, task: dict[str, Any]) -> None:
        task_id = task.get("task_id")
        if not task_id:
            raise ValueError("task.task_id is required")

        status = task.get("status", "todo")
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        data = self._read()
        data.setdefault("tasks", {})

        if task_id in data["tasks"]:
            raise ValueError(f"Task already exists: {task_id}")

        task.setdefault("status", status)
        task.setdefault("artifacts", {})
        task.setdefault("blocked_by", [])
        data["tasks"][task_id] = task
        self._write(data)

    def update_status(self, task_id: str, status: str) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        data = self._read()
        if task_id not in data.get("tasks", {}):
            raise KeyError(f"Task not found: {task_id}")

        data["tasks"][task_id]["status"] = status
        self._write(data)

    def attach_artifact(self, task_id: str, artifact_type: str, artifact_id: str) -> None:
        data = self._read()
        if task_id not in data.get("tasks", {}):
            raise KeyError(f"Task not found: {task_id}")

        task = data["tasks"][task_id]
        task.setdefault("artifacts", {})
        task["artifacts"][artifact_type] = artifact_id
        self._write(data)

    def get_task(self, task_id: str) -> dict[str, Any]:
        data = self._read()
        if task_id not in data.get("tasks", {}):
            raise KeyError(f"Task not found: {task_id}")
        return data["tasks"][task_id]
