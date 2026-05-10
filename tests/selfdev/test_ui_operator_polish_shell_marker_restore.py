from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_operator_polish_shell_marker_is_restored_without_touching_app_contract():
    html = read_ui_file("index.html")
    css = read_ui_file("styles.css")
    app = read_ui_file("app.js")

    assert "selfdev-shell" in html
    assert ".selfdev-shell" in css

    # Goal 27 read-only contract checks app.js only. Restoring the legacy
    # HTML/CSS marker must not reintroduce forbidden action terms there.
    assert "commit" not in app
    assert "shell" not in app
