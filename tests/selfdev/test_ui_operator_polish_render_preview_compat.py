from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_JS = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_polished_ui_keeps_render_artifact_preview_helper_contract():
    app = APP_JS.read_text(encoding="utf-8")

    assert "function renderArtifactPreview" in app
    assert "renderArtifactPreview(result.payload || {}, artifactId, result.ok)" in app
    assert "loadArtifactPreview" in app
    assert "/artifact-previews/{artifact_id}" in app
    assert "/artifact-previews/" in app


def test_polished_ui_preview_helper_remains_read_only():
    app = APP_JS.read_text(encoding="utf-8")

    assert 'method: "GET"' in app
    assert 'method: "POST"' not in app
    assert 'method: "PUT"' not in app
    assert 'method: "PATCH"' not in app
    assert 'method: "DELETE"' not in app
