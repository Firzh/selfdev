"""Deterministic Safety Gate.

Safety Gate does not execute actions.
It only checks requested actions and paths against local policy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath


DEFAULT_DENIED_ACTIONS = {
    "run_shell",
    "arbitrary_shell",
    "git_push",
    "git_merge",
    "git_rebase",
    "git_reset_hard",
    "modify_env",
    "read_secret",
    "delete_file",
    "deploy",
    "release",
}

DEFAULT_DENIED_PATHS = {
    ".env",
    ".env.*",
    ".git/",
    "data/secrets/",
}


@dataclass
class SafetyResult:
    status: str
    reasons: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def normalize_path(path: str) -> str:
    return str(PurePosixPath(path.replace("\\", "/")))


def _matches_denied_path(path: str, denied_path: str) -> bool:
    normalized = normalize_path(path)
    denied = normalize_path(denied_path)

    if denied.endswith("*"):
        return normalized.startswith(denied[:-1])

    if denied.endswith("/"):
        return normalized.startswith(denied)

    return normalized == denied or normalized.startswith(denied + "/")


def check_action(action: str, denied_actions: set[str] | None = None) -> SafetyResult:
    denied = denied_actions or DEFAULT_DENIED_ACTIONS
    if action in denied:
        return SafetyResult(status="BLOCK", reasons=[f"Denied action: {action}"])
    return SafetyResult(status="PASS", reasons=[])


def check_actions(actions: list[str], denied_actions: set[str] | None = None) -> SafetyResult:
    denied = denied_actions or DEFAULT_DENIED_ACTIONS
    reasons = [f"Denied action: {action}" for action in actions if action in denied]
    if reasons:
        return SafetyResult(status="BLOCK", reasons=reasons)
    return SafetyResult(status="PASS", reasons=[])


def check_paths(paths: list[str], denied_paths: set[str] | None = None) -> SafetyResult:
    denied = denied_paths or DEFAULT_DENIED_PATHS
    reasons: list[str] = []

    for raw_path in paths:
        for denied_path in denied:
            if _matches_denied_path(raw_path, denied_path):
                reasons.append(f"Denied path touched: {raw_path}")

    if reasons:
        return SafetyResult(status="BLOCK", reasons=reasons)

    return SafetyResult(status="PASS", reasons=[])
