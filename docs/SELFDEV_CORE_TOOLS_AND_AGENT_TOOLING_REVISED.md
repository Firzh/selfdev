# SelfDev Core Tools and Agent Tooling

**Document status:** Revised tooling design  
**Document type:** Core tool catalogue and agent tool grant specification  
**Version:** v0.2  
**Date:** 2026-05-07  
**System:** SelfDev  
**Position:** Standalone system tooling, not limited to AI RAG Local  

---

## 1. Purpose

This document defines the revised core tools and agent tooling for SelfDev.

The purpose is to:

```text
separate agent-facing tools from execution tools
apply least privilege per agent
make request-only validation explicit
prevent tool overgranting
protect secrets and denied paths
support multiple target systems
standardize artifact paths
support Safety Gate, Runner, Verification Engine, and Commit Gate
```

SelfDev is now a standalone system. These tools are not specific to AI RAG Local. AI RAG Local is one managed target system.

---

## 2. Tool Categories

| Category | Function | Agent access |
|---|---|---|
| Read tools | Read manifest, scoped files, diffs, artifacts, reports, registry entries | Allowed by scope |
| Write artifact tools | Write structured plans, reviews, patches, reports, requests | Allowed by role |
| Orchestration tools | Kanban, message bus, routing, state, artifact summary | Siwa and runtime only |
| Knowledge retrieval tools | Retrieve agent-specific references | Allowed by knowledge routing |
| Request-only tools | Request checks, scans, builds, tests, dry runs | Allowed, but not executed by agent |
| Execution tools | Apply patch, run test, build, lint, dry-run commands | Runner only |
| Verification tools | Schema checks, tests, lint result parsing, policy checks | Verification Engine only |
| Safety tools | Denied path, secret, unsafe command, permission and policy checks | Safety Gate only |
| Commit tools | Local commit only after all gates pass | Commit Gate only |

---

## 3. Global Tool Rules

```text
Agents may read only scoped inputs.
Agents may write only role-specific artifacts.
Agents may request validation, but may not execute validation.
Agents may not run shell.
Agents may not apply patch.
Agents may not commit.
Agents may not push.
Agents may not deploy.
Agents may not modify .env.
Agents may not read secrets.
Execution must pass through Runner.
Verification must pass through Verification Engine.
Policy enforcement must pass through Safety Gate.
Local commit must pass through Commit Gate.
Push, merge, release, and production deployment remain Human Owner actions.
```

---

## 4. Core Tool 1: Runner

### 4.1 Definition

Runner is the controlled deterministic executor.

Runner does not reason. Runner executes approved requests that already passed policy.

### 4.2 Position

```text
Senior Reviewer approval
  ↓
Safety Gate PASS
  ↓
Runner executes approved action
  ↓
Verification Engine validates result
```

### 4.3 Allowed Runner Actions

```yaml
runner_allowed_actions:
  patch:
    - git_apply_check
    - git_apply_final_patch

  python:
    - python_compile_check
    - python_import_check
    - pytest

  docs:
    - markdownlint
    - vale_check
    - link_check
    - mkdocs_build
    - openapi_validate
    - asyncapi_validate

  devops_safe:
    - yaml_validate
    - github_actions_lint
    - dockerfile_lint
    - docker_compose_config
    - terraform_validate
    - terraform_plan_with_human_approval
    - helm_template
    - kubectl_dry_run_client
    - ansible_syntax_check
    - grafana_json_validate
    - prometheus_rule_check

  security_safe:
    - nvd_lookup
    - kev_lookup
    - dependency_audit
    - zap_baseline_with_authorized_scope
    - nuclei_template_check_with_whitelist

  runtime_read_only:
    - systemctl_status
    - journalctl_tail_scoped
    - df_h
    - du_sh_allowed_path
    - free_m
    - uptime
    - ps_aux
    - ss_tulpn
    - nginx_t
    - apachectl_configtest
    - sshd_t
```

### 4.4 Denied Runner Actions

