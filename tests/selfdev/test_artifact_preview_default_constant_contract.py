from __future__ import annotations

import json
from pathlib import Path

from selfdev.runtime.artifact_preview import DEFAULT_MAX_CHARS, DEFAULT_MAX_PREVIEW_CHARS, preview_artifact


ARTIFACT_ID = "task-demo.opung.draft_patch"


def write_artifact_fixture(workspace: Path) -> None:
    artifact_dir = workspace / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "draft.patch").write_text(
        "prefix API_TOKEN=super-secret-value suffix",
        encoding="utf-8",
    )
    (artifact_dir / "index.json").write_text(
        json.dumps(
            {
                "artifacts": {
                    ARTIFACT_ID: {
                        "artifact_id": ARTIFACT_ID,
                        "path": "artifacts/draft.patch",
                    }
                }
            }
        ),
        encoding="utf-8",
    )


def test_artifact_preview_exports_read_api_default_constant():
    assert DEFAULT_MAX_PREVIEW_CHARS == 12_000
    assert DEFAULT_MAX_CHARS == DEFAULT_MAX_PREVIEW_CHARS


def test_artifact_preview_keeps_redaction_marker_visible_with_bounded_content(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)

    result = preview_artifact(ARTIFACT_ID, workspace=workspace, max_chars=24)

    assert result.exists is True
    assert result.content_status == "loaded_truncated"
    assert result.preview_length <= 24
    assert len(result.content or "") <= 24
    assert "[REDACTED" in (result.content or "")
    assert "super-secret-value" not in (result.content or "")
