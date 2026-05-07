from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.safety_flow import write_safety_decision


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a deterministic SelfDev Safety Gate decision.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--action", action="append", default=[], help="Requested action. Can be repeated.")
    parser.add_argument("--changed-path", action="append", default=[], help="Changed path. Can be repeated.")
    args = parser.parse_args()

    result = write_safety_decision(
        task_id=args.task_id,
        requested_actions=args.action,
        changed_paths=args.changed_path,
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.safety_status == "PASS":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
