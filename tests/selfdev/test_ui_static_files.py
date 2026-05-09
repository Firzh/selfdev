from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    path = UI_DIR / name
    assert path.exists(), f"Missing UI file: {path}"
    return path.read_text(encoding="utf-8")


def test_ui_static_console_files_exist():
    assert (UI_DIR / "index.html").exists()
    assert (UI_DIR / "app.js").exists()
    assert (UI_DIR / "styles.css").exists()


def test_index_declares_read_only_operator_console():
    html = read_ui_file("index.html")

    assert "SelfDev Operator Console" in html
    assert "READ ONLY" in html
    assert "Failure-first boundary" in html
    assert "app.js" in html
    assert "styles.css" in html


def test_app_uses_only_existing_read_only_api_endpoints():
    app = read_ui_file("app.js")

    for endpoint in [
        "/health",
        "/summary",
        "/kanban",
        "/actions/{task_id}",
        "/actions/",
    ]:
        assert endpoint in app

    assert 'method: "GET"' in app
    assert 'method: "POST"' not in app
    assert 'method: "PUT"' not in app
    assert 'method: "PATCH"' not in app
    assert 'method: "DELETE"' not in app


def test_app_makes_safety_boundary_visible():
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


def test_static_console_has_no_dangerous_frontend_action_terms():
    app = read_ui_file("app.js")
    html = read_ui_file("index.html")
    combined = f"{app}\n{html}".lower()

    forbidden_snippets = [
        "child_process",
        "exec(",
        "spawn(",
        "applypatch",
        "apply_patch(",
        "git commit",
        "git push",
        "git merge",
        "terraform apply",
        "kubectl apply",
    ]

    for snippet in forbidden_snippets:
        assert snippet not in combined


def test_css_contains_operator_console_layout_classes():
    css = read_ui_file("styles.css")

    for selector in [
        ".topbar",
        ".layout",
        ".panel",
        ".status-card",
        ".task-card",
        ".action-card",
        ".mode-badge",
    ]:
        assert selector in css
