from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    path = UI_DIR / name
    assert path.exists(), f"Missing UI file: {path}"
    return path.read_text(encoding="utf-8")


def test_static_ui_declares_redacted_artifact_preview_panel():
    html = read_ui_file("index.html")

    assert "Redacted artifact preview" in html
    assert "artifact-id-input" in html
    assert "artifact-preview-button" in html
    assert "artifact-preview-content" in html
    assert "Preview content is bounded" in html


def test_static_ui_calls_artifact_preview_read_endpoint_only_with_get():
    app = read_ui_file("app.js")

    assert "/artifact-previews/{artifact_id}" in app
    assert "/artifact-previews/" in app
    assert "loadArtifactPreview" in app
    assert "renderArtifactPreview" in app
    assert 'method: "GET"' in app
    assert 'method: "POST"' not in app
    assert 'method: "PUT"' not in app
    assert 'method: "PATCH"' not in app
    assert 'method: "DELETE"' not in app


def test_static_ui_keeps_existing_read_only_console_contract():
    app = read_ui_file("app.js")
    html = read_ui_file("index.html")
    combined = f"{app}\n{html}"

    for endpoint in [
        "/health",
        "/summary",
        "/targets",
        "/kanban",
        "/actions/{task_id}",
        "/actions/",
        "/artifacts",
    ]:
        assert endpoint in app

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

    assert "SelfDev Operator Console" in html
    assert "READ ONLY" in html
    assert "Failure-first boundary" in html
    assert "app.js" in html
    assert "styles.css" in html

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
    lower_combined = combined.lower()
    for snippet in forbidden_snippets:
        assert snippet not in lower_combined


def test_static_ui_styles_artifact_preview_panel():
    css = read_ui_file("styles.css")

    for selector in [
        ".topbar",
        ".layout",
        ".panel",
        ".status-card",
        ".task-card",
        ".action-card",
        ".mode-badge",
        ".artifact-preview-panel",
        ".artifact-preview-content",
        ".artifact-preview-meta",
        ".inline-status",
    ]:
        assert selector in css
