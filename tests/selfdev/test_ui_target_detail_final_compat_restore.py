from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "selfdev" / "ui" / "web" / "index.html"
APP = ROOT / "selfdev" / "ui" / "web" / "app.js"


def test_target_detail_restore_keeps_read_only_badge():
    html = HTML.read_text(encoding="utf-8")

    assert "SelfDev Operator Console" in html
    assert "READ ONLY" in html


def test_target_detail_restore_keeps_artifact_selection_contract():
    app = APP.read_text(encoding="utf-8")

    assert 'byId("artifact-id-input").value = artifactId' in app
    assert "data-artifact-id" in app
    for forbidden in ['method: "POST"', 'method: "PUT"', 'method: "DELETE"', "applyPatch", "commit", "shell"]:
        assert forbidden not in app
