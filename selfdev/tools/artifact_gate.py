"""Artifact Gate for registered SelfDev outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from selfdev.runtime.artifact_registry import VALID_ARTIFACT_TYPES


@dataclass
class ArtifactGateResult:
    status: str
    reasons: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def _is_within_workspace(path: Path, workspace: Path) -> bool:
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def validate_artifact_record(record: dict, workspace: Path | str = "data/agent_workspace") -> ArtifactGateResult:
    reasons: list[str] = []
    workspace_path = Path(workspace)

    required_fields = {
        "artifact_id",
        "task_id",
        "agent_id",
        "artifact_type",
        "path",
    }

    missing = sorted(required_fields - set(record))
    if missing:
        reasons.append("Missing artifact fields: " + ", ".join(missing))
        return ArtifactGateResult(status="FAIL", reasons=reasons)

    artifact_type = record.get("artifact_type")
    if artifact_type not in VALID_ARTIFACT_TYPES:
        reasons.append(f"Invalid artifact_type: {artifact_type}")

    artifact_path = Path(record["path"])

    if not artifact_path.is_absolute():
        artifact_path = workspace_path / artifact_path

    if not _is_within_workspace(artifact_path, workspace_path):
        reasons.append(f"Artifact path escapes workspace: {record['path']}")

    if not artifact_path.exists():
        reasons.append(f"Artifact file missing: {artifact_path}")
    elif artifact_path.stat().st_size == 0:
        reasons.append(f"Artifact file is empty: {artifact_path}")

    if reasons:
        return ArtifactGateResult(status="FAIL", reasons=reasons)

    return ArtifactGateResult(status="PASS", reasons=[])


def validate_required_artifacts(
    records: list[dict],
    required_types: list[str],
) -> ArtifactGateResult:
    existing_types = {record.get("artifact_type") for record in records}
    missing = sorted(set(required_types) - existing_types)

    if missing:
        return ArtifactGateResult(
            status="FAIL",
            reasons=["Missing required artifact types: " + ", ".join(missing)],
        )

    return ArtifactGateResult(status="PASS", reasons=[])
