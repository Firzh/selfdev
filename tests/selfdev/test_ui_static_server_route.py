from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

from selfdev.api.http_server import create_server


def start_test_server(workspace: Path, ui_dir: Path):
    server = create_server(
        host="127.0.0.1",
        port=0,
        workspace=workspace,
        config_dir=Path("config/selfdev"),
        ui_dir=ui_dir,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    return server, base_url


def get_text(url: str):
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        body = response.read().decode("utf-8")
    return content_type, body


def test_http_ui_root_serves_index_html(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    ui_dir = root / "selfdev" / "ui" / "web"
    server, base_url = start_test_server(tmp_path / "workspace", ui_dir)
    try:
        content_type, body = get_text(f"{base_url}/ui")
        assert content_type.startswith("text/html")
        assert "<html" in body.lower() or "<!doctype html" in body.lower()
    finally:
        server.shutdown()
        server.server_close()


def test_http_ui_index_path_matches_root(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    ui_dir = root / "selfdev" / "ui" / "web"
    server, base_url = start_test_server(tmp_path / "workspace", ui_dir)
    try:
        _, root_body = get_text(f"{base_url}/ui")
        _, index_body = get_text(f"{base_url}/ui/index.html")
        assert index_body == root_body
    finally:
        server.shutdown()
        server.server_close()


def test_http_ui_serves_javascript_and_css_assets(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    ui_dir = root / "selfdev" / "ui" / "web"
    server, base_url = start_test_server(tmp_path / "workspace", ui_dir)
    try:
        js_type, js_body = get_text(f"{base_url}/ui/app.js")
        css_type, css_body = get_text(f"{base_url}/ui/styles.css")
        assert js_type.startswith("application/javascript")
        assert css_type.startswith("text/css")
        assert js_body.strip()
        assert css_body.strip()
    finally:
        server.shutdown()
        server.server_close()


def test_http_ui_rejects_path_traversal(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    ui_dir = root / "selfdev" / "ui" / "web"
    server, base_url = start_test_server(tmp_path / "workspace", ui_dir)
    try:
        try:
            urllib.request.urlopen(f"{base_url}/ui/%2e%2e/README.md", timeout=5)
            raise AssertionError("Expected HTTP 400")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "invalid_static_path"
    finally:
        server.shutdown()
        server.server_close()


def test_http_ui_missing_asset_returns_404(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    ui_dir = root / "selfdev" / "ui" / "web"
    server, base_url = start_test_server(tmp_path / "workspace", ui_dir)
    try:
        try:
            urllib.request.urlopen(f"{base_url}/ui/missing.js", timeout=5)
            raise AssertionError("Expected HTTP 404")
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "not_found"
    finally:
        server.shutdown()
        server.server_close()
