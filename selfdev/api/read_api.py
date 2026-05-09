"""Read-only API service layer for SelfDev.

This module is intentionally framework-free. It can later be wrapped by FastAPI,
Flask, Tauri commands, or a local UI.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from selfdev.runtime.artifact_preview import DEFAULT_MAX_PREVIEW_CHARS, preview_artifact


def _safe_registry_id(value: str) -> bool:
    item_id = value.strip()
    if not item_id:
        return False
    if "/" in item_id or "\\" in item_id:
        return False
    if item_id in {".", ".."}:
        return False
    return True


@dataclass
class ReadApi:
    workspace: Path = Path("data/agent_workspace")
    config_dir: Path = Path("config/selfdev")

    def _read_json_file(self, path: Path, default: dict[str, Any]) -> dict[str, Any]:
        if not path.exists():
            return default
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"JSON file must contain object: {path}")
        return data

    def _read_yaml_file(self, path: Path, default: dict[str, Any]) -> dict[str, Any]:
        if not path.exists():
            return default
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            return default
        if not isinstance(data, dict):
            raise ValueError(f"YAML file must contain mapping: {path}")
        return data

    def _workspace_file_content(self, path_value: Any) -> tuple[str | None, str]:
        if not isinstance(path_value, str) or not path_value.strip():
            return None, "missing_path"

        raw_path = Path(path_value)
        if raw_path.is_absolute():
            candidate = raw_path.resolve()
        else:
            candidate = (self.workspace / raw_path).resolve()

        workspace_root = self.workspace.resolve()
        try:
            candidate.relative_to(workspace_root)
        except ValueError:
            return None, "unsafe_path"

        if not candidate.exists():
            return None, "missing_file"
        if not candidate.is_file():
            return None, "not_file"

        try:
            return candidate.read_text(encoding="utf-8"), "loaded"
        except UnicodeDecodeError:
            return None, "binary_or_non_utf8"

    def health(self) -> dict[str, Any]:
        required_config = [
            "agents.yaml",
            "tools.yaml",
            "routing_rules.yaml",
            "workflow.yaml",
            "targets.yaml",
            "safety_policy.yaml",
        ]
        config_status = {
            name: (self.config_dir / name).exists()
            for name in required_config
        }

        workspace_dirs = [
            "kanban",
            "agents",
            "artifacts",
            "state",
            "reviews",
            "safety",
            "verification",
            "runner",
            "approvals",
        ]
        workspace_status = {
            name: (self.workspace / name).exists()
            for name in workspace_dirs
        }

        ok = all(config_status.values())
        return {
            "service": "selfdev-read-api",
            "status": "ok" if ok else "degraded",
            "mode": "read_only",
            "config": config_status,
            "workspace": workspace_status,
        }

    def agents(self) -> dict[str, Any]:
        return self._read_yaml_file(
            self.config_dir / "agents.yaml",
            default={"agents": {}},
        )

    def tools(self) -> dict[str, Any]:
        return self._read_yaml_file(
            self.config_dir / "tools.yaml",
            default={"tools": {}},
        )

    def targets(self) -> dict[str, Any]:
        return self._read_yaml_file(
            self.config_dir / "targets.yaml",
            default={"targets": {}},
        )

    def target(self, target_id: str) -> dict[str, Any]:
        if not _safe_registry_id(target_id):
            raise ValueError("target_id must be a single registry id segment")

        targets = self.targets().get("targets", {})
        if target_id not in targets:
            return {
                "target_id": target_id,
                "exists": False,
                "target": None,
            }

        return {
            "target_id": target_id,
            "exists": True,
            "target": targets[target_id],
        }

    def kanban(self) -> dict[str, Any]:
        return self._read_json_file(
            self.workspace / "kanban" / "board.json",
            default={"tasks": {}},
        )

    def artifacts(self) -> dict[str, Any]:
        return self._read_json_file(
            self.workspace / "artifacts" / "index.json",
            default={"artifacts": {}},
        )

    def artifact(self, artifact_id: str) -> dict[str, Any]:
        if not _safe_registry_id(artifact_id):
            raise ValueError("artifact_id must be a single registry id segment")

        artifacts = self.artifacts().get("artifacts", {})
        if artifact_id not in artifacts:
            return {
                "artifact_id": artifact_id,
                "exists": False,
                "artifact": None,
                "content_status": "missing_registry_record",
                "content": None,
            }

        record = artifacts[artifact_id]
        content, content_status = self._workspace_file_content(record.get("path"))
        return {
            "artifact_id": artifact_id,
            "exists": True,
            "artifact": record,
            "content_status": content_status,
            "content": content,
        }

    def artifact_preview(
        self,
        artifact_id: str,
        max_chars: int = DEFAULT_MAX_PREVIEW_CHARS,
    ) -> dict[str, Any]:
        return preview_artifact(
            artifact_id=artifact_id,
            workspace=self.workspace,
            max_chars=max_chars,
        ).to_dict()

    def state(self, task_id: str) -> dict[str, Any]:
        if not task_id:
            raise ValueError("task_id is required")

        path = self.workspace / "state" / f"{task_id}.state.json"
        if not path.exists():
            return {
                "task_id": task_id,
                "exists": False,
                "state": None,
            }

        return {
            "task_id": task_id,
            "exists": True,
            "state": self._read_json_file(path, default={}),
        }

    def summary(self) -> dict[str, Any]:
        health = self.health()
        kanban = self.kanban()
        artifacts = self.artifacts()
        agents = self.agents()
        targets = self.targets()

        tasks = kanban.get("tasks", {})
        artifact_items = artifacts.get("artifacts", {})
        agent_items = agents.get("agents", {})
        target_items = targets.get("targets", {})

        return {
            "service": "selfdev-read-api",
            "mode": "read_only",
            "health_status": health["status"],
            "task_count": len(tasks),
            "artifact_count": len(artifact_items),
            "agent_count": len(agent_items),
            "target_count": len(target_items),
        }
