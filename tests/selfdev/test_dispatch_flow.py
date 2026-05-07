from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import yaml

from selfdev.runtime.dispatcher import dispatch_manifest_file


def manifest_data(task_type: str = "documentation") -> dict:
    return {
        "task_id": "task-dispatch-001",
        "title": "Dispatch test task",
        "risk_level": "low",
        "mode": "plan",
        "task_type": task_type,
        "target_id": "selfdev",
        "objective": "Create a safe dispatch message for an agent.",
        "allowed_paths": ["README.md", "docs/"],
        "denied_paths": [".env", ".env.*", ".git/", "data/secrets/"],
        "required_outputs": ["docs_plan"],
        "required_reviews": ["senior_reviewer"],
        "stop_conditions": ["manifest_invalid"],
        "human_gate_required": False,
    }


def write_manifest(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_dispatch_documentation_manifest_creates_message_state_and_kanban(tmp_path: Path):
    manifest = write_manifest(tmp_path, manifest_data("documentation"))
    result = dispatch_manifest_file(manifest, workspace=tmp_path / "workspace")

    assert result.status == "dispatched"
    assert result.target_agent == "adit"
    assert result.message_path is not None
    assert result.state_path is not None

    message_path = Path(result.message_path)
    assert message_path.exists()

    message = json.loads(message_path.read_text(encoding="utf-8"))
    assert message["from_agent"] == "siwa"
    assert message["to_agent"] == "adit"
    assert message["message_type"] == "task_assignment"

    board_path = tmp_path / "workspace" / "kanban" / "board.json"
    board = json.loads(board_path.read_text(encoding="utf-8"))
    assert "task-dispatch-001" in board["tasks"]
    assert board["tasks"]["task-dispatch-001"]["status"] == "in_progress"

    state = json.loads(Path(result.state_path).read_text(encoding="utf-8"))
    assert state["stage"] == "dispatched"
    assert state["current_agent"] == "adit"


def test_dispatch_high_risk_manifest_goes_to_human_required(tmp_path: Path):
    data = manifest_data("dependency_change")
    data["task_id"] = "task-dispatch-risk-001"
    data["risk_level"] = "high"
    data["human_gate_required"] = True
    manifest = write_manifest(tmp_path, data)

    result = dispatch_manifest_file(manifest, workspace=tmp_path / "workspace")

    assert result.status == "human_required"
    assert result.target_agent == "doni"
    assert result.message_path is None

    board_path = tmp_path / "workspace" / "kanban" / "board.json"
    board = json.loads(board_path.read_text(encoding="utf-8"))
    assert board["tasks"]["task-dispatch-risk-001"]["status"] == "human_required"


def test_dispatch_manifest_cli_accepts_example_manifest(tmp_path: Path):
    root = Path(__file__).resolve().parents[2]
    manifest = root / "examples" / "manifests" / "task-docs-001.yaml"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/selfdev/dispatch_manifest.py",
            str(manifest),
            "--workspace",
            str(tmp_path / "workspace"),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"status": "dispatched"' in result.stdout
    assert '"target_agent": "adit"' in result.stdout
