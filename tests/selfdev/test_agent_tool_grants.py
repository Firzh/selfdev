from __future__ import annotations

from pathlib import Path
import yaml

FORBIDDEN_FOR_AGENTS = {
    "run_shell",
    "arbitrary_shell",
    "apply_patch",
    "git_commit",
    "git_push",
    "git_merge",
    "git_rebase",
    "git_reset_hard",
    "deploy",
    "release",
    "restart_service",
    "read_secret",
    "modify_env",
    "delete_file",
}


def load_yaml(path: Path) -> dict:
    assert path.exists(), f"Missing YAML: {path}"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"YAML must be mapping: {path}"
    return data


def collect_tool_ids(tools_config: dict) -> set[str]:
    tools = tools_config.get("tools", {})
    if isinstance(tools, dict):
        return set(tools.keys())
    if isinstance(tools, list):
        return {item["tool_id"] for item in tools if isinstance(item, dict) and "tool_id" in item}
    raise AssertionError("tools.yaml must contain tools as mapping or list")


def test_agent_allowed_tools_exist_in_tool_registry():
    root = Path(__file__).resolve().parents[2]
    agents = load_yaml(root / "config/selfdev/agents.yaml").get("agents", {})
    tool_ids = collect_tool_ids(load_yaml(root / "config/selfdev/tools.yaml"))

    missing_refs: list[str] = []
    for agent_id, agent in agents.items():
        for tool in agent.get("allowed_tools", []):
            if tool not in tool_ids:
                missing_refs.append(f"{agent_id}:{tool}")
    assert not missing_refs, "Allowed tools missing in tools.yaml: " + ", ".join(missing_refs)


def test_forbidden_tools_not_granted_to_normal_agents():
    root = Path(__file__).resolve().parents[2]
    agents = load_yaml(root / "config/selfdev/agents.yaml").get("agents", {})

    offenders = []
    for agent_id, agent in agents.items():
        allowed = set(agent.get("allowed_tools", []))
        forbidden_granted = sorted(allowed & FORBIDDEN_FOR_AGENTS)
        if forbidden_granted:
            offenders.append(f"{agent_id}: {forbidden_granted}")

    assert not offenders, "Forbidden tools granted: " + " | ".join(offenders)


def test_forbidden_tools_are_explicitly_denied_where_relevant():
    root = Path(__file__).resolve().parents[2]
    agents = load_yaml(root / "config/selfdev/agents.yaml").get("agents", {})

    missing_denials = []
    for agent_id, agent in agents.items():
        denied = set(agent.get("denied_tools", []))
        missing = sorted({"git_push", "git_merge", "read_secret", "modify_env"} - denied)
        if missing:
            missing_denials.append(f"{agent_id}: {missing}")

    assert not missing_denials, "Missing baseline denied tools: " + " | ".join(missing_denials)