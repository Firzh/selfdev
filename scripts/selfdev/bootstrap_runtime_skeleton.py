from __future__ import annotations

from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[2]


def write_file(rel_path: str, content: str) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print(f"updated: {rel_path}")


def main() -> int:
    write_file(
        "selfdev/runtime/state_manager.py",
        '''
        """File-based workflow state manager."""

        from __future__ import annotations

        import json
        from pathlib import Path
        from typing import Any


        class StateManager:
            def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
                self.workspace = Path(workspace)
                self.state_dir = self.workspace / "state"
                self.state_dir.mkdir(parents=True, exist_ok=True)

            def state_path(self, task_id: str) -> Path:
                if not task_id:
                    raise ValueError("task_id is required")
                return self.state_dir / f"{task_id}.state.json"

            def write_state(self, task_id: str, state: dict[str, Any]) -> Path:
                if state.get("task_id") != task_id:
                    raise ValueError("state.task_id must match task_id")
                path = self.state_path(task_id)
                path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
                return path

            def read_state(self, task_id: str) -> dict[str, Any]:
                path = self.state_path(task_id)
                if not path.exists():
                    raise FileNotFoundError(f"State file not found: {path}")
                return json.loads(path.read_text(encoding="utf-8"))

            def exists(self, task_id: str) -> bool:
                return self.state_path(task_id).exists()
        ''',
    )

    write_file(
        "selfdev/runtime/message_bus.py",
        '''
        """File-based message bus for agent inbox and outbox."""

        from __future__ import annotations

        import json
        from pathlib import Path
        from typing import Any


        REQUIRED_MESSAGE_FIELDS = {
            "message_id",
            "from_agent",
            "to_agent",
            "task_id",
            "message_type",
        }


        class MessageBus:
            def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
                self.workspace = Path(workspace)
                self.agents_dir = self.workspace / "agents"
                self.agents_dir.mkdir(parents=True, exist_ok=True)

            def _validate_message(self, message: dict[str, Any]) -> None:
                missing = REQUIRED_MESSAGE_FIELDS - set(message)
                if missing:
                    raise ValueError(f"Missing message fields: {sorted(missing)}")

            def inbox_dir(self, agent_id: str) -> Path:
                path = self.agents_dir / agent_id / "inbox"
                path.mkdir(parents=True, exist_ok=True)
                return path

            def outbox_dir(self, agent_id: str) -> Path:
                path = self.agents_dir / agent_id / "outbox"
                path.mkdir(parents=True, exist_ok=True)
                return path

            def send(self, message: dict[str, Any]) -> Path:
                self._validate_message(message)
                target = message["to_agent"]
                message_id = message["message_id"]
                path = self.inbox_dir(target) / f"{message_id}.json"
                path.write_text(json.dumps(message, indent=2, ensure_ascii=False), encoding="utf-8")

                sender = message["from_agent"]
                outbox_path = self.outbox_dir(sender) / f"{message_id}.json"
                outbox_path.write_text(json.dumps(message, indent=2, ensure_ascii=False), encoding="utf-8")
                return path

            def read(self, agent_id: str, message_id: str, box: str = "inbox") -> dict[str, Any]:
                if box not in {"inbox", "outbox"}:
                    raise ValueError("box must be inbox or outbox")
                base = self.inbox_dir(agent_id) if box == "inbox" else self.outbox_dir(agent_id)
                path = base / f"{message_id}.json"
                if not path.exists():
                    raise FileNotFoundError(f"Message not found: {path}")
                return json.loads(path.read_text(encoding="utf-8"))
        ''',
    )

    write_file(
        "selfdev/runtime/kanban.py",
        '''
        """Minimal file-based Kanban board."""

        from __future__ import annotations

        import json
        from pathlib import Path
        from typing import Any


        VALID_STATUSES = {
            "todo",
            "picked",
            "in_progress",
            "blocked",
            "needs_review",
            "needs_revision",
            "ready_for_senior",
            "ready_for_verification",
            "verification_failed",
            "verified",
            "commit_ready",
            "done",
            "rejected",
            "human_required",
        }


        class KanbanBoard:
            def __init__(self, workspace: Path | str = "data/agent_workspace") -> None:
                self.workspace = Path(workspace)
                self.board_dir = self.workspace / "kanban"
                self.board_dir.mkdir(parents=True, exist_ok=True)
                self.board_path = self.board_dir / "board.json"
                if not self.board_path.exists():
                    self._write({"tasks": {}})

            def _read(self) -> dict[str, Any]:
                return json.loads(self.board_path.read_text(encoding="utf-8"))

            def _write(self, data: dict[str, Any]) -> None:
                self.board_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

            def create_task(self, task: dict[str, Any]) -> None:
                task_id = task.get("task_id")
                if not task_id:
                    raise ValueError("task.task_id is required")
                status = task.get("status", "todo")
                if status not in VALID_STATUSES:
                    raise ValueError(f"Invalid status: {status}")

                data = self._read()
                data.setdefault("tasks", {})
                if task_id in data["tasks"]:
                    raise ValueError(f"Task already exists: {task_id}")

                task.setdefault("status", status)
                task.setdefault("artifacts", {})
                task.setdefault("blocked_by", [])
                data["tasks"][task_id] = task
                self._write(data)

            def update_status(self, task_id: str, status: str) -> None:
                if status not in VALID_STATUSES:
                    raise ValueError(f"Invalid status: {status}")

                data = self._read()
                if task_id not in data.get("tasks", {}):
                    raise KeyError(f"Task not found: {task_id}")

                data["tasks"][task_id]["status"] = status
                self._write(data)

            def get_task(self, task_id: str) -> dict[str, Any]:
                data = self._read()
                if task_id not in data.get("tasks", {}):
                    raise KeyError(f"Task not found: {task_id}")
                return data["tasks"][task_id]
        ''',
    )

    write_file(
        "selfdev/tools/safety_gate.py",
        '''
        """Deterministic Safety Gate.

        This module does not execute actions. It only classifies whether a proposed
        action or changed path is safe under local policy.
        """

        from __future__ import annotations

        from dataclasses import dataclass, field
        from pathlib import PurePosixPath


        DEFAULT_DENIED_ACTIONS = {
            "run_shell",
            "arbitrary_shell",
            "git_push",
            "git_merge",
            "git_rebase",
            "git_reset_hard",
            "modify_env",
            "read_secret",
            "delete_file",
            "deploy",
            "release",
        }

        DEFAULT_DENIED_PATHS = {
            ".env",
            ".git/",
            "data/secrets/",
        }


        @dataclass
        class SafetyResult:
            status: str
            reasons: list[str] = field(default_factory=list)

            @property
            def passed(self) -> bool:
                return self.status == "PASS"


        def normalize_path(path: str) -> str:
            return str(PurePosixPath(path.replace("\\\\", "/")))


        def check_action(action: str, denied_actions: set[str] | None = None) -> SafetyResult:
            denied = denied_actions or DEFAULT_DENIED_ACTIONS
            if action in denied:
                return SafetyResult(status="BLOCK", reasons=[f"Denied action: {action}"])
            return SafetyResult(status="PASS", reasons=[])


        def check_paths(paths: list[str], denied_paths: set[str] | None = None) -> SafetyResult:
            denied = denied_paths or DEFAULT_DENIED_PATHS
            reasons: list[str] = []

            for raw_path in paths:
                path = normalize_path(raw_path)
                for denied_path in denied:
                    denied_norm = normalize_path(denied_path)
                    if path == denied_norm.rstrip("/") or path.startswith(denied_norm):
                        reasons.append(f"Denied path touched: {raw_path}")

            if reasons:
                return SafetyResult(status="BLOCK", reasons=reasons)
            return SafetyResult(status="PASS", reasons=[])
        ''',
    )

    write_file(
        "selfdev/tools/verification_engine.py",
        '''
        """Minimal deterministic verification engine."""

        from __future__ import annotations

        from dataclasses import dataclass, field
        from pathlib import Path


        @dataclass
        class VerificationResult:
            status: str
            checks: dict[str, str] = field(default_factory=dict)
            notes: list[str] = field(default_factory=list)

            @property
            def passed(self) -> bool:
                return self.status == "PASS"


        def verify_required_files(paths: list[str]) -> VerificationResult:
            checks: dict[str, str] = {}
            notes: list[str] = []

            for raw_path in paths:
                path = Path(raw_path)
                if path.exists():
                    checks[raw_path] = "PASS"
                else:
                    checks[raw_path] = "FAIL"
                    notes.append(f"Missing required file: {raw_path}")

            status = "PASS" if all(result == "PASS" for result in checks.values()) else "FAIL"
            return VerificationResult(status=status, checks=checks, notes=notes)
        ''',
    )

    write_file(
        "selfdev/tools/runner.py",
        '''
        """Controlled Runner skeleton.

        Runner is intentionally non-executing in this phase.
        """

        from __future__ import annotations

        from dataclasses import dataclass, field


        DENIED_RUNNER_ACTIONS = {
            "git_push",
            "git_merge",
            "terraform_apply",
            "terraform_destroy",
            "kubectl_apply_real_cluster",
            "kubectl_delete",
            "restart_service",
            "modify_env",
            "read_secret",
            "rm_rf",
        }


        @dataclass
        class RunnerResult:
            status: str
            action: str
            notes: list[str] = field(default_factory=list)


        def validate_runner_request(action: str) -> RunnerResult:
            if action in DENIED_RUNNER_ACTIONS:
                return RunnerResult(status="BLOCKED", action=action, notes=[f"Denied runner action: {action}"])
            return RunnerResult(status="ACCEPTED", action=action, notes=["Request accepted for later implementation."])
        ''',
    )

    write_file(
        "selfdev/tools/commit_gate.py",
        '''
        """Commit Gate skeleton.

        Commit Gate only evaluates readiness. It does not commit in this phase.
        """

        from __future__ import annotations

        from dataclasses import dataclass, field


        @dataclass
        class CommitReadiness:
            status: str
            missing: list[str] = field(default_factory=list)

            @property
            def ready(self) -> bool:
                return self.status == "READY"


        def evaluate_commit_readiness(requirements: dict[str, bool]) -> CommitReadiness:
            missing = [name for name, ok in requirements.items() if not ok]
            if missing:
                return CommitReadiness(status="BLOCKED", missing=missing)
            return CommitReadiness(status="READY", missing=[])
        ''',
    )

    write_file(
        "tests/selfdev/test_runtime_skeleton.py",
        '''
        from __future__ import annotations

        from pathlib import Path

        from selfdev.runtime.state_manager import StateManager
        from selfdev.runtime.message_bus import MessageBus
        from selfdev.runtime.kanban import KanbanBoard
        from selfdev.tools.safety_gate import check_action, check_paths
        from selfdev.tools.verification_engine import verify_required_files
        from selfdev.tools.runner import validate_runner_request
        from selfdev.tools.commit_gate import evaluate_commit_readiness


        def test_state_manager_write_and_read(tmp_path: Path):
            manager = StateManager(tmp_path)
            manager.write_state("task-001", {"task_id": "task-001", "status": "in_progress"})
            state = manager.read_state("task-001")
            assert state["task_id"] == "task-001"
            assert state["status"] == "in_progress"


        def test_message_bus_send_and_read(tmp_path: Path):
            bus = MessageBus(tmp_path)
            bus.send({
                "message_id": "msg-001",
                "from_agent": "siwa",
                "to_agent": "adit",
                "task_id": "task-001",
                "message_type": "task_assignment",
            })
            message = bus.read("adit", "msg-001")
            assert message["from_agent"] == "siwa"
            assert message["to_agent"] == "adit"


        def test_kanban_create_and_update(tmp_path: Path):
            board = KanbanBoard(tmp_path)
            board.create_task({
                "task_id": "task-001",
                "title": "Test task",
                "status": "todo",
            })
            board.update_status("task-001", "in_progress")
            task = board.get_task("task-001")
            assert task["status"] == "in_progress"


        def test_safety_gate_blocks_denied_action():
            result = check_action("git_push")
            assert result.status == "BLOCK"


        def test_safety_gate_blocks_denied_path():
            result = check_paths([".env"])
            assert result.status == "BLOCK"


        def test_verification_engine_checks_required_files(tmp_path: Path):
            existing = tmp_path / "ok.txt"
            existing.write_text("ok", encoding="utf-8")
            result = verify_required_files([str(existing), str(tmp_path / "missing.txt")])
            assert result.status == "FAIL"
            assert result.checks[str(existing)] == "PASS"


        def test_runner_blocks_denied_action():
            result = validate_runner_request("terraform_destroy")
            assert result.status == "BLOCKED"


        def test_commit_gate_requires_all_requirements():
            result = evaluate_commit_readiness({
                "senior_review": True,
                "safety_gate": True,
                "verification": False,
            })
            assert result.status == "BLOCKED"
            assert "verification" in result.missing
        ''',
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())