from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.redaction import redact_text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Redact sensitive values from provided text without reading or writing files."
    )
    parser.add_argument("--text", required=True, help="Text to redact.")
    args = parser.parse_args()

    result = redact_text(args.text)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
