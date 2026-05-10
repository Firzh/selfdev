from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "selfdev" / "ui" / "web"


def read_ui_file(name: str) -> str:
    return (UI_DIR / name).read_text(encoding="utf-8")


def test_static_ui_has_artifact_browser_for_preview_selection():
    html = read_ui_file("index.html")

    assert "Artifact browser" in html
    assert "artifact-list" in html
    assert "Click an artifact card" in html
    assert "Redacted artifact preview" in html
    assert "artifact-id-input" in html


def test_static_ui_fetches_artifacts_and_wires_cards_to_preview():
    app = read_ui_file("app.js")

    assert 'readJson("/artifacts")' in app
    assert "function renderArtifacts" in app
    assert "function artifactEntries" in app
    assert "data-artifact-id" in app
    assert 'byId("artifact-id-input").value = artifactId' in app
    assert "loadArtifactPreview();" in app
    assert "/artifact-previews/{artifact_id}" in app
    assert "/artifact-previews/" in app
    assert "renderArtifactPreview" in app


def test_static_ui_artifact_browser_remains_read_only():
    app = read_ui_file("app.js")

    assert 'method: "GET"' in app
    assert "fetch(" in app
    for forbidden in ['method: "POST"', 'method: "PUT"', 'method: "DELETE"', "applyPatch", "commit", "shell"]:
        assert forbidden not in app


def test_static_ui_styles_artifact_browser_cards():
    css = read_ui_file("styles.css")

    for selector in [
        ".artifact-browser-panel",
        ".artifact-list",
        ".artifact-card",
        ".artifact-card:hover",
        ".artifact-preview-panel",
        ".artifact-preview-content",
        ".artifact-preview-meta",
    ]:
        assert selector in css
