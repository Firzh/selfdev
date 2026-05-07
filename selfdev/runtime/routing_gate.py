"""Deterministic routing gate for SelfDev."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml

from selfdev.runtime.manifest_validator import validate_manifest_dict, load_manifest


@dataclass
class RoutingDecision:
    task_id: str
    task_type: str
    decision: str
    primary_agent: str | None = None
    required_review: list[str] = field(default_factory=list)
    requires_human_review: bool = False
    automation_allowed: bool = True
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "decision": self.decision,
            "primary_agent": self.primary_agent,
            "required_review": self.required_review,
            "requires_human_review": self.requires_human_review,
            "automation_allowed": self.automation_allowed,
            "reasons": self.reasons,
        }


def load_routing_rules(path: Path | str = "config/selfdev/routing_rules.yaml") -> dict[str, Any]:
    route_path = Path(path)
    if not route_path.exists():
        raise FileNotFoundError(f"Routing rules file not found: {route_path}")

    data = yaml.safe_load(route_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("routing_rules.yaml must be a YAML mapping")

    rules = data.get("routing_rules")
    if not isinstance(rules, dict):
        raise ValueError("routing_rules.yaml must contain mapping key: routing_rules")

    return rules


def resolve_route(manifest: dict[str, Any], routing_rules: dict[str, Any]) -> RoutingDecision:
    validation = validate_manifest_dict(manifest)
    task_id = str(manifest.get("task_id", "unknown"))
    task_type = str(manifest.get("task_type", "unknown"))

    if not validation.valid:
        return RoutingDecision(
            task_id=task_id,
            task_type=task_type,
            decision="manifest_invalid",
            reasons=validation.errors,
            automation_allowed=False,
        )

    rule = routing_rules.get(task_type)
    if not rule:
        return RoutingDecision(
            task_id=task_id,
            task_type=task_type,
            decision="human_required",
            reasons=[f"No routing rule found for task_type: {task_type}"],
            automation_allowed=False,
            requires_human_review=True,
        )

    primary = rule.get("primary")
    required_review = rule.get("required_review", [])
    requires_human = bool(rule.get("requires_human_review", False))
    automation_allowed = bool(rule.get("automation_allowed", True))

    if not primary:
        return RoutingDecision(
            task_id=task_id,
            task_type=task_type,
            decision="human_required",
            reasons=[f"Routing rule for {task_type} has no primary agent"],
            automation_allowed=False,
            requires_human_review=True,
        )

    decision = "human_required" if requires_human or primary == "human_owner" else "route"

    return RoutingDecision(
        task_id=task_id,
        task_type=task_type,
        decision=decision,
        primary_agent=primary,
        required_review=list(required_review),
        requires_human_review=requires_human,
        automation_allowed=automation_allowed,
        reasons=[f"Matched routing rule for task_type: {task_type}"],
    )


def resolve_manifest_file(
    manifest_path: Path | str,
    routing_rules_path: Path | str = "config/selfdev/routing_rules.yaml",
) -> RoutingDecision:
    manifest = load_manifest(manifest_path)
    routing_rules = load_routing_rules(routing_rules_path)
    return resolve_route(manifest, routing_rules)
