#!/usr/bin/env python3
"""Check current SelfDev read API payloads against the stable envelope."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.api.payload_contract import (  # noqa: E402
    normalize_error_payload,
    normalize_payload,
    validate_payload_envelope,
)
from selfdev.api.read_api import ReadApi  # noqa: E402

DEFAULT_RESOURCES = (
    "health",
    "summary",
    "agents",
    "tools",
    "kanban",
    "artifacts",
    "targets",
)


def _make_api(workspace: Path, config_dir: Path) -> ReadApi:
    try:
        return ReadApi(workspace=workspace, config_dir=config_dir)
    except TypeError:
        return ReadApi(workspace=workspace)


def _read_resource(api: ReadApi, resource: str) -> Any:
    readers = {
        "health": api.health,
        "summary": api.summary,
        "agents": api.agents,
        "tools": api.tools,
        "kanban": api.kanban,
        "artifacts": api.artifacts,
        "targets": api.targets,
    }
    reader = readers.get(resource)
    if reader is None:
        raise KeyError(f"unsupported resource: {resource}")
    return reader()


def _parse_resources(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_RESOURCES)
    return [item.strip() for item in raw.split(",") if item.strip()]


def build_report(resources: list[str], workspace: Path, config_dir: Path) -> dict[str, Any]:
    api = _make_api(workspace=workspace, config_dir=config_dir)
    payloads: dict[str, Any] = {}
    errors: dict[str, list[str]] = {}

    for resource in resources:
        try:
            payload = _read_resource(api, resource)
            envelope = normalize_payload(resource, payload)
        except Exception as exc:  # pragma: no cover - defensive CLI reporting
            envelope = normalize_error_payload(resource, exc.__class__.__name__)
        validation_errors = validate_payload_envelope(envelope)
        payloads[resource] = envelope
        if validation_errors:
            errors[resource] = validation_errors

    return {
        "mode": "read_only",
        "checked": resources,
        "ok": not errors,
        "errors": errors,
        "payloads": payloads,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("data/agent_workspace"))
    parser.add_argument("--config-dir", type=Path, default=Path("config/selfdev"))
    parser.add_argument("--resources", default=",".join(DEFAULT_RESOURCES))
    args = parser.parse_args(argv)

    report = build_report(
        resources=_parse_resources(args.resources),
        workspace=args.workspace,
        config_dir=args.config_dir,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
