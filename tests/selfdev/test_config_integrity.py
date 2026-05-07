from __future__ import annotations

from pathlib import Path
import yaml


def load_yaml(path: Path) -> dict:
    assert path.exists(), f"Missing config file: {path}"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"Config must be YAML mapping: {path}"
    return data


def test_required_config_files_exist():
    root = Path(__file__).resolve().parents[2]
    required = [
        "config/selfdev/agents.yaml",
        "config/selfdev/tools.yaml",
        "config/selfdev/routing_rules.yaml",
        "config/selfdev/workflow.yaml",
        "config/selfdev/targets.yaml",
        "config/selfdev/safety_policy.yaml",
    ]
    missing = [f for f in required if not (root / f).exists()]
    assert not missing, "Missing config files: " + ", ".join(missing)


def test_required_agents_exist():
    root = Path(__file__).resolve().parents[2]
    data = load_yaml(root / "config/selfdev/agents.yaml")
    agents = data.get("agents", {})
    assert isinstance(agents, dict), "agents.yaml must contain mapping key: agents"

    required_agents = {
        "siwa",
        "opung",
        "adit",
        "asep",
        "doni",
        "supri",
        "senior_reviewer",
    }
    missing = required_agents - set(agents.keys())
    assert not missing, "Missing required agents: " + ", ".join(sorted(missing))

    for agent_id, agent in agents.items():
        assert "role" in agent, f"Agent {agent_id} missing role"
        assert "model" in agent, f"Agent {agent_id} missing model"
        assert "allowed_tools" in agent, f"Agent {agent_id} missing allowed_tools"
        assert "denied_tools" in agent, f"Agent {agent_id} missing denied_tools"
        assert isinstance(agent["allowed_tools"], list), f"Agent {agent_id} allowed_tools must be list"
        assert isinstance(agent["denied_tools"], list), f"Agent {agent_id} denied_tools must be list"