```yaml
runner_denied_actions:
  git:
    - git_push
    - git_merge
    - git_rebase
    - git_reset_hard
    - git_clean_fd
    - git_checkout_main
    - git_checkout_master
    - git_tag
    - git_release

  destructive:
    - rm_rf
    - delete_mass_files
    - wipe_data
    - modify_env
    - read_secret

  infrastructure:
    - terraform_apply
    - terraform_destroy
    - kubectl_apply_real_cluster
    - kubectl_delete
    - helm_install_real_cluster
    - helm_upgrade_real_cluster
    - ansible_playbook_real_server
    - docker_compose_up_production
    - restart_service
    - stop_service
    - kill_process
    - deploy_to_cloud

  identity_and_access:
    - useradd
    - userdel
    - usermod
    - passwd
    - visudo_edit
    - chmod_sensitive
    - chown_sensitive

  offensive_security:
    - exploit_execution
    - payload_generation
    - brute_force
    - reverse_shell
    - credential_theft
    - active_external_scan_without_roe
```

### 4.5 Runner Input Contract

```yaml
task_id:
target_system:
requested_by:
request_type:
manifest:
allowed_paths:
denied_paths:
requires:
  - senior_approval
  - safety_pass
```

### 4.6 Runner Output Contract

Path:

```text
workspace/agent_workspace/runner/{task_id}.runner_report.md
```

Template:

```md
# Runner Report

## Task ID

## Target System

## Request Type

## Requested By

## Action

## Allowed Scope

## Result
PASS | FAIL | BLOCKED

## stdout

## stderr

## Files Changed

## Duration

## Notes
```

---

## 5. Core Tool 2: Verification Engine

### 5.1 Definition

Verification Engine validates results. It does not fix or edit.

### 5.2 Verification Checks

```yaml
verification_checks:
  repository:
    - branch_policy_check
    - git_status_check
    - changed_files_check
    - diff_limit_check
    - denied_path_check

  security:
    - secret_pattern_check
    - unsafe_command_check
    - agent_permission_check
    - dependency_risk_check
    - network_scan_policy_check

  code:
    - python_compile_check
    - python_import_check
    - unit_tests
    - integration_tests_if_manifest_allows
    - coverage_report_if_requested

  documentation:
    - markdown_structure_check
    - required_docs_section_check
    - changelog_check
    - readme_check
    - adr_check
    - openapi_validation
    - asyncapi_validation
    - link_check
    - vale_check_optional

  devops:
    - yaml_validation
    - github_actions_policy_check
    - dockerfile_policy_check
    - compose_config_check
    - kubernetes_dry_run_client
    - helm_template_check
    - terraform_validate
    - ansible_syntax_check
    - grafana_json_check
    - prometheus_rule_check

  runtime:
    - redaction_check
    - read_only_command_check
    - service_status_output_check
    - incident_report_schema_check
```

### 5.3 Verification Output Contract

Path:

```text
workspace/agent_workspace/verification/{task_id}.verification.md
```

Template:

```md
# Verification Report

## Task ID

## Target System

## Summary
PASS | FAIL | BLOCKED

## Checks

| Check | Result | Blocking | Notes |
|---|---|---:|---|

## Changed Files

## Failed Checks

## Required Fixes

## Final Decision
allow_commit | request_revision | abort
```

### 5.4 Verification Failure Rules

Verification Engine must fail if:

```text
task_id missing
changed files unknown
denied path changed
secret detected
blocking test failed
schema validation failed
Safety Gate BLOCK exists
Runner failed
required check missing
```

---

## 6. Core Tool 3: Safety Gate

### 6.1 Definition

Safety Gate is the deterministic policy enforcement layer.

It blocks unsafe patches, requests, commands, tool changes, and commit requests before execution.

### 6.2 Safety Gate Checks

```yaml
safety_checks:
  path:
    - denied_path_check
    - allowed_path_check
    - scope_drift_check

  secret:
    - secret_pattern_check
    - env_access_check
    - private_key_check
    - credential_file_check

  command:
    - unsafe_command_check
    - destructive_command_check
    - runtime_mutation_check
    - deployment_command_check

  policy:
    - agent_permission_escalation_check
    - tool_registry_change_check
    - safety_policy_weakening_check
    - commit_policy_weakening_check
    - senior_review_bypass_check

  patch:
    - oversized_diff_check
    - dependency_change_check
    - architecture_change_check
    - public_api_change_check

  security:
    - unapproved_network_scan_check
    - offensive_payload_check
    - exploit_instruction_check
    - credential_theft_check
```

