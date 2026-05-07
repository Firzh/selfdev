# SelfDev Specification

**Status:** initial implementation specification  
**Date:** 2026-05-07

## 1. System Scope

SelfDev is a standalone local multi-agent self-development system.

SelfDev can manage one or more target systems. The first target system is `ai-rag-local`, but SelfDev must remain independent from it.

## 2. Target System Contract

Target systems are registered in:

```text
config/selfdev/targets.yaml
```

Required fields:

```yaml
targets:
  - target_id: ai-rag-local
    name: AI RAG Local
    root_path: ../ai-rag-local
    type: python_rag_app
    default_branch: master
    allowed_paths:
      - app/
      - tests/
      - docs/
      - scripts/
    denied_paths:
      - .env
      - .env.*
      - .git/
      - data/secrets/
      - credentials/
```

## 3. Agent Registry Contract

Agent registry lives in:

```text
config/selfdev/agents.yaml
```

Required agent IDs:

```text
siwa
opung
adit
asep
doni
supri
senior_reviewer
```

Each agent must define:

```yaml
agent_id:
name:
role:
model:
base_model:
temperature:
allowed_tools:
denied_tools:
responsibilities:
denied_responsibilities:
```

## 4. Core Tools Contract

Core tools:

```text
runner
verification_engine
safety_gate
commit_gate
```

Rules:

```text
Runner executes controlled approved actions.
Verification Engine validates deterministic checks.
Safety Gate blocks unsafe actions.
Commit Gate creates local commit only after all required checks pass.
No push, merge, or release is allowed.
```

## 5. Tool Registry Contract

Tool registry lives in:

```text
config/selfdev/tools.yaml
```

Tool categories:

```text
read_tools
write_artifact_tools
orchestration_tools
request_tools
execution_tools
core_tools
```

Denied for normal agents:

```text
run_shell
apply_patch
git_commit
git_push
git_merge
git_rebase
deploy
restart_service
read_secret
modify_env
delete_file
```

## 6. Routing Rules Contract

Routing rules live in:

```text
config/selfdev/routing_rules.yaml
```

Minimum routing:

```yaml
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

  high_risk:
    primary: siwa
    required_review:
      - asep
      - doni
      - senior_reviewer
    requires_human_review: true
```

## 7. Manifest Contract

Every task starts from a manifest.

Required fields:

```yaml
task_id:
target_id:
title:
task_type:
objective:
risk_level:
mode:
allowed_paths:
denied_paths:
required_outputs:
required_reviewers:
stop_conditions:
```

Allowed modes:

```text
plan
review
patch
dry_run
```

## 8. Workspace Contract

Workspace root:

```text
data/agent_workspace/
```

Required folders:

```text
kanban/
agents/
manifests/
orchestration/
plans/
patches/
docs/
reviews/
safety/
verification/
runner/
approvals/
requests/
audit/
state/
logs/
traces/
performance/
errors/
```

## 9. Message Bus Contract

Initial message bus is file-based.

```text
data/agent_workspace/agents/{agent_id}/inbox/
data/agent_workspace/agents/{agent_id}/outbox/
```

Message types:

```text
task_assignment
artifact_ready
review_request
revision_request
human_escalation
validation_request
runner_request
commit_request
```

## 10. Artifact Contract

Every artifact must include:

```text
task_id
agent_id
artifact_type
created_at
decision if applicable
evidence if making a finding
```

Every artifact path must stay inside:

```text
data/agent_workspace/
```

## 11. Test Contract

Initial tests must cover:

```text
required config exists
agent registry valid
required agents exist
tool registry valid
routing references existing agents
tool grants reference existing tools
forbidden tools are denied to normal agents
workspace folders exist
script relationship is valid
core tool modules import safely
```

## 12. Safety Contract

Safety Gate blocks:

```text
secret access
.env modification
denied path access
arbitrary shell
mass delete
push
merge
release
deployment without human approval
agent permission escalation
Commit Gate bypass
Senior Reviewer bypass
Verification Engine bypass
```

## 13. Commit Contract

Commit Gate can create a local commit only if:

```text
manifest valid
required artifacts complete
Senior Reviewer approved
Safety Gate PASS
Runner PASS
Verification Engine PASS
Asep not blocking
Doni not blocking
changed files inside allowed paths
push disabled
```
