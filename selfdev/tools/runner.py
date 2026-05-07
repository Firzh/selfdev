"""Controlled Runner skeleton.

Runner is intentionally non-executing in this phase.
"""

from __future__ import annotations

from dataclasses import dataclass, field


DENIED_RUNNER_ACTIONS = {
    "git_push",
    "git_merge",
    "terraform_apply",
    "terraform_destroy",
    "kubectl_apply_real_cluster",
    "kubectl_delete",
    "restart_service",
    "modify_env",
    "read_secret",
    "rm_rf",
}


@dataclass
class RunnerResult:
    status: str
    action: str
    notes: list[str] = field(default_factory=list)


def validate_runner_request(action: str) -> RunnerResult:
    if action in DENIED_RUNNER_ACTIONS:
        return RunnerResult(status="BLOCKED", action=action, notes=[f"Denied runner action: {action}"])
    return RunnerResult(status="ACCEPTED", action=action, notes=["Request accepted for later implementation."])
