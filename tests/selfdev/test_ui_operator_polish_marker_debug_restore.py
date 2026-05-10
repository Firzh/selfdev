from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_operator_polish_marker_contract_is_restored():
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


def test_operator_polish_selector_contract_is_restored():
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
