"""Manifest validation for SelfDev task intake."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


REQUIRED_FIELDS = {
    "task_id",
    "title",
    "risk_level",
    "mode",
    "task_type",
    "objective",
    "target_id",
    "allowed_paths",
    "denied_paths",
    "required_outputs",
    "required_reviews",
    "stop_conditions",
}

VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}
VALID_MODES = {"plan", "patch", "review", "validate", "commit_request"}

VALID_TASK_TYPES = {
    "documentation",
    "implementation",
    "implementation_with_security_risk",
    "security_review",
    "devops_review",
    "runtime_issue",
    "dependency_change",
    "tool_registry_change",
    "agent_permission_change",
    "high_risk",
    "critical",
}

DEFAULT_DENIED_PATHS = {
    ".env",
    ".env.*",
    ".git/",
    "data/secrets/",
}


@dataclass
class ManifestValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    manifest: dict[str, Any] | None = None


def load_manifest(path: Path | str) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest must be a YAML mapping")

    return data


def _is_list_of_string(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _path_matches_denied(path: str, denied_paths: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    for denied in denied_paths:
        denied_norm = denied.replace("\\", "/")
        if denied_norm.endswith("*"):
            prefix = denied_norm[:-1]
            if normalized.startswith(prefix):
                return True
        if normalized == denied_norm.rstrip("/") or normalized.startswith(denied_norm):
            return True
    return False


def validate_manifest_dict(manifest: dict[str, Any]) -> ManifestValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED_FIELDS - set(manifest))
    if missing:
        errors.append("Missing required fields: " + ", ".join(missing))

    risk_level = manifest.get("risk_level")
    if risk_level and risk_level not in VALID_RISK_LEVELS:
        errors.append(f"Invalid risk_level: {risk_level}")

    mode = manifest.get("mode")
    if mode and mode not in VALID_MODES:
        errors.append(f"Invalid mode: {mode}")

    task_type = manifest.get("task_type")
    if task_type and task_type not in VALID_TASK_TYPES:
        errors.append(f"Invalid task_type: {task_type}")

    allowed_paths = manifest.get("allowed_paths")
    denied_paths = manifest.get("denied_paths")

    if allowed_paths is not None and not _is_list_of_string(allowed_paths):
        errors.append("allowed_paths must be a list of strings")

    if denied_paths is not None and not _is_list_of_string(denied_paths):
        errors.append("denied_paths must be a list of strings")

    if isinstance(denied_paths, list):
        missing_default_denied = sorted(DEFAULT_DENIED_PATHS - set(denied_paths))
        if missing_default_denied:
            warnings.append("Recommended denied_paths missing: " + ", ".join(missing_default_denied))

    if isinstance(allowed_paths, list) and isinstance(denied_paths, list):
        for allowed_path in allowed_paths:
            if _path_matches_denied(allowed_path, denied_paths):
                errors.append(f"allowed_paths contains denied path: {allowed_path}")

    required_outputs = manifest.get("required_outputs")
    if required_outputs is not None and not _is_list_of_string(required_outputs):
        errors.append("required_outputs must be a list of strings")

    required_reviews = manifest.get("required_reviews")
    if required_reviews is not None and not _is_list_of_string(required_reviews):
        errors.append("required_reviews must be a list of strings")

    stop_conditions = manifest.get("stop_conditions")
    if stop_conditions is not None and not _is_list_of_string(stop_conditions):
        errors.append("stop_conditions must be a list of strings")

    objective = manifest.get("objective")
    if isinstance(objective, str) and len(objective.strip()) < 10:
        errors.append("objective must be at least 10 characters")

    high_risk_types = {
        "dependency_change",
        "tool_registry_change",
        "agent_permission_change",
        "high_risk",
        "critical",
    }
    if task_type in high_risk_types and not manifest.get("human_gate_required", False):
        errors.append(f"{task_type} requires human_gate_required: true")

    return ManifestValidationResult(
        valid=not errors,
        errors=errors,
        warnings=warnings,
        manifest=manifest,
    )


def validate_manifest_file(path: Path | str) -> ManifestValidationResult:
    try:
        manifest = load_manifest(path)
    except Exception as exc:
        return ManifestValidationResult(valid=False, errors=[str(exc)])

    return validate_manifest_dict(manifest)
