from __future__ import annotations

from pathlib import Path
import yaml

from selfdev.runtime.manifest_validator import (
    validate_manifest_dict,
    validate_manifest_file,
)


def valid_manifest() -> dict:
    return {
        "task_id": "task-001",
        "title": "Valid task",
        "risk_level": "low",
        "mode": "plan",
        "task_type": "documentation",
        "target_id": "selfdev",
        "objective": "Create a safe documentation plan.",
        "allowed_paths": ["README.md", "docs/"],
        "denied_paths": [".env", ".env.*", ".git/", "data/secrets/"],
        "required_outputs": ["docs_plan"],
        "required_reviews": ["senior_reviewer"],
        "stop_conditions": ["manifest_invalid"],
        "human_gate_required": False,
    }


def test_valid_manifest_dict_passes():
    result = validate_manifest_dict(valid_manifest())
    assert result.valid is True
    assert result.errors == []


def test_missing_required_field_fails():
    manifest = valid_manifest()
    manifest.pop("task_id")
    result = validate_manifest_dict(manifest)
    assert result.valid is False
    assert any("Missing required fields" in error for error in result.errors)


def test_invalid_risk_level_fails():
    manifest = valid_manifest()
    manifest["risk_level"] = "danger"
    result = validate_manifest_dict(manifest)
    assert result.valid is False
    assert "Invalid risk_level: danger" in result.errors


def test_denied_path_in_allowed_paths_fails():
    manifest = valid_manifest()
    manifest["allowed_paths"] = [".env"]
    result = validate_manifest_dict(manifest)
    assert result.valid is False
    assert any("allowed_paths contains denied path" in error for error in result.errors)


def test_high_risk_task_requires_human_gate():
    manifest = valid_manifest()
    manifest["task_type"] = "dependency_change"
    manifest["risk_level"] = "high"
    manifest["human_gate_required"] = False
    result = validate_manifest_dict(manifest)
    assert result.valid is False
    assert any("requires human_gate_required" in error for error in result.errors)


def test_manifest_file_validation(tmp_path: Path):
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(valid_manifest()), encoding="utf-8")
    result = validate_manifest_file(path)
    assert result.valid is True
