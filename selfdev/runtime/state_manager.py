"""File-based workflow state manager."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateManager:
    def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
        self.workspace = Path(workspace)
        self.state_dir = self.workspace / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def state_path(self, task_id: str) -> Path:
        if not task_id:
            raise ValueError("task_id is required")
        return self.state_dir / f"{task_id}.state.json"

    def write_state(self, task_id: str, state: dict[str, Any]) -> Path:
        if state.get("task_id") != task_id:
            raise ValueError("state.task_id must match task_id")
        path = self.state_path(task_id)
        path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def read_state(self, task_id: str) -> dict[str, Any]:
        path = self.state_path(task_id)
        if not path.exists():
            raise FileNotFoundError(f"State file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def exists(self, task_id: str) -> bool:
        return self.state_path(task_id).exists()
