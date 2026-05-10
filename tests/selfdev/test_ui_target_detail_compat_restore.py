from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI / name).read_text(encoding="utf-8")


def test_goal_28_keeps_legacy_html_markers():
    html = read_ui_file("index.html")

    for marker in [
        "SelfDev Operator Console",
        "Preview content is bounded",
        "Click an artifact card",
        "target-detail-panel",
        "target-id-input",
        "target-detail-button",
        "target-detail-content",
    ]:
        assert marker in html


def test_goal_28_keeps_artifact_browser_css_markers():
    css = read_ui_file("styles.css")

    for selector in [
        ".artifact-browser-panel",
        ".artifact-list",
        ".artifact-card",
        ".artifact-card:hover",
        ".artifact-preview-panel",
        ".artifact-preview-content",
        ".artifact-preview-meta",
        ".target-detail-panel",
        ".target-detail-content",
    ]:
        assert selector in css


def test_goal_28_keeps_artifact_card_id_contract_without_mutation_terms():
    app = read_ui_file("app.js")

    assert "data-artifact-id" in app
    assert "/targets/{target_id}" in app
    assert "function renderTargetDetail" in app
    assert "loadTargetDetail" in app
    for forbidden in [
        'method: "POST"',
        'method: "PUT"',
        'method: "DELETE"',
        "applyPatch",
        "commit",
        "shell",
    ]:
        assert forbidden not in app
