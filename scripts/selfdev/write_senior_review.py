from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.senior_review_gate import write_senior_review


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a Senior Reviewer decision.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--task-id", required=True)
    parser.add_argument(
        "--decision",
        required=True,
        choices=[
            "approve_for_runner",
            "request_revision",
            "request_specialist_review",
            "block",
            "human_required",
        ],
    )
    parser.add_argument(
        "--reason",
        action="append",
        default=[],
        help="Reason for the decision. Can be passed multiple times.",
    )
    args = parser.parse_args()

    result = write_senior_review(
        task_id=args.task_id,
        decision=args.decision,
        reasons=args.reason,
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.status in {"ready_for_verification", "needs_revision", "needs_review", "human_required"}:
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
