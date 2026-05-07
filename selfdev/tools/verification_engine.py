"""Minimal deterministic verification engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VerificationResult:
    status: str
    checks: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def verify_required_files(paths: list[str]) -> VerificationResult:
    checks: dict[str, str] = {}
    notes: list[str] = []

    for raw_path in paths:
        path = Path(raw_path)
        if path.exists():
            checks[raw_path] = "PASS"
        else:
            checks[raw_path] = "FAIL"
            notes.append(f"Missing required file: {raw_path}")

    status = "PASS" if all(result == "PASS" for result in checks.values()) else "FAIL"
    return VerificationResult(status=status, checks=checks, notes=notes)
