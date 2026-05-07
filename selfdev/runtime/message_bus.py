"""File-based message bus for agent inbox and outbox."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_MESSAGE_FIELDS = {
    "message_id",
    "from_agent",
    "to_agent",
    "task_id",
    "message_type",
}


class MessageBus:
    def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
        self.workspace = Path(workspace)
        self.agents_dir = self.workspace / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)

    def _validate_message(self, message: dict[str, Any]) -> None:
        missing = REQUIRED_MESSAGE_FIELDS - set(message)
        if missing:
            raise ValueError(f"Missing message fields: {sorted(missing)}")

    def inbox_dir(self, agent_id: str) -> Path:
        path = self.agents_dir / agent_id / "inbox"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def outbox_dir(self, agent_id: str) -> Path:
        path = self.agents_dir / agent_id / "outbox"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def send(self, message: dict[str, Any]) -> Path:
        self._validate_message(message)
        target = message["to_agent"]
        message_id = message["message_id"]
        path = self.inbox_dir(target) / f"{message_id}.json"
        path.write_text(json.dumps(message, indent=2, ensure_ascii=False), encoding="utf-8")

        sender = message["from_agent"]
        outbox_path = self.outbox_dir(sender) / f"{message_id}.json"
        outbox_path.write_text(json.dumps(message, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def read(self, agent_id: str, message_id: str, box: str = "inbox") -> dict[str, Any]:
        if box not in {"inbox", "outbox"}:
            raise ValueError("box must be inbox or outbox")
        base = self.inbox_dir(agent_id) if box == "inbox" else self.outbox_dir(agent_id)
        path = base / f"{message_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Message not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))
