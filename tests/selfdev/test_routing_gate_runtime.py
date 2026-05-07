from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import yaml

from selfdev.runtime.routing_gate import load_routing_rules, resolve_route


def valid_manifest(task_type: str = "documentation") -> dict:
    return {
        "task_id": "task-001",
        "title": "Valid task",
        "risk_level": "low",
        "mode": "plan",
        "task_type": task_type,
        "target_id": "selfdev",
        "objective": "Create a safe deterministic routing decision.",
        "allowed_paths": ["README.md", "docs/"],
        "denied_paths": [".env", ".env.*", ".git/", "data/secrets/"],
        "required_outputs": ["docs_plan"],
        "required_reviews": ["senior_reviewer"],
        "stop_conditions": ["manifest_invalid"],
        "human_gate_required": False,
    }


def test_load_routing_rules():
    rules = load_routing_rules()
    assert "documentation" in rules
    assert "implementation" in rules


def test_documentation_routes_to_adit():
    rules = load_routing_rules()
    decision = resolve_route(valid_manifest("documentation"), rules)
    assert decision.decision == "route"
    assert decision.primary_agent == "adit"
    assert "senior_reviewer" in decision.required_review


def test_implementation_routes_to_opung():
    rules = load_routing_rules()
    decision = resolve_route(valid_manifest("implementation"), rules)
    assert decision.decision == "route"
    assert decision.primary_agent == "opung"
    assert "senior_reviewer" in decision.required_review


def test_dependency_change_requires_human_review():
    rules = load_routing_rules()
    manifest = valid_manifest("dependency_change")
    manifest["risk_level"] = "high"
    manifest["human_gate_required"] = True
    decision = resolve_route(manifest, rules)
    assert decision.decision == "human_required"
    assert decision.primary_agent == "doni"
    assert decision.requires_human_review is True
    assert "asep" in decision.required_review
    assert "senior_reviewer" in decision.required_review


def test_invalid_manifest_does_not_route():
    rules = load_routing_rules()
    manifest = valid_manifest("documentation")
    manifest.pop("task_id")
    decision = resolve_route(manifest, rules)
    assert decision.decision == "manifest_invalid"
    assert decision.automation_allowed is False


def test_route_manifest_cli_accepts_example_manifest():
    root = Path(__file__).resolve().parents[2]
    manifest = root / "examples" / "manifests" / "task-docs-001.yaml"
    result = subprocess.run(
        [sys.executable, "scripts/selfdev/route_manifest.py", str(manifest)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert '"decision": "route"' in result.stdout
    assert '"primary_agent": "adit"' in result.stdout
