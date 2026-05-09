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


ARTIFACT_ID = "task-artifact.opung.draft_patch"


def write_artifact_fixture(workspace: Path) -> None:
    artifact_path = workspace / "artifacts" / "task-artifact" / "draft.patch"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text("diff --git a/example.py b/example.py\n", encoding="utf-8")

    index_path = workspace / "artifacts" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(
            {
                "artifacts": {
                    ARTIFACT_ID: {
                        "artifact_id": ARTIFACT_ID,
                        "task_id": "task-artifact",
                        "agent_id": "opung",
                        "artifact_type": "draft_patch",
                        "path": "artifacts/task-artifact/draft.patch",
                        "status": "collected",
                        "metadata": {"source": "test"},
                    }
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def write_unsafe_artifact_fixture(workspace: Path) -> None:
    index_path = workspace / "artifacts" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(
            {
                "artifacts": {
                    "task-artifact.opung.unsafe": {
                        "artifact_id": "task-artifact.opung.unsafe",
                        "task_id": "task-artifact",
                        "agent_id": "opung",
                        "artifact_type": "draft_patch",
                        "path": "../outside.patch",
                        "status": "collected",
                        "metadata": {},
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


def test_read_api_artifact_loads_registered_text_content(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)

    payload = ReadApi(workspace=workspace).artifact(ARTIFACT_ID)

    assert payload["artifact_id"] == ARTIFACT_ID
    assert payload["exists"] is True
    assert payload["artifact"]["artifact_type"] == "draft_patch"
    assert payload["content_status"] == "loaded"
    assert "diff --git" in payload["content"]


def test_read_api_artifact_reports_missing_registry_record(tmp_path: Path):
    payload = ReadApi(workspace=tmp_path / "workspace").artifact("missing.artifact")

    assert payload["exists"] is False
    assert payload["artifact"] is None
    assert payload["content_status"] == "missing_registry_record"
    assert payload["content"] is None


def test_read_api_artifact_does_not_read_outside_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_unsafe_artifact_fixture(workspace)

    payload = ReadApi(workspace=workspace).artifact("task-artifact.opung.unsafe")

    assert payload["exists"] is True
    assert payload["content_status"] == "unsafe_path"
    assert payload["content"] is None


def test_http_artifact_endpoint_loads_registered_artifact(tmp_path: Path):
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)
    server, base_url = start_test_server(workspace)

    try:
        payload = get_json(f"{base_url}/artifacts/{ARTIFACT_ID}")
        assert payload["exists"] is True
        assert payload["content_status"] == "loaded"
        assert "diff --git" in payload["content"]
    finally:
        server.shutdown()
        server.server_close()


def test_http_artifact_endpoint_rejects_path_segments(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")

    try:
        try:
            urllib.request.urlopen(f"{base_url}/artifacts/bad/segment", timeout=5)
            raise AssertionError("Expected HTTP 400")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "invalid_artifact_id"
    finally:
        server.shutdown()
        server.server_close()


def test_read_api_cli_artifact(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    workspace = tmp_path / "workspace"
    write_artifact_fixture(workspace)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "artifact",
            "--workspace",
            str(workspace),
            "--artifact-id",
            ARTIFACT_ID,
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["exists"] is True
    assert payload["content_status"] == "loaded"


def test_read_api_cli_artifact_requires_artifact_id(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "artifact",
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
