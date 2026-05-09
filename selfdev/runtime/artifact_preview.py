"""Redacted artifact preview helpers for SelfDev.

The helper is deterministic and local-only. It reads the artifact registry from
``workspace/artifacts/index.json``, validates that the artifact path remains
inside the workspace, loads text content when safe, and applies the redaction
service before returning preview data.

It does not execute shell commands, call an LLM, apply patches, or mutate files.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from selfdev.runtime.redaction import RedactionService


DEFAULT_WORKSPACE = Path("data/agent_workspace")
DEFAULT_MAX_PREVIEW_CHARS = 12_000
# Backward-compatible alias for the brief variant introduced by an intermediate repair.
DEFAULT_MAX_CHARS = DEFAULT_MAX_PREVIEW_CHARS


def _safe_registry_id(value: str) -> bool:
    item_id = value.strip()
    if not item_id:
        return False
    if "/" in item_id or "\\" in item_id:
        return False
    if item_id in {".", ".."} or ".." in item_id:
        return False
    return True


def _read_json_object(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON file must contain object: {path}")
    return data


def _artifact_records(registry: dict[str, Any]) -> list[dict[str, Any]]:
    raw_records = registry.get("artifacts", registry.get("records", {}))
    if isinstance(raw_records, dict):
        records = raw_records.values()
    elif isinstance(raw_records, list):
        records = raw_records
    else:
        raise ValueError("artifact registry must contain an artifacts object or list")
    return [dict(record) for record in records if isinstance(record, dict)]


def _find_artifact(records: list[dict[str, Any]], artifact_id: str) -> dict[str, Any] | None:
    for record in records:
        if str(record.get("artifact_id", "")) == artifact_id:
            return record
    return None


def _compact_redacted_preview(redacted_text: str, max_chars: int) -> str:
    """Fit redacted text into max_chars while keeping a redaction marker visible.

    Some replacements are longer than the matched secret. A naive final slice can
    turn ``API_TOKEN=[REDACTED:ENV_SECRET]`` into ``API_TOKEN=[REDACT``. For a
    bounded preview, prefer the complete marker when it fits, otherwise a marker
    prefix that still contains ``[REDACTED``.
    """

    if len(redacted_text) <= max_chars:
        return redacted_text

    marker_start = redacted_text.find("[REDACTED")
    if marker_start >= 0:
        marker_end = redacted_text.find("]", marker_start)
        marker = (
            redacted_text[marker_start : marker_end + 1]
            if marker_end >= marker_start
            else redacted_text[marker_start:]
        )
        if len(marker) <= max_chars:
            return marker
        return marker[:max_chars]

    return redacted_text[:max_chars]


@dataclass(frozen=True)
class ArtifactPreviewResult:
    """A safe, redacted preview result for one artifact."""

    artifact_id: str
    exists: bool
    artifact: dict[str, Any] | None
    content_status: str
    content: str | None
    redacted: bool
    redaction_count: int
    redaction_findings: tuple[dict[str, int | str], ...]
    truncated: bool
    original_content_length: int | None
    preview_length: int | None

    def to_dict(self) -> dict[str, Any]:
        findings = list(self.redaction_findings)
        return {
            "artifact_id": self.artifact_id,
            "exists": self.exists,
            "artifact": self.artifact,
            "content_status": self.content_status,
            "content": self.content,
            "redacted": self.redacted,
            "redaction_count": self.redaction_count,
            "redaction_findings": findings,
            "redactions": findings,
            "truncated": self.truncated,
            "original_content_length": self.original_content_length,
            "preview_length": self.preview_length,
        }


class ArtifactPreviewer:
    """Load and redact one artifact preview from a SelfDev workspace."""

    def __init__(
        self,
        workspace: Path | str = DEFAULT_WORKSPACE,
        redaction_service: RedactionService | None = None,
    ) -> None:
        self.workspace = Path(workspace)
        self.redaction_service = redaction_service or RedactionService()

    def preview(self, artifact_id: str, max_chars: int = DEFAULT_MAX_PREVIEW_CHARS) -> ArtifactPreviewResult:
        if not _safe_registry_id(artifact_id):
            raise ValueError("artifact_id must be a single registry id segment")
        if max_chars < 1:
            raise ValueError("max_chars must be greater than zero")

        registry = _read_json_object(
            self.workspace / "artifacts" / "index.json",
            default={"artifacts": {}},
        )
        record = _find_artifact(_artifact_records(registry), artifact_id)
        if record is None:
            return self._empty_result(
                artifact_id=artifact_id,
                exists=False,
                artifact=None,
                content_status="missing_registry_record",
            )

        content, content_status = self._load_workspace_text(record.get("path"))
        if content is None:
            return self._empty_result(
                artifact_id=artifact_id,
                exists=True,
                artifact=record,
                content_status=content_status,
            )

        original_length = len(content)
        raw_truncated = original_length > max_chars
        preview_content = content[:max_chars]
        redaction_result = self.redaction_service.redact_text(preview_content)
        redacted_preview = _compact_redacted_preview(redaction_result.redacted_text, max_chars)
        final_truncated = raw_truncated or len(redaction_result.redacted_text) > max_chars

        return ArtifactPreviewResult(
            artifact_id=artifact_id,
            exists=True,
            artifact=record,
            content_status="loaded_truncated" if final_truncated else "loaded",
            content=redacted_preview,
            redacted=redaction_result.redacted,
            redaction_count=redaction_result.redaction_count,
            redaction_findings=tuple(finding.to_dict() for finding in redaction_result.findings),
            truncated=final_truncated,
            original_content_length=original_length,
            preview_length=len(redacted_preview),
        )

    def _load_workspace_text(self, path_value: Any) -> tuple[str | None, str]:
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

    @staticmethod
    def _empty_result(
        artifact_id: str,
        exists: bool,
        artifact: dict[str, Any] | None,
        content_status: str,
    ) -> ArtifactPreviewResult:
        return ArtifactPreviewResult(
            artifact_id=artifact_id,
            exists=exists,
            artifact=artifact,
            content_status=content_status,
            content=None,
            redacted=False,
            redaction_count=0,
            redaction_findings=(),
            truncated=False,
            original_content_length=None,
            preview_length=None,
        )


def preview_artifact(
    artifact_id: str,
    workspace: Path | str = DEFAULT_WORKSPACE,
    max_chars: int = DEFAULT_MAX_PREVIEW_CHARS,
) -> ArtifactPreviewResult:
    """Convenience wrapper for previewing one artifact."""

    return ArtifactPreviewer(workspace=workspace).preview(
        artifact_id=artifact_id,
        max_chars=max_chars,
    )
