# Short-Term Development Plan

## Purpose

This plan tracks the short-term implementation path for SelfDev.

SelfDev is a standalone local multi-agent self-development system. It can manage `ai-rag-local`, but it is not limited to `ai-rag-local`.

## Milestone Rule

Every 10 commits or 10 phases, documentation must be updated before adding new feature code.

Documentation update includes:

```text
README.md
CHANGELOG.md
docs/IMPLEMENTATION_STATUS.md
docs/DEV_PLAN_SHORT_TERM.md
docs/SPECIFICATION.md
docs/TEST_PLAN.md
```

## Completed Short-Term Goals

### Goal 1: Contract baseline

Status: Done

Outputs:

```text
scripts/selfdev/run_contract_tests.py
tests/selfdev/
config/selfdev/
```

### Goal 2: Runtime skeleton

Status: Done

Outputs:

```text
selfdev/runtime/state_manager.py
selfdev/runtime/message_bus.py
selfdev/runtime/kanban.py
selfdev/tools/safety_gate.py
selfdev/tools/verification_engine.py
selfdev/tools/runner.py
selfdev/tools/commit_gate.py
```

### Goal 3: Manifest validation

Status: Done

Outputs:

```text
schemas/selfdev/manifest.schema.json
selfdev/runtime/manifest_validator.py
scripts/selfdev/validate_manifest.py
examples/manifests/task-docs-001.yaml
```

### Goal 4: Routing Gate

Status: Done

Outputs:

```text
selfdev/runtime/routing_gate.py
scripts/selfdev/route_manifest.py
```

### Goal 5: Dispatch Flow

Status: Done

Outputs:

```text
selfdev/runtime/dispatcher.py
scripts/selfdev/dispatch_manifest.py
```

### Goal 6: Artifact Registry and Artifact Gate

Status: Done

Outputs:

```text
selfdev/runtime/artifact_registry.py
selfdev/tools/artifact_gate.py
scripts/selfdev/register_artifact.py
```

### Goal 7: Artifact Collection Flow

Status: Done

Outputs:

```text
selfdev/runtime/artifact_collector.py
scripts/selfdev/collect_artifacts.py
```

### Goal 8: Senior Review Gate Skeleton

Status: Done

Outputs:

```text
selfdev/runtime/senior_review_gate.py
scripts/selfdev/write_senior_review.py
```

## Next Short-Term Goals

### Goal 9: Safety Gate Integration

Status: Next

Required outputs:

```text
selfdev/runtime/safety_flow.py
scripts/selfdev/write_safety_decision.py
tests/selfdev/test_safety_flow.py
```

Expected behavior:

```text
changed paths and requested actions are checked
safety report artifact is written
safety artifact is registered
Kanban and state are updated
blocked safety result prevents Runner request
```

### Goal 10: Verification Report Flow

Status: Pending

Required outputs:

```text
selfdev/runtime/verification_flow.py
scripts/selfdev/write_verification_report.py
tests/selfdev/test_verification_flow.py
```

Expected behavior:

```text
verification checks produce report artifact
PASS moves task toward commit readiness
FAIL moves task to needs_revision or verification_failed
```

### Goal 11: Runner Request Flow

Status: Pending

Required outputs:

```text
selfdev/runtime/runner_flow.py
scripts/selfdev/request_runner_action.py
tests/selfdev/test_runner_flow.py
```

Expected behavior:

```text
Runner request is accepted only after Senior Review and Safety Gate pass
dangerous Runner actions are blocked
Runner report artifact is written
```

### Goal 12: Commit Readiness Flow

Status: Pending

Required outputs:

```text
selfdev/runtime/commit_readiness_flow.py
scripts/selfdev/evaluate_commit_readiness.py
tests/selfdev/test_commit_readiness_flow.py
```

Expected behavior:

```text
Commit Gate checks required PASS artifacts
Commit Gate does not run git commit yet
Commit readiness artifact is written
```

### Goal 13: Full Dry Run

Status: Pending

Expected flow:

```text
manifest validate
route
dispatch
collect artifact
senior review
safety decision
verification
commit readiness
```

### Goal 14: Minimal API Read-Only Layer

Status: Pending

Expected outputs:

```text
selfdev/api/
GET /health
GET /kanban
GET /agents
GET /tools
GET /artifacts
GET /state/{task_id}
```

### Goal 15: UI Read-Only Dashboard

Status: Pending

Expected output:

```text
selfdev/ui/web/
```

## Do Not Implement Yet

```text
LLM calls
automatic patch application
automatic shell execution
automatic commit
push
merge
release
deployment
desktop wrapper
real scanner execution
```
