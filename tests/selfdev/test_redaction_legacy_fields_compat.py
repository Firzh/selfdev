from selfdev.runtime.redaction import RedactionResult, RedactionService, redact_text


def test_redaction_result_exposes_legacy_fields_and_string_contains():
    result = redact_text("PASSWORD=hunter2")

    assert isinstance(result, RedactionResult)
    assert result.redacted is True
    assert result.redaction_count == 1
    assert result.text == result.redacted_text
    assert result.matches == result.findings
    assert result.redactions == result.findings
    assert "hunter2" not in result
    assert "[REDACTED:ENV_SECRET]" in result
    assert all(not hasattr(match, "value") for match in result.matches)


def test_redaction_policy_result_keeps_expanded_coverage():
    raw = "\n".join(
        [
            "PASSWORD=hunter2-value",
            "postgres://selfdev:db-secret-value@localhost:5432/app",
            "https://user:basic-secret-value@example.test/path",
            "owner=operator@example.test",
            "path=C:\\Users\\alice\\workspace",
            "home=/home/bob/selfdev",
        ]
    )

    result = RedactionService().redact(raw)

    assert result.redacted is True
    for raw_secret in [
        "hunter2-value",
        "db-secret-value",
        "basic-secret-value",
        "operator@example.test",
        "alice",
        "/home/bob",
    ]:
        assert raw_secret not in result.text
    assert result.redaction_count >= 6
