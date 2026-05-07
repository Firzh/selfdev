from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from selfdev.api.http_server import create_server
from selfdev.api.read_api import ReadApi


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve SelfDev read-only local HTTP API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--workspace", default="data/agent_workspace")
    parser.add_argument("--config-dir", default="config/selfdev")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print read-only API health and exit without starting server.",
    )
    args = parser.parse_args()

    if args.check:
        api = ReadApi(
            workspace=Path(args.workspace),
            config_dir=Path(args.config_dir),
        )
        print(json.dumps(api.health(), indent=2, ensure_ascii=False))
        return 0

    server = create_server(
        host=args.host,
        port=args.port,
        workspace=Path(args.workspace),
        config_dir=Path(args.config_dir),
    )

    print(f"SelfDev read-only API listening on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SelfDev read-only API.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
