from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from selfdev.runtime.redaction import RedactionResult, RedactionService, redact_text

ROOT = Path(__file__).resolve().parents[2]


def test_redaction_result_contract_is_structured_and_legacy_compatible():
    result = redact_text("API_TOKEN=super-secret-value")

    assert isinstance(result, RedactionResult)
    assert result.redacted is True
    assert result.text == result.redacted_text
    assert "super-secret-value" not in result.redacted_text
    assert result.redactions
    assert result.redactions[0]["rule"] == "env_secret_assignment"


def test_redaction_service_rejects_non_string_input_contract():
    with pytest.raises(TypeError, match="text must be a string"):
        RedactionService().redact_text(None)  # type: ignore[arg-type]


def test_redaction_cli_outputs_json_contract():
    completed = subprocess.run(
        [sys.executable, "scripts/selfdev/redact_text.py", "--text", "PASSWORD=hunter2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["redacted"] is True
    assert "hunter2" not in payload["redacted_text"]
