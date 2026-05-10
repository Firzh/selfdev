from selfdev.runtime.redaction import RedactionFinding, RedactionResult, redact_text


def test_matches_remain_typed_legacy_alias_and_redactions_are_dicts():
    result = redact_text("PASSWORD=hunter2")

    assert isinstance(result, RedactionResult)
    assert result.matches == result.findings
    assert isinstance(result.findings[0], RedactionFinding)
    assert isinstance(result.redactions[0], dict)
    assert result.redactions[0]["rule"] == "env_secret_assignment"
    assert result.findings[0]["rule"] == "env_secret_assignment"
    assert "hunter2" not in result


def test_to_dict_exposes_findings_and_counts_without_raw_values():
    result = redact_text("token=github_pat_abcdefghijklmnopqrstuvwxyz1234567890")
    payload = result.to_dict()

    assert payload["redacted"] is True
    assert payload["redaction_count"] == result.redaction_count
    assert payload["findings"]
    assert payload["redactions"]
    assert payload["matches"]
    assert "github_pat_abcdefghijklmnopqrstuvwxyz1234567890" not in str(payload)
