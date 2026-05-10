from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_JS = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_static_ui_read_only_boundary_avoids_forbidden_capability_terms():
    app = APP_JS.read_text(encoding="utf-8")

    assert "No command execution" in app
    assert "No VCS write" in app
    assert "No mutation" in app
    for forbidden in ["shell", "commit", 'method: "POST"', 'method: "PUT"', 'method: "DELETE"']:
        assert forbidden not in app
