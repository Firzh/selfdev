from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.runtime.manifest_validator import validate_manifest_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SelfDev task manifest.")
    parser.add_argument("manifest", help="Path to manifest YAML file")
    args = parser.parse_args()

    result = validate_manifest_file(Path(args.manifest))

    if result.valid:
        print("Manifest valid")
        for warning in result.warnings:
            print(f"WARNING: {warning}")
        return 0

    print("Manifest invalid", file=sys.stderr)
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())