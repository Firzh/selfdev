from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX_HTML = ROOT / "selfdev" / "ui" / "web" / "index.html"
APP_JS = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_failure_first_boundary_marker_is_restored():
    html = INDEX_HTML.read_text(encoding="utf-8")

    assert "SelfDev Operator Console" in html
    assert "READ ONLY" in html
    assert "Failure-first boundary" in html


def test_failure_first_boundary_restore_does_not_touch_app_forbidden_terms():
    app = APP_JS.read_text(encoding="utf-8")

    for forbidden in [
        'method: "POST"',
        'method: "PUT"',
        'method: "DELETE"',
        "applyPatch",
        "commit",
        "shell",
    ]:
        assert forbidden not in app
