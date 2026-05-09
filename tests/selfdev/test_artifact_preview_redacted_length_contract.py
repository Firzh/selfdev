from __future__ import annotations

import json
from pathlib import Path

from selfdev.runtime.artifact_preview import preview_artifact


ARTIFACT_ID = "task-demo.opung.draft_patch"


def test_redacted_preview_never_exceeds_max_chars_after_redaction(tmp_path: Path):
    workspace = tmp_path / "workspace"
    artifact_dir = workspace / "artifacts"
    artifact_dir.mkdir(parents=True)
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

    result = preview_artifact(ARTIFACT_ID, workspace=workspace, max_chars=18)

    assert result.exists is True
    assert result.content_status == "loaded_truncated"
    assert result.truncated is True
    assert result.preview_length == len(result.content or "")
    assert result.preview_length <= 18
    assert "super-secret-value" not in (result.content or "")
