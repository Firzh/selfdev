"""Deterministic redaction helpers for SelfDev.

The service is intentionally local and regex-based. It does not read files,
call models, execute commands, or mutate repository state.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Pattern, Sequence, Tuple


@dataclass(frozen=True)
class RedactionFinding:
    """A sanitized description of one redaction match."""

    rule: str
    start: int
    end: int
    replacement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "start": self.start,
            "end": self.end,
            "replacement": self.replacement,
        }

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]


class _RedactionRecord(dict):
    """Sanitized dict view that compares equal to its typed finding."""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RedactionFinding):
            return dict.__eq__(self, other.to_dict())
        return dict.__eq__(self, other)


@dataclass(frozen=True)
class RedactionResult:
    """Structured redaction result with legacy-compatible fields."""

    original_text: str
    redacted_text: str
    findings: Tuple[RedactionFinding, ...] = ()

    @property
    def text(self) -> str:
        return self.redacted_text

    @property
    def redacted(self) -> bool:
        return self.original_text != self.redacted_text or bool(self.findings)

    @property
    def redaction_count(self) -> int:
        return len(self.findings)

    @property
    def redactions(self) -> Tuple[dict[str, Any], ...]:
        return tuple(_RedactionRecord(finding.to_dict()) for finding in self.findings)

    @property
    def matches(self) -> Tuple[RedactionFinding, ...]:
        # Legacy alias: older tests compare matches directly to findings.
        return self.findings

    def to_dict(self) -> dict[str, Any]:
        findings = [finding.to_dict() for finding in self.findings]
        return {
            "text": self.redacted_text,
            "redacted_text": self.redacted_text,
            "redacted": self.redacted,
            "redaction_count": self.redaction_count,
            "findings": findings,
            "redactions": findings,
            "matches": findings,
        }

    def __contains__(self, needle: object) -> bool:
        return isinstance(needle, str) and needle in self.redacted_text

    def __str__(self) -> str:
        return self.redacted_text


@dataclass(frozen=True)
class RedactionRule:
    name: str
    pattern: Pattern[str]
    replacement: str


def _compile(pattern: str, flags: int = 0) -> Pattern[str]:
    return re.compile(pattern, flags)


DEFAULT_RULES: Tuple[RedactionRule, ...] = (
    RedactionRule(
        "private_key_block",
        _compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
        "[REDACTED:PRIVATE_KEY]",
    ),
    RedactionRule(
        "bearer_token",
        _compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),
        "Bearer [REDACTED:BEARER_TOKEN]",
    ),
    RedactionRule(
        "github_token",
        _compile(r"github_(?:pat|token)_[A-Za-z0-9_]{20,}"),
        "[REDACTED:GITHUB_TOKEN]",
    ),
    RedactionRule(
        "secret_key",
        _compile(r"sk-[A-Za-z0-9]{20,}"),
        "[REDACTED:SECRET_KEY]",
    ),
    RedactionRule(
        "database_url_password",
        _compile(r"((?:postgres|postgresql|mysql|mariadb)://[^:\s/@]+:)([^@\s]+)(@)"),
        r"\1[REDACTED:URL_PASSWORD]\3",
    ),
    RedactionRule(
        "basic_auth_url",
        _compile(r"(https?://)([^/\s:@]+):([^@/\s]+)@"),
        r"\1[REDACTED:BASIC_AUTH]@",
    ),
    RedactionRule(
        "env_secret_assignment",
        _compile(
            r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|KEY|CREDENTIAL)[A-Z0-9_]*\s*=\s*)(?!\[REDACTED:)([^\s'\"#]+)"
        ),
        r"\1[REDACTED:ENV_SECRET]",
    ),
    RedactionRule(
        "email",
        _compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "[REDACTED:EMAIL]",
    ),
    RedactionRule(
        "windows_user_path",
        _compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+"),
        "[REDACTED:USER_PATH]",
    ),
    RedactionRule(
        "unix_home_path",
        _compile(r"(?<![A-Za-z0-9_])/(?:home|Users)/[^/\s]+"),
        "[REDACTED:USER_PATH]",
    ),
)


class RedactionService:
    """Deterministic text redaction service."""

    def __init__(self, rules: Sequence[RedactionRule] | None = None) -> None:
        self.rules: Tuple[RedactionRule, ...] = tuple(rules or DEFAULT_RULES)

    def redact(self, text: str) -> RedactionResult:
        return self.redact_text(text)

    def redact_text(self, text: str) -> RedactionResult:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        redacted_text = text
        findings: list[RedactionFinding] = []
        for rule in self.rules:
            redacted_text, new_findings = self._apply_rule(rule, redacted_text)
            findings.extend(new_findings)
        findings.sort(key=lambda item: (item.start, item.end, item.rule))
        return RedactionResult(
            original_text=text,
            redacted_text=redacted_text,
            findings=tuple(findings),
        )

    def _apply_rule(self, rule: RedactionRule, text: str) -> tuple[str, list[RedactionFinding]]:
        findings: list[RedactionFinding] = []

        def replace(match: re.Match[str]) -> str:
            replacement = match.expand(rule.replacement)
            if replacement == match.group(0):
                return match.group(0)
            findings.append(
                RedactionFinding(
                    rule=rule.name,
                    start=match.start(),
                    end=match.end(),
                    replacement=replacement,
                )
            )
            return replacement

        return rule.pattern.sub(replace, text), findings


def redact_text(text: str) -> RedactionResult:
    return RedactionService().redact_text(text)