### 6.3 Safety Severity

| Level | Meaning | Action |
|---|---|---|
| LOW | Minor issue | Log |
| MEDIUM | Possible scope drift | Require review |
| HIGH | Repository or runtime risk | Block |
| CRITICAL | Secret, destructive command, push, production risk | Block and human escalation |

### 6.4 Safety Gate Output Contract

Path:

```text
workspace/agent_workspace/safety/{task_id}.safety_report.md
```

Template:

```md
# Safety Gate Report

## Task ID

## Target System

## Summary
PASS | WARN | BLOCK

## Risk Level
LOW | MEDIUM | HIGH | CRITICAL

## Checks

| Check | Result | Notes |
|---|---|---|

## Blocked Items

## Required Action

## Human Escalation Required
yes/no
```

---

## 7. Core Tool 4: Commit Gate

### 7.1 Definition

Commit Gate creates local commit only after all required gates pass.

Commit Gate is not an agent.

Commit Gate must never push.

### 7.2 Commit Gate Requirements

```text
manifest allows local commit
Senior approval exists
Safety Gate PASS
Verification Engine PASS
denied path check PASS
secret check PASS
branch policy PASS
diff limit PASS
commit_request.yaml exists
commit message valid
allow_push is false
```

### 7.3 Commit Request Input

Path:

```text
workspace/agent_workspace/approvals/{task_id}.commit_request.yaml
```

Template:

```yaml
task_id:
target_system:
decision: request_local_commit
approved_by: senior_reviewer
manifest:
final_patch:
safety_report:
verification_report:
commit_message:
allow_local_commit: true
allow_push: false
```

### 7.4 Commit Gate Output Contract

Path:

```text
workspace/agent_workspace/commits/{task_id}.commit_record.md
```

Template:

```md
# Commit Record

## Task ID

## Target System

## Result
COMMITTED | BLOCKED | FAILED

## Commit Hash

## Commit Message

## Branch

## Changed Files

## Safety Report

## Verification Report

## Senior Approval

## Notes
```

---

## 8. Governance Tools

### 8.1 Agent Registry

```yaml
agent_registry_tools:
  allow:
    - agent_registry_lookup
    - agent_capability_lookup
    - agent_status_lookup
  deny:
    - modify_agent_permissions_without_human
    - create_agent_without_human
    - delete_agent_without_human
```

### 8.2 Tool Registry

```yaml
tool_registry_tools:
  allow:
    - tool_registry_lookup
    - tool_capability_lookup
    - tool_risk_lookup
  deny:
    - grant_tool_without_human
    - remove_safety_gate
    - weaken_tool_policy
```

### 8.3 Target System Registry

```yaml
target_registry_tools:
  allow:
    - target_system_lookup
    - target_policy_lookup
    - target_allowed_paths_lookup
    - target_denied_paths_lookup
  deny:
    - modify_target_registry_without_human
    - weaken_target_policy
```

### 8.4 Human Gate

```yaml
human_gate_tools:
  allow:
    - write_human_review_request
    - record_human_decision
    - block_until_human_decision
  deny:
    - approve_on_behalf_of_human
    - bypass_human_decision
```

---

## 9. Siwa Miwa Tool Grant

Role:

```text
orchestrator, planner, router, dispatcher, evaluator, human-gate manager
```

Allowed tools:

```yaml
siwa_tools:
  allow:
    - read_manifest
    - validate_manifest_schema
    - target_system_lookup
    - kanban_create_task
    - kanban_split_task
    - kanban_assign_task
    - kanban_update_status
    - kanban_attach_artifact
    - kanban_block_task
    - kanban_close_task
    - message_send
    - message_read_reply
    - agent_registry_lookup
    - tool_registry_lookup
    - workflow_state_read
    - workflow_state_write
    - artifact_index_read
    - artifact_summary_write
    - human_escalation_request
    - retrieve_orchestration_pattern
```

Denied tools:

```yaml
siwa_tools:
  deny:
    - read_env
    - read_secret
    - arbitrary_shell
    - write_patch
    - apply_patch
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - git_reset
    - delete_file
    - modify_source_file
    - modify_agent_permissions_without_human
```

Request-only tools:

```yaml
siwa_request_tools:
  allow:
    - request_specialist_review
    - request_human_review
    - request_artifact_validation
```

