from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_operator_region_markers_remain_available_after_artifact_list_integration():
    html = read_ui_file("index.html")
    css = read_ui_file("styles.css")

    assert "selfdev-shell" in html
    assert "topbar-actions" in html
    assert ".selfdev-shell" in css
    assert ".topbar-actions" in css
    assert ".boundary-grid" in css


def test_artifact_list_patch_does_not_restore_mutating_ui_terms():
    app = read_ui_file("app.js")

    for forbidden in [
        'method: "POST"',
        'method: "PUT"',
        'method: "DELETE"',
        "applyPatch",
        "commit",
        "shell",
    ]:
        assert forbidden not in app
