from __future__ import annotations

from pathlib import Path

from selfdev.api.http_server import create_handler, create_server


def test_create_handler_accepts_ui_dir_keyword(tmp_path: Path) -> None:
    ui_dir = tmp_path / "ui"
    ui_dir.mkdir()
    (ui_dir / "index.html").write_text("<html>ok</html>", encoding="utf-8")

    handler = create_handler(
        workspace=tmp_path / "workspace",
        config_dir=tmp_path / "config",
        ui_dir=ui_dir,
    )

    assert handler is not None


def test_create_server_accepts_ui_dir_keyword(tmp_path: Path) -> None:
    ui_dir = tmp_path / "ui"
    ui_dir.mkdir()
    (ui_dir / "index.html").write_text("<html>ok</html>", encoding="utf-8")

    server = create_server(
        host="127.0.0.1",
        port=0,
        workspace=tmp_path / "workspace",
        config_dir=tmp_path / "config",
        ui_dir=ui_dir,
    )
    try:
        assert server.server_address[0] == "127.0.0.1"
    finally:
        server.server_close()
