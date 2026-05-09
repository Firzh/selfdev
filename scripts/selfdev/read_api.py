from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.api.read_api import ReadApi


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read SelfDev state through the read-only API layer."
    )
    parser.add_argument(
        "resource",
        choices=[
            "health",
            "summary",
            "agents",
            "tools",
            "targets",
            "target",
            "kanban",
            "artifacts",
            "artifact",
            "state",
        ],
    )
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--config-dir", default="config/selfdev")
    parser.add_argument("--task-id", default="")
    parser.add_argument("--target-id", default="")
    parser.add_argument("--artifact-id", default="")
    args = parser.parse_args()

    api = ReadApi(
        workspace=Path(args.workspace),
        config_dir=Path(args.config_dir),
    )

    if args.resource == "health":
        payload = api.health()
    elif args.resource == "summary":
        payload = api.summary()
    elif args.resource == "agents":
        payload = api.agents()
    elif args.resource == "tools":
        payload = api.tools()
    elif args.resource == "targets":
        payload = api.targets()
    elif args.resource == "target":
        if not args.target_id:
            print("ERROR: --target-id is required for target resource", file=sys.stderr)
            return 2
        payload = api.target(args.target_id)
    elif args.resource == "kanban":
        payload = api.kanban()
    elif args.resource == "artifacts":
        payload = api.artifacts()
    elif args.resource == "artifact":
        if not args.artifact_id:
            print("ERROR: --artifact-id is required for artifact resource", file=sys.stderr)
            return 2
        payload = api.artifact(args.artifact_id)
    elif args.resource == "state":
        if not args.task_id:
            print("ERROR: --task-id is required for state resource", file=sys.stderr)
            return 2
        payload = api.state(args.task_id)
    else:
        print(f"ERROR: unsupported resource: {args.resource}", file=sys.stderr)
        return 2

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
