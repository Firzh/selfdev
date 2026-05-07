from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from selfdev.runtime.full_dry_run import run_full_dry_run


def manifest_data(task_id: str = "task-dry-run-001") -> dict:
    return {
        "task_id": task_id,
        "title": "Full dry run test",
        "risk_level": "low",
        "mode": "plan",
        "task_type": "documentation",
        "target_id": "selfdev",
        "objective": "Run a safe deterministic full dry run for SelfDev.",
        "allowed_paths": ["docs/"],
        "denied_paths": [".env", ".env.*", ".git/", "data/secrets/"],
        "required_outputs": ["docs_plan", "doc_gap_report"],
        "required_reviews": ["senior_reviewer"],
        "stop_conditions": ["manifest_invalid", "scope_unclear"],
        "human_gate_required": False,
    }


def write_manifest(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_full_dry_run_completes(tmp_path: Path):
    workspace = tmp_path / "workspace"
    manifest = write_manifest(tmp_path, manifest_data())

    result = run_full_dry_run(
        manifest_path=manifest,
        workspace=workspace,
    )

    assert result.status == "dry_run_complete"
    assert result.task_id == "task-dry-run-001"

    expected_stages = {
        "manifest_validation",
        "dispatch",
        "mock_artifact_reply",
        "artifact_collection",
        "senior_review",
        "safety",
        "verification",
        "runner",
        "commit_readiness",
    }

    assert expected_stages <= set(result.stages)

    board = json.loads((workspace / "kanban" / "board.json").read_text(encoding="utf-8"))
    task = board["tasks"]["task-dry-run-001"]
    assert task["status"] == "commit_ready"
    assert "docs_plan" in task["artifacts"]
    assert "doc_gap_report" in task["artifacts"]
    assert "senior_review" in task["artifacts"]
    assert "safety_report" in task["artifacts"]
    assert "verification_report" in task["artifacts"]
    assert "runner_report" in task["artifacts"]
    assert "commit_request" in task["artifacts"]

    registry = json.loads((workspace / "artifacts" / "index.json").read_text(encoding="utf-8"))
    assert len(registry["artifacts"]) >= 7

    state = json.loads((workspace / "state" / "task-dry-run-001.state.json").read_text(encoding="utf-8"))
    assert state["stage"] == "commit_readiness_completed"
    assert state["commit_status"] == "READY"


def test_full_dry_run_stops_on_denied_runner_action(tmp_path: Path):
    workspace = tmp_path / "workspace"
    manifest = write_manifest(tmp_path, manifest_data("task-dry-run-block"))

    result = run_full_dry_run(
        manifest_path=manifest,
        workspace=workspace,
        runner_action="terraform_destroy",
    )

    assert result.status == "blocked"
    assert result.stages["runner"]["runner_status"] == "BLOCKED"


def test_full_dry_run_cli_completes(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    manifest = write_manifest(tmp_path, manifest_data("task-dry-run-cli"))

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/run_full_dry_run.py",
            str(manifest),
            "--workspace",
            str(workspace),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"status": "dry_run_complete"' in result.stdout
    assert '"task_id": "task-dry-run-cli"' in result.stdout
