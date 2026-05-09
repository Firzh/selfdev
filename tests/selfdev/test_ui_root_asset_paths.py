from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[2]
INDEX_HTML = ROOT / "selfdev" / "ui" / "web" / "index.html"


def test_ui_root_uses_ui_scoped_asset_paths():
    html = INDEX_HTML.read_text(encoding="utf-8")

    assert 'href="/ui/styles.css"' in html
    assert 'src="/ui/app.js"' in html
    assert 'href="styles.css"' not in html
    assert 'src="app.js"' not in html


def test_ui_asset_paths_resolve_under_ui_root_from_ui_endpoint():
    html = INDEX_HTML.read_text(encoding="utf-8")

    stylesheet = "/ui/styles.css" if 'href="/ui/styles.css"' in html else "styles.css"
    script = "/ui/app.js" if 'src="/ui/app.js"' in html else "app.js"

    ui_root_url = "http://127.0.0.1:8765/ui"
    assert urlparse(urljoin(ui_root_url, stylesheet)).path == "/ui/styles.css"
    assert urlparse(urljoin(ui_root_url, script)).path == "/ui/app.js"
