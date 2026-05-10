from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_JS = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_app_uses_unified_read_only_boundary_terms():
    app = APP_JS.read_text(encoding="utf-8")

    for marker in [
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
        assert marker in app

    for forbidden in [
        'method: "POST"',
        'method: "PUT"',
        'method: "DELETE"',
        "applyPatch",
        "commit",
        "shell",
    ]:
        assert forbidden not in app


def test_app_preserves_render_artifact_preview_result_contract():
    app = APP_JS.read_text(encoding="utf-8")

    assert "function renderArtifactPreview" in app
    assert "renderArtifactPreview(result.payload || {}, artifactId, result.ok)" in app
