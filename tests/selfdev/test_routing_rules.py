from __future__ import annotations

from pathlib import Path
import yaml


def load_yaml(path: Path) -> dict:
    assert path.exists(), f"Missing YAML: {path}"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"YAML must be mapping: {path}"
    return data


def test_routing_references_existing_agents():
    root = Path(__file__).resolve().parents[2]
    agents = set(load_yaml(root / "config/selfdev/agents.yaml").get("agents", {}).keys())
    routes = load_yaml(root / "config/selfdev/routing_rules.yaml").get("routing_rules", {})
    assert routes, "routing_rules.yaml must define routing_rules"

    invalid = []
    for task_type, rule in routes.items():
        primary = rule.get("primary")
        if primary not in agents and primary != "human_owner":
            invalid.append(f"{task_type}.primary={primary}")
        for reviewer in rule.get("required_review", []):
            if reviewer not in agents and reviewer != "human_owner":
                invalid.append(f"{task_type}.required_review={reviewer}")

    assert not invalid, "Routing references unknown agents: " + ", ".join(invalid)


def test_high_risk_routes_require_human_review():
    root = Path(__file__).resolve().parents[2]
    routes = load_yaml(root / "config/selfdev/routing_rules.yaml").get("routing_rules", {})

    high_risk_like = ["high_risk", "critical", "dependency_change", "tool_registry_change", "agent_permission_change"]
    missing = []
    for key in high_risk_like:
        rule = routes.get(key)
        if rule and not rule.get("requires_human_review", False):
            missing.append(key)
    assert not missing, "High-risk routes missing human review: " + ", ".join(missing)


def test_implementation_route_uses_opung_and_senior_reviewer():
    root = Path(__file__).resolve().parents[2]
    routes = load_yaml(root / "config/selfdev/routing_rules.yaml").get("routing_rules", {})
    implementation = routes.get("implementation")
    assert implementation, "Missing implementation route"
    assert implementation.get("primary") == "opung"
    assert "senior_reviewer" in implementation.get("required_review", [])