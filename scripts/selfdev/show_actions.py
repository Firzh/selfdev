from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.api.action_availability import get_action_availability


def main() -> int:
    parser = argparse.ArgumentParser(description="Show available SelfDev actions for a task.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args()

    result = get_action_availability(
        task_id=args.task_id,
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.exists:
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
