from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.full_dry_run import run_full_dry_run


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic SelfDev full dry run.")
    parser.add_argument("manifest", help="Path to task manifest YAML")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--runner-action", default="git_apply_check")
    args = parser.parse_args()

    result = run_full_dry_run(
        manifest_path=Path(args.manifest),
        workspace=Path(args.workspace),
        runner_action=args.runner_action,
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.status == "dry_run_complete":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
