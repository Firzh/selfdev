from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_polished_ui_uses_absolute_ui_assets_and_viewport():
    html = read_ui_file("index.html")

    assert '<meta name="viewport"' in html
    assert 'href="/ui/styles.css"' in html
    assert 'src="/ui/app.js"' in html
    assert 'SelfDev Operator Console' in html
    assert 'READ ONLY' in html
    assert 'Failure-first boundary' in html


def test_polished_ui_has_operator_usability_regions():
    html = read_ui_file("index.html")

    for marker in [
        "selfdev-shell",
        "topbar-actions",
        "safetyBoundary",
        "targetList",
        "kanbanList",
        "artifactList",
        "Redacted artifact preview",
        "previewContent",
    ]:
        assert marker in html


def test_polished_ui_keeps_read_only_fetch_contract():
    app = read_ui_file("app.js")

    for endpoint in [
        "/health",
        "/summary",
        "/targets",
        "/kanban",
        "/artifacts",
        "/actions/{task_id}",
        "/actions/",
        "/artifact-previews/",
    ]:
        assert endpoint in app

    assert 'method: "GET"' in app
    assert 'method: "POST"' not in app
    assert 'method: "PUT"' not in app
    assert 'method: "PATCH"' not in app
    assert 'method: "DELETE"' not in app


def test_polished_ui_styles_are_not_browser_default():
    css = read_ui_file("styles.css")

    for selector in [
        ".selfdev-shell",
        ".topbar",
        ".layout",
        ".panel",
        ".status-card",
        ".task-card",
        ".action-card",
        ".mode-badge",
        ".boundary-grid",
        ".preview-panel",
    ]:
        assert selector in css

    assert "radial-gradient" in css
    assert "grid-template-columns" in css
    assert "border-radius" in css


def test_polished_ui_safety_boundary_terms_remain_visible():
    app = read_ui_file("app.js")

    for boundary in [
        "No mutation",
        "No shell execution",
        "No patch apply",
        "No commit",
        "No push",
        "No merge",
        "No deploy",
        "No release",
        "No .env modification",
        "No secret read",
    ]:
        assert boundary in app
