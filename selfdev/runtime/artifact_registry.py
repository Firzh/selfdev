"""File-based artifact registry for SelfDev."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


VALID_ARTIFACT_TYPES = {
    "orchestration_plan",
    "implementation_plan",
    "draft_patch",
    "docs_plan",
    "docs_patch",
    "doc_gap_report",
    "security_review",
    "devops_review",
    "runtime_review",
    "senior_review",
    "safety_report",
    "runner_report",
    "verification_report",
    "commit_request",
    "error_report",
    "performance_warning",
}


@dataclass
class ArtifactRecord:
    artifact_id: str
    task_id: str
    agent_id: str
    artifact_type: str
    path: str
    status: str = "registered"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "artifact_type": self.artifact_type,
            "path": self.path,
            "status": self.status,
            "metadata": self.metadata,
        }


class ArtifactRegistry:
    def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
        self.workspace = Path(workspace)
        self.registry_dir = self.workspace / "artifacts"
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.registry_dir / "index.json"
        if not self.index_path.exists():
            self._write({"artifacts": {}})

    def _read(self) -> dict[str, Any]:
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self.index_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def register(self, record: ArtifactRecord) -> None:
        if record.artifact_type not in VALID_ARTIFACT_TYPES:
            raise ValueError(f"Invalid artifact_type: {record.artifact_type}")

        data = self._read()
        data.setdefault("artifacts", {})

        if record.artifact_id in data["artifacts"]:
            raise ValueError(f"Artifact already registered: {record.artifact_id}")

        data["artifacts"][record.artifact_id] = record.to_dict()
        self._write(data)

    def get(self, artifact_id: str) -> dict[str, Any]:
        data = self._read()
        artifacts = data.get("artifacts", {})
        if artifact_id not in artifacts:
            raise KeyError(f"Artifact not found: {artifact_id}")
        return artifacts[artifact_id]

    def list_for_task(self, task_id: str) -> list[dict[str, Any]]:
        data = self._read()
        return [
            item
            for item in data.get("artifacts", {}).values()
            if item.get("task_id") == task_id
        ]
