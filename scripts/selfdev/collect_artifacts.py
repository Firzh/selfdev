from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.artifact_collector import collect_artifact_reply


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect artifact_ready reply from an agent.")
    parser.add_argument("reply", help="Path to artifact_ready JSON message")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument(
        "--required-artifact-type",
        action="append",
        default=[],
        help="Required artifact type. Can be passed multiple times.",
    )
    args = parser.parse_args()

    result = collect_artifact_reply(
        reply_path=Path(args.reply),
        workspace=Path(args.workspace),
        required_artifact_types=args.required_artifact_type,
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.status == "ready_for_senior":
        return 0

    if result.status == "needs_revision":
        return 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
