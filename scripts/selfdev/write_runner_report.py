from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.runner_flow import write_runner_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a deterministic SelfDev Runner report.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--action", required=True)
    args = parser.parse_args()

    result = write_runner_report(
        task_id=args.task_id,
        action=args.action,
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.runner_status == "ACCEPTED":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
