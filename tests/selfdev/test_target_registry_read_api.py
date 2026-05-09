from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from selfdev.api.read_api import ReadApi


ROOT = Path(__file__).resolve().parents[2]


def _write_targets(config_dir: Path) -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "targets.yaml").write_text(
        yaml.safe_dump(
            {
                "targets": {
                    "selfdev": {
                        "name": "SelfDev",
                        "type": "local_system",
                        "root_path": ".",
                        "allowed_paths": ["docs/", "config/", "selfdev/", "scripts/", "tests/"],
                        "denied_paths": [".env", ".git/"],
                    }
                }
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def test_read_api_lists_targets(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    payload = ReadApi(config_dir=config_dir).targets()

    assert "selfdev" in payload["targets"]
    assert payload["targets"]["selfdev"]["name"] == "SelfDev"


def test_read_api_returns_single_target(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    payload = ReadApi(config_dir=config_dir).target("selfdev")

    assert payload["target_id"] == "selfdev"
    assert payload["exists"] is True
    assert payload["target"]["type"] == "local_system"


def test_read_api_returns_missing_target(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    payload = ReadApi(config_dir=config_dir).target("missing")

    assert payload == {"target_id": "missing", "exists": False, "target": None}


@pytest.mark.parametrize("bad_target_id", ["", "../secret", "a/b", "a\\b", ".", ".."])
def test_read_api_rejects_invalid_target_id(tmp_path: Path, bad_target_id: str) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    with pytest.raises(ValueError):
        ReadApi(config_dir=config_dir).target(bad_target_id)


def test_read_api_summary_includes_target_count(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    workspace = tmp_path / "workspace"
    _write_targets(config_dir)

    payload = ReadApi(workspace=workspace, config_dir=config_dir).summary()

    assert payload["target_count"] == 1


def test_cli_lists_targets(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "targets",
            "--config-dir",
            str(config_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert "selfdev" in payload["targets"]


def test_cli_reads_single_target(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "target",
            "--target-id",
            "selfdev",
            "--config-dir",
            str(config_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["exists"] is True
    assert payload["target_id"] == "selfdev"


def test_cli_requires_target_id(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    _write_targets(config_dir)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/read_api.py",
            "target",
            "--config-dir",
            str(config_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "--target-id is required" in result.stderr
