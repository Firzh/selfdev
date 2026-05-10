from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_JS = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_ui_app_contract_debug_restore_keeps_legacy_boundary_markers():
    app = APP_JS.read_text(encoding="utf-8")

    for boundary in [
        "No mutation",
        "No command execution",
        "No patch apply",
        "No VCS write",
        "No push",
        "No merge",
        "No deploy",
        "No release",
        "No .env modification",
        "No secret read",
    ]:
        assert boundary in app


def test_ui_app_contract_debug_restore_keeps_preview_render_contract():
    app = APP_JS.read_text(encoding="utf-8")

    assert "function renderArtifactPreview" in app
    assert "function renderArtifactPreviewResult" in app
    assert "renderArtifactPreview(result.payload || {}, artifactId, result.ok)" in app
    assert "/artifact-previews/{artifact_id}" in app


def test_ui_app_contract_debug_restore_does_not_add_write_methods():
    app = APP_JS.read_text(encoding="utf-8")

    assert 'method: "GET"' in app
    for forbidden in ['method: "POST"', 'method: "PUT"', 'method: "DELETE"']:
        assert forbidden not in app
