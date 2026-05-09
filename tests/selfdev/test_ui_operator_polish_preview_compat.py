from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_polished_ui_keeps_legacy_artifact_preview_markers():
    html = read_ui_file("index.html")

    for marker in [
        "Redacted artifact preview",
        "artifact-id-input",
        "artifact-preview-button",
        "artifact-preview-content",
        "Preview content is bounded",
    ]:
        assert marker in html


def test_polished_ui_keeps_legacy_artifact_preview_endpoint_template():
    app = read_ui_file("app.js")

    assert "/artifact-previews/{artifact_id}" in app
    assert "/artifact-previews/" in app
    assert "loadArtifactPreview" in app
    assert "renderArtifacts" in app
    assert 'method: "GET"' in app
    assert 'method: "POST"' not in app
    assert 'method: "PUT"' not in app
    assert 'method: "PATCH"' not in app
    assert 'method: "DELETE"' not in app


def test_polished_ui_keeps_legacy_artifact_preview_style_selectors():
    css = read_ui_file("styles.css")

    for selector in [
        ".artifact-preview-panel",
        ".artifact-preview-content",
        ".artifact-preview-meta",
        ".inline-status",
    ]:
        assert selector in css
