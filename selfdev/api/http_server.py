"""Minimal local HTTP API skeleton for SelfDev.

This server is read-only. It uses Python standard library only.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from selfdev.api.action_availability import get_action_availability
from selfdev.api.read_api import ReadApi


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def _safe_segment(raw_value: str) -> str | None:
    value = unquote(raw_value).strip()
    if not value:
        return None
    if "/" in value or "\\" in value:
        return None
    if value in {".", ".."}:
        return None
    return value


def _safe_static_path(raw_value: str) -> Path | None:
    value = unquote(raw_value).lstrip("/")
    if value in {"", "."}:
        value = "index.html"

    path = Path(value)
    if path.is_absolute():
        return None
    if any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path


def _content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "text/html; charset=utf-8"
    if suffix == ".css":
        return "text/css; charset=utf-8"
    if suffix == ".js":
        content_type = "application/javascript"
        return f"{content_type}; charset=utf-8"
    if suffix == ".json":
        return "application/json; charset=utf-8"
    if suffix == ".svg":
        return "image/svg+xml"
    return "application/octet-stream"


def create_handler(
    workspace: Path | str = "data/agent_workspace",
    config_dir: Path | str = "config/selfdev",
    ui_dir: Path | str | None = None,
) -> type[BaseHTTPRequestHandler]:
    workspace_path = Path(workspace)
    config_path = Path(config_dir)
    ui_path = Path(ui_dir) if ui_dir is not None else Path("selfdev/ui/web")

    class SelfDevReadOnlyHandler(BaseHTTPRequestHandler):
        server_version = "SelfDevReadOnlyHTTP/0.1"

        def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
            body = _json_bytes(payload)
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_bytes(self, status_code: int, body: bytes, content_type: str) -> None:
            self.send_response(status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _api(self) -> ReadApi:
            return ReadApi(workspace=workspace_path, config_dir=config_path)

        def _serve_ui(self, raw_path: str) -> None:
            static_path = _safe_static_path(raw_path)
            if static_path is None:
                self._send_json(400, {
                    "error": "invalid_static_path",
                    "message": "static path must stay inside the UI directory",
                })
                return

            candidate = (ui_path / static_path).resolve()
            root = ui_path.resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                self._send_json(400, {
                    "error": "invalid_static_path",
                    "message": "static path must stay inside the UI directory",
                })
                return

            if not candidate.exists() or not candidate.is_file():
                self._send_json(404, {
                    "error": "not_found",
                    "path": f"/ui/{static_path.as_posix()}",
                })
                return

            self._send_bytes(
                200,
                candidate.read_bytes(),
                _content_type(candidate),
            )

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            api = self._api()

            try:
                if path == "/ui":
                    self._serve_ui("index.html")
                    return

                if path.startswith("/ui/"):
                    self._serve_ui(path.removeprefix("/ui/"))
                    return

                if path == "/health":
                    self._send_json(200, api.health())
                    return

                if path == "/summary":
                    self._send_json(200, api.summary())
                    return

                if path == "/agents":
                    self._send_json(200, api.agents())
                    return

                if path == "/tools":
                    self._send_json(200, api.tools())
                    return

                if path == "/kanban":
                    self._send_json(200, api.kanban())
                    return

                if path == "/targets":
                    self._send_json(200, api.targets())
                    return

                if path.startswith("/targets/"):
                    target_id = _safe_segment(path.removeprefix("/targets/"))
                    if target_id is None:
                        self._send_json(400, {
                            "error": "invalid_target_id",
                            "message": "target_id must be a single path segment",
                        })
                        return
                    self._send_json(200, api.target(target_id))
                    return

                if path.startswith("/artifact-previews/"):
                    artifact_id = _safe_segment(path.removeprefix("/artifact-previews/"))
                    if artifact_id is None:
                        self._send_json(400, {
                            "error": "invalid_artifact_id",
                            "message": "artifact_id must be a single path segment",
                        })
                        return
                    self._send_json(200, api.artifact_preview(artifact_id))
                    return

                if path == "/artifacts":
                    self._send_json(200, api.artifacts())
                    return

                if path.startswith("/artifacts/"):
                    artifact_id = _safe_segment(path.removeprefix("/artifacts/"))
                    if artifact_id is None:
                        self._send_json(400, {
                            "error": "invalid_artifact_id",
                            "message": "artifact_id must be a single path segment",
                        })
                        return
                    self._send_json(200, api.artifact(artifact_id))
                    return

                if path.startswith("/state/"):
                    task_id = _safe_segment(path.removeprefix("/state/"))
                    if task_id is None:
                        self._send_json(400, {
                            "error": "invalid_task_id",
                            "message": "task_id must be a single path segment",
                        })
                        return
                    self._send_json(200, api.state(task_id))
                    return

                if path.startswith("/actions/"):
                    task_id = _safe_segment(path.removeprefix("/actions/"))
                    if task_id is None:
                        self._send_json(400, {
                            "error": "invalid_task_id",
                            "message": "task_id must be a single path segment",
                        })
                        return

                    result = get_action_availability(
                        task_id=task_id,
                        workspace=workspace_path,
                    )
                    self._send_json(200, result.to_dict())
                    return

                self._send_json(404, {
                    "error": "not_found",
                    "path": path,
                })
                return
            except Exception as exc:
                self._send_json(500, {
                    "error": "internal_error",
                    "message": str(exc),
                })

        def do_POST(self) -> None:
            self._send_json(405, {
                "error": "method_not_allowed",
                "message": "This API skeleton is read-only.",
            })

        def do_PUT(self) -> None:
            self._send_json(405, {
                "error": "method_not_allowed",
                "message": "This API skeleton is read-only.",
            })

        def do_DELETE(self) -> None:
            self._send_json(405, {
                "error": "method_not_allowed",
                "message": "This API skeleton is read-only.",
            })

        def log_message(self, format: str, *args: Any) -> None:
            return

    return SelfDevReadOnlyHandler


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    workspace: Path | str = "data/agent_workspace",
    config_dir: Path | str = "config/selfdev",
    ui_dir: Path | str | None = None,
) -> ThreadingHTTPServer:
    handler = create_handler(
        workspace=workspace,
        config_dir=config_dir,
        ui_dir=ui_dir,
    )
    return ThreadingHTTPServer((host, port), handler)
