from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.artifact_preview import DEFAULT_MAX_PREVIEW_CHARS, preview_artifact


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preview one registered SelfDev artifact with deterministic redaction."
    )
    parser.add_argument("--workspace", default="data/agent_workspace", help="SelfDev workspace directory.")
    parser.add_argument("--artifact-id", required=True, help="Artifact id from artifacts/index.json.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_PREVIEW_CHARS,
        help="Maximum text characters to include before redaction.",
    )
    args = parser.parse_args()

    result = preview_artifact(
        artifact_id=args.artifact_id,
        workspace=Path(args.workspace),
        max_chars=args.max_chars,
    )
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
