"""Stable payload envelope helpers for SelfDev read APIs.

This module is deterministic and read-only. It only normalizes in-memory payloads
so callers can wrap current read API data without changing the underlying API
surface.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

PAYLOAD_CONTRACT_NAME = "selfdev.read_api.payload.v1"
READ_ONLY_MODE = "read_only"
_VALID_STATUSES = {"ok", "error"}


@dataclass(frozen=True)
class PayloadMeta:
    """Metadata carried by every read-only payload envelope."""

    resource: str
    status: str = "ok"
    exists: bool | None = None
    error: Mapping[str, Any] | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": PAYLOAD_CONTRACT_NAME,
            "resource": self.resource,
            "mode": READ_ONLY_MODE,
            "status": self.status,
            "exists": self.exists,
            "error": dict(self.error) if self.error is not None else None,
            "warnings": list(self.warnings),
        }


def _warning_tuple(warnings: Sequence[str] | None) -> tuple[str, ...]:
    if warnings is None:
        return ()
    return tuple(str(item) for item in warnings)


def normalize_payload(
    resource: str,
    data: Any,
    *,
    status: str = "ok",
    exists: bool | None = None,
    warnings: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Wrap read API data in a stable read-only payload envelope."""

    meta = PayloadMeta(
        resource=str(resource),
        status=str(status),
        exists=exists,
        error=None,
        warnings=_warning_tuple(warnings),
    )
    return {"meta": meta.to_dict(), "data": data}


def normalize_error_payload(
    resource: str,
    error: str | Mapping[str, Any] | None = None,
    *,
    code: str | None = None,
    message: str | None = None,
    exists: bool | None = None,
    warnings: Sequence[str] | None = None,
    data: Any | None = None,
) -> dict[str, Any]:
    """Wrap an error in the same stable read-only payload envelope.

    The function accepts the original positional error value as well as the
    newer ``code=`` keyword contract used by the Goal 29 tests.
    """

    if isinstance(error, Mapping):
        existing_error = dict(error)
    elif error is None:
        existing_error = {}
    else:
        existing_error = {"code": str(error), "message": str(error)}

    error_code = code or existing_error.get("code") or "error"
    error_message = message or existing_error.get("message") or str(error_code)
    normalized_error = {"code": str(error_code), "message": str(error_message)}
    for key, value in existing_error.items():
        if key not in normalized_error:
            normalized_error[key] = value

    meta = PayloadMeta(
        resource=str(resource),
        status="error",
        exists=exists,
        error=normalized_error,
        warnings=_warning_tuple(warnings),
    )
    return {"meta": meta.to_dict(), "data": {} if data is None else data}


def validate_payload_envelope(envelope: Mapping[str, Any]) -> list[str]:
    """Return validation errors for a normalized payload envelope."""

    errors: list[str] = []
    if not isinstance(envelope, Mapping):
        return ["envelope must be a mapping"]

    meta = envelope.get("meta")
    if not isinstance(meta, Mapping):
        errors.append("meta must be a mapping")
        return errors

    if meta.get("contract") != PAYLOAD_CONTRACT_NAME:
        errors.append("meta.contract mismatch")
    if meta.get("mode") != READ_ONLY_MODE:
        errors.append("meta.mode must be read_only")
    if not isinstance(meta.get("resource"), str) or not meta.get("resource"):
        errors.append("meta.resource is required")
    if meta.get("status") not in _VALID_STATUSES:
        errors.append("meta.status must be ok or error")
    if meta.get("exists") is not None and not isinstance(meta.get("exists"), bool):
        errors.append("meta.exists must be bool or null")
    if "data" not in envelope:
        errors.append("data key is required")
    if not isinstance(meta.get("warnings"), list):
        errors.append("meta.warnings must be a list")

    if meta.get("status") == "error":
        error = meta.get("error")
        if not isinstance(error, Mapping):
            errors.append("meta.error must be a mapping when status is error")
        else:
            if not error.get("code"):
                errors.append("meta.error.code is required")
            if not error.get("message"):
                errors.append("meta.error.message is required")
    elif meta.get("error") is not None:
        errors.append("meta.error must be null when status is ok")

    return errors


def is_valid_payload_envelope(envelope: Mapping[str, Any]) -> bool:
    """Return True when the envelope matches the read API payload contract."""

    return not validate_payload_envelope(envelope)
