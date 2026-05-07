from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.routing_gate import resolve_manifest_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve SelfDev routing for a task manifest.")
    parser.add_argument("manifest", help="Path to manifest YAML file")
    parser.add_argument(
        "--routing-rules",
        default="config/selfdev/routing_rules.yaml",
        help="Path to routing_rules.yaml",
    )
    args = parser.parse_args()

    decision = resolve_manifest_file(
        manifest_path=Path(args.manifest),
        routing_rules_path=Path(args.routing_rules),
    )

    print(json.dumps(decision.to_dict(), indent=2, ensure_ascii=False))

    if decision.decision == "manifest_invalid":
        return 1

    if decision.decision == "human_required":
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
