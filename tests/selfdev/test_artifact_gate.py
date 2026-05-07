from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from selfdev.runtime.artifact_registry import ArtifactRecord, ArtifactRegistry
from selfdev.tools.artifact_gate import validate_artifact_record, validate_required_artifacts


def test_artifact_registry_register_and_get(tmp_path: Path):
    artifact_file = tmp_path / "docs" / "task-001.docs_plan.md"
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    artifact_file.write_text("# Docs Plan\n", encoding="utf-8")

    registry = ArtifactRegistry(tmp_path)
    record = ArtifactRecord(
        artifact_id="artifact-001",
        task_id="task-001",
        agent_id="adit",
        artifact_type="docs_plan",
        path="docs/task-001.docs_plan.md",
    )

    registry.register(record)
    loaded = registry.get("artifact-001")

    assert loaded["task_id"] == "task-001"
    assert loaded["agent_id"] == "adit"
    assert loaded["artifact_type"] == "docs_plan"


def test_artifact_gate_passes_valid_artifact(tmp_path: Path):
    artifact_file = tmp_path / "docs" / "task-001.docs_plan.md"
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    artifact_file.write_text("# Docs Plan\n", encoding="utf-8")

    record = {
        "artifact_id": "artifact-001",
        "task_id": "task-001",
        "agent_id": "adit",
        "artifact_type": "docs_plan",
        "path": "docs/task-001.docs_plan.md",
    }

    result = validate_artifact_record(record, workspace=tmp_path)
    assert result.status == "PASS"


def test_artifact_gate_fails_empty_artifact(tmp_path: Path):
    artifact_file = tmp_path / "docs" / "empty.md"
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    artifact_file.write_text("", encoding="utf-8")

    record = {
        "artifact_id": "artifact-empty",
        "task_id": "task-001",
        "agent_id": "adit",
        "artifact_type": "docs_plan",
        "path": "docs/empty.md",
    }

    result = validate_artifact_record(record, workspace=tmp_path)
    assert result.status == "FAIL"
    assert any("empty" in reason for reason in result.reasons)


def test_artifact_gate_blocks_path_escape(tmp_path: Path):
    outside = tmp_path.parent / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")

    record = {
        "artifact_id": "artifact-outside",
        "task_id": "task-001",
        "agent_id": "adit",
        "artifact_type": "docs_plan",
        "path": str(outside),
    }

    result = validate_artifact_record(record, workspace=tmp_path)
    assert result.status == "FAIL"
    assert any("escapes workspace" in reason for reason in result.reasons)


def test_required_artifacts_fail_when_missing_type():
    records = [
        {
            "artifact_id": "artifact-001",
            "task_id": "task-001",
            "agent_id": "adit",
            "artifact_type": "docs_plan",
            "path": "docs/task-001.docs_plan.md",
        }
    ]

    result = validate_required_artifacts(records, ["docs_plan", "doc_gap_report"])
    assert result.status == "FAIL"
    assert "doc_gap_report" in result.reasons[0]


def test_register_artifact_cli(tmp_path: Path):
    artifact_file = tmp_path / "docs" / "task-001.docs_plan.md"
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    artifact_file.write_text("# Docs Plan\n", encoding="utf-8")

    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/register_artifact.py",
            "--workspace",
            str(tmp_path),
            "--artifact-id",
            "artifact-001",
            "--task-id",
            "task-001",
            "--agent-id",
            "adit",
            "--artifact-type",
            "docs_plan",
            "--path",
            "docs/task-001.docs_plan.md",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"artifact_id": "artifact-001"' in result.stdout