Failure-first rule:

```text
Siwa may route and coordinate.
Siwa must not execute source changes.
Unknown routing must become human_required.
```

---

## 10. Opung Tool Grant

Role:

```text
scoped coding implementer, small patch drafter, unit test drafter
```

Allowed tools:

```yaml
opung_tools:
  allow:
    - read_manifest
    - read_file
    - list_files
    - git_diff
    - retrieve_coding_reference
    - retrieve_official_language_docs
    - retrieve_standard_library_docs
    - retrieve_unit_testing_pattern
    - retrieve_error_message_reference
    - retrieve_same_repo_context
    - write_implementation_plan
    - write_draft_patch
    - write_test_draft_patch
    - write_patch_notes
    - write_scope_request
    - write_stop_request
```

Denied tools:

```yaml
opung_tools:
  deny:
    - apply_patch
    - run_shell
    - run_tests
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - docker_build
    - docker_compose_up
    - terraform_apply
    - kubectl_apply
```

Request-only tools:

```yaml
opung_request_tools:
  allow:
    - request_runner_test
    - request_import_check
    - request_unit_test_run
    - request_scope_expansion
    - request_senior_review
    - request_asep_review
    - request_doni_review
```

Failure-first rule:

```text
Opung writes draft patches only.
Opung cannot apply patches or run tests.
Dependency change stops Opung and routes to Doni plus Asep if needed.
```

---

## 11. Adit Tool Grant

Role:

```text
documentation architect, documentation maintainer, API documentation assistant, runbook writer
```

Allowed tools:

```yaml
adit_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - write_doc_plan
    - write_docs_patch
    - write_changelog_patch
    - write_readme_patch
    - write_doc_gap_report
    - write_style_review
    - retrieve_doc_pattern
    - classify_doc_diataxis
    - propose_docs_validation
```

Denied tools:

```yaml
adit_tools:
  deny:
    - modify_source_code
    - apply_patch
    - run_shell
    - npm_install
    - npm_run_build
    - mkdocs_build
    - mkdocs_gh_deploy
    - docusaurus_build
    - redocly_build
    - runbook_run
    - git_commit
    - git_push
    - delete_file
    - modify_env
    - publish_docs
```

Request-only tools:

```yaml
adit_request_tools:
  allow:
    - request_docs_build
    - request_openapi_validate
    - request_asyncapi_validate
    - request_vale_check
    - request_markdownlint
    - request_link_check
```

Failure-first rule:

```text
Adit writes docs artifacts only.
Adit must not build or deploy docs.
Adit must not document behavior without evidence.
```

---

## 12. Asep Tool Grant

Role:

```text
defensive security reviewer and vulnerability intelligence analyst
```

Allowed tools:

```yaml
asep_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - retrieve_security_reference
    - retrieve_owasp_wstg
    - retrieve_owasp_asvs
    - retrieve_owasp_api_top10
    - retrieve_owasp_cheatsheet
    - retrieve_cwe
    - retrieve_capec
    - retrieve_attack_context
    - request_nvd_lookup
    - request_kev_lookup
    - request_dependency_audit
    - request_zap_plan_validation
    - request_nuclei_template_validation
    - write_security_review
    - write_security_test_case
    - write_vulnerability_report
    - write_validation_request
```

Denied tools:

```yaml
asep_tools:
  deny:
    - apply_patch
    - write_source_code
    - run_shell
    - run_zap_scan
    - run_nuclei_scan
    - exploit_execution
    - payload_generation
    - reverse_shell_generation
    - credential_theft_instruction
    - persistence_instruction
    - lateral_movement_instruction
    - network_attack
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - modify_env
```

Request-only tools:

```yaml
asep_runner_requests:
  nvd_lookup:
    executor: verification_engine
    cache_required: true
    rate_limit_required: true

  kev_lookup:
    executor: verification_engine
    cache_required: true

  dependency_audit:
    executor: verification_engine

  zap_baseline:
    executor: runner
    requires:
      - authorized_scope
      - local_or_staging_target
      - human_approval_if_active_scan

  nuclei_template_check:
    executor: runner
    requires:
      - whitelist_template
      - authorized_scope
      - human_approval_if_external_target
```

Failure-first rule:

