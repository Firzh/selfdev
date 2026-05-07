from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.commit_readiness_flow import evaluate_task_commit_readiness


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate SelfDev commit readiness.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    parser.add_argument(
        "--required-artifact",
        action="append",
        default=[],
        help="Required artifact type. Can be repeated. Uses default list if omitted.",
    )
    args = parser.parse_args()

    result = evaluate_task_commit_readiness(
        task_id=args.task_id,
        workspace=Path(args.workspace),
        required_artifacts=args.required_artifact or None,
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.commit_status == "READY":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
