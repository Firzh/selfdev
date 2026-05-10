from __future__ import annotations

from selfdev.api.payload_contract import normalize_error_payload, validate_payload_envelope


def test_normalize_error_payload_accepts_code_keyword_contract():
    payload = normalize_error_payload(
        resource="health",
        code="example_error",
        message="Example failure",
        exists=False,
    )

    assert payload["meta"]["status"] == "error"
    assert payload["meta"]["exists"] is False
    assert payload["meta"]["error"] == {
        "code": "example_error",
        "message": "Example failure",
    }
    assert payload["data"] == {}
    validate_payload_envelope(payload)


def test_normalize_error_payload_still_accepts_error_mapping_contract():
    payload = normalize_error_payload(
        "target",
        error={"code": "missing", "message": "Target missing", "detail": "selfdev"},
    )

    assert payload["meta"]["error"]["code"] == "missing"
    assert payload["meta"]["error"]["message"] == "Target missing"
    assert payload["meta"]["error"]["detail"] == "selfdev"
    validate_payload_envelope(payload)