```text
Asep writes defensive review only.
Asep does not execute scanner.
Scanner validation must go through Runner and scope approval.
```

---

## 13. Doni Tool Grant

Role:

```text
DevOps, CI/CD, IaC, deployment, observability, and runtime reviewer
```

Allowed tools:

```yaml
doni_tools:
  allow:
    - read_file
    - list_files
    - git_diff
    - retrieve_devops_reference
    - inspect_workflow_yaml
    - inspect_dockerfile
    - inspect_compose_yaml
    - inspect_kubernetes_yaml
    - inspect_helm_chart
    - inspect_terraform_files
    - inspect_ansible_playbook
    - inspect_grafana_dashboard
    - inspect_prometheus_rules
    - inspect_runbook
    - write_devops_review
    - write_validation_request
```

Denied tools:

```yaml
doni_tools:
  deny:
    - run_shell
    - docker_build
    - docker_compose_up
    - kubectl_apply
    - kubectl_delete
    - helm_install
    - helm_upgrade
    - terraform_apply
    - terraform_destroy
    - ansible_playbook
    - restart_service
    - deploy_to_cloud
    - modify_env
    - git_commit
    - git_push
    - delete_file
```

Request-only tools:

```yaml
doni_runner_requests:
  github_actions_lint:
    executor: verification_engine

  yaml_validation:
    executor: verification_engine

  dockerfile_lint:
    executor: verification_engine

  compose_config_check:
    executor: runner
    requires_human_if_network_exposed: true

  kubernetes_dry_run:
    executor: runner
    cluster_required: false
    mode: client_dry_run

  helm_template:
    executor: runner
    no_cluster_required: true

  terraform_validate:
    executor: runner

  terraform_plan:
    executor: runner
    requires_human_approval: true

  ansible_syntax_check:
    executor: runner

  grafana_json_validate:
    executor: verification_engine

  prometheus_rule_check:
    executor: verification_engine
```

Failure-first rule:

```text
Doni reviews DevOps risk.
Doni does not deploy or apply infrastructure.
Terraform plan requires human approval when tied to real environment.
```

---

## 14. Supri Tool Grant

Role:

```text
read-only local sysadmin analyst, runtime status analyst, log triage assistant, incident classifier, SOP writer
```

Allowed tools:

```yaml
supri_tools:
  allow:
    - read_manifest
    - read_runner_report
    - read_verification_report
    - read_safety_report
    - read_error_report
    - read_log_excerpt
    - read_service_status_snapshot
    - read_resource_snapshot
    - read_incident_ticket
    - retrieve_sysadmin_reference
    - retrieve_linux_man_page
    - retrieve_tldr_page
    - retrieve_systemd_reference
    - retrieve_nginx_reference
    - retrieve_apache_reference
    - retrieve_ssh_hardening_reference
    - retrieve_cis_reference
    - retrieve_scap_reference
    - write_runtime_summary
    - write_incident_classification
    - write_troubleshooting_checklist
    - write_backup_restore_sop
    - write_user_management_sop
    - write_hardening_checklist
    - write_read_only_request
    - write_stop_request
```

Denied tools:

```yaml
supri_tools:
  deny:
    - run_shell
    - restart_service
    - stop_service
    - kill_process
    - delete_file
    - edit_config
    - modify_env
    - read_secret
    - create_user
    - delete_user
    - change_password
    - edit_sudoers
    - install_package
    - run_ansible_playbook
    - run_openscap_remediation
    - apply_cis_hardening
    - reload_nginx
    - restart_apache
    - restart_sshd
    - terraform_apply
    - kubectl_apply
    - docker_compose_up
    - docker_compose_down
    - git_commit
    - git_push
```

Request-only tools:

```yaml
supri_request_tools:
  allow:
    - request_service_status_check
    - request_journalctl_tail
    - request_disk_usage_check
    - request_memory_check
    - request_process_snapshot
    - request_network_socket_snapshot
    - request_nginx_configtest
    - request_apache_configtest
    - request_sshd_configtest
    - request_log_redaction_check
```

Allowed read-only command examples through Runner:

```text
systemctl status <service>
journalctl -u <service> --no-pager -n 200
df -h
du -sh <allowed_path>
free -m
uptime
ps aux
ss -tulpn
nginx -t
apachectl configtest
sshd -t
```

