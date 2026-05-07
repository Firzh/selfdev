from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_validate_manifest_cli_accepts_example_manifest():
    root = Path(__file__).resolve().parents[2]
    manifest = root / "examples" / "manifests" / "task-docs-001.yaml"
    result = subprocess.run(
        [sys.executable, "scripts/selfdev/validate_manifest.py", str(manifest)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Manifest valid" in result.stdout
