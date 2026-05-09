from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from selfdev.runtime.artifact_preview import ArtifactPreviewer, preview_artifact


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ID = "task-demo.opung.draft_patch"


def write_artifact_fixture(workspace: Path, content: str = "API_TOKEN=super-secret-value\npatch body") -> Path:
    artifact_path = workspace / "artifacts" / "draft.patch"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(content, encoding="utf-8")

    index_path = workspace / "artifacts" / "index.json"
    index_path.write_text(
        json.dumps(
            {
                "artifacts": {
                    ARTIFACT_ID: {
                        "artifact_id": ARTIFACT_ID,
                        "task_id": "task-demo",
                        "agent_id": "opung",
                        "artifact_type": "draft_patch",
                        "path": "artifacts/draft.patch",
                        "status": "ready",
                        "metadata": {},
                    }
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return artifact_path


def test_artifact_preview_redacts_loaded_text_content(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)

    result = preview_artifact(ARTIFACT_ID, workspace=workspace)

    assert result.exists is True
    assert result.content_status == "loaded"
    assert result.redacted is True
    assert result.redaction_count == 1
    assert "API_TOKEN=" in (result.content or "")
    assert "super-secret-value" not in (result.content or "")
    assert "[REDACTED:ENV_SECRET]" in (result.content or "")
    assert result.original_content_length is not None
    assert result.preview_length == len(result.content or "")


def test_artifact_preview_reports_missing_registry_record(tmp_path: Path):
    result = ArtifactPreviewer(workspace=tmp_path / "workspace").preview("missing-artifact")

    assert result.exists is False
    assert result.artifact is None
    assert result.content_status == "missing_registry_record"
    assert result.content is None
    assert result.redacted is False


def test_artifact_preview_rejects_unsafe_artifact_id(tmp_path: Path):
    with pytest.raises(ValueError, match="single registry id segment"):
        preview_artifact("bad/segment", workspace=tmp_path / "workspace")


def test_artifact_preview_rejects_invalid_max_chars(tmp_path: Path):
    with pytest.raises(ValueError, match="greater than zero"):
        preview_artifact("artifact", workspace=tmp_path / "workspace", max_chars=0)


def test_artifact_preview_blocks_path_escape(tmp_path: Path):
    workspace = tmp_path / "workspace"
    index_dir = workspace / "artifacts"
    index_dir.mkdir(parents=True, exist_ok=True)
    (tmp_path / "outside.txt").write_text("API_TOKEN=outside", encoding="utf-8")
    (index_dir / "index.json").write_text(
        json.dumps(
            {
                "artifacts": {
                    ARTIFACT_ID: {
                        "artifact_id": ARTIFACT_ID,
                        "path": "../outside.txt",
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    result = preview_artifact(ARTIFACT_ID, workspace=workspace)

    assert result.exists is True
    assert result.content_status == "unsafe_path"
    assert result.content is None
    assert result.redacted is False


def test_artifact_preview_truncates_before_redaction(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace, content="prefix API_TOKEN=super-secret-value suffix")

    result = preview_artifact(ARTIFACT_ID, workspace=workspace, max_chars=18)

    assert result.exists is True
    assert result.content_status == "loaded_truncated"
    assert result.truncated is True
    assert result.original_content_length == len("prefix API_TOKEN=super-secret-value suffix")
    assert len(result.content or "") <= 18


def test_artifact_preview_cli_outputs_json_without_raw_secret(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "selfdev" / "preview_artifact.py"),
            "--workspace",
            str(workspace),
            "--artifact-id",
            ARTIFACT_ID,
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["exists"] is True
    assert payload["content_status"] == "loaded"
    assert payload["redacted"] is True
    assert "super-secret-value" not in completed.stdout
    assert "[REDACTED:ENV_SECRET]" in payload["content"]
