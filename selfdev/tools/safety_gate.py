"""Deterministic Safety Gate.

This module does not execute actions. It only classifies whether a proposed
action or changed path is safe under local policy.
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


def check_action(action: str, denied_actions: set[str] | None = None) -> SafetyResult:
    denied = denied_actions or DEFAULT_DENIED_ACTIONS
    if action in denied:
        return SafetyResult(status="BLOCK", reasons=[f"Denied action: {action}"])
    return SafetyResult(status="PASS", reasons=[])


def check_paths(paths: list[str], denied_paths: set[str] | None = None) -> SafetyResult:
    denied = denied_paths or DEFAULT_DENIED_PATHS
    reasons: list[str] = []

    for raw_path in paths:
        path = normalize_path(raw_path)
        for denied_path in denied:
            denied_norm = normalize_path(denied_path)
            if path == denied_norm.rstrip("/") or path.startswith(denied_norm):
                reasons.append(f"Denied path touched: {raw_path}")

    if reasons:
        return SafetyResult(status="BLOCK", reasons=reasons)
    return SafetyResult(status="PASS", reasons=[])
