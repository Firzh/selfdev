from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.dispatcher import dispatch_manifest_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch a SelfDev manifest to the selected agent.")
    parser.add_argument("manifest", help="Path to manifest YAML file")
    parser.add_argument(
        "--workspace",
        default="data/agent_workspace",
        help="SelfDev workspace directory",
    )
    args = parser.parse_args()

    result = dispatch_manifest_file(
        manifest_path=Path(args.manifest),
        workspace=Path(args.workspace),
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if result.status == "blocked":
        return 1

    if result.status == "human_required":
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
