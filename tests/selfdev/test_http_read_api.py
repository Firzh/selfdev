from __future__ import annotations

import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

from selfdev.api.http_server import create_server
from selfdev.runtime.kanban import KanbanBoard
from selfdev.runtime.state_manager import StateManager


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
    base_url = f"http://{host}:{port}"
    return server, base_url


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.status == 200
        return json.loads(response.read().decode("utf-8"))


def test_http_health_endpoint(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")
    try:
        payload = get_json(f"{base_url}/health")
        assert payload["service"] == "selfdev-read-api"
        assert payload["mode"] == "read_only"
        assert payload["config"]["agents.yaml"] is True
    finally:
        server.shutdown()
        server.server_close()


def test_http_agents_endpoint(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")
    try:
        payload = get_json(f"{base_url}/agents")
        assert "agents" in payload
        assert "siwa" in payload["agents"]
        assert "senior_reviewer" in payload["agents"]
    finally:
        server.shutdown()
        server.server_close()


def test_http_kanban_endpoint_reads_workspace(tmp_path: Path):
    workspace = tmp_path / "workspace"
    board = KanbanBoard(workspace)
    board.create_task({
        "task_id": "task-http-001",
        "title": "HTTP read test",
        "status": "todo",
        "priority": "medium",
        "risk_level": "low",
        "target_id": "selfdev",
        "owner_agent": "siwa",
        "assigned_by": "human_owner",
        "task_type": "documentation",
        "artifacts": {},
        "blocked_by": [],
    })

    server, base_url = start_test_server(workspace)
    try:
        payload = get_json(f"{base_url}/kanban")
        assert "task-http-001" in payload["tasks"]
        assert payload["tasks"]["task-http-001"]["status"] == "todo"
    finally:
        server.shutdown()
        server.server_close()


def test_http_state_endpoint_reads_task_state(tmp_path: Path):
    workspace = tmp_path / "workspace"
    manager = StateManager(workspace)
    manager.write_state("task-http-state", {
        "task_id": "task-http-state",
        "status": "verified",
    })

    server, base_url = start_test_server(workspace)
    try:
        payload = get_json(f"{base_url}/state/task-http-state")
        assert payload["exists"] is True
        assert payload["state"]["status"] == "verified"
    finally:
        server.shutdown()
        server.server_close()


def test_http_unknown_route_returns_404(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")
    try:
        try:
            urllib.request.urlopen(f"{base_url}/missing", timeout=5)
            raise AssertionError("Expected HTTP 404")
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "not_found"
    finally:
        server.shutdown()
        server.server_close()


def test_http_rejects_post_request(tmp_path: Path):
    server, base_url = start_test_server(tmp_path / "workspace")
    try:
        request = urllib.request.Request(
            f"{base_url}/health",
            data=b"{}",
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        try:
            urllib.request.urlopen(request, timeout=5)
            raise AssertionError("Expected HTTP 405")
        except urllib.error.HTTPError as exc:
            assert exc.code == 405
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "method_not_allowed"
    finally:
        server.shutdown()
        server.server_close()


def test_serve_read_api_cli_check():
    root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/serve_read_api.py",
            "--check",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["service"] == "selfdev-read-api"
    assert payload["mode"] == "read_only"
