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


DEFAULT_UI_DIR = Path(__file__).resolve().parents[1] / "ui" / "web"
STATIC_CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def _safe_task_id(raw_task_id: str) -> str | None:
    task_id = unquote(raw_task_id).strip()
    if not task_id:
        return None
    if "/" in task_id or "\\" in task_id:
        return None
    if task_id in {".", ".."}:
        return None
    return task_id


def _content_type_for(path: Path) -> str:
    return STATIC_CONTENT_TYPES.get(path.suffix.lower(), "application/octet-stream")


def _resolve_ui_file(path: str, ui_dir: Path) -> tuple[int | None, Path | None]:
    """Resolve a /ui request to a local static file.

    Returns:
        (None, None) when the path is not a UI route.
        (200, file_path) when a safe file exists.
        (400, None) when the path is unsafe.
        (404, None) when the path is safe but not found.
    """

    if path == "/ui":
        raw_relative_path = "index.html"
    elif path.startswith("/ui/"):
        raw_relative_path = path.removeprefix("/ui/") or "index.html"
    else:
        return None, None

    relative_path = unquote(raw_relative_path).strip()
    if not relative_path or relative_path == ".":
        relative_path = "index.html"

    if "\x00" in relative_path or "\\" in relative_path:
        return 400, None

    base_dir = ui_dir.resolve()
    candidate = (base_dir / relative_path).resolve()

    try:
        candidate.relative_to(base_dir)
    except ValueError:
        return 400, None

    if not candidate.is_file():
        return 404, None

    return 200, candidate


def create_handler(
    workspace: Path | str = "data/agent_workspace",
    config_dir: Path | str = "config/selfdev",
    ui_dir: Path | str = DEFAULT_UI_DIR,
) -> type[BaseHTTPRequestHandler]:
    workspace_path = Path(workspace)
    config_path = Path(config_dir)
    ui_path = Path(ui_dir)

    class SelfDevReadOnlyHandler(BaseHTTPRequestHandler):
        server_version = "SelfDevReadOnlyHTTP/0.2"

        def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
            body = _json_bytes(payload)
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_static_file(self, path: Path) -> None:
            body = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", _content_type_for(path))
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _api(self) -> ReadApi:
            return ReadApi(workspace=workspace_path, config_dir=config_path)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            api = self._api()

            try:
                ui_status, ui_file = _resolve_ui_file(path, ui_path)
                if ui_status is not None:
                    if ui_status == 200 and ui_file is not None:
                        self._send_static_file(ui_file)
                        return
                    if ui_status == 400:
                        self._send_json(
                            400,
                            {
                                "error": "invalid_static_path",
                                "message": "UI static paths must stay inside the configured UI directory.",
                            },
                        )
                        return
                    self._send_json(
                        404,
                        {
                            "error": "not_found",
                            "path": path,
                        },
                    )
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

                if path == "/artifacts":
                    self._send_json(200, api.artifacts())
                    return

                if path.startswith("/state/"):
                    task_id = _safe_task_id(path.removeprefix("/state/"))
                    if task_id is None:
                        self._send_json(
                            400,
                            {
                                "error": "invalid_task_id",
                                "message": "task_id must be a single path segment",
                            },
                        )
                        return
                    self._send_json(200, api.state(task_id))
                    return

                if path.startswith("/actions/"):
                    task_id = _safe_task_id(path.removeprefix("/actions/"))
                    if task_id is None:
                        self._send_json(
                            400,
                            {
                                "error": "invalid_task_id",
                                "message": "task_id must be a single path segment",
                            },
                        )
                        return
                    result = get_action_availability(
                        task_id=task_id,
                        workspace=workspace_path,
                    )
                    self._send_json(200, result.to_dict())
                    return

                self._send_json(
                    404,
                    {
                        "error": "not_found",
                        "path": path,
                    },
                )
                return
            except Exception as exc:
                self._send_json(
                    500,
                    {
                        "error": "internal_error",
                        "message": str(exc),
                    },
                )

        def do_POST(self) -> None:
            self._send_json(
                405,
                {
                    "error": "method_not_allowed",
                    "message": "This API skeleton is read-only.",
                },
            )

        def do_PUT(self) -> None:
            self._send_json(
                405,
                {
                    "error": "method_not_allowed",
                    "message": "This API skeleton is read-only.",
                },
            )

        def do_DELETE(self) -> None:
            self._send_json(
                405,
                {
                    "error": "method_not_allowed",
                    "message": "This API skeleton is read-only.",
                },
            )

        def log_message(self, format: str, *args: Any) -> None:
            return

    return SelfDevReadOnlyHandler


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    workspace: Path | str = "data/agent_workspace",
    config_dir: Path | str = "config/selfdev",
    ui_dir: Path | str = DEFAULT_UI_DIR,
) -> ThreadingHTTPServer:
    handler = create_handler(workspace=workspace, config_dir=config_dir, ui_dir=ui_dir)
    return ThreadingHTTPServer((host, port), handler)
