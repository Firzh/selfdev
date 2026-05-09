"""Read-only API service layer for SelfDev.

This module is intentionally framework-free. It can later be wrapped by FastAPI,
Flask, Tauri commands, or a local UI.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml


def _safe_registry_id(raw_value: str) -> str | None:
    value = unquote(raw_value).strip()
    if not value:
        return None
    if "/" in value or "\\" in value:
        return None
    if value in {".", ".."}:
        return None
    return value


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
        payload = self._read_yaml_file(
            self.config_dir / "targets.yaml",
            default={"targets": {}},
        )
        targets = payload.get("targets", {})
        if targets is None:
            targets = {}
        if not isinstance(targets, dict):
            raise ValueError("targets.yaml must contain a 'targets' mapping")
        return {"targets": targets}

    def target(self, target_id: str) -> dict[str, Any]:
        safe_target_id = _safe_registry_id(target_id)
        if safe_target_id is None:
            raise ValueError("target_id must be a single path segment")
        targets = self.targets().get("targets", {})
        target = targets.get(safe_target_id)
        if target is None:
            return {
                "target_id": safe_target_id,
                "exists": False,
                "target": None,
            }
        if not isinstance(target, dict):
            raise ValueError(f"target entry must be a mapping: {safe_target_id}")
        return {
            "target_id": safe_target_id,
            "exists": True,
            "target": target,
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
