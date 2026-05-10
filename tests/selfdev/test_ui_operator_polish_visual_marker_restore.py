from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "selfdev" / "ui" / "web" / "styles.css"


def test_operator_polish_visual_markers_are_restored():
    css = CSS.read_text(encoding="utf-8")

    assert "radial-gradient" in css
    assert "box-shadow" in css
    assert ".preview-panel" in css


def test_operator_visual_restore_does_not_introduce_mutation_terms():
    css = CSS.read_text(encoding="utf-8")

    for forbidden in ["applyPatch", 'method: "POST"', 'method: "PUT"', 'method: "DELETE"']:
        assert forbidden not in css
