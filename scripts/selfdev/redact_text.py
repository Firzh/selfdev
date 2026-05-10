#!/usr/bin/env python3
"""Redact text using SelfDev deterministic redaction policy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.redaction import redact_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Redact sensitive text deterministically.")
    parser.add_argument("--text", default="", help="Text to redact")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = redact_text(args.text)
    payload = {
        "text": result.text,
        "redacted_text": result.redacted_text,
        "redacted": result.redacted,
        "redaction_count": result.redaction_count,
        "findings": [finding.to_dict() for finding in result.findings],
        "redactions": list(result.redactions),
        "matches": [finding.to_dict() for finding in result.matches],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
