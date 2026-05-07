"""Commit Gate skeleton.

Commit Gate only evaluates readiness. It does not commit in this phase.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CommitReadiness:
    status: str
    missing: list[str] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        return self.status == "READY"


def evaluate_commit_readiness(requirements: dict[str, bool]) -> CommitReadiness:
    missing = [name for name, ok in requirements.items() if not ok]
    if missing:
        return CommitReadiness(status="BLOCKED", missing=missing)
    return CommitReadiness(status="READY", missing=[])
