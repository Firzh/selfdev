from __future__ import annotations

from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[2]


def write_file(rel_path: str, content: str) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print(f"created: {rel_path}")


def touch(rel_path: str) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text('"""SelfDev placeholder module."""\n', encoding="utf-8")
    print(f"created: {rel_path}")


def main() -> int:
    write_file(
        "config/selfdev/tools.yaml",
        """
        tools:
          read_file: {category: read, risk: low}
          list_files: {category: read, risk: low}
          git_diff: {category: read, risk: low}
          read_artifact: {category: read, risk: low}
          write_artifact: {category: write_artifact, risk: low}
          write_doc_plan: {category: write_artifact, risk: low}
          write_docs_patch: {category: write_artifact, risk: medium}
          write_doc_gap_report: {category: write_artifact, risk: low}
          write_security_review: {category: write_artifact, risk: medium}
          write_devops_review: {category: write_artifact, risk: medium}
          write_runtime_review: {category: write_artifact, risk: medium}
          write_senior_review: {category: write_artifact, risk: medium}
          write_implementation_plan: {category: write_artifact, risk: medium}
          write_draft_patch: {category: write_artifact, risk: medium}
          write_validation_request: {category: request, risk: medium}
          request_runner_validation: {category: request, risk: medium}
          request_dependency_audit: {category: request, risk: medium}
          request_read_only_check: {category: request, risk: medium}
          request_specialist_review: {category: request, risk: medium}
          kanban_create_task: {category: orchestration, risk: low}
          kanban_update_status: {category: orchestration, risk: low}
          kanban_attach_artifact: {category: orchestration, risk: low}
          message_send: {category: orchestration, risk: low}
          message_read_reply: {category: orchestration, risk: low}
          agent_registry_lookup: {category: orchestration, risk: low}
          tool_registry_lookup: {category: orchestration, risk: low}
          workflow_state_read: {category: orchestration, risk: low}
          workflow_state_write: {category: orchestration, risk: low}
          human_escalation_request: {category: request, risk: high}
        """,
    )

    baseline_denied = [
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
    ]

    denied_yaml = "\n".join([f"      - {item}" for item in baseline_denied])

    write_file(
        "config/selfdev/agents.yaml",
        f"""
        agents:
          siwa:
            role: orchestrator
            model: siwa:latest
            allowed_tools:
              - kanban_create_task
              - kanban_update_status
              - kanban_attach_artifact
              - message_send
              - message_read_reply
              - agent_registry_lookup
              - tool_registry_lookup
              - workflow_state_read
              - workflow_state_write
              - human_escalation_request
            denied_tools:
        {denied_yaml}

          opung:
            role: scoped_coding_implementer
            model: opung:latest
            allowed_tools:
              - read_file
              - list_files
              - git_diff
              - write_implementation_plan
              - write_draft_patch
              - write_validation_request
            denied_tools:
        {denied_yaml}

          adit:
            role: documentation_agent
            model: adit:latest
            allowed_tools:
              - read_file
              - list_files
              - git_diff
              - write_doc_plan
              - write_docs_patch
              - write_doc_gap_report
              - write_validation_request
            denied_tools:
        {denied_yaml}

          asep:
            role: defensive_security_reviewer
            model: asep:latest
            allowed_tools:
              - read_file
              - list_files
              - git_diff
              - write_security_review
              - request_dependency_audit
              - request_runner_validation
            denied_tools:
        {denied_yaml}

          doni:
            role: devops_reviewer
            model: doni:latest
            allowed_tools:
              - read_file
              - list_files
              - git_diff
              - write_devops_review
              - write_validation_request
              - request_runner_validation
            denied_tools:
        {denied_yaml}

          supri:
            role: read_only_sysadmin_analyst
            model: supri:latest
            allowed_tools:
              - read_file
              - list_files
              - read_artifact
              - write_runtime_review
              - request_read_only_check
            denied_tools:
        {denied_yaml}

          senior_reviewer:
            role: final_reviewer
            model: senior_reviewer:latest
            allowed_tools:
              - read_file
              - list_files
              - git_diff
              - read_artifact
              - write_senior_review
              - request_specialist_review
              - write_validation_request
            denied_tools:
        {denied_yaml}
        """,
    )

    write_file(
        "config/selfdev/routing_rules.yaml",
        """
        routing_rules:
          documentation:
            primary: adit
            required_review:
              - senior_reviewer

          implementation:
            primary: opung
            required_review:
              - senior_reviewer

          implementation_with_security_risk:
            primary: opung
            required_review:
              - asep
              - senior_reviewer

          security_review:
            primary: asep
            required_review:
              - senior_reviewer

          devops_review:
            primary: doni
            required_review:
              - senior_reviewer

          runtime_issue:
            primary: supri
            required_review:
              - doni
              - senior_reviewer

          dependency_change:
            primary: doni
            required_review:
              - asep
              - senior_reviewer
            requires_human_review: true

          tool_registry_change:
            primary: asep
            required_review:
              - doni
              - senior_reviewer
            requires_human_review: true

          agent_permission_change:
            primary: asep
            required_review:
              - senior_reviewer
            requires_human_review: true

          high_risk:
            primary: siwa
            required_review:
              - asep
              - doni
              - senior_reviewer
            requires_human_review: true

          critical:
            primary: human_owner
            required_review: []
            requires_human_review: true
            automation_allowed: false
        """,
    )

    write_file(
        "config/selfdev/workflow.yaml",
        """
        workflow:
          name: selfdev_local_multi_agent
          mode: sequential_first
          stages:
            - load_manifest
            - validate_manifest
            - classify_risk
            - route_agent
            - dispatch_message
            - collect_artifact
            - review_artifact
            - safety_gate
            - runner
            - verification_engine
            - commit_gate

          limits:
            max_dispatch_rounds: 3
            max_revision_rounds: 2
            max_agent_wait_seconds: 300
        """,
    )

    write_file(
        "config/selfdev/targets.yaml",
        """
        targets:
          selfdev:
            name: SelfDev
            type: local_system
            root_path: .
            allowed_paths:
              - docs/
              - config/
              - schemas/
              - selfdev/
              - scripts/
              - tests/
            denied_paths:
              - .env
              - .env.*
              - .git/
              - data/secrets/
        """,
    )

    write_file(
        "config/selfdev/safety_policy.yaml",
        """
        safety_policy:
          denied_paths:
            - .env
            - .env.*
            - .git/
            - data/secrets/

          denied_actions:
            - run_shell
            - arbitrary_shell
            - git_push
            - git_merge
            - git_rebase
            - git_reset_hard
            - modify_env
            - read_secret
            - delete_file
            - deploy
            - release

          human_required:
            - dependency_change
            - tool_registry_change
            - agent_permission_change
            - security_policy_change
            - architecture_change
            - commit_policy_change
        """,
    )

    modules = [
        "selfdev/tools/safety_gate.py",
        "selfdev/tools/verification_engine.py",
        "selfdev/tools/runner.py",
        "selfdev/tools/commit_gate.py",
        "selfdev/runtime/state_manager.py",
        "selfdev/runtime/message_bus.py",
        "selfdev/runtime/kanban.py",
    ]

    for rel in modules:
        touch(rel)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())