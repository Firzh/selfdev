import json
import subprocess
import sys

from selfdev.runtime.redaction import RedactionFinding, RedactionResult, RedactionService, redact_text


def test_password_exact_key_is_redacted_and_matches_are_typed_alias():
    result = redact_text("PASSWORD=hunter2")

    assert isinstance(result, RedactionResult)
    assert result.redacted is True
    assert result.redaction_count == 1
    assert result.matches == result.findings
    assert isinstance(result.findings[0], RedactionFinding)
    assert result.redactions[0]["rule"] == "env_secret_assignment"
    assert result.findings[0]["rule"] == "env_secret_assignment"
    assert "hunter2" not in result


def test_expanded_policy_keeps_specific_markers_before_env_assignment():
    raw = " ".join(
        [
            "PASSWORD=hunter2-value",
            "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456",
            "token=github_pat_abcdefghijklmnopqrstuvwxyz1234567890",
            "secret=sk-abcdefghijklmnopqrstuvwxyz123456",
            "postgres://selfdev:db-secret-value@localhost:5432/app",
            "https://user:basic-secret-value@example.test/path",
            "owner=operator@example.test",
            "path=C:\\Users\\alice\\workspace",
            "home=/home/bob/selfdev",
        ]
    )

    result = RedactionService().redact(raw)

    assert result.redacted is True
    for raw_value in [
        "hunter2-value",
        "abcdefghijklmnopqrstuvwxyz1234567890",
        "sk-abcdefghijklmnopqrstuvwxyz123456",
        "db-secret-value",
        "basic-secret-value",
        "operator@example.test",
        "alice",
        "/home/bob",
    ]:
        assert raw_value not in result.text
    assert "[REDACTED:ENV_SECRET]" in result.text
    assert "[REDACTED:BEARER_TOKEN]" in result.text
    assert "[REDACTED:GITHUB_TOKEN]" in result.text
    assert "[REDACTED:SECRET_KEY]" in result.text
    assert "[REDACTED:URL_PASSWORD]" in result.text
    assert "[REDACTED:BASIC_AUTH]" in result.text
    assert "[REDACTED:EMAIL]" in result.text
    assert "[REDACTED:USER_PATH]" in result.text


def test_redaction_cli_default_json_redacts_password_exact_key():
    completed = subprocess.run(
        [sys.executable, "scripts/selfdev/redact_text.py", "--text", "PASSWORD=hunter2"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["redacted"] is True
    assert payload["redaction_count"] == 1
    assert "hunter2" not in completed.stdout