Denied command examples:

```text
systemctl restart
systemctl stop
kill
rm
chmod
chown
useradd
usermod
passwd
visudo edit
nginx reload
apachectl restart
sshd restart
ansible-playbook
oscap xccdf remediate
```

Failure-first rule:

```text
Supri is read-only by default.
Supri can request safe checks.
Supri must stop for restart, config edit, secret access, user change, or restore action.
```

---

## 15. Senior Reviewer Tool Grant

Role:

```text
final code reviewer, maintainability auditor, test-readiness reviewer, merge-readiness evaluator, commit-request approver
```

Allowed tools:

```yaml
senior_reviewer_tools:
  allow:
    - read_manifest
    - read_agent_artifacts
    - read_git_diff
    - read_draft_patch
    - read_final_patch
    - read_opung_notes
    - read_asep_security_review
    - read_doni_devops_review
    - read_adit_docs_review
    - read_supri_runtime_summary
    - read_runner_report
    - read_verification_report
    - read_safety_report
    - read_static_analysis_report
    - read_linter_report
    - read_coverage_report
    - retrieve_code_review_reference
    - retrieve_maintainability_reference
    - retrieve_static_analysis_reference
    - write_senior_review
    - write_revision_request
    - write_specialist_review_request
    - write_apply_approval
    - write_commit_request
```

Denied tools:

```yaml
senior_reviewer_tools:
  deny:
    - run_shell
    - apply_patch
    - run_tests
    - run_codeql
    - run_semgrep
    - run_sonar
    - run_linter
    - install_dependency
    - modify_env
    - read_secret
    - git_commit
    - git_push
    - git_merge
    - git_rebase
    - delete_file
    - deploy
```

Request-only tools:

```yaml
senior_reviewer_request_tools:
  allow:
    - request_runner_apply_patch
    - request_verification
    - request_unit_tests
    - request_coverage_report
    - request_codeql_analysis
    - request_semgrep_scan
    - request_sonarqube_quality_gate
    - request_super_linter
    - request_megalinter
    - request_duplicate_code_check
    - request_complexity_check
    - request_asep_review
    - request_doni_review
    - request_adit_review
    - request_supri_review
```

Failure-first rule:

```text
Senior Reviewer may approve, request revision, request validation, request specialist review, and request commit.
Senior Reviewer must not execute, commit, push, merge, or deploy.
```

---

## 16. Tool Grant Summary Matrix

| Agent | Read | Write artifact | Draft patch | Review | Request validation | Execute | Commit | Push |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Siwa | Yes | Yes | No | Completeness only | Yes | No | No | No |
| Opung | Scoped | Yes | Yes | No | Yes | No | No | No |
| Adit | Scoped | Yes | Docs only | Docs only | Yes | No | No | No |
| Asep | Scoped | Yes | No | Security | Yes | No | No | No |
| Doni | Scoped | Yes | No | DevOps | Yes | No | No | No |
| Supri | Scoped snapshots | Yes | No | Runtime | Read-only only | No | No | No |
| Senior Reviewer | Artifacts and diff | Yes | No | Final | Yes | No | No | No |

---

## 17. Tool Activation Policy

### 17.1 Initial Phase

```yaml
initial_tool_policy:
  safety_gate:
    enabled: true
    mode: strict

  verification_engine:
    enabled: true
    required_checks:
      - denied_path_check
      - secret_pattern_check
      - schema_validation

  runner:
    enabled: true
    apply_patch: false
    safe_validation_only: true

  commit_gate:
    enabled: false
    reason: Enable only after Runner and Verification Engine are stable.
```

### 17.2 Stable Phase

```yaml
stable_tool_policy:
  safety_gate:
    enabled: true
    mode: strict

  verification_engine:
    enabled: true
    required_checks:
      - denied_path_check
      - secret_pattern_check
      - unit_tests
      - schema_validation
      - changelog_check

  runner:
    enabled: true
    apply_patch: true

  commit_gate:
    enabled: true
    allow_local_commit: true
    allow_push: false
```

---

## 18. Recommended `tools.yaml`

