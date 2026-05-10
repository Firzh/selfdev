from __future__ import annotations

import subprocess
import sys

from selfdev.runtime.redaction import RedactionService, redact_text


def test_redaction_policy_covers_common_secret_shapes_without_leaking_values():
    raw = "\n".join(
        [
            "API_TOKEN=super-secret-value",
            "PASSWORD=hunter2-value",
            "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456",
            "github_pat_1234567890abcdefghijklmnopqrstuvwxyzABCDEF",
            "sk-abcdefghijklmnopqrstuvwxyz1234567890",
            "postgres://selfdev:db-secret-value@localhost:5432/app",
            "https://user:basic-secret-value@example.test/path",
        ]
    )

    result = RedactionService().redact(raw)

    assert result.redacted is True
    assert "super-secret-value" not in result.text
    assert "hunter2-value" not in result.text
    assert "abcdefghijklmnopqrstuvwxyz1234567890" not in result.text
    assert "db-secret-value" not in result.text
    assert "basic-secret-value" not in result.text
    assert "[REDACTED:ENV_SECRET]" in result.text
    assert "[REDACTED:BEARER_TOKEN]" in result.text
    assert "[REDACTED:GITHUB_TOKEN]" in result.text
    assert "[REDACTED:SECRET_KEY]" in result.text
    assert "[REDACTED:URL_PASSWORD]" in result.text
    assert "[REDACTED:BASIC_AUTH]" in result.text
    assert all(not hasattr(match, "value") for match in result.matches)


def test_redaction_policy_covers_private_keys_email_and_user_paths():
    raw = "\n".join(
        [
            "owner=operator@example.test",
            "path=C:\\Users\\alice\\workspace\\selfdev",
            "home=/home/bob/selfdev",
            "-----BEGIN PRIVATE KEY-----",
            "abc123secretmaterial",
            "-----END PRIVATE KEY-----",
        ]
    )

    text = redact_text(raw)

    assert "operator@example.test" not in text
    assert "alice" not in text
    assert "/home/bob" not in text
    assert "abc123secretmaterial" not in text
    assert "[REDACTED:EMAIL]" in text
    assert "[REDACTED:USER_PATH]" in text
    assert "[REDACTED:PRIVATE_KEY]" in text


def test_redaction_policy_leaves_plain_status_text_unchanged():
    raw = "SelfDev read only status is ok. No sensitive credential is present."

    result = RedactionService().redact(raw)

    assert result.text == raw
    assert result.redacted is False
    assert result.matches == ()


def test_redact_text_cli_supports_plain_and_json_output():
    plain = subprocess.run(
        [sys.executable, "scripts/selfdev/redact_text.py", "--text", "API_TOKEN=super-secret-value"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert plain.returncode == 0, plain.stderr
    assert "super-secret-value" not in plain.stdout
    assert "[REDACTED:ENV_SECRET]" in plain.stdout

    structured = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/redact_text.py",
            "--text",
            "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert structured.returncode == 0, structured.stderr
    assert "BEARER_TOKEN" in structured.stdout
    assert "abcdefghijklmnopqrstuvwxyz123456" not in structured.stdout


def test_redaction_policy_sources_avoid_write_capability_markers():
    sources = chr(10).join(
        [
            open("selfdev/runtime/redaction.py", encoding="utf-8").read(),
            open("scripts/selfdev/redact_text.py", encoding="utf-8").read(),
        ]
    )
    forbidden = [
        "method: " + '"POST"',
        "method: " + '"PUT"',
        "method: " + '"DELETE"',
        "apply" + "Patch",
        "git " + "push",
        "git " + "merge",
    ]
    for marker in forbidden:
        assert marker not in sources
