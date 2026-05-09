from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from selfdev.runtime.redaction import RedactionService, redact_text


ROOT = Path(__file__).resolve().parents[2]


def test_redaction_service_redacts_env_secret_but_preserves_key_name():
    text = "API_TOKEN=super-secret-value keep this visible"

    result = redact_text(text)

    assert result.redacted is True
    assert result.redaction_count == 1
    assert "API_TOKEN=" in result.redacted_text
    assert "super-secret-value" not in result.redacted_text
    assert "[REDACTED:ENV_SECRET]" in result.redacted_text
    assert result.findings[0].rule == "env_secret_assignment"


def test_redaction_service_redacts_common_token_shapes():
    text = (
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456 "
        "token=github_pat_abcdefghijklmnopqrstuvwxyz1234567890 "
        "secret=sk-abcdefghijklmnopqrstuvwxyz123456"
    )

    result = RedactionService().redact_text(text)

    assert result.redacted is True
    assert result.redaction_count >= 3
    assert "Bearer abcdefghijklmnopqrstuvwxyz123456" not in result.redacted_text
    assert "github_pat_abcdefghijklmnopqrstuvwxyz1234567890" not in result.redacted_text
    assert "sk-abcdefghijklmnopqrstuvwxyz123456" not in result.redacted_text
    assert "Bearer [REDACTED:BEARER_TOKEN]" in result.redacted_text
    assert "[REDACTED:GITHUB_TOKEN]" in result.redacted_text
    assert "[REDACTED:SECRET_KEY]" in result.redacted_text


def test_redaction_service_is_noop_for_plain_text():
    text = "plain deterministic status without credentials"

    result = redact_text(text)

    assert result.redacted is False
    assert result.redaction_count == 0
    assert result.redacted_text == text
    assert result.to_dict()["findings"] == []


def test_redaction_service_rejects_non_string_input():
    with pytest.raises(TypeError, match="text must be a string"):
        redact_text(123)  # type: ignore[arg-type]


def test_redact_text_cli_outputs_json_without_raw_secret():
    secret = "PASSWORD=hunter2"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "selfdev" / "redact_text.py"),
            "--text",
            secret,
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["redacted"] is True
    assert payload["redaction_count"] == 1
    assert "PASSWORD=" in payload["redacted_text"]
    assert "hunter2" not in payload["redacted_text"]
    assert "hunter2" not in completed.stdout
