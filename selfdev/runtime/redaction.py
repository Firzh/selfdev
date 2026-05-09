"""Deterministic redaction service for SelfDev.

The service is intentionally conservative and dependency-free. It does not
read files, write files, call an LLM, or execute commands. Future flows can use
it before showing logs, prompts, review comments, or artifact previews.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class RedactionRule:
    """A single deterministic redaction rule."""

    name: str
    pattern: Pattern[str]
    replacement: str
    description: str


@dataclass(frozen=True)
class RedactionFinding:
    """Metadata for one redaction match."""

    rule: str
    start: int
    end: int

    def to_dict(self) -> dict[str, int | str]:
        return {
            "rule": self.rule,
            "start": self.start,
            "end": self.end,
        }


@dataclass(frozen=True)
class RedactionResult:
    """Result returned by the redaction service."""

    original_length: int
    redacted_text: str
    findings: tuple[RedactionFinding, ...]

    @property
    def redaction_count(self) -> int:
        return len(self.findings)

    @property
    def redacted(self) -> bool:
        return bool(self.findings)

    def to_dict(self) -> dict[str, object]:
        return {
            "redacted": self.redacted,
            "redaction_count": self.redaction_count,
            "original_length": self.original_length,
            "redacted_length": len(self.redacted_text),
            "redacted_text": self.redacted_text,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def _compile(pattern: str) -> Pattern[str]:
    return re.compile(pattern, re.MULTILINE)


DEFAULT_RULES: tuple[RedactionRule, ...] = (
    RedactionRule(
        name="github_token",
        pattern=_compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        replacement="[REDACTED:GITHUB_TOKEN]",
        description="GitHub fine-grained or classic personal access token shape.",
    ),
    RedactionRule(
        name="openai_style_secret",
        pattern=_compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
        replacement="[REDACTED:SECRET_KEY]",
        description="OpenAI-style secret key shape.",
    ),
    RedactionRule(
        name="bearer_token",
        pattern=_compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
        replacement="Bearer [REDACTED:BEARER_TOKEN]",
        description="Bearer authorization token.",
    ),
    RedactionRule(
        name="env_secret_assignment",
        pattern=_compile(
            r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|API_KEY|PRIVATE_KEY|ACCESS_KEY|AUTH_KEY)[A-Z0-9_]*)"
            r"(\s*=\s*)"
            r"([^\s#]+)"
        ),
        replacement=r"\1\2[REDACTED:ENV_SECRET]",
        description="Environment-style secret assignment; keeps the variable name visible.",
    ),
)


class RedactionService:
    """Apply deterministic redaction rules to text."""

    def __init__(self, rules: tuple[RedactionRule, ...] = DEFAULT_RULES) -> None:
        self.rules = rules

    def redact_text(self, text: str) -> RedactionResult:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        findings: list[RedactionFinding] = []
        redacted_text = text

        for rule in self.rules:
            matches = list(rule.pattern.finditer(redacted_text))
            if not matches:
                continue
            findings.extend(
                RedactionFinding(rule=rule.name, start=match.start(), end=match.end())
                for match in matches
            )
            redacted_text = rule.pattern.sub(rule.replacement, redacted_text)

        return RedactionResult(
            original_length=len(text),
            redacted_text=redacted_text,
            findings=tuple(findings),
        )


def redact_text(text: str) -> RedactionResult:
    """Convenience wrapper for the default deterministic service."""

    return RedactionService().redact_text(text)