```yaml
tools:
  read:
    - read_manifest
    - read_file
    - list_files
    - git_diff
    - read_artifact
    - read_runner_report
    - read_verification_report
    - read_safety_report

  write_artifact:
    - write_implementation_plan
    - write_draft_patch
    - write_test_draft_patch
    - write_patch_notes
    - write_doc_plan
    - write_docs_patch
    - write_doc_gap_report
    - write_security_review
    - write_devops_review
    - write_runtime_summary
    - write_incident_classification
    - write_senior_review
    - write_revision_request
    - write_apply_approval
    - write_commit_request

  orchestration:
    - kanban_create_task
    - kanban_split_task
    - kanban_assign_task
    - kanban_update_status
    - kanban_attach_artifact
    - message_send
    - message_read_reply
    - workflow_state_read
    - workflow_state_write
    - artifact_index_read
    - artifact_summary_write

  request_only:
    - request_runner_test
    - request_unit_test_run
    - request_docs_build
    - request_openapi_validate
    - request_asyncapi_validate
    - request_nvd_lookup
    - request_kev_lookup
    - request_dependency_audit
    - request_zap_baseline
    - request_nuclei_template_check
    - request_github_actions_lint
    - request_dockerfile_lint
    - request_compose_config_check
    - request_kubernetes_dry_run
    - request_helm_template
    - request_terraform_validate
    - request_terraform_plan
    - request_ansible_syntax_check
    - request_read_only_runtime_check
    - request_codeql_analysis
    - request_semgrep_scan
    - request_sonarqube_quality_gate

  execution_runner_only:
    - git_apply_check
    - git_apply_final_patch
    - pytest
    - python_compile_check
    - python_import_check
    - markdownlint
    - mkdocs_build
    - yaml_validate
    - docker_compose_config
    - terraform_validate
    - helm_template
    - kubectl_dry_run_client
    - ansible_syntax_check

  verification_engine_only:
    - schema_validation
    - denied_path_check
    - secret_pattern_check
    - diff_limit_check
    - branch_policy_check
    - artifact_contract_check
    - verification_report_write

  safety_gate_only:
    - unsafe_command_check
    - destructive_command_check
    - secret_access_check
    - policy_weakening_check
    - permission_escalation_check
    - push_bypass_check

  commit_gate_only:
    - local_commit
    - commit_record_write
```

---

## 19. Recommended `agent_tool_grants.yaml`

