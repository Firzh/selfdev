from __future__ import annotations

import json
from pathlib import Path

from selfdev.runtime.artifact_preview import preview_artifact


ARTIFACT_ID = "task-demo.opung.draft_patch"


def write_artifact_fixture(workspace: Path, content: str) -> None:
    artifact_dir = workspace / "artifacts"
    artifact_dir.mkdir(parents=True)
    artifact_file = artifact_dir / "demo.patch"
    artifact_file.write_text(content, encoding="utf-8")
    (artifact_dir / "index.json").write_text(
        json.dumps(
            {
                "artifacts": [
                    {
                        "artifact_id": ARTIFACT_ID,
                        "task_id": "task-demo",
                        "agent_id": "opung",
                        "artifact_type": "draft_patch",
                        "path": "artifacts/demo.patch",
                        "status": "ready",
                        "metadata": {},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_redacted_preview_keeps_marker_visible_within_max_chars(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace, "prefix API_TOKEN=super-secret-value suffix")

    result = preview_artifact(ARTIFACT_ID, workspace=workspace, max_chars=24)

    assert result.content_status == "loaded_truncated"
    assert result.redacted is True
    assert result.preview_length <= 24
    assert len(result.content or "") <= 24
    assert "[REDACTED" in (result.content or "")
    assert "super-secret-value" not in (result.content or "")
