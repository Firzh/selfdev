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
| `selfdev.tools.safety_gate` | Check denied actions and denied paths |
| `selfdev.tools.verification_engine` | Run minimal deterministic verification |
| `selfdev.tools.runner` | Validate Runner requests only |
| `selfdev.tools.commit_gate` | Evaluate commit readiness only |
| `selfdev.tools.artifact_gate` | Validate artifact records |

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

## 6. Dispatch Contract

A dispatch creates:

```text
Kanban task
State file
Message assignment
```

Message assignment path:

```text
data/agent_workspace/agents/{agent_id}/inbox/{message_id}.json
```

State path:

```text
data/agent_workspace/state/{task_id}.state.json
```

Kanban path:

```text
data/agent_workspace/kanban/board.json
```

## 7. Artifact Contract

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

Valid artifact types include:

```text
orchestration_plan
implementation_plan
draft_patch
docs_plan
docs_patch
doc_gap_report
security_review
devops_review
runtime_review
senior_review
safety_report
runner_report
verification_report
commit_request
error_report
performance_warning
```

## 8. Artifact Collection Contract

Agent reply message must include:

```json
{
  "message_id": "...",
  "from_agent": "...",
  "to_agent": "siwa",
  "task_id": "...",
  "message_type": "artifact_ready",
  "status": "completed",
  "artifacts": {}
}
```

The collector must:

```text
validate reply shape
validate each artifact
register each valid artifact
attach artifact to Kanban
update state
move valid task to ready_for_senior
move incomplete task to needs_revision
```

## 9. Senior Review Contract

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

Senior Review Gate must write:

```text
data/agent_workspace/reviews/{task_id}.senior_review.md
```

It must register the review as an artifact.

## 10. Safety Rule

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

## 11. Commit Rule

Commit Gate currently evaluates readiness only.

It does not run `git commit`.

Future commit readiness must require:

```text
Senior Review approval
Safety Gate PASS
Runner report PASS
Verification Engine PASS
no blocking specialist review
manifest allows commit request
push disabled
```

## 12. Current Limitation

The system is not yet an autonomous developer.

It is currently a deterministic local workflow skeleton.
