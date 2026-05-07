from __future__ import annotations

from pathlib import Path
import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict:
    assert path.exists(), f"Missing YAML file: {path}"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"YAML must be a mapping: {path}"
    return data
