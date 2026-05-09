from __future__ import annotations

import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

from selfdev.api.http_server import create_server
from selfdev.api.read_api import ReadApi


ARTIFACT_ID = "task-demo.opung.draft_patch"


def write_artifact_fixture(workspace: Path, content: str) -> None:
    artifact_path = workspace / "artifacts" / "task-demo" / "draft.patch"
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
                        "path": "artifacts/task-demo/draft.patch",
                        "status": "collected",
                        "metadata": {"source": "test"},
                    }
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def start_test_server(workspace: Path):
    server = create_server(
        host="127.0.0.1",
        port=0,
        workspace=workspace,
        config_dir=Path("config/selfdev"),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.status == 200
        return json.loads(response.read().decode("utf-8"))


def test_read_api_artifact_preview_returns_redacted_bounded_content(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace, "prefix API_TOKEN=super-secret-value suffix")

    payload = ReadApi(workspace=workspace).artifact_preview(ARTIFACT_ID, max_chars=24)

    assert payload["artifact_id"] == ARTIFACT_ID
    assert payload["exists"] is True
    assert payload["content_status"] == "loaded_truncated"
    assert payload["redacted"] is True
    assert payload["preview_length"] <= 24
    assert "super-secret-value" not in (payload["content"] or "")
    assert "[REDACTED" in (payload["content"] or "")


def test_read_api_artifact_preview_reports_missing_record(tmp_path: Path):
    payload = ReadApi(workspace=tmp_path / "workspace").artifact_preview("missing.artifact")

    assert payload["artifact_id"] == "missing.artifact"
    assert payload["exists"] is False
    assert payload["content_status"] == "missing_registry_record"
    assert payload["content"] is None


def test_http_artifact_preview_endpoint_returns_redacted_preview(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace, "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456")
    server, base_url = start_test_server(workspace)

    try:
        payload = get_json(f"{base_url}/artifact-previews/{ARTIFACT_ID}")
        assert payload["exists"] is True
        assert payload["redacted"] is True
        assert "abcdefghijklmnopqrstuvwxyz123456" not in (payload["content"] or "")
        assert "[REDACTED:BEARER_TOKEN]" in (payload["content"] or "")
    finally:
        server.shutdown()
        server.server_close()


def test_http_artifact_preview_endpoint_rejects_path_segments(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")

    try:
        try:
            urllib.request.urlopen(f"{base_url}/artifact-previews/bad/segment", timeout=5)
            raise AssertionError("Expected HTTP 400")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "invalid_artifact_id"
    finally:
        server.shutdown()
        server.server_close()


def test_read_api_cli_artifact_preview(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace, "API_TOKEN=super-secret-value")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "artifact-preview",
            "--workspace",
            str(workspace),
            "--artifact-id",
            ARTIFACT_ID,
            "--max-chars",
            "80",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["exists"] is True
    assert payload["redacted"] is True
    assert "super-secret-value" not in (payload["content"] or "")


def test_read_api_cli_artifact_preview_requires_artifact_id(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "artifact-preview",
            "--workspace",
            str(tmp_path / "workspace"),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--artifact-id is required" in result.stderr
