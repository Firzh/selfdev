from selfdev.runtime.redaction import RedactionFinding, RedactionResult, redact_text


def test_redactions_are_dict_views_equal_to_typed_findings():
    result = redact_text("PASSWORD=hunter2")

    assert isinstance(result, RedactionResult)
    assert result.redacted is True
    assert result.matches == result.findings
    assert result.redactions == result.findings
    assert isinstance(result.findings[0], RedactionFinding)
    assert isinstance(result.redactions[0], dict)
    assert result.redactions[0]["rule"] == result.findings[0].rule
    assert "hunter2" not in result.text


def test_redactions_dict_view_preserves_json_ready_to_dict():
    result = redact_text("Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456")
    payload = result.to_dict()

    assert payload["redacted"] is True
    assert payload["redaction_count"] == result.redaction_count
    assert isinstance(payload["redactions"], list)
    assert payload["redactions"][0]["rule"] == "bearer_token"
    assert "abcdefghijklmnopqrstuvwxyz123456" not in payload["text"]
