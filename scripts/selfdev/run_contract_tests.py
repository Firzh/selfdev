from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    tests_dir = repo_root / "tests" / "selfdev"
    if not tests_dir.exists():
        print(f"Missing tests directory: {tests_dir}", file=sys.stderr)
        return 2

    cmd = [sys.executable, "-m", "pytest", str(tests_dir), "-q"]
    return subprocess.call(cmd, cwd=repo_root)


if __name__ == "__main__":
    raise SystemExit(main())