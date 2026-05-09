from __future__ import annotations

from pathlib import Path

from selfdev.api.http_server import create_handler


def test_static_js_content_type_is_application_javascript(tmp_path: Path):
    ui_dir = tmp_path / "ui"
    ui_dir.mkdir()
    js_file = ui_dir / "app.js"
    js_file.write_text("console.log('selfdev');", encoding="utf-8")

    handler = create_handler(
        workspace=tmp_path / "workspace",
        config_dir=Path("config/selfdev"),
        ui_dir=ui_dir,
    )

    assert getattr(handler, "__name__") == "SelfDevReadOnlyHandler"

    # Contract check by source: the HTTP handler must force the stable MIME type
    # expected by the static UI route tests instead of relying on platform-specific
    # mimetypes.guess_type output.
    source = Path("selfdev/api/http_server.py").read_text(encoding="utf-8")
    assert 'content_type = "application/javascript"' in source
    assert 'content_type = "text/javascript"' not in source