```yaml
agent_tool_grants:
  siwa:
    allow_groups:
      - read_manifest
      - orchestration
      - registry_lookup
      - workflow_state
      - artifact_summary
      - human_escalation
    deny_groups:
      - execution_runner_only
      - commit_gate_only
      - secret_access
      - source_patch_write

  opung:
    allow_tools:
      - read_manifest
      - read_file
      - list_files
      - git_diff
      - retrieve_coding_reference
      - retrieve_same_repo_context
      - write_implementation_plan
      - write_draft_patch
      - write_test_draft_patch
      - write_patch_notes
      - write_scope_request
      - write_stop_request
    request_only:
      - request_unit_test_run
      - request_import_check
      - request_senior_review
      - request_asep_review
      - request_doni_review
    deny_groups:
      - execution_runner_only
      - commit_gate_only
      - deployment
      - secret_access

  adit:
    allow_tools:
      - read_file
      - list_files
      - git_diff
      - retrieve_doc_pattern
      - classify_doc_diataxis
      - write_doc_plan
      - write_docs_patch
      - write_changelog_patch
      - write_readme_patch
      - write_doc_gap_report
      - write_style_review
    request_only:
      - request_markdownlint
      - request_vale_check
      - request_mkdocs_build
      - request_openapi_validate
      - request_asyncapi_validate
    deny_groups:
      - source_code_modify
      - execution_runner_only
      - docs_deploy
      - commit_gate_only
      - secret_access

  asep:
    allow_tools:
      - read_file
      - list_files
      - git_diff
      - retrieve_security_reference
      - retrieve_owasp_wstg
      - retrieve_owasp_asvs
      - retrieve_owasp_api_top10
      - retrieve_cwe
      - retrieve_capec
      - retrieve_attack_context
      - write_security_review
      - write_vulnerability_report
      - write_validation_request
    request_only:
      - request_nvd_lookup
      - request_kev_lookup
      - request_dependency_audit
      - request_zap_baseline
      - request_nuclei_template_check
    deny_groups:
      - offensive_security
      - execution_runner_only
      - commit_gate_only
      - source_patch_write
      - secret_access

  doni:
    allow_tools:
      - read_file
      - list_files
      - git_diff
      - retrieve_devops_reference
      - inspect_workflow_yaml
      - inspect_dockerfile
      - inspect_compose_yaml
      - inspect_kubernetes_yaml
      - inspect_helm_chart
      - inspect_terraform_files
      - inspect_ansible_playbook
      - inspect_grafana_dashboard
      - inspect_prometheus_rules
      - inspect_runbook
      - write_devops_review
      - write_validation_request
    request_only:
      - request_github_actions_lint
      - request_yaml_validation
      - request_dockerfile_lint
      - request_compose_config_check
      - request_kubernetes_dry_run
      - request_helm_template
      - request_terraform_validate
      - request_terraform_plan
      - request_ansible_syntax_check
      - request_grafana_json_validate
      - request_prometheus_rule_check
    deny_groups:
      - deployment_execute
      - infrastructure_apply
      - execution_runner_only
      - commit_gate_only
      - secret_access

  supri:
    allow_tools:
      - read_manifest
      - read_runner_report
      - read_verification_report
      - read_safety_report
      - read_error_report
      - read_log_excerpt
      - read_service_status_snapshot
      - read_resource_snapshot
      - retrieve_sysadmin_reference
      - retrieve_linux_man_page
      - retrieve_tldr_page
      - retrieve_systemd_reference
      - write_runtime_summary
      - write_incident_classification
      - write_troubleshooting_checklist
      - write_backup_restore_sop
      - write_user_management_sop
      - write_hardening_checklist
      - write_read_only_request
      - write_stop_request
    request_only:
      - request_service_status_check
      - request_journalctl_tail
      - request_disk_usage_check
      - request_memory_check
      - request_process_snapshot
      - request_network_socket_snapshot
      - request_configtest
      - request_log_redaction_check
    deny_groups:
      - runtime_mutation
      - user_management_execute
      - hardening_execute
      - backup_restore_execute
      - execution_runner_only
      - commit_gate_only
      - secret_access

  senior_reviewer:
    allow_tools:
      - read_manifest
      - read_agent_artifacts
      - read_git_diff
      - read_draft_patch
      - read_final_patch
      - read_opung_notes
      - read_asep_security_review
      - read_doni_devops_review
      - read_adit_docs_review
      - read_supri_runtime_summary
      - read_runner_report
      - read_verification_report
      - read_safety_report
      - read_static_analysis_report
      - read_linter_report
      - read_coverage_report
      - retrieve_code_review_reference
      - retrieve_maintainability_reference
      - retrieve_static_analysis_reference
      - write_senior_review
      - write_revision_request
      - write_specialist_review_request
      - write_apply_approval
      - write_commit_request
    request_only:
      - request_runner_apply_patch
      - request_verification
      - request_unit_tests
      - request_coverage_report
      - request_codeql_analysis
      - request_semgrep_scan
      - request_sonarqube_quality_gate
      - request_super_linter
      - request_megalinter
      - request_duplicate_code_check
      - request_complexity_check
      - request_asep_review
      - request_doni_review
      - request_adit_review
      - request_supri_review
    deny_groups:
      - execution_runner_only
      - commit_gate_only
      - deployment_execute
      - secret_access
```

---

## 20. Tooling Acceptance Criteria

Tooling is acceptable if:

```text
all agents have explicit allow list
all agents have explicit deny list
all execution tools are Runner-only
all verification tools are Verification Engine-only
all safety tools are Safety Gate-only
all commit tools are Commit Gate-only
all request-only tools specify executor
all risky checks specify human approval requirement
no agent can read .env
no agent can read secrets
no agent can run shell
no agent can commit
no agent can push
no agent can deploy
```

---

## 21. Final Tooling Summary

Final formula:

```text
Agent thinks and writes artifacts.
Knowledge base informs the agent.
Agent-facing tools give limited power.
Request-only tools create controlled requests.
Safety Gate blocks unsafe work.
Runner executes approved work.
Verification Engine proves the result.
Senior Reviewer decides readiness.
Commit Gate creates local commits.
Human Owner controls push, merge, release, deployment, and high-risk action.
```
