from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI / name).read_text(encoding="utf-8")


def test_static_ui_declares_target_detail_panel_contract():
    html = read_ui_file("index.html")

    for marker in [
        "target-detail-panel",
        "target-id-input",
        "target-detail-button",
        "target-detail-content",
        "targetList",
    ]:
        assert marker in html


def test_static_ui_wires_target_list_to_detail_endpoint():
    app = read_ui_file("app.js")

    for marker in [
        "/targets/{target_id}",
        "/targets/",
        "function renderTargetDetail",
        "loadTargetDetail",
        "renderTargets",
        "targetEntries",
        'method: "GET"',
    ]:
        assert marker in app


def test_static_ui_target_detail_remains_read_only():
    app = read_ui_file("app.js")

    assert "fetch(" in app
    for forbidden in [
        'method: "POST"',
        'method: "PUT"',
        'method: "DELETE"',
        "applyPatch",
        "commit",
        "shell",
    ]:
        assert forbidden not in app


def test_static_ui_keeps_existing_operator_markers():
    html = read_ui_file("index.html")
    css = read_ui_file("styles.css")
    app = read_ui_file("app.js")

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

    for marker in [
        ".selfdev-shell",
        ".topbar",
        ".layout",
        ".panel",
        ".boundary-grid",
        ".preview-panel",
        "radial-gradient",
        "box-shadow",
    ]:
        assert marker in css

    for marker in [
        "No command execution",
        "No VCS write",
        "renderArtifactPreview(result.payload || {}, artifactId, result.ok)",
    ]:
        assert marker in app
