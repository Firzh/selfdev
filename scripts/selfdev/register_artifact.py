from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.artifact_registry import ArtifactRecord, ArtifactRegistry
from selfdev.tools.artifact_gate import validate_artifact_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Register and validate a SelfDev artifact.")
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--artifact-type", required=True)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace)

    record = ArtifactRecord(
        artifact_id=args.artifact_id,
        task_id=args.task_id,
        agent_id=args.agent_id,
        artifact_type=args.artifact_type,
        path=args.path,
    )

    result = validate_artifact_record(record.to_dict(), workspace=workspace)
    if not result.passed:
        print("Artifact invalid", file=sys.stderr)
        for reason in result.reasons:
            print(f"ERROR: {reason}", file=sys.stderr)
        return 1

    registry = ArtifactRegistry(workspace)
    registry.register(record)

    print(json.dumps(record.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
