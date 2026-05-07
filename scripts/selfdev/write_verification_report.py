from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.verification_flow import write_verification_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a deterministic SelfDev verification report.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    parser.add_argument(
        "--required-file",
        action="append",
        default=[],
        help="Required file path relative to workspace. Can be repeated.",
    )
    args = parser.parse_args()

    result = write_verification_report(
        task_id=args.task_id,
        required_files=args.required_file,
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.verification_status == "PASS":
        return 0

    if result.verification_status == "FAIL":
        return 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
