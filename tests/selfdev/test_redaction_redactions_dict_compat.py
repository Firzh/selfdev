from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from selfdev.runtime.redaction import RedactionFinding, RedactionResult, redact_text


ROOT = Path(__file__).resolve().parents[2]


def test_redactions_are_sanitized_dicts_and_findings_remain_typed():
    result = redact_text(
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456 "
        "token=github_pat_abcdefghijklmnopqrstuvwxyz1234567890 "
        "secret=sk-abcdefghijklmnopqrstuvwxyz123456 "
        "PASSWORD=hunter2-value"
    )

    assert isinstance(result, RedactionResult)
    assert result.redaction_count >= 4
    assert result.redactions
    assert isinstance(result.redactions[0], dict)
    assert "rule" in result.redactions[0]
    assert isinstance(result.findings[0], RedactionFinding)
    assert all("value" not in item for item in result.redactions)
    assert "[REDACTED:GITHUB_TOKEN]" in result.redacted_text
    assert "[REDACTED:SECRET_KEY]" in result.redacted_text
    assert "[REDACTED:ENV_SECRET]" in result.redacted_text
    assert "hunter2-value" not in result.redacted_text


def test_redaction_result_supports_string_contains_without_leaking_raw_values():
    result = redact_text(
        "owner=operator@example.test path=C:\\Users\\alice\\workspace home=/home/bob/selfdev"
    )

    assert "operator@example.test" not in result
    assert "alice" not in result
    assert "/home/bob" not in result
    assert "[REDACTED:EMAIL]" in result
    assert "[REDACTED:USER_PATH]" in result
    assert str(result) == result.redacted_text


def test_redact_text_cli_default_json_and_json_flag_are_compatible():
    for extra_args in ([], ["--json"]):
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/selfdev/redact_text.py",
                "--text",
                "PASSWORD=hunter2-value",
                *extra_args,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        payload = json.loads(completed.stdout)
        assert payload["redacted"] is True
        assert payload["redaction_count"] == 1
        assert "hunter2-value" not in completed.stdout
        assert payload["redactions"][0]["rule"] == "env_secret_assignment"
