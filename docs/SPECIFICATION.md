# SelfDev Specification

## 1. System Identity

SelfDev is a standalone local multi-agent self-development system.

It coordinates agents, tools, reviews, artifacts, and gates to support safe local development.

SelfDev can manage many target systems. `ai-rag-local` is only the first expected managed target.

## 2. Current Implementation Scope

The current implementation is deterministic and file-based.

No LLM integration is active.

No agent execution is active.

No shell execution is active.

No mutation API is active.

## 3. Current Core Modules

| Module | Purpose |
|---|---|
| `selfdev.runtime.state_manager` | Read and write task state |
| `selfdev.runtime.message_bus` | File-based agent inbox and outbox |
| `selfdev.runtime.kanban` | File-based task board |
| `selfdev.runtime.manifest_validator` | Validate task manifest |
| `selfdev.runtime.routing_gate` | Resolve manifest to routing decision |
| `selfdev.runtime.dispatcher` | Dispatch manifest to Kanban, state, and message bus |
| `selfdev.runtime.artifact_registry` | Register artifact records |
| `selfdev.runtime.artifact_collector` | Collect `artifact_ready` replies |
| `selfdev.runtime.senior_review_gate` | Write senior review decision |
| `selfdev.runtime.safety_flow` | Write Safety Gate report |
| `selfdev.runtime.verification_flow` | Write Verification Engine report |
| `selfdev.runtime.runner_flow` | Write Runner report without execution |
| `selfdev.runtime.commit_readiness_flow` | Write Commit Gate readiness report |
| `selfdev.runtime.full_dry_run` | Run deterministic full dry run |
| `selfdev.tools.safety_gate` | Check denied actions and denied paths |
| `selfdev.tools.verification_engine` | Run minimal deterministic verification |
| `selfdev.tools.runner` | Validate Runner requests only |
| `selfdev.tools.commit_gate` | Evaluate commit readiness only |
| `selfdev.tools.artifact_gate` | Validate artifact records |
| `selfdev.api.read_api` | Framework-free read-only API service |
| `selfdev.api.http_server` | Standard-library read-only HTTP API |
| `selfdev.api.action_availability` | Read-only action availability model |

## 4. Manifest Contract

A task manifest must include:

```yaml
task_id:
title:
risk_level:
mode:
task_type:
target_id:
objective:
allowed_paths:
denied_paths:
required_outputs:
required_reviews:
stop_conditions:
```

High-risk task types require:

```yaml
human_gate_required: true
```

High-risk task types:

```text
dependency_change
tool_registry_change
agent_permission_change
high_risk
critical
```

## 5. Routing Contract

Routing is deterministic.

The source of truth is:

```text
config/selfdev/routing_rules.yaml
```

Current routing examples:

| Task Type | Primary Agent | Required Review |
|---|---|---|
| documentation | adit | senior_reviewer |
| implementation | opung | senior_reviewer |
| implementation_with_security_risk | opung | asep, senior_reviewer |
| security_review | asep | senior_reviewer |
| devops_review | doni | senior_reviewer |
| runtime_issue | supri | doni, senior_reviewer |
| dependency_change | doni | asep, senior_reviewer, human required |
| critical | human_owner | automation disabled |

## 6. Artifact Contract

An artifact record must include:

```yaml
artifact_id:
task_id:
agent_id:
artifact_type:
path:
status:
metadata:
```

Artifact must:

```text
use a valid artifact type
exist inside workspace
not be empty
not escape workspace path
```

## 7. Senior Review Contract

Valid Senior Reviewer decisions:

```text
approve_for_runner
request_revision
request_specialist_review
block
human_required
```

Decision mapping:

| Decision | Next Status |
|---|---|
| approve_for_runner | ready_for_verification |
| request_revision | needs_revision |
| request_specialist_review | needs_review |
| block | blocked |
| human_required | human_required |

## 8. Safety Contract

Safety Gate checks:

```text
requested actions
changed paths
```

Denied actions include:

```text
run_shell
arbitrary_shell
git_push
git_merge
git_rebase
git_reset_hard
modify_env
read_secret
delete_file
deploy
release
```

Denied paths include:

```text
.env
.env.*
.git/
data/secrets/
```

Safety output:

```text
data/agent_workspace/safety/{task_id}.safety_report.md
```

## 9. Verification Contract

Verification Report Flow currently checks required files.

PASS status:

```text
verified
```

FAIL status:

```text
verification_failed
```

Verification output:

```text
data/agent_workspace/verification/{task_id}.verification_report.md
```

## 10. Runner Contract

Runner Request Flow currently validates the requested action only.

It does not run commands.

Accepted status:

```text
commit_ready
```

Blocked status:

```text
blocked
```

Runner output:

```text
data/agent_workspace/runner/{task_id}.runner_report.md
```

## 11. Commit Readiness Contract

Commit Gate currently evaluates readiness only.

It does not run `git commit`.

Required artifacts:

```text
senior_review
safety_report
verification_report
runner_report
```

Commit readiness output:

```text
data/agent_workspace/approvals/{task_id}.commit_request.md
```

## 12. Read-only API Contract

Current framework-free service:

```text
selfdev.api.read_api.ReadApi
```

Current CLI:

```text
scripts/selfdev/read_api.py
```

Current HTTP server:

```text
scripts/selfdev/serve_read_api.py
```

Current HTTP endpoints:

```text
GET /health
GET /summary
GET /agents
GET /tools
GET /kanban
GET /artifacts
GET /state/{task_id}
GET /actions/{task_id}
```

The HTTP API rejects:

```text
POST
PUT
DELETE
```

## 13. Action Availability Contract

Action availability is read-only.

It returns:

```json
{
  "task_id": "...",
  "exists": true,
  "status": "...",
  "available_actions": {},
  "reasons": {},
  "artifacts": {}
}
```

The UI must use this model instead of inferring action authority client-side.

## 14. Current Limitation

The system is not yet an autonomous developer.

It is currently a deterministic local workflow skeleton with read-only API support.
