from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.api.payload_contract import (
    PAYLOAD_CONTRACT_NAME,
    READ_ONLY_MODE,
    normalize_error_payload,
    normalize_payload,
    validate_payload_envelope,
)
from selfdev.api.read_api import ReadApi


def test_normalize_payload_adds_stable_read_only_meta():
    payload = normalize_payload("health", {"status": "ok"})

    assert payload["meta"]["contract"] == PAYLOAD_CONTRACT_NAME
    assert payload["meta"]["resource"] == "health"
    assert payload["meta"]["mode"] == READ_ONLY_MODE
    assert payload["meta"]["status"] == "ok"
    assert payload["meta"]["error"] is None
    assert payload["data"] == {"status": "ok"}
    validate_payload_envelope(payload)

    error_payload = normalize_error_payload(
        resource="health",
        code="example_error",
        message="Example failure",
        exists=False,
    )
    assert error_payload["meta"]["status"] == "error"
    assert error_payload["meta"]["exists"] is False
    assert error_payload["meta"]["error"]["code"] == "example_error"
    assert error_payload["data"] == {}
    validate_payload_envelope(error_payload)


def test_current_read_api_payloads_can_be_wrapped(tmp_path: Path):
    api = ReadApi(workspace=tmp_path / "workspace")

    resources = {
        "health": api.health,
        "summary": api.summary,
        "agents": api.agents,
        "tools": api.tools,
        "kanban": api.kanban,
        "artifacts": api.artifacts,
        "targets": api.targets,
    }

    for resource, loader in resources.items():
        envelope = normalize_payload(resource, loader())
        assert envelope["meta"]["resource"] == resource
        assert envelope["meta"]["mode"] == READ_ONLY_MODE
        assert envelope["meta"]["status"] == "ok"
        validate_payload_envelope(envelope)


def test_payload_contract_checker_cli_is_read_only_and_reports_json():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/check_read_api_payloads.py",
            "--resources",
            "health,summary",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["mode"] == READ_ONLY_MODE
    assert payload["checked"] == ["health", "summary"]

    for resource in payload["checked"]:
        envelope = payload["payloads"][resource]
        assert envelope["meta"]["contract"] == PAYLOAD_CONTRACT_NAME
        assert envelope["meta"]["resource"] == resource
        assert envelope["meta"]["mode"] == READ_ONLY_MODE
        validate_payload_envelope(envelope)


def test_generated_contract_sources_avoid_forbidden_write_capability_markers():
    sources = chr(10).join(
        [
            Path("selfdev/api/payload_contract.py").read_text(encoding="utf-8"),
            Path("scripts/selfdev/check_read_api_payloads.py").read_text(encoding="utf-8"),
            Path("tests/selfdev/test_read_api_payload_consistency.py").read_text(encoding="utf-8"),
        ]
    )

    forbidden = [
        "method: " + chr(34) + "POST" + chr(34),
        "method: " + chr(34) + "PUT" + chr(34),
        "method: " + chr(34) + "DELETE" + chr(34),
        "apply" + "Patch",
        "git " + "push",
        "git " + "merge",
    ]

    for marker in forbidden:
        assert marker not in sources
