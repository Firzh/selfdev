"""Minimal local HTTP API skeleton for SelfDev.

This server is read-only.
It uses Python standard library only.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, unquote

from selfdev.api.read_api import ReadApi


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def create_handler(
    workspace: Path | str = "data/agent_workspace",
    config_dir: Path | str = "config/selfdev",
) -> type[BaseHTTPRequestHandler]:
    workspace_path = Path(workspace)
    config_path = Path(config_dir)

    class SelfDevReadOnlyHandler(BaseHTTPRequestHandler):
        server_version = "SelfDevReadOnlyHTTP/0.1"

        def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
            body = _json_bytes(payload)
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _api(self) -> ReadApi:
            return ReadApi(workspace=workspace_path, config_dir=config_path)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            api = self._api()

            try:
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
                    task_id = unquote(path.removeprefix("/state/")).strip()
                    if not task_id or "/" in task_id or "\\" in task_id:
                        self._send_json(400, {
                            "error": "invalid_task_id",
                            "message": "task_id must be a single path segment",
                        })
                        return

                    self._send_json(200, api.state(task_id))
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
) -> ThreadingHTTPServer:
    handler = create_handler(workspace=workspace, config_dir=config_dir)
    return ThreadingHTTPServer((host, port), handler)
