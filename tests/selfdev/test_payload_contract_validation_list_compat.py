from __future__ import annotations

from selfdev.api.payload_contract import (
    normalize_error_payload,
    normalize_payload,
    validate_payload_envelope,
)


def test_validate_payload_envelope_returns_empty_list_for_valid_payload():
    payload = normalize_payload("health", {"status": "ok"})

    assert validate_payload_envelope(payload) == []


def test_validate_payload_envelope_returns_errors_without_raising():
    errors = validate_payload_envelope({"meta": {"mode": "wrong"}, "data": {}})

    assert isinstance(errors, list)
    assert errors


def test_normalize_error_payload_supports_positional_and_code_keyword():
    positional = normalize_error_payload("health", "missing")
    keyword = normalize_error_payload(
        resource="health",
        code="example_error",
        message="Example failure",
        exists=False,
    )

    assert positional["meta"]["error"]["code"] == "missing"
    assert keyword["meta"]["error"]["code"] == "example_error"
    assert keyword["meta"]["error"]["message"] == "Example failure"
    assert keyword["data"] == {}
    assert validate_payload_envelope(positional) == []
    assert validate_payload_envelope(keyword) == []